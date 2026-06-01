#!/usr/bin/env python3
"""Validate public KJVA handoff docs keep current no-input wording."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PHRASES_BY_DOC = {
    Path("README.md"): (
        "KJVA/apocrypha source-readiness is tracked separately",
        "9 handoff rows and 8 manual-input-needed rows",
        "new independent KJVA result output blocked",
    ),
    Path("docs/REAL_REPORT_RUN.md"): (
        "KJVA no-input handoff status consolidates 9 handoff rows",
        "no-new-KJVA-result boundary",
    ),
    Path("docs/FINAL_REPORT.md"): (
        "The KJVA no-input handoff keeps that boundary in one place.",
        "result allowed 0",
        "It is a source-readiness work map, not a new KJVA result.",
    ),
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "KJVA No-Input Handoff Status",
        "9 handoff rows, 9 handoff-ready rows, 8",
        "result allowed 0",
        "This handoff does not approve source use",
    ),
    Path("protocols/README.md"): (
        "KJVA no-input handoff at 9 handoff rows",
        "8 manual-input-needed rows",
        "result allowed 0",
    ),
    Path("reports/real_report_run/summary.md"): (
        "## KJVA No-Input Handoff Status",
        "| Result allowed | 0 |",
        "Claim status: `kjva_no_input_handoff_blocks_new_result`",
        "Current read: this is a work map, not a statistical result.",
    ),
}
FORBIDDEN_PHRASES_BY_DOC = {
    Path("README.md"): (
        "new independent KJVA result output allowed",
    ),
    Path("docs/REAL_REPORT_RUN.md"): (
        "KJVA source-lock ready at 1",
    ),
    Path("docs/FINAL_REPORT.md"): (
        "new KJVA result is ready",
    ),
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "KJVA result allowed 1",
    ),
    Path("protocols/README.md"): (
        "KJVA source lock ready",
    ),
    Path("reports/real_report_run/summary.md"): (
        "| Result allowed | 1 |",
        "new KJVA result is ready",
    ),
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_public_handoff_docs(args.root)
    if failures:
        for failure in failures:
            print(f"KJVA public handoff doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA public handoff docs ok: {args.root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser


def validate_kjva_public_handoff_docs(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []
    for relative_path, required_phrases in REQUIRED_PHRASES_BY_DOC.items():
        doc = root / relative_path
        if not doc.exists():
            failures.append(f"{relative_path} is missing")
            continue
        text = doc.read_text(encoding="utf-8")
        normalized_text = normalize_space(text)
        for phrase in required_phrases:
            if normalize_space(phrase) not in normalized_text:
                failures.append(f"{relative_path} missing phrase: {phrase}")
        for phrase in FORBIDDEN_PHRASES_BY_DOC.get(relative_path, ()):
            if normalize_space(phrase) in normalized_text:
                failures.append(f"{relative_path} contains stale phrase: {phrase}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
