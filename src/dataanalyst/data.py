"""Data loading and saving helpers.

Thin wrappers around pandas so notebooks and scripts share one place to change
how data is read/written (encoding, dtypes, path conventions, etc.).
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

from .paths import PROCESSED_DIR, RAW_DIR

# Kaggle dataset backing this project.
KAGGLE_DATASET = "srisyra02/e-commerce-sales-performance-analysis"


def fetch_dataset(dataset: str = KAGGLE_DATASET, dest: Path = RAW_DIR) -> list[Path]:
    """Download a Kaggle dataset and copy its files into ``data/raw/``.

    Uses ``kagglehub`` (which reads credentials from ``~/.kaggle/kaggle.json`` or
    the ``KAGGLE_USERNAME`` / ``KAGGLE_KEY`` environment variables). Files already
    present in ``dest`` are left untouched, so it's safe to call repeatedly.

    Returns the list of file paths now available in ``dest``.
    """
    import kagglehub  # imported lazily so the rest of the package has no hard dep

    cache_dir = Path(kagglehub.dataset_download(dataset))
    dest.mkdir(parents=True, exist_ok=True)

    files: list[Path] = []
    for src in sorted(cache_dir.rglob("*")):
        if src.is_file():
            target = dest / src.name
            if not target.exists():
                shutil.copy2(src, target)
            files.append(target)
    return files


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
