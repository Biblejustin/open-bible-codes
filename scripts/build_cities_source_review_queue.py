#!/usr/bin/env python3
"""Build Cities source-review queue from recovery and text-shape audits."""

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


DEFAULT_RECOVERY = Path("reports/cities_pdf_recovery_probe/cities_pdf_recovery_probe.csv")
DEFAULT_TEXT_AUDIT = Path(
    "reports/cities_pdf_recovery_probe/cities_recovered_pdf_text_audit.csv"
)
DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_source_review_queue.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_source_review_queue_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_REVIEW_QUEUE.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_review_queue.manifest.json"
)

QUEUE_FIELDNAMES = [
    "priority_rank",
    "lane",
    "label",
    "source_pages",
    "family",
    "url",
    "usable_status",
    "archive_status",
    "archive_cdx_candidate_count",
    "selected_source",
    "selected_path",
    "pdf_pages",
    "text_status",
    "normalized_text_chars",
    "sha256",
    "review_action",
    "blocker",
    "claim_boundary",
]

SUMMARY_FIELDNAMES = [
    "lane",
    "rows",
    "families",
    "source_pages",
    "review_action",
    "claim_boundary",
]

LANE_PRIORITY = {
    "review_extractable_text": 1,
    "ocr_image_only_pdf": 2,
    "encoding_or_ocr_candidate": 3,
    "recover_missing_pdf": 4,
}

LANE_ACTIONS = {
    "review_extractable_text": (
        "review extracted text headings and table scope before any city-row normalization"
    ),
    "ocr_image_only_pdf": (
        "OCR or page-image review needed before source rows can be inspected"
    ),
    "encoding_or_ocr_candidate": (
        "try alternate extraction or OCR; current text stream is not source-ready"
    ),
    "recover_missing_pdf": (
        "manual live/archive recovery needed before text or source-row review"
    ),
}

LANE_BLOCKERS = {
    "review_extractable_text": "source review still needed",
    "ocr_image_only_pdf": "no extractable text from recovered PDF",
    "encoding_or_ocr_candidate": "pdftotext output is garbled or non-Latin",
    "recover_missing_pdf": "no usable PDF recovered",
}

CLAIM_BOUNDARY = (
    "source-review triage only; no OCR result, no city normalization, no ELS, "
    "no compactness, no p-level"
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    recovery_rows = read_csv(args.recovery)
    text_rows = {row["label"]: row for row in read_csv(args.text_audit)}
    queue_rows = build_queue(recovery_rows, text_rows)
    summary_rows = build_summary(queue_rows)
    write_csv(args.out, QUEUE_FIELDNAMES, queue_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, queue_rows, summary_rows)
    write_manifest(
        args.manifest_out,
        args,
        len(recovery_rows),
        len(text_rows),
        queue_rows,
        summary_rows,
        started,
    )
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recovery", type=Path, default=DEFAULT_RECOVERY)
    parser.add_argument("--text-audit", type=Path, default=DEFAULT_TEXT_AUDIT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_queue(
    recovery_rows: list[dict[str, str]],
    text_rows: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for recovery in recovery_rows:
        text = text_rows.get(recovery.get("label", ""), {})
        lane = classify_lane(recovery, text)
        rows.append(
            {
                "priority_rank": LANE_PRIORITY[lane],
                "lane": lane,
                "label": recovery.get("label", ""),
                "source_pages": recovery.get("source_pages", ""),
                "family": text.get("family") or family_from_source_pages(
                    recovery.get("source_pages", "")
                ),
                "url": recovery.get("url", ""),
                "usable_status": recovery.get("usable_status", ""),
                "archive_status": recovery.get("archive_status", ""),
                "archive_cdx_candidate_count": recovery.get(
                    "archive_cdx_candidate_count", ""
                ),
                "selected_source": recovery.get("selected_source", ""),
                "selected_path": recovery.get("selected_path", ""),
                "pdf_pages": text.get("pdf_pages") or recovery.get("pdf_pages", ""),
                "text_status": text.get("text_status", "not_audited"),
                "normalized_text_chars": text.get("normalized_text_chars", ""),
                "sha256": text.get("sha256") or recovery.get("archive_sha256", ""),
                "review_action": LANE_ACTIONS[lane],
                "blocker": LANE_BLOCKERS[lane],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            int(row["priority_rank"]),
            str(row["source_pages"]),
            str(row["label"]),
        ),
    )


def classify_lane(recovery: dict[str, str], text: dict[str, str]) -> str:
    if recovery.get("usable_status") == "no_pdf_recovered":
        return "recover_missing_pdf"
    status = text.get("text_status", "")
    if status == "extractable_text":
        return "review_extractable_text"
    if status == "zero_extractable_text":
        return "ocr_image_only_pdf"
    if status == "extractable_but_garbled_or_nonlatin":
        return "encoding_or_ocr_candidate"
    return "recover_missing_pdf"


def build_summary(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    by_lane = Counter(str(row["lane"]) for row in rows)
    summary: list[dict[str, str]] = []
    for lane in sorted(by_lane, key=lambda value: LANE_PRIORITY[value]):
        lane_rows = [row for row in rows if row["lane"] == lane]
        summary.append(
            {
                "lane": lane,
                "rows": str(len(lane_rows)),
                "families": summarize_values(lane_rows, "family"),
                "source_pages": summarize_values(lane_rows, "source_pages"),
                "review_action": LANE_ACTIONS[lane],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return summary


def summarize_values(rows: list[dict[str, object]], field: str) -> str:
    counts = Counter(str(row.get(field, "")) for row in rows if row.get(field, ""))
    return "; ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def family_from_source_pages(source_pages: str) -> str:
    if "gans" in source_pages:
        return "gans_communities"
    if "aumann" in source_pages:
        return "aumann_committee"
    if "simon" in source_pages or "mckay" in source_pages:
        return "simon_mckay"
    return "other"


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: list[dict[str, str]],
) -> None:
    lines = [
        "# Cities Source Review Queue",
        "",
        "Status: source-review triage only. This joins the PDF recovery probe and",
        "recovered-PDF text audit into next-action buckets. It does not run OCR,",
        "normalize city names, run ELS searches, compute compactness, or verify",
        "p-levels.",
        "",
        "## Summary",
        "",
        f"- Rows queued: {len(rows)}.",
        "",
        "| Lane | Rows | Families | Source pages | Next action |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for row in summary:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_cell(row['lane'])}`",
                    markdown_cell(row["rows"]),
                    markdown_cell(row["families"]),
                    markdown_cell(row["source_pages"]),
                    markdown_cell(row["review_action"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Queue",
            "",
            "| Priority | Lane | Label | Family | Text status | Pages | Text chars | Blocker | URL |",
            "| ---: | --- | --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["priority_rank"]),
                    f"`{markdown_cell(row['lane'])}`",
                    markdown_cell(row["label"]),
                    markdown_cell(row["family"]),
                    markdown_cell(row["text_status"]),
                    markdown_cell(row["pdf_pages"]),
                    markdown_cell(row["normalized_text_chars"]),
                    markdown_cell(row["blocker"]),
                    markdown_link("url", str(row["url"])),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "This queue is planning metadata. It does not decide source admissibility,",
            "does not create city-name rows, and does not make any result-bearing claim.",
            "Any later result protocol must separately lock source rows, normalization,",
            "filters, Genesis text, skip caps, compactness metric, and controls.",
            "",
            "The extractable-text role review in `docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md`",
            "separates the five readable PDFs into data-table, method-context, and",
            "commentary/critique lanes without changing this queue's boundary. The",
            "data-table lane now points at `docs/GANS_COMMUNITIES_SOURCE_AUDIT.md` for",
            "existing source-shape coverage only: 66 records and 210 community rows, with no",
            "source-row import.",
            "",
            "The unreadable-PDF review in `docs/CITIES_UNREADABLE_PDF_REVIEW.md` separates",
            "the seven recovered but unreadable PDFs into OCR/image-only and",
            "encoding-or-OCR routes without running OCR or repairing text.",
            "The OCR feasibility probe in `docs/CITIES_UNREADABLE_PDF_OCR_FEASIBILITY.md`",
            "records OCR count/status metrics for those same seven rows without tracking",
            "OCR text.",
            "The OCR review packet in `docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_PACKET.md`",
            "adds ignored local page-image and OCR-text sidecars and tracks only",
            "paths/counts/status before any source-row use.",
            "The OCR review checklist in `docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_CHECKLIST.md`",
            "orders those sidecars for page-image comparison and contact-sheet review.",
            "The OCR page review in `docs/CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md`",
            "records visual page-role decisions for all 41 OCR-packet pages while keeping",
            "source-row imports at zero.",
            "The source-row lock queue in `docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md`",
            "then filters those reviewed page roles to 14 table/list/exception-note",
            "candidate pages that need separate citable source-row locks before use.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    recovery_rows: int,
    text_rows: int,
    queue_rows: list[dict[str, object]],
    summary_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "recovery": str(args.recovery),
            "text_audit": str(args.text_audit),
        },
        "rows": {
            "recovery": recovery_rows,
            "text_audit": text_rows,
            "queue": len(queue_rows),
        },
        "lane_counts": {row["lane"]: row["rows"] for row in summary_rows},
        "outputs": {
            "queue": str(args.out),
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


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
