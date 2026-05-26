#!/usr/bin/env python3
"""Build a WRR source-row review bundle from checklist, crops, and OCR words."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_ROW_CHECKLIST = Path(
    "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv"
)
DEFAULT_CROP_PACKET = Path("reports/wrr_1994/wrr_source_row_crop_packet.csv")
DEFAULT_OCR_WORD_PACKET = Path("reports/wrr_1994/wrr_source_row_ocr_word_packet.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_source_row_review_bundle.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/wrr_source_row_review_bundle_summary.csv")
DEFAULT_MD = Path("docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_source_row_review_bundle.manifest.json")

NO_INPUT_BOUNDARY = (
    "No row transcription, source correction, pair exclusion, or method change "
    "is selected by this bundle."
)

FIELDNAMES = [
    "run_label",
    "row_rank",
    "row_number",
    "concept",
    "review_state",
    "action_terms",
    "residual_pairs",
    "frontier_pairs",
    "terms_to_verify",
    "crop_path",
    "crop_exists",
    "word_count",
    "hebrew_letter_count",
    "low_conf_word_count",
    "min_conf",
    "median_conf",
    "name_column_ocr",
    "date_column_ocr",
    "table2_bridge_read",
    "no_input_boundary",
    "allowed_without_input",
    "next_manual_action",
]

SUMMARY_FIELDNAMES = ["metric", "value", "read"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    row_checklist = read_rows(args.row_checklist)
    crop_packet = read_rows(args.crop_packet)
    ocr_word_packet = read_rows(args.ocr_word_packet)
    bundle_rows = build_bundle_rows(row_checklist, crop_packet, ocr_word_packet)
    summary_rows = build_summary_rows(bundle_rows)
    write_csv(args.out, bundle_rows, FIELDNAMES)
    write_csv(args.summary_out, summary_rows, SUMMARY_FIELDNAMES)
    write_markdown(args.markdown_out, bundle_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, bundle_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--row-checklist", type=Path, default=DEFAULT_ROW_CHECKLIST)
    parser.add_argument("--crop-packet", type=Path, default=DEFAULT_CROP_PACKET)
    parser.add_argument("--ocr-word-packet", type=Path, default=DEFAULT_OCR_WORD_PACKET)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_bundle_rows(
    row_checklist: list[dict[str, str]],
    crop_packet: list[dict[str, str]],
    ocr_word_packet: list[dict[str, str]],
) -> list[dict[str, object]]:
    crops_by_row = keyed_rows(crop_packet, "row_number")
    words_by_row = keyed_rows(ocr_word_packet, "row_number")
    rows: list[dict[str, object]] = []
    for row in row_checklist:
        row_number = row.get("row_number", "")
        crop = crops_by_row.get(row_number, {})
        words = words_by_row.get(row_number, {})
        rows.append(
            {
                "run_label": row.get("run_label", ""),
                "row_rank": int_or_zero(row.get("row_rank", "")),
                "row_number": row_number,
                "concept": row.get("concept", ""),
                "review_state": row.get("review_state", ""),
                "action_terms": int_or_zero(row.get("action_terms", "")),
                "residual_pairs": int_or_zero(row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(row.get("frontier_pairs", "")),
                "terms_to_verify": row.get("terms_to_verify", ""),
                "crop_path": crop.get("crop_path", ""),
                "crop_exists": crop.get("crop_exists", ""),
                "word_count": int_or_zero(words.get("word_count", "")),
                "hebrew_letter_count": int_or_zero(words.get("hebrew_letter_count", "")),
                "low_conf_word_count": int_or_zero(words.get("low_conf_word_count", "")),
                "min_conf": words.get("min_conf", ""),
                "median_conf": words.get("median_conf", ""),
                "name_column_ocr": words.get("name_tokens_rtl", ""),
                "date_column_ocr": words.get("date_tokens_rtl", ""),
                "table2_bridge_read": row.get("table2_bridge_read", ""),
                "no_input_boundary": NO_INPUT_BOUNDARY,
                "allowed_without_input": "organize crop and OCR evidence only",
                "next_manual_action": next_manual_action(row, crop, words),
            }
        )
    rows.sort(key=lambda item: (int(item["row_rank"]), str(item["row_number"])))
    return rows


def next_manual_action(
    row: dict[str, str], crop: dict[str, str], words: dict[str, str]
) -> str:
    frontier = int_or_zero(row.get("frontier_pairs", ""))
    has_crop = crop.get("crop_exists", "").lower() == "true"
    has_words = int_or_zero(words.get("word_count", "")) > 0
    if frontier > 0 and has_crop and has_words:
        return "review crop and OCR words together before any frontier source decision"
    if frontier > 0 and has_crop:
        return "review crop before any frontier source decision; OCR words unavailable"
    if frontier > 0:
        return "retrieve row image before any frontier source decision"
    return "review after frontier rows unless policy scope changes"


def build_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    frontier_rows = [row for row in rows if int(row.get("frontier_pairs", 0)) > 0]
    rows_with_crops = [
        row for row in rows if str(row.get("crop_exists", "")).lower() == "true"
    ]
    rows_with_words = [row for row in rows if int(row.get("word_count", 0)) > 0]
    return [
        metric("row_review_clusters", len(rows), "source-row review bundle rows"),
        metric("frontier_rows", len(frontier_rows), "rows with minimum-frontier pair links"),
        metric("action_terms", sum_int(rows, "action_terms"), "terms requiring row-level review"),
        metric("residual_pairs", sum_int(rows, "residual_pairs"), "residual pair links"),
        metric("frontier_pairs", sum_int(rows, "frontier_pairs"), "minimum-frontier pair links"),
        metric("rows_with_generated_crops", len(rows_with_crops), "rows with generated crop paths"),
        metric("rows_with_ocr_words", len(rows_with_words), "rows with OCR words in the row band"),
        metric("total_ocr_words", sum_int(rows, "word_count"), "OCR words in bundled rows"),
        metric(
            "low_confidence_ocr_words",
            sum_int(rows, "low_conf_word_count"),
            "OCR words below the packet confidence threshold",
        ),
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    summary = {str(row["metric"]): row for row in summary_rows}
    lines = [
        "# WRR Source Row Review Bundle",
        "",
        "Status: no-input row-review bundle for WRR source-row review.",
        "It combines row-checklist, crop-path, and OCR-word evidence; it does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_source_row_review_bundle "
            f"--row-checklist {args.row_checklist} "
            f"--crop-packet {args.crop_packet} "
            f"--ocr-word-packet {args.ocr_word_packet} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Row review clusters: {summary_value(summary, 'row_review_clusters')}.",
        f"- Frontier rows: {summary_value(summary, 'frontier_rows')}.",
        f"- Rows with generated crops: {summary_value(summary, 'rows_with_generated_crops')}.",
        f"- Rows with OCR words: {summary_value(summary, 'rows_with_ocr_words')}.",
        f"- Low-confidence OCR words: {summary_value(summary, 'low_confidence_ocr_words')}.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Row Bundle",
        "",
        "| Rank | Row | Frontier | Terms | Words | Low conf | Crop | Name-column OCR | Date-column OCR | Next action |",
        "| ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {row_rank} | `{row_number}` | {frontier_pairs} | {action_terms} | "
            "{word_count} | {low_conf_word_count} | {crop} | {name} | {date} | "
            "{next_manual_action} |".format(
                crop=markdown_crop_link(row.get("crop_path", "")),
                name=markdown_cell(row.get("name_column_ocr", "")),
                date=markdown_cell(row.get("date_column_ocr", "")),
                **markdown_row(row),
            )
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Crop and OCR availability is not transcription verification.",
            "- OCR confidence is review triage only.",
            "- Manual row decisions still require a separate citable decision record.",
            "- No row here changes the working WRR source or excludes a pair automatically.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_source_row_review_bundle",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "rows": len(rows),
        "summary": {str(row["metric"]): row["value"] for row in summary_rows},
        "inputs": {
            "row_checklist": str(args.row_checklist),
            "crop_packet": str(args.crop_packet),
            "ocr_word_packet": str(args.ocr_word_packet),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def keyed_rows(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows if row.get(key, "")}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def metric(name: str, value: object, read: str) -> dict[str, object]:
    return {"metric": name, "value": value, "read": read}


def summary_value(summary: dict[str, dict[str, object]], metric_name: str) -> object:
    return summary.get(metric_name, {}).get("value", "")


def sum_int(rows: list[dict[str, object]], field: str) -> int:
    return sum(int_or_zero(str(row.get(field, ""))) for row in rows)


def int_or_zero(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def markdown_row(row: dict[str, object]) -> dict[str, str]:
    return {key: markdown_cell(value) for key, value in row.items()}


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def markdown_crop_link(value: object) -> str:
    path = str(value).strip()
    if not path:
        return ""
    href = "../" + path if not path.startswith("../") else path
    return f"[crop]({href})"


if __name__ == "__main__":
    raise SystemExit(main())
