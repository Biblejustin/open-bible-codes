#!/usr/bin/env python3
"""Merge WRR corrected-distance shard CSVs."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.analyze_wrr_corrected_distance import (
    FIELDNAMES,
    SUMMARY_FIELDNAMES,
    count_status,
)


OUT = Path("reports/wrr_1994/wrr2_corrected_distance_smoke_merged.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_corrected_distance_smoke_merged_summary.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_corrected_distance_smoke_merged.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_corrected_distance_smoke_merged.manifest.json")


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    shard_paths = args.shard
    if args.expected_shard_count and len(shard_paths) != args.expected_shard_count:
        raise ValueError("number of --shard inputs does not match --expected-shard-count")
    rows = merge_rows(read_shards(shard_paths))
    summary_rows = read_summaries(args.shard_summary)
    validate_merge_inputs(
        rows,
        summary_rows,
        expected_shard_count=args.expected_shard_count,
    )
    summary = summarize_merged_rows(rows, summary_rows)
    write_csv(args.out, FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary, args)
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
    parser.add_argument("--shard", type=Path, action="append", required=True)
    parser.add_argument("--shard-summary", type=Path, action="append", default=[])
    parser.add_argument("--expected-shard-count", type=int, default=0)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_shards(paths: list[Path]) -> list[list[dict[str, str]]]:
    return [read_csv(path) for path in paths]


def read_summaries(paths: list[Path]) -> list[dict[str, str]]:
    rows = []
    for path in paths:
        summary_rows = read_csv(path)
        if len(summary_rows) != 1:
            raise ValueError(f"expected exactly one summary row in {path}")
        rows.append(summary_rows[0])
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def merge_rows(shards: list[list[dict[str, str]]]) -> list[dict[str, str]]:
    rows = [row for shard in shards for row in shard]
    seen: set[str] = set()
    for row in rows:
        pair_id = row.get("pair_id", "")
        if not pair_id:
            raise ValueError("shard row missing pair_id")
        if pair_id in seen:
            raise ValueError(f"duplicate pair_id across shards: {pair_id}")
        seen.add(pair_id)
    return sorted(rows, key=lambda row: row["pair_id"])


def summarize_merged_rows(
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> dict[str, object]:
    defined_rows = [
        row for row in rows if row.get("corrected_distance_status") == "defined"
    ]
    min_row = min(
        defined_rows,
        key=lambda row: float(row["corrected_distance"]),
        default=None,
    )
    params = merged_parameters(summary_rows)
    selected_pairs = (
        params.get("selected_pairs")
        if params.get("selected_pairs") not in ("", None)
        else str(len(rows))
    )
    shard_count = (
        params.get("shard_count")
        if params.get("shard_count") not in ("", None)
        else str(len(summary_rows) or 1)
    )
    return {
        "selected_pairs": selected_pairs,
        "shard_index": "merged",
        "shard_count": shard_count,
        "pairs": len(rows),
        "candidate_lane": params.get("candidate_lane", ""),
        "search_max_skip": params.get("search_max_skip", ""),
        "skip_cap_mode": params.get("skip_cap_mode", ""),
        "skip_cap_formula": params.get("skip_cap_formula", ""),
        "minimum_valid": params.get("minimum_valid", ""),
        "defined_corrected_distances": len(defined_rows),
        "ordinary_not_valid_pairs": count_status(rows, "ordinary_not_valid"),
        "under_minimum_valid_pairs": count_status(
            rows,
            "under_minimum_valid_perturbations",
        ),
        "min_corrected_distance": "" if min_row is None else min_row["corrected_distance"],
        "min_corrected_pair_id": "" if min_row is None else min_row["pair_id"],
        "max_pair_valid_perturbations": max(
            (int(row["pair_valid_perturbations"]) for row in rows),
            default=0,
        ),
        "status": "diagnostic_only_not_wrr_reproduction",
    }


def validate_merge_inputs(
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    *,
    expected_shard_count: int = 0,
) -> None:
    if not summary_rows:
        return
    expected_rows = sum(int_value(row.get("pairs", "")) for row in summary_rows)
    if expected_rows != len(rows):
        raise ValueError(f"shard summaries report {expected_rows} rows, merged CSV has {len(rows)}")
    shard_count = shard_count_from_summaries(summary_rows)
    if expected_shard_count and shard_count != expected_shard_count:
        raise ValueError(
            f"shard summaries use shard_count {shard_count}, expected {expected_shard_count}"
        )
    indexes = sorted(int_value(row.get("shard_index", "")) for row in summary_rows)
    expected_indexes = list(range(shard_count))
    if indexes != expected_indexes:
        raise ValueError(f"shard indexes {indexes} do not match expected {expected_indexes}")
    selected_values = {
        int_value(row.get("selected_pairs", ""))
        for row in summary_rows
        if row.get("selected_pairs", "") != ""
    }
    if len(selected_values) == 1 and len(rows) != next(iter(selected_values)):
        raise ValueError(
            f"merged CSV has {len(rows)} rows, selected_pairs reports {next(iter(selected_values))}"
        )


def shard_count_from_summaries(summary_rows: list[dict[str, str]]) -> int:
    values = {int_value(row.get("shard_count", "")) for row in summary_rows}
    if len(values) != 1:
        raise ValueError(f"shard summaries disagree on shard_count: {sorted(values)}")
    shard_count = next(iter(values))
    if shard_count < 1:
        raise ValueError("shard_count must be >= 1")
    return shard_count


def merged_parameters(summary_rows: list[dict[str, str]]) -> dict[str, str]:
    if not summary_rows:
        return {}
    fields = [
        "selected_pairs",
        "shard_count",
        "candidate_lane",
        "search_max_skip",
        "skip_cap_mode",
        "skip_cap_formula",
        "minimum_valid",
    ]
    params: dict[str, str] = {}
    for field in fields:
        values = {row.get(field, "") for row in summary_rows if row.get(field, "") != ""}
        if len(values) > 1:
            raise ValueError(f"shard summaries disagree on {field}: {sorted(values)}")
        params[field] = next(iter(values), "")
    return params


def int_value(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary: dict[str, object],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# WRR2 Corrected Distance Shard Merge",
        "",
        "Status: merged local/Windows shard outputs; diagnostic only.",
        "",
        f"- shard files: `{len(args.shard)}`",
        f"- merged rows: `{len(rows)}`",
        f"- defined corrected distances: `{summary['defined_corrected_distances']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key in SUMMARY_FIELDNAMES:
        lines.append(f"| `{key}` | {summary[key]} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "shards": [str(path) for path in args.shard],
        "shard_summaries": [str(path) for path in args.shard_summary],
        "rows": len(rows),
        "summary": summary,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
