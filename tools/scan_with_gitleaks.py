"""Wrapper to run gitleaks against the project using the example rules."""
import shutil
import subprocess
import sys
from pathlib import Path

RULE_PATH = Path(__file__).parents[1] / "rules" / "gitleaks.toml"


def run_gitleaks(target_dir: Path):
    gitleaks_bin = shutil.which("gitleaks")
    if not gitleaks_bin:
        print("gitleaks not found on PATH. Install it from https://github.com/zricethezav/gitleaks and re-run.")
        return 2
    cmd = [gitleaks_bin, "detect", "--source", str(target_dir), "--config-path", str(RULE_PATH), "--report-format", "json"]
    print("Running:", " ".join(cmd))
    try:
        subprocess.check_call(cmd)
        return 0
    except subprocess.CalledProcessError as e:
        return e.returncode


if __name__ == "__main__":
    target = Path(".")
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
    sys.exit(run_gitleaks(target))
