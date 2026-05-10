#!/usr/bin/env python3
"""Build a compact manual-review bundle for exact-center rows."""

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
from els.term_display import display_term


DEFAULT_QUEUE = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_review_queue.csv")
DEFAULT_CONTEXT = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_context.csv")
DEFAULT_MATRIX_DIR = Path("reports/dynamic_skip_focus/exact_center_matrix")
DEFAULT_BIBLE_EXT_DIR = Path("reports/dynamic_skip_focus/exact_center_extensions")
DEFAULT_CONTROL_EXT_DIR = Path("reports/dynamic_skip_focus/exact_center_control_extensions")
DEFAULT_OUT = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_review_bundle.csv")
DEFAULT_MARKDOWN = Path("docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_REVIEW_BUNDLE.md")
DEFAULT_MANIFEST = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_review_bundle.manifest.json")

FIELDNAMES = [
    "rank",
    "priority",
    "corpus_class",
    "corpus",
    "term_id",
    "normalized_term",
    "center_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "exact_center_paths",
    "min_abs_skip",
    "max_abs_skip",
    "review_bucket",
    "strong_extension_rows",
    "best_extension_score",
    "best_extension",
    "best_extension_type",
    "best_extension_match_kind",
    "best_extension_match_count",
    "best_extension_examples",
    "matrix_paths",
    "matrix_min_rows_spanned",
    "matrix_max_rows_spanned",
    "center_word_context",
    "center_verse_excerpt",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    queue_rows = read_rows(args.queue)
    context_rows = read_rows(args.context)
    extension_rows = read_extension_rows([args.bible_extension_dir, args.control_extension_dir])
    matrix_rows = read_many(sorted(args.matrix_dir.glob("matrix_*_summary.csv")))
    bundle_rows = build_bundle(queue_rows, context_rows, extension_rows, matrix_rows)
    write_csv(args.out, bundle_rows)
    write_markdown(args.markdown_out, bundle_rows, args)
    write_manifest(args.manifest_out, args, bundle_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT)
    parser.add_argument("--matrix-dir", type=Path, default=DEFAULT_MATRIX_DIR)
    parser.add_argument("--bible-extension-dir", type=Path, default=DEFAULT_BIBLE_EXT_DIR)
    parser.add_argument("--control-extension-dir", type=Path, default=DEFAULT_CONTROL_EXT_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def build_bundle(
    queue_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
    extension_rows: list[dict[str, str]],
    matrix_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    context_by_key = {review_key(row): row for row in context_rows}
    extensions_by_key = aggregate_extensions(extension_rows)
    matrix_by_key = aggregate_matrix(matrix_rows)
    bundle_rows = []
    for row in queue_rows:
        exact_key = review_key(row)
        matrix_key = path_key(row)
        extension = extensions_by_key.get(exact_key, empty_extension())
        matrix = matrix_by_key.get(matrix_key, empty_matrix())
        context = context_by_key.get(exact_key, {})
        bundle_rows.append(
            {
                "rank": row["rank"],
                "priority": priority(row, extension),
                "corpus_class": row["corpus_class"],
                "corpus": row["corpus"],
                "term_id": row["term_id"],
                "normalized_term": row["normalized_term"],
                "center_ref": row["center_ref"],
                "center_source": row["center_source"],
                "center_word_index": row["center_word_index"],
                "center_word": row["center_word"],
                "exact_center_paths": row["exact_center_paths"],
                "min_abs_skip": row["min_abs_skip"],
                "max_abs_skip": row["max_abs_skip"],
                "review_bucket": row["review_bucket"],
                "strong_extension_rows": extension["rows"],
                "best_extension_score": extension["score"],
                "best_extension": extension["extended_sequence"],
                "best_extension_type": extension["extension_type"],
                "best_extension_match_kind": extension["match_kind"],
                "best_extension_match_count": extension["match_count"],
                "best_extension_examples": extension["matched_examples"],
                "matrix_paths": int(row["exact_center_paths"]),
                "matrix_min_rows_spanned": matrix["min_rows_spanned"],
                "matrix_max_rows_spanned": matrix["max_rows_spanned"],
                "center_word_context": context.get("center_word_context", ""),
                "center_verse_excerpt": truncate(context.get("center_verse_text", ""), 220),
            }
        )
    return sorted(bundle_rows, key=bundle_sort_key)


def aggregate_extensions(rows: list[dict[str, str]]) -> dict[tuple[str, str, str, str], dict[str, object]]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[review_key(row)].append(row)
    return {key: extension_summary(value) for key, value in grouped.items()}


def extension_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    best = max(rows, key=lambda row: int(row.get("extension_score") or 0))
    return {
        "rows": len(rows),
        "score": int(best.get("extension_score") or 0),
        "extended_sequence": best.get("extended_sequence", ""),
        "extension_type": best.get("extension_type", ""),
        "match_kind": best.get("match_kind", ""),
        "match_count": int(best.get("match_count") or 0),
        "matched_examples": best.get("matched_examples", ""),
    }


def empty_extension() -> dict[str, object]:
    return {
        "rows": 0,
        "score": 0,
        "extended_sequence": "",
        "extension_type": "",
        "match_kind": "",
        "match_count": 0,
        "matched_examples": "",
    }


def aggregate_matrix(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, object]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[path_key(row)].append(row)
    return {key: matrix_summary(value) for key, value in grouped.items()}


def matrix_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    rows_spanned = [int(row.get("rows_spanned") or 0) for row in rows]
    return {
        "paths": len(rows),
        "min_rows_spanned": min(rows_spanned, default=0),
        "max_rows_spanned": max(rows_spanned, default=0),
    }


def empty_matrix() -> dict[str, object]:
    return {"paths": 0, "min_rows_spanned": 0, "max_rows_spanned": 0}


def priority(row: dict[str, str], extension: dict[str, object]) -> str:
    has_strong_extension = int(extension["rows"]) > 0
    if row.get("corpus_class") == "bible" and has_strong_extension:
        return "bible_exact_center_with_strong_extension"
    if row.get("corpus_class") == "bible":
        return "bible_exact_center"
    if has_strong_extension:
        return "control_exact_center_with_strong_extension"
    return "control_exact_center"


def bundle_sort_key(row: dict[str, object]) -> tuple[int, int, int]:
    priority_order = {
        "bible_exact_center_with_strong_extension": 0,
        "control_exact_center_with_strong_extension": 1,
        "bible_exact_center": 2,
        "control_exact_center": 3,
    }
    return (
        priority_order[str(row["priority"])],
        -int(row["exact_center_paths"]),
        int(row["rank"]),
    )


def review_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("corpus", ""),
        row.get("normalized_term", ""),
        row.get("center_ref", ""),
        row.get("center_word_index", ""),
    )


def path_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("corpus", ""),
        row.get("normalized_term", ""),
        row.get("center_ref", ""),
    )


def read_extension_rows(directories: list[Path]) -> list[dict[str, str]]:
    paths = []
    for directory in directories:
        paths.extend(sorted(directory.glob("top_*.csv")))
    return read_many(paths)


def read_many(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        if path.exists():
            rows.extend(read_rows(path))
    return rows


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]], args: argparse.Namespace) -> None:
    lines = [
        "# Strong Full-Span Exact-Center Review Bundle",
        "",
        "This report joins exact-center queue rows with readable context, strong",
        "same-skip extension flags, and matrix path counts. The CSV is the working",
        "manual-review bundle.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Scope",
        "",
        f"- bundle rows: {len(rows):,}",
        f"- rows with strong extension flag: {sum(1 for row in rows if int(row['strong_extension_rows']) > 0):,}",
        f"- bundle CSV: `{args.out}`",
        "",
        "## Top Bundle Rows",
        "",
        "| Rank | Priority | Corpus | Term | Center | Paths | Strong ext rows | Best extension | Matrix paths | Context |",
        "| ---: | --- | --- | --- | --- | ---: | ---: | --- | ---: | --- |",
    ]
    for row in rows[: args.markdown_row_limit]:
        lines.append(bundle_markdown_row(row))
    if len(rows) > args.markdown_row_limit:
        lines.append(f"| ... | ... | ... | ... | ... | ... | ... | ... | ... | {len(rows) - args.markdown_row_limit:,} more rows in CSV |")
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Priority is a queueing label, not a claim label.",
            "- Strong extension flags come from the capped top-extension CSVs.",
            "- Matrix path count equals the exact-center path count for the review unit; use the matrix CSVs for exact path geometry.",
            "- Control rows remain in the bundle because they are the comparison baseline.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def bundle_markdown_row(row: dict[str, object]) -> str:
    return (
        f"| {row['rank']} | {row['priority']} | {row['corpus']} | {display_term(str(row['normalized_term']))} | "
        f"{row['center_ref']} | {int(row['exact_center_paths']):,} | "
        f"{int(row['strong_extension_rows']):,} | {md_cell(display_term(str(row['best_extension'])))} | "
        f"{int(row['matrix_paths']):,} | {md_cell(truncate(str(row['center_word_context']), 100))} |"
    )


def write_manifest(path: Path, args: argparse.Namespace, rows: list[dict[str, object]], started: float) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_dynamic_span_exact_center_review_bundle.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "queue": str(args.queue),
        "context": str(args.context),
        "matrix_dir": str(args.matrix_dir),
        "bible_extension_dir": str(args.bible_extension_dir),
        "control_extension_dir": str(args.control_extension_dir),
        "out": str(args.out),
        "markdown_out": str(args.markdown_out),
        "rows": len(rows),
        "strong_extension_rows": sum(1 for row in rows if int(row["strong_extension_rows"]) > 0),
        "git_commit": git_commit(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reproduce_command(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_dynamic_span_exact_center_review_bundle "
        f"--queue {args.queue} "
        f"--context {args.context} "
        f"--matrix-dir {args.matrix_dir} "
        f"--bible-extension-dir {args.bible_extension_dir} "
        f"--control-extension-dir {args.control_extension_dir} "
        f"--out {args.out} "
        f"--markdown-out {args.markdown_out} "
        f"--manifest-out {args.manifest_out} "
        f"--markdown-row-limit {args.markdown_row_limit}"
    )


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def truncate(value: str, limit: int) -> str:
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
