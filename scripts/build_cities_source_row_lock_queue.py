#!/usr/bin/env python3
"""Build Cities source-row lock queue from reviewed OCR page roles."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_PAGE_REVIEW = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review.csv"
)
DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_source_row_lock_queue.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_queue_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_queue.manifest.json"
)

CLAIM_BOUNDARY = (
    "source-row lock planning only; no OCR body text, no source-row import, no "
    "city normalization, no ELS, no compactness, no p-level"
)

ROLE_CONFIG = {
    "prose_with_source_table_page": (
        1,
        "table_candidate_page",
        "page has visual table material; needs citable source-row lock before use",
    ),
    "source_table_page": (
        1,
        "table_candidate_page",
        "page has visual table material; needs citable source-row lock before use",
    ),
    "source_table_and_notes_page": (
        1,
        "table_candidate_page",
        "page has visual table and note material; needs citable source-row lock before use",
    ),
    "source_list_page": (
        2,
        "source_list_candidate_page",
        "page has visual list material; needs citable source-row lock before use",
    ),
    "source_exception_notes_page": (
        3,
        "exception_note_candidate_page",
        "page has source-exception notes; needs separate citable decision before use",
    ),
    "criteria_and_source_exception_page": (
        3,
        "exception_note_candidate_page",
        "page has criteria and source-exception notes; needs separate citable decision before use",
    ),
}

FIELDNAMES = [
    "lock_rank",
    "label",
    "page_number",
    "family",
    "lane",
    "visual_page_role",
    "page_class",
    "packet_ocr_status",
    "packet_ocr_text_signal_chars",
    "page_image_path",
    "source_row_use",
    "current_decision",
    "lock_status",
    "next_action",
    "claim_boundary",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    page_review_rows = read_csv(args.page_review)
    queue_rows = build_lock_queue_rows(page_review_rows)
    summary_rows = build_summary_rows(queue_rows)
    write_csv(args.out, FIELDNAMES, queue_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, queue_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, queue_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page-review", type=Path, default=DEFAULT_PAGE_REVIEW)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_lock_queue_rows(page_review_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in page_review_rows:
        role = row.get("visual_page_role", "")
        if role not in ROLE_CONFIG:
            continue
        source_row_use = row.get("source_row_use", "")
        decision = row.get("decision", "")
        if source_row_use != "no_source_row_use" or decision != "no_source_row_import":
            raise ValueError(
                f"{row.get('label', '')} p{row.get('page_number', '')} "
                "already carries source-row use; lock queue must stay pre-import"
            )
        priority, page_class, next_action = ROLE_CONFIG[role]
        rows.append(
            {
                "lock_rank": "0",
                "label": row.get("label", ""),
                "page_number": row.get("page_number", ""),
                "family": row.get("family", ""),
                "lane": row.get("lane", ""),
                "visual_page_role": role,
                "page_class": page_class,
                "packet_ocr_status": row.get("packet_ocr_status", ""),
                "packet_ocr_text_signal_chars": row.get(
                    "packet_ocr_text_signal_chars", ""
                ),
                "page_image_path": row.get("page_image_path", ""),
                "source_row_use": source_row_use,
                "current_decision": decision,
                "lock_status": "needs_citable_source_row_lock",
                "next_action": next_action,
                "claim_boundary": CLAIM_BOUNDARY,
                "_priority": str(priority),
            }
        )
    rows.sort(key=queue_sort_key)
    for index, row in enumerate(rows, start=1):
        row["lock_rank"] = str(index)
        row.pop("_priority", None)
    return rows


def queue_sort_key(row: dict[str, str]) -> tuple[int, str, int]:
    return (
        int_or_zero(row.get("_priority", "")),
        row.get("label", ""),
        int_or_zero(row.get("page_number", "")),
    )


def build_summary_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        metric("queue_rows", len(rows)),
        metric("unique_labels", len({row["label"] for row in rows})),
        metric("table_candidate_pages", count_class(rows, "table_candidate_page")),
        metric(
            "source_list_candidate_pages",
            count_class(rows, "source_list_candidate_page"),
        ),
        metric(
            "exception_note_candidate_pages",
            count_class(rows, "exception_note_candidate_page"),
        ),
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
        "# Cities Source Row Lock Queue",
        "",
        "Status: source-row lock planning record from reviewed OCR page roles.",
        "It does not import source rows, track OCR body text, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "No OCR body text or source-script body text appears in this doc, CSV, summary, or manifest.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_row_lock_queue "
            f"--page-review {args.page_review} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        f"- Queue rows: {summary['queue_rows']}.",
        f"- Unique labels: {summary['unique_labels']}.",
        f"- Table-bearing candidate pages: {summary['table_candidate_pages']}.",
        f"- Source-list candidate pages: {summary['source_list_candidate_pages']}.",
        f"- Exception-note candidate pages: {summary['exception_note_candidate_pages']}.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- Boundary: {CLAIM_BOUNDARY}",
        "",
        "## Candidate Pages",
        "",
        "| Rank | Label | Page | Role | Class | OCR status | Signal chars | Lock status | Next action |",
        "| ---: | --- | ---: | --- | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["lock_rank"]),
                    markdown_cell(row["label"]),
                    markdown_cell(row["page_number"]),
                    f"`{markdown_cell(row['visual_page_role'])}`",
                    f"`{markdown_cell(row['page_class'])}`",
                    f"`{markdown_cell(row['packet_ocr_status'])}`",
                    markdown_cell(row["packet_ocr_text_signal_chars"]),
                    f"`{markdown_cell(row['lock_status'])}`",
                    markdown_cell(row["next_action"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This queue names page locations only.",
            "- It does not transcribe city rows, names, dates, spellings, or OCR body text.",
            "- Candidate pages still need a separate citable source-row lock before any source data can be used.",
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
        "inputs": {"page_review": str(args.page_review)},
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
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


def count_class(rows: list[dict[str, str]], page_class: str) -> int:
    return sum(1 for row in rows if row.get("page_class") == page_class)


def count_imports(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if row.get("source_row_use") != "no_source_row_use")


def metric(name: str, value: object) -> dict[str, str]:
    return {"metric": name, "value": str(value)}


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


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
