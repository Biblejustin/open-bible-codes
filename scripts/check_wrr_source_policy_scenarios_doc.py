#!/usr/bin/env python3
"""Validate WRR source-policy scenario doc stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts import analyze_wrr_source_policy_scenarios as analyzer

DEFAULT_DOC = analyzer.DEFAULT_MD
DEFAULT_SCENARIOS = analyzer.DEFAULT_OUT
DEFAULT_TERM_IMPACTS = analyzer.DEFAULT_TERM_IMPACT_OUT
DEFAULT_SCENARIO_PAIRS = analyzer.DEFAULT_PAIR_OUT
DEFAULT_MANIFEST = analyzer.DEFAULT_MANIFEST

SCENARIO_FIELDNAMES = analyzer.SUMMARY_FIELDNAMES
TERM_IMPACT_FIELDNAMES = analyzer.TERM_IMPACT_FIELDNAMES
SCENARIO_PAIR_FIELDNAMES = analyzer.PAIR_FIELDNAMES

EXPECTED_SCENARIOS = {
    "keep_all_working_source": {
        "policy_type": "baseline",
        "excluded_terms": "0",
        "excluded_pairs": "0",
        "review_only_terms": "0",
        "review_only_pairs": "0",
        "remaining_pairs": "182",
        "remaining_appellation_min_length_pairs": "165",
        "remaining_length_filtered_pairs": "86",
        "gap_to_source_cited_163_after_appellation_min_length": "-2",
        "gap_to_source_cited_163_after_length_filtered": "77",
    },
    "exclude_wnp_zacut_only": {
        "policy_type": "diagnostic_exclusion",
        "excluded_terms": "4",
        "excluded_pairs": "8",
        "review_only_terms": "0",
        "review_only_pairs": "0",
        "remaining_pairs": "174",
        "remaining_appellation_min_length_pairs": "157",
        "remaining_length_filtered_pairs": "78",
        "gap_to_source_cited_163_after_appellation_min_length": "6",
        "gap_to_source_cited_163_after_length_filtered": "85",
    },
    "exclude_book_title_only": {
        "policy_type": "diagnostic_exclusion",
        "excluded_terms": "1",
        "excluded_pairs": "1",
        "review_only_terms": "0",
        "review_only_pairs": "0",
        "remaining_pairs": "181",
        "remaining_appellation_min_length_pairs": "164",
        "remaining_length_filtered_pairs": "86",
        "gap_to_source_cited_163_after_appellation_min_length": "-1",
        "gap_to_source_cited_163_after_length_filtered": "77",
    },
    "review_chelm_spelling_only": {
        "policy_type": "review_only",
        "excluded_terms": "0",
        "excluded_pairs": "0",
        "review_only_terms": "2",
        "review_only_pairs": "2",
        "remaining_pairs": "182",
        "remaining_appellation_min_length_pairs": "165",
        "remaining_length_filtered_pairs": "86",
        "gap_to_source_cited_163_after_appellation_min_length": "-2",
        "gap_to_source_cited_163_after_length_filtered": "77",
    },
    "exclude_all_source_review_flags": {
        "policy_type": "diagnostic_exclusion",
        "excluded_terms": "7",
        "excluded_pairs": "11",
        "review_only_terms": "0",
        "review_only_pairs": "0",
        "remaining_pairs": "171",
        "remaining_appellation_min_length_pairs": "154",
        "remaining_length_filtered_pairs": "78",
        "gap_to_source_cited_163_after_appellation_min_length": "9",
        "gap_to_source_cited_163_after_length_filtered": "85",
    },
}
EXPECTED_TERM_IMPACTS = {
    "wrr2_27_app_02": ("ZKWTA", "wnp_disputed_zacut_appellation", "2", "163", "0", "true"),
    "wrr2_27_app_03": ("ZKWTW", "wnp_disputed_zacut_appellation", "2", "163", "0", "true"),
    "wrr2_27_app_05": ("M$HZKWTA", "wnp_disputed_zacut_appellation", "2", "163", "0", "true"),
    "wrr2_27_app_06": ("M$HZKWTW", "wnp_disputed_zacut_appellation", "2", "163", "0", "true"),
    "wrr2_30_app_05": ("B@LY$RLBB", "wnp_book_title_appellation_dispute", "1", "164", "-1", "false"),
    "wrr2_32_app_04": ("$LMHMXLMA", "wnp_chelm_spelling_context", "1", "164", "-1", "false"),
    "wrr2_32_app_05": ("$LMHMX@LMA", "wnp_chelm_spelling_context", "1", "164", "-1", "false"),
}
EXPECTED_SCENARIO_PAIR_COUNTS = {
    ("exclude_wnp_zacut_only", "excluded"): 8,
    ("exclude_book_title_only", "excluded"): 1,
    ("review_chelm_spelling_only", "review_only_no_exclusion"): 2,
    ("exclude_all_source_review_flags", "excluded"): 11,
}

REQUIRED_PHRASES = (
    "# WRR Source Policy Scenario Impact",
    "Status: scenario impact for selected keep_all_working_source policy.",
    "The selected working policy keeps all imported WRR2 same-record pairs; exclusion scenarios are not applied.",
    "Visual-review notes remain triage only and do not exclude pairs automatically.",
    "| keep_all_working_source | `baseline` | 0 | 0 | 165 | 86 | -2 | 77 |",
    "| exclude_wnp_zacut_only | `diagnostic_exclusion` | 8 | 0 | 157 | 78 | 6 | 85 |",
    "| exclude_all_source_review_flags | `diagnostic_exclusion` | 11 | 0 | 154 | 78 | 9 | 85 |",
    "source/title-prefix rule review; visual notes show title text without visible B@L prefix",
    "source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass",
    "## Single-Term Impact",
    "| `wrr2_27_app_02` | `ZKWTA` | `wnp_disputed_zacut_appellation` | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |",
    "`review_chelm_spelling_only` keeps pair counts stable and records review scope.",
    "Locked local WRR evidence now uses keep_all_working_source, printed D(w), full cap1000 corrected distances, and a keep-all 999,999 date-label permutation",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_policy_scenarios_doc(
        args.doc,
        args.scenarios,
        args.term_impacts,
        args.scenario_pairs,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR source-policy scenarios doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-policy scenarios doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--term-impacts", type=Path, default=DEFAULT_TERM_IMPACTS)
    parser.add_argument("--scenario-pairs", type=Path, default=DEFAULT_SCENARIO_PAIRS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_source_policy_scenarios_doc(
    doc: Path,
    scenarios: Path | None = DEFAULT_SCENARIOS,
    term_impacts: Path | None = DEFAULT_TERM_IMPACTS,
    scenario_pairs: Path | None = DEFAULT_SCENARIO_PAIRS,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]
    if scenarios is not None:
        failures.extend(validate_scenarios_csv(scenarios))
    if term_impacts is not None:
        failures.extend(validate_term_impacts_csv(term_impacts))
    if scenario_pairs is not None:
        failures.extend(validate_scenario_pairs_csv(scenario_pairs))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_scenarios_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != SCENARIO_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    by_scenario = {row.get("scenario", ""): row for row in rows}
    if set(by_scenario) != set(EXPECTED_SCENARIOS):
        failures.append(f"{path} scenario set drifted")
    for scenario, expected in EXPECTED_SCENARIOS.items():
        row = by_scenario.get(scenario)
        if row is None:
            continue
        for key, value in expected.items():
            if row.get(key) != value:
                failures.append(f"{path} {scenario} {key} drifted")
        if row.get("source_policy_selected") != "false":
            failures.append(f"{path} {scenario} selected-policy flag drifted")
        if not row.get("diagnostic_read"):
            failures.append(f"{path} {scenario} missing diagnostic read")
    return failures


def validate_term_impacts_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != TERM_IMPACT_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    by_term = {row.get("term_id", ""): row for row in rows}
    if set(by_term) != set(EXPECTED_TERM_IMPACTS):
        failures.append(f"{path} term set drifted")
    for term_id, expected in EXPECTED_TERM_IMPACTS.items():
        row = by_term.get(term_id)
        if row is None:
            continue
        term, flags, affected, remaining, gap, closes = expected
        checks = {
            "term": term,
            "flags": flags,
            "affected_pairs": affected,
            "remaining_appellation_min_length_pairs_if_excluded": remaining,
            "gap_to_source_cited_163_after_appellation_min_length_if_excluded": gap,
            "closes_appellation_min_length_gap_to_163": closes,
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} {term_id} {key} drifted")
        if row.get("term_side") != "appellation":
            failures.append(f"{path} {term_id} term side drifted")
    return failures


def validate_scenario_pairs_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != SCENARIO_PAIR_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    counter = Counter(
        (row.get("scenario", ""), row.get("scenario_action", "")) for row in rows
    )
    if dict(counter) != EXPECTED_SCENARIO_PAIR_COUNTS:
        failures.append(f"{path} scenario/action counts drifted")
    if len(rows) != sum(EXPECTED_SCENARIO_PAIR_COUNTS.values()):
        failures.append(f"{path} row count drifted")
    for row in rows:
        if row.get("pair_review_status") not in {
            "diagnostic_exclusion_candidate_not_locked",
            "needs_primary_source_pair_rule",
        }:
            failures.append(f"{path} {row.get('pair_id', '')} review status drifted")
        if not row.get("source_review_flags") or not row.get("flagged_term_ids"):
            failures.append(f"{path} {row.get('pair_id', '')} missing flags")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "analyze_wrr_source_policy_scenarios.py",
        "inputs": {
            "pair_table": str(analyzer.DEFAULT_PAIR_TABLE),
            "source_queue": str(analyzer.DEFAULT_SOURCE_QUEUE),
        },
        "expected_published_pairs": 163,
        "scenarios": list(EXPECTED_SCENARIOS),
        "flagged_terms": len(EXPECTED_TERM_IMPACTS),
        "impact_rows": sum(EXPECTED_SCENARIO_PAIR_COUNTS.values()),
        "term_impact_rows": len(EXPECTED_TERM_IMPACTS),
        "outputs": {
            "csv": str(DEFAULT_SCENARIOS),
            "pair_csv": str(DEFAULT_SCENARIO_PAIRS),
            "term_impact_csv": str(DEFAULT_TERM_IMPACTS),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{manifest} {key} drifted")
    return failures


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
