#!/usr/bin/env python3
"""Aggregate WRR corrected-distance rows into diagnostic P1..P4 statistics."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.wrr import p1_binomial_tail, p2_product_statistic


INPUT = Path("reports/wrr_1994/wrr2_corrected_distance_smoke.csv")
OUT = Path("reports/wrr_1994/wrr2_corrected_distance_aggregate.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_corrected_distance_aggregate.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_corrected_distance_aggregate.manifest.json")

FIELDNAMES = [
    "source",
    "rows",
    "defined_corrected_distances",
    "undefined_rows",
    "p3_p4_sample_rows",
    "p3_p4_sample_defined_corrected_distances",
    "p3_p4_sample_undefined_rows",
    "p1_threshold",
    "p1",
    "p2",
    "p3",
    "p4",
    "min_corrected_distance",
    "max_corrected_distance",
    "status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_rows(args.input)
    summary = aggregate(rows, source=str(args.input), p1_threshold=args.p1_threshold)
    write_rows(args.out, [summary])
    write_markdown(args.markdown_out, summary)
    if args.manifest_out:
        write_manifest(args, summary, started)
    print(args.out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--p1-threshold", type=float, default=0.2)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def aggregate(
    rows: list[dict[str, str]],
    *,
    source: str,
    p1_threshold: float,
) -> dict[str, object]:
    values = corrected_distance_values(rows)
    p3_rows = p3_p4_sample_rows(rows)
    p3_values = corrected_distance_values(p3_rows)
    if values:
        p1 = p1_binomial_tail(values, threshold=p1_threshold)
        p2 = p2_product_statistic(values)
        status = "diagnostic_only_not_wrr_reproduction"
        min_c: object = min(values)
        max_c: object = max(values)
    else:
        p1 = ""
        p2 = ""
        status = "no_defined_corrected_distances"
        min_c = ""
        max_c = ""
    if p3_values:
        p3: object = p1_binomial_tail(p3_values, threshold=p1_threshold)
        p4: object = p2_product_statistic(p3_values)
    else:
        p3 = ""
        p4 = ""
    return {
        "source": source,
        "rows": len(rows),
        "defined_corrected_distances": len(values),
        "undefined_rows": len(rows) - len(values),
        "p3_p4_sample_rows": len(p3_rows),
        "p3_p4_sample_defined_corrected_distances": len(p3_values),
        "p3_p4_sample_undefined_rows": len(p3_rows) - len(p3_values),
        "p1_threshold": c_cell(p1_threshold),
        "p1": "" if p1 == "" else c_cell(float(p1)),
        "p2": "" if p2 == "" else c_cell(float(p2)),
        "p3": "" if p3 == "" else c_cell(float(p3)),
        "p4": "" if p4 == "" else c_cell(float(p4)),
        "min_corrected_distance": "" if min_c == "" else c_cell(float(min_c)),
        "max_corrected_distance": "" if max_c == "" else c_cell(float(max_c)),
        "status": status,
    }


def corrected_distance_values(rows: list[dict[str, str]]) -> list[float]:
    values: list[float] = []
    for row in rows:
        if row.get("corrected_distance_status") != "defined":
            continue
        value = row.get("corrected_distance", "").strip()
        if not value:
            continue
        values.append(float(value))
    return values


def p3_p4_sample_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if has_rabbi_title_flag(row)
        and not truthy(row.get("appellation_starts_with_rabbi_title"))
    ]


def has_rabbi_title_flag(row: dict[str, str]) -> bool:
    return row.get("appellation_starts_with_rabbi_title", "").strip() != ""


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, summary: dict[str, object]) -> None:
    lines = [
        "# WRR2 Corrected Distance Aggregate",
        "",
        "This aggregates already-defined corrected-distance rows into WRR-style",
        "P1..P4 diagnostics. P3/P4 use the paper-described smaller sample",
        "where appellations starting with title Rabbi are omitted. It does not",
        "perform permutation tests and is not",
        "a WRR reproduction.",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for field in FIELDNAMES:
        lines.append(f"| `{field}` | {summary[field]} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "input": str(args.input),
        "parameters": {"p1_threshold": args.p1_threshold},
        "summary": summary,
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def c_cell(value: float) -> str:
    return f"{value:.12g}"


if __name__ == "__main__":
    raise SystemExit(main())
