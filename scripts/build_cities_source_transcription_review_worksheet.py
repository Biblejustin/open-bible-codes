#!/usr/bin/env python3
"""Build Cities source-transcription review worksheet from locked source pages."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_EVIDENCE_PACKET = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_packet.csv"
)
DEFAULT_RECORDS = Path(
    "data/study/mappings/cities_source_transcription_decisions.csv"
)
DEFAULT_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_source_transcription_review_worksheet.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_transcription_review_worksheet.manifest.json"
)

REVIEW_STATE = "pending_readable_transcription"
REQUIRED_TRANSCRIPTION_EVIDENCE = (
    "readable Hebrew transcription plus row/column alignment evidence and "
    "explicit import decision record"
)
CLAIM_BOUNDARY = (
    "worksheet only; no OCR body text, no source-script body text, no "
    "source-row import, no city normalization, no ELS, no compactness, no p-level"
)

FIELDNAMES = [
    "transcription_rank",
    "transcription_decision_id",
    "source_lock_decision_id",
    "queue_lock_rank",
    "label",
    "page_number",
    "family",
    "page_class",
    "visual_page_role",
    "source_url",
    "selected_source",
    "selected_path",
    "source_sha256",
    "pdf_pages",
    "page_image_path",
    "lock_record_decision_status",
    "lock_record_selected_action",
    "review_state",
    "required_source_evidence",
    "required_alignment_evidence",
    "required_decision_record",
    "allowed_without_input",
    "next_manual_action",
    "source_row_import",
    "city_name_normalization",
    "els_runs",
    "compactness_runs",
    "p_levels",
    "current_transcription_status",
    "current_selected_action",
    "current_evidence_citation",
    "current_evidence_summary",
    "claim_boundary",
]

RECORD_FIELDS = [
    "transcription_decision_id",
    "source_lock_decision_id",
    "source_label",
    "page_number",
    "page_class",
    "decision_status",
    "selected_action",
    "evidence_citation",
    "evidence_summary",
    "locked_by",
    "locked_at",
    "notes",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    records = records_by_transcription_id(read_rows_if_exists(args.records_template))
    rows = build_worksheet_rows(read_rows(args.evidence_packet), records)
    write_csv(args.out, FIELDNAMES, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args.manifest_out, args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-packet", type=Path, default=DEFAULT_EVIDENCE_PACKET)
    parser.add_argument("--records-template", type=Path, default=DEFAULT_RECORDS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_worksheet_rows(
    evidence_rows: list[dict[str, str]],
    records_by_id: dict[str, dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    records = records_by_id or {}
    locked_rows = [
        row
        for row in evidence_rows
        if row.get("record_decision_status") == "locked"
        and row.get("record_selected_action") == "source_row_lock_ready"
    ]
    rows = [
        worksheet_row(index, row, records)
        for index, row in enumerate(locked_rows, start=1)
    ]
    return rows


def worksheet_row(
    index: int,
    row: dict[str, str],
    records_by_id: dict[str, dict[str, str]],
) -> dict[str, str]:
    source_lock_decision_id = row.get("decision_id", "")
    transcription_decision_id = f"cities_source_transcription_{index:03d}"
    record = records_by_id.get(transcription_decision_id, {})
    if row.get("source_row_use") != "no_source_row_use":
        raise ValueError(f"{source_lock_decision_id} allows source-row use")
    if row.get("current_decision") != "no_source_row_import":
        raise ValueError(f"{source_lock_decision_id} imports source rows")
    return {
        "transcription_rank": str(index),
        "transcription_decision_id": transcription_decision_id,
        "source_lock_decision_id": source_lock_decision_id,
        "queue_lock_rank": row.get("queue_lock_rank", ""),
        "label": row.get("label", ""),
        "page_number": row.get("page_number", ""),
        "family": row.get("family", ""),
        "page_class": row.get("page_class", ""),
        "visual_page_role": row.get("visual_page_role", ""),
        "source_url": row.get("source_url", ""),
        "selected_source": row.get("selected_source", ""),
        "selected_path": row.get("selected_path", ""),
        "source_sha256": row.get("source_sha256", ""),
        "pdf_pages": row.get("pdf_pages", ""),
        "page_image_path": row.get("page_image_path", ""),
        "lock_record_decision_status": row.get("record_decision_status", ""),
        "lock_record_selected_action": row.get("record_selected_action", ""),
        "review_state": REVIEW_STATE,
        "required_source_evidence": required_source_evidence(row),
        "required_alignment_evidence": REQUIRED_TRANSCRIPTION_EVIDENCE,
        "required_decision_record": required_decision_record(row),
        "allowed_without_input": "organize transcription review only",
        "next_manual_action": next_manual_action(row.get("page_class", "")),
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "current_transcription_status": record.get("decision_status", "").strip()
        or "unrecorded",
        "current_selected_action": record.get("selected_action", ""),
        "current_evidence_citation": record.get("evidence_citation", ""),
        "current_evidence_summary": record.get("evidence_summary", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def required_source_evidence(row: dict[str, str]) -> str:
    return (
        "cite archived PDF checksum, rendered page image, visual page role, "
        f"and readable source-row transcription evidence for {row.get('decision_id', '')}"
    )


def required_decision_record(row: dict[str, str]) -> str:
    return (
        "record explicit import, exclude, or defer decision for "
        f"{row.get('decision_id', '')} before any source row changes"
    )


def next_manual_action(page_class: str) -> str:
    return {
        "table_candidate_page": (
            "prepare row/column transcription plan before importing table rows"
        ),
        "source_list_candidate_page": (
            "prepare source-list transcription plan before importing list rows"
        ),
        "exception_note_candidate_page": (
            "prepare exception-note interpretation plan before changing source rows"
        ),
    }.get(page_class, "prepare readable transcription plan before source-row use")


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    class_counts = Counter(row["page_class"] for row in rows)
    status_counts = Counter(row["current_transcription_status"] for row in rows)
    lines = [
        "# Cities Source Transcription Review Worksheet",
        "",
        "Status: no-input worksheet for future Cities source-row transcription review.",
        "It organizes locked source pages for later readable transcription review but does not transcribe rows or import source rows.",
        "No OCR body text or source-script body text appears in this doc, CSV, or manifest.",
        CLAIM_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_transcription_review_worksheet "
            f"--evidence-packet {args.evidence_packet} "
            f"--records-template {args.records_template} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Rows needing transcription review: {len(rows)}.",
        f"- Locked source pages: {locked_source_pages(rows)}.",
        f"- Table-bearing candidate pages: {class_counts['table_candidate_page']}.",
        f"- Source-list candidate pages: {class_counts['source_list_candidate_page']}.",
        f"- Exception-note candidate pages: {class_counts['exception_note_candidate_page']}.",
        f"- Target records file: `{args.records_template}`.",
        f"- Transcription decision rows recorded: {recorded_rows(rows)}.",
        f"- Unrecorded transcription decision rows: {status_counts['unrecorded']}.",
        f"- Review state: `{REVIEW_STATE}`.",
        "- Source-row imports: 0.",
        "- City-name normalization: 0.",
        "- ELS runs: 0.",
        "- Compactness runs: 0.",
        "- p-levels: 0.",
        f"- Required evidence: {REQUIRED_TRANSCRIPTION_EVIDENCE}.",
        "",
        "## Decision Record Fields",
        "",
        "`" + ",".join(RECORD_FIELDS) + "`",
        "",
        "## Worksheet",
        "",
        "| Rank | Transcription id | Source-lock id | Label | Page | Class | Role | State | Next manual action |",
        "| ---: | --- | --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["transcription_rank"]),
                    f"`{markdown_cell(row['transcription_decision_id'])}`",
                    f"`{markdown_cell(row['source_lock_decision_id'])}`",
                    markdown_cell(row["label"]),
                    markdown_cell(row["page_number"]),
                    f"`{markdown_cell(row['page_class'])}`",
                    f"`{markdown_cell(row['visual_page_role'])}`",
                    f"`{markdown_cell(row['review_state'])}`",
                    markdown_cell(row["next_manual_action"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This worksheet organizes review work only.",
            "- Locked source pages are not source rows.",
            "- A future decision record must cite readable transcription and row/column alignment evidence before any source row can be imported.",
            "- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    status_counts = Counter(row["current_transcription_status"] for row in rows)
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "evidence_packet": str(args.evidence_packet),
            "records_template": str(args.records_template),
        },
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "locked_source_pages": locked_source_pages(rows),
        "class_counts": dict(Counter(row["page_class"] for row in rows)),
        "transcription_record_status_counts": dict(status_counts),
        "recorded_rows": recorded_rows(rows),
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
        "review_state": REVIEW_STATE,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def locked_source_pages(rows: list[dict[str, str]]) -> int:
    return sum(
        1
        for row in rows
        if row.get("lock_record_decision_status") == "locked"
        and row.get("lock_record_selected_action") == "source_row_lock_ready"
    )


def recorded_rows(rows: list[dict[str, str]]) -> int:
    return sum(
        1
        for row in rows
        if row.get("current_transcription_status") != "unrecorded"
    )


def records_by_transcription_id(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, str]]:
    return {row["transcription_decision_id"]: row for row in rows if row.get("transcription_decision_id")}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_rows_if_exists(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_rows(path)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
