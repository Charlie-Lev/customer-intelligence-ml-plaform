"""Tests for training and prediction."""

from pathlib import Path
import pytest

from src.models import (
    load_model,
    predict_customers,
    save_training_artifacts,
    train_model,
)


def test_training_and_prediction(
    customer_dataframe,
    tmp_path: Path,
):
    result = train_model(customer_dataframe)

    assert set(result.metrics) == {
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    }

    model_path = tmp_path / "model.joblib"
    metrics_path = tmp_path / "metrics.json"

    save_training_artifacts(
        result,
        model_path,
        metrics_path,
    )

    restored = load_model(model_path)
    predictions = predict_customers(
        restored,
        customer_dataframe.head(10),
    )

    assert len(predictions) == 10
    assert predictions[
        "churn_probability"
    ].between(0, 1).all()


def test_invalid_threshold(customer_dataframe):
    result = train_model(customer_dataframe)

    with pytest.raises(ValueError):
        predict_customers(
            result.pipeline,
            customer_dataframe.head(1),
            threshold=1.2,
        )
