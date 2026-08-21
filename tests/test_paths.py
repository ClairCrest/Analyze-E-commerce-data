"""Sanity checks for project path resolution."""

from dataanalyst import paths


def test_project_root_contains_data_dir():
    assert (paths.PROJECT_ROOT / "data").is_dir()


def test_raw_dir_under_data_dir():
    assert paths.RAW_DIR.parent == paths.DATA_DIR
