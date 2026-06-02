#!/usr/bin/env python3
"""Build Bible-vs-control findings from a broad count sweep."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import subprocess
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.statistics import estimated_search_space, hits_per_million
from els.term_display import display_term
from scripts.analyze_broad_search import find_run_manifest, read_count_rows
from scripts.json_utils import read_json_object


COUNTS_DIR = Path("reports/windows_cpu/broad_2_500")
OUT = Path("reports/windows_cpu/broad_2_500/bible_control_comparison.csv")
MARKDOWN_OUT = Path("docs/WINDOWS_CPU_BROAD_2_500_FINDINGS.md")
MANIFEST_OUT = Path("reports/windows_cpu/broad_2_500/bible_control_comparison.manifest.json")
CALIBRATION_TERM_SETS = {"frequency_anchors", "null_controls"}

FIELDNAMES = [
    "term_set",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term_display",
    "normalized_term",
    "normalized_length",
    "bible_rows",
    "control_rows",
    "bible_present_rows",
    "control_present_rows",
    "bible_max_corpus",
    "bible_max_hit_count",
    "bible_max_rate_per_million",
    "control_max_corpus",
    "control_max_hit_count",
    "control_max_rate_per_million",
    "control_median_rate_per_million",
    "bible_over_control_max_rate_ratio",
    "bible_over_control_median_rate_ratio",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    manifest_path = find_run_manifest(args.counts_dir)
    manifest = read_json(manifest_path)
    corpus_meta = corpus_metadata(manifest)
    count_rows = read_count_rows(args.counts_dir)
    comparison_rows = compare_rows(count_rows, corpus_meta, manifest)
    write_csv(args.out, comparison_rows)
    write_markdown(args.markdown_out, comparison_rows, args, manifest, manifest_path)
    write_manifest(args.manifest_out, args, manifest_path, comparison_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts-dir", type=Path, default=COUNTS_DIR)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--markdown-out", type=Path, default=MARKDOWN_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    parser.add_argument("--title", default="Windows CPU Broad Skip 2..500 Bible-Control Findings")
    parser.add_argument("--min-display-length", type=int, default=4)
    parser.add_argument("--low-count-threshold", type=int, default=10)
    return parser


def corpus_metadata(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(row["label"]): dict(row["summary"]) for row in manifest.get("corpora", [])}


def compare_rows(
    rows: list[dict[str, str]],
    corpus_meta: dict[str, dict[str, Any]],
    manifest: dict[str, Any],
) -> list[dict[str, str]]:
    enriched = [
        enrich_count_row(row, corpus_meta, manifest)
        for row in rows
        if row.get("status") == "counted" and row.get("corpus") in corpus_meta
    ]
    grouped: dict[tuple[str, str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in enriched:
        grouped[
            (
                row["term_set"],
                row["term_id"],
                row["concept"],
                row["term_language"],
                row["normalized_term"],
                str(row["normalized_length"]),
            )
        ].append(row)

    output = []
    for _key, group in sorted(grouped.items()):
        bible_rows = [row for row in group if row["corpus_class"] == "bible"]
        control_rows = [row for row in group if row["corpus_class"] == "control"]
        if not bible_rows or not control_rows:
            continue
        bible_max = max(bible_rows, key=rate)
        control_max = max(control_rows, key=rate)
        control_rates = [rate(row) for row in control_rows]
        control_median = statistics.median(control_rates) if control_rates else None
        bible_max_rate = rate(bible_max)
        control_max_rate = rate(control_max)
        row0 = group[0]
        output.append(
            {
                "term_set": row0["term_set"],
                "term_id": row0["term_id"],
                "concept": row0["concept"],
                "category": row0["category"],
                "term_language": row0["term_language"],
                "term_display": display_term(row0["normalized_term"], english=row0["concept"]),
                "normalized_term": row0["normalized_term"],
                "normalized_length": str(row0["normalized_length"]),
                "bible_rows": str(len(bible_rows)),
                "control_rows": str(len(control_rows)),
                "bible_present_rows": str(sum(hit_count(row) > 0 for row in bible_rows)),
                "control_present_rows": str(sum(hit_count(row) > 0 for row in control_rows)),
                "bible_max_corpus": bible_max["corpus"],
                "bible_max_hit_count": str(hit_count(bible_max)),
                "bible_max_rate_per_million": str(hits_per_million(hit_count(bible_max), bible_max["search_space"])),
                "control_max_corpus": control_max["corpus"],
                "control_max_hit_count": str(hit_count(control_max)),
                "control_max_rate_per_million": str(
                    hits_per_million(hit_count(control_max), control_max["search_space"])
                ),
                "control_median_rate_per_million": str(round_float(control_median)),
                "bible_over_control_max_rate_ratio": ratio_text(bible_max_rate, control_max_rate),
                "bible_over_control_median_rate_ratio": ratio_text(bible_max_rate, control_median),
                "read": read_label(bible_max, control_max, control_median),
            }
        )
    return output


def enrich_count_row(
    row: dict[str, str],
    corpus_meta: dict[str, dict[str, Any]],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    copied: dict[str, Any] = dict(row)
    corpus = str(copied["corpus"])
    summary = corpus_meta[corpus]
    copied["corpus_class"] = corpus_class(summary)
    copied["normalized_length"] = int(copied.get("normalized_length") or 0)
    copied["hit_count"] = int(copied.get("hit_count") or 0)
    copied["search_space"] = estimated_search_space(
        int(summary.get("letters") or 0),
        copied["normalized_length"],
        int(copied.get("min_skip") or manifest.get("min_skip") or 2),
        int(copied.get("max_skip") or manifest.get("max_skip") or 100),
        str(copied.get("direction") or manifest.get("direction") or "both"),
    )
    return copied


def corpus_class(summary: dict[str, Any]) -> str:
    name = str(summary.get("name", ""))
    return "control" if name.startswith("Non-Bible ") else "bible"


def hit_count(row: dict[str, Any]) -> int:
    return int(row.get("hit_count") or 0)


def rate(row: dict[str, Any]) -> float:
    search_space = int(row.get("search_space") or 0)
    if search_space <= 0:
        return 0.0
    return hit_count(row) * 1_000_000 / search_space


def ratio_text(numerator: float, denominator: float | None) -> str:
    if denominator is None:
        return ""
    if denominator == 0:
        return "inf" if numerator > 0 else ""
    return str(round_float(numerator / denominator))


def round_float(value: float | None) -> float | str:
    if value is None:
        return ""
    return round(value, 6)


def read_label(
    bible_max: dict[str, Any],
    control_max: dict[str, Any],
    control_median: float | None,
    *,
    low_count_threshold: int = 10,
) -> str:
    bible_rate = rate(bible_max)
    control_rate = rate(control_max)
    if hit_count(bible_max) == 0 and hit_count(control_max) == 0:
        return "absent in Bible and controls at this range"
    if bible_rate > control_rate:
        if hit_count(bible_max) < low_count_threshold:
            return "Bible-over-control low-count queue row"
        return "Bible max rate exceeds all observed controls"
    if control_median is not None and bible_rate > control_median:
        return "Bible max rate exceeds control median but not control max"
    return "control background equals or exceeds Bible max rate"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    args: argparse.Namespace,
    manifest: dict[str, Any],
    manifest_path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    min_length = int(args.min_display_length)
    visible = [row for row in rows if int(row["normalized_length"]) >= min_length]
    strong_original = [
        row
        for row in visible
        if row["read"] == "Bible max rate exceeds all observed controls"
        and int(row["bible_max_hit_count"]) >= int(args.low_count_threshold)
        and row["term_language"] in {"hebrew", "greek"}
        and row["term_set"] not in CALIBRATION_TERM_SETS
    ]
    strong_english = [
        row
        for row in visible
        if row["read"] == "Bible max rate exceeds all observed controls"
        and int(row["bible_max_hit_count"]) >= int(args.low_count_threshold)
        and row["term_language"] == "english"
        and row["term_set"] not in CALIBRATION_TERM_SETS
    ]
    calibration = [
        row
        for row in visible
        if row["read"] == "Bible max rate exceeds all observed controls"
        and int(row["bible_max_hit_count"]) >= int(args.low_count_threshold)
        and row["term_set"] in CALIBRATION_TERM_SETS
    ]
    low_count = [
        row
        for row in visible
        if row["read"] == "Bible-over-control low-count queue row"
        and int(row["control_max_hit_count"]) == 0
        and int(row["bible_max_hit_count"]) > 0
    ]
    control_background = [
        row
        for row in visible
        if row["read"] == "control background equals or exceeds Bible max rate"
        and int(row["control_max_hit_count"]) > 0
    ]
    lines = [
        f"# {args.title}",
        "",
        "This report summarizes the Windows desktop CPU broad count sweep as a",
        "language-matched Bible-vs-control comparison. The raw sweep is retained;",
        "this layer only normalizes by legal ELS search positions and compares each",
        "term against non-Bible corpora in the same language.",
        "",
        "## Scope",
        "",
        f"- Count directory: `{args.counts_dir}`",
        f"- Run manifest: `{manifest_path}`",
        f"- Skip range: `{manifest.get('min_skip', 2)}..{manifest.get('max_skip', 100)}`",
        f"- Direction: `{manifest.get('direction', 'both')}`",
        f"- Term sets: {len(manifest.get('term_sets', []))}",
        f"- Corpora: {len(manifest.get('corpora', []))}",
        f"- Comparison rows: {len(rows)}",
        f"- Display filter in this markdown: normalized length >= {min_length}",
        "",
        "## Main Read",
        "",
        "- Raw high-count rows are dominated by short forms, acronyms, and ordinary language density.",
        "- The comparison CSV keeps all rows; this markdown highlights longer rows first.",
        "- A zero-control row with one or two Bible hits is a queue item, not a claim.",
        "- Null controls can also show favorable ratios; that is a warning against interpreting ratios alone.",
        "- Any favorable row still needs centered-hit context, version distribution, and matched controls.",
        "",
        "## Stronger Original-Language Bible-Over-Control Rows",
        "",
        "| Term | Set | Bible max | Control max | Control median | Ratio vs max | Read |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in distinct_terms(sorted(strong_original, key=ratio_sort_key, reverse=True))[:30]:
        lines.append(comparison_row(row))
    lines.extend(
        [
            "",
            "## English/KJV Secondary Rows",
            "",
            "English rows are useful as translation evidence and as method pressure,",
            "but absence or presence here does not decide the original-language hypothesis.",
            "",
            "| Term | Set | Bible max | Control max | Control median | Ratio vs max | Read |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in distinct_terms(sorted(strong_english, key=ratio_sort_key, reverse=True))[:20]:
        lines.append(comparison_row(row))
    lines.extend(
        [
            "",
            "## Calibration Rows That Also Exceed Controls",
            "",
            "These are not claim rows. They show why favorable Bible/control ratios",
            "still need centered context, source sensitivity, and matched controls.",
            "",
            "| Term | Set | Bible max | Control max | Control median | Ratio vs max | Read |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in distinct_terms(sorted(calibration, key=ratio_sort_key, reverse=True))[:15]:
        lines.append(comparison_row(row))
    lines.extend(
        [
            "",
            "## Bible-Only Low-Count Queue Rows",
            "",
            "These rows have at least one Bible hit and zero observed language-matched",
            "control hits in this broad count sweep, but the absolute Bible count is",
            "below the low-count threshold.",
            "",
            "| Term | Set | Bible corpus | Bible hits | Bible rate | Read |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in distinct_terms(sorted(low_count, key=low_count_sort_key))[:30]:
        lines.append(
            "| "
            + " | ".join(
                [
                    term_cell(row),
                    row["term_set"],
                    row["bible_max_corpus"],
                    row["bible_max_hit_count"],
                    row["bible_max_rate_per_million"],
                    row["read"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Control-Background Rows",
            "",
            "These rows are useful negative pressure: language-matched controls meet or",
            "exceed the best Bible rate in this broad count sweep.",
            "",
            "| Term | Set | Bible max | Control max | Control median | Ratio vs max | Read |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in distinct_terms(sorted(control_background, key=ratio_sort_key))[:30]:
        lines.append(comparison_row(row))
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- comparison CSV: `{args.out}`",
            f"- manifest: `{args.manifest_out}`",
            "",
            "## Caution",
            "",
            "This is still a broad count layer. It does not say that a hit is centered",
            "on a relevant surface word, and it does not inspect the letter path. Use it",
            "to select rows for centered/contextual review, not as final evidence.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def comparison_row(row: dict[str, str]) -> str:
    return (
        f"| {term_cell(row)} | {row['term_set']} "
        f"| {row['bible_max_rate_per_million']} ({row['bible_max_corpus']}) "
        f"| {row['control_max_rate_per_million']} ({row['control_max_corpus']}) "
        f"| {row['control_median_rate_per_million']} "
        f"| {row['bible_over_control_max_rate_ratio']} | {row['read']} |"
    )


def term_cell(row: dict[str, str]) -> str:
    return f"`{row['term_id']}` {row['term_display']}"


def distinct_terms(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen = set()
    output = []
    for row in rows:
        key = (row["term_language"], row["normalized_term"], row["concept"])
        if key in seen:
            continue
        seen.add(key)
        output.append(row)
    return output


def ratio_sort_key(row: dict[str, str]) -> float:
    value = row["bible_over_control_max_rate_ratio"]
    if value == "inf":
        return math.inf
    if not value:
        return 0.0
    return float(value)


def low_count_sort_key(row: dict[str, str]) -> tuple[int, str]:
    return (-int(row["bible_max_hit_count"]), row["term_id"])


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    run_manifest: Path,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "script": "scripts/build_broad_bible_control_findings.py",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "counts_dir": str(args.counts_dir),
        "run_manifest": str(run_manifest),
        "comparison_rows": len(rows),
        "outputs": [str(args.out), str(args.markdown_out), str(args.manifest_out)],
        "git_commit": git_commit(),
        "seconds": round(time.perf_counter() - started, 3),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return read_json_object(path)


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
