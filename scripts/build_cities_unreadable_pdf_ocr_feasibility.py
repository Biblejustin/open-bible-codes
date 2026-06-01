#!/usr/bin/env python3
"""Probe OCR feasibility for recovered unreadable Cities PDFs without storing OCR text."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import tempfile
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_wrr_wayback_source_recovery_probe import markdown_cell, markdown_link


DEFAULT_REVIEW = Path("reports/cities_pdf_recovery_probe/cities_unreadable_pdf_review.csv")
DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_feasibility.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_feasibility_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_UNREADABLE_PDF_OCR_FEASIBILITY.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_feasibility.manifest.json"
)

FIELDNAMES = [
    "label",
    "family",
    "lane",
    "pdf_pages",
    "pages_attempted",
    "pages_with_ocr_text",
    "ocr_text_signal_chars",
    "avg_signal_chars_per_page",
    "ocr_status",
    "ocr_note",
    "language",
    "dpi",
    "psm",
    "selected_path",
    "url",
    "claim_boundary",
]

SUMMARY_FIELDNAMES = ["metric", "value"]

CLAIM_BOUNDARY = (
    "OCR feasibility only; no OCR text stored in tracked files, no repaired text, "
    "no source-row import, no city normalization, no ELS, no compactness, no p-level"
)


@dataclass(frozen=True)
class OcrResult:
    pages_attempted: int
    pages_with_text: int
    signal_chars: int
    status: str
    note: str


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    review_rows = read_csv(args.review)
    results = collect_ocr_results(review_rows, args)
    rows = build_probe_rows(review_rows, results, args)
    summary = build_summary(rows)
    write_csv(args.out, FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary)
    write_markdown(args.markdown_out, rows, summary)
    write_manifest(args.manifest_out, args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--language", default="eng")
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--psm", default="6")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="maximum pages per PDF to OCR; 0 means all pages declared in review CSV",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def collect_ocr_results(
    review_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, OcrResult]:
    missing = missing_dependencies(args.language)
    results: dict[str, OcrResult] = {}
    for row in review_rows:
        if missing:
            results[row["label"]] = OcrResult(
                pages_attempted=0,
                pages_with_text=0,
                signal_chars=0,
                status="blocked_missing_dependency",
                note=", ".join(missing),
            )
            continue
        results[row["label"]] = run_ocr_for_row(row, args)
    return results


def missing_dependencies(language: str) -> list[str]:
    missing: list[str] = []
    if shutil.which("pdftoppm") is None:
        missing.append("pdftoppm")
    if shutil.which("tesseract") is None:
        missing.append("tesseract")
    elif language not in available_tesseract_languages():
        missing.append(f"tesseract_language:{language}")
    return missing


def available_tesseract_languages() -> set[str]:
    completed = subprocess.run(
        ["tesseract", "--list-langs"],
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip() and not line.startswith("List of available languages")
    }


def run_ocr_for_row(row: dict[str, str], args: argparse.Namespace) -> OcrResult:
    source = Path(row.get("selected_path", ""))
    if not source.exists():
        return OcrResult(0, 0, 0, "source_missing", str(source))
    page_count = pages_to_attempt(row.get("pdf_pages", ""), args.max_pages)
    if page_count <= 0:
        return OcrResult(0, 0, 0, "no_pages_attempted", "missing page count")

    total_chars = 0
    pages_with_text = 0
    pages_attempted = 0
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="cities-ocr-") as tmp:
        tmp_path = Path(tmp)
        for page in range(1, page_count + 1):
            pages_attempted += 1
            try:
                image = render_page(source, page, args.dpi, tmp_path)
                text = run_tesseract(image, args.language, args.psm)
            except (OSError, subprocess.SubprocessError) as error:
                errors.append(f"page {page}: {error}")
                continue
            signal = ocr_text_signal_chars(text)
            total_chars += signal
            if signal >= 20:
                pages_with_text += 1
    status = classify_ocr_status(total_chars, pages_with_text, errors)
    return OcrResult(
        pages_attempted=pages_attempted,
        pages_with_text=pages_with_text,
        signal_chars=total_chars,
        status=status,
        note="; ".join(errors[:3]),
    )


def pages_to_attempt(pdf_pages: str, max_pages: int) -> int:
    try:
        pages = int(pdf_pages)
    except ValueError:
        return 0
    if max_pages > 0:
        return min(pages, max_pages)
    return pages


def render_page(source: Path, page: int, dpi: int, tmp_path: Path) -> Path:
    prefix = tmp_path / f"page_{page}"
    command = [
        "pdftoppm",
        "-f",
        str(page),
        "-l",
        str(page),
        "-r",
        str(dpi),
        "-png",
        str(source),
        str(prefix),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    candidates = sorted(tmp_path.glob(f"page_{page}-*.png"))
    if not candidates:
        raise FileNotFoundError(f"pdftoppm did not render page {page}")
    return candidates[0]


def run_tesseract(image: Path, language: str, psm: str) -> str:
    command = [
        "tesseract",
        str(image),
        "stdout",
        "-l",
        language,
        "--psm",
        str(psm),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return completed.stdout


def ocr_text_signal_chars(text: str) -> int:
    return sum(1 for char in text if char.isalpha() or char.isdigit())


def classify_ocr_status(total_chars: int, pages_with_text: int, errors: list[str]) -> str:
    if errors and total_chars == 0:
        return "ocr_error"
    if total_chars >= 100 and pages_with_text > 0:
        return "ocr_text_detected"
    if total_chars > 0:
        return "low_ocr_text"
    return "ocr_empty"


def build_probe_rows(
    review_rows: list[dict[str, str]],
    results: dict[str, OcrResult],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for review in review_rows:
        result = results[review["label"]]
        avg_chars = (
            f"{result.signal_chars / result.pages_attempted:.1f}"
            if result.pages_attempted
            else "0.0"
        )
        rows.append(
            {
                "label": review.get("label", ""),
                "family": review.get("family", ""),
                "lane": review.get("lane", ""),
                "pdf_pages": review.get("pdf_pages", ""),
                "pages_attempted": str(result.pages_attempted),
                "pages_with_ocr_text": str(result.pages_with_text),
                "ocr_text_signal_chars": str(result.signal_chars),
                "avg_signal_chars_per_page": avg_chars,
                "ocr_status": result.status,
                "ocr_note": result.note,
                "language": args.language,
                "dpi": str(args.dpi),
                "psm": str(args.psm),
                "selected_path": review.get("selected_path", ""),
                "url": review.get("url", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(rows, key=lambda row: (row["ocr_status"], row["lane"], row["label"]))


def build_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    statuses = Counter(row["ocr_status"] for row in rows)
    rows_with_text = sum(1 for row in rows if int(row["pages_with_ocr_text"]) > 0)
    pages_attempted = sum(int(row["pages_attempted"]) for row in rows)
    pages_with_text = sum(int(row["pages_with_ocr_text"]) for row in rows)
    signal_chars = sum(int(row["ocr_text_signal_chars"]) for row in rows)
    summary = [
        {"metric": "rows_reviewed", "value": str(len(rows))},
        {"metric": "rows_with_ocr_text", "value": str(rows_with_text)},
        {"metric": "pages_attempted", "value": str(pages_attempted)},
        {"metric": "pages_with_ocr_text", "value": str(pages_with_text)},
        {"metric": "ocr_text_signal_chars", "value": str(signal_chars)},
    ]
    for status in sorted(statuses):
        summary.append({"metric": f"status_{status}", "value": str(statuses[status])})
    summary.append({"metric": "claim_boundary", "value": CLAIM_BOUNDARY})
    return summary


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary: list[dict[str, str]],
) -> None:
    values = {row["metric"]: row["value"] for row in summary}
    lines = [
        "# Cities Unreadable PDF OCR Feasibility",
        "",
        f"Status: OCR feasibility only. This runs local OCR against {values['rows_reviewed']}",
        "recovered unreadable Cities PDF rows and records only counts/status. It does",
        "not store OCR text in tracked files, repair text, import source rows,",
        "normalize city names, run ELS searches, compute compactness, or verify",
        "p-levels.",
        "",
        "## Summary",
        "",
        f"- Rows reviewed: {values['rows_reviewed']}.",
        f"- Rows with OCR text: {values['rows_with_ocr_text']}.",
        f"- Pages attempted: {values['pages_attempted']}.",
        f"- Pages with OCR text: {values['pages_with_ocr_text']}.",
        f"- OCR text signal chars: {values['ocr_text_signal_chars']}.",
        f"- OCR text detected rows: {values.get('status_ocr_text_detected', '0')}.",
        f"- Low OCR text rows: {values.get('status_low_ocr_text', '0')}.",
        f"- OCR empty rows: {values.get('status_ocr_empty', '0')}.",
        f"- OCR error rows: {values.get('status_ocr_error', '0')}.",
        "",
        "## Rows",
        "",
        "| Label | Lane | Pages attempted | Pages with text | Signal chars | Avg chars/page | Status | URL |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["label"]),
                    f"`{markdown_cell(row['lane'])}`",
                    markdown_cell(row["pages_attempted"]),
                    markdown_cell(row["pages_with_ocr_text"]),
                    markdown_cell(row["ocr_text_signal_chars"]),
                    markdown_cell(row["avg_signal_chars_per_page"]),
                    markdown_cell(row["ocr_status"]),
                    markdown_link("url", row["url"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "This probe records OCR feasibility metrics only. It does not publish OCR",
            "text, repair text, decide source admissibility, create city-name rows,",
            "or make a result-bearing claim. Any OCR text used later must be reviewed",
            "against page images and locked before source-row normalization or ELS",
            "work.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {"review": str(args.review)},
        "parameters": {
            "language": args.language,
            "dpi": args.dpi,
            "psm": args.psm,
            "max_pages": args.max_pages,
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary},
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
