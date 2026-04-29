from vegetable_vision.notebooks import (
    build_notebook,
    slugify,
    split_by_numbered_top_level_sections,
    strip_cell_outputs,
)


def test_slugify() -> None:
    assert slugify("Model Training For 101px by 101px (With Data Augmentation)") == (
        "model_training_for_101px_by_101px_with_data_augmentation"
    )


def test_split_by_numbered_top_level_sections() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "source": ["# Title\n"]},
            {"cell_type": "markdown", "source": ["# 1. Importing of Libraries\n"]},
            {
                "cell_type": "code",
                "source": ["import os\n"],
                "outputs": ["x"],
                "execution_count": 1,
            },
            {"cell_type": "markdown", "source": ["# 2. Loading of Dataset\n"]},
        ]
    }

    sections = split_by_numbered_top_level_sections(notebook)

    assert [section.filename for section in sections] == [
        "00_project_overview.ipynb",
        "01_importing_of_libraries.ipynb",
        "02_loading_of_dataset.ipynb",
    ]
    assert sections[1].start_cell == 1
    assert sections[1].end_cell == 2


def test_strip_cell_outputs() -> None:
    cell = {"cell_type": "code", "source": ["1 + 1"], "outputs": ["2"], "execution_count": 7}

    stripped = strip_cell_outputs(cell)

    assert stripped["outputs"] == []
    assert stripped["execution_count"] is None
    assert cell["outputs"] == ["2"]


def test_build_notebook_preserves_metadata_and_strips_outputs() -> None:
    source = {"metadata": {"kernel": "python"}, "nbformat": 4, "nbformat_minor": 5}
    cells = [{"cell_type": "code", "source": ["1"], "outputs": ["1"], "execution_count": 1}]

    notebook = build_notebook(source, cells)

    assert notebook["metadata"] == {"kernel": "python"}
    assert notebook["cells"][0]["outputs"] == []
