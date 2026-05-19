#!/usr/bin/env python3
"""Build a compact final-report highlight table from locked report artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.term_display import display_center, display_term


DEFAULT_CENTERED_SUMMARY = Path("reports/centered_occurrence_index/presence_summary.csv")
DEFAULT_CLAIM_CATALOG = Path("claims/claim_catalog.csv")
DEFAULT_OUT = Path("reports/final_report_highlights/highlights.csv")
DEFAULT_MARKDOWN = Path("docs/FINAL_REPORT_HIGHLIGHTS.md")
DEFAULT_MANIFEST = Path("reports/final_report_highlights/manifest.json")

FIELDNAMES = [
    "rank",
    "highlight_type",
    "status",
    "normalized_term",
    "display_term",
    "center_ref",
    "center_word",
    "display_center",
    "corpora",
    "occurrence_type",
    "source_family",
    "total_paths",
    "frequency_read",
    "control_read",
    "context_excerpt",
    "final_report_read",
]

TYPE_WEIGHT = {
    "centered_self_exact_word": 100,
    "centered_self_surface_form": 85,
    "relevant_center_same_concept": 70,
    "relevant_center_same_category": 60,
    "center_verse_relevant": 50,
    "span_relevant": 40,
}

SOURCE_WEIGHT = {
    "gog_source_review": 80,
    "original_language_findings": 60,
    "strong_full_span_exact_center": 45,
    "all_codes_followup": 35,
}

HIGHLIGHT_SOURCE_FAMILIES = {
    "gog_source_review",
    "original_language_findings",
    "strong_full_span_exact_center",
}

HIGHLIGHT_OCCURRENCE_TYPES = {
    "centered_self_exact_word",
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    centered_rows = read_rows(args.centered_summary)
    claim_rows = read_rows(args.claim_catalog)
    highlights = build_highlights(centered_rows, limit=args.limit)
    write_csv(args.out, highlights)
    write_markdown(args.markdown_out, highlights, claim_rows, args)
    write_manifest(args.manifest_out, args, highlights, claim_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--centered-summary", type=Path, default=DEFAULT_CENTERED_SUMMARY)
    parser.add_argument("--claim-catalog", type=Path, default=DEFAULT_CLAIM_CATALOG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--limit", type=int, default=40)
    return parser


def build_highlights(rows: list[dict[str, str]], *, limit: int) -> list[dict[str, object]]:
    bible_rows = [
        row
        for row in rows
        if row.get("corpus_class") == "bible"
        and row.get("source_family") in HIGHLIGHT_SOURCE_FAMILIES
        and row.get("occurrence_type") in HIGHLIGHT_OCCURRENCE_TYPES
    ]
    best_by_key: dict[str, dict[str, str]] = {}
    for row in bible_rows:
        key = row.get("normalized_term", "")
        current = best_by_key.get(key)
        if current is None or highlight_sort_key(row) < highlight_sort_key(current):
            best_by_key[key] = row

    selected = sorted(best_by_key.values(), key=highlight_sort_key)[:limit]
    highlights: list[dict[str, object]] = []
    for rank, row in enumerate(selected, start=1):
        highlights.append(
            {
                "rank": rank,
                "highlight_type": highlight_type(row),
                "status": highlight_status(row),
                "normalized_term": row.get("normalized_term", ""),
                "display_term": display_term(row.get("normalized_term", "")),
                "center_ref": row.get("center_ref", ""),
                "center_word": row.get("center_word", ""),
                "display_center": display_center(row.get("center_ref", ""), row.get("center_word", "")),
                "corpora": row.get("corpora", ""),
                "occurrence_type": row.get("occurrence_type", ""),
                "source_family": row.get("source_family", ""),
                "total_paths": int_or_zero(row.get("total_paths", "")),
                "frequency_read": row.get("frequency_reads", ""),
                "control_read": row.get("control_reads", ""),
                "context_excerpt": row.get("context_excerpt", ""),
                "final_report_read": final_report_read(row),
            }
        )
    return highlights


def highlight_sort_key(row: dict[str, str]) -> tuple[int, int, int, int, str, str]:
    score = highlight_score(row)
    return (
        -score,
        int_or_zero(row.get("summary_rank", "")),
        -int_or_zero(row.get("total_paths", "")),
        -len(row.get("corpora", "").split(";")),
        row.get("normalized_term", ""),
        row.get("center_ref", ""),
    )


def highlight_score(row: dict[str, str]) -> int:
    score = TYPE_WEIGHT.get(row.get("occurrence_type", ""), 0)
    score += SOURCE_WEIGHT.get(row.get("source_family", ""), 0)
    frequency = row.get("frequency_reads", "").lower()
    corpora = row.get("corpora", "")
    if "promote" in frequency and "not frequency-promoted" not in frequency:
        score += 25
    if "low-count review" in frequency:
        score += 15
    if "background" in frequency:
        score -= 10
    if "hold" in frequency:
        score -= 5
    if "not frequency-promoted" in frequency:
        score -= 5
    if len([part for part in corpora.split(";") if part]) >= 4:
        score += 20
    score += min(int_or_zero(row.get("total_paths", "")), 20)
    return score


def highlight_type(row: dict[str, str]) -> str:
    occurrence_type = row.get("occurrence_type", "")
    if occurrence_type.startswith("centered_self"):
        return "centered_self_occurrence"
    if occurrence_type.startswith("relevant_center"):
        return "related_center_occurrence"
    if occurrence_type == "center_verse_relevant":
        return "center_verse_relevant_occurrence"
    if occurrence_type == "span_relevant":
        return "span_relevant_occurrence"
    return "occurrence_review"


def highlight_status(row: dict[str, str]) -> str:
    frequency = row.get("frequency_reads", "").lower()
    if row.get("normalized_term") == "ιησουσ":
        return "occurrence_hold_for_referent_or_controls"
    if "not frequency-promoted" in frequency:
        return "contextual_occurrence_frequency_cautioned"
    if "promote" in frequency and "not frequency-promoted" not in frequency:
        return "occurrence_review_promoted_by_current_filter"
    if "background" in frequency:
        return "occurrence_background_pressure"
    if "hold" in frequency:
        return "occurrence_hold_for_referent_or_controls"
    return "occurrence_review_candidate_not_claim"


def final_report_read(row: dict[str, str]) -> str:
    term = display_term(row.get("normalized_term", ""))
    center = display_center(row.get("center_ref", ""), row.get("center_word", ""))
    status = highlight_status(row).replace("_", " ")
    return f"List occurrence: hidden {term} centered at {center}; {status}."


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    highlights: list[dict[str, object]],
    claim_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    status_counts: dict[str, int] = {}
    for row in highlights:
        status = str(row["status"])
        status_counts[status] = status_counts.get(status, 0) + 1

    controlled_claim_rows = [
        row
        for row in claim_rows
        if row.get("status") in {"controlled_review_candidate", "partially_reproducible"}
    ]

    lines = [
        "# Final Report Highlights",
        "",
        "Status: compact final-report table assembled from locked report artifacts.",
        "This is not a new ELS search and it does not promote rows to public claims.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.build_final_report_highlights "
            f"--centered-summary {args.centered_summary} "
            f"--claim-catalog {args.claim_catalog} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        f"- highlight rows: {len(highlights)}",
        f"- controlled or partial catalog rows: {len(controlled_claim_rows)}",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")

    lines.extend(
        [
            "",
            "## Highlight Rows",
            "",
            "| Rank | Status | Term | Center | Corpora | Occurrence type | Paths | Read |",
            "| ---: | --- | --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in highlights[: args.limit]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["rank"]),
                    escape_md(str(row["status"])),
                    escape_md(str(row["display_term"])),
                    escape_md(str(row["display_center"])),
                    escape_md(str(row["corpora"])),
                    f"`{escape_md(str(row['occurrence_type']))}`",
                    str(row["total_paths"]),
                    escape_md(str(row["final_report_read"])),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Catalog Rows To Keep Beside The Highlights",
            "",
            "| Claim ID | Status | Current read | Evidence |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in controlled_claim_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_md(row.get('claim_id', ''))}`",
                    f"`{escape_md(row.get('status', ''))}`",
                    escape_md(row.get("current_reproduction", "")),
                    f"`{escape_md(row.get('evidence', ''))}`",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- This table is a presentation layer over the centered-occurrence index and claim catalog.",
            "- A row appears here because it is useful for final-report review, not because it is claim-grade.",
            "- Frequency and control reads should be carried into any public writeup beside the occurrence.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    highlights: list[dict[str, object]],
    claim_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "build_final_report_highlights",
        "version": __version__,
        "generated_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "commit": git_commit(),
        "inputs": {
            "centered_summary": str(args.centered_summary),
            "claim_catalog": str(args.claim_catalog),
        },
        "outputs": {
            "highlights": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "highlight_rows": len(highlights),
        "claim_catalog_rows": len(claim_rows),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def int_or_zero(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
