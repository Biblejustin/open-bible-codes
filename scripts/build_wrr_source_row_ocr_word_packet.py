#!/usr/bin/env python3
"""Build WRR source-row OCR word packet from row crops and TSV words."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.analyze_wrr_primary_table2_row_ocr_probe import (
    DATE_COLUMN_X,
    NAME_COLUMN_X,
    normalize_hebrew_for_match,
    read_tsv_words,
)


DEFAULT_CROP_PACKET = Path("reports/wrr_1994/wrr_source_row_crop_packet.csv")
DEFAULT_TSV = Path("reports/wrr_1994/wrr_primary_table2_row_ocr.tsv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_source_row_ocr_word_packet.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_source_row_ocr_word_summary.csv")
DEFAULT_MD = Path("docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_source_row_ocr_word_packet.manifest.json")

NO_INPUT_BOUNDARY = (
    "OCR words are review aids only; no row transcription, source correction, "
    "pair exclusion, or method change is selected by this packet."
)

FIELDNAMES = [
    "run_label",
    "row_rank",
    "row_number",
    "concept",
    "frontier_pairs",
    "row_band_top",
    "row_band_bottom",
    "crop_path",
    "name_tokens_rtl",
    "name_normalized",
    "date_tokens_rtl",
    "date_normalized",
    "all_tokens_rtl",
    "all_normalized",
    "word_count",
    "hebrew_letter_count",
    "low_conf_word_count",
    "min_conf",
    "median_conf",
    "no_input_boundary",
    "next_manual_action",
]

SUMMARY_FIELDNAMES = ["metric", "value", "read"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    crop_rows = read_csv(args.crop_packet)
    words = read_tsv_words(args.tsv)
    rows = build_token_rows(crop_rows, words, args)
    summary_rows = build_summary_rows(rows, args)
    write_csv(args.out, rows, FIELDNAMES)
    write_csv(args.summary_out, summary_rows, SUMMARY_FIELDNAMES)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crop-packet", type=Path, default=DEFAULT_CROP_PACKET)
    parser.add_argument("--tsv", type=Path, default=DEFAULT_TSV)
    parser.add_argument("--low-conf-threshold", type=float, default=50.0)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_token_rows(
    crop_rows: list[dict[str, str]], words: list[object], args: argparse.Namespace
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for crop in crop_rows:
        band = (float_or_zero(crop.get("row_band_top", "")), float_or_zero(crop.get("row_band_bottom", "")))
        crop_x = (
            int_or_zero(crop.get("crop_left", "")),
            int_or_zero(crop.get("crop_right", "")),
        )
        row_words = words_in_band(words, band, crop_x)
        name_words = words_in_band(words, band, NAME_COLUMN_X)
        date_words = words_in_band(words, band, DATE_COLUMN_X)
        confidences = [word.conf for word in row_words]
        all_text = token_text(row_words)
        low_conf = [word for word in row_words if word.conf < args.low_conf_threshold]
        rows.append(
            {
                "run_label": crop.get("run_label", ""),
                "row_rank": int_or_zero(crop.get("row_rank", "")),
                "row_number": crop.get("row_number", ""),
                "concept": crop.get("concept", ""),
                "frontier_pairs": int_or_zero(crop.get("frontier_pairs", "")),
                "row_band_top": crop.get("row_band_top", ""),
                "row_band_bottom": crop.get("row_band_bottom", ""),
                "crop_path": crop.get("crop_path", ""),
                "name_tokens_rtl": token_text(name_words),
                "name_normalized": normalize_hebrew_for_match(token_text(name_words)),
                "date_tokens_rtl": token_text(date_words),
                "date_normalized": normalize_hebrew_for_match(token_text(date_words)),
                "all_tokens_rtl": all_text,
                "all_normalized": normalize_hebrew_for_match(all_text),
                "word_count": len(row_words),
                "hebrew_letter_count": len(normalize_hebrew_for_match(all_text)),
                "low_conf_word_count": len(low_conf),
                "min_conf": format_float(min(confidences) if confidences else 0.0),
                "median_conf": format_float(statistics.median(confidences) if confidences else 0.0),
                "no_input_boundary": NO_INPUT_BOUNDARY,
                "next_manual_action": next_manual_action(crop, len(low_conf)),
            }
        )
    rows.sort(key=lambda item: (int(item["row_rank"]), str(item["row_number"])))
    return rows


def words_in_band(words: list[object], band: tuple[float, float], x_range: tuple[int, int]) -> list[object]:
    selected = [
        word
        for word in words
        if band[0] <= word.center_y < band[1] and x_range[0] <= word.center_x <= x_range[1]
    ]
    return sorted(selected, key=lambda word: (-word.center_x, word.center_y))


def token_text(words: list[object]) -> str:
    return " ".join(str(word.text).strip() for word in words if str(word.text).strip())


def next_manual_action(crop: dict[str, str], low_conf_count: int) -> str:
    if int_or_zero(crop.get("frontier_pairs", "")) > 0:
        return "compare OCR words with crop and source row before any frontier source decision"
    if low_conf_count:
        return "keep OCR word read as low-confidence review aid"
    return "keep OCR word read as later review aid unless policy scope changes"


def build_summary_rows(
    rows: list[dict[str, object]], args: argparse.Namespace
) -> list[dict[str, object]]:
    return [
        metric("source_rows", len(rows), "source-transcription rows with OCR word entries"),
        metric("rows_with_tokens", sum(1 for row in rows if int(row["word_count"]) > 0), "rows with at least one TSV token in crop band"),
        metric("frontier_rows", sum(1 for row in rows if int(row["frontier_pairs"]) > 0), "rows touching minimum-frontier pairs"),
        metric("total_ocr_words", sum(int(row["word_count"]) for row in rows), "TSV words inside reviewed row crop bands"),
        metric("total_hebrew_letters", sum(int(row["hebrew_letter_count"]) for row in rows), "normalized Hebrew letters from OCR word strings"),
        metric("low_conf_threshold", format_float(args.low_conf_threshold), "word confidence threshold for review flags"),
        metric("low_conf_words", sum(int(row["low_conf_word_count"]) for row in rows), "TSV words below confidence threshold"),
        metric("ocr_boundary", NO_INPUT_BOUNDARY, "no source or method decision selected"),
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    summary = {str(row["metric"]): row for row in summary_rows}
    lines = [
        "# WRR Source Row OCR Word Packet",
        "",
        "Status: no-input OCR word packet for WRR source-row review.",
        "It lists OCR words by source row and expected columns; it is not transcription verification and does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_source_row_ocr_word_packet "
            f"--crop-packet {args.crop_packet} "
            f"--tsv {args.tsv} "
            f"--low-conf-threshold {format_float(args.low_conf_threshold)} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Source rows: {summary['source_rows']['value']}.",
        f"- Rows with OCR words: {summary['rows_with_tokens']['value']}.",
        f"- Frontier rows: {summary['frontier_rows']['value']}.",
        f"- Total OCR words: {summary['total_ocr_words']['value']}.",
        f"- Low-confidence OCR words: {summary['low_conf_words']['value']} below {summary['low_conf_threshold']['value']}.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Row Words",
        "",
        "| Rank | Row | Frontier | Words | Low conf | Name-column OCR | Date-column OCR | Next action |",
        "| ---: | --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {row_rank} | `{row_number}` | {frontier_pairs} | {word_count} | "
            "{low_conf_word_count} | {name_tokens_rtl} | {date_tokens_rtl} | "
            "{next_manual_action} |".format(**markdown_row(row))
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- OCR words are read from the current local Table 2 TSV and row bands.",
            "- OCR word availability is not transcription verification.",
            "- Low confidence counts are review triage only.",
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
        "tool": "build_wrr_source_row_ocr_word_packet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "inputs": {
            "crop_packet": str(args.crop_packet),
            "tsv": str(args.tsv),
            "low_conf_threshold": args.low_conf_threshold,
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def metric(name: str, value: object, read: str) -> dict[str, object]:
    return {"metric": name, "value": value, "read": read}


def markdown_row(row: dict[str, object]) -> dict[str, str]:
    return {key: markdown_cell(value) for key, value in row.items()}


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def float_or_zero(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return 0.0


def format_float(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


if __name__ == "__main__":
    raise SystemExit(main())
