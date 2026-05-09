#!/usr/bin/env python3
"""Export exact-center rows from dynamic-span partition or hit outputs."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from els import __version__
from scripts.export_dynamic_span_hits import ROOT
from scripts.summarize_dynamic_span_partition_outputs import (
    completed_plan_rows,
    display_path,
    open_partition_output,
    partition_output_path,
)


DEFAULT_OUT = ROOT / "reports/dynamic_skip_focus/exact_center_rows.csv"
DEFAULT_SUMMARY = ROOT / "reports/dynamic_skip_focus/exact_center_rows_summary.csv"
DEFAULT_MARKDOWN = ROOT / "docs/DYNAMIC_SKIP_EXACT_CENTER_ROWS.md"
DEFAULT_MANIFEST = ROOT / "reports/dynamic_skip_focus/exact_center_rows.manifest.json"

EXACT_FIELDNAMES = [
    "source_kind",
    "source_path",
    "partition_id",
    "corpus",
    "term_id",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "span_letters",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "center_normalized_word",
    "start_offset",
    "center_offset",
    "end_offset",
]

SUMMARY_FIELDNAMES = [
    "corpus",
    "term_id",
    "normalized_term",
    "source_kind",
    "source_items",
    "scanned_hit_rows",
    "exact_center_rows",
    "exact_center_rows_per_million_hits",
    "distinct_center_refs",
    "top_center_refs",
    "top_center_words",
]


class SummaryAccumulator:
    def __init__(self, corpus: str, term_id: str, normalized_term: str, source_kind: str) -> None:
        self.corpus = corpus
        self.term_id = term_id
        self.normalized_term = normalized_term
        self.source_kind = source_kind
        self.source_items = 0
        self.scanned_hit_rows = 0
        self.exact_center_rows = 0
        self.center_refs: Counter[str] = Counter()
        self.center_words: Counter[str] = Counter()

    def add_source(self) -> None:
        self.source_items += 1

    def add_hit(self, hit: dict[str, str], *, exact: bool) -> None:
        self.scanned_hit_rows += 1
        if not exact:
            return
        self.exact_center_rows += 1
        center_ref = hit.get("center_ref", "")
        center_word = hit.get("center_word", "")
        if center_ref:
            self.center_refs[center_ref] += 1
        if center_word:
            self.center_words[center_word] += 1

    def to_row(self) -> dict[str, str]:
        rate = 0.0
        if self.scanned_hit_rows:
            rate = 1_000_000 * self.exact_center_rows / self.scanned_hit_rows
        return {
            "corpus": self.corpus,
            "term_id": self.term_id,
            "normalized_term": self.normalized_term,
            "source_kind": self.source_kind,
            "source_items": str(self.source_items),
            "scanned_hit_rows": str(self.scanned_hit_rows),
            "exact_center_rows": str(self.exact_center_rows),
            "exact_center_rows_per_million_hits": str(round(rate, 6)),
            "distinct_center_refs": str(len(self.center_refs)),
            "top_center_refs": format_counter(self.center_refs, 10),
            "top_center_words": format_counter(self.center_words, 10),
        }


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    export_result = export_exact_center_rows(args.plan, args.hit_file, args.out)
    summary_rows = sorted(
        (accumulator.to_row() for accumulator in export_result["summaries"].values()),
        key=lambda row: (-int(row["exact_center_rows"]), row["corpus"], row["term_id"], row["source_kind"]),
    )
    write_csv(args.summary, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, summary_rows, args, export_result)
    write_manifest(args.manifest_out, args, summary_rows, export_result, started)
    print(args.out)
    print(args.summary)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, action="append", default=[])
    parser.add_argument("--hit-file", type=Path, action="append", default=[])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def export_exact_center_rows(plan_paths: list[Path], hit_files: list[Path], out: Path) -> dict[str, Any]:
    summaries: dict[tuple[str, str, str, str], SummaryAccumulator] = {}
    totals = {
        "plan_files": len(plan_paths),
        "hit_files": len(hit_files),
        "partition_sources": 0,
        "hit_file_sources": 0,
        "scanned_hit_rows": 0,
        "exact_center_rows": 0,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXACT_FIELDNAMES)
        writer.writeheader()
        for plan_path in plan_paths:
            plan_rows = completed_plan_rows(read_rows(plan_path))
            for row in plan_rows:
                totals["partition_sources"] += 1
                scan_partition(row, writer, summaries, totals)
        for hit_file in hit_files:
            totals["hit_file_sources"] += 1
            scan_hit_file(hit_file, writer, summaries, totals)
    return {"summaries": summaries, "totals": totals}


def scan_partition(
    plan_row: dict[str, str],
    writer: csv.DictWriter,
    summaries: dict[tuple[str, str, str, str], SummaryAccumulator],
    totals: dict[str, int],
) -> None:
    path = partition_output_path(plan_row)
    with open_partition_output(path) as handle:
        reader = csv.DictReader(handle)
        source_added = False
        for hit in reader:
            accumulator = summary_for(hit, summaries, "partition")
            if not source_added:
                accumulator.add_source()
                source_added = True
            exact = is_exact_center_word(hit)
            accumulator.add_hit(hit, exact=exact)
            totals["scanned_hit_rows"] += 1
            if exact:
                totals["exact_center_rows"] += 1
                writer.writerow(exact_row("partition", path, plan_row.get("partition_id", ""), hit))


def scan_hit_file(
    hit_file: Path,
    writer: csv.DictWriter,
    summaries: dict[tuple[str, str, str, str], SummaryAccumulator],
    totals: dict[str, int],
) -> None:
    with hit_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        seen_sources: set[tuple[str, str, str]] = set()
        for hit in reader:
            accumulator = summary_for(hit, summaries, "hit_file")
            source_key = (hit.get("corpus", ""), hit.get("term_id", ""), hit.get("normalized_term", ""))
            if source_key not in seen_sources:
                seen_sources.add(source_key)
                accumulator.add_source()
            exact = is_exact_center_word(hit)
            accumulator.add_hit(hit, exact=exact)
            totals["scanned_hit_rows"] += 1
            if exact:
                totals["exact_center_rows"] += 1
                writer.writerow(exact_row("hit_file", hit_file, "", hit))


def summary_for(
    hit: dict[str, str],
    summaries: dict[tuple[str, str, str, str], SummaryAccumulator],
    source_kind: str,
) -> SummaryAccumulator:
    key = (
        hit.get("corpus", ""),
        hit.get("term_id", ""),
        hit.get("normalized_term", ""),
        source_kind,
    )
    if key not in summaries:
        summaries[key] = SummaryAccumulator(*key)
    return summaries[key]


def is_exact_center_word(hit: dict[str, str]) -> bool:
    normalized_term = hit.get("normalized_term", "")
    return bool(normalized_term and hit.get("center_normalized_word", "") == normalized_term)


def exact_row(source_kind: str, source_path: Path, partition_id: str, hit: dict[str, str]) -> dict[str, str]:
    return {
        "source_kind": source_kind,
        "source_path": display_path(source_path),
        "partition_id": partition_id,
        "corpus": hit.get("corpus", ""),
        "term_id": hit.get("term_id", ""),
        "term": hit.get("term", ""),
        "normalized_term": hit.get("normalized_term", ""),
        "skip": hit.get("skip", ""),
        "direction": hit.get("direction", ""),
        "span_letters": hit.get("span_letters", ""),
        "start_ref": hit.get("start_ref", ""),
        "center_ref": hit.get("center_ref", ""),
        "end_ref": hit.get("end_ref", ""),
        "center_source": hit.get("center_source", ""),
        "center_word_index": hit.get("center_word_index", ""),
        "center_word": hit.get("center_word", ""),
        "center_normalized_word": hit.get("center_normalized_word", ""),
        "start_offset": hit.get("start_offset", ""),
        "center_offset": hit.get("center_offset", ""),
        "end_offset": hit.get("end_offset", ""),
    }


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    args: argparse.Namespace,
    export_result: dict[str, Any],
) -> None:
    totals = export_result["totals"]
    lines = [
        "# Dynamic Skip Exact-Center Rows",
        "",
        "This report exports only hit rows where the normalized hidden term exactly",
        "matches the normalized surface word at the ELS center.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Scope",
        "",
        f"- plan files: {totals['plan_files']:,}",
        f"- hit files: {totals['hit_files']:,}",
        f"- partition sources scanned: {totals['partition_sources']:,}",
        f"- hit-file sources scanned: {totals['hit_file_sources']:,}",
        f"- scanned hit rows: {totals['scanned_hit_rows']:,}",
        f"- exact-center rows exported: {totals['exact_center_rows']:,}",
        f"- exact row CSV: `{display_path(args.out)}`",
        f"- summary CSV: `{display_path(args.summary)}`",
        "",
        "## Term Summary",
        "",
        "| Corpus | Term | Source | Hits scanned | Exact center | Exact perM | Top center refs |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['corpus']} | `{row['term_id']}` | `{row['source_kind']}` | "
            f"{int(row['scanned_hit_rows']):,} | {int(row['exact_center_rows']):,} | "
            f"{float(row['exact_center_rows_per_million_hits']):,.6f} | {row['top_center_refs']} |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Exact-center rows are review flags, not claim evidence by themselves.",
            "- A high exact-center rate can reflect ordinary surface vocabulary in the corpus.",
            "- Use this with language-matched controls and version/source distribution.",
            "- Non-Bible controls can use source-level center refs; use `center_source`, `center_word_index`, and offsets in the row CSV for exact local traceability.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def reproduce_command(args: argparse.Namespace) -> str:
    parts = ["python3 -m scripts.export_dynamic_span_exact_center_rows"]
    for plan in args.plan:
        parts.extend(["--plan", display_path(plan)])
    for hit_file in args.hit_file:
        parts.extend(["--hit-file", display_path(hit_file)])
    parts.extend(["--out", display_path(args.out)])
    parts.extend(["--summary", display_path(args.summary)])
    parts.extend(["--markdown-out", display_path(args.markdown_out)])
    return " ".join(parts)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    export_result: dict[str, Any],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "script": "scripts/export_dynamic_span_exact_center_rows.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "plans": [display_path(path) for path in args.plan],
        "hit_files": [display_path(path) for path in args.hit_file],
        "out": display_path(args.out),
        "summary": display_path(args.summary),
        "markdown_out": display_path(args.markdown_out),
        "summary_rows": len(rows),
        "totals": export_result["totals"],
        "git_commit": git_commit(),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def format_counter(counter: Counter[str], limit: int) -> str:
    return "; ".join(f"{key}={count}" for key, count in counter.most_common(limit) if key)


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
