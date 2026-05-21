#!/usr/bin/env python3
"""Select deterministic pilot rows from a representative-control target table."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


FIELDNAMES = [
    "concept",
    "corpus",
    "term_set",
    "term_id",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "normalized_length",
    "hit_count",
    "status",
]

HIT_BANDS = (
    (10_000, "10000+"),
    (1_000, "1000..9999"),
    (100, "100..999"),
    (10, "10..99"),
    (1, "1..9"),
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_rows(args.targets)
    selected = select_pilot_rows(
        rows,
        per_corpus=args.per_corpus,
        top_per_corpus=args.top_per_corpus,
        min_hit_count=args.min_hit_count,
    )
    write_rows(args.out, selected)
    write_markdown(args.markdown_out, rows, selected, args)
    write_manifest(args, rows, selected, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, required=True)
    parser.add_argument("--per-corpus", type=int, default=100)
    parser.add_argument("--top-per-corpus", type=int, default=20)
    parser.add_argument("--min-hit-count", type=int, default=1)
    parser.add_argument("--title", default="Control Target Pilot Selection")
    return parser


def select_pilot_rows(
    rows: list[dict[str, str]],
    *,
    per_corpus: int,
    top_per_corpus: int,
    min_hit_count: int = 1,
) -> list[dict[str, str]]:
    eligible = [row for row in rows if int_or_zero(row.get("hit_count")) >= min_hit_count]
    selected: list[dict[str, str]] = []
    for corpus in sorted({row.get("corpus", "") for row in eligible}):
        corpus_rows = [row for row in eligible if row.get("corpus", "") == corpus]
        selected.extend(
            select_corpus_rows(
                corpus_rows,
                per_corpus=per_corpus,
                top_per_corpus=top_per_corpus,
            )
        )
    return sorted(selected, key=output_sort_key)


def select_corpus_rows(
    rows: list[dict[str, str]],
    *,
    per_corpus: int,
    top_per_corpus: int,
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    selected_keys: set[tuple[str, str, str]] = set()

    def add(row: dict[str, str]) -> None:
        key = row_key(row)
        if len(selected) >= per_corpus or key in selected_keys:
            return
        selected.append(row)
        selected_keys.add(key)

    for row in sorted(rows, key=priority_sort_key)[: min(top_per_corpus, per_corpus)]:
        add(row)

    buckets: dict[tuple[int, int, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row_key(row) in selected_keys:
            continue
        buckets[bucket_key(row)].append(row)
    for bucket_rows in buckets.values():
        bucket_rows.sort(key=priority_sort_key)

    keys = sorted(buckets)
    while len(selected) < per_corpus and keys:
        next_keys = []
        for key in keys:
            bucket_rows = buckets[key]
            if bucket_rows:
                add(bucket_rows.pop(0))
            if bucket_rows:
                next_keys.append(key)
        if next_keys == keys:
            continue
        keys = next_keys
    return selected


def bucket_key(row: dict[str, str]) -> tuple[int, int, str]:
    length = int_or_zero(row.get("normalized_length"))
    hit_count = int_or_zero(row.get("hit_count"))
    return (min(length, 9), hit_band_order(hit_count), row.get("category", ""))


def hit_band_order(hit_count: int) -> int:
    for index, (threshold, _label) in enumerate(HIT_BANDS):
        if hit_count >= threshold:
            return index
    return len(HIT_BANDS)


def hit_band_label(hit_count: int) -> str:
    for threshold, label in HIT_BANDS:
        if hit_count >= threshold:
            return label
    return "0"


def priority_sort_key(row: dict[str, str]) -> tuple[int, int, str, str]:
    return (
        -int_or_zero(row.get("hit_count")),
        int_or_zero(row.get("normalized_length")),
        row.get("term_id", ""),
        row.get("corpus", ""),
    )


def output_sort_key(row: dict[str, str]) -> tuple[str, int, int, str]:
    return (
        row.get("corpus", ""),
        -int_or_zero(row.get("hit_count")),
        int_or_zero(row.get("normalized_length")),
        row.get("term_id", ""),
    )


def row_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (row.get("corpus", ""), row.get("term_set", ""), row.get("term_id", ""))


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    selected: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    lines = [
        f"# {args.title}",
        "",
        "Status: deterministic pilot target list.",
        "",
        "This pilot samples the large representative-control target table before any",
        "full-run interpretation. It is a runtime and calibration step, not a",
        "replacement for full registered controls.",
        "",
        "## Selection Rule",
        "",
        f"- source rows: {len(rows):,}",
        f"- selected rows: {len(selected):,}",
        f"- rows per corpus: {args.per_corpus:,}",
        f"- top-density rows per corpus forced in: {args.top_per_corpus:,}",
        "- remaining rows selected by round-robin buckets of normalized length, hit band, and category.",
        "",
        "## Counts",
        "",
        "| Group | Total | Selected |",
        "| --- | ---: | ---: |",
    ]
    for corpus in sorted({row.get("corpus", "") for row in rows}):
        lines.append(
            f"| `{corpus}` | {count_matching(rows, corpus=corpus):,} | "
            f"{count_matching(selected, corpus=corpus):,} |"
        )
    lines.extend(["", "## Selected Lengths", "", "| Length | Rows |", "| --- | ---: |"])
    for length, count in sorted(Counter(row.get("normalized_length", "") for row in selected).items()):
        lines.append(f"| `{length}` | {count:,} |")
    lines.extend(["", "## Selected Hit Bands", "", "| Hit band | Rows |", "| --- | ---: |"])
    for band, count in sorted(
        Counter(hit_band_label(int_or_zero(row.get("hit_count"))) for row in selected).items()
    ):
        lines.append(f"| `{band}` | {count:,} |")
    lines.extend(["", "## Top Selected Rows", ""])
    lines.extend(
        [
            "| Corpus | Term ID | Concept | Length | Hits |",
            "| --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in sorted(selected, key=priority_sort_key)[:40]:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.get("corpus", ""),
                    f"`{row.get('term_id', '')}`",
                    md_cell(row.get("concept", "")),
                    row.get("normalized_length", ""),
                    row.get("hit_count", ""),
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    selected: list[dict[str, str]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "tool": "select_control_target_pilot",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "targets": str(args.targets),
        "out": str(args.out),
        "markdown_out": str(args.markdown_out),
        "per_corpus": args.per_corpus,
        "top_per_corpus": args.top_per_corpus,
        "min_hit_count": args.min_hit_count,
        "source_rows": len(rows),
        "selected_rows": len(selected),
        "selected_by_corpus": dict(Counter(row.get("corpus", "") for row in selected)),
        "seconds": round(time.perf_counter() - started, 3),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def count_matching(rows: list[dict[str, str]], *, corpus: str) -> int:
    return sum(1 for row in rows if row.get("corpus", "") == corpus)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


if __name__ == "__main__":
    raise SystemExit(main())
