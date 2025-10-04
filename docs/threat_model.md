# Threat Model and Safety

This research focuses on detecting accidental secrets in code. It does not aim to locate leaked secrets across public services.

Assumptions:
- Source code may contain accidentally committed keys, tokens, or credentials.
- The scanner will be run by repository owners or CI with appropriate access controls.

Safe-handling guidance:
- Treat detected values as sensitive; avoid printing full secrets in logs.
- Replace any real secrets in examples with placeholders before sharing publicly.
