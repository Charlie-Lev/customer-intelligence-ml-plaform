"""Tests for loading and validation."""

from pathlib import Path
import pandas as pd
import pytest

from src.data import (
    DataValidationError,
    load_customer_data,
    validate_customer_data,
)


def test_load_customer_data(customer_dataframe):
    loaded = load_customer_data(
        "data/raw/customer_churn.csv"
    )
    assert loaded.shape == customer_dataframe.shape


def test_duplicate_ids_are_rejected(customer_dataframe):
    broken = customer_dataframe.copy()
    broken.loc[1, "customer_id"] = broken.loc[0, "customer_id"]

    with pytest.raises(
        DataValidationError,
        match="duplicated customer_id",
    ):
        validate_customer_data(broken)


def test_missing_file_is_rejected(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_customer_data(tmp_path / "missing.csv")
