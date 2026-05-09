#!/usr/bin/env python3
"""Prepare an ignored broad CRD surface-match run directory."""

from __future__ import annotations

import argparse
import csv
import re
import tomllib
from pathlib import Path

from scripts.apply_crd_relevance_review import read_review_rows, write_dictionary as write_reviewed_dictionary
from scripts.check_crd_relevance_dictionary import check_dictionary
from scripts.classify_centered_relevance import sha256_file
from scripts.scaffold_crd_relevance_dictionary import (
    read_terms,
    surface_keywords_by_concept,
    write_dictionary as write_draft_dictionary,
    write_queue,
)


TERM_FIELDNAMES = ["term_id", "concept", "category", "language", "term", "notes"]
DEFAULT_EXCLUDED_TERM_FILES = {"crd_placeholder_terms.csv"}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    term_files = resolve_term_files(args)
    rows = read_terms(term_files)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    concept_surface_keywords = surface_keywords_by_concept(rows) if args.seed_mode == "concept" else {}

    combined_terms = args.out_dir / "terms_combined.csv"
    draft_dictionary = args.out_dir / "relevance_dictionary_draft.toml"
    queue = args.out_dir / "relevance_review_queue.csv"
    dictionary = args.out_dir / f"relevance_dictionary_{args.seed_mode}_surface.toml"
    preregistration = args.out_dir / f"CRD_{args.seed_mode.upper()}_SURFACE_PREREGISTRATION.md"
    protocol = args.out_dir / "protocol.toml"

    write_combined_terms(combined_terms, rows)
    write_draft_dictionary(
        draft_dictionary,
        rows,
        locked_by=args.locked_by,
        reviewer=args.reviewer,
        drafted_with=args.drafted_with,
        seed_surface_term=args.seed_mode == "self",
        concept_surface_keywords=concept_surface_keywords,
    )
    write_queue(
        queue,
        rows,
        seed_surface_term=args.seed_mode == "self",
        concept_surface_keywords=concept_surface_keywords,
    )
    write_reviewed_dictionary(
        dictionary,
        read_review_rows(queue),
        locked_by=args.locked_by,
        reviewer=args.reviewer,
        drafted_with=args.drafted_with,
    )
    dictionary_sha = sha256_file(dictionary)
    write_preregistration(preregistration, dictionary, dictionary_sha, args.locked_by, seed_mode=args.seed_mode)
    preregistration_sha = sha256_file(preregistration)
    write_protocol(
        protocol,
        base_protocol=args.base_protocol,
        combined_terms=combined_terms,
        dictionary=dictionary,
        dictionary_sha=dictionary_sha,
        preregistration=preregistration,
        preregistration_sha=preregistration_sha,
        out_dir=args.out_dir,
        progress_interval_seconds=args.progress_interval_seconds,
        seed_mode=args.seed_mode,
    )
    check_dictionary(
        dictionary=dictionary,
        term_files=[combined_terms],
        require_reviewed=True,
        expected_sha256=dictionary_sha,
    )
    print(f"terms={len(rows)}")
    print(f"combined_terms={combined_terms}")
    print(f"dictionary={dictionary}")
    print(f"dictionary_sha256={dictionary_sha}")
    print(f"preregistration={preregistration}")
    print(f"preregistration_sha256={preregistration_sha}")
    print(f"protocol={protocol}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms-dir", type=Path, default=Path("terms"))
    parser.add_argument("--term-file", type=Path, action="append")
    parser.add_argument("--exclude-term-file", action="append", default=sorted(DEFAULT_EXCLUDED_TERM_FILES))
    parser.add_argument("--base-protocol", type=Path, default=Path("protocols/centered_relevance_density.toml"))
    parser.add_argument("--out-dir", type=Path, default=Path("reports/crd_self_surface"))
    parser.add_argument("--seed-mode", choices=["self", "concept"], default="self")
    parser.add_argument("--locked-by", default="gpt-5-assisted-draft")
    parser.add_argument("--reviewer", default="gpt-5-assisted-draft")
    parser.add_argument("--drafted-with", default="gpt-5")
    parser.add_argument("--progress-interval-seconds", type=float, default=30)
    return parser


def resolve_term_files(args: argparse.Namespace) -> list[Path]:
    if args.term_file:
        return list(args.term_file)
    excluded = {Path(value).name for value in args.exclude_term_file}
    return [
        path
        for path in sorted(args.terms_dir.glob("*.csv"))
        if path.name not in excluded
    ]


def write_combined_terms(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TERM_FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_preregistration(
    path: Path,
    dictionary: Path,
    dictionary_sha: str,
    locked_by: str,
    *,
    seed_mode: str,
) -> None:
    scope = relevance_scope(seed_mode)
    path.write_text(
        f"""# CRD {seed_mode.title()}-Surface Preregistration

Status: locked local broad {seed_mode}-surface deterministic CRD screening run.

## Hypothesis

Hidden ELS hits whose centered surface text contains {scope} can be compared across Bible editions and language-matched secular controls. This is a screening run for exact surface coincidence only, not a broader free-form related-term interpretation.

## Term List Path

`{path.parent / "terms_combined.csv"}`

## Relevance Dictionary Path And Hash

- path: `{dictionary}`
- sha256: `{dictionary_sha}`

## Classifier Mode And Locked Parameters

- classifier_mode: `deterministic`
- llm_provider: `openai`
- llm_model: `gpt-5`
- llm_model_version: `gpt-5`
- llm_temperature: `0`
- llm_max_tokens: `200`
- max_api_calls: `0`
- max_estimated_cost_usd: `0`

## Corpora

Same corpus list as `protocols/centered_relevance_density.toml`.

## Skip Range

`2..100`

## Direction

`both`

## Decision Rule

For each `(term, corpus)`, count centered ELS hits whose context contains {scope}. Compare Bible maximum density against language-matched secular-control maximum density per term. Treat `exceeds_secular_max = true` as a review-priority flag only.

## Multiple Comparisons Correction

Benjamini-Hochberg q <= 0.05 if downstream p-values are computed. This screening run reports deterministic density only and does not itself compute p-values.

## Lock Date

2026-05-09

## Locked By

{locked_by}

## Reviewers

{locked_by}

## Locked Hash

Recorded in the generated local protocol after this document is locked.

## Sample Audit Log Review

Deterministic {seed_mode}-surface mode only. No LLM classification API calls are made and no LLM audit-log sample is required for execution.
""",
        encoding="utf-8",
    )


def write_protocol(
    path: Path,
    *,
    base_protocol: Path,
    combined_terms: Path,
    dictionary: Path,
    dictionary_sha: str,
    preregistration: Path,
    preregistration_sha: str,
    out_dir: Path,
    progress_interval_seconds: float,
    seed_mode: str,
) -> None:
    base_text = base_protocol.read_text(encoding="utf-8")
    base = tomllib.loads(base_text)
    corpus_blocks = extract_corpus_blocks(base_text)
    path.write_text(
        f"""name = "centered_relevance_density_{seed_mode}_surface"
description = "Local broad deterministic CRD run for hidden terms centered on {relevance_scope(seed_mode)}."
progress_interval_seconds = {progress_interval_seconds:g}

term_file = "{combined_terms.as_posix()}"
relevance_dictionary = "{dictionary.as_posix()}"
relevance_dictionary_sha256 = "{dictionary_sha}"
skip_range = "2..100"
direction = "both"
min_term_length = 3
max_hits_per_term = 200
classifier_mode = "deterministic"
llm_model = "{base["llm_model"]}"
llm_model_version = "{base["llm_model_version"]}"
llm_provider = "{base["llm_provider"]}"
system_prompt_path = "{base["system_prompt_path"]}"
system_prompt_sha256 = "{base["system_prompt_sha256"]}"
user_prompt_template_path = "{base["user_prompt_template_path"]}"
user_prompt_template_sha256 = "{base["user_prompt_template_sha256"]}"
llm_temperature = 0
llm_max_tokens = 200
max_api_calls = 0
max_estimated_cost_usd = 0
estimated_cost_per_call_usd = 0
output_dir = "{out_dir.as_posix()}"
preregistration_doc = "{preregistration.as_posix()}"
preregistration_sha256 = "{preregistration_sha}"

{corpus_blocks}
""",
        encoding="utf-8",
    )


def extract_corpus_blocks(text: str) -> str:
    start = text.index("[[corpus_list]]")
    match = re.search(r"\n\[\[steps\]\]", text[start:])
    end = start + match.start() if match else len(text)
    return text[start:end].strip()


def relevance_scope(seed_mode: str) -> str:
    if seed_mode == "concept":
        return "a visible spelling from a committed term row sharing the same language and concept"
    return "the term's own visible surface spelling"


if __name__ == "__main__":
    raise SystemExit(main())
