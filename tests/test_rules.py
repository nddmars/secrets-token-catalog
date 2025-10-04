from pathlib import Path
import tempfile
import sqlite3
from src.rules import RuleSet
from tools.init_rules_db import init_db


def test_load_rules_from_yaml(tmp_path):
    repo = Path(__file__).parents[1]
    yaml_path = repo / 'rules' / 'rules.yaml'
    rs = RuleSet.from_yaml(yaml_path)
    assert any(r.token_id == 'AWS-001' for r in rs.rules)


def test_yaml_matching(tmp_path):
    repo = Path(__file__).parents[1]
    yaml_path = repo / 'rules' / 'rules.yaml'
    rs = RuleSet.from_yaml(yaml_path)
    sample = 'AKIAEXAMPLEKEY123456 and some other text'
    findings = rs.match_text(sample)
    assert any(f['token_id'] == 'AWS-001' for f in findings)


def test_init_db_and_load(tmp_path):
    repo = Path(__file__).parents[1]
    out_db = tmp_path / 'rules.db'
    yaml_path = repo / 'rules' / 'rules.yaml'
    init_db(yaml_path, out_db)
    rs = RuleSet.from_sqlite(out_db)
    assert any(r.token_id == 'AWS-001' for r in rs.rules)
    sample = 'AKIAEXAMPLEKEY123456'
    findings = rs.match_text(sample)
    assert any(f['token_id'] == 'AWS-001' for f in findings)
