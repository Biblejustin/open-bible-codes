#!/usr/bin/env python3
"""Build ranked review queues from relaxed all-code surface-context exports."""

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
from els.report_db import (
    DuckDBUnavailable,
    ReportDBStale,
    fetch_dicts,
    quote_identifier,
    report_table_name_for_path,
    sanitize_table_name,
    sql_literal,
    verify_table_current,
)
from scripts.analyze_hebrew_hit_version_presence import canonical_ref


DEFAULT_HITS = Path("reports/hebrew_theology_all_codes/surface_all_codes.csv")
DEFAULT_SUMMARY = Path("reports/hebrew_theology_all_codes/surface_all_codes_summary.csv")
DEFAULT_QUEUE = Path("reports/hebrew_theology_all_codes/triage_queue.csv")
DEFAULT_MD = Path("docs/HEBREW_THEOLOGY_ALL_CODES_TRIAGE.md")
DEFAULT_MANIFEST = Path("reports/hebrew_theology_all_codes/triage.manifest.json")
DEFAULT_REPORT_DB = Path("reports/db/open_bible_codes.duckdb")

BUCKET_ORDER = {
    "center_word_exact": 0,
    "center_word_same_concept": 1,
    "center_word_same_category": 2,
    "center_verse_exact": 3,
    "center_verse_same_concept": 4,
    "center_verse_same_category": 5,
    "span_exact": 6,
    "span_same_concept": 7,
    "span_same_category": 8,
    "hidden_path_only": 9,
}

QUEUE_FIELDNAMES = [
    "bucket",
    "bucket_rank",
    "overall_rank",
    "presence_scope",
    "present_corpora",
    "corpus_count",
    "corpus_row_count",
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "normalized_length",
    "skip",
    "direction",
    "span_letters",
    "offsets_by_corpus",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_word",
    "center_normalized_word",
    "center_words_by_corpus",
    "best_context",
    "center_word_exact",
    "center_word_same_concept",
    "center_word_same_category",
    "center_exact",
    "center_same_concept",
    "center_same_category",
    "span_exact",
    "span_same_concept",
    "span_same_category",
    "center_word_related_terms",
    "center_verse_related_terms",
    "span_related_refs",
    "control_band",
    "control_p",
    "control_q",
    "control_read",
    "triage_score",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    control_by_term = read_control_summaries(args.controlled_summary)
    summary_by_term, all_corpora = read_summary(args.summary)
    candidate_limit = max(args.max_rows_per_bucket * args.candidate_multiplier, args.max_rows_per_bucket)
    db = resolve_db(args)
    args.effective_db = str(db) if db is not None else ""
    if db is not None:
        candidates_by_bucket, all_corpora_from_hits, scanned_rows = collect_candidates_db(
            db=db,
            table=args.hits_table or report_table_name_for_path(args.hits),
            control_by_term=control_by_term,
            limit=candidate_limit,
        )
    else:
        candidates_by_bucket, all_corpora_from_hits, scanned_rows = collect_candidates(
            args.hits,
            control_by_term,
            limit=candidate_limit,
        )
    all_corpora.update(all_corpora_from_hits)
    selected_keys = {
        candidate["pattern_key"]
        for candidates in candidates_by_bucket.values()
        for candidate in candidates
    }
    presence_by_key = (
        collect_presence_db(db, args.hits_table or report_table_name_for_path(args.hits), selected_keys)
        if db is not None
        else collect_presence(args.hits, selected_keys)
    )
    queue_rows = build_queue_rows(
        candidates_by_bucket,
        presence_by_key,
        summary_by_term,
        control_by_term,
        all_corpora=all_corpora,
        max_rows_per_bucket=args.max_rows_per_bucket,
    )
    write_rows(args.queue_out, QUEUE_FIELDNAMES, queue_rows)
    write_markdown(args.markdown_out, args, queue_rows, scanned_rows, all_corpora)
    write_manifest(
        args.manifest_out,
        args,
        queue_rows,
        scanned_rows=scanned_rows,
        selected_keys=len(selected_keys),
        all_corpora=all_corpora,
        started=started,
    )
    print(args.queue_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hits", type=Path, default=DEFAULT_HITS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--controlled-summary", type=Path, action="append", default=[])
    parser.add_argument("--title", default="Hebrew Theology All-Codes Triage")
    parser.add_argument("--max-rows-per-bucket", type=int, default=100)
    parser.add_argument(
        "--candidate-multiplier",
        type=int,
        default=50,
        help="First-pass candidate pool multiplier before corpus-presence reranking.",
    )
    parser.add_argument("--queue-out", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--db", type=Path, help="Read hit rows from a DuckDB report database.")
    parser.add_argument("--hits-table", help="DuckDB hits table name. Defaults to a name derived from --hits.")
    parser.add_argument("--no-db", action="store_true", help="Disable automatic DuckDB use even when a current DB exists.")
    return parser


def resolve_db(args: argparse.Namespace) -> Path | None:
    if args.no_db:
        return None
    db = args.db
    explicit = db is not None
    if db is None:
        db = DEFAULT_REPORT_DB
        if not db.exists():
            return None
    try:
        verify_table_current(
            db_path=db,
            table_name=args.hits_table or report_table_name_for_path(args.hits),
            source_path=args.hits,
        )
    except (DuckDBUnavailable, FileNotFoundError, ReportDBStale):
        if explicit:
            raise
        return None
    return db


def read_summary(path: Path) -> tuple[dict[str, dict[str, str]], set[str]]:
    by_term: dict[str, dict[str, str]] = {}
    corpora: set[str] = set()
    if not path.exists():
        return by_term, corpora
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            corpora.add(row.get("corpus", ""))
            by_term.setdefault(row.get("term_id", ""), row)
    corpora.discard("")
    return by_term, corpora


def read_control_summaries(paths: list[Path]) -> dict[str, dict[str, str]]:
    by_term: dict[str, dict[str, str]] = {}
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                term_id = row.get("term_id", "")
                if not term_id:
                    continue
                current = by_term.get(term_id)
                if current is None or control_sort_key(row) < control_sort_key(current):
                    by_term[term_id] = row
    return by_term


def collect_candidates(
    path: Path,
    control_by_term: dict[str, dict[str, str]],
    *,
    limit: int,
) -> tuple[dict[str, list[dict[str, Any]]], set[str], int]:
    candidates_by_bucket: dict[str, list[dict[str, Any]]] = defaultdict(list)
    corpora: set[str] = set()
    scanned = 0
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            scanned += 1
            corpora.add(row.get("corpus", ""))
            bucket = bucket_for_row(row)
            score = first_pass_score(row, control_by_term.get(row.get("term_id", ""), {}))
            candidates = candidates_by_bucket[bucket]
            candidates.append(
                {
                    "score": score,
                    "row": row,
                    "bucket": bucket,
                    "pattern_key": pattern_key(row),
                }
            )
            if len(candidates) > limit * 2:
                candidates.sort(key=lambda candidate: candidate["score"])
                del candidates[limit:]
    for candidates in candidates_by_bucket.values():
        candidates.sort(key=lambda candidate: candidate["score"])
        del candidates[limit:]
    corpora.discard("")
    return candidates_by_bucket, corpora, scanned


def collect_candidates_db(
    *,
    db: Path,
    table: str,
    control_by_term: dict[str, dict[str, str]],
    limit: int,
) -> tuple[dict[str, list[dict[str, Any]]], set[str], int]:
    qtable = quote_identifier(sanitize_table_name(table))
    rows = fetch_dicts(
        db_path=db,
        query=f"""
            WITH labeled AS (
                SELECT
                    *,
                    rowid AS _source_rowid,
                    {bucket_sql()} AS _bucket,
                    {control_rank_sql(control_by_term)} AS _control_rank
                FROM {qtable}
            ),
            ranked AS (
                SELECT
                    *,
                    row_number() OVER (
                        PARTITION BY _bucket
                        ORDER BY
                            _control_rank,
                            abs(coalesce(try_cast(skip AS BIGINT), 0)),
                            coalesce(try_cast(span_letters AS BIGINT), 999999999),
                            -length(coalesce(normalized_term, '')),
                            center_ref,
                            term_id,
                            _source_rowid
                    ) AS _rank
                FROM labeled
            )
            SELECT *
            FROM ranked
            WHERE _rank <= {int(limit)}
            ORDER BY _bucket, _rank
        """,
    )
    candidates_by_bucket: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        bucket = row.pop("_bucket", bucket_for_row(row))
        row.pop("_control_rank", None)
        row.pop("_rank", None)
        row.pop("_source_rowid", None)
        candidates_by_bucket[bucket].append(
            {
                "score": first_pass_score(row, control_by_term.get(row.get("term_id", ""), {})),
                "row": row,
                "bucket": bucket,
                "pattern_key": pattern_key(row),
            }
        )
    for candidates in candidates_by_bucket.values():
        candidates.sort(key=lambda candidate: candidate["score"])
        del candidates[limit:]
    corpora = {
        row["corpus"]
        for row in fetch_dicts(
            db_path=db,
            query=f"SELECT DISTINCT corpus FROM {qtable} WHERE corpus IS NOT NULL AND corpus != ''",
        )
    }
    scanned = int_or_zero(fetch_dicts(db_path=db, query=f"SELECT count(*) AS row_count FROM {qtable}")[0]["row_count"])
    return candidates_by_bucket, corpora, scanned


def collect_presence(path: Path, selected_keys: set[tuple[str, ...]]) -> dict[tuple[str, ...], dict[str, Any]]:
    presence: dict[tuple[str, ...], dict[str, Any]] = {
        key: {"corpora": set(), "row_count": 0, "center_words": {}} for key in selected_keys
    }
    if not selected_keys:
        return presence
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = pattern_key(row)
            if key not in presence:
                continue
            item = presence[key]
            corpus = row.get("corpus", "")
            if corpus:
                item["corpora"].add(corpus)
                item["center_words"].setdefault(corpus, row.get("center_normalized_word", ""))
                item.setdefault("offsets", {}).setdefault(
                    corpus,
                    "/".join(
                        [
                            row.get("start_offset", ""),
                            row.get("center_offset", ""),
                            row.get("end_offset", ""),
                        ]
                    ),
                )
            item["row_count"] += 1
    return presence


def collect_presence_db(
    db: Path,
    table: str,
    selected_keys: set[tuple[str, ...]],
) -> dict[tuple[str, ...], dict[str, Any]]:
    presence: dict[tuple[str, ...], dict[str, Any]] = {
        key: {"corpora": set(), "row_count": 0, "center_words": {}} for key in selected_keys
    }
    if not selected_keys:
        return presence
    qtable = quote_identifier(sanitize_table_name(table))
    combos = sorted({key[:4] for key in selected_keys})
    for chunk in chunks(combos, 500):
        values = ",\n".join("(" + ",".join(sql_literal(part) for part in key) + ")" for key in chunk)
        rows = fetch_dicts(
            db_path=db,
            query=f"""
                WITH keys(term_id, normalized_term, skip, direction) AS (
                    VALUES {values}
                )
                SELECT h.*
                FROM {qtable} AS h
                JOIN keys AS k
                  ON h.term_id = k.term_id
                 AND h.normalized_term = k.normalized_term
                 AND h.skip = k.skip
                 AND h.direction = k.direction
                ORDER BY h.rowid
            """,
        )
        for row in rows:
            key = pattern_key(row)
            if key not in presence:
                continue
            item = presence[key]
            corpus = row.get("corpus", "")
            if corpus:
                item["corpora"].add(corpus)
                item["center_words"].setdefault(corpus, row.get("center_normalized_word", ""))
                item.setdefault("offsets", {}).setdefault(
                    corpus,
                    "/".join(
                        [
                            row.get("start_offset", ""),
                            row.get("center_offset", ""),
                            row.get("end_offset", ""),
                        ]
                    ),
                )
            item["row_count"] += 1
    return presence


def build_queue_rows(
    candidates_by_bucket: dict[str, list[dict[str, Any]]],
    presence_by_key: dict[tuple[str, ...], dict[str, Any]],
    summary_by_term: dict[str, dict[str, str]],
    control_by_term: dict[str, dict[str, str]],
    *,
    all_corpora: set[str],
    max_rows_per_bucket: int,
) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    all_count = len(all_corpora)
    overall_rank = 1
    for bucket in sorted(BUCKET_ORDER, key=BUCKET_ORDER.get):
        candidates = candidates_by_bucket.get(bucket, [])
        rows = []
        best_by_key: dict[tuple[str, ...], dict[str, Any]] = {}
        for candidate in candidates:
            current = best_by_key.get(candidate["pattern_key"])
            if current is None or candidate["score"] < current["score"]:
                best_by_key[candidate["pattern_key"]] = candidate
        for candidate in best_by_key.values():
            row = candidate["row"]
            presence = presence_by_key.get(candidate["pattern_key"], {})
            corpora = sorted(presence.get("corpora", set()))
            control = control_by_term.get(row.get("term_id", ""), {})
            summary = summary_by_term.get(row.get("term_id", ""), {})
            rows.append(
                queue_row(
                    bucket,
                    row,
                    control,
                    summary,
                    corpora=corpora,
                    center_words_by_corpus=presence.get("center_words", {}),
                    offsets_by_corpus=presence.get("offsets", {}),
                    corpus_row_count=int(presence.get("row_count", 0)),
                    all_corpus_count=all_count,
                )
            )
        rows.sort(key=final_score_tuple)
        rows = rows[:max_rows_per_bucket]
        for bucket_rank, row in enumerate(rows, start=1):
            row["bucket_rank"] = bucket_rank
            row["overall_rank"] = overall_rank
            row["triage_score"] = triage_score_text(row)
            overall_rank += 1
            output.append(row)
    return output


def queue_row(
    bucket: str,
    row: dict[str, str],
    control: dict[str, str],
    summary: dict[str, str],
    *,
    corpora: list[str],
    center_words_by_corpus: dict[str, str],
    offsets_by_corpus: dict[str, str],
    corpus_row_count: int,
    all_corpus_count: int,
) -> dict[str, object]:
    corpus_count = len(corpora)
    return {
        "bucket": bucket,
        "bucket_rank": 0,
        "overall_rank": 0,
        "presence_scope": presence_scope(corpus_count, all_corpus_count),
        "present_corpora": ",".join(corpora),
        "corpus_count": corpus_count,
        "corpus_row_count": corpus_row_count,
        "term_id": row.get("term_id", ""),
        "concept": row.get("concept", ""),
        "category": row.get("category", ""),
        "term": row.get("term", ""),
        "normalized_term": row.get("normalized_term", ""),
        "normalized_length": summary.get("normalized_length", len(row.get("normalized_term", ""))),
        "skip": row.get("skip", ""),
        "direction": row.get("direction", ""),
        "span_letters": row.get("span_letters", ""),
        "offsets_by_corpus": ";".join(
            f"{corpus}:{offsets_by_corpus.get(corpus, '')}" for corpus in corpora
        ),
        "start_ref": canonical_ref(row.get("start_ref", "")),
        "center_ref": canonical_ref(row.get("center_ref", "")),
        "end_ref": canonical_ref(row.get("end_ref", "")),
        "center_word": row.get("center_word", ""),
        "center_normalized_word": row.get("center_normalized_word", ""),
        "center_words_by_corpus": ";".join(
            f"{corpus}:{center_words_by_corpus.get(corpus, '')}" for corpus in corpora
        ),
        "best_context": row.get("best_context", ""),
        "center_word_exact": row.get("center_word_exact", ""),
        "center_word_same_concept": row.get("center_word_same_concept", ""),
        "center_word_same_category": row.get("center_word_same_category", ""),
        "center_exact": row.get("center_exact", ""),
        "center_same_concept": row.get("center_same_concept", ""),
        "center_same_category": row.get("center_same_category", ""),
        "span_exact": row.get("span_exact", ""),
        "span_same_concept": row.get("span_same_concept", ""),
        "span_same_category": row.get("span_same_category", ""),
        "center_word_related_terms": ";".join(
            part for part in (
                row.get("center_word_same_concept_terms", ""),
                row.get("center_word_same_category_terms", ""),
            )
            if part
        ),
        "center_verse_related_terms": ";".join(
            part for part in (
                row.get("center_same_concept_terms", ""),
                row.get("center_same_category_terms", ""),
            )
            if part
        ),
        "span_related_refs": ";".join(
            part for part in (
                row.get("span_exact_refs", ""),
                row.get("span_same_concept_refs", ""),
                row.get("span_same_category_refs", ""),
            )
            if part
        ),
        "control_band": control.get("representative_best_band")
        or control.get("paired_best_band")
        or control.get("paired_band", ""),
        "control_p": control.get("representative_best_p")
        or control.get("paired_best_p")
        or control.get("combined_min_p_ge", ""),
        "control_q": control.get("representative_best_q")
        or control.get("paired_best_q")
        or control.get("combined_min_q_value", ""),
        "control_read": control.get("representative_best_read")
        or control.get("paired_best_read")
        or control.get("read", ""),
        "triage_score": "",
    }


def bucket_for_row(row: dict[str, str]) -> str:
    if truthy(row.get("center_word_exact", "")):
        return "center_word_exact"
    if truthy(row.get("center_word_same_concept", "")):
        return "center_word_same_concept"
    if truthy(row.get("center_word_same_category", "")):
        return "center_word_same_category"
    if truthy(row.get("center_exact", "")):
        return "center_verse_exact"
    if truthy(row.get("center_same_concept", "")):
        return "center_verse_same_concept"
    if truthy(row.get("center_same_category", "")):
        return "center_verse_same_category"
    if truthy(row.get("span_exact", "")):
        return "span_exact"
    if truthy(row.get("span_same_concept", "")):
        return "span_same_concept"
    if truthy(row.get("span_same_category", "")):
        return "span_same_category"
    return "hidden_path_only"


def bucket_sql() -> str:
    return """
        CASE
            WHEN lower(coalesce(center_word_exact, '')) IN ('true', '1', 'yes') THEN 'center_word_exact'
            WHEN lower(coalesce(center_word_same_concept, '')) IN ('true', '1', 'yes') THEN 'center_word_same_concept'
            WHEN lower(coalesce(center_word_same_category, '')) IN ('true', '1', 'yes') THEN 'center_word_same_category'
            WHEN lower(coalesce(center_exact, '')) IN ('true', '1', 'yes') THEN 'center_verse_exact'
            WHEN lower(coalesce(center_same_concept, '')) IN ('true', '1', 'yes') THEN 'center_verse_same_concept'
            WHEN lower(coalesce(center_same_category, '')) IN ('true', '1', 'yes') THEN 'center_verse_same_category'
            WHEN lower(coalesce(span_exact, '')) IN ('true', '1', 'yes') THEN 'span_exact'
            WHEN lower(coalesce(span_same_concept, '')) IN ('true', '1', 'yes') THEN 'span_same_concept'
            WHEN lower(coalesce(span_same_category, '')) IN ('true', '1', 'yes') THEN 'span_same_category'
            ELSE 'hidden_path_only'
        END
    """


def control_rank_sql(control_by_term: dict[str, dict[str, str]]) -> str:
    if not control_by_term:
        return "3"
    cases = [
        f"WHEN {sql_literal(term_id)} THEN {control_rank(control)}"
        for term_id, control in sorted(control_by_term.items())
    ]
    return "CASE term_id " + " ".join(cases) + " ELSE 3 END"


def first_pass_score(row: dict[str, str], control: dict[str, str]) -> tuple[Any, ...]:
    return (
        BUCKET_ORDER[bucket_for_row(row)],
        control_rank(control),
        abs(int_or_zero(row.get("skip", ""))),
        int_or_large(row.get("span_letters", "")),
        -len(row.get("normalized_term", "")),
        canonical_ref(row.get("center_ref", "")),
        row.get("term_id", ""),
    )


def final_score_tuple(row: dict[str, object]) -> tuple[Any, ...]:
    return (
        BUCKET_ORDER[str(row["bucket"])],
        -int(row.get("corpus_count", 0)),
        control_rank_from_values(str(row.get("control_p", "")), str(row.get("control_q", ""))),
        abs(int_or_zero(row.get("skip", ""))),
        int_or_large(row.get("span_letters", "")),
        -int_or_zero(row.get("normalized_length", "")),
        str(row.get("center_ref", "")),
        str(row.get("term_id", "")),
    )


def control_sort_key(row: dict[str, str]) -> tuple[float, float, str]:
    return (
        float_or_one(row.get("representative_best_q") or row.get("combined_min_q_value", "")),
        float_or_one(row.get("representative_best_p") or row.get("combined_min_p_ge", "")),
        row.get("corpus", ""),
    )


def control_rank(control: dict[str, str]) -> int:
    return control_rank_from_values(
        control.get("representative_best_p") or control.get("combined_min_p_ge", ""),
        control.get("representative_best_q") or control.get("combined_min_q_value", ""),
    )


def control_rank_from_values(raw_p: str, raw_q: str) -> int:
    q = float_or_one(raw_q)
    p = float_or_one(raw_p)
    if q <= 0.05:
        return 0
    if p <= 0.05:
        return 1
    if raw_p or raw_q:
        return 2
    return 3


def pattern_key(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row.get("term_id", ""),
        row.get("normalized_term", ""),
        row.get("skip", ""),
        row.get("direction", ""),
        canonical_ref(row.get("start_ref", "")),
        canonical_ref(row.get("center_ref", "")),
        canonical_ref(row.get("end_ref", "")),
    )


def presence_scope(corpus_count: int, all_corpus_count: int) -> str:
    if corpus_count and corpus_count == all_corpus_count:
        return "all_source"
    if corpus_count > 1:
        return "multi_source"
    if corpus_count == 1:
        return "source_specific"
    return "unknown"


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    scanned_rows: int,
    all_corpora: set[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_bucket = group_by_bucket(rows)
    lines = [
        f"# {args.title}",
        "",
        "This is a compact review queue built from the relaxed all-codes export.",
        "It ranks same center-word rows first, then related center-word rows,",
        "center-verse rows, span rows, and finally hidden-path-only rows.",
        "",
        "It is a triage aid, not a claim-grade filter.",
        "",
        "## Inputs",
        "",
        f"- Hits: `{args.hits}`",
        f"- Summary: `{args.summary}`",
        f"- Report DB: `{args.effective_db or 'not used'}`",
        f"- Queue CSV: `{args.queue_out}`",
        f"- Corpora: `{', '.join(sorted(all_corpora))}`",
        "",
        "## Counts",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Raw rows scanned | {scanned_rows:,} |",
        f"| Queue rows | {len(rows):,} |",
    ]
    for bucket in sorted(BUCKET_ORDER, key=BUCKET_ORDER.get):
        lines.append(f"| `{bucket}` queue rows | {len(by_bucket.get(bucket, [])):,} |")
    lines.extend(["", "## Top Queue Rows", ""])
    for bucket in sorted(BUCKET_ORDER, key=BUCKET_ORDER.get):
        bucket_rows = by_bucket.get(bucket, [])
        if not bucket_rows:
            continue
        lines.extend(
            [
                f"### {bucket}",
                "",
                "| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |",
                "| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |",
            ]
        )
        for row in bucket_rows[:20]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["bucket_rank"]),
                        str(row["presence_scope"]),
                        f"`{row['term_id']}`",
                        str(row["concept"]),
                        str(row["skip"]),
                        str(row["span_letters"]),
                        str(row["center_ref"]),
                        f"`{row['center_normalized_word']}`",
                        str(row["control_band"] or row["control_read"]),
                    ]
                )
                + " |"
            )
        lines.append("")
    lines.extend(
        [
            "## Read",
            "",
            "Rows at the top are good manual-review candidates because their hidden ELS",
            "path center is located on, or near, surface language from the same declared",
            "term set. The `presence_scope` column reports whether the selected exact",
            "ref-key pattern appears in every configured source, multiple sources, or",
            "only one source among the selected candidate keys.",
        ]
    )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    *,
    scanned_rows: int,
    selected_keys: int,
    all_corpora: set[str],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": "triage_surface_all_codes",
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "git_commit": run_git("rev-parse", "--short", "HEAD"),
        "hits": str(args.hits),
        "summary": str(args.summary),
        "report_db": args.effective_db,
        "controlled_summaries": [str(path) for path in args.controlled_summary],
        "queue_out": str(args.queue_out),
        "markdown_out": str(args.markdown_out),
        "max_rows_per_bucket": args.max_rows_per_bucket,
        "candidate_multiplier": args.candidate_multiplier,
        "scanned_rows": scanned_rows,
        "selected_keys": selected_keys,
        "queue_rows": len(rows),
        "corpora": sorted(all_corpora),
        "bucket_counts": dict(Counter(str(row["bucket"]) for row in rows)),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def group_by_bucket(rows: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["bucket"])].append(row)
    return grouped


def triage_score_text(row: dict[str, object]) -> str:
    return (
        f"bucket={BUCKET_ORDER[str(row['bucket'])]};"
        f"corpora={row.get('corpus_count', 0)};"
        f"control={control_rank_from_values(str(row.get('control_p', '')), str(row.get('control_q', '')))};"
        f"skip={abs(int_or_zero(row.get('skip', '')))};"
        f"span={int_or_large(row.get('span_letters', ''))}"
    )


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


def int_or_zero(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def int_or_large(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 999999999


def float_or_one(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 1.0


def run_git(*args: str) -> str:
    completed = subprocess.run(["git", *args], check=False, capture_output=True, text=True)
    return completed.stdout.strip()


def chunks(values: list[tuple[str, ...]], size: int) -> Any:
    for index in range(0, len(values), size):
        yield values[index : index + size]


if __name__ == "__main__":
    raise SystemExit(main())
