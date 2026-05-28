#!/usr/bin/env python3
"""Build Cities source-row lock evidence packet from worksheet rows."""

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


DEFAULT_WORKSHEET = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_worksheet.csv"
)
DEFAULT_SOURCE_QUEUE = Path("reports/cities_pdf_recovery_probe/cities_source_review_queue.csv")
DEFAULT_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_packet.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_packet.manifest.json"
)

CLAIM_BOUNDARY = (
    "diagnostic evidence packet only; no OCR body text, no source-row "
    "transcription, no source-row import, no city normalization, no ELS, no "
    "compactness, no p-level"
)

FIELDNAMES = [
    "evidence_rank",
    "decision_id",
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
    "record_decision_status",
    "record_selected_action",
    "evidence_prompt",
    "evidence_required",
    "source_row_use",
    "current_decision",
    "claim_boundary",
]

SUMMARY_FIELDNAMES = [
    "metric",
    "value",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    worksheet_rows = read_rows(args.worksheet)
    source_rows = read_rows(args.source_queue)
    packet_rows = build_packet_rows(worksheet_rows, source_rows)
    summary_rows = build_summary_rows(packet_rows)
    write_csv(args.out, FIELDNAMES, packet_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, packet_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, packet_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worksheet", type=Path, default=DEFAULT_WORKSHEET)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_packet_rows(
    worksheet_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_by_label = {row.get("label", ""): row for row in source_rows}
    rows: list[dict[str, str]] = []
    for row in worksheet_rows:
        source = source_by_label.get(row.get("label", ""), {})
        if row.get("source_row_use") != "no_source_row_use":
            raise ValueError(f"{row.get('decision_id', '')} allows source-row use")
        if row.get("current_decision") != "no_source_row_import":
            raise ValueError(f"{row.get('decision_id', '')} imports source rows")
        rows.append(
            {
                "evidence_rank": "0",
                "decision_id": row.get("decision_id", ""),
                "queue_lock_rank": row.get("queue_lock_rank", ""),
                "label": row.get("label", ""),
                "page_number": row.get("page_number", ""),
                "family": row.get("family", ""),
                "page_class": row.get("page_class", ""),
                "visual_page_role": row.get("visual_page_role", ""),
                "source_url": source.get("url", ""),
                "selected_source": source.get("selected_source", ""),
                "selected_path": source.get("selected_path", ""),
                "source_sha256": source.get("sha256", ""),
                "pdf_pages": source.get("pdf_pages", ""),
                "page_image_path": row.get("page_image_path", ""),
                "record_decision_status": row.get("record_decision_status", ""),
                "record_selected_action": row.get("record_selected_action", ""),
                "evidence_prompt": row.get("evidence_prompt", ""),
                "evidence_required": evidence_required(row),
                "source_row_use": row.get("source_row_use", ""),
                "current_decision": row.get("current_decision", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.sort(key=lambda row: int_or_zero(row["queue_lock_rank"]))
    for index, row in enumerate(rows, start=1):
        row["evidence_rank"] = str(index)
    return rows


def evidence_required(row: dict[str, str]) -> str:
    return (
        "verify archived PDF checksum, rendered page image, visual page role, "
        f"and admissibility for {row.get('decision_id', '')}; do not transcribe body text"
    )


def build_summary_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    class_counts = Counter(row["page_class"] for row in rows)
    return [
        metric("evidence_rows", len(rows)),
        metric("unique_labels", len({row["label"] for row in rows})),
        metric("table_candidate_pages", class_counts["table_candidate_page"]),
        metric("source_list_candidate_pages", class_counts["source_list_candidate_page"]),
        metric("exception_note_candidate_pages", class_counts["exception_note_candidate_page"]),
        metric("recorded_decision_rows", count_recorded(rows)),
        metric("source_row_imports", count_imports(rows)),
        metric("els_runs", 0),
        metric("compactness_runs", 0),
        metric("claim_boundary", CLAIM_BOUNDARY),
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Source Row Lock Evidence Packet",
        "",
        "Status: diagnostic evidence packet for Cities source-row lock candidates.",
        "It joins decision ids to PDF/source metadata and page-image paths without OCR body text.",
        "It does not transcribe rows, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "No OCR body text or source-script body text appears in this doc, CSV, summary, or manifest.",
        "The local checker verifies every packet row points to an existing recovered PDF and page-image artifact.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_row_lock_evidence_packet "
            f"--worksheet {args.worksheet} "
            f"--source-queue {args.source_queue} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Evidence rows: {summary['evidence_rows']}.",
        f"- Unique labels: {summary['unique_labels']}.",
        f"- Table-bearing candidate pages: {summary['table_candidate_pages']}.",
        f"- Source-list candidate pages: {summary['source_list_candidate_pages']}.",
        f"- Exception-note candidate pages: {summary['exception_note_candidate_pages']}.",
        f"- Recorded decision rows: {summary['recorded_decision_rows']}.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- Boundary: {CLAIM_BOUNDARY}",
        "",
        "## Evidence Rows",
        "",
        "| Rank | Decision id | Label | Page | Class | Source | SHA256 | Page image | Record status | Evidence required |",
        "| ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["evidence_rank"]),
                    f"`{markdown_cell(row['decision_id'])}`",
                    markdown_cell(row["label"]),
                    markdown_cell(row["page_number"]),
                    f"`{markdown_cell(row['page_class'])}`",
                    markdown_cell(row["selected_source"]),
                    f"`{markdown_cell(row['source_sha256'][:12])}`",
                    f"`{markdown_cell(row['page_image_path'])}`",
                    f"`{markdown_cell(row['record_decision_status'])}`",
                    markdown_cell(row["evidence_required"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This packet collects evidence locations only.",
            "- Page images and recovered PDFs remain supporting artifacts; this doc does not copy their body text.",
            "- A future decision record must cite page evidence before any source rows can be imported.",
            "- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "worksheet": str(args.worksheet),
            "source_queue": str(args.source_queue),
        },
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "source_row_imports": count_imports(rows),
        "els_runs": 0,
        "compactness_runs": 0,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_recorded(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if row.get("record_decision_status") != "unrecorded")


def count_imports(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if row.get("source_row_use") != "no_source_row_use")


def metric(name: str, value: object) -> dict[str, str]:
    return {"metric": name, "value": str(value)}


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def read_rows(path: Path) -> list[dict[str, str]]:
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
