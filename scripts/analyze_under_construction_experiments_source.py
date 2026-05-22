#!/usr/bin/env python3
"""Audit Torah-code.org under-construction experiment pages without ELS results."""

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
    Path("reports/wrr_1994/torah_code_experiment_chumash.html"),
    Path("reports/wrr_1994/torah_code_experiment_twin_towers.html"),
    Path("reports/wrr_1994/torah_code_experiment_tsunami.html"),
    Path("reports/wrr_1994/torah_code_experiment_katrina.html"),
    Path("reports/wrr_1994/torah_code_experiment_great_rabbis.html"),
    Path("reports/wrr_1994/torah_code_experiment_son_rabbis.html"),
]
EXPECTED_LABELS = {
    "chumash": "Chumash",
    "twin_towers": "Twin Towers",
    "tsunami": "Tsunami",
    "katrina": "Katrina",
    "great_rabbis": "Great Rabbis",
    "son_rabbis": "Son Rabbis",
}
DEFAULT_OUT = Path("reports/wrr_1994/under_construction_experiment_pages.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/under_construction_experiment_summary.csv")
DEFAULT_ANCHORS_OUT = Path("reports/wrr_1994/under_construction_experiment_anchors.csv")
DEFAULT_MD = Path("docs/UNDER_CONSTRUCTION_EXPERIMENT_SOURCE_AUDIT.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/under_construction_experiment_source_audit.manifest.json"
)

ROW_FIELDNAMES = [
    "experiment",
    "path",
    "bytes",
    "sha256",
    "title",
    "heading",
    "link_count",
    "pdf_link_count",
    "under_construction",
    "expected_label_present",
    "title_matches_expected",
    "heading_matches_expected",
]
SUMMARY_FIELDNAMES = [
    "source_files",
    "under_construction_pages",
    "pdf_link_pages",
    "title_mismatch_pages",
    "heading_mismatch_pages",
    "katrina_mislabeled_tsunami",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.links: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "a":
            for name, value in attrs:
                if name.lower() == "href" and value:
                    self.links.append(value)

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
    experiment = experiment_for_path(path)
    expected_label = EXPECTED_LABELS.get(experiment, experiment)
    title = extractor.title
    heading = extract_heading(text)
    lower_text = extractor.text.lower()
    return {
        "experiment": experiment,
        "path": str(path),
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "title": title,
        "heading": heading,
        "link_count": len(extractor.links),
        "pdf_link_count": sum(1 for link in extractor.links if ".pdf" in link.lower()),
        "under_construction": "under construction" in lower_text,
        "expected_label_present": expected_label.lower() in lower_text,
        "title_matches_expected": expected_label.lower() in title.lower(),
        "heading_matches_expected": expected_label.lower() in heading.lower(),
    }


def experiment_for_path(path: Path) -> str:
    name = path.name.lower()
    for experiment in EXPECTED_LABELS:
        if experiment in name:
            return experiment
    return "unknown"


def extract_heading(text: str) -> str:
    match = re.search(r"<p><b>(.*?)</b></p>", text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    heading = re.sub(r"<.*?>", "", match.group(1))
    return normalize_space(html.unescape(heading))


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "source_files": len(rows),
        "under_construction_pages": sum(1 for row in rows if row["under_construction"]),
        "pdf_link_pages": sum(1 for row in rows if int(row["pdf_link_count"]) > 0),
        "title_mismatch_pages": sum(1 for row in rows if not row["title_matches_expected"]),
        "heading_mismatch_pages": sum(1 for row in rows if not row["heading_matches_expected"]),
        "katrina_mislabeled_tsunami": any(
            row["experiment"] == "katrina" and "tsunami" in str(row["title"]).lower()
            for row in rows
        ),
        "claim_status": "source_status_only_not_data_bearing",
    }


def protocol_anchors(
    rows: list[dict[str, object]],
    summary: dict[str, object],
) -> list[dict[str, str]]:
    checks: list[tuple[str, str, bool, str]] = [
        (
            "all_pages",
            "all_pages_under_construction",
            int(summary["under_construction_pages"]) == len(rows),
            "all audited pages report Under Construction",
        ),
        (
            "all_pages",
            "no_pdf_data_links",
            int(summary["pdf_link_pages"]) == 0,
            "audited pages do not link source PDFs",
        ),
        (
            "katrina",
            "katrina_page_mislabeled_tsunami",
            bool(summary["katrina_mislabeled_tsunami"]),
            "Katrina source file title/body is labeled Tsunami",
        ),
    ]
    for row in rows:
        checks.append(
            (
                str(row["experiment"]),
                f"{row['experiment']}_under_construction",
                bool(row["under_construction"]),
                f"{row['experiment']} page reports Under Construction",
            )
        )
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
        "# Under-Construction Experiment Source Audit",
        "",
        "Status: source-status audit only. This is not an ELS result, not a",
        "statistical test, and not a claim-ready replication.",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| source files scanned | {summary['source_files']} |",
        f"| under-construction pages | {summary['under_construction_pages']} |",
        f"| pages linking PDFs | {summary['pdf_link_pages']} |",
        f"| title mismatch pages | {summary['title_mismatch_pages']} |",
        f"| heading mismatch pages | {summary['heading_mismatch_pages']} |",
        f"| Katrina mislabeled as Tsunami | {summary['katrina_mislabeled_tsunami']} |",
        "",
        "## Page Status",
        "",
        "| Experiment | Title | Heading | Under Construction | Title Match | Heading Match |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['experiment']} | {row['title']} | {row['heading']} | "
            f"{row['under_construction']} | {row['title_matches_expected']} | "
            f"{row['heading_matches_expected']} |"
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
            "These pages are status placeholders in this crawl. They should not supply",
            "terms, controls, p-values, or source data unless a future source recovery",
            "finds data-bearing pages and records fresh checksums.",
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
