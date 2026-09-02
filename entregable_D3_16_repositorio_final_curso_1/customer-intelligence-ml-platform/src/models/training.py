"""Training pipeline for churn classification."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.features.preprocessing import (
    build_preprocessing_pipeline,
    split_features_target,
)
from src.models.evaluation import evaluate_binary_classifier


@dataclass(frozen=True)
class TrainingResult:
    pipeline: Pipeline
    metrics: dict[str, float]
    train_rows: int
    test_rows: int


def build_training_pipeline(
    *,
    random_state: int = 42,
) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessing_pipeline()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=random_state,
                ),
            ),
        ]
    )


def train_model(
    dataframe: pd.DataFrame,
    *,
    test_size: float = 0.20,
    random_state: int = 42,
) -> TrainingResult:
    features, target = split_features_target(dataframe)

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )

    pipeline = build_training_pipeline(random_state=random_state)
    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    metrics = evaluate_binary_classifier(
        y_test,
        predictions,
        probabilities,
    )

    return TrainingResult(
        pipeline=pipeline,
        metrics=metrics,
        train_rows=len(X_train),
        test_rows=len(X_test),
    )


def save_training_artifacts(
    result: TrainingResult,
    model_path: str | Path,
    metrics_path: str | Path,
) -> None:
    model_path = Path(model_path)
    metrics_path = Path(metrics_path)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(result.pipeline, model_path)

    metrics_path.write_text(
        json.dumps(
            {
                "metrics": result.metrics,
                "train_rows": result.train_rows,
                "test_rows": result.test_rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
