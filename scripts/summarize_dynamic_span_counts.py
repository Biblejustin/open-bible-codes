#!/usr/bin/env python3
"""Summarize dynamic-span count outputs."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


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
DEFAULT_OUT = Path("docs/DYNAMIC_SKIP_FOCUS_COUNTS.md")
DEFAULT_MANIFEST = Path("reports/dynamic_skip_focus/summary.manifest.json")


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_all(args.input)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args.manifest_out, args, rows, started)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, action="append", default=[])
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_all(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths or DEFAULT_INPUTS:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                item = dict(row)
                item["source_file"] = str(path)
                rows.append(item)
    return rows


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_mode = Counter(row["mode"] for row in rows)
    by_corpus = Counter(row["corpus"] for row in rows)
    lines = [
        "# Dynamic Skip Focus Counts",
        "",
        "This report records completed full-distance ELS counts for the selected",
        "focus terms. These are observed counts, not expectation-only planning",
        "numbers. `letters-per-term` uses `floor(corpus_letters / term_letters)`;",
        "`full-span` uses the largest skip where the term can still fit in the",
        "corpus.",
        "",
        "Reproduce with:",
        "",
        "```bash",
        "python3 -m scripts.run_protocol protocols/dynamic_skip_focus_counts.toml --resume",
        "python3 -m scripts.summarize_dynamic_span_counts",
        "```",
        "",
        "The full-span rows are intentional search targets. Expected-hit estimates",
        "are useful for planning runtime and controls, but they do not replace",
        "running the search.",
        "",
        "Bible and non-Bible rows are intentionally listed together here so the",
        "same search rule can be compared across language-matched background",
        "texts. English rows are secondary evidence only; absence or presence in",
        "English translation does not decide an original-language hypothesis.",
        "",
        "## Run Counts",
        "",
        f"- Rows counted: {len(rows):,}",
        f"- Modes: `{dict(sorted(by_mode.items()))}`",
        f"- Corpora: `{dict(sorted(by_corpus.items()))}`",
        "",
        "## Selected Local / Modern Rows",
        "",
        "| Corpus | Mode | Term | Count | Rate / 1M positions | Forward | Backward | Max skip | Seconds |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    focus_ids = {
        "dyn_trump_e",
        "dyn_vance_e",
        "dyn_netanyahu_e",
        "dyn_iran_e",
        "dyn_cowboy_e",
        "dyn_catering_e",
        "dyn_simsberry_e",
        "dyn_simscorner_e",
        "dyn_trump_h",
        "dyn_vance_h",
        "dyn_netanyahu_h",
        "dyn_iran_h",
        "dyn_trump_g",
        "dyn_vance_g",
        "dyn_netanyahu_g",
        "dyn_iran_g",
    }
    for row in sorted(
        (row for row in rows if row["term_id"] in focus_ids),
        key=lambda item: (item["term_id"], item["corpus"], item["mode"]),
    ):
        lines.append(table_row(row))
    lines.extend(
        [
            "",
            "## Highest Counts",
            "",
            "| Corpus | Mode | Term | Count | Rate / 1M positions | Forward | Backward | Max skip | Seconds |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in sorted(rows, key=lambda item: int(item["hit_count"] or 0), reverse=True)[:40]:
        lines.append(table_row(row))
    lines.extend(
        [
            "",
            "## Lowest Nonzero Counts",
            "",
            "| Corpus | Mode | Term | Count | Rate / 1M positions | Forward | Backward | Max skip | Seconds |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    nonzero = [row for row in rows if int(row["hit_count"] or 0) > 0]
    for row in sorted(nonzero, key=lambda item: int(item["hit_count"]))[:40]:
        lines.append(table_row(row))
    zero_count = sum(1 for row in rows if int(row["hit_count"] or 0) == 0)
    lines.extend(
        [
            "",
            "## Read",
            "",
            f"- Zero-count rows: {zero_count:,}",
            "- Large counts are expected for short terms and large skip spaces.",
            "- These counts answer presence/density. Context, exact center-word,",
            "  same-skip extension, and non-Bible controls remain separate reports.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def table_row(row: dict[str, str]) -> str:
    return (
        f"| {row['corpus']} | `{row['mode']}` | `{row['term_id']}` "
        f"| {row['hit_count']} | {row.get('hits_per_million_positions', '')} "
        f"| {row['forward_count']} | {row['backward_count']} "
        f"| {row['effective_max_skip']} | {round(float(row['counter_elapsed_seconds'] or 0), 3)} |"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "script": "scripts/summarize_dynamic_span_counts.py",
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
