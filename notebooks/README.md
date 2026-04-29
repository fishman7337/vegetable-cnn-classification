# Notebooks

This folder contains the original notebook and generated section notebooks derived from it.

- `DELE_CA1_A.ipynb`: exact copy of the original notebook.
- `manifest.json`: mapping from generated notebooks back to original cell ranges.
- `00_project_overview.ipynb` through `09_bibliographies.ipynb`: source-preserving section notebooks with outputs stripped.

Refresh this folder with:

```bash
python scripts/split_notebook.py
```

Verify generated notebooks are current with:

```bash
python scripts/split_notebook.py --check
```
