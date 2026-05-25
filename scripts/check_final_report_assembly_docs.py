#!/usr/bin/env python3
"""Validate final-report assembly docs keep source and claim boundaries."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PHRASES_BY_DOC = {
    Path("docs/FINAL_REPORT.md"): (
        "Status: reader-facing report over the current locked report set",
        "does not promote any row to a public claim",
        "Primary assembly source: `reports/real_report_run/summary.md`",
        "`protocols/real_report_run.toml`",
        "no current result should be presented as a public claim",
    ),
    Path("docs/FINAL_REPORT_DRAFT.md"): (
        "Status: reader-facing draft assembled from the current locked report set",
        "does not promote any row to a public claim",
        "Current assembly source: `reports/real_report_run/summary.md`",
        "formal report protocol",
        "No current row should be written as a public claim",
    ),
    Path("docs/FINAL_REPORT_OUTLINE.md"): (
        "Status: writing scaffold for the current completed report set",
        "This is not a new analysis run",
        "No current row should be labeled as a public claim",
        "`reports/real_report_run/summary.md`",
        "`docs/CONSOLIDATED_FINDINGS.md`",
        "`docs/CLAIM_CATALOG.md`",
        "`docs/REAL_REPORT_RUN.md`",
    ),
    Path("docs/FINAL_REPORT_HIGHLIGHTS.md"): (
        "Status: compact final-report table assembled from locked report artifacts",
        "does not promote rows to public claims",
        "python3 -m scripts.build_final_report_highlights",
        "presentation layer over the centered-occurrence index and claim catalog",
        "not because it is claim-grade",
    ),
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_final_report_assembly_docs(args.root)
    if failures:
        for failure in failures:
            print(f"final-report assembly doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"final-report assembly docs ok: {args.root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser


def validate_final_report_assembly_docs(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []
    for relative_path, required_phrases in REQUIRED_PHRASES_BY_DOC.items():
        doc = root / relative_path
        if not doc.exists():
            failures.append(f"{relative_path} is missing")
            continue
        normalized_text = normalize_space(doc.read_text(encoding="utf-8"))
        for phrase in required_phrases:
            if normalize_space(phrase) not in normalized_text:
                failures.append(f"{relative_path} missing phrase: {phrase}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
