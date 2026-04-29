# Architecture Notes

## Package Structure

`src/vegetable_vision/` contains reusable code extracted from the notebook workflow:

- `config.py`: environment-backed configuration
- `data.py`: dataset layout validation and Keras generator creation
- `models.py`: CNN architecture builders
- `training.py`: callbacks, class weights, and JSON metrics
- `train.py`: CLI training entrypoint
- `evaluate.py`: CLI evaluation entrypoint
- `notebooks.py`: notebook splitting helpers

## Design Choices

TensorFlow is imported lazily so CI can validate repository logic quickly without installing the full ML stack. Training and evaluation still require the `ml` optional dependency group.

The package uses a `src/` layout to avoid accidental imports from the repository root and to make packaging behavior closer to CI and production environments.

## Model Builders

The model builders mirror the original experimental families at a maintainable level:

- `build_sequential_cnn`
- `build_functional_cnn`
- `build_residual_cnn`
- `build_depthwise_separable_cnn`

The original notebook also includes inception-like experiments and extensive Keras Tuner searches. Those remain in the notebook for historical fidelity.

## Extension Points

Recommended future additions:

- an inference module for single-image and batch prediction
- a formal experiment tracker
- model export to ONNX or TFLite
- sample non-sensitive test images
- DVC pipeline stages if the dataset can be versioned externally
