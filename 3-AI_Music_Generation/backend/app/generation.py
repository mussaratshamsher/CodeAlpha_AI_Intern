import os
import random
from typing import Optional, List

import pretty_midi

from .config import Paths
from .generate import generate_tokens
from .midi_utils import seed_notes_to_midi, notes_to_pretty_midi


_NOTE_TO_MIDI = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11,
}


def _midi_to_notes(midi_notes: List[int], length: int, temperature: float) -> List[int]:
    """
    Fallback placeholder when model artifacts are missing.
    """
    if not midi_notes:
        midi_notes = [60, 64, 67, 69]

    notes = list(midi_notes)
    t = max(0.1, float(temperature))

    for _ in range(len(notes), length):
        last = notes[-1]
        base_step = 2
        step_range = int(round(base_step * t))
        step_range = max(1, min(24, step_range))

        step = random.randint(-step_range, step_range)
        if t < 0.8 and abs(step) > 5:
            step = int(step / 2)

        candidate = last + step
        candidate = max(21, min(108, candidate))
        notes.append(candidate)

    return notes[:length]


def _fallback_generate_mid(seed_notes: Optional[str], length: int, temperature: float, output_path: str) -> str:
    seed_midi = seed_notes_to_midi(seed_notes)
    midi_notes = _midi_to_notes(seed_midi, length=length, temperature=temperature)
    return notes_to_pretty_midi(
        midi_pitches=midi_notes,
        out_path=output_path,
        step_seconds=0.25,
        bpm=120,
        velocity=100,
    )


def _tokens_to_midi_pitches(tokens: List[str], length: int) -> List[int]:
    midi_pitches: List[int] = []

    for tok in tokens:
        tok = tok.strip()
        if tok == "REST":
            continue

        # chord token: take first note as representative pitch
        if "." in tok:
            tok = tok.split(".")[0]

        # expected like "C4" or "D#5"
        if len(tok) < 2:
            continue

        name = tok[:-1]
        octave_part = tok[-1]
        if not octave_part.isdigit():
            continue

        octave = int(octave_part)

        note_name = name.replace("DB", "C#").replace("EB", "D#").replace("GB", "F#").replace("AB", "G#").replace("BB", "A#")
        note_name = note_name.upper()

        if note_name not in _NOTE_TO_MIDI:
            continue

        midi = (octave + 1) * 12 + _NOTE_TO_MIDI[note_name]
        midi_pitches.append(max(0, min(127, midi)))

        if len(midi_pitches) >= length:
            break

    return midi_pitches


def generate_midi(
    seed_notes: Optional[str],
    length: int,
    temperature: float,
    output_dir: str,
    filename: str = "generated.mid",
) -> str:
    """
    Uses trained LSTM when available; otherwise uses a deterministic fallback.
    """
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, filename)

    length = int(length)
    length = max(16, min(2048, length))

    paths = Paths()
    model_exists = paths.model_path.exists()
    mapping_exists = paths.mapping_path.exists()

    if not (model_exists and mapping_exists):
        return _fallback_generate_mid(seed_notes, length, temperature, output_path=out_path)

    # Generate from LSTM model (token-based). Our tokens are built from music21 pitch strings
    # like "C4", "D#5", or chord tokens "C4.E4.G4".
    seed_tokens: List[str] = []
    if seed_notes:
        # e.g. "C4 E4 G4 A4" -> ["C4","E4","G4","A4"]
        seed_tokens = [t.strip().replace(",", "") for t in seed_notes.split() if t.strip()]

    gen = generate_tokens(
        seed_tokens=seed_tokens,
        length=length,
        temperature=temperature,
        sequence_length=64,
        model_path=paths.model_path,
        mapping_path=paths.mapping_path,
    )

    midi_pitches = _tokens_to_midi_pitches(gen.generated_tokens, length=length)
    if not midi_pitches:
        return _fallback_generate_mid(seed_notes, length, temperature, output_path=out_path)

    return notes_to_pretty_midi(
        midi_pitches=midi_pitches[:length],
        out_path=out_path,
        step_seconds=0.25,
        bpm=120,
        velocity=100,
    )
