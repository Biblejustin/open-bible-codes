#!/usr/bin/env python3
"""Compare ChurchAges-style ELS count claims to letter-frequency expectations."""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import Corpus, load_corpus
from els.search import normalize_for_corpus
from els.skip_plan import (
    directional_factor,
    expected_hits_through_skip,
    max_skip_for_mode,
    query_probability,
)
from els.statistics import estimated_search_space, hits_per_million, round_float


DEFAULT_CLAIMS = Path("data/study/churchages_claim_counts.csv")
DEFAULT_OUT = Path("reports/churchages_statistics/audit.csv")
DEFAULT_MD = Path("reports/churchages_statistics/audit.md")
DEFAULT_MANIFEST = Path("reports/churchages_statistics/audit.manifest.json")

FIELDNAMES = [
    "term_id",
    "term",
    "corpus",
    "corpus_language",
    "direction",
    "observed_hits",
    "normalized_term",
    "normalized_length",
    "corpus_letters",
    "claimed_corpus_letters",
    "corpus_letter_delta_vs_claim",
    "min_skip",
    "max_skip_mode",
    "effective_max_skip",
    "letter_probability",
    "churchages_triangle_positions",
    "churchages_expected_hits",
    "churchages_observed_minus_expected",
    "churchages_error_pct",
    "exact_search_space_positions",
    "exact_expected_hits",
    "exact_observed_minus_expected",
    "exact_error_pct",
    "observed_hits_per_million_exact_positions",
    "source_url",
    "notes",
    "status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    claim_rows = read_rows(args.claims)
    corpus_cache: dict[Path, Corpus] = {}
    audit_rows = [audit_claim(row, corpus_cache) for row in claim_rows]
    write_rows(args.out, audit_rows)
    write_markdown(args.markdown_out, audit_rows, args)
    write_manifest(args.manifest_out, args, audit_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", type=Path, default=DEFAULT_CLAIMS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def audit_claim(row: dict[str, str], corpus_cache: dict[Path, Corpus]) -> dict[str, str]:
    config = Path(row["config"])
    corpus = corpus_cache.get(config)
    if corpus is None:
        corpus = load_corpus(config)
        corpus_cache[config] = corpus

    term = row["term"]
    query = normalize_for_corpus(corpus, term)
    direction = row.get("direction") or "forward"
    min_skip = int(row.get("min_skip") or 2)
    max_skip_mode = row.get("max_skip_mode") or "letters-per-term"
    max_skip = effective_max_skip(
        len(corpus.text),
        len(query),
        mode=max_skip_mode,
        fixed_value=row.get("max_skip", ""),
    )
    observed = optional_int(row.get("observed_hits", ""))
    claimed_letters = optional_int(row.get("claimed_corpus_letters", ""))
    probability = query_probability(corpus.text, query)
    churchages_positions = churchages_triangle_positions(
        len(corpus.text),
        len(query),
        direction,
    )
    churchages_expected = churchages_positions * probability
    exact_positions = estimated_search_space(
        len(corpus.text),
        len(query),
        min_skip,
        max_skip,
        direction,
    )
    exact_expected = expected_hits_through_skip(
        len(corpus.text),
        len(query),
        probability,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
    )
    return {
        "term_id": row.get("term_id", ""),
        "term": term,
        "corpus": row.get("corpus", ""),
        "corpus_language": corpus.language,
        "direction": direction,
        "observed_hits": "" if observed is None else str(observed),
        "normalized_term": query,
        "normalized_length": str(len(query)),
        "corpus_letters": str(len(corpus.text)),
        "claimed_corpus_letters": "" if claimed_letters is None else str(claimed_letters),
        "corpus_letter_delta_vs_claim": (
            "" if claimed_letters is None else str(len(corpus.text) - claimed_letters)
        ),
        "min_skip": str(min_skip),
        "max_skip_mode": max_skip_mode,
        "effective_max_skip": str(max_skip),
        "letter_probability": scientific(probability),
        "churchages_triangle_positions": round_float(churchages_positions),
        "churchages_expected_hits": round_float(churchages_expected),
        "churchages_observed_minus_expected": observed_delta(observed, churchages_expected),
        "churchages_error_pct": observed_error_pct(observed, churchages_expected),
        "exact_search_space_positions": str(exact_positions),
        "exact_expected_hits": round_float(exact_expected),
        "exact_observed_minus_expected": observed_delta(observed, exact_expected),
        "exact_error_pct": observed_error_pct(observed, exact_expected),
        "observed_hits_per_million_exact_positions": (
            "" if observed is None else hits_per_million(observed, exact_positions)
        ),
        "source_url": row.get("source_url", ""),
        "notes": row.get("notes", ""),
        "status": "audited" if query else "skipped_empty_term",
    }


def effective_max_skip(
    text_length: int,
    query_length: int,
    *,
    mode: str,
    fixed_value: str,
) -> int:
    if mode == "fixed":
        if not fixed_value:
            raise ValueError("fixed max_skip_mode requires max_skip")
        return int(fixed_value)
    return max_skip_for_mode(text_length, query_length, mode)


def churchages_triangle_positions(text_length: int, query_length: int, direction: str) -> float:
    """Return the simplified ChurchAges scatter-plot triangle area.

    The cited article treats the horizontal axis as corpus length and the
    vertical axis as corpus length divided by term length, then multiplies the
    triangle area by the term's independent-letter probability.
    """

    if text_length <= 0 or query_length <= 0:
        return 0.0
    return 0.5 * text_length * (text_length / query_length) * directional_factor(direction)


def optional_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def observed_delta(observed: int | None, expected: float) -> float | str:
    if observed is None:
        return ""
    return round_float(observed - expected)


def observed_error_pct(observed: int | None, expected: float) -> float | str:
    if observed is None or expected == 0:
        return ""
    return round_float(100 * (observed - expected) / expected)


def scientific(value: float) -> str:
    if value == 0 or not math.isfinite(value):
        return str(value)
    return f"{value:.12e}"


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# ChurchAges Statistics Audit",
        "",
        "This report compares published ChurchAges observed ELS counts with two",
        "independent-letter expectations:",
        "",
        "- `churchages_expected_hits`: simplified scatter-plot triangle area times",
        "  corpus-specific letter probability.",
        "- `exact_expected_hits`: exact valid ELS start-position count through the",
        "  selected skip cap times the same letter probability.",
        "",
        "The comparison tests a count-density claim. It does not test theological",
        "meaning, surface-context meaning, or post-hoc cluster selection.",
        "",
        "## Inputs",
        "",
        f"- Claims: `{args.claims}`",
        f"- CSV: `{args.out}`",
        "",
        "## Results",
        "",
        "| Term | Direction | Observed | ChurchAges expected | Error % | Exact expected | Exact error % | Corpus letters | Claimed letters |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['term']}`",
                    text_value(row["direction"]),
                    text_value(row["observed_hits"]),
                    text_value(row["churchages_expected_hits"]),
                    text_value(row["churchages_error_pct"]),
                    text_value(row["exact_expected_hits"]),
                    text_value(row["exact_error_pct"]),
                    text_value(row["corpus_letters"]),
                    text_value(row["claimed_corpus_letters"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "If the ChurchAges-style expectation is close to observed, that supports",
            "the narrower point that common independent-letter density explains much",
            "of the raw count volume. A close count prediction is not evidence that",
            "a term is meaningful. The exact-window column is usually the better",
            "internal baseline because it counts legal start/skip positions instead",
            "of using the simplified triangle area.",
            "",
            "The KJV source used here has a different normalized letter count from",
            "the ChurchAges article. That difference is reported in the CSV and can",
            "affect the comparison.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "script": "scripts/analyze_churchages_statistics.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "claims": str(args.claims),
        "out": str(args.out),
        "markdown_out": str(args.markdown_out),
        "rows": len(rows),
        "git_commit": git_commit(),
    }
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def text_value(value: object) -> str:
    return "" if value is None else str(value)


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
