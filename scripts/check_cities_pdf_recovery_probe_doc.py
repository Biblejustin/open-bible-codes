#!/usr/bin/env python3
"""Validate Cities PDF recovery probe doc keeps source limits explicit."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_DOC = Path("docs/CITIES_PDF_RECOVERY_PROBE.md")
DEFAULT_ROWS = Path("reports/cities_pdf_recovery_probe/cities_pdf_recovery_probe.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_pdf_recovery_probe_summary.csv"
)
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_pdf_recovery_probe.manifest.json"
)

EXPECTED_ROW_FIELDNAMES = [
    "label",
    "source_pages",
    "url",
    "live_final_url",
    "live_http_status",
    "live_status",
    "live_kind",
    "live_bytes",
    "live_sha256",
    "archive_probe_url",
    "archive_status",
    "archive_snapshot_source",
    "archive_timestamp",
    "archive_cdx_checked",
    "archive_cdx_candidate_count",
    "archive_raw_url",
    "archive_kind",
    "archive_bytes",
    "archive_sha256",
    "selected_source",
    "selected_path",
    "pdf_pages",
    "pdf_text_chars",
    "usable_status",
]
EXPECTED_SUMMARY = {
    "pdf_urls_probed": "35",
    "live_pdf_rows": "0",
    "live_html_or_other_rows": "35",
    "archive_available_rows": "12",
    "archive_cdx_checked_rows": "2",
    "archive_cdx_candidate_rows": "2",
    "archive_pdf_rows": "12",
    "usable_pdf_rows": "12",
    "unrecovered_pdf_rows": "23",
    "current_pdf_recovery_status": "partial_pdf_sources_recovered",
}
EXPECTED_USABLE_ROWS = {
    "cities_pdf_wrr": ("10", "0", "a63419d9f20ba23f"),
    "cities_pdf_dp365a_appendix_6": ("2", "0", "5d9949a0a348bcd9"),
    "cities_pdf_dp365a_appendix_7": ("5", "0", "7b7e2015bb628417"),
    "cities_pdf_dp365a_p1_4": ("4", "6115", "90fb6ff653d2fc97"),
    "cities_pdf_dp365a_p12_17": ("6", "37639", "127d829147cbc1ec"),
    "cities_pdf_dp365a_p5_11": ("7", "18107", "e89e869d452f4294"),
    "cities_pdf_dp365a_part_2_p105_111": ("7", "0", "248d3ff6a9fd1042"),
    "cities_pdf_dp_365_1": ("2", "7044", "ae09dc718ad2e798"),
    "cities_pdf_dp_365_2": ("2", "6248", "5301f21fa3c1b5b8"),
    "cities_pdf_dp_365_4": ("2", "5759", "4dc4119f30430dc2"),
    "cities_pdf_communities_data": ("8", "30281", "ac0b221064e144ca"),
    "cities_pdf_gans": ("5", "25846", "212cb24f918b9a41"),
}
EXPECTED_KEY_UNRECOVERED = (
    "cities_pdf_gans_original_report",
    "cities_pdf_dp364_appendix_4",
    "cities_pdf_margoliot_cities_data",
)
EXPECTED_CLAIM_BOUNDARY = "live/archive PDF recovery probe only; no ELS result"

REQUIRED_PHRASES = (
    "# Cities PDF Recovery Probe",
    "Status: live/archive PDF recovery probe only.",
    "does not update the cached `reports/wrr_1994/` bundle",
    "does not make claim-ready source decisions",
    "| PDF URLs probed | 35 |",
    "Current PDF recovery status:",
    "Recovered PDF bytes are source-shape inputs only.",
    "city-name normalization",
    "ELS searches",
    "p-level verification",
)

EXPECTED_LABELS = (
    "cities_pdf_gans_original_report",
    "cities_pdf_dp364_appendix_4",
    "cities_pdf_margoliot_cities_data",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_pdf_recovery_probe_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"Cities PDF recovery probe doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities PDF recovery probe doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_cities_pdf_recovery_probe_doc(
    doc: Path,
    *,
    rows: Path | None = DEFAULT_ROWS,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    present_labels = probe_labels(text)
    missing = sorted(set(EXPECTED_LABELS) - present_labels)
    if missing:
        failures.append(f"{doc} missing probe labels: " + ", ".join(missing))
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
        if len(cells) >= 6 and cells[0].startswith("cities_pdf_"):
            labels.add(cells[0])
    return labels


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def validate_rows_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != EXPECTED_ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != int(EXPECTED_SUMMARY["pdf_urls_probed"]):
        failures.append(f"{path} has {len(rows)} rows; expected 35")
    usable = [row for row in rows if row.get("usable_status") == "usable_archived_pdf"]
    unrecovered = [row for row in rows if row.get("usable_status") == "no_pdf_recovered"]
    if len(usable) != int(EXPECTED_SUMMARY["usable_pdf_rows"]):
        failures.append(f"{path} usable PDF row count drifted")
    if len(unrecovered) != int(EXPECTED_SUMMARY["unrecovered_pdf_rows"]):
        failures.append(f"{path} unrecovered PDF row count drifted")
    by_label = {row.get("label", ""): row for row in rows}
    for label, (pages, text_chars, sha_prefix) in EXPECTED_USABLE_ROWS.items():
        row = by_label.get(label)
        if row is None:
            failures.append(f"{path} missing usable row {label}")
            continue
        checks = {
            "selected_source": "archive",
            "archive_kind": "pdf",
            "usable_status": "usable_archived_pdf",
            "pdf_pages": pages,
            "pdf_text_chars": text_chars,
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} {label} {key} drifted")
        if not row.get("archive_sha256", "").startswith(sha_prefix):
            failures.append(f"{path} {label} archive_sha256 drifted")
        if not row.get("selected_path", "").endswith(f"{label}.pdf"):
            failures.append(f"{path} {label} selected_path drifted")
    for label in EXPECTED_KEY_UNRECOVERED:
        row = by_label.get(label)
        if row is None:
            failures.append(f"{path} missing unrecovered row {label}")
            continue
        if row.get("usable_status") != "no_pdf_recovered":
            failures.append(f"{path} {label} usable_status drifted")
        if row.get("selected_source") or row.get("selected_path"):
            failures.append(f"{path} {label} selected source/path drifted")
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
    if data.get("rows") != int(EXPECTED_SUMMARY["pdf_urls_probed"]):
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
