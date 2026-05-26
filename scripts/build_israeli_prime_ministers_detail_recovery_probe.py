#!/usr/bin/env python3
"""Probe missing Israeli prime-minister detail pages without running ELS results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_wrr_source_recovery_probe import (
    HtmlMetadataParser,
    markdown_cell,
    normalize_space,
)
from scripts.download_wrr_sources import FetchResult, fetch_url


ROOT_URL = "https://www.torah-code.org"
SPAM_MARKERS = ("slot bet", "deposit pulsa", "rtp slot")
DEFAULT_OUT_DIR = Path("reports/israeli_prime_ministers_detail_recovery_probe")
DEFAULT_OUT = DEFAULT_OUT_DIR / "detail_recovery_probe.csv"
DEFAULT_SUMMARY_OUT = DEFAULT_OUT_DIR / "detail_recovery_probe_summary.csv"
DEFAULT_MD = Path("docs/ISRAELI_PRIME_MINISTERS_DETAIL_RECOVERY_PROBE.md")
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "detail_recovery_probe.manifest.json"

EXPECTED_PAGES = (
    (9, "Benjamin Netanyahu"),
    (10, "Ehud Barak"),
    (11, "Ariel Sharon"),
    (12, "Ehud Olmert"),
)

ROW_FIELDNAMES = [
    "page_index",
    "expected_title",
    "requested_url",
    "final_url",
    "redirected",
    "http_status",
    "path",
    "bytes",
    "sha256",
    "title",
    "canonical",
    "expected_title_present",
    "canonical_is_root",
    "final_url_is_root",
    "spam_marker_present",
    "usable_status",
]

SUMMARY_FIELDNAMES = [
    "pages_probed",
    "expected_title_present_rows",
    "redirected_rows",
    "root_final_url_rows",
    "root_canonical_rows",
    "spam_marker_rows",
    "usable_detail_pages",
    "unrecovered_detail_pages",
    "recovery_status",
]


@dataclass(frozen=True)
class DetailPage:
    page_index: int
    expected_title: str

    @property
    def url(self) -> str:
        return (
            "https://www.torah-code.org/experiments/"
            f"israeli_prime_ministers_{self.page_index}.html"
        )

    @property
    def filename(self) -> str:
        return f"israeli_prime_ministers_{self.page_index}.html"


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    pages = [DetailPage(index, title) for index, title in EXPECTED_PAGES]
    rows = fetch_and_analyze_pages(pages, args.out_dir)
    summary = build_summary(rows)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, rows)
    write_manifest(args.manifest_out, args, summary, len(rows), started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def fetch_and_analyze_pages(
    pages: list[DetailPage], out_dir: Path
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    out_dir.mkdir(parents=True, exist_ok=True)
    for page in pages:
        result = fetch_url(page.url)
        path = out_dir / page.filename
        path.write_bytes(result.data)
        rows.append(analyze_snapshot(page, result, path))
    return rows


def analyze_snapshot(
    page: DetailPage, result: FetchResult, path: Path
) -> dict[str, object]:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    parser = HtmlMetadataParser()
    parser.feed(text)
    title = html.unescape(parser.title)
    canonical = parser.canonical
    lower_text = text.lower()
    expected_present = page.expected_title.lower() in lower_text
    canonical_is_root = canonical.rstrip("/") == ROOT_URL
    final_url_is_root = result.final_url.rstrip("/") == ROOT_URL
    spam_marker_present = any(marker in lower_text for marker in SPAM_MARKERS)
    usable = (
        expected_present
        and not canonical_is_root
        and not final_url_is_root
        and not spam_marker_present
    )
    return {
        "page_index": page.page_index,
        "expected_title": page.expected_title,
        "requested_url": page.url,
        "final_url": result.final_url,
        "redirected": result.final_url != page.url,
        "http_status": result.http_status,
        "path": str(path),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "title": normalize_space(title),
        "canonical": canonical,
        "expected_title_present": expected_present,
        "canonical_is_root": canonical_is_root,
        "final_url_is_root": final_url_is_root,
        "spam_marker_present": spam_marker_present,
        "usable_status": "usable_detail_page" if usable else "unrecovered_detail_page",
    }


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    status_counts = Counter(str(row["usable_status"]) for row in rows)
    usable = status_counts.get("usable_detail_page", 0)
    unrecovered = status_counts.get("unrecovered_detail_page", 0)
    return {
        "pages_probed": len(rows),
        "expected_title_present_rows": sum(
            1 for row in rows if row["expected_title_present"]
        ),
        "redirected_rows": sum(1 for row in rows if row["redirected"]),
        "root_final_url_rows": sum(1 for row in rows if row["final_url_is_root"]),
        "root_canonical_rows": sum(1 for row in rows if row["canonical_is_root"]),
        "spam_marker_rows": sum(1 for row in rows if row["spam_marker_present"]),
        "usable_detail_pages": usable,
        "unrecovered_detail_pages": unrecovered,
        "recovery_status": (
            "some_detail_pages_recovered" if usable else "no_detail_pages_recovered"
        ),
    }


def write_markdown(
    path: Path, summary: dict[str, object], rows: list[dict[str, object]]
) -> None:
    lines = [
        "# Israeli Prime Ministers Detail Recovery Probe",
        "",
        "Status: live-source recovery probe only. This does not run ELS searches,",
        "does not modify the cached WRR source bundle, and does not infer missing",
        "detail-page data.",
        "",
        "## Summary",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| missing detail pages probed | {summary['pages_probed']} |",
        f"| rows where expected title appeared | {summary['expected_title_present_rows']} |",
        f"| redirected rows | {summary['redirected_rows']} |",
        f"| final URL is Torah-code root | {summary['root_final_url_rows']} |",
        f"| canonical URL is Torah-code root | {summary['root_canonical_rows']} |",
        f"| unrelated slot/gambling markers | {summary['spam_marker_rows']} |",
        f"| usable detail pages | {summary['usable_detail_pages']} |",
        "",
        f"Current recovery status: `{summary['recovery_status']}`.",
        "",
        "## Probe Rows",
        "",
        "| Page | Expected title | HTTP | Redirected | Final Root | Expected Text | Spam Marker | Bytes | SHA-256 | Status |",
        "| ---: | --- | ---: | --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["page_index"]),
                    markdown_cell(row["expected_title"]),
                    markdown_cell(row["http_status"]),
                    markdown_cell(row["redirected"]),
                    markdown_cell(row["final_url_is_root"]),
                    markdown_cell(row["expected_title_present"]),
                    markdown_cell(row["spam_marker_present"]),
                    markdown_cell(row["bytes"]),
                    f"`{str(row['sha256'])[:16]}`",
                    markdown_cell(row["usable_status"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Source Boundary",
            "",
            "This probe checks current live URLs for the four missing detail pages:",
            "`israeli_prime_ministers_9.html` through `_12.html`. A row is treated",
            "as usable only when the download contains the expected prime-minister",
            "title, does not end at the Torah-code root URL, does not declare the",
            "site root as canonical, and lacks unrelated spam markers.",
            "",
            "If these pages remain unrecovered, the Israeli prime-ministers lane stays",
            "source-shape only. Do not run a result-bearing protocol from inferred",
            "detail pages.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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
        "rows": rows,
        "summary": summary,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "live source recovery only; no ELS result",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
