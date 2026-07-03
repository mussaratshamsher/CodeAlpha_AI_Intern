from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import tensorflow as tf
from tensorflow import keras

from .config import Paths


def load_mapping(mapping_path: Path) -> Dict[str, Any]:
    with open(mapping_path, "rb") as f:
        return pickle.load(f)


def load_training_arrays(processed_dir: Path, fallback: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    x_path = processed_dir / "X.npy"
    y_path = processed_dir / "y.npy"
    if x_path.exists() and y_path.exists():
        X = np.load(x_path)
        y = np.load(y_path)
        return X, y

    if not fallback:
        raise FileNotFoundError(f"Missing {x_path} and {y_path}")

    raise FileNotFoundError(
        "Processed arrays not found. Run src/preprocess.py first to generate X.npy/y.npy."
    )


def build_lstm_model(vocab_size: int, sequence_length: int, embedding_dim: int = 128, lstm_units: int = 256):
    model = keras.Sequential(
        [
            keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=sequence_length),
            keras.layers.LSTM(lstm_units, return_sequences=True),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(lstm_units),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(vocab_size, activation="softmax"),
        ]
    )
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def train(
    sequence_length: int = 64,
    epochs: int = 30,
    batch_size: int = 64,
    processed_dir: Path | None = None,
    mapping_path: Path | None = None,
    model_out_path: Path | None = None,
):
    paths = Paths()
    processed_dir = processed_dir or paths.processed_dir
    mapping_path = mapping_path or paths.mapping_path
    model_out_path = model_out_path or paths.model_path

    arrays_X, arrays_y = load_training_arrays(processed_dir)
    if len(arrays_X.shape) != 2:
        raise ValueError(f"Expected X to be 2D (samples, seq_len) but got shape: {arrays_X.shape}")

    # Load vocab size from mapping
    mapping = load_mapping(mapping_path)
    token_to_id = mapping["token_to_id"]
    vocab_size = int(len(token_to_id))

    # Ensure sequence_length matches
    if arrays_X.shape[1] != sequence_length:
        # If preprocessing used a different sequence length, slice or error
        sequence_length = int(arrays_X.shape[1])

    model = build_lstm_model(vocab_size=vocab_size, sequence_length=sequence_length)

    # Train/val split
    val_split = 0.2
    callbacks = [
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
        keras.callbacks.ModelCheckpoint(model_out_path.as_posix(), monitor="val_loss", save_best_only=True),
    ]

    history = model.fit(
        arrays_X,
        arrays_y,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=val_split,
        callbacks=callbacks,
        verbose=1,
    )

    model_out_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(model_out_path)

    print(f"Training complete. Saved model to: {model_out_path}")
    return history


if __name__ == "__main__":
    # Example usage:
    # python -m src.train
    train()
