"""Tests for Git and DVC configuration files."""

from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_dvc_yaml_has_train_and_predict_stages() -> None:
    payload = yaml.safe_load((ROOT / "dvc.yaml").read_text(encoding="utf-8"))

    assert "train" in payload["stages"]
    assert "predict" in payload["stages"]


def test_train_stage_tracks_model_and_metrics() -> None:
    payload = yaml.safe_load((ROOT / "dvc.yaml").read_text(encoding="utf-8"))
    stage = payload["stages"]["train"]

    assert "artifacts/models/churn_pipeline.joblib" in stage["outs"]
    assert stage["metrics"][0].get(
        "reports/metrics/training_metrics.json"
    ) == {"cache": False}


def test_params_include_prediction_threshold() -> None:
    payload = yaml.safe_load((ROOT / "params.yaml").read_text(encoding="utf-8"))

    assert 0 < payload["prediction"]["threshold"] < 1


def test_devcontainer_uses_python_311() -> None:
    content = (ROOT / ".devcontainer/devcontainer.json").read_text(
        encoding="utf-8"
    )

    assert "3.11" in content
