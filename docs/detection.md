# Detection Approach

We prototype a small set of detectors:

- Pattern-based (regular expressions for known key formats)
- High-entropy string detection (base64-like or long random-looking strings)
- Context heuristics (file extension, surrounding keywords like "password", "secret")

Each detector returns findings with a confidence score. The scanner aggregates and reports findings.

Limitations:
- Heuristics can produce false positives in tests, fixtures, and encoded data.
- This prototype does not include leak prevention workflows or secret revocation automation.
