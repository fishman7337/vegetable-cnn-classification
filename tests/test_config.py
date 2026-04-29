from pathlib import Path

from vegetable_vision.config import (
    TrainingConfig,
    load_paths_from_env,
    load_training_config_from_env,
)


def test_training_config_input_shape_grayscale() -> None:
    config = TrainingConfig(image_size=23, color_mode="grayscale")

    assert config.input_shape == (23, 23, 1)


def test_training_config_input_shape_rgb() -> None:
    config = TrainingConfig(image_size=101, color_mode="rgb")

    assert config.input_shape == (101, 101, 3)


def test_load_paths_from_env_resolves_relative_paths(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("DATASET_DIR", "data/raw/Dataset (A)")
    monkeypatch.setenv("MODEL_DIR", "models")

    paths = load_paths_from_env(project_root=tmp_path)

    assert paths.dataset_dir == tmp_path / "data" / "raw" / "Dataset (A)"
    assert paths.model_dir == tmp_path / "models"


def test_load_training_config_from_env(monkeypatch) -> None:
    monkeypatch.setenv("IMAGE_SIZE", "23")
    monkeypatch.setenv("USE_AUGMENTATION", "false")

    config = load_training_config_from_env()

    assert config.image_size == 23
    assert config.use_augmentation is False
