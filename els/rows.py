"""CSV schema and row-producing helpers.

Field-name schemas for every CSV the CLI emits, plus the pure functions that
turn domain objects (hits, extensions, matrix letters, skip plans) into row
dicts, and the thin CSV writers built on those schemas. Extracted from els.cli
so the schema and its producers live in one place; cli.py re-imports the whole
surface for its commands and for backward-compatible `from els.cli import ...`.

None of this touches argparse, command state, or the multiprocessing surface
worker globals: it is pure data shaping plus CSV I/O.
"""

from __future__ import annotations

import csv
import sys
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path

from els.extensions import EXTENSION_TYPE_PRIORITY, extension_score as score_extension
from els.io import open_dict_writer
from els.search import ELSHit
from els.surface import SurfaceTerm


FIELDNAMES = [
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_offset",
    "end_offset",
    "span_letters",
    "sequence",
    "start_ref",
    "end_ref",
    "start_source",
    "end_source",
    "center_offset",
    "center_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "center_normalized_word",
]

SURFACE_CONTEXT_FIELDNAMES = [
    "corpus",
    "term_source",
    "term_id",
    "concept",
    "category",
    *FIELDNAMES,
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
    "center_word_same_concept_terms",
    "center_word_same_category_terms",
    "center_same_concept_terms",
    "center_same_category_terms",
    "span_exact_refs",
    "span_same_concept_refs",
    "span_same_category_refs",
]

PAIR_FIELDNAMES = [
    "corpus",
    "left_term_id",
    "left_concept",
    "left_term",
    "left_normalized",
    "left_skip",
    "left_start_ref",
    "left_end_ref",
    "left_center_ref",
    "left_center_word_index",
    "left_center_word",
    "left_center_normalized_word",
    "left_start_offset",
    "left_end_offset",
    "right_term_id",
    "right_concept",
    "right_term",
    "right_normalized",
    "right_skip",
    "right_start_ref",
    "right_end_ref",
    "right_center_ref",
    "right_center_word_index",
    "right_center_word",
    "right_center_normalized_word",
    "right_start_offset",
    "right_end_offset",
    "center_distance",
    "span_gap",
    "overlap",
    "same_center_ref",
    "same_center_chapter",
    "same_signed_skip",
    "same_abs_skip",
    "skip_abs_delta",
    "span_union_letters",
    "compactness_score",
    "cylindrical_row_width",
    "cylindrical_distance",
]

BATCH_FIELDNAMES = [
    "corpus",
    "corpus_language",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "normalized_length",
    "min_skip",
    "max_skip",
    "direction",
    "hit_count",
    "status",
]

EXTENSION_FIELDNAMES = [
    "corpus",
    *FIELDNAMES,
    "extension_type",
    "extension_side",
    "extension_length",
    "before_letters",
    "after_letters",
    "extended_sequence",
    "matched_normalized",
    "match_kind",
    "match_count",
    "matched_examples",
    "matched_refs",
    "extension_start_offset",
    "extension_end_offset",
    "extension_start_ref",
    "extension_end_ref",
]

EXTENSION_SUMMARY_FIELDNAMES = [
    "corpus",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "extension_type",
    "extension_side",
    "match_kind",
    "rows",
    "unique_extended_sequences",
    "max_extension_length",
    "max_match_count",
]

EXTENSION_TOP_FIELDNAMES = [
    *EXTENSION_FIELDNAMES,
    "extension_score",
]

MATRIX_LETTER_FIELDNAMES = [
    "corpus",
    "hit_index",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "letter_index",
    "letter",
    "offset",
    "row_width",
    "row",
    "col",
    "ref",
    "word_index",
    "word",
    "normalized_word",
    "start_ref",
    "end_ref",
    "center_ref",
]

MATRIX_SUMMARY_FIELDNAMES = [
    "corpus",
    "hit_index",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "row_width",
    "min_row",
    "max_row",
    "min_col",
    "max_col",
    "rows_spanned",
    "cols_spanned",
    "letter_count",
    "first_offset",
    "last_offset",
    "start_ref",
    "end_ref",
    "center_ref",
]

SKIP_PLAN_FIELDNAMES = [
    "term",
    "normalized_term",
    "normalized_length",
    "min_skip",
    "max_skip_limit",
    "selected_max_skip",
    "direction",
    "target_expected_hits",
    "expected_hits",
    "expected_at_min_skip",
    "status",
]


def surface_context_row(corpus_label: str, term: SurfaceTerm, hit: ELSHit, context) -> dict[str, object]:
    row = {
        "corpus": corpus_label,
        "term_source": term.term_source,
        "term_id": term.term_id,
        "concept": term.concept,
        "category": term.category,
    }
    row.update(hit.as_row())
    row.update(
        {
            "best_context": context.best_context,
            "center_word_exact": context.center_word_exact,
            "center_word_same_concept": context.center_word_same_concept,
            "center_word_same_category": context.center_word_same_category,
            "center_exact": context.center_exact,
            "center_same_concept": context.center_same_concept,
            "center_same_category": context.center_same_category,
            "span_exact": context.span_exact,
            "span_same_concept": context.span_same_concept,
            "span_same_category": context.span_same_category,
            "center_word_same_concept_terms": context.center_word_same_concept_terms,
            "center_word_same_category_terms": context.center_word_same_category_terms,
            "center_same_concept_terms": context.center_same_concept_terms,
            "center_same_category_terms": context.center_same_category_terms,
            "span_exact_refs": context.span_exact_refs,
            "span_same_concept_refs": context.span_same_concept_refs,
            "span_same_category_refs": context.span_same_category_refs,
        }
    )
    return row


def extension_row(corpus_label: str, hit: ELSHit, extension) -> dict[str, object]:
    row = {"corpus": corpus_label}
    row.update(hit.as_row())
    row.update(
        {
            "extension_type": extension.extension_type,
            "extension_side": extension.extension_side,
            "extension_length": extension.extension_length,
            "before_letters": extension.before_letters,
            "after_letters": extension.after_letters,
            "extended_sequence": extension.extended_sequence,
            "matched_normalized": extension.matched_normalized,
            "match_kind": extension.match_kind,
            "match_count": extension.match_count,
            "matched_examples": extension.matched_examples,
            "matched_refs": extension.matched_refs,
            "extension_start_offset": extension.extension_start_offset,
            "extension_end_offset": extension.extension_end_offset,
            "extension_start_ref": extension.extension_start_ref,
            "extension_end_ref": extension.extension_end_ref,
        }
    )
    return row


def matrix_letter_row(corpus_label: str, hit: ELSHit, letter, row_width: int) -> dict[str, object]:
    return {
        "corpus": corpus_label,
        "hit_index": letter.hit_index,
        "term": hit.term,
        "normalized_term": hit.normalized_term,
        "skip": hit.skip,
        "direction": hit.direction,
        "letter_index": letter.letter_index,
        "letter": letter.letter,
        "offset": letter.offset,
        "row_width": row_width,
        "row": letter.row,
        "col": letter.col,
        "ref": letter.ref,
        "word_index": letter.word_index,
        "word": letter.word,
        "normalized_word": letter.normalized_word,
        "start_ref": hit.start_ref,
        "end_ref": hit.end_ref,
        "center_ref": hit.center_ref,
    }


def matrix_summary_row(corpus_label: str, hit: ELSHit, summary) -> dict[str, object]:
    return {
        "corpus": corpus_label,
        "hit_index": summary.hit_index,
        "term": hit.term,
        "normalized_term": hit.normalized_term,
        "skip": hit.skip,
        "direction": hit.direction,
        "row_width": summary.row_width,
        "min_row": summary.min_row,
        "max_row": summary.max_row,
        "min_col": summary.min_col,
        "max_col": summary.max_col,
        "rows_spanned": summary.rows_spanned,
        "cols_spanned": summary.cols_spanned,
        "letter_count": summary.letter_count,
        "first_offset": summary.first_offset,
        "last_offset": summary.last_offset,
        "start_ref": hit.start_ref,
        "end_ref": hit.end_ref,
        "center_ref": hit.center_ref,
    }


def skip_plan_row(plan) -> dict[str, object]:
    return {
        "term": plan.term,
        "normalized_term": plan.normalized_term,
        "normalized_length": plan.normalized_length,
        "min_skip": plan.min_skip,
        "max_skip_limit": plan.max_skip_limit,
        "selected_max_skip": plan.selected_max_skip,
        "direction": plan.direction,
        "target_expected_hits": round(plan.target_expected_hits, 6),
        "expected_hits": round(plan.expected_hits, 6),
        "expected_at_min_skip": round(plan.expected_at_min_skip, 6),
        "status": plan.status,
    }


def add_extension_summary_group(
    groups: dict[tuple[str, ...], dict[str, object]],
    row: dict[str, str],
    extension_length: int,
) -> None:
    key = (
        row.get("corpus", ""),
        row.get("term", ""),
        row.get("normalized_term", ""),
        row.get("skip", ""),
        row.get("direction", ""),
        row.get("extension_type", ""),
        row.get("extension_side", ""),
        row.get("match_kind", ""),
    )
    group = groups.setdefault(
        key,
        {
            "corpus": key[0],
            "term": key[1],
            "normalized_term": key[2],
            "skip": key[3],
            "direction": key[4],
            "extension_type": key[5],
            "extension_side": key[6],
            "match_kind": key[7],
            "rows": 0,
            "unique_extended_sequences": set(),
            "max_extension_length": 0,
            "max_match_count": 0,
        },
    )
    group["rows"] = int(group["rows"]) + 1
    unique_sequences = group["unique_extended_sequences"]
    assert isinstance(unique_sequences, set)
    unique_sequences.add(row.get("extended_sequence", ""))
    group["max_extension_length"] = max(
        int(group["max_extension_length"]),
        extension_length,
    )
    group["max_match_count"] = max(
        int(group["max_match_count"]),
        int_or_zero(row.get("match_count", "")),
    )


def extension_summary_rows(
    groups: dict[tuple[str, ...], dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for group in groups.values():
        unique_sequences = group["unique_extended_sequences"]
        assert isinstance(unique_sequences, set)
        rows.append(
            {
                "corpus": group["corpus"],
                "term": group["term"],
                "normalized_term": group["normalized_term"],
                "skip": group["skip"],
                "direction": group["direction"],
                "extension_type": group["extension_type"],
                "extension_side": group["extension_side"],
                "match_kind": group["match_kind"],
                "rows": group["rows"],
                "unique_extended_sequences": len(unique_sequences),
                "max_extension_length": group["max_extension_length"],
                "max_match_count": group["max_match_count"],
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            str(row["corpus"]),
            str(row["term"]),
            int_or_zero(row["skip"]),
            str(row["direction"]),
            str(row["extension_type"]),
            str(row["match_kind"]),
        ),
    )


def extension_score(row: dict[str, str], extension_length: int) -> int:
    return score_extension(
        row.get("extension_type", ""),
        extension_length,
        row.get("match_kind", ""),
        int_or_zero(row.get("match_count", "")),
    )


def extension_rank_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        int_or_zero(row.get("extension_score", "")),
        int_or_zero(row.get("extension_length", "")),
        EXTENSION_TYPE_PRIORITY.get(str(row.get("extension_type", "")), 0),
        int_or_zero(row.get("match_count", "")),
        str(row.get("corpus", "")),
        str(row.get("term", "")),
        str(row.get("extended_sequence", "")),
    )


def hit_from_row(row: dict[str, str]) -> ELSHit:
    start_offset = int(row["start_offset"])
    end_offset = int(row["end_offset"])
    center_offset = row.get("center_offset")
    if center_offset in (None, ""):
        center_offset = str((min(start_offset, end_offset) + max(start_offset, end_offset)) // 2)
    return ELSHit(
        term=row["term"],
        normalized_term=row["normalized_term"],
        skip=int(row["skip"]),
        start_offset=start_offset,
        end_offset=end_offset,
        span_letters=int(row["span_letters"]),
        sequence=row["sequence"],
        start_ref=row["start_ref"],
        end_ref=row["end_ref"],
        start_source=row["start_source"],
        end_source=row["end_source"],
        center_offset=int(center_offset),
        center_ref=row.get("center_ref", ""),
        center_source=row.get("center_source", ""),
        center_word_index=int_or_empty(row.get("center_word_index", "")),
        center_word=row.get("center_word", ""),
        center_normalized_word=row.get("center_normalized_word", ""),
    )


def hit_with_corpus_center(corpus, hit: ELSHit) -> ELSHit:
    if hit.center_ref and hit.center_word:
        return hit
    word = corpus.word_at(hit.center_offset)
    return replace(
        hit,
        center_ref=hit.center_ref or corpus.ref_at(hit.center_offset),
        center_source=hit.center_source or corpus.source_at(hit.center_offset),
        center_word_index=(
            hit.center_word_index
            if hit.center_word_index != ""
            else (word.word_index if word is not None else "")
        ),
        center_word=hit.center_word or (word.raw_word if word is not None else ""),
        center_normalized_word=(
            hit.center_normalized_word
            or (word.normalized_word if word is not None else "")
        ),
    )


def int_or_empty(value: str) -> int | str:
    value = str(value)
    if value == "":
        return ""
    return int(value)


def int_or_zero(value: object) -> int:
    if value in (None, ""):
        return 0
    return int(value)


@contextmanager
def open_hits_writer(output_path: str | None):
    if output_path:
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
            writer.writeheader()
            yield writer
        return

    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDNAMES)
    writer.writeheader()
    yield writer


def write_hits(hits, output_path: str | None) -> None:
    with open_hits_writer(output_path) as writer:
        writer.writerows(hit.as_row() for hit in hits)


def write_batch_rows(rows: list[dict[str, object]], output_path: str | Path) -> None:
    with open_dict_writer(output_path, BATCH_FIELDNAMES) as writer:
        writer.writerows(rows)
