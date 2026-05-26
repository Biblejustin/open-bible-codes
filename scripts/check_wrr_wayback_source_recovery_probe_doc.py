#!/usr/bin/env python3
"""Validate WRR Wayback source-recovery probe doc keeps archive limits explicit."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts.build_wrr_wayback_source_recovery_probe import (
    PROBE_SOURCES,
    ROW_FIELDNAMES,
    SOURCE_BY_LABEL,
    SUMMARY_FIELDNAMES,
)


DEFAULT_DOC = Path("docs/WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md")
DEFAULT_ROWS = Path(
    "reports/wrr_wayback_source_recovery_probe/wayback_source_recovery_probe.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/wrr_wayback_source_recovery_probe/wayback_source_recovery_probe_summary.csv"
)
DEFAULT_MANIFEST = Path(
    "reports/wrr_wayback_source_recovery_probe/wayback_source_recovery_probe.manifest.json"
)

EXPECTED_PROBE_LABELS = tuple(source.label for source in PROBE_SOURCES)
EXPECTED_SUMMARY = {
    "probe_rows": "18",
    "unique_concepts": "9",
    "availability_available_rows": "5",
    "cdx_checked_rows": "14",
    "cdx_candidate_rows": "1",
    "cdx_fallback_rows": "1",
    "archive_downloaded_rows": "5",
    "expected_label_present_rows": "5",
    "spam_marker_rows": "0",
    "usable_archived_source_rows": "5",
    "usable_archived_concepts": "5",
    "missing_archived_concepts": "4",
    "current_archive_recovery_status": "partial_archived_sources_recovered",
}
EXPECTED_ROW_OBSERVED = {
    "torah_code_research_program_1_html": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_program_1_shtml": {
        "closest_available": "True",
        "snapshot_source": "availability_closest",
        "closest_timestamp": "20220921212759",
        "cdx_candidate_count": "0",
        "expected_label_present": "True",
        "spam_marker_present": "False",
        "bytes": "10423",
        "sha256": "0c1b9806f557db576b0960b4ad9c2cd7577408f443fe15b2bc6816ec2748d983",
        "title": "Torah Codes -- Research Program",
        "usable_status": "usable_archived_source",
    },
    "torah_code_research_program_2_html": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_program_2_shtml": {
        "closest_available": "True",
        "snapshot_source": "cdx_fallback",
        "closest_timestamp": "20090125122256",
        "cdx_candidate_count": "3",
        "expected_label_present": "True",
        "spam_marker_present": "False",
        "bytes": "8536",
        "sha256": "4ba0a3a929e36a3d834efebb01ace58567616fbf3c02dca7051e193668425af7",
        "title": "Torah Codes -- Research Program",
        "usable_status": "usable_archived_source",
    },
    "torah_code_research_model_overview_html": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_model_overview_shtml": {
        "closest_available": "True",
        "snapshot_source": "availability_closest",
        "closest_timestamp": "20160615070555",
        "cdx_candidate_count": "0",
        "expected_label_present": "True",
        "spam_marker_present": "False",
        "bytes": "9885",
        "sha256": "8b96e9f680933611306892fe5d1d5c213a5344ec96d9c4a57b1730d7fa385fca",
        "title": "Torah Codes -- The Model",
        "usable_status": "usable_archived_source",
    },
    "torah_code_research_geometric_model_level_1_html": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_geometric_model_level_1_shtml": {
        "closest_available": "True",
        "snapshot_source": "availability_closest",
        "closest_timestamp": "20150728045249",
        "cdx_candidate_count": "0",
        "expected_label_present": "True",
        "spam_marker_present": "False",
        "bytes": "9058",
        "sha256": "c01daa7f0fbd0cb828b3afcf1df2dcc6ed583a33a4e472fda988a83cba1c7039",
        "title": "Torah Codes -- The Geometric Model",
        "usable_status": "usable_archived_source",
    },
    "torah_code_research_geometric_model_level_2_html": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_geometric_model_level_2_shtml": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_geometric_model_level_3_html": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_geometric_model_level_3_shtml": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_els_model_level_1_html": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_els_model_level_1_shtml": {
        "closest_available": "True",
        "snapshot_source": "availability_closest",
        "closest_timestamp": "20150728045254",
        "cdx_candidate_count": "0",
        "expected_label_present": "True",
        "spam_marker_present": "False",
        "bytes": "9776",
        "sha256": "7e4f22c6edfdb0f3491b1bc69e53073567d305134c81d858be28e37a4794dc06",
        "title": "Torah Codes -- ELS Model Level 1",
        "usable_status": "usable_archived_source",
    },
    "torah_code_research_els_model_level_2_html": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_els_model_level_2_shtml": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_els_model_level_3_html": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
    "torah_code_research_els_model_level_3_shtml": {
        "closest_available": "False",
        "snapshot_source": "",
        "closest_timestamp": "",
        "cdx_candidate_count": "0",
        "expected_label_present": "False",
        "spam_marker_present": "False",
        "bytes": "0",
        "sha256": "",
        "title": "",
        "usable_status": "no_archived_snapshot",
    },
}
EXPECTED_CLAIM_BOUNDARY = "archived-source recovery probe only; no ELS result"

REQUIRED_PHRASES = (
    "# WRR Wayback Source Recovery Probe",
    "Status: archived-source recovery probe only.",
    "does not update the cached `reports/wrr_1994/` bundle",
    "claim-ready source decisions",
    "| Wayback URLs probed | 18 |",
    "| unique research concepts probed | 9 |",
    "| rows with archived snapshot | 5 |",
    "| rows checked with CDX fallback |",
    "| rows with CDX exact-URL candidates |",
    "| rows recovered through CDX fallback |",
    "| rows where expected label appeared | 5 |",
    "| unrelated slot/gambling markers | 0 |",
    "| usable archived source rows | 5 |",
    "| usable archived concepts | 5 |",
    "| missing archived concepts | 4 |",
    "Current archive recovery status: `partial_archived_sources_recovered`.",
    "falls back to CDX exact-URL 200-capture rows",
    "geometric-model or ELS-model pages",
    "WRR residual",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_wayback_source_recovery_probe_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(
                f"WRR Wayback source-recovery probe doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR Wayback source-recovery probe doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_wayback_source_recovery_probe_doc(
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
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def probe_labels(text: str) -> set[str]:
    labels: set[str] = set()
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 10 and cells[0].startswith("torah_code_research_"):
            labels.add(cells[0])
    return labels


def validate_rows_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    labels = [row.get("label", "") for row in rows]
    if tuple(labels) != EXPECTED_PROBE_LABELS:
        failures.append(f"{path} probe label order drifted")
    for row in rows:
        label = row.get("label", "")
        source = SOURCE_BY_LABEL.get(label)
        if source is None:
            failures.append(f"{path} unknown label {label}")
            continue
        source_checks = {
            "concept": source.concept,
            "family": source.family,
            "original_url": source.url,
            "expected_label": source.expected_label,
        }
        for key, value in source_checks.items():
            if row.get(key) != value:
                failures.append(f"{path} {label} {key} drifted")
        for key, value in EXPECTED_ROW_OBSERVED.get(label, {}).items():
            if row.get(key) != value:
                failures.append(f"{path} {label} {key} drifted")
        expected_path = (
            f"reports/wrr_wayback_source_recovery_probe/snapshots/{label}.html"
            if row.get("usable_status") == "usable_archived_source"
            else ""
        )
        if row.get("path") != expected_path:
            failures.append(f"{path} {label} path drifted")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != SUMMARY_FIELDNAMES:
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
    if data.get("rows") != len(EXPECTED_PROBE_LABELS):
        failures.append(f"{path} rows drifted")
    if data.get("claim_boundary") != EXPECTED_CLAIM_BOUNDARY:
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
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
