#!/usr/bin/env python3
"""Audit Hakkaac KJV Apocrypha pages as marker-only boundary candidates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from els import __version__


DEFAULT_OUT_DIR = Path("reports/kjva_hakkaac_apocrypha_boundary_candidate")
DEFAULT_ROWS = DEFAULT_OUT_DIR / "chapter_markers.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_HAKKAAC_APOCRYPHA_BOUNDARY_CANDIDATE.md")
USER_AGENT = "OpenBibleCodes-EDLS Hakkaac boundary candidate audit/1.0"

HAKKAAC_SIRACH_URL = (
    "https://hakkaac.org/Bible/Bible/ap/KJV/KJV-AP/KJV_Sirach.html"
)
HAKKAAC_MANASSEH_URL = (
    "https://hakkaac.org/Bible/Bible/ap/KJV/KJV-AP/KJV_Prayer-of-Manasses.html"
)

ROW_FIELDNAMES = [
    "page_id",
    "source_url",
    "source_status",
    "bytes",
    "sha256",
    "license_note_present",
    "book",
    "chapter",
    "marker_count",
    "markers_present",
    "target_markers",
    "target_status",
    "candidate_status",
    "notes",
]
SUMMARY_FIELDNAMES = [
    "pages_scanned",
    "license_note_pages",
    "sirach_44_marker_count",
    "sirach_44_has_23",
    "prayer_marker_count",
    "prayer_has_1_to_15",
    "candidate_resolves_sirach",
    "candidate_resolves_prayer",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]


@dataclass(frozen=True)
class PageCandidate:
    page_id: str
    url: str
    book: str
    chapter_heading: str
    chapter: int
    target_markers: tuple[int, ...]


@dataclass(frozen=True)
class TextPayload:
    raw: bytes
    final_url: str
    status: str
    error: str = ""


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[str] = []

    def handle_data(self, data: str) -> None:
        normalized = " ".join(data.split())
        if normalized:
            self.items.append(normalized)


CANDIDATES: tuple[PageCandidate, ...] = (
    PageCandidate(
        page_id="hakkaac_sirach_44",
        url=HAKKAAC_SIRACH_URL,
        book="SIR",
        chapter_heading="Sirach 44",
        chapter=44,
        target_markers=(23,),
    ),
    PageCandidate(
        page_id="hakkaac_manasseh_1",
        url=HAKKAAC_MANASSEH_URL,
        book="MAN",
        chapter_heading="Prayer of Manasses 1",
        chapter=1,
        target_markers=tuple(range(1, 16)),
    ),
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = [analyze_candidate(candidate, timeout=args.timeout) for candidate in CANDIDATES]
    summary = build_summary(rows)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary)
    write_manifest(args.manifest_out, args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--out", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def analyze_candidate(candidate: PageCandidate, *, timeout: float) -> dict[str, Any]:
    payload = fetch_page(candidate.url, timeout=timeout)
    text = payload.raw.decode("utf-8", errors="replace")
    visible_items = html_visible_items(text)
    markers = extract_chapter_markers(visible_items, candidate.chapter_heading)
    marker_set = set(markers)
    target_set = set(candidate.target_markers)
    missing = sorted(target_set - marker_set)
    if not missing:
        target_status = "all_target_markers_present"
    elif len(candidate.target_markers) == 1:
        target_status = "target_marker_missing"
    else:
        target_status = "target_marker_range_incomplete"
    candidate_status = classify_candidate(candidate, target_status)
    return {
        "page_id": candidate.page_id,
        "source_url": payload.final_url,
        "source_status": payload.status,
        "bytes": len(payload.raw),
        "sha256": hashlib.sha256(payload.raw).hexdigest() if payload.raw else "",
        "license_note_present": license_note_present(text),
        "book": candidate.book,
        "chapter": candidate.chapter,
        "marker_count": len(markers),
        "markers_present": compact_markers(markers),
        "target_markers": compact_markers(candidate.target_markers),
        "target_status": target_status,
        "candidate_status": candidate_status,
        "notes": notes_for_candidate(candidate, target_status),
    }


def fetch_page(url: str, *, timeout: float) -> TextPayload:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            return TextPayload(
                raw=response.read(),
                final_url=response.geturl(),
                status=f"http_{response.status}",
            )
    except HTTPError as exc:
        return TextPayload(raw=b"", final_url=url, status=f"http_error_{exc.code}", error=str(exc))
    except (OSError, URLError) as exc:
        return TextPayload(raw=b"", final_url=url, status="fetch_error", error=str(exc))


def html_visible_items(text: str) -> list[str]:
    parser = VisibleTextParser()
    parser.feed(text)
    return parser.items


def extract_chapter_markers(items: list[str], chapter_heading: str) -> list[int]:
    try:
        start = items.index(chapter_heading)
    except ValueError:
        return []
    try:
        marker_start = items.index("▽", start) + 1
    except ValueError:
        return []
    markers: list[int] = []
    index = marker_start
    while index < len(items):
        item = items[index]
        if item.startswith("◁") or item.startswith("◀") or item == "Old Testament":
            break
        if item.isdigit():
            markers.append(int(item))
        index += 1
    return markers


def compact_markers(markers: tuple[int, ...] | list[int]) -> str:
    values = list(markers)
    if not values:
        return ""
    if len(values) == 1:
        return str(values[0])
    if values == list(range(values[0], values[-1] + 1)):
        return f"{values[0]}..{values[-1]}"
    return ";".join(str(value) for value in values)


def license_note_present(text: str) -> bool:
    lowered = text.lower()
    return (
        "public domain" in lowered
        and "outside the united kingdom" in lowered
        and "king james bible" in lowered
    )


def classify_candidate(candidate: PageCandidate, target_status: str) -> str:
    if candidate.book == "SIR" and target_status == "all_target_markers_present":
        return "sirach_marker_gap_candidate_not_source_lock"
    if candidate.book == "MAN" and target_status == "all_target_markers_present":
        return "prayer_boundary_candidate_not_source_lock"
    if candidate.book == "SIR" and target_status == "target_marker_missing":
        return "does_not_resolve_sirach_marker_gap"
    return "candidate_needs_review"


def notes_for_candidate(candidate: PageCandidate, target_status: str) -> str:
    if candidate.book == "SIR" and target_status == "all_target_markers_present":
        return "Marker-only audit finds Sirach 44:23 on this candidate page."
    if candidate.book == "SIR":
        return "Marker-only audit finds no Sirach 44:23 marker on this candidate page."
    if candidate.book == "MAN" and target_status == "all_target_markers_present":
        return "Marker-only audit finds Prayer of Manasseh markers 1..15 on this candidate page."
    return "Marker-only audit needs review."


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_page = {row["page_id"]: row for row in rows}
    sirach = by_page.get("hakkaac_sirach_44", {})
    prayer = by_page.get("hakkaac_manasseh_1", {})
    return {
        "pages_scanned": len(rows),
        "license_note_pages": sum(1 for row in rows if bool(row["license_note_present"])),
        "sirach_44_marker_count": sirach.get("marker_count", 0),
        "sirach_44_has_23": sirach.get("target_status") == "all_target_markers_present",
        "prayer_marker_count": prayer.get("marker_count", 0),
        "prayer_has_1_to_15": prayer.get("markers_present") == "1..15",
        "candidate_resolves_sirach": sirach.get("target_status") == "all_target_markers_present",
        "candidate_resolves_prayer": prayer.get("target_status") == "all_target_markers_present",
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "candidate_audit_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    rows: list[dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    lines = [
        "# KJVA Hakkaac Apocrypha Boundary Candidate",
        "",
        "Status: candidate audit only.",
        "",
        "This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.",
        "It scans Hakkaac KJV Apocrypha pages for visible verse markers only.",
        "It does not commit Bible text, normalize Bible text, create a local corpus, split unmarked prose, or authorize a result-bearing run.",
        "",
        "## Summary",
        "",
        f"- Pages scanned: {summary['pages_scanned']}.",
        f"- Pages with public-domain note: {summary['license_note_pages']}.",
        f"- Sirach 44 marker count: {summary['sirach_44_marker_count']}.",
        f"- Sirach 44 has marker 23: {int(bool(summary['sirach_44_has_23']))}.",
        f"- Prayer of Manasseh marker count: {summary['prayer_marker_count']}.",
        f"- Prayer of Manasseh has markers 1..15: {int(bool(summary['prayer_has_1_to_15']))}.",
        f"- Candidate resolves Sirach blocker: {int(bool(summary['candidate_resolves_sirach']))}.",
        f"- Candidate resolves Prayer blocker: {int(bool(summary['candidate_resolves_prayer']))}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready sources: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Marker Rows",
        "",
        "| Page | Book | Chapter | Markers | Target | Status | Candidate status |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['page_id']}` | {row['book']} | {row['chapter']} | `{row['markers_present']}` | `{row['target_markers']}` | `{row['target_status']}` | `{row['candidate_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "This candidate helps the Prayer of Manasseh boundary question because the page exposes markers 1..15.",
            "This candidate helps the Sirach marker-gap question because the Sirach 44 page exposes marker 23.",
            "Any use still needs a source-use decision, checksum lock, collation against current KJVA, source-order rule, and study-lock sidecar before results.",
            "",
            "## Boundary",
            "",
            "No Bible text is written to tracked outputs.",
            "This page does not change KJVA bridge result status.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, Any]],
    summary: dict[str, Any],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.analyze_kjva_hakkaac_apocrypha_boundary_candidate",
        "claim_boundary": "candidate audit only; no ELS result",
        "text_retention": "no Bible text written to tracked outputs",
        "row_count": len(rows),
        "summary": summary,
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {"urls": [candidate.url for candidate in CANDIDATES]},
        "outputs": {
            "rows": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
