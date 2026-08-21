"""Generate the analysis figures embedded in the README.

Run with:  uv run python scripts/generate_figures.py

Reads the cleaned dataset from data/processed/ and writes PNGs to assets/.
All aggregation logic lives in ``dataanalyst.analysis`` so figures and notebooks
stay in sync.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless: save files, don't open windows

import matplotlib.pyplot as plt
import seaborn as sns

from dataanalyst.analysis import (
    avg_revenue_by_discount,
    customer_features,
    delivery_band,
    revenue_by,
    revenue_pivot,
    segment_revenue_share,
    top_customers,
)
from dataanalyst.data import load_processed
from dataanalyst.paths import ASSETS_DIR

NUMERIC_COLS = ["quantity", "unit_price", "discount", "delivery_days", "customer_rating", "revenue"]

sns.set_theme(style="whitegrid")


def _save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(ASSETS_DIR / name, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print("wrote", ASSETS_DIR / name)


def _barh(series, title: str, xlabel: str, palette: str) -> plt.Figure:
    """Horizontal bar chart of a Series (index on the y-axis)."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = series.index.astype(str)
    sns.barplot(x=series.values, y=labels, ax=ax, palette=palette, hue=labels, legend=False)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    return fig


def main() -> None:
    ASSETS_DIR.mkdir(exist_ok=True)
    df = load_processed("ecommerce_clean.parquet")

    # 1. Revenue by product category
    _save(
        _barh(revenue_by(df, "product_category"), "Total revenue by product category",
              "Revenue", "Blues_r"),
        "revenue_by_category.png",
    )

    # 2. Revenue by category x region
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(revenue_pivot(df), annot=True, fmt=",.0f", cmap="YlGnBu", ax=ax)
    ax.set_title("Total revenue by category and region")
    _save(fig, "revenue_category_region.png")

    # 3. Average order revenue by discount band
    avg_disc = avg_revenue_by_discount(df)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(x=avg_disc.index.astype(str), y=avg_disc.values, ax=ax, palette="Reds_r",
                hue=avg_disc.index.astype(str), legend=False)
    ax.set_title("Average order revenue by discount band")
    ax.set_xlabel("Discount band")
    ax.set_ylabel("Avg revenue per order")
    _save(fig, "avg_revenue_by_discount.png")

    # 4. Correlation heatmap
    fig, ax = plt.subplots(figsize=(7, 5.5))
    sns.heatmap(df[NUMERIC_COLS].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation between numeric features")
    _save(fig, "correlation_heatmap.png")

    # 5. Customer rating by delivery band
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(x=delivery_band(df), y=df["customer_rating"], ax=ax)
    ax.set_title("Customer rating by delivery-time band")
    ax.set_xlabel("Delivery days")
    ax.set_ylabel("Customer rating")
    _save(fig, "rating_by_delivery.png")

    # 6. Top 10 customers by revenue
    top = top_customers(df)
    _save(
        _barh(top, "Top 10 customers by total revenue", "Total revenue", "Greens_r"),
        "top_customers.png",
    )

    # 7. Revenue share by customer segment (FM segmentation)
    share = segment_revenue_share(customer_features(df))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = share.index.astype(str)
    sns.barplot(x=labels, y=share.values, ax=ax, palette="viridis", hue=labels, legend=False)
    ax.set_title("Share of total revenue by customer segment")
    ax.set_xlabel("")
    ax.set_ylabel("Revenue share (%)")
    _save(fig, "revenue_by_segment.png")


if __name__ == "__main__":
    main()
