#!/usr/bin/env python3
"""Audit same-skip before/after extensions for selected all-codes paths."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import Corpus, load_corpus
from els.extensions import (
    ALL_CODES_EXTENSION_TYPE_PRIORITY,
    ExtensionLexicon,
    build_extension_lexicon,
    extension_score as score_extension,
    extensions_for_hit,
)
from els.search import ELSHit
from scripts.analyze_all_codes_letter_paths import DEFAULT_CORPORA, parse_corpus_args


PATH_SUMMARY_IN = Path("reports/all_codes_followup_letter_paths/path_summary.csv")
OUT_DIR = Path("reports/all_codes_followup_extensions")
EXTENSIONS_OUT = OUT_DIR / "extensions.csv"
COMPOUND_OUT = OUT_DIR / "compound_extensions.csv"
SUMMARY_OUT = OUT_DIR / "summary.csv"
MD_OUT = Path("docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"

EXTENSION_FIELDNAMES = [
    "selection_rank",
    "source_queue",
    "bucket",
    "presence_scope",
    "term_id",
    "concept",
    "category",
    "audit_corpus",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "center_ref",
    "center_word",
    "center_normalized_word",
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
    "extension_score",
]

SUMMARY_FIELDNAMES = [
    "selection_rank",
    "source_queue",
    "bucket",
    "presence_scope",
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "center_ref",
    "center_word",
    "center_normalized_word",
    "corpus_count",
    "path_rows",
    "extension_rows",
    "unique_extended_sequences",
    "max_extension_length",
    "best_audit_corpus",
    "best_extension_type",
    "best_extended_sequence",
    "best_match_kind",
    "best_match_count",
    "best_matched_examples",
    "best_matched_refs",
    "best_extension_score",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    path_rows = read_rows(args.path_summary)
    configs = parse_corpus_args(args.corpus)
    corpora = {label: load_corpus(config) for label, config in configs.items()}
    lexicons = {
        label: build_extension_lexicon(corpus, max_phrase_words=args.phrase_words)
        for label, corpus in corpora.items()
    }
    extension_rows = build_extension_rows(path_rows, corpora, lexicons, args)
    summary_rows = build_summary_rows(path_rows, extension_rows)
    write_rows(args.extensions_out, EXTENSION_FIELDNAMES, extension_rows)
    compound_rows = [row for row in extension_rows if is_compound_extension(row)]
    write_rows(args.compound_out, EXTENSION_FIELDNAMES, compound_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, path_rows, extension_rows, summary_rows, args)
    write_manifest(args, path_rows, extension_rows, summary_rows, started)
    print(args.extensions_out)
    print(args.compound_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path-summary", type=Path, default=PATH_SUMMARY_IN)
    parser.add_argument("--corpus", action="append", default=list(DEFAULT_CORPORA))
    parser.add_argument("--max-before", type=int, default=12)
    parser.add_argument("--max-after", type=int, default=12)
    parser.add_argument("--phrase-words", type=int, default=4)
    parser.add_argument("--include-both-sided", action="store_true")
    parser.add_argument("--max-extensions-per-path", type=int, default=20)
    parser.add_argument("--markdown-row-limit", type=int, default=100)
    parser.add_argument("--extensions-out", type=Path, default=EXTENSIONS_OUT)
    parser.add_argument("--compound-out", type=Path, default=COMPOUND_OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def build_extension_rows(
    path_rows: list[dict[str, str]],
    corpora: dict[str, Corpus],
    lexicons: dict[str, ExtensionLexicon],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in path_rows:
        corpus_label = row["audit_corpus"]
        if corpus_label not in corpora:
            raise KeyError(f"missing configured corpus {corpus_label!r}")
        corpus = corpora[corpus_label]
        hit = hit_from_path_row(corpus, row)
        extensions = extensions_for_hit(
            corpus,
            hit,
            lexicons[corpus_label],
            max_before=args.max_before,
            max_after=args.max_after,
            include_both_sided=args.include_both_sided,
            max_extensions=None,
        )
        ranked = sorted(
            (extension_row(row, extension) for extension in extensions),
            key=extension_rank_key,
            reverse=True,
        )
        if args.max_extensions_per_path > 0:
            ranked = ranked[: args.max_extensions_per_path]
        rows.extend(ranked)
    return rows


def hit_from_path_row(corpus: Corpus, row: dict[str, str]) -> ELSHit:
    start = int(row["audit_start_offset"])
    center = int(row["audit_center_offset"])
    end = int(row["audit_end_offset"])
    center_word = corpus.word_at(center)
    return ELSHit(
        term=row.get("term", ""),
        normalized_term=row["normalized_term"],
        skip=int(row["skip"]),
        start_offset=start,
        end_offset=end,
        span_letters=int_or_default(row.get("span_letters", ""), abs(end - start) + 1),
        sequence=row["sequence"],
        start_ref=row["audit_start_ref"],
        end_ref=row["audit_end_ref"],
        start_source=corpus.source_at(start),
        end_source=corpus.source_at(end),
        center_offset=center,
        center_ref=row["audit_center_ref"],
        center_source=corpus.source_at(center),
        center_word_index=center_word.word_index if center_word is not None else "",
        center_word=row.get("audit_center_word", ""),
        center_normalized_word=row.get("audit_center_normalized_word", ""),
    )


def extension_row(row: dict[str, str], extension: Any) -> dict[str, str]:
    extension_length = int(extension.extension_length)
    output = {
        "selection_rank": row.get("selection_rank", ""),
        "source_queue": row.get("source_queue", ""),
        "bucket": row.get("bucket", ""),
        "presence_scope": row.get("presence_scope", ""),
        "term_id": row.get("term_id", ""),
        "concept": row.get("concept", ""),
        "category": row.get("category", ""),
        "audit_corpus": row.get("audit_corpus", ""),
        "term": row.get("term", ""),
        "normalized_term": row.get("normalized_term", ""),
        "skip": row.get("skip", ""),
        "direction": row.get("direction", ""),
        "center_ref": row.get("audit_center_ref", ""),
        "center_word": row.get("audit_center_word", ""),
        "center_normalized_word": row.get("audit_center_normalized_word", ""),
        "extension_type": extension.extension_type,
        "extension_side": extension.extension_side,
        "extension_length": str(extension_length),
        "before_letters": extension.before_letters,
        "after_letters": extension.after_letters,
        "extended_sequence": extension.extended_sequence,
        "matched_normalized": extension.matched_normalized,
        "match_kind": extension.match_kind,
        "match_count": str(extension.match_count),
        "matched_examples": extension.matched_examples,
        "matched_refs": extension.matched_refs,
        "extension_start_offset": str(extension.extension_start_offset),
        "extension_end_offset": str(extension.extension_end_offset),
        "extension_start_ref": extension.extension_start_ref,
        "extension_end_ref": extension.extension_end_ref,
    }
    output["extension_score"] = str(extension_score(output, extension_length))
    return output


def build_summary_rows(
    path_rows: list[dict[str, str]],
    extension_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    paths_by_rank = group_by(path_rows, "selection_rank")
    extensions_by_rank = group_by(extension_rows, "selection_rank")
    rows: list[dict[str, str]] = []
    for rank in sorted(paths_by_rank, key=int_sort_key):
        paths = paths_by_rank[rank]
        extensions = sorted(
            extensions_by_rank.get(rank, []),
            key=extension_rank_key,
            reverse=True,
        )
        first = paths[0]
        best = extensions[0] if extensions else {}
        rows.append(
            {
                "selection_rank": first.get("selection_rank", ""),
                "source_queue": first.get("source_queue", ""),
                "bucket": first.get("bucket", ""),
                "presence_scope": first.get("presence_scope", ""),
                "term_id": first.get("term_id", ""),
                "concept": first.get("concept", ""),
                "category": first.get("category", ""),
                "term": first.get("term", ""),
                "normalized_term": first.get("normalized_term", ""),
                "skip": first.get("skip", ""),
                "direction": first.get("direction", ""),
                "center_ref": first.get("center_ref", ""),
                "center_word": first.get("center_word", ""),
                "center_normalized_word": first.get("center_normalized_word", ""),
                "corpus_count": str(len({row["audit_corpus"] for row in paths})),
                "path_rows": str(len(paths)),
                "extension_rows": str(len(extensions)),
                "unique_extended_sequences": str(
                    len({row["extended_sequence"] for row in extensions})
                ),
                "max_extension_length": str(
                    max((int_value(row["extension_length"]) for row in extensions), default=0)
                ),
                "best_audit_corpus": best.get("audit_corpus", ""),
                "best_extension_type": best.get("extension_type", ""),
                "best_extended_sequence": best.get("extended_sequence", ""),
                "best_match_kind": best.get("match_kind", ""),
                "best_match_count": best.get("match_count", ""),
                "best_matched_examples": best.get("matched_examples", ""),
                "best_matched_refs": best.get("matched_refs", ""),
                "best_extension_score": best.get("extension_score", ""),
            }
        )
    return rows


def write_markdown(
    path: Path,
    path_rows: list[dict[str, str]],
    extension_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    by_corpus = Counter(row["audit_corpus"] for row in extension_rows)
    by_type = Counter(row["extension_type"] for row in extension_rows)
    compound_rows = [row for row in extension_rows if is_compound_extension(row)]
    compound_ranks = {row["selection_rank"] for row in compound_rows}
    rows_with_extensions = [
        row for row in summary_rows if int_value(row["extension_rows"]) > 0
    ]
    max_extension_length = max(
        (int_value(row["extension_length"]) for row in extension_rows),
        default=0,
    )
    rows_to_show = sorted(
        rows_with_extensions,
        key=lambda row: (
            int_value(row["best_extension_score"]),
            int_value(row["max_extension_length"]),
            row["normalized_term"],
        ),
        reverse=True,
    )[: args.markdown_row_limit]
    lines = [
        "# All-Codes Follow-Up Extensions",
        "",
        "Status: same-skip extension audit, not a claim or statistical test.",
        "",
        "This report checks whether the hidden ELS path can be extended before,",
        "after, or on both sides at the same skip interval into a surface-attested",
        "word or phrase in that corpus. Hidden-path-only rows are retained; a",
        "same-skip extension is an added review feature, not a requirement.",
        "",
        "## Inputs",
        "",
        f"- Path summary: `{args.path_summary}`",
        f"- Compound extension CSV: `{args.compound_out}`",
        f"- Max before letters: {args.max_before}",
        f"- Max after letters: {args.max_after}",
        f"- Max surface phrase words in lexicon: {args.phrase_words}",
        f"- Both-sided extensions: {args.include_both_sided}",
        "",
        "## Counts",
        "",
        f"- path rows checked: {len(path_rows):,}",
        f"- selected rows checked: {len(summary_rows):,}",
        f"- selected rows with extensions: {len(rows_with_extensions):,}",
        f"- extension rows: {len(extension_rows):,}",
        f"- selected rows with compound extensions: {len(compound_ranks):,}",
        f"- compound extension rows containing hidden term: {len(compound_rows):,}",
        f"- max extension length: {max_extension_length:,}",
        f"- extension rows by corpus: `{dict(sorted(by_corpus.items()))}`",
        f"- extension rows by type: `{dict(sorted(by_type.items()))}`",
        "",
        "## Best Extensions By Selected Row",
        "",
        "| Rank | Queue | Bucket | Term | Corpus | Type | Extended sequence | Kind | Count | Examples |",
        "| ---: | --- | --- | --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for row in rows_to_show:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["selection_rank"],
                    row["source_queue"],
                    f"`{row['bucket']}`",
                    f"`{row['normalized_term']}`",
                    row["best_audit_corpus"],
                    f"`{row['best_extension_type']}`",
                    f"`{row['best_extended_sequence']}`",
                    f"`{row['best_match_kind']}`",
                    row["best_match_count"],
                    md_cell(truncate(row["best_matched_examples"], 80)),
                ]
            )
            + " |"
        )
    if len(rows_with_extensions) > len(rows_to_show):
        lines.append(
            f"| ... | ... | ... | ... | ... | ... | ... | ... | ... | "
            f"{len(rows_with_extensions) - len(rows_to_show):,} more rows in CSV |"
        )
    lines.extend(
        [
            "",
            "## Compound Extension Rows",
            "",
            "| Rank | Corpus | Term | Type | Extended sequence | Kind | Count | Refs |",
            "| ---: | --- | --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in sorted(compound_rows, key=extension_rank_key, reverse=True)[
        : args.markdown_row_limit
    ]:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["selection_rank"],
                    row["audit_corpus"],
                    f"`{row['normalized_term']}`",
                    f"`{row['extension_type']}`",
                    f"`{row['extended_sequence']}`",
                    f"`{row['match_kind']}`",
                    row["match_count"],
                    md_cell(truncate(row["matched_refs"], 80)),
                ]
            )
            + " |"
        )
    if len(compound_rows) > args.markdown_row_limit:
        lines.append(
            f"| ... | ... | ... | ... | ... | ... | ... | "
            f"{len(compound_rows) - args.markdown_row_limit:,} more rows in CSV |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "The extension lexicon is built from normalized surface words and phrases in",
            "the same corpus. A row here means the same ELS lane can spell a larger",
            "surface-attested token somewhere in that text. It does not mean the hidden",
            "path appears openly at the center verse, and it does not replace controls.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    path_rows: list[dict[str, str]],
    extension_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    started: float,
) -> None:
    rows_with_extensions = sum(int_value(row["extension_rows"]) > 0 for row in summary_rows)
    compound_rows = sum(is_compound_extension(row) for row in extension_rows)
    compound_ranks = {
        row["selection_rank"] for row in extension_rows if is_compound_extension(row)
    }
    payload = {
        "tool": "analyze_all_codes_extensions",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "path_summary": str(args.path_summary),
        "path_rows": len(path_rows),
        "selected_rows": len(summary_rows),
        "selected_rows_with_extensions": rows_with_extensions,
        "extension_rows": len(extension_rows),
        "selected_rows_with_compound_extensions": len(compound_ranks),
        "compound_extension_rows": compound_rows,
        "max_extension_length": max(
            (int_value(row["extension_length"]) for row in extension_rows),
            default=0,
        ),
        "extension_rows_by_corpus": dict(
            sorted(Counter(row["audit_corpus"] for row in extension_rows).items())
        ),
        "extension_rows_by_type": dict(
            sorted(Counter(row["extension_type"] for row in extension_rows).items())
        ),
        "outputs": [
            str(args.extensions_out),
            str(args.compound_out),
            str(args.summary_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def extension_score(row: dict[str, str], extension_length: int) -> int:
    return score_extension(
        row.get("extension_type", ""),
        extension_length,
        row.get("match_kind", ""),
        int_value(row.get("match_count", "")),
        high_priority_scale=True,
    )


def is_compound_extension(row: dict[str, str]) -> bool:
    return row.get("extension_type", "") in {
        "before_plus_term",
        "term_plus_after",
        "before_plus_term_plus_after",
    }


def extension_rank_key(row: dict[str, str]) -> tuple[int, int, int, int, str, str]:
    return (
        int_value(row.get("extension_score", "")),
        int_value(row.get("extension_length", "")),
        ALL_CODES_EXTENSION_TYPE_PRIORITY.get(row.get("extension_type", ""), 0),
        int_value(row.get("match_count", "")),
        row.get("audit_corpus", ""),
        row.get("extended_sequence", ""),
    )


def group_by(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get(field, "")].append(row)
    return grouped


def int_sort_key(value: str) -> tuple[int, str]:
    return (int_value(value), value)


def int_value(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def int_or_default(value: Any, default: int) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def truncate(value: str, limit: int) -> str:
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
