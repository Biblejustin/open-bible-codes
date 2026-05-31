#!/usr/bin/env python3
"""Build non-text blocker evidence for remaining Gutenberg KJVA source-lock gaps."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from collections import OrderedDict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from scripts.analyze_kjva_gutenberg_source_lock_prep import (
    APOCRYPHA_CHAPTER_VERSE_MARKER_RE,
    APOCRYPHA_NUMBER_ONLY_MARKER_RE,
    APOCRYPHA_TXT_URL,
    SOURCE_SECTIONS,
    detect_heading,
    normalize_heading,
    read_or_fetch_text,
)


DEFAULT_KJVA_CSV = Path("data/processed/ebible/eng-kjv.csv")
DEFAULT_OUT_DIR = Path("reports/kjva_gutenberg_source_lock_blocker_packet")
DEFAULT_MARKER_DIFF = DEFAULT_OUT_DIR / "marker_diff.csv"
DEFAULT_BOUNDARY_OPTIONS = DEFAULT_OUT_DIR / "boundary_options.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_GUTENBERG_SOURCE_LOCK_BLOCKER_PACKET.md")

MARKER_DIFF_FIELDNAMES = [
    "book",
    "local_ref",
    "chapter",
    "verse",
    "status",
    "source_line",
    "previous_source_marker",
    "next_source_marker",
    "notes",
]
BOUNDARY_OPTION_FIELDNAMES = [
    "book",
    "issue",
    "option_id",
    "recommendation_status",
    "recommendation",
    "blocker",
    "result_boundary",
]
SUMMARY_FIELDNAMES = [
    "source_status",
    "source_mode",
    "source_url_or_path",
    "apocrypha_plain_text_bytes",
    "apocrypha_plain_text_sha256",
    "raw_text_retained",
    "sirach_source_markers",
    "sirach_local_markers",
    "sirach_missing_source_marker_count",
    "sirach_extra_source_marker_count",
    "sirach_gap_refs",
    "manasseh_source_section_detected",
    "manasseh_source_section_start_line",
    "manasseh_source_section_end_line",
    "manasseh_source_markers",
    "manasseh_local_markers",
    "manasseh_boundary_option_rows",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]


@dataclass(frozen=True)
class MarkerRecord:
    component: str
    line: int
    marker_kind: str
    chapter: int
    verse: int


@dataclass(frozen=True)
class SectionSpan:
    component: str
    start_line: int
    end_line: int


@dataclass(frozen=True)
class LocalMarkerRecord:
    book: str
    ref: str
    chapter: int
    verse: int


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    payload = read_or_fetch_text(
        args.apocrypha_txt_path,
        args.apocrypha_txt_url,
        timeout=args.timeout,
    )
    source_markers, source_spans = parse_apocrypha_markers_and_spans(
        payload.raw.decode("utf-8", errors="replace")
    )
    local_markers = load_local_markers(args.kjva_csv, books=("SIR", "MAN"))
    marker_diff = build_sirach_marker_diff(
        source_markers.get("SIR", []),
        local_markers.get("SIR", []),
    )
    boundary_options = build_boundary_options(source_markers, source_spans, local_markers)
    summary = build_summary(
        payload=payload,
        source_markers=source_markers,
        source_spans=source_spans,
        local_markers=local_markers,
        marker_diff=marker_diff,
        boundary_options=boundary_options,
    )
    write_csv(args.out, MARKER_DIFF_FIELDNAMES, marker_diff)
    write_csv(args.boundary_options_out, BOUNDARY_OPTION_FIELDNAMES, boundary_options)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, marker_diff, boundary_options)
    write_manifest(
        args.manifest_out,
        args,
        summary,
        marker_diff,
        boundary_options,
        started,
    )
    print(args.out)
    print(args.boundary_options_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kjva-csv", type=Path, default=DEFAULT_KJVA_CSV)
    parser.add_argument("--apocrypha-txt-url", default=APOCRYPHA_TXT_URL)
    parser.add_argument("--apocrypha-txt-path", type=Path)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--out", type=Path, default=DEFAULT_MARKER_DIFF)
    parser.add_argument(
        "--boundary-options-out",
        type=Path,
        default=DEFAULT_BOUNDARY_OPTIONS,
    )
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def parse_apocrypha_markers_and_spans(
    text: str,
) -> tuple[dict[str, list[MarkerRecord]], dict[str, SectionSpan]]:
    aliases: dict[str, str] = {}
    for section in SOURCE_SECTIONS:
        for alias in section.aliases:
            aliases[normalize_heading(alias)] = section.component

    markers: dict[str, list[MarkerRecord]] = {
        section.component: [] for section in SOURCE_SECTIONS
    }
    spans: dict[str, SectionSpan] = {}
    lines = text.splitlines()
    current = ""
    current_start = 0
    index = 0
    while index < len(lines):
        heading = detect_heading(lines, index, aliases)
        if heading is not None:
            if current:
                spans[current] = SectionSpan(current, current_start, index)
            current, consumed = heading
            current_start = index + 1
            index += consumed
            continue

        stripped = lines[index].strip()
        marker_kind = ""
        match = APOCRYPHA_CHAPTER_VERSE_MARKER_RE.match(stripped)
        if match is not None:
            marker_kind = "chapter_verse"
            chapter = int(match.group("chapter"))
            verse = int(match.group("verse"))
        else:
            match = APOCRYPHA_NUMBER_ONLY_MARKER_RE.match(stripped)
            if match is not None:
                marker_kind = "number_only"
                chapter = 1
                verse = int(match.group("verse"))
        if current and marker_kind:
            markers[current].append(
                MarkerRecord(
                    component=current,
                    line=index + 1,
                    marker_kind=marker_kind,
                    chapter=chapter,
                    verse=verse,
                )
            )
        index += 1
    if current:
        spans[current] = SectionSpan(current, current_start, len(lines))
    return markers, spans


def load_local_markers(
    path: Path,
    *,
    books: tuple[str, ...],
) -> dict[str, list[LocalMarkerRecord]]:
    wanted = set(books)
    records: dict[str, list[LocalMarkerRecord]] = {book: [] for book in books}
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            book = row["book"]
            if book not in wanted:
                continue
            records[book].append(
                LocalMarkerRecord(
                    book=book,
                    ref=row["ref"],
                    chapter=int(row["chapter"]),
                    verse=int(row["verse"]),
                )
            )
    return records


def build_sirach_marker_diff(
    source_markers: list[MarkerRecord],
    local_markers: list[LocalMarkerRecord],
) -> list[dict[str, str]]:
    source_by_marker = {(row.chapter, row.verse): row for row in source_markers}
    local_by_marker = {(row.chapter, row.verse): row for row in local_markers}
    all_markers = sorted(set(source_by_marker) | set(local_by_marker))
    rows: list[dict[str, str]] = []
    for chapter, verse in all_markers:
        source = source_by_marker.get((chapter, verse))
        local = local_by_marker.get((chapter, verse))
        if source is not None and local is not None:
            continue
        status = "missing_source_marker" if local is not None else "extra_source_marker"
        rows.append(
            {
                "book": "SIR",
                "local_ref": local.ref if local is not None else "",
                "chapter": str(chapter),
                "verse": str(verse),
                "status": status,
                "source_line": str(source.line) if source is not None else "",
                "previous_source_marker": format_marker(
                    "SIR", nearest_previous(source_markers, chapter, verse)
                ),
                "next_source_marker": format_marker(
                    "SIR", nearest_next(source_markers, chapter, verse)
                ),
                "notes": (
                    "present in local KJVA marker list; absent from Gutenberg marker list"
                    if status == "missing_source_marker"
                    else "present in Gutenberg marker list; absent from local KJVA marker list"
                ),
            }
        )
    return rows


def nearest_previous(
    markers: list[MarkerRecord],
    chapter: int,
    verse: int,
) -> MarkerRecord | None:
    prior = [
        marker for marker in markers if (marker.chapter, marker.verse) < (chapter, verse)
    ]
    return prior[-1] if prior else None


def nearest_next(
    markers: list[MarkerRecord],
    chapter: int,
    verse: int,
) -> MarkerRecord | None:
    later = [
        marker for marker in markers if (marker.chapter, marker.verse) > (chapter, verse)
    ]
    return later[0] if later else None


def format_marker(book: str, marker: MarkerRecord | None) -> str:
    if marker is None:
        return ""
    return f"{book} {marker.chapter}:{marker.verse}@line {marker.line}"


def build_boundary_options(
    source_markers: dict[str, list[MarkerRecord]],
    source_spans: dict[str, SectionSpan],
    local_markers: dict[str, list[LocalMarkerRecord]],
) -> list[dict[str, str]]:
    sirach_diff = build_sirach_marker_diff(
        source_markers.get("SIR", []),
        local_markers.get("SIR", []),
    )
    sirach_gap = ";".join(row["local_ref"] for row in sirach_diff if row["local_ref"])
    man_span = source_spans.get("MAN")
    man_issue = (
        f"source section lines {man_span.start_line}-{man_span.end_line}; "
        f"source markers {len(source_markers.get('MAN', []))}; "
        f"local markers {len(local_markers.get('MAN', []))}"
        if man_span is not None
        else "source section not detected"
    )
    return [
        option(
            "SIR",
            f"missing Gutenberg source marker for {sirach_gap or 'unknown Sirach ref'}",
            "sirach_defer_until_citable_collation",
            "recommended",
            "Keep Sirach blocked until a citable non-text collation explains the marker gap.",
            "SIR marker list is one marker short.",
        ),
        option(
            "SIR",
            f"missing Gutenberg source marker for {sirach_gap or 'unknown Sirach ref'}",
            "sirach_do_not_auto_insert_marker",
            "required_boundary",
            "Do not insert or infer the missing marker inside the result stream automatically.",
            "Automatic insertion would be an editorial source change.",
        ),
        option(
            "MAN",
            man_issue,
            "manasseh_defer_until_citable_marked_source",
            "recommended",
            "Keep Prayer of Manasseh blocked until a citable marked source or boundary policy exists.",
            "Gutenberg section has no verse markers.",
        ),
        option(
            "MAN",
            man_issue,
            "manasseh_exclude_until_policy_lock",
            "acceptable_fallback",
            "Exclude Prayer of Manasseh from a source-locked Gutenberg stream unless a boundary policy is locked first.",
            "Unmarked prose cannot be split reproducibly without an external rule.",
        ),
        option(
            "MAN",
            man_issue,
            "manasseh_manual_split_requires_review",
            "blocked",
            "Manual 15-verse splitting requires a cited rule and separate review before any result-bearing run.",
            "Manual boundaries would affect ELS paths.",
        ),
    ]


def option(
    book: str,
    issue: str,
    option_id: str,
    recommendation_status: str,
    recommendation: str,
    blocker: str,
) -> dict[str, str]:
    return {
        "book": book,
        "issue": issue,
        "option_id": option_id,
        "recommendation_status": recommendation_status,
        "recommendation": recommendation,
        "blocker": blocker,
        "result_boundary": "not_result_bearing",
    }


def build_summary(
    *,
    payload: Any,
    source_markers: dict[str, list[MarkerRecord]],
    source_spans: dict[str, SectionSpan],
    local_markers: dict[str, list[LocalMarkerRecord]],
    marker_diff: list[dict[str, str]],
    boundary_options: list[dict[str, str]],
) -> dict[str, Any]:
    missing = [row for row in marker_diff if row["status"] == "missing_source_marker"]
    extra = [row for row in marker_diff if row["status"] == "extra_source_marker"]
    man_span = source_spans.get("MAN")
    return {
        "source_status": payload.status,
        "source_mode": payload.source_mode,
        "source_url_or_path": payload.final_url,
        "apocrypha_plain_text_bytes": len(payload.raw),
        "apocrypha_plain_text_sha256": hashlib.sha256(payload.raw).hexdigest()
        if payload.raw
        else "",
        "raw_text_retained": False,
        "sirach_source_markers": len(source_markers.get("SIR", [])),
        "sirach_local_markers": len(local_markers.get("SIR", [])),
        "sirach_missing_source_marker_count": len(missing),
        "sirach_extra_source_marker_count": len(extra),
        "sirach_gap_refs": ";".join(row["local_ref"] for row in missing if row["local_ref"]),
        "manasseh_source_section_detected": man_span is not None,
        "manasseh_source_section_start_line": man_span.start_line if man_span else "",
        "manasseh_source_section_end_line": man_span.end_line if man_span else "",
        "manasseh_source_markers": len(source_markers.get("MAN", [])),
        "manasseh_local_markers": len(local_markers.get("MAN", [])),
        "manasseh_boundary_option_rows": sum(
            1 for row in boundary_options if row["book"] == "MAN"
        ),
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "blocker_packet_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    marker_diff: list[dict[str, str]],
    boundary_options: list[dict[str, str]],
) -> None:
    lines = [
        "# KJVA Gutenberg Source-Lock Blocker Packet",
        "",
        "Status: blocker packet only.",
        "",
        "This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.",
        "It locates the two remaining Project Gutenberg KJVA source-lock blockers using marker evidence only.",
        "It does not commit Bible text, normalize Bible text, create a local corpus, split unmarked prose, or authorize a result-bearing run.",
        "",
        "## Summary",
        "",
        f"- Sirach source markers: {summary['sirach_source_markers']}.",
        f"- Sirach local markers: {summary['sirach_local_markers']}.",
        f"- Sirach missing source markers: {summary['sirach_missing_source_marker_count']}.",
        f"- Sirach extra source markers: {summary['sirach_extra_source_marker_count']}.",
        f"- Sirach gap: `{summary['sirach_gap_refs']}`.",
        f"- Prayer of Manasseh source section detected: {int(bool(summary['manasseh_source_section_detected']))}.",
        f"- Prayer of Manasseh source markers: {summary['manasseh_source_markers']}.",
        f"- Local Prayer of Manasseh markers: {summary['manasseh_local_markers']}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready sources: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Sirach Marker Gap",
        "",
        "The marker-only comparison finds one local KJVA Sirach marker that is absent from the Gutenberg marker list.",
        "",
        "| Book | Local ref | Status | Previous source marker | Next source marker |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in marker_diff:
        lines.append(
            f"| {row['book']} | `{row['local_ref']}` | `{row['status']}` | `{row['previous_source_marker']}` | `{row['next_source_marker']}` |"
        )
    lines.extend(
        [
            "",
            "## Prayer Of Manasseh Boundary",
            "",
            "The Project Gutenberg source section is detected, but it has no verse markers in the body text.",
            "The local KJVA corpus has 15 Prayer of Manasseh verse markers.",
            "",
            "## Decision Options",
            "",
            "| Book | Option | Status | Recommendation | Blocker |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in boundary_options:
        lines.append(
            f"| {row['book']} | `{row['option_id']}` | `{row['recommendation_status']}` | {row['recommendation']} | {row['blocker']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This packet narrows the blockers. It does not resolve them.",
            "Sirach remains blocked until the missing marker is explained by citable collation evidence.",
            "Prayer of Manasseh remains blocked until a marked source, exclusion policy, or cited boundary rule is chosen before results.",
            "No Bible text is written to tracked outputs.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, Any],
    marker_diff: list[dict[str, str]],
    boundary_options: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.build_kjva_gutenberg_source_lock_blocker_packet",
        "claim_boundary": "blocker packet only; no ELS result",
        "text_retention": "no Bible text written to tracked outputs",
        "row_counts": {
            "marker_diff": len(marker_diff),
            "boundary_options": len(boundary_options),
        },
        "summary": summary,
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "kjva_csv": str(args.kjva_csv),
            "apocrypha_txt_url": str(args.apocrypha_txt_url),
            "apocrypha_txt_path": str(args.apocrypha_txt_path or ""),
        },
        "outputs": {
            "marker_diff": str(args.out),
            "boundary_options": str(args.boundary_options_out),
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


def local_marker_summary(records: dict[str, list[LocalMarkerRecord]]) -> OrderedDict[str, int]:
    return OrderedDict((book, len(rows)) for book, rows in records.items())


if __name__ == "__main__":
    raise SystemExit(main())
