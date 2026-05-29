#!/usr/bin/env python3
"""Build a coordinate-only Cities line-crop band map without transcription."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts import build_cities_source_page_line_crop_packet as packet_builder
from scripts import build_cities_source_page_line_crop_triage as triage_builder
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_PACKET = packet_builder.DEFAULT_OUT
DEFAULT_TRIAGE = triage_builder.DEFAULT_OUT
DEFAULT_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_map.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_map_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_MAP.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_map.manifest.json"
)

DEFAULT_GAP_THRESHOLD = 40
CLAIM_BOUNDARY = (
    "band map only; coordinate grouping of line crops, no OCR body text, "
    "no source-script body text, no verified transcription, no source-row "
    "import, no city normalization, no ELS, no compactness, no p-level"
)
PRIORITY_ORDER = [
    "priority_1_dense_text",
    "priority_2_medium_text",
    "priority_3_short_text",
    "priority_4_no_text",
]

FIELDNAMES = [
    "band_rank",
    "band_id",
    "transcription_decision_id",
    "label",
    "page_number",
    "page_class",
    "page_band_rank",
    "gap_threshold_px",
    "gap_before_band_px",
    "first_line_rank",
    "last_line_rank",
    "first_page_line_rank",
    "last_page_line_rank",
    "line_crop_rows",
    "crop_images_available",
    "band_top",
    "band_bottom",
    "band_height",
    "max_internal_gap_px",
    "ocr_word_count",
    "ocr_hebrew_letters",
    "priority_1_dense_text",
    "priority_2_medium_text",
    "priority_3_short_text",
    "priority_4_no_text",
    "dominant_review_priority",
    "allowed_without_input",
    "next_manual_action",
    "source_row_import",
    "city_name_normalization",
    "els_runs",
    "compactness_runs",
    "p_levels",
    "claim_boundary",
]
SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    packet_fieldnames, packet_rows = read_csv(args.packet)
    triage_fieldnames, triage_rows = read_csv(args.triage)
    band_rows = build_band_rows(
        packet_rows,
        triage_rows,
        gap_threshold=args.gap_threshold,
    )
    summary_rows = build_summary_rows(
        packet_fieldnames,
        triage_fieldnames,
        packet_rows,
        triage_rows,
        band_rows,
        gap_threshold=args.gap_threshold,
    )
    write_csv(args.out, FIELDNAMES, band_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, band_rows, summary_rows, args)
    write_manifest(
        args.manifest_out,
        args,
        band_rows,
        summary_rows,
        packet_fieldnames,
        triage_fieldnames,
        started,
    )
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--triage", type=Path, default=DEFAULT_TRIAGE)
    parser.add_argument("--gap-threshold", type=int, default=DEFAULT_GAP_THRESHOLD)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_band_rows(
    packet_rows: list[dict[str, str]],
    triage_rows: list[dict[str, str]],
    *,
    gap_threshold: int = DEFAULT_GAP_THRESHOLD,
) -> list[dict[str, str]]:
    priority_by_line_rank = {
        row.get("line_rank", ""): row.get("review_priority", "")
        for row in triage_rows
    }
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in packet_rows:
        grouped[row.get("transcription_decision_id", "")].append(row)

    bands: list[dict[str, str]] = []
    band_rank = 0
    for transcription_id in sorted(grouped):
        page_rows = sorted(grouped[transcription_id], key=lambda row: to_int(row.get("page_line_rank")))
        current: list[dict[str, str]] = []
        gap_before_band = 0
        page_band_rank = 0
        previous_bottom: int | None = None
        for row in page_rows:
            top = to_int(row.get("line_top"))
            if previous_bottom is not None:
                gap = top - previous_bottom
                if gap >= gap_threshold and current:
                    band_rank += 1
                    page_band_rank += 1
                    bands.append(
                        band_row(
                            band_rank,
                            page_band_rank,
                            current,
                            priority_by_line_rank,
                            gap_threshold=gap_threshold,
                            gap_before_band=gap_before_band,
                        )
                    )
                    current = []
                    gap_before_band = gap
            current.append(row)
            previous_bottom = to_int(row.get("line_bottom"))
        if current:
            band_rank += 1
            page_band_rank += 1
            bands.append(
                band_row(
                    band_rank,
                    page_band_rank,
                    current,
                    priority_by_line_rank,
                    gap_threshold=gap_threshold,
                    gap_before_band=gap_before_band,
                )
            )
    return bands


def band_row(
    band_rank: int,
    page_band_rank: int,
    rows: list[dict[str, str]],
    priority_by_line_rank: dict[str, str],
    *,
    gap_threshold: int,
    gap_before_band: int,
) -> dict[str, str]:
    first = rows[0]
    last = rows[-1]
    priorities = Counter(
        priority_by_line_rank.get(row.get("line_rank", ""), "")
        for row in rows
    )
    dominant = dominant_priority(priorities)
    gaps = [
        to_int(next_row.get("line_top")) - to_int(row.get("line_bottom"))
        for row, next_row in zip(rows, rows[1:])
    ]
    band_top = min(to_int(row.get("line_top")) for row in rows)
    band_bottom = max(to_int(row.get("line_bottom")) for row in rows)
    return {
        "band_rank": str(band_rank),
        "band_id": f"cities_source_line_band_{band_rank:03d}",
        "transcription_decision_id": first.get("transcription_decision_id", ""),
        "label": first.get("label", ""),
        "page_number": first.get("page_number", ""),
        "page_class": first.get("page_class", ""),
        "page_band_rank": str(page_band_rank),
        "gap_threshold_px": str(gap_threshold),
        "gap_before_band_px": str(gap_before_band),
        "first_line_rank": first.get("line_rank", ""),
        "last_line_rank": last.get("line_rank", ""),
        "first_page_line_rank": first.get("page_line_rank", ""),
        "last_page_line_rank": last.get("page_line_rank", ""),
        "line_crop_rows": str(len(rows)),
        "crop_images_available": str(count_value(rows, "crop_exists", "true")),
        "band_top": str(band_top),
        "band_bottom": str(band_bottom),
        "band_height": str(band_bottom - band_top),
        "max_internal_gap_px": str(max(gaps) if gaps else 0),
        "ocr_word_count": str(sum_int(rows, "ocr_word_count")),
        "ocr_hebrew_letters": str(sum_int(rows, "ocr_hebrew_letters")),
        "priority_1_dense_text": str(priorities.get("priority_1_dense_text", 0)),
        "priority_2_medium_text": str(priorities.get("priority_2_medium_text", 0)),
        "priority_3_short_text": str(priorities.get("priority_3_short_text", 0)),
        "priority_4_no_text": str(priorities.get("priority_4_no_text", 0)),
        "dominant_review_priority": dominant,
        "allowed_without_input": "group line crops by coordinate gaps only",
        "next_manual_action": "use band map to navigate visual review; do not import source rows",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def dominant_priority(counts: Counter[str]) -> str:
    return max(PRIORITY_ORDER, key=lambda priority: (counts.get(priority, 0), -PRIORITY_ORDER.index(priority)))


def build_summary_rows(
    packet_fieldnames: list[str],
    triage_fieldnames: list[str],
    packet_rows: list[dict[str, str]],
    triage_rows: list[dict[str, str]],
    band_rows: list[dict[str, str]],
    *,
    gap_threshold: int,
) -> list[dict[str, str]]:
    page_counts = Counter(row.get("transcription_decision_id", "") for row in packet_rows)
    band_page_counts = Counter(row.get("transcription_decision_id", "") for row in band_rows)
    summary: list[tuple[str, str | int]] = [
        (
            "packet_fieldnames_match",
            str(packet_fieldnames == packet_builder.FIELDNAMES).lower(),
        ),
        (
            "triage_fieldnames_match",
            str(triage_fieldnames == triage_builder.FIELDNAMES).lower(),
        ),
        ("gap_threshold_px", gap_threshold),
        ("band_rows", len(band_rows)),
        ("source_line_rows", len(packet_rows)),
        ("triage_rows", len(triage_rows)),
        ("unique_table_pages", len(page_counts)),
        ("crop_images_available", count_value(packet_rows, "crop_exists", "true")),
        ("ocr_words", sum_int(packet_rows, "ocr_word_count")),
        ("ocr_hebrew_letters", sum_int(packet_rows, "ocr_hebrew_letters")),
        ("source_row_imports", 0),
        ("city_name_normalization", 0),
        ("els_runs", 0),
        ("compactness_runs", 0),
        ("p_levels", 0),
    ]
    for transcription_id in sorted(band_page_counts):
        summary.append((f"bands_{transcription_id}", band_page_counts[transcription_id]))
    for priority in PRIORITY_ORDER:
        summary.append((priority, sum_int(band_rows, priority)))
    summary.append(("claim_boundary", CLAIM_BOUNDARY))
    return [{"metric": metric, "value": str(value)} for metric, value in summary]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Source Page Line Crop Band Map",
        "",
        "Status: coordinate-only band map for Cities source-page line crops.",
        "It groups adjacent line crops when vertical gaps are below the configured threshold.",
        "No OCR body text or source-script body text appears in this doc, CSV, or manifest.",
        CLAIM_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_band_map "
            f"--packet {args.packet} "
            f"--triage {args.triage} "
            f"--gap-threshold {args.gap_threshold} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Gap threshold: {summary['gap_threshold_px']} px.",
        f"- Band rows: {summary['band_rows']}.",
        f"- Source line rows: {summary['source_line_rows']}.",
        f"- Unique table pages: {summary['unique_table_pages']}.",
        f"- Crop images available: {summary['crop_images_available']}.",
        f"- OCR words represented by line boxes: {summary['ocr_words']}.",
        f"- OCR Hebrew letters represented by line boxes: {summary['ocr_hebrew_letters']}.",
        "- Source-row imports: 0.",
        "- City-name normalization: 0.",
        "- ELS runs: 0.",
        "- Compactness runs: 0.",
        "- p-levels: 0.",
        f"- Boundary: {CLAIM_BOUNDARY}",
        "",
        "## Page Bands",
        "",
        "| Transcription id | Bands |",
        "| --- | ---: |",
    ]
    for row in rows:
        metric = f"bands_{row['transcription_decision_id']}"
        if row["page_band_rank"] == "1":
            lines.append(
                f"| `{markdown_cell(row['transcription_decision_id'])}` | {summary[metric]} |"
            )
    lines.extend(
        [
            "",
            "## Band Rows",
            "",
            "| Band | Page | Lines | Crop rows | Top-bottom | Dominant priority |",
            "| ---: | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["band_rank"]),
                    f"`{markdown_cell(row['transcription_decision_id'])}`",
                    f"{markdown_cell(row['first_page_line_rank'])}-{markdown_cell(row['last_page_line_rank'])}",
                    markdown_cell(row["line_crop_rows"]),
                    f"{markdown_cell(row['band_top'])}-{markdown_cell(row['band_bottom'])}",
                    f"`{markdown_cell(row['dominant_review_priority'])}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Band grouping uses local crop coordinates only.",
            "- A band is not a verified source row, table row, transcription, or city-name record.",
            "- Any future source import still needs readable row evidence and an explicit import decision.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    band_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    packet_fieldnames: list[str],
    triage_fieldnames: list[str],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "packet": str(args.packet),
            "triage": str(args.triage),
        },
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(band_rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "gap_threshold_px": args.gap_threshold,
        "packet_fieldnames_match": packet_fieldnames == packet_builder.FIELDNAMES,
        "triage_fieldnames_match": triage_fieldnames == triage_builder.FIELDNAMES,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_packet_boundary": packet_builder.NO_INPUT_BOUNDARY,
        "source_triage_boundary": triage_builder.CLAIM_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def count_value(rows: list[dict[str, str]], key: str, value: str) -> int:
    return sum(1 for row in rows if row.get(key) == value)


def sum_int(rows: list[dict[str, str]], key: str) -> int:
    return sum(to_int(row.get(key)) for row in rows)


def to_int(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
