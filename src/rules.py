"""Rule loader and matcher for the secrets scanning prototype.
Supports loading rules from YAML or SQLite and matching text with regex + entropy + length + keyword checks.
"""
from pathlib import Path
import re
import sqlite3
import yaml
import math
from typing import List, Dict, Any


def _shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    from collections import Counter
    counts = Counter(data)
    entropy = 0.0
    for c in counts.values():
        p = c / len(data)
        entropy -= p * math.log2(p)
    return entropy


class Rule:
    def __init__(self, row: Dict[str, Any]):
        self.token_id = row.get('token_id') or row.get('token_id')
        self.token_name = row.get('token_name')
        self.detection_category = row.get('detection_category')
        self.regex_pattern = row.get('regex_pattern')
        self.keywords_prefixes = row.get('keywords_prefixes') or []
        # if loaded from sqlite it's a comma-separated string
        if isinstance(self.keywords_prefixes, str):
            self.keywords_prefixes = [k for k in self.keywords_prefixes.split(',') if k]
        self.minimum_entropy = float(row.get('minimum_entropy') or 0)
        self.token_length = row.get('token_length')
        # token_length may be an int or a range "min-max"; normalize
        if isinstance(self.token_length, str) and '-' in self.token_length:
            parts = self.token_length.split('-')
            self.length_min = int(parts[0])
            self.length_max = int(parts[1])
        else:
            try:
                self.length_min = int(self.token_length)
                self.length_max = int(self.token_length)
            except Exception:
                self.length_min = None
                self.length_max = None
        self.default_severity = row.get('default_severity')
        self.rule_status = row.get('rule_status')
        self._compiled = re.compile(self.regex_pattern)

    def matches(self, text: str):
        findings = []
        for m in self._compiled.finditer(text):
            val = m.groupdict().get('val') if 'val' in m.groupdict() else m.group(0)
            ent = _shannon_entropy(val)
            length_ok = True
            if self.length_min is not None:
                length_ok = (self.length_min <= len(val) <= self.length_max)
            entropy_ok = (ent >= self.minimum_entropy) if self.minimum_entropy else True
            # quick keyword check
            kw_ok = True
            if self.keywords_prefixes:
                kw_ok = any(val.startswith(k) or k.lower() in val.lower() for k in self.keywords_prefixes)
            if length_ok and entropy_ok and kw_ok:
                findings.append({
                    'token_id': self.token_id,
                    'token_name': self.token_name,
                    'match': val,
                    'entropy': ent,
                    'length': len(val),
                    'severity': self.default_severity
                })
        return findings


class RuleSet:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    @classmethod
    def from_yaml(cls, path: Path):
        with open(path, 'r', encoding='utf-8') as fh:
            data = yaml.safe_load(fh)
        rules = [Rule(r) for r in data]
        return cls(rules)

    @classmethod
    def from_sqlite(cls, path: Path):
        conn = sqlite3.connect(str(path))
        cur = conn.cursor()
        cur.execute('SELECT token_id, token_name, detection_category, regex_pattern, keywords_prefixes, minimum_entropy, token_length, default_severity, rule_status FROM rules')
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        data = [dict(zip(cols, r)) for r in rows]
        conn.close()
        rules = [Rule(r) for r in data]
        return cls(rules)

    def match_text(self, text: str):
        findings = []
        for r in self.rules:
            findings.extend(r.matches(text))
        return findings
