#!/usr/bin/env python3
"""Build local OCR review sidecars for unreadable Cities PDFs without tracking OCR text."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_unreadable_pdf_ocr_feasibility import (
    DEFAULT_REVIEW,
    available_tesseract_languages,
    markdown_cell,
    markdown_link,
    ocr_text_signal_chars,
    pages_to_attempt,
)


DEFAULT_BASE_DIR = Path("reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review")
DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_packet.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_packet_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_PACKET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_packet.manifest.json"
)

CLAIM_BOUNDARY = (
    "OCR review packet only; OCR text sidecars and page images are ignored local "
    "review aids; no OCR text in tracked files, no repaired text, no source-row "
    "import, no city normalization, no ELS, no compactness, no p-level"
)

FIELDNAMES = [
    "label",
    "family",
    "lane",
    "page_number",
    "pdf_pages",
    "image_path",
    "ocr_text_path",
    "image_exists",
    "ocr_text_exists",
    "ocr_text_signal_chars",
    "ocr_word_count",
    "ocr_line_count",
    "ocr_status",
    "ocr_note",
    "language",
    "dpi",
    "psm",
    "selected_path",
    "url",
    "claim_boundary",
    "next_manual_action",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    review_rows = read_csv(args.review)
    rows = build_review_packet_rows(review_rows, args)
    summary = build_summary(rows)
    write_csv(args.out, FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary)
    write_markdown(args.markdown_out, rows, summary, args)
    write_manifest(args.manifest_out, args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--base-dir", type=Path, default=DEFAULT_BASE_DIR)
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
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_review_packet_rows(
    review_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    missing = missing_dependencies(args.language)
    rows: list[dict[str, str]] = []
    for review in review_rows:
        page_count = pages_to_attempt(review.get("pdf_pages", ""), args.max_pages)
        for page in range(1, page_count + 1):
            rows.append(build_page_row(review, page, args, missing))
    return rows


def missing_dependencies(language: str) -> list[str]:
    missing: list[str] = []
    if shutil.which("pdftoppm") is None:
        missing.append("pdftoppm")
    if shutil.which("tesseract") is None:
        missing.append("tesseract")
    elif language not in available_tesseract_languages():
        missing.append(f"tesseract_language:{language}")
    return missing


def build_page_row(
    review: dict[str, str],
    page: int,
    args: argparse.Namespace,
    missing: list[str],
) -> dict[str, str]:
    label = review.get("label", "")
    image_path = args.base_dir / "page_images" / f"{label}_p{page:03d}.png"
    ocr_text_path = args.base_dir / "ocr_text" / f"{label}_p{page:03d}.txt"
    source = Path(review.get("selected_path", ""))
    if missing:
        return page_row(review, page, image_path, ocr_text_path, args, "blocked_missing_dependency", ", ".join(missing))
    if not source.exists():
        return page_row(review, page, image_path, ocr_text_path, args, "source_missing", str(source))
    try:
        render_page_to_path(source, page, args.dpi, image_path)
        text = run_tesseract(image_path, args.language, args.psm)
        write_ocr_text(ocr_text_path, text)
    except (OSError, subprocess.SubprocessError) as error:
        return page_row(review, page, image_path, ocr_text_path, args, "ocr_error", str(error))
    signal_chars = ocr_text_signal_chars(text)
    return page_row(
        review,
        page,
        image_path,
        ocr_text_path,
        args,
        "page_ocr_text_detected" if signal_chars >= 20 else "page_ocr_empty",
        "",
        signal_chars=signal_chars,
        word_count=ocr_word_count(text),
        line_count=ocr_line_count(text),
    )


def page_row(
    review: dict[str, str],
    page: int,
    image_path: Path,
    ocr_text_path: Path,
    args: argparse.Namespace,
    status: str,
    note: str,
    *,
    signal_chars: int = 0,
    word_count: int = 0,
    line_count: int = 0,
) -> dict[str, str]:
    return {
        "label": review.get("label", ""),
        "family": review.get("family", ""),
        "lane": review.get("lane", ""),
        "page_number": str(page),
        "pdf_pages": review.get("pdf_pages", ""),
        "image_path": str(image_path),
        "ocr_text_path": str(ocr_text_path),
        "image_exists": str(image_path.exists()).lower(),
        "ocr_text_exists": str(ocr_text_path.exists()).lower(),
        "ocr_text_signal_chars": str(signal_chars),
        "ocr_word_count": str(word_count),
        "ocr_line_count": str(line_count),
        "ocr_status": status,
        "ocr_note": note,
        "language": args.language,
        "dpi": str(args.dpi),
        "psm": str(args.psm),
        "selected_path": review.get("selected_path", ""),
        "url": review.get("url", ""),
        "claim_boundary": CLAIM_BOUNDARY,
        "next_manual_action": next_manual_action(status),
    }


def render_page_to_path(source: Path, page: int, dpi: int, image_path: Path) -> None:
    image_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = image_path.with_suffix("")
    for stale in image_path.parent.glob(f"{prefix.name}-*.png"):
        stale.unlink()
    subprocess.run(
        [
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
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    candidates = sorted(image_path.parent.glob(f"{prefix.name}-*.png"))
    if not candidates:
        raise FileNotFoundError(f"pdftoppm did not render page {page}")
    candidates[0].replace(image_path)
    for extra in candidates[1:]:
        extra.unlink(missing_ok=True)


def run_tesseract(image_path: Path, language: str, psm: str) -> str:
    completed = subprocess.run(
        [
            "tesseract",
            str(image_path),
            "stdout",
            "-l",
            language,
            "--psm",
            str(psm),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def write_ocr_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def ocr_word_count(text: str) -> int:
    return sum(1 for token in text.split() if any(char.isalnum() for char in token))


def ocr_line_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def next_manual_action(status: str) -> str:
    if status == "page_ocr_text_detected":
        return "review OCR text sidecar against page image before any source-row use"
    if status == "page_ocr_empty":
        return "review page image manually; OCR did not produce text signal"
    if status == "source_missing":
        return "recover source PDF before review"
    if status == "blocked_missing_dependency":
        return "install OCR dependency before review"
    return "inspect OCR error before review"


def build_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    statuses = Counter(row["ocr_status"] for row in rows)
    rows_with_text = [row for row in rows if int(row["ocr_text_signal_chars"]) >= 20]
    summary = [
        {"metric": "page_rows", "value": str(len(rows))},
        {"metric": "pdf_rows", "value": str(len({row["label"] for row in rows}))},
        {"metric": "pages_with_ocr_text", "value": str(len(rows_with_text))},
        {
            "metric": "pages_without_ocr_text",
            "value": str(len(rows) - len(rows_with_text)),
        },
        {
            "metric": "ocr_text_signal_chars",
            "value": str(sum(int(row["ocr_text_signal_chars"]) for row in rows)),
        },
        {
            "metric": "ocr_words",
            "value": str(sum(int(row["ocr_word_count"]) for row in rows)),
        },
        {
            "metric": "ocr_lines",
            "value": str(sum(int(row["ocr_line_count"]) for row in rows)),
        },
        {
            "metric": "image_sidecars",
            "value": str(sum(1 for row in rows if row["image_exists"] == "true")),
        },
        {
            "metric": "ocr_text_sidecars",
            "value": str(sum(1 for row in rows if row["ocr_text_exists"] == "true")),
        },
    ]
    for status in sorted(statuses):
        summary.append({"metric": f"status_{status}", "value": str(statuses[status])})
    summary.append({"metric": "claim_boundary", "value": CLAIM_BOUNDARY})
    return summary


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Unreadable PDF OCR Review Packet",
        "",
        f"Status: OCR review packet only. This renders local page images and OCR text sidecars for {summary['pdf_rows']} recovered unreadable Cities PDF rows, then records only paths/counts/status in tracked files.",
        "It does not track OCR text, repair text, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_unreadable_pdf_ocr_review_packet "
            f"--review {args.review} "
            f"--base-dir {args.base_dir} "
            f"--language {args.language} "
            f"--dpi {args.dpi} "
            f"--psm {args.psm} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        f"- PDF rows: {summary['pdf_rows']}.",
        f"- Page rows: {summary['page_rows']}.",
        f"- Pages with OCR text: {summary['pages_with_ocr_text']}.",
        f"- Pages without OCR text: {summary['pages_without_ocr_text']}.",
        f"- OCR text signal chars: {summary['ocr_text_signal_chars']}.",
        f"- OCR words: {summary['ocr_words']}.",
        f"- OCR lines: {summary['ocr_lines']}.",
        f"- Image sidecars: {summary['image_sidecars']}.",
        f"- OCR text sidecars: {summary['ocr_text_sidecars']}.",
        f"- Page OCR text detected rows: {summary.get('status_page_ocr_text_detected', '0')}.",
        f"- Page OCR empty rows: {summary.get('status_page_ocr_empty', '0')}.",
        f"- OCR error rows: {summary.get('status_ocr_error', '0')}.",
        f"- Boundary: {CLAIM_BOUNDARY}",
        "",
        "## Page Packet",
        "",
        "| Label | Page | Signal chars | Words | Lines | Status | Image | OCR text sidecar | Next action |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["label"]),
                    markdown_cell(row["page_number"]),
                    markdown_cell(row["ocr_text_signal_chars"]),
                    markdown_cell(row["ocr_word_count"]),
                    markdown_cell(row["ocr_line_count"]),
                    markdown_cell(row["ocr_status"]),
                    markdown_file_link("image", row["image_path"]),
                    markdown_file_link("ocr text", row["ocr_text_path"]),
                    markdown_cell(row["next_manual_action"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "- OCR text sidecars are ignored local review aids, not tracked source text.",
            "- OCR text must be checked against page images before any source-row use.",
            "- This packet does not decide source admissibility or create city-name rows.",
            "- Any later transcription decisions need separate citable decision records.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_file_link(label: str, path: str) -> str:
    if not path:
        return ""
    return markdown_link(label, "../" + path)


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
        "inputs": {"review": str(args.review)},
        "parameters": {
            "base_dir": str(args.base_dir),
            "language": args.language,
            "dpi": args.dpi,
            "psm": args.psm,
            "max_pages": args.max_pages,
        },
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
