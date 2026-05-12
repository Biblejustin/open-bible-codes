#!/usr/bin/env python3
"""Summarize broad count term presence by corpus/version."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.term_display import display_term


COUNTS_DIR = Path("reports/broad_search")
SUMMARY_OUT = Path("reports/broad_search/broad_version_presence.csv")
MD_OUT = Path("reports/broad_search/broad_version_presence.md")
MANIFEST_OUT = Path("reports/broad_search/broad_version_presence.manifest.json")

FIELDNAMES = [
    "term_set",
    "term_id",
    "concept",
    "category",
    "term_language",
    "normalized_term",
    "normalized_length",
    "observed_corpora",
    "observed_corpus_count",
    "present_corpora",
    "absent_corpora",
    "presence_scope",
    "total_hits",
    "max_hit_count",
    "max_corpus",
    "hit_counts_by_corpus",
    "read",
]

FOCUS_CONCEPTS = {
    "Trump",
    "Donald Trump",
    "Vance",
    "Netanyahu",
    "Iran",
    "Russia",
    "Europe",
    "Germany",
    "Turkey",
    "United States",
    "United States Of America",
    "USA",
    "United Nations",
    "European Union",
    "Gog",
    "Magog",
    "Beast",
    "Dragon",
    "Cowboy",
    "Catering",
    "Cowboy Catering",
    "Simsberry",
    "Simscorner",
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_count_rows(args.counts_dir)
    if args.corpus:
        allowed = set(args.corpus)
        rows = [row for row in rows if row.get("corpus", "") in allowed]
    summary_rows = version_presence_rows(rows)
    write_rows(args.summary_out, summary_rows)
    write_markdown(args.markdown_out, summary_rows, args)
    write_manifest(args, len(rows), len(summary_rows), started)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts-dir", type=Path, default=COUNTS_DIR)
    parser.add_argument("--corpus", action="append", default=[])
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_count_rows(counts_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(counts_dir.glob("*_counts.csv")):
        if not is_term_set_counts_file(path):
            continue
        term_set = path.name.removesuffix("_counts.csv")
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                copied = dict(row)
                copied["term_set"] = term_set
                rows.append(copied)
    return rows


def is_term_set_counts_file(path: Path) -> bool:
    if path.name.startswith("broad_search_"):
        return False
    return (path.parent / f"{path.stem}.manifest.json").exists()


def version_presence_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row.get("term_set", ""), row.get("term_id", ""))].append(row)
    output = [presence_row(group) for group in groups.values()]
    return sorted(output, key=presence_sort_key)


def presence_row(group: list[dict[str, str]]) -> dict[str, object]:
    first = group[0]
    observed = sorted({row.get("corpus", "") for row in group if row.get("corpus", "")})
    hit_counts = {row.get("corpus", ""): hit_count(row) for row in group}
    present = [corpus for corpus in observed if hit_counts.get(corpus, 0) > 0]
    absent = [corpus for corpus in observed if hit_counts.get(corpus, 0) == 0]
    max_corpus = max(observed, key=lambda corpus: hit_counts.get(corpus, 0), default="")
    total_hits = sum(hit_counts.values())
    scope = presence_scope(present, absent)
    return {
        "term_set": first.get("term_set", ""),
        "term_id": first.get("term_id", ""),
        "concept": first.get("concept", ""),
        "category": first.get("category", ""),
        "term_language": first.get("term_language", ""),
        "normalized_term": first.get("normalized_term", ""),
        "normalized_length": int_or_zero(first.get("normalized_length")),
        "observed_corpora": ",".join(observed),
        "observed_corpus_count": len(observed),
        "present_corpora": ",".join(present),
        "absent_corpora": ",".join(absent),
        "presence_scope": scope,
        "total_hits": total_hits,
        "max_hit_count": hit_counts.get(max_corpus, 0),
        "max_corpus": max_corpus,
        "hit_counts_by_corpus": "; ".join(
            f"{corpus}:{hit_counts.get(corpus, 0)}" for corpus in observed
        ),
        "read": read_label(
            scope,
            total_hits,
            int_or_zero(first.get("normalized_length")),
            len(observed),
        ),
    }


def presence_scope(present: list[str], absent: list[str]) -> str:
    if not present:
        return "absent_all_observed_sources"
    if not absent:
        return "present_all_observed_sources"
    if len(present) > 1:
        return "present_multiple_sources"
    return "source_specific"


def read_label(scope: str, total_hits: int, length: int, observed_count: int) -> str:
    if scope == "absent_all_observed_sources":
        return "absent at this range"
    if length <= 3:
        return "high-noise short form"
    if length == 4 and total_hits >= 1000:
        return "dense short form"
    if scope == "source_specific":
        return "source-specific broad-count row"
    if scope == "present_multiple_sources":
        return "present in multiple observed corpora"
    if observed_count == 1:
        return "present in only compatible corpus"
    return "present in every compatible corpus"


def presence_sort_key(row: dict[str, object]) -> tuple[int, int, str, str]:
    scope_order = {
        "present_all_observed_sources": 0,
        "present_multiple_sources": 1,
        "source_specific": 2,
        "absent_all_observed_sources": 3,
    }
    return (
        scope_order.get(str(row["presence_scope"]), 9),
        -int(row["total_hits"]),
        str(row["term_set"]),
        str(row["term_id"]),
    )


def display_presence_term(row: dict[str, object]) -> str:
    term_id = str(row["term_id"])
    term = display_term(str(row["normalized_term"]), english=str(row.get("concept", "")) or None)
    return f"`{term_id}` {term}"


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    scope_counts = Counter(str(row["presence_scope"]) for row in rows)
    focus_rows = [
        row
        for row in rows
        if row.get("concept", "") in FOCUS_CONCEPTS
    ]
    lines = [
        "# Broad Version Presence",
        "",
        "This report groups broad ELS count rows by term and records which observed",
        "corpora contain at least one hit at the broad skip range.",
        "",
        "## Scope Counts",
        "",
        "| Scope | Terms |",
        "| --- | ---: |",
    ]
    for scope, count in sorted(scope_counts.items()):
        lines.append(f"| `{scope}` | {count} |")
    lines.extend(
        [
            "",
            "## Focus Terms",
            "",
            "| Set | Term | Observed | Present | Absent | Hits by corpus | Scope | Read |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in sorted(focus_rows, key=lambda item: int(item["total_hits"]), reverse=True)[:80]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["term_set"]),
                    display_presence_term(row),
                    str(row["observed_corpora"]),
                    str(row["present_corpora"]),
                    str(row["absent_corpora"]),
                    str(row["hit_counts_by_corpus"]),
                    f"`{row['presence_scope']}`",
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Caution",
            "",
            "This is raw count presence, not a control result. It is useful for seeing",
            "which source texts contain a term at least once under the broad ELS scan.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    input_rows: int,
    output_rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_broad_version_presence",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "counts_dir": str(args.counts_dir),
        "corpora_filter": list(args.corpus),
        "input_rows": input_rows,
        "output_rows": output_rows,
        "outputs": [
            str(args.summary_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
        "seconds": round(time.perf_counter() - started, 3),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def hit_count(row: dict[str, str]) -> int:
    return int_or_zero(row.get("hit_count"))


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


if __name__ == "__main__":
    raise SystemExit(main())
