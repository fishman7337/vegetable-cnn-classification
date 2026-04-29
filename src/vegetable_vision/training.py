"""Training utilities shared by scripts and notebooks."""

from __future__ import annotations

import json
from pathlib import Path


def make_callbacks(model_dir: str | Path, *, monitor: str = "val_accuracy"):
    """Create standard Keras callbacks for reproducible model training."""

    try:
        from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    except ImportError as exc:
        raise ImportError("TensorFlow is required. Install with `pip install -e .[ml]`.") from exc

    model_path = Path(model_dir)
    model_path.mkdir(parents=True, exist_ok=True)
    return [
        ModelCheckpoint(
            filepath=str(model_path / "best_model.keras"),
            monitor=monitor,
            save_best_only=True,
        ),
        EarlyStopping(monitor=monitor, patience=15, restore_best_weights=True),
        ReduceLROnPlateau(monitor=monitor, factor=0.5, patience=5, min_lr=1e-6),
    ]


def compute_class_weights(generator) -> dict[int, float]:
    """Compute balanced class weights for a Keras directory iterator."""

    try:
        import numpy as np
        from sklearn.utils.class_weight import compute_class_weight
    except ImportError as exc:
        raise ImportError("NumPy and scikit-learn are required for class weights.") from exc

    classes = np.asarray(generator.classes)
    class_indices = np.unique(classes)
    weights = compute_class_weight(class_weight="balanced", classes=class_indices, y=classes)
    return {
        int(label): float(weight) for label, weight in zip(class_indices, weights, strict=False)
    }


def save_json(payload: dict, path: str | Path) -> None:
    """Write JSON with stable formatting."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
