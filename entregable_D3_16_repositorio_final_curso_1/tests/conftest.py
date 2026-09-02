"""Shared pytest fixtures."""

from pathlib import Path
import pandas as pd
import pytest


@pytest.fixture
def customer_dataframe() -> pd.DataFrame:
    return pd.read_csv(
        Path("data/raw/customer_churn.csv")
    )
