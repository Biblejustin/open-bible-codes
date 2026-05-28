#!/usr/bin/env python3
"""Build local Hebrew OCR sidecars for locked Cities source pages."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell
from scripts.build_cities_source_page_review_bundle import DEFAULT_OUT as DEFAULT_BUNDLE


DEFAULT_BASE_DIR = Path("reports/cities_pdf_recovery_probe/source_page_ocr_review")
DEFAULT_TESSDATA_DIR = Path("reports/wrr_1994/tessdata")
DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_packet.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_packet_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_OCR_REVIEW_PACKET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_packet.manifest.json"
)

NO_INPUT_BOUNDARY = (
    "Source-page OCR review packet only; OCR text sidecars are ignored local "
    "review aids, no OCR body text or source-script body text in tracked files, "
    "no source-row import, no city normalization, no ELS, no compactness, no p-level"
)

HEBREW_RE = re.compile(r"[\u0590-\u05ff]")

FIELDNAMES = [
    "ocr_rank",
    "transcription_decision_id",
    "source_lock_decision_id",
    "label",
    "page_number",
    "page_class",
    "page_image_path",
    "page_image_exists",
    "ocr_text_path",
    "ocr_text_exists",
    "ocr_status",
    "ocr_note",
    "ocr_text_signal_chars",
    "ocr_hebrew_letters",
    "ocr_word_count",
    "ocr_line_count",
    "language",
    "psm",
    "tessdata_dir",
    "source_row_import",
    "city_name_normalization",
    "els_runs",
    "compactness_runs",
    "p_levels",
    "no_input_boundary",
    "next_manual_action",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    bundle_rows = read_rows(args.bundle)
    rows = build_ocr_packet_rows(bundle_rows, args)
    summary_rows = build_summary_rows(rows, args)
    write_csv(args.out, FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--base-dir", type=Path, default=DEFAULT_BASE_DIR)
    parser.add_argument("--tessdata-dir", type=Path, default=DEFAULT_TESSDATA_DIR)
    parser.add_argument("--language", default="heb")
    parser.add_argument("--psm", default="4")
    parser.add_argument("--refresh-ocr", action="store_true")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_ocr_packet_rows(
    bundle_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    missing = missing_dependencies(args)
    rows: list[dict[str, str]] = []
    for rank, bundle_row in enumerate(bundle_rows, start=1):
        rows.append(build_ocr_packet_row(rank, bundle_row, args, missing))
    return rows


def build_ocr_packet_row(
    rank: int,
    bundle_row: dict[str, str],
    args: argparse.Namespace,
    missing: list[str],
) -> dict[str, str]:
    image_path = Path(bundle_row.get("page_image_path", ""))
    transcription_id = bundle_row.get("transcription_decision_id", "")
    ocr_text_path = args.base_dir / "ocr_text" / f"{safe_stem(transcription_id)}.txt"
    if missing:
        return page_row(
            rank,
            bundle_row,
            image_path,
            ocr_text_path,
            args,
            "blocked_missing_ocr_dependency",
            ", ".join(missing),
        )
    if not image_path.exists():
        return page_row(
            rank,
            bundle_row,
            image_path,
            ocr_text_path,
            args,
            "source_page_image_missing",
            str(image_path),
        )
    try:
        if args.refresh_ocr or not ocr_text_path.exists():
            text = run_tesseract(image_path, args)
            write_local_ocr_text(ocr_text_path, text)
        else:
            text = ocr_text_path.read_text(encoding="utf-8")
    except (OSError, subprocess.SubprocessError) as error:
        return page_row(
            rank,
            bundle_row,
            image_path,
            ocr_text_path,
            args,
            "ocr_error",
            str(error),
        )
    signal_chars = ocr_text_signal_chars(text)
    hebrew_letters = ocr_hebrew_letters(text)
    status = classify_ocr_status(signal_chars, hebrew_letters)
    return page_row(
        rank,
        bundle_row,
        image_path,
        ocr_text_path,
        args,
        status,
        "",
        signal_chars=signal_chars,
        hebrew_letters=hebrew_letters,
        word_count=ocr_word_count(text),
        line_count=ocr_line_count(text),
    )


def missing_dependencies(args: argparse.Namespace) -> list[str]:
    missing: list[str] = []
    if shutil.which("tesseract") is None:
        missing.append("tesseract")
    traineddata = args.tessdata_dir / f"{args.language}.traineddata"
    if not traineddata.exists():
        missing.append(str(traineddata))
    return missing


def run_tesseract(image_path: Path, args: argparse.Namespace) -> str:
    completed = subprocess.run(
        [
            "tesseract",
            "--tessdata-dir",
            str(args.tessdata_dir),
            "-l",
            args.language,
            "--psm",
            str(args.psm),
            str(image_path),
            "stdout",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def page_row(
    rank: int,
    bundle_row: dict[str, str],
    image_path: Path,
    ocr_text_path: Path,
    args: argparse.Namespace,
    status: str,
    note: str,
    *,
    signal_chars: int = 0,
    hebrew_letters: int = 0,
    word_count: int = 0,
    line_count: int = 0,
) -> dict[str, str]:
    return {
        "ocr_rank": str(rank),
        "transcription_decision_id": bundle_row.get("transcription_decision_id", ""),
        "source_lock_decision_id": bundle_row.get("source_lock_decision_id", ""),
        "label": bundle_row.get("label", ""),
        "page_number": bundle_row.get("page_number", ""),
        "page_class": bundle_row.get("page_class", ""),
        "page_image_path": str(image_path),
        "page_image_exists": str(image_path.exists()).lower(),
        "ocr_text_path": str(ocr_text_path),
        "ocr_text_exists": str(ocr_text_path.exists()).lower(),
        "ocr_status": status,
        "ocr_note": note,
        "ocr_text_signal_chars": str(signal_chars),
        "ocr_hebrew_letters": str(hebrew_letters),
        "ocr_word_count": str(word_count),
        "ocr_line_count": str(line_count),
        "language": args.language,
        "psm": str(args.psm),
        "tessdata_dir": str(args.tessdata_dir),
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "no_input_boundary": NO_INPUT_BOUNDARY,
        "next_manual_action": next_manual_action(status),
    }


def classify_ocr_status(signal_chars: int, hebrew_letters: int) -> str:
    if hebrew_letters >= 20:
        return "source_page_ocr_text_detected"
    if signal_chars > 0:
        return "source_page_low_ocr_text"
    return "source_page_ocr_empty"


def next_manual_action(status: str) -> str:
    if status == "source_page_ocr_text_detected":
        return "manual compare ignored OCR sidecar to page image; do not import rows"
    if status == "source_page_low_ocr_text":
        return "manual inspect page image; OCR sidecar is weak"
    if status == "source_page_ocr_empty":
        return "manual inspect page image; OCR produced no usable signal"
    if status == "blocked_missing_ocr_dependency":
        return "restore local Hebrew OCR dependency before OCR review"
    if status == "source_page_image_missing":
        return "restore page image before OCR review"
    return "manual inspect OCR error before using page"


def build_summary_rows(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    statuses = Counter(row["ocr_status"] for row in rows)
    return [
        metric("source_page_ocr_rows", len(rows)),
        metric("page_images_found", count_value(rows, "page_image_exists", "true")),
        metric("page_images_missing", count_value(rows, "page_image_exists", "false")),
        metric("ocr_pages_attempted", attempted_count(rows)),
        metric("pages_with_ocr_text", statuses["source_page_ocr_text_detected"]),
        metric("pages_with_low_ocr_text", statuses["source_page_low_ocr_text"]),
        metric("pages_with_empty_ocr_text", statuses["source_page_ocr_empty"]),
        metric("ocr_errors", statuses["ocr_error"]),
        metric("blocked_missing_ocr_dependency", statuses["blocked_missing_ocr_dependency"]),
        metric("ocr_text_sidecars", count_value(rows, "ocr_text_exists", "true")),
        metric("ocr_text_signal_chars", sum_int(rows, "ocr_text_signal_chars")),
        metric("ocr_hebrew_letters", sum_int(rows, "ocr_hebrew_letters")),
        metric("ocr_words", sum_int(rows, "ocr_word_count")),
        metric("ocr_lines", sum_int(rows, "ocr_line_count")),
        metric("language", args.language),
        metric("psm", args.psm),
        metric("tessdata_dir", args.tessdata_dir),
        metric("source_row_imports", 0),
        metric("city_name_normalization", 0),
        metric("els_runs", 0),
        metric("compactness_runs", 0),
        metric("p_levels", 0),
        metric("no_input_boundary", NO_INPUT_BOUNDARY),
    ]


def attempted_count(rows: list[dict[str, str]]) -> int:
    blocked = {"blocked_missing_ocr_dependency", "source_page_image_missing"}
    return sum(1 for row in rows if row["ocr_status"] not in blocked)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Source Page OCR Review Packet",
        "",
        "Status: local Hebrew OCR review packet for locked Cities source pages.",
        "OCR text sidecars are local ignored review aids only.",
        "Tracked files contain no OCR body text or source-script body text.",
        "This does not import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_ocr_review_packet "
            f"--bundle {args.bundle} "
            f"--base-dir {args.base_dir} "
            f"--tessdata-dir {args.tessdata_dir} "
            f"--language {args.language} "
            f"--psm {args.psm} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Source-page OCR rows: {summary['source_page_ocr_rows']}.",
        f"- Page images found: {summary['page_images_found']}.",
        f"- Page images missing: {summary['page_images_missing']}.",
        f"- OCR pages attempted: {summary['ocr_pages_attempted']}.",
        f"- Pages with OCR text: {summary['pages_with_ocr_text']}.",
        f"- Pages with low OCR text: {summary['pages_with_low_ocr_text']}.",
        f"- Pages with empty OCR text: {summary['pages_with_empty_ocr_text']}.",
        f"- OCR errors: {summary['ocr_errors']}.",
        f"- Missing OCR dependency rows: {summary['blocked_missing_ocr_dependency']}.",
        f"- OCR text sidecars: {summary['ocr_text_sidecars']}.",
        f"- OCR text signal chars: {summary['ocr_text_signal_chars']}.",
        f"- OCR Hebrew letters: {summary['ocr_hebrew_letters']}.",
        f"- OCR words: {summary['ocr_words']}.",
        f"- OCR lines: {summary['ocr_lines']}.",
        f"- Language: `{summary['language']}`.",
        f"- PSM: `{summary['psm']}`.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- City-name normalization: {summary['city_name_normalization']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- p-levels: {summary['p_levels']}.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Packet Rows",
        "",
        "| Rank | Transcription id | Label | Page | Class | Status | Hebrew letters | Words | Sidecar | Next manual action |",
        "| ---: | --- | --- | ---: | --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["ocr_rank"]),
                    f"`{markdown_cell(row['transcription_decision_id'])}`",
                    markdown_cell(row["label"]),
                    markdown_cell(row["page_number"]),
                    f"`{markdown_cell(row['page_class'])}`",
                    f"`{markdown_cell(row['ocr_status'])}`",
                    markdown_cell(row["ocr_hebrew_letters"]),
                    markdown_cell(row["ocr_word_count"]),
                    f"`{markdown_cell(row['ocr_text_path'])}`",
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
            "- OCR sidecar availability is not transcription verification.",
            "- OCR counts are review logistics only; the tracked packet does not quote source text.",
            "- Future source-row import still requires readable transcription, row/column alignment evidence, and an explicit import decision record.",
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
        "inputs": {
            "bundle": str(args.bundle),
            "tessdata_dir": str(args.tessdata_dir),
            "language": args.language,
            "psm": str(args.psm),
        },
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
            "base_dir": str(args.base_dir),
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


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_local_ocr_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def safe_stem(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._") or "ocr"


def ocr_text_signal_chars(text: str) -> int:
    return sum(1 for char in text if char.isalpha() or char.isdigit())


def ocr_hebrew_letters(text: str) -> int:
    return sum(1 for char in text if HEBREW_RE.fullmatch(char))


def ocr_word_count(text: str) -> int:
    return sum(1 for token in text.split() if any(char.isalnum() for char in token))


def ocr_line_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def count_value(rows: list[dict[str, str]], key: str, value: str) -> int:
    return sum(1 for row in rows if row.get(key) == value)


def sum_int(rows: list[dict[str, str]], key: str) -> int:
    total = 0
    for row in rows:
        try:
            total += int(row.get(key, "0"))
        except ValueError:
            continue
    return total


def metric(name: str, value: object) -> dict[str, str]:
    return {"metric": name, "value": str(value)}


if __name__ == "__main__":
    raise SystemExit(main())
