#!/usr/bin/env python3
"""Summarize forward/backward direction strata from the match-strata index."""

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


DEFAULT_STRATA = Path("reports/match_strata_index/occurrence_strata.csv")
DEFAULT_OUT = Path("reports/direction_asymmetry/summary.csv")
DEFAULT_TERM_OUT = Path("reports/direction_asymmetry/term_summary.csv")
DEFAULT_MARKDOWN_OUT = Path("docs/DIRECTION_ASYMMETRY.md")
DEFAULT_MANIFEST_OUT = Path("reports/direction_asymmetry/manifest.json")

FIELDNAMES = [
    "source_family",
    "corpus_class",
    "corpus",
    "bucket",
    "term_groups",
    "hit_rows",
    "distinct_terms",
    "forward_hits",
    "backward_hits",
    "share_of_term_groups",
]

TERM_FIELDNAMES = [
    "source_family",
    "corpus_class",
    "corpus",
    "term_id",
    "normalized_term",
    "bucket",
    "hit_rows",
    "forward_hits",
    "backward_hits",
    "direction_imbalance_score",
]

DIRECTION_BUCKETS = (
    "forward_only",
    "backward_only",
    "bidirectional_present",
    "no_direction_data",
)


@dataclass(frozen=True)
class TermDirectionGroup:
    source_family: str
    corpus_class: str
    corpus: str
    term_id: str
    normalized_term: str
    bucket: str
    hit_rows: int
    forward_hits: int
    backward_hits: int
    direction_imbalance_score: str


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    input_rows = read_rows(args.strata)
    term_groups = build_term_direction_groups(input_rows)
    summary_rows = summarize_direction_asymmetry(term_groups)
    write_rows(args.out, FIELDNAMES, summary_rows)
    write_rows(args.term_out, TERM_FIELDNAMES, [term_group_row(group) for group in term_groups])
    write_markdown(args.markdown_out, args, input_rows, term_groups, summary_rows)
    write_manifest(args.manifest_out, args, input_rows, term_groups, summary_rows, started)
    print(args.out)
    print(args.term_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strata", type=Path, default=DEFAULT_STRATA)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--term-out", type=Path, default=DEFAULT_TERM_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def build_term_direction_groups(rows: list[dict[str, str]]) -> list[TermDirectionGroup]:
    grouped: dict[tuple[str, str, str, str, str], list[dict[str, str]]] = {}
    for row in rows:
        key = (
            row.get("source_family", ""),
            row.get("corpus_class", ""),
            row.get("corpus", ""),
            row.get("term_id", ""),
            row.get("normalized_term", ""),
        )
        grouped.setdefault(key, []).append(row)

    output: list[TermDirectionGroup] = []
    for key, group_rows in sorted(grouped.items()):
        bucket = first_nonempty(row.get("direction_stratum", "") for row in group_rows) or "no_direction_data"
        if bucket not in DIRECTION_BUCKETS:
            bucket = "no_direction_data"
        forward_hits = max_int(row.get("forward_direction_count", "") for row in group_rows)
        backward_hits = max_int(row.get("backward_direction_count", "") for row in group_rows)
        imbalance = first_nonempty(row.get("direction_imbalance_score", "") for row in group_rows) or "0.000000"
        output.append(
            TermDirectionGroup(
                source_family=key[0],
                corpus_class=key[1],
                corpus=key[2],
                term_id=key[3],
                normalized_term=key[4],
                bucket=bucket,
                hit_rows=len(group_rows),
                forward_hits=forward_hits,
                backward_hits=backward_hits,
                direction_imbalance_score=imbalance,
            )
        )
    return output


def summarize_direction_asymmetry(groups: list[TermDirectionGroup]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str], list[TermDirectionGroup]] = {}
    for group in groups:
        key = (group.source_family, group.corpus_class, group.corpus)
        grouped.setdefault(key, []).append(group)

    output: list[dict[str, object]] = []
    for key, corpus_groups in sorted(grouped.items()):
        total = len(corpus_groups)
        for bucket in DIRECTION_BUCKETS:
            matching = [group for group in corpus_groups if group.bucket == bucket]
            output.append(
                {
                    "source_family": key[0],
                    "corpus_class": key[1],
                    "corpus": key[2],
                    "bucket": bucket,
                    "term_groups": len(matching),
                    "hit_rows": sum(group.hit_rows for group in matching),
                    "distinct_terms": len({group.term_id for group in matching if group.term_id}),
                    "forward_hits": sum(group.forward_hits for group in matching),
                    "backward_hits": sum(group.backward_hits for group in matching),
                    "share_of_term_groups": f"{len(matching) / total:.6f}" if total else "0.000000",
                }
            )
    return output


def first_nonempty(values: Any) -> str:
    for value in values:
        stripped = str(value).strip()
        if stripped:
            return stripped
    return ""


def max_int(values: Any) -> int:
    maximum = 0
    for value in values:
        try:
            maximum = max(maximum, int(str(value).strip()))
        except ValueError:
            continue
    return maximum


def term_group_row(group: TermDirectionGroup) -> dict[str, object]:
    return {
        "source_family": group.source_family,
        "corpus_class": group.corpus_class,
        "corpus": group.corpus,
        "term_id": group.term_id,
        "normalized_term": group.normalized_term,
        "bucket": group.bucket,
        "hit_rows": group.hit_rows,
        "forward_hits": group.forward_hits,
        "backward_hits": group.backward_hits,
        "direction_imbalance_score": group.direction_imbalance_score,
    }


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    args: argparse.Namespace,
    input_rows: list[dict[str, str]],
    term_groups: list[TermDirectionGroup],
    summary_rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bucket_totals = Counter(group.bucket for group in term_groups)
    lines = [
        "# Direction Asymmetry",
        "",
        "Status: post-search review aid, not claim promotion.",
        "",
        "This report summarizes whether a term/corpus group appears only in the",
        "forward direction, only in the backward direction, or in both directions.",
        "It depends on the already-built match-strata index and does not perform",
        "a new ELS search.",
        "",
        "## Settings",
        "",
        f"- Strata input: `{args.strata}`",
        f"- Input rows: `{len(input_rows)}`",
        f"- Term/corpus groups: `{len(term_groups)}`",
        "",
        "## Overall Direction Counts",
        "",
        "| Bucket | Term/corpus groups |",
        "| --- | ---: |",
    ]
    for bucket in DIRECTION_BUCKETS:
        lines.append(f"| `{bucket}` | {bucket_totals[bucket]:,} |")

    lines.extend(
        [
            "",
            "## Source / Corpus Summary",
            "",
            "| Source family | Corpus class | Corpus | Bucket | Term groups | Hit rows | Forward hits | Backward hits | Share |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary_rows[: args.markdown_row_limit]:
        lines.append(
            "| "
            f"`{row['source_family']}` | `{row['corpus_class']}` | `{row['corpus']}` | "
            f"`{row['bucket']}` | {row['term_groups']} | {row['hit_rows']} | "
            f"{row['forward_hits']} | {row['backward_hits']} | {row['share_of_term_groups']} |"
        )
    if len(summary_rows) > args.markdown_row_limit:
        lines.append(
            "| ... | ... | ... | ... | ... | ... | ... | ... | "
            f"{len(summary_rows) - args.markdown_row_limit:,} more rows in CSV |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Direction asymmetry is counted per term/corpus group, not per isolated hit.",
            "- `forward_only` and `backward_only` are review filters. They are not",
            "  findings without matched controls and a locked comparison rule.",
            "- The term-level CSV preserves hit-row counts and grouped forward/backward",
            "  totals for later filtering.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    input_rows: list[dict[str, str]],
    term_groups: list[TermDirectionGroup],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_direction_asymmetry.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "input_rows": len(input_rows),
        "term_groups": len(term_groups),
        "summary_rows": len(summary_rows),
        "inputs": {"strata": str(args.strata)},
        "outputs": {
            "out": str(args.out),
            "term_out": str(args.term_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
