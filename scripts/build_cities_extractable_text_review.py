#!/usr/bin/env python3
"""Classify extractable Cities PDFs by source-review role."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_wrr_wayback_source_recovery_probe import markdown_cell, markdown_link


DEFAULT_QUEUE = Path("reports/cities_pdf_recovery_probe/cities_source_review_queue.csv")
DEFAULT_TEXT_AUDIT = Path(
    "reports/cities_pdf_recovery_probe/cities_recovered_pdf_text_audit.csv"
)
DEFAULT_ANCHORS = Path("reports/cities_pdf_recovery_probe/cities_recovered_pdf_text_anchors.csv")
DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_extractable_text_review.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_extractable_text_review_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_extractable_text_review.manifest.json"
)

FIELDNAMES = [
    "label",
    "family",
    "source_role",
    "data_bearing_status",
    "anchor",
    "anchor_status",
    "pdf_pages",
    "normalized_text_chars",
    "selected_path",
    "url",
    "review_read",
    "next_action",
    "claim_boundary",
]

SUMMARY_FIELDNAMES = [
    "metric",
    "value",
]

CLAIM_BOUNDARY = (
    "extractable-text role review only; no source-row import, no city normalization, "
    "no ELS, no compactness, no p-level"
)

SOURCE_ROLES = {
    "cities_pdf_communities_data": (
        "communities_data_table",
        "data_bearing_candidate",
        "Communities data/protocol table candidate; inspect table schema and rows before any import.",
        "manual source-row and table-schema review",
    ),
    "cities_pdf_gans": (
        "communities_method_paper",
        "method_context_candidate",
        "Paper/method context candidate; not a city-name source table by itself.",
        "use for method/context audit before any result protocol",
    ),
    "cities_pdf_dp_365_1": (
        "aumann_committee_perspective",
        "commentary_or_perspective",
        "Aumann committee perspective text; source context, not a row table.",
        "use for source-history review, not city-row import",
    ),
    "cities_pdf_dp_365_2": (
        "furstenberg_committee_perspective",
        "commentary_or_perspective",
        "Furstenberg committee perspective text; source context, not a row table.",
        "use for source-history review, not city-row import",
    ),
    "cities_pdf_dp_365_4": (
        "witztum_critique_response",
        "critique_or_response",
        "Witztum critique/response text; source context, not a row table.",
        "use for dispute/context review, not city-row import",
    ),
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    queue_rows = read_csv(args.queue)
    text_rows = {row["label"]: row for row in read_csv(args.text_audit)}
    anchor_rows = read_csv(args.anchors)
    review_rows = build_review_rows(queue_rows, text_rows, anchor_rows)
    summary = build_summary(review_rows)
    write_csv(args.out, FIELDNAMES, review_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary)
    write_markdown(args.markdown_out, review_rows, summary)
    write_manifest(args.manifest_out, args, review_rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--text-audit", type=Path, default=DEFAULT_TEXT_AUDIT)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_review_rows(
    queue_rows: list[dict[str, str]],
    text_rows: dict[str, dict[str, str]],
    anchor_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    anchor_by_label = {row["label"]: row for row in anchor_rows}
    rows: list[dict[str, str]] = []
    for queue_row in queue_rows:
        if queue_row.get("lane") != "review_extractable_text":
            continue
        label = queue_row["label"]
        role, status, read, action = classify_source_role(label)
        text = text_rows.get(label, {})
        anchor = anchor_by_label.get(label, {})
        rows.append(
            {
                "label": label,
                "family": queue_row.get("family", ""),
                "source_role": role,
                "data_bearing_status": status,
                "anchor": anchor.get("anchor", ""),
                "anchor_status": anchor.get("status", ""),
                "pdf_pages": queue_row.get("pdf_pages", ""),
                "normalized_text_chars": queue_row.get("normalized_text_chars", ""),
                "selected_path": queue_row.get("selected_path", ""),
                "url": queue_row.get("url", ""),
                "review_read": read,
                "next_action": action,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(rows, key=lambda row: (row["data_bearing_status"], row["label"]))


def classify_source_role(label: str) -> tuple[str, str, str, str]:
    return SOURCE_ROLES.get(
        label,
        (
            "unclassified_extractable_text",
            "manual_classification_needed",
            "Extractable text exists but source role is not classified.",
            "classify role before any source-row work",
        ),
    )


def build_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    status_counts = Counter(row["data_bearing_status"] for row in rows)
    role_counts = Counter(row["source_role"] for row in rows)
    found_anchors = sum(1 for row in rows if row["anchor_status"] == "found")
    summary = [
        {"metric": "extractable_rows_reviewed", "value": str(len(rows))},
        {"metric": "anchors_found", "value": str(found_anchors)},
    ]
    for status in sorted(status_counts):
        summary.append({"metric": f"status_{status}", "value": str(status_counts[status])})
    for role in sorted(role_counts):
        summary.append({"metric": f"role_{role}", "value": str(role_counts[role])})
    summary.append({"metric": "claim_boundary", "value": CLAIM_BOUNDARY})
    return summary


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary: list[dict[str, str]],
) -> None:
    values = {row["metric"]: row["value"] for row in summary}
    lines = [
        "# Cities Extractable Text Review",
        "",
        "Status: source-role review only. This classifies the five extractable",
        "Cities PDFs by likely review use. It does not import source rows,",
        "normalize city names, run ELS searches, compute compactness, or verify",
        "p-levels.",
        "",
        "## Summary",
        "",
        f"- Extractable rows reviewed: {values['extractable_rows_reviewed']}.",
        f"- Anchors found: {values['anchors_found']} of {values['extractable_rows_reviewed']}.",
        f"- Data-bearing candidates: {values.get('status_data_bearing_candidate', '0')}.",
        f"- Method-context candidates: {values.get('status_method_context_candidate', '0')}.",
        f"- Commentary/critique rows: {commentary_count(values)}.",
        "",
        "## Rows",
        "",
        "| Label | Source role | Data-bearing status | Anchor | Pages | Text chars | Next action | URL |",
        "| --- | --- | --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["label"]),
                    markdown_cell(row["source_role"]),
                    markdown_cell(row["data_bearing_status"]),
                    markdown_cell(row["anchor_status"] or row["anchor"]),
                    markdown_cell(row["pdf_pages"]),
                    markdown_cell(row["normalized_text_chars"]),
                    markdown_cell(row["next_action"]),
                    markdown_link("url", row["url"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "This review is planning metadata. It separates a likely data-table source",
            "candidate from method/context and commentary/critique texts. It does not",
            "decide admissibility, does not create city-name rows, and does not make a",
            "result-bearing claim.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def commentary_count(values: dict[str, str]) -> int:
    return int(values.get("status_commentary_or_perspective", "0")) + int(
        values.get("status_critique_or_response", "0")
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "queue": str(args.queue),
            "text_audit": str(args.text_audit),
            "anchors": str(args.anchors),
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary},
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
