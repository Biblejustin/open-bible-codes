#!/usr/bin/env python3
"""Select a compact follow-up set from all-codes triage queues."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from scripts.triage_surface_all_codes import BUCKET_ORDER, QUEUE_FIELDNAMES, int_or_zero


DEFAULT_QUEUES = [
    "hebrew_theology=reports/hebrew_theology_all_codes/triage_queue.csv",
    "hebrew_screening=reports/hebrew_screening_all_codes/triage_queue.csv",
    "greek_screening=reports/greek_screening_all_codes/triage_queue.csv",
]
OUT_DIR = Path("reports/all_codes_followup_selection")
SELECTED_OUT = OUT_DIR / "selected_rows.csv"
MD_OUT = Path("docs/ALL_CODES_FOLLOWUP_SELECTION.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"

SELECTED_FIELDNAMES = [
    "selection_rank",
    "source_queue",
    "selection_reason",
    *QUEUE_FIELDNAMES,
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    queue_paths = parse_queue_args(args.queue or DEFAULT_QUEUES)
    queue_rows = read_queue_rows(queue_paths)
    selected_rows = select_rows(
        queue_rows,
        max_rows_per_queue=args.max_rows_per_queue,
        max_rows_per_bucket=args.max_rows_per_bucket,
        max_rows_per_term=args.max_rows_per_term,
    )
    write_rows(args.selected_out, selected_rows)
    write_markdown(args.markdown_out, args, queue_paths, queue_rows, selected_rows)
    write_manifest(args, queue_paths, queue_rows, selected_rows, started)
    print(args.selected_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", action="append", default=[])
    parser.add_argument("--max-rows-per-queue", type=int, default=30)
    parser.add_argument("--max-rows-per-bucket", type=int, default=3)
    parser.add_argument("--max-rows-per-term", type=int, default=2)
    parser.add_argument("--title", default="All-Codes Follow-Up Selection")
    parser.add_argument("--selected-out", type=Path, default=SELECTED_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def parse_queue_args(values: list[str]) -> dict[str, Path]:
    parsed: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected LABEL=PATH for --queue, got {value!r}")
        label, path = value.split("=", 1)
        parsed[label] = Path(path)
    return parsed


def read_queue_rows(queue_paths: dict[str, Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for label, path in queue_paths.items():
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                row = dict(row)
                row["source_queue"] = label
                rows.append(row)
    return rows


def select_rows(
    rows: list[dict[str, str]],
    *,
    max_rows_per_queue: int,
    max_rows_per_bucket: int,
    max_rows_per_term: int,
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    seen_patterns: set[tuple[str, ...]] = set()
    rows_by_queue = group_by(rows, "source_queue")
    for queue in sorted(rows_by_queue):
        selected_for_queue = select_queue_rows(
            rows_by_queue[queue],
            max_rows_per_queue=max_rows_per_queue,
            max_rows_per_bucket=max_rows_per_bucket,
            max_rows_per_term=max_rows_per_term,
            seen_patterns=seen_patterns,
        )
        selected.extend(selected_for_queue)
    for rank, row in enumerate(selected, start=1):
        row["selection_rank"] = str(rank)
    return selected


def select_queue_rows(
    rows: list[dict[str, str]],
    *,
    max_rows_per_queue: int,
    max_rows_per_bucket: int,
    max_rows_per_term: int,
    seen_patterns: set[tuple[str, ...]],
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    per_bucket: Counter[str] = Counter()
    per_term: Counter[str] = Counter()
    by_bucket = group_by(rows, "bucket")
    for bucket in sorted(BUCKET_ORDER, key=BUCKET_ORDER.get):
        bucket_rows = sorted(by_bucket.get(bucket, []), key=queue_sort_key)
        for source in bucket_rows:
            if len(selected) >= max_rows_per_queue:
                return selected
            if per_bucket[bucket] >= max_rows_per_bucket:
                break
            term_id = source.get("term_id", "")
            if per_term[term_id] >= max_rows_per_term:
                continue
            key = pattern_key(source)
            if key in seen_patterns:
                continue
            row = selected_row(source)
            row["selection_reason"] = (
                f"bucket={bucket}; scope={source.get('presence_scope', '')}; "
                f"bucket_rank={source.get('bucket_rank', '')}; caps="
                f"{per_bucket[bucket] + 1}/{max_rows_per_bucket},"
                f"{per_term[term_id] + 1}/{max_rows_per_term}"
            )
            selected.append(row)
            seen_patterns.add(key)
            per_bucket[bucket] += 1
            per_term[term_id] += 1
    return selected


def selected_row(source: dict[str, str]) -> dict[str, str]:
    row = {field: source.get(field, "") for field in SELECTED_FIELDNAMES}
    row["source_queue"] = source.get("source_queue", "")
    return row


def queue_sort_key(row: dict[str, str]) -> tuple[Any, ...]:
    return (
        scope_rank(row.get("presence_scope", "")),
        int_or_zero(row.get("bucket_rank", "")),
        int_or_zero(row.get("overall_rank", "")),
        abs(int_or_zero(row.get("skip", ""))),
        int_or_zero(row.get("span_letters", "")),
        row.get("term_id", ""),
    )


def scope_rank(value: str) -> int:
    return {"all_source": 0, "multi_source": 1, "source_specific": 2}.get(value, 3)


def pattern_key(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row.get("term_id", ""),
        row.get("normalized_term", ""),
        row.get("skip", ""),
        row.get("direction", ""),
        row.get("start_ref", ""),
        row.get("center_ref", ""),
        row.get("end_ref", ""),
    )


def group_by(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get(field, "")].append(row)
    return grouped


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SELECTED_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    args: argparse.Namespace,
    queue_paths: dict[str, Path],
    queue_rows: list[dict[str, str]],
    selected_rows: list[dict[str, str]],
) -> None:
    queue_counts = Counter(row["source_queue"] for row in queue_rows)
    selected_queue_counts = Counter(row["source_queue"] for row in selected_rows)
    selected_bucket_counts = Counter(row["bucket"] for row in selected_rows)
    lines = [
        f"# {args.title}",
        "",
        "Status: compact post-screen review selection, not a claim.",
        "",
        "This narrows the relaxed all-codes triage queues into a small manual-review",
        "set. It keeps hidden-path-only rows eligible while ranking rows from same",
        "center-word, related center-word, center-verse, and span-context buckets first.",
        "",
        "## Inputs",
        "",
    ]
    for label, path_value in queue_paths.items():
        lines.append(f"- `{label}`: `{path_value}`")
    lines.extend(
        [
            "",
            "## Selection Rule",
            "",
            f"- max rows per queue: {args.max_rows_per_queue}",
            f"- max rows per bucket: {args.max_rows_per_bucket}",
            f"- max rows per term: {args.max_rows_per_term}",
            "- prefer all-source rows, then multi-source, then source-specific rows;",
            "- deduplicate exact term/skip/ref keys across source queues;",
            "- do not require an open-text surface echo; hidden-path-only rows remain eligible.",
            "",
            "## Counts",
            "",
            "| Queue | Queue rows | Selected rows |",
            "| --- | ---: | ---: |",
        ]
    )
    for label in sorted(queue_paths):
        lines.append(
            f"| {label} | {queue_counts[label]:,} | {selected_queue_counts[label]:,} |"
        )
    lines.extend(
        [
            "",
            "| Selected bucket | Rows |",
            "| --- | ---: |",
        ]
    )
    for bucket in sorted(BUCKET_ORDER, key=BUCKET_ORDER.get):
        if selected_bucket_counts[bucket]:
            lines.append(f"| `{bucket}` | {selected_bucket_counts[bucket]:,} |")
    lines.extend(
        [
            "",
            "## Selected Rows",
            "",
            "| Rank | Queue | Bucket | Scope | Term | Concept | Skip | Center | Center word |",
            "| ---: | --- | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in selected_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["selection_rank"],
                    row["source_queue"],
                    f"`{row['bucket']}`",
                    row["presence_scope"],
                    f"`{row['term_id']}`",
                    row["concept"],
                    row["skip"],
                    row["center_ref"],
                    f"`{row['center_normalized_word']}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "This is a work queue. Rows here should receive letter-path and surface",
            "context review next. Statistical status remains inherited from the source",
            "triage/control columns; this selector does not add significance.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    queue_paths: dict[str, Path],
    queue_rows: list[dict[str, str]],
    selected_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "select_all_codes_followup",
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "git_commit": run_git("rev-parse", "--short", "HEAD"),
        "queues": {label: str(path) for label, path in queue_paths.items()},
        "queue_rows": len(queue_rows),
        "selected_rows": len(selected_rows),
        "max_rows_per_queue": args.max_rows_per_queue,
        "max_rows_per_bucket": args.max_rows_per_bucket,
        "max_rows_per_term": args.max_rows_per_term,
        "selected_by_queue": dict(Counter(row["source_queue"] for row in selected_rows)),
        "selected_by_bucket": dict(Counter(row["bucket"] for row in selected_rows)),
        "outputs": [
            str(args.selected_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def run_git(*args: str) -> str:
    completed = subprocess.run(["git", *args], check=False, capture_output=True, text=True)
    return completed.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
