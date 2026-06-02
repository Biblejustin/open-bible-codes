#!/usr/bin/env python3
"""Validate missing research model page audit doc keeps source limits explicit."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_DOC = Path("docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md")
DEFAULT_ROWS = Path("reports/wrr_1994/research_missing_model_pages.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/research_missing_model_pages_summary.csv")
DEFAULT_MANIFEST = Path("reports/wrr_1994/research_missing_model_pages.manifest.json")

EXPECTED_ROW_FIELDNAMES = [
    "model_page",
    "path",
    "requested_url",
    "bytes",
    "sha256",
    "title",
    "canonical",
    "expected_label",
    "expected_label_present",
    "canonical_is_root",
    "spam_marker_present",
    "usable_status",
]
EXPECTED_MODEL_ROWS = {
    "geometric_model_level_2": (
        "https://www.torah-code.org/research/research_3a.html",
        "Geometric Model Level 2",
        "reports/wrr_1994/torah_code_research_geometric_model_level_2.html",
    ),
    "geometric_model_level_3": (
        "https://www.torah-code.org/research/research_3b.html",
        "Geometric Model Level 3",
        "reports/wrr_1994/torah_code_research_geometric_model_level_3.html",
    ),
    "els_model_level_2": (
        "https://www.torah-code.org/research/research_3d.html",
        "ELS Model Level 2",
        "reports/wrr_1994/torah_code_research_els_model_level_2.html",
    ),
    "els_model_level_3": (
        "https://www.torah-code.org/research/research_3e.html",
        "ELS Model Level 3",
        "reports/wrr_1994/torah_code_research_els_model_level_3.html",
    ),
}
EXPECTED_BYTES = "629155"
EXPECTED_SHA256 = "d60a59519b55bcff8b6a287eab9c7b06113e0967e95b362cfccaeb66d9cb84f4"
EXPECTED_TITLE = (
    "Daftar Bet Kecil 100, 200, 300, 500 Perak - Agen Slot Bet Kecil "
    "Deposit Via Pulsa 5000 Terjangkau"
)
EXPECTED_CANONICAL = "https://www.torah-code.org/"
EXPECTED_USABLE_STATUS = "unusable_redirect_or_root_content"
EXPECTED_SUMMARY = {
    "source_files": "4",
    "overview_expected_level23_links": "4",
    "expected_label_present_files": "0",
    "root_canonical_files": "4",
    "spam_marker_files": "4",
    "usable_model_pages": "0",
    "adjacent_source_files": "2",
    "adjacent_expected_label_present_files": "2",
    "adjacent_spam_marker_files": "0",
    "adjacent_usable_model_pages": "2",
    "claim_status": "source_status_only_not_data_bearing",
}
EXPECTED_CLAIM_BOUNDARY = "source-status audit only; no ELS result"
EXPECTED_ANCHOR_STATUS_COUNTS = {"found": 8}

REQUIRED_PHRASES = (
    "# Research Missing Model Pages Audit",
    "Status: source-status audit only.",
    "not an ELS result",
    "not a claim-ready model reconstruction",
    "| downloaded source files | 4 |",
    "| overview level-2/3 links | 4 |",
    "| files containing expected model labels | 0 |",
    "| files declaring root canonical URL | 4 |",
    "| files with unrelated slot/gambling markers | 4 |",
    "| usable level-2/3 model pages | 0 |",
    "| adjacent level-1 source files | 2 |",
    "| usable adjacent level-1 model pages | 2 |",
    "Treat these four levels as missing source material",
    "until clean Torah-code research pages are recovered and checksummed.",
    "the missing level-2/3 model rules.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_research_missing_model_pages_audit_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"research missing model pages audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"research missing model pages audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_research_missing_model_pages_audit_doc(
    doc: Path,
    *,
    rows: Path | None = DEFAULT_ROWS,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    if rows is not None:
        failures.extend(validate_rows_csv(rows))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_rows_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != EXPECTED_ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != len(EXPECTED_MODEL_ROWS):
        failures.append(f"{path} has {len(rows)} rows; expected 4")
    observed_model_pages = [row.get("model_page", "") for row in rows]
    if observed_model_pages != list(EXPECTED_MODEL_ROWS):
        failures.append(f"{path} model_page order drifted")
    by_model = {row.get("model_page", ""): row for row in rows}
    for model_page, (url, label, expected_path) in EXPECTED_MODEL_ROWS.items():
        row = by_model.get(model_page)
        if row is None:
            failures.append(f"{path} missing row {model_page}")
            continue
        checks = {
            "path": expected_path,
            "requested_url": url,
            "bytes": EXPECTED_BYTES,
            "sha256": EXPECTED_SHA256,
            "title": EXPECTED_TITLE,
            "canonical": EXPECTED_CANONICAL,
            "expected_label": label,
            "expected_label_present": "False",
            "canonical_is_root": "True",
            "spam_marker_present": "True",
            "usable_status": EXPECTED_USABLE_STATUS,
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} {model_page} {key} drifted")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != list(EXPECTED_SUMMARY):
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} has {len(rows)} rows; expected 1")
        return failures
    row = rows[0]
    for key, value in EXPECTED_SUMMARY.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_manifest(path: Path) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    if data.get("rows") != len(EXPECTED_MODEL_ROWS):
        failures.append(f"{path} rows drifted")
    if data.get("adjacent_rows") != 2:
        failures.append(f"{path} adjacent_rows drifted")
    if data.get("claim_boundary") != EXPECTED_CLAIM_BOUNDARY:
        failures.append(f"{path} claim_boundary drifted")
    if data.get("anchor_status_counts") != EXPECTED_ANCHOR_STATUS_COUNTS:
        failures.append(f"{path} anchor_status_counts drifted")
    summary = data.get("summary")
    if not isinstance(summary, dict):
        failures.append(f"{path} summary missing or not an object")
        return failures
    for key, value in EXPECTED_SUMMARY.items():
        if str(summary.get(key, "")) != value:
            failures.append(f"{path} summary {key} drifted")
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


if __name__ == "__main__":
    raise SystemExit(main())
