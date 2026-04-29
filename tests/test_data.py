from pathlib import Path

import pytest

from vegetable_vision.data import (
    apply_folder_renames,
    discover_classes,
    find_empty_class_dirs,
    move_matching_files,
    validate_dataset_layout,
)


def make_dataset(root: Path) -> None:
    for split in ("train", "validation", "test"):
        for class_name in ("Beans", "Carrot"):
            class_dir = root / split / class_name
            class_dir.mkdir(parents=True)
            (class_dir / "0001.jpg").write_bytes(b"fake")


def test_validate_dataset_layout(tmp_path: Path) -> None:
    make_dataset(tmp_path)

    layout = validate_dataset_layout(tmp_path)

    assert layout["train"] == ["Beans", "Carrot"]
    assert layout["validation"] == ["Beans", "Carrot"]


def test_discover_classes_missing_split(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        discover_classes(tmp_path / "missing")


def test_find_empty_class_dirs(tmp_path: Path) -> None:
    make_dataset(tmp_path)
    empty_dir = tmp_path / "train" / "Pumpkin"
    empty_dir.mkdir()

    assert find_empty_class_dirs(tmp_path) == [empty_dir]


def test_apply_folder_renames_dry_run(tmp_path: Path) -> None:
    source = tmp_path / "Cauliflower with Broccoli"
    source.mkdir()

    changes = apply_folder_renames(
        tmp_path,
        {"Cauliflower with Broccoli": "Cauliflower and Broccoli"},
    )

    assert changes == [(source, tmp_path / "Cauliflower and Broccoli")]
    assert source.exists()


def test_move_matching_files(tmp_path: Path) -> None:
    source = tmp_path / "Beans"
    target = tmp_path / "Carrot"
    source.mkdir()
    target.mkdir()
    image = source / "0001.jpg"
    image.write_bytes(b"fake")

    changes = move_matching_files(source, target, ["0001"], dry_run=False)

    assert changes == [(image, target / "0001.jpg")]
    assert not image.exists()
    assert (target / "0001.jpg").exists()
