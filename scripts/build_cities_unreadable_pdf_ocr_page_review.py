#!/usr/bin/env python3
"""Build manual page-image review records for priority Cities OCR pages."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_PACKET = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_packet.csv"
)
DEFAULT_DECISIONS = Path("data/study/mappings/cities_ocr_page_review_decisions.csv")
DEFAULT_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review.manifest.json"
)

CLAIM_BOUNDARY = (
    "manual page-image review only; no OCR body text in tracked files, no "
    "repaired text, no source-row import, no city normalization, no ELS, no "
    "compactness, no p-level"
)

FIELDNAMES = [
    "review_rank",
    "decision_id",
    "label",
    "page_number",
    "family",
    "lane",
    "packet_ocr_status",
    "packet_ocr_text_signal_chars",
    "page_image_path",
    "visual_review_status",
    "visual_page_role",
    "visual_text_signal",
    "ocr_read_status",
    "source_row_use",
    "decision",
    "reviewed_by",
    "reviewed_at",
    "notes",
    "claim_boundary",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    packet_rows = read_csv(args.packet)
    decision_rows = read_csv(args.decisions)
    review_rows = build_page_review_rows(packet_rows, decision_rows)
    summary_rows = build_summary_rows(review_rows, packet_rows)
    write_csv(args.out, FIELDNAMES, review_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, review_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, review_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--decisions", type=Path, default=DEFAULT_DECISIONS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_page_review_rows(
    packet_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    packet_by_page = {
        (row.get("label", ""), row.get("page_number", "")): row for row in packet_rows
    }
    seen_decisions: set[str] = set()
    rows: list[dict[str, str]] = []
    for decision in sorted(decision_rows, key=decision_sort_key):
        decision_id = decision.get("decision_id", "").strip()
        if not decision_id:
            raise ValueError("decision row missing decision_id")
        if decision_id in seen_decisions:
            raise ValueError(f"duplicate decision_id: {decision_id}")
        seen_decisions.add(decision_id)
        key = (decision.get("label", ""), decision.get("page_number", ""))
        packet = packet_by_page.get(key)
        if packet is None:
            raise ValueError(
                f"decision {decision_id} points to missing packet page: {key[0]} p{key[1]}"
            )
        rows.append(
            {
                "review_rank": "0",
                "decision_id": decision_id,
                "label": key[0],
                "page_number": key[1],
                "family": packet.get("family", ""),
                "lane": packet.get("lane", ""),
                "packet_ocr_status": packet.get("ocr_status", ""),
                "packet_ocr_text_signal_chars": packet.get("ocr_text_signal_chars", ""),
                "page_image_path": packet.get("image_path", ""),
                "visual_review_status": decision.get("visual_review_status", ""),
                "visual_page_role": decision.get("visual_page_role", ""),
                "visual_text_signal": decision.get("visual_text_signal", ""),
                "ocr_read_status": decision.get("ocr_read_status", ""),
                "source_row_use": decision.get("source_row_use", ""),
                "decision": decision.get("decision", ""),
                "reviewed_by": decision.get("reviewed_by", ""),
                "reviewed_at": decision.get("reviewed_at", ""),
                "notes": decision.get("notes", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for index, row in enumerate(rows, start=1):
        row["review_rank"] = str(index)
    return rows


def decision_sort_key(row: dict[str, str]) -> tuple[str, int, str]:
    return (
        row.get("label", ""),
        int_or_zero(row.get("page_number", "")),
        row.get("decision_id", ""),
    )


def build_summary_rows(
    rows: list[dict[str, str]],
    packet_rows: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    source_imports = [
        row for row in rows if row.get("source_row_use") != "no_source_row_use"
    ]
    packet_page_count = len(packet_rows) if packet_rows is not None else len(rows)
    unreviewed_packet_pages = max(packet_page_count - len(rows), 0)
    return [
        metric("packet_pages", packet_page_count),
        metric("reviewed_packet_pages", len(rows)),
        metric("unreviewed_packet_pages", unreviewed_packet_pages),
        metric("review_rows", len(rows)),
        metric("reviewed_pages", count_eq(rows, "visual_review_status", "reviewed")),
        metric("ocr_empty_pages_reviewed", count_ocr_empty(rows)),
        metric("low_signal_pages_reviewed", count_low_signal(rows)),
        metric("visual_text_present_pages", count_eq(rows, "visual_text_signal", "text_present")),
        metric("source_row_imports", len(source_imports)),
        metric("els_runs", 0),
        metric("compactness_runs", 0),
        metric("claim_boundary", CLAIM_BOUNDARY),
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Unreadable PDF OCR Page Review",
        "",
        "Status: manual page-image review record. This records reviewer labels for reviewed Cities OCR packet pages.",
        "It does not track OCR body text, repair text, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "No OCR body text appears in this doc, CSV, summary, or manifest.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_unreadable_pdf_ocr_page_review "
            f"--packet {args.packet} "
            f"--decisions {args.decisions} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        f"- Packet pages: {summary['packet_pages']}.",
        f"- Reviewed packet pages: {summary['reviewed_packet_pages']}.",
        f"- Unreviewed packet pages: {summary['unreviewed_packet_pages']}.",
        f"- Review rows: {summary['review_rows']}.",
        f"- Reviewed pages: {summary['reviewed_pages']}.",
        f"- OCR-empty pages reviewed: {summary['ocr_empty_pages_reviewed']}.",
        f"- Low-signal pages reviewed: {summary['low_signal_pages_reviewed']}.",
        f"- Visual-text-present pages: {summary['visual_text_present_pages']}.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- Boundary: {CLAIM_BOUNDARY}",
        "",
        "## Page Decisions",
        "",
        "| Rank | Label | Page | OCR status | Signal chars | Visual role | OCR read status | Source-row use | Decision | Notes |",
        "| ---: | --- | ---: | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["review_rank"]),
                    markdown_cell(row["label"]),
                    markdown_cell(row["page_number"]),
                    f"`{markdown_cell(row['packet_ocr_status'])}`",
                    markdown_cell(row["packet_ocr_text_signal_chars"]),
                    f"`{markdown_cell(row['visual_page_role'])}`",
                    f"`{markdown_cell(row['ocr_read_status'])}`",
                    f"`{markdown_cell(row['source_row_use'])}`",
                    f"`{markdown_cell(row['decision'])}`",
                    markdown_cell(row["notes"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- These rows are page-image review records only.",
            "- OCR sidecars remain ignored local files and are not tracked source text.",
            "- Source-row decisions require separate citable decision records.",
            "- No reviewed page here changes source admissibility or creates city-name rows.",
            "- Contact sheets and page images remain visual aids, not public source-text artifacts.",
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
        "inputs": {"packet": str(args.packet), "decisions": str(args.decisions)},
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


def count_eq(rows: list[dict[str, str]], field: str, value: str) -> int:
    return sum(1 for row in rows if row.get(field) == value)


def count_ocr_empty(rows: list[dict[str, str]]) -> int:
    return sum(
        1
        for row in rows
        if row.get("packet_ocr_status") != "page_ocr_text_detected"
    )


def count_low_signal(rows: list[dict[str, str]]) -> int:
    return sum(
        1
        for row in rows
        if int_or_zero(row.get("packet_ocr_text_signal_chars", "")) < 100
    )


def metric(name: str, value: object) -> dict[str, str]:
    return {"metric": name, "value": str(value)}


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


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
