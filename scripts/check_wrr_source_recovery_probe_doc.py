#!/usr/bin/env python3
"""Validate WRR source-recovery probe doc keeps live-source limits explicit."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_DOC = Path("docs/WRR_SOURCE_RECOVERY_PROBE.md")
DEFAULT_ROWS = Path("reports/wrr_source_recovery_probe/source_recovery_probe.csv")
DEFAULT_SUMMARY = Path("reports/wrr_source_recovery_probe/source_recovery_probe_summary.csv")
DEFAULT_SOURCE_MANIFEST = Path("reports/wrr_source_recovery_probe/sources.manifest.json")
DEFAULT_REPORT_MANIFEST = Path(
    "reports/wrr_source_recovery_probe/source_recovery_probe.manifest.json"
)

EXPECTED_PROBE_LABELS = (
    "torah_code_research_program_1",
    "torah_code_research_program_1_shtml",
    "torah_code_research_program_2",
    "torah_code_research_program_2_shtml",
    "torah_code_research_model_overview",
    "torah_code_research_model_overview_shtml",
    "torah_code_research_geometric_model_level_1",
    "torah_code_research_geometric_model_level_1_shtml",
    "torah_code_research_geometric_model_level_2",
    "torah_code_research_geometric_model_level_2_shtml",
    "torah_code_research_geometric_model_level_3",
    "torah_code_research_geometric_model_level_3_shtml",
    "torah_code_research_els_model_level_1",
    "torah_code_research_els_model_level_1_shtml",
    "torah_code_research_els_model_level_2",
    "torah_code_research_els_model_level_2_shtml",
    "torah_code_research_els_model_level_3",
    "torah_code_research_els_model_level_3_shtml",
)
EXPECTED_LABEL_TEXT = {
    "torah_code_research_program_1": "Research Program",
    "torah_code_research_program_1_shtml": "Research Program",
    "torah_code_research_program_2": "Research Program",
    "torah_code_research_program_2_shtml": "Research Program",
    "torah_code_research_model_overview": "The Model",
    "torah_code_research_model_overview_shtml": "The Model",
    "torah_code_research_geometric_model_level_1": "The Geometric Model",
    "torah_code_research_geometric_model_level_1_shtml": "The Geometric Model",
    "torah_code_research_geometric_model_level_2": "Geometric Model Level 2",
    "torah_code_research_geometric_model_level_2_shtml": "Geometric Model Level 2",
    "torah_code_research_geometric_model_level_3": "Geometric Model Level 3",
    "torah_code_research_geometric_model_level_3_shtml": "Geometric Model Level 3",
    "torah_code_research_els_model_level_1": "ELS Model Level 1",
    "torah_code_research_els_model_level_1_shtml": "ELS Model Level 1",
    "torah_code_research_els_model_level_2": "ELS Model Level 2",
    "torah_code_research_els_model_level_2_shtml": "ELS Model Level 2",
    "torah_code_research_els_model_level_3": "ELS Model Level 3",
    "torah_code_research_els_model_level_3_shtml": "ELS Model Level 3",
}
EXPECTED_ROW_FIELDNAMES = [
    "label",
    "requested_url",
    "final_url",
    "redirected",
    "http_status",
    "download_status",
    "path",
    "bytes",
    "sha256",
    "title",
    "canonical",
    "expected_label",
    "expected_label_present",
    "canonical_is_root",
    "final_url_is_root",
    "spam_marker_present",
    "usable_status",
]
EXPECTED_SUMMARY = {
    "downloads": "18",
    "expected_label_rows": "18",
    "expected_label_present_rows": "0",
    "redirected_rows": "18",
    "root_final_url_rows": "18",
    "root_canonical_rows": "18",
    "spam_marker_rows": "18",
    "usable_current_source_rows": "0",
    "unusable_current_download_rows": "18",
    "current_recovery_status": "no_live_sources_recovered",
}
EXPECTED_SUMMARY_FIELDNAMES = list(EXPECTED_SUMMARY)
ROOT_URL = "https://www.torah-code.org/"
EXPECTED_BYTES = "629155"
EXPECTED_SHA256 = "d60a59519b55bcff8b6a287eab9c7b06113e0967e95b362cfccaeb66d9cb84f4"
EXPECTED_REPORT_CLAIM_BOUNDARY = "live-source recovery probe only; no ELS result"

REQUIRED_PHRASES = (
    "# WRR Source Recovery Probe",
    "Status: live-source recovery probe only.",
    "does not update the cached `reports/wrr_1994/` bundle",
    "claim-ready source decisions",
    "| downloads probed | 18 |",
    "| rows where expected label appeared | 0 |",
    "| redirected rows | 18 |",
    "| final URL is Torah-code root | 18 |",
    "| canonical URL is Torah-code root | 18 |",
    "| unrelated slot/gambling markers | 18 |",
    "| usable current source rows | 0 |",
    "Current recovery status: `no_live_sources_recovered`.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_recovery_probe_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        source_manifest=args.source_manifest,
        report_manifest=args.report_manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR source-recovery probe doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-recovery probe doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_SOURCE_MANIFEST)
    parser.add_argument("--report-manifest", type=Path, default=DEFAULT_REPORT_MANIFEST)
    return parser


def validate_source_recovery_probe_doc(
    doc: Path,
    *,
    rows: Path | None = DEFAULT_ROWS,
    summary: Path | None = DEFAULT_SUMMARY,
    source_manifest: Path | None = DEFAULT_SOURCE_MANIFEST,
    report_manifest: Path | None = DEFAULT_REPORT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    present_labels = probe_labels(text)
    missing_labels = sorted(set(EXPECTED_PROBE_LABELS) - present_labels)
    if missing_labels:
        failures.append(
            f"{doc} missing probe labels: " + ", ".join(missing_labels)
        )
    if rows is not None:
        failures.extend(validate_rows_csv(rows))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if source_manifest is not None:
        failures.extend(validate_source_manifest(source_manifest))
    if report_manifest is not None:
        failures.extend(validate_report_manifest(report_manifest))
    return failures


def probe_labels(text: str) -> set[str]:
    labels: set[str] = set()
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 9 and cells[0].startswith("torah_code_research_"):
            labels.add(cells[0])
    return labels


def validate_rows_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != EXPECTED_ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    labels = [row.get("label", "") for row in rows]
    if tuple(labels) != EXPECTED_PROBE_LABELS:
        failures.append(f"{path} probe label order drifted")
    for row in rows:
        label = row.get("label", "")
        expected_label = EXPECTED_LABEL_TEXT.get(label, "")
        checks = {
            "final_url": ROOT_URL,
            "redirected": "True",
            "http_status": "200",
            "download_status": "downloaded",
            "bytes": EXPECTED_BYTES,
            "sha256": EXPECTED_SHA256,
            "canonical": ROOT_URL,
            "expected_label": expected_label,
            "expected_label_present": "False",
            "canonical_is_root": "True",
            "final_url_is_root": "True",
            "spam_marker_present": "True",
            "usable_status": "unusable_current_download",
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} {label} {key} drifted")
        if not row.get("requested_url", "").startswith("https://www.torah-code.org/"):
            failures.append(f"{path} {label} requested_url drifted")
        if row.get("path") != f"reports/wrr_source_recovery_probe/{label}.html":
            failures.append(f"{path} {label} path drifted")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != EXPECTED_SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} has {len(rows)} rows; expected 1")
        return failures
    row = rows[0]
    for key, value in EXPECTED_SUMMARY.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_source_manifest(path: Path) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    downloads = data.get("downloads")
    if not isinstance(downloads, list):
        return [f"{path} downloads missing or not a list"]
    labels = [str(row.get("label", "")) for row in downloads if isinstance(row, dict)]
    if tuple(labels) != EXPECTED_PROBE_LABELS:
        failures.append(f"{path} download label order drifted")
    for row in downloads:
        if not isinstance(row, dict):
            failures.append(f"{path} download row is not an object")
            continue
        label = str(row.get("label", ""))
        checks: dict[str, object] = {
            "final_url": ROOT_URL,
            "redirected": True,
            "http_status": 200,
            "status": "downloaded",
            "bytes": int(EXPECTED_BYTES),
            "sha256": EXPECTED_SHA256,
            "path": f"reports/wrr_source_recovery_probe/{label}.html",
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} {label} {key} drifted")
        if not str(row.get("url", "")).startswith("https://www.torah-code.org/"):
            failures.append(f"{path} {label} url drifted")
    return failures


def validate_report_manifest(path: Path) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    if data.get("rows") != len(EXPECTED_PROBE_LABELS):
        failures.append(f"{path} rows drifted")
    if data.get("claim_boundary") != EXPECTED_REPORT_CLAIM_BOUNDARY:
        failures.append(f"{path} claim_boundary drifted")
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
