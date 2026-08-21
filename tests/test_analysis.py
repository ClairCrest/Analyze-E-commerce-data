"""Tests for the analysis helpers."""

import pandas as pd

from dataanalyst.analysis import kpis, monthly_revenue, revenue_by


def _sample() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_date": ["1/1/2022", "1/15/2022", "2/3/2022"],
            "region": ["West", "West", "East"],
            "revenue": [100.0, 300.0, 200.0],
        }
    )


def test_kpis_basic():
    result = kpis(_sample())
    assert result["n_orders"] == 3
    assert result["total_revenue"] == 600.0
    assert result["avg_order_value"] == 200.0


def test_revenue_by_sorts_descending():
    result = revenue_by(_sample(), "region")
    assert list(result.index) == ["West", "East"]
    assert result.loc["West"] == 400.0


def test_monthly_revenue_groups_by_month():
    result = monthly_revenue(_sample())
    assert len(result) == 2  # January and February
    assert result.iloc[0] == 400.0  # two January orders
    assert result.iloc[1] == 200.0  # one February order
