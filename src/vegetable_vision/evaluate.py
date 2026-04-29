"""Command line evaluation entrypoint."""

from __future__ import annotations

import argparse
from pathlib import Path

from vegetable_vision.config import TrainingConfig, load_paths_from_env
from vegetable_vision.data import build_image_generators
from vegetable_vision.training import save_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a trained Vegetable Vision model.")
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=Path("reports/evaluation.json"))
    parser.add_argument("--image-size", type=int, default=101)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--color-mode", choices=["grayscale", "rgb"], default="grayscale")
    return parser.parse_args()


def main() -> None:
    try:
        from tensorflow.keras.models import load_model
    except ImportError as exc:
        raise ImportError("TensorFlow is required. Install with `pip install -e .[ml]`.") from exc

    args = parse_args()
    paths = load_paths_from_env()
    config = TrainingConfig(
        image_size=args.image_size,
        batch_size=args.batch_size,
        color_mode=args.color_mode,
        use_augmentation=False,
    )
    _, _, test_generator = build_image_generators(args.data_dir or paths.dataset_dir, config)
    model = load_model(args.model_path)
    test_loss, test_accuracy = model.evaluate(test_generator, verbose=2)
    save_json(
        {
            "model_path": str(args.model_path),
            "test_accuracy": float(test_accuracy),
            "test_loss": float(test_loss),
        },
        args.output,
    )


if __name__ == "__main__":
    main()
