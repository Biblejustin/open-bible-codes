#!/usr/bin/env python3
"""Summarize ANU WRR famous-rabbi source list record shapes."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.import_wrr_terms import parse_wrr_records


DEFAULT_SOURCES = (
    ("wrr1", Path("reports/wrr_1994/WRR1.txt")),
    ("wrr2", Path("reports/wrr_1994/WRR2.txt")),
    ("se2a", Path("reports/wrr_1994/SE2a.txt")),
    ("se2b", Path("reports/wrr_1994/SE2b.txt")),
    ("se3", Path("reports/wrr_1994/SE3.txt")),
)
OUT = Path("reports/wrr_1994/wrr_source_shapes.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr_source_shapes_summary.csv")
MD_OUT = Path("reports/wrr_1994/wrr_source_shapes.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr_source_shapes.manifest.json")

FIELDNAMES = [
    "label",
    "path",
    "records",
    "undated_records",
    "appellations",
    "dates",
    "same_record_pairs",
    "records_with_multiple_dates",
    "max_appellations_per_record",
    "max_dates_per_record",
    "status",
    "diagnostic",
]

SUMMARY_FIELDNAMES = [
    "source_files",
    "parsed_files",
    "expected_published_pairs",
    "files_matching_expected_pairs",
    "max_same_record_pairs",
    "closest_label",
    "closest_pair_gap",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    sources = parse_source_args(args.source)
    rows = [source_shape(label, path, encoding=args.encoding) for label, path in sources]
    summary = summarize(rows, expected_pairs=args.expected_published_pairs)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary)
    if args.manifest_out:
        write_manifest(args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Source in label=path form. Defaults to the ANU famous-rabbis files.",
    )
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--expected-published-pairs", type=int, default=163)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def parse_source_args(values: list[str]) -> list[tuple[str, Path]]:
    if not values:
        return list(DEFAULT_SOURCES)
    sources = []
    for value in values:
        if "=" not in value:
            raise ValueError(f"source must be label=path: {value!r}")
        label, path = value.split("=", 1)
        if not label.strip() or not path.strip():
            raise ValueError(f"source must be label=path: {value!r}")
        sources.append((label.strip(), Path(path.strip())))
    return sources


def source_shape(label: str, path: Path, *, encoding: str = "utf-8") -> dict[str, object]:
    try:
        records = parse_wrr_records(path.read_text(encoding=encoding))
    except Exception as error:  # pragma: no cover - exercised through returned status
        return {
            "label": label,
            "path": str(path),
            "records": 0,
            "undated_records": 0,
            "appellations": 0,
            "dates": 0,
            "same_record_pairs": 0,
            "records_with_multiple_dates": 0,
            "max_appellations_per_record": 0,
            "max_dates_per_record": 0,
            "status": "parse_error",
            "diagnostic": str(error),
        }
    return {
        "label": label,
        "path": str(path),
        "records": len(records),
        "undated_records": sum(1 for record in records if not record.dates),
        "appellations": sum(len(record.appellations) for record in records),
        "dates": sum(len(record.dates) for record in records),
        "same_record_pairs": sum(len(record.appellations) * len(record.dates) for record in records),
        "records_with_multiple_dates": sum(1 for record in records if len(record.dates) > 1),
        "max_appellations_per_record": max((len(record.appellations) for record in records), default=0),
        "max_dates_per_record": max((len(record.dates) for record in records), default=0),
        "status": "parsed",
        "diagnostic": "",
    }


def summarize(rows: list[dict[str, object]], *, expected_pairs: int) -> dict[str, object]:
    parsed = [row for row in rows if row["status"] == "parsed"]
    matching = [row for row in parsed if int(row["same_record_pairs"]) == expected_pairs]
    closest = min(
        parsed,
        key=lambda row: abs(expected_pairs - int(row["same_record_pairs"])),
        default=None,
    )
    return {
        "source_files": len(rows),
        "parsed_files": len(parsed),
        "expected_published_pairs": expected_pairs,
        "files_matching_expected_pairs": len(matching),
        "max_same_record_pairs": max((int(row["same_record_pairs"]) for row in parsed), default=0),
        "closest_label": "" if closest is None else str(closest["label"]),
        "closest_pair_gap": "" if closest is None else expected_pairs - int(closest["same_record_pairs"]),
    }


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: dict[str, object],
) -> None:
    lines = [
        "# WRR Source Shape Audit",
        "",
        "This report summarizes the raw record shape of the ANU/McKay famous-rabbis",
        "plain-text files. It does not decide the corrected-distance eligibility",
        "path; it only shows whether the available source files directly expose the",
        "commonly cited published distance count.",
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
            "## Source Files",
            "",
            "| Label | Records | Undated | Appellations | Dates | Raw pairs | Status |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["label"]),
                    str(row["records"]),
                    str(row["undated_records"]),
                    str(row["appellations"]),
                    str(row["dates"]),
                    str(row["same_record_pairs"]),
                    str(row["status"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Caution",
            "",
            "None of these raw source files should be promoted to the WRR 1994 distance",
            "table by count alone. If the expected distance count is absent here, the next",
            "step is source reconciliation, not metric implementation.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
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


if __name__ == "__main__":
    raise SystemExit(main())
