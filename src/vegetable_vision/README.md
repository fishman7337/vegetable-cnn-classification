# vegetable_vision

Reusable Python package for the Vegetable Vision CNN project.

- `config.py`: environment-backed path and training configuration.
- `data.py`: dataset validation, cleanup helpers, and Keras generator creation.
- `models.py`: CNN architecture builders.
- `training.py`: callbacks, class weighting, and metrics persistence.
- `train.py`: training CLI entrypoint.
- `evaluate.py`: evaluation CLI entrypoint.
- `notebooks.py`: notebook splitting helpers.

TensorFlow imports are lazy where practical so non-training tests can run quickly in CI.
