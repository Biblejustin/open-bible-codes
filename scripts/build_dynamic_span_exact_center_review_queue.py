#!/usr/bin/env python3
"""Build a word-level review queue from dynamic-span exact-center rows."""

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
from scripts.compare_dynamic_span_bible_controls import BIBLE_CORPORA


DEFAULT_IN = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_rows.csv")
DEFAULT_OUT = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_review_queue.csv")
DEFAULT_MARKDOWN = Path("docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_REVIEW_QUEUE.md")
DEFAULT_MANIFEST = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_review_queue.manifest.json")

QUEUE_FIELDNAMES = [
    "rank",
    "corpus_class",
    "corpus",
    "term_id",
    "normalized_term",
    "center_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "center_normalized_word",
    "exact_center_paths",
    "forward_paths",
    "backward_paths",
    "min_abs_skip",
    "max_abs_skip",
    "min_span_letters",
    "max_span_letters",
    "example_skip",
    "example_direction",
    "example_start_ref",
    "example_end_ref",
    "example_start_offset",
    "example_center_offset",
    "example_end_offset",
    "source_kinds",
    "source_paths",
    "review_bucket",
]


class ReviewUnit:
    def __init__(self, first: dict[str, str]) -> None:
        self.corpus = first.get("corpus", "")
        self.term_id = first.get("term_id", "")
        self.normalized_term = first.get("normalized_term", "")
        self.center_ref = first.get("center_ref", "")
        self.center_source = first.get("center_source", "")
        self.center_word_index = first.get("center_word_index", "")
        self.center_word = first.get("center_word", "")
        self.center_normalized_word = first.get("center_normalized_word", "")
        self.rows = 0
        self.direction_counts: Counter[str] = Counter()
        self.abs_skips: list[int] = []
        self.spans: list[int] = []
        self.source_kinds: Counter[str] = Counter()
        self.source_paths: Counter[str] = Counter()
        self.example = first

    @property
    def corpus_class(self) -> str:
        return "bible" if self.corpus in BIBLE_CORPORA else "control"

    def add(self, row: dict[str, str]) -> None:
        self.rows += 1
        direction = row.get("direction", "")
        if direction:
            self.direction_counts[direction] += 1
        skip = parse_int(row.get("skip", ""))
        if skip is not None:
            self.abs_skips.append(abs(skip))
        span = parse_int(row.get("span_letters", ""))
        if span is not None:
            self.spans.append(span)
        source_kind = row.get("source_kind", "")
        if source_kind:
            self.source_kinds[source_kind] += 1
        source_path = row.get("source_path", "")
        if source_path:
            self.source_paths[source_path] += 1
        if better_example(row, self.example):
            self.example = row

    def sort_key(self) -> tuple[int, int, int, str, str, str, str, int]:
        return (
            0 if self.corpus_class == "bible" else 1,
            -self.rows,
            min(self.abs_skips) if self.abs_skips else 0,
            self.corpus,
            self.term_id,
            self.center_ref,
            self.center_source,
            parse_int(self.center_word_index) or 0,
        )

    def to_row(self, rank: int) -> dict[str, str]:
        example = self.example
        return {
            "rank": str(rank),
            "corpus_class": self.corpus_class,
            "corpus": self.corpus,
            "term_id": self.term_id,
            "normalized_term": self.normalized_term,
            "center_ref": self.center_ref,
            "center_source": self.center_source,
            "center_word_index": self.center_word_index,
            "center_word": self.center_word,
            "center_normalized_word": self.center_normalized_word,
            "exact_center_paths": str(self.rows),
            "forward_paths": str(self.direction_counts.get("forward", 0)),
            "backward_paths": str(self.direction_counts.get("backward", 0)),
            "min_abs_skip": str(min(self.abs_skips)) if self.abs_skips else "",
            "max_abs_skip": str(max(self.abs_skips)) if self.abs_skips else "",
            "min_span_letters": str(min(self.spans)) if self.spans else "",
            "max_span_letters": str(max(self.spans)) if self.spans else "",
            "example_skip": example.get("skip", ""),
            "example_direction": example.get("direction", ""),
            "example_start_ref": example.get("start_ref", ""),
            "example_end_ref": example.get("end_ref", ""),
            "example_start_offset": example.get("start_offset", ""),
            "example_center_offset": example.get("center_offset", ""),
            "example_end_offset": example.get("end_offset", ""),
            "source_kinds": format_counter(self.source_kinds, 4),
            "source_paths": format_counter(self.source_paths, 3),
            "review_bucket": review_bucket(self),
        }


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    result = build_queue(args.input)
    write_csv(args.out, result["rows"])
    write_markdown(args.markdown_out, result, args)
    write_manifest(args.manifest_out, result, args, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_IN)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--top", type=int, default=40)
    return parser


def build_queue(path: Path) -> dict[str, Any]:
    units: dict[tuple[str, ...], ReviewUnit] = {}
    total_rows = 0
    for row in read_rows(path):
        total_rows += 1
        key = review_key(row)
        if key not in units:
            units[key] = ReviewUnit(row)
        units[key].add(row)
    ordered = sorted(units.values(), key=lambda unit: unit.sort_key())
    output_rows = [unit.to_row(rank) for rank, unit in enumerate(ordered, 1)]
    return {
        "input": str(path),
        "total_exact_rows": total_rows,
        "review_units": len(output_rows),
        "rows": output_rows,
        "corpus_counts": Counter(row["corpus"] for row in output_rows),
        "class_counts": Counter(row["corpus_class"] for row in output_rows),
        "term_counts": Counter((row["corpus"], row["term_id"]) for row in output_rows),
    }


def review_key(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row.get("corpus", ""),
        row.get("term_id", ""),
        row.get("normalized_term", ""),
        row.get("center_ref", ""),
        row.get("center_source", ""),
        row.get("center_word_index", ""),
        row.get("center_normalized_word", ""),
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=QUEUE_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, result: dict[str, Any], args: argparse.Namespace) -> None:
    rows = result["rows"]
    bible_rows = [row for row in rows if row["corpus_class"] == "bible"]
    control_rows = [row for row in rows if row["corpus_class"] == "control"]
    lines = [
        "# Strong Full-Span Exact-Center Review Queue",
        "",
        "This report condenses exact-center ELS paths into surface-word review units.",
        "One review unit is one corpus, term, center ref/source, and center word index.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Scope",
        "",
        f"- input exact rows: `{args.input}`",
        f"- exact-center paths read: {result['total_exact_rows']:,}",
        f"- word-level review units: {result['review_units']:,}",
        f"- Bible review units: {len(bible_rows):,}",
        f"- control review units: {len(control_rows):,}",
        f"- queue CSV: `{args.out}`",
        "",
        "## Top Bible Review Units",
        "",
        "| Rank | Corpus | Term | Center | Word index | Surface word | Paths | Skip range | Example path |",
        "| ---: | --- | --- | --- | ---: | --- | ---: | ---: | --- |",
    ]
    for row in bible_rows[: args.top]:
        lines.append(review_table_row(row))
    lines.extend(
        [
            "",
            "## Top Control Review Units",
            "",
            "| Rank | Corpus | Term | Center | Word index | Surface word | Paths | Skip range | Example path |",
            "| ---: | --- | --- | --- | ---: | --- | ---: | ---: | --- |",
        ]
    )
    for row in control_rows[: args.top]:
        lines.append(review_table_row(row))
    lines.extend(
        [
            "",
            "## Corpus Summary",
            "",
            "| Corpus | Class | Review units | Exact-center paths |",
            "| --- | --- | ---: | ---: |",
        ]
    )
    for corpus, group in corpus_groups(rows):
        lines.append(
            f"| {corpus} | {group[0]['corpus_class']} | {len(group):,} | "
            f"{sum(int(row['exact_center_paths']) for row in group):,} |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- This is a review queue, not a claim promotion rule.",
            "- High path count means many hidden paths center on the same surface word.",
            "- Bible rows should still be read against language-matched controls and ordinary surface frequency.",
            "- Non-Bible controls often use source-level refs; inspect `center_source`, `center_word_index`, and offsets in the CSV.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def review_table_row(row: dict[str, str]) -> str:
    example = (
        f"{row['example_start_ref']} -> {row['center_ref']} -> {row['example_end_ref']} "
        f"({row['example_direction']} {row['example_skip']})"
    )
    skip_range = f"{row['min_abs_skip']}..{row['max_abs_skip']}"
    return (
        f"| {row['rank']} | {row['corpus']} | `{row['term_id']}` | {row['center_ref']} | "
        f"{row['center_word_index']} | {row['center_word']} | {int(row['exact_center_paths']):,} | "
        f"{skip_range} | {example} |"
    )


def corpus_groups(rows: list[dict[str, str]]) -> list[tuple[str, list[dict[str, str]]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["corpus"], []).append(row)
    return sorted(
        grouped.items(),
        key=lambda item: (0 if item[1][0]["corpus_class"] == "bible" else 1, item[0]),
    )


def write_manifest(path: Path, result: dict[str, Any], args: argparse.Namespace, started: float) -> None:
    payload = {
        "script": "scripts/build_dynamic_span_exact_center_review_queue.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "input": str(args.input),
        "out": str(args.out),
        "markdown_out": str(args.markdown_out),
        "total_exact_rows": result["total_exact_rows"],
        "review_units": result["review_units"],
        "git_commit": git_commit(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def review_bucket(unit: ReviewUnit) -> str:
    if unit.corpus_class == "control":
        return "control background"
    if unit.rows >= 25:
        return "bible high-path review"
    if unit.rows >= 5:
        return "bible medium-path review"
    return "bible low-count review"


def better_example(candidate: dict[str, str], current: dict[str, str]) -> bool:
    candidate_skip = abs(parse_int(candidate.get("skip", "")) or 0)
    current_skip = abs(parse_int(current.get("skip", "")) or 0)
    if candidate_skip != current_skip:
        return candidate_skip < current_skip
    return candidate.get("direction", "") < current.get("direction", "")


def parse_int(value: str) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def format_counter(counter: Counter[str], limit: int) -> str:
    return "; ".join(f"{key}={count}" for key, count in counter.most_common(limit) if key)


def reproduce_command(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_dynamic_span_exact_center_review_queue "
        f"--input {args.input} "
        f"--out {args.out} "
        f"--markdown-out {args.markdown_out}"
    )


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
