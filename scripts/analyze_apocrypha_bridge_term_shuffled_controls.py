#!/usr/bin/env python3
"""Compare apocrypha bridge terms with shuffled insertion-block controls."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import load_corpus
from els.search import process_context, resolve_count_jobs
from els.statistics import benjamini_hochberg_q_values, round_float, tail_p_value_ge
from scripts.analyze_apocrypha_bridge_candidates import DEFAULT_TERMS, read_term_records
from scripts.analyze_apocrypha_bridge_controls import (
    DEFAULT_CANONICAL_CONFIG,
    DEFAULT_OBSERVED,
    boundary_offsets,
    read_rows,
)
from scripts.analyze_apocrypha_bridge_shuffled_controls import count_bridge_rows, shuffled_text


DEFAULT_SAMPLE_OUT = Path("reports/kjv_apocrypha_bridge_term_shuffled_controls/sample_summary.csv")
DEFAULT_TERM_SAMPLE_OUT = Path("reports/kjv_apocrypha_bridge_term_shuffled_controls/term_samples.csv")
DEFAULT_TERM_SUMMARY_OUT = Path("reports/kjv_apocrypha_bridge_term_shuffled_controls/term_summary.csv")
DEFAULT_MARKDOWN = Path("docs/KJV_APOCRYPHA_BRIDGE_TERM_SHUFFLED_CONTROLS.md")
DEFAULT_MANIFEST = Path("reports/kjv_apocrypha_bridge_term_shuffled_controls/manifest.json")

SAMPLE_FIELDNAMES = [
    "sample",
    "seed",
    "bridge_rows",
    "terms_with_bridge_rows",
    "canonical_to_apocrypha",
    "apocrypha_to_canonical",
    "multi_segment_bridge",
]

TERM_SAMPLE_FIELDNAMES = [
    "sample",
    "seed",
    "normalized_term",
    "bridge_rows",
    "canonical_to_apocrypha",
    "apocrypha_to_canonical",
    "multi_segment_bridge",
]

TERM_SUMMARY_FIELDNAMES = [
    "rank",
    "normalized_term",
    "term_ids",
    "concepts",
    "categories",
    "observed_bridge_rows",
    "samples",
    "sample_min",
    "sample_mean",
    "sample_max",
    "samples_ge_observed",
    "p_ge",
    "q_ge",
    "observed_minus_sample_max",
    "observed_gt_sample_max",
]


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
    existing_sample_rows = read_sample_rows(args.sample_out) if args.resume_samples else None
    existing_term_sample_rows = read_term_sample_rows(args.term_sample_out) if args.resume_samples else None
    sample_rows, term_sample_rows = run_samples(
        corpus.text[: boundary["canonical_prefix_letters"]],
        apocrypha_block,
        term_records,
        boundary,
        args,
        existing_sample_rows=existing_sample_rows,
        existing_term_sample_rows=existing_term_sample_rows,
    )
    term_summary = summarize_terms(observed_rows, term_sample_rows, term_records, args.samples)
    write_csv(args.sample_out, sample_rows, SAMPLE_FIELDNAMES)
    write_csv(args.term_sample_out, term_sample_rows, TERM_SAMPLE_FIELDNAMES)
    write_csv(args.term_summary_out, term_summary, TERM_SUMMARY_FIELDNAMES)
    write_markdown(args.markdown_out, term_summary, sample_rows, corpus, boundary, args)
    write_manifest(args.manifest_out, args, sample_rows, term_summary, corpus, boundary, started)
    print(args.sample_out)
    print(args.term_sample_out)
    print(args.term_summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-label", default="KJVA")
    parser.add_argument("--canonical-config", type=Path, default=DEFAULT_CANONICAL_CONFIG)
    parser.add_argument("--terms", type=Path, action="append")
    parser.add_argument("--observed", type=Path, default=DEFAULT_OBSERVED)
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260509)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=250)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--min-term-length", type=int, default=4)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--resume-samples", action="store_true")
    parser.add_argument("--sample-out", type=Path, default=DEFAULT_SAMPLE_OUT)
    parser.add_argument("--term-sample-out", type=Path, default=DEFAULT_TERM_SAMPLE_OUT)
    parser.add_argument("--term-summary-out", type=Path, default=DEFAULT_TERM_SUMMARY_OUT)
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
    existing_sample_rows: list[dict[str, object]] | None = None,
    existing_term_sample_rows: list[dict[str, object]] | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    sample_rows_by_key: dict[tuple[int, int], dict[str, object]] = {}
    term_sample_rows_by_key: dict[tuple[int, int], list[dict[str, object]]] = {}
    missing_samples: list[tuple[int, int]] = []
    existing_sample_by_key = {
        (int(row["sample"]), int(row["seed"])): row
        for row in existing_sample_rows or []
        if row.get("sample") and row.get("seed")
    }
    existing_terms_by_key: dict[tuple[int, int], list[dict[str, object]]] = {}
    for row in existing_term_sample_rows or []:
        key = (int(row["sample"]), int(row["seed"]))
        existing_terms_by_key.setdefault(key, []).append(row)

    for sample in range(1, args.samples + 1):
        seed = args.seed + sample - 1
        key = (sample, seed)
        existing_sample = existing_sample_by_key.get(key)
        existing_terms = existing_terms_by_key.get(key)
        if existing_sample is not None and (
            existing_terms is not None or int(existing_sample.get("terms_with_bridge_rows", 0)) == 0
        ):
            sample_rows_by_key[key] = existing_sample
            term_sample_rows_by_key[key] = existing_terms or []
            continue
        missing_samples.append(key)

    worker_options = sample_worker_options(args)
    effective_jobs = resolve_count_jobs(args.jobs, len(missing_samples)) if missing_samples else 1
    if effective_jobs > 1:
        with ProcessPoolExecutor(
            max_workers=effective_jobs,
            mp_context=process_context(),
            initializer=initialize_sample_worker,
            initargs=(canonical_prefix, apocrypha_block, term_records, boundary, worker_options),
        ) as executor:
            for sample_row, term_rows in executor.map(count_sample_worker, missing_samples):
                key = (int(sample_row["sample"]), int(sample_row["seed"]))
                sample_rows_by_key[key] = sample_row
                term_sample_rows_by_key[key] = term_rows
                if args.resume_samples:
                    write_csv(args.sample_out, ordered_sample_rows(sample_rows_by_key), SAMPLE_FIELDNAMES)
                    write_csv(args.term_sample_out, ordered_term_sample_rows(term_sample_rows_by_key), TERM_SAMPLE_FIELDNAMES)
    else:
        worker_args = argparse.Namespace(**worker_options)
        for sample, seed in missing_samples:
            sample_row, term_rows = count_sample(
                canonical_prefix,
                apocrypha_block,
                term_records,
                boundary,
                worker_args,
                sample,
                seed,
            )
            key = (sample, seed)
            sample_rows_by_key[key] = sample_row
            term_sample_rows_by_key[key] = term_rows
            if args.resume_samples:
                write_csv(args.sample_out, ordered_sample_rows(sample_rows_by_key), SAMPLE_FIELDNAMES)
                write_csv(args.term_sample_out, ordered_term_sample_rows(term_sample_rows_by_key), TERM_SAMPLE_FIELDNAMES)
    return ordered_sample_rows(sample_rows_by_key), ordered_term_sample_rows(term_sample_rows_by_key)


def ordered_sample_rows(rows_by_key: dict[tuple[int, int], dict[str, object]]) -> list[dict[str, object]]:
    return [row for _key, row in sorted(rows_by_key.items())]


def ordered_term_sample_rows(rows_by_key: dict[tuple[int, int], list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for _key, term_rows in sorted(rows_by_key.items()):
        rows.extend(term_rows)
    return rows


def sample_worker_options(args: argparse.Namespace) -> dict[str, object]:
    return {
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "jobs": 1,
    }


def count_sample(
    canonical_prefix: str,
    apocrypha_block: str,
    term_records: dict[str, list[dict[str, str]]],
    boundary: dict[str, int],
    args: argparse.Namespace,
    sample: int,
    seed: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    text = canonical_prefix + shuffled_text(apocrypha_block, seed)
    total_by_type, term_by_type = count_bridge_rows(text, term_records, boundary, args)
    return (
        {
            "sample": sample,
            "seed": seed,
            "bridge_rows": sum(total_by_type.values()),
            "terms_with_bridge_rows": len(term_by_type),
            "canonical_to_apocrypha": total_by_type["canonical_to_apocrypha"],
            "apocrypha_to_canonical": total_by_type["apocrypha_to_canonical"],
            "multi_segment_bridge": total_by_type["multi_segment_bridge"],
        },
        term_sample_records(sample, seed, term_by_type),
    )


_SAMPLE_WORKER_CANONICAL_PREFIX = ""
_SAMPLE_WORKER_APOCRYPHA_BLOCK = ""
_SAMPLE_WORKER_TERM_RECORDS: dict[str, list[dict[str, str]]] = {}
_SAMPLE_WORKER_BOUNDARY: dict[str, int] = {}
_SAMPLE_WORKER_ARGS: argparse.Namespace | None = None


def initialize_sample_worker(
    canonical_prefix: str,
    apocrypha_block: str,
    term_records: dict[str, list[dict[str, str]]],
    boundary: dict[str, int],
    options: dict[str, object],
) -> None:
    global _SAMPLE_WORKER_CANONICAL_PREFIX
    global _SAMPLE_WORKER_APOCRYPHA_BLOCK
    global _SAMPLE_WORKER_TERM_RECORDS
    global _SAMPLE_WORKER_BOUNDARY
    global _SAMPLE_WORKER_ARGS

    _SAMPLE_WORKER_CANONICAL_PREFIX = canonical_prefix
    _SAMPLE_WORKER_APOCRYPHA_BLOCK = apocrypha_block
    _SAMPLE_WORKER_TERM_RECORDS = term_records
    _SAMPLE_WORKER_BOUNDARY = boundary
    _SAMPLE_WORKER_ARGS = argparse.Namespace(**options)


def count_sample_worker(sample_seed: tuple[int, int]) -> tuple[dict[str, object], list[dict[str, object]]]:
    if _SAMPLE_WORKER_ARGS is None:
        raise RuntimeError("sample worker is not initialized")
    sample, seed = sample_seed
    return count_sample(
        _SAMPLE_WORKER_CANONICAL_PREFIX,
        _SAMPLE_WORKER_APOCRYPHA_BLOCK,
        _SAMPLE_WORKER_TERM_RECORDS,
        _SAMPLE_WORKER_BOUNDARY,
        _SAMPLE_WORKER_ARGS,
        sample,
        seed,
    )


def term_sample_records(
    sample: int,
    seed: int,
    term_by_type: dict[str, Counter[str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for term in sorted(term_by_type):
        counts = term_by_type[term]
        rows.append(
            {
                "sample": sample,
                "seed": seed,
                "normalized_term": term,
                "bridge_rows": sum(counts.values()),
                "canonical_to_apocrypha": counts["canonical_to_apocrypha"],
                "apocrypha_to_canonical": counts["apocrypha_to_canonical"],
                "multi_segment_bridge": counts["multi_segment_bridge"],
            }
        )
    return rows


def summarize_terms(
    observed_rows: list[dict[str, str]],
    term_sample_rows: list[dict[str, object]],
    term_records: dict[str, list[dict[str, str]]],
    samples: int,
) -> list[dict[str, object]]:
    observed_counts = Counter(
        row["normalized_term"]
        for row in observed_rows
        if row["normalized_term"] in term_records
    )
    sample_counts_by_term: dict[str, list[int]] = {term: [0] * samples for term in observed_counts}
    for row in term_sample_rows:
        term = str(row["normalized_term"])
        if term not in sample_counts_by_term:
            continue
        sample_index = int(row["sample"]) - 1
        if 0 <= sample_index < samples:
            sample_counts_by_term[term][sample_index] = int(row["bridge_rows"])

    rows: list[dict[str, object]] = []
    for term, observed in observed_counts.items():
        counts = sample_counts_by_term[term]
        samples_ge = sum(1 for count in counts if count >= observed)
        sample_max = max(counts) if counts else 0
        first_record = term_records.get(term, [{}])[0]
        rows.append(
            {
                "normalized_term": term,
                "term_ids": ";".join(record.get("term_id", "") for record in term_records.get(term, [])),
                "concepts": ";".join(record.get("concept", "") for record in term_records.get(term, [])),
                "categories": ";".join(record.get("category", "") for record in term_records.get(term, [])),
                "observed_bridge_rows": observed,
                "samples": samples,
                "sample_min": min(counts) if counts else 0,
                "sample_mean": round_float(mean(counts)),
                "sample_max": sample_max,
                "samples_ge_observed": samples_ge,
                "p_ge": round_float(tail_p_value_ge(observed, counts)),
                "q_ge": "",
                "observed_minus_sample_max": observed - sample_max,
                "observed_gt_sample_max": str(observed > sample_max),
                "_sort_term": first_record.get("term_id", term),
            }
        )
    q_values = benjamini_hochberg_q_values([float(row["p_ge"]) for row in rows])
    for row, q_value in zip(rows, q_values, strict=True):
        row["q_ge"] = round_float(q_value)
    rows.sort(
        key=lambda row: (
            row["observed_gt_sample_max"] != "True",
            float(row["q_ge"]),
            float(row["p_ge"]),
            -int(row["observed_minus_sample_max"]),
            -int(row["observed_bridge_rows"]),
            str(row["_sort_term"]),
        )
    )
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank
        del row["_sort_term"]
    return rows


def read_sample_rows(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [normalize_int_row(row, SAMPLE_FIELDNAMES) for row in csv.DictReader(handle)]


def read_term_sample_rows(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [normalize_term_sample_row(row) for row in csv.DictReader(handle)]


def normalize_term_sample_row(row: dict[str, str]) -> dict[str, object]:
    normalized = normalize_int_row(row, [field for field in TERM_SAMPLE_FIELDNAMES if field != "normalized_term"])
    normalized["normalized_term"] = row.get("normalized_term", "")
    return normalized


def normalize_int_row(row: dict[str, str], fieldnames: list[str]) -> dict[str, object]:
    normalized: dict[str, object] = {}
    for field in fieldnames:
        value = row.get(field, "")
        normalized[field] = int(value) if value != "" else 0
    return normalized


def mean(values: list[int]) -> float:
    return sum(values) / len(values) if values else 0.0


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    term_summary: list[dict[str, object]],
    sample_rows: list[dict[str, object]],
    corpus: Any,
    boundary: dict[str, int],
    args: argparse.Namespace,
) -> None:
    observed_gt_sample_max = sum(1 for row in term_summary if row["observed_gt_sample_max"] == "True")
    q_le_005 = sum(float(row["q_ge"]) <= 0.05 for row in term_summary)
    sample_totals = [int(row["bridge_rows"]) for row in sample_rows]
    lines = [
        f"# {args.canonical_label} Apocrypha Bridge Term Shuffled Controls ({args.samples} Samples)",
        "",
        "Status: term-level shuffled-insertion controls. This is not a claim report.",
        "",
        "This control keeps the canonical prefix and apocrypha/deuterocanon block",
        "length fixed, shuffles the block letters, and records bridge rows per",
        "observed bridge term.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Summary",
        "",
        f"- corpus letters: {len(corpus.text)}",
        f"- canonical prefix letters: {boundary['canonical_prefix_letters']}",
        f"- apocrypha block letters: {boundary['apocrypha_block_letters']}",
        f"- bridge terms reviewed: {len(term_summary)}",
        f"- shuffled samples: {len(sample_rows)}",
        f"- total shuffled min/mean/max: {min(sample_totals)} / {round_float(mean(sample_totals))} / {max(sample_totals)}",
        f"- terms with observed count above every shuffled sample: {observed_gt_sample_max}",
        f"- terms with BH q_ge <= 0.05: {q_le_005}",
        "",
        "## Top Terms",
        "",
        "| Rank | Term | Concept | Observed | Shuffled max | Shuffled mean | Samples >= obs | p_ge | q_ge | Delta |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in term_summary[:50]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["rank"]),
                    f"`{row['normalized_term']}`",
                    str(row["concepts"]),
                    str(row["observed_bridge_rows"]),
                    str(row["sample_max"]),
                    str(row["sample_mean"]),
                    str(row["samples_ge_observed"]),
                    str(row["p_ge"]),
                    str(row["q_ge"]),
                    str(row["observed_minus_sample_max"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- This is a post-screen calibration over already observed bridge terms.",
            "- `p_ge` is add-one empirical tail probability for the term count under",
            "  shuffled insertion blocks.",
            "- `q_ge` is Benjamini-Hochberg correction across the emitted bridge terms.",
            "- It should guide follow-up priority, not convert bridge terms into claims.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    sample_rows: list[dict[str, object]],
    term_summary: list[dict[str, object]],
    corpus: Any,
    boundary: dict[str, int],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_apocrypha_bridge_term_shuffled_controls",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "args": manifest_args(args),
        "corpus_letters": len(corpus.text),
        "boundary": boundary,
        "samples": len(sample_rows),
        "terms": len(term_summary),
        "terms_observed_gt_sample_max": sum(1 for row in term_summary if row["observed_gt_sample_max"] == "True"),
        "terms_q_le_0_05": sum(float(row["q_ge"]) <= 0.05 for row in term_summary),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
        "python3 -m scripts.analyze_apocrypha_bridge_term_shuffled_controls",
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
            "--sample-out",
            str(args.sample_out),
            "--term-sample-out",
            str(args.term_sample_out),
            "--term-summary-out",
            str(args.term_summary_out),
            "--markdown-out",
            str(args.markdown_out),
            "--manifest-out",
            str(args.manifest_out),
        ]
    )
    return " ".join(parts)


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
