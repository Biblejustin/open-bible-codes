#!/usr/bin/env python3
"""Audit the Wikisource KJVA/apocrypha source candidate without importing text."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from els import __version__


WIKISOURCE_URL = (
    "https://en.wikisource.org/wiki/"
    "The_Holy_Bible,_containing_the_Old_%26_New_Testament_%26_the_Apocrypha"
)
DEFAULT_OUT_DIR = Path("reports/kjva_wikisource_candidate_source")
DEFAULT_ROWS = DEFAULT_OUT_DIR / "source_status.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_ANCHORS = DEFAULT_OUT_DIR / "anchors.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_WIKISOURCE_CANDIDATE_SOURCE_AUDIT.md")
USER_AGENT = "OpenBibleCodes-EDLS source-status audit/1.0"

ROW_FIELDNAMES = [
    "source_id",
    "url",
    "final_url",
    "fetch_status",
    "error",
    "bytes",
    "sha256",
    "title",
    "apocrypha_marker_present",
    "kjv_marker_present",
    "standard_1769_marker_present",
    "ballantyne_marker_present",
    "public_domain_marker_present",
    "source_audit_status",
    "verse_numbered_import_ready",
    "result_ready_status",
]
SUMMARY_FIELDNAMES = [
    "source_pages",
    "fetched_pages",
    "source_candidate_pages",
    "verse_import_ready_pages",
    "result_ready_pages",
    "apocrypha_marker_pages",
    "public_domain_marker_pages",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class SourceCandidate:
    source_id: str
    url: str


@dataclass(frozen=True)
class FetchedPage:
    raw: bytes
    final_url: str
    fetch_status: str
    error: str = ""


DEFAULT_CANDIDATES = (
    SourceCandidate("wikisource_ballantyne_1911_kjva", WIKISOURCE_URL),
)


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if not stripped:
            return
        if self.in_title:
            self.title_parts.append(stripped)
        self.parts.append(stripped)

    @property
    def text(self) -> str:
        return normalize_space(" ".join(self.parts))

    @property
    def title(self) -> str:
        return normalize_space(" ".join(self.title_parts))


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    candidates = (SourceCandidate("wikisource_ballantyne_1911_kjva", args.url),)
    rows = [
        analyze_candidate(candidate, fetch_source(candidate.url, timeout=args.timeout))
        for candidate in candidates
    ]
    summary = build_summary(rows)
    anchors = build_anchors(rows, summary)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, rows, anchors)
    write_manifest(args.manifest_out, args, rows, summary, anchors, started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=WIKISOURCE_URL)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--out", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    return parser


def fetch_source(url: str, *, timeout: float) -> FetchedPage:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            return FetchedPage(
                raw=response.read(),
                final_url=response.geturl(),
                fetch_status="fetched",
            )
    except HTTPError as exc:
        return FetchedPage(
            raw=b"",
            final_url=url,
            fetch_status=f"http_error_{exc.code}",
            error=str(exc),
        )
    except (OSError, URLError) as exc:
        return FetchedPage(
            raw=b"",
            final_url=url,
            fetch_status="fetch_error",
            error=str(exc),
        )


def analyze_candidate(
    candidate: SourceCandidate,
    page: FetchedPage,
) -> dict[str, object]:
    text = page.raw.decode("utf-8", errors="replace")
    extractor = TextExtractor()
    if text:
        extractor.feed(text)
    normalized = extractor.text
    lower_text = normalized.lower()
    marker_checks = {
        "apocrypha_marker_present": "apocrypha" in lower_text,
        "kjv_marker_present": "king james" in lower_text,
        "standard_1769_marker_present": "standard version of 1769" in lower_text
        or "1769" in lower_text,
        "ballantyne_marker_present": "ballantyne" in lower_text,
        "public_domain_marker_present": "public domain" in lower_text,
    }
    fetched = page.fetch_status == "fetched"
    source_candidate = fetched and all(marker_checks.values())
    return {
        "source_id": candidate.source_id,
        "url": candidate.url,
        "final_url": page.final_url,
        "fetch_status": page.fetch_status,
        "error": page.error,
        "bytes": len(page.raw),
        "sha256": sha256_bytes(page.raw) if page.raw else "",
        "title": html.unescape(extractor.title),
        **marker_checks,
        "source_audit_status": (
            "source_candidate_needs_import" if source_candidate else "source_candidate_not_confirmed"
        ),
        "verse_numbered_import_ready": False,
        "result_ready_status": "not_result_ready",
    }


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "source_pages": len(rows),
        "fetched_pages": sum(1 for row in rows if row["fetch_status"] == "fetched"),
        "source_candidate_pages": sum(
            1 for row in rows if row["source_audit_status"] == "source_candidate_needs_import"
        ),
        "verse_import_ready_pages": sum(
            1 for row in rows if bool(row["verse_numbered_import_ready"])
        ),
        "result_ready_pages": sum(
            1 for row in rows if row["result_ready_status"] != "not_result_ready"
        ),
        "apocrypha_marker_pages": sum(
            1 for row in rows if bool(row["apocrypha_marker_present"])
        ),
        "public_domain_marker_pages": sum(
            1 for row in rows if bool(row["public_domain_marker_present"])
        ),
        "claim_status": "source_status_only_not_result_bearing",
    }


def build_anchors(
    rows: list[dict[str, object]],
    summary: dict[str, object],
) -> list[dict[str, str]]:
    row = rows[0] if rows else {}
    checks = [
        (
            "wikisource",
            "page_fetch_status_recorded",
            bool(row.get("fetch_status")),
            "fetch status recorded for the Wikisource candidate",
        ),
        (
            "wikisource",
            "apocrypha_marker_recorded",
            "apocrypha_marker_present" in row,
            "Apocrypha marker presence is recorded without retaining text",
        ),
        (
            "wikisource",
            "verse_import_not_ready",
            int(summary["verse_import_ready_pages"]) == 0,
            "no verse-numbered import is declared ready",
        ),
        (
            "wikisource",
            "result_not_ready",
            int(summary["result_ready_pages"]) == 0,
            "no result-bearing replication is declared ready",
        ),
    ]
    return [
        {
            "source": source,
            "anchor": anchor,
            "status": "found" if ok else "missing",
            "diagnostic": diagnostic,
        }
        for source, anchor, ok, diagnostic in checks
    ]


def write_markdown(
    path: Path,
    summary: dict[str, object],
    rows: list[dict[str, object]],
    anchors: list[dict[str, str]],
) -> None:
    found = sum(1 for row in anchors if row["status"] == "found")
    lines = [
        "# KJVA Wikisource Candidate Source Audit",
        "",
        "Status: source-status audit only. This is not an ELS result, not a",
        "corpus import, and not a claim-ready replication.",
        "",
        "## Setup",
        "",
        "This audit checks whether the Wikisource Ballantyne KJV + Apocrypha",
        "candidate can be named as a future source candidate. It fetches the",
        "page, records metadata and source markers, and does not retain or",
        "commit Bible text.",
        "",
        "Primary candidate:",
        "",
        f"- {WIKISOURCE_URL}",
        "",
        "## Findings",
        "",
        f"- Source pages checked: {summary['source_pages']}.",
        f"- Fetched pages: {summary['fetched_pages']}.",
        f"- Pages with Apocrypha marker: {summary['apocrypha_marker_pages']}.",
        f"- Pages with public-domain marker: {summary['public_domain_marker_pages']}.",
        "- Verse-numbered import ready pages: 0.",
        "- Result-ready pages: 0.",
        "",
        "This is useful only as a source-candidate check. A future KJVA",
        "replication still needs lawful text import, verse mapping, book-order",
        "lock, collation against the current eBible KJVA source family, checksum",
        "record, term lock, and study-lock sidecar before any ELS run.",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| source pages | {summary['source_pages']} |",
        f"| fetched pages | {summary['fetched_pages']} |",
        f"| source-candidate pages | {summary['source_candidate_pages']} |",
        f"| verse import ready pages | {summary['verse_import_ready_pages']} |",
        f"| result ready pages | {summary['result_ready_pages']} |",
        f"| Apocrypha marker pages | {summary['apocrypha_marker_pages']} |",
        f"| public-domain marker pages | {summary['public_domain_marker_pages']} |",
        "",
        "## Page Status",
        "",
        "| Source | Fetch | Bytes | Title | Apocrypha | KJV | 1769 | Ballantyne | Public Domain | Status |",
        "| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["source_id"]),
                    markdown_cell(row["fetch_status"]),
                    markdown_cell(row["bytes"]),
                    markdown_cell(row["title"]),
                    markdown_cell(row["apocrypha_marker_present"]),
                    markdown_cell(row["kjv_marker_present"]),
                    markdown_cell(row["standard_1769_marker_present"]),
                    markdown_cell(row["ballantyne_marker_present"]),
                    markdown_cell(row["public_domain_marker_present"]),
                    markdown_cell(row["source_audit_status"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Protocol Anchors",
            "",
            f"Found anchors: {found} of {len(anchors)}.",
            "",
            "| Source | Anchor | Status | Diagnostic |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in anchors:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["source"]),
                    f"`{markdown_cell(row['anchor'])}`",
                    markdown_cell(row["status"]),
                    markdown_cell(row["diagnostic"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "This audit does not import Bible text, normalize verses, run ELS",
            "searches, evaluate controls, or upgrade the completed KJVA bridge",
            "lane. It only records whether the Wikisource page remains a",
            "metadata-level candidate for future source work.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    anchors: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "sources": [args.url],
        "rows": len(rows),
        "summary": summary,
        "anchors": anchors,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "source-status audit only; no ELS result",
        "text_retention": "metadata only; no Bible text retained",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
