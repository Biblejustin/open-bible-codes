#!/usr/bin/env python3
"""Summarize matrix-cluster candidate relations against secular controls."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.term_display import display_term


DEFAULT_CANDIDATES = Path("reports/matrix_clusters/candidates.csv")
DEFAULT_RELATION_OUT = Path("reports/matrix_clusters/relation_control_summary.csv")
DEFAULT_TERM_PAIR_OUT = Path("reports/matrix_clusters/term_pair_control_summary.csv")
DEFAULT_MARKDOWN_OUT = Path("docs/MATRIX_CLUSTER_CONTROL_SUMMARY.md")
DEFAULT_MANIFEST_OUT = Path("reports/matrix_clusters/control_summary.manifest.json")

RELATION_FIELDNAMES = [
    "cell_relation",
    "bible_pairs",
    "secular_control_pairs",
    "bible_corpora",
    "secular_control_corpora",
    "bible_pairs_per_corpus",
    "secular_control_pairs_per_corpus",
    "bible_to_control_rate_ratio",
    "bible_max_corpus_pairs",
    "secular_max_corpus_pairs",
    "exceeds_secular_max",
]

TERM_PAIR_FIELDNAMES = [
    "cell_relation",
    "term_a_id",
    "term_b_id",
    "term_a_concept",
    "term_b_concept",
    "term_a_normalized",
    "term_b_normalized",
    "bible_pairs",
    "secular_control_pairs",
    "bible_corpora",
    "secular_control_corpora",
    "bible_pairs_per_corpus",
    "secular_control_pairs_per_corpus",
    "bible_to_control_rate_ratio",
    "exceeds_secular_max",
]

def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_rows(args.candidates)
    relation_summary = summarize_by_relation(rows)
    term_pair_summary = summarize_by_term_pair(rows)
    write_rows(args.relation_out, RELATION_FIELDNAMES, relation_summary)
    write_rows(args.term_pair_out, TERM_PAIR_FIELDNAMES, term_pair_summary)
    write_markdown(args.markdown_out, args, rows, relation_summary, term_pair_summary)
    write_manifest(args.manifest_out, args, rows, relation_summary, term_pair_summary, started)
    print(args.relation_out)
    print(args.term_pair_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--relation-out", type=Path, default=DEFAULT_RELATION_OUT)
    parser.add_argument("--term-pair-out", type=Path, default=DEFAULT_TERM_PAIR_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    parser.add_argument("--markdown-row-limit", type=int, default=40)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def summarize_by_relation(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    relations = sorted({row.get("cell_relation", "") for row in rows if row.get("cell_relation", "")})
    output = [relation_summary_row("all", rows)]
    output.extend(relation_summary_row(relation, [row for row in rows if row.get("cell_relation", "") == relation]) for relation in relations)
    return sorted(output, key=lambda row: (row["cell_relation"] != "all", str(row["cell_relation"])))


def relation_summary_row(relation: str, rows: list[dict[str, str]]) -> dict[str, object]:
    bible_rows = rows_for_class(rows, "bible")
    control_rows = rows_for_class(rows, "secular_control")
    bible_corpus_counts = corpus_counts(bible_rows)
    control_corpus_counts = corpus_counts(control_rows)
    return {
        "cell_relation": relation,
        "bible_pairs": len(bible_rows),
        "secular_control_pairs": len(control_rows),
        "bible_corpora": len(bible_corpus_counts),
        "secular_control_corpora": len(control_corpus_counts),
        "bible_pairs_per_corpus": rate_text(len(bible_rows), len(bible_corpus_counts)),
        "secular_control_pairs_per_corpus": rate_text(len(control_rows), len(control_corpus_counts)),
        "bible_to_control_rate_ratio": ratio_text(
            per_corpus_rate(len(bible_rows), len(bible_corpus_counts)),
            per_corpus_rate(len(control_rows), len(control_corpus_counts)),
        ),
        "bible_max_corpus_pairs": max(bible_corpus_counts.values(), default=0),
        "secular_max_corpus_pairs": max(control_corpus_counts.values(), default=0),
        "exceeds_secular_max": bool_text(max(bible_corpus_counts.values(), default=0) > max(control_corpus_counts.values(), default=0)),
    }


def summarize_by_term_pair(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, tuple[str, str, str], tuple[str, str, str]], list[dict[str, str]]] = {}
    for row in rows:
        key = (
            row.get("cell_relation", ""),
            *canonical_term_pair(row),
        )
        grouped.setdefault(key, []).append(row)

    output = [term_pair_summary_row(key, group_rows) for key, group_rows in grouped.items()]
    return sorted(
        output,
        key=lambda row: (
            -int(row["bible_pairs"]),
            -int(row["secular_control_pairs"]),
            str(row["cell_relation"]),
            str(row["term_a_id"]),
            str(row["term_b_id"]),
        ),
    )


def term_pair_summary_row(
    key: tuple[str, tuple[str, str, str], tuple[str, str, str]],
    rows: list[dict[str, str]],
) -> dict[str, object]:
    relation, term_a, term_b = key
    bible_rows = rows_for_class(rows, "bible")
    control_rows = rows_for_class(rows, "secular_control")
    bible_corpus_counts = corpus_counts(bible_rows)
    control_corpus_counts = corpus_counts(control_rows)
    return {
        "cell_relation": relation,
        "term_a_id": term_a[0],
        "term_b_id": term_b[0],
        "term_a_concept": term_a[1],
        "term_b_concept": term_b[1],
        "term_a_normalized": term_a[2],
        "term_b_normalized": term_b[2],
        "bible_pairs": len(bible_rows),
        "secular_control_pairs": len(control_rows),
        "bible_corpora": len(bible_corpus_counts),
        "secular_control_corpora": len(control_corpus_counts),
        "bible_pairs_per_corpus": rate_text(len(bible_rows), len(bible_corpus_counts)),
        "secular_control_pairs_per_corpus": rate_text(len(control_rows), len(control_corpus_counts)),
        "bible_to_control_rate_ratio": ratio_text(
            per_corpus_rate(len(bible_rows), len(bible_corpus_counts)),
            per_corpus_rate(len(control_rows), len(control_corpus_counts)),
        ),
        "exceeds_secular_max": bool_text(max(bible_corpus_counts.values(), default=0) > max(control_corpus_counts.values(), default=0)),
    }


def canonical_term_pair(row: dict[str, str]) -> tuple[tuple[str, str, str], tuple[str, str, str]]:
    left = (
        row.get("left_term_id", ""),
        row.get("left_concept", ""),
        row.get("left_normalized_term", ""),
    )
    right = (
        row.get("right_term_id", ""),
        row.get("right_concept", ""),
        row.get("right_normalized_term", ""),
    )
    ordered = sorted((left, right), key=lambda item: (item[0], item[1], item[2]))
    return ordered[0], ordered[1]


def rows_for_class(rows: list[dict[str, str]], corpus_class: str) -> list[dict[str, str]]:
    return [row for row in rows if row.get("corpus_class", "") == corpus_class]


def corpus_counts(rows: list[dict[str, str]]) -> Counter[str]:
    return Counter(row.get("corpus_label", "") for row in rows if row.get("corpus_label", ""))


def per_corpus_rate(pairs: int, corpora: int) -> float | None:
    if corpora == 0:
        return None
    return pairs / corpora


def rate_text(pairs: int, corpora: int) -> str:
    rate = per_corpus_rate(pairs, corpora)
    return "" if rate is None else f"{rate:.6f}"


def ratio_text(numerator: float | None, denominator: float | None) -> str:
    if numerator is None or denominator in (None, 0):
        return ""
    return f"{numerator / denominator:.6f}"


def bool_text(value: bool) -> str:
    return "yes" if value else "no"


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    relation_summary: list[dict[str, object]],
    term_pair_summary: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    class_counts = Counter(row.get("corpus_class", "") for row in rows)
    lines = [
        "# Matrix Cluster Control Summary",
        "",
        "Status: relation-specific screening summary, not claim promotion.",
        "",
        "This report summarizes matrix-neighborhood candidate pairs by nearest-cell relation and compares Bible rows with language-matched secular-control rows already present in the candidate file. The rate ratio is per observed corpus in each class, not a p-value.",
        "",
        "No row in this report is promoted as significant. Claim-grade matrix work still needs a preregistered relation metric, locked row-width family, matched control family, and multiple-comparison correction.",
        "",
        "## Settings",
        "",
        f"- Candidate input: `{args.candidates}`",
        f"- Candidate rows: `{len(rows):,}`",
        f"- Bible candidate rows: `{class_counts['bible']:,}`",
        f"- Secular-control candidate rows: `{class_counts['secular_control']:,}`",
        "",
        "## Relation Summary",
        "",
        "| Relation | Bible pairs | Control pairs | Bible corpora | Control corpora | Bible/control rate ratio | Bible max corpus | Control max corpus | Exceeds control max |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in relation_summary:
        lines.append(
            "| "
            f"`{row['cell_relation']}` | {row['bible_pairs']} | {row['secular_control_pairs']} | "
            f"{row['bible_corpora']} | {row['secular_control_corpora']} | "
            f"{empty_dash(row['bible_to_control_rate_ratio'])} | {row['bible_max_corpus_pairs']} | "
            f"{row['secular_max_corpus_pairs']} | `{row['exceeds_secular_max']}` |"
        )

    lines.extend(
        [
            "",
            "## Top Term-Pair Rows",
            "",
            "| Relation | Term A | Term B | Bible pairs | Control pairs | Bible/control rate ratio | Exceeds control max |",
            "| --- | --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in term_pair_summary[: args.markdown_row_limit]:
        term_a = display_term(str(row["term_a_normalized"]), english=str(row["term_a_concept"]))
        term_b = display_term(str(row["term_b_normalized"]), english=str(row["term_b_concept"]))
        lines.append(
            "| "
            f"`{row['cell_relation']}` | {md_cell(term_a)} | {md_cell(term_b)} | "
            f"{row['bible_pairs']} | {row['secular_control_pairs']} | "
            f"{empty_dash(row['bible_to_control_rate_ratio'])} | `{row['exceeds_secular_max']}` |"
        )
    if len(term_pair_summary) > args.markdown_row_limit:
        lines.append(
            f"| ... | ... | ... | ... | ... | ... | {len(term_pair_summary) - args.markdown_row_limit:,} more rows in CSV |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- `exceeds_secular_max=yes` means the largest Bible corpus count is above the largest secular-control corpus count for that row.",
            "- Empty ratios mean the control denominator is zero.",
            "- This is useful for review prioritization and control auditing only.",
            "- A later confirmatory matrix study should lock which relation rows count and how they are corrected before reading this report.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def empty_dash(value: object) -> str:
    text = str(value)
    return text if text else "--"


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    relation_summary: list[dict[str, object]],
    term_pair_summary: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/summarize_matrix_cluster_controls.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "candidate_rows": len(rows),
        "relation_summary_rows": len(relation_summary),
        "term_pair_summary_rows": len(term_pair_summary),
        "corpus_class_counts": dict(Counter(row.get("corpus_class", "") for row in rows)),
        "inputs": {"candidates": str(args.candidates)},
        "outputs": {
            "relation_out": str(args.relation_out),
            "term_pair_out": str(args.term_pair_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
