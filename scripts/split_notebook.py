"""Split the original CA1 notebook into section notebooks."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from vegetable_vision.notebooks import (  # noqa: E402
    build_notebook,
    load_notebook,
    split_by_numbered_top_level_sections,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("DELE_CA1_A.ipynb"))
    parser.add_argument("--output-dir", type=Path, default=Path("notebooks"))
    parser.add_argument("--keep-outputs", action="store_true")
    parser.add_argument("--check", action="store_true", help="Verify generated files are current.")
    return parser.parse_args()


def expected_payload(
    args: argparse.Namespace,
) -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    source_path = args.source
    source_notebook = load_notebook(source_path)
    sections = split_by_numbered_top_level_sections(source_notebook)
    strip_outputs = not args.keep_outputs

    manifest = {
        "source_notebook": str(source_path),
        "strip_outputs": strip_outputs,
        "section_count": len(sections),
        "source_cell_count": len(source_notebook.get("cells", [])),
        "sections": [
            {
                "filename": section.filename,
                "title": section.title,
                "original_start_cell": section.start_cell,
                "original_end_cell": section.end_cell,
                "cell_count": len(section.cells),
            }
            for section in sections
        ],
    }
    notebooks = {
        section.filename: build_notebook(
            source_notebook,
            section.cells,
            strip_outputs=strip_outputs,
        )
        for section in sections
    }
    return manifest, notebooks


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    source_path = args.source
    output_dir = args.output_dir
    manifest, notebooks = expected_payload(args)

    if args.check:
        expected_paths = {output_dir / filename: payload for filename, payload in notebooks.items()}
        expected_paths[output_dir / "manifest.json"] = manifest
        missing_or_changed = []
        for path, payload in expected_paths.items():
            expected = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                missing_or_changed.append(str(path))
        original_copy = output_dir / source_path.name
        if not original_copy.exists() or original_copy.read_bytes() != source_path.read_bytes():
            missing_or_changed.append(str(original_copy))
        if missing_or_changed:
            raise SystemExit("Notebook split output is stale: " + ", ".join(missing_or_changed))
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, output_dir / source_path.name)

    expected_filenames = set(notebooks)
    for existing_notebook in output_dir.glob("*.ipynb"):
        if (
            existing_notebook.name not in expected_filenames
            and existing_notebook.name != source_path.name
        ):
            existing_notebook.unlink()

    for filename, notebook in notebooks.items():
        write_json(output_dir / filename, notebook)
    write_json(output_dir / "manifest.json", manifest)


if __name__ == "__main__":
    main()
