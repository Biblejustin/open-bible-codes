#!/usr/bin/env python3
"""Audit WRR expected-count skip caps for imported terms."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.cli import accepted_term_languages
from els.corpus import load_corpus
from els.search import normalize_for_corpus
from els.term_display import display_term
from els.wrr import expected_els_count, relative_letter_frequencies, skip_cap_for_expected_count


TERMS = Path("reports/wrr_1994/wrr2_terms.csv")
COUNTS = Path("reports/wrr_1994/wrr2_genesis_counts.csv")
CONFIG = Path("configs/example_koren_genesis.toml")
OUT = Path("reports/wrr_1994/wrr2_skip_caps.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_skip_caps_summary.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_skip_caps.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_skip_caps.manifest.json")

FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "normalized_length",
    "observed_max_skip",
    "observed_hits",
    "expected_at_observed_max_skip",
    "target_expected_hits",
    "skip_cap",
    "expected_at_skip_cap",
    "skip_cap_formula",
    "printed_skip_cap",
    "program_skip_cap",
    "program_minus_printed",
    "expected_at_program_skip_cap",
    "program_target_reached",
    "target_reached",
    "skip_cap_band",
]

SUMMARY_FIELDNAMES = [
    "rows",
    "unique_normalized_terms",
    "observed_max_skip",
    "target_expected_hits",
    "max_skip_limit",
    "skip_cap_formula",
    "cap_le_observed_max_skip",
    "cap_le_500",
    "cap_le_1000",
    "cap_gt_1000",
    "program_cap_lt_printed",
    "program_cap_eq_printed",
    "program_cap_gt_printed",
    "program_target_unreached_rows",
    "target_unreached_rows",
    "observed_zero_rows",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus = load_corpus(args.config)
    count_rows = {row["term_id"]: row for row in read_rows(args.counts)}
    rows = skip_cap_rows(read_rows(args.terms), count_rows, corpus, args)
    summary = summarize(rows, args)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary)
    if args.manifest_out:
        write_manifest(args, corpus, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, default=TERMS)
    parser.add_argument("--counts", type=Path, default=COUNTS)
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--min-term-length", type=int, default=5)
    parser.add_argument("--max-term-length", type=int, default=8)
    parser.add_argument("--observed-max-skip", type=int, default=250)
    parser.add_argument("--target-expected-hits", type=float, default=10.0)
    parser.add_argument("--max-skip-limit", type=int)
    parser.add_argument("--skip-cap-formula", choices=["printed", "program"], default="printed")
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def skip_cap_rows(
    term_rows: list[dict[str, str]],
    count_rows: dict[str, dict[str, str]],
    corpus,
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    frequencies = relative_letter_frequencies(corpus.text)
    languages = accepted_term_languages(corpus.language)
    output = []
    for row in term_rows:
        if row.get("language", "").strip() not in languages:
            continue
        normalized = normalize_for_corpus(corpus, row.get("term", ""))
        if len(normalized) < args.min_term_length or len(normalized) > args.max_term_length:
            continue
        cap = skip_cap_for_expected_count(
            corpus.text,
            normalized,
            target_expected=args.target_expected_hits,
            max_skip_limit=args.max_skip_limit,
            formula=args.skip_cap_formula,
        )
        printed_cap = skip_cap_for_expected_count(
            corpus.text,
            normalized,
            target_expected=args.target_expected_hits,
            max_skip_limit=args.max_skip_limit,
            formula="printed",
        )
        program_cap = skip_cap_for_expected_count(
            corpus.text,
            normalized,
            target_expected=args.target_expected_hits,
            max_skip_limit=args.max_skip_limit,
            formula="program",
        )
        expected_at_observed = expected_els_count(
            len(corpus.text),
            normalized,
            args.observed_max_skip,
            frequencies,
            formula=args.skip_cap_formula,
        )
        expected_at_cap = expected_els_count(
            len(corpus.text),
            normalized,
            cap,
            frequencies,
            formula=args.skip_cap_formula,
        )
        expected_at_program_cap = expected_els_count(
            len(corpus.text),
            normalized,
            program_cap,
            frequencies,
            formula="program",
        )
        target_reached = expected_at_cap >= args.target_expected_hits
        program_target_reached = expected_at_program_cap >= args.target_expected_hits
        count_row = count_rows.get(row["term_id"], {})
        output.append(
            {
                "term_id": row["term_id"],
                "concept": row.get("concept", ""),
                "category": row.get("category", ""),
                "term": row.get("term", ""),
                "normalized_term": normalized,
                "normalized_length": len(normalized),
                "observed_max_skip": args.observed_max_skip,
                "observed_hits": int_or_zero(count_row.get("hit_count")),
                "expected_at_observed_max_skip": round(expected_at_observed, 6),
                "target_expected_hits": args.target_expected_hits,
                "skip_cap": cap,
                "expected_at_skip_cap": round(expected_at_cap, 6),
                "skip_cap_formula": args.skip_cap_formula,
                "printed_skip_cap": printed_cap,
                "program_skip_cap": program_cap,
                "program_minus_printed": program_cap - printed_cap,
                "expected_at_program_skip_cap": round(expected_at_program_cap, 6),
                "program_target_reached": program_target_reached,
                "target_reached": target_reached,
                "skip_cap_band": skip_cap_band(cap, args),
            }
        )
    return sorted(output, key=lambda item: (int(item["skip_cap"]), str(item["term_id"])))


def summarize(rows: list[dict[str, object]], args: argparse.Namespace) -> dict[str, object]:
    caps = [int(row["skip_cap"]) for row in rows]
    bands = Counter(row["skip_cap_band"] for row in rows)
    return {
        "rows": len(rows),
        "unique_normalized_terms": len({row["normalized_term"] for row in rows}),
        "observed_max_skip": args.observed_max_skip,
        "target_expected_hits": args.target_expected_hits,
        "max_skip_limit": args.max_skip_limit or "word_max",
        "skip_cap_formula": args.skip_cap_formula,
        "cap_le_observed_max_skip": sum(1 for cap in caps if cap <= args.observed_max_skip),
        "cap_le_500": bands["cap_le_500"],
        "cap_le_1000": bands["cap_le_1000"],
        "cap_gt_1000": bands["cap_gt_1000"],
        "program_cap_lt_printed": sum(
            1 for row in rows if int(row.get("program_skip_cap", 0)) < int(row.get("printed_skip_cap", 0))
        ),
        "program_cap_eq_printed": sum(
            1 for row in rows if int(row.get("program_skip_cap", 0)) == int(row.get("printed_skip_cap", 0))
        ),
        "program_cap_gt_printed": sum(
            1 for row in rows if int(row.get("program_skip_cap", 0)) > int(row.get("printed_skip_cap", 0))
        ),
        "program_target_unreached_rows": sum(
            1 for row in rows if not bool(row.get("program_target_reached", False))
        ),
        "target_unreached_rows": sum(1 for row in rows if not bool(row["target_reached"])),
        "observed_zero_rows": sum(1 for row in rows if int_or_zero(row["observed_hits"]) == 0),
    }


def skip_cap_band(cap: int, args: argparse.Namespace) -> str:
    if cap <= args.observed_max_skip:
        return "cap_le_observed_max_skip"
    if cap <= 500:
        return "cap_le_500"
    if cap <= 1000:
        return "cap_le_1000"
    return "cap_gt_1000"


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: dict[str, object],
) -> None:
    top_low = rows[:15]
    top_high = rows[-15:]
    lines = [
        "# WRR2 Skip-Cap Audit",
        "",
        "This report estimates the WRR appendix-style skip cap D(w) where expected ELS hits reach 10 for imported length 5..8 terms.",
        "It keeps the selected formula in `skip_cap` and also reports printed-formula and reported-program-formula caps side by side.",
        "",
        "## Summary",
        "",
        "| Item | Count |",
        "| --- | ---: |",
    ]
    for key in SUMMARY_FIELDNAMES:
        lines.append(f"| `{key}` | {summary[key]} |")
    lines.extend(
        [
            "",
            "## Smallest Caps",
            "",
            "| Term | Length | Observed hits at 250 | Skip cap | Program cap | Expected at cap |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in top_low:
        lines.append(skip_cap_markdown_row(row))
    lines.extend(
        [
            "",
            "## Largest Caps",
            "",
            "| Term | Length | Observed hits at 250 | Skip cap | Program cap | Expected at cap |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in top_high:
        lines.append(skip_cap_markdown_row(row))
    lines.extend(
        [
            "",
            "## Caution",
            "",
            "This estimates D(w) from corpus letter frequencies only. It does not compute corrected distances or WRR permutation statistics.",
            "The printed-formula versus reported-program-formula choice remains a reproduction-method decision.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def skip_cap_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row["normalized_term"]), english=str(row.get("concept", "")) or None)
    return (
        "| "
        + " | ".join(
            [
                f"`{row['term_id']}` {term}",
                str(row["normalized_length"]),
                str(row["observed_hits"]),
                str(row["skip_cap"]),
                str(row.get("program_skip_cap", "")),
                str(row["expected_at_skip_cap"]),
            ]
        )
        + " |"
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    args: argparse.Namespace,
    corpus,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "terms": str(args.terms),
        "counts": str(args.counts),
        "config": str(args.config),
        "skip_cap_formula": args.skip_cap_formula,
        "corpus": corpus.summary(),
        "summary": summary,
        "rows": len(rows),
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


if __name__ == "__main__":
    raise SystemExit(main())
