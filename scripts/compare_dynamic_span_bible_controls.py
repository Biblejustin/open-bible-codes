#!/usr/bin/env python3
"""Compare dynamic-span Bible counts against language-matched controls."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import subprocess
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


BIBLE_CORPORA = {
    "MT_WLC",
    "UXLC",
    "MAM",
    "EBIBLE_WLC",
    "UHB",
    "LXX",
    "TR_NT",
    "BYZ_NT",
    "TCG_NT",
    "SBLGNT",
    "KJV",
}

DEFAULT_INPUTS = [
    Path("reports/dynamic_skip_focus/english_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/greek_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/hebrew_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/english_full_span_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/greek_full_span_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/hebrew_full_span_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/nonbible_english_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/nonbible_greek_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/nonbible_hebrew_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/nonbible_english_full_span_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/nonbible_greek_full_span_pair_counts.csv"),
    Path("reports/dynamic_skip_focus/nonbible_hebrew_full_span_pair_counts.csv"),
]
DEFAULT_OUT = Path("reports/dynamic_skip_focus/bible_control_comparison.csv")
DEFAULT_MARKDOWN = Path("docs/DYNAMIC_SKIP_BIBLE_CONTROL_COMPARISON.md")
DEFAULT_MANIFEST = Path("reports/dynamic_skip_focus/bible_control_comparison.manifest.json")

FIELDNAMES = [
    "term_id",
    "concept",
    "term_language",
    "mode",
    "bible_rows",
    "control_rows",
    "bible_present_rows",
    "control_present_rows",
    "bible_max_corpus",
    "bible_max_hit_count",
    "bible_max_rate_per_million",
    "control_max_corpus",
    "control_max_hit_count",
    "control_max_rate_per_million",
    "control_median_rate_per_million",
    "bible_over_control_max_rate_ratio",
    "bible_over_control_median_rate_ratio",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_rows(args.input or DEFAULT_INPUTS)
    comparison_rows = compare(rows)
    write_csv(args.out, comparison_rows)
    write_markdown(args.markdown_out, comparison_rows, args)
    write_manifest(args.manifest_out, args, comparison_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, action="append", default=[])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["source_file"] = str(path)
                rows.append(item)
    return rows


def compare(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["term_id"], row["mode"])].append(row)

    output = []
    for (_term_id, _mode), group in sorted(grouped.items()):
        bible_rows = [row for row in group if corpus_class(row["corpus"]) == "bible"]
        control_rows = [row for row in group if corpus_class(row["corpus"]) == "control"]
        if not bible_rows:
            continue
        bible_max = max(bible_rows, key=rate)
        control_max = max(control_rows, key=rate) if control_rows else None
        control_rates = [rate(row) for row in control_rows]
        control_median = statistics.median(control_rates) if control_rates else None
        output.append(
            {
                "term_id": group[0]["term_id"],
                "concept": group[0].get("concept", ""),
                "term_language": group[0].get("term_language", ""),
                "mode": group[0]["mode"],
                "bible_rows": str(len(bible_rows)),
                "control_rows": str(len(control_rows)),
                "bible_present_rows": str(sum(hit_count(row) > 0 for row in bible_rows)),
                "control_present_rows": str(sum(hit_count(row) > 0 for row in control_rows)),
                "bible_max_corpus": bible_max["corpus"],
                "bible_max_hit_count": bible_max["hit_count"],
                "bible_max_rate_per_million": str(round_float(rate(bible_max))),
                "control_max_corpus": control_max["corpus"] if control_max else "",
                "control_max_hit_count": control_max["hit_count"] if control_max else "",
                "control_max_rate_per_million": str(round_float(rate(control_max))) if control_max else "",
                "control_median_rate_per_million": str(round_float(control_median)) if control_median is not None else "",
                "bible_over_control_max_rate_ratio": ratio_text(rate(bible_max), rate(control_max) if control_max else None),
                "bible_over_control_median_rate_ratio": ratio_text(rate(bible_max), control_median),
                "read": read_label(rate(bible_max), rate(control_max) if control_max else None, control_median),
            }
        )
    return output


def corpus_class(label: str) -> str:
    return "bible" if label in BIBLE_CORPORA else "control"


def hit_count(row: dict[str, str]) -> int:
    return int(row.get("hit_count") or 0)


def rate(row: dict[str, str] | None) -> float:
    if row is None:
        return 0.0
    value = row.get("hits_per_million_positions")
    if value not in {None, ""}:
        return float(value)
    search_space = int(row.get("search_space_positions") or 0)
    if search_space <= 0:
        return 0.0
    return 1_000_000 * hit_count(row) / search_space


def ratio_text(numerator: float, denominator: float | None) -> str:
    if denominator is None:
        return ""
    if denominator == 0:
        return "inf" if numerator > 0 else ""
    return str(round_float(numerator / denominator))


def round_float(value: float | None) -> float | str:
    if value is None:
        return ""
    return round(value, 6)


def read_label(bible_rate: float, control_max_rate: float | None, control_median_rate: float | None) -> str:
    if control_max_rate is None or control_median_rate is None:
        return "needs language-matched control run"
    if bible_rate > control_max_rate:
        return "bible max rate exceeds all observed controls"
    if bible_rate > control_median_rate:
        return "bible max rate exceeds control median but not control max"
    return "control background equals or exceeds bible max rate"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Dynamic Skip Bible-Control Comparison",
        "",
        "This report compares the selected dynamic-skip terms in Bible corpora",
        "against language-matched non-Bible controls using the same search rule.",
        "It reports normalized hit rates per million legal ELS positions, not only",
        "raw hit totals.",
        "",
        "The primary hypothesis concerns original-language Bible texts. English",
        "rows are secondary translation evidence: a KJV hit may be interesting,",
        "but KJV absence does not count against an original-language hypothesis.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "python3 -m scripts.run_protocol protocols/dynamic_skip_focus_counts.toml --resume",
        "python3 -m scripts.compare_dynamic_span_bible_controls",
        "```",
        "",
        "## Strongest Bible-Over-Control Rows",
        "",
        "| Term | Language | Mode | Bible max | Control max | Control median | Ratio vs max | Read |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in sorted(rows, key=ratio_sort_key, reverse=True)[:40]:
        lines.append(comparison_table_row(row))
    lines.extend(
        [
            "",
            "## Control-Background Rows",
            "",
            "| Term | Language | Mode | Bible max | Control max | Control median | Ratio vs max | Read |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in sorted(rows, key=ratio_sort_key)[:40]:
        lines.append(comparison_table_row(row))
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- This is an observed-control comparison, not a final claim test.",
            "- A favorable row should still be checked for all-hit context,",
            "  version/source distribution, same-skip extensions, and matched",
            "  shuffled or real-word controls.",
            "- A non-Bible match does not disprove the hypothesis by itself, but it",
            "  raises the background rate that a Bible pattern must exceed.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def ratio_sort_key(row: dict[str, str]) -> float:
    value = row["bible_over_control_max_rate_ratio"]
    if value == "inf":
        return float("inf")
    if value == "":
        return 0.0
    return float(value)


def comparison_table_row(row: dict[str, str]) -> str:
    return (
        f"| `{row['term_id']}` | {row['term_language']} | `{row['mode']}` "
        f"| {row['bible_max_rate_per_million']} | {row['control_max_rate_per_million']} "
        f"| {row['control_median_rate_per_million']} "
        f"| {row['bible_over_control_max_rate_ratio']} | {row['read']} |"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "script": "scripts/compare_dynamic_span_bible_controls.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "rows": len(rows),
        "git_commit": git_commit(),
    }
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
