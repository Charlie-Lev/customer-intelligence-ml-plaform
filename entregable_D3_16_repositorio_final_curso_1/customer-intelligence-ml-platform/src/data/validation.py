"""Validation rules for customer churn data."""

from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


REQUIRED_COLUMNS = {
    "customer_id",
    "gender",
    "age",
    "region",
    "customer_segment",
    "contract_type",
    "tenure_months",
    "monthly_fee",
    "total_spent",
    "internet_service",
    "tv_service",
    "streaming_service",
    "support_calls",
    "complaints",
    "payment_method",
    "last_payment_delay",
    "digital_usage_score",
    "marketing_score",
    "preferred_contact_hour",
    "internal_campaign_code",
    "churn",
}


class DataValidationError(ValueError):
    """Raised when a customer dataset fails validation."""


@dataclass(frozen=True)
class ValidationReport:
    """Summary of customer dataset validation."""

    rows: int
    columns: int
    duplicate_customer_ids: int
    missing_values: int
    churn_rate: float

    def to_dict(self) -> dict[str, int | float]:
        return {
            "rows": self.rows,
            "columns": self.columns,
            "duplicate_customer_ids": self.duplicate_customer_ids,
            "missing_values": self.missing_values,
            "churn_rate": self.churn_rate,
        }


def validate_customer_data(
    dataframe: pd.DataFrame,
    *,
    require_target: bool = True,
    minimum_rows: int = 100,
) -> ValidationReport:
    """Validate structure and basic business rules."""
    if not isinstance(dataframe, pd.DataFrame):
        raise DataValidationError("Input must be a pandas DataFrame.")

    errors: list[str] = []
    required = set(REQUIRED_COLUMNS)

    if not require_target:
        required.discard("churn")

    missing_columns = sorted(required - set(dataframe.columns))
    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")

    if len(dataframe) < minimum_rows:
        errors.append(
            f"Dataset contains {len(dataframe)} rows; "
            f"at least {minimum_rows} are required."
        )

    duplicate_ids = 0
    if "customer_id" in dataframe.columns:
        duplicate_ids = int(dataframe["customer_id"].duplicated().sum())
        if duplicate_ids:
            errors.append(f"Found {duplicate_ids} duplicated customer_id values.")

    churn_rate = 0.0
    if "churn" in dataframe.columns:
        invalid_target = set(dataframe["churn"].dropna().unique()) - {0, 1}
        if invalid_target:
            errors.append(f"Column 'churn' contains invalid values: {invalid_target}")

        churn_rate = float(dataframe["churn"].mean())
        if not 0.05 <= churn_rate <= 0.60:
            errors.append(
                f"Churn rate {churn_rate:.2%} is outside the expected range."
            )

    if errors:
        raise DataValidationError(
            "Dataset validation failed:\\n- " + "\\n- ".join(errors)
        )

    return ValidationReport(
        rows=int(dataframe.shape[0]),
        columns=int(dataframe.shape[1]),
        duplicate_customer_ids=duplicate_ids,
        missing_values=int(dataframe.isna().sum().sum()),
        churn_rate=churn_rate,
    )
