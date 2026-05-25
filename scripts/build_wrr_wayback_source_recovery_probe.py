#!/usr/bin/env python3
"""Probe Wayback snapshots for missing Torah-code research source pages."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

from els import __version__


DEFAULT_OUT_DIR = Path("reports/wrr_wayback_source_recovery_probe")
DEFAULT_OUT = DEFAULT_OUT_DIR / "wayback_source_recovery_probe.csv"
DEFAULT_SUMMARY_OUT = DEFAULT_OUT_DIR / "wayback_source_recovery_probe_summary.csv"
DEFAULT_MD = Path("docs/WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md")
DEFAULT_MANIFEST_OUT = DEFAULT_OUT_DIR / "wayback_source_recovery_probe.manifest.json"

WAYBACK_AVAILABLE_ENDPOINT = "https://archive.org/wayback/available?url="
WAYBACK_CDX_ENDPOINT = "https://web.archive.org/cdx?url="
SPAM_MARKERS = ("slot bet", "deposit pulsa", "rtp slot")


@dataclass(frozen=True)
class ProbeSource:
    label: str
    concept: str
    url: str
    expected_label: str
    family: str


PROBE_SOURCES = (
    ProbeSource(
        "torah_code_research_program_1_html",
        "research_program_1",
        "https://www.torah-code.org/research/research_1.html",
        "Research Program",
        "research_program",
    ),
    ProbeSource(
        "torah_code_research_program_1_shtml",
        "research_program_1",
        "http://www.torah-code.org/research/research_1.shtml",
        "Research Program",
        "research_program",
    ),
    ProbeSource(
        "torah_code_research_program_2_html",
        "research_program_2",
        "https://www.torah-code.org/research/research_2.html",
        "Research Program",
        "research_program",
    ),
    ProbeSource(
        "torah_code_research_program_2_shtml",
        "research_program_2",
        "http://www.torah-code.org/research/research_2.shtml",
        "Research Program",
        "research_program",
    ),
    ProbeSource(
        "torah_code_research_model_overview_html",
        "model_overview",
        "https://www.torah-code.org/research/research_2a.html",
        "The Model",
        "research_model",
    ),
    ProbeSource(
        "torah_code_research_model_overview_shtml",
        "model_overview",
        "http://www.torah-code.org/research/research_2a.shtml",
        "The Model",
        "research_model",
    ),
    ProbeSource(
        "torah_code_research_geometric_model_level_1_html",
        "geometric_model_level_1",
        "https://www.torah-code.org/research/research_3.html",
        "The Geometric Model",
        "geometric_model",
    ),
    ProbeSource(
        "torah_code_research_geometric_model_level_1_shtml",
        "geometric_model_level_1",
        "http://www.torah-code.org/research/research_3.shtml",
        "The Geometric Model",
        "geometric_model",
    ),
    ProbeSource(
        "torah_code_research_geometric_model_level_2_html",
        "geometric_model_level_2",
        "https://www.torah-code.org/research/research_3a.html",
        "Geometric Model Level 2",
        "geometric_model",
    ),
    ProbeSource(
        "torah_code_research_geometric_model_level_2_shtml",
        "geometric_model_level_2",
        "http://www.torah-code.org/research/research_3a.shtml",
        "Geometric Model Level 2",
        "geometric_model",
    ),
    ProbeSource(
        "torah_code_research_geometric_model_level_3_html",
        "geometric_model_level_3",
        "https://www.torah-code.org/research/research_3b.html",
        "Geometric Model Level 3",
        "geometric_model",
    ),
    ProbeSource(
        "torah_code_research_geometric_model_level_3_shtml",
        "geometric_model_level_3",
        "http://www.torah-code.org/research/research_3b.shtml",
        "Geometric Model Level 3",
        "geometric_model",
    ),
    ProbeSource(
        "torah_code_research_els_model_level_1_html",
        "els_model_level_1",
        "https://www.torah-code.org/research/research_3c.html",
        "ELS Model Level 1",
        "els_model",
    ),
    ProbeSource(
        "torah_code_research_els_model_level_1_shtml",
        "els_model_level_1",
        "http://www.torah-code.org/research/research_3c.shtml",
        "ELS Model Level 1",
        "els_model",
    ),
    ProbeSource(
        "torah_code_research_els_model_level_2_html",
        "els_model_level_2",
        "https://www.torah-code.org/research/research_3d.html",
        "ELS Model Level 2",
        "els_model",
    ),
    ProbeSource(
        "torah_code_research_els_model_level_2_shtml",
        "els_model_level_2",
        "http://www.torah-code.org/research/research_3d.shtml",
        "ELS Model Level 2",
        "els_model",
    ),
    ProbeSource(
        "torah_code_research_els_model_level_3_html",
        "els_model_level_3",
        "https://www.torah-code.org/research/research_3e.html",
        "ELS Model Level 3",
        "els_model",
    ),
    ProbeSource(
        "torah_code_research_els_model_level_3_shtml",
        "els_model_level_3",
        "http://www.torah-code.org/research/research_3e.shtml",
        "ELS Model Level 3",
        "els_model",
    ),
)

SOURCE_BY_LABEL = {source.label: source for source in PROBE_SOURCES}

ROW_FIELDNAMES = [
    "label",
    "concept",
    "family",
    "original_url",
    "expected_label",
    "availability_status",
    "closest_available",
    "closest_status",
    "closest_timestamp",
    "closest_url",
    "snapshot_source",
    "cdx_status",
    "cdx_candidate_count",
    "archive_raw_url",
    "archive_fetch_status",
    "path",
    "bytes",
    "sha256",
    "title",
    "expected_label_present",
    "spam_marker_present",
    "usable_status",
]

SUMMARY_FIELDNAMES = [
    "probe_rows",
    "unique_concepts",
    "availability_available_rows",
    "cdx_checked_rows",
    "cdx_candidate_rows",
    "cdx_fallback_rows",
    "archive_downloaded_rows",
    "expected_label_present_rows",
    "spam_marker_rows",
    "usable_archived_source_rows",
    "usable_archived_concepts",
    "missing_archived_concepts",
    "current_archive_recovery_status",
]


class HtmlMetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True

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
    sources = selected_sources(args.label)
    rows = [
        probe_source(source, args.snapshot_dir, refresh=args.refresh)
        for source in sources
    ]
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
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_OUT_DIR / "snapshots")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument(
        "--label",
        action="append",
        default=[],
        help="Probe only a specific Wayback source label. May be repeated.",
    )
    return parser


def selected_sources(labels: list[str]) -> list[ProbeSource]:
    if not labels:
        return list(PROBE_SOURCES)
    unknown = [label for label in labels if label not in SOURCE_BY_LABEL]
    if unknown:
        raise SystemExit("unknown Wayback source labels: " + ", ".join(unknown))
    return [SOURCE_BY_LABEL[label] for label in labels]


def probe_source(
    source: ProbeSource,
    snapshot_dir: Path,
    *,
    refresh: bool,
) -> dict[str, object]:
    availability_status = "availability_checked"
    closest: dict[str, Any] = {}
    snapshot_source = ""
    cdx_status = "not_checked"
    cdx_candidate_count = 0
    availability_url = wayback_availability_url(source.url)
    try:
        availability = fetch_json(availability_url)
        closest = closest_snapshot(availability)
    except Exception as exc:  # pragma: no cover - exact network failures vary.
        availability_status = f"availability_error:{type(exc).__name__}"
    closest_available = bool(closest.get("available"))
    if closest_available:
        snapshot_source = "availability_closest"
    else:
        try:
            cdx_candidates = cdx_snapshots(source.url)
            cdx_candidate_count = len(cdx_candidates)
            cdx_status = "cdx_checked"
            closest = select_cdx_snapshot(cdx_candidates)
            if closest.get("available"):
                snapshot_source = "cdx_fallback"
                closest_available = True
        except Exception as exc:  # pragma: no cover - exact network failures vary.
            cdx_status = f"cdx_error:{type(exc).__name__}"
    closest_url = str(closest.get("url") or "")
    archive_raw_url = wayback_raw_snapshot_url(closest_url)
    target = snapshot_dir / f"{source.label}.html"
    archive_fetch_status = "not_available"
    raw = b""
    if closest_available and archive_raw_url:
        if target.exists() and not refresh:
            archive_fetch_status = "cached"
            raw = target.read_bytes()
        else:
            try:
                raw = fetch_bytes(archive_raw_url)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
                archive_fetch_status = "downloaded"
            except Exception as exc:  # pragma: no cover - exact network failures vary.
                archive_fetch_status = f"download_error:{type(exc).__name__}"
                raw = b""
    return analyze_snapshot(
        source=source,
        availability_status=availability_status,
        closest=closest,
        archive_raw_url=archive_raw_url,
        archive_fetch_status=archive_fetch_status,
        snapshot_source=snapshot_source,
        cdx_status=cdx_status,
        cdx_candidate_count=cdx_candidate_count,
        path=target if raw else None,
        raw=raw,
    )


def analyze_snapshot(
    *,
    source: ProbeSource,
    availability_status: str,
    closest: dict[str, Any],
    archive_raw_url: str,
    archive_fetch_status: str,
    snapshot_source: str,
    cdx_status: str,
    cdx_candidate_count: int,
    path: Path | None,
    raw: bytes,
) -> dict[str, object]:
    text = raw.decode("utf-8", errors="replace") if raw else ""
    lower_text = text.lower()
    parser = HtmlMetadataParser()
    if text:
        parser.feed(text)
    expected_present = source.expected_label.lower() in lower_text
    spam_marker_present = any(marker in lower_text for marker in SPAM_MARKERS)
    usable = bool(raw and expected_present and not spam_marker_present)
    if usable:
        usable_status = "usable_archived_source"
    elif not closest.get("available"):
        usable_status = "no_archived_snapshot"
    elif not raw:
        usable_status = "archive_download_failed"
    else:
        usable_status = "unusable_archived_snapshot"
    return {
        "label": source.label,
        "concept": source.concept,
        "family": source.family,
        "original_url": source.url,
        "expected_label": source.expected_label,
        "availability_status": availability_status,
        "closest_available": bool(closest.get("available", False)),
        "closest_status": closest.get("status", ""),
        "closest_timestamp": closest.get("timestamp", ""),
        "closest_url": closest.get("url", ""),
        "snapshot_source": snapshot_source,
        "cdx_status": cdx_status,
        "cdx_candidate_count": cdx_candidate_count,
        "archive_raw_url": archive_raw_url,
        "archive_fetch_status": archive_fetch_status,
        "path": str(path or ""),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest() if raw else "",
        "title": html.unescape(parser.title),
        "expected_label_present": expected_present,
        "spam_marker_present": spam_marker_present,
        "usable_status": usable_status,
    }


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    status_counts = Counter(str(row["usable_status"]) for row in rows)
    concepts = {str(row["concept"]) for row in rows}
    usable_concepts = {
        str(row["concept"])
        for row in rows
        if row["usable_status"] == "usable_archived_source"
    }
    usable_rows = status_counts.get("usable_archived_source", 0)
    return {
        "probe_rows": len(rows),
        "unique_concepts": len(concepts),
        "availability_available_rows": sum(
            1 for row in rows if row["closest_available"]
        ),
        "cdx_checked_rows": sum(
            1 for row in rows if str(row["cdx_status"]).startswith("cdx_")
        ),
        "cdx_candidate_rows": sum(
            1 for row in rows if int(row["cdx_candidate_count"]) > 0
        ),
        "cdx_fallback_rows": sum(
            1 for row in rows if row["snapshot_source"] == "cdx_fallback"
        ),
        "archive_downloaded_rows": sum(
            1 for row in rows if row["archive_fetch_status"] in {"downloaded", "cached"}
        ),
        "expected_label_present_rows": sum(
            1 for row in rows if row["expected_label_present"]
        ),
        "spam_marker_rows": sum(1 for row in rows if row["spam_marker_present"]),
        "usable_archived_source_rows": usable_rows,
        "usable_archived_concepts": len(usable_concepts),
        "missing_archived_concepts": len(concepts - usable_concepts),
        "current_archive_recovery_status": (
            "partial_archived_sources_recovered"
            if usable_rows
            else "no_archived_sources_recovered"
        ),
    }


def wayback_availability_url(url: str) -> str:
    return WAYBACK_AVAILABLE_ENDPOINT + quote(url, safe="")


def wayback_cdx_url(url: str) -> str:
    params = (
        "&output=json"
        "&fl=timestamp,statuscode,mimetype,digest,original"
        "&filter=statuscode:200"
        "&collapse=digest"
        "&limit=20"
    )
    return WAYBACK_CDX_ENDPOINT + quote(url, safe="") + params


def closest_snapshot(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return dict(payload.get("archived_snapshots", {}).get("closest", {}))


def cdx_snapshots(url: str) -> list[dict[str, str]]:
    payload = fetch_json(wayback_cdx_url(url))
    if not isinstance(payload, list) or len(payload) <= 1:
        return []
    header = [str(value) for value in payload[0]]
    rows: list[dict[str, str]] = []
    for raw_row in payload[1:]:
        if not isinstance(raw_row, list):
            continue
        row = {
            header[index]: str(value)
            for index, value in enumerate(raw_row)
            if index < len(header)
        }
        if row.get("timestamp") and row.get("original"):
            rows.append(row)
    return rows


def select_cdx_snapshot(rows: list[dict[str, str]]) -> dict[str, Any]:
    if not rows:
        return {}
    row = rows[-1]
    timestamp = row["timestamp"]
    original = row["original"]
    return {
        "available": True,
        "status": row.get("statuscode", ""),
        "timestamp": timestamp,
        "url": f"https://web.archive.org/web/{timestamp}/{original}",
    }


def wayback_raw_snapshot_url(snapshot_url: str) -> str:
    if not snapshot_url:
        return ""
    match = re.search(r"https?://web\.archive\.org/web/(\d+)/(.*)", snapshot_url)
    if not match:
        return snapshot_url
    timestamp, original_url = match.groups()
    return f"https://web.archive.org/web/{timestamp}id_/{original_url}"


def fetch_json(url: str) -> Any:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 EDLS source audit"})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 EDLS source audit"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def write_markdown(
    path: Path,
    summary: dict[str, object],
    rows: list[dict[str, object]],
) -> None:
    usable_rows = [
        row for row in rows if row["usable_status"] == "usable_archived_source"
    ]
    missing_concepts = sorted(
        {str(row["concept"]) for row in rows}
        - {str(row["concept"]) for row in usable_rows}
    )
    lines = [
        "# WRR Wayback Source Recovery Probe",
        "",
        "Status: archived-source recovery probe only. This does not run ELS searches,",
        "does not update the cached `reports/wrr_1994/` bundle, and does not make",
        "claim-ready source decisions.",
        "",
        "## Summary",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| Wayback URLs probed | {summary['probe_rows']} |",
        f"| unique research concepts probed | {summary['unique_concepts']} |",
        f"| rows with archived snapshot | {summary['availability_available_rows']} |",
        f"| rows checked with CDX fallback | {summary['cdx_checked_rows']} |",
        f"| rows with CDX exact-URL candidates | {summary['cdx_candidate_rows']} |",
        f"| rows recovered through CDX fallback | {summary['cdx_fallback_rows']} |",
        f"| archived files downloaded or cached | {summary['archive_downloaded_rows']} |",
        f"| rows where expected label appeared | {summary['expected_label_present_rows']} |",
        f"| unrelated slot/gambling markers | {summary['spam_marker_rows']} |",
        f"| usable archived source rows | {summary['usable_archived_source_rows']} |",
        f"| usable archived concepts | {summary['usable_archived_concepts']} |",
        f"| missing archived concepts | {summary['missing_archived_concepts']} |",
        "",
        f"Current archive recovery status: `{summary['current_archive_recovery_status']}`.",
        "",
        "## Usable Archived Concepts",
        "",
        "| Concept | Label | Timestamp | Title | Archived source |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in usable_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["concept"]),
                    markdown_cell(row["label"]),
                    markdown_cell(row["closest_timestamp"]),
                    markdown_cell(row["title"]),
                    markdown_link("snapshot", str(row["archive_raw_url"])),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Missing Archived Concepts",
            "",
            "| Concept | Read |",
            "| --- | --- |",
        ]
    )
    for concept in missing_concepts:
        lines.append(
            f"| {markdown_cell(concept)} | no usable archived source recovered in this probe |"
        )
    lines.extend(
        [
            "",
            "## Probe Rows",
            "",
            "| Label | Available | Source | Timestamp | CDX candidates | Expected Text | Spam Marker | Bytes | SHA-256 | Status |",
            "| --- | --- | --- | --- | ---: | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["label"]),
                    markdown_cell(row["closest_available"]),
                    markdown_cell(row["snapshot_source"]),
                    markdown_cell(row["closest_timestamp"]),
                    markdown_cell(row["cdx_candidate_count"]),
                    markdown_cell(row["expected_label_present"]),
                    markdown_cell(row["spam_marker_present"]),
                    markdown_cell(row["bytes"]),
                    f"`{str(row['sha256'])[:16]}`" if row["sha256"] else "",
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
            "This archive probe recovers research-program and model-context pages when",
            "Wayback has a clean snapshot. It first checks the Wayback closest-snapshot",
            "endpoint and then falls back to CDX exact-URL 200-capture rows when the",
            "closest endpoint returns no archived snapshot. The CDX fallback did not",
            "recover the missing level-2/3 geometric-model or ELS-model pages in this",
            "run, and it does not resolve WRR residual appellation normalization or",
            "pair-rule questions.",
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
        "rows": rows,
        "summary": summary,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "archived-source recovery probe only; no ELS result",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


def markdown_link(label: str, url: str) -> str:
    if not url:
        return ""
    return f"[{label}]({url})"


if __name__ == "__main__":
    raise SystemExit(main())
