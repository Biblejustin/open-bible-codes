#!/usr/bin/env python3
"""Probe row-aligned OCR matches for WRR 1994 primary-PDF Table 2."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.analyze_wrr_primary_table2_ocr_probe import (
    DEFAULT_RENDER_PREFIX,
    DEFAULT_SOURCE,
    DEFAULT_TESSDATA_DIR,
    count_rows,
    markdown_cell,
    michigan_to_hebrew_normalized,
    missing_ocr_dependencies,
    normalize_hebrew_for_match,
    read_rows,
    render_page,
    row_number_from_term_id,
    terms_from_records,
    write_rows,
)
from scripts.import_wrr_terms import parse_wrr_records


DEFAULT_TERMS = Path("reports/wrr_1994/wrr2_terms.csv")
DEFAULT_TSV_BASE = Path("reports/wrr_1994/wrr_primary_table2_row_ocr")
DEFAULT_TSV = DEFAULT_TSV_BASE.with_suffix(".tsv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe_summary.csv")
DEFAULT_MD = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe.manifest.json")

ROW_COUNT = 32
ROW_MARKER_LEFT_MIN = 500
ROW_MARKER_LEFT_MAX = 590
ROW_MARKER_TOP_MIN = 400
ROW_MARKER_TOP_MAX = 2100
NAME_COLUMN_X = (850, 1450)
DATE_COLUMN_X = (1450, 2050)

FIELDNAMES = [
    "term_id",
    "row_number",
    "concept",
    "category",
    "michigan_term",
    "hebrew_normalized",
    "row_ocr_status",
    "match_basis",
    "column",
    "row_ocr_text_normalized",
    "current_read",
]

SUMMARY_FIELDNAMES = [
    "total_terms",
    "matched_terms",
    "missing_terms",
    "appellation_terms",
    "matched_appellation_terms",
    "date_terms",
    "matched_date_terms",
    "source_rows",
    "source_rows_with_any_match",
    "source_rows_with_all_terms_matched",
    "detected_row_markers",
    "inferred_row_markers",
    "ocr_words",
    "ocr_hebrew_letters",
    "tsv_status",
    "status",
]


@dataclass(frozen=True)
class TsvWord:
    text: str
    left: int
    top: int
    width: int
    height: int
    conf: float

    @property
    def center_x(self) -> float:
        return self.left + (self.width / 2)

    @property
    def center_y(self) -> float:
        return self.top + (self.height / 2)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    terms = read_terms(args)
    tsv_path, tsv_status, tsv_note = acquire_tsv(args)
    words = read_tsv_words(tsv_path) if tsv_path.exists() else []
    centers, detected_rows = build_row_centers(words)
    rows = build_row_probe_rows(terms, words, centers)
    summary = summarize_row_probe(rows, words, detected_rows, tsv_status)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary, args, tsv_note)
    write_manifest(args, rows, summary, tsv_note, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--source-records", type=Path)
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--page", type=int, default=6)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--psm", default="6")
    parser.add_argument("--tessdata-dir", type=Path, default=DEFAULT_TESSDATA_DIR)
    parser.add_argument("--render-prefix", type=Path, default=DEFAULT_RENDER_PREFIX)
    parser.add_argument("--tsv-base", type=Path, default=DEFAULT_TSV_BASE)
    parser.add_argument("--tsv", type=Path, default=DEFAULT_TSV)
    parser.add_argument("--refresh-ocr", action="store_true")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_terms(args: argparse.Namespace) -> list[dict[str, str]]:
    if args.source_records is None:
        return read_rows(args.terms)
    records = parse_wrr_records(args.source_records.read_text(encoding="utf-8"))
    return terms_from_records(records)


def acquire_tsv(args: argparse.Namespace) -> tuple[Path, str, str]:
    if args.tsv.exists() and not args.refresh_ocr:
        return args.tsv, "existing_tsv", str(args.tsv)

    missing = missing_ocr_dependencies(args)
    if missing:
        args.tsv.parent.mkdir(parents=True, exist_ok=True)
        args.tsv.write_text(tsv_header(), encoding="utf-8")
        return args.tsv, "blocked_missing_ocr_dependency", ", ".join(missing)

    image = rendered_image_path(args)
    if not image.exists() or args.refresh_ocr:
        image = render_page(args)
    tsv_path = run_tesseract_tsv(args, image)
    return tsv_path, "generated_tsv", str(tsv_path)


def rendered_image_path(args: argparse.Namespace) -> Path:
    padded = Path(f"{args.render_prefix}-{args.page:02d}.png")
    if padded.exists():
        return padded
    return Path(f"{args.render_prefix}-{args.page}.png")


def run_tesseract_tsv(args: argparse.Namespace, image: Path) -> Path:
    args.tsv_base.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "tesseract",
        "--tessdata-dir",
        str(args.tessdata_dir),
        "-l",
        "heb",
        "--psm",
        str(args.psm),
        "-c",
        "tessedit_create_tsv=1",
        str(image),
        str(args.tsv_base),
    ]
    subprocess.run(cmd, check=True)
    generated = args.tsv_base.with_suffix(".tsv")
    if generated != args.tsv:
        args.tsv.parent.mkdir(parents=True, exist_ok=True)
        args.tsv.write_text(generated.read_text(encoding="utf-8"), encoding="utf-8")
    return args.tsv


def tsv_header() -> str:
    return "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"


def read_tsv_words(path: Path) -> list[TsvWord]:
    words: list[TsvWord] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            text = (row.get("text") or "").strip()
            if not text:
                continue
            try:
                words.append(
                    TsvWord(
                        text=text,
                        left=int(float(row.get("left") or 0)),
                        top=int(float(row.get("top") or 0)),
                        width=int(float(row.get("width") or 0)),
                        height=int(float(row.get("height") or 0)),
                        conf=float(row.get("conf") or 0),
                    )
                )
            except ValueError:
                continue
    return words


def build_row_centers(words: list[TsvWord], row_count: int = ROW_COUNT) -> tuple[dict[int, float], set[int]]:
    marker_groups: dict[int, list[TsvWord]] = {}
    for word in words:
        row_number = row_marker_number(word)
        if row_number is None or not 1 <= row_number <= row_count:
            continue
        marker_groups.setdefault(row_number, []).append(word)

    assigned: dict[int, float] = {}
    for row_number in sorted(marker_groups):
        candidates = sorted(marker_groups[row_number], key=lambda item: item.center_y)
        if (
            len(candidates) > 1
            and row_number > 1
            and (row_number - 1) not in marker_groups
            and (row_number - 1) not in assigned
        ):
            assigned[row_number - 1] = candidates[0].center_y
            assigned[row_number] = candidates[-1].center_y
        else:
            assigned[row_number] = candidates[0].center_y

    centers: dict[int, float] = {}
    for row_number in range(1, row_count + 1):
        if row_number in assigned:
            centers[row_number] = assigned[row_number]
            continue
        centers[row_number] = infer_row_center(row_number, assigned)
    return centers, set(assigned)


def row_marker_number(word: TsvWord) -> int | None:
    if not (ROW_MARKER_LEFT_MIN <= word.left <= ROW_MARKER_LEFT_MAX):
        return None
    if not (ROW_MARKER_TOP_MIN <= word.top <= ROW_MARKER_TOP_MAX):
        return None
    match = re.fullmatch(r"\.?([0-9]{1,2})\.?", word.text)
    if not match:
        return None
    return int(match.group(1))


def infer_row_center(row_number: int, assigned: dict[int, float]) -> float:
    if not assigned:
        return 0.0
    lower = max((number for number in assigned if number < row_number), default=None)
    higher = min((number for number in assigned if number > row_number), default=None)
    if lower is not None and higher is not None:
        span = assigned[higher] - assigned[lower]
        return assigned[lower] + (span * (row_number - lower) / (higher - lower))
    if lower is not None:
        return assigned[lower] + (40.0 * (row_number - lower))
    return assigned[higher] - (40.0 * (higher - row_number))  # type: ignore[index]


def build_row_probe_rows(
    terms: list[dict[str, str]],
    words: list[TsvWord],
    centers: dict[int, float],
) -> list[dict[str, str]]:
    bands = row_bands(centers)
    rows = []
    for term in terms:
        row_number = row_number_from_term_id(term.get("term_id", ""))
        row_index = int(row_number) if row_number.isdigit() else 0
        category = term.get("category", "")
        column = "name" if category == "wrr_appellation" else "date"
        row_text = normalized_row_column_text(words, bands.get(row_index, (0.0, 0.0)), column)
        hebrew = michigan_to_hebrew_normalized(term.get("term", ""))
        matched = bool(hebrew and hebrew in row_text)
        rows.append(
            {
                "term_id": term.get("term_id", ""),
                "row_number": row_number,
                "concept": term.get("concept", ""),
                "category": category,
                "michigan_term": term.get("term", ""),
                "hebrew_normalized": hebrew,
                "row_ocr_status": "matched" if matched else "not_matched",
                "match_basis": f"row_aligned_{column}_column_ocr_exact_normalized_substring",
                "column": column,
                "row_ocr_text_normalized": row_text,
                "current_read": current_read(matched),
            }
        )
    return rows


def row_bands(centers: dict[int, float]) -> dict[int, tuple[float, float]]:
    bands: dict[int, tuple[float, float]] = {}
    row_count = max(centers) if centers else 0
    for row_number in range(1, row_count + 1):
        center = centers[row_number]
        previous_center = centers[row_number - 1] if row_number > 1 else center - 40.0
        next_center = centers[row_number + 1] if row_number < row_count else center + 40.0
        bands[row_number] = ((previous_center + center) / 2, (center + next_center) / 2)
    return bands


def normalized_row_column_text(
    words: list[TsvWord],
    band: tuple[float, float],
    column: str,
) -> str:
    x_min, x_max = NAME_COLUMN_X if column == "name" else DATE_COLUMN_X
    selected = [
        word
        for word in words
        if band[0] <= word.center_y < band[1] and x_min <= word.center_x <= x_max
    ]
    return normalize_hebrew_for_match("".join(word.text for word in selected))


def current_read(matched: bool) -> str:
    if matched:
        return (
            "Row-aligned OCR column contains the normalized secondary term string; "
            "probe only, not claim-grade primary verification."
        )
    return (
        "Row-aligned OCR column does not contain the normalized secondary term string; "
        "this may be OCR failure, transcription difference, or missing primary support."
    )


def summarize_row_probe(
    rows: list[dict[str, str]],
    words: list[TsvWord],
    detected_rows: set[int],
    tsv_status: str,
) -> dict[str, str]:
    row_ids = {row["row_number"] for row in rows if row["row_number"]}
    matched_row_ids = {
        row["row_number"]
        for row in rows
        if row["row_number"] and row["row_ocr_status"] == "matched"
    }
    rows_with_all_terms = {
        row_id
        for row_id in row_ids
        if all(
            row["row_ocr_status"] == "matched"
            for row in rows
            if row["row_number"] == row_id
        )
    }
    matched = count_rows(rows, "row_ocr_status", "matched")
    appellations = [row for row in rows if row["category"] == "wrr_appellation"]
    dates = [row for row in rows if row["category"] == "wrr_date"]
    ocr_text = "".join(word.text for word in words)
    status = "row_ocr_probe_not_verification" if words else "blocked_missing_ocr_dependency"
    return {
        "total_terms": str(len(rows)),
        "matched_terms": str(matched),
        "missing_terms": str(len(rows) - matched),
        "appellation_terms": str(len(appellations)),
        "matched_appellation_terms": str(count_rows(appellations, "row_ocr_status", "matched")),
        "date_terms": str(len(dates)),
        "matched_date_terms": str(count_rows(dates, "row_ocr_status", "matched")),
        "source_rows": str(len(row_ids)),
        "source_rows_with_any_match": str(len(matched_row_ids)),
        "source_rows_with_all_terms_matched": str(len(rows_with_all_terms)),
        "detected_row_markers": str(len(detected_rows)),
        "inferred_row_markers": str(max(0, ROW_COUNT - len(detected_rows))),
        "ocr_words": str(len(words)),
        "ocr_hebrew_letters": str(len(normalize_hebrew_for_match(ocr_text))),
        "tsv_status": tsv_status,
        "status": status,
    }


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary: dict[str, str],
    args: argparse.Namespace,
    tsv_note: str,
) -> None:
    lines = [
        "# WRR Primary Table 2 Row OCR Probe",
        "",
        "Status: row-aligned OCR probe only; not verified primary Hebrew transcription.",
        "",
        "This renders/OCRs the primary WRR 1994 Table 2 page to TSV, derives row",
        "bands from OCR row markers, then checks secondary WRR2 Hebrew terms only",
        "inside the matching row and expected name/date column. It is stronger",
        "triage than full-page OCR, but still not claim-grade verification.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_primary_table2_row_ocr_probe "
            + f"--source {args.source} "
            + (f"--source-records {args.source_records} " if args.source_records else "")
            + f"--terms {args.terms} "
            + f"--tessdata-dir {args.tessdata_dir} "
            + f"--out {args.out} "
            + f"--summary-out {args.summary_out} "
            + f"--markdown-out {args.markdown_out} "
            + f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        f"- TSV status: `{summary['tsv_status']}`",
        f"- TSV note: `{tsv_note}`",
        "",
        "| Item | Count |",
        "| --- | ---: |",
    ]
    for key in SUMMARY_FIELDNAMES:
        lines.append(f"| `{key}` | {markdown_cell(summary[key])} |")
    lines.extend(
        [
            "",
            "## Unmatched Terms",
            "",
            "| Term ID | Category | Michigan | Hebrew normalized | Column |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        if row["row_ocr_status"] == "not_matched":
            lines.append(
                "| "
                + " | ".join(
                    [
                        markdown_cell(row["term_id"]),
                        markdown_cell(row["category"]),
                        markdown_cell(row["michigan_term"]),
                        markdown_cell(row["hebrew_normalized"]),
                        markdown_cell(row["column"]),
                    ]
                )
                + " |"
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary: dict[str, str],
    tsv_note: str,
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "source": str(args.source),
            "source_records": "" if args.source_records is None else str(args.source_records),
            "terms": str(args.terms),
            "tsv": str(args.tsv),
            "tessdata_dir": str(args.tessdata_dir),
        },
        "tsv_note": tsv_note,
        "summary": summary,
        "rows": len(rows),
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
