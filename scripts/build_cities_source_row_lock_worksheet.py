#!/usr/bin/env python3
"""Build Cities source-row lock worksheet with current record status."""

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


DEFAULT_QUEUE = Path("reports/cities_pdf_recovery_probe/cities_source_row_lock_queue.csv")
DEFAULT_RECORDS = Path("data/study/mappings/cities_source_row_lock_decisions.csv")
DEFAULT_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_worksheet.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_ROW_LOCK_WORKSHEET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_worksheet.manifest.json"
)

CLAIM_BOUNDARY = (
    "worksheet only; no OCR body text, no source-row transcription, no "
    "source-row import, no city normalization, no ELS, no compactness, no p-level"
)

FIELDNAMES = [
    "worksheet_rank",
    "decision_id",
    "queue_lock_rank",
    "label",
    "page_number",
    "family",
    "page_class",
    "visual_page_role",
    "page_image_path",
    "required_decision_record",
    "evidence_prompt",
    "suggested_decision_status_values",
    "suggested_selected_action_values",
    "current_lock_status",
    "source_row_use",
    "current_decision",
    "record_decision_status",
    "record_selected_action",
    "record_locked_by",
    "record_locked_at",
    "record_evidence_citation",
    "record_evidence_summary",
    "claim_boundary",
]

RECORD_FIELDS = [
    "decision_id",
    "queue_lock_rank",
    "label",
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
    records = records_by_decision_id(read_rows_if_exists(args.records_template))
    rows = build_worksheet_rows(read_rows(args.queue), records)
    write_csv(args.out, FIELDNAMES, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args.manifest_out, args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--records-template", type=Path, default=DEFAULT_RECORDS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_worksheet_rows(
    queue_rows: list[dict[str, str]],
    record_by_id: dict[str, dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    records = record_by_id or {}
    rows = [worksheet_row(row, records) for row in queue_rows]
    for index, row in enumerate(rows, start=1):
        row["worksheet_rank"] = str(index)
    return rows


def worksheet_row(
    row: dict[str, str],
    record_by_id: dict[str, dict[str, str]],
) -> dict[str, str]:
    lock_rank = int(row.get("lock_rank", "0"))
    decision_id = f"cities_source_row_lock_{lock_rank:03d}"
    record = record_by_id.get(decision_id, {})
    return {
        "worksheet_rank": "0",
        "decision_id": decision_id,
        "queue_lock_rank": str(lock_rank),
        "label": row.get("label", ""),
        "page_number": row.get("page_number", ""),
        "family": row.get("family", ""),
        "page_class": row.get("page_class", ""),
        "visual_page_role": row.get("visual_page_role", ""),
        "page_image_path": row.get("page_image_path", ""),
        "required_decision_record": required_decision_record(row),
        "evidence_prompt": evidence_prompt(row.get("page_class", "")),
        "suggested_decision_status_values": suggested_status_values(),
        "suggested_selected_action_values": suggested_action_values(),
        "current_lock_status": row.get("lock_status", ""),
        "source_row_use": row.get("source_row_use", ""),
        "current_decision": row.get("current_decision", ""),
        "record_decision_status": record.get("decision_status", "").strip()
        or "unrecorded",
        "record_selected_action": record.get("selected_action", ""),
        "record_locked_by": record.get("locked_by", ""),
        "record_locked_at": record.get("locked_at", ""),
        "record_evidence_citation": record.get("evidence_citation", ""),
        "record_evidence_summary": record.get("evidence_summary", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def required_decision_record(row: dict[str, str]) -> str:
    return (
        "cite PDF/page evidence, page role, and admissibility decision before "
        f"{row.get('label', '')} p{row.get('page_number', '')} can feed source rows"
    )


def evidence_prompt(page_class: str) -> str:
    return {
        "table_candidate_page": (
            "cite PDF/archive checksum, page image, table scope, and row/column boundary method; do not transcribe row text here"
        ),
        "source_list_candidate_page": (
            "cite PDF/archive checksum, page image, and list scope; do not transcribe list rows here"
        ),
        "exception_note_candidate_page": (
            "cite PDF/archive checksum, page image, and note scope; decide future source-row effect without body text here"
        ),
    }.get(page_class, "cite page evidence before any source-row lock")


def suggested_status_values() -> str:
    return ";".join(["unrecorded", "locked", "deferred_no_lock"])


def suggested_action_values() -> str:
    return ";".join(
        [
            "no_source_row_import",
            "source_row_lock_ready",
            "exclude_page_from_source_rows",
            "deferred_no_lock",
        ]
    )


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    class_counts = Counter(row["page_class"] for row in rows)
    status_counts = Counter(row["record_decision_status"] for row in rows)
    action_counts = Counter(
        row["record_selected_action"] for row in rows if row["record_selected_action"]
    )
    recorded_count = sum(1 for row in rows if row["record_decision_status"] != "unrecorded")
    lines = [
        "# Cities Source Row Lock Worksheet",
        "",
        "Status: worksheet plus current Cities source-row lock decision-record status.",
        "It reads the source-row lock queue and optional decision records but does not update either file.",
        "No OCR body text or source-script body text appears in this doc, CSV, or manifest.",
        CLAIM_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_row_lock_worksheet "
            f"--queue {args.queue} "
            f"--records-template {args.records_template} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Worksheet rows: {len(rows)}.",
        f"- Table-bearing candidate pages: {class_counts['table_candidate_page']}.",
        f"- Source-list candidate pages: {class_counts['source_list_candidate_page']}.",
        f"- Exception-note candidate pages: {class_counts['exception_note_candidate_page']}.",
        f"- Target records file: `{args.records_template}`.",
        f"- Recorded decision rows: {recorded_count}.",
        f"- Locked decision rows: {status_counts['locked']}.",
        f"- Unrecorded decision rows: {status_counts['unrecorded']}.",
        f"- Source-row imports: {count_imports(rows)}.",
        "- ELS runs: 0.",
        "- Compactness runs: 0.",
        f"- Recorded selected actions: {format_counter(action_counts)}.",
        "",
        "## Lock Row Fields",
        "",
        "`" + ",".join(RECORD_FIELDS) + "`",
        "",
        "The worksheet gives exact `decision_id`, queue fields, evidence prompts, and current record fields when a lock row exists.",
        "A future lock row may mark a page ready for source-row work, but this worksheet itself never imports or transcribes source rows.",
        "`docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md` joins these decision ids to recovered PDF metadata and page-image paths without source text.",
        "",
        "## Worksheet",
        "",
        "| Decision id | Rank | Label | Page | Class | Role | Record status | Recorded action | Evidence prompt | Suggested actions |",
        "| --- | ---: | --- | ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_cell(row['decision_id'])}`",
                    markdown_cell(row["worksheet_rank"]),
                    markdown_cell(row["label"]),
                    markdown_cell(row["page_number"]),
                    f"`{markdown_cell(row['page_class'])}`",
                    f"`{markdown_cell(row['visual_page_role'])}`",
                    f"`{markdown_cell(row['record_decision_status'])}`",
                    f"`{markdown_cell(row['record_selected_action'])}`",
                    markdown_cell(row["evidence_prompt"]),
                    f"`{markdown_cell(row['suggested_selected_action_values'])}`",
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    class_counts = Counter(row["page_class"] for row in rows)
    status_counts = Counter(row["record_decision_status"] for row in rows)
    action_counts = Counter(
        row["record_selected_action"] for row in rows if row["record_selected_action"]
    )
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "queue": str(args.queue),
            "records_template": str(args.records_template),
        },
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "class_counts": dict(class_counts),
        "record_status_counts": dict(status_counts),
        "recorded_action_counts": dict(action_counts),
        "recorded_rows": sum(
            1 for row in rows if row["record_decision_status"] != "unrecorded"
        ),
        "locked_rows": status_counts["locked"],
        "source_row_imports": count_imports(rows),
        "els_runs": 0,
        "compactness_runs": 0,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def records_by_decision_id(record_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["decision_id"]: row for row in record_rows if row.get("decision_id")}


def count_imports(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if row.get("source_row_use") != "no_source_row_use")


def format_counter(counter: Counter[str]) -> str:
    if not counter:
        return "none"
    return "; ".join(f"{key}={counter[key]}" for key in sorted(counter))


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
