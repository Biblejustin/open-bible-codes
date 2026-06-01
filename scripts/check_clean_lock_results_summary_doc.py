#!/usr/bin/env python3
"""Validate the clean-lock results summary keeps its cautious boundaries."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CLEAN_LOCK_RESULTS_SUMMARY.md")
DOC_REFERENCE_RE = re.compile(r"`(docs/[^`]+\.md)`")

REQUIRED_HEADINGS = (
    "## Lanes",
    "## Detailed Reports",
    "## Read",
    "## Next Work",
)

REQUIRED_PHRASES = (
    "Status: summary of completed clean-lock and preregistered prospective runs; no claim.",
    "The new clean-lock work produced review queues, not conclusive claims.",
    "does not have the later `reports/study_locks/*.manifest.json` and preflight sidecar",
    "current manifest/preflight workflow before producing new result-bearing output",
    "| Greek surface new terms | 236 |",
    "| Greek lexicon extension | 5,009 |",
    "| Hebrew Gospel/genealogy | 27 |",
    "| Hebrew concordance words | 3,577 |",
    "| KJVA apocrypha bridge prospective | 7 |",
    "0 adjusted-support terms",
    "5 controlled surface rows met the registered `q <= 0.05` threshold",
    "strict function-word rerun removed those common rows",
    "no registered term survived BH correction",
    "one same-length non-Bible replacement block matched the observed total",
    "Any next follow-up should be preregistered from stricter gates before searching.",
)

FORBIDDEN_PHRASES = (
    "claim-ready",
    "settled claim",
)

FORBIDDEN_PATTERNS = (
    re.compile(r"(?<!not )(?<!no )conclusive claims?\b", re.IGNORECASE),
)

REQUIRED_REFERENCES = (
    "docs/GREEK_SURFACE_NEW_TERMS_REPORT.md",
    "docs/GREEK_SURFACE_NEW_TERMS_CONTROL_EVALUATION.md",
    "docs/GREEK_SURFACE_NEW_TERMS_CONTEXT_REVIEW.md",
    "docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_REPORT.md",
    "docs/COMPOUND_EXTENSION_PROSPECTIVE_REPORT.md",
    "docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_REPORT.md",
    "docs/HEBREW_CONCORDANCE_WORDS_CONTROL_PILOT_REPORT.md",
    "docs/HEBREW_CONCORDANCE_UNCORRECTED_QUEUE.md",
    "docs/HEBREW_CONCORDANCE_UNCORRECTED_SCREENING_AUDIT.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_PREREGISTRATION.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_clean_lock_results_summary_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"clean-lock summary failure: {failure}", file=sys.stderr)
        return 1
    print(f"clean-lock summary ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_clean_lock_results_summary_doc(doc: Path = DEFAULT_DOC) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures: list[str] = []
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            failures.append(f"{doc} missing heading: {heading}")
    for phrase in REQUIRED_PHRASES:
        if normalize_space(phrase) not in normalized:
            failures.append(f"{doc} missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in normalized.lower():
            failures.append(f"{doc} contains forbidden phrase: {phrase}")
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(normalized):
            failures.append(f"{doc} contains forbidden pattern: {pattern.pattern}")
    references = sorted(set(DOC_REFERENCE_RE.findall(text)))
    for reference in REQUIRED_REFERENCES:
        if reference not in references:
            failures.append(f"{doc} missing reference: {reference}")
    reference_base = doc.parent.parent if doc.parent.name == "docs" else Path.cwd()
    for reference in references:
        if not (reference_base / reference).exists():
            failures.append(f"{doc} reference is missing locally: {reference}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
