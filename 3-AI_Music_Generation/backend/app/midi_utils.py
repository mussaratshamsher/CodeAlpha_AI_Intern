from __future__ import annotations

from typing import Dict, List, Tuple, Any

import pretty_midi


_NOTE_NAME_TO_MIDI = {
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


def seed_notes_to_midi(seed_notes: str | None) -> List[int]:
    """
    Parse seed like: "C4 E4 G4 A4"
    Returns MIDI pitches (0-127) for the model seed.
    """
    if not seed_notes:
        return [60, 64, 67, 69]  # C4 E4 G4 A4

    tokens = [t.strip() for t in seed_notes.replace(",", " ").split() if t.strip()]
    out: List[int] = []

    for tok in tokens:
        tok = tok.upper()
        # Basic flat -> sharp conversion
        tok = tok.replace("DB", "C#").replace("EB", "D#").replace("GB", "F#")
        tok = tok.replace("AB", "G#").replace("BB", "A#")

        i = 0
        while i < len(tok) and not tok[i].isdigit() and tok[i] != "-":
            i += 1
        if i == 0 or i >= len(tok):
            continue

        name = tok[:i]
        octave = int(tok[i:])
        if name not in _NOTE_NAME_TO_MIDI:
            continue

        midi = (octave + 1) * 12 + _NOTE_NAME_TO_MIDI[name]
        midi = max(0, min(127, midi))
        out.append(midi)

    return out if out else [60, 64, 67, 69]


def notes_to_pretty_midi(
    midi_pitches: List[int],
    out_path: str,
    bpm: int = 120,
    velocity: int = 100,
    step_seconds: float = 0.25,
    program: int = 0,
) -> str:
    """
    Convert MIDI pitches into a simple single-track MIDI file.
    """
    pm = pretty_midi.PrettyMIDI()
    track = pretty_midi.Instrument(program=program, name="MusicGen Track")

    # step_seconds defines note duration; keep it simple
    start = 0.0
    for p in midi_pitches:
        note = pretty_midi.Note(
            velocity=int(velocity),
            pitch=int(p),
            start=start,
            end=start + float(step_seconds),
        )
        track.notes.append(note)
        start += float(step_seconds)

    pm.instruments.append(track)
    pm.write(out_path)
    return out_path
