"""Generate the analysis figures embedded in the README.

Run with:  uv run python scripts/generate_figures.py

Reads the cleaned dataset from data/processed/ and writes PNGs to assets/.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: save files, don't open windows

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from dataanalyst.data import load_processed
from dataanalyst.paths import PROJECT_ROOT

ASSETS = PROJECT_ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")


def _save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(ASSETS / name, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print("wrote", ASSETS / name)


def main() -> None:
    df = load_processed("ecommerce_clean.parquet")

    # 1. Revenue by product category
    rev_cat = df.groupby("product_category")["revenue"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(x=rev_cat.values, y=rev_cat.index, ax=ax, palette="Blues_r", hue=rev_cat.index,
                legend=False)
    ax.set_title("Total revenue by product category")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("")
    _save(fig, "revenue_by_category.png")

    # 2. Revenue by category x region
    pivot = df.pivot_table(index="product_category", columns="region", values="revenue",
                           aggfunc="sum")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="YlGnBu", ax=ax)
    ax.set_title("Total revenue by category and region")
    _save(fig, "revenue_category_region.png")

    # 3. Average order revenue by discount band
    df["discount_band"] = pd.cut(df["discount"], bins=[-0.001, 0.1, 0.2, 0.3, 1.0],
                                 labels=["0-10%", "10-20%", "20-30%", "30%+"])
    avg_disc = df.groupby("discount_band", observed=True)["revenue"].mean()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(x=avg_disc.index, y=avg_disc.values, ax=ax, palette="Reds_r",
                hue=avg_disc.index, legend=False)
    ax.set_title("Average order revenue by discount band")
    ax.set_xlabel("Discount band")
    ax.set_ylabel("Avg revenue per order")
    _save(fig, "avg_revenue_by_discount.png")

    # 4. Correlation heatmap
    numeric = df[["quantity", "unit_price", "discount", "delivery_days",
                  "customer_rating", "revenue"]]
    fig, ax = plt.subplots(figsize=(7, 5.5))
    sns.heatmap(numeric.corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation between numeric features")
    _save(fig, "correlation_heatmap.png")

    # 5. Customer rating by delivery band
    df["delivery_band"] = pd.cut(df["delivery_days"], bins=[0, 3, 6, 9, df["delivery_days"].max()])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(data=df, x="delivery_band", y="customer_rating", ax=ax)
    ax.set_title("Customer rating by delivery-time band")
    ax.set_xlabel("Delivery days")
    ax.set_ylabel("Customer rating")
    _save(fig, "rating_by_delivery.png")


if __name__ == "__main__":
    main()
