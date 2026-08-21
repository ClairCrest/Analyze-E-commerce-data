# E-Commerce Sales Performance Analysis

Analysis of e-commerce sales data using Python (pandas + Jupyter). Package and
environment management is handled by [uv](https://docs.astral.sh/uv/).

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```powershell
uv sync          # creates .venv and installs all dependencies from uv.lock
```

That's it — `uv sync` builds the environment, installs the `dataanalyst`
package (so it's importable in notebooks/tests), and pins everything via
`uv.lock` for reproducible installs.

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

## Data

The dataset is pulled programmatically from Kaggle — no manual download needed.

1. Create a Kaggle API token (Kaggle → *Settings* → *API* → **Create New Token**)
   and save the downloaded `kaggle.json` to `~/.kaggle/kaggle.json`.
2. Fetch the data into `data/raw/`:

   ```python
   from dataanalyst.data import fetch_dataset
   fetch_dataset()   # downloads via kagglehub, skips files already present
   ```

Data files live under `data/` and are git-ignored — only the folder structure is tracked.

## Usage

Start JupyterLab and open `notebooks/01_exploratory_analysis.ipynb`:

```powershell
uv run jupyter lab
```

Load data in a notebook or script:

```python
from dataanalyst.data import load_raw, save_processed

df = load_raw("E-Commerce Sales Analytics.csv")
save_processed(df_clean, "ecommerce_clean.parquet")
```

## Common commands

```powershell
uv sync                  # install / update the environment
uv add <package>         # add a runtime dependency
uv add --dev <package>   # add a dev dependency
uv run pytest            # run tests
uv run ruff check .      # lint
uv run jupyter lab       # launch notebooks
```
