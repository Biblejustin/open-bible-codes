#!/usr/bin/env python3
"""Validate prospective study lane profiles."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from scripts import scaffold_prospective_study as scaffold


DEFAULT_PROFILE_FILE = Path("configs/prospective_study_lanes.json")
REQUIRED_FIELDS = [
    "id",
    "title",
    "status",
    "language",
    "term_file",
    "protocol",
    "report_doc",
    "sources",
    "skip_range",
    "direction",
    "min_normalized_length",
    "candidate_type",
    "context_rule",
    "controls",
    "correction",
    "source_term_files",
    "dedupe_rule",
    "excluded_prior",
    "candidate_rule",
    "primary_row_outcome",
    "primary_study_outcome",
]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_profiles(args.profile_file)
    if failures:
        for failure in failures:
            print(f"profile validation failure: {failure}")
        return 1
    print(f"profile validation passed: {args.profile_file}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile_file", type=Path, nargs="?", default=DEFAULT_PROFILE_FILE)
    return parser


def validate_profiles(path: Path) -> list[str]:
    failures: list[str] = []
    try:
        profiles = scaffold.load_profiles(path)
    except (OSError, ValueError) as exc:
        return [f"could not read profile file {path}: {exc}"]
    seen: set[str] = set()
    for index, profile in enumerate(profiles, start=1):
        profile_id = str(profile.get("id", f"row_{index}"))
        failures.extend(validate_profile(profile, profile_id=profile_id))
        if profile_id in seen:
            failures.append(f"{profile_id}: duplicate id")
        seen.add(profile_id)
    if not profiles:
        failures.append("profile file contains no profiles")
    return failures


def validate_profile(profile: dict[str, Any], *, profile_id: str) -> list[str]:
    failures: list[str] = []
    for field in REQUIRED_FIELDS:
        if missing(profile.get(field)):
            failures.append(f"{profile_id}: missing {field}")
    try:
        normalized_id = scaffold.normalize_name(profile_id)
    except ValueError as exc:
        failures.append(f"{profile_id}: invalid id: {exc}")
    else:
        if normalized_id != profile_id:
            failures.append(f"{profile_id}: id must already be normalized")
    failures.extend(validate_path_prefix(profile, profile_id, "term_file", "terms/"))
    failures.extend(validate_path_prefix(profile, profile_id, "protocol", "protocols/"))
    failures.extend(validate_path_prefix(profile, profile_id, "report_doc", "docs/"))
    sources = profile.get("sources", [])
    if isinstance(sources, list):
        for source_index, source in enumerate(sources, start=1):
            failures.extend(validate_source(source, profile_id, source_index))
    else:
        failures.append(f"{profile_id}: sources must be a list")
    return failures


def validate_path_prefix(
    profile: dict[str, Any],
    profile_id: str,
    field: str,
    prefix: str,
) -> list[str]:
    value = profile.get(field)
    if missing(value):
        return []
    text = str(value)
    if not text.startswith(prefix):
        return [f"{profile_id}: {field} must start with {prefix}"]
    return []


def validate_source(source: Any, profile_id: str, source_index: int) -> list[str]:
    if not isinstance(source, dict):
        return [f"{profile_id}: source {source_index} must be an object"]
    label = source.get("label")
    path = source.get("path")
    failures = []
    if missing(label):
        failures.append(f"{profile_id}: source {source_index} missing label")
    if missing(path):
        failures.append(f"{profile_id}: source {source_index} missing path")
        return failures
    if not Path(str(path)).exists():
        failures.append(f"{profile_id}: source path missing: {path}")
    return failures


def missing(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, list) and not value:
        return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
