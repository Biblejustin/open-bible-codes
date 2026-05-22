#!/usr/bin/env python3
"""Audit Torah-code.org hypothesis-testing pages without ELS results."""

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


DEFAULT_SOURCES = [
    Path("reports/wrr_1994/torah_code_hypothesis_testing_overview.html"),
    Path("reports/wrr_1994/torah_code_hypothesis_testing_errors.html"),
    Path("reports/wrr_1994/torah_code_hypothesis_testing_hypotheses.html"),
    Path("reports/wrr_1994/torah_code_hypothesis_testing_simulated_experiments.html"),
]
EXPECTED_LABELS = {
    "overview": "Hypothesis Testing",
    "errors": "Types of Errors",
    "hypotheses": "Types of Hypotheses",
    "simulated_experiments": "Simulated Experiments",
}
METHOD_ANCHORS = (
    "Null hypothesis",
    "Alternative hypothesis",
    "test statistic",
    "critical region",
    "acceptance region",
)
SPAM_MARKERS = ("slot bet", "deposit pulsa", "rtp slot")
ROOT_URL = "https://www.torah-code.org"

DEFAULT_OUT = Path("reports/wrr_1994/hypothesis_testing_source_pages.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/hypothesis_testing_source_summary.csv")
DEFAULT_ANCHORS_OUT = Path("reports/wrr_1994/hypothesis_testing_source_anchors.csv")
DEFAULT_MD = Path("docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/hypothesis_testing_source_audit.manifest.json")

ROW_FIELDNAMES = [
    "page",
    "path",
    "bytes",
    "sha256",
    "title",
    "canonical",
    "link_count",
    "expected_label",
    "expected_label_present",
    "spam_marker_present",
    "canonical_is_root",
    "method_anchor_count",
    "usable_status",
]
SUMMARY_FIELDNAMES = [
    "source_files",
    "expected_label_present_pages",
    "spam_marker_pages",
    "root_canonical_pages",
    "usable_method_pages",
    "unusable_method_pages",
    "overview_method_anchor_count",
    "overview_link_count",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self.links: list[str] = []
        self.canonical = ""
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lower_attrs = {name.lower(): value or "" for name, value in attrs}
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "a":
            href = lower_attrs.get("href", "")
            if href:
                self.links.append(href)
        if tag.lower() == "link" and lower_attrs.get("rel", "").lower() == "canonical":
            self.canonical = lower_attrs.get("href", "")

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
    source_paths = args.source or DEFAULT_SOURCES
    args.source = source_paths
    rows = [analyze_file(path) for path in source_paths]
    summary = build_summary(rows)
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
    extractor = TextExtractor()
    extractor.feed(text)
    page = page_for_path(path)
    expected_label = EXPECTED_LABELS.get(page, page)
    normalized_text = extractor.text
    lower_text = normalized_text.lower()
    canonical = html.unescape(extractor.canonical)
    expected_present = expected_label.lower() in lower_text
    spam_marker_present = any(marker in lower_text for marker in SPAM_MARKERS)
    canonical_is_root = canonical.rstrip("/") == ROOT_URL
    method_anchor_count = sum(anchor.lower() in lower_text for anchor in METHOD_ANCHORS)
    usable = expected_present and not spam_marker_present and not canonical_is_root
    return {
        "page": page,
        "path": str(path),
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "title": html.unescape(extractor.title),
        "canonical": canonical,
        "link_count": len(extractor.links),
        "expected_label": expected_label,
        "expected_label_present": expected_present,
        "spam_marker_present": spam_marker_present,
        "canonical_is_root": canonical_is_root,
        "method_anchor_count": method_anchor_count,
        "usable_status": "usable_method_source" if usable else "unusable_current_download",
    }


def page_for_path(path: Path) -> str:
    name = path.name.lower()
    if "overview" in name:
        return "overview"
    if "errors" in name:
        return "errors"
    if "hypotheses" in name:
        return "hypotheses"
    if "simulated_experiments" in name:
        return "simulated_experiments"
    return "unknown"


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    status_counts = Counter(str(row["usable_status"]) for row in rows)
    overview = next((row for row in rows if row["page"] == "overview"), {})
    return {
        "source_files": len(rows),
        "expected_label_present_pages": sum(1 for row in rows if row["expected_label_present"]),
        "spam_marker_pages": sum(1 for row in rows if row["spam_marker_present"]),
        "root_canonical_pages": sum(1 for row in rows if row["canonical_is_root"]),
        "usable_method_pages": status_counts.get("usable_method_source", 0),
        "unusable_method_pages": status_counts.get("unusable_current_download", 0),
        "overview_method_anchor_count": overview.get("method_anchor_count", 0),
        "overview_link_count": overview.get("link_count", 0),
        "claim_status": "source_status_only_not_result_bearing",
    }


def protocol_anchors(
    rows: list[dict[str, object]],
    summary: dict[str, object],
) -> list[dict[str, str]]:
    by_page = {str(row["page"]): row for row in rows}
    checks: list[tuple[str, str, bool, str]] = [
        (
            "overview",
            "overview_expected_label_present",
            bool(by_page.get("overview", {}).get("expected_label_present")),
            "overview page contains the Hypothesis Testing label",
        ),
        (
            "overview",
            "overview_method_anchors_present",
            int(summary["overview_method_anchor_count"]) >= 4,
            "overview page contains core null/alternative/test-statistic language",
        ),
        (
            "linked_pages",
            "linked_page_status_recorded",
            len(rows) >= 4,
            "overview and three linked pages were audited",
        ),
    ]
    checks.extend(
        (
            str(row["page"]),
            f"{row['page']}_usable_status_recorded",
            str(row["usable_status"]) in {"usable_method_source", "unusable_current_download"},
            f"{row['page']} current source status is explicit",
        )
        for row in rows
    )
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
    if int(summary["usable_method_pages"]):
        use_boundary = [
            "These pages can support only a general source-status statement about the",
            "site's hypothesis-testing introduction. They do not supply WRR pair rows,",
            "Fisher weights, Torah-code source data, or a result-bearing protocol.",
        ]
    else:
        use_boundary = [
            "Current live downloads do not supply usable hypothesis-testing source pages.",
            "This audit only records the unavailable/spam-root source status; it does not",
            "supply WRR pair rows, Fisher weights, Torah-code source data, or a",
            "result-bearing protocol.",
        ]
    lines = [
        "# Hypothesis-Testing Source Audit",
        "",
        "Status: source-status audit only. This is not an ELS result, not a",
        "statistical test, and not a claim-ready replication.",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| source files scanned | {summary['source_files']} |",
        f"| expected labels present | {summary['expected_label_present_pages']} |",
        f"| spam-marker pages | {summary['spam_marker_pages']} |",
        f"| root-canonical pages | {summary['root_canonical_pages']} |",
        f"| usable method pages | {summary['usable_method_pages']} |",
        f"| unusable current downloads | {summary['unusable_method_pages']} |",
        f"| overview method anchors | {summary['overview_method_anchor_count']} |",
        f"| overview links | {summary['overview_link_count']} |",
        "",
        "## Page Status",
        "",
        "| Page | Title | Expected Text | Spam Marker | Method Anchors | Links | Status |",
        "| --- | --- | --- | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["page"]),
                    markdown_cell(row["title"]),
                    markdown_cell(row["expected_label_present"]),
                    markdown_cell(row["spam_marker_present"]),
                    markdown_cell(row["method_anchor_count"]),
                    markdown_cell(row["link_count"]),
                    markdown_cell(row["usable_status"]),
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
            *use_boundary,
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
        "sources": [str(path) for path in args.source],
        "rows": rows,
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
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
