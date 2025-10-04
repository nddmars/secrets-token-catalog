# Rule format

Rules are stored in YAML and SQLite. The YAML format follows the "Rule Catalog Sheet (The Definitive Library)" described in the project.

Fields:
- token_id: unique identifier (string)
- token_name: human-friendly name
- detection_category: grouping for enabling/disabling categories
- regex_pattern: regex used for matching
- keywords_prefixes: list of strings used for fast checks
- minimum_entropy: minimum Shannon entropy expected
- token_length: expected token length or range "min-max"
- default_severity: High/Medium/Low
- rule_status: Active/Deprecated/Testing

Use `tools/init_rules_db.py` to initialize `rules/rules.db` from `rules/rules.yaml`.
