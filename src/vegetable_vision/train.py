"""Command line training entrypoint."""

from __future__ import annotations

import argparse
from pathlib import Path

from vegetable_vision.config import TrainingConfig, load_paths_from_env
from vegetable_vision.data import (
    build_image_generators,
    set_global_determinism,
    validate_dataset_layout,
)
from vegetable_vision.models import (
    build_depthwise_separable_cnn,
    build_functional_cnn,
    build_residual_cnn,
    build_sequential_cnn,
)
from vegetable_vision.training import compute_class_weights, make_callbacks, save_json

MODEL_BUILDERS = {
    "sequential": build_sequential_cnn,
    "functional": build_functional_cnn,
    "residual": build_residual_cnn,
    "depthwise": build_depthwise_separable_cnn,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a Vegetable Vision CNN model.")
    parser.add_argument("--data-dir", type=Path, default=None, help="Dataset root directory.")
    parser.add_argument("--model-dir", type=Path, default=None, help="Directory for saved models.")
    parser.add_argument("--model", choices=sorted(MODEL_BUILDERS), default="depthwise")
    parser.add_argument("--image-size", type=int, default=101)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--color-mode", choices=["grayscale", "rgb"], default="grayscale")
    parser.add_argument("--no-augmentation", action="store_true")
    parser.add_argument("--no-class-weighting", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = load_paths_from_env()
    dataset_dir = args.data_dir or paths.dataset_dir
    model_dir = args.model_dir or paths.model_dir

    config = TrainingConfig(
        image_size=args.image_size,
        color_mode=args.color_mode,
        batch_size=args.batch_size,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        seed=args.seed,
        use_augmentation=not args.no_augmentation,
        use_class_weighting=not args.no_class_weighting,
    )

    set_global_determinism(config.seed)
    layout = validate_dataset_layout(dataset_dir)
    train_generator, validation_generator, test_generator = build_image_generators(
        dataset_dir, config
    )

    builder = MODEL_BUILDERS[args.model]
    model = builder(
        config.input_shape,
        num_classes=len(layout["train"]),
        learning_rate=config.learning_rate,
    )
    class_weight = compute_class_weights(train_generator) if config.use_class_weighting else None

    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=config.epochs,
        callbacks=make_callbacks(model_dir),
        class_weight=class_weight,
    )
    test_loss, test_accuracy = model.evaluate(test_generator, verbose=2)

    model_dir.mkdir(parents=True, exist_ok=True)
    model.save(model_dir / f"{args.model}_{config.image_size}px.keras")
    save_json(
        {
            "model": args.model,
            "image_size": config.image_size,
            "test_accuracy": float(test_accuracy),
            "test_loss": float(test_loss),
            "history": history.history,
        },
        model_dir / "metrics.json",
    )


if __name__ == "__main__":
    main()
