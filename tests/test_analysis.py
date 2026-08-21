"""Tests for the analysis helpers."""

import pandas as pd

from dataanalyst.analysis import (
    avg_revenue_by_discount,
    customer_features,
    delivery_band,
    discount_band,
    kpis,
    monthly_revenue,
    revenue_by,
    revenue_pivot,
    top_customers,
)


def _sample() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_date": ["1/1/2022", "1/15/2022", "2/3/2022"],
            "region": ["West", "West", "East"],
            "revenue": [100.0, 300.0, 200.0],
        }
    )


def _orders() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "product_category": ["A", "A", "B", "B"],
            "region": ["West", "East", "West", "East"],
            "customer_id": [1, 1, 2, 3],
            "discount": [0.05, 0.15, 0.25, 0.40],
            "delivery_days": [2, 5, 8, 12],
            "revenue": [100.0, 200.0, 300.0, 400.0],
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


def test_discount_band_labels():
    bands = discount_band(_orders())
    assert list(bands.astype(str)) == ["0-10%", "10-20%", "20-30%", "30%+"]


def test_delivery_band_covers_max_value():
    bands = delivery_band(_orders())
    assert bands.notna().all()  # the 12-day order must fall inside the top band


def test_avg_revenue_by_discount_orders_bands():
    result = avg_revenue_by_discount(_orders())
    assert list(result.index.astype(str)) == ["0-10%", "10-20%", "20-30%", "30%+"]
    assert result.iloc[0] == 100.0


def test_revenue_pivot_shape():
    pivot = revenue_pivot(_orders())
    assert set(pivot.index) == {"A", "B"}
    assert set(pivot.columns) == {"West", "East"}
    assert pivot.loc["A", "West"] == 100.0


def test_top_customers_ranks_by_revenue():
    # Totals: customer 1 -> 300, customer 2 -> 300, customer 3 -> 400.
    result = top_customers(_orders(), n=2)
    assert result.index[0] == 3  # highest revenue
    assert result.iloc[0] == 400.0
    assert len(result) == 2


def test_customer_features_aggregates_per_customer():
    orders = _orders().assign(customer_rating=[4.0, 2.0, 5.0, 3.0])
    feats = customer_features(orders)
    assert list(feats.columns) == ["n_orders", "total_revenue", "avg_order_value", "avg_rating"]
    # Customer 1 placed two orders (100 + 200).
    assert feats.loc[1, "n_orders"] == 2
    assert feats.loc[1, "total_revenue"] == 300.0
    assert feats.loc[1, "avg_order_value"] == 150.0
    assert feats.loc[1, "avg_rating"] == 3.0
