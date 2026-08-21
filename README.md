# dataAnalyst

A Python data-analysis project (pandas + Jupyter).

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .              # makes `dataanalyst` importable in notebooks/tests
```

## Structure

```
data/
  raw/         # original, immutable inputs (git-ignored)
  processed/   # cleaned / derived data (git-ignored)
  external/    # third-party source data (git-ignored)
notebooks/     # Jupyter notebooks, numbered by stage (01_, 02_, ...)
src/dataanalyst/  # reusable code (paths, loaders, transforms)
reports/
  figures/     # exported charts (git-ignored)
tests/         # pytest tests
```

## Usage

Start JupyterLab:

```powershell
jupyter lab
```

Load data in a notebook or script:

```python
from dataanalyst.data import load_raw, save_processed

df = load_raw("sales.csv")
save_processed(df_clean, "sales_clean.parquet")
```

## Testing

```powershell
pytest
ruff check .
```
