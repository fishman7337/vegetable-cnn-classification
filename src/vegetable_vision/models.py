"""Reusable CNN model builders derived from the original notebook experiments."""

from __future__ import annotations


def _keras():
    try:
        from tensorflow.keras import Model, Sequential
        from tensorflow.keras.layers import (
            Activation,
            Add,
            BatchNormalization,
            Concatenate,
            Conv2D,
            Dense,
            Dropout,
            Flatten,
            Input,
            MaxPooling2D,
            SeparableConv2D,
        )
        from tensorflow.keras.optimizers import Adam
    except ImportError as exc:
        raise ImportError("TensorFlow is required. Install with `pip install -e .[ml]`.") from exc

    return {
        "Activation": Activation,
        "Add": Add,
        "Adam": Adam,
        "BatchNormalization": BatchNormalization,
        "Concatenate": Concatenate,
        "Conv2D": Conv2D,
        "Dense": Dense,
        "Dropout": Dropout,
        "Flatten": Flatten,
        "Input": Input,
        "MaxPooling2D": MaxPooling2D,
        "Model": Model,
        "SeparableConv2D": SeparableConv2D,
        "Sequential": Sequential,
    }


def _compile(model, learning_rate: float):
    Adam = _keras()["Adam"]
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def build_sequential_cnn(
    input_shape: tuple[int, int, int],
    num_classes: int,
    *,
    learning_rate: float = 0.001,
    dropout: float = 0.35,
):
    """Build a compact sequential CNN baseline."""

    k = _keras()
    model = k["Sequential"](
        [
            k["Input"](shape=input_shape),
            k["Conv2D"](32, (3, 3), activation="relu", padding="same"),
            k["BatchNormalization"](),
            k["MaxPooling2D"](),
            k["Conv2D"](64, (3, 3), activation="relu", padding="same"),
            k["BatchNormalization"](),
            k["MaxPooling2D"](),
            k["Conv2D"](128, (3, 3), activation="relu", padding="same"),
            k["BatchNormalization"](),
            k["MaxPooling2D"](),
            k["Flatten"](),
            k["Dense"](128, activation="relu"),
            k["Dropout"](dropout),
            k["Dense"](num_classes, activation="softmax"),
        ]
    )
    return _compile(model, learning_rate)


def build_functional_cnn(
    input_shape: tuple[int, int, int],
    num_classes: int,
    *,
    learning_rate: float = 0.001,
    dropout: float = 0.35,
):
    """Build the functional CNN family used for the best-model comparison."""

    k = _keras()
    inputs = k["Input"](shape=input_shape)
    x = k["Conv2D"](32, (3, 3), padding="same", activation="relu")(inputs)
    x = k["BatchNormalization"]()(x)
    x = k["MaxPooling2D"]()(x)
    x = k["Conv2D"](64, (3, 3), padding="same", activation="relu")(x)
    x = k["BatchNormalization"]()(x)
    x = k["MaxPooling2D"]()(x)
    x = k["Conv2D"](128, (3, 3), padding="same", activation="relu")(x)
    x = k["BatchNormalization"]()(x)
    x = k["MaxPooling2D"]()(x)
    x = k["Flatten"]()(x)
    x = k["Dense"](128, activation="relu")(x)
    x = k["Dropout"](dropout)(x)
    outputs = k["Dense"](num_classes, activation="softmax")(x)
    return _compile(k["Model"](inputs, outputs, name="functional_cnn"), learning_rate)


def build_residual_cnn(
    input_shape: tuple[int, int, int],
    num_classes: int,
    *,
    learning_rate: float = 0.001,
    dropout: float = 0.35,
):
    """Build a small residual CNN variant."""

    k = _keras()
    inputs = k["Input"](shape=input_shape)
    x = k["Conv2D"](32, (3, 3), padding="same", activation="relu")(inputs)
    x = k["BatchNormalization"]()(x)

    shortcut = k["Conv2D"](64, (1, 1), padding="same")(x)
    y = k["Conv2D"](64, (3, 3), padding="same", activation="relu")(x)
    y = k["BatchNormalization"]()(y)
    y = k["Conv2D"](64, (3, 3), padding="same")(y)
    x = k["Activation"]("relu")(k["Add"]()([shortcut, y]))
    x = k["MaxPooling2D"]()(x)

    x = k["Conv2D"](128, (3, 3), padding="same", activation="relu")(x)
    x = k["BatchNormalization"]()(x)
    x = k["MaxPooling2D"]()(x)
    x = k["Flatten"]()(x)
    x = k["Dense"](128, activation="relu")(x)
    x = k["Dropout"](dropout)(x)
    outputs = k["Dense"](num_classes, activation="softmax")(x)
    return _compile(k["Model"](inputs, outputs, name="residual_cnn"), learning_rate)


def build_depthwise_separable_cnn(
    input_shape: tuple[int, int, int],
    num_classes: int,
    *,
    learning_rate: float = 0.001,
    dropout: float = 0.35,
):
    """Build a depthwise separable CNN for efficient high-accuracy training."""

    k = _keras()
    inputs = k["Input"](shape=input_shape)
    x = inputs
    for filters in (32, 64, 128):
        x = k["SeparableConv2D"](filters, (3, 3), padding="same", activation="relu")(x)
        x = k["BatchNormalization"]()(x)
        x = k["MaxPooling2D"]()(x)
    x = k["Flatten"]()(x)
    x = k["Dense"](128, activation="relu")(x)
    x = k["Dropout"](dropout)(x)
    outputs = k["Dense"](num_classes, activation="softmax")(x)
    return _compile(k["Model"](inputs, outputs, name="depthwise_separable_cnn"), learning_rate)
