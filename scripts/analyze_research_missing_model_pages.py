#!/usr/bin/env python3
"""Audit missing Torah-code research model level-2/3 pages without ELS results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from collections import Counter
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path

from els import __version__


DEFAULT_OVERVIEW = Path("reports/wrr_1994/torah_code_research_model_overview.html")
DEFAULT_SOURCES = [
    Path("reports/wrr_1994/torah_code_research_geometric_model_level_2.html"),
    Path("reports/wrr_1994/torah_code_research_geometric_model_level_3.html"),
    Path("reports/wrr_1994/torah_code_research_els_model_level_2.html"),
    Path("reports/wrr_1994/torah_code_research_els_model_level_3.html"),
]
EXPECTED = {
    "torah_code_research_geometric_model_level_2.html": (
        "geometric_model_level_2",
        "Geometric Model Level 2",
        "https://www.torah-code.org/research/research_3a.html",
    ),
    "torah_code_research_geometric_model_level_3.html": (
        "geometric_model_level_3",
        "Geometric Model Level 3",
        "https://www.torah-code.org/research/research_3b.html",
    ),
    "torah_code_research_els_model_level_2.html": (
        "els_model_level_2",
        "ELS Model Level 2",
        "https://www.torah-code.org/research/research_3d.html",
    ),
    "torah_code_research_els_model_level_3.html": (
        "els_model_level_3",
        "ELS Model Level 3",
        "https://www.torah-code.org/research/research_3e.html",
    ),
}
DEFAULT_OUT = Path("reports/wrr_1994/research_missing_model_pages.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/research_missing_model_pages_summary.csv")
DEFAULT_ANCHORS_OUT = Path("reports/wrr_1994/research_missing_model_pages_anchors.csv")
DEFAULT_MD = Path("docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/research_missing_model_pages.manifest.json")

ROW_FIELDNAMES = [
    "model_page",
    "path",
    "requested_url",
    "bytes",
    "sha256",
    "title",
    "canonical",
    "expected_label",
    "expected_label_present",
    "canonical_is_root",
    "spam_marker_present",
    "usable_status",
]
SUMMARY_FIELDNAMES = [
    "source_files",
    "overview_expected_level23_links",
    "expected_label_present_files",
    "root_canonical_files",
    "spam_marker_files",
    "usable_model_pages",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


class HtmlMetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.links: list[str] = []
        self.canonical = ""
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lower_attrs = {name.lower(): value or "" for name, value in attrs}
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "a" and lower_attrs.get("href"):
            self.links.append(lower_attrs["href"])
        if tag.lower() == "link" and lower_attrs.get("rel", "").lower() == "canonical":
            self.canonical = lower_attrs.get("href", "")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title and data.strip():
            self.title_parts.append(data.strip())

    @property
    def title(self) -> str:
        return normalize_space(" ".join(self.title_parts))


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    sources = args.source or DEFAULT_SOURCES
    args.source = sources
    rows = [analyze_file(path) for path in sources]
    overview_links = count_overview_level23_links(args.overview)
    summary = build_summary(rows, overview_links)
    anchors = protocol_anchors(rows, summary)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, rows, anchors)
    write_manifest(args.manifest_out, args, summary, anchors, len(rows), started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--overview", type=Path, default=DEFAULT_OVERVIEW)
    parser.add_argument("--source", action="append", type=Path, default=[])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def analyze_file(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    parser = HtmlMetadataParser()
    parser.feed(text)
    model_page, expected_label, requested_url = EXPECTED[path.name]
    lower_text = text.lower()
    expected_present = expected_label.lower() in lower_text
    root_canonical = parser.canonical.rstrip("/") == "https://www.torah-code.org"
    spam_marker = any(marker in lower_text for marker in ["slot bet", "deposit pulsa", "rtp slot"])
    usable = expected_present and not root_canonical and not spam_marker
    return {
        "model_page": model_page,
        "path": str(path),
        "requested_url": requested_url,
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "title": html.unescape(parser.title),
        "canonical": parser.canonical,
        "expected_label": expected_label,
        "expected_label_present": expected_present,
        "canonical_is_root": root_canonical,
        "spam_marker_present": spam_marker,
        "usable_status": "usable_model_page" if usable else "unusable_redirect_or_root_content",
    }


def count_overview_level23_links(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    return sum(
        1
        for target in ["research_3a.html", "research_3b.html", "research_3d.html", "research_3e.html"]
        if target in text
    )


def build_summary(rows: list[dict[str, object]], overview_links: int) -> dict[str, object]:
    return {
        "source_files": len(rows),
        "overview_expected_level23_links": overview_links,
        "expected_label_present_files": sum(1 for row in rows if row["expected_label_present"]),
        "root_canonical_files": sum(1 for row in rows if row["canonical_is_root"]),
        "spam_marker_files": sum(1 for row in rows if row["spam_marker_present"]),
        "usable_model_pages": sum(1 for row in rows if row["usable_status"] == "usable_model_page"),
        "claim_status": "source_status_only_not_data_bearing",
    }


def protocol_anchors(
    rows: list[dict[str, object]],
    summary: dict[str, object],
) -> list[dict[str, str]]:
    checks = [
        (
            "overview",
            "overview_links_four_level23_pages",
            int(summary["overview_expected_level23_links"]) == 4,
            "overview links four level-2/3 model pages",
        ),
        (
            "downloads",
            "all_four_downloads_present",
            int(summary["source_files"]) == 4,
            "four linked model pages downloaded",
        ),
        (
            "downloads",
            "no_expected_model_labels_present",
            int(summary["expected_label_present_files"]) == 0,
            "downloaded pages do not contain expected model labels",
        ),
        (
            "downloads",
            "all_canonical_root",
            int(summary["root_canonical_files"]) == 4,
            "downloaded pages declare root canonical URL",
        ),
        (
            "downloads",
            "all_spam_markers_present",
            int(summary["spam_marker_files"]) == 4,
            "downloaded pages contain unrelated slot/gambling markers",
        ),
        (
            "downloads",
            "no_usable_level23_model_pages",
            int(summary["usable_model_pages"]) == 0,
            "no linked level-2/3 model page is usable source material",
        ),
    ]
    return [
        {
            "source": source,
            "anchor": anchor,
            "status": "found" if found else "missing",
            "diagnostic": diagnostic if found else "anchor text not found",
        }
        for source, anchor, found, diagnostic in checks
    ]


def write_markdown(
    path: Path,
    summary: dict[str, object],
    rows: list[dict[str, object]],
    anchors: list[dict[str, str]],
) -> None:
    anchor_counts = Counter(anchor["status"] for anchor in anchors)
    lines = [
        "# Research Missing Model Pages Audit",
        "",
        "Status: source-status audit only. This is not an ELS result, not a",
        "statistical test, and not a claim-ready model reconstruction.",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| downloaded source files | {summary['source_files']} |",
        f"| overview level-2/3 links | {summary['overview_expected_level23_links']} |",
        f"| files containing expected model labels | {summary['expected_label_present_files']} |",
        f"| files declaring root canonical URL | {summary['root_canonical_files']} |",
        f"| files with unrelated slot/gambling markers | {summary['spam_marker_files']} |",
        f"| usable level-2/3 model pages | {summary['usable_model_pages']} |",
        "",
        "## Page Status",
        "",
        "| Model Page | Expected Label Present | Canonical Is Root | Unrelated Marker | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['model_page']} | {row['expected_label_present']} | "
            f"{row['canonical_is_root']} | {row['spam_marker_present']} | "
            f"{row['usable_status']} |"
        )
    lines.extend(
        [
            "",
            "## Protocol Anchors",
            "",
            f"Found anchors: {anchor_counts.get('found', 0)} of {len(anchors)}.",
            "",
            "| Source | Anchor | Status | Diagnostic |",
            "| --- | --- | --- | --- |",
        ]
    )
    for anchor in anchors:
        lines.append(
            f"| {anchor['source']} | `{anchor['anchor']}` | {anchor['status']} | {anchor['diagnostic']} |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "The overview links level-2/3 geometric and ELS model pages, but the current",
            "downloads are root-canonical pages with unrelated slot/gambling content and",
            "no expected model labels. Treat these four levels as missing source material",
            "until clean Torah-code research pages are recovered and checksummed.",
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
    anchors: list[dict[str, str]],
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "overview": str(args.overview),
        "sources": [str(path) for path in args.source],
        "summary": summary,
        "anchor_status_counts": dict(Counter(anchor["status"] for anchor in anchors)),
        "rows": rows,
        "outputs": {
            "pages": str(args.out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "source-status audit only; no ELS result",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
