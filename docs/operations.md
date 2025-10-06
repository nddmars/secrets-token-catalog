# Operations & Tuning

Track rule performance metrics in `rules/operations.yaml` or the SQLite DB produced by `tools/init_operations_db.py`.

Fields include:
- detection_rule_id
- test_audit_sample_size
- true_positives
- false_positives
- false_negatives
- Recall
- Precision
- last_audit_date
- tuning_recommendation

Use `src.operations.OperationsSet` to load metrics and compute precision/recall programmatically.
