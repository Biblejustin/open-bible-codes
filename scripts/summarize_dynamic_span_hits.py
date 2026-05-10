#!/usr/bin/env python3
"""Summarize exported dynamic full-span ELS hits without filtering them away."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from els import __version__
from els.report_db import ReportDBStale, connect, quote_identifier, verify_table_current
from els.term_display import contains_greek, contains_hebrew, display_term
from scripts.export_dynamic_span_hits import DEFAULT_COUNTS, DEFAULT_OUT, ROOT


DEFAULT_COMPARISON = ROOT / "reports/dynamic_skip_focus/bible_control_comparison.csv"
DEFAULT_HITS_TABLE = "dynamic_skip_focus_full_span_exported_hits"
DEFAULT_SUMMARY_CSV = ROOT / "reports/dynamic_skip_focus/full_span_hit_summary.csv"
DEFAULT_EXAMPLES_CSV = ROOT / "reports/dynamic_skip_focus/full_span_hit_examples.csv"
DEFAULT_VERSION_CSV = ROOT / "reports/dynamic_skip_focus/full_span_version_presence.csv"
DEFAULT_REPORT = ROOT / "docs/DYNAMIC_SKIP_FULL_SPAN_HIT_FINDINGS.md"
DEFAULT_MANIFEST = ROOT / "reports/dynamic_skip_focus/full_span_hit_findings.manifest.json"

CONTROL_PREFIXES = ("HEB_PBY_", "GRC_PERSEUS_", "ENG_PG_")

SUMMARY_FIELDNAMES = [
    "corpus",
    "corpus_language",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "mode",
    "count_row_hit_count",
    "exported_hits",
    "forward_hits",
    "backward_hits",
    "exact_center_word_hits",
    "min_abs_skip",
    "max_abs_skip",
    "min_span_letters",
    "max_span_letters",
    "distinct_center_refs",
    "distinct_center_words",
    "top_center_refs",
    "top_center_words",
]

EXAMPLE_FIELDNAMES = [
    "example_type",
    "corpus",
    "term_id",
    "concept",
    "term",
    "normalized_term",
    "count_row_hit_count",
    "skip",
    "direction",
    "span_letters",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_word",
    "center_normalized_word",
]

VERSION_FIELDNAMES = [
    "term_id",
    "concept",
    "term_language",
    "term",
    "normalized_term",
    "mode",
    "bible_present_corpora",
    "control_present_corpora",
    "bible_zero_corpora",
    "control_zero_corpora",
    "bible_max_corpus",
    "bible_max_hit_count",
    "control_max_corpus",
    "control_max_hit_count",
]


@dataclass
class HitAccumulator:
    corpus: str
    corpus_language: str
    term_id: str
    concept: str
    category: str
    term_language: str
    term: str
    normalized_term: str
    mode: str
    count_row_hit_count: int
    exported_hits: int = 0
    forward_hits: int = 0
    backward_hits: int = 0
    exact_center_word_hits: int = 0
    min_abs_skip: int | None = None
    max_abs_skip: int | None = None
    min_span_letters: int | None = None
    max_span_letters: int | None = None
    center_refs: Counter[str] = field(default_factory=Counter)
    center_words: Counter[str] = field(default_factory=Counter)
    examples: list[dict[str, str]] = field(default_factory=list)
    exact_examples: list[dict[str, str]] = field(default_factory=list)

    def add(self, row: dict[str, str], *, example_limit: int) -> None:
        self.exported_hits += 1
        if row.get("direction") == "forward":
            self.forward_hits += 1
        elif row.get("direction") == "backward":
            self.backward_hits += 1

        abs_skip = abs(int(row["skip"]))
        span_letters = int(row["span_letters"])
        self.min_abs_skip = abs_skip if self.min_abs_skip is None else min(self.min_abs_skip, abs_skip)
        self.max_abs_skip = abs_skip if self.max_abs_skip is None else max(self.max_abs_skip, abs_skip)
        self.min_span_letters = (
            span_letters if self.min_span_letters is None else min(self.min_span_letters, span_letters)
        )
        self.max_span_letters = (
            span_letters if self.max_span_letters is None else max(self.max_span_letters, span_letters)
        )
        self.center_refs[row.get("center_ref", "")] += 1
        center_word = row.get("center_normalized_word") or row.get("center_word", "")
        if center_word:
            self.center_words[center_word] += 1

        if row.get("center_normalized_word") == self.normalized_term:
            self.exact_center_word_hits += 1
            if len(self.exact_examples) < example_limit:
                self.exact_examples.append(row)

        candidate = compact_example(row, "low_count")
        if len(self.examples) < example_limit:
            self.examples.append(candidate)
            self.examples.sort(key=example_sort_key)
        elif example_sort_key(candidate) < example_sort_key(self.examples[-1]):
            self.examples[-1] = candidate
            self.examples.sort(key=example_sort_key)

    def as_row(self) -> dict[str, str | int]:
        return {
            "corpus": self.corpus,
            "corpus_language": self.corpus_language,
            "term_id": self.term_id,
            "concept": self.concept,
            "category": self.category,
            "term_language": self.term_language,
            "term": self.term,
            "normalized_term": self.normalized_term,
            "mode": self.mode,
            "count_row_hit_count": self.count_row_hit_count,
            "exported_hits": self.exported_hits,
            "forward_hits": self.forward_hits,
            "backward_hits": self.backward_hits,
            "exact_center_word_hits": self.exact_center_word_hits,
            "min_abs_skip": self.min_abs_skip or 0,
            "max_abs_skip": self.max_abs_skip or 0,
            "min_span_letters": self.min_span_letters or 0,
            "max_span_letters": self.max_span_letters or 0,
            "distinct_center_refs": len(self.center_refs),
            "distinct_center_words": len(self.center_words),
            "top_center_refs": format_counter(self.center_refs, 5),
            "top_center_words": format_counter(self.center_words, 5),
        }


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.db:
        hit_summary, examples = summarize_hit_table(
            db_path=args.db,
            table_name=args.hits_table,
            source_path=args.hits,
            low_count_threshold=args.low_count_threshold,
            examples_per_group=args.examples_per_group,
        )
    else:
        hit_summary, examples = summarize_hit_file(
            args.hits,
            low_count_threshold=args.low_count_threshold,
            examples_per_group=args.examples_per_group,
        )
    count_rows = read_many(args.counts or DEFAULT_COUNTS)
    version_rows = build_version_presence_rows(count_rows, mode="full-span")
    comparison_rows = read_rows(args.comparison) if args.comparison.exists() else []

    write_csv(args.summary_csv, SUMMARY_FIELDNAMES, hit_summary)
    write_csv(args.examples_csv, EXAMPLE_FIELDNAMES, examples)
    write_csv(args.version_csv, VERSION_FIELDNAMES, version_rows)
    write_report(args.report, hit_summary, examples, version_rows, comparison_rows, args)
    write_manifest(args.manifest, args, hit_summary, examples, version_rows, started)

    print(args.summary_csv)
    print(args.examples_csv)
    print(args.version_csv)
    print(args.report)
    print(args.manifest)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hits", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--counts", type=Path, action="append", default=[])
    parser.add_argument("--comparison", type=Path, default=DEFAULT_COMPARISON)
    parser.add_argument("--summary-csv", type=Path, default=DEFAULT_SUMMARY_CSV)
    parser.add_argument("--examples-csv", type=Path, default=DEFAULT_EXAMPLES_CSV)
    parser.add_argument("--version-csv", type=Path, default=DEFAULT_VERSION_CSV)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--low-count-threshold", type=int, default=100)
    parser.add_argument("--examples-per-group", type=int, default=5)
    parser.add_argument("--db", type=Path, default=None, help="DuckDB report database with imported hit table.")
    parser.add_argument("--hits-table", default=DEFAULT_HITS_TABLE, help="DuckDB table for --hits.")
    return parser


def summarize_hit_file(
    path: Path,
    *,
    low_count_threshold: int,
    examples_per_group: int,
) -> tuple[list[dict[str, str | int]], list[dict[str, str]]]:
    accumulators: dict[tuple[str, str, str], HitAccumulator] = {}
    low_count_examples: list[dict[str, str]] = []
    exact_center_examples: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row["corpus"], row["term_id"], row["mode"])
            if key not in accumulators:
                accumulators[key] = HitAccumulator(
                    corpus=row["corpus"],
                    corpus_language=row["corpus_language"],
                    term_id=row["term_id"],
                    concept=row["concept"],
                    category=row["category"],
                    term_language=row["term_language"],
                    term=row["term"],
                    normalized_term=row["normalized_term"],
                    mode=row["mode"],
                    count_row_hit_count=int(row["count_row_hit_count"]),
                )
            acc = accumulators[key]
            acc.add(row, example_limit=examples_per_group)
    for acc in sorted(accumulators.values(), key=lambda item: (item.count_row_hit_count, item.corpus, item.term_id)):
        if acc.count_row_hit_count <= low_count_threshold:
            low_count_examples.extend(acc.examples)
        for row in acc.exact_examples:
            exact_center_examples.append(compact_example(row, "exact_center_word"))
    summary_rows = [acc.as_row() for acc in sorted(accumulators.values(), key=lambda item: (item.corpus, item.term_id))]
    examples = exact_center_examples + low_count_examples
    examples.sort(key=lambda row: (row["example_type"], int(row["count_row_hit_count"] or 0), row["corpus"], row["term_id"]))
    return summary_rows, examples


def summarize_hit_table(
    *,
    db_path: Path,
    table_name: str,
    source_path: Path,
    low_count_threshold: int,
    examples_per_group: int,
) -> tuple[list[dict[str, str | int]], list[dict[str, str]]]:
    try:
        verify_table_current(db_path=db_path, table_name=table_name, source_path=source_path)
    except ReportDBStale as exc:
        raise SystemExit(str(exc)) from exc

    table = quote_identifier(table_name)
    with connect(db_path, read_only=True) as con:
        summary_rows = fetch_summary_rows(con, table)
        ref_counts = fetch_top_counts(con, table, "center_ref")
        word_counts = fetch_top_center_word_counts(con, table)
        exact_examples = fetch_examples(
            con,
            table,
            example_type="exact_center_word",
            examples_per_group=examples_per_group,
            where_sql="center_normalized_word = normalized_term",
            order_sql="rowid",
        )
        low_count_examples = fetch_examples(
            con,
            table,
            example_type="low_count",
            examples_per_group=examples_per_group,
            where_sql=f"CAST(count_row_hit_count AS BIGINT) <= {low_count_threshold}",
            order_sql="ABS(CAST(skip AS BIGINT)), CAST(span_letters AS BIGINT), center_ref",
        )

    for row in summary_rows:
        key = (str(row["corpus"]), str(row["term_id"]), str(row["mode"]))
        row["top_center_refs"] = format_top_pairs(ref_counts.get(key, []))
        row["top_center_words"] = format_top_pairs(word_counts.get(key, []))
    examples = exact_examples + low_count_examples
    examples.sort(key=lambda row: (row["example_type"], int(row["count_row_hit_count"] or 0), row["corpus"], row["term_id"]))
    return summary_rows, examples


def fetch_summary_rows(con: Any, table: str) -> list[dict[str, str | int]]:
    cursor = con.execute(
        f"""
        SELECT
            corpus,
            ANY_VALUE(corpus_language) AS corpus_language,
            term_id,
            ANY_VALUE(concept) AS concept,
            ANY_VALUE(category) AS category,
            ANY_VALUE(term_language) AS term_language,
            ANY_VALUE(term) AS term,
            ANY_VALUE(normalized_term) AS normalized_term,
            mode,
            MAX(CAST(count_row_hit_count AS BIGINT)) AS count_row_hit_count,
            COUNT(*) AS exported_hits,
            SUM(CASE WHEN direction = 'forward' THEN 1 ELSE 0 END) AS forward_hits,
            SUM(CASE WHEN direction = 'backward' THEN 1 ELSE 0 END) AS backward_hits,
            SUM(CASE WHEN center_normalized_word = normalized_term THEN 1 ELSE 0 END) AS exact_center_word_hits,
            MIN(ABS(CAST(skip AS BIGINT))) AS min_abs_skip,
            MAX(ABS(CAST(skip AS BIGINT))) AS max_abs_skip,
            MIN(CAST(span_letters AS BIGINT)) AS min_span_letters,
            MAX(CAST(span_letters AS BIGINT)) AS max_span_letters,
            COUNT(DISTINCT NULLIF(center_ref, '')) AS distinct_center_refs,
            COUNT(DISTINCT NULLIF(COALESCE(NULLIF(center_normalized_word, ''), center_word), '')) AS distinct_center_words
        FROM {table}
        GROUP BY corpus, term_id, mode
        ORDER BY corpus, term_id
        """
    )
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    numeric_columns = {
        "count_row_hit_count",
        "exported_hits",
        "forward_hits",
        "backward_hits",
        "exact_center_word_hits",
        "min_abs_skip",
        "max_abs_skip",
        "min_span_letters",
        "max_span_letters",
        "distinct_center_refs",
        "distinct_center_words",
    }
    output: list[dict[str, str | int]] = []
    for db_row in rows:
        item: dict[str, str | int] = {}
        for column, value in zip(columns, db_row, strict=True):
            item[column] = int(value) if column in numeric_columns else str(value or "")
        item["top_center_refs"] = ""
        item["top_center_words"] = ""
        output.append(item)
    return output


def fetch_top_counts(con: Any, table: str, column: str) -> dict[tuple[str, str, str], list[tuple[str, int]]]:
    rows = con.execute(
        f"""
        SELECT corpus, term_id, mode, {column} AS value, COUNT(*) AS count, MIN(rowid) AS first_seen
        FROM {table}
        WHERE {column} <> ''
        GROUP BY corpus, term_id, mode, {column}
        ORDER BY corpus, term_id, mode, count DESC, first_seen
        """
    ).fetchall()
    return group_top_count_rows(rows)


def fetch_top_center_word_counts(con: Any, table: str) -> dict[tuple[str, str, str], list[tuple[str, int]]]:
    rows = con.execute(
        f"""
        WITH words AS (
            SELECT
                corpus,
                term_id,
                mode,
                rowid,
                COALESCE(NULLIF(center_normalized_word, ''), center_word) AS value
            FROM {table}
        )
        SELECT corpus, term_id, mode, value, COUNT(*) AS count, MIN(rowid) AS first_seen
        FROM words
        WHERE value <> ''
        GROUP BY corpus, term_id, mode, value
        ORDER BY corpus, term_id, mode, count DESC, first_seen
        """
    ).fetchall()
    return group_top_count_rows(rows)


def group_top_count_rows(rows: list[tuple[Any, ...]]) -> dict[tuple[str, str, str], list[tuple[str, int]]]:
    grouped: dict[tuple[str, str, str], list[tuple[str, int]]] = defaultdict(list)
    for corpus, term_id, mode, value, count, _first_seen in rows:
        key = (str(corpus), str(term_id), str(mode))
        if len(grouped[key]) < 5:
            grouped[key].append((str(value), int(count)))
    return grouped


def fetch_examples(
    con: Any,
    table: str,
    *,
    example_type: str,
    examples_per_group: int,
    where_sql: str,
    order_sql: str,
) -> list[dict[str, str]]:
    cursor = con.execute(
        f"""
        SELECT *
        FROM (
            SELECT
                *,
                ROW_NUMBER() OVER (
                    PARTITION BY corpus, term_id, mode
                    ORDER BY {order_sql}
                ) AS rn
            FROM {table}
            WHERE {where_sql}
        )
        WHERE rn <= ?
        ORDER BY corpus, term_id, mode, rn
        """,
        [examples_per_group],
    )
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    examples = []
    for db_row in rows:
        row = {column: "" if value is None else str(value) for column, value in zip(columns, db_row, strict=True)}
        examples.append(compact_example(row, example_type))
    return examples


def format_top_pairs(values: list[tuple[str, int]]) -> str:
    return "; ".join(f"{value}={count}" for value, count in values if value)


def build_version_presence_rows(rows: list[dict[str, str]], *, mode: str) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("mode") == mode:
            grouped[(row["term_id"], row["mode"])].append(row)

    output = []
    for (_term_id, _mode), items in sorted(grouped.items()):
        template = items[0]
        bible_present = [item for item in items if not is_control_corpus(item["corpus"]) and int(item["hit_count"]) > 0]
        control_present = [item for item in items if is_control_corpus(item["corpus"]) and int(item["hit_count"]) > 0]
        bible_zero = [item for item in items if not is_control_corpus(item["corpus"]) and int(item["hit_count"]) == 0]
        control_zero = [item for item in items if is_control_corpus(item["corpus"]) and int(item["hit_count"]) == 0]
        bible_max = max(bible_present, key=lambda item: int(item["hit_count"]), default={})
        control_max = max(control_present, key=lambda item: int(item["hit_count"]), default={})
        output.append(
            {
                "term_id": template["term_id"],
                "concept": template.get("concept", ""),
                "term_language": template.get("term_language", ""),
                "term": template.get("term", ""),
                "normalized_term": template.get("normalized_term", ""),
                "mode": template["mode"],
                "bible_present_corpora": format_counted_corpora(bible_present),
                "control_present_corpora": format_counted_corpora(control_present),
                "bible_zero_corpora": ",".join(sorted(item["corpus"] for item in bible_zero)),
                "control_zero_corpora": ",".join(sorted(item["corpus"] for item in control_zero)),
                "bible_max_corpus": bible_max.get("corpus", ""),
                "bible_max_hit_count": bible_max.get("hit_count", "0"),
                "control_max_corpus": control_max.get("corpus", ""),
                "control_max_hit_count": control_max.get("hit_count", "0"),
            }
        )
    return output


def compact_example(row: dict[str, str], example_type: str) -> dict[str, str]:
    return {
        "example_type": example_type,
        "corpus": row["corpus"],
        "term_id": row["term_id"],
        "concept": row["concept"],
        "term": row["term"],
        "normalized_term": row["normalized_term"],
        "count_row_hit_count": row["count_row_hit_count"],
        "skip": row["skip"],
        "direction": row["direction"],
        "span_letters": row["span_letters"],
        "start_ref": row["start_ref"],
        "center_ref": row["center_ref"],
        "end_ref": row["end_ref"],
        "center_word": row["center_word"],
        "center_normalized_word": row["center_normalized_word"],
    }


def example_sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    return (abs(int(row["skip"])), int(row["span_letters"]), row["center_ref"])


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_many(paths: Iterable[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        if path.exists():
            rows.extend(read_rows(path))
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    hit_summary: list[dict[str, str | int]],
    examples: list[dict[str, str]],
    version_rows: list[dict[str, str]],
    comparison_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exported_hits = sum(int(row["exported_hits"]) for row in hit_summary)
    exact_center_total = sum(int(row["exact_center_word_hits"]) for row in hit_summary)
    term_lookup = term_metadata_by_id(version_rows, hit_summary)
    bible_over_control = [
        row
        for row in comparison_rows
        if row.get("mode") == "full-span" and row.get("read") == "bible max rate exceeds all observed controls"
    ]
    low_count = [row for row in hit_summary if int(row["count_row_hit_count"]) <= args.low_count_threshold]
    command_lines = ["python3 -m scripts.summarize_dynamic_span_hits"]
    if args.db:
        command_lines.extend(
            [
                f"  --db {display_path(args.db)}",
                f"  --hits-table {args.hits_table}",
            ]
        )
    lines = [
        "# Dynamic Full-Span Hit Findings",
        "",
        "This report summarizes the exported dynamic full-span hit file without",
        "requiring a surface-center match. Every exported hit remains available",
        "in the hit CSV; exact center-word matches are reported as an additional",
        "flag, not as the admission rule.",
        "",
        "## Reproduce",
        "",
        "```bash",
        " \\\n".join(command_lines),
        "```",
        "",
        "## Scope",
        "",
        f"- exported term/corpus rows summarized: {len(hit_summary):,}",
        f"- exported hit rows summarized: {exported_hits:,}",
        f"- low-count threshold for examples: {args.low_count_threshold:,}",
        f"- exact center-word hits found: {exact_center_total:,}",
        f"- summary CSV: `{display_path(args.summary_csv)}`",
        f"- example CSV: `{display_path(args.examples_csv)}`",
        f"- version CSV: `{display_path(args.version_csv)}`",
        f"- report database: `{display_path(args.db)}`" if args.db else "- report database: not used",
        "",
        "## Version Presence Read",
        "",
        "Version presence is taken from the full-span count rows, including rows",
        "whose hit-level detail was deferred for partitioned export. That keeps",
        "the version question separate from the practical export threshold.",
        "",
        "| Term | Language | Bible present | Control present | Bible max | Control max |",
        "| --- | --- | --- | --- | ---: | ---: |",
    ]
    for row in sorted(version_rows, key=version_sort_key):
        lines.append(
            f"| {cell(display_term_cell(row))} | {row['term_language']} | "
            f"{cell(row['bible_present_corpora'])} | {cell(row['control_present_corpora'])} | "
            f"{max_cell(row['bible_max_corpus'], row['bible_max_hit_count'])} | "
            f"{max_cell(row['control_max_corpus'], row['control_max_hit_count'])} |"
        )
    lines.extend(
        [
            "",
            "## Bible-Over-Control Signals",
            "",
            "| Term | Language | Bible max corpus | Bible max rate | Control max rate | Ratio |",
            "| --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in sorted(bible_over_control, key=lambda item: float(item["bible_over_control_max_rate_ratio"].replace("inf", "1e999")), reverse=True)[:15]:
        display_row = row_with_term_metadata(row, term_lookup)
        lines.append(
            f"| {cell(display_term_cell(display_row))} | {row['term_language']} | {row['bible_max_corpus']} | "
            f"{row['bible_max_rate_per_million']} | {row['control_max_rate_per_million']} | "
            f"{row['bible_over_control_max_rate_ratio']} |"
        )
    lines.extend(
        [
            "",
            "## Low-Count Exported Rows",
            "",
            "Low-count rows are useful for human review because they are not dense",
            "letter-background fields. They still need controls and contextual",
            "review before any claim language.",
            "",
            "| Corpus | Term | Hits | Min abs skip | Center refs | Center words |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in sorted(low_count, key=lambda item: (int(item["count_row_hit_count"]), item["corpus"], item["term_id"]))[:25]:
        lines.append(
            f"| {row['corpus']} | {cell(display_term_cell(row))} | {row['count_row_hit_count']} | "
            f"{row['min_abs_skip']} | {cell(str(row['top_center_refs']))} | "
            f"{cell(display_top_center_words(str(row['top_center_words'])))} |"
        )
    lines.extend(
        [
            "",
            "## Example Hits",
            "",
            "| Type | Corpus | Term | Skip | Start | Center | End | Center word |",
            "| --- | --- | --- | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in examples[:30]:
        lines.append(
            f"| `{row['example_type']}` | {row['corpus']} | {cell(display_term_cell(row))} | {row['skip']} | "
            f"{row['start_ref']} | {row['center_ref']} | {row['end_ref']} | {cell(display_center_word(row))} |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Hidden-code presence and exact surface-center matches are separate observations.",
            "- The current export includes all hits for manageable count rows and defers dense rows for partitioned export.",
            "- A version-specific hit can be meaningful as a distribution fact even when the same term is absent elsewhere.",
            "- Non-Bible controls are comparison backgrounds, not disproof by themselves.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    hit_summary: list[dict[str, str | int]],
    examples: list[dict[str, str]],
    version_rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "script": "scripts/summarize_dynamic_span_hits.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "hit_summary_rows": len(hit_summary),
        "example_rows": len(examples),
        "version_rows": len(version_rows),
        "hits": display_path(args.hits),
        "summary_csv": display_path(args.summary_csv),
        "examples_csv": display_path(args.examples_csv),
        "version_csv": display_path(args.version_csv),
        "report": display_path(args.report),
        "db": display_path(args.db) if args.db else "",
        "hits_table": args.hits_table if args.db else "",
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def is_control_corpus(corpus: str) -> bool:
    return corpus.startswith(CONTROL_PREFIXES)


def format_counted_corpora(rows: list[dict[str, str]]) -> str:
    return "; ".join(f"{row['corpus']}={row['hit_count']}" for row in sorted(rows, key=lambda item: item["corpus"]))


def format_counter(counter: Counter[str], limit: int) -> str:
    return "; ".join(f"{key}={count}" for key, count in counter.most_common(limit) if key)


def version_sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    bible_present = 1 if row["bible_present_corpora"] else 0
    control_present = 1 if row["control_present_corpora"] else 0
    return (-bible_present, control_present, row["term_language"], row["term_id"])


def cell(value: str) -> str:
    return value.replace("|", "\\|") if value else ""


def term_metadata_by_id(*row_groups: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for rows in row_groups:
        for row in rows:
            term_id = str(row.get("term_id", ""))
            if term_id and term_id not in lookup and (row.get("term") or row.get("normalized_term")):
                lookup[term_id] = dict(row)
    return lookup


def row_with_term_metadata(row: dict[str, str], lookup: dict[str, dict[str, Any]]) -> dict[str, Any]:
    merged = dict(lookup.get(row.get("term_id", ""), {}))
    for key, value in row.items():
        if value or key not in merged:
            merged[key] = value
    return merged


def display_term_cell(row: dict[str, Any]) -> str:
    term_id = str(row.get("term_id", ""))
    term = str(row.get("term") or row.get("normalized_term") or "")
    if not term:
        return f"`{term_id}`" if term_id else ""
    label = display_term(term, english=str(row.get("concept") or "") or None)
    return f"{label}<br>`{term_id}`" if term_id else label


def display_center_word(row: dict[str, str]) -> str:
    word = row.get("center_word", "")
    if not (contains_hebrew(word) or contains_greek(word)):
        return word
    english = row.get("concept", "") if row.get("center_normalized_word") == row.get("normalized_term") else ""
    return display_term(word, english=english or None)


def display_top_center_words(value: str) -> str:
    parts = []
    for item in value.split("; "):
        if not item:
            continue
        word, sep, count = item.rpartition("=")
        if sep and (contains_hebrew(word) or contains_greek(word)):
            parts.append(f"{display_term(word)}={count}")
        else:
            parts.append(item)
    return "; ".join(parts)


def max_cell(corpus: str, hit_count: str) -> str:
    return f"{corpus}={hit_count}" if corpus else "none=0"


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
