#!/usr/bin/env python3
"""Summarize relaxed surface-context all-code collections."""

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


DEFAULT_HITS = Path("reports/hebrew_theology_all_codes/surface_all_codes.csv")
DEFAULT_SUMMARY = Path("reports/hebrew_theology_all_codes/surface_all_codes_summary.csv")
DEFAULT_MD = Path("docs/HEBREW_THEOLOGY_ALL_CODES_COLLECTION.md")
DEFAULT_MANIFEST = Path("reports/hebrew_theology_all_codes/summary.manifest.json")


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    hit_rows = read_rows(args.hits)
    summary_rows = read_rows(args.summary)
    aggregates = aggregate(summary_rows, hit_rows)
    write_markdown(args.markdown_out, args, aggregates)
    write_manifest(args.manifest_out, args, aggregates, started)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hits", type=Path, default=DEFAULT_HITS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--title", default="Hebrew Theology All-Codes Collection")
    parser.add_argument(
        "--description",
        default=(
            "This report intentionally keeps every hidden-path ELS row from the "
            "surface-context collection and then flags same-word, related-center, "
            "center-verse, and span context. It is a collection index, not a "
            "claim-grade filter."
        ),
    )
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def aggregate(
    summary_rows: list[dict[str, str]],
    hit_rows: list[dict[str, str]],
) -> dict[str, Any]:
    by_term: dict[str, dict[str, Any]] = defaultdict(lambda: defaultdict(int))
    by_context = Counter()
    corpora = set()
    for row in summary_rows:
        key = row["term_id"]
        corpora.add(row.get("corpus", ""))
        bucket = by_term[key]
        bucket["term_id"] = key
        bucket["concept"] = row.get("concept", "")
        bucket["category"] = row.get("category", "")
        bucket["term"] = row.get("term", "")
        bucket["normalized_term"] = row.get("normalized_term", "")
        for field in (
            "hit_count",
            "context_hit_count",
            "exact_center_word_hits",
            "same_concept_center_word_hits",
            "same_category_center_word_hits",
            "exact_center_hits",
            "same_concept_center_hits",
            "same_category_center_hits",
            "exact_span_hits",
            "same_concept_span_hits",
            "same_category_span_hits",
        ):
            bucket[field] += int_or_zero(row.get(field, ""))
    for row in hit_rows:
        context = row.get("best_context", "") or "hidden_path_only"
        by_context[context] += 1
    term_rows = sorted(
        (dict(values) for values in by_term.values()),
        key=lambda row: (
            -int(row.get("hit_count", 0)),
            str(row.get("term_id", "")),
        ),
    )
    return {
        "corpora": sorted(label for label in corpora if label),
        "summary_rows": len(summary_rows),
        "hit_rows": len(hit_rows),
        "term_count": len(term_rows),
        "total_hits": sum(int(row.get("hit_count", 0)) for row in term_rows),
        "context_hits": sum(int(row.get("context_hit_count", 0)) for row in term_rows),
        "center_word_exact_hits": sum(
            int(row.get("exact_center_word_hits", 0)) for row in term_rows
        ),
        "center_word_related_hits": sum(
            int(row.get("same_concept_center_word_hits", 0))
            + int(row.get("same_category_center_word_hits", 0))
            for row in term_rows
        ),
        "center_verse_exact_hits": sum(int(row.get("exact_center_hits", 0)) for row in term_rows),
        "center_verse_related_hits": sum(
            int(row.get("same_concept_center_hits", 0))
            + int(row.get("same_category_center_hits", 0))
            for row in term_rows
        ),
        "span_context_hits": sum(
            int(row.get("exact_span_hits", 0))
            + int(row.get("same_concept_span_hits", 0))
            + int(row.get("same_category_span_hits", 0))
            for row in term_rows
        ),
        "context_counts": dict(by_context),
        "term_rows": term_rows,
    }


def write_markdown(path: Path, args: argparse.Namespace, aggregates: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {args.title}",
        "",
        args.description,
        "",
        "## Inputs",
        "",
        f"- Hits: `{args.hits}`",
        f"- Summary: `{args.summary}`",
        f"- Corpora: `{', '.join(aggregates['corpora'])}`",
        "",
        "## Collection Counts",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Terms represented | {aggregates['term_count']:,} |",
        f"| Corpus-term summary rows | {aggregates['summary_rows']:,} |",
        f"| Hidden-path rows retained | {aggregates['hit_rows']:,} |",
        f"| Total hits from summary | {aggregates['total_hits']:,} |",
        f"| Any surface-context hits | {aggregates['context_hits']:,} |",
        f"| Center word contains same term | {aggregates['center_word_exact_hits']:,} |",
        f"| Center word contains related term | {aggregates['center_word_related_hits']:,} |",
        f"| Center verse contains same term | {aggregates['center_verse_exact_hits']:,} |",
        f"| Center verse contains related term | {aggregates['center_verse_related_hits']:,} |",
        f"| Hit span contains same/related term | {aggregates['span_context_hits']:,} |",
        "",
        "## Context Labels",
        "",
        "| Best context | Rows |",
        "| --- | ---: |",
    ]
    for label, count in sorted(
        aggregates["context_counts"].items(),
        key=lambda item: (-item[1], item[0]),
    ):
        lines.append(f"| `{label}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Top Terms",
            "",
            "| Term | Concept | Hidden hits | Center word same | Center word related | Center verse same | Center verse related | Span context |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in aggregates["term_rows"][:30]:
        center_word_related = int(row.get("same_concept_center_word_hits", 0)) + int(
            row.get("same_category_center_word_hits", 0)
        )
        center_verse_related = int(row.get("same_concept_center_hits", 0)) + int(
            row.get("same_category_center_hits", 0)
        )
        span_context = (
            int(row.get("exact_span_hits", 0))
            + int(row.get("same_concept_span_hits", 0))
            + int(row.get("same_category_span_hits", 0))
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.get('term_id', '')}`",
                    str(row.get("concept", "")),
                    f"{int(row.get('hit_count', 0)):,}",
                    f"{int(row.get('exact_center_word_hits', 0)):,}",
                    f"{center_word_related:,}",
                    f"{int(row.get('exact_center_hits', 0)):,}",
                    f"{center_verse_related:,}",
                    f"{span_context:,}",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "This output is deliberately broad. Hidden-path-only rows are retained for",
            "inspection. Same-center-word rows are a narrower subset. Same-concept and",
            "same-category center-word rows are related-surface prompts, not automatic",
            "interpretations. Claim-grade filtering still belongs in the controlled",
            "reports.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    aggregates: dict[str, Any],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": "summarize_surface_all_codes",
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "git_commit": run_git("rev-parse", "--short", "HEAD"),
        "hits": str(args.hits),
        "summary": str(args.summary),
        "markdown_out": str(args.markdown_out),
        "aggregates": {
            key: value
            for key, value in aggregates.items()
            if key != "term_rows"
        },
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def int_or_zero(value: str | int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def run_git(*args: str) -> str:
    completed = subprocess.run(["git", *args], check=False, capture_output=True, text=True)
    return completed.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
