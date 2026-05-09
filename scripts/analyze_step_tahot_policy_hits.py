#!/usr/bin/env python3
"""Audit STEP_TAHOT-only ELS rows against TAHOT word source-type policy."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, load_corpus


DEFAULT_PATTERNS = Path("reports/step_tahot_screening_version_presence/hit_patterns.csv")
DEFAULT_TAHOT_CSV = Path("data/processed/step/tahot.csv")
DEFAULT_CONFIG = Path("configs/example_step_tahot.toml")
OUT_DIR = Path("reports/step_tahot_policy_hits")
ROWS_OUT = OUT_DIR / "step_tahot_only_policy_hits.csv"
SUMMARY_OUT = OUT_DIR / "summary.csv"
MD_OUT = OUT_DIR / "step_tahot_policy_hits.md"
MANIFEST_OUT = OUT_DIR / "manifest.json"
SOURCE_LABEL = "STEP_TAHOT"

ROW_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_ref",
    "center_ref",
    "end_ref",
    "source_type_prefixes",
    "policy_flags",
    "q_count",
    "r_count",
    "x_count",
    "other_non_l_count",
    "letter_path_word_types",
    "letter_path_words",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


@dataclass(frozen=True)
class PolicyAuditRow:
    row: dict[str, str]
    prefixes: tuple[str, ...]
    flags: tuple[str, ...]
    q_count: int
    r_count: int
    x_count: int
    other_non_l_count: int
    word_types: tuple[str, ...]
    words: tuple[str, ...]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus = load_corpus(args.config)
    source_types = load_tahot_source_types(args.tahot_csv)
    pattern_rows = read_pattern_rows(args.patterns)
    audit_rows = [
        audit_pattern_row(row, corpus, source_types, args.source_label)
        for row in pattern_rows
        if is_source_only(row, args.source_label)
    ]
    summary = summarize(audit_rows)
    write_audit_rows(args.rows_out, audit_rows)
    write_summary(args.summary_out, summary)
    write_markdown(args.markdown_out, audit_rows, summary, args)
    write_manifest(args, len(pattern_rows), audit_rows, summary, started)
    print(args.rows_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patterns", type=Path, default=DEFAULT_PATTERNS)
    parser.add_argument("--tahot-csv", type=Path, default=DEFAULT_TAHOT_CSV)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--source-label", default=SOURCE_LABEL)
    parser.add_argument("--rows-out", type=Path, default=ROWS_OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def load_tahot_source_types(path: Path) -> dict[tuple[str, int], str]:
    source_types: dict[tuple[str, int], str] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            ref = row["ref"]
            for word_index, source_type in enumerate(row["source_types"].split(), start=1):
                source_types[(ref, word_index)] = source_type
    return source_types


def read_pattern_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def is_source_only(row: dict[str, str], source_label: str) -> bool:
    return split_corpora(row["present_corpora"]) == [source_label]


def split_corpora(value: str) -> list[str]:
    return [part for part in value.replace(";", ",").split(",") if part]


def audit_pattern_row(
    row: dict[str, str],
    corpus: Corpus,
    source_types: dict[tuple[str, int], str],
    source_label: str,
) -> PolicyAuditRow:
    start, end = parse_source_offsets(row["offsets_by_corpus"], source_label)
    skip = int(row["skip"])
    term_length = len(row["normalized_term"])
    positions = [start + index * skip for index in range(term_length)]
    if positions[-1] != end:
        raise ValueError(f"offsets do not match skip for row: {row}")

    word_types: list[str] = []
    words: list[str] = []
    prefixes: list[str] = []
    counts: Counter[str] = Counter()
    for position in positions:
        word = corpus.word_at(position)
        if word is None:
            word_type = ""
            word_label = ""
        else:
            word_type = source_types.get((word.ref, int(word.word_index)), "")
            word_label = f"{word.ref}#{word.word_index}:{word.normalized_word}"
        prefix = source_type_prefix(word_type)
        prefixes.append(prefix)
        counts[prefix] += 1
        word_types.append(word_type)
        words.append(word_label)

    flags = policy_flags(counts)
    return PolicyAuditRow(
        row=row,
        prefixes=tuple(prefixes),
        flags=tuple(flags),
        q_count=counts["Q"],
        r_count=counts["R"],
        x_count=counts["X"],
        other_non_l_count=sum(
            count
            for prefix, count in counts.items()
            if prefix and not prefix.startswith("L") and prefix not in {"Q", "R", "X"}
        ),
        word_types=tuple(word_types),
        words=tuple(words),
    )


def parse_source_offsets(value: str, source_label: str) -> tuple[int, int]:
    for part in value.split(";"):
        part = part.strip()
        if not part.startswith(f"{source_label}:"):
            continue
        offsets = part.split(":", 1)[1]
        start, end = offsets.split("-", 1)
        return int(start), int(end)
    raise ValueError(f"missing {source_label} offsets: {value}")


def source_type_prefix(value: str) -> str:
    return value.split("(", 1)[0]


def policy_flags(counts: Counter[str]) -> list[str]:
    flags: list[str] = []
    for prefix in ("Q", "R", "X"):
        if counts[prefix]:
            flags.append(prefix)
    if any(
        prefix
        for prefix in counts
        if prefix and not prefix.startswith("L") and prefix not in {"Q", "R", "X"}
    ):
        flags.append("OTHER_NON_L")
    if not flags:
        flags.append("L_ONLY_PATH")
    return flags


def summarize(rows: list[PolicyAuditRow]) -> dict[str, int]:
    return {
        "source_only_rows": len(rows),
        "rows_touching_q": sum("Q" in row.flags for row in rows),
        "rows_touching_r": sum("R" in row.flags for row in rows),
        "rows_touching_x": sum("X" in row.flags for row in rows),
        "rows_touching_other_non_l": sum("OTHER_NON_L" in row.flags for row in rows),
        "rows_l_only_path": sum(row.flags == ("L_ONLY_PATH",) for row in rows),
    }


def write_audit_rows(path: Path, rows: list[PolicyAuditRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ROW_FIELDNAMES)
        writer.writeheader()
        for audit in rows:
            source = audit.row
            writer.writerow(
                {
                    "term_id": source["term_id"],
                    "concept": source["concept"],
                    "category": source["category"],
                    "term": source["term"],
                    "normalized_term": source["normalized_term"],
                    "skip": source["skip"],
                    "direction": source["direction"],
                    "start_ref": source["start_ref"],
                    "center_ref": source["center_ref"],
                    "end_ref": source["end_ref"],
                    "source_type_prefixes": " ".join(audit.prefixes),
                    "policy_flags": " ".join(audit.flags),
                    "q_count": audit.q_count,
                    "r_count": audit.r_count,
                    "x_count": audit.x_count,
                    "other_non_l_count": audit.other_non_l_count,
                    "letter_path_word_types": " ".join(audit.word_types),
                    "letter_path_words": "; ".join(audit.words),
                }
            )


def write_summary(path: Path, summary: dict[str, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDNAMES)
        writer.writeheader()
        for metric, value in summary.items():
            writer.writerow({"metric": metric, "value": value})


def write_markdown(
    path: Path,
    rows: list[PolicyAuditRow],
    summary: dict[str, int],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# STEP TAHOT Policy Hit Audit",
        "",
        "This report audits STEP_TAHOT-only exact-hit rows against the TAHOT",
        "word source-type metadata for each hidden-letter path.",
        "",
        "## Inputs",
        "",
        f"- Patterns: `{args.patterns}`",
        f"- TAHOT CSV: `{args.tahot_csv}`",
        f"- Corpus config: `{args.config}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    lines.extend(f"| `{metric}` | {value:,} |" for metric, value in summary.items())
    lines.extend(
        [
            "",
            "## First Policy-Touching Rows",
            "",
            "| Term | Flags | Skip | Refs | Source-type path |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    examples = [row for row in rows if row.flags != ("L_ONLY_PATH",)][:50]
    for audit in examples:
        source = audit.row
        lines.append(
            "| "
            f"`{source['term_id']}` | "
            f"`{' '.join(audit.flags)}` | "
            f"{source['skip']} | "
            f"{source['start_ref']} / {source['center_ref']} / {source['end_ref']} | "
            f"`{' '.join(audit.word_types)}` |"
        )
    if not examples:
        lines.append("| _none_ |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Read",
            "",
            "`Q`, `R`, and `X` flags mean the ELS path touches at least one",
            "letter in a word whose selected TAHOT row is tied to qere, restored",
            "text, or LXX-based Hebrew additions. `L_ONLY_PATH` rows may still be",
            "STEP_TAHOT-only because of upstream versification, word division, or",
            "nearby selected readings shifting the letter stream.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    pattern_row_count: int,
    audit_rows: list[PolicyAuditRow],
    summary: dict[str, int],
    started: float,
) -> None:
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "tool": "analyze_step_tahot_policy_hits",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "patterns": str(args.patterns),
        "tahot_csv": str(args.tahot_csv),
        "config": str(args.config),
        "source_label": args.source_label,
        "pattern_rows": pattern_row_count,
        "audit_rows": len(audit_rows),
        "summary": summary,
        "outputs": {
            "rows": str(args.rows_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
