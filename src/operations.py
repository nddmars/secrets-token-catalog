"""Loader and calculator for rules operations/tuning metrics."""
from pathlib import Path
import sqlite3
import yaml
from typing import Dict, Any


def _safe_div(a, b):
    try:
        return a / b
    except Exception:
        return None


class OperationEntry:
    def __init__(self, row: Dict[str, Any]):
        self.detection_rule_id = row.get('detection_rule_id') or row.get('detection_rule_id')
        self.test_audit_sample_size = int(row.get('test_audit_sample_size') or 0)
        self.true_positives = int(row.get('true_positives') or 0)
        self.false_positives = int(row.get('false_positives') or 0)
        self.false_negatives = int(row.get('false_negatives') or 0)
        self.last_audit_date = row.get('last_audit_date')
        self.tuning_recommendation = row.get('tuning_recommendation')

    @property
    def precision(self):
        denom = (self.true_positives + self.false_positives)
        return _safe_div(self.true_positives, denom) if denom else None

    @property
    def recall(self):
        denom = (self.true_positives + self.false_negatives)
        return _safe_div(self.true_positives, denom) if denom else None


class OperationsSet:
    def __init__(self, entries):
        self.entries = entries

    @classmethod
    def from_yaml(cls, path: Path):
        with open(path, 'r', encoding='utf-8') as fh:
            data = yaml.safe_load(fh)
        entries = [OperationEntry(r) for r in data]
        return cls(entries)

    @classmethod
    def from_sqlite(cls, path: Path):
        conn = sqlite3.connect(str(path))
        cur = conn.cursor()
        cur.execute('SELECT detection_rule_id, test_audit_sample_size, true_positives, false_positives, false_negatives, last_audit_date, tuning_recommendation FROM operations')
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        data = [dict(zip(cols, r)) for r in rows]
        conn.close()
        entries = [OperationEntry(r) for r in data]
        return cls(entries)

    def get_by_rule(self, token_id):
        for e in self.entries:
            if e.detection_rule_id == token_id:
                return e
        return None
