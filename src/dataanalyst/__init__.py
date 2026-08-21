"""dataAnalyst — reusable helpers for the e-commerce analysis project."""

from .analysis import (
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
from .data import fetch_dataset, load_processed, load_raw, save_processed
from .paths import (
    ASSETS_DIR,
    DATA_DIR,
    PROCESSED_DIR,
    PROJECT_ROOT,
    RAW_DIR,
    REPORTS_DIR,
)

__all__ = [
    "ASSETS_DIR",
    "DATA_DIR",
    "PROCESSED_DIR",
    "PROJECT_ROOT",
    "RAW_DIR",
    "REPORTS_DIR",
    "avg_revenue_by_discount",
    "customer_features",
    "delivery_band",
    "discount_band",
    "fetch_dataset",
    "kpis",
    "load_processed",
    "load_raw",
    "monthly_revenue",
    "revenue_by",
    "revenue_pivot",
    "save_processed",
    "top_customers",
]
