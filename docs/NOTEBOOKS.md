# Notebook Guide

## Preserved Original

`DELE_CA1_A.ipynb` is the original CA1 notebook and remains at the repository root. A direct copy is also stored in `notebooks/DELE_CA1_A.ipynb`.

## Split Notebooks

The split notebooks in `notebooks/` are generated from the original notebook by numbered top-level sections. They preserve source cells while stripping execution outputs for cleaner diffs and faster review.

Generate or refresh them with:

```bash
python scripts/split_notebook.py
```

Check that generated notebooks are current:

```bash
python scripts/split_notebook.py --check
```

## Why Outputs Are Stripped

The original notebook already preserves the executed outputs. The generated notebooks are intended for reading and maintenance, so stripped outputs keep version control cleaner.

## Editing Guidance

If the academic submission needs to stay historically accurate, do not edit `DELE_CA1_A.ipynb`. Make future improvements in:

- `src/vegetable_vision/`
- `tests/`
- `docs/`
- regenerated section notebooks

If the original notebook must be updated, regenerate the split notebooks and confirm the manifest changes.
