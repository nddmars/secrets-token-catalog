"""Demo script to tune a rule.

- Runs RuleSet and scanner on example files
- Compares findings to a small ground-truth to compute TP/FP/FN
- Updates `rules/operations.yaml` for the rule and prints precision/recall and recommendation

This is a simplified demo intended for research and manual verification.
"""
from pathlib import Path
import yaml
import json
from src.rules import RuleSet
from src.scanner import scan_text

# Ground truth mapping for examples; in real life this comes from manual audit
GROUND_TRUTH = {
    'examples/seeded_repo/app.py': [
        # list of secret substrings known to be secrets in this file
        'AKIAEXAMPLEKEY123456',
        'abcd1234efgh5678IJKL9012'
    ],
    'examples/clean_repo/app.py': []
}

RULE_ID = 'AWS-001'
REPO_ROOT = Path(__file__).parents[1]
RULE_YAML = REPO_ROOT / 'rules' / 'rules.yaml'
OPS_YAML = REPO_ROOT / 'rules' / 'operations.yaml'


def load_rules():
    return RuleSet.from_yaml(RULE_YAML)


def run_and_evaluate(rule_id: str):
    rs = load_rules()
    # find the target rule
    target = None
    for r in rs.rules:
        if r.token_id == rule_id:
            target = r
            break
    if not target:
        print('Rule', rule_id, 'not found')
        return

    tp = 0
    fp = 0
    fn = 0
    sample_count = 0

    for rel_path, secrets in GROUND_TRUTH.items():
        path = REPO_ROOT / rel_path
        sample_count += 1
        text = path.read_text(encoding='utf-8')
        findings = target.matches(text)
        found_values = [f['match'] for f in findings]
        # Count TP: ground-truth secrets found by the rule
        for s in secrets:
            if any(s in fv or fv in s for fv in found_values):
                tp += 1
            else:
                fn += 1
        # Count FP: findings that are not in ground truth
        for fv in found_values:
            if not any(fv in s or s in fv for s in secrets):
                fp += 1

    # Update operations YAML (load, replace entry for rule_id)
    ops = []
    if OPS_YAML.exists():
        ops = yaml.safe_load(OPS_YAML) or []
    # replace or append
    updated = False
    for e in ops:
        if e.get('detection_rule_id') == rule_id:
            e['test_audit_sample_size'] = sample_count
            e['true_positives'] = tp
            e['false_positives'] = fp
            e['false_negatives'] = fn
            e['last_audit_date'] = '2025-10-04'
            e['tuning_recommendation'] = make_recommendation(tp, fp, fn)
            updated = True
            break
    if not updated:
        ops.append({
            'detection_rule_id': rule_id,
            'test_audit_sample_size': sample_count,
            'true_positives': tp,
            'false_positives': fp,
            'false_negatives': fn,
            'last_audit_date': '2025-10-04',
            'tuning_recommendation': make_recommendation(tp, fp, fn)
        })

    with open(OPS_YAML, 'w', encoding='utf-8') as fh:
        yaml.safe_dump(ops, fh, sort_keys=False)

    precision = None
    recall = None
    if tp + fp > 0:
        precision = tp / (tp + fp)
    if tp + fn > 0:
        recall = tp / (tp + fn)

    print('Rule:', rule_id)
    print('Samples scanned:', sample_count)
    print('TP:', tp, 'FP:', fp, 'FN:', fn)
    print('Precision:', precision)
    print('Recall:', recall)
    print('Recommendation:', make_recommendation(tp, fp, fn))


def make_recommendation(tp, fp, fn):
    # naive recommendation rules
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    if precision < 0.7:
        return 'Refine regex or add stricter keywords to reduce false positives.'
    if recall < 0.7:
        return 'Loosen regex or add more prefixes/keywords to improve recall.'
    return 'No change recommended; rule is balanced.'


if __name__ == '__main__':
    run_and_evaluate(RULE_ID)
