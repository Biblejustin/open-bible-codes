#!/usr/bin/env python3
"""Validate Hakkaac KJVA Apocrypha boundary-candidate audit."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import analyze_kjva_hakkaac_apocrypha_boundary_candidate as audit


DEFAULT_DOC = audit.DEFAULT_MD
DEFAULT_ROWS = audit.DEFAULT_ROWS
DEFAULT_SUMMARY = audit.DEFAULT_SUMMARY
DEFAULT_MANIFEST = audit.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA Hakkaac Apocrypha Boundary Candidate",
    "Status: candidate audit only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "not a result-bearing replication",
    "does not commit Bible text, normalize Bible text, create a local corpus",
    "Pages scanned: 2.",
    "Pages with public-domain note: 2.",
    "Sirach 44 marker count: 23.",
    "Sirach 44 has marker 23: 1.",
    "Prayer of Manasseh marker count: 15.",
    "Prayer of Manasseh has markers 1..15: 1.",
    "Candidate resolves Sirach blocker: 1.",
    "Candidate resolves Prayer blocker: 1.",
    "Source-lock ready: 0.",
    "Result-ready sources: 0.",
    "Claim status: `candidate_audit_only_not_result_bearing`.",
    "`sirach_marker_gap_candidate_not_source_lock`",
    "`prayer_boundary_candidate_not_source_lock`",
    "No Bible text is written to tracked outputs.",
    "does not change KJVA bridge result status",
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
    failures = validate_kjva_hakkaac_apocrypha_boundary_candidate_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA Hakkaac boundary candidate failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA Hakkaac boundary candidate ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_hakkaac_apocrypha_boundary_candidate_doc(
    doc: Path = DEFAULT_DOC,
    *,
    rows: Path | None = DEFAULT_ROWS,
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
    if rows is not None:
        failures.extend(validate_rows_csv(rows))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_rows_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != audit.ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 2:
        failures.append(f"{path} expected 2 marker rows, found {len(rows)}")
        return failures
    by_id = {row["page_id"]: row for row in rows}
    sirach = by_id.get("hakkaac_sirach_44", {})
    prayer = by_id.get("hakkaac_manasseh_1", {})
    expected = {
        "hakkaac_sirach_44": {
            "book": "SIR",
            "marker_count": "23",
            "markers_present": "1..23",
            "target_markers": "23",
            "target_status": "all_target_markers_present",
            "candidate_status": "sirach_marker_gap_candidate_not_source_lock",
        },
        "hakkaac_manasseh_1": {
            "book": "MAN",
            "marker_count": "15",
            "markers_present": "1..15",
            "target_markers": "1..15",
            "target_status": "all_target_markers_present",
            "candidate_status": "prayer_boundary_candidate_not_source_lock",
        },
    }
    for row_id, checks in expected.items():
        row = by_id.get(row_id)
        if row is None:
            failures.append(f"{path} missing row {row_id}")
            continue
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} {row_id} {key} drifted: {row.get(key)!r}")
    if sirach.get("license_note_present") != "True":
        failures.append(f"{path} Sirach license note drifted")
    if prayer.get("license_note_present") != "True":
        failures.append(f"{path} Prayer license note drifted")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != audit.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "pages_scanned": "2",
        "license_note_pages": "2",
        "sirach_44_marker_count": "23",
        "sirach_44_has_23": "True",
        "prayer_marker_count": "15",
        "prayer_has_1_to_15": "True",
        "candidate_resolves_sirach": "True",
        "candidate_resolves_prayer": "True",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "candidate_audit_only_not_result_bearing",
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
    if payload.get("claim_boundary") != "candidate audit only; no ELS result":
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
