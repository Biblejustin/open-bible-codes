#!/usr/bin/env python3
"""Build matched Greek length-3 surface controls for the Gog exact-center row."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, load_corpus
from els.search import ELSHit
from els.skip_plan import max_skip_for_mode
from els.term_display import display_term
from scripts.build_gog_promoted_exact_center_source_review import (
    exact_center_hits_for_surface_words,
    hit_sort_key,
    path_row,
)


DEFAULT_OUT = Path("reports/dynamic_skip_focus/gog_length3_surface_control_review.csv")
DEFAULT_BY_SOURCE_OUT = Path("reports/dynamic_skip_focus/gog_length3_surface_control_by_source.csv")
DEFAULT_PATHS_OUT = Path("reports/dynamic_skip_focus/gog_length3_surface_control_path_examples.csv")
DEFAULT_MARKDOWN = Path("docs/DYNAMIC_SKIP_GOG_LENGTH3_SURFACE_CONTROL_REVIEW.md")
DEFAULT_MANIFEST = Path("reports/dynamic_skip_focus/gog_length3_surface_control_review.manifest.json")

DEFAULT_CORPORA = [
    ("TR_NT", "configs/example_ebible_grctr.toml"),
    ("BYZ_NT", "configs/example_ebible_grcmt.toml"),
    ("TCG_NT", "configs/example_ebible_grctcgnt.toml"),
    ("SBLGNT", "configs/example_sblgnt.toml"),
]

SUMMARY_FIELDNAMES = [
    "term",
    "is_target",
    "total_exact_center_paths",
    "sources_with_paths",
    "min_source_paths",
    "max_source_paths",
    "source_counts",
    "rank_desc",
    "rank_asc",
    "controls_ge_target",
    "controls_gt_target",
    "controls_le_target",
    "controls_lt_target",
    "read",
]

BY_SOURCE_FIELDNAMES = [
    "term",
    "is_target",
    "corpus",
    "surface_word_centers",
    "exact_center_paths",
    "max_skip",
    "skip_values",
]

PATH_FIELDNAMES = [
    "term",
    "is_target",
    "corpus",
    "path_rank",
    "skip",
    "direction",
    "span_letters",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_word",
    "row_width",
    "rows_spanned",
    "letter_path",
]


@dataclass(frozen=True)
class SourceResult:
    corpus: str
    max_skip: int
    surface_word_centers: int
    hits: tuple[ELSHit, ...]


@dataclass(frozen=True)
class TermResult:
    term: str
    is_target: bool
    sources: tuple[SourceResult, ...]

    @property
    def total_paths(self) -> int:
        return sum(len(source.hits) for source in self.sources)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.corpus is None:
        args.corpus = [f"{label}={config}" for label, config in DEFAULT_CORPORA]
    corpus_configs = parse_corpus_specs(args.corpus)
    corpora = {label: load_corpus(Path(config)) for label, config in corpus_configs}
    terms = matched_surface_terms(corpora, length=args.length, occurrences_per_source=args.occurrences_per_source)
    if args.target not in terms:
        raise SystemExit(f"target {args.target!r} not found in matched control universe")
    results = [
        review_term(
            term,
            corpora,
            target=args.target,
            min_skip=args.min_skip,
            max_skip_mode=args.max_skip_mode,
        )
        for term in terms
    ]
    summary_rows = summary_rows_for_results(results, target=args.target)
    by_source_rows = by_source_rows_for_results(results)
    path_rows = path_rows_for_results(results, corpora, limit_per_source=args.path_example_limit_per_source)
    write_csv(args.out, SUMMARY_FIELDNAMES, summary_rows)
    write_csv(args.by_source_out, BY_SOURCE_FIELDNAMES, by_source_rows)
    write_csv(args.paths_out, PATH_FIELDNAMES, path_rows)
    write_markdown(args.markdown_out, summary_rows, by_source_rows, path_rows, args)
    write_manifest(args.manifest_out, args, summary_rows, by_source_rows, path_rows, started)
    print(args.out)
    print(args.by_source_out)
    print(args.paths_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="γωγ")
    parser.add_argument("--length", type=int, default=3)
    parser.add_argument("--occurrences-per-source", type=int, default=1)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip-mode", choices=["full-span", "letters-per-term"], default="full-span")
    parser.add_argument("--corpus", action="append", default=None)
    parser.add_argument("--path-example-limit-per-source", type=int, default=5)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--by-source-out", type=Path, default=DEFAULT_BY_SOURCE_OUT)
    parser.add_argument("--paths-out", type=Path, default=DEFAULT_PATHS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def parse_corpus_specs(values: list[str]) -> list[tuple[str, str]]:
    specs = []
    for value in values:
        if "=" not in value:
            raise SystemExit(f"--corpus must be label=config_path: {value}")
        label, config = value.split("=", 1)
        specs.append((label, config))
    return specs


def matched_surface_terms(
    corpora: dict[str, Corpus],
    *,
    length: int,
    occurrences_per_source: int,
) -> list[str]:
    counts_by_label = {
        label: Counter(word.normalized_word for word in corpus.words if len(word.normalized_word) == length)
        for label, corpus in corpora.items()
    }
    common = set.intersection(*(set(counts) for counts in counts_by_label.values()))
    return sorted(
        term
        for term in common
        if all(counts_by_label[label][term] == occurrences_per_source for label in counts_by_label)
    )


def review_term(
    term: str,
    corpora: dict[str, Corpus],
    *,
    target: str,
    min_skip: int,
    max_skip_mode: str,
) -> TermResult:
    sources = []
    for label, corpus in corpora.items():
        max_skip = max_skip_for_mode(len(corpus.text), len(term), max_skip_mode)
        surface_words = tuple(word for word in corpus.words if word.normalized_word == term)
        hits = tuple(
            exact_center_hits_for_surface_words(
                corpus,
                term,
                term,
                surface_words,
                min_skip=min_skip,
                max_skip=max_skip,
            )
        )
        sources.append(
            SourceResult(
                corpus=label,
                max_skip=max_skip,
                surface_word_centers=len(surface_words),
                hits=hits,
            )
        )
    return TermResult(term=term, is_target=term == target, sources=tuple(sources))


def summary_rows_for_results(results: list[TermResult], *, target: str) -> list[dict[str, object]]:
    target_result = next(result for result in results if result.term == target)
    target_total = target_result.total_paths
    totals = [result.total_paths for result in results]
    sorted_desc = sorted(results, key=lambda result: (-result.total_paths, result.term))
    sorted_asc = sorted(results, key=lambda result: (result.total_paths, result.term))
    desc_rank = {result.term: index for index, result in enumerate(sorted_desc, start=1)}
    asc_rank = {result.term: index for index, result in enumerate(sorted_asc, start=1)}
    rows = []
    for result in sorted_desc:
        source_counts = {source.corpus: len(source.hits) for source in result.sources}
        rows.append(
            {
                "term": result.term,
                "is_target": result.is_target,
                "total_exact_center_paths": result.total_paths,
                "sources_with_paths": sum(count > 0 for count in source_counts.values()),
                "min_source_paths": min(source_counts.values()),
                "max_source_paths": max(source_counts.values()),
                "source_counts": format_source_counts(source_counts),
                "rank_desc": desc_rank[result.term],
                "rank_asc": asc_rank[result.term],
                "controls_ge_target": sum(total >= target_total for total in totals),
                "controls_gt_target": sum(total > target_total for total in totals),
                "controls_le_target": sum(total <= target_total for total in totals),
                "controls_lt_target": sum(total < target_total for total in totals),
                "read": read_for_result(result, target_total),
            }
        )
    return rows


def by_source_rows_for_results(results: list[TermResult]) -> list[dict[str, object]]:
    rows = []
    for result in sorted(results, key=lambda item: item.term):
        for source in result.sources:
            skip_values = sorted({hit.skip for hit in source.hits}, key=lambda value: (abs(value), value))
            rows.append(
                {
                    "term": result.term,
                    "is_target": result.is_target,
                    "corpus": source.corpus,
                    "surface_word_centers": source.surface_word_centers,
                    "exact_center_paths": len(source.hits),
                    "max_skip": source.max_skip,
                    "skip_values": ";".join(str(value) for value in skip_values[:20]),
                }
            )
    return rows


def path_rows_for_results(
    results: list[TermResult],
    corpora: dict[str, Corpus],
    *,
    limit_per_source: int,
) -> list[dict[str, object]]:
    rows = []
    for result in sorted(results, key=lambda item: (not item.is_target, -item.total_paths, item.term)):
        for source in result.sources:
            review = type(
                "Review",
                (),
                {
                    "label": source.corpus,
                    "corpus": corpora[source.corpus],
                },
            )()
            for path_rank, hit in enumerate(sorted(source.hits, key=hit_sort_key)[:limit_per_source], start=1):
                detail = path_row(review, path_rank, hit)
                rows.append(
                    {
                        "term": result.term,
                        "is_target": result.is_target,
                        "corpus": source.corpus,
                        "path_rank": path_rank,
                        "skip": detail["skip"],
                        "direction": detail["direction"],
                        "span_letters": detail["span_letters"],
                        "start_ref": detail["start_ref"],
                        "center_ref": detail["center_ref"],
                        "end_ref": detail["end_ref"],
                        "center_word": detail["center_word"],
                        "row_width": detail["row_width"],
                        "rows_spanned": detail["rows_spanned"],
                        "letter_path": detail["letter_path"],
                    }
                )
    return rows


def read_for_result(result: TermResult, target_total: int) -> str:
    if result.is_target and result.total_paths == target_total:
        return "target term"
    if result.total_paths > target_total:
        return "matched control exceeds target"
    if result.total_paths == target_total:
        return "matched control equals target"
    return "matched control below target"


def format_source_counts(counts: dict[str, int]) -> str:
    return ";".join(f"{label}:{counts[label]}" for label in sorted(counts))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    by_source_rows: list[dict[str, object]],
    path_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    target = next(row for row in summary_rows if str(row["term"]) == args.target)
    control_count = len(summary_rows) - 1
    lines = [
        "# Gog Length-3 Surface Control Review",
        "",
        f"This report builds matched Greek controls for the promoted {display_gog_term(args.target)} exact-center",
        "row. The control universe is normalized Greek surface words of length 3",
        "that occur exactly once in every compared Greek NT source.",
        "",
        "## Reproduce",
        "",
        "```bash",
        command_line(args),
        "```",
        "",
        "## Bottom Line",
        "",
        f"- matched term universe: {len(summary_rows):,} terms, including target {display_gog_term(args.target)}",
        f"- non-target controls: {control_count:,}",
        f"- target total exact-center paths: {int(target['total_exact_center_paths']):,}",
        f"- controls above target: {int(target['controls_gt_target']):,} of {control_count:,}",
        f"- controls below target: {int(target['controls_lt_target']):,} of {control_count:,}",
        f"- target rank by descending exact-center paths: {target['rank_desc']} of {len(summary_rows):,}",
        f"- target rank by ascending exact-center paths: {target['rank_asc']} of {len(summary_rows):,}",
        "",
        f"Current read: {display_gog_term(args.target)} remains a contextually meaningful centered-self",
        "occurrence, not a frequency-promoted row. The hidden word centers on the",
        "open Gog word in the Gog/Magog verse across all compared Greek NT streams.",
        "The matched controls only say its path count is not unusually high among",
        "comparable length-3 surface words.",
        "",
    ]
    lines.extend(summary_table(summary_rows))
    lines.extend(by_source_table(by_source_rows, args.target))
    lines.extend(path_table(path_rows, args.target))
    lines.extend(read_lines())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summary_table(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "## Matched Terms",
        "",
        "| Rank desc | Rank asc | Term | Target | Total paths | Source counts | Read |",
        "| ---: | ---: | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['rank_desc']} | {row['rank_asc']} | {display_gog_term(str(row['term']))} | "
            f"{row['is_target']} | {int(row['total_exact_center_paths']):,} | "
            f"`{row['source_counts']}` | {row['read']} |"
        )
    lines.append("")
    return lines


def by_source_table(rows: list[dict[str, object]], target: str) -> list[str]:
    selected = [row for row in rows if row["term"] == target]
    lines = [
        "## Target By Source",
        "",
        "| Corpus | Surface centers | Exact-center paths | Max skip | Skip values |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in selected:
        lines.append(
            f"| {row['corpus']} | {row['surface_word_centers']} | "
            f"{row['exact_center_paths']} | {int(row['max_skip']):,} | `{row['skip_values']}` |"
        )
    lines.append("")
    return lines


def path_table(rows: list[dict[str, object]], target: str) -> list[str]:
    selected = [row for row in rows if row["term"] == target]
    lines = [
        "## Target Path Examples",
        "",
        "| Corpus | Path | Skip | Span | Letter path |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for row in selected:
        span = f"{row['start_ref']} -> {row['center_ref']} -> {row['end_ref']}"
        lines.append(
            f"| {row['corpus']} | {row['path_rank']} | {row['skip']} | "
            f"{md_cell(span)} | {md_cell(row['letter_path'])} |"
        )
    lines.append("")
    return lines


def read_lines() -> list[str]:
    return [
        "## Read",
        "",
        "- This is a post-discovery matched control, not a preregistered claim test.",
        "- The control is still valuable because it matches the key mechanics: Greek, length 3, full-span skip, exact-center surface word, one surface occurrence per source.",
        f"- {display_gog_term('γωγ')} being source-stable and centered on the Gog/Magog verse is the contextual finding to preserve.",
        "- The matched-control count is a frequency caution, not a reason to remove the centered-self occurrence from the final report.",
        "- A stronger future test would preregister a length-3 surface-control universe before selecting a target.",
        "",
    ]


def display_gog_term(term: str) -> str:
    english = "Gog" if term == "γωγ" else None
    return display_term(term, english=english)


def command_line(args: argparse.Namespace) -> str:
    corpora = " ".join(f"--corpus {value}" for value in args.corpus)
    return (
        "python3 -m scripts.build_gog_length3_surface_control_review "
        f"--target {args.target} --length {args.length} "
        f"--occurrences-per-source {args.occurrences_per_source} "
        f"--min-skip {args.min_skip} --max-skip-mode {args.max_skip_mode} "
        f"{corpora} --out {args.out} --by-source-out {args.by_source_out} "
        f"--paths-out {args.paths_out} --markdown-out {args.markdown_out} "
        f"--manifest-out {args.manifest_out}"
    )


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary_rows: list[dict[str, object]],
    by_source_rows: list[dict[str, object]],
    path_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_gog_length3_surface_control_review",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "git_commit": git_commit(),
        "summary_rows": len(summary_rows),
        "by_source_rows": len(by_source_rows),
        "path_rows": len(path_rows),
        "inputs": {
            "target": args.target,
            "length": args.length,
            "occurrences_per_source": args.occurrences_per_source,
            "min_skip": args.min_skip,
            "max_skip_mode": args.max_skip_mode,
            "corpus": args.corpus,
        },
        "outputs": {
            "out": str(args.out),
            "by_source_out": str(args.by_source_out),
            "paths_out": str(args.paths_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
