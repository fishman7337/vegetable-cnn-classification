"""Configuration helpers for the Vegetable Vision CNN project."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_SPLITS = ("train", "validation", "test")
DEFAULT_IMAGE_SIZES = (23, 101)


def _bool_from_env(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class ProjectPaths:
    """Filesystem locations used by training, evaluation, and reporting."""

    root: Path
    dataset_dir: Path
    output_dir: Path
    model_dir: Path
    reports_dir: Path

    def resolved(self) -> ProjectPaths:
        """Return the same paths as absolute paths under ``root`` when relative."""

        def resolve(path: Path) -> Path:
            return path if path.is_absolute() else (self.root / path).resolve()

        return ProjectPaths(
            root=self.root.resolve(),
            dataset_dir=resolve(self.dataset_dir),
            output_dir=resolve(self.output_dir),
            model_dir=resolve(self.model_dir),
            reports_dir=resolve(self.reports_dir),
        )


@dataclass(frozen=True)
class TrainingConfig:
    """Training options shared by the CLI and notebook-derived code."""

    image_size: int = 101
    color_mode: str = "grayscale"
    batch_size: int = 32
    epochs: int = 100
    learning_rate: float = 0.001
    seed: int = 42
    use_augmentation: bool = True
    use_class_weighting: bool = True

    @property
    def input_shape(self) -> tuple[int, int, int]:
        channels = 1 if self.color_mode == "grayscale" else 3
        return (self.image_size, self.image_size, channels)


def load_paths_from_env(project_root: str | Path | None = None) -> ProjectPaths:
    """Load project paths from environment variables with repo-friendly defaults."""

    root = Path(project_root or os.getenv("PROJECT_ROOT", Path.cwd()))
    return ProjectPaths(
        root=root,
        dataset_dir=Path(os.getenv("DATASET_DIR", "data/raw/Dataset (A)")),
        output_dir=Path(os.getenv("OUTPUT_DIR", "artifacts")),
        model_dir=Path(os.getenv("MODEL_DIR", "models")),
        reports_dir=Path(os.getenv("REPORTS_DIR", "reports")),
    ).resolved()


def load_training_config_from_env() -> TrainingConfig:
    """Load training defaults from environment variables."""

    return TrainingConfig(
        image_size=int(os.getenv("IMAGE_SIZE", "101")),
        color_mode=os.getenv("COLOR_MODE", "grayscale"),
        batch_size=int(os.getenv("BATCH_SIZE", "32")),
        epochs=int(os.getenv("EPOCHS", "100")),
        learning_rate=float(os.getenv("LEARNING_RATE", "0.001")),
        seed=int(os.getenv("SEED", "42")),
        use_augmentation=_bool_from_env(os.getenv("USE_AUGMENTATION"), True),
        use_class_weighting=_bool_from_env(os.getenv("USE_CLASS_WEIGHTING"), True),
    )
