# Vegetable Vision CNN

An MLOps-ready convolutional neural network project for vegetable image classification, rebuilt from the original ST1504 Deep Learning CA1 notebook into a cleaner repository structure with reusable Python modules, tests, security checks, and documentation.

The original notebook remains preserved as `DELE_CA1_A.ipynb` and is also copied directly to `notebooks/DELE_CA1_A.ipynb`. Source-preserving split notebooks are generated under `notebooks/` to make review and maintenance easier.

## Academic Context

This project was completed under Singapore Polytechnic, School of Computing, Diploma in Applied AI & Analytics, for the module Deep Learning (ST1504), CA1 Part A. It was done by Goh Kun Ming, DAAA student, in AY25/26 Year 2 Semester 1. Lecturer: Gerald Chua Deng Xiang.

## Project Goals

- Classify vegetable images using CNN architectures implemented with TensorFlow/Keras.
- Compare 23px and 101px image inputs, with and without data augmentation.
- Evaluate sequential, functional, residual, inception-like, and depthwise separable CNN designs.
- Preserve the original notebook submission while adding production-style project hygiene.
- Add repeatable setup, CI, pytest, security scanning, and MLOps documentation.

## Repository Layout

```text
.
|-- DELE_CA1_A.ipynb                 # Original notebook, kept intact
|-- notebooks/                       # Split notebook sections and manifest
|-- src/vegetable_vision/            # Reusable package code
|-- tests/                           # Pytest suite for config, data, and notebook tooling
|-- data/                            # Local dataset placeholders, ignored by git
|-- models/                          # Local model artifact placeholders, ignored by git
|-- reports/                         # Metrics and generated reports
|-- docs/                            # MLOps, dataset, model, and project documentation
|-- .github/workflows/               # CI, security, and CodeQL workflows
|-- .env.example                     # Local environment template
|-- pyproject.toml                   # Package, tooling, and test configuration
|-- requirements.txt                 # Runtime reproduction environment
`-- requirements-dev.txt             # Developer/test tooling
```

## Quick Start

Create and activate a virtual environment, then install the developer tooling:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

For full notebook reproduction and model training, install the ML extras:

```bash
python -m pip install -e ".[ml,notebook]"
```

Copy `.env.example` to `.env` and update `DATASET_DIR` to point at the assessment dataset.

## Dataset Layout

The training code expects this structure:

```text
DATASET_DIR/
  train/<class_name>/*.jpg
  validation/<class_name>/*.jpg
  test/<class_name>/*.jpg
```

The image dataset is not committed to git. Place it under `data/raw/Dataset (A)` locally or set `DATASET_DIR` in `.env`.

## Notebook Workflow

The monolithic notebook has been split by numbered top-level sections:

```bash
python scripts/split_notebook.py
```

The split notebooks intentionally strip execution outputs to keep diffs readable. The original notebook remains unchanged at the repository root and is copied to `notebooks/DELE_CA1_A.ipynb`.

To verify the split notebooks are current:

```bash
python scripts/split_notebook.py --check
```

## Training

Example local training command:

```bash
vegetable-vision-train \
  --data-dir "data/raw/Dataset (A)" \
  --model depthwise \
  --image-size 101 \
  --epochs 100
```

Evaluate a saved model:

```bash
vegetable-vision-evaluate \
  --model-path models/depthwise_101px.keras \
  --data-dir "data/raw/Dataset (A)" \
  --output reports/evaluation.json
```

## Quality Gates

Run the same local checks used in CI:

```bash
ruff format --check src tests scripts
ruff check src tests scripts
pytest --cov=vegetable_vision --cov-report=term-missing
bandit -q -r src scripts
pip-audit -r requirements-dev.txt --skip-editable --progress-spinner off
pip-audit -r requirements.txt --skip-editable --progress-spinner off
python scripts/split_notebook.py --check
```

GitHub Actions also runs pytest, Ruff, Bandit, dependency auditing, notebook integrity checks, and CodeQL analysis.

## Documentation

- [Project context](docs/PROJECT_CONTEXT.md)
- [Dataset documentation](docs/DATASET.md)
- [MLOps guide](docs/MLOPS.md)
- [Model card](docs/MODEL_CARD.md)
- [Notebook guide](docs/NOTEBOOKS.md)
- [Architecture notes](docs/ARCHITECTURE.md)
- [CI and security](docs/CI_SECURITY.md)

## Status

This repository is an academic deep learning project that has been reorganized for maintainability. The code and tests validate repository tooling and reusable helpers, but full model reproduction still requires the original dataset and suitable GPU/Colab compute.
