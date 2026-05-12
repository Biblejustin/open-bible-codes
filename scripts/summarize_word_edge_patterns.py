#!/usr/bin/env python3
"""Summarize consecutive-word acrostic and telestic search outputs."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.term_display import display_term


SUMMARY_FIELDS = [
    "pattern_type",
    "corpus_label",
    "corpus",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "hits",
    "forward_hits",
    "backward_hits",
    "center_refs_sample",
]


@dataclass(frozen=True)
class SummaryKey:
    pattern_type: str
    corpus_label: str
    corpus: str
    term_id: str
    concept: str
    category: str
    normalized_term: str


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_hit_rows(args.hits)
    summary_rows = summarize_rows(rows)
    write_rows(args.summary_out, summary_rows)
    write_markdown(args.markdown_out, summary_rows, rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, started)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hits", action="append", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, default=Path("reports/word_edge_patterns/summary.csv"))
    parser.add_argument("--markdown-out", type=Path, default=Path("docs/WORD_EDGE_PATTERN_AUDIT.md"))
    parser.add_argument("--manifest-out", type=Path, default=Path("reports/word_edge_patterns/summary.manifest.json"))
    parser.add_argument("--title", default="Word-Edge Pattern Audit")
    parser.add_argument("--description", default="Opt-in consecutive-word acrostic and telestic pattern audit.")
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def read_hit_rows(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            rows.extend(dict(row) for row in csv.DictReader(handle))
    return rows


def summarize_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[SummaryKey, list[dict[str, str]]] = {}
    for row in rows:
        key = SummaryKey(
            pattern_type=row.get("pattern_type", ""),
            corpus_label=row.get("corpus_label", ""),
            corpus=row.get("corpus", ""),
            term_id=row.get("term_id", ""),
            concept=row.get("concept", ""),
            category=row.get("category", ""),
            normalized_term=row.get("normalized_term", ""),
        )
        groups.setdefault(key, []).append(row)

    output = []
    for key, group_rows in groups.items():
        directions = Counter(row.get("direction", "") for row in group_rows)
        refs = sorted({row.get("center_ref", "") for row in group_rows if row.get("center_ref", "")})
        output.append(
            {
                "pattern_type": key.pattern_type,
                "corpus_label": key.corpus_label,
                "corpus": key.corpus,
                "term_id": key.term_id,
                "concept": key.concept,
                "category": key.category,
                "normalized_term": key.normalized_term,
                "hits": len(group_rows),
                "forward_hits": directions["forward"],
                "backward_hits": directions["backward"],
                "center_refs_sample": ";".join(refs[:10]),
            }
        )
    return sorted(
        output,
        key=lambda row: (
            str(row["pattern_type"]),
            str(row["corpus_label"] or row["corpus"]),
            -int(row["hits"]),
            str(row["term_id"]),
        ),
    )


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    hit_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    corpus_count = len({row.get("corpus_label", "") or row.get("corpus", "") for row in hit_rows})
    term_count = len({row.get("term_id", "") for row in hit_rows if row.get("term_id", "")})
    lines = [
        f"# {args.title}",
        "",
        args.description,
        "",
        "This is not an ordinary ELS path search. Each pattern consumes one",
        "letter from each consecutive surface word, using either first letters",
        "(acrostic) or last letters (telestic). It widens the review surface and",
        "needs matched controls before claim language.",
        "",
        "## Bottom Line",
        "",
        f"- hit rows: {len(hit_rows):,}",
        f"- summarized rows: {len(summary_rows):,}",
        f"- corpora with hits: {corpus_count:,}",
        f"- terms with hits: {term_count:,}",
        "",
        "## Summary Rows",
        "",
        "| Pattern | Corpus | Term | Hits | F/B | Center refs sample |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for row in summary_rows[: args.markdown_row_limit]:
        lines.append(markdown_row(row))
    if len(summary_rows) > args.markdown_row_limit:
        lines.append(f"| ... | ... | ... | ... | ... | {len(summary_rows) - args.markdown_row_limit:,} more rows in CSV |")
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Acrostic means first letters of consecutive normalized words.",
            "- Telestic means last letters of consecutive normalized words.",
            "- Backward means the consecutive word-edge sequence reads the target term in reverse.",
            "- Capped rows mean `hits` may be a floor when the search step used `--max-hits-per-term`.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    corpus = row.get("corpus_label", "") or row.get("corpus", "")
    direction_counts = f"{row.get('forward_hits', 0)}/{row.get('backward_hits', 0)}"
    return (
        f"| `{row.get('pattern_type', '')}` | `{corpus}` | {term} | "
        f"{int(row.get('hits', 0)):,} | {direction_counts} | "
        f"{md_cell(row.get('center_refs_sample', ''))} |"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    hit_rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/summarize_word_edge_patterns.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "hit_rows": len(hit_rows),
        "summary_rows": len(summary_rows),
        "inputs": {"hits": [str(path) for path in args.hits]},
        "outputs": {
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
