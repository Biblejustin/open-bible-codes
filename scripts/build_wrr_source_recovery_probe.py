#!/usr/bin/env python3
"""Summarize live WRR/Torah-code source recovery probe downloads."""

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
from typing import Any

from els import __version__


DEFAULT_MANIFEST = Path("reports/wrr_source_recovery_probe/sources.manifest.json")
DEFAULT_OUT = Path("reports/wrr_source_recovery_probe/source_recovery_probe.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_source_recovery_probe/source_recovery_probe_summary.csv")
DEFAULT_MD = Path("docs/WRR_SOURCE_RECOVERY_PROBE.md")
DEFAULT_MANIFEST_OUT = Path("reports/wrr_source_recovery_probe/source_recovery_probe.manifest.json")

EXPECTED_LABELS = {
    "torah_code_research_program_1": "Research Program",
    "torah_code_research_program_1_shtml": "Research Program",
    "torah_code_research_program_2": "Research Program",
    "torah_code_research_program_2_shtml": "Research Program",
    "torah_code_research_model_overview": "The Model",
    "torah_code_research_model_overview_shtml": "The Model",
    "torah_code_research_geometric_model_level_1": "The Geometric Model",
    "torah_code_research_geometric_model_level_1_shtml": "The Geometric Model",
    "torah_code_research_geometric_model_level_2": "Geometric Model Level 2",
    "torah_code_research_geometric_model_level_2_shtml": "Geometric Model Level 2",
    "torah_code_research_geometric_model_level_3": "Geometric Model Level 3",
    "torah_code_research_geometric_model_level_3_shtml": "Geometric Model Level 3",
    "torah_code_research_els_model_level_1": "ELS Model Level 1",
    "torah_code_research_els_model_level_1_shtml": "ELS Model Level 1",
    "torah_code_research_els_model_level_2": "ELS Model Level 2",
    "torah_code_research_els_model_level_2_shtml": "ELS Model Level 2",
    "torah_code_research_els_model_level_3": "ELS Model Level 3",
    "torah_code_research_els_model_level_3_shtml": "ELS Model Level 3",
}
SPAM_MARKERS = ("slot bet", "deposit pulsa", "rtp slot")
ROOT_URL = "https://www.torah-code.org"

ROW_FIELDNAMES = [
    "label",
    "requested_url",
    "final_url",
    "redirected",
    "http_status",
    "download_status",
    "path",
    "bytes",
    "sha256",
    "title",
    "canonical",
    "expected_label",
    "expected_label_present",
    "canonical_is_root",
    "final_url_is_root",
    "spam_marker_present",
    "usable_status",
]
SUMMARY_FIELDNAMES = [
    "downloads",
    "expected_label_rows",
    "expected_label_present_rows",
    "redirected_rows",
    "root_final_url_rows",
    "root_canonical_rows",
    "spam_marker_rows",
    "usable_current_source_rows",
    "unusable_current_download_rows",
    "current_recovery_status",
]


class HtmlMetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title_parts: list[str] = []
        self.canonical = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lower_attrs = {name.lower(): value or "" for name, value in attrs}
        if tag.lower() == "title":
            self.in_title = True
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
    manifest = read_json(args.manifest)
    rows = [analyze_download(row) for row in manifest.get("downloads", [])]
    summary = build_summary(rows)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, rows, args.manifest)
    write_manifest(args.manifest_out, args, summary, len(rows), started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    return parser


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def analyze_download(download: dict[str, Any]) -> dict[str, object]:
    label = str(download.get("label", ""))
    path = Path(str(download.get("path", "")))
    expected_label = EXPECTED_LABELS.get(label, "")
    text = ""
    title = ""
    canonical = ""
    actual_bytes = int(download.get("bytes") or 0)
    sha256 = str(download.get("sha256") or "")
    if path.exists():
        raw = path.read_bytes()
        actual_bytes = len(raw)
        sha256 = hashlib.sha256(raw).hexdigest()
        text = raw.decode("utf-8", errors="replace")
        parser = HtmlMetadataParser()
        parser.feed(text)
        title = html.unescape(parser.title)
        canonical = parser.canonical
    lower_text = text.lower()
    final_url = str(download.get("final_url") or "")
    requested_url = str(download.get("url") or "")
    expected_present = bool(expected_label and expected_label.lower() in lower_text)
    canonical_is_root = canonical.rstrip("/") == ROOT_URL
    final_url_is_root = final_url.rstrip("/") == ROOT_URL
    spam_marker_present = any(marker in lower_text for marker in SPAM_MARKERS)
    usable = (
        path.exists()
        and expected_present
        and not canonical_is_root
        and not final_url_is_root
        and not spam_marker_present
    )
    if not path.exists():
        usable_status = "probe_file_missing"
    elif usable:
        usable_status = "usable_current_source"
    else:
        usable_status = "unusable_current_download"
    return {
        "label": label,
        "requested_url": requested_url,
        "final_url": final_url,
        "redirected": bool(download.get("redirected", False)),
        "http_status": download.get("http_status"),
        "download_status": download.get("status", ""),
        "path": str(path),
        "bytes": actual_bytes,
        "sha256": sha256,
        "title": title,
        "canonical": canonical,
        "expected_label": expected_label,
        "expected_label_present": expected_present,
        "canonical_is_root": canonical_is_root,
        "final_url_is_root": final_url_is_root,
        "spam_marker_present": spam_marker_present,
        "usable_status": usable_status,
    }


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    status_counts = Counter(str(row["usable_status"]) for row in rows)
    usable = status_counts.get("usable_current_source", 0)
    return {
        "downloads": len(rows),
        "expected_label_rows": sum(1 for row in rows if row["expected_label"]),
        "expected_label_present_rows": sum(1 for row in rows if row["expected_label_present"]),
        "redirected_rows": sum(1 for row in rows if row["redirected"]),
        "root_final_url_rows": sum(1 for row in rows if row["final_url_is_root"]),
        "root_canonical_rows": sum(1 for row in rows if row["canonical_is_root"]),
        "spam_marker_rows": sum(1 for row in rows if row["spam_marker_present"]),
        "usable_current_source_rows": usable,
        "unusable_current_download_rows": status_counts.get("unusable_current_download", 0),
        "current_recovery_status": (
            "some_live_sources_recovered" if usable else "no_live_sources_recovered"
        ),
    }


def write_markdown(
    path: Path,
    summary: dict[str, object],
    rows: list[dict[str, object]],
    source_manifest: Path,
) -> None:
    lines = [
        "# WRR Source Recovery Probe",
        "",
        "Status: live-source recovery probe only. This does not run ELS searches,",
        "does not update the cached `reports/wrr_1994/` bundle, and does not make",
        "claim-ready source decisions.",
        "",
        "## Summary",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| downloads probed | {summary['downloads']} |",
        f"| rows with expected labels configured | {summary['expected_label_rows']} |",
        f"| rows where expected label appeared | {summary['expected_label_present_rows']} |",
        f"| redirected rows | {summary['redirected_rows']} |",
        f"| final URL is Torah-code root | {summary['root_final_url_rows']} |",
        f"| canonical URL is Torah-code root | {summary['root_canonical_rows']} |",
        f"| unrelated slot/gambling markers | {summary['spam_marker_rows']} |",
        f"| usable current source rows | {summary['usable_current_source_rows']} |",
        "",
        f"Current recovery status: `{summary['current_recovery_status']}`.",
        "",
        "## Probe Rows",
        "",
        "| Label | HTTP | Redirected | Final Root | Expected Text | Spam Marker | Bytes | SHA-256 | Status |",
        "| --- | ---: | --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["label"]),
                    markdown_cell(row["http_status"]),
                    markdown_cell(row["redirected"]),
                    markdown_cell(row["final_url_is_root"]),
                    markdown_cell(row["expected_label_present"]),
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
            f"Probe manifest: `{source_manifest}`.",
            "Use this document to see whether previously missing Torah-code model pages",
            "have become directly recoverable. A row is treated as usable only when the",
            "download contains the expected page label, does not declare the site root as",
            "canonical, does not end at the site root URL, and lacks unrelated spam markers.",
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
        "input_manifest": str(args.manifest),
        "rows": rows,
        "summary": summary,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "live-source recovery probe only; no ELS result",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
