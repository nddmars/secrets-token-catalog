"""Initialize a SQLite rules DB from `rules/rules.yaml`.
Usage: python tools/init_rules_db.py [out.db]
"""
import sqlite3
import sys
from pathlib import Path
import yaml

SCHEMA = '''
CREATE TABLE IF NOT EXISTS rules (
    token_id TEXT PRIMARY KEY,
    token_name TEXT,
    detection_category TEXT,
    regex_pattern TEXT,
    keywords_prefixes TEXT,
    minimum_entropy REAL,
    token_length TEXT,
    default_severity TEXT,
    rule_status TEXT
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
        cur.execute('''INSERT OR REPLACE INTO rules (token_id, token_name, detection_category, regex_pattern, keywords_prefixes, minimum_entropy, token_length, default_severity, rule_status) VALUES (?,?,?,?,?,?,?,?,?)''', (
            r.get('token_id'),
            r.get('token_name'),
            r.get('detection_category'),
            r.get('regex_pattern'),
            ','.join(r.get('keywords_prefixes', [])),
            r.get('minimum_entropy'),
            str(r.get('token_length')),
            r.get('default_severity'),
            r.get('rule_status')
        ))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    repo = Path(__file__).parents[1]
    yaml_path = repo / 'rules' / 'rules.yaml'
    out_db = Path(sys.argv[1]) if len(sys.argv) > 1 else repo / 'rules' / 'rules.db'
    init_db(yaml_path, out_db)
    print('Initialized rules DB at', out_db)
