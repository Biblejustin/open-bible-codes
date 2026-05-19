#!/usr/bin/env python3
"""Run shuffled-letter null baselines for English triage seed hits."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import load_corpus
from els.stats import shuffled_letter_controls, summarize_null_counts


DEFAULT_CONTEXT_SUMMARY = Path("reports/english_version_control_triage/context_summary.csv")
DEFAULT_TERMS = Path("reports/english_version_control_triage/context_seed_terms.csv")
DEFAULT_VERSIONS = Path("reports/biblegateway_english_versions/included_versions.csv")
DEFAULT_OUT_DIR = Path("reports/english_seed_shuffle_baseline")

FIELDNAMES = [
    "corpus",
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "observed",
    "samples",
    "null_mean",
    "null_stdev",
    "z_score",
    "p_greater_equal",
    "percentile",
    "null_min",
    "null_max",
    "shuffled_counts",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    terms = read_terms(args.terms)
    version_configs = read_version_configs(args.versions)
    candidate_keys = read_candidate_keys(args)
    rows_by_corpus = selected_context_rows(args.context_summary, candidate_keys)
    baseline_rows = run_baselines(rows_by_corpus, terms, version_configs, args)
    write_rows(args.out, baseline_rows)
    write_markdown(args.markdown_out, baseline_rows, args)
    write_manifest(args, baseline_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-summary", type=Path, default=DEFAULT_CONTEXT_SUMMARY)
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--versions", type=Path, default=DEFAULT_VERSIONS)
    parser.add_argument("--samples", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260519)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=100)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--candidate-summary", type=Path, default=None)
    parser.add_argument("--candidate-read", action="append", default=[])
    parser.add_argument("--candidate-p-ge-max", type=float, default=None)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR / "summary.csv")
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_OUT_DIR / "summary.md")
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_OUT_DIR / "manifest.json")
    return parser


def read_terms(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["term_id"]: dict(row) for row in csv.DictReader(handle)}


def read_version_configs(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = [dict(row) for row in csv.DictReader(handle)]
    return {
        row["label"]: row.get("resolved_config_path") or row.get("config_path", "")
        for row in rows
    }


def read_candidate_keys(args: argparse.Namespace) -> set[tuple[str, str]] | None:
    if args.candidate_summary is None:
        return None
    reads = set(args.candidate_read)
    keys: set[tuple[str, str]] = set()
    with args.candidate_summary.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if reads and row.get("read", "") not in reads:
                continue
            if args.candidate_p_ge_max is not None:
                p_ge = float_value(row.get("p_greater_equal"))
                if p_ge is None or p_ge > args.candidate_p_ge_max:
                    continue
            keys.add((row["corpus"], row["term_id"]))
    if not keys:
        raise SystemExit("candidate filter selected no rows")
    return keys


def selected_context_rows(
    path: Path,
    candidate_keys: set[tuple[str, str]] | None = None,
) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if int_value(row.get("hit_count")) <= 0:
                continue
            if candidate_keys is not None and (row["corpus"], row["term_id"]) not in candidate_keys:
                continue
            grouped[row["corpus"]].append(dict(row))
    return dict(grouped)


def run_baselines(
    rows_by_corpus: dict[str, list[dict[str, str]]],
    terms: dict[str, dict[str, str]],
    version_configs: dict[str, str],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    output = []
    for corpus_label, rows in sorted(rows_by_corpus.items()):
        config = version_configs.get(corpus_label, "")
        if not config:
            continue
        corpus = load_corpus(config)
        term_rows = [terms[row["term_id"]] for row in rows if row["term_id"] in terms]
        controls = shuffled_letter_controls(
            corpus,
            [row["term"] for row in term_rows],
            min_skip=args.min_skip,
            max_skip=args.max_skip,
            direction=args.direction,
            shuffles=args.samples,
            seed=args.seed + stable_seed_offset(corpus_label),
            jobs=args.jobs,
        )
        by_term = {term: result for term, result in controls}
        for term_row in term_rows:
            result = by_term[term_row["term"]]
            summary = summarize_null_counts(result.observed, result.shuffled_counts)
            output.append(
                {
                    "corpus": corpus_label,
                    "term_id": term_row["term_id"],
                    "concept": term_row["concept"],
                    "category": term_row["category"],
                    "term": term_row["term"],
                    "normalized_term": normalize_display(term_row["term"]),
                    "observed": result.observed,
                    "samples": summary.samples,
                    "null_mean": float_or_blank(summary.mean),
                    "null_stdev": float_or_blank(summary.stdev),
                    "z_score": float_or_blank(summary.z_score),
                    "p_greater_equal": float_or_blank(summary.p_greater_equal),
                    "percentile": float_or_blank(summary.percentile),
                    "null_min": blank_if_none(summary.min_count),
                    "null_max": blank_if_none(summary.max_count),
                    "shuffled_counts": ";".join(str(count) for count in result.shuffled_counts),
                    "read": read_label(result.observed, summary.p_greater_equal, summary.z_score),
                }
            )
    return sorted(output, key=baseline_sort_key)


def stable_seed_offset(value: str) -> int:
    return sum((index + 1) * ord(char) for index, char in enumerate(value))


def normalize_display(value: str) -> str:
    return "".join(char.lower() for char in value if char.isalpha())


def int_value(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def float_value(value: object) -> float | None:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def blank_if_none(value: object) -> object:
    return "" if value is None else value


def float_or_blank(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6g}"


def read_label(observed: int, p_ge: float | None, z_score: float | None) -> str:
    if p_ge is None:
        return "no shuffle samples"
    if observed == 0:
        return "absent in observed corpus"
    if p_ge <= 0.05:
        return "observed above shuffled baseline floor"
    if z_score is not None and z_score >= 2:
        return "observed elevated vs shuffled mean"
    return "not elevated in small shuffle baseline"


def baseline_sort_key(row: dict[str, object]) -> tuple[float, float, str, str]:
    p = float(row["p_greater_equal"]) if row["p_greater_equal"] != "" else 1.0
    z = float(row["z_score"]) if row["z_score"] != "" else -999.0
    return (p, -z, str(row["corpus"]), str(row["term_id"]))


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# English Seed Shuffle Baseline",
        "",
        "This is a small exploratory full-corpus letter-shuffle baseline for the",
        "English triage seed terms that had observed target-version hits.",
        "",
        "## Scope",
        "",
        f"- Samples per corpus: {args.samples}",
        f"- Skip range: `{args.min_skip}..{args.max_skip}`",
        f"- Direction: `{args.direction}`",
        f"- Jobs per count: {args.jobs}",
        "",
        "## Summary",
        "",
        "| Corpus | Term | Observed | Null mean | Null min-max | p_ge | z | Read |",
        "| --- | --- | ---: | ---: | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["corpus"]),
                    f"`{row['term_id']}` {row['concept']}",
                    str(row["observed"]),
                    str(row["null_mean"]),
                    f"{row['null_min']}-{row['null_max']}",
                    str(row["p_greater_equal"]),
                    str(row["z_score"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Caution",
            "",
            f"With {args.samples} samples, the best possible p_ge floor is",
            f"`1 / {args.samples + 1} = {1 / (args.samples + 1):.4f}`.",
            "Promote nothing from this alone.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    started: float,
) -> None:
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "tool": "analyze_english_seed_shuffle_baseline",
        "created_utc": datetime.now(UTC).isoformat(),
        "context_summary": str(args.context_summary.resolve()),
        "terms": str(args.terms.resolve()),
        "versions": str(args.versions.resolve()),
        "samples": args.samples,
        "seed": args.seed,
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "jobs": args.jobs,
        "candidate_summary": (
            str(args.candidate_summary.resolve()) if args.candidate_summary else ""
        ),
        "candidate_read": args.candidate_read,
        "candidate_p_ge_max": args.candidate_p_ge_max,
        "rows": len(rows),
        "seconds": round(time.perf_counter() - started, 3),
        "outputs": [str(args.out), str(args.markdown_out)],
    }
    args.manifest_out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
