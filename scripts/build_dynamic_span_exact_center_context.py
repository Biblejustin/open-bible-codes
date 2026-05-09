#!/usr/bin/env python3
"""Build readable excerpts for exact-center review queue rows."""

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
from els.corpus import Corpus, load_corpus
from scripts.export_dynamic_span_hits import DEFAULT_CORPORA


DEFAULT_QUEUE = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_review_queue.csv")
DEFAULT_OUT = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_context.csv")
DEFAULT_MARKDOWN = Path("docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_CONTEXT.md")
DEFAULT_MANIFEST = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_context.manifest.json")
DEFAULT_TEXT_LIMIT = 2000

FIELDNAMES = [
    "rank",
    "corpus_class",
    "corpus",
    "term_id",
    "normalized_term",
    "center_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "exact_center_paths",
    "review_bucket",
    "example_skip",
    "example_direction",
    "example_start_ref",
    "example_center_ref",
    "example_end_ref",
    "start_verse_text",
    "center_verse_text",
    "end_verse_text",
    "center_word_context",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    queue_rows = select_queue_rows(read_rows(args.queue), args)
    corpora = load_needed_corpora(queue_rows, corpus_config_map(args.corpus))
    context_rows = [
        context_row(row, corpora[row["corpus"]], text_limit=args.text_limit)
        for row in queue_rows
    ]
    write_csv(args.out, context_rows)
    write_markdown(args.markdown_out, context_rows, args)
    write_manifest(args.manifest_out, args, queue_rows, context_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--bible-limit", type=int, default=80)
    parser.add_argument("--control-limit", type=int, default=30)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    parser.add_argument("--text-limit", type=int, default=DEFAULT_TEXT_LIMIT)
    parser.add_argument("--corpus", action="append", default=[])
    return parser


def corpus_config_map(overrides: list[str]) -> dict[str, Path]:
    configs = {label: Path(path) for label, path in DEFAULT_CORPORA.items()}
    for value in overrides:
        if "=" not in value:
            raise ValueError(f"expected LABEL=CONFIG for --corpus, got {value!r}")
        label, config = value.split("=", 1)
        configs[label] = Path(config)
    return configs


def select_queue_rows(rows: list[dict[str, str]], args: argparse.Namespace) -> list[dict[str, str]]:
    bible = [row for row in rows if row.get("corpus_class") == "bible"][: args.bible_limit]
    controls = [row for row in rows if row.get("corpus_class") == "control"][: args.control_limit]
    return bible + controls


def load_needed_corpora(rows: list[dict[str, str]], configs: dict[str, Path]) -> dict[str, Corpus]:
    corpora = {}
    for label in sorted({row["corpus"] for row in rows}):
        if label not in configs:
            raise KeyError(f"no corpus config for {label}")
        corpora[label] = load_corpus(configs[label])
    return corpora


def context_row(
    row: dict[str, str],
    corpus: Corpus,
    *,
    text_limit: int = DEFAULT_TEXT_LIMIT,
) -> dict[str, str]:
    center_offset = require_int(row["example_center_offset"], "example_center_offset")
    start_offset = require_int(row["example_start_offset"], "example_start_offset")
    end_offset = require_int(row["example_end_offset"], "example_end_offset")
    center_verse = corpus.verses[corpus.position_to_verse[center_offset]]
    start_verse = corpus.verses[corpus.position_to_verse[start_offset]]
    end_verse = corpus.verses[corpus.position_to_verse[end_offset]]
    center_word = corpus.word_at(center_offset)
    return {
        "rank": row["rank"],
        "corpus_class": row["corpus_class"],
        "corpus": row["corpus"],
        "term_id": row["term_id"],
        "normalized_term": row["normalized_term"],
        "center_ref": row["center_ref"],
        "center_source": row["center_source"],
        "center_word_index": row["center_word_index"],
        "center_word": row["center_word"],
        "exact_center_paths": row["exact_center_paths"],
        "review_bucket": row["review_bucket"],
        "example_skip": row["example_skip"],
        "example_direction": row["example_direction"],
        "example_start_ref": row["example_start_ref"],
        "example_center_ref": center_verse.ref,
        "example_end_ref": row["example_end_ref"],
        "start_verse_text": clean_text(start_verse.raw_text, text_limit),
        "center_verse_text": clean_text(center_verse.raw_text, text_limit),
        "end_verse_text": clean_text(end_verse.raw_text, text_limit),
        "center_word_context": clean_text(
            word_context(corpus, center_word.ref, center_word.word_index) if center_word else "",
            text_limit,
        ),
    }


def word_context(corpus: Corpus, ref: str, word_index: int, *, radius: int = 5) -> str:
    words = [
        word
        for word in corpus.words
        if word.ref == ref and abs(word.word_index - word_index) <= radius
    ]
    return " ".join(mark_center(word.raw_word, word.word_index == word_index) for word in words)


def mark_center(raw_word: str, center: bool) -> str:
    return f"[{raw_word}]" if center else raw_word


def clean_text(value: str, limit: int) -> str:
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    counts = Counter(row["corpus"] for row in rows)
    lines = [
        "# Strong Full-Span Exact-Center Context",
        "",
        "This report adds readable center/start/end text to the exact-center review queue.",
        "It is an inspection aid, not a claim rule.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Scope",
        "",
        f"- queue input: `{args.queue}`",
        f"- excerpt rows: {len(rows):,}",
        f"- rows by corpus: `{dict(sorted(counts.items()))}`",
        f"- context CSV: `{args.out}`",
        "",
        "## Top Context Rows",
        "",
        "| Rank | Corpus | Term | Center | Paths | Word context | Center verse excerpt |",
        "| ---: | --- | --- | --- | ---: | --- | --- |",
    ]
    for row in rows[: args.markdown_row_limit]:
        lines.append(
            f"| {row['rank']} | {row['corpus']} | `{row['term_id']}` | {row['center_ref']} | "
            f"{int(row['exact_center_paths']):,} | {md_cell(row['center_word_context'])} | "
            f"{md_cell(truncate(row['center_verse_text'], 180))} |"
        )
    if len(rows) > args.markdown_row_limit:
        lines.append(f"| ... | ... | ... | ... | ... | ... | {len(rows) - args.markdown_row_limit:,} more rows in CSV |")
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Bracketed word in `Word context` is the centered surface word.",
            "- `start_verse_text` and `end_verse_text` in the CSV show the example hidden path endpoints.",
            "- Large skip spans can cross large textual ranges; center context is usually the most readable first pass.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    queue_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_dynamic_span_exact_center_context.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "queue": str(args.queue),
        "out": str(args.out),
        "markdown_out": str(args.markdown_out),
        "queue_rows_selected": len(queue_rows),
        "context_rows": len(context_rows),
        "git_commit": git_commit(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def require_int(value: str, field: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an integer, got {value!r}") from exc


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def truncate(value: str, limit: int) -> str:
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def reproduce_command(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_dynamic_span_exact_center_context "
        f"--queue {args.queue} "
        f"--out {args.out} "
        f"--markdown-out {args.markdown_out} "
        f"--manifest-out {args.manifest_out} "
        f"--bible-limit {args.bible_limit} "
        f"--control-limit {args.control_limit} "
        f"--markdown-row-limit {args.markdown_row_limit} "
        f"--text-limit {args.text_limit}"
    )


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
