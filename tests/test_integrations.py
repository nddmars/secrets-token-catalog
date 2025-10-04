import shutil
import subprocess
from pathlib import Path
import pytest


def is_tool(name):
    return shutil.which(name) is not None


def test_gitleaks_wrapper_runs_or_skips(tmp_path):
    # Skip if gitleaks isn't installed
    if not is_tool("gitleaks"):
        pytest.skip("gitleaks not installed; skipping integration test")
    repo_root = Path(__file__).parents[1]
    res = subprocess.run([str(repo_root / "tools" / "scan_with_gitleaks.py"), str(repo_root)], capture_output=True, text=True)
    assert res.returncode in (0,1,2)


def test_trufflehog_wrapper_runs_or_skips(tmp_path):
    if not is_tool("trufflehog"):
        pytest.skip("trufflehog not installed; skipping integration test")
    repo_root = Path(__file__).parents[1]
    res = subprocess.run([str(repo_root / "tools" / "scan_with_trufflehog.py"), str(repo_root)], capture_output=True, text=True)
    assert res.returncode in (0,1,2)
