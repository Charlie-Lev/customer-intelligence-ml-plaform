"""Command-line entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.data import load_csv
from src.models import (
    load_model,
    predict_customers,
    save_training_artifacts,
    train_model,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Customer churn MLE pipeline"
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    train_parser = subparsers.add_parser("train")
    train_parser.add_argument(
        "--data",
        type=Path,
        required=True,
    )
    train_parser.add_argument(
        "--model-output",
        type=Path,
        default=Path(
            "artifacts/models/churn_pipeline.joblib"
        ),
    )
    train_parser.add_argument(
        "--metrics-output",
        type=Path,
        default=Path(
            "reports/metrics/training_metrics.json"
        ),
    )
    train_parser.add_argument(
        "--test-size",
        type=float,
        default=0.20,
    )
    train_parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    predict_parser = subparsers.add_parser("predict")
    predict_parser.add_argument(
        "--data",
        type=Path,
        required=True,
    )
    predict_parser.add_argument(
        "--model",
        type=Path,
        required=True,
    )
    predict_parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "reports/predictions/customer_predictions.csv"
        ),
    )
    predict_parser.add_argument(
        "--threshold",
        type=float,
        default=0.50,
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()
    dataframe = load_csv(args.data)

    if args.command == "train":
        result = train_model(
            dataframe,
            test_size=args.test_size,
            random_state=args.seed,
        )
        save_training_artifacts(
            result,
            args.model_output,
            args.metrics_output,
        )
        print(result.metrics)
        return

    model = load_model(args.model)
    predictions = predict_customers(
        model,
        dataframe,
        threshold=args.threshold,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(args.output, index=False)
    print(args.output)


if __name__ == "__main__":
    main()
