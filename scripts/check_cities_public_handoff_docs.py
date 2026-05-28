#!/usr/bin/env python3
"""Validate public handoff docs keep Cities source-row boundary visible."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PHRASES_BY_DOC = {
    Path("README.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages, 2 populated lock rows, no source rows imported",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "data/study/mappings/cities_source_row_lock_decisions.csv",
    ),
    Path("docs/REAL_REPORT_RUN.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages, 2 populated lock rows, no source rows imported",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "data/study/mappings/cities_source_row_lock_decisions.csv",
    ),
    Path("docs/FINAL_REPORT.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages, 2 populated lock rows, no source rows imported",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md",
    ),
    Path("docs/FINAL_REPORT_DRAFT.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages, 2 populated lock rows, no source rows imported",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md",
    ),
    Path("docs/FINAL_REPORT_OUTLINE.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages, 2 populated lock rows, no source rows imported",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
    ),
    Path("docs/CLAIM_CATALOG.md"): (
        "Torah-code.org Cities/Aumann/Simon-McKay source chain",
        "Cities source-row lock handoff",
        "14 source-row lock candidate pages, 2 populated lock rows, no source rows imported",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "data/study/mappings/cities_source_row_lock_decisions.csv",
    ),
    Path("docs/CONSOLIDATED_FINDINGS.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages, 2 populated lock rows, no source rows imported",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
    ),
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages, 2 populated lock rows, no source rows imported",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
    ),
    Path("protocols/README.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages, 2 populated lock rows, no source rows imported",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "data/study/mappings/cities_source_row_lock_decisions.csv",
    ),
}

FORBIDDEN_PHRASES_BY_DOC = {
    Path("README.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
    ),
    Path("docs/FINAL_REPORT.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
    ),
    Path("docs/FINAL_REPORT_DRAFT.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
    ),
    Path("docs/FINAL_REPORT_OUTLINE.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
    ),
    Path("docs/CLAIM_CATALOG.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
    ),
    Path("docs/CONSOLIDATED_FINDINGS.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
    ),
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
    ),
    Path("protocols/README.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
    ),
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_public_handoff_docs(args.root)
    if failures:
        for failure in failures:
            print(f"Cities public handoff doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities public handoff docs ok: {args.root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser


def validate_public_handoff_docs(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []
    for relative_path, required_phrases in REQUIRED_PHRASES_BY_DOC.items():
        doc = root / relative_path
        if not doc.exists():
            failures.append(f"{relative_path} is missing")
            continue
        text = normalize_space(doc.read_text(encoding="utf-8"))
        for phrase in required_phrases:
            if normalize_space(phrase) not in text:
                failures.append(f"{relative_path} missing phrase: {phrase}")
        for phrase in FORBIDDEN_PHRASES_BY_DOC.get(relative_path, ()):
            if normalize_space(phrase) in text:
                failures.append(f"{relative_path} contains stale phrase: {phrase}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
