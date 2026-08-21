"""Canonical project paths.

Import these instead of hardcoding relative paths so that code works the same
whether it's run from a notebook, a script, or a test.
"""

from pathlib import Path

# src/dataanalyst/paths.py -> project root is three levels up.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Committed figures embedded in the README.
ASSETS_DIR = PROJECT_ROOT / "assets"
