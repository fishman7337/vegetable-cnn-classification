"""Dataset validation, cleanup, and generator helpers."""

from __future__ import annotations

import random
import shutil
from collections.abc import Iterable
from pathlib import Path

from vegetable_vision.config import DEFAULT_SPLITS, TrainingConfig

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def set_global_determinism(seed: int) -> None:
    """Set common random seeds without importing TensorFlow unless available."""

    random.seed(seed)
    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:
        pass

    try:
        import tensorflow as tf

        tf.random.set_seed(seed)
    except ImportError:
        pass


def discover_classes(split_dir: str | Path) -> list[str]:
    """Return sorted class directory names for a dataset split."""

    split_path = Path(split_dir)
    if not split_path.exists():
        raise FileNotFoundError(f"Dataset split not found: {split_path}")

    return sorted(path.name for path in split_path.iterdir() if path.is_dir())


def validate_dataset_layout(
    dataset_dir: str | Path,
    splits: Iterable[str] = DEFAULT_SPLITS,
) -> dict[str, list[str]]:
    """Validate the expected train/validation/test folder layout."""

    dataset_path = Path(dataset_dir)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_path}")

    layout: dict[str, list[str]] = {}
    for split in splits:
        split_path = dataset_path / split
        classes = discover_classes(split_path)
        if not classes:
            raise ValueError(f"No class folders found in: {split_path}")
        layout[split] = classes
    return layout


def find_empty_class_dirs(dataset_dir: str | Path) -> list[Path]:
    """Find class folders that do not contain supported image files."""

    dataset_path = Path(dataset_dir)
    empty_dirs: list[Path] = []
    for split in DEFAULT_SPLITS:
        split_path = dataset_path / split
        if not split_path.exists():
            continue
        for class_dir in sorted(path for path in split_path.iterdir() if path.is_dir()):
            if not any(file.suffix.lower() in IMAGE_EXTENSIONS for file in class_dir.iterdir()):
                empty_dirs.append(class_dir)
    return empty_dirs


def apply_folder_renames(
    root_dir: str | Path,
    rename_map: dict[str, str],
    *,
    dry_run: bool = True,
) -> list[tuple[Path, Path]]:
    """Rename class folders according to ``rename_map`` and return planned changes."""

    root_path = Path(root_dir)
    changes: list[tuple[Path, Path]] = []
    for old_name, new_name in rename_map.items():
        source = root_path / old_name
        target = root_path / new_name
        if source.exists():
            changes.append((source, target))
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                source.rename(target)
    return changes


def move_matching_files(
    source_dir: str | Path,
    target_dir: str | Path,
    stems: Iterable[str],
    *,
    extensions: Iterable[str] = IMAGE_EXTENSIONS,
    dry_run: bool = True,
) -> list[tuple[Path, Path]]:
    """Move files whose stem matches known mislabeled examples."""

    source_path = Path(source_dir)
    target_path = Path(target_dir)
    stem_set = set(stems)
    extension_set = {extension.lower() for extension in extensions}
    changes: list[tuple[Path, Path]] = []

    if not source_path.exists():
        return changes

    for file_path in sorted(source_path.iterdir()):
        if file_path.stem in stem_set and file_path.suffix.lower() in extension_set:
            destination = target_path / file_path.name
            changes.append((file_path, destination))
            if not dry_run:
                target_path.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(destination))
    return changes


def build_image_generators(dataset_dir: str | Path, config: TrainingConfig):
    """Create Keras image generators for train, validation, and test splits."""

    try:
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
    except ImportError as exc:
        raise ImportError(
            "TensorFlow is required for generator creation. Install with `pip install -e .[ml]`."
        ) from exc

    dataset_path = Path(dataset_dir)
    augmentation_args = {}
    if config.use_augmentation:
        augmentation_args = {
            "rotation_range": 20,
            "width_shift_range": 0.1,
            "height_shift_range": 0.1,
            "zoom_range": 0.15,
            "horizontal_flip": True,
        }

    train_datagen = ImageDataGenerator(rescale=1.0 / 255, **augmentation_args)
    eval_datagen = ImageDataGenerator(rescale=1.0 / 255)

    common = {
        "target_size": (config.image_size, config.image_size),
        "color_mode": config.color_mode,
        "batch_size": config.batch_size,
        "class_mode": "categorical",
        "seed": config.seed,
    }

    train_generator = train_datagen.flow_from_directory(dataset_path / "train", **common)
    validation_generator = eval_datagen.flow_from_directory(
        dataset_path / "validation",
        shuffle=False,
        **common,
    )
    test_generator = eval_datagen.flow_from_directory(
        dataset_path / "test",
        shuffle=False,
        **common,
    )
    return train_generator, validation_generator, test_generator
