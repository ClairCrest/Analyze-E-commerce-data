"""Reusable analysis functions for the e-commerce sales data.

Keeping these here (instead of only in notebooks) means they can be unit-tested
and reused across notebooks, scripts, and reports without copy-pasting logic.
"""

from __future__ import annotations

import pandas as pd

# Shared bin definitions so notebooks and the figure script band data identically.
DISCOUNT_BINS = [-0.001, 0.1, 0.2, 0.3, 1.0]
DISCOUNT_LABELS = ["0-10%", "10-20%", "20-30%", "30%+"]
DELIVERY_BINS = [0, 3, 6, 9]  # the top edge is filled in per-dataset by delivery_band()


def kpis(df: pd.DataFrame, revenue_col: str = "revenue") -> dict[str, float]:
    """Return headline KPIs for a sales table.

    Includes order count, total revenue, and average order value (AOV).
    """
    revenue = df[revenue_col]
    return {
        "n_orders": len(df),
        "total_revenue": float(revenue.sum()),
        "avg_order_value": float(revenue.mean()),
        "median_order_value": float(revenue.median()),
    }


def revenue_by(df: pd.DataFrame, dimension: str, revenue_col: str = "revenue") -> pd.Series:
    """Total revenue grouped by ``dimension``, sorted high to low."""
    return df.groupby(dimension)[revenue_col].sum().sort_values(ascending=False)


def monthly_revenue(
    df: pd.DataFrame, date_col: str = "order_date", revenue_col: str = "revenue"
) -> pd.Series:
    """Total revenue per calendar month, indexed by month start timestamp."""
    months = pd.to_datetime(df[date_col]).dt.to_period("M").dt.to_timestamp()
    return df.groupby(months)[revenue_col].sum().sort_index()


def discount_band(df: pd.DataFrame, discount_col: str = "discount") -> pd.Series:
    """Bucket the discount column into labelled bands (``0-10%`` ... ``30%+``)."""
    return pd.cut(df[discount_col], bins=DISCOUNT_BINS, labels=DISCOUNT_LABELS)


def delivery_band(df: pd.DataFrame, delivery_col: str = "delivery_days") -> pd.Series:
    """Bucket delivery days into bands; the final band extends to the max value."""
    top = max(df[delivery_col].max(), DELIVERY_BINS[-1] + 1)
    return pd.cut(df[delivery_col], bins=[*DELIVERY_BINS, top])


def avg_revenue_by_discount(df: pd.DataFrame, revenue_col: str = "revenue") -> pd.Series:
    """Average order revenue within each discount band, in band order."""
    bands = discount_band(df)
    return df.groupby(bands, observed=True)[revenue_col].mean()


def revenue_pivot(
    df: pd.DataFrame,
    index: str = "product_category",
    columns: str = "region",
    revenue_col: str = "revenue",
) -> pd.DataFrame:
    """Revenue pivot table of ``index`` against ``columns``."""
    return df.pivot_table(index=index, columns=columns, values=revenue_col, aggfunc="sum")


def top_customers(
    df: pd.DataFrame, n: int = 10, customer_col: str = "customer_id", revenue_col: str = "revenue"
) -> pd.Series:
    """Top ``n`` customers by total revenue, highest first."""
    return df.groupby(customer_col)[revenue_col].sum().nlargest(n)
