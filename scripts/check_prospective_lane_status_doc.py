#!/usr/bin/env python3
"""Validate generated prospective lane status doc freshness."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts import build_prospective_lane_status as lane_status
from scripts import scaffold_prospective_study as scaffold


DEFAULT_DOC = lane_status.DEFAULT_OUT
DEFAULT_PROFILES = lane_status.DEFAULT_PROFILES
EXPECTED_PROFILE_ROWS = (
    (
        "greek_surface_new_terms",
        "completed_context_cautioned_review_material",
        "terms/greek_surface_new_terms_clean_lock.csv",
        "protocols/greek_surface_new_terms.toml",
        "docs/GREEK_SURFACE_NEW_TERMS_REPORT.md",
    ),
    (
        "greek_lexicon_extension_prospective",
        "completed_context_cautioned_review_material",
        "terms/greek_lexicon_extension_terms_clean_lock.csv",
        "protocols/greek_lexicon_extension_prospective_lock.toml",
        "docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_REPORT.md",
    ),
    (
        "hebrew_modern_geopolitical_presence",
        "completed_negative_controlled_result",
        "terms/hebrew_modern_geopolitical_prospective_terms.csv",
        "protocols/hebrew_modern_geopolitical_prospective.toml",
        "docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md",
    ),
    (
        "gog_magog_pair_controls",
        "completed_negative_weak_controlled_result",
        "terms/gog_magog_pair_prospective_terms.csv",
        "protocols/gog_magog_pair_prospective.toml",
        "docs/GOG_MAGOG_PAIR_PROSPECTIVE_REPORT.md",
    ),
    (
        "compound_extension_prospective",
        "completed_negative_controlled_result",
        "terms/compound_extension_prospective_terms_clean_lock.csv",
        "protocols/compound_extension_prospective.toml",
        "docs/COMPOUND_EXTENSION_PROSPECTIVE_REPORT.md",
    ),
    (
        "hebrew_concordance_words_prospective",
        "completed_negative_controlled_result",
        "terms/hebrew_concordance_prospective_terms_clean_lock.csv",
        "protocols/hebrew_concordance_words_prospective.toml",
        "docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_REPORT.md",
    ),
    (
        "local_terms_negative_appendix",
        "completed_negative_curiosity_appendix",
        "terms/local_terms_appendix.csv",
        "protocols/local_terms_appendix.toml",
        "docs/LOCAL_TERMS_APPENDIX_REPORT.md",
    ),
    (
        "kjva_apocrypha_bridge_prospective",
        "completed_negative_controlled_result",
        "terms/kjv_apocrypha_bridge_prospective_terms.csv",
        "protocols/kjv_apocrypha_bridge_prospective_controls_5000.toml",
        "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md",
    ),
)
EXPECTED_STATUS_COUNTS = {
    "completed_context_cautioned_review_material": 2,
    "completed_negative_controlled_result": 4,
    "completed_negative_weak_controlled_result": 1,
    "completed_negative_curiosity_appendix": 1,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_lane_status_doc(args.doc, args.profiles)
    if failures:
        for failure in failures:
            print(f"prospective lane-status doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"prospective lane-status doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    return parser


def validate_lane_status_doc(doc: Path, profiles_path: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    try:
        profiles = scaffold.load_profiles(profiles_path)
    except (OSError, ValueError) as exc:
        return [f"could not read profile file {profiles_path}: {exc}"]

    failures: list[str] = []
    if profiles_path == DEFAULT_PROFILES:
        failures.extend(validate_default_profiles_json(profiles_path, profiles))
    expected = lane_status.render_markdown(profiles, Path(display_path(profiles_path)))
    actual = doc.read_text(encoding="utf-8")
    if actual != expected:
        failures.append(
            f"{doc} is stale; rerun python3 -m scripts.build_prospective_lane_status"
        )
    return failures


def validate_default_profiles_json(
    profiles_path: Path,
    profiles: list[dict[str, Any]],
) -> list[str]:
    failures: list[str] = []
    try:
        payload = json.loads(profiles_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"could not read profile JSON {profiles_path}: {exc}"]
    if not isinstance(payload.get("profiles"), list):
        failures.append(f"{profiles_path} profiles missing or not a list")
    observed_rows = tuple(
        (
            str(profile.get("id", "")),
            str(profile.get("status", "")),
            str(profile.get("term_file", "")),
            str(profile.get("protocol", "")),
            str(profile.get("report_doc", "")),
        )
        for profile in profiles
    )
    if observed_rows != EXPECTED_PROFILE_ROWS:
        failures.append(f"{profiles_path} profile rows drifted")
    status_counts = dict(Counter(row[1] for row in observed_rows))
    if status_counts != EXPECTED_STATUS_COUNTS:
        failures.append(f"{profiles_path} status counts drifted")
    return failures


def display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
