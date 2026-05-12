#!/usr/bin/env python3
"""Summarize WRR imported-term count smoke outputs."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.term_display import display_term


COUNTS_OUT = Path("reports/wrr_1994/wrr2_genesis_counts.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_genesis_count_summary.csv")
TOP_OUT = Path("reports/wrr_1994/wrr2_genesis_top_counts.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_genesis_count_summary.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_genesis_count_summary.manifest.json")

SUMMARY_FIELDNAMES = [
    "concept",
    "appellation_rows",
    "date_rows",
    "appellation_hits",
    "date_hits",
    "zero_appellation_rows",
    "zero_date_rows",
    "best_appellation_term_id",
    "best_appellation_hits",
    "best_date_term_id",
    "best_date_hits",
]

TOP_FIELDNAMES = [
    "rank",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "normalized_length",
    "hit_count",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_rows(args.counts)
    summary_rows = summarize_by_concept(rows)
    top_rows = top_counts(rows, args.top)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.top_out, TOP_FIELDNAMES, top_rows)
    write_markdown(args.markdown_out, rows, summary_rows, top_rows)
    if args.manifest_out:
        write_manifest(args, rows, summary_rows, top_rows, started)
    print(args.summary_out)
    print(args.top_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts", type=Path, default=COUNTS_OUT)
    parser.add_argument("--top", type=int, default=30)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--top-out", type=Path, default=TOP_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize_by_concept(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    by_concept: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_concept[row.get("concept", "")].append(row)
    output = []
    for concept, group in by_concept.items():
        apps = [row for row in group if row.get("category") == "wrr_appellation"]
        dates = [row for row in group if row.get("category") == "wrr_date"]
        best_app = best_row(apps)
        best_date = best_row(dates)
        output.append(
            {
                "concept": concept,
                "appellation_rows": len(apps),
                "date_rows": len(dates),
                "appellation_hits": sum(hit_count(row) for row in apps),
                "date_hits": sum(hit_count(row) for row in dates),
                "zero_appellation_rows": sum(1 for row in apps if hit_count(row) == 0),
                "zero_date_rows": sum(1 for row in dates if hit_count(row) == 0),
                "best_appellation_term_id": best_app.get("term_id", "") if best_app else "",
                "best_appellation_hits": hit_count(best_app) if best_app else "",
                "best_date_term_id": best_date.get("term_id", "") if best_date else "",
                "best_date_hits": hit_count(best_date) if best_date else "",
            }
        )
    return sorted(output, key=lambda row: str(row["concept"]))


def top_counts(rows: list[dict[str, str]], limit: int) -> list[dict[str, object]]:
    counted = [row for row in rows if row.get("status") == "counted"]
    output = []
    for rank, row in enumerate(sorted(counted, key=hit_count, reverse=True)[:limit], start=1):
        output.append(
            {
                "rank": rank,
                "term_id": row["term_id"],
                "concept": row["concept"],
                "category": row["category"],
                "normalized_term": row["normalized_term"],
                "normalized_length": int_or_zero(row.get("normalized_length")),
                "hit_count": hit_count(row),
            }
        )
    return output


def best_row(rows: list[dict[str, str]]) -> dict[str, str] | None:
    if not rows:
        return None
    return max(rows, key=hit_count)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    top_rows: list[dict[str, object]],
) -> None:
    category_counts = category_summary(rows)
    lines = [
        "# WRR2 Genesis Count Audit",
        "",
        "This is a source/import smoke report for the external WRR2 list. It is not the WRR aggregate statistic.",
        "",
        "## Scope",
        "",
        "- Corpus: Koren Genesis Michigan-Claremont",
        "- Skip range: `2..250`",
        "- Direction: `both`",
        "- Terms: external WRR2 list converted into ignored report CSV rows",
        "",
        "## Category Summary",
        "",
        "| Category | Rows | Zero rows | Total hits |",
        "| --- | ---: | ---: | ---: |",
    ]
    for category, stats in sorted(category_counts.items()):
        lines.append(
            f"| `{category}` | {stats['rows']} | {stats['zero_rows']} | {stats['total_hits']} |"
        )
    lines.extend(
        [
            "",
            "## Top Count Rows",
            "",
            "| Rank | Term | Concept | Category | Length | Hits |",
            "| ---: | --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in top_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["rank"]),
                    display_top_term(row),
                    str(row["concept"]),
                    f"`{row['category']}`",
                    str(row["normalized_length"]),
                    str(row["hit_count"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Record Summary",
            "",
            "| Concept | App rows | Date rows | App hits | Date hits | Best app | Best date |",
            "| --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in summary_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["concept"]),
                    str(row["appellation_rows"]),
                    str(row["date_rows"]),
                    str(row["appellation_hits"]),
                    str(row["date_hits"]),
                    f"`{row['best_appellation_term_id']}` ({row['best_appellation_hits']})",
                    f"`{row['best_date_term_id']}` ({row['best_date_hits']})",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Caution",
            "",
            "Raw counts only confirm that imported terms can be searched. WRR replication still needs the declared distance metric and permutation statistic.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def display_top_term(row: dict[str, object]) -> str:
    term_id = str(row["term_id"])
    term = display_term(str(row["normalized_term"]), english=str(row.get("concept", "")) or None)
    return f"`{term_id}` {term}"


def category_summary(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    output: dict[str, dict[str, int]] = {}
    for row in rows:
        category = row.get("category", "")
        stats = output.setdefault(category, {"rows": 0, "zero_rows": 0, "total_hits": 0})
        stats["rows"] += 1
        count = hit_count(row)
        stats["total_hits"] += count
        if count == 0:
            stats["zero_rows"] += 1
    return output


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    top_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "counts": str(args.counts),
        "rows": len(rows),
        "summary_rows": len(summary_rows),
        "top_rows": len(top_rows),
        "outputs": {
            "summary": str(args.summary_out),
            "top": str(args.top_out),
            "markdown": str(args.markdown_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def hit_count(row: dict[str, str] | None) -> int:
    if row is None:
        return 0
    return int_or_zero(row.get("hit_count", ""))


def int_or_zero(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
