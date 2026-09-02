"""CSV loading functions."""

from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.data.validation import validate_customer_data
from src.utils.logger import get_logger
from src.utils.paths import get_project_path


logger = get_logger(__name__)


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a generic CSV file."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported.")

    try:
        dataframe = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"Dataset is empty: {path}") from exc

    if dataframe.empty:
        raise ValueError(f"Dataset contains no records: {path}")

    return dataframe


def load_customer_data(
    path: str | Path = "data/raw/customer_churn.csv",
    *,
    validate: bool = True,
    require_target: bool = True,
    minimum_rows: int = 100,
) -> pd.DataFrame:
    """Load the canonical customer churn CSV."""
    data_path = Path(path)

    if not data_path.is_absolute():
        data_path = get_project_path(data_path)

    dataframe = load_csv(data_path)

    if validate:
        validate_customer_data(
            dataframe,
            require_target=require_target,
            minimum_rows=minimum_rows,
        )

    logger.info("Loaded customer dataset with shape %s", dataframe.shape)
    return dataframe
