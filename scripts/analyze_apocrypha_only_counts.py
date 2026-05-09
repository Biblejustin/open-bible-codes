#!/usr/bin/env python3
"""Compare ordinary ELS counts inside the LXX apocrypha block."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import Corpus, VerseSpan, load_corpus
from els.search import count_els_terms_by_lanes
from els.statistics import estimated_search_space, hits_per_million

from scripts.analyze_apocrypha_bridge_candidates import (
    APOCRYPHA_BOOKS,
    DEFAULT_TERMS,
    read_term_records,
)
from scripts.analyze_apocrypha_bridge_controls import DEFAULT_CONTROLS, parse_label_config, repeated_prefix


DEFAULT_CONFIG = Path("configs/example_ebible_grclxx.toml")
DEFAULT_OUT = Path("reports/apocrypha_only_counts/counts.csv")
DEFAULT_SUMMARY = Path("reports/apocrypha_only_counts/summary.csv")
DEFAULT_MARKDOWN = Path("docs/APOCRYPHA_ONLY_COUNTS.md")
DEFAULT_MANIFEST = Path("reports/apocrypha_only_counts/manifest.json")

FIELDNAMES = [
    "segment",
    "segment_label",
    "normalized_term",
    "term_ids",
    "concepts",
    "categories",
    "term_length",
    "hit_count",
    "search_space",
    "hits_per_million",
]

SUMMARY_FIELDNAMES = [
    "metric",
    "value",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.terms is None:
        args.terms = list(DEFAULT_TERMS)
    if args.control is None:
        args.control = list(DEFAULT_CONTROLS)
    corpus = load_corpus(args.config)
    term_records = read_term_records(args.terms, corpus, min_length=args.min_term_length)
    segments = build_segments(corpus, args)
    rows = []
    for segment, label, text in segments:
        rows.extend(count_segment(segment, label, text, term_records, args))
    summary = summarize(rows, segments, term_records, args)
    write_csv(args.out, rows, FIELDNAMES)
    write_csv(args.summary_out, summary, SUMMARY_FIELDNAMES)
    write_markdown(args.markdown_out, rows, summary, args)
    write_manifest(args.manifest_out, args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-label", default="LXX")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--terms", type=Path, action="append")
    parser.add_argument("--control", action="append")
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=250)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--min-term-length", type=int, default=4)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_segments(corpus: Corpus, args: argparse.Namespace) -> list[tuple[str, str, str]]:
    apocrypha_text = text_for_class(corpus, apocrypha=True)
    canonical_text = text_for_class(corpus, apocrypha=False)
    segments = [
        ("bible_apocrypha", args.corpus_label, apocrypha_text),
        ("bible_canonical", args.corpus_label, canonical_text),
    ]
    for label, config_path in [parse_label_config(value) for value in args.control]:
        control = load_corpus(config_path)
        segments.append(("nonbible_control", label, repeated_prefix(control.text, len(apocrypha_text))))
    return segments


def text_for_class(corpus: Corpus, *, apocrypha: bool) -> str:
    parts = []
    for verse in corpus.verses:
        is_apocrypha = verse.book in APOCRYPHA_BOOKS
        if is_apocrypha == apocrypha and verse.norm_length:
            parts.append(corpus.text[verse.norm_start : verse.norm_end + 1])
    return "".join(parts)


def count_segment(
    segment: str,
    label: str,
    text: str,
    term_records: dict[str, list[dict[str, str]]],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    counts = count_els_terms_by_lanes(
        text,
        term_records.keys(),
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.jobs,
    )
    rows = []
    for query, count in sorted(counts.items()):
        records = term_records[query]
        search_space = estimated_search_space(
            len(text),
            len(query),
            args.min_skip,
            args.max_skip,
            args.direction,
        )
        rows.append(
            {
                "segment": segment,
                "segment_label": label,
                "normalized_term": query,
                "term_ids": join_unique(record["term_id"] for record in records),
                "concepts": join_unique(record["concept"] for record in records),
                "categories": join_unique(record["category"] for record in records),
                "term_length": len(query),
                "hit_count": count,
                "search_space": search_space,
                "hits_per_million": hits_per_million(count, search_space),
            }
        )
    return rows


def summarize(
    rows: list[dict[str, object]],
    segments: list[tuple[str, str, str]],
    term_records: dict[str, list[dict[str, str]]],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    summary = [
        {"metric": "queries_tested", "value": len(term_records)},
        {"metric": "min_skip", "value": args.min_skip},
        {"metric": "max_skip", "value": args.max_skip},
        {"metric": "direction", "value": args.direction},
    ]
    for segment, label, text in segments:
        segment_rows = [
            row for row in rows if row["segment"] == segment and row["segment_label"] == label
        ]
        nonzero = [row for row in segment_rows if int(row["hit_count"]) > 0]
        summary.extend(
            [
                {"metric": f"{segment}:{label}:letters", "value": len(text)},
                {"metric": f"{segment}:{label}:nonzero_terms", "value": len(nonzero)},
                {
                    "metric": f"{segment}:{label}:total_hits",
                    "value": sum(int(row["hit_count"]) for row in segment_rows),
                },
            ]
        )
    return summary


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    by_segment = segment_lookup(rows)
    apoc_rows = by_segment.get(("bible_apocrypha", args.corpus_label), [])
    control_labels = [parse_label_config(value)[0] for value in args.control]
    lines = [
        f"# {args.corpus_label} Apocrypha-Only Counts",
        "",
        f"Status: ordinary ELS count comparison for the {args.corpus_label}",
        "apocrypha/deuterocanon block. This is not a bridge-completion report",
        "and not a claim report.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Summary",
        "",
    ]
    for row in summary:
        lines.append(f"- {row['metric']}: {row['value']}")

    lines.extend(
        [
            "",
            "## Top Apocrypha Terms By Hit Count",
            "",
            "| Term | Concepts | Hits | Hits/M | Canonical hits/M | Max control hits/M | Read |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in sorted(apoc_rows, key=lambda item: (-int(item["hit_count"]), str(item["normalized_term"])))[:40]:
        query = str(row["normalized_term"])
        canonical = row_for(by_segment, "bible_canonical", args.corpus_label, query)
        controls = [
            row_for(by_segment, "nonbible_control", label, query)
            for label in control_labels
        ]
        max_control_rate = max(float_or_zero(control.get("hits_per_million")) for control in controls)
        apoc_rate = float_or_zero(row["hits_per_million"])
        canonical_rate = float_or_zero(canonical.get("hits_per_million"))
        read = "above_controls" if apoc_rate > max_control_rate else "control_background"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_md(query)}`",
                    escape_md(str(row["concepts"])),
                    str(row["hit_count"]),
                    str(row["hits_per_million"]),
                    str(canonical.get("hits_per_million", "")),
                    str(round(max_control_rate, 6)),
                    f"`{read}`",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            f"- This counts ordinary ELS hits inside the existing {args.corpus_label}",
            "  deuterocanon/apocrypha block.",
            f"- Canonical {args.corpus_label} and same-length non-Bible control blocks are comparison",
            "  backgrounds, not final significance tests.",
            "- Short terms dominate raw hit counts; use normalized hits-per-million",
            "  rather than raw totals when comparing segments.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def segment_lookup(rows: list[dict[str, object]]) -> dict[tuple[str, str], list[dict[str, object]]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault((str(row["segment"]), str(row["segment_label"])), []).append(row)
    return grouped


def row_for(
    grouped: dict[tuple[str, str], list[dict[str, object]]],
    segment: str,
    label: str,
    query: str,
) -> dict[str, object]:
    for row in grouped.get((segment, label), []):
        if row.get("normalized_term") == query:
            return row
    return {}


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_apocrypha_only_counts",
        "version": __version__,
        "generated_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "commit": git_commit(),
        "inputs": {
            "config": str(args.config),
            "controls": args.control,
            "terms": [str(path) for path in args.terms],
        },
        "outputs": {
            "counts": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": summary,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reproduce_command(args: argparse.Namespace) -> str:
    controls = " ".join(f"--control {value}" for value in args.control)
    terms = " ".join(f"--terms {path}" for path in args.terms)
    return (
        "python3 -m scripts.analyze_apocrypha_only_counts "
        f"--corpus-label {args.corpus_label} --config {args.config} "
        f"{controls} {terms} --min-skip {args.min_skip} --max-skip {args.max_skip} "
        f"--direction {args.direction} --min-term-length {args.min_term_length} "
        f"--jobs {args.jobs} --out {args.out} --summary-out {args.summary_out} "
        f"--markdown-out {args.markdown_out} --manifest-out {args.manifest_out}"
    )


def join_unique(values: Any) -> str:
    seen: list[str] = []
    for value in values:
        text = str(value)
        if text and text not in seen:
            seen.append(text)
    return ";".join(seen)


def float_or_zero(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
