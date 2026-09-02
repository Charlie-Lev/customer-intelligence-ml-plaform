"""Generate synthetic customer churn datasets for NovaTel Perú S.A.C.

The generator creates:
1. A baseline training dataset.
2. Optionally, a future dataset with distribution drift for monitoring lessons.

Usage:
    python data/raw/generate_dataset.py
    python data/raw/generate_dataset.py --rows 5000 --output data/raw/customer_churn.csv
    python data/raw/generate_dataset.py --scenario drift --output data/monitoring/customer_churn_new_data.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


REGIONS = ("Lima", "Norte", "Centro", "Sur", "Oriente")
CONTRACT_TYPES = ("Mensual", "Anual", "Bianual")
INTERNET_SERVICES = ("Fibra", "DSL", "Sin internet")
PAYMENT_METHODS = ("Tarjeta", "Débito automático", "Transferencia", "Efectivo")
CUSTOMER_SEGMENTS = ("Masivo", "Joven digital", "Familia", "Premium")


def _sigmoid(values: np.ndarray) -> np.ndarray:
    """Return the logistic sigmoid of an array."""
    return 1.0 / (1.0 + np.exp(-values))


def generate_customer_churn(
    n_rows: int = 1_000,
    random_state: int = 42,
    scenario: str = "baseline",
) -> pd.DataFrame:
    """Generate a reproducible synthetic churn dataset.

    Args:
        n_rows: Number of customer records.
        random_state: Seed used by NumPy.
        scenario: Either ``baseline`` or ``drift``.

    Returns:
        DataFrame containing customer features and the binary target ``churn``.

    Raises:
        ValueError: If n_rows is too small or scenario is unsupported.
    """
    if n_rows < 100:
        raise ValueError("n_rows must be at least 100.")
    if scenario not in {"baseline", "drift"}:
        raise ValueError("scenario must be 'baseline' or 'drift'.")

    rng = np.random.default_rng(random_state)
    drift = scenario == "drift"

    gender = rng.choice(["Femenino", "Masculino"], n_rows, p=[0.49, 0.51])
    age = np.clip(rng.normal(38 if not drift else 35, 13, n_rows).round(), 18, 82).astype(int)
    region = rng.choice(
        REGIONS,
        n_rows,
        p=[0.43, 0.20, 0.14, 0.14, 0.09] if not drift else [0.35, 0.25, 0.14, 0.15, 0.11],
    )
    contract_type = rng.choice(
        CONTRACT_TYPES,
        n_rows,
        p=[0.50, 0.34, 0.16] if not drift else [0.62, 0.27, 0.11],
    )
    tenure_months = np.clip(
        rng.gamma(shape=2.2, scale=17 if not drift else 13, size=n_rows).round(),
        1,
        120,
    ).astype(int)

    customer_segment = rng.choice(
        CUSTOMER_SEGMENTS,
        n_rows,
        p=[0.43, 0.22, 0.25, 0.10],
    )
    internet_service = rng.choice(
        INTERNET_SERVICES,
        n_rows,
        p=[0.55, 0.34, 0.11] if not drift else [0.48, 0.42, 0.10],
    )
    streaming_service = np.where(
        internet_service == "Sin internet",
        "No",
        rng.choice(["Sí", "No"], n_rows, p=[0.58, 0.42]),
    )
    tv_service = np.where(
        internet_service == "Sin internet",
        "No",
        rng.choice(["Sí", "No"], n_rows, p=[0.52, 0.48]),
    )

    base_fee = (
        42
        + np.where(internet_service == "Fibra", 52, np.where(internet_service == "DSL", 30, 0))
        + np.where(streaming_service == "Sí", 18, 0)
        + np.where(tv_service == "Sí", 15, 0)
        + np.where(customer_segment == "Premium", 35, 0)
    )
    monthly_fee = np.clip(base_fee + rng.normal(0, 9, n_rows), 35, 260).round(2)

    support_lambda = (
        1.0
        + np.where(internet_service == "DSL", 0.7, 0)
        + np.where(contract_type == "Mensual", 0.4, 0)
        + (0.4 if drift else 0)
    )
    support_calls = np.clip(rng.poisson(support_lambda), 0, 12)
    complaints = np.clip(
        rng.poisson(0.25 + 0.22 * support_calls + (0.15 if drift else 0)),
        0,
        8,
    )
    last_payment_delay = np.clip(
        rng.gamma(shape=1.35, scale=3.8 if not drift else 5.2, size=n_rows).round(),
        0,
        45,
    ).astype(int)

    digital_usage_score = np.clip(
        rng.normal(
            62
            + np.where(internet_service == "Fibra", 10, 0)
            + np.where(customer_segment == "Joven digital", 8, 0),
            15,
            n_rows,
        ),
        0,
        100,
    ).round(1)
    marketing_score = np.clip(
        rng.normal(
            52 + 0.18 * digital_usage_score + np.where(contract_type != "Mensual", 5, 0),
            13,
            n_rows,
        ),
        0,
        100,
    ).round(1)

    total_spent = np.maximum(
        monthly_fee * tenure_months * rng.normal(0.94, 0.07, n_rows),
        monthly_fee,
    ).round(2)

    # Logistic data-generating process. The intercept is calibrated to produce
    # approximately 20–25% churn in the baseline dataset.
    logit = (
        -0.60
        + 0.80 * (contract_type == "Mensual")
        - 0.55 * (contract_type == "Bianual")
        - 0.018 * tenure_months
        + 0.24 * support_calls
        + 0.48 * complaints
        + 0.055 * last_payment_delay
        - 0.015 * digital_usage_score
        - 0.007 * marketing_score
        + 0.18 * (internet_service == "DSL")
        - 0.18 * (internet_service == "Fibra")
        + 0.20 * (monthly_fee > 145)
        + (0.38 if drift else 0.0)
        + rng.normal(0, 0.34, n_rows)
    )
    churn_probability = _sigmoid(logit)
    churn = rng.binomial(1, churn_probability)

    dataframe = pd.DataFrame(
        {
            "customer_id": [f"NT-{index:06d}" for index in range(1, n_rows + 1)],
            "gender": gender,
            "age": age,
            "region": region,
            "customer_segment": customer_segment,
            "contract_type": contract_type,
            "tenure_months": tenure_months,
            "monthly_fee": monthly_fee,
            "total_spent": total_spent,
            "internet_service": internet_service,
            "tv_service": tv_service,
            "streaming_service": streaming_service,
            "support_calls": support_calls,
            "complaints": complaints,
            "payment_method": rng.choice(
                PAYMENT_METHODS,
                n_rows,
                p=[0.31, 0.31, 0.25, 0.13] if not drift else [0.26, 0.24, 0.29, 0.21],
            ),
            "last_payment_delay": last_payment_delay,
            "digital_usage_score": digital_usage_score,
            "marketing_score": marketing_score,
            # Deliberately weak/irrelevant variables for feature-selection exercises.
            "preferred_contact_hour": rng.integers(8, 21, n_rows),
            "internal_campaign_code": rng.choice(
                ["CMP-A", "CMP-B", "CMP-C", "CMP-D"], n_rows
            ),
            "churn": churn,
        }
    )

    # Introduce about 5% missingness in selected non-target columns.
    missing_columns = [
        "age",
        "region",
        "total_spent",
        "internet_service",
        "digital_usage_score",
        "marketing_score",
    ]
    for column in missing_columns:
        missing_count = max(1, int(n_rows * rng.uniform(0.025, 0.055)))
        missing_indices = rng.choice(n_rows, size=missing_count, replace=False)
        dataframe.loc[missing_indices, column] = np.nan

    # Introduce outliers in roughly 2% of records.
    outlier_count = max(1, int(n_rows * 0.02))
    outlier_indices = rng.choice(n_rows, size=outlier_count, replace=False)
    dataframe.loc[outlier_indices, "monthly_fee"] = (
        dataframe.loc[outlier_indices, "monthly_fee"] * rng.uniform(2.2, 3.5, outlier_count)
    ).round(2)
    dataframe.loc[outlier_indices, "support_calls"] = rng.integers(13, 25, outlier_count)
    dataframe.loc[outlier_indices, "last_payment_delay"] = rng.integers(46, 95, outlier_count)

    return dataframe


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=1_000, help="Number of records.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument(
        "--scenario",
        choices=["baseline", "drift"],
        default="baseline",
        help="Data-generating scenario.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "customer_churn.csv",
        help="Destination CSV path.",
    )
    return parser.parse_args()


def main() -> None:
    """Generate and save the requested dataset."""
    args = parse_args()
    dataset = generate_customer_churn(
        n_rows=args.rows,
        random_state=args.seed,
        scenario=args.scenario,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(args.output, index=False, encoding="utf-8-sig")

    churn_rate = dataset["churn"].mean()
    print(f"Dataset saved to: {args.output}")
    print(f"Rows: {len(dataset):,}")
    print(f"Columns: {dataset.shape[1]}")
    print(f"Churn rate: {churn_rate:.2%}")


if __name__ == "__main__":
    main()
