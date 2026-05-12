#!/usr/bin/env python3
"""Build an occurrence-first index for centered and relevant-center ELS rows."""

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
from els.normalization import normalize_english, normalize_greek, normalize_hebrew
from els.term_display import display_term


DEFAULT_ALL_CODES_REVIEW = Path("reports/all_codes_followup_review/review_summary.csv")
DEFAULT_ALL_CODES_SELECTED = Path("reports/all_codes_followup_selection/selected_rows.csv")
DEFAULT_ALL_CODES_CONTEXT = Path("reports/all_codes_followup_context/context_excerpts.csv")
DEFAULT_STRONG_QUEUE = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_review_queue.csv")
DEFAULT_STRONG_BUNDLE = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_review_bundle.csv")
DEFAULT_ORIGINAL_FINDINGS = Path(
    "reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_findings.csv"
)
DEFAULT_GOG_SOURCE_REVIEW = Path("reports/dynamic_skip_focus/gog_promoted_exact_center_source_review.csv")
DEFAULT_GOG_CONTROL_REVIEW = Path("reports/dynamic_skip_focus/gog_length3_surface_control_review.csv")
DEFAULT_APOCRYPHA_BRIDGE_CONTEXT = Path("reports/apocrypha_bridge_context/context.csv")
DEFAULT_KJV_APOCRYPHA_BRIDGE_CONTEXT = Path("reports/kjv_apocrypha_bridge_context/context.csv")
DEFAULT_OUT = Path("reports/centered_occurrence_index/centered_occurrences.csv")
DEFAULT_SUMMARY_OUT = Path("reports/centered_occurrence_index/presence_summary.csv")
DEFAULT_MARKDOWN = Path("docs/CENTERED_OCCURRENCE_INDEX.md")
DEFAULT_MANIFEST = Path("reports/centered_occurrence_index/manifest.json")

FIELDNAMES = [
    "occurrence_rank",
    "source_family",
    "occurrence_type",
    "corpus_class",
    "corpus",
    "source_queue",
    "presence_scope",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_word",
    "center_normalized_word",
    "offset_triplets",
    "letter_path",
    "skip",
    "direction",
    "path_rows",
    "exact_center_paths",
    "present_corpora",
    "frequency_read",
    "context_read",
    "control_read",
    "review_note",
    "context_excerpt",
    "source_record",
]

SUMMARY_FIELDNAMES = [
    "summary_rank",
    "occurrence_type",
    "source_family",
    "corpus_class",
    "concept",
    "normalized_term",
    "center_ref",
    "center_word",
    "center_normalized_word",
    "corpora",
    "source_queues",
    "occurrence_rows",
    "total_paths",
    "max_paths",
    "frequency_reads",
    "control_reads",
    "context_excerpt",
]

TYPE_ORDER = {
    "centered_self_exact_word": 0,
    "centered_self_surface_form": 1,
    "relevant_center_same_concept": 2,
    "relevant_center_same_category": 3,
    "center_verse_relevant": 4,
    "span_relevant": 5,
    "hidden_path_only": 6,
}

SOURCE_ORDER = {
    "gog_source_review": 0,
    "original_language_findings": 1,
    "strong_full_span_exact_center": 2,
    "all_codes_followup": 3,
    "apocrypha_bridge_context": 4,
    "kjv_apocrypha_bridge_context": 5,
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = build_occurrences(args)
    summary_rows = build_presence_summary(rows)
    write_csv(args.out, rows)
    write_csv(args.summary_out, summary_rows, fieldnames=SUMMARY_FIELDNAMES)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-codes-review", type=Path, default=DEFAULT_ALL_CODES_REVIEW)
    parser.add_argument("--all-codes-selected", type=Path, default=DEFAULT_ALL_CODES_SELECTED)
    parser.add_argument("--all-codes-context", type=Path, default=DEFAULT_ALL_CODES_CONTEXT)
    parser.add_argument("--strong-queue", type=Path, default=DEFAULT_STRONG_QUEUE)
    parser.add_argument("--strong-bundle", type=Path, default=DEFAULT_STRONG_BUNDLE)
    parser.add_argument("--original-findings", type=Path, default=DEFAULT_ORIGINAL_FINDINGS)
    parser.add_argument("--gog-source-review", type=Path, default=DEFAULT_GOG_SOURCE_REVIEW)
    parser.add_argument("--gog-control-review", type=Path, default=DEFAULT_GOG_CONTROL_REVIEW)
    parser.add_argument("--apocrypha-bridge-context", type=Path, default=DEFAULT_APOCRYPHA_BRIDGE_CONTEXT)
    parser.add_argument(
        "--kjv-apocrypha-bridge-context",
        type=Path,
        default=DEFAULT_KJV_APOCRYPHA_BRIDGE_CONTEXT,
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def build_occurrences(args: argparse.Namespace) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    gog_frequency_read = gog_control_read(args.gog_control_review)
    rows.extend(
        all_codes_occurrences(
            read_rows_if_exists(args.all_codes_review),
            read_rows_if_exists(args.all_codes_context),
            read_rows_if_exists(args.all_codes_selected),
        )
    )
    rows.extend(
        strong_full_span_occurrences(
            read_rows_if_exists(args.strong_queue),
            read_rows_if_exists(args.strong_bundle),
        )
    )
    rows.extend(original_language_occurrences(read_rows_if_exists(args.original_findings)))
    rows.extend(gog_source_occurrences(read_rows_if_exists(args.gog_source_review), gog_frequency_read))
    rows.extend(
        apocrypha_bridge_occurrences(
            read_rows_if_exists(args.apocrypha_bridge_context),
            source_family="apocrypha_bridge_context",
        )
    )
    rows.extend(
        apocrypha_bridge_occurrences(
            read_rows_if_exists(args.kjv_apocrypha_bridge_context),
            source_family="kjv_apocrypha_bridge_context",
        )
    )
    rows = sorted(rows, key=occurrence_sort_key)
    for index, row in enumerate(rows, start=1):
        row["occurrence_rank"] = index
    return rows


def build_presence_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str, str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[presence_key(row)].append(row)
    summary_rows = [presence_summary_row(value) for value in grouped.values()]
    summary_rows = sorted(summary_rows, key=presence_sort_key)
    for index, row in enumerate(summary_rows, start=1):
        row["summary_rank"] = index
    return summary_rows


def presence_key(row: dict[str, object]) -> tuple[str, str, str, str, str, str]:
    return (
        str(row.get("occurrence_type", "")),
        str(row.get("source_family", "")),
        str(row.get("corpus_class", "")),
        str(row.get("normalized_term", "")),
        center_ref_base(row.get("center_ref", "")),
        normalize_value(str(row.get("center_normalized_word") or row.get("center_word", ""))),
    )


def presence_summary_row(rows: list[dict[str, object]]) -> dict[str, object]:
    first = rows[0]
    path_values = [int_or_zero(row.get("exact_center_paths") or row.get("path_rows")) for row in rows]
    return {
        "summary_rank": "",
        "occurrence_type": first.get("occurrence_type", ""),
        "source_family": first.get("source_family", ""),
        "corpus_class": first.get("corpus_class", ""),
        "concept": first.get("concept", ""),
        "normalized_term": first.get("normalized_term", ""),
        "center_ref": center_ref_base(first.get("center_ref", "")),
        "center_word": first.get("center_word", ""),
        "center_normalized_word": first.get("center_normalized_word", ""),
        "corpora": join_unique(row.get("corpus", "") for row in rows),
        "source_queues": join_unique(row.get("source_queue", "") for row in rows),
        "occurrence_rows": len(rows),
        "total_paths": sum(path_values),
        "max_paths": max(path_values, default=0),
        "frequency_reads": join_unique(row.get("frequency_read", "") for row in rows),
        "control_reads": join_unique(row.get("control_read", "") for row in rows),
        "context_excerpt": first_nonempty(row.get("context_excerpt", "") for row in rows),
    }


def presence_sort_key(row: dict[str, object]) -> tuple[int, int, int, str, str, str]:
    return (
        TYPE_ORDER.get(str(row["occurrence_type"]), 99),
        0 if row.get("corpus_class") == "bible" else 1,
        SOURCE_ORDER.get(str(row["source_family"]), 99),
        str(row.get("normalized_term", "")),
        str(row.get("center_ref", "")),
        str(row.get("corpora", "")),
    )


def all_codes_occurrences(
    review_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
    selected_rows: list[dict[str, str]] | None = None,
) -> list[dict[str, object]]:
    context_by_rank = context_examples_by_rank(context_rows)
    selected_by_rank = {row.get("selection_rank", ""): row for row in selected_rows or []}
    rows = []
    for row in review_rows:
        if row.get("bucket") not in {
            "center_word_exact",
            "center_word_same_concept",
            "center_word_same_category",
            "center_verse_exact",
            "center_verse_same_concept",
            "center_verse_same_category",
            "span_exact",
            "span_same_concept",
            "span_same_category",
        }:
            continue
        context = context_by_rank.get(row.get("selection_rank", ""), {})
        selected = selected_by_rank.get(row.get("selection_rank", ""), {})
        rows.append(
            base_row(
                source_family="all_codes_followup",
                occurrence_type=classify_occurrence(row),
                corpus_class="bible",
                corpus="",
                source_queue=row.get("source_queue", ""),
                presence_scope=row.get("presence_scope", ""),
                term_id=row.get("term_id", ""),
                concept=row.get("concept", ""),
                category=row.get("category", ""),
                normalized_term=row.get("normalized_term", ""),
                start_ref=selected.get("start_ref", ""),
                center_ref=row.get("center_ref", ""),
                end_ref=selected.get("end_ref", ""),
                center_word=row.get("center_word", ""),
                center_normalized_word=row.get("center_normalized_word", ""),
                offset_triplets=selected.get("offsets_by_corpus", ""),
                skip=row.get("skip", ""),
                direction=row.get("direction", ""),
                path_rows=row.get("path_rows", ""),
                exact_center_paths="",
                present_corpora=row.get("path_corpora", ""),
                frequency_read=frequency_read(row),
                context_read=row.get("best_context", ""),
                control_read=row.get("control_read", ""),
                review_note=row.get("review_note", ""),
                context_excerpt=context.get("center_verse_text", ""),
                source_record=f"all_codes_review:{row.get('selection_rank', '')}",
            )
        )
    return rows


def strong_full_span_occurrences(
    queue_rows: list[dict[str, str]],
    bundle_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    bundle_by_key = {strong_key(row): row for row in bundle_rows}
    rows = []
    for row in queue_rows:
        bundle = bundle_by_key.get(strong_key(row), {})
        rows.append(
            base_row(
                source_family="strong_full_span_exact_center",
                occurrence_type=classify_occurrence(row),
                corpus_class=row.get("corpus_class", ""),
                corpus=row.get("corpus", ""),
                source_queue="dynamic_skip_focus",
                presence_scope="",
                term_id=row.get("term_id", ""),
                concept="",
                category="",
                normalized_term=row.get("normalized_term", ""),
                start_ref=row.get("example_start_ref", ""),
                center_ref=row.get("center_ref", ""),
                end_ref=row.get("example_end_ref", ""),
                center_word=row.get("center_word", ""),
                center_normalized_word=row.get("center_normalized_word", ""),
                offset_triplets=offset_triplet(row.get("corpus", ""), row),
                skip=row.get("example_skip", ""),
                direction=row.get("example_direction", ""),
                path_rows=row.get("source_paths", ""),
                exact_center_paths=row.get("exact_center_paths", ""),
                present_corpora=row.get("corpus", ""),
                frequency_read=row.get("review_bucket", ""),
                context_read=bundle.get("priority", ""),
                control_read="control row" if row.get("corpus_class") == "control" else "",
                review_note=extension_note(bundle),
                context_excerpt=bundle.get("center_word_context", ""),
                source_record=f"strong_queue:{row.get('rank', '')}",
            )
        )
    return rows


def original_language_occurrences(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    output = []
    for row in rows:
        output.append(
            base_row(
                source_family="original_language_findings",
                occurrence_type=classify_occurrence(row),
                corpus_class="bible",
                corpus=row.get("corpus", ""),
                source_queue="dynamic_skip_focus_original_language",
                presence_scope="",
                term_id=row.get("term_id", ""),
                concept="",
                category="",
                normalized_term=row.get("normalized_term", ""),
                start_ref=row.get("example_start_ref", ""),
                center_ref=row.get("center_ref", ""),
                end_ref=row.get("example_end_ref", ""),
                center_word=row.get("center_word", ""),
                center_normalized_word=row.get("center_word", ""),
                skip=row.get("example_skip", ""),
                direction=row.get("example_direction", ""),
                path_rows=row.get("path_rows_joined", ""),
                exact_center_paths=row.get("exact_center_paths", ""),
                present_corpora=row.get("corpus", ""),
                frequency_read=row.get("recommendation", ""),
                context_read=row.get("surface_read", ""),
                control_read=row.get("control_read", ""),
                review_note=row.get("manual_review_note", ""),
                context_excerpt=row.get("center_word_context", ""),
                source_record=f"original_findings:{row.get('finding_rank', '')}",
            )
        )
    return output


def gog_source_occurrences(rows: list[dict[str, str]], frequency_read_value: str) -> list[dict[str, object]]:
    output = []
    for row in rows:
        if int_or_zero(row.get("exact_center_paths")) <= 0:
            continue
        output.append(
            base_row(
                source_family="gog_source_review",
                occurrence_type="centered_self_exact_word",
                corpus_class="bible",
                corpus=row.get("corpus", ""),
                source_queue="gog_source_review",
                presence_scope="source_comparison",
                term_id="dyn_gog_g",
                concept="Gog",
                category="apocalyptic",
                normalized_term=row.get("normalized_term", "γωγ"),
                start_ref="",
                center_ref=row.get("center_refs", ""),
                end_ref="",
                center_word="Gog",
                center_normalized_word=row.get("normalized_term", "γωγ"),
                skip=row.get("skip_values", ""),
                direction="both",
                path_rows="",
                exact_center_paths=row.get("exact_center_paths", ""),
                present_corpora=row.get("corpus", ""),
                frequency_read=frequency_read_value,
                context_read="hidden Gog centers on open Gog in Rev 20:8",
                control_read=row.get("read", ""),
                review_note="source-stable centered-self occurrence; frequency strength reported separately",
                context_excerpt="Rev 20:8 Gog/Magog context",
                source_record=f"gog_source_review:{row.get('corpus', '')}",
            )
        )
    return output


def apocrypha_bridge_occurrences(
    rows: list[dict[str, str]],
    *,
    source_family: str,
) -> list[dict[str, object]]:
    output = []
    for row in rows:
        if row.get("context_bucket") == "hidden_path_only":
            continue
        output.append(
            base_row(
                source_family=source_family,
                occurrence_type=classify_occurrence(row),
                corpus_class="bible",
                corpus=row.get("corpus", ""),
                source_queue="apocrypha_bridge",
                presence_scope=row.get("bridge_type", ""),
                term_id=row.get("term_ids", ""),
                concept=row.get("concepts", ""),
                category=row.get("categories", ""),
                normalized_term=row.get("normalized_term", ""),
                start_ref=row.get("start_ref", ""),
                center_ref=row.get("center_ref", ""),
                end_ref=row.get("end_ref", ""),
                center_word=row.get("center_word", ""),
                center_normalized_word=row.get("center_normalized_word", ""),
                letter_path=row.get("letter_path", ""),
                skip=row.get("skip", ""),
                direction=row.get("direction", ""),
                path_rows="1",
                exact_center_paths="",
                present_corpora=row.get("corpus", ""),
                frequency_read="bridge candidate; frequency read in bridge controls",
                context_read=row.get("context_bucket", ""),
                control_read="bridge controls available separately",
                review_note="apocrypha bridge candidate with surface context bucket",
                context_excerpt=row.get("center_verse_text", ""),
                source_record=f"{source_family}:{row.get('context_rank', '')}",
            )
        )
    return output


def classify_occurrence(row: dict[str, str]) -> str:
    bucket = row.get("bucket") or row.get("context_bucket", "")
    review_class = row.get("review_class", "")
    normalized_term = normalize_value(row.get("normalized_term", ""))
    center_normalized = normalize_value(row.get("center_normalized_word") or row.get("center_word", ""))
    if normalized_term and center_normalized == normalized_term:
        return "centered_self_exact_word"
    if bucket == "center_word_exact" or review_class == "same_surface_word_at_center":
        return "centered_self_surface_form"
    if bucket == "center_word_same_concept" or "same_concept" in review_class:
        return "relevant_center_same_concept"
    if bucket == "center_word_same_category" or "same_category" in review_class:
        return "relevant_center_same_category"
    if bucket.startswith("center_verse_"):
        return "center_verse_relevant"
    if bucket.startswith("span_"):
        return "span_relevant"
    if row.get("center_normalized_word"):
        return "centered_self_surface_form"
    return "hidden_path_only"


def base_row(**values: object) -> dict[str, object]:
    row = {field: "" for field in FIELDNAMES}
    row.update(values)
    return row


def context_examples_by_rank(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("selection_rank", "")].append(row)
    return {rank: values[0] for rank, values in grouped.items() if rank}


def gog_control_read(path: Path) -> str:
    for row in read_rows_if_exists(path):
        if row.get("is_target") == "True":
            return (
                "length-3 matched-control rank "
                f"desc {row.get('rank_desc', '')}/asc {row.get('rank_asc', '')}; "
                f"controls above target {row.get('controls_gt_target', '')}; "
                "not frequency-promoted"
            )
    return ""


def frequency_read(row: dict[str, str]) -> str:
    parts = []
    if row.get("control_q"):
        parts.append(f"control q={row['control_q']}")
    if row.get("control_p"):
        parts.append(f"control p={row['control_p']}")
    if row.get("control_band"):
        parts.append(f"control band={row['control_band']}")
    return "; ".join(parts)


def extension_note(row: dict[str, str]) -> str:
    if int_or_zero(row.get("strong_extension_rows")) > 0:
        return f"strong same-skip extension: {row.get('best_extension', '')}"
    return ""


def strong_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("corpus", ""),
        row.get("normalized_term", ""),
        row.get("center_ref", ""),
        row.get("center_word_index", ""),
    )


def offset_triplet(corpus: str, row: dict[str, str]) -> str:
    start = row.get("example_start_offset", "")
    center = row.get("example_center_offset", "")
    end = row.get("example_end_offset", "")
    if not corpus or not start or not center or not end:
        return ""
    return f"{corpus}:{start}/{center}/{end}"


def occurrence_sort_key(row: dict[str, object]) -> tuple[int, int, int, int, str, str, str]:
    return (
        TYPE_ORDER.get(str(row["occurrence_type"]), 99),
        0 if row.get("corpus_class") == "bible" else 1,
        SOURCE_ORDER.get(str(row["source_family"]), 99),
        -int_or_zero(row.get("exact_center_paths") or row.get("path_rows")),
        str(row.get("normalized_term", "")),
        str(row.get("corpus", "")),
        str(row.get("center_ref", "")),
    )


def write_csv(path: Path, rows: list[dict[str, object]], *, fieldnames: list[str] = FIELDNAMES) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    source_counts = Counter(str(row["source_family"]) for row in rows)
    type_counts = Counter(str(row["occurrence_type"]) for row in rows)
    class_counts = Counter(str(row["corpus_class"]) for row in rows)
    summary_type_counts = Counter(str(row["occurrence_type"]) for row in summary_rows)
    summary_class_counts = Counter(str(row["corpus_class"]) for row in summary_rows)
    summary_source_counts = Counter(str(row["source_family"]) for row in summary_rows)
    lines = [
        "# Centered Occurrence Index",
        "",
        "This is an occurrence-first index. It lists hidden ELS rows where the",
        "center lands on the same surface word, an inflected/containing surface",
        "form, or a related center word/context. Frequency and control reads are",
        "carried alongside the occurrence; they do not remove real occurrences",
        "from review.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Bottom Line",
        "",
        f"- indexed occurrence rows: {len(rows):,}",
        f"- unique term-center presence rows: {len(summary_rows):,}",
        f"- Bible occurrence rows: {class_counts['bible']:,}",
        f"- Bible presence rows: {summary_class_counts['bible']:,}",
        f"- control occurrence rows: {class_counts['control']:,}",
        f"- control presence rows: {summary_class_counts['control']:,}",
        "- frequency controls are interpretation context, not deletion criteria.",
        "",
        "## Occurrence Types",
        "",
        "| Type | Presence rows | Occurrence rows |",
        "| --- | ---: | ---: |",
    ]
    for label, _order in sorted(TYPE_ORDER.items(), key=lambda item: item[1]):
        if type_counts[label]:
            lines.append(f"| `{label}` | {summary_type_counts[label]:,} | {type_counts[label]:,} |")
    lines.extend(["", "## Source Families", "", "| Source family | Presence rows | Occurrence rows |", "| --- | ---: | ---: |"])
    for label, count in sorted(source_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{label}` | {summary_source_counts[label]:,} | {count:,} |")
    lines.extend(
        [
            "",
            "## Top Presence Rows",
            "",
            "| Rank | Type | Source | Corpora | Term | Center | Occurrence rows | Total paths | Frequency read | Context |",
            "| ---: | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in summary_rows[: args.markdown_row_limit]:
        lines.append(summary_markdown_row(row))
    if len(summary_rows) > args.markdown_row_limit:
        lines.append(
            f"| ... | ... | ... | ... | ... | ... | ... | ... | ... | {len(summary_rows) - args.markdown_row_limit:,} more rows in CSV |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Presence rows are grouped by term, center reference, source family, and center surface form.",
            "- `centered_self_exact_word` is the strongest occurrence stratum.",
            "- `centered_self_surface_form` includes inflected or containing surface forms and should be manually checked.",
            "- Relevant-center rows are retained because they answer a different question than raw frequency.",
            "- Control rows are kept in the CSV so Bible occurrences can be read against a visible baseline.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summary_markdown_row(row: dict[str, object]) -> str:
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    return (
        f"| {row['summary_rank']} | `{row['occurrence_type']}` | `{row['source_family']}` | "
        f"{row.get('corpora', '')} | "
        f"{display_term(str(row.get('normalized_term', '')), english=str(row.get('concept', '')))} | "
        f"{md_cell(center)} | "
        f"{int_or_zero(row.get('occurrence_rows')):,} | {int_or_zero(row.get('total_paths')):,} | "
        f"{md_cell(truncate(str(row.get('frequency_reads', '')), 70))} | "
        f"{md_cell(truncate(str(row.get('context_excerpt', '')), 100))} |"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_centered_occurrence_index.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "rows": len(rows),
        "summary_rows": len(summary_rows),
        "type_counts": dict(Counter(str(row["occurrence_type"]) for row in rows)),
        "summary_type_counts": dict(Counter(str(row["occurrence_type"]) for row in summary_rows)),
        "source_counts": dict(Counter(str(row["source_family"]) for row in rows)),
        "summary_source_counts": dict(Counter(str(row["source_family"]) for row in summary_rows)),
        "inputs": {
            "all_codes_review": str(args.all_codes_review),
            "all_codes_selected": str(args.all_codes_selected),
            "all_codes_context": str(args.all_codes_context),
            "strong_queue": str(args.strong_queue),
            "strong_bundle": str(args.strong_bundle),
            "original_findings": str(args.original_findings),
            "gog_source_review": str(args.gog_source_review),
            "gog_control_review": str(args.gog_control_review),
            "apocrypha_bridge_context": str(args.apocrypha_bridge_context),
            "kjv_apocrypha_bridge_context": str(args.kjv_apocrypha_bridge_context),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reproduce_command(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_centered_occurrence_index "
        f"--all-codes-review {args.all_codes_review} "
        f"--all-codes-selected {args.all_codes_selected} "
        f"--all-codes-context {args.all_codes_context} "
        f"--strong-queue {args.strong_queue} "
        f"--strong-bundle {args.strong_bundle} "
        f"--original-findings {args.original_findings} "
        f"--gog-source-review {args.gog_source_review} "
        f"--gog-control-review {args.gog_control_review} "
        f"--apocrypha-bridge-context {args.apocrypha_bridge_context} "
        f"--kjv-apocrypha-bridge-context {args.kjv_apocrypha_bridge_context} "
        f"--out {args.out} "
        f"--summary-out {args.summary_out} "
        f"--markdown-out {args.markdown_out} "
        f"--manifest-out {args.manifest_out}"
    )


def read_rows_if_exists(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def int_or_zero(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def normalize_value(value: str) -> str:
    value = value.strip()
    if any("\u0590" <= char <= "\u05ff" for char in value):
        return normalize_hebrew(value)
    if any(("\u0370" <= char <= "\u03ff") or ("\u1f00" <= char <= "\u1fff") for char in value):
        return normalize_greek(value)
    return normalize_english(value)


def center_ref_base(value: object) -> str:
    return str(value).split("=", 1)[0].strip().upper()


def join_unique(values: Any) -> str:
    seen = []
    for value in values:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.append(text)
    return ";".join(seen)


def first_nonempty(values: Any) -> str:
    for value in values:
        text = str(value).strip()
        if text:
            return text
    return ""


def md_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def truncate(value: str, limit: int) -> str:
    value = " ".join(str(value).split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
