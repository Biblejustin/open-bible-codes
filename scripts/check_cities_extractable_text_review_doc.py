#!/usr/bin/env python3
"""Validate Cities extractable-text review doc stays role-review only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_extractable_text_review as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# Cities Extractable Text Review",
    "Status: source-role review only.",
    "does not import source rows",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Extractable rows reviewed: 5.",
    "Data-bearing candidates: 1.",
    "Data candidates with existing source-shape audit: 1.",
    "Gans source-shape records: 66.",
    "Gans community rows: 210.",
    "Method-context candidates: 1.",
    "Commentary/critique rows: 3.",
    "docs/GANS_COMMUNITIES_SOURCE_AUDIT.md",
    "source_shape_covered_not_result_bearing",
    "does not create city-name rows",
    "does not make a result-bearing claim",
    "not a result protocol",
)

EXPECTED_LABELS = (
    "cities_pdf_communities_data",
    "cities_pdf_gans",
    "cities_pdf_dp_365_1",
    "cities_pdf_dp_365_2",
    "cities_pdf_dp_365_4",
)

EXPECTED_STATUSES = (
    "data_bearing_candidate",
    "method_context_candidate",
    "commentary_or_perspective",
    "critique_or_response",
)

EXPECTED_ROWS = (
    {
        "label": "cities_pdf_dp_365_1",
        "family": "aumann_committee",
        "source_role": "aumann_committee_perspective",
        "data_bearing_status": "commentary_or_perspective",
        "anchor": "aumann_personal_perspective",
        "anchor_status": "found",
        "pdf_pages": "2",
        "normalized_text_chars": "6903",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp_365_1.pdf",
        "existing_source_audit": "",
        "existing_source_audit_status": "",
        "existing_records": "",
        "existing_community_rows": "",
        "url": "https://www.torah-code.org/experiments/dp_365_1.pdf",
        "review_read": "Aumann committee perspective text; source context, not a row table.",
        "next_action": "use for source-history review, not city-row import",
        "claim_boundary": builder.CLAIM_BOUNDARY,
    },
    {
        "label": "cities_pdf_dp_365_2",
        "family": "aumann_committee",
        "source_role": "furstenberg_committee_perspective",
        "data_bearing_status": "commentary_or_perspective",
        "anchor": "furstenberg_personal_perspective",
        "anchor_status": "found",
        "pdf_pages": "2",
        "normalized_text_chars": "6087",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp_365_2.pdf",
        "existing_source_audit": "",
        "existing_source_audit_status": "",
        "existing_records": "",
        "existing_community_rows": "",
        "url": "https://www.torah-code.org/experiments/dp_365_2.pdf",
        "review_read": "Furstenberg committee perspective text; source context, not a row table.",
        "next_action": "use for source-history review, not city-row import",
        "claim_boundary": builder.CLAIM_BOUNDARY,
    },
    {
        "label": "cities_pdf_dp_365_4",
        "family": "aumann_committee",
        "source_role": "witztum_critique_response",
        "data_bearing_status": "critique_or_response",
        "anchor": "witztum_critique_title",
        "anchor_status": "found",
        "pdf_pages": "2",
        "normalized_text_chars": "5456",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp_365_4.pdf",
        "existing_source_audit": "",
        "existing_source_audit_status": "",
        "existing_records": "",
        "existing_community_rows": "",
        "url": "https://www.torah-code.org/experiments/dp_365_4.pdf",
        "review_read": "Witztum critique/response text; source context, not a row table.",
        "next_action": "use for dispute/context review, not city-row import",
        "claim_boundary": builder.CLAIM_BOUNDARY,
    },
    {
        "label": "cities_pdf_communities_data",
        "family": "gans_communities",
        "source_role": "communities_data_table",
        "data_bearing_status": "data_bearing_candidate",
        "anchor": "gans_communities_data_title",
        "anchor_status": "found",
        "pdf_pages": "8",
        "normalized_text_chars": "18135",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_communities_data.pdf",
        "existing_source_audit": "docs/GANS_COMMUNITIES_SOURCE_AUDIT.md",
        "existing_source_audit_status": "source_shape_covered_not_result_bearing",
        "existing_records": "66",
        "existing_community_rows": "210",
        "url": "https://www.torah-code.org/papers/communities_data.pdf",
        "review_read": "Communities data/protocol table candidate; inspect table schema and rows before any import.",
        "next_action": "covered by Gans communities source-shape audit; next result step still needs locked preregistration",
        "claim_boundary": builder.CLAIM_BOUNDARY,
    },
    {
        "label": "cities_pdf_gans",
        "family": "gans_communities",
        "source_role": "communities_method_paper",
        "data_bearing_status": "method_context_candidate",
        "anchor": "gans_paper_title",
        "anchor_status": "found",
        "pdf_pages": "5",
        "normalized_text_chars": "19499",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_gans.pdf",
        "existing_source_audit": "",
        "existing_source_audit_status": "",
        "existing_records": "",
        "existing_community_rows": "",
        "url": "https://www.torah-code.org/papers/gans.pdf",
        "review_read": "Paper/method context candidate; not a city-name source table by itself.",
        "next_action": "use for method/context audit before any result protocol",
        "claim_boundary": builder.CLAIM_BOUNDARY,
    },
)

EXPECTED_SUMMARY_ROWS = (
    {"metric": "extractable_rows_reviewed", "value": "5"},
    {"metric": "anchors_found", "value": "5"},
    {"metric": "data_candidates_with_existing_source_shape_audit", "value": "1"},
    {"metric": "gans_source_records", "value": "66"},
    {"metric": "gans_source_community_rows", "value": "210"},
    {"metric": "status_commentary_or_perspective", "value": "2"},
    {"metric": "status_critique_or_response", "value": "1"},
    {"metric": "status_data_bearing_candidate", "value": "1"},
    {"metric": "status_method_context_candidate", "value": "1"},
    {"metric": "role_aumann_committee_perspective", "value": "1"},
    {"metric": "role_communities_data_table", "value": "1"},
    {"metric": "role_communities_method_paper", "value": "1"},
    {"metric": "role_furstenberg_committee_perspective", "value": "1"},
    {"metric": "role_witztum_critique_response", "value": "1"},
    {"metric": "claim_boundary", "value": builder.CLAIM_BOUNDARY},
)

EXPECTED_MANIFEST_SUMMARY = {row["metric"]: row["value"] for row in EXPECTED_SUMMARY_ROWS}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_extractable_text_review_doc(
        args.doc,
        args.rows,
        args.summary,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"Cities extractable-text review doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities extractable-text review doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_cities_extractable_text_review_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, summary_csv, manifest_json)
        if not path.exists()
    ]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    rows_data = read_csv(rows_csv)
    summary_data = read_csv(summary_csv)
    if isinstance(rows_data, str):
        return [rows_data]
    if isinstance(summary_data, str):
        return [summary_data]
    _, rows = rows_data
    _, summary_rows = summary_data
    summary = {row["metric"]: row["value"] for row in summary_rows}
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(validate_rows_csv(rows_csv, rows_data))
    failures.extend(validate_summary_csv(summary_csv, summary_data))
    failures.extend(validate_manifest(manifest_json))
    failures.extend(validate_rows(doc, normalized, rows))
    failures.extend(validate_summary(doc, normalized, summary))
    return failures


def validate_rows_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != list(EXPECTED_ROWS):
        failures.append(f"{path} row data drifted")
    return failures


def validate_summary_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != list(EXPECTED_SUMMARY_ROWS):
        failures.append(f"{path} summary rows drifted")
    return failures


def validate_manifest(path: Path) -> list[str]:
    data = read_json(path)
    if isinstance(data, str):
        return [data]
    checks: dict[str, Any] = {
        "tool": "build_cities_extractable_text_review.py",
        "inputs": {
            "queue": str(builder.DEFAULT_QUEUE),
            "text_audit": str(builder.DEFAULT_TEXT_AUDIT),
            "anchors": str(builder.DEFAULT_ANCHORS),
            "gans_summary": str(builder.DEFAULT_GANS_SUMMARY),
        },
        "rows": len(EXPECTED_ROWS),
        "summary": EXPECTED_MANIFEST_SUMMARY,
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "claim_boundary": builder.CLAIM_BOUNDARY,
    }
    failures: list[str] = []
    for key, expected in checks.items():
        if data.get(key) != expected:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    labels = {row.get("label", "") for row in rows}
    statuses = {row.get("data_bearing_status", "") for row in rows}
    failures: list[str] = []
    for label in EXPECTED_LABELS:
        if label not in labels:
            failures.append(f"rows CSV missing label: {label}")
        if label not in normalized_doc:
            failures.append(f"{doc} missing label: {label}")
    for status in EXPECTED_STATUSES:
        if status not in statuses:
            failures.append(f"rows CSV missing status: {status}")
        if status not in normalized_doc:
            failures.append(f"{doc} missing status: {status}")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    summary: dict[str, str],
) -> list[str]:
    expected = {
        "Extractable rows reviewed": summary.get("extractable_rows_reviewed", ""),
        "Anchors found": summary.get("anchors_found", ""),
        "Data-bearing candidates": summary.get("status_data_bearing_candidate", ""),
        "Data candidates with existing source-shape audit": summary.get(
            "data_candidates_with_existing_source_shape_audit",
            "",
        ),
        "Gans source-shape records": summary.get("gans_source_records", ""),
        "Gans community rows": summary.get("gans_source_community_rows", ""),
        "Method-context candidates": summary.get("status_method_context_candidate", ""),
    }
    failures: list[str] = []
    for label, value in expected.items():
        if not value:
            failures.append(f"summary CSV missing metric for {label}")
            continue
        if label == "Anchors found":
            needle = normalize_space(
                f"- {label}: {value} of {summary.get('extractable_rows_reviewed', '')}."
            )
        else:
            needle = normalize_space(f"- {label}: {value}.")
        if needle not in normalized_doc:
            failures.append(f"{doc} missing summary value: {label}={value}")
    return failures


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
