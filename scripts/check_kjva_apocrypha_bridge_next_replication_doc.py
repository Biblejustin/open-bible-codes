#!/usr/bin/env python3
"""Validate the KJVA apocrypha bridge next-replication planning boundary."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/KJVA_APOCRYPHA_BRIDGE_NEXT_REPLICATION_DESIGN.md")

REQUIRED_PHRASES = (
    "Status: planning document only. This is not a result report.",
    "No KJVA apocrypha bridge claim language is supported by current controls.",
    "Do not run a result-bearing KJVA replication until a new study-lock manifest and preflight sidecar exist.",
    "fresh term/source target set before seeing new output",
    "Exclude terms used in the post-screen confirmatory and completed prospective bridge lanes.",
    "must not be matched or exceeded by the non-Bible insertion controls",
    "No reuse of the completed 7-term prospective lane as a fresh discovery.",
    "No claim wording from the single observed `tobit` bridge row.",
    "No significance wording from raw bridge counts alone.",
)
REQUIRED_LINKS = (
    "terms/kjv_apocrypha_bridge_prospective_terms.csv",
    "reports/kjv_apocrypha_bridge_prospective/bridge_candidates.csv",
    "reports/kjv_apocrypha_bridge_prospective/term_summary.csv",
    "reports/kjv_apocrypha_bridge_prospective_nonbible_controls/control_summary.csv",
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md",
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md",
    "configs/prospective_study_lanes.json",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:claim report|claim-grade|proved|proves|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "This is not a result report.",
    "No KJVA apocrypha bridge claim language is supported by current controls.",
    "No claim wording from the single observed `tobit` bridge row.",
    "No significance wording from raw bridge counts alone.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_next_replication_doc(args.doc)
    if failures:
        for failure in failures:
            print(
                f"KJVA apocrypha bridge next-replication doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"KJVA apocrypha bridge next-replication doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_next_replication_doc(doc: Path = DEFAULT_DOC) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures: list[str] = []
    for phrase in REQUIRED_PHRASES:
        if normalize_space(phrase) not in normalized:
            failures.append(f"{doc} missing phrase: {phrase}")
    for link in REQUIRED_LINKS:
        if f"`{link}`" not in text:
            failures.append(f"{doc} missing evidence link: {link}")
    failures.extend(validate_no_overclaim(doc, text))
    return failures


def validate_no_overclaim(doc: Path, text: str) -> list[str]:
    failures: list[str] = []
    allowed = {normalize_space(context) for context in ALLOWED_FORBIDDEN_CONTEXTS}
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not FORBIDDEN_OVERCLAIM_RE.search(line):
            continue
        normalized_line = normalize_space(line).lstrip("- ")
        if normalized_line in allowed:
            continue
        failures.append(f"{doc}:{line_number} possible overclaim wording: {line.strip()}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
