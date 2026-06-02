#!/usr/bin/env python3
"""Summarize completed dynamic full-span partition exports."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from els import __version__
from els.term_display import contains_greek, contains_hebrew, display_term
from scripts.export_dynamic_span_hits import ROOT
from scripts.json_utils import read_json_object
from scripts.plan_dynamic_span_partitions import DEFAULT_OUT as DEFAULT_PLAN


DEFAULT_PARTITION_SUMMARY = ROOT / "reports/dynamic_skip_focus/full_span_partition_output_summary.csv"
DEFAULT_TERM_SUMMARY = ROOT / "reports/dynamic_skip_focus/full_span_partition_term_summary.csv"
DEFAULT_EXAMPLES = ROOT / "reports/dynamic_skip_focus/full_span_partition_examples.csv"
DEFAULT_REPORT = ROOT / "docs/DYNAMIC_SKIP_FULL_SPAN_PARTITION_FINDINGS.md"
DEFAULT_MANIFEST = ROOT / "reports/dynamic_skip_focus/full_span_partition_findings.manifest.json"
DEFAULT_SUMMARY_CACHE = ROOT / "reports/dynamic_skip_focus/full_span_partition_summary_cache.json"
CACHE_VERSION = 1

PARTITION_FIELDNAMES = [
    "partition_id",
    "corpus",
    "term_id",
    "mode",
    "partition_index",
    "partition_count",
    "min_abs_skip",
    "max_abs_skip",
    "estimated_partition_hits",
    "exported_hits",
    "estimate_delta",
    "forward_hits",
    "backward_hits",
    "exact_center_word_hits",
    "top_center_refs",
    "top_center_words",
    "out",
]

TERM_FIELDNAMES = [
    "corpus",
    "term_id",
    "concept",
    "term",
    "normalized_term",
    "mode",
    "total_hit_count",
    "planned_partitions",
    "completed_partitions",
    "completed_exported_hits",
    "exact_center_word_hits",
    "coverage_status",
    "completed_skip_ranges",
]

EXAMPLE_FIELDNAMES = [
    "example_type",
    "partition_id",
    "corpus",
    "term_id",
    "concept",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "span_letters",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_word",
    "center_normalized_word",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    plan_rows = read_rows(args.plan)
    cache = {} if args.no_cache else load_summary_cache(args.summary_cache)
    if args.cache_only:
        completed = cached_plan_rows(plan_rows, cache)
        partition_rows, examples, cache_stats = summarize_cached_partitions(completed, cache)
    else:
        completed = completed_plan_rows(plan_rows, manifest_only=args.manifest_only)
        partition_rows, examples, cache_stats = summarize_partitions(
            completed,
            examples_per_partition=args.examples_per_partition,
            cache=cache,
            manifest_only=args.manifest_only,
        )
    if not args.no_cache and not args.cache_only:
        write_summary_cache(args.summary_cache, cache)
    term_rows = build_term_summary(plan_rows, partition_rows)
    write_csv(args.partition_summary, PARTITION_FIELDNAMES, partition_rows)
    write_csv(args.term_summary, TERM_FIELDNAMES, term_rows)
    write_csv(args.examples, EXAMPLE_FIELDNAMES, examples)
    write_report(args.report, plan_rows, partition_rows, term_rows, examples, args, cache_stats)
    write_manifest(args.manifest, args, plan_rows, partition_rows, term_rows, examples, cache_stats, started)
    print(args.partition_summary)
    print(args.term_summary)
    print(args.examples)
    print(args.report)
    print(args.manifest)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--partition-summary", type=Path, default=DEFAULT_PARTITION_SUMMARY)
    parser.add_argument("--term-summary", type=Path, default=DEFAULT_TERM_SUMMARY)
    parser.add_argument("--examples", type=Path, default=DEFAULT_EXAMPLES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--summary-cache", type=Path, default=DEFAULT_SUMMARY_CACHE)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument(
        "--cache-only",
        action="store_true",
        help="Refresh summaries from the existing summary cache when dense partition payloads are offline.",
    )
    parser.add_argument("--examples-per-partition", type=int, default=3)
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Summarize completion and exported-hit counts from manifests without scanning dense hit CSVs.",
    )
    return parser


def completed_plan_rows(
    plan_rows: list[dict[str, str]],
    *,
    manifest_only: bool = False,
) -> list[dict[str, str]]:
    completed = []
    for row in plan_rows:
        out = partition_output_path(row)
        manifest = partition_manifest_path(row)
        if manifest_only and manifest.exists():
            completed.append(row)
        elif out.exists() and manifest.exists():
            completed.append(row)
    return completed


def cached_plan_rows(plan_rows: list[dict[str, str]], cache: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    completed = []
    for row in plan_rows:
        if row["partition_id"] in cache and partition_manifest_path(row).exists():
            completed.append(row)
    return completed


def summarize_cached_partitions(
    rows: list[dict[str, str]],
    cache: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    summaries = []
    examples = []
    for row in rows:
        cached = cache[row["partition_id"]]
        summaries.append(dict(cached["summary"]))
        examples.extend(dict(example) for example in cached.get("examples", []))
    summaries.sort(key=lambda item: (item["corpus"], item["term_id"], int(item["partition_index"])))
    examples.sort(key=lambda item: (item["example_type"], item["corpus"], item["term_id"], item["partition_id"]))
    return summaries, examples, {"hits": len(rows), "misses": 0, "entries": len(cache)}


def summarize_partitions(
    rows: list[dict[str, str]],
    *,
    examples_per_partition: int,
    cache: dict[str, dict[str, Any]] | None = None,
    manifest_only: bool = False,
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    summaries = []
    examples = []
    cache_stats = {"hits": 0, "misses": 0, "entries": len(cache or {})}
    for row in rows:
        summary, partition_examples = cached_or_summarized_partition(
            row,
            examples_per_partition=examples_per_partition,
            cache=cache,
            cache_stats=cache_stats,
            manifest_only=manifest_only,
        )
        summaries.append(summary)
        examples.extend(partition_examples)
    summaries.sort(key=lambda item: (item["corpus"], item["term_id"], int(item["partition_index"])))
    examples.sort(key=lambda item: (item["example_type"], item["corpus"], item["term_id"], item["partition_id"]))
    cache_stats["entries"] = len(cache or {})
    return summaries, examples, cache_stats


def cached_or_summarized_partition(
    row: dict[str, str],
    *,
    examples_per_partition: int,
    cache: dict[str, dict[str, Any]] | None,
    cache_stats: dict[str, int],
    manifest_only: bool,
) -> tuple[dict[str, str], list[dict[str, str]]]:
    fingerprint = partition_fingerprint(row, examples_per_partition, manifest_only=manifest_only)
    cache_key = row["partition_id"]
    if cache is not None:
        cached = cache.get(cache_key)
        if cached and cached.get("fingerprint") == fingerprint:
            cache_stats["hits"] += 1
            return dict(cached["summary"]), [dict(example) for example in cached["examples"]]
    cache_stats["misses"] += 1
    summary, examples = summarize_partition_output(
        row,
        examples_per_partition=examples_per_partition,
        manifest_only=manifest_only,
    )
    if cache is not None:
        cache[cache_key] = {
            "fingerprint": fingerprint,
            "summary": summary,
            "examples": examples,
        }
    return summary, examples


def summarize_partition_output(
    plan_row: dict[str, str],
    *,
    examples_per_partition: int,
    manifest_only: bool = False,
) -> tuple[dict[str, str], list[dict[str, str]]]:
    out = partition_output_path(plan_row)
    if manifest_only:
        return summarize_partition_manifest(plan_row, out), []
    center_refs: Counter[str] = Counter()
    center_words: Counter[str] = Counter()
    exported_hits = 0
    forward_hits = 0
    backward_hits = 0
    exact_center_word_hits = 0
    exact_examples = []
    low_skip_examples = []
    with open_partition_output(out) as handle:
        for hit in csv.DictReader(handle):
            exported_hits += 1
            if hit.get("direction") == "forward":
                forward_hits += 1
            elif hit.get("direction") == "backward":
                backward_hits += 1
            center_refs[hit.get("center_ref", "")] += 1
            center_word = hit.get("center_normalized_word") or hit.get("center_word", "")
            if center_word:
                center_words[center_word] += 1
            if hit.get("center_normalized_word") == hit.get("normalized_term"):
                exact_center_word_hits += 1
                if len(exact_examples) < examples_per_partition:
                    exact_examples.append(compact_example(plan_row, hit, "exact_center_word"))
            candidate = compact_example(plan_row, hit, "low_abs_skip")
            if len(low_skip_examples) < examples_per_partition:
                low_skip_examples.append(candidate)
                low_skip_examples.sort(key=example_sort_key)
            elif example_sort_key(candidate) < example_sort_key(low_skip_examples[-1]):
                low_skip_examples[-1] = candidate
                low_skip_examples.sort(key=example_sort_key)

    estimated = int(plan_row["estimated_partition_hits"])
    summary = {
        "partition_id": plan_row["partition_id"],
        "corpus": plan_row["corpus"],
        "term_id": plan_row["term_id"],
        "mode": plan_row["mode"],
        "partition_index": plan_row["partition_index"],
        "partition_count": plan_row["partition_count"],
        "min_abs_skip": plan_row["min_abs_skip"],
        "max_abs_skip": plan_row["max_abs_skip"],
        "estimated_partition_hits": plan_row["estimated_partition_hits"],
        "exported_hits": str(exported_hits),
        "estimate_delta": str(exported_hits - estimated),
        "forward_hits": str(forward_hits),
        "backward_hits": str(backward_hits),
        "exact_center_word_hits": str(exact_center_word_hits),
        "top_center_refs": format_counter(center_refs, 5),
        "top_center_words": format_counter(center_words, 5),
        "out": display_path(out),
    }
    return summary, exact_examples + low_skip_examples


def summarize_partition_manifest(plan_row: dict[str, str], out: Path) -> dict[str, str]:
    manifest = read_json_object(partition_manifest_path(plan_row))
    exported_hits = int(manifest.get("exported_hits") or 0)
    estimated = int(plan_row["estimated_partition_hits"])
    return {
        "partition_id": plan_row["partition_id"],
        "corpus": plan_row["corpus"],
        "term_id": plan_row["term_id"],
        "mode": plan_row["mode"],
        "partition_index": plan_row["partition_index"],
        "partition_count": plan_row["partition_count"],
        "min_abs_skip": plan_row["min_abs_skip"],
        "max_abs_skip": plan_row["max_abs_skip"],
        "estimated_partition_hits": plan_row["estimated_partition_hits"],
        "exported_hits": str(exported_hits),
        "estimate_delta": str(exported_hits - estimated),
        "forward_hits": "not_computed",
        "backward_hits": "not_computed",
        "exact_center_word_hits": "not_computed",
        "top_center_refs": "",
        "top_center_words": "",
        "out": display_path(out),
    }


def build_term_summary(
    plan_rows: list[dict[str, str]],
    partition_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    planned: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    completed: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in plan_rows:
        planned[(row["corpus"], row["term_id"], row["mode"])].append(row)
    for row in partition_rows:
        completed[(row["corpus"], row["term_id"], row["mode"])].append(row)

    output = []
    for key, rows in sorted(planned.items()):
        completed_rows = sorted(completed.get(key, []), key=lambda item: int(item["partition_index"]))
        template = rows[0]
        completed_count = len(completed_rows)
        planned_count = int(template["partition_count"])
        completed_hits = sum(int(row["exported_hits"]) for row in completed_rows)
        exact_hits = sum_int_cells_or_not_computed(row["exact_center_word_hits"] for row in completed_rows)
        coverage_status = "complete" if completed_count == planned_count else "partial" if completed_count else "not_started"
        output.append(
            {
                "corpus": template["corpus"],
                "term_id": template["term_id"],
                "concept": template.get("concept", ""),
                "term": template.get("term", ""),
                "normalized_term": template.get("normalized_term", ""),
                "mode": template["mode"],
                "total_hit_count": template["total_hit_count"],
                "planned_partitions": str(planned_count),
                "completed_partitions": str(completed_count),
                "completed_exported_hits": str(completed_hits),
                "exact_center_word_hits": str(exact_hits),
                "coverage_status": coverage_status,
                "completed_skip_ranges": "; ".join(
                    f"{row['min_abs_skip']}-{row['max_abs_skip']}" for row in completed_rows[:10]
                ),
            }
        )
    return output


def compact_example(plan_row: dict[str, str], hit: dict[str, str], example_type: str) -> dict[str, str]:
    return {
        "example_type": example_type,
        "partition_id": plan_row["partition_id"],
        "corpus": plan_row["corpus"],
        "term_id": plan_row["term_id"],
        "concept": plan_row.get("concept", ""),
        "term": hit.get("term", ""),
        "normalized_term": hit.get("normalized_term", ""),
        "skip": hit.get("skip", ""),
        "direction": hit.get("direction", ""),
        "span_letters": hit.get("span_letters", ""),
        "start_ref": hit.get("start_ref", ""),
        "center_ref": hit.get("center_ref", ""),
        "end_ref": hit.get("end_ref", ""),
        "center_word": hit.get("center_word", ""),
        "center_normalized_word": hit.get("center_normalized_word", ""),
    }


def write_report(
    path: Path,
    plan_rows: list[dict[str, str]],
    partition_rows: list[dict[str, str]],
    term_rows: list[dict[str, str]],
    examples: list[dict[str, str]],
    args: argparse.Namespace,
    cache_stats: dict[str, int],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exported_hits = sum(int(row["exported_hits"]) for row in partition_rows)
    exact_hits = sum_int_cells_or_not_computed(row["exact_center_word_hits"] for row in partition_rows)
    completed_terms = [row for row in term_rows if row["coverage_status"] == "complete"]
    partial_terms = [row for row in term_rows if row["coverage_status"] == "partial"]
    lines = [
        f"# {report_title(args.report)}",
        "",
        *report_intro_lines(args.report),
        "This report summarizes completed dense full-span partition outputs.",
        "It is additive to the manageable-row export: a dense row becomes",
        "complete when all planned partition outputs exist and summarize.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Scope",
        "",
        f"- planned partitions: {len(plan_rows):,}",
        f"- completed partition outputs summarized: {len(partition_rows):,}",
        f"- completed dense rows: {len(completed_terms):,}",
        f"- partial dense rows: {len(partial_terms):,}",
        f"- exported partition hit rows summarized: {exported_hits:,}",
        f"- exact center-word hits in completed partitions: {format_count_cell(exact_hits)}",
        f"- partition summary CSV: `{display_path(args.partition_summary)}`",
        f"- term summary CSV: `{display_path(args.term_summary)}`",
        f"- examples CSV: `{display_path(args.examples)}`",
        "",
        "## Completed Dense Rows",
        "",
        "| Corpus | Term | Hits | Exact center-word hits |",
        "| --- | --- | ---: | ---: |",
    ]
    for row in completed_terms:
        lines.append(
            f"| {row['corpus']} | {cell(display_term_cell(row))} | "
            f"{int(row['completed_exported_hits']):,} | {format_count_cell(row['exact_center_word_hits'])} |"
        )
    lines.extend(
        [
            "",
            "## Partial Dense Rows",
            "",
            "| Corpus | Term | Completed partitions | Hits so far | Skip ranges |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in partial_terms[:25]:
        lines.append(
            f"| {row['corpus']} | {cell(display_term_cell(row))} | "
            f"{row['completed_partitions']}/{row['planned_partitions']} | "
            f"{int(row['completed_exported_hits']):,} | {row['completed_skip_ranges']} |"
        )
    lines.extend(
        [
            "",
            "## Completed Partitions",
            "",
            "| Partition | Exported hits | Estimated hits | Delta | Exact center-word hits |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in sorted(partition_rows, key=lambda item: (item["corpus"], item["term_id"], int(item["partition_index"])))[:50]:
        lines.append(
            f"| `{row['partition_id']}` | {int(row['exported_hits']):,} | "
            f"{int(row['estimated_partition_hits']):,} | {int(row['estimate_delta']):,} | "
            f"{format_count_cell(row['exact_center_word_hits'])} |"
        )
    lines.extend(
        [
            "",
            "## Example Hits",
            "",
            "| Type | Corpus | Term | Skip | Center | Center word |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in examples[:30]:
        lines.append(
            f"| `{row['example_type']}` | {row['corpus']} | {cell(display_term_cell(row))} | "
            f"{row['skip']} | {row['center_ref']} | {cell(display_center_word(row))} |"
        )
    lines.extend(exact_center_followup_lines(args, exact_hits))
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Completed partition rows are no longer deferred; their hit-level metadata exists.",
            "- Exact center-word hits are flags, not the admission rule.",
            "- `not_computed` means the manifest-only path was used; hit counts still come from export manifests.",
            "- Partition estimates are planning estimates; exported hit rows are observed counts.",
            "- The ignored partition CSVs are reproducible from the tracked plan and runner.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def exact_center_followup_lines(args: argparse.Namespace, exact_hits: int | str) -> list[str]:
    if not (args.manifest_only or exact_hits == "not_computed"):
        return []
    followups = [
        ROOT / "docs/DYNAMIC_SKIP_FULL_SPAN_HIT_FINDINGS.md",
        ROOT / "docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_FINDINGS.md",
        ROOT / "docs/DYNAMIC_SKIP_STRONG_CONTROL_FULL_SPAN_EXACT_CENTER_FINDINGS.md",
        ROOT / "docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ORIGINAL_LANGUAGE_FINDINGS.md",
    ]
    lines = [
        "",
        "## Targeted Exact-Center Follow-Ups",
        "",
        "This broad summary used manifest-only mode, so it preserves the full",
        "partition completion and hit-count totals without rescanning archived dense",
        "hit payloads for center-word metadata. `not_computed` in this report means",
        "center-word metadata was not scanned here; it does not mean exact-center",
        "hits are absent.",
        "",
        "| Follow-up | Purpose |",
        "| --- | --- |",
    ]
    descriptions = {
        "DYNAMIC_SKIP_FULL_SPAN_HIT_FINDINGS.md": "manageable full-span hit summary with exact-center examples",
        "DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_FINDINGS.md": "Bible rows where strong full-span signals were rescanned for exact centers",
        "DYNAMIC_SKIP_STRONG_CONTROL_FULL_SPAN_EXACT_CENTER_FINDINGS.md": (
            "language-matched control rows corresponding to strong Bible exact-center rows"
        ),
        "DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ORIGINAL_LANGUAGE_FINDINGS.md": (
            "original-language synthesis of promoted, hold, and background exact-center rows"
        ),
    }
    for path in followups:
        label = path.name
        lines.append(f"| `{display_path(path)}` | {descriptions[label]} |")
    return lines


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    plan_rows: list[dict[str, str]],
    partition_rows: list[dict[str, str]],
    term_rows: list[dict[str, str]],
    examples: list[dict[str, str]],
    cache_stats: dict[str, int],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "script": "scripts/summarize_dynamic_span_partition_outputs.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "plan": display_path(args.plan),
        "planned_partitions": len(plan_rows),
        "completed_partition_outputs": len(partition_rows),
        "term_summary_rows": len(term_rows),
        "example_rows": len(examples),
        "partition_summary": display_path(args.partition_summary),
        "term_summary": display_path(args.term_summary),
        "examples": display_path(args.examples),
        "report": display_path(args.report),
        "summary_cache": display_path(args.summary_cache),
        "cache_enabled": not args.no_cache,
        "cache_only": args.cache_only,
        "manifest_only": args.manifest_only,
        "cache_hits": cache_stats["hits"],
        "cache_misses": cache_stats["misses"],
        "cache_entries": cache_stats["entries"],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reproduce_command(args: argparse.Namespace) -> str:
    command = ["python3 -m scripts.summarize_dynamic_span_partition_outputs"]
    if args.plan != DEFAULT_PLAN:
        command.append(f"--plan {display_path(args.plan)}")
    if args.cache_only:
        command.append("--cache-only")
    if args.manifest_only:
        command.append("--manifest-only")
    if args.no_cache:
        command.append("--no-cache")
    if args.examples_per_partition != 3:
        command.append(f"--examples-per-partition {args.examples_per_partition}")
    return " ".join(command)


def report_title(path: Path) -> str:
    titles = {
        "DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_FINDINGS.md": "Strong Full-Span Exact-Center Findings",
        "DYNAMIC_SKIP_STRONG_CONTROL_FULL_SPAN_EXACT_CENTER_FINDINGS.md": (
            "Strong Control Full-Span Exact-Center Findings"
        ),
    }
    return titles.get(path.name, "Dynamic Full-Span Partition Findings")


def report_intro_lines(path: Path) -> list[str]:
    intros = {
        "DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_FINDINGS.md": [
            "This targeted follow-up scans archived dense hit payloads for the",
            "full-span rows whose Bible max normalized rate exceeded all observed",
            "language-matched controls. It is not a new search; it summarizes hit-level",
            "metadata from already-completed partition exports.",
            "",
        ],
        "DYNAMIC_SKIP_STRONG_CONTROL_FULL_SPAN_EXACT_CENTER_FINDINGS.md": [
            "This targeted control follow-up scans archived dense hit payloads for the",
            "language-matched control-max rows corresponding to strong Bible full-span rows",
            "with exact center-word hits.",
            "",
        ],
    }
    return intros.get(path.name, [])


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def display_term_cell(row: dict[str, str]) -> str:
    term_id = row.get("term_id", "")
    term = row.get("term") or row.get("normalized_term") or ""
    if not term:
        return f"`{term_id}`" if term_id else ""
    label = display_term(term, english=row.get("concept") or None)
    return f"{label}<br>`{term_id}`" if term_id else label


def display_center_word(row: dict[str, str]) -> str:
    word = row.get("center_word", "")
    if not (contains_hebrew(word) or contains_greek(word)):
        return word
    english = row.get("concept", "") if row.get("center_normalized_word") == row.get("normalized_term") else ""
    return display_term(word, english=english or None)


def cell(value: str) -> str:
    return value.replace("|", "\\|") if value else ""


def load_summary_cache(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(payload, dict):
        return {}
    if payload.get("cache_version") != CACHE_VERSION:
        return {}
    entries = payload.get("entries")
    return entries if isinstance(entries, dict) else {}


def write_summary_cache(path: Path, cache: dict[str, dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "cache_version": CACHE_VERSION,
        "created_at": datetime.now(UTC).isoformat(),
        "entries": cache,
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def partition_fingerprint(
    row: dict[str, str],
    examples_per_partition: int,
    *,
    manifest_only: bool = False,
) -> dict[str, int | str | bool]:
    out = partition_output_path(row)
    manifest = partition_manifest_path(row)
    manifest_stat = manifest.stat()
    marker = archive_marker_path(row)
    marker_stat = marker.stat() if marker.exists() else None
    fingerprint: dict[str, int | str | bool] = {
        "cache_version": CACHE_VERSION,
        "examples_per_partition": examples_per_partition,
        "manifest_only": manifest_only,
        "out": display_path(out),
        "manifest": display_path(manifest),
        "manifest_size": manifest_stat.st_size,
        "manifest_mtime_ns": manifest_stat.st_mtime_ns,
        "archive_marker": display_path(marker) if marker.exists() else "",
        "archive_marker_size": marker_stat.st_size if marker_stat else 0,
        "archive_marker_mtime_ns": marker_stat.st_mtime_ns if marker_stat else 0,
    }
    if out.exists():
        out_stat = out.stat()
        fingerprint.update(
            {
                "out_size": out_stat.st_size,
                "out_mtime_ns": out_stat.st_mtime_ns,
            }
        )
    elif not manifest_only:
        out.stat()
    return fingerprint


def partition_output_path(row: dict[str, str]) -> Path:
    out = Path(row["out"])
    path = out if out.is_absolute() else ROOT / out
    if path.exists():
        return path
    gz_path = path.with_suffix(path.suffix + ".gz")
    if gz_path.exists():
        return gz_path
    archived_path = archived_partition_output_path(row)
    if archived_path is not None and archived_path.exists():
        return archived_path
    return path


def compressed_partition_output_path(row: dict[str, str]) -> Path:
    out = Path(row["out"])
    path = out if out.is_absolute() else ROOT / out
    return path.with_suffix(path.suffix + ".gz")


def archived_partition_output_path(row: dict[str, str]) -> Path | None:
    marker = archive_marker_path(row)
    if not marker.exists():
        return None
    try:
        payload = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    archive_path = payload.get("archive_path")
    if not isinstance(archive_path, str) or not archive_path:
        return None
    return Path(archive_path)


def archive_marker_path(row: dict[str, str]) -> Path:
    gz_out = compressed_partition_output_path(row)
    return gz_out.with_suffix(gz_out.suffix + ".archived.json")


def open_partition_output(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return path.open("r", encoding="utf-8", newline="")


def partition_manifest_path(row: dict[str, str]) -> Path:
    manifest = Path(row["manifest_out"])
    return manifest if manifest.is_absolute() else ROOT / manifest


def format_counter(counter: Counter[str], limit: int) -> str:
    return "; ".join(f"{key}={count}" for key, count in counter.most_common(limit) if key)


def sum_int_cells_or_not_computed(values: Iterable[str]) -> int | str:
    total = 0
    for value in values:
        try:
            total += int(value)
        except (TypeError, ValueError):
            return "not_computed"
    return total


def format_count_cell(value: int | str) -> str:
    if isinstance(value, int):
        return f"{value:,}"
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def example_sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    return (abs(int(row["skip"] or 0)), int(row["span_letters"] or 0), row["center_ref"])


def cell(value: str) -> str:
    return value.replace("|", "\\|") if value else ""


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
