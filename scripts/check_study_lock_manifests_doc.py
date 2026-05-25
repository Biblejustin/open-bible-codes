#!/usr/bin/env python3
"""Validate study-lock workflow doc against prospective profile state."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts import build_prospective_lane_status as lane_status
from scripts import scaffold_prospective_study as scaffold


DEFAULT_DOC = Path("docs/STUDY_LOCK_MANIFESTS.md")
DEFAULT_PROFILES = Path("configs/prospective_study_lanes.json")
READINESS_DOC = Path("docs/PROSPECTIVE_STUDY_READINESS.md")
TEMPLATE_DOC = Path("docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md")
HISTORICAL_STATUS_PHRASE = "historical/status records"
FRESH_TARGET_PHRASE = "genuinely new term/source target set"
NO_COMPLETED_PROFILE_AS_CLAIM_PHRASE = (
    "Do not use a completed profile as a new claim-producing lane"
)
LOCK_NOT_RESULT_PHRASE = "A lock manifest is not a result"
REQUIRED_COMMANDS = (
    "python3 -m scripts.scaffold_prospective_study --list-profiles",
    "python3 -m scripts.check_prospective_study_lanes",
    "python3 -m scripts.check_preregistration_placeholders",
    "python3 -m scripts.audit_prospective_terms",
    "python3 -m scripts.preflight_prospective_study",
    "python3 -m scripts.build_study_lock_manifest",
    "python3 -m scripts.check_study_lock_manifest",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_study_lock_doc(args.doc, args.profiles)
    if failures:
        for failure in failures:
            print(f"study-lock manifests doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"study-lock manifests doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    return parser


def validate_study_lock_doc(doc: Path, profiles_path: Path) -> list[str]:
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
        TEMPLATE_DOC.as_posix(),
    )
    for link in required_links:
        if f"`{link}`" not in text:
            failures.append(f"{doc} missing link: {link}")
    for command in REQUIRED_COMMANDS:
        if command not in text:
            failures.append(f"{doc} missing command: {command}")
    for phrase in (
        FRESH_TARGET_PHRASE,
        NO_COMPLETED_PROFILE_AS_CLAIM_PHRASE,
        LOCK_NOT_RESULT_PHRASE,
    ):
        if not contains_phrase(normalized_text, phrase):
            failures.append(f"{doc} missing guard phrase: {phrase}")

    if ready:
        ready_ids = ", ".join(f"`{profile['id']}`" for profile in ready)
        if contains_phrase(normalized_text, HISTORICAL_STATUS_PHRASE):
            failures.append(
                f"{doc} says profiles are historical/status records but ready profiles show: "
                f"{ready_ids}"
            )
        for profile in ready:
            lane_id = f"`{profile['id']}`"
            if lane_id not in text:
                failures.append(f"{doc} missing ready lane id: {lane_id}")
    elif not contains_phrase(normalized_text, HISTORICAL_STATUS_PHRASE):
        failures.append(f"{doc} missing historical/status-record boundary")

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
