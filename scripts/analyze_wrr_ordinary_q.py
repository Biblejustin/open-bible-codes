#!/usr/bin/env python3
"""Compute WRR ordinary Q diagnostics from defined minimality domains only."""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import load_corpus
from els.wrr import WrrElsOccurrence, ordinary_els_offsets, wrr_word_pair_proximity


PAIR_TABLE = Path("reports/wrr_1994/wrr2_pair_eligibility_table.csv")
DOMAIN_ASSIGNMENTS = Path("reports/wrr_1994/wrr2_domain_assignments.csv")
DOMAIN_SUMMARY = Path("reports/wrr_1994/wrr2_domain_summary.csv")
CONFIG = Path("configs/example_koren_genesis.toml")
OUT = Path("reports/wrr_1994/wrr2_ordinary_q_defined_only.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_ordinary_q_defined_only_summary.csv")
LANE_SUMMARY_OUT = Path("reports/wrr_1994/wrr2_ordinary_q_defined_only_lanes.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_ordinary_q_defined_only.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_ordinary_q_defined_only.manifest.json")

FIELDNAMES = [
    "pair_id",
    "concept",
    "candidate_lane",
    "pair_review_status",
    "appellation_term_id",
    "date_term_id",
    "appellation_hits",
    "appellation_defined_domains",
    "appellation_undefined_domains",
    "date_hits",
    "date_defined_domains",
    "date_undefined_domains",
    "defined_domain_pair_count",
    "ordinary_q_defined_only",
    "q_status",
    "read",
]

SUMMARY_FIELDNAMES = [
    "pairs",
    "pairs_with_defined_domain_pair",
    "all_observed_domains_defined_pairs",
    "defined_only_incomplete_pairs",
    "no_defined_domain_pair_pairs",
    "max_ordinary_q_defined_only",
    "max_q_pair_id",
    "status",
]

LANE_SUMMARY_FIELDNAMES = [
    "candidate_lane",
    "pairs",
    "pairs_with_defined_domain_pair",
    "all_observed_domains_defined_pairs",
    "defined_only_incomplete_pairs",
    "no_defined_domain_pair_pairs",
    "max_ordinary_q_defined_only",
    "max_q_pair_id",
]


@dataclass(frozen=True)
class DomainSummary:
    hit_count: int = 0
    defined_domains: int = 0
    undefined_domains: int = 0


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus = load_corpus(args.config)
    pair_rows = read_rows(args.pair_table)
    summaries = read_domain_summaries(args.domain_summary)
    occurrences = read_defined_occurrences(args.domain_assignments)
    rows = build_q_rows(
        pair_rows,
        summaries,
        occurrences,
        text_length=len(corpus.text),
        row_width_count=args.row_width_count,
    )
    summary = summarize_q_rows(rows)
    lane_rows = summarize_lane_rows(rows)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_rows(args.lane_summary_out, LANE_SUMMARY_FIELDNAMES, lane_rows)
    write_markdown(args.markdown_out, rows, summary, lane_rows, args)
    if args.manifest_out:
        write_manifest(args, corpus.summary(), rows, summary, lane_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.lane_summary_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair-table", type=Path, default=PAIR_TABLE)
    parser.add_argument("--domain-assignments", type=Path, default=DOMAIN_ASSIGNMENTS)
    parser.add_argument("--domain-summary", type=Path, default=DOMAIN_SUMMARY)
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--row-width-count", type=int, default=10)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--lane-summary-out", type=Path, default=LANE_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_domain_summaries(path: Path) -> dict[str, DomainSummary]:
    summaries: dict[str, DomainSummary] = {}
    for row in read_rows(path):
        summaries[row["term_id"]] = DomainSummary(
            hit_count=int_or_zero(row.get("hit_count")),
            defined_domains=int_or_zero(row.get("defined_domains")),
            undefined_domains=int_or_zero(row.get("undefined_domains")),
        )
    return summaries


def read_defined_occurrences(path: Path) -> dict[str, tuple[WrrElsOccurrence, ...]]:
    rows_by_term: dict[str, list[WrrElsOccurrence]] = {}
    for row in read_rows(path):
        if row.get("domain_status") != "defined":
            continue
        skip = int(row["skip"])
        offsets = ordinary_els_offsets(
            int(row["start_offset"]),
            skip,
            int(row["normalized_length"]),
        )
        occurrence = WrrElsOccurrence(
            offsets=offsets,
            skip=skip,
            domain_start=int(row["domain_start"]),
            domain_end=int(row["domain_end"]),
        )
        rows_by_term.setdefault(row["term_id"], []).append(occurrence)
    return {term_id: tuple(rows) for term_id, rows in rows_by_term.items()}


def build_q_rows(
    pair_rows: list[dict[str, str]],
    summaries: dict[str, DomainSummary],
    occurrences: dict[str, tuple[WrrElsOccurrence, ...]],
    *,
    text_length: int,
    row_width_count: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for pair in pair_rows:
        app_id = pair["appellation_term_id"]
        date_id = pair["date_term_id"]
        app_summary = summaries.get(app_id, DomainSummary())
        date_summary = summaries.get(date_id, DomainSummary())
        app_occurrences = occurrences.get(app_id, ())
        date_occurrences = occurrences.get(date_id, ())
        defined_pair_count = len(app_occurrences) * len(date_occurrences)
        q_value = ""
        if defined_pair_count:
            q_value = q_cell(
                wrr_word_pair_proximity(
                    app_occurrences,
                    date_occurrences,
                    text_length=text_length,
                    row_width_count=row_width_count,
                )
            )
        q_status = q_status_for(app_summary, date_summary, defined_pair_count)
        rows.append(
            {
                "pair_id": pair["pair_id"],
                "concept": pair.get("concept", ""),
                "candidate_lane": pair.get("candidate_lane", ""),
                "pair_review_status": pair.get("pair_review_status", ""),
                "appellation_term_id": app_id,
                "date_term_id": date_id,
                "appellation_hits": app_summary.hit_count,
                "appellation_defined_domains": app_summary.defined_domains,
                "appellation_undefined_domains": app_summary.undefined_domains,
                "date_hits": date_summary.hit_count,
                "date_defined_domains": date_summary.defined_domains,
                "date_undefined_domains": date_summary.undefined_domains,
                "defined_domain_pair_count": defined_pair_count,
                "ordinary_q_defined_only": q_value,
                "q_status": q_status,
                "read": read_label(q_status),
            }
        )
    return rows


def q_status_for(
    app_summary: DomainSummary,
    date_summary: DomainSummary,
    defined_pair_count: int,
) -> str:
    if defined_pair_count == 0:
        return "no_defined_domain_pair"
    if app_summary.undefined_domains or date_summary.undefined_domains:
        return "defined_domain_only_incomplete"
    return "all_observed_domains_defined"


def read_label(q_status: str) -> str:
    if q_status == "all_observed_domains_defined":
        return "ordinary Q diagnostic has all observed domains defined"
    if q_status == "defined_domain_only_incomplete":
        return "ordinary Q diagnostic uses defined domains only; undefined rows omitted"
    return "ordinary Q diagnostic unavailable because one side has no defined domain"


def summarize_q_rows(rows: list[dict[str, object]]) -> dict[str, object]:
    q_rows = [row for row in rows if row["ordinary_q_defined_only"] != ""]
    max_row = max(
        q_rows,
        key=lambda row: float(row["ordinary_q_defined_only"]),
        default=None,
    )
    return {
        "pairs": len(rows),
        "pairs_with_defined_domain_pair": len(q_rows),
        "all_observed_domains_defined_pairs": count_status(
            rows,
            "all_observed_domains_defined",
        ),
        "defined_only_incomplete_pairs": count_status(
            rows,
            "defined_domain_only_incomplete",
        ),
        "no_defined_domain_pair_pairs": count_status(rows, "no_defined_domain_pair"),
        "max_ordinary_q_defined_only": ""
        if max_row is None
        else max_row["ordinary_q_defined_only"],
        "max_q_pair_id": "" if max_row is None else max_row["pair_id"],
        "status": "diagnostic_only_not_corrected_distance",
    }


def summarize_lane_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    lanes = sorted({str(row["candidate_lane"]) for row in rows})
    return [summarize_lane(row_group(rows, "candidate_lane", lane), lane) for lane in lanes]


def summarize_lane(rows: list[dict[str, object]], lane: str) -> dict[str, object]:
    summary = summarize_q_rows(rows)
    return {
        "candidate_lane": lane,
        "pairs": summary["pairs"],
        "pairs_with_defined_domain_pair": summary["pairs_with_defined_domain_pair"],
        "all_observed_domains_defined_pairs": summary[
            "all_observed_domains_defined_pairs"
        ],
        "defined_only_incomplete_pairs": summary["defined_only_incomplete_pairs"],
        "no_defined_domain_pair_pairs": summary["no_defined_domain_pair_pairs"],
        "max_ordinary_q_defined_only": summary["max_ordinary_q_defined_only"],
        "max_q_pair_id": summary["max_q_pair_id"],
    }


def row_group(
    rows: list[dict[str, object]],
    field: str,
    value: str,
) -> list[dict[str, object]]:
    return [row for row in rows if str(row[field]) == value]


def count_status(rows: list[dict[str, object]], status: str) -> int:
    return sum(1 for row in rows if row["q_status"] == status)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    lane_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# WRR Ordinary Q Defined-Domain Diagnostic",
        "",
        f"- pair table: `{args.pair_table}`",
        f"- row width count: `{args.row_width_count}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
    ]
    for key, value in summary.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Candidate Lanes",
            "",
            "| Lane | Pairs | Defined-domain pairs | Complete | Incomplete | Unavailable | Max Q |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in lane_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["candidate_lane"]),
                    str(row["pairs"]),
                    str(row["pairs_with_defined_domain_pair"]),
                    str(row["all_observed_domains_defined_pairs"]),
                    str(row["defined_only_incomplete_pairs"]),
                    str(row["no_defined_domain_pair_pairs"]),
                    str(row["max_ordinary_q_defined_only"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Highest Defined-Domain Ordinary Q Rows",
            "",
            "| Pair ID | Concept | Lane | Defined domain pairs | Ordinary Q | Status |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    shown = 0
    for row in sorted(rows, key=q_sort_key):
        if row["ordinary_q_defined_only"] == "":
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["pair_id"]),
                    str(row["concept"]),
                    str(row["candidate_lane"]),
                    str(row["defined_domain_pair_count"]),
                    str(row["ordinary_q_defined_only"]),
                    str(row["q_status"]),
                ]
            )
            + " |"
        )
        shown += 1
        if shown >= 25:
            break
    if shown == 0:
        lines.append("| none |  |  | 0 |  | no_defined_domain_pair |")
    lines.extend(
        [
            "",
            "This diagnostic is not corrected distance `c(w,w')`. It uses only "
            "ELS rows with defined domains of minimality and marks incomplete "
            "pairs when undefined rows were omitted.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def q_sort_key(row: dict[str, object]) -> tuple[float, int, str]:
    q_value = row["ordinary_q_defined_only"]
    return (
        -float(q_value) if q_value != "" else 0.0,
        -int(row["defined_domain_pair_count"]),
        str(row["pair_id"]),
    )


def write_manifest(
    args: argparse.Namespace,
    corpus_summary: dict[str, object],
    rows: list[dict[str, object]],
    summary: dict[str, object],
    lane_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_wrr_ordinary_q",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "inputs": {
            "pair_table": str(args.pair_table),
            "domain_assignments": str(args.domain_assignments),
            "domain_summary": str(args.domain_summary),
            "config": str(args.config),
            "corpus": corpus_summary,
        },
        "parameters": {"row_width_count": args.row_width_count},
        "outputs": {
            "rows": str(args.out),
            "summary": str(args.summary_out),
            "lane_summary": str(args.lane_summary_out),
            "markdown": str(args.markdown_out),
        },
        "counts": {"rows": len(rows), "lane_rows": len(lane_rows), **summary},
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def q_cell(value: float) -> str:
    return f"{value:.12g}"


def int_or_zero(value: str | None) -> int:
    if value in (None, ""):
        return 0
    return int(value)


if __name__ == "__main__":
    raise SystemExit(main())
