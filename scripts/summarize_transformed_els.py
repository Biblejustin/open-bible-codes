#!/usr/bin/env python3
"""Summarize opt-in transformed-corpus ELS search outputs."""

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
    "transform",
    "corpus_label",
    "base_corpus",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "hits",
    "forward_hits",
    "backward_hits",
    "min_abs_skip",
    "max_abs_skip",
    "capped_at_step_limit",
    "center_refs_sample",
]


@dataclass(frozen=True)
class SummaryKey:
    transform: str
    corpus_label: str
    base_corpus: str
    term_id: str
    concept: str
    category: str
    normalized_term: str


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_hit_rows(args.hits)
    summary_rows = summarize_rows(rows, cap_threshold=args.cap_threshold)
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
    parser.add_argument("--summary-out", type=Path, default=Path("reports/transformed_els/summary.csv"))
    parser.add_argument("--markdown-out", type=Path, default=Path("docs/TRANSFORMED_ELS_AUDIT.md"))
    parser.add_argument("--manifest-out", type=Path, default=Path("reports/transformed_els/summary.manifest.json"))
    parser.add_argument("--title", default="Transformed ELS Audit")
    parser.add_argument("--description", default="Opt-in ELS search over deterministic transformed corpus text.")
    parser.add_argument("--cap-threshold", type=int, default=0)
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


def summarize_rows(rows: list[dict[str, str]], *, cap_threshold: int = 0) -> list[dict[str, object]]:
    groups: dict[SummaryKey, list[dict[str, str]]] = {}
    for row in rows:
        key = SummaryKey(
            transform=row.get("transform", ""),
            corpus_label=row.get("corpus_label", ""),
            base_corpus=row.get("base_corpus", ""),
            term_id=row.get("term_id", ""),
            concept=row.get("concept", ""),
            category=row.get("category", ""),
            normalized_term=row.get("normalized_term", ""),
        )
        groups.setdefault(key, []).append(row)

    output = []
    for key, group_rows in groups.items():
        directions = Counter(row.get("direction", "") for row in group_rows)
        skips = sorted(abs_int(row.get("skip", "")) for row in group_rows if abs_int(row.get("skip", "")) is not None)
        refs = sorted({row.get("center_ref", "") for row in group_rows if row.get("center_ref", "")})
        output.append(
            {
                "transform": key.transform,
                "corpus_label": key.corpus_label,
                "base_corpus": key.base_corpus,
                "term_id": key.term_id,
                "concept": key.concept,
                "category": key.category,
                "normalized_term": key.normalized_term,
                "hits": len(group_rows),
                "forward_hits": directions["forward"],
                "backward_hits": directions["backward"],
                "min_abs_skip": "" if not skips else min(skips),
                "max_abs_skip": "" if not skips else max(skips),
                "capped_at_step_limit": "yes" if cap_threshold > 0 and len(group_rows) >= cap_threshold else "no",
                "center_refs_sample": ";".join(refs[:10]),
            }
        )
    return sorted(
        output,
        key=lambda row: (
            str(row["transform"]),
            str(row["corpus_label"] or row["base_corpus"]),
            -int(row["hits"]),
            str(row["term_id"]),
        ),
    )


def abs_int(value: str) -> int | None:
    try:
        return abs(int(value))
    except (TypeError, ValueError):
        return None


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
    corpus_count = len({row.get("base_corpus", "") for row in hit_rows if row.get("base_corpus", "")})
    term_count = len({row.get("term_id", "") for row in hit_rows if row.get("term_id", "")})
    lines = [
        f"# {args.title}",
        "",
        args.description,
        "",
        "This is an opt-in transformed-text audit. It widens the search surface",
        "and does not promote any row to claim status without separately locked",
        "language-matched controls.",
        "",
        "## Bottom Line",
        "",
        f"- hit rows: {len(hit_rows):,}",
        f"- summarized term/corpus rows: {len(summary_rows):,}",
        f"- corpora with hits: {corpus_count:,}",
        f"- terms with hits: {term_count:,}",
        "",
        "## Summary Rows",
        "",
        "| Transform | Corpus | Term | Hits | Capped | F/B | Skip range | Center refs sample |",
        "| --- | --- | --- | ---: | --- | ---: | --- | --- |",
    ]
    for row in summary_rows[: args.markdown_row_limit]:
        lines.append(markdown_row(row))
    if len(summary_rows) > args.markdown_row_limit:
        lines.append(f"| ... | ... | ... | ... | ... | ... | ... | {len(summary_rows) - args.markdown_row_limit:,} more rows in CSV |")
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Transform hits are found after deterministic text substitution, then mapped back to original corpus references.",
            "- The same transform must be applied to non-Bible controls before any comparative claim.",
            "- `Capped=yes` means `hits` may be a floor because the search step reached its per-term limit.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    skip_range = f"{row.get('min_abs_skip', '')}-{row.get('max_abs_skip', '')}"
    direction_counts = f"{row.get('forward_hits', 0)}/{row.get('backward_hits', 0)}"
    corpus = row.get("corpus_label", "") or row.get("base_corpus", "")
    return (
        f"| `{row.get('transform', '')}` | `{corpus}` | {term} | "
        f"{int(row.get('hits', 0)):,} | `{row.get('capped_at_step_limit', '')}` | "
        f"{direction_counts} | {skip_range} | "
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
        "script": "scripts/summarize_transformed_els.py",
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
