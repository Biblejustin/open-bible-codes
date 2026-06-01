#!/usr/bin/env python3
"""Validate KJVA source-policy blocker packet boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_kjva_source_policy_blocker_packet as packet


DEFAULT_DOC = packet.DEFAULT_MD
DEFAULT_OPTIONS = packet.DEFAULT_OPTIONS
DEFAULT_BLOCKERS = packet.DEFAULT_BLOCKERS
DEFAULT_SUMMARY = packet.DEFAULT_SUMMARY
DEFAULT_MANIFEST = packet.DEFAULT_MANIFEST

REQUIRED_OPTION_IDS = {
    "current_ebible_rerun_only",
    "project_gutenberg_only_candidate",
    "project_gutenberg_hakkaac_split_candidate",
    "hakkaac_primary_stream",
    "defer_new_kjva_replication",
}
REQUIRED_BLOCKER_IDS = {
    "source_use_policy_lock",
    "gutenberg_sirach_44_23_marker_gap",
    "gutenberg_prayer_of_manasseh_boundary",
    "hakkaac_sirach_19_1_length_drift",
    "verse_map_and_collation_lock",
    "term_control_study_lock",
    "role_sidecar_complete_but_not_sufficient",
}
REQUIRED_PHRASES = (
    "# KJVA Source Policy Blocker Packet",
    "Status: source-policy blocker packet only.",
    "not an ELS result",
    "not a corpus import",
    "not a source-use approval",
    "not a source lock",
    "not a result-bearing replication",
    "does not commit Bible text",
    "Policy option rows: 5.",
    "Blocker rows: 7.",
    "Policy-ready options: 2.",
    "Blocked options: 3.",
    "Checksum records ready: 2.",
    "Split-source role sidecar written: 1.",
    "Current rerun locked: 1.",
    "Source-use ready pages: 0.",
    "Gutenberg Sirach gap refs: `SIR 44:23`.",
    "Gutenberg Prayer of Manasseh markers: 0/15.",
    "Hakkaac length-drift verses: 1.",
    "Source-lock ready: 0.",
    "Result-ready: 0.",
    "`source_policy_blocker_packet_only_not_result_bearing`",
    "`current_ebible_rerun_only`",
    "`project_gutenberg_only_candidate`",
    "`project_gutenberg_hakkaac_split_candidate`",
    "`hakkaac_primary_stream`",
    "`defer_new_kjva_replication`",
    "`source_use_policy_lock`",
    "`gutenberg_sirach_44_23_marker_gap`",
    "`gutenberg_prayer_of_manasseh_boundary`",
    "`hakkaac_sirach_19_1_length_drift`",
    "`verse_map_and_collation_lock`",
    "`term_control_study_lock`",
    "`role_sidecar_complete_but_not_sufficient`",
    "The only policy-ready path here is current-source rerun and continued deferral",
    "Any new independent KJVA result run still needs source-use, source-text",
    "No Bible text is written to tracked outputs.",
    "does not change any KJVA bridge result status",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:source-lock ready|source-use approved|result-bearing replication is ready|"
    r"claim report|claim-level|proved|proves|proof|conclusive evidence|"
    r"significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Source-lock ready: 0.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_source_policy_blocker_packet_doc(
        args.doc,
        options=args.options,
        blockers=args.blockers,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA source-policy blocker packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA source-policy blocker packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--options", type=Path, default=DEFAULT_OPTIONS)
    parser.add_argument("--blockers", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_source_policy_blocker_packet_doc(
    doc: Path = DEFAULT_DOC,
    *,
    options: Path | None = DEFAULT_OPTIONS,
    blockers: Path | None = DEFAULT_BLOCKERS,
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
    failures.extend(validate_no_overclaim(doc, text))
    if options is not None:
        failures.extend(validate_options_csv(options))
    if blockers is not None:
        failures.extend(validate_blockers_csv(blockers))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_options_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != packet.OPTION_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 5:
        failures.append(f"{path} expected 5 option rows, found {len(rows)}")
    ids = {row.get("option_id") for row in rows}
    for option_id in REQUIRED_OPTION_IDS:
        if option_id not in ids:
            failures.append(f"{path} missing option row {option_id}")
    statuses = [row.get("status") for row in rows]
    if statuses.count("policy_ready") != 2:
        failures.append(f"{path} expected 2 policy_ready options")
    if statuses.count("blocked") != 3:
        failures.append(f"{path} expected 3 blocked options")
    for row in rows:
        if row.get("result_boundary") != "not_result_bearing":
            failures.append(f"{path} {row.get('option_id')} result_boundary drifted")
    return failures


def validate_blockers_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != packet.BLOCKER_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 7:
        failures.append(f"{path} expected 7 blocker rows, found {len(rows)}")
    ids = {row.get("blocker_id") for row in rows}
    for blocker_id in REQUIRED_BLOCKER_IDS:
        if blocker_id not in ids:
            failures.append(f"{path} missing blocker row {blocker_id}")
    if {row.get("result_boundary") for row in rows} != {"not_result_bearing"}:
        failures.append(f"{path} result_boundary drifted")
    if not any(row.get("status") == "closed_as_planning_only" for row in rows):
        failures.append(f"{path} expected planning-only closed blocker row")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != packet.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "policy_option_rows": "5",
        "blocker_rows": "7",
        "policy_ready_options": "2",
        "blocked_options": "3",
        "checksum_records_ready": "2",
        "split_source_role_sidecar_written": "True",
        "current_rerun_locked": "True",
        "source_use_ready_pages": "0",
        "gutenberg_sirach_gap_refs": "SIR 44:23",
        "gutenberg_manasseh_source_markers": "0",
        "gutenberg_manasseh_local_markers": "15",
        "hakkaac_length_drift_verses": "1",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "source_policy_blocker_packet_only_not_result_bearing",
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
    if payload.get("claim_boundary") != "source-policy blocker packet only; no ELS result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "no Bible text written to tracked outputs":
        failures.append(f"{path} text_retention drifted")
    if payload.get("summary", {}).get("result_ready") is not False:
        failures.append(f"{path} summary.result_ready drifted")
    outputs = payload.get("outputs", {})
    markdown = outputs.get("markdown") if isinstance(outputs, dict) else None
    allowed_markdown_paths = {str(doc)}
    try:
        allowed_markdown_paths.add(str(doc.relative_to(Path.cwd())))
    except ValueError:
        pass
    if markdown not in allowed_markdown_paths:
        failures.append(f"{path} markdown output drifted")
    return failures


def validate_no_overclaim(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    for match in FORBIDDEN_OVERCLAIM_RE.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        line_text = text.splitlines()[line - 1].strip()
        if any(context in line_text for context in ALLOWED_FORBIDDEN_CONTEXTS):
            continue
        failures.append(f"{path}:{line} overclaim phrase: {match.group(0)!r}")
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
