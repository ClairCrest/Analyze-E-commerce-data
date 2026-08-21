"""Reusable analysis functions for the e-commerce sales data.

Keeping these here (instead of only in notebooks) means they can be unit-tested
and reused across notebooks and reports.
"""

from __future__ import annotations

import pandas as pd


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
    return (
        df.groupby(dimension)[revenue_col].sum().sort_values(ascending=False)
    )


def monthly_revenue(
    df: pd.DataFrame, date_col: str = "order_date", revenue_col: str = "revenue"
) -> pd.Series:
    """Total revenue per calendar month, indexed by month start timestamp."""
    months = pd.to_datetime(df[date_col]).dt.to_period("M").dt.to_timestamp()
    return df.groupby(months)[revenue_col].sum().sort_index()
