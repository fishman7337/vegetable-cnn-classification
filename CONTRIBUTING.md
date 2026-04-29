# Contributing

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

Install ML dependencies only when you need to train or reproduce notebooks:

```bash
python -m pip install -e ".[ml,notebook]"
```

## Development Workflow

1. Create a focused branch.
2. Keep datasets, generated models, and credentials out of git.
3. Add or update tests for code changes.
4. Run quality checks before pushing.
5. Update documentation when behavior or setup changes.

## Checks

```bash
ruff format --check src tests scripts
ruff check src tests scripts
pytest --cov=vegetable_vision --cov-report=term-missing
bandit -q -r src scripts
pip-audit -r requirements-dev.txt --skip-editable --progress-spinner off
pip-audit -r requirements.txt --skip-editable --progress-spinner off
python scripts/split_notebook.py --check
```

## Notebook Changes

If `DELE_CA1_A.ipynb` changes, regenerate the split notebooks:

```bash
python scripts/split_notebook.py
```

## Commit Guidance

Use short, descriptive commit messages, for example:

```text
Add CI and MLOps documentation
```
