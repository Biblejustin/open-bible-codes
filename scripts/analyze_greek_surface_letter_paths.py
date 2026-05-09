#!/usr/bin/env python3
"""Export letter-path audits for tightened Greek surface-triage rows."""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import Corpus, load_corpus


SELECTED_IN = Path("reports/greek_expanded_surface_triage/selected_patterns.csv")
OUT_DIR = Path("reports/greek_expanded_surface_letter_paths")
SUMMARY_OUT = OUT_DIR / "path_summary.csv"
LETTERS_OUT = OUT_DIR / "letter_paths.csv"
MD_OUT = Path("docs/GREEK_EXPANDED_SURFACE_LETTER_PATHS.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"
DEFAULT_CORPORA = (
    "TR_NT=configs/example_ebible_grctr.toml",
    "BYZ_NT=configs/example_ebible_grcmt.toml",
    "TCG_NT=configs/example_ebible_grctcgnt.toml",
    "SBLGNT=configs/example_sblgnt.toml",
)

SUMMARY_FIELDNAMES = [
    "term_id",
    "concept",
    "normalized_term",
    "corpus",
    "skip",
    "direction",
    "sequence",
    "matches_term",
    "start_ref",
    "center_ref",
    "end_ref",
    "path_refs",
    "center_word",
    "center_normalized_word",
    "start_offset",
    "center_offset",
    "end_offset",
    "path_offsets",
]

LETTER_FIELDNAMES = [
    "term_id",
    "normalized_term",
    "corpus",
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


@dataclass(frozen=True)
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
    write_markdown(args.markdown_out, summary_rows, letter_rows, args)
    write_manifest(args, summary_rows, letter_rows, started)
    print(args.summary_out)
    print(args.letters_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selected", type=Path, default=SELECTED_IN)
    parser.add_argument("--corpus", action="append", default=list(DEFAULT_CORPORA))
    parser.add_argument("--title", default="Greek Expanded Surface Letter Paths")
    parser.add_argument(
        "--status",
        default="audit sheet for selected surface-triage rows; no claim.",
    )
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--letters-out", type=Path, default=LETTERS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def parse_corpus_args(values: list[str]) -> dict[str, Path]:
    parsed = {}
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
    positions = tuple(start + index * skip for index in range(len(row["normalized_term"])))
    sequence = "".join(corpus.text[position] for position in positions)
    center_word = corpus.word_at(center)
    path_refs = unique_in_order(corpus.ref_at(position) for position in positions)
    letters = tuple(
        letter_row(row, corpus_label, corpus, position, index)
        for index, position in enumerate(positions, start=1)
    )
    summary = {
        "term_id": row["term_id"],
        "concept": row["concept"],
        "normalized_term": row["normalized_term"],
        "corpus": corpus_label,
        "skip": row["skip"],
        "direction": row["direction"],
        "sequence": sequence,
        "matches_term": str(sequence == row["normalized_term"]),
        "start_ref": corpus.ref_at(start),
        "center_ref": corpus.ref_at(center),
        "end_ref": corpus.ref_at(end),
        "path_refs": "; ".join(path_refs),
        "center_word": center_word.raw_word if center_word is not None else "",
        "center_normalized_word": center_word.normalized_word if center_word is not None else "",
        "start_offset": str(start),
        "center_offset": str(center),
        "end_offset": str(end),
        "path_offsets": "/".join(str(position) for position in positions),
    }
    return PathAudit(summary=summary, letters=letters)


def letter_row(
    row: dict[str, str],
    corpus_label: str,
    corpus: Corpus,
    position: int,
    letter_index: int,
) -> dict[str, str]:
    word = corpus.word_at(position)
    return {
        "term_id": row["term_id"],
        "normalized_term": row["normalized_term"],
        "corpus": corpus_label,
        "skip": row["skip"],
        "direction": row["direction"],
        "letter_index": str(letter_index),
        "offset": str(position),
        "letter": corpus.text[position],
        "ref": corpus.ref_at(position),
        "word_index": str(word.word_index) if word is not None else "",
        "word": word.raw_word if word is not None else "",
        "normalized_word": word.normalized_word if word is not None else "",
    }


def parse_offsets_by_corpus(value: str) -> dict[str, tuple[int, int, int]]:
    parsed = {}
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
    return [item for item in value.split(",") if item]


def unique_in_order(values: Any) -> list[str]:
    seen = set()
    output = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, str]],
    letter_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    lines = [
        f"# {args.title}",
        "",
        f"Status: {args.status}",
        "",
        "This report reconstructs the actual ELS letter positions for the tightened",
        "Greek surface rows. It is an audit aid, not an additional statistical",
        "test.",
        "",
        "## Inputs",
        "",
        f"- Selected rows: `{args.selected}`",
        "",
        "## Path Summary",
        "",
        "| Term | Corpus | Sequence | Skip | Center | Center word | Path refs |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['normalized_term']}`",
                    row["corpus"],
                    f"`{row['sequence']}`",
                    row["skip"],
                    row["center_ref"],
                    f"`{row['center_word']}`",
                    row["path_refs"],
                ]
            )
            + " |"
        )
    lines.extend(["", "## Letter Rows", ""])
    for summary in summary_rows:
        lines.extend(
            [
                f"### `{summary['normalized_term']}` / {summary['corpus']}",
                "",
                "| # | Offset | Letter | Ref | Word |",
                "| ---: | ---: | --- | --- | --- |",
            ]
        )
        for row in letter_rows:
            if row["term_id"] != summary["term_id"] or row["corpus"] != summary["corpus"]:
                continue
            lines.append(
                "| "
                + " | ".join(
                    [
                        row["letter_index"],
                        row["offset"],
                        f"`{row['letter']}`",
                        row["ref"],
                        f"`{row['word']}`",
                    ]
                )
                + " |"
            )
        lines.append("")
    lines.extend(
        [
            "## Read",
            "",
            *letter_path_read_lines(summary_rows),
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def letter_path_read_lines(summary_rows: list[dict[str, str]]) -> list[str]:
    if not summary_rows:
        return [
            "No selected rows were available for letter-path reconstruction.",
            "This is expected when the upstream prospective triage selected zero rows.",
        ]
    return [
        "Each row should spell the selected normalized term exactly. The center word",
        "is recorded separately because exact-center surface means the center verse",
        "contains the surface term, not necessarily that the center word is the",
        "same word.",
    ]


def write_manifest(
    args: argparse.Namespace,
    summary_rows: list[dict[str, str]],
    letter_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_greek_surface_letter_paths",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "selected": str(args.selected),
        "summary_rows": len(summary_rows),
        "letter_rows": len(letter_rows),
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
