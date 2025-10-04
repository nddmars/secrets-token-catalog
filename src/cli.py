"""Command-line interface for the scanner."""
import argparse
from .scanner import scan_text


def main():
    p = argparse.ArgumentParser(description="Scan a file for potential secrets")
    p.add_argument("path")
    args = p.parse_args()
    with open(args.path, "r", encoding="utf-8") as fh:
        text = fh.read()
    findings = scan_text(text)
    if not findings:
        print("No findings detected")
    else:
        for f in findings:
            print(f"[{f['detector']}] (line {f['lineno']}) confidence={f['confidence']:.2f} -> {f['snippet']}")


if __name__ == "__main__":
    main()
