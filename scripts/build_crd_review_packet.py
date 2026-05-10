#!/usr/bin/env python3
"""Build a readable Markdown packet from a compact CRD review queue."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


REASON_ORDER = {
    "top_finite_ratio": 0,
    "bible_positive_secular_zero": 1,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = read_dicts(args.queue)
    write_packet(
        rows=rows,
        output=args.output,
        title=args.title,
        examples_per_term=args.examples_per_term,
    )
    print(args.output)
    print(f"queue_rows={len(rows)}")
    print(f"terms={len({row.get('term_id', '') for row in rows})}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--title", default="CRD Review Packet")
    parser.add_argument("--examples-per-term", type=int, default=3)
    return parser


def write_packet(
    *,
    rows: list[dict[str, str]],
    output: Path,
    title: str,
    examples_per_term: int,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        f"# {title}",
        "",
        "Status: generated local review packet from ignored CRD queue output.",
        "",
        "## Summary",
        "",
    ]
    lines.extend(summary_lines(rows))
    lines.extend(["", "## Terms", ""])
    for term_id, term_rows in grouped_term_rows(rows):
        lines.extend(term_section(term_id, term_rows, examples_per_term=examples_per_term))
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def summary_lines(rows: list[dict[str, str]]) -> list[str]:
    languages = Counter(row.get("language", "") for row in rows)
    corpora = Counter(row.get("corpus", "") for row in rows)
    reasons = Counter(row.get("selection_reason", "") for row in rows)
    scopes = Counter(row.get("surface_match_scope", "") for row in rows)
    return [
        f"- queue rows: {len(rows):,}",
        f"- selected terms: {len({row.get('term_id', '') for row in rows}):,}",
        f"- languages: {format_counter(languages)}",
        f"- corpora: {format_counter(corpora)}",
        f"- selection reasons: {format_counter(reasons)}",
        f"- surface scopes: {format_counter(scopes)}",
    ]


def grouped_term_rows(rows: list[dict[str, str]]) -> list[tuple[str, list[dict[str, str]]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("term_id", "")].append(row)
    return sorted(grouped.items(), key=lambda item: term_sort_key(item[1][0]))


def term_sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    reason = row.get("selection_reason", "")
    rank = parse_int(row.get("selection_rank")) or 0
    return (REASON_ORDER.get(reason, 99), rank, row.get("term_id", ""))


def term_section(
    term_id: str,
    rows: list[dict[str, str]],
    *,
    examples_per_term: int,
) -> list[str]:
    first = rows[0]
    lines = [
        f"### `{term_id}`",
        "",
        f"- term: `{first.get('term', '')}`",
        f"- concept: {first.get('concept', '')}",
        f"- language: {first.get('language', '')}",
        f"- category: {first.get('category', '')}",
        f"- selection: {first.get('selection_reason', '')} rank {first.get('selection_rank', '')}",
        f"- Bible max: {first.get('bible_max_density', '')} in {first.get('bible_max_corpus', '')}",
        f"- secular max: {first.get('secular_max_density', '')} in {first.get('secular_max_corpus', '')}",
        f"- ratio: {first.get('ratio', '')}",
        "",
        "| Corpus | Center ref | Skip | Direction | Center word | Matched surface | Start-End |",
        "| --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for row in sorted(rows, key=example_sort_key)[:examples_per_term]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row.get("corpus", "")),
                    md_cell(row.get("center_ref", "")),
                    md_cell(row.get("skip", "")),
                    md_cell(row.get("direction", "")),
                    md_cell(row.get("center_word", "")),
                    md_cell(row.get("matched_surface_keyword", "")),
                    md_cell(f"{row.get('start_ref', '')} to {row.get('end_ref', '')}"),
                ]
            )
            + " |"
        )
    lines.extend(["", "Representative center verses:", ""])
    for row in sorted(rows, key=example_sort_key)[:examples_per_term]:
        lines.append(
            f"- `{row.get('corpus', '')}` `{row.get('center_ref', '')}`: "
            + compact_text(row.get("center_verse_text", ""))
        )
    lines.append("")
    return lines


def example_sort_key(row: dict[str, str]) -> tuple[str, str, int, str]:
    return (
        row.get("corpus", ""),
        row.get("center_ref", ""),
        abs(parse_int(row.get("skip")) or 0),
        row.get("hit_id", ""),
    )


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def format_counter(counter: Counter[str]) -> str:
    parts = [f"{key or 'blank'}={value:,}" for key, value in counter.most_common()]
    return ", ".join(parts)


def md_cell(value: str) -> str:
    return compact_text(value).replace("|", "\\|")


def compact_text(value: str, *, limit: int = 220) -> str:
    compacted = " ".join(value.split())
    if len(compacted) <= limit:
        return compacted
    return compacted[: limit - 3].rstrip() + "..."


if __name__ == "__main__":
    raise SystemExit(main())
