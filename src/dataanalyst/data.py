"""Data loading and saving helpers.

Thin wrappers around pandas so notebooks and scripts share one place to change
how data is read/written (encoding, dtypes, path conventions, etc.).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .paths import PROCESSED_DIR, RAW_DIR


def load_raw(filename: str, **kwargs) -> pd.DataFrame:
    """Load a CSV from data/raw/."""
    return pd.read_csv(RAW_DIR / filename, **kwargs)


def load_processed(filename: str, **kwargs) -> pd.DataFrame:
    """Load a Parquet (or CSV) file from data/processed/."""
    path = PROCESSED_DIR / filename
    if path.suffix == ".parquet":
        return pd.read_parquet(path, **kwargs)
    return pd.read_csv(path, **kwargs)


def save_processed(df: pd.DataFrame, filename: str, **kwargs) -> Path:
    """Write a DataFrame to data/processed/ and return the path.

    Parquet is preferred (preserves dtypes); falls back to CSV by extension.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / filename
    if path.suffix == ".parquet":
        df.to_parquet(path, index=False, **kwargs)
    else:
        df.to_csv(path, index=False, **kwargs)
    return path
