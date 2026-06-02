#!/usr/bin/env python3
"""Validate consolidated no-input blocker summary boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_no_input_blocker_summary as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_STATUS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

REQUIRED_LANES = {"wrr", "cities", "kjva"}
REQUIRED_PHRASES = (
    "# No-Input Blocker Summary",
    "Status: consolidated blocker map.",
    "not a new result",
    "not a statistical claim",
    "not a source-text lock",
    "not permission to run result-bearing follow-ups",
    "Lane rows: 3.",
    "Total status rows: 26.",
    "Total manual-input-needed rows: 22.",
    "Result-allowed lanes: 0.",
    "Blocked result lanes: 3.",
    "WRR remaining defined-distance gap: 91.",
    "Cities pending transcription rows: 14.",
    "KJVA blocked next-result gates: 10.",
    "`no_result_bearing_work_without_manual_or_citable_input`",
    "WRR exact-reproduction follow-up",
    "Cities source-row follow-up",
    "KJVA independent-source follow-up",
    "Citable source policy or human-readable source review is still required.",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"(?:result allowed:\s*[1-9]|new result allowed|new result selected|"
    r"statistical claim selected|source-text lock selected|"
    r"permission granted to run result-bearing)",
    re.IGNORECASE,
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_no_input_blocker_summary_doc(
        args.doc,
        status=args.status,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"no-input blocker summary failure: {failure}", file=sys.stderr)
        return 1
    print(f"no-input blocker summary ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_no_input_blocker_summary_doc(
    doc: Path = DEFAULT_DOC,
    *,
    status: Path | None = DEFAULT_STATUS,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures: list[str] = []
    for phrase in REQUIRED_PHRASES:
        if normalize_space(phrase) not in normalized:
            failures.append(f"{doc} missing phrase: {phrase}")
    for match in FORBIDDEN_OVERCLAIM_RE.finditer(text):
        if match.group(0).lower().startswith("result allowed: 0"):
            continue
        line = text.count("\n", 0, match.start()) + 1
        failures.append(f"{doc}:{line} overclaim phrase: {match.group(0)!r}")
    if status is not None:
        failures.extend(validate_status_csv(status))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_status_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.LANE_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 3:
        failures.append(f"{path} expected 3 lane rows, found {len(rows)}")
    lane_ids = {row.get("lane_id") for row in rows}
    for lane_id in REQUIRED_LANES:
        if lane_id not in lane_ids:
            failures.append(f"{path} missing lane {lane_id}")
    if any(row.get("result_allowed") != "0" for row in rows):
        failures.append(f"{path} expected every result_allowed value to be 0")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "lane_rows": "3",
        "total_status_rows": "26",
        "total_manual_input_needed_rows": "22",
        "result_allowed_lanes": "0",
        "blocked_result_lanes": "3",
        "wrr_remaining_gap": "91",
        "cities_pending_transcription_rows": "14",
        "kjva_blocked_gate_rows": "10",
        "claim_boundary": builder.CLAIM_BOUNDARY,
    }
    row = rows[0]
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
    return failures


def validate_manifest(path: Path, *, doc: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path} is invalid JSON: {exc}"]
    failures: list[str] = []
    if payload.get("tool") != "scripts.build_no_input_blocker_summary":
        failures.append(f"{path} tool drifted")
    if payload.get("claim_boundary") != "no-input blocker summary only; no result-bearing output":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "no Bible text written to tracked outputs":
        failures.append(f"{path} text_retention drifted")
    if payload.get("summary", {}).get("result_allowed_lanes") != 0:
        failures.append(f"{path} summary.result_allowed_lanes drifted")
    outputs = payload.get("outputs", {})
    if not isinstance(outputs, dict) or outputs.get("markdown") != str(doc):
        failures.append(f"{path} markdown output drifted")
    return failures


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
