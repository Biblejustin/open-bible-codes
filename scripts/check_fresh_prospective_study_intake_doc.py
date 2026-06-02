#!/usr/bin/env python3
"""Validate the fresh prospective-study intake gate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/FRESH_PROSPECTIVE_STUDY_INTAKE.md")

REQUIRED_HEADINGS = (
    "# Fresh Prospective Study Intake",
    "## Required Intake Package",
    "## Intake Checklist",
    "## Default Commands",
    "## Allowed No-Input Work",
    "## Relationship To Current Lanes",
    "## Cautions",
)

REQUIRED_LINKS = (
    "configs/prospective_study_lanes.json",
    "docs/PROSPECTIVE_LANE_STATUS.md",
    "docs/PROSPECTIVE_STUDY_READINESS.md",
)

REQUIRED_PHRASES = (
    "Status: intake gate only; no result-producing run yet.",
    "Do not use it to rebrand an already-screened row as a new discovery.",
    "If any item is missing",
    "must not produce new result-bearing output",
    "no tracked lane remains `ready_for_preflight`",
    "fresh term/source target set",
    "python3 -m scripts.audit_prospective_terms",
    "python3 -m scripts.build_study_lock_manifest",
    "python3 -m scripts.preflight_prospective_study",
)

REQUIRED_GATES = (
    "Source lawfulness",
    "Source identity",
    "Term provenance",
    "Prior-evidence audit",
    "Study rule",
    "Controls",
    "Multiple testing",
    "Outputs",
    "Lock",
    "Preflight",
)

DISALLOWED_PHRASES = (
    "run new results now",
    "result-producing run is allowed",
    "claim-grade ready",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_fresh_prospective_study_intake_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"fresh prospective-study intake doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"fresh prospective-study intake doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_fresh_prospective_study_intake_doc(doc: Path = DEFAULT_DOC) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]

    text = doc.read_text(encoding="utf-8")
    normalized = normalize_whitespace(text)
    failures: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            failures.append(f"{doc} missing heading: {heading}")

    for link in REQUIRED_LINKS:
        if f"`{link}`" not in text:
            failures.append(f"{doc} missing link: {link}")

    for phrase in REQUIRED_PHRASES:
        if normalize_whitespace(phrase) not in normalized:
            failures.append(f"{doc} missing guard phrase: {phrase}")

    for gate in REQUIRED_GATES:
        if f"| {gate} |" not in text:
            failures.append(f"{doc} missing checklist gate: {gate}")

    for phrase in DISALLOWED_PHRASES:
        if phrase.casefold() in text.casefold():
            failures.append(f"{doc} has disallowed phrase: {phrase}")

    return failures


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
