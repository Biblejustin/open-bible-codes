#!/usr/bin/env python3
"""Export letter-path audits for selected all-codes follow-up rows."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import Corpus, load_corpus
from els.term_display import display_term
from scripts.select_all_codes_followup import SELECTED_FIELDNAMES


SELECTED_IN = Path("reports/all_codes_followup_selection/selected_rows.csv")
OUT_DIR = Path("reports/all_codes_followup_letter_paths")
SUMMARY_OUT = OUT_DIR / "path_summary.csv"
LETTERS_OUT = OUT_DIR / "letter_paths.csv"
MD_OUT = Path("docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"
DEFAULT_CORPORA = (
    "MT_WLC=configs/example_oshb_wlc.toml",
    "UXLC=configs/example_uxlc.toml",
    "EBIBLE_WLC=configs/example_ebible_hebwlc.toml",
    "MAM=configs/example_mam.toml",
    "UHB=configs/example_uhb.toml",
    "TR_NT=configs/example_ebible_grctr.toml",
    "BYZ_NT=configs/example_ebible_grcmt.toml",
    "TCG_NT=configs/example_ebible_grctcgnt.toml",
    "SBLGNT=configs/example_sblgnt.toml",
)

AUDIT_FIELDNAMES = [
    "audit_corpus",
    "sequence",
    "matches_term",
    "audit_start_ref",
    "audit_center_ref",
    "audit_end_ref",
    "path_refs",
    "audit_center_word",
    "audit_center_normalized_word",
    "audit_start_offset",
    "audit_center_offset",
    "audit_end_offset",
    "path_offsets",
]
SUMMARY_FIELDNAMES = [*SELECTED_FIELDNAMES, *AUDIT_FIELDNAMES]

LETTER_FIELDNAMES = [
    "selection_rank",
    "source_queue",
    "bucket",
    "presence_scope",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "audit_corpus",
    "skip",
    "direction",
    "letter_index",
    "offset",
    "letter",
    "ref",
    "word_index",
    "word",
    "normalized_word",
]


@dataclass
class PathAudit:
    summary: dict[str, str]
    letters: tuple[dict[str, str], ...]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    selected_rows = read_rows(args.selected)
    configs = parse_corpus_args(args.corpus)
    corpora = {label: load_corpus(config) for label, config in configs.items()}
    audits = build_audits(selected_rows, corpora)
    summary_rows = [audit.summary for audit in audits]
    letter_rows = [letter for audit in audits for letter in audit.letters]
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.letters_out, LETTER_FIELDNAMES, letter_rows)
    write_markdown(args.markdown_out, selected_rows, summary_rows, letter_rows, args)
    write_manifest(args, selected_rows, summary_rows, letter_rows, started)
    print(args.summary_out)
    print(args.letters_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selected", type=Path, default=SELECTED_IN)
    parser.add_argument("--corpus", action="append", default=list(DEFAULT_CORPORA))
    parser.add_argument("--title", default="All-Codes Follow-Up Letter Paths")
    parser.add_argument(
        "--status",
        default="audit sheet for selected Hebrew and Greek all-codes follow-up rows; no claim.",
    )
    parser.add_argument("--markdown-row-limit", type=int, default=120)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--letters-out", type=Path, default=LETTERS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def parse_corpus_args(values: list[str]) -> dict[str, Path]:
    parsed: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected LABEL=CONFIG for --corpus, got {value!r}")
        label, config = value.split("=", 1)
        parsed[label] = Path(config)
    return parsed


def build_audits(
    selected_rows: list[dict[str, str]],
    corpora: dict[str, Corpus],
) -> list[PathAudit]:
    audits: list[PathAudit] = []
    for row in selected_rows:
        offsets_by_corpus = parse_offsets_by_corpus(row["offsets_by_corpus"])
        for corpus_label in split_corpora(row["present_corpora"]):
            if corpus_label not in corpora:
                raise KeyError(f"missing configured corpus {corpus_label!r}")
            if corpus_label not in offsets_by_corpus:
                raise KeyError(f"missing offsets for corpus {corpus_label!r}")
            corpus = corpora[corpus_label]
            start, center, end = offsets_by_corpus[corpus_label]
            audits.append(audit_row(row, corpus_label, corpus, start, center, end))
    return audits


def audit_row(
    row: dict[str, str],
    corpus_label: str,
    corpus: Corpus,
    start: int,
    center: int,
    end: int,
) -> PathAudit:
    skip = int(row["skip"])
    normalized_term = row["normalized_term"]
    positions = tuple(start + index * skip for index in range(len(normalized_term)))
    sequence = "".join(corpus.text[position] for position in positions)
    center_word = corpus.word_at(center)
    path_refs = unique_in_order(corpus.ref_at(position) for position in positions)
    summary = {
        **selected_metadata(row),
        "audit_corpus": corpus_label,
        "sequence": sequence,
        "matches_term": str(sequence == normalized_term),
        "audit_start_ref": corpus.ref_at(start),
        "audit_center_ref": corpus.ref_at(center),
        "audit_end_ref": corpus.ref_at(end),
        "path_refs": "; ".join(path_refs),
        "audit_center_word": center_word.raw_word if center_word is not None else "",
        "audit_center_normalized_word": (
            center_word.normalized_word if center_word is not None else ""
        ),
        "audit_start_offset": str(start),
        "audit_center_offset": str(center),
        "audit_end_offset": str(end),
        "path_offsets": "/".join(str(position) for position in positions),
    }
    letters = tuple(
        letter_row(row, corpus_label, corpus, position, index)
        for index, position in enumerate(positions, start=1)
    )
    return PathAudit(summary=summary, letters=letters)


def selected_metadata(row: dict[str, str]) -> dict[str, str]:
    return {field: row.get(field, "") for field in SELECTED_FIELDNAMES}


def letter_row(
    row: dict[str, str],
    corpus_label: str,
    corpus: Corpus,
    position: int,
    letter_index: int,
) -> dict[str, str]:
    word = corpus.word_at(position)
    return {
        "selection_rank": row.get("selection_rank", ""),
        "source_queue": row.get("source_queue", ""),
        "bucket": row.get("bucket", ""),
        "presence_scope": row.get("presence_scope", ""),
        "term_id": row.get("term_id", ""),
        "concept": row.get("concept", ""),
        "category": row.get("category", ""),
        "normalized_term": row.get("normalized_term", ""),
        "audit_corpus": corpus_label,
        "skip": row.get("skip", ""),
        "direction": row.get("direction", ""),
        "letter_index": str(letter_index),
        "offset": str(position),
        "letter": corpus.text[position],
        "ref": corpus.ref_at(position),
        "word_index": str(word.word_index) if word is not None else "",
        "word": word.raw_word if word is not None else "",
        "normalized_word": word.normalized_word if word is not None else "",
    }


def parse_offsets_by_corpus(value: str) -> dict[str, tuple[int, int, int]]:
    parsed: dict[str, tuple[int, int, int]] = {}
    for item in value.split(";"):
        item = item.strip()
        if not item:
            continue
        corpus, offsets = item.split(":", 1)
        parts = tuple(int(part) for part in offsets.split("/"))
        if len(parts) != 3:
            raise ValueError(f"expected start/center/end offsets, got {item!r}")
        parsed[corpus] = parts
    return parsed


def split_corpora(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def unique_in_order(values: Any) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def write_markdown(
    path: Path,
    selected_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    letter_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    mismatches = [row for row in summary_rows if row["matches_term"] != "True"]
    selected_by_queue = Counter(row.get("source_queue", "") for row in selected_rows)
    summary_by_corpus = Counter(row["audit_corpus"] for row in summary_rows)
    summary_by_bucket = Counter(row["bucket"] for row in summary_rows)
    rows_to_show = summary_rows[: args.markdown_row_limit]
    lines = [
        f"# {args.title}",
        "",
        f"Status: {args.status}",
        "",
        "This report reconstructs the actual ELS letter positions for the selected",
        "Hebrew and Greek all-codes follow-up rows. Hidden-path-only rows are",
        "audited the same way as rows with open-text surface echoes. This is an",
        "audit sheet, not an added statistical test.",
        "",
        "## Inputs",
        "",
        f"- Selected rows: `{args.selected}`",
        "",
        "## Counts",
        "",
        f"- selected input rows: {len(selected_rows):,}",
        f"- path summary rows: {len(summary_rows):,}",
        f"- letter rows: {len(letter_rows):,}",
        f"- sequence mismatches: {len(mismatches):,}",
        f"- selected by queue: `{dict(sorted(selected_by_queue.items()))}`",
        f"- path rows by corpus: `{dict(sorted(summary_by_corpus.items()))}`",
        f"- path rows by bucket: `{dict(sorted(summary_by_bucket.items()))}`",
        "",
        "## Path Summary",
        "",
        "| Rank | Queue | Bucket | Term | Corpus | Sequence | Skip | Center | Center word | Path refs |",
        "| ---: | --- | --- | --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in rows_to_show:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["selection_rank"],
                    row["source_queue"],
                    f"`{row['bucket']}`",
                    display_term(row["normalized_term"], english=row["concept"]),
                    row["audit_corpus"],
                    display_term(row["sequence"], english=row["concept"]),
                    row["skip"],
                    row["audit_center_ref"],
                    display_term(row["audit_center_word"]),
                    row["path_refs"],
                ]
            )
            + " |"
        )
    if len(summary_rows) > len(rows_to_show):
        lines.append(
            f"| ... | ... | ... | ... | ... | ... | ... | ... | ... | "
            f"{len(summary_rows) - len(rows_to_show):,} more rows in CSV |"
        )
    lines.extend(["", "## Read", "", *letter_path_read_lines(summary_rows, mismatches)])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def letter_path_read_lines(
    summary_rows: list[dict[str, str]],
    mismatches: list[dict[str, str]],
) -> list[str]:
    if not summary_rows:
        return [
            "No selected rows were available for letter-path reconstruction.",
            "This means the upstream follow-up selection selected zero rows.",
        ]
    lines = [
        "Every path row should spell the selected normalized term exactly. Center",
        "word is recorded separately: it identifies the surface word at the center",
        "offset, not a requirement that hidden path and surface word be identical.",
        "Exact surface echo and hidden-path-only rows are both retained for review.",
    ]
    if mismatches:
        lines.append(
            f"Warning: {len(mismatches):,} rows did not reconstruct the normalized term."
        )
    return lines


def write_manifest(
    args: argparse.Namespace,
    selected_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    letter_rows: list[dict[str, str]],
    started: float,
) -> None:
    mismatches = [row for row in summary_rows if row["matches_term"] != "True"]
    payload = {
        "tool": "analyze_all_codes_letter_paths",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "selected": str(args.selected),
        "selected_rows": len(selected_rows),
        "summary_rows": len(summary_rows),
        "letter_rows": len(letter_rows),
        "mismatches": len(mismatches),
        "selected_by_queue": dict(
            sorted(Counter(row.get("source_queue", "") for row in selected_rows).items())
        ),
        "summary_by_corpus": dict(
            sorted(Counter(row["audit_corpus"] for row in summary_rows).items())
        ),
        "summary_by_bucket": dict(
            sorted(Counter(row["bucket"] for row in summary_rows).items())
        ),
        "outputs": [
            str(args.summary_out),
            str(args.letters_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


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
