from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    project_root: Path = Path(__file__).resolve().parents[1]
    data_root: Path = project_root / "data"
    raw_midi_dir: Path = data_root / "raw_midi"
    processed_dir: Path = data_root / "processed"

    models_dir: Path = project_root / "models"
    model_path: Path = models_dir / "lstm_model.keras"
    mapping_path: Path = models_dir / "notes_mapping.pkl"

    outputs_dir: Path = project_root / "outputs"


@dataclass(frozen=True)
class GenerationConfig:
    # Model / inference defaults
    sequence_length: int = 64
    max_generated_notes: int = 256

    # Generation sampling
    temperature_min: float = 0.2
    temperature_max: float = 2.0
