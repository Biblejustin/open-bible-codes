#!/usr/bin/env python3
"""Validate WRR manual-decision record worksheet reports lock status safely."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_manual_decision_record_worksheet as builder

DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_WORKSHEET = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

FIELDNAMES = builder.FIELDNAMES

ALLOWED_WITHOUT_INPUT = "organize evidence only"
SUGGESTED_STATUS_VALUES = (
    "accepted_keep;accepted_correction;accepted_exclusion;accepted_method_lock;"
    "deferred_no_lock"
)

LANE_LOCKS = {
    "source_policy_pair_rule": {
        "rows": 1,
        "review_state": "pending_source_policy_pair_rule_lock",
        "source_checklist": "docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md",
        "required_decision_record": (
            "cited source/pair-rule decision for Chełm forms before changing source lock"
        ),
        "evidence_prompt": (
            "cite primary source and pair-rule evidence before changing the working source"
        ),
        "suggested_actions": (
            "no_source_change;source_policy_correction;pair_rule_change;deferred_no_lock"
        ),
        "record_action": "no_source_change",
    },
    "source_transcription_row_cluster": {
        "rows": 22,
        "review_state": "pending_manual_source_lock",
        "source_checklist": "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md",
        "required_decision_record": (
            "explicit keep, correct, exclude, or method/pair-universe decision "
            "recorded outside this checklist"
        ),
        "evidence_prompt": (
            "cite row image or source-list transcription plus row/column alignment evidence"
        ),
        "suggested_actions": (
            "no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock"
        ),
        "record_action": "no_source_change",
    },
    "page_image_near_match": {
        "rows": 3,
        "review_state": "pending_page_image_lock",
        "source_checklist": "docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md",
        "required_decision_record": (
            "explicit page-image transcription decision with cited image evidence"
        ),
        "evidence_prompt": "cite page-image transcription evidence",
        "suggested_actions": (
            "no_source_change;source_correction;pair_exclusion;deferred_no_lock"
        ),
        "record_action": "no_source_change",
    },
    "method_pair_universe": {
        "rows": 11,
        "review_state": "pending_method_pair_universe_lock",
        "source_checklist": "docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md",
        "required_decision_record": (
            "explicit method or pair-universe decision explaining zero ordinary hits"
        ),
        "evidence_prompt": (
            "explain zero ordinary hits with explicit method or pair-universe evidence"
        ),
        "suggested_actions": (
            "method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock"
        ),
        "record_action": "method_lock",
    },
}

EXPECTED_ACTION_COUNTS = {"method_lock": 11, "no_source_change": 26}

REQUIRED_PHRASES = (
    "# WRR Manual Decision Record Worksheet",
    "Status: worksheet plus current WRR manual decision-record status.",
    "It reads `data/study/mappings/wrr_manual_decision_records.csv` but does not update it.",
    "Record rows document manual locks; this worksheet does not mutate source rows, method rules, replacement choices, or pair membership.",
    "- Worksheet rows: 37.",
    "- Source-policy/pair-rule rows: 1.",
    "- Source-transcription row-cluster rows: 22.",
    "- Page-image rows: 3.",
    "- Method/pair-universe rows: 11.",
    "- Target records file: `data/study/mappings/wrr_manual_decision_records.csv`.",
    "- Recorded decision rows: 37.",
    "- Locked decision rows: 37.",
    "- Unrecorded decision rows: 0.",
    "- Recorded selected actions: method_lock=11; no_source_change=26.",
    "The worksheet gives exact `decision_id`, register fields, and current record fields when a lock row exists.",
    "Locked rows are evidence records. Working-source changes, replacement locks, and pair exclusions remain absent unless `selected_action` names them.",
    "`decision_id,register_decision_rank,decision_lane,review_state,decision_target,source_checklist,decision_status,selected_action,evidence_citation,evidence_summary,locked_by,locked_at,notes`",
    "method_lock",
    "no_source_change",
    "`wrr_decision_001`",
    "`wrr_decision_037`",
)

FORBIDDEN_PHRASES = (
    "selected correction",
    "selected exclusion",
    "source corrected to",
    "pair excluded",
    "replacement locked",
    "method changed to",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_worksheet_doc(args.doc, args.worksheet, args.manifest)
    if failures:
        for failure in failures:
            print(f"WRR manual decision record worksheet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR manual decision record worksheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--worksheet", type=Path, default=DEFAULT_WORKSHEET)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_worksheet_doc(
    doc: Path,
    worksheet: Path | None = DEFAULT_WORKSHEET,
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
    failures.extend(
        f"{doc} contains forbidden phrase: {phrase}"
        for phrase in FORBIDDEN_PHRASES
        if phrase in normalized_text
    )
    if worksheet is not None:
        failures.extend(validate_worksheet_csv(worksheet))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_worksheet_csv(worksheet: Path) -> list[str]:
    data = _read_csv(worksheet)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != FIELDNAMES:
        failures.append(f"{worksheet} fieldnames drifted")
    expected_rows = sum(int(locks["rows"]) for locks in LANE_LOCKS.values())
    if len(rows) != expected_rows:
        failures.append(f"{worksheet} has {len(rows)} rows; expected {expected_rows}")
    expected_ids = [f"wrr_decision_{index:03d}" for index in range(1, expected_rows + 1)]
    if [row.get("decision_id", "") for row in rows] != expected_ids:
        failures.append(f"{worksheet} decision_id sequence drifted")
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if [row.get("register_decision_rank", "") for row in rows] != expected_ranks:
        failures.append(f"{worksheet} register rank sequence drifted")

    action_counts = {
        action: sum(1 for row in rows if row.get("record_selected_action") == action)
        for action in EXPECTED_ACTION_COUNTS
    }
    for action, expected in EXPECTED_ACTION_COUNTS.items():
        if action_counts[action] != expected:
            failures.append(f"{worksheet} {action} count={action_counts[action]}")

    for lane, locks in LANE_LOCKS.items():
        lane_rows = [row for row in rows if row.get("decision_lane") == lane]
        failures.extend(_validate_lane_rows(worksheet, lane, lane_rows, locks))
    known_lanes = set(LANE_LOCKS)
    for row in rows:
        decision_id = row.get("decision_id", "")
        if row.get("decision_lane") not in known_lanes:
            failures.append(f"{worksheet} {decision_id} unknown lane")
        if row.get("suggested_decision_status_values") != SUGGESTED_STATUS_VALUES:
            failures.append(f"{worksheet} {decision_id} status values drifted")
        if row.get("allowed_without_input") != ALLOWED_WITHOUT_INPUT:
            failures.append(f"{worksheet} {decision_id} allowed action drifted")
        if row.get("record_decision_status") != "locked":
            failures.append(f"{worksheet} {decision_id} record status drifted")
        if row.get("record_locked_by") != "Justin Scaggs":
            failures.append(f"{worksheet} {decision_id} locked_by drifted")
        if row.get("record_locked_at") != "2026-05-25":
            failures.append(f"{worksheet} {decision_id} locked_at drifted")
        if not row.get("record_evidence_citation") or not row.get("record_evidence_summary"):
            failures.append(f"{worksheet} {decision_id} missing evidence record")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected_rows = sum(int(locks["rows"]) for locks in LANE_LOCKS.values())
    expected = {
        "tool": "build_wrr_manual_decision_record_worksheet",
        "rows": expected_rows,
        "lane_counts": {
            lane: int(locks["rows"])
            for lane, locks in sorted(LANE_LOCKS.items())
        },
        "recorded_rows": expected_rows,
        "locked_rows": expected_rows,
        "unrecorded_rows": 0,
        "record_status_counts": {"locked": expected_rows},
        "recorded_action_counts": dict(sorted(EXPECTED_ACTION_COUNTS.items())),
        "inputs": {
            "register": str(builder.DEFAULT_REGISTER),
            "records_template": str(builder.DEFAULT_RECORDS_TEMPLATE),
        },
        "outputs": {
            "out": str(DEFAULT_WORKSHEET),
            "markdown_out": str(DEFAULT_DOC),
            "manifest_out": str(DEFAULT_MANIFEST),
        },
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{manifest} {key} drifted")
    return failures


def _validate_lane_rows(
    worksheet: Path,
    lane: str,
    rows: list[dict[str, str]],
    locks: dict[str, object],
) -> list[str]:
    failures: list[str] = []
    if len(rows) != locks["rows"]:
        failures.append(f"{worksheet} {lane} has {len(rows)} rows")
    for row in rows:
        decision_id = row.get("decision_id", "")
        for key in (
            "review_state",
            "source_checklist",
            "required_decision_record",
            "evidence_prompt",
        ):
            if row.get(key) != locks[key]:
                failures.append(f"{worksheet} {decision_id} {key} drifted")
        if row.get("suggested_selected_action_values") != locks["suggested_actions"]:
            failures.append(f"{worksheet} {decision_id} suggested actions drifted")
        if row.get("record_selected_action") != locks["record_action"]:
            failures.append(f"{worksheet} {decision_id} selected action drifted")
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
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"{path} is invalid JSON: {exc}"
    if not isinstance(data, dict):
        return f"{path} JSON root must be an object"
    return data


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
