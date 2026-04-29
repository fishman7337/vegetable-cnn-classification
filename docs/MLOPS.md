# MLOps Guide

## Reproducibility

Use `.env.example` as the local configuration template. The key reproducibility controls are:

- `DATASET_DIR`
- `IMAGE_SIZE`
- `COLOR_MODE`
- `BATCH_SIZE`
- `EPOCHS`
- `LEARNING_RATE`
- `SEED`
- `USE_AUGMENTATION`
- `USE_CLASS_WEIGHTING`

The package exposes `TrainingConfig` and `ProjectPaths` so notebook code and scripts can share the same configuration shape.

## Experiment Tracking

For lightweight local tracking:

- save metrics to `reports/`
- save generated figures to `reports/figures/`
- save model artifacts to `models/`
- document notable runs in the model card or an experiment log

For larger work, add MLflow or Weights & Biases and keep credentials in environment variables rather than committed files.

## Artifact Policy

Git should store source, tests, configuration, and documentation. Git should not store:

- raw datasets
- processed image folders
- model checkpoints
- Keras tuner directories
- generated weights
- run caches

The `.gitignore` file keeps these outputs local by default.

## Validation Gates

Local validation:

```bash
ruff format --check src tests scripts
ruff check src tests scripts
pytest --cov=vegetable_vision --cov-report=term-missing
bandit -q -r src scripts
pip-audit -r requirements-dev.txt --skip-editable --progress-spinner off
pip-audit -r requirements.txt --skip-editable --progress-spinner off
python scripts/split_notebook.py --check
```

CI validation:

- Python package installation
- Ruff formatting and linting
- pytest
- coverage reporting
- Bandit static security scan
- pip-audit dependency scan
- notebook split integrity check
- CodeQL analysis

## Deployment Notes

The original assignment focuses on model training and evaluation rather than production serving. If this project is extended, recommended next steps are:

- export the selected Keras model to a versioned artifact store
- add a small inference module with input validation
- add batch prediction tests using sample non-sensitive images
- add model monitoring for drift and confidence distribution
- document expected hardware and latency constraints
