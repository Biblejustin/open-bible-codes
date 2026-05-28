#!/usr/bin/env python3
"""Build Cities source-page review bundle from transcription worksheet rows."""

from __future__ import annotations

import argparse
import csv
import json
import struct
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_WORKSHEET = Path(
    "reports/cities_pdf_recovery_probe/cities_source_transcription_review_worksheet.csv"
)
DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_source_page_review_bundle.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_review_bundle_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_review_bundle.manifest.json"
)

NO_INPUT_BOUNDARY = (
    "Page-image review bundle only; no OCR body text, no source-script body "
    "text, no source-row import, no city normalization, no ELS, no compactness, "
    "no p-level"
)

FIELDNAMES = [
    "bundle_rank",
    "transcription_decision_id",
    "source_lock_decision_id",
    "label",
    "page_number",
    "page_class",
    "visual_page_role",
    "selected_source",
    "selected_path",
    "source_sha256",
    "page_image_path",
    "page_image_exists",
    "page_image_width",
    "page_image_height",
    "review_state",
    "next_manual_action",
    "source_row_import",
    "city_name_normalization",
    "els_runs",
    "compactness_runs",
    "p_levels",
    "no_input_boundary",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    worksheet_rows = read_rows(args.worksheet)
    bundle_rows = build_bundle_rows(worksheet_rows)
    summary_rows = build_summary_rows(bundle_rows)
    write_csv(args.out, FIELDNAMES, bundle_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, bundle_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, bundle_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worksheet", type=Path, default=DEFAULT_WORKSHEET)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_bundle_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    bundle_rows: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        path = Path(row.get("page_image_path", ""))
        width, height = image_dimensions(path)
        bundle_rows.append(
            {
                "bundle_rank": str(index),
                "transcription_decision_id": row.get("transcription_decision_id", ""),
                "source_lock_decision_id": row.get("source_lock_decision_id", ""),
                "label": row.get("label", ""),
                "page_number": row.get("page_number", ""),
                "page_class": row.get("page_class", ""),
                "visual_page_role": row.get("visual_page_role", ""),
                "selected_source": row.get("selected_source", ""),
                "selected_path": row.get("selected_path", ""),
                "source_sha256": row.get("source_sha256", ""),
                "page_image_path": row.get("page_image_path", ""),
                "page_image_exists": str(path.exists()).lower(),
                "page_image_width": str(width),
                "page_image_height": str(height),
                "review_state": row.get("review_state", ""),
                "next_manual_action": row.get("next_manual_action", ""),
                "source_row_import": "0",
                "city_name_normalization": "0",
                "els_runs": "0",
                "compactness_runs": "0",
                "p_levels": "0",
                "no_input_boundary": NO_INPUT_BOUNDARY,
            }
        )
    return bundle_rows


def build_summary_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    class_counts = Counter(row["page_class"] for row in rows)
    return [
        metric("bundle_rows", len(rows)),
        metric("page_images_found", count_value(rows, "page_image_exists", "true")),
        metric("page_images_missing", count_value(rows, "page_image_exists", "false")),
        metric("table_candidate_pages", class_counts["table_candidate_page"]),
        metric("source_list_candidate_pages", class_counts["source_list_candidate_page"]),
        metric("exception_note_candidate_pages", class_counts["exception_note_candidate_page"]),
        metric("source_row_imports", 0),
        metric("city_name_normalization", 0),
        metric("els_runs", 0),
        metric("compactness_runs", 0),
        metric("p_levels", 0),
        metric("no_input_boundary", NO_INPUT_BOUNDARY),
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Source Page Review Bundle",
        "",
        "Status: no-input page-image review bundle for locked Cities source pages.",
        "It verifies page-image paths and dimensions for later manual transcription review.",
        "No OCR body text or source-script body text appears in this doc, CSV, summary, or manifest.",
        "It does not import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_review_bundle "
            f"--worksheet {args.worksheet} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Bundle rows: {summary['bundle_rows']}.",
        f"- Page images found: {summary['page_images_found']}.",
        f"- Page images missing: {summary['page_images_missing']}.",
        f"- Table-bearing candidate pages: {summary['table_candidate_pages']}.",
        f"- Source-list candidate pages: {summary['source_list_candidate_pages']}.",
        f"- Exception-note candidate pages: {summary['exception_note_candidate_pages']}.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- City-name normalization: {summary['city_name_normalization']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- p-levels: {summary['p_levels']}.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Page Bundle",
        "",
        "| Rank | Transcription id | Label | Page | Class | Image | Size | Next manual action |",
        "| ---: | --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["bundle_rank"]),
                    f"`{markdown_cell(row['transcription_decision_id'])}`",
                    markdown_cell(row["label"]),
                    markdown_cell(row["page_number"]),
                    f"`{markdown_cell(row['page_class'])}`",
                    f"`{markdown_cell(row['page_image_path'])}`",
                    markdown_cell(
                        f"{row['page_image_width']}x{row['page_image_height']}"
                    ),
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
            "- Page-image existence is not transcription verification.",
            "- Page dimensions are review logistics only.",
            "- Future source-row use still requires readable transcription, row/column alignment evidence, and an explicit import decision record.",
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
        "inputs": {"worksheet": str(args.worksheet)},
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "no_input_boundary": NO_INPUT_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def image_dimensions(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    with path.open("rb") as handle:
        header = handle.read(24)
    if header.startswith(b"\x89PNG\r\n\x1a\n") and header[12:16] == b"IHDR":
        width, height = struct.unpack(">II", header[16:24])
        return int(width), int(height)
    return 0, 0


def count_value(rows: list[dict[str, str]], field: str, value: str) -> int:
    return sum(1 for row in rows if row.get(field) == value)


def metric(name: str, value: object) -> dict[str, str]:
    return {"metric": name, "value": str(value)}


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
