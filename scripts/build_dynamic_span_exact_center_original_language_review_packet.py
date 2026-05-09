#!/usr/bin/env python3
"""Build a manual-review packet for original-language exact-center rows."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_BUNDLE = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_review_bundle.csv")
DEFAULT_EXACT_ROWS = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_rows.csv")
DEFAULT_CONTEXT = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_context.csv")
DEFAULT_MATRIX_DIR = Path("reports/dynamic_skip_focus/exact_center_matrix")
DEFAULT_EXACT_SUMMARY = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_rows_summary.csv")
DEFAULT_REVIEW_OUT = Path(
    "reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_review_packet.csv"
)
DEFAULT_PATHS_OUT = Path(
    "reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_review_paths.csv"
)
DEFAULT_MARKDOWN = Path(
    "docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ORIGINAL_LANGUAGE_REVIEW_PACKET.md"
)
DEFAULT_MANIFEST = Path(
    "reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_review_packet.manifest.json"
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

REVIEW_FIELDNAMES = [
    "review_rank",
    "priority",
    "corpus",
    "term_id",
    "normalized_term",
    "center_ref",
    "center_word_index",
    "center_word",
    "exact_center_paths",
    "path_rows_joined",
    "min_abs_skip",
    "max_abs_skip",
    "min_rows_spanned",
    "max_rows_spanned",
    "strong_extension_rows",
    "best_extension",
    "best_extension_type",
    "best_extension_match_kind",
    "best_extension_examples",
    "example_skip",
    "example_direction",
    "example_start_ref",
    "example_end_ref",
    "example_row_width",
    "example_rows_spanned",
    "example_letter_path",
    "center_word_context",
    "center_verse_excerpt",
    "control_comparison",
    "control_read",
]

PATH_FIELDNAMES = [
    "review_rank",
    "path_rank",
    "corpus",
    "term_id",
    "normalized_term",
    "skip",
    "direction",
    "span_letters",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_word_index",
    "center_word",
    "start_offset",
    "center_offset",
    "end_offset",
    "row_width",
    "rows_spanned",
    "cols_spanned",
    "matrix_min_row",
    "matrix_max_row",
    "matrix_min_col",
    "matrix_max_col",
    "letter_path",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    bundle_rows = read_rows(args.bundle)
    exact_rows = read_rows(args.exact_rows)
    context_rows = read_rows(args.context)
    matrix_rows = read_many(sorted(args.matrix_dir.glob("matrix_*_summary.csv")))
    letter_rows = read_many(sorted(args.matrix_dir.glob("matrix_*_letters.csv")))
    exact_summary_rows = read_rows(args.exact_summary)

    review_rows, path_rows = build_packet(
        bundle_rows,
        exact_rows,
        context_rows,
        matrix_rows,
        letter_rows,
        exact_summary_rows,
        limit=args.limit,
    )
    write_csv(args.review_out, REVIEW_FIELDNAMES, review_rows)
    write_csv(args.paths_out, PATH_FIELDNAMES, path_rows)
    write_markdown(args.markdown_out, review_rows, path_rows, exact_summary_rows, args)
    write_manifest(args.manifest_out, args, review_rows, path_rows, started)
    print(args.review_out)
    print(args.paths_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--exact-rows", type=Path, default=DEFAULT_EXACT_ROWS)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT)
    parser.add_argument("--matrix-dir", type=Path, default=DEFAULT_MATRIX_DIR)
    parser.add_argument("--exact-summary", type=Path, default=DEFAULT_EXACT_SUMMARY)
    parser.add_argument("--review-out", type=Path, default=DEFAULT_REVIEW_OUT)
    parser.add_argument("--paths-out", type=Path, default=DEFAULT_PATHS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    parser.add_argument("--markdown-path-limit", type=int, default=120)
    return parser


def build_packet(
    bundle_rows: list[dict[str, str]],
    exact_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
    matrix_rows: list[dict[str, str]],
    letter_rows: list[dict[str, str]],
    exact_summary_rows: list[dict[str, str]],
    *,
    limit: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    selected = [
        row
        for row in bundle_rows
        if row.get("corpus_class") == "bible" and row.get("corpus") in ORIGINAL_LANGUAGE_CORPORA
    ]
    selected = sorted(selected, key=review_sort_key)
    if limit > 0:
        selected = selected[:limit]

    exact_by_key = group_by_review_key(exact_rows)
    context_by_key = {review_key(row): row for row in context_rows}
    matrix_by_path = {path_key(row): row for row in matrix_rows}
    letters_by_path = group_letters(letter_rows)
    controls_by_term = control_summary_by_term(exact_summary_rows)

    review_rows: list[dict[str, object]] = []
    path_rows: list[dict[str, object]] = []
    for review_rank, row in enumerate(selected, start=1):
        key = review_key(row)
        paths = sorted(exact_by_key.get(key, []), key=path_sort_key)
        context = context_by_key.get(key, {})
        control_comparison, control_read = control_text(row, controls_by_term)
        review_path_rows = [
            path_detail_row(review_rank, path_rank, path, matrix_by_path, letters_by_path)
            for path_rank, path in enumerate(paths, start=1)
        ]
        path_rows.extend(review_path_rows)
        example = review_path_rows[0] if review_path_rows else {}
        review_rows.append(
            {
                "review_rank": review_rank,
                "priority": row.get("priority", ""),
                "corpus": row.get("corpus", ""),
                "term_id": row.get("term_id", ""),
                "normalized_term": row.get("normalized_term", ""),
                "center_ref": row.get("center_ref", ""),
                "center_word_index": row.get("center_word_index", ""),
                "center_word": row.get("center_word", ""),
                "exact_center_paths": int_value(row.get("exact_center_paths", "")),
                "path_rows_joined": len(paths),
                "min_abs_skip": int_value(row.get("min_abs_skip", "")),
                "max_abs_skip": int_value(row.get("max_abs_skip", "")),
                "min_rows_spanned": min_numeric(review_path_rows, "rows_spanned"),
                "max_rows_spanned": max_numeric(review_path_rows, "rows_spanned"),
                "strong_extension_rows": int_value(row.get("strong_extension_rows", "")),
                "best_extension": row.get("best_extension", ""),
                "best_extension_type": row.get("best_extension_type", ""),
                "best_extension_match_kind": row.get("best_extension_match_kind", ""),
                "best_extension_examples": row.get("best_extension_examples", ""),
                "example_skip": example.get("skip", context.get("example_skip", "")),
                "example_direction": example.get("direction", context.get("example_direction", "")),
                "example_start_ref": example.get("start_ref", context.get("example_start_ref", "")),
                "example_end_ref": example.get("end_ref", context.get("example_end_ref", "")),
                "example_row_width": example.get("row_width", ""),
                "example_rows_spanned": example.get("rows_spanned", ""),
                "example_letter_path": example.get("letter_path", ""),
                "center_word_context": row.get("center_word_context") or context.get("center_word_context", ""),
                "center_verse_excerpt": row.get("center_verse_excerpt") or truncate(context.get("center_verse_text", ""), 220),
                "control_comparison": control_comparison,
                "control_read": control_read,
            }
        )
    return review_rows, path_rows


def review_sort_key(row: dict[str, str]) -> tuple[int, int, int, int]:
    return (
        priority_order(row.get("priority", "")),
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


def review_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("corpus", ""),
        row.get("normalized_term", ""),
        row.get("center_ref", ""),
        row.get("center_word_index", ""),
    )


def path_key(row: dict[str, str]) -> tuple[str, str, str, str, str, str, str]:
    return (
        row.get("corpus", ""),
        row.get("normalized_term", ""),
        row.get("skip", ""),
        row.get("direction", ""),
        row.get("start_ref", ""),
        row.get("center_ref", ""),
        row.get("end_ref", ""),
    )


def group_by_review_key(rows: list[dict[str, str]]) -> dict[tuple[str, str, str, str], list[dict[str, str]]]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("corpus") in ORIGINAL_LANGUAGE_CORPORA:
            grouped[review_key(row)].append(row)
    return grouped


def group_letters(rows: list[dict[str, str]]) -> dict[tuple[str, str, str, str, str, str, str], list[dict[str, str]]]:
    grouped: dict[tuple[str, str, str, str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("corpus") in ORIGINAL_LANGUAGE_CORPORA:
            grouped[path_key(row)].append(row)
    return grouped


def path_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    return (
        abs(int_value(row.get("skip", ""))),
        min(int_value(row.get("start_offset", "")), int_value(row.get("end_offset", ""))),
        max(int_value(row.get("start_offset", "")), int_value(row.get("end_offset", ""))),
    )


def path_detail_row(
    review_rank: int,
    path_rank: int,
    path: dict[str, str],
    matrix_by_path: dict[tuple[str, str, str, str, str, str, str], dict[str, str]],
    letters_by_path: dict[tuple[str, str, str, str, str, str, str], list[dict[str, str]]],
) -> dict[str, object]:
    key = path_key(path)
    matrix = matrix_by_path.get(key, {})
    letters = sorted(letters_by_path.get(key, []), key=lambda row: int_value(row.get("letter_index", "")))
    return {
        "review_rank": review_rank,
        "path_rank": path_rank,
        "corpus": path.get("corpus", ""),
        "term_id": path.get("term_id", ""),
        "normalized_term": path.get("normalized_term", ""),
        "skip": int_value(path.get("skip", "")),
        "direction": path.get("direction", ""),
        "span_letters": int_value(path.get("span_letters", "")),
        "start_ref": path.get("start_ref", ""),
        "center_ref": path.get("center_ref", ""),
        "end_ref": path.get("end_ref", ""),
        "center_word_index": path.get("center_word_index", ""),
        "center_word": path.get("center_word", ""),
        "start_offset": int_value(path.get("start_offset", "")),
        "center_offset": int_value(path.get("center_offset", "")),
        "end_offset": int_value(path.get("end_offset", "")),
        "row_width": int_value(matrix.get("row_width", "")),
        "rows_spanned": int_value(matrix.get("rows_spanned", "")),
        "cols_spanned": int_value(matrix.get("cols_spanned", "")),
        "matrix_min_row": int_value(matrix.get("min_row", "")),
        "matrix_max_row": int_value(matrix.get("max_row", "")),
        "matrix_min_col": int_value(matrix.get("min_col", "")),
        "matrix_max_col": int_value(matrix.get("max_col", "")),
        "letter_path": format_letter_path(letters),
    }


def control_summary_by_term(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    controls = {"HEB_PBY_BIALIK", "GRC_PERSEUS_HERODOTUS", "ENG_PG_SHAKESPEARE"}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("corpus") in controls:
            grouped[row.get("normalized_term", "")].append(row)
    return grouped


def control_text(
    row: dict[str, str],
    controls_by_term: dict[str, list[dict[str, str]]],
) -> tuple[str, str]:
    term = row.get("normalized_term", "")
    controls = sorted(controls_by_term.get(term, []), key=lambda item: item.get("corpus", ""))
    if not controls:
        return "", "no language-matched control summary found"
    parts = []
    has_nonzero = False
    for control in controls:
        exact_rows = int_value(control.get("exact_center_rows", ""))
        has_nonzero = has_nonzero or exact_rows > 0
        per_million = control.get("exact_center_rows_per_million_hits", "")
        parts.append(f"{control.get('corpus')}:{exact_rows} exact-center rows ({per_million}/M)")
    if has_nonzero:
        read = "language-matched controls also produce exact-center rows; treat as background-rate warning"
    else:
        read = "available language-matched control summary has zero exact-center rows for this normalized term"
    return "; ".join(parts), read


def format_letter_path(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    parts = []
    for row in rows:
        parts.append(
            f"{row.get('letter')}@{row.get('ref')}:{row.get('word')}[r{row.get('row')},c{row.get('col')}]"
        )
    return " | ".join(parts)


def min_numeric(rows: list[dict[str, object]], field: str) -> int:
    values = [int(row[field]) for row in rows if int(row.get(field) or 0) > 0]
    return min(values, default=0)


def max_numeric(rows: list[dict[str, object]], field: str) -> int:
    values = [int(row[field]) for row in rows if int(row.get(field) or 0) > 0]
    return max(values, default=0)


def int_value(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_many(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        rows.extend(read_rows(path))
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    review_rows: list[dict[str, object]],
    path_rows: list[dict[str, object]],
    exact_summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Strong Full-Span Exact-Center Original-Language Review Packet",
        "",
        "This packet is a human-review entry point for original-language Bible rows",
        "from the full-span exact-center run. It keeps English KJV rows and",
        "non-Bible controls out of the primary table, but still reports matched",
        "control summaries where available.",
        "",
        "## Reproduce",
        "",
        "```bash",
        command_line(args),
        "```",
        "",
        "## Scope",
        "",
        f"- review units: {len(review_rows):,}",
        f"- path rows joined: {len(path_rows):,}",
        f"- review CSV: `{args.review_out}`",
        f"- path CSV: `{args.paths_out}`",
        "",
    ]
    lines.extend(summary_lines(review_rows, path_rows))
    lines.extend(control_summary_lines(exact_summary_rows))
    lines.extend(review_table_lines(review_rows[: args.markdown_row_limit]))
    lines.extend(path_table_lines(path_rows[: args.markdown_path_limit]))
    lines.extend(read_lines())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summary_lines(review_rows: list[dict[str, object]], path_rows: list[dict[str, object]]) -> list[str]:
    by_corpus = Counter(str(row["corpus"]) for row in review_rows)
    path_by_corpus = Counter(str(row["corpus"]) for row in path_rows)
    by_term = Counter(str(row["normalized_term"]) for row in review_rows)
    lines = ["## Corpus Counts", "", "| Corpus | Review units | Path rows |", "| --- | ---: | ---: |"]
    for corpus, count in sorted(by_corpus.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {corpus} | {count:,} | {path_by_corpus[corpus]:,} |")
    lines.extend(["", "## Term Counts", "", "| Term | Review units |", "| --- | ---: |"])
    for term, count in sorted(by_term.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{term}` | {count:,} |")
    lines.append("")
    return lines


def control_summary_lines(rows: list[dict[str, str]]) -> list[str]:
    controls = [
        row
        for row in rows
        if row.get("corpus") in {"HEB_PBY_BIALIK", "GRC_PERSEUS_HERODOTUS", "ENG_PG_SHAKESPEARE"}
    ]
    controls = sorted(controls, key=lambda row: (row.get("normalized_term", ""), row.get("corpus", "")))
    lines = [
        "## Available Control Summaries",
        "",
        "| Control corpus | Term | Exact-center rows | Rows per million hits | Top center words |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in controls:
        lines.append(
            f"| {row.get('corpus')} | `{row.get('normalized_term')}` | "
            f"{int_value(row.get('exact_center_rows')):,} | "
            f"{row.get('exact_center_rows_per_million_hits')} | "
            f"{md_cell(truncate(row.get('top_center_words', ''), 90))} |"
        )
    lines.append("")
    return lines


def review_table_lines(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "## Review Units",
        "",
        "| Rank | Corpus | Term | Center | Paths | Example span | Matrix | Control read | Context |",
        "| ---: | --- | --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        span = f"{row['example_start_ref']} -> {row['center_ref']} -> {row['example_end_ref']}"
        matrix = f"{row['example_rows_spanned']} rows @ width {row['example_row_width']}"
        lines.append(
            f"| {row['review_rank']} | {row['corpus']} | `{row['normalized_term']}` | "
            f"{row['center_ref']} `{row['center_word']}` | {int(row['exact_center_paths']):,} | "
            f"{md_cell(span)} | {md_cell(matrix)} | {md_cell(row['control_read'])} | "
            f"{md_cell(truncate(str(row['center_word_context']), 100))} |"
        )
    lines.append("")
    return lines


def path_table_lines(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "## Path Detail Sample",
        "",
        "| Review | Path | Corpus | Term | Skip | Span | Matrix | Letters |",
        "| ---: | ---: | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in rows:
        span = f"{row['start_ref']} -> {row['center_ref']} -> {row['end_ref']}"
        matrix = f"rows {row['matrix_min_row']}-{row['matrix_max_row']}, col {row['matrix_min_col']}"
        lines.append(
            f"| {row['review_rank']} | {row['path_rank']} | {row['corpus']} | "
            f"`{row['normalized_term']}` | {row['skip']} | {md_cell(span)} | "
            f"{md_cell(matrix)} | {md_cell(truncate(str(row['letter_path']), 140))} |"
        )
    lines.append("")
    return lines


def read_lines() -> list[str]:
    return [
        "## Read",
        "",
        "- This is a manual-review packet, not a claim report.",
        "- Exact-center means the hidden path centers on a matching surface word.",
        "- Hebrew controls show substantial background exact-center pressure for `ישוע` and `משיח` in the Bialik control corpus.",
        "- Greek Herodotus controls currently show zero exact-center rows for `ιησουσ` and `γωγ`, but that does not by itself create a claim.",
        "- A promoted row still needs source/version comparison, surface-frequency checks, controls, and manual passage reading.",
        "",
    ]


def command_line(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_dynamic_span_exact_center_original_language_review_packet "
        f"--bundle {args.bundle} --exact-rows {args.exact_rows} --context {args.context} "
        f"--matrix-dir {args.matrix_dir} --exact-summary {args.exact_summary} "
        f"--review-out {args.review_out} --paths-out {args.paths_out} "
        f"--markdown-out {args.markdown_out} --manifest-out {args.manifest_out}"
    )


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def truncate(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 3)] + "..."


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    review_rows: list[dict[str, object]],
    path_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_dynamic_span_exact_center_original_language_review_packet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "git_commit": git_commit(),
        "review_rows": len(review_rows),
        "path_rows": len(path_rows),
        "inputs": {
            "bundle": str(args.bundle),
            "exact_rows": str(args.exact_rows),
            "context": str(args.context),
            "matrix_dir": str(args.matrix_dir),
            "exact_summary": str(args.exact_summary),
        },
        "outputs": {
            "review_out": str(args.review_out),
            "paths_out": str(args.paths_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
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
