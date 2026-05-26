#!/usr/bin/env python3
"""Classify unreadable recovered Cities PDFs by OCR/encoding review route."""

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
DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_unreadable_pdf_review.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_review_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_UNREADABLE_PDF_REVIEW.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_review.manifest.json"
)

UNREADABLE_LANES = ("ocr_image_only_pdf", "encoding_or_ocr_candidate")

FIELDNAMES = [
    "label",
    "family",
    "lane",
    "text_status",
    "pdf_pages",
    "normalized_text_chars",
    "selected_path",
    "sha256",
    "source_role_hint",
    "review_route",
    "next_action",
    "url",
    "claim_boundary",
]

SUMMARY_FIELDNAMES = ["metric", "value"]

CLAIM_BOUNDARY = (
    "unreadable-PDF planning only; no OCR output, no repaired text, no source-row import, "
    "no city normalization, no ELS, no compactness, no p-level"
)

REVIEW_ROUTES = {
    "ocr_image_only_pdf": "page_image_or_ocr_review",
    "encoding_or_ocr_candidate": "alternate_extraction_or_ocr_fallback",
}

NEXT_ACTIONS = {
    "ocr_image_only_pdf": (
        "inspect page images and run OCR before source-role classification"
    ),
    "encoding_or_ocr_candidate": (
        "try alternate extraction; if still garbled, run OCR before source-role classification"
    ),
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    queue_rows = read_csv(args.queue)
    review_rows = build_review_rows(queue_rows)
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
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_review_rows(queue_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in queue_rows:
        lane = row.get("lane", "")
        if lane not in UNREADABLE_LANES:
            continue
        rows.append(
            {
                "label": row.get("label", ""),
                "family": row.get("family", ""),
                "lane": lane,
                "text_status": row.get("text_status", ""),
                "pdf_pages": row.get("pdf_pages", ""),
                "normalized_text_chars": row.get("normalized_text_chars", ""),
                "selected_path": row.get("selected_path", ""),
                "sha256": row.get("sha256", ""),
                "source_role_hint": source_role_hint(row.get("label", "")),
                "review_route": REVIEW_ROUTES[lane],
                "next_action": NEXT_ACTIONS[lane],
                "url": row.get("url", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(rows, key=lambda row: (row["lane"], row["label"]))


def source_role_hint(label: str) -> str:
    if label == "cities_pdf_wrr":
        return "wrr_context_paper"
    if label.startswith("cities_pdf_dp365a_"):
        return "aumann_committee_recovered_segment"
    return "unclassified_unreadable_pdf"


def build_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    lanes = Counter(row["lane"] for row in rows)
    families = Counter(row["family"] for row in rows)
    total_pages = sum(int_or_zero(row["pdf_pages"]) for row in rows)
    garbled_chars = sum(
        int_or_zero(row["normalized_text_chars"])
        for row in rows
        if row["lane"] == "encoding_or_ocr_candidate"
    )
    summary = [
        {"metric": "unreadable_rows_reviewed", "value": str(len(rows))},
        {"metric": "ocr_image_only_rows", "value": str(lanes.get("ocr_image_only_pdf", 0))},
        {
            "metric": "encoding_or_ocr_candidate_rows",
            "value": str(lanes.get("encoding_or_ocr_candidate", 0)),
        },
        {"metric": "aumann_committee_rows", "value": str(families.get("aumann_committee", 0))},
        {"metric": "other_family_rows", "value": str(families.get("other", 0))},
        {"metric": "total_pages_needing_review", "value": str(total_pages)},
        {"metric": "garbled_text_chars", "value": str(garbled_chars)},
        {"metric": "claim_boundary", "value": CLAIM_BOUNDARY},
    ]
    return summary


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary: list[dict[str, str]],
) -> None:
    values = {row["metric"]: row["value"] for row in summary}
    lines = [
        "# Cities Unreadable PDF Review",
        "",
        "Status: OCR/encoding planning only. This classifies recovered Cities PDFs",
        "that are image-only or garbled by text extraction. It does not run OCR,",
        "repair text, import source rows, normalize city names, run ELS searches,",
        "compute compactness, or verify p-levels.",
        "",
        "## Summary",
        "",
        f"- Unreadable rows reviewed: {values['unreadable_rows_reviewed']}.",
        f"- OCR/image-only rows: {values['ocr_image_only_rows']}.",
        f"- Encoding-or-OCR candidate rows: {values['encoding_or_ocr_candidate_rows']}.",
        f"- Aumann committee rows: {values['aumann_committee_rows']}.",
        f"- Other-family rows: {values['other_family_rows']}.",
        f"- Pages needing review: {values['total_pages_needing_review']}.",
        f"- Garbled text chars: {values['garbled_text_chars']}.",
        "",
        "## Rows",
        "",
        "| Label | Family | Lane | Text status | Pages | Text chars | Role hint | Route | Next action | URL |",
        "| --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["label"]),
                    markdown_cell(row["family"]),
                    f"`{markdown_cell(row['lane'])}`",
                    markdown_cell(row["text_status"]),
                    markdown_cell(row["pdf_pages"]),
                    markdown_cell(row["normalized_text_chars"]),
                    markdown_cell(row["source_role_hint"]),
                    markdown_cell(row["review_route"]),
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
            "This review is planning metadata for the seven recovered but unreadable",
            "Cities PDFs. It does not repair the PDFs, create OCR text, decide source",
            "admissibility, create city-name rows, or make a result-bearing claim.",
            "Any later OCR output must be reviewed and locked before source-row",
            "normalization or ELS work.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


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
        "inputs": {"queue": str(args.queue)},
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
