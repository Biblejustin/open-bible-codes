#!/usr/bin/env python3
"""Build a consolidated Cities no-input handoff status packet."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_QUEUE_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_queue_summary.csv"
)
DEFAULT_EVIDENCE_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_summary.csv"
)
DEFAULT_ROW_LOCK_DECISIONS = Path(
    "data/study/mappings/cities_source_row_lock_decisions.csv"
)
DEFAULT_TRANSCRIPTION_WORKSHEET = Path(
    "reports/cities_pdf_recovery_probe/cities_source_transcription_review_worksheet.csv"
)
DEFAULT_TRANSCRIPTION_DECISIONS = Path(
    "data/study/mappings/cities_source_transcription_decisions.csv"
)
DEFAULT_PAGE_BUNDLE_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_review_bundle_summary.csv"
)
DEFAULT_OCR_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_packet_summary.csv"
)
DEFAULT_LINE_CROP_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet_summary.csv"
)
DEFAULT_PRIORITY_CONTACT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_contact_sheet_summary.csv"
)
DEFAULT_PRIORITY_REVIEW_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_worksheet_summary.csv"
)
DEFAULT_OUT = Path("reports/cities_no_input_handoff_status/status.csv")
DEFAULT_SUMMARY_OUT = Path("reports/cities_no_input_handoff_status/summary.csv")
DEFAULT_MD = Path("docs/CITIES_NO_INPUT_HANDOFF_STATUS.md")
DEFAULT_MANIFEST = Path("reports/cities_no_input_handoff_status/manifest.json")

STATUS_FIELDNAMES = [
    "status_id",
    "area",
    "current_status",
    "current_value",
    "handoff_ready",
    "manual_input_needed",
    "next_action",
    "boundary",
    "source",
]
SUMMARY_FIELDNAMES = [
    "status_rows",
    "handoff_ready_rows",
    "manual_input_needed_rows",
    "queue_rows",
    "evidence_rows",
    "source_row_lock_decision_rows",
    "locked_source_row_lock_decisions",
    "transcription_review_rows",
    "transcription_decision_rows",
    "pending_transcription_rows",
    "page_review_bundle_rows",
    "page_images_found",
    "ocr_review_rows",
    "ocr_pages_with_text",
    "ocr_text_sidecars",
    "ocr_hebrew_letters",
    "line_crop_rows",
    "line_crops_available",
    "line_crop_ocr_words",
    "line_crop_hebrew_letters",
    "priority_review_rows",
    "priority_contact_sheets",
    "priority_contact_sheets_available",
    "priority_dense_text_rows",
    "priority_medium_text_rows",
    "priority_short_text_rows",
    "bucket_likely_row_or_header",
    "bucket_short_label_or_marker",
    "source_row_imports",
    "city_name_normalization",
    "els_runs",
    "compactness_runs",
    "p_levels",
    "result_allowed",
    "claim_status",
]

CLAIM_BOUNDARY = "cities_no_input_handoff_blocks_source_import_and_results"


class LoadedInputs:
    def __init__(
        self,
        *,
        queue_summary: list[dict[str, str]],
        evidence_summary: list[dict[str, str]],
        row_lock_decisions: list[dict[str, str]],
        transcription_worksheet: list[dict[str, str]],
        transcription_decisions: list[dict[str, str]],
        page_bundle_summary: list[dict[str, str]],
        ocr_summary: list[dict[str, str]],
        line_crop_summary: list[dict[str, str]],
        priority_contact_summary: list[dict[str, str]],
        priority_review_summary: list[dict[str, str]],
    ) -> None:
        self.queue_summary = queue_summary
        self.evidence_summary = evidence_summary
        self.row_lock_decisions = row_lock_decisions
        self.transcription_worksheet = transcription_worksheet
        self.transcription_decisions = transcription_decisions
        self.page_bundle_summary = page_bundle_summary
        self.ocr_summary = ocr_summary
        self.line_crop_summary = line_crop_summary
        self.priority_contact_summary = priority_contact_summary
        self.priority_review_summary = priority_review_summary


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    inputs = LoadedInputs(
        queue_summary=read_rows(args.queue_summary),
        evidence_summary=read_rows(args.evidence_summary),
        row_lock_decisions=read_rows(args.row_lock_decisions),
        transcription_worksheet=read_rows(args.transcription_worksheet),
        transcription_decisions=read_rows(args.transcription_decisions),
        page_bundle_summary=read_rows(args.page_bundle_summary),
        ocr_summary=read_rows(args.ocr_summary),
        line_crop_summary=read_rows(args.line_crop_summary),
        priority_contact_summary=read_rows(args.priority_contact_summary),
        priority_review_summary=read_rows(args.priority_review_summary),
    )
    summary = build_summary(inputs)
    rows = build_status_rows(summary, args)
    write_csv(args.out, STATUS_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, rows)
    write_manifest(args.manifest_out, args, summary, rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue-summary", type=Path, default=DEFAULT_QUEUE_SUMMARY)
    parser.add_argument("--evidence-summary", type=Path, default=DEFAULT_EVIDENCE_SUMMARY)
    parser.add_argument(
        "--row-lock-decisions", type=Path, default=DEFAULT_ROW_LOCK_DECISIONS
    )
    parser.add_argument(
        "--transcription-worksheet", type=Path, default=DEFAULT_TRANSCRIPTION_WORKSHEET
    )
    parser.add_argument(
        "--transcription-decisions", type=Path, default=DEFAULT_TRANSCRIPTION_DECISIONS
    )
    parser.add_argument(
        "--page-bundle-summary", type=Path, default=DEFAULT_PAGE_BUNDLE_SUMMARY
    )
    parser.add_argument("--ocr-summary", type=Path, default=DEFAULT_OCR_SUMMARY)
    parser.add_argument(
        "--line-crop-summary", type=Path, default=DEFAULT_LINE_CROP_SUMMARY
    )
    parser.add_argument(
        "--priority-contact-summary",
        type=Path,
        default=DEFAULT_PRIORITY_CONTACT_SUMMARY,
    )
    parser.add_argument(
        "--priority-review-summary",
        type=Path,
        default=DEFAULT_PRIORITY_REVIEW_SUMMARY,
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_summary(inputs: LoadedInputs) -> dict[str, Any]:
    queue = metric_dict(inputs.queue_summary)
    evidence = metric_dict(inputs.evidence_summary)
    bundle = metric_dict(inputs.page_bundle_summary)
    ocr = metric_dict(inputs.ocr_summary)
    line_crop = metric_dict(inputs.line_crop_summary)
    priority_contact = metric_dict(inputs.priority_contact_summary)
    priority_review = metric_dict(inputs.priority_review_summary)
    row_lock_statuses = Counter(
        row.get("decision_status", "") for row in inputs.row_lock_decisions
    )
    transcription_statuses = Counter(
        row.get("current_transcription_status", "")
        for row in inputs.transcription_worksheet
    )
    return {
        "status_rows": 8,
        "handoff_ready_rows": 8,
        "manual_input_needed_rows": 6,
        "queue_rows": int_or_zero(queue.get("queue_rows")),
        "evidence_rows": int_or_zero(evidence.get("evidence_rows")),
        "source_row_lock_decision_rows": len(inputs.row_lock_decisions),
        "locked_source_row_lock_decisions": row_lock_statuses.get("locked", 0),
        "transcription_review_rows": len(inputs.transcription_worksheet),
        "transcription_decision_rows": len(inputs.transcription_decisions),
        "pending_transcription_rows": transcription_statuses.get("unrecorded", 0),
        "page_review_bundle_rows": int_or_zero(bundle.get("bundle_rows")),
        "page_images_found": int_or_zero(bundle.get("page_images_found")),
        "ocr_review_rows": int_or_zero(ocr.get("source_page_ocr_rows")),
        "ocr_pages_with_text": int_or_zero(ocr.get("pages_with_ocr_text")),
        "ocr_text_sidecars": int_or_zero(ocr.get("ocr_text_sidecars")),
        "ocr_hebrew_letters": int_or_zero(ocr.get("ocr_hebrew_letters")),
        "line_crop_rows": int_or_zero(line_crop.get("line_crop_rows")),
        "line_crops_available": int_or_zero(line_crop.get("line_crops_available")),
        "line_crop_ocr_words": int_or_zero(line_crop.get("ocr_words")),
        "line_crop_hebrew_letters": int_or_zero(line_crop.get("ocr_hebrew_letters")),
        "priority_review_rows": int_or_zero(priority_review.get("priority_review_rows")),
        "priority_contact_sheets": int_or_zero(priority_contact.get("priority_sheets")),
        "priority_contact_sheets_available": int_or_zero(
            priority_contact.get("priority_sheets_available")
        ),
        "priority_dense_text_rows": int_or_zero(
            priority_review.get("priority_1_dense_text")
        ),
        "priority_medium_text_rows": int_or_zero(
            priority_review.get("priority_2_medium_text")
        ),
        "priority_short_text_rows": int_or_zero(
            priority_review.get("priority_3_short_text")
        ),
        "bucket_likely_row_or_header": int_or_zero(
            priority_review.get("bucket_likely_row_or_header")
        ),
        "bucket_short_label_or_marker": int_or_zero(
            priority_review.get("bucket_short_label_or_marker")
        ),
        "source_row_imports": int_or_zero(evidence.get("source_row_imports")),
        "city_name_normalization": int_or_zero(bundle.get("city_name_normalization")),
        "els_runs": int_or_zero(evidence.get("els_runs")),
        "compactness_runs": int_or_zero(evidence.get("compactness_runs")),
        "p_levels": int_or_zero(bundle.get("p_levels")),
        "result_allowed": False,
        "claim_status": CLAIM_BOUNDARY,
    }


def build_status_rows(
    summary: dict[str, Any], args: argparse.Namespace
) -> list[dict[str, str]]:
    return [
        status_row(
            "source_row_lock_queue",
            "source-row lock queue",
            "locked_review_inventory",
            (
                f"{summary['queue_rows']} queue rows; "
                f"{summary['evidence_rows']} evidence rows"
            ),
            "yes",
            "no",
            "keep queue aligned to evidence packet and decision records",
            "queue identifies source pages only; no source rows imported",
            args.queue_summary,
        ),
        status_row(
            "source_row_lock_decisions",
            "source-row lock decisions",
            "locked_page_level_evidence",
            (
                f"{summary['source_row_lock_decision_rows']} decision rows; "
                f"{summary['locked_source_row_lock_decisions']} locked"
            ),
            "yes",
            "no",
            "preserve page-level locks and require separate transcription before import",
            "page lock is not row transcription or source-row import",
            args.row_lock_decisions,
        ),
        status_row(
            "transcription_review",
            "readable transcription review",
            "pending_manual_transcription",
            (
                f"{summary['transcription_review_rows']} worksheet rows; "
                f"{summary['pending_transcription_rows']} pending; "
                f"{summary['transcription_decision_rows']} decision rows"
            ),
            "yes",
            "yes",
            "capture readable row and column evidence before any source-row decision",
            "no verified source-row text is in tracked outputs",
            args.transcription_worksheet,
        ),
        status_row(
            "page_review_bundle",
            "page-image review bundle",
            "visual_review_aid_only",
            (
                f"{summary['page_review_bundle_rows']} bundle rows; "
                f"{summary['page_images_found']} page images found"
            ),
            "yes",
            "yes",
            "use page images only as evidence pointers for future human review",
            "page images do not authorize city-name normalization or ELS",
            args.page_bundle_summary,
        ),
        status_row(
            "local_ocr_review_aids",
            "local OCR review aids",
            "ignored_local_review_aids",
            (
                f"{summary['ocr_review_rows']} OCR rows; "
                f"{summary['ocr_pages_with_text']} pages with text; "
                f"{summary['ocr_text_sidecars']} ignored sidecars"
            ),
            "yes",
            "yes",
            "review OCR only as local aid; do not promote it to source rows",
            "OCR body text is not tracked and is not source-row evidence by itself",
            args.ocr_summary,
        ),
        status_row(
            "line_crop_review_aids",
            "line-crop review aids",
            "ignored_local_review_aids",
            (
                f"{summary['line_crop_rows']} crop rows; "
                f"{summary['line_crops_available']} images; "
                f"{summary['line_crop_ocr_words']} OCR words"
            ),
            "yes",
            "yes",
            "use crop images to focus future row/column review",
            "line crops do not verify source rows or permit ELS",
            args.line_crop_summary,
        ),
        status_row(
            "priority_review_queue",
            "priority line-crop review",
            "pending_manual_review",
            (
                f"{summary['priority_review_rows']} priority rows; "
                f"{summary['priority_dense_text_rows']} dense; "
                f"{summary['priority_medium_text_rows']} medium; "
                f"{summary['priority_short_text_rows']} short"
            ),
            "yes",
            "yes",
            "review likely rows and headers before any transcription decision",
            "priority rank is a review order, not a source-use decision",
            args.priority_review_summary,
        ),
        status_row(
            "result_boundary",
            "result boundary",
            "blocked",
            (
                f"source-row imports {summary['source_row_imports']}; "
                f"city normalization {summary['city_name_normalization']}; "
                f"ELS runs {summary['els_runs']}; "
                f"compactness {summary['compactness_runs']}; "
                f"p-levels {summary['p_levels']}; "
                f"result allowed {int(bool(summary['result_allowed']))}"
            ),
            "yes",
            "yes",
            "wait for verified source rows, normalization rules, preregistration, and controls",
            "no Cities source-row import, ELS run, compactness run, or p-level exists",
            args.evidence_summary,
        ),
    ]


def write_markdown(
    path: Path, summary: dict[str, Any], rows: list[dict[str, str]]
) -> None:
    lines = [
        "# Cities No-Input Handoff Status",
        "",
        "Status: consolidated Cities no-input handoff.",
        "",
        "This is not a source-row import, not city-name normalization, not an ELS run, not a compactness run, not a p-level, and not a Cities result.",
        "It gathers the current Cities source-row queue, source-row lock decisions, transcription worksheet, page-image bundle, OCR review aids, and line-crop review aids into one guarded handoff.",
        "It exists so future work starts from one status file without treating local review aids as result-bearing source data.",
        "",
        "## Summary",
        "",
        f"- Status rows: {summary['status_rows']}.",
        f"- Handoff-ready rows: {summary['handoff_ready_rows']}.",
        f"- Manual-input-needed rows: {summary['manual_input_needed_rows']}.",
        f"- Queue rows: {summary['queue_rows']}.",
        f"- Evidence rows: {summary['evidence_rows']}.",
        f"- Source-row lock decision rows: {summary['source_row_lock_decision_rows']}.",
        f"- Locked source-row lock decisions: {summary['locked_source_row_lock_decisions']}.",
        f"- Transcription review rows: {summary['transcription_review_rows']}.",
        f"- Pending transcription rows: {summary['pending_transcription_rows']}.",
        f"- Transcription decision rows: {summary['transcription_decision_rows']}.",
        f"- Page review bundle rows: {summary['page_review_bundle_rows']}.",
        f"- Page images found: {summary['page_images_found']}.",
        f"- OCR review rows: {summary['ocr_review_rows']}.",
        f"- OCR pages with text: {summary['ocr_pages_with_text']}.",
        f"- OCR text sidecars: {summary['ocr_text_sidecars']}.",
        f"- OCR Hebrew letters: {summary['ocr_hebrew_letters']}.",
        f"- Line crop rows: {summary['line_crop_rows']}.",
        f"- Line crops available: {summary['line_crops_available']}.",
        f"- Line crop OCR words: {summary['line_crop_ocr_words']}.",
        f"- Line crop Hebrew letters: {summary['line_crop_hebrew_letters']}.",
        f"- Priority review rows: {summary['priority_review_rows']}.",
        f"- Priority contact sheets: {summary['priority_contact_sheets']}.",
        f"- Priority contact sheets available: {summary['priority_contact_sheets_available']}.",
        f"- Dense-text priority rows: {summary['priority_dense_text_rows']}.",
        f"- Medium-text priority rows: {summary['priority_medium_text_rows']}.",
        f"- Short-text priority rows: {summary['priority_short_text_rows']}.",
        f"- Likely row/header bucket rows: {summary['bucket_likely_row_or_header']}.",
        f"- Short label/marker bucket rows: {summary['bucket_short_label_or_marker']}.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- City-name normalization: {summary['city_name_normalization']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- P-levels: {summary['p_levels']}.",
        f"- Result allowed: {int(bool(summary['result_allowed']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Handoff Rows",
        "",
        "| Status id | Area | Status | Value | Manual input | Boundary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['status_id']}` | {row['area']} | `{row['current_status']}` | {row['current_value']} | `{row['manual_input_needed']}` | {row['boundary']} |"
        )
    lines.extend(
        [
            "",
            "## Next Work",
            "",
            "The no-input path can keep queue counts, page evidence, review aids, and public boundary language aligned.",
            "It cannot read Hebrew for the project, verify row transcription, import source rows, normalize city names, run ELS searches, compute compactness, or report p-levels.",
            "A future Cities result remains blocked until readable source rows, import decisions, normalization rules, preregistration, and controls are locked.",
            "",
            "## Cautions",
            "",
            "- This handoff is a map of remaining work, not a Cities experiment result.",
            "- Local OCR and crop images are review aids only; they are not source rows.",
            "- Page-level source locks do not decide row text, row inclusion, or city-name spelling.",
            "- No Cities source-row import, ELS run, compactness run, or p-level is present in this packet.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, Any],
    rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.build_cities_no_input_handoff_status",
        "claim_boundary": "Cities no-input handoff only; no source import or result",
        "text_retention": "no OCR body text or source-script body text written to tracked outputs",
        "summary": summary,
        "status_rows": len(rows),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "queue_summary": str(args.queue_summary),
            "evidence_summary": str(args.evidence_summary),
            "row_lock_decisions": str(args.row_lock_decisions),
            "transcription_worksheet": str(args.transcription_worksheet),
            "transcription_decisions": str(args.transcription_decisions),
            "page_bundle_summary": str(args.page_bundle_summary),
            "ocr_summary": str(args.ocr_summary),
            "line_crop_summary": str(args.line_crop_summary),
            "priority_contact_summary": str(args.priority_contact_summary),
            "priority_review_summary": str(args.priority_review_summary),
        },
        "outputs": {
            "status": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def status_row(
    status_id: str,
    area: str,
    current_status: str,
    current_value: str,
    handoff_ready: str,
    manual_input_needed: str,
    next_action: str,
    boundary: str,
    source: Path,
) -> dict[str, str]:
    return {
        "status_id": status_id,
        "area": area,
        "current_status": current_status,
        "current_value": current_value,
        "handoff_ready": handoff_ready,
        "manual_input_needed": manual_input_needed,
        "next_action": next_action,
        "boundary": boundary,
        "source": str(source),
    }


def metric_dict(rows: list[dict[str, str]]) -> dict[str, str]:
    return {row.get("metric", ""): row.get("value", "") for row in rows}


def int_or_zero(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
