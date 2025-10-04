"""A tiny scanning API that uses detectors to find potential secrets."""
from . import detectors


def scan_text(text: str):
    """Run all detectors against `text` and return a list of finding dicts."""
    findings = []
    funcs = [detectors.detect_aws_access_key, detectors.detect_private_key, detectors.detect_high_entropy_strings, detectors.detect_keywords_context]
    for f in funcs:
        for hit in f(text):
            findings.append(hit.to_dict())
    return findings


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as fh:
        print(scan_text(fh.read()))
