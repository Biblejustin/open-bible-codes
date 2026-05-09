#!/usr/bin/env python3
"""Plan dynamic full-distance ELS skip searches before running heavy counts."""

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
from els.corpus import Corpus, load_corpus
from els.search import normalize_for_corpus
from els.skip_plan import expected_hits_through_skip, max_skip_for_mode, query_probability
from els.statistics import estimated_search_space, hits_per_million, round_float


DEFAULT_TERMS = Path("terms/dynamic_skip_focus_terms.csv")
DEFAULT_OUT = Path("reports/dynamic_skip_focus/expectations.csv")
DEFAULT_MD = Path("docs/DYNAMIC_SKIP_FOCUS_EXPECTATIONS.md")
DEFAULT_MANIFEST = Path("reports/dynamic_skip_focus/expectations.manifest.json")

FIELDNAMES = [
    "corpus",
    "corpus_language",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "normalized_length",
    "mode",
    "min_skip",
    "effective_max_skip",
    "direction",
    "corpus_letters",
    "search_space_positions",
    "letter_probability",
    "expected_hits",
    "expected_hits_per_million_positions",
    "recommendation",
    "notes",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    terms = read_rows(args.terms)
    corpora = load_corpora(args.corpus)
    rows = build_rows(args, terms, corpora)
    write_rows(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args.manifest_out, args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument(
        "--corpus",
        action="append",
        default=[
            "MT_WLC=configs/example_oshb_wlc.toml",
            "UHB=configs/example_uhb.toml",
            "LXX=configs/example_ebible_grclxx.toml",
            "TR_NT=configs/example_ebible_grctr.toml",
            "SBLGNT=configs/example_sblgnt.toml",
            "KJV=configs/example_ebible_engkjv.toml",
        ],
    )
    parser.add_argument(
        "--mode",
        action="append",
        choices=["full-span", "letters-per-term"],
        default=[],
    )
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_corpora(values: list[str]) -> dict[str, Corpus]:
    corpora: dict[str, Corpus] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected LABEL=CONFIG for --corpus, got {value!r}")
        label, config = value.split("=", 1)
        corpora[label] = load_corpus(Path(config))
    return corpora


def build_rows(
    args: argparse.Namespace,
    terms: list[dict[str, str]],
    corpora: dict[str, Corpus],
) -> list[dict[str, str]]:
    modes = args.mode or ["letters-per-term", "full-span"]
    rows: list[dict[str, str]] = []
    for corpus_label, corpus in corpora.items():
        for term in terms:
            if term.get("language") != corpus.language:
                continue
            normalized = normalize_for_corpus(corpus, term.get("term", ""))
            if not normalized:
                continue
            probability = query_probability(corpus.text, normalized)
            for mode in modes:
                max_skip = max_skip_for_mode(len(corpus.text), len(normalized), mode)
                search_space = estimated_search_space(
                    len(corpus.text),
                    len(normalized),
                    args.min_skip,
                    max_skip,
                    args.direction,
                )
                expected = expected_hits_through_skip(
                    len(corpus.text),
                    len(normalized),
                    probability,
                    min_skip=args.min_skip,
                    max_skip=max_skip,
                    direction=args.direction,
                )
                rows.append(
                    {
                        "corpus": corpus_label,
                        "corpus_language": corpus.language,
                        "term_id": term.get("term_id", ""),
                        "concept": term.get("concept", ""),
                        "category": term.get("category", ""),
                        "term_language": term.get("language", ""),
                        "term": term.get("term", ""),
                        "normalized_term": normalized,
                        "normalized_length": str(len(normalized)),
                        "mode": mode,
                        "min_skip": str(args.min_skip),
                        "effective_max_skip": str(max_skip),
                        "direction": args.direction,
                        "corpus_letters": str(len(corpus.text)),
                        "search_space_positions": str(search_space),
                        "letter_probability": f"{probability:.12e}",
                        "expected_hits": str(round_float(expected)),
                        "expected_hits_per_million_positions": (
                            "" if search_space == 0 else str(round_float(1_000_000 * expected / search_space))
                        ),
                        "recommendation": recommendation(max_skip, expected, search_space),
                        "notes": term.get("notes", ""),
                    }
                )
    return sorted(
        rows,
        key=lambda row: (
            row["corpus"],
            row["mode"],
            float(row["expected_hits"] or 0),
            row["term_id"],
        ),
        reverse=True,
    )


def recommendation(max_skip: int, expected_hits: float, search_space: int) -> str:
    if max_skip > 100_000:
        return "requires_long_run_or_large_span_counter"
    if search_space > 1_000_000_000:
        return "targeted_large_span_count_candidate"
    if expected_hits > 100_000:
        return "count_but_expect_many_hits"
    if expected_hits >= 1:
        return "good_targeted_count_candidate"
    return "rare_expected_target"


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_recommendation: dict[str, int] = {}
    for row in rows:
        by_recommendation[row["recommendation"]] = by_recommendation.get(row["recommendation"], 0) + 1
    lines = [
        "# Dynamic Skip Focus Expectations",
        "",
        "This is a planning report for full-distance ELS searches. It does not",
        "count observed hits. It estimates the search space and expected hit count",
        "from corpus-specific letter frequencies before launching expensive",
        "dynamic-skip counts.",
        "",
        "Reproduce with:",
        "",
        "```bash",
        "python3 -m scripts.analyze_dynamic_skip_expectations",
        "```",
        "",
        "## Inputs",
        "",
        f"- Terms: `{args.terms}`",
        f"- Direction: `{args.direction}`",
        f"- Minimum skip: `{args.min_skip}`",
        f"- CSV: `{args.out}`",
        "",
        "## Recommendation Counts",
        "",
        "| Recommendation | Rows |",
        "| --- | ---: |",
    ]
    for label, count in sorted(by_recommendation.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{label}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Lowest Expected Rows",
            "",
            "| Corpus | Mode | Term | Length | Max skip | Expected hits | Recommendation |",
            "| --- | --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in sorted(rows, key=lambda item: float(item["expected_hits"] or 0))[:40]:
        lines.append(table_row(row))
    lines.extend(
        [
            "",
            "## Highest Expected Rows",
            "",
            "| Corpus | Mode | Term | Length | Max skip | Expected hits | Recommendation |",
            "| --- | --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in sorted(rows, key=lambda item: float(item["expected_hits"] or 0), reverse=True)[:40]:
        lines.append(table_row(row))
    lines.extend(
        [
            "",
            "## Read",
            "",
            "Rows marked `requires_long_run_or_large_span_counter` are not impossible,",
            "and they are not excluded from search. The label means the legacy",
            "Python lane scanner is the wrong tool for that span. Use the compiled",
            "dynamic span counter and the full-span protocol when the research",
            "question calls for the full distance.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def table_row(row: dict[str, str]) -> str:
    return (
        f"| {row['corpus']} | `{row['mode']}` | `{row['term_id']}` "
        f"| {row['normalized_length']} | {row['effective_max_skip']} "
        f"| {row['expected_hits']} | `{row['recommendation']}` |"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "script": "scripts/analyze_dynamic_skip_expectations.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "terms": str(args.terms),
        "rows": len(rows),
        "git_commit": git_commit(),
    }
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
