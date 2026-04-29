"""Notebook splitting helpers used to keep the original submission readable."""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

NUMBERED_TOP_LEVEL_HEADING = re.compile(r"^#\s+(?P<number>\d+)\.\s+(?P<title>.+?)\s*$")
TITLE_REPLACEMENTS = {
    "Libaries": "Libraries",
    "libaries": "libraries",
}


@dataclass(frozen=True)
class NotebookSection:
    """A contiguous group of notebook cells."""

    number: int
    title: str
    filename: str
    start_cell: int
    end_cell: int
    cells: list[dict[str, Any]]


def slugify(value: str) -> str:
    """Turn a section title into a stable filename slug."""

    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "section"


def normalize_title(value: str) -> str:
    """Correct common spelling mistakes in generated section metadata."""

    normalized = value
    for source, replacement in TITLE_REPLACEMENTS.items():
        normalized = normalized.replace(source, replacement)
    return normalized


def load_notebook(path: str | Path) -> dict[str, Any]:
    """Load a notebook JSON document."""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def strip_cell_outputs(cell: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of a notebook cell without execution-only output fields."""

    stripped = copy.deepcopy(cell)
    if stripped.get("cell_type") == "code":
        stripped["outputs"] = []
        stripped["execution_count"] = None
    return stripped


def split_by_numbered_top_level_sections(notebook: dict[str, Any]) -> list[NotebookSection]:
    """Split cells at markdown headings such as ``# 4. Model Training``."""

    cells = notebook.get("cells", [])
    starts: list[tuple[int, int, str]] = []
    for index, cell in enumerate(cells):
        if cell.get("cell_type") != "markdown":
            continue
        source = "".join(cell.get("source", []))
        for line in source.splitlines():
            match = NUMBERED_TOP_LEVEL_HEADING.match(line.strip())
            if match:
                starts.append(
                    (index, int(match.group("number")), normalize_title(match.group("title")))
                )
                break

    if not starts:
        return [
            NotebookSection(
                number=0,
                title="Project Overview",
                filename="00_project_overview.ipynb",
                start_cell=0,
                end_cell=len(cells) - 1,
                cells=copy.deepcopy(cells),
            )
        ]

    sections: list[NotebookSection] = []
    first_start = starts[0][0]
    if first_start > 0:
        sections.append(
            NotebookSection(
                number=0,
                title="Project Overview",
                filename="00_project_overview.ipynb",
                start_cell=0,
                end_cell=first_start - 1,
                cells=copy.deepcopy(cells[:first_start]),
            )
        )

    for position, (start, number, title) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(cells)
        filename = f"{number:02d}_{slugify(title)}.ipynb"
        sections.append(
            NotebookSection(
                number=number,
                title=title,
                filename=filename,
                start_cell=start,
                end_cell=end - 1,
                cells=copy.deepcopy(cells[start:end]),
            )
        )
    return sections


def build_notebook(
    source_notebook: dict[str, Any],
    cells: list[dict[str, Any]],
    *,
    strip_outputs: bool = True,
) -> dict[str, Any]:
    """Create a notebook document from existing cells and source metadata."""

    output_cells = (
        [strip_cell_outputs(cell) for cell in cells] if strip_outputs else copy.deepcopy(cells)
    )
    return {
        "cells": output_cells,
        "metadata": copy.deepcopy(source_notebook.get("metadata", {})),
        "nbformat": source_notebook.get("nbformat", 4),
        "nbformat_minor": source_notebook.get("nbformat_minor", 5),
    }
