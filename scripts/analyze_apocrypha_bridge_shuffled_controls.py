#!/usr/bin/env python3
"""Compare apocrypha bridge rows with shuffled insertion-block controls."""

from __future__ import annotations

import argparse
import csv
import json
import random
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import load_corpus
from els.statistics import round_float, tail_p_value_ge
from scripts.analyze_apocrypha_bridge_candidates import (
    DEFAULT_TERMS,
    classify_bridge,
    read_term_records,
)
from scripts.analyze_apocrypha_bridge_controls import (
    DEFAULT_CANONICAL_CONFIG,
    DEFAULT_OBSERVED,
    boundary_offsets,
    position_classes,
    read_rows,
)


DEFAULT_OUT = Path("reports/apocrypha_bridge_shuffled_controls/sample_summary.csv")
DEFAULT_SUMMARY_OUT = Path("reports/apocrypha_bridge_shuffled_controls/summary.csv")
DEFAULT_MARKDOWN = Path("docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md")
DEFAULT_MANIFEST = Path("reports/apocrypha_bridge_shuffled_controls/manifest.json")

SAMPLE_FIELDNAMES = [
    "sample",
    "seed",
    "bridge_rows",
    "terms_with_bridge_rows",
    "canonical_to_apocrypha",
    "apocrypha_to_canonical",
    "multi_segment_bridge",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.terms is None:
        args.terms = list(DEFAULT_TERMS)
    corpus = load_corpus(args.canonical_config)
    boundary = boundary_offsets(corpus)
    observed_rows = read_rows(args.observed)
    term_records = read_term_records(args.terms, corpus, min_length=args.min_term_length)
    apocrypha_block = corpus.text[
        boundary["canonical_prefix_letters"] : boundary["canonical_prefix_letters"] + boundary["apocrypha_block_letters"]
    ]
    sample_rows = run_samples(
        corpus.text[: boundary["canonical_prefix_letters"]],
        apocrypha_block,
        term_records,
        boundary,
        args,
        existing_rows=read_existing_sample_rows(args.out) if args.resume_samples else None,
        progress_out=args.out if args.resume_samples else None,
    )
    summary_rows = summarize(sample_rows, observed_rows, corpus, boundary, args)
    write_csv(args.out, sample_rows, SAMPLE_FIELDNAMES)
    write_csv(args.summary_out, summary_rows, SUMMARY_FIELDNAMES)
    write_markdown(args.markdown_out, sample_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, sample_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-label", default="LXX")
    parser.add_argument("--canonical-config", type=Path, default=DEFAULT_CANONICAL_CONFIG)
    parser.add_argument("--terms", type=Path, action="append")
    parser.add_argument("--observed", type=Path, default=DEFAULT_OBSERVED)
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260509)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=250)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--min-term-length", type=int, default=4)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--resume-samples", action="store_true")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def run_samples(
    canonical_prefix: str,
    apocrypha_block: str,
    term_records: dict[str, list[dict[str, str]]],
    boundary: dict[str, int],
    args: argparse.Namespace,
    *,
    existing_rows: list[dict[str, object]] | None = None,
    progress_out: Path | None = None,
) -> list[dict[str, object]]:
    rows = []
    existing_by_sample = {
        (int(row["sample"]), int(row["seed"])): row
        for row in existing_rows or []
        if row.get("sample") and row.get("seed")
    }
    for sample in range(1, args.samples + 1):
        seed = args.seed + sample - 1
        existing = existing_by_sample.get((sample, seed))
        if existing is not None:
            rows.append(existing)
            continue
        text = canonical_prefix + shuffled_text(apocrypha_block, seed)
        total_by_type, term_by_type = count_bridge_rows(text, term_records, boundary, args)
        rows.append(
            {
                "sample": sample,
                "seed": seed,
                "bridge_rows": sum(total_by_type.values()),
                "terms_with_bridge_rows": len(term_by_type),
                "canonical_to_apocrypha": total_by_type["canonical_to_apocrypha"],
                "apocrypha_to_canonical": total_by_type["apocrypha_to_canonical"],
                "multi_segment_bridge": total_by_type["multi_segment_bridge"],
            }
        )
        if progress_out is not None:
            write_csv(progress_out, rows, SAMPLE_FIELDNAMES)
    return rows


def read_existing_sample_rows(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [normalize_sample_row(row) for row in csv.DictReader(handle)]


def normalize_sample_row(row: dict[str, str]) -> dict[str, object]:
    normalized: dict[str, object] = {}
    for field in SAMPLE_FIELDNAMES:
        value = row.get(field, "")
        normalized[field] = int(value) if value != "" else 0
    return normalized


def shuffled_text(text: str, seed: int) -> str:
    letters = list(text)
    random.Random(seed).shuffle(letters)
    return "".join(letters)


def count_bridge_rows(
    text: str,
    term_records: dict[str, list[dict[str, str]]],
    boundary: dict[str, int],
    args: argparse.Namespace,
) -> tuple[Counter[str], dict[str, Counter[str]]]:
    total_by_type: Counter[str] = Counter()
    term_by_type: dict[str, Counter[str]] = {}
    prefix_length = boundary["canonical_prefix_letters"]
    for query in term_records:
        for skip in range(args.min_skip, args.max_skip + 1):
            if args.direction in {"forward", "both"}:
                for start in bridge_start_range(
                    len(text),
                    prefix_length,
                    len(query),
                    skip,
                    forward=True,
                ):
                    if matches_at_skip(text, query, start, skip):
                        classes = position_classes(
                            range(start, start + len(query) * skip, skip),
                            prefix_length,
                        )
                        bridge_type = classify_bridge(classes)
                        total_by_type[bridge_type] += 1
                        term_by_type.setdefault(query, Counter())[bridge_type] += 1
            if args.direction in {"backward", "both"}:
                for start in bridge_start_range(
                    len(text),
                    prefix_length,
                    len(query),
                    skip,
                    forward=False,
                ):
                    negative_skip = -skip
                    if matches_at_skip(text, query, start, negative_skip):
                        classes = position_classes(
                            range(start, start + len(query) * negative_skip, negative_skip),
                            prefix_length,
                        )
                        bridge_type = classify_bridge(classes)
                        total_by_type[bridge_type] += 1
                        term_by_type.setdefault(query, Counter())[bridge_type] += 1
    return total_by_type, term_by_type


def bridge_start_range(
    text_length: int,
    prefix_length: int,
    query_length: int,
    skip: int,
    *,
    forward: bool,
) -> range:
    span = (query_length - 1) * skip
    if forward:
        start_min = max(0, prefix_length - span)
        start_max = min(prefix_length - 1, text_length - 1 - span)
    else:
        start_min = max(prefix_length, span)
        start_max = min(text_length - 1, prefix_length + span - 1)
    if start_max < start_min:
        return range(0)
    return range(start_min, start_max + 1)


def matches_at_skip(text: str, query: str, start: int, skip: int) -> bool:
    for index, char in enumerate(query):
        if text[start + index * skip] != char:
            return False
    return True


def summarize(
    sample_rows: list[dict[str, object]],
    observed_rows: list[dict[str, str]],
    corpus: Any,
    boundary: dict[str, int],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    observed_total = len(observed_rows)
    sample_counts = [int(row["bridge_rows"]) for row in sample_rows]
    samples_ge = sum(1 for value in sample_counts if value >= observed_total)
    p_ge = tail_p_value_ge(observed_total, sample_counts)
    summary: list[dict[str, object]] = [
        {"metric": "corpus", "value": args.canonical_label},
        {"metric": "corpus_letters", "value": len(corpus.text)},
        {"metric": "canonical_prefix_letters", "value": boundary["canonical_prefix_letters"]},
        {"metric": "apocrypha_block_letters", "value": boundary["apocrypha_block_letters"]},
        {"metric": "observed_bridge_rows", "value": observed_total},
        {"metric": "samples", "value": len(sample_rows)},
        {"metric": "sample_min", "value": min(sample_counts) if sample_counts else ""},
        {"metric": "sample_mean", "value": round_float(mean(sample_counts)) if sample_counts else ""},
        {"metric": "sample_max", "value": max(sample_counts) if sample_counts else ""},
        {"metric": "samples_ge_observed", "value": samples_ge},
        {"metric": "p_ge", "value": round_float(p_ge)},
    ]
    return summary


def mean(values: list[int]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    sample_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    summary = {str(row["metric"]): row["value"] for row in summary_rows}
    lines = [
        f"# {args.canonical_label} Apocrypha Bridge Shuffled Controls ({args.samples} Samples)",
        "",
        "Status: shuffled-insertion controls. This is not a claim report.",
        "",
        "The control keeps the canonical prefix and apocrypha/deuterocanon block",
        "length fixed, but shuffles the block letters before counting bridge rows.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Summary",
        "",
        f"- observed bridge rows: {summary.get('observed_bridge_rows', '')}",
        f"- shuffled samples: {summary.get('samples', '')}",
        f"- shuffled min/mean/max: {summary.get('sample_min', '')} / {summary.get('sample_mean', '')} / {summary.get('sample_max', '')}",
        f"- shuffled samples >= observed: {summary.get('samples_ge_observed', '')}",
        f"- empirical p_ge: {summary.get('p_ge', '')}",
        "",
        "## Samples",
        "",
        "| Sample | Seed | Bridge rows | Terms | C→A | A→C | Multi |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in sample_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["sample"]),
                    str(row["seed"]),
                    str(row["bridge_rows"]),
                    str(row["terms_with_bridge_rows"]),
                    str(row["canonical_to_apocrypha"]),
                    str(row["apocrypha_to_canonical"]),
                    str(row["multi_segment_bridge"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "This is a calibration control. With finite samples, the add-one",
            "empirical p-value remains resolution-limited. Treat the result as",
            "background calibration, not claim evidence.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    sample_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_apocrypha_bridge_shuffled_controls",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "args": manifest_args(args),
        "samples": len(sample_rows),
        "summary": summary_rows,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def manifest_args(args: argparse.Namespace) -> dict[str, object]:
    data: dict[str, object] = {}
    for key, value in vars(args).items():
        if key == "terms":
            data[key] = [str(path) for path in value]
        elif isinstance(value, Path):
            data[key] = str(value)
        else:
            data[key] = value
    return data


def reproduce_command(args: argparse.Namespace) -> str:
    parts = [
        "python3 -m scripts.analyze_apocrypha_bridge_shuffled_controls",
        "--canonical-label",
        args.canonical_label,
        "--canonical-config",
        str(args.canonical_config),
        "--observed",
        str(args.observed),
    ]
    for path in args.terms:
        parts.extend(["--terms", str(path)])
    parts.extend(
        [
            "--samples",
            str(args.samples),
            "--seed",
            str(args.seed),
            "--min-skip",
            str(args.min_skip),
            "--max-skip",
            str(args.max_skip),
            "--direction",
            args.direction,
            "--min-term-length",
            str(args.min_term_length),
            "--jobs",
            str(args.jobs),
        ]
    )
    if args.resume_samples:
        parts.append("--resume-samples")
    parts.extend(
        [
            "--out",
            str(args.out),
            "--summary-out",
            str(args.summary_out),
            "--markdown-out",
            str(args.markdown_out),
            "--manifest-out",
            str(args.manifest_out),
        ]
    )
    return " ".join(parts)


if __name__ == "__main__":
    raise SystemExit(main())
