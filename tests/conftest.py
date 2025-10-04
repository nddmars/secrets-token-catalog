import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def repo_root():
    return Path(__file__).parents[1]
