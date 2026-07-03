from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import tensorflow as tf
from tensorflow import keras

from .config import Paths


def load_mapping(mapping_path: Path) -> Dict[str, Any]:
    with open(mapping_path, "rb") as f:
        return pickle.load(f)


def load_model(model_path: Path) -> keras.Model:
    return keras.models.load_model(model_path)


def sample_with_temperature(probs: np.ndarray, temperature: float) -> int:
    """
    probs: 1D array of probabilities (sums to ~1)
    returns sampled index.
    """
    temperature = float(temperature)
    temperature = max(0.01, temperature)

    # convert to log space
    logits = np.log(np.maximum(probs, 1e-12))
    logits = logits / temperature
    exp = np.exp(logits - np.max(logits))
    p = exp / np.sum(exp)
    return int(np.random.choice(len(p), p=p))


@dataclass(frozen=True)
class GenerationResult:
    generated_tokens: List[str]
    generated_ids: List[int]


def generate_tokens(
    seed_tokens: List[str],
    length: int,
    temperature: float = 1.0,
    sequence_length: int = 64,
    model_path: Optional[Path] = None,
    mapping_path: Optional[Path] = None,
) -> GenerationResult:
    paths = Paths()
    model_path = model_path or paths.model_path
    mapping_path = mapping_path or paths.mapping_path

    mapping = load_mapping(mapping_path)
    token_to_id = mapping["token_to_id"]
    id_to_token = mapping["id_to_token"]

    model = load_model(model_path)

    if not seed_tokens:
        # fallback: pick any token in vocab
        seed_tokens = [id_to_token[0]]

    seed_tokens = seed_tokens[-sequence_length:]
    seed_ids = [token_to_id[t] for t in seed_tokens if t in token_to_id]

    if len(seed_ids) < sequence_length:
        # pad using first id to reach sequence length
        pad_id = seed_ids[0] if seed_ids else 0
        seed_ids = [pad_id] * (sequence_length - len(seed_ids)) + seed_ids

    input_ids = np.array(seed_ids, dtype=np.int32)[None, ...]  # shape (1, seq_len)
    generated_ids: List[int] = list(seed_ids)

    for _ in range(length - sequence_length):
        preds = model.predict(input_ids, verbose=0)  # (1, vocab_size)
        next_id = sample_with_temperature(preds[0], temperature=temperature)
        generated_ids.append(next_id)

        # shift window
        input_ids = np.array(generated_ids[-sequence_length:], dtype=np.int32)[None, ...]

    generated_tokens = [id_to_token[i] for i in generated_ids]
    return GenerationResult(generated_tokens=generated_tokens, generated_ids=generated_ids)
