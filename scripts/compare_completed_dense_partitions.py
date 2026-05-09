#!/usr/bin/env python3
"""Compare completed dense full-span partition exports by term."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from scripts.export_dynamic_span_hits import ROOT
from scripts.summarize_dynamic_span_partition_outputs import DEFAULT_TERM_SUMMARY


CONTROL_PREFIXES = ("HEB_PBY_", "GRC_PERSEUS_", "ENG_PG_")
DEFAULT_OUT = ROOT / "reports/dynamic_skip_focus/completed_dense_bible_control_comparison.csv"
DEFAULT_MARKDOWN = ROOT / "docs/DYNAMIC_SKIP_COMPLETED_DENSE_COMPARISON.md"
DEFAULT_MANIFEST = ROOT / "reports/dynamic_skip_focus/completed_dense_bible_control_comparison.manifest.json"

FIELDNAMES = [
    "term_id",
    "mode",
    "completion_read",
    "bible_completed_corpora",
    "control_completed_corpora",
    "bible_completed_hits",
    "control_completed_hits",
    "bible_exact_center_word_hits",
    "control_exact_center_word_hits",
    "bible_max_corpus",
    "bible_max_hits",
    "control_max_corpus",
    "control_max_hits",
    "control_over_bible_hits_ratio",
    "control_over_bible_exact_center_ratio",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_rows(args.term_summary)
    comparison_rows = compare_completed(rows)
    write_csv(args.out, FIELDNAMES, comparison_rows)
    write_markdown(args.markdown_out, comparison_rows, args)
    write_manifest(args.manifest_out, args, comparison_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--term-summary", type=Path, default=DEFAULT_TERM_SUMMARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def compare_completed(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("coverage_status") == "complete":
            grouped[(row["term_id"], row["mode"])].append(row)

    output = []
    for (term_id, mode), group in sorted(grouped.items()):
        bible_rows = sorted((row for row in group if not is_control_corpus(row["corpus"])), key=lambda row: row["corpus"])
        control_rows = sorted((row for row in group if is_control_corpus(row["corpus"])), key=lambda row: row["corpus"])
        bible_hits = sum(hit_count(row) for row in bible_rows)
        control_hits = sum(hit_count(row) for row in control_rows)
        bible_exact = sum(exact_hits(row) for row in bible_rows)
        control_exact = sum(exact_hits(row) for row in control_rows)
        bible_max = max(bible_rows, key=hit_count) if bible_rows else None
        control_max = max(control_rows, key=hit_count) if control_rows else None
        output.append(
            {
                "term_id": term_id,
                "mode": mode,
                "completion_read": completion_read(bible_rows, control_rows),
                "bible_completed_corpora": ", ".join(row["corpus"] for row in bible_rows),
                "control_completed_corpora": ", ".join(row["corpus"] for row in control_rows),
                "bible_completed_hits": str(bible_hits),
                "control_completed_hits": str(control_hits),
                "bible_exact_center_word_hits": str(bible_exact),
                "control_exact_center_word_hits": str(control_exact),
                "bible_max_corpus": bible_max["corpus"] if bible_max else "",
                "bible_max_hits": str(hit_count(bible_max)) if bible_max else "",
                "control_max_corpus": control_max["corpus"] if control_max else "",
                "control_max_hits": str(hit_count(control_max)) if control_max else "",
                "control_over_bible_hits_ratio": ratio_text(control_hits, bible_hits),
                "control_over_bible_exact_center_ratio": ratio_text(control_exact, bible_exact),
            }
        )
    return output


def completion_read(bible_rows: list[dict[str, str]], control_rows: list[dict[str, str]]) -> str:
    if bible_rows and control_rows:
        return "completed bible and control dense exports available"
    if bible_rows:
        return "completed bible dense export available; control still deferred or absent"
    return "completed control dense export available; bible still deferred or absent"


def hit_count(row: dict[str, str] | None) -> int:
    return int(row.get("completed_exported_hits") or 0) if row else 0


def exact_hits(row: dict[str, str] | None) -> int:
    return int(row.get("exact_center_word_hits") or 0) if row else 0


def ratio_text(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "inf" if numerator > 0 else ""
    return str(round(numerator / denominator, 6))


def is_control_corpus(corpus: str) -> bool:
    return corpus.startswith(CONTROL_PREFIXES)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    both = [row for row in rows if row["bible_completed_corpora"] and row["control_completed_corpora"]]
    bible_only = [row for row in rows if row["bible_completed_corpora"] and not row["control_completed_corpora"]]
    control_only = [row for row in rows if row["control_completed_corpora"] and not row["bible_completed_corpora"]]
    lines = [
        "# Completed Dense Bible-Control Comparison",
        "",
        "This report compares only dense full-span rows whose partition exports are complete.",
        "It is a hit-level completion view, not a normalized rate test. Use",
        "`docs/DYNAMIC_SKIP_BIBLE_CONTROL_COMPARISON.md` for normalized count-rate background.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "python3 -m scripts.summarize_dynamic_span_partition_outputs",
        "python3 -m scripts.compare_completed_dense_partitions",
        "```",
        "",
        "## Scope",
        "",
        f"- compared term/mode rows: {len(rows):,}",
        f"- completed on Bible and controls: {len(both):,}",
        f"- completed on Bible only: {len(bible_only):,}",
        f"- completed on controls only: {len(control_only):,}",
        f"- input term summary: `{display_path(args.term_summary)}`",
        f"- output CSV: `{display_path(args.out)}`",
        "",
        "## Completed On Both Bible And Controls",
        "",
        "| Term | Mode | Bible hits | Control hits | Bible exact center | Control exact center | Control/Bible raw hit ratio |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in sorted(both, key=lambda item: int(item["control_completed_hits"]), reverse=True)[:60]:
        lines.append(summary_row(row))
    lines.extend(
        [
            "",
            "## Bible-Only Completed Rows",
            "",
            "| Term | Mode | Corpora | Hits | Exact center hits |",
            "| --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in sorted(bible_only, key=lambda item: int(item["bible_completed_hits"]), reverse=True)[:60]:
        lines.append(
            f"| `{row['term_id']}` | `{row['mode']}` | {row['bible_completed_corpora']} | "
            f"{int(row['bible_completed_hits']):,} | {int(row['bible_exact_center_word_hits']):,} |"
        )
    lines.extend(
        [
            "",
            "## Control-Only Completed Rows",
            "",
            "| Term | Mode | Corpora | Hits | Exact center hits |",
            "| --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in sorted(control_only, key=lambda item: int(item["control_completed_hits"]), reverse=True)[:60]:
        lines.append(
            f"| `{row['term_id']}` | `{row['mode']}` | {row['control_completed_corpora']} | "
            f"{int(row['control_completed_hits']):,} | {int(row['control_exact_center_word_hits']):,} |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Exact center-word hits are retained as flags, not as the gate for inclusion.",
            "- Raw dense hit totals are useful for triage, but corpus lengths differ.",
            "- Completion status matters: absence from this report may mean the dense partition remains deferred.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def summary_row(row: dict[str, str]) -> str:
    return (
        f"| `{row['term_id']}` | `{row['mode']}` | {int(row['bible_completed_hits']):,} | "
        f"{int(row['control_completed_hits']):,} | {int(row['bible_exact_center_word_hits']):,} | "
        f"{int(row['control_exact_center_word_hits']):,} | {row['control_over_bible_hits_ratio']} |"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "script": "scripts/compare_completed_dense_partitions.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "rows": len(rows),
        "term_summary": display_path(args.term_summary),
        "out": display_path(args.out),
        "markdown_out": display_path(args.markdown_out),
        "git_commit": git_commit(),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
