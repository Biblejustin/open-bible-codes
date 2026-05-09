#!/usr/bin/env python3
"""Run paired length-matched controls for focused targeted-term rows."""

from __future__ import annotations

import argparse
import csv
import json
import random
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, load_corpus
from els.search import count_els_terms_by_lanes
from els.statistics import (
    benjamini_hochberg_q_values,
    estimated_search_space,
    hits_per_million,
    numeric_value,
    round_float,
)
from els.stats import NullSummary, summarize_null_counts


DEFAULT_CORPORA = {
    "MT_WLC": Path("configs/example_oshb_wlc.toml"),
    "UHB": Path("configs/example_uhb.toml"),
    "LXX": Path("configs/example_ebible_grclxx.toml"),
    "TR_NT": Path("configs/example_ebible_grctr.toml"),
    "SBLGNT": Path("configs/example_sblgnt.toml"),
}

TARGET_SUMMARY = Path("reports/targeted_terms_summary.csv")
SUMMARY_OUT = Path("reports/targeted_paired_controls_summary.csv")
EXAMPLES_OUT = Path("reports/targeted_paired_controls_examples.csv")
MD_OUT = Path("reports/targeted_paired_controls.md")
MANIFEST_OUT = Path("reports/targeted_paired_controls.manifest.json")

TARGET_ORDER = {
    "Iran": 0,
    "Trump": 1,
    "Vance": 2,
    "Netanyahu": 3,
    "Gog": 4,
    "Magog": 5,
    "Russia": 6,
    "Europe": 7,
    "Turkey": 8,
    "Germany": 9,
}
CORPUS_ORDER = {"MT_WLC": 0, "UHB": 1, "LXX": 2, "TR_NT": 3, "SBLGNT": 4}

SUMMARY_FIELDNAMES = [
    "concept",
    "corpus",
    "term_set",
    "term_id",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "normalized_length",
    "observed_hits",
    "min_skip",
    "max_skip",
    "direction",
    "search_space_positions",
    "hits_per_million_positions",
    "term_shuffle_samples",
    "term_shuffle_unique",
    "term_shuffle_same_as_observed",
    "term_shuffle_mean",
    "term_shuffle_stdev",
    "term_shuffle_z_score",
    "term_shuffle_p_ge",
    "term_shuffle_q_value",
    "term_shuffle_percentile",
    "term_shuffle_min",
    "term_shuffle_max",
    "random_samples",
    "random_unique",
    "random_same_as_observed",
    "random_mean",
    "random_stdev",
    "random_z_score",
    "random_p_ge",
    "random_q_value",
    "random_percentile",
    "random_min",
    "random_max",
    "combined_min_p_ge",
    "combined_min_q_value",
    "paired_band",
    "warning_count",
    "flags",
    "read",
]

EXAMPLE_FIELDNAMES = [
    *SUMMARY_FIELDNAMES,
    "term_shuffle_counts_sample",
    "term_shuffle_terms_sample",
    "random_counts_sample",
    "random_terms_sample",
]


@dataclass(frozen=True)
class TargetRow:
    row: dict[str, str]
    observed_hits: int
    normalized_term: str


@dataclass(frozen=True)
class PairedControlRow:
    row: dict[str, object]
    term_counts: tuple[int, ...]
    term_samples: tuple[str, ...]
    random_counts: tuple[int, ...]
    random_samples: tuple[str, ...]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpora_by_label = corpus_configs(args.corpus)
    targets = read_targets(
        args.target_summary,
        corpora=set(args.target_corpus or []),
        term_ids=set(args.term_id or []),
        concepts=set(args.concept or []),
        min_observed_hits=args.min_observed_hits,
    )
    outputs: list[PairedControlRow] = []
    corpus_manifests: list[dict[str, object]] = []
    for corpus_label in sorted({target.row["corpus"] for target in targets}, key=corpus_sort):
        config = corpora_by_label.get(corpus_label)
        if config is None:
            raise SystemExit(f"no default corpus config for {corpus_label}")
        corpus_started = time.perf_counter()
        corpus = load_corpus(config)
        corpus_targets = [target for target in targets if target.row["corpus"] == corpus_label]
        outputs.extend(analyze_corpus(corpus_label, corpus, corpus_targets, args))
        corpus_manifests.append(
            {
                "label": corpus_label,
                "config": str(config),
                "summary": corpus.summary(),
                "targets": len(corpus_targets),
                "seconds": round(time.perf_counter() - corpus_started, 3),
            }
        )

    annotate_rows(outputs)
    summary_rows = [row.row for row in sorted(outputs, key=output_sort_key)]
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(
        args.examples_out,
        EXAMPLE_FIELDNAMES,
        example_rows(sorted(outputs, key=example_sort_key), args.max_examples),
    )
    write_markdown(args.markdown_out, summary_rows)
    write_manifest(args, corpus_manifests, len(summary_rows), started)

    print(args.summary_out)
    print(args.examples_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-summary", type=Path, default=TARGET_SUMMARY)
    parser.add_argument(
        "--corpus",
        action="append",
        default=None,
        help="Labeled corpus config in LABEL=path form. If supplied, replaces defaults.",
    )
    parser.add_argument("--target-corpus", action="append", default=None)
    parser.add_argument("--term-id", action="append", default=None)
    parser.add_argument("--concept", action="append", default=None)
    parser.add_argument("--min-observed-hits", type=int, default=0)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=50)
    parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    parser.add_argument("--term-shuffle-samples", type=int, default=200)
    parser.add_argument("--random-samples", type=int, default=200)
    parser.add_argument("--seed", type=int, default=911)
    parser.add_argument("--jobs", type=int, default=0)
    parser.add_argument("--max-examples", type=int, default=80)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--examples-out", type=Path, default=EXAMPLES_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def corpus_configs(values: list[str] | None) -> dict[str, Path]:
    if not values:
        return dict(DEFAULT_CORPORA)
    return dict(split_labeled_path(value) for value in values)


def split_labeled_path(value: str) -> tuple[str, Path]:
    if "=" not in value:
        path = Path(value)
        return path.stem, path
    label, path = value.split("=", 1)
    if not label:
        raise ValueError(f"empty corpus label: {value}")
    return label, Path(path)


def read_targets(
    path: Path,
    *,
    corpora: set[str] | None = None,
    term_ids: set[str] | None = None,
    concepts: set[str] | None = None,
    min_observed_hits: int = 0,
) -> list[TargetRow]:
    rows = read_rows(path)
    targets: list[TargetRow] = []
    for row in rows:
        if corpora and row.get("corpus", "") not in corpora:
            continue
        if term_ids and row.get("term_id", "") not in term_ids:
            continue
        if concepts and row.get("concept", "") not in concepts:
            continue
        normalized = row["normalized_term"]
        if not normalized:
            continue
        observed_hits = int_or_zero(row["hit_count"])
        if observed_hits < min_observed_hits:
            continue
        targets.append(
            TargetRow(
                row=row,
                observed_hits=observed_hits,
                normalized_term=normalized,
            )
        )
    return targets


def analyze_corpus(
    corpus_label: str,
    corpus: Corpus,
    targets: list[TargetRow],
    args: argparse.Namespace,
) -> list[PairedControlRow]:
    term_samples_by_key: dict[tuple[str, str, str], tuple[str, ...]] = {}
    random_samples_by_key: dict[tuple[str, str, str], tuple[str, ...]] = {}
    for target in targets:
        key = target_key(target)
        term_rng = random.Random(stable_seed(args.seed, corpus_label, target.row["term_id"], "term"))
        random_rng = random.Random(stable_seed(args.seed, corpus_label, target.row["term_id"], "random"))
        term_samples_by_key[key] = sample_term_controls(
            target.normalized_term,
            samples=args.term_shuffle_samples,
            rng=term_rng,
        )
        random_samples_by_key[key] = sample_random_controls(
            length=len(target.normalized_term),
            corpus_text=corpus.text,
            samples=args.random_samples,
            rng=random_rng,
        )

    unique_controls = sorted(
        {
            sample
            for samples in [*term_samples_by_key.values(), *random_samples_by_key.values()]
            for sample in samples
            if sample
        }
    )
    control_counts = count_els_terms_by_lanes(
        corpus.text,
        unique_controls,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.jobs,
    )

    rows = []
    for target in targets:
        key = target_key(target)
        term_samples = term_samples_by_key[key]
        random_samples = random_samples_by_key[key]
        term_counts = tuple(control_counts.get(sample, 0) for sample in term_samples)
        random_counts = tuple(control_counts.get(sample, 0) for sample in random_samples)
        term_summary = summarize_null_counts(target.observed_hits, term_counts)
        random_summary = summarize_null_counts(target.observed_hits, random_counts)
        rows.append(
            PairedControlRow(
                row=summary_row(
                    corpus_label,
                    corpus,
                    target,
                    term_samples,
                    random_samples,
                    term_summary,
                    random_summary,
                    args,
                ),
                term_counts=term_counts,
                term_samples=term_samples,
                random_counts=random_counts,
                random_samples=random_samples,
            )
        )
    return rows


def summary_row(
    corpus_label: str,
    corpus: Corpus,
    target: TargetRow,
    term_samples: tuple[str, ...],
    random_samples: tuple[str, ...],
    term_summary: NullSummary,
    random_summary: NullSummary,
    args: argparse.Namespace,
) -> dict[str, object]:
    search_space = estimated_search_space(
        len(corpus.text),
        len(target.normalized_term),
        args.min_skip,
        args.max_skip,
        args.direction,
    )
    p_values = [
        value
        for value in [term_summary.p_greater_equal, random_summary.p_greater_equal]
        if value is not None
    ]
    row = {
        "concept": target.row["concept"],
        "corpus": corpus_label,
        "term_set": target.row["term_set"],
        "term_id": target.row["term_id"],
        "category": target.row["category"],
        "term_language": target.row["term_language"],
        "term": target.row["term"],
        "normalized_term": target.normalized_term,
        "normalized_length": len(target.normalized_term),
        "observed_hits": target.observed_hits,
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "search_space_positions": search_space,
        "hits_per_million_positions": hits_per_million(target.observed_hits, search_space),
        **summary_fields("term_shuffle", term_summary),
        "term_shuffle_unique": len(set(term_samples)),
        "term_shuffle_same_as_observed": sum(
            1 for sample in term_samples if sample == target.normalized_term
        ),
        **summary_fields("random", random_summary),
        "random_unique": len(set(random_samples)),
        "random_same_as_observed": sum(
            1 for sample in random_samples if sample == target.normalized_term
        ),
        "combined_min_p_ge": round_float(min(p_values)) if p_values else "",
        "term_shuffle_q_value": "",
        "random_q_value": "",
        "combined_min_q_value": "",
        "paired_band": "",
        "warning_count": "",
        "flags": "",
        "read": "",
    }
    row["flags"] = ";".join(
        flags_for_row(target, row, term_summary, random_summary, term_samples, random_samples)
    )
    return row


def summary_fields(prefix: str, summary: NullSummary) -> dict[str, object]:
    return {
        f"{prefix}_samples": summary.samples,
        f"{prefix}_mean": round_float(summary.mean),
        f"{prefix}_stdev": round_float(summary.stdev),
        f"{prefix}_z_score": round_float(summary.z_score),
        f"{prefix}_p_ge": round_float(summary.p_greater_equal),
        f"{prefix}_percentile": round_float(summary.percentile),
        f"{prefix}_min": empty_if_none(summary.min_count),
        f"{prefix}_max": empty_if_none(summary.max_count),
    }


def flags_for_row(
    target: TargetRow,
    row: dict[str, object],
    term_summary: NullSummary,
    random_summary: NullSummary,
    term_samples: tuple[str, ...],
    random_samples: tuple[str, ...],
) -> list[str]:
    flags = []
    if len(target.normalized_term) <= 3:
        flags.append("short_term")
    if target.observed_hits < 5:
        flags.append("low_observed_hits")
    if int_or_zero(row["search_space_positions"]) >= 10_000_000:
        flags.append("huge_search_space")
    elif int_or_zero(row["search_space_positions"]) >= 1_000_000:
        flags.append("large_search_space")
    if term_summary.samples < 100:
        flags.append("few_term_shuffle_controls")
    if random_summary.samples < 100:
        flags.append("few_random_controls")
    if term_summary.stdev == 0:
        flags.append("zero_term_shuffle_variance")
    if random_summary.stdev == 0:
        flags.append("zero_random_variance")
    if term_samples and len(set(term_samples)) < max(2, len(term_samples) // 4):
        flags.append("low_term_shuffle_diversity")
    if random_samples and len(set(random_samples)) < max(2, len(random_samples) // 4):
        flags.append("low_random_diversity")
    if target.normalized_term in term_samples:
        flags.append("term_shuffle_contains_observed")
    if target.normalized_term in random_samples:
        flags.append("random_contains_observed")
    return sorted(set(flags))


def annotate_rows(rows: list[PairedControlRow]) -> None:
    row_dicts = [row.row for row in rows]
    apply_q_values(row_dicts, "term_shuffle_p_ge", "term_shuffle_q_value")
    apply_q_values(row_dicts, "random_p_ge", "random_q_value")
    apply_q_values(row_dicts, "combined_min_p_ge", "combined_min_q_value")
    for row in row_dicts:
        flags = split_flags(str(row.get("flags", "")))
        band = paired_band(row)
        row["paired_band"] = band
        combined_p = numeric_value(row.get("combined_min_p_ge"))
        combined_q = numeric_value(row.get("combined_min_q_value"))
        if combined_p is not None and combined_p <= 0.05 and (
            combined_q is None or combined_q > 0.10
        ):
            flags.append("uncorrected_only")
        if combined_q is not None:
            flags.append("paired_min_p_adjusted")
        row["flags"] = ";".join(sorted(set(flags)))
        row["warning_count"] = len(split_flags(str(row["flags"])))
        row["read"] = read_label(row)


def paired_band(row: dict[str, object]) -> str:
    combined_q = numeric_value(row.get("combined_min_q_value"))
    combined_p = numeric_value(row.get("combined_min_p_ge"))
    if combined_q is not None:
        if combined_q <= 0.01:
            return "paired_q_le_0.01"
        if combined_q <= 0.05:
            return "paired_q_le_0.05"
        if combined_q <= 0.10:
            return "paired_q_le_0.10"
    if combined_p is not None and combined_p <= 0.05:
        return "paired_uncorrected_p_le_0.05"
    return "not_unusual"


def read_label(row: dict[str, object]) -> str:
    observed = int_or_zero(row.get("observed_hits"))
    length = int_or_zero(row.get("normalized_length"))
    band = str(row.get("paired_band", ""))
    if observed == 0:
        return "absent"
    if band.startswith("paired_q_"):
        return "paired-control screen; review before claim"
    if band == "paired_uncorrected_p_le_0.05":
        return "uncorrected paired-control screen only"
    if length <= 4 and observed > 1000:
        return "not unusual; short-form density remains likely"
    return "not unusual under paired controls"


def apply_q_values(rows: list[dict[str, object]], p_field: str, q_field: str) -> None:
    q_values = benjamini_hochberg_q_values(
        [numeric_value(row.get(p_field)) for row in rows]
    )
    for row, q_value in zip(rows, q_values, strict=True):
        row[q_field] = round_float(q_value)


def sample_term_controls(query: str, *, samples: int, rng: random.Random) -> tuple[str, ...]:
    letters = list(query)
    output = []
    for _index in range(max(0, samples)):
        shuffled = letters[:]
        rng.shuffle(shuffled)
        output.append("".join(shuffled))
    return tuple(output)


def sample_random_controls(
    *,
    length: int,
    corpus_text: str,
    samples: int,
    rng: random.Random,
) -> tuple[str, ...]:
    if length < 1 or samples < 1:
        return ()
    counts = Counter(corpus_text)
    alphabet = sorted(counts)
    weights = [counts[char] for char in alphabet]
    return tuple(
        "".join(rng.choices(alphabet, weights=weights, k=length))
        for _index in range(samples)
    )


def example_rows(rows: list[PairedControlRow], limit: int) -> list[dict[str, object]]:
    output = []
    for control_row in rows[:limit]:
        row = dict(control_row.row)
        row["term_shuffle_counts_sample"] = sample_csv_cell(control_row.term_counts)
        row["term_shuffle_terms_sample"] = sample_csv_cell(control_row.term_samples)
        row["random_counts_sample"] = sample_csv_cell(control_row.random_counts)
        row["random_terms_sample"] = sample_csv_cell(control_row.random_samples)
        output.append(row)
    return output


def write_markdown(path: Path, rows: list[dict[str, object]]) -> None:
    band_counts = Counter(str(row["paired_band"]) for row in rows)
    lines = [
        "# Targeted Paired Controls",
        "",
        "This report reruns focused target rows against two paired controls: shuffled term letters and corpus-letter random strings of the same normalized length.",
        "",
        "## Band Counts",
        "",
        "| Band | Rows |",
        "| --- | ---: |",
    ]
    for band, count in sorted(band_counts.items()):
        lines.append(f"| `{band}` | {count} |")
    lines.extend(
        [
            "",
            "## Concept Read",
            "",
            "| Concept | Best row | Best paired band | Read |",
            "| --- | --- | --- | --- |",
        ]
    )
    for concept in sorted({str(row["concept"]) for row in rows}, key=concept_sort):
        concept_rows = [row for row in rows if row["concept"] == concept]
        best = min(concept_rows, key=markdown_best_key)
        lines.append(
            "| "
            + " | ".join(
                [
                    concept,
                    f"{best['corpus']} `{best['term_id']}` hits={best['observed_hits']}",
                    f"`{best['paired_band']}` p={best['combined_min_p_ge']} q={best['combined_min_q_value']}",
                    str(best["read"]),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Row Details", ""])
    for concept in sorted({str(row["concept"]) for row in rows}, key=concept_sort):
        concept_rows = [row for row in rows if row["concept"] == concept]
        lines.extend(
            [
                f"### {concept}",
                "",
                "| Corpus | Term | Hits | Term p | Random p | Combined q | Band | Read |",
                "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
            ]
        )
        for row in sorted(concept_rows, key=output_sort_key):
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["corpus"]),
                        f"`{row['term_id']}`",
                        str(row["observed_hits"]),
                        str(row["term_shuffle_p_ge"]),
                        str(row["random_p_ge"]),
                        str(row["combined_min_q_value"]),
                        f"`{row['paired_band']}`",
                        str(row["read"]),
                    ]
                )
                + " |"
            )
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    corpora: list[dict[str, object]],
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_targeted_paired_controls",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "target_summary": str(args.target_summary),
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "term_shuffle_samples": args.term_shuffle_samples,
        "random_samples": args.random_samples,
        "seed": args.seed,
        "jobs": args.jobs,
        "corpora": corpora,
        "rows": rows,
        "outputs": [
            str(args.summary_out),
            str(args.examples_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
        "seconds": round(time.perf_counter() - started, 3),
        "notes": [
            "Term-shuffle controls preserve each target row's normalized letters.",
            "Random controls preserve normalized length and draw from same-corpus letter frequencies.",
            "p_ge values are empirical greater-or-equal tail estimates with add-one smoothing.",
            "combined_min_q_value applies Benjamini-Hochberg correction across emitted focused rows.",
        ],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def target_key(target: TargetRow) -> tuple[str, str, str]:
    return (target.row["corpus"], target.row["term_set"], target.row["term_id"])


def output_sort_key(row: dict[str, object] | PairedControlRow) -> tuple[int, str, int, str]:
    row_dict = row.row if isinstance(row, PairedControlRow) else row
    return (
        TARGET_ORDER.get(str(row_dict["concept"]), 99),
        str(row_dict["term_id"]),
        CORPUS_ORDER.get(str(row_dict["corpus"]), 99),
        str(row_dict["term_set"]),
    )


def example_sort_key(row: PairedControlRow) -> tuple[float, float, int, str, str]:
    row_dict = row.row
    combined_q = numeric_value(row_dict.get("combined_min_q_value"))
    combined_p = numeric_value(row_dict.get("combined_min_p_ge"))
    return (
        1.0 if combined_q is None else combined_q,
        1.0 if combined_p is None else combined_p,
        -int_or_zero(row_dict.get("observed_hits")),
        str(row_dict.get("concept", "")),
        str(row_dict.get("term_id", "")),
    )


def markdown_best_key(row: dict[str, object]) -> tuple[float, float, int]:
    combined_q = numeric_value(row.get("combined_min_q_value"))
    combined_p = numeric_value(row.get("combined_min_p_ge"))
    return (
        1.0 if combined_q is None else combined_q,
        1.0 if combined_p is None else combined_p,
        -int_or_zero(row.get("observed_hits")),
    )


def corpus_sort(corpus_label: str) -> int:
    return CORPUS_ORDER.get(corpus_label, 99)


def concept_sort(concept: str) -> int:
    return TARGET_ORDER.get(concept, 99)


def stable_seed(*parts: object) -> int:
    value = 0
    for part in parts:
        for char in str(part):
            value = (value * 131 + ord(char)) % 2_147_483_647
    return value


def sample_csv_cell(values: tuple[object, ...], limit: int = 20) -> str:
    return ";".join(str(value) for value in values[:limit])


def split_flags(raw_flags: str) -> list[str]:
    return [flag for flag in raw_flags.split(";") if flag]


def empty_if_none(value: int | None) -> int | str:
    return "" if value is None else value


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


if __name__ == "__main__":
    raise SystemExit(main())
