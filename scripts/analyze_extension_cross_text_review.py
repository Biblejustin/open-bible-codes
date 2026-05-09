#!/usr/bin/env python3
"""Check exact-center extension cohort rows against the opposite Greek NT text."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.analyze_extension_context_review import overlap_key


BASE = Path("reports/protocols/public_baseline")
COHORT_REVIEW = Path("reports/extension_exact_center_cohort_review_summary.csv")
EXTENSION_FILES = {
    "TR_NT": BASE / "surface_context_extensions_tr_nt.csv",
    "SBLGNT": BASE / "surface_context_extensions_sblgnt.csv",
}

SUMMARY_OUT = Path("reports/extension_exact_center_cross_text_summary.csv")
MD_OUT = Path("reports/extension_exact_center_cross_text.md")
MANIFEST_OUT = Path("reports/extension_exact_center_cross_text.manifest.json")

FIELDNAMES = [
    "overlap_key",
    "source_corpus",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "extension_type",
    "extended_sequence",
    "source_center_ref",
    "source_context_read",
    "source_control_band",
    "source_combined_q",
    "opposite_corpus",
    "opposite_match_count",
    "opposite_center_refs",
    "opposite_hit_refs",
    "opposite_matched_refs",
    "cross_text_status",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    cohort_rows = read_rows(args.cohort_review)
    indexes = {label: extension_index(path) for label, path in EXTENSION_FILES.items()}
    rows = [cross_text_row(row, indexes) for row in cohort_rows]
    write_rows(args.summary_out, rows)
    write_markdown(args.markdown_out, rows)
    write_manifest(args, len(cohort_rows), len(rows), started)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cohort-review", type=Path, default=COHORT_REVIEW)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def extension_index(path: Path) -> dict[str, list[dict[str, str]]]:
    rows_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_rows(path):
        rows_by_key[overlap_key(row)].append(row)
    return dict(rows_by_key)


def cross_text_row(
    row: dict[str, str],
    indexes: dict[str, dict[str, list[dict[str, str]]]],
) -> dict[str, str]:
    key = row["overlap_key"]
    source_corpus = row["corpus"]
    opposite_corpus = "SBLGNT" if source_corpus == "TR_NT" else "TR_NT"
    opposite_rows = indexes.get(opposite_corpus, {}).get(key, [])
    status = cross_text_status(len(opposite_rows))
    return {
        "overlap_key": key,
        "source_corpus": source_corpus,
        "term": row["term"],
        "normalized_term": row["normalized_term"],
        "skip": row["skip"],
        "direction": row["direction"],
        "extension_type": row["extension_type"],
        "extended_sequence": row["extended_sequence"],
        "source_center_ref": row["center_ref"],
        "source_context_read": row["context_read"],
        "source_control_band": row["control_band"],
        "source_combined_q": row["combined_min_q"],
        "opposite_corpus": opposite_corpus,
        "opposite_match_count": str(len(opposite_rows)),
        "opposite_center_refs": refs_cell(opposite_rows, "center_ref"),
        "opposite_hit_refs": refs_cell(opposite_rows, "start_ref", "end_ref"),
        "opposite_matched_refs": refs_cell(opposite_rows, "matched_refs"),
        "cross_text_status": status,
        "read": read_label(status),
    }


def cross_text_status(opposite_count: int) -> str:
    if opposite_count > 0:
        return "cross_text_match"
    return "source_only"


def read_label(status: str) -> str:
    if status == "cross_text_match":
        return "same extension key appears in both Greek NT texts"
    return "no same extension key in opposite Greek NT extension file"


def refs_cell(rows: list[dict[str, str]], *fields: str) -> str:
    values = []
    for row in rows:
        if len(fields) == 1:
            value = row.get(fields[0], "")
        else:
            value = "-".join(row.get(field, "") for field in fields)
        if value:
            values.append(value)
    return "; ".join(sorted(set(values)))


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        "# Extension Exact-Center Cross-Text Review",
        "",
        "Checks whether exact-center extension cohort rows have the same extension key in the opposite Greek NT text.",
        "",
        "| Source | Term | Center | Opposite text | Opposite matches | Status | Read |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["source_corpus"],
                    f"`{row['term']}` `{row['extended_sequence']}`",
                    row["source_center_ref"],
                    row["opposite_corpus"],
                    row["opposite_match_count"],
                    f"`{row['cross_text_status']}`",
                    row["read"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "`δοξα` is the only exact-center cohort key that appears in both TR_NT and SBLGNT. SBLGNT `αιμα` and `υιος` are source-only under this exact extension-key test.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    input_rows: int,
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_extension_cross_text_review",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "cohort_review": str(args.cohort_review),
        "extension_files": {label: str(path) for label, path in EXTENSION_FILES.items()},
        "input_rows": input_rows,
        "rows": rows,
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


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
