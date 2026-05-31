#!/usr/bin/env python3
"""Validate Project Gutenberg KJVA source-lock blocker packet boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_kjva_gutenberg_source_lock_blocker_packet as packet


DEFAULT_DOC = packet.DEFAULT_MD
DEFAULT_MARKER_DIFF = packet.DEFAULT_MARKER_DIFF
DEFAULT_BOUNDARY_OPTIONS = packet.DEFAULT_BOUNDARY_OPTIONS
DEFAULT_SUMMARY = packet.DEFAULT_SUMMARY
DEFAULT_MANIFEST = packet.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA Gutenberg Source-Lock Blocker Packet",
    "Status: blocker packet only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "not a result-bearing replication",
    "does not commit Bible text, normalize Bible text, create a local corpus",
    "Sirach source markers: 1392.",
    "Sirach local markers: 1393.",
    "Sirach missing source markers: 1.",
    "Sirach extra source markers: 0.",
    "Sirach gap: `SIR 44:23`.",
    "Prayer of Manasseh source section detected: 1.",
    "Prayer of Manasseh source markers: 0.",
    "Local Prayer of Manasseh markers: 15.",
    "Source-lock ready: 0.",
    "Result-ready sources: 0.",
    "Claim status: `blocker_packet_only_not_result_bearing`.",
    "`SIR 44:23`",
    "`missing_source_marker`",
    "`sirach_defer_until_citable_collation`",
    "`manasseh_defer_until_citable_marked_source`",
    "No Bible text is written to tracked outputs.",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:source-lock ready|result-bearing replication is ready|claim report|"
    r"claim-level|proved|proves|proof|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Source-lock ready: 0.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_gutenberg_source_lock_blocker_packet_doc(
        args.doc,
        marker_diff=args.marker_diff,
        boundary_options=args.boundary_options,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(
                f"KJVA Gutenberg source-lock blocker packet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"KJVA Gutenberg source-lock blocker packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--marker-diff", type=Path, default=DEFAULT_MARKER_DIFF)
    parser.add_argument(
        "--boundary-options",
        type=Path,
        default=DEFAULT_BOUNDARY_OPTIONS,
    )
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_gutenberg_source_lock_blocker_packet_doc(
    doc: Path = DEFAULT_DOC,
    *,
    marker_diff: Path | None = DEFAULT_MARKER_DIFF,
    boundary_options: Path | None = DEFAULT_BOUNDARY_OPTIONS,
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
    if marker_diff is not None:
        failures.extend(validate_marker_diff_csv(marker_diff))
    if boundary_options is not None:
        failures.extend(validate_boundary_options_csv(boundary_options))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_marker_diff_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != packet.MARKER_DIFF_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 marker-diff row, found {len(rows)}")
        return failures
    row = rows[0]
    expected = {
        "book": "SIR",
        "local_ref": "SIR 44:23",
        "chapter": "44",
        "verse": "23",
        "status": "missing_source_marker",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
    if "SIR 44:22" not in row.get("previous_source_marker", ""):
        failures.append(f"{path} previous_source_marker drifted")
    if "SIR 45:1" not in row.get("next_source_marker", ""):
        failures.append(f"{path} next_source_marker drifted")
    return failures


def validate_boundary_options_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != packet.BOUNDARY_OPTION_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 5:
        failures.append(f"{path} expected 5 boundary option rows, found {len(rows)}")
    option_ids = {row["option_id"] for row in rows}
    for required in {
        "sirach_defer_until_citable_collation",
        "sirach_do_not_auto_insert_marker",
        "manasseh_defer_until_citable_marked_source",
        "manasseh_exclude_until_policy_lock",
        "manasseh_manual_split_requires_review",
    }:
        if required not in option_ids:
            failures.append(f"{path} missing option {required}")
    if any(row.get("result_boundary") != "not_result_bearing" for row in rows):
        failures.append(f"{path} has result-bearing option row")
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
        "raw_text_retained": "False",
        "sirach_source_markers": "1392",
        "sirach_local_markers": "1393",
        "sirach_missing_source_marker_count": "1",
        "sirach_extra_source_marker_count": "0",
        "sirach_gap_refs": "SIR 44:23",
        "manasseh_source_section_detected": "True",
        "manasseh_source_markers": "0",
        "manasseh_local_markers": "15",
        "manasseh_boundary_option_rows": "3",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "blocker_packet_only_not_result_bearing",
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
    if payload.get("claim_boundary") != "blocker packet only; no ELS result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "no Bible text written to tracked outputs":
        failures.append(f"{path} text_retention drifted")
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
