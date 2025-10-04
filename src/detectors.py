"""Simple detectors for secrets scanning."""
import re
import math

KEYWORDS = ["password", "secret", "token", "apikey", "api_key", "aws_access_key_id", "private_key"]

AWS_ACCESS_KEY_RE = re.compile(r"AKIA[0-9A-Z]{16}")
PRIVATE_KEY_BEGIN = re.compile(r"-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----")
GENERIC_SECRET_RE = re.compile(r"(?P<quote>[\'\"])?(?P<val>[A-Za-z0-9]{20,})\1")


def _shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    import collections
    counts = collections.Counter(data)
    entropy = 0.0
    for c in counts.values():
        p = c / len(data)
        entropy -= p * math.log2(p)
    return entropy


class Finding:
    def __init__(self, detector: str, snippet: str, lineno: int, confidence: float):
        self.detector = detector
        self.snippet = snippet
        self.lineno = lineno
        self.confidence = confidence

    def to_dict(self):
        return {
            "detector": self.detector,
            "snippet": self.snippet,
            "lineno": self.lineno,
            "confidence": self.confidence,
        }


def detect_aws_access_key(text: str):
    findings = []
    for m in AWS_ACCESS_KEY_RE.finditer(text):
        findings.append(Finding("aws-access-key", m.group(0), 0, 0.9))
    return findings


def detect_private_key(text: str):
    findings = []
    if PRIVATE_KEY_BEGIN.search(text):
        findings.append(Finding("private-key-block", "<privkey>", 0, 0.95))
    return findings


def detect_high_entropy_strings(text: str, entropy_threshold: float = 3.5):
    findings = []
    for m in GENERIC_SECRET_RE.finditer(text):
        val = m.group('val')
        ent = _shannon_entropy(val)
        if ent >= entropy_threshold and len(val) >= 20:
            findings.append(Finding("high-entropy", val, 0, min(0.5 + (ent - entropy_threshold) / 4, 0.95)))
    return findings


def detect_keywords_context(text: str):
    findings = []
    for i, line in enumerate(text.splitlines(), start=1):
        low = line.lower()
        for kw in KEYWORDS:
            if kw in low and any(c.isalnum() for c in low):
                findings.append(Finding("keyword-context", line.strip(), i, 0.4))
                break
    return findings
