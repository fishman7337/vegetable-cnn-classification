# Model Card

## Model Name

Vegetable Vision CNN

## Intended Use

This project is intended for academic image classification experiments on vegetable classes from the ST1504 CA1 Part A dataset. It is suitable for learning, experimentation, and reproducibility practice.

It is not intended for safety-critical food inspection, health decisions, or commercial quality assurance without additional validation.

## Training Data

The original notebook uses the provided CA1 vegetable image dataset with train, validation, and test splits. The dataset is not included in this repository.

## Model Families Explored

The original notebook compares:

- sequential CNN
- functional API CNN
- ResNet-like CNN
- inception-like CNN
- depthwise separable CNN

Each family is explored across 23px and 101px inputs, with and without augmentation.

## Reported Performance

The notebook narrative reports strong results for the 101px experiments, including a depthwise separable model test accuracy of approximately 94.2 percent and test loss of approximately 0.38. Treat these as notebook-reported results until the exact dataset and environment are reproduced.

## Limitations

- Performance depends on the original dataset split and label corrections.
- The notebook includes long-running Keras Tuner searches that may require Colab or GPU compute.
- Saved outputs in the original notebook may not reflect a fresh run in a new environment.
- The project has not been validated on external vegetable images.
- Class imbalance and mislabeled samples can affect results.

## Ethical Considerations

Use the model only in contexts where misclassification is acceptable. Clearly communicate uncertainty and avoid presenting academic validation as production assurance.

## Maintenance

Future maintainers should:

- rerun training only with documented dataset versions
- store trained model artifacts outside git
- update this card when model architecture, dataset, or reported metrics change
- keep CI and security checks passing
