"""Initialize a SQLite DB for operations/tuning metrics from `rules/operations.yaml`.
Usage: python tools/init_operations_db.py [out.db]
"""
import sqlite3
import sys
from pathlib import Path
import yaml

SCHEMA = '''
CREATE TABLE IF NOT EXISTS operations (
    detection_rule_id TEXT PRIMARY KEY,
    test_audit_sample_size INTEGER,
    true_positives INTEGER,
    false_positives INTEGER,
    false_negatives INTEGER,
    last_audit_date TEXT,
    tuning_recommendation TEXT
);
'''


def load_yaml(path: Path):
    with open(path, 'r', encoding='utf-8') as fh:
        return yaml.safe_load(fh)


def init_db(yaml_path: Path, out_db: Path):
    data = load_yaml(yaml_path)
    conn = sqlite3.connect(str(out_db))
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    for r in data:
        cur.execute('''INSERT OR REPLACE INTO operations (detection_rule_id, test_audit_sample_size, true_positives, false_positives, false_negatives, last_audit_date, tuning_recommendation) VALUES (?,?,?,?,?,?,?)''', (
            r.get('detection_rule_id'),
            r.get('test_audit_sample_size'),
            r.get('true_positives'),
            r.get('false_positives'),
            r.get('false_negatives'),
            r.get('last_audit_date'),
            r.get('tuning_recommendation')
        ))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    repo = Path(__file__).parents[1]
    yaml_path = repo / 'rules' / 'operations.yaml'
    out_db = Path(sys.argv[1]) if len(sys.argv) > 1 else repo / 'rules' / 'operations.db'
    init_db(yaml_path, out_db)
    print('Initialized operations DB at', out_db)
