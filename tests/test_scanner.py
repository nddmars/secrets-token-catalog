import pytest
from src import scanner


def test_detects_seeded_secret(tmp_path):
    p = tmp_path / "sample.py"
    p.write_text('API_TOKEN = "abcd1234efgh5678IJKL9012"\n')
    findings = scanner.scan_text(p.read_text())
    assert any(f['detector'] in ('high-entropy','aws-access-key') for f in findings)


def test_no_findings_in_clean_file(tmp_path):
    p = tmp_path / "clean.py"
    p.write_text('print("hello")\n')
    findings = scanner.scan_text(p.read_text())
    assert findings == []
