#!/usr/bin/env python3
"""Bridge WRR primary Table 2 row anchors to secondary WRR2 record shapes."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.import_wrr_terms import WrrRecord, parse_wrr_records


DEFAULT_ANCHORS = Path("reports/wrr_1994/wrr_primary_table2_anchors.csv")
DEFAULT_SOURCE = Path("reports/wrr_1994/WRR2.txt")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_table2_source_bridge.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_table2_source_bridge_summary.csv")
DEFAULT_MD = Path("reports/wrr_1994/wrr_table2_source_bridge.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_table2_source_bridge.manifest.json")

FIELDNAMES = [
    "row_number",
    "english_name",
    "primary_anchor_status",
    "primary_page",
    "secondary_record_status",
    "secondary_appellations",
    "secondary_dates",
    "secondary_same_record_pairs",
    "primary_hebrew_cells_status",
    "current_read",
]

SUMMARY_FIELDNAMES = [
    "primary_rows",
    "primary_rows_found",
    "secondary_records",
    "rows_with_primary_and_secondary",
    "secondary_appellations",
    "secondary_dates",
    "secondary_same_record_pairs",
    "undated_secondary_records",
    "primary_hebrew_cells_verified",
    "status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    anchors = read_rows(args.anchors)
    records = parse_wrr_records(args.source.read_text(encoding=args.encoding))
    rows = build_bridge_rows(anchors, records)
    summary = summarize(rows)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary, args)
    write_manifest(args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_bridge_rows(
    anchor_rows: list[dict[str, str]],
    records: list[WrrRecord],
) -> list[dict[str, str]]:
    records_by_index = {record.index: record for record in records}
    rows = []
    for anchor in sorted(anchor_rows, key=lambda row: int_or_zero(row.get("row_number", ""))):
        row_number = int_or_zero(anchor.get("row_number", ""))
        record = records_by_index.get(row_number)
        rows.append(build_bridge_row(anchor, record))
    return rows


def build_bridge_row(anchor: dict[str, str], record: WrrRecord | None) -> dict[str, str]:
    primary_found = anchor.get("status") == "found"
    secondary_found = record is not None
    appellations = 0 if record is None else len(record.appellations)
    dates = 0 if record is None else len(record.dates)
    pair_count = appellations * dates
    return {
        "row_number": anchor.get("row_number", ""),
        "english_name": anchor.get("english_name", ""),
        "primary_anchor_status": anchor.get("status", ""),
        "primary_page": anchor.get("page", ""),
        "secondary_record_status": "found" if secondary_found else "missing",
        "secondary_appellations": str(appellations) if secondary_found else "",
        "secondary_dates": str(dates) if secondary_found else "",
        "secondary_same_record_pairs": str(pair_count) if secondary_found else "",
        "primary_hebrew_cells_status": "not_verified",
        "current_read": current_read(primary_found, secondary_found, appellations, dates, pair_count),
    }


def current_read(
    primary_found: bool,
    secondary_found: bool,
    appellations: int,
    dates: int,
    pair_count: int,
) -> str:
    if primary_found and secondary_found:
        return (
            "Primary English row label and secondary WRR2 record align by row number; "
            f"secondary record has {appellations} appellations, {dates} dates, "
            f"and {pair_count} same-record pairs. Hebrew cells are not verified."
        )
    if primary_found:
        return "Primary English row label found, but no secondary WRR2 record exists for this row."
    if secondary_found:
        return "Secondary WRR2 record exists, but primary English row-label anchor was not found."
    return "Neither primary row-label anchor nor secondary WRR2 record was found."


def summarize(rows: list[dict[str, str]]) -> dict[str, str]:
    primary_found = sum(1 for row in rows if row["primary_anchor_status"] == "found")
    secondary_found = sum(1 for row in rows if row["secondary_record_status"] == "found")
    both_found = sum(
        1
        for row in rows
        if row["primary_anchor_status"] == "found"
        and row["secondary_record_status"] == "found"
    )
    secondary_dates = sum(int_or_zero(row["secondary_dates"]) for row in rows)
    undated = sum(
        1
        for row in rows
        if row["secondary_record_status"] == "found"
        and int_or_zero(row["secondary_dates"]) == 0
    )
    primary_verified = sum(
        1 for row in rows if row["primary_hebrew_cells_status"] == "verified"
    )
    return {
        "primary_rows": str(len(rows)),
        "primary_rows_found": str(primary_found),
        "secondary_records": str(secondary_found),
        "rows_with_primary_and_secondary": str(both_found),
        "secondary_appellations": str(sum(int_or_zero(row["secondary_appellations"]) for row in rows)),
        "secondary_dates": str(secondary_dates),
        "secondary_same_record_pairs": str(sum(int_or_zero(row["secondary_same_record_pairs"]) for row in rows)),
        "undated_secondary_records": str(undated),
        "primary_hebrew_cells_verified": str(primary_verified),
        "status": "bridge_only_not_transcription",
    }


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary: dict[str, str],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# WRR Table 2 Source Bridge",
        "",
        "Status: primary row-label to secondary-record bridge; not Hebrew table transcription.",
        "",
        "This joins primary Table 2 English row anchors to the secondary WRR2",
        "plain-text record shape by row number. It makes the current dependency",
        "explicit: the row labels are primary-audited, but the Hebrew appellation",
        "and date cells still come from a secondary transcription.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_table2_source_bridge "
            f"--anchors {args.anchors} "
            f"--source {args.source} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        "| Item | Count |",
        "| --- | ---: |",
    ]
    for key in SUMMARY_FIELDNAMES:
        lines.append(f"| `{key}` | {summary[key]} |")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Row | Primary English label | Primary | Secondary | Apps | Dates | Pairs | Hebrew cells |",
            "| ---: | --- | --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["row_number"]),
                    markdown_cell(row["english_name"]),
                    f"`{markdown_cell(row['primary_anchor_status'])}`",
                    f"`{markdown_cell(row['secondary_record_status'])}`",
                    markdown_cell(row["secondary_appellations"]),
                    markdown_cell(row["secondary_dates"]),
                    markdown_cell(row["secondary_same_record_pairs"]),
                    f"`{markdown_cell(row['primary_hebrew_cells_status'])}`",
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary: dict[str, str],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "anchors": str(args.anchors),
            "source": str(args.source),
        },
        "summary": summary,
        "rows": len(rows),
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def int_or_zero(value: object) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
