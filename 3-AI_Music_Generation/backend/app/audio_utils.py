from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional


def _which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)


def midi_to_wav_with_fluidsynth(
    midi_path: str | Path,
    wav_path: str | Path,
    *,
    soundfont_path: str | Path,
    sample_rate: int = 44100,
) -> str:
    """Convert MIDI->WAV using FluidSynth CLI.

    Requires:
      - fluidsynth binary available
      - a usable SoundFont file (e.g. .sf2)
    """
    midi_path = str(midi_path)
    wav_path = str(wav_path)
    soundfont_path = str(soundfont_path)

    if not _which("fluidsynth"):
        raise RuntimeError("FluidSynth (fluidsynth) not found in PATH.")
    if not os.path.exists(soundfont_path):
        raise RuntimeError(f"SoundFont not found: {soundfont_path}")

    # -ni: realtime interactive? keep defaults; we want batch.
    # Output WAV file.
    # Example:
    # fluidsynth -ni -F output.wav soundfont.sf2 input.mid
    cmd = [
        "fluidsynth",
        "-ni",
        "-F",
        wav_path,
        "-r",
        str(sample_rate),
        soundfont_path,
        midi_path,
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"FluidSynth failed (code={proc.returncode}).\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )

    if not os.path.exists(wav_path):
        raise RuntimeError("FluidSynth did not create output WAV file.")

    return wav_path


def midi_to_wav_fallback(
    midi_path: str | Path,
    wav_path: str | Path,
) -> str:
    """Best-effort fallback MIDI->WAV.

    If FluidSynth isn't available, we generate a simple monophonic WAV using
    `pretty_midi` (MIDI parsing) and `wave` + `math`.

    This is not a realistic instrument render, but it guarantees that:
    - /generate does not fail
    - the browser can play something via HTML5 <audio>

    For production-quality audio, use FluidSynth + a SoundFont.
    """

    import wave
    import math

    from pretty_midi import PrettyMIDI

    midi_path = Path(midi_path)
    wav_path = Path(wav_path)

    pm = PrettyMIDI(str(midi_path))

    # Mix all notes from all tracks into a simple synthesis.
    notes = []
    for inst in pm.instruments:
        for n in inst.notes:
            # PrettyMIDI gives seconds in n.start / n.end
            notes.append((n.start, n.end, int(n.pitch), int(n.velocity)))

    if not notes:
        # Create a short silent wav so frontend still works.
        sr = 44100
        duration = 0.25
        nframes = int(sr * duration)
        with wave.open(str(wav_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(b"\x00\x00" * nframes)
        return str(wav_path)

    sr = 44100
    end_time = max(e for _, e, _, _ in notes)
    duration = max(0.1, float(end_time) + 0.05)
    nframes = int(sr * duration)

    # mono buffer
    samples = [0.0] * nframes

    def midi_to_freq(m: int) -> float:
        return 440.0 * (2.0 ** ((m - 69) / 12.0))

    # simple square/triangle-ish synthesis (we'll do sine + envelope)
    for start, end, pitch, velocity in notes:
        start_i = max(0, int(start * sr))
        end_i = min(nframes, int(end * sr))
        if end_i <= start_i:
            continue

        freq = midi_to_freq(pitch)
        vel = max(1, min(127, velocity)) / 127.0

        for i in range(start_i, end_i):
            t = i / sr
            # envelope: quick attack + release
            rel = (i - start_i) / max(1, (end_i - start_i))
            env = 1.0
            attack = 0.01
            if t - start < attack:
                env = (t - start) / attack
            # fade out near end
            if end - t < 0.02:
                env *= max(0.0, (end - t) / 0.02)

            # sum waveform
            samples[i] += env * vel * math.sin(2.0 * math.pi * freq * t)

    # Normalize
    peak = max(abs(x) for x in samples) or 1.0
    norm = 0.9 / peak

    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        frames = bytearray()
        for x in samples:
            v = int(max(-1.0, min(1.0, x * norm)) * 32767)
            frames += int(v).to_bytes(2, byteorder="little", signed=True)
        wf.writeframes(frames)

    return str(wav_path)



def ensure_wav_from_midi(
    midi_path: str | Path,
    *,
    out_dir: str | Path,
    output_basename: str,
    sample_rate: int = 44100,
    soundfont_path: str | Path | None = None,
) -> str:
    """Create a WAV file from a MIDI input.

    Returns absolute wav path.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    midi_path = Path(midi_path)
    wav_path = out_dir / f"{output_basename}.wav"

    if wav_path.exists():
        return str(wav_path)

    sf = soundfont_path or os.environ.get("SOUND_FONT_PATH")
    if sf:
        try:
            return midi_to_wav_with_fluidsynth(
                midi_path,
                wav_path,
                soundfont_path=sf,
                sample_rate=sample_rate,
            )
        except Exception:
            # If fluidsynth exists but fails for any reason, re-raise.
            # If fluidsynth missing, try fallback (which currently errors fast).
            if _which("fluidsynth"):
                raise

    return midi_to_wav_fallback(midi_path, wav_path)

