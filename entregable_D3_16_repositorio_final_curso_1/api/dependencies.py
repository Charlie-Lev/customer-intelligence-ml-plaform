from functools import lru_cache
from pathlib import Path
import joblib
import yaml
PROJECT_ROOT = Path(__file__).resolve().parents[1]
@lru_cache(maxsize=1)
def get_model():
    model_path = PROJECT_ROOT / "artifacts/models/churn_pipeline.joblib"
    return joblib.load(model_path)
@lru_cache(maxsize=1)

def get_params() -> dict:
    params_path = PROJECT_ROOT / "params.yaml"
    with params_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def get_prediction_threshold() -> float:
    return float(get_params()["prediction"]["threshold"])
