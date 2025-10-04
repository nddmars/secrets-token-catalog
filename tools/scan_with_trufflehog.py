"""Wrapper to run trufflehog3 (python) against the project using example rules.
This wrapper supports the `trufflehog` Python CLI that can accept a rules file as input.
"""
import shutil
import subprocess
import sys
from pathlib import Path

RULE_PATH = Path(__file__).parents[1] / "rules" / "trufflehog_rules.json"


def run_trufflehog(target_dir: Path):
    trufflehog_bin = shutil.which("trufflehog")
    if not trufflehog_bin:
        print("trufflehog not found on PATH. Install it (for example 'pip install trufflehog3') and re-run.")
        return 2
    cmd = [trufflehog_bin, "filesystem", str(target_dir), "--rules", str(RULE_PATH), "--json"]
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
    sys.exit(run_trufflehog(target))
