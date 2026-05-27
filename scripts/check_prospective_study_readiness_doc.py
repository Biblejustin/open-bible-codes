#!/usr/bin/env python3
"""Validate prospective-study readiness doc against lane profile state."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts import build_prospective_lane_status as lane_status
from scripts import scaffold_prospective_study as scaffold
from scripts.prospective_profile_snapshot import status_count_phrases


DEFAULT_DOC = Path("docs/PROSPECTIVE_STUDY_READINESS.md")
DEFAULT_PROFILES = Path("configs/prospective_study_lanes.json")
NO_READY_PHRASE = "There is no remaining `ready_for_preflight` lane"
FRESH_TARGET_PHRASE = "fresh term/source target set"
NO_BLOCKED_PHRASE = "all tracked profiles are completed, negative/weak, or context-cautioned"
NO_CLAIM_RERUN_PHRASE = "Do not rerun a completed profile as a claim lane"
LANE_STATUS_DOC = Path("docs/PROSPECTIVE_LANE_STATUS.md")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_readiness_doc(args.doc, args.profiles)
    if failures:
        for failure in failures:
            print(f"prospective readiness doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"prospective readiness doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    return parser


def validate_readiness_doc(doc: Path, profiles_path: Path) -> list[str]:
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
    blocked = lane_status.blocked_profiles(profiles)

    profile_display = display_path(profiles_path)
    if f"`{profile_display}`" not in text:
        failures.append(f"{doc} missing profile link: {profile_display}")
    if f"`{LANE_STATUS_DOC.as_posix()}`" not in text:
        failures.append(f"{doc} missing lane-status link: {LANE_STATUS_DOC}")
    if not contains_phrase(normalized_text, NO_CLAIM_RERUN_PHRASE):
        failures.append(f"{doc} missing no-claim-rerun guard")
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
    else:
        if not contains_phrase(normalized_text, NO_READY_PHRASE):
            failures.append(f"{doc} missing no-ready-lanes status")
        if not contains_phrase(normalized_text, FRESH_TARGET_PHRASE):
            failures.append(f"{doc} missing fresh-target boundary")

    if blocked:
        for profile in blocked:
            lane_id = f"`{profile['id']}`"
            if lane_id not in text:
                failures.append(f"{doc} missing blocked lane id: {lane_id}")
    else:
        if not contains_phrase(normalized_text, NO_BLOCKED_PHRASE):
            failures.append(f"{doc} missing no-blocked-lanes status")

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
