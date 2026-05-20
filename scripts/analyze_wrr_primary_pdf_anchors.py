#!/usr/bin/env python3
"""Audit key WRR 1994 primary-PDF method anchors."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from pypdf import PdfReader

from els import __version__


DEFAULT_SOURCE = Path("reports/wrr_1994/wrr_1994_paper.pdf")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_primary_pdf_anchors.csv")
DEFAULT_MD = Path("reports/wrr_1994/wrr_primary_pdf_anchors.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_primary_pdf_anchors.manifest.json")

FIELDNAMES = [
    "anchor_id",
    "method_area",
    "status",
    "page",
    "search_text",
    "current_read",
]


@dataclass(frozen=True)
class Anchor:
    anchor_id: str
    method_area: str
    search_text: str
    current_read: str


ANCHORS = (
    Anchor(
        "sample_298_word_pairs",
        "pair_universe",
        "298 word pairs",
        "Primary paper reports 298 second-list word pairs after the length 5..8 screen.",
    ),
    Anchor(
        "koren_text",
        "genesis_text",
        "Koren text is precisely",
        "Primary paper identifies the Koren Genesis text as the text used by WRR.",
    ),
    Anchor(
        "permutation_count",
        "permutation",
        "999,999 random permutations",
        "Primary paper reports 999,999 random permutations of the 32 personalities.",
    ),
    Anchor(
        "expected_els_target",
        "skip_cap",
        "expected number of ELS's",
        "Primary paper describes D(w) as a term-specific bound targeting expected ELS count 10.",
    ),
    Anchor(
        "corrected_distance",
        "corrected_distance",
        "corrected distance",
        "Primary paper includes corrected-distance method text, but later sources clarify implementation details.",
    ),
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    pages = extract_pages(args.source)
    rows = build_anchor_rows(pages, ANCHORS)
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def extract_pages(path: Path) -> list[str]:
    reader = PdfReader(str(path))
    return [page.extract_text() or "" for page in reader.pages]


def build_anchor_rows(pages: list[str], anchors: tuple[Anchor, ...]) -> list[dict[str, str]]:
    rows = []
    for anchor in anchors:
        page_number = find_page(pages, anchor.search_text)
        rows.append(
            {
                "anchor_id": anchor.anchor_id,
                "method_area": anchor.method_area,
                "status": "found" if page_number is not None else "missing",
                "page": str(page_number or ""),
                "search_text": anchor.search_text,
                "current_read": anchor.current_read,
            }
        )
    return rows


def find_page(pages: list[str], search_text: str) -> int | None:
    normalized_search = normalize_space(search_text).casefold()
    for index, page in enumerate(pages, start=1):
        if normalized_search in normalize_space(page).casefold():
            return index
    return None


def normalize_space(value: str) -> str:
    return " ".join(value.split())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    lines = [
        "# WRR Primary PDF Anchors",
        "",
        "Status: source-anchor audit from the local WRR 1994 PDF; not term-table extraction.",
        "",
        "This checks whether key method/count statements are reachable in extracted",
        "PDF text. It deliberately avoids treating the garbled Hebrew table text as",
        "machine-ready term data.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_primary_pdf_anchors "
            f"--source {args.source} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Anchors",
        "",
        "| Anchor | Area | Status | Page | Current read |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_cell(row['anchor_id'])}`",
                    markdown_cell(row["method_area"]),
                    f"`{markdown_cell(row['status'])}`",
                    markdown_cell(row["page"]),
                    markdown_cell(row["current_read"]),
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def write_manifest(args: argparse.Namespace, rows: list[dict[str, str]], started: float) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "source": str(args.source),
        "source_sha256": sha256_file(args.source),
        "rows": len(rows),
        "missing": sum(1 for row in rows if row["status"] != "found"),
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
