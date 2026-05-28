#!/usr/bin/env python3
"""Build local line-crop review packet for Cities table candidate pages."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_source_page_ocr_review_packet import (
    DEFAULT_OUT as DEFAULT_OCR_PACKET,
)
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_BASE_DIR = Path("reports/cities_pdf_recovery_probe/source_page_line_crops")
DEFAULT_TESSDATA_DIR = Path("reports/wrr_1994/tessdata")
DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_PACKET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet.manifest.json"
)

NO_INPUT_BOUNDARY = (
    "Line crops are local review aids only; tracked files contain no OCR body "
    "text or source-script body text, no verified transcription, no source-row "
    "import, no city normalization, no ELS, no compactness, no p-level"
)

HEBREW_RE = re.compile(r"[\u0590-\u05ff]")

FIELDNAMES = [
    "line_rank",
    "transcription_decision_id",
    "label",
    "page_number",
    "page_class",
    "page_line_rank",
    "page_image_path",
    "tsv_path",
    "tsv_exists",
    "line_left",
    "line_top",
    "line_right",
    "line_bottom",
    "line_width",
    "line_height",
    "crop_left",
    "crop_top",
    "crop_right",
    "crop_bottom",
    "crop_width",
    "crop_height",
    "crop_path",
    "crop_exists",
    "ocr_word_count",
    "ocr_hebrew_letters",
    "source_row_import",
    "city_name_normalization",
    "els_runs",
    "compactness_runs",
    "p_levels",
    "no_input_boundary",
    "next_manual_action",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


@dataclass(frozen=True)
class TsvWord:
    text: str
    left: int
    top: int
    width: int
    height: int
    block_num: str
    par_num: str
    line_num: str

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height


@dataclass(frozen=True)
class LineBox:
    left: int
    top: int
    right: int
    bottom: int
    word_count: int
    hebrew_letters: int


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    packet_rows = read_rows(args.packet)
    table_rows = [row for row in packet_rows if row.get("page_class") == "table_candidate_page"]
    crop_rows = build_crop_rows(table_rows, args)
    write_csv(args.out, FIELDNAMES, crop_rows)
    summary_rows = build_summary_rows(table_rows, crop_rows, args)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, crop_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, table_rows, crop_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_OCR_PACKET)
    parser.add_argument("--base-dir", type=Path, default=DEFAULT_BASE_DIR)
    parser.add_argument("--tessdata-dir", type=Path, default=DEFAULT_TESSDATA_DIR)
    parser.add_argument("--language", default="heb")
    parser.add_argument("--psm", default="4")
    parser.add_argument("--refresh-ocr", action="store_true")
    parser.add_argument("--line-padding-y", type=int, default=6)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_crop_rows(
    table_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    missing = missing_dependencies(args)
    rows: list[dict[str, str]] = []
    line_rank = 1
    for table_row in table_rows:
        page_rows = build_page_crop_rows(table_row, args, missing)
        for page_row in page_rows:
            page_row["line_rank"] = str(line_rank)
            rows.append(page_row)
            line_rank += 1
    return rows


def build_page_crop_rows(
    table_row: dict[str, str],
    args: argparse.Namespace,
    missing: list[str],
) -> list[dict[str, str]]:
    image_path = Path(table_row.get("page_image_path", ""))
    transcription_id = table_row.get("transcription_decision_id", "")
    tsv_path = args.base_dir / "tsv" / f"{safe_stem(transcription_id)}.tsv"
    crop_dir = args.base_dir / "crops" / safe_stem(transcription_id)
    if missing or not image_path.exists():
        return [
            empty_page_row(
                table_row,
                tsv_path,
                crop_dir / f"{safe_stem(transcription_id)}_line001.png",
                "missing OCR dependency: " + ", ".join(missing)
                if missing
                else "missing page image",
            )
        ]
    if args.refresh_ocr or not tsv_path.exists():
        run_tesseract_tsv(image_path, tsv_path, args)
    words = read_tsv_words(tsv_path)
    line_boxes = build_line_boxes(words)
    write_line_crops(image_path, crop_dir, transcription_id, line_boxes, args)
    rows: list[dict[str, str]] = []
    for page_line_rank, line_box in enumerate(line_boxes, start=1):
        crop_path = crop_dir / f"{safe_stem(transcription_id)}_line{page_line_rank:03d}.png"
        rows.append(
            line_row(
                table_row,
                tsv_path,
                crop_path,
                page_line_rank,
                line_box,
                image_path,
                args,
            )
        )
    return rows


def missing_dependencies(args: argparse.Namespace) -> list[str]:
    missing: list[str] = []
    if shutil.which("tesseract") is None:
        missing.append("tesseract")
    traineddata = args.tessdata_dir / f"{args.language}.traineddata"
    if not traineddata.exists():
        missing.append(str(traineddata))
    return missing


def run_tesseract_tsv(image_path: Path, tsv_path: Path, args: argparse.Namespace) -> None:
    tsv_path.parent.mkdir(parents=True, exist_ok=True)
    base = tsv_path.with_suffix("")
    subprocess.run(
        [
            "tesseract",
            "--tessdata-dir",
            str(args.tessdata_dir),
            "-l",
            args.language,
            "--psm",
            str(args.psm),
            "-c",
            "tessedit_create_tsv=1",
            str(image_path),
            str(base),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def read_tsv_words(path: Path) -> list[TsvWord]:
    words: list[TsvWord] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t", quoting=csv.QUOTE_NONE)
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
                        block_num=row.get("block_num", ""),
                        par_num=row.get("par_num", ""),
                        line_num=row.get("line_num", ""),
                    )
                )
            except ValueError:
                continue
    return words


def build_line_boxes(words: list[TsvWord]) -> list[LineBox]:
    grouped: dict[tuple[str, str, str], list[TsvWord]] = defaultdict(list)
    for word in words:
        grouped[(word.block_num, word.par_num, word.line_num)].append(word)
    boxes: list[LineBox] = []
    for line_words in grouped.values():
        hebrew_letters = sum(hebrew_letter_count(word.text) for word in line_words)
        if hebrew_letters <= 0:
            continue
        left = min(word.left for word in line_words)
        top = min(word.top for word in line_words)
        right = max(word.right for word in line_words)
        bottom = max(word.bottom for word in line_words)
        boxes.append(
            LineBox(
                left=left,
                top=top,
                right=right,
                bottom=bottom,
                word_count=len(line_words),
                hebrew_letters=hebrew_letters,
            )
        )
    boxes.sort(key=lambda box: (box.top, box.left))
    return boxes


def write_line_crops(
    image_path: Path,
    crop_dir: Path,
    transcription_id: str,
    line_boxes: list[LineBox],
    args: argparse.Namespace,
) -> None:
    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover - local dependency guard
        raise RuntimeError("Pillow is required to write line crops") from exc
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    crop_dir.mkdir(parents=True, exist_ok=True)
    for page_line_rank, box in enumerate(line_boxes, start=1):
        crop_path = crop_dir / f"{safe_stem(transcription_id)}_line{page_line_rank:03d}.png"
        top = max(0, box.top - args.line_padding_y)
        bottom = min(height, max(top + 1, box.bottom + args.line_padding_y))
        image.crop((0, top, width, bottom)).save(crop_path)


def line_row(
    table_row: dict[str, str],
    tsv_path: Path,
    crop_path: Path,
    page_line_rank: int,
    box: LineBox,
    image_path: Path,
    args: argparse.Namespace,
) -> dict[str, str]:
    width, height = image_dimensions(image_path)
    crop_top = max(0, box.top - args.line_padding_y)
    crop_bottom = min(height, max(crop_top + 1, box.bottom + args.line_padding_y))
    return {
        "line_rank": "0",
        "transcription_decision_id": table_row.get("transcription_decision_id", ""),
        "label": table_row.get("label", ""),
        "page_number": table_row.get("page_number", ""),
        "page_class": table_row.get("page_class", ""),
        "page_line_rank": str(page_line_rank),
        "page_image_path": str(image_path),
        "tsv_path": str(tsv_path),
        "tsv_exists": str(tsv_path.exists()).lower(),
        "line_left": str(box.left),
        "line_top": str(box.top),
        "line_right": str(box.right),
        "line_bottom": str(box.bottom),
        "line_width": str(max(0, box.right - box.left)),
        "line_height": str(max(0, box.bottom - box.top)),
        "crop_left": "0",
        "crop_top": str(crop_top),
        "crop_right": str(width),
        "crop_bottom": str(crop_bottom),
        "crop_width": str(width),
        "crop_height": str(max(0, crop_bottom - crop_top)),
        "crop_path": str(crop_path),
        "crop_exists": str(crop_path.exists()).lower(),
        "ocr_word_count": str(box.word_count),
        "ocr_hebrew_letters": str(box.hebrew_letters),
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "no_input_boundary": NO_INPUT_BOUNDARY,
        "next_manual_action": "compare local line crop to page image and OCR HTML; do not import source rows",
    }


def empty_page_row(
    table_row: dict[str, str],
    tsv_path: Path,
    crop_path: Path,
    action: str,
) -> dict[str, str]:
    return {
        "line_rank": "0",
        "transcription_decision_id": table_row.get("transcription_decision_id", ""),
        "label": table_row.get("label", ""),
        "page_number": table_row.get("page_number", ""),
        "page_class": table_row.get("page_class", ""),
        "page_line_rank": "0",
        "page_image_path": table_row.get("page_image_path", ""),
        "tsv_path": str(tsv_path),
        "tsv_exists": str(tsv_path.exists()).lower(),
        "line_left": "0",
        "line_top": "0",
        "line_right": "0",
        "line_bottom": "0",
        "line_width": "0",
        "line_height": "0",
        "crop_left": "0",
        "crop_top": "0",
        "crop_right": "0",
        "crop_bottom": "0",
        "crop_width": "0",
        "crop_height": "0",
        "crop_path": str(crop_path),
        "crop_exists": "false",
        "ocr_word_count": "0",
        "ocr_hebrew_letters": "0",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "no_input_boundary": NO_INPUT_BOUNDARY,
        "next_manual_action": action,
    }


def build_summary_rows(
    table_rows: list[dict[str, str]],
    crop_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    return [
        metric("table_candidate_pages", len(table_rows)),
        metric("line_crop_rows", len(crop_rows)),
        metric("line_crops_available", count_value(crop_rows, "crop_exists", "true")),
        metric("tsv_sidecars", len({row["tsv_path"] for row in crop_rows if row["tsv_exists"] == "true"})),
        metric("ocr_words", sum_int(crop_rows, "ocr_word_count")),
        metric("ocr_hebrew_letters", sum_int(crop_rows, "ocr_hebrew_letters")),
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


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    page_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        page_counts[row["transcription_decision_id"]] += 1
    lines = [
        "# Cities Source Page Line Crop Packet",
        "",
        "Status: local line-crop review packet for Cities table candidate pages.",
        "Tracked files contain no OCR body text or source-script body text.",
        "This does not verify a transcription, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_packet "
            f"--packet {args.packet} "
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
        f"- Table candidate pages: {summary['table_candidate_pages']}.",
        f"- Line crop rows: {summary['line_crop_rows']}.",
        f"- Line crops available: {summary['line_crops_available']}.",
        f"- TSV sidecars: {summary['tsv_sidecars']}.",
        f"- OCR words represented by line boxes: {summary['ocr_words']}.",
        f"- OCR Hebrew letters represented by line boxes: {summary['ocr_hebrew_letters']}.",
        f"- Language: `{summary['language']}`.",
        f"- PSM: `{summary['psm']}`.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- City-name normalization: {summary['city_name_normalization']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- p-levels: {summary['p_levels']}.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Page Counts",
        "",
        "| Transcription id | Line crops |",
        "| --- | ---: |",
    ]
    for transcription_id in sorted(page_counts):
        lines.append(
            f"| `{markdown_cell(transcription_id)}` | {page_counts[transcription_id]} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Line crops are local review aids, not verified row transcriptions.",
            "- TSV sidecars may contain OCR text locally; tracked files do not.",
            "- Future source-row import still requires readable transcription, row/column alignment evidence, and an explicit import decision record.",
            "- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    table_rows: list[dict[str, str]],
    crop_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "packet": str(args.packet),
            "tessdata_dir": str(args.tessdata_dir),
            "language": args.language,
            "psm": str(args.psm),
        },
        "outputs": {
            "base_dir": str(args.base_dir),
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "table_pages": len(table_rows),
        "rows": len(crop_rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "no_input_boundary": NO_INPUT_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def image_dimensions(path: Path) -> tuple[int, int]:
    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover - local dependency guard
        raise RuntimeError("Pillow is required to inspect line crop images") from exc
    with Image.open(path) as image:
        return image.size


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def safe_stem(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._") or "line"


def hebrew_letter_count(text: str) -> int:
    return sum(1 for char in text if HEBREW_RE.fullmatch(char))


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
