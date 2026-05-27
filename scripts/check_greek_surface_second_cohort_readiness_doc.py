#!/usr/bin/env python3
"""Validate Greek surface second-cohort readiness boundary."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts import build_prospective_lane_status as lane_status
from scripts import scaffold_prospective_study as scaffold
from scripts.prospective_profile_snapshot import status_count_phrases


DEFAULT_DOC = Path("docs/GREEK_SURFACE_SECOND_COHORT_READINESS.md")
DEFAULT_PROFILES = Path("configs/prospective_study_lanes.json")
READINESS_DOC = Path("docs/PROSPECTIVE_STUDY_READINESS.md")
SOURCE_TERM_FILE = Path("terms/greek_expanded_prospective_terms.csv")
NO_READY_PHRASE = "no tracked lane remains `ready_for_preflight`"
FRESH_TARGET_PHRASE = "fresh term/source target set"
BLOCKED_STATUS_PHRASE = "blocked pending genuinely new terms"
NOT_FROM_EXISTING_POOL_PHRASE = (
    "new source term file not derived from `terms/greek_expanded_prospective_terms.csv`"
)
ZERO_OUTPUT_PHRASE = "output rows: 0"
NO_EXISTING_POOL_RERUN_PHRASE = (
    "do not run another Greek surface result-producing study from the existing expanded pool"
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_second_cohort_doc(args.doc, args.profiles)
    if failures:
        for failure in failures:
            print(f"Greek second-cohort readiness doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Greek second-cohort readiness doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    return parser


def validate_second_cohort_doc(doc: Path, profiles_path: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    try:
        profiles = scaffold.load_profiles(profiles_path)
    except (OSError, ValueError) as exc:
        return [f"could not read profile file {profiles_path}: {exc}"]

    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_whitespace(text)
    failures: list[str] = []
    ready = lane_status.ready_profiles(profiles)

    for link in (
        display_path(SOURCE_TERM_FILE),
        READINESS_DOC.as_posix(),
    ):
        if f"`{link}`" not in text:
            failures.append(f"{doc} missing link: {link}")
    for phrase in (
        BLOCKED_STATUS_PHRASE,
        FRESH_TARGET_PHRASE,
        NOT_FROM_EXISTING_POOL_PHRASE,
        ZERO_OUTPUT_PHRASE,
        NO_EXISTING_POOL_RERUN_PHRASE,
    ):
        if not contains_phrase(normalized_text, phrase):
            failures.append(f"{doc} missing guard phrase: {phrase}")
    for phrase in status_count_phrases(profiles):
        if not contains_phrase(normalized_text, phrase):
            failures.append(f"{doc} missing status-count phrase: {phrase}")

    if ready:
        ready_ids = ", ".join(f"`{profile['id']}`" for profile in ready)
        if contains_phrase(normalized_text, NO_READY_PHRASE):
            failures.append(f"{doc} says no ready lanes but profiles show: {ready_ids}")
    elif not contains_phrase(normalized_text, NO_READY_PHRASE):
        failures.append(f"{doc} missing no-ready-lanes boundary")

    return failures


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def contains_phrase(normalized_text: str, phrase: str) -> bool:
    return normalize_whitespace(phrase) in normalized_text


def display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
