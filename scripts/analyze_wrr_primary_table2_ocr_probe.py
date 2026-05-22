#!/usr/bin/env python3
"""Probe OCR matches for WRR 1994 primary-PDF Table 2 Hebrew cells."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.import_wrr_terms import WrrRecord, parse_wrr_records


DEFAULT_SOURCE = Path("reports/wrr_1994/wrr_1994_paper.pdf")
DEFAULT_TERMS = Path("reports/wrr_1994/wrr2_terms.csv")
DEFAULT_TESSDATA_DIR = Path("reports/wrr_1994/tessdata")
DEFAULT_RENDER_PREFIX = Path("reports/wrr_1994/wrr_primary_table2_page")
DEFAULT_OCR_BASE = Path("reports/wrr_1994/wrr_primary_table2_heb_ocr")
DEFAULT_OCR_TEXT = Path("reports/wrr_1994/wrr_primary_table2_heb_ocr.txt")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_primary_table2_ocr_probe.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_primary_table2_ocr_probe_summary.csv")
DEFAULT_MD = Path("reports/wrr_1994/wrr_primary_table2_ocr_probe.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_primary_table2_ocr_probe.manifest.json")

MC_TO_HEBREW = {
    "A": "א",
    "B": "ב",
    "G": "ג",
    "D": "ד",
    "H": "ה",
    "W": "ו",
    "Z": "ז",
    "X": "ח",
    "+": "ט",
    "Y": "י",
    "K": "כ",
    "L": "ל",
    "M": "מ",
    "N": "נ",
    "S": "ס",
    "@": "ע",
    "P": "פ",
    "C": "צ",
    "Q": "ק",
    "R": "ר",
    "$": "ש",
    "T": "ת",
}

FINAL_FORMS = str.maketrans({"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"})
HEBREW_LETTER_RE = re.compile(r"[\u05d0-\u05ea]")

FIELDNAMES = [
    "term_id",
    "row_number",
    "concept",
    "category",
    "michigan_term",
    "hebrew_normalized",
    "ocr_status",
    "match_basis",
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
    "ocr_hebrew_letters",
    "ocr_status",
    "status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    terms = read_terms(args)
    ocr_text, ocr_status, ocr_note = acquire_ocr_text(args)
    rows = build_probe_rows(terms, ocr_text)
    summary = summarize(rows, ocr_text, ocr_status)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary, args, ocr_note)
    write_manifest(args, rows, summary, ocr_note, started)
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
    parser.add_argument("--psm", default="4")
    parser.add_argument("--tessdata-dir", type=Path, default=DEFAULT_TESSDATA_DIR)
    parser.add_argument("--render-prefix", type=Path, default=DEFAULT_RENDER_PREFIX)
    parser.add_argument("--ocr-base", type=Path, default=DEFAULT_OCR_BASE)
    parser.add_argument("--ocr-text", type=Path, default=DEFAULT_OCR_TEXT)
    parser.add_argument("--refresh-ocr", action="store_true")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_terms(args: argparse.Namespace) -> list[dict[str, str]]:
    if args.source_records is None:
        return read_rows(args.terms)
    records = parse_wrr_records(args.source_records.read_text(encoding="utf-8"))
    return terms_from_records(records)


def terms_from_records(records: list[WrrRecord]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for record in records:
        concept = f"WRR2 {record.index:02d}"
        for app_index, appellation in enumerate(record.appellations, start=1):
            rows.append(
                {
                    "term_id": f"wrr2_{record.index:02d}_app_{app_index:02d}",
                    "concept": concept,
                    "category": "wrr_appellation",
                    "term": appellation,
                }
            )
        for date_index, date in enumerate(record.dates, start=1):
            rows.append(
                {
                    "term_id": f"wrr2_{record.index:02d}_date_{date_index:02d}",
                    "concept": concept,
                    "category": "wrr_date",
                    "term": date,
                }
            )
    return rows


def acquire_ocr_text(args: argparse.Namespace) -> tuple[str, str, str]:
    if args.ocr_text.exists() and not args.refresh_ocr:
        return args.ocr_text.read_text(encoding="utf-8"), "existing_ocr_text", str(args.ocr_text)

    missing = missing_ocr_dependencies(args)
    if missing:
        args.ocr_text.parent.mkdir(parents=True, exist_ok=True)
        args.ocr_text.write_text("", encoding="utf-8")
        return "", "blocked_missing_ocr_dependency", ", ".join(missing)

    image = render_page(args)
    text_path = run_tesseract(args, image)
    return text_path.read_text(encoding="utf-8"), "generated_ocr_text", str(text_path)


def missing_ocr_dependencies(args: argparse.Namespace) -> list[str]:
    missing = []
    if shutil.which("pdftoppm") is None:
        missing.append("pdftoppm")
    if shutil.which("tesseract") is None:
        missing.append("tesseract")
    if not (args.tessdata_dir / "heb.traineddata").exists():
        missing.append(str(args.tessdata_dir / "heb.traineddata"))
    return missing


def render_page(args: argparse.Namespace) -> Path:
    args.render_prefix.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "pdftoppm",
        "-f",
        str(args.page),
        "-l",
        str(args.page),
        "-r",
        str(args.dpi),
        "-png",
        str(args.source),
        str(args.render_prefix),
    ]
    subprocess.run(cmd, check=True)
    rendered = Path(f"{args.render_prefix}-{args.page:02d}.png")
    if not rendered.exists():
        rendered = Path(f"{args.render_prefix}-{args.page}.png")
    return rendered


def run_tesseract(args: argparse.Namespace, image: Path) -> Path:
    args.ocr_base.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "tesseract",
        "--tessdata-dir",
        str(args.tessdata_dir),
        "-l",
        "heb",
        "--psm",
        str(args.psm),
        str(image),
        str(args.ocr_base),
    ]
    subprocess.run(cmd, check=True)
    return args.ocr_base.with_suffix(".txt")


def build_probe_rows(terms: list[dict[str, str]], ocr_text: str) -> list[dict[str, str]]:
    normalized_ocr = normalize_hebrew_for_match(ocr_text)
    rows = []
    for term in terms:
        hebrew = michigan_to_hebrew_normalized(term.get("term", ""))
        matched = bool(hebrew and hebrew in normalized_ocr)
        rows.append(
            {
                "term_id": term.get("term_id", ""),
                "row_number": row_number_from_term_id(term.get("term_id", "")),
                "concept": term.get("concept", ""),
                "category": term.get("category", ""),
                "michigan_term": term.get("term", ""),
                "hebrew_normalized": hebrew,
                "ocr_status": "matched" if matched else "not_matched",
                "match_basis": "full_page_ocr_exact_normalized_substring",
                "current_read": current_read(matched),
            }
        )
    return rows


def michigan_to_hebrew_normalized(value: str) -> str:
    return normalize_hebrew_for_match("".join(MC_TO_HEBREW.get(char, "") for char in value))


def normalize_hebrew_for_match(value: str) -> str:
    normalized = value.translate(FINAL_FORMS)
    return "".join(char for char in normalized if HEBREW_LETTER_RE.fullmatch(char))


def row_number_from_term_id(term_id: str) -> str:
    parts = term_id.split("_")
    return parts[1] if len(parts) > 1 and parts[1].isdigit() else ""


def current_read(matched: bool) -> str:
    if matched:
        return (
            "OCR text contains the normalized secondary term string; probe only, "
            "not row-aligned primary verification."
        )
    return (
        "OCR text does not contain the normalized secondary term string; this may be "
        "OCR failure, transcription difference, or missing primary support."
    )


def summarize(
    rows: list[dict[str, str]],
    ocr_text: str,
    ocr_status: str,
) -> dict[str, str]:
    row_ids = {row["row_number"] for row in rows if row["row_number"]}
    matched_row_ids = {
        row["row_number"]
        for row in rows
        if row["row_number"] and row["ocr_status"] == "matched"
    }
    rows_with_all_terms = {
        row_id
        for row_id in row_ids
        if all(
            row["ocr_status"] == "matched"
            for row in rows
            if row["row_number"] == row_id
        )
    }
    matched = count_rows(rows, "ocr_status", "matched")
    appellations = [row for row in rows if row["category"] == "wrr_appellation"]
    dates = [row for row in rows if row["category"] == "wrr_date"]
    status = "ocr_probe_not_verification" if ocr_text else "blocked_missing_ocr_dependency"
    return {
        "total_terms": str(len(rows)),
        "matched_terms": str(matched),
        "missing_terms": str(len(rows) - matched),
        "appellation_terms": str(len(appellations)),
        "matched_appellation_terms": str(count_rows(appellations, "ocr_status", "matched")),
        "date_terms": str(len(dates)),
        "matched_date_terms": str(count_rows(dates, "ocr_status", "matched")),
        "source_rows": str(len(row_ids)),
        "source_rows_with_any_match": str(len(matched_row_ids)),
        "source_rows_with_all_terms_matched": str(len(rows_with_all_terms)),
        "ocr_hebrew_letters": str(len(normalize_hebrew_for_match(ocr_text))),
        "ocr_status": ocr_status,
        "status": status,
    }


def count_rows(rows: list[dict[str, str]], key: str, value: str) -> int:
    return sum(1 for row in rows if row.get(key) == value)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary: dict[str, str],
    args: argparse.Namespace,
    ocr_note: str,
) -> None:
    lines = [
        "# WRR Primary Table 2 OCR Probe",
        "",
        "Status: OCR probe only; not a verified primary Hebrew transcription.",
        "",
        "This renders/OCRs the primary WRR 1994 Table 2 page when Hebrew",
        "Tesseract data is available, then checks whether normalized secondary",
        "WRR2 terms appear somewhere in the full-page OCR text. It is useful",
        "for triage, but it is not row-aligned and must not be treated as",
        "claim-grade term verification.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_primary_table2_ocr_probe "
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
        f"- OCR status: `{summary['ocr_status']}`",
        f"- OCR note: `{ocr_note}`",
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
            "| Term ID | Category | Michigan | Hebrew normalized |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        if row["ocr_status"] == "not_matched":
            lines.append(
                "| "
                + " | ".join(
                    [
                        markdown_cell(row["term_id"]),
                        markdown_cell(row["category"]),
                        markdown_cell(row["michigan_term"]),
                        markdown_cell(row["hebrew_normalized"]),
                    ]
                )
                + " |"
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary: dict[str, str],
    ocr_note: str,
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
            "ocr_text": str(args.ocr_text),
            "tessdata_dir": str(args.tessdata_dir),
        },
        "ocr_note": ocr_note,
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
