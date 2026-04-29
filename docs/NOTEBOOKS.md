# Notebook Guide

## Preserved Original

`notebooks/DELE_CA1_A.ipynb` is the original CA1 notebook.

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

If the academic submission needs to stay historically accurate, do not edit `notebooks/DELE_CA1_A.ipynb`. Make future improvements in:

- `src/vegetable_vision/`
- `tests/`
- `docs/`
- regenerated section notebooks

If the original notebook must be updated, regenerate the split notebooks and confirm the manifest changes.
