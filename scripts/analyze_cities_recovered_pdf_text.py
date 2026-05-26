#!/usr/bin/env python3
"""Audit extractable text from recovered Cities PDF sources without ELS work."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_wrr_wayback_source_recovery_probe import markdown_cell, markdown_link


DEFAULT_RECOVERY_CSV = Path("reports/cities_pdf_recovery_probe/cities_pdf_recovery_probe.csv")
DEFAULT_OUT_DIR = Path("reports/cities_pdf_recovery_probe")
DEFAULT_OUT = DEFAULT_OUT_DIR / "cities_recovered_pdf_text_audit.csv"
DEFAULT_SUMMARY_OUT = DEFAULT_OUT_DIR / "cities_recovered_pdf_text_audit_summary.csv"
DEFAULT_ANCHORS_OUT = DEFAULT_OUT_DIR / "cities_recovered_pdf_text_anchors.csv"
DEFAULT_MD = Path("docs/CITIES_RECOVERED_PDF_TEXT_AUDIT.md")
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "cities_recovered_pdf_text_audit.manifest.json"

ROW_FIELDNAMES = [
    "label",
    "source_pages",
    "url",
    "selected_source",
    "selected_path",
    "sha256",
    "bytes",
    "pdf_pages",
    "text_chars",
    "normalized_text_chars",
    "latin_letter_ratio",
    "text_status",
    "family",
    "title_guess",
]

SUMMARY_FIELDNAMES = [
    "recovered_pdf_rows",
    "extractable_text_rows",
    "zero_text_rows",
    "garbled_or_nonlatin_rows",
    "gans_family_rows",
    "aumann_family_rows",
    "other_family_rows",
    "anchor_rows",
    "anchors_found",
    "claim_status",
]

ANCHOR_FIELDNAMES = ["anchor", "label", "status", "diagnostic"]

ANCHORS = (
    (
        "gans_communities_data_title",
        "cities_pdf_communities_data",
        "The Linguistic Protocol and Data used for the Communities Experiment",
        "Gans/Inbal/Bombach communities data title found",
    ),
    (
        "gans_paper_title",
        "cities_pdf_gans",
        "Patterns of Equidistant Letter Sequence Pairs in Genesis",
        "Gans/Inbal/Bombach paper title found",
    ),
    (
        "aumann_personal_perspective",
        "cities_pdf_dp_365_1",
        "A PERSONAL PERSPECTIVE ON THE WORK OF THE",
        "Aumann personal-perspective title found",
    ),
    (
        "furstenberg_personal_perspective",
        "cities_pdf_dp_365_2",
        "ANOTHER PERSONAL PERSPECTIVE ON THE WORK OF THE",
        "Furstenberg personal-perspective title found",
    ),
    (
        "witztum_critique_title",
        "cities_pdf_dp_365_4",
        "A CRITIQUE OF THE REPORT SUBMITTED BY THE COMMITTEE",
        "Witztum critique title found",
    ),
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = analyze_recovered_pdfs(args.recovery_csv)
    anchors = protocol_anchors(rows)
    summary = build_summary(rows, anchors)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, rows, anchors)
    write_manifest(args.manifest_out, args, summary, len(rows), started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recovery-csv", type=Path, default=DEFAULT_RECOVERY_CSV)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def analyze_recovered_pdfs(recovery_csv: Path) -> list[dict[str, object]]:
    with recovery_csv.open(encoding="utf-8", newline="") as handle:
        recovered = [
            row
            for row in csv.DictReader(handle)
            if row.get("usable_status") != "no_pdf_recovered"
        ]
    return [analyze_row(row) for row in recovered]


def analyze_row(recovery_row: dict[str, str]) -> dict[str, object]:
    path = Path(recovery_row["selected_path"])
    text = extract_pdf_text(path)
    normalized = normalize_space(text)
    ratio = latin_letter_ratio(normalized)
    return {
        "label": recovery_row["label"],
        "source_pages": recovery_row["source_pages"],
        "url": recovery_row["url"],
        "selected_source": recovery_row["selected_source"],
        "selected_path": str(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "pdf_pages": recovery_row["pdf_pages"] or pdfinfo_pages(path),
        "text_chars": len(text.strip()),
        "normalized_text_chars": len(normalized),
        "latin_letter_ratio": f"{ratio:.3f}",
        "text_status": text_status(normalized, ratio),
        "family": classify_family(recovery_row["label"]),
        "title_guess": title_guess(normalized),
    }


def extract_pdf_text(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise SystemExit("pdftotext is required; install poppler") from error
    if completed.returncode != 0:
        return ""
    return completed.stdout


def pdfinfo_pages(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdfinfo", str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return ""
    if completed.returncode != 0:
        return ""
    for line in completed.stdout.splitlines():
        if line.startswith("Pages:"):
            return line.split(":", 1)[1].strip()
    return ""


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def latin_letter_ratio(text: str) -> float:
    letters = [char for char in text if char.isalpha()]
    if not letters:
        return 0.0
    latin = [char for char in letters if "A" <= char.upper() <= "Z"]
    return len(latin) / len(letters)


def text_status(normalized: str, ratio: float) -> str:
    if not normalized:
        return "zero_extractable_text"
    if alpha_char_ratio(normalized) < 0.25:
        return "extractable_but_garbled_or_nonlatin"
    if ratio < 0.25:
        return "extractable_but_garbled_or_nonlatin"
    return "extractable_text"


def alpha_char_ratio(text: str) -> float:
    if not text:
        return 0.0
    return sum(1 for char in text if char.isalpha()) / len(text)


def classify_family(label: str) -> str:
    if label in {"cities_pdf_gans", "cities_pdf_communities_data"}:
        return "gans_communities"
    if label.startswith("cities_pdf_dp"):
        return "aumann_committee"
    return "other"


def title_guess(normalized: str) -> str:
    if not normalized:
        return ""
    return normalized[:120]


def protocol_anchors(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    text_by_label = {str(row["label"]): str(row["title_guess"]) for row in rows}
    full_text_by_label: dict[str, str] = {}
    for row in rows:
        path = Path(str(row["selected_path"]))
        full_text_by_label[str(row["label"])] = normalize_space(extract_pdf_text(path))
    anchors: list[dict[str, str]] = []
    for anchor, label, phrase, diagnostic in ANCHORS:
        haystack = full_text_by_label.get(label) or text_by_label.get(label, "")
        found = normalize_space(phrase).lower() in haystack.lower()
        anchors.append(
            {
                "anchor": anchor,
                "label": label,
                "status": "found" if found else "missing",
                "diagnostic": diagnostic if found else "anchor text not found",
            }
        )
    return anchors


def build_summary(
    rows: list[dict[str, object]],
    anchors: list[dict[str, str]],
) -> dict[str, object]:
    status_counts = Counter(str(row["text_status"]) for row in rows)
    family_counts = Counter(str(row["family"]) for row in rows)
    return {
        "recovered_pdf_rows": len(rows),
        "extractable_text_rows": status_counts.get("extractable_text", 0),
        "zero_text_rows": status_counts.get("zero_extractable_text", 0),
        "garbled_or_nonlatin_rows": status_counts.get(
            "extractable_but_garbled_or_nonlatin", 0
        ),
        "gans_family_rows": family_counts.get("gans_communities", 0),
        "aumann_family_rows": family_counts.get("aumann_committee", 0),
        "other_family_rows": family_counts.get("other", 0),
        "anchor_rows": len(anchors),
        "anchors_found": sum(1 for row in anchors if row["status"] == "found"),
        "claim_status": "source_shape_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    summary: dict[str, object],
    rows: list[dict[str, object]],
    anchors: list[dict[str, str]],
) -> None:
    anchor_counts = Counter(anchor["status"] for anchor in anchors)
    lines = [
        "# Cities Recovered PDF Text Audit",
        "",
        "Status: source-shape audit only. This reads text from PDFs recovered by",
        "`docs/CITIES_PDF_RECOVERY_PROBE.md`; it does not run OCR, normalize city",
        "names, run ELS searches, compute compactness, or verify p-levels.",
        "",
        "## Summary",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| recovered PDF rows audited | {summary['recovered_pdf_rows']} |",
        f"| extractable text rows | {summary['extractable_text_rows']} |",
        f"| zero-text rows | {summary['zero_text_rows']} |",
        f"| garbled/non-Latin extract rows | {summary['garbled_or_nonlatin_rows']} |",
        f"| Gans/community family rows | {summary['gans_family_rows']} |",
        f"| Aumann committee family rows | {summary['aumann_family_rows']} |",
        f"| other family rows | {summary['other_family_rows']} |",
        "",
        "## Protocol Anchors",
        "",
        f"Found anchors: {anchor_counts.get('found', 0)} of {len(anchors)}.",
        "",
        "| Anchor | Label | Status | Diagnostic |",
        "| --- | --- | --- | --- |",
    ]
    for anchor in anchors:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(anchor["anchor"]),
                    markdown_cell(anchor["label"]),
                    markdown_cell(anchor["status"]),
                    markdown_cell(anchor["diagnostic"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Label | Family | Text status | Pages | Text chars | SHA-256 | Source URL |",
            "| --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["label"]),
                    markdown_cell(row["family"]),
                    markdown_cell(row["text_status"]),
                    markdown_cell(row["pdf_pages"]),
                    markdown_cell(row["normalized_text_chars"]),
                    f"`{str(row['sha256'])[:16]}`",
                    markdown_link("url", str(row["url"])),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "Rows with extractable text are now separated from image-only or garbled",
            "PDFs for future source-review planning. This audit does not decide which",
            "texts are admissible for a result-bearing protocol. Any later protocol",
            "must separately lock source rows, normalization, filters, Genesis text,",
            "skip caps, compactness metric, and controls before ELS work.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, object],
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "input_recovery_csv": str(args.recovery_csv),
        "rows": rows,
        "summary": summary,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "source-shape audit only; no ELS result",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
