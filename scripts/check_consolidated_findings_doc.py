#!/usr/bin/env python3
"""Validate consolidated findings prospective-boundary claims."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts import build_prospective_lane_status as lane_status
from scripts import scaffold_prospective_study as scaffold
from scripts.prospective_profile_snapshot import status_count_phrases


DEFAULT_DOC = Path("docs/CONSOLIDATED_FINDINGS.md")
DEFAULT_PROFILES = Path("configs/prospective_study_lanes.json")
READINESS_DOC = Path("docs/PROSPECTIVE_STUDY_READINESS.md")
LANE_STATUS_DOC = Path("docs/PROSPECTIVE_LANE_STATUS.md")
CLAIM_STANDARD_DOC = Path("docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md")
NO_READY_PHRASE = "no remaining `ready_for_preflight` lane"
FRESH_TARGET_PHRASE = "genuinely new term/source target set"
NO_RERUN_PHRASE = "Completed lanes should not be rerun as claim-oriented studies"
NO_RAW_COUNT_PHRASE = (
    "Avoid more raw count expansion unless the claim standard is fixed in advance"
)
CURRENT_STATUS_PHRASE = "Current next target status"
KJVA_SOURCE_HANDOFF_PHRASE = (
    "4 candidate-source audit rows, 0 candidate verse-import-ready pages, "
    "0 candidate result-ready pages, and result allowed 0"
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_consolidated_findings_doc(args.doc, args.profiles)
    if failures:
        for failure in failures:
            print(f"consolidated findings doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"consolidated findings doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    return parser


def validate_consolidated_findings_doc(doc: Path, profiles_path: Path) -> list[str]:
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

    required_links = (
        display_path(profiles_path),
        READINESS_DOC.as_posix(),
        LANE_STATUS_DOC.as_posix(),
        CLAIM_STANDARD_DOC.as_posix(),
    )
    for link in required_links:
        if f"`{link}`" not in text:
            failures.append(f"{doc} missing link: {link}")

    for phrase in (
        CURRENT_STATUS_PHRASE,
        FRESH_TARGET_PHRASE,
        NO_RERUN_PHRASE,
        NO_RAW_COUNT_PHRASE,
        KJVA_SOURCE_HANDOFF_PHRASE,
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
        for profile in ready:
            lane_id = f"`{profile['id']}`"
            if lane_id not in text:
                failures.append(f"{doc} missing ready lane id: {lane_id}")
    elif not contains_phrase(normalized_text, NO_READY_PHRASE):
        failures.append(f"{doc} missing no-ready-lanes status")

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
