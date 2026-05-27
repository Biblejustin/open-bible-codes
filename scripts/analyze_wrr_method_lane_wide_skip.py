#!/usr/bin/env python3
"""Probe WRR method-lane terms for wider-skip ordinary Genesis hits."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from els import __version__
from els.corpus import Corpus, load_corpus
from els.normalization import normalize_text
from els.search import build_hit, iter_els_query_matches_by_lanes


DEFAULT_METHOD_PACKET = Path(
    "reports/wrr_1994/wrr_method_pair_universe_evidence_packet.csv"
)
DEFAULT_CONFIG = Path("configs/example_koren_genesis.toml")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_method_lane_wide_skip_probe.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/wrr_1994/wrr_method_lane_wide_skip_probe_summary.csv"
)
DEFAULT_MD = Path("docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_method_lane_wide_skip_probe.manifest.json"
)
DEFAULT_PROFILE_SKIPS = (250, 1000, 2500, 5000)
DEFAULT_MAX_SKIP = 5000

BASE_FIELDNAMES = [
    "term_id",
    "term",
    "normalized_term",
    "concept",
    "row_number",
    "pair_id",
    "date_term_id",
    "max_skip",
    "direction",
]
TAIL_FIELDNAMES = [
    "total_hits_through_max",
    "found_within_max_skip",
    "first_hit_skip",
    "first_hit_direction",
    "first_hit_start_offset",
    "first_hit_end_offset",
    "first_hit_start_ref",
    "first_hit_end_ref",
    "first_hit_span_letters",
    "read",
]
SUMMARY_FIELDNAMES = [
    "terms",
    "max_skip",
    "direction",
    "profile_skips",
    "terms_with_any_hit",
    "terms_zero_through_max",
    "terms_with_first_hit_after_1000",
    "total_hits_through_max",
    "read",
]
BOUNDARY = (
    "Wide-skip hits are diagnostic only; no source correction, method change, "
    "or pair exclusion is selected."
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    profiles = normalize_profiles(args.profile_skip, args.max_skip)
    packet_rows = read_rows(args.method_packet)
    corpus = load_corpus(args.config)
    probe_rows = build_probe_rows(
        packet_rows,
        corpus,
        profiles=profiles,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.jobs,
    )
    summary_rows = build_summary_rows(
        probe_rows,
        profiles=profiles,
        max_skip=args.max_skip,
        direction=args.direction,
    )
    write_csv(args.out, probe_fieldnames(profiles), probe_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, probe_rows, summary_rows, profiles, args)
    write_manifest(args.manifest_out, args, profiles, probe_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method-packet", type=Path, default=DEFAULT_METHOD_PACKET)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--max-skip", type=int, default=DEFAULT_MAX_SKIP)
    parser.add_argument(
        "--profile-skip",
        type=int,
        action="append",
        default=list(DEFAULT_PROFILE_SKIPS),
        help="Skip cap to count cumulatively. Can be repeated.",
    )
    parser.add_argument(
        "--direction",
        choices=("forward", "backward", "both"),
        default="both",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Search jobs. Default 1 avoids multiprocessing startup fragility.",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def normalize_profiles(profile_skips: Iterable[int], max_skip: int) -> list[int]:
    profiles = sorted({skip for skip in profile_skips if 2 <= skip <= max_skip})
    if max_skip not in profiles:
        profiles.append(max_skip)
    return profiles


def probe_fieldnames(profiles: list[int]) -> list[str]:
    return [
        *BASE_FIELDNAMES,
        *[profile_field(profile) for profile in profiles],
        *TAIL_FIELDNAMES,
    ]


def profile_field(profile: int) -> str:
    return f"hits_le_{profile}"


def build_probe_rows(
    packet_rows: list[dict[str, str]],
    corpus: Corpus,
    *,
    profiles: list[int],
    max_skip: int,
    direction: str,
    jobs: int,
) -> list[dict[str, object]]:
    query_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in packet_rows:
        query = normalize_text(row.get("term", ""), corpus.language)
        if query:
            query_rows[query].append(row)

    profile_counts: dict[str, dict[int, int]] = {
        query: {profile: 0 for profile in profiles} for query in query_rows
    }
    total_counts: dict[str, int] = {query: 0 for query in query_rows}
    first_hits: dict[str, tuple[int, int, int]] = {}

    for query, skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        query_rows.keys(),
        min_skip=2,
        max_skip=max_skip,
        direction=direction,
        jobs=jobs,
    ):
        total_counts[query] += 1
        abs_skip = abs(skip)
        for profile in profiles:
            if abs_skip <= profile:
                profile_counts[query][profile] += 1
        if query not in first_hits:
            first_hits[query] = (skip, start, end)

    rows: list[dict[str, object]] = []
    for packet_row in packet_rows:
        term = packet_row.get("term", "")
        query = normalize_text(term, corpus.language)
        first = first_hits.get(query)
        output: dict[str, object] = {
            "term_id": packet_row.get("term_id", ""),
            "term": term,
            "normalized_term": query,
            "concept": packet_row.get("concept", ""),
            "row_number": packet_row.get("row_number", ""),
            "pair_id": packet_row.get("pair_id", ""),
            "date_term_id": packet_row.get("date_term_id", ""),
            "max_skip": max_skip,
            "direction": direction,
        }
        for profile in profiles:
            output[profile_field(profile)] = profile_counts.get(query, {}).get(profile, 0)
        output["total_hits_through_max"] = total_counts.get(query, 0)
        if first is None:
            output.update(empty_hit_fields(max_skip))
        else:
            skip, start, end = first
            hit = build_hit(corpus, term, query, skip, start, end)
            output.update(
                {
                    "found_within_max_skip": "true",
                    "first_hit_skip": hit.skip,
                    "first_hit_direction": hit.direction,
                    "first_hit_start_offset": hit.start_offset,
                    "first_hit_end_offset": hit.end_offset,
                    "first_hit_start_ref": hit.start_ref,
                    "first_hit_end_ref": hit.end_ref,
                    "first_hit_span_letters": hit.span_letters,
                    "read": hit_read(hit.skip),
                }
            )
        rows.append(output)
    return rows


def empty_hit_fields(max_skip: int) -> dict[str, object]:
    return {
        "found_within_max_skip": "false",
        "first_hit_skip": "",
        "first_hit_direction": "",
        "first_hit_start_offset": "",
        "first_hit_end_offset": "",
        "first_hit_start_ref": "",
        "first_hit_end_ref": "",
        "first_hit_span_letters": "",
        "read": (
            f"No ordinary Genesis ELS hit found through skip {max_skip}; this "
            "is not a near-cap miss under the wide-skip probe."
        ),
    }


def hit_read(skip: int) -> str:
    abs_skip = abs(skip)
    if abs_skip <= 1000:
        return (
            "Unexpected ordinary hit inside the selected high-cap range; review "
            "against corrected-distance inputs."
        )
    return (
        "First ordinary hit appears only beyond the selected high-cap range; "
        "diagnostic only, not a method change."
    )


def build_summary_rows(
    probe_rows: list[dict[str, object]],
    *,
    profiles: list[int],
    max_skip: int,
    direction: str,
) -> list[dict[str, object]]:
    terms = len(probe_rows)
    with_hit = sum(1 for row in probe_rows if row["found_within_max_skip"] == "true")
    after_1000 = sum(
        1
        for row in probe_rows
        if row["found_within_max_skip"] == "true"
        and abs(int(row["first_hit_skip"])) > 1000
    )
    total_hits = sum(int(row["total_hits_through_max"]) for row in probe_rows)
    return [
        {
            "terms": terms,
            "max_skip": max_skip,
            "direction": direction,
            "profile_skips": ";".join(str(profile) for profile in profiles),
            "terms_with_any_hit": with_hit,
            "terms_zero_through_max": terms - with_hit,
            "terms_with_first_hit_after_1000": after_1000,
            "total_hits_through_max": total_hits,
            "read": summary_read(terms, with_hit, max_skip),
        }
    ]


def summary_read(terms: int, with_hit: int, max_skip: int) -> str:
    if with_hit == 0:
        return (
            f"All {terms} OCR-matched method-lane terms remain absent through "
            f"skip {max_skip}; the method lane is not explained by a small cap "
            "extension."
        )
    return (
        f"{with_hit} of {terms} OCR-matched method-lane terms have a wider-skip "
        "ordinary hit; diagnostic only."
    )


def write_markdown(
    path: Path,
    probe_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    profiles: list[int],
    args: argparse.Namespace,
) -> None:
    summary = summary_rows[0] if summary_rows else {}
    lines = [
        "# WRR Method-Lane Wide-Skip Probe",
        "",
        "Status: diagnostic probe for OCR-matched WRR method-lane terms.",
        "It does not choose source corrections, method changes, or pair exclusions.",
        "",
        "## Setup",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_method_lane_wide_skip "
            f"--method-packet {args.method_packet} "
            f"--config {args.config} "
            f"--max-skip {args.max_skip} "
            f"--direction {args.direction} "
            f"--jobs {args.jobs} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- method-lane terms: {summary.get('terms', 0)}.",
        f"- max skip probed: {summary.get('max_skip', args.max_skip)}.",
        f"- profile skips: {summary.get('profile_skips', '')}.",
        f"- terms with any wider-skip hit: {summary.get('terms_with_any_hit', 0)}.",
        f"- terms still zero through max skip: {summary.get('terms_zero_through_max', 0)}.",
        f"- total hits through max skip: {summary.get('total_hits_through_max', 0)}.",
        f"- boundary: {BOUNDARY}",
        "",
        "## Term Results",
        "",
        "| Rank | Term id | Term | Hits <=1000 | Hits <=5000 | First hit | Read |",
        "| ---: | --- | --- | ---: | ---: | --- | --- |",
    ]
    for index, row in enumerate(probe_rows, start=1):
        hit_1000 = row.get("hits_le_1000", "")
        hit_max = row.get(profile_field(max(profiles)), "")
        first_hit = row.get("first_hit_skip") or "none"
        lines.append(
            "| {rank} | `{term_id}` | `{term}` | {hit_1000} | {hit_max} | {first_hit} | {read} |".format(
                rank=index,
                term_id=row.get("term_id", ""),
                term=row.get("term", ""),
                hit_1000=hit_1000,
                hit_max=hit_max,
                first_hit=first_hit,
                read=row.get("read", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Cautions",
            "",
            "- This is a cap-sensitivity diagnostic, not a WRR reproduction result.",
            "- Absence through wider skips does not establish that the source row is wrong.",
            "- No row here changes the locked local WRR method report.",
            "- Exact published reproduction remains caveated by the documented 163-distance gap.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    profiles: list[int],
    probe_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_wrr_method_lane_wide_skip",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "parameters": {
            "max_skip": args.max_skip,
            "direction": args.direction,
            "jobs": args.jobs,
            "profile_skips": profiles,
        },
        "inputs": {
            "method_packet": str(args.method_packet),
            "config": str(args.config),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
        "probe_rows": len(probe_rows),
        "summary_rows": len(summary_rows),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    raise SystemExit(main())
