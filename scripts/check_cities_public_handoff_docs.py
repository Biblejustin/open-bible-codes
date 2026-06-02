#!/usr/bin/env python3
"""Validate public handoff docs keep Cities source-row boundary visible."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PHRASES_BY_DOC = {
    Path("README.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages",
        "14 populated lock rows",
        "no source rows imported",
        "14 pending transcription-review rows",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "whole-project consolidated no-input blocker map",
        "`docs/NO_INPUT_BLOCKER_SUMMARY.md`",
        "data/study/mappings/cities_source_row_lock_decisions.csv",
        "data/study/mappings/cities_source_transcription_decisions.csv",
        "docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md",
        "docs/CITIES_NO_INPUT_HANDOFF_STATUS.md",
        "8 handoff rows",
        "6 manual-input-needed rows",
        "61 OCR packet pages",
        "41 reviewed OCR packet pages",
        "20 unreviewed OCR packet pages",
        "no Cities result allowed",
    ),
    Path("docs/REAL_REPORT_RUN.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages",
        "14 populated lock rows",
        "no source rows imported",
        "14 pending transcription-review rows",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "data/study/mappings/cities_source_row_lock_decisions.csv",
        "data/study/mappings/cities_source_transcription_decisions.csv",
        "docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md",
        "docs/CITIES_NO_INPUT_HANDOFF_STATUS.md",
        "8 handoff rows",
        "6 manual-input-needed rows",
        "61 OCR packet pages",
        "41 reviewed OCR packet pages",
        "20 unreviewed OCR packet pages",
        "no Cities result allowed",
    ),
    Path("docs/FINAL_REPORT.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages",
        "14 populated lock rows",
        "no source rows imported",
        "14 pending transcription-review rows",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md",
        "CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md",
        "CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md",
        "CITIES_NO_INPUT_HANDOFF_STATUS.md",
        "8 handoff rows",
        "6 manual-input-needed rows",
        "61 OCR packet pages",
        "41 reviewed OCR packet pages",
        "20 unreviewed OCR packet pages",
        "no Cities result allowed",
    ),
    Path("docs/FINAL_REPORT_DRAFT.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages",
        "14 populated lock rows",
        "no source rows imported",
        "14 pending transcription-review rows",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md",
        "CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md",
        "CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md",
        "CITIES_NO_INPUT_HANDOFF_STATUS.md",
        "8 handoff rows",
        "6 manual-input-needed rows",
        "61 OCR packet pages",
        "41 reviewed OCR packet pages",
        "20 unreviewed OCR packet pages",
        "no Cities result allowed",
    ),
    Path("docs/FINAL_REPORT_OUTLINE.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages",
        "14 populated lock rows",
        "no source rows imported",
        "14 pending transcription-review rows",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "docs/CITIES_NO_INPUT_HANDOFF_STATUS.md",
        "8 handoff rows",
        "61 OCR packet pages",
        "41 reviewed OCR packet pages",
        "20 unreviewed OCR packet pages",
        "no Cities result allowed",
    ),
    Path("docs/CLAIM_CATALOG.md"): (
        "Torah-code.org Cities/Aumann/Simon-McKay source chain",
        "Cities source-row lock handoff",
        "14 source-row lock candidate pages",
        "14 populated lock rows",
        "no source rows imported",
        "14 pending transcription-review rows",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "data/study/mappings/cities_source_row_lock_decisions.csv",
        "data/study/mappings/cities_source_transcription_decisions.csv",
        "docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md",
        "docs/CITIES_NO_INPUT_HANDOFF_STATUS.md",
        "8 handoff rows",
        "6 manual-input-needed rows",
        "61 OCR packet pages",
        "41 reviewed OCR packet pages",
        "20 unreviewed OCR packet pages",
        "no Cities result allowed",
    ),
    Path("docs/CONSOLIDATED_FINDINGS.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages",
        "14 populated lock rows",
        "no source rows imported",
        "14 pending transcription-review rows",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "docs/CITIES_NO_INPUT_HANDOFF_STATUS.md",
        "8 handoff rows",
        "6 manual-input-needed rows",
        "61 OCR packet pages",
        "41 reviewed OCR packet pages",
        "20 unreviewed OCR packet pages",
        "no Cities result allowed",
    ),
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages",
        "14 populated lock rows",
        "no source rows imported",
        "14 pending transcription-review rows",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "Cities no-input handoff",
        "8 handoff rows",
        "6 manual-input-needed rows",
        "Current overview wording now keeps the same no-result boundary visible: 14 source-row lock candidate pages, 14 populated source-row lock rows, 8 handoff rows, 6 manual-input-needed rows, 14 transcription review rows, 61 OCR packet pages, 41 reviewed OCR packet pages, 20 unreviewed OCR packet pages, 203 priority line-crop review rows, and no Cities result allowed.",
        "61 packet pages, 41 reviewed packet pages, and 20 unreviewed packet pages",
        "61 OCR packet pages",
        "41 reviewed OCR packet pages",
        "20 unreviewed OCR packet pages",
        "no Cities result allowed",
    ),
    Path("protocols/README.md"): (
        "Cities source-row lock handoff:",
        "14 source-row lock candidate pages",
        "14 populated lock rows",
        "no source rows imported",
        "14 pending transcription-review rows",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "data/study/mappings/cities_source_row_lock_decisions.csv",
        "data/study/mappings/cities_source_transcription_decisions.csv",
        "docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md",
        "docs/CITIES_NO_INPUT_HANDOFF_STATUS.md",
        "8 handoff rows",
        "6 manual-input-needed rows",
        "61 OCR packet pages",
        "41 reviewed OCR packet pages",
        "20 unreviewed OCR packet pages",
        "no Cities result allowed",
    ),
    Path("reports/real_report_run/summary.md"): (
        "## Cities Source-Row Lock Status",
        "| Queue rows | 14 |",
        "| Populated decision records | 14 |",
        "| Source-row imports | 0 |",
        "| ELS runs | 0 |",
        "| Compactness runs | 0 |",
        "| No-input handoff rows | 8 |",
        "| No-input manual-input-needed rows | 6 |",
        "| No-input OCR packet pages | 61 |",
        "| No-input reviewed OCR packet pages | 41 |",
        "| No-input unreviewed OCR packet pages | 20 |",
        "| No-input result allowed | 0 |",
        "Current read: Cities source-row pages remain a source-review lane only.",
        "`docs/CITIES_NO_INPUT_HANDOFF_STATUS.md`",
    ),
}

FORBIDDEN_PHRASES_BY_DOC = {
    Path("README.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
        "14 transcription review rows, 203 priority",
    ),
    Path("docs/FINAL_REPORT.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
        "14 transcription review rows, 203 priority",
    ),
    Path("docs/FINAL_REPORT_DRAFT.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
        "14 transcription review rows, 203 priority",
    ),
    Path("docs/FINAL_REPORT_OUTLINE.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
        "14 transcription review rows, 203 priority",
    ),
    Path("docs/CLAIM_CATALOG.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
        "14 transcription review rows, 203 priority",
    ),
    Path("docs/CONSOLIDATED_FINDINGS.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
        "14 transcription review rows, 203 priority",
    ),
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
        "14 transcription review rows, 203 priority",
    ),
    Path("protocols/README.md"): (
        "Cities city-name rows are imported",
        "Cities ELS run is ready",
        "14 transcription review rows, 203 priority",
    ),
    Path("reports/real_report_run/summary.md"): (
        "| Source-row imports | 1 |",
        "| ELS runs | 1 |",
        "| Compactness runs | 1 |",
        "Cities ELS run is ready",
        "14 transcription review rows, 203 priority",
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
