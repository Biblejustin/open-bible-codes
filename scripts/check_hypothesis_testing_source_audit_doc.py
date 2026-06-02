#!/usr/bin/env python3
"""Validate hypothesis-testing source audit doc keeps source limits explicit."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import analyze_hypothesis_testing_source as analyzer


DEFAULT_DOC = Path("docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md")
DEFAULT_ROWS = analyzer.DEFAULT_OUT
DEFAULT_SUMMARY = analyzer.DEFAULT_SUMMARY_OUT
DEFAULT_ANCHORS = analyzer.DEFAULT_ANCHORS_OUT
DEFAULT_MANIFEST = analyzer.DEFAULT_MANIFEST
DEFAULT_SOURCE_MANIFEST = Path("reports/wrr_1994/hypothesis_testing_sources.manifest.json")

EXPECTED_BYTES = "629155"
EXPECTED_SHA256 = "d60a59519b55bcff8b6a287eab9c7b06113e0967e95b362cfccaeb66d9cb84f4"
EXPECTED_TITLE = (
    "Daftar Bet Kecil 100, 200, 300, 500 Perak - Agen Slot Bet Kecil "
    "Deposit Via Pulsa 5000 Terjangkau"
)
EXPECTED_CANONICAL = "https://www.torah-code.org/"
EXPECTED_LINK_COUNT = "507"
EXPECTED_ROWS = {
    "overview": (
        "reports/wrr_1994/torah_code_hypothesis_testing_overview.html",
        "Hypothesis Testing",
        "torah_code_hypothesis_testing_overview",
        "https://www.torah-code.org/hypothesis_testing/hypothesis_1.html",
    ),
    "errors": (
        "reports/wrr_1994/torah_code_hypothesis_testing_errors.html",
        "Types of Errors",
        "torah_code_hypothesis_testing_errors",
        "https://www.torah-code.org/hypothesis_testing/hypothesis_2.html",
    ),
    "hypotheses": (
        "reports/wrr_1994/torah_code_hypothesis_testing_hypotheses.html",
        "Types of Hypotheses",
        "torah_code_hypothesis_testing_hypotheses",
        "https://www.torah-code.org/hypothesis_testing/hypotheses.html",
    ),
    "simulated_experiments": (
        "reports/wrr_1994/torah_code_hypothesis_testing_simulated_experiments.html",
        "Simulated Experiments",
        "torah_code_hypothesis_testing_simulated_experiments",
        "https://www.torah-code.org/hypothesis_testing/simulated_experiments.html",
    ),
}
EXPECTED_SUMMARY = {
    "source_files": "4",
    "expected_label_present_pages": "0",
    "spam_marker_pages": "4",
    "root_canonical_pages": "4",
    "usable_method_pages": "0",
    "unusable_method_pages": "4",
    "overview_method_anchor_count": "0",
    "overview_link_count": "507",
    "claim_status": "source_status_only_not_result_bearing",
}
EXPECTED_ANCHORS = [
    {
        "source": "overview",
        "anchor": "overview_expected_label_present",
        "status": "missing",
        "diagnostic": "overview page contains the Hypothesis Testing label",
    },
    {
        "source": "overview",
        "anchor": "overview_method_anchors_present",
        "status": "missing",
        "diagnostic": "overview page contains core null/alternative/test-statistic language",
    },
    {
        "source": "linked_pages",
        "anchor": "linked_page_status_recorded",
        "status": "found",
        "diagnostic": "overview and three linked pages were audited",
    },
    {
        "source": "overview",
        "anchor": "overview_usable_status_recorded",
        "status": "found",
        "diagnostic": "overview current source status is explicit",
    },
    {
        "source": "errors",
        "anchor": "errors_usable_status_recorded",
        "status": "found",
        "diagnostic": "errors current source status is explicit",
    },
    {
        "source": "hypotheses",
        "anchor": "hypotheses_usable_status_recorded",
        "status": "found",
        "diagnostic": "hypotheses current source status is explicit",
    },
    {
        "source": "simulated_experiments",
        "anchor": "simulated_experiments_usable_status_recorded",
        "status": "found",
        "diagnostic": "simulated_experiments current source status is explicit",
    },
]
EXPECTED_CLAIM_BOUNDARY = "source-status audit only; no ELS result"

REQUIRED_PHRASES = (
    "# Hypothesis-Testing Source Audit",
    "Status: source-status audit only.",
    "not an ELS result",
    "| source files scanned | 4 |",
    "| expected labels present | 0 |",
    "| spam-marker pages | 4 |",
    "| root-canonical pages | 4 |",
    "| usable method pages | 0 |",
    "| unusable current downloads | 4 |",
    "Current live downloads do not supply usable hypothesis-testing source pages.",
    "Fisher weights",
    "result-bearing protocol",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_hypothesis_testing_source_audit_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        anchors=args.anchors,
        manifest=args.manifest,
        source_manifest=args.source_manifest,
    )
    if failures:
        for failure in failures:
            print(f"hypothesis-testing source audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"hypothesis-testing source audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_SOURCE_MANIFEST)
    return parser


def validate_hypothesis_testing_source_audit_doc(
    doc: Path,
    *,
    rows: Path | None = DEFAULT_ROWS,
    summary: Path | None = DEFAULT_SUMMARY,
    anchors: Path | None = DEFAULT_ANCHORS,
    manifest: Path | None = DEFAULT_MANIFEST,
    source_manifest: Path | None = DEFAULT_SOURCE_MANIFEST,
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
    if anchors is not None:
        failures.extend(validate_anchors_csv(anchors))
    if manifest is not None:
        failures.extend(
            validate_manifest(
                manifest,
                doc=doc,
                rows=rows or DEFAULT_ROWS,
                summary=summary or DEFAULT_SUMMARY,
                anchors=anchors or DEFAULT_ANCHORS,
            )
        )
    if source_manifest is not None:
        failures.extend(validate_source_manifest(source_manifest))
    return failures


def validate_rows_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != analyzer.ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    observed_pages = [row.get("page", "") for row in rows]
    if observed_pages != list(EXPECTED_ROWS):
        failures.append(f"{path} page order drifted")
    by_page = {row.get("page", ""): row for row in rows}
    for page, (source_path, label, _download_label, _url) in EXPECTED_ROWS.items():
        row = by_page.get(page)
        if row is None:
            failures.append(f"{path} missing page {page}")
            continue
        checks = {
            "path": source_path,
            "bytes": EXPECTED_BYTES,
            "sha256": EXPECTED_SHA256,
            "title": EXPECTED_TITLE,
            "canonical": EXPECTED_CANONICAL,
            "link_count": EXPECTED_LINK_COUNT,
            "expected_label": label,
            "expected_label_present": "False",
            "spam_marker_present": "True",
            "canonical_is_root": "True",
            "method_anchor_count": "0",
            "usable_status": "unusable_current_download",
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} {page} {key} drifted")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != analyzer.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} has {len(rows)} rows; expected 1")
        return failures
    row = rows[0]
    for key, value in EXPECTED_SUMMARY.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_anchors_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != analyzer.ANCHOR_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != EXPECTED_ANCHORS:
        failures.append(f"{path} anchor rows drifted")
    return failures


def validate_manifest(
    path: Path,
    *,
    doc: Path,
    rows: Path,
    summary: Path,
    anchors: Path,
) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    if data.get("rows") != len(EXPECTED_ROWS):
        failures.append(f"{path} rows drifted")
    if data.get("summary") != _int_summary():
        failures.append(f"{path} summary drifted")
    if data.get("anchors") != EXPECTED_ANCHORS:
        failures.append(f"{path} anchors drifted")
    if data.get("sources") != [row[0] for row in EXPECTED_ROWS.values()]:
        failures.append(f"{path} sources drifted")
    if data.get("outputs") != {
        "csv": str(rows),
        "summary": str(summary),
        "anchors": str(anchors),
        "markdown": str(doc),
        "manifest": str(path),
    }:
        failures.append(f"{path} outputs drifted")
    if data.get("claim_boundary") != EXPECTED_CLAIM_BOUNDARY:
        failures.append(f"{path} claim_boundary drifted")
    return failures


def validate_source_manifest(path: Path) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    downloads = data.get("downloads")
    if not isinstance(downloads, list):
        return [f"{path} downloads missing or not a list"]
    if len(downloads) != len(EXPECTED_ROWS):
        failures.append(f"{path} download count drifted")
    expected_by_label = {
        download_label: (source_path, url)
        for source_path, _label, download_label, url in EXPECTED_ROWS.values()
    }
    observed_labels = [str(row.get("label", "")) for row in downloads]
    if observed_labels != list(expected_by_label):
        failures.append(f"{path} download label order drifted")
    for row in downloads:
        label = str(row.get("label", ""))
        expected = expected_by_label.get(label)
        if expected is None:
            failures.append(f"{path} unexpected download label {label}")
            continue
        source_path, url = expected
        checks: dict[str, Any] = {
            "path": source_path,
            "url": url,
            "bytes": int(EXPECTED_BYTES),
            "sha256": EXPECTED_SHA256,
            "final_url": EXPECTED_CANONICAL,
            "http_status": 200,
            "status": "downloaded",
            "redirected": True,
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} {label} {key} drifted")
    return failures


def _int_summary() -> dict[str, object]:
    return {
        key: int(value) if value.isdigit() else value
        for key, value in EXPECTED_SUMMARY.items()
    }


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
