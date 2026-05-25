#!/usr/bin/env python3
"""Validate public WRR handoff docs keep current decision-lock wording."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PHRASES_BY_DOC = {
    Path("README.md"): (
        "WRR claim-blocker packet:",
        "WRR source-policy review checklist:",
        "WRR source-transcription row review checklist:",
        "WRR remaining-lane review checklist:",
        "WRR manual decision register:",
        "WRR manual decision records:",
        "WRR manual decision record worksheet:",
        "Chełm source-policy/pair-rule target as a review lane",
        "37 manual-decision inventory rows representing 58 action terms, 59 residual pair links, and 40 minimum-frontier pair links",
        "records all 37 current locks: 26 `no_source_change` rows and 11 `method_lock` rows",
        "current record status, selected action, and evidence prompt for all 37 lock rows",
        "review order with required decision-record fields",
        "review lanes with required decision-record fields",
        "source-transcription row clusters, page-image near-match terms, and method/pair-universe counts",
        "without choosing corrections or exclusions",
    ),
    Path("docs/REAL_REPORT_RUN.md"): (
        "WRR claim-readiness doc records selected local-lock readiness",
        "summarizes the residual term, row, page-image, and method/pair-universe review lanes",
        "WRR source-policy checklist keeps the Chełm source-policy/pair-rule target as a review lane",
        "WRR source-transcription row checklist keeps the 22 row clusters in review order",
        "WRR remaining-lane checklist keeps 3 page-image terms and 11 method/pair-universe terms in review lanes",
        "WRR manual decision register consolidates 37 manual-decision inventory rows",
        "WRR manual decision-record checker keeps 37 populated lock rows aligned to the current register",
        "WRR manual decision-record worksheet lists the exact rank/lane/target fields plus current record status",
        "no-input handoff with term targets, source-transcription row clusters, page-image near matches, and method/pair-universe counts",
        "locks them as 26 `no_source_change` rows and 11 `method_lock` rows",
    ),
    Path("docs/FINAL_REPORT.md"): (
        "Exact published reproduction remains caveated by source-transcription limits and the 163-distance gap",
        "source-policy term, 43 source-transcription terms, 3 page-image near-match terms, and 11 method/pair-universe terms",
        "row-cluster priorities, page-image near matches, and method/pair-universe counts",
        "source-policy checklist keeps the Chełm source-policy/pair-rule target as a review lane",
        "row-review checklist keeps the 22 source-transcription row clusters in review order",
        "remaining-lane checklist keeps the 3 page-image near-match terms and 11 method/pair-universe terms in review lanes",
        "manual decision register consolidates 37 manual-decision inventory rows representing 58 action terms, 59 residual pair links, and 40 minimum-frontier pair links",
        "populated decision-record CSV locks all 37 rows as 26 `no_source_change` decisions and 11 `method_lock` decisions",
    ),
    Path("docs/FINAL_REPORT_DRAFT.md"): (
        "The residual handoff is packetized without selecting corrections",
        "source-policy term, 43 source-transcription terms, 3 page-image near-match terms, and 11 method/pair-universe terms",
        "method/pair-universe counts for no-input review",
        "source-policy checklist keeps the Chełm source-policy/pair-rule target as a review lane",
        "row-review checklist keeps the 22 source-transcription row clusters in review order",
        "remaining-lane checklist keeps the 3 page-image near-match terms and 11 method/pair-universe terms in review lanes",
        "manual decision register consolidates 37 manual-decision inventory rows representing 58 action terms, 59 residual pair links, and 40 minimum-frontier pair links",
        "populated decision-record CSV locks all 37 rows as 26 `no_source_change` decisions and 11 `method_lock` decisions",
    ),
    Path("docs/FINAL_REPORT_OUTLINE.md"): (
        "43 source-transcription terms, 3 page-image near-match terms, and 11 method/pair-universe terms",
        "claim-blocker packet mirrors top term targets, row clusters, page-image near matches, and method/pair-universe",
        "source-policy checklist keeps the Chełm source-policy/pair-rule target as a review lane",
        "row-review checklist keeps 22 row clusters in review order",
        "remaining-lane checklist keeps 3 page-image terms and 11 method/pair-universe terms in review lanes",
        "manual decision register consolidates 37 manual-decision inventory rows representing 58 action terms",
        "populated decision-record CSV locks all 37 rows as 26 `no_source_change` decisions and 11 `method_lock` decisions",
        "exact published WRR reproduction remains caveated by source-transcription limits and the 163-distance gap",
    ),
    Path("docs/CONSOLIDATED_FINDINGS.md"): (
        "The residual handoff is now packetized without selecting corrections",
        "source-policy term, 43 source-transcription terms, 3 page-image near-match terms, and 11 method/pair-universe terms",
        "claim-blocker packet mirroring top term targets, row clusters, page-image near matches, and method/pair-universe counts",
        "source-policy checklist keeps the Chełm source-policy/pair-rule target as a review lane",
        "row-review checklist keeps the 22 source-transcription row clusters in review order",
        "remaining-lane checklist keeps the 3 page-image near-match terms and 11 method/pair-universe terms in review lanes",
        "manual decision register consolidates 37 manual-decision inventory rows representing 58 action terms, 59 residual pair links, and 40 minimum-frontier pair links",
        "decision-record CSV locks all 37 rows as 26 `no_source_change` decisions and 11 `method_lock` decisions",
    ),
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "source-transcription row cluster summary, page-image near-match lane, and method/pair-universe summary",
        "source-transcription/row-alignment targets, 3 page-image near-match targets, and 11 method/pair-universe targets",
        "Chełm source-policy/pair-rule target as a review lane",
        "22 row clusters in review order",
        "14 remaining-lane terms in page-image and method/pair-universe review lanes",
        "37 manual-decision inventory rows",
        "current locks: 26 `no_source_change` rows and 11 `method_lock` rows",
        "current record status, selected action, and evidence prompt for all 37 lock rows",
        "row-level review order, and page-image review boundary",
    ),
}

FORBIDDEN_PHRASES_BY_DOC = {
    Path("docs/REAL_REPORT_RUN.md"): (
        "still carries blocked status",
        "open method decisions",
        "all four blocker areas until source/method locks change",
    ),
    Path("docs/FINAL_REPORT.md"): (
        "all four blocker areas until source/method locks change",
    ),
    Path("docs/FINAL_REPORT_DRAFT.md"): (
        "all four blocker areas until source/method locks change",
    ),
    Path("docs/FINAL_REPORT_OUTLINE.md"): (
        "all four blocker areas until source/method locks change",
    ),
    Path("docs/CONSOLIDATED_FINDINGS.md"): (
        "all four blocker areas until source/method locks change",
    ),
    Path("docs/REMAINING_WORK_REGISTER.md"): (
        "header-only template for future manual-lock records",
        "Header-only status means no correction",
        "future lock rows without filling the lock CSV",
    ),
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_public_handoff_docs(args.root)
    if failures:
        for failure in failures:
            print(f"WRR public handoff doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR public handoff docs ok: {args.root}")
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
