#!/usr/bin/env python3
"""Build an original-language shortlist from the exact-center review bundle."""

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
from els.term_display import display_center, display_term


DEFAULT_BUNDLE = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_review_bundle.csv")
DEFAULT_OUT = Path(
    "reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_shortlist.csv"
)
DEFAULT_MARKDOWN = Path("docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ORIGINAL_LANGUAGE_SHORTLIST.md")
DEFAULT_MANIFEST = Path(
    "reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_shortlist.manifest.json"
)

ORIGINAL_LANGUAGE_CORPORA = {
    "MT_WLC",
    "UXLC",
    "EBIBLE_WLC",
    "MAM",
    "UHB",
    "LXX",
    "TR_NT",
    "BYZ_NT",
    "TCG_NT",
    "SBLGNT",
}

FIELDNAMES = [
    "shortlist_rank",
    "priority",
    "corpus",
    "term_id",
    "normalized_term",
    "center_ref",
    "center_word",
    "exact_center_paths",
    "min_abs_skip",
    "max_abs_skip",
    "strong_extension_rows",
    "best_extension",
    "best_extension_type",
    "best_extension_match_kind",
    "best_extension_examples",
    "matrix_paths",
    "matrix_min_rows_spanned",
    "matrix_max_rows_spanned",
    "center_word_context",
    "center_verse_excerpt",
    "source_rank",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    bundle_rows = read_rows(args.bundle)
    shortlist = build_shortlist(bundle_rows, limit=args.limit)
    write_csv(args.out, shortlist)
    write_markdown(args.markdown_out, shortlist, args)
    write_manifest(args.manifest_out, args, bundle_rows, shortlist, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--limit", type=int, default=120)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def build_shortlist(rows: list[dict[str, str]], *, limit: int) -> list[dict[str, object]]:
    selected = [
        row
        for row in rows
        if row.get("corpus_class") == "bible" and row.get("corpus") in ORIGINAL_LANGUAGE_CORPORA
    ]
    ranked = sorted(selected, key=shortlist_sort_key)
    if limit > 0:
        ranked = ranked[:limit]
    return [shortlist_row(index, row) for index, row in enumerate(ranked, start=1)]


def shortlist_sort_key(row: dict[str, str]) -> tuple[int, int, int, int, int]:
    return (
        priority_order(row.get("priority", "")),
        -int_value(row.get("strong_extension_rows", "")),
        -int_value(row.get("exact_center_paths", "")),
        int_value(row.get("min_abs_skip", "")),
        int_value(row.get("rank", "")),
    )


def priority_order(value: str) -> int:
    if value == "bible_exact_center_with_strong_extension":
        return 0
    if value == "bible_exact_center":
        return 1
    return 2


def shortlist_row(index: int, row: dict[str, str]) -> dict[str, object]:
    return {
        "shortlist_rank": index,
        "priority": row.get("priority", ""),
        "corpus": row.get("corpus", ""),
        "term_id": row.get("term_id", ""),
        "normalized_term": row.get("normalized_term", ""),
        "center_ref": row.get("center_ref", ""),
        "center_word": row.get("center_word", ""),
        "exact_center_paths": int_value(row.get("exact_center_paths", "")),
        "min_abs_skip": int_value(row.get("min_abs_skip", "")),
        "max_abs_skip": int_value(row.get("max_abs_skip", "")),
        "strong_extension_rows": int_value(row.get("strong_extension_rows", "")),
        "best_extension": row.get("best_extension", ""),
        "best_extension_type": row.get("best_extension_type", ""),
        "best_extension_match_kind": row.get("best_extension_match_kind", ""),
        "best_extension_examples": row.get("best_extension_examples", ""),
        "matrix_paths": int_value(row.get("matrix_paths", "")),
        "matrix_min_rows_spanned": int_value(row.get("matrix_min_rows_spanned", "")),
        "matrix_max_rows_spanned": int_value(row.get("matrix_max_rows_spanned", "")),
        "center_word_context": row.get("center_word_context", ""),
        "center_verse_excerpt": row.get("center_verse_excerpt", ""),
        "source_rank": row.get("rank", ""),
    }


def int_value(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]], args: argparse.Namespace) -> None:
    lines = [
        "# Strong Full-Span Exact-Center Original-Language Shortlist",
        "",
        "This report filters the full exact-center review bundle to Hebrew and Greek Bible corpora.",
        "KJV rows and non-Bible controls stay in the comparison bundle, but are not primary",
        "original-language review rows here.",
        "",
        "## Reproduce",
        "",
        "```bash",
        command_line(args),
        "```",
        "",
        "## Scope",
        "",
        f"- original-language shortlist rows: {len(rows):,}",
        f"- source bundle: `{args.bundle}`",
        f"- shortlist CSV: `{args.out}`",
        "",
    ]
    lines.extend(summary_lines(rows))
    lines.extend(top_rows_lines(rows[: args.markdown_row_limit]))
    lines.extend(read_lines())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summary_lines(rows: list[dict[str, object]]) -> list[str]:
    by_corpus = Counter(str(row["corpus"]) for row in rows)
    by_term = Counter(str(row["normalized_term"]) for row in rows)
    lines = ["## Corpus Counts", "", "| Corpus | Rows |", "| --- | ---: |"]
    for corpus, count in sorted(by_corpus.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {corpus} | {count:,} |")
    lines.extend(["", "## Term Counts", "", "| Term | Rows |", "| --- | ---: |"])
    for term, count in sorted(by_term.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {display_term(term)} | {count:,} |")
    lines.append("")
    return lines


def top_rows_lines(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "## Top Shortlist Rows",
        "",
        "| Rank | Priority | Corpus | Term | Center | Paths | Strong ext rows | Best extension | Matrix paths | Context |",
        "| ---: | --- | --- | --- | --- | ---: | ---: | --- | ---: | --- |",
    ]
    for row in rows:
        term = display_term(str(row["normalized_term"]))
        center = display_center(str(row["center_ref"]), str(row["center_word"]))
        lines.append(
            f"| {row['shortlist_rank']} | {row['priority']} | {row['corpus']} | "
            f"{term} | {center} | {row['exact_center_paths']} | "
            f"{row['strong_extension_rows']} | {row['best_extension']} | {row['matrix_paths']} | "
            f"{row['center_word_context']} |"
        )
    lines.append("")
    return lines


def read_lines() -> list[str]:
    return [
        "## Read",
        "",
        "- This is a review queue, not a claim list.",
        "- Rows are original-language Bible rows only; English KJV rows and controls remain in the parent bundle.",
        "- High exact-center path count can still reflect ordinary surface vocabulary.",
        "- Manual review should compare the center passage, matrix path, extension flag, and language-matched controls.",
        "",
    ]


def command_line(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_dynamic_span_exact_center_original_language_shortlist "
        f"--bundle {args.bundle} --out {args.out} --markdown-out {args.markdown_out} "
        f"--manifest-out {args.manifest_out} --limit {args.limit} "
        f"--markdown-row-limit {args.markdown_row_limit}"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    bundle_rows: list[dict[str, str]],
    shortlist: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_dynamic_span_exact_center_original_language_shortlist",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "git_commit": git_commit(),
        "bundle": str(args.bundle),
        "rows_in_bundle": len(bundle_rows),
        "shortlist_rows": len(shortlist),
        "original_language_corpora": sorted(ORIGINAL_LANGUAGE_CORPORA),
        "out": str(args.out),
        "markdown_out": str(args.markdown_out),
        "manifest_out": str(args.manifest_out),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
