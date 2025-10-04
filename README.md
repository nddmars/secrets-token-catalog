# Secrets Token Catalog

Canonical token/rule catalog and tuning harness for secrets detection (uses gitleaks, trufflehog, etc.)

Contents:
- `docs/` - research notes, threat model, detection approach
- `src/` - prototype Python scanner with pluggable detectors and simple CLI
- `examples/` - small example repos (seeded with fake secrets and a clean repo)
- `tests/` - unit tests for detectors and scanner
- `.github/workflows/ci.yml` - CI to run tests

Rules and external scanners
---------------------------

This repository includes example rule files for external scanners in the `rules/` directory:

- `rules/gitleaks.toml` — example rules for gitleaks
- `rules/trufflehog_rules.json` — example rules for trufflehog

There are small wrapper scripts in `tools/` which call the scanners if they are installed:

- `tools/scan_with_gitleaks.py`
- `tools/scan_with_trufflehog.py`

To run gitleaks locally (PowerShell):

```powershell
# install gitleaks (see gitleaks docs) then:
python tools\scan_with_gitleaks.py .
```

To run trufflehog locally (PowerShell):

```powershell
# install trufflehog3 (pip install trufflehog3) or other trufflehog CLI then:
python tools\scan_with_trufflehog.py .
```

Integration tests in `tests/test_integrations.py` will skip if the external tools are not installed.

Operations & tuning
-------------------

This repo also includes a separate operations/tuning dataset used to track TP/FP/FN and compute Precision/Recall:

- `rules/operations.yaml` — sample operations sheet
- `tools/init_operations_db.py` — initialize `rules/operations.db` from the YAML
- `src/operations.py` — loader and calculator for precision/recall

Use `python tools/init_operations_db.py` to create a SQLite DB for operations metrics.

Quick start (local):

1. Create a virtualenv and install dependencies

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Run tests:

```powershell
python -m pytest -q
```

3. Run scanner CLI on a file:

```powershell
python -m src.cli examples\seeded_repo\app.py
```

Notes:
- This is a research prototype and not production-ready.
- Replace seeded example secrets with safe placeholders if sharing the repo.
