from __future__ import annotations

import pickle
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from music21 import converter, instrument, chord, note

from .config import Paths


def _extract_notes_from_midi(midi_path: Path) -> List:
    """
    Extract note/chord tokens from a MIDI file using music21.
    Tokens are:
      - note: e.g., 'C4'
      - chord: e.g., 'C4.E4.G4' (sorted pitch classes)
      - rest: 'REST'
    """
    try:
        score = converter.parse(str(midi_path))
    except Exception:
        return []

    parts = instrument.partitionByInstrument(score)
    notes_out: List = []

    # If there are parts, iterate each; otherwise treat whole score as one stream
    parts = parts.parts if parts else [score]

    for part in parts:
        for element in part.re.recurse():
            # NOTE
            if isinstance(element, note.Note):
                notes_out.append(str(element.pitch))
            # CHORD
            elif isinstance(element, chord.Chord):
                # Sort pitches for deterministic chord token
                pitches = sorted([p.nameWithOctave for p in element.pitches])
                notes_out.append(".".join(pitches))
            # REST
            elif isinstance(element, note.Rest):
                notes_out.append("REST")

    return notes_out


def build_vocab(tokens: List) -> Tuple[Dict, Dict]:
    """
    Build token->id and id->token vocab.
    """
    tokens = [t for t in tokens if t is not None]
    unique_tokens = sorted(set(tokens))
    token_to_id = {t: i for i, t in enumerate(unique_tokens)}
    id_to_token = {i: t for t, i in token_to_id.items()}
    return token_to_id, id_to_token


def create_sequences(ids: List[int], sequence_length: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create sliding-window sequences.
    X shape: (num_samples, sequence_length)
    y shape: (num_samples,)
    """
    X = []
    y = []
    for i in range(len(ids) - sequence_length):
        X.append(ids[i : i + sequence_length])
        y.append(ids[i + sequence_length])
    return np.array(X, dtype=np.int32), np.array(y, dtype=np.int32)


def preprocess_dataset(
    sequence_length: int = 64,
    raw_midi_dir: Path | None = None,
    processed_dir: Path | None = None,
    mapping_out_path: Path | None = None,
) -> None:
    """
    Reads MIDI files from `raw_midi_dir`, creates vocab + training sequences,
    and stores mapping artifacts into `models/`.

    For the current portfolio submission, you can run this script to build:
      - models/notes_mapping.pkl
      - processed arrays (optional)
    """
    paths = Paths()
    raw_midi_dir = raw_midi_dir or paths.raw_midi_dir
    processed_dir = processed_dir or paths.processed_dir
    mapping_out_path = mapping_out_path or paths.mapping_path

    processed_dir.mkdir(parents=True, exist_ok=True)
    mapping_out_path.parent.mkdir(parents=True, exist_ok=True)

    all_tokens: List = []

    midi_files = list(raw_midi_dir.glob("**/*.mid")) + list(raw_midi_dir.glob("**/*.midi"))
    if not midi_files:
        raise FileNotFoundError(f"No MIDI files found under: {raw_midi_dir}")

    for mp in midi_files:
        tokens = _extract_notes_from_midi(mp)
        all_tokens.extend(tokens)

    if len(all_tokens) < sequence_length + 10:
        raise RuntimeError(
            f"Not enough extracted tokens ({len(all_tokens)}). Add more MIDI files or verify parsing."
        )

    token_to_id, id_to_token = build_vocab(all_tokens)

    ids = [token_to_id[t] for t in all_tokens]
    X, y = create_sequences(ids, sequence_length=sequence_length)

    # Save mapping
    with open(mapping_out_path, "wb") as f:
        pickle.dump({"token_to_id": token_to_id, "id_to_token": id_to_token}, f)

    # Save arrays (optional but handy)
    np.save(processed_dir / "X.npy", X)
    np.save(processed_dir / "y.npy", y)

    print(f"Preprocessing done. Tokens: {len(all_tokens)} | Vocab: {len(token_to_id)}")
    print(f"Saved mapping: {mapping_out_path}")
    print(f"Saved arrays: {processed_dir / 'X.npy'} , {processed_dir / 'y.npy'}")
