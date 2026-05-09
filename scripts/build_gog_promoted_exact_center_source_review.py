#!/usr/bin/env python3
"""Review the promoted Gog exact-center row across Greek NT sources."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, WordSpan, load_corpus
from els.search import ELSHit, build_hit, normalize_for_corpus
from els.skip_plan import max_skip_for_mode


DEFAULT_OUT = Path("reports/dynamic_skip_focus/gog_promoted_exact_center_source_review.csv")
DEFAULT_PATHS_OUT = Path("reports/dynamic_skip_focus/gog_promoted_exact_center_source_review_paths.csv")
DEFAULT_MARKDOWN = Path("docs/DYNAMIC_SKIP_GOG_PROMOTED_EXACT_CENTER_SOURCE_REVIEW.md")
DEFAULT_MANIFEST = Path("reports/dynamic_skip_focus/gog_promoted_exact_center_source_review.manifest.json")

DEFAULT_CORPORA = [
    ("TR_NT", "configs/example_ebible_grctr.toml"),
    ("BYZ_NT", "configs/example_ebible_grcmt.toml"),
    ("TCG_NT", "configs/example_ebible_grctcgnt.toml"),
    ("SBLGNT", "configs/example_sblgnt.toml"),
]

SUMMARY_FIELDNAMES = [
    "corpus",
    "config",
    "letters",
    "normalized_term",
    "max_skip",
    "surface_word_centers",
    "exact_center_paths",
    "distinct_center_refs",
    "center_refs",
    "skip_values",
    "read",
]

PATH_FIELDNAMES = [
    "corpus",
    "path_rank",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "span_letters",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_word_index",
    "center_word",
    "center_normalized_word",
    "start_offset",
    "center_offset",
    "end_offset",
    "row_width",
    "rows_spanned",
    "cols_spanned",
    "letter_path",
]


@dataclass(frozen=True)
class CorpusReview:
    label: str
    config: Path
    corpus: Corpus
    letters: int
    normalized_term: str
    max_skip: int
    surface_words: tuple[WordSpan, ...]
    hits: tuple[ELSHit, ...]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.corpus is None:
        args.corpus = [f"{label}={config}" for label, config in DEFAULT_CORPORA]
    corpus_specs = parse_corpus_specs(args.corpus)
    reviews = [
        review_corpus(label, Path(config), args.term, args.min_skip, args.max_skip_mode)
        for label, config in corpus_specs
    ]
    summary_rows = [summary_row(review) for review in reviews]
    path_rows = [
        path_row(review, path_rank, hit)
        for review in reviews
        for path_rank, hit in enumerate(sorted(review.hits, key=hit_sort_key), start=1)
    ]
    write_csv(args.out, SUMMARY_FIELDNAMES, summary_rows)
    write_csv(args.paths_out, PATH_FIELDNAMES, path_rows)
    write_markdown(args.markdown_out, reviews, summary_rows, path_rows, args)
    write_manifest(args.manifest_out, args, summary_rows, path_rows, started)
    print(args.out)
    print(args.paths_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--term", default="γωγ")
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip-mode", choices=["full-span", "letters-per-term"], default="full-span")
    parser.add_argument(
        "--corpus",
        action="append",
        default=None,
        help="label=config_path; may be repeated",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
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


def review_corpus(
    label: str,
    config: Path,
    term: str,
    min_skip: int,
    max_skip_mode: str,
) -> CorpusReview:
    corpus = load_corpus(config)
    normalized = normalize_for_corpus(corpus, term)
    if len(normalized) % 2 == 0:
        raise SystemExit("promoted exact-center source review currently requires an odd-length term")
    max_skip = max_skip_for_mode(len(corpus.text), len(normalized), max_skip_mode)
    surface_words = tuple(word for word in corpus.words if word.normalized_word == normalized)
    hits = tuple(
        exact_center_hits_for_surface_words(
            corpus,
            term,
            normalized,
            surface_words,
            min_skip=min_skip,
            max_skip=max_skip,
        )
    )
    return CorpusReview(
        label=label,
        config=config,
        corpus=corpus,
        letters=len(corpus.text),
        normalized_term=normalized,
        max_skip=max_skip,
        surface_words=surface_words,
        hits=hits,
    )


def exact_center_hits_for_surface_words(
    corpus: Corpus,
    term: str,
    normalized: str,
    surface_words: tuple[WordSpan, ...],
    *,
    min_skip: int,
    max_skip: int,
) -> list[ELSHit]:
    midpoint = len(normalized) // 2
    hits: list[ELSHit] = []
    seen: set[tuple[int, int, int]] = set()
    for word in surface_words:
        for center_offset in range(word.norm_start, word.norm_end + 1):
            if corpus.text[center_offset] != normalized[midpoint]:
                continue
            for skip in range(min_skip, max_skip + 1):
                forward_start = center_offset - midpoint * skip
                forward_end = center_offset + (len(normalized) - midpoint - 1) * skip
                if matches_at(corpus.text, normalized, forward_start, skip):
                    key = (skip, forward_start, forward_end)
                    if key not in seen:
                        seen.add(key)
                        hits.append(build_hit(corpus, term, normalized, skip, forward_start, forward_end))
                backward_start = center_offset + midpoint * skip
                backward_end = center_offset - (len(normalized) - midpoint - 1) * skip
                if matches_at(corpus.text, normalized, backward_start, -skip):
                    key = (-skip, backward_start, backward_end)
                    if key not in seen:
                        seen.add(key)
                        hits.append(build_hit(corpus, term, normalized, -skip, backward_start, backward_end))
    return hits


def matches_at(text: str, query: str, start: int, skip: int) -> bool:
    end = start + (len(query) - 1) * skip
    if min(start, end) < 0 or max(start, end) >= len(text):
        return False
    for index, char in enumerate(query):
        if text[start + index * skip] != char:
            return False
    return True


def summary_row(review: CorpusReview) -> dict[str, object]:
    center_refs = Counter(hit.center_ref for hit in review.hits)
    skip_values = sorted({hit.skip for hit in review.hits}, key=lambda value: (abs(value), value))
    return {
        "corpus": review.label,
        "config": str(review.config),
        "letters": review.letters,
        "normalized_term": review.normalized_term,
        "max_skip": review.max_skip,
        "surface_word_centers": len(review.surface_words),
        "exact_center_paths": len(review.hits),
        "distinct_center_refs": len(center_refs),
        "center_refs": format_counter(center_refs),
        "skip_values": ";".join(str(value) for value in skip_values),
        "read": source_read(review),
    }


def source_read(review: CorpusReview) -> str:
    if not review.surface_words:
        return "surface term absent in this source"
    if not review.hits:
        return "surface term present, but no exact-center hidden path found"
    if review.label == "TCG_NT":
        return "promoted source retains exact-center hidden paths"
    return "comparison source also has exact-center hidden paths"


def path_row(review: CorpusReview, path_rank: int, hit: ELSHit) -> dict[str, object]:
    width = abs(hit.skip)
    letter_positions = [hit.start_offset + index * hit.skip for index in range(len(hit.normalized_term))]
    rows = [position // width for position in letter_positions]
    cols = [position % width for position in letter_positions]
    return {
        "corpus": review.label,
        "path_rank": path_rank,
        "term": hit.term,
        "normalized_term": hit.normalized_term,
        "skip": hit.skip,
        "direction": hit.direction,
        "span_letters": hit.span_letters,
        "start_ref": hit.start_ref,
        "center_ref": hit.center_ref,
        "end_ref": hit.end_ref,
        "center_word_index": hit.center_word_index,
        "center_word": hit.center_word,
        "center_normalized_word": hit.center_normalized_word,
        "start_offset": hit.start_offset,
        "center_offset": hit.center_offset,
        "end_offset": hit.end_offset,
        "row_width": width,
        "rows_spanned": max(rows) - min(rows) + 1,
        "cols_spanned": max(cols) - min(cols) + 1,
        "letter_path": format_letter_path(review, hit),
    }


def format_letter_path(review: CorpusReview, hit: ELSHit) -> str:
    width = abs(hit.skip)
    parts = []
    for index, letter in enumerate(hit.normalized_term):
        offset = hit.start_offset + index * hit.skip
        word = review.corpus.word_at(offset)
        raw_word = word.raw_word if word is not None else ""
        parts.append(f"{letter}@{review.corpus.ref_at(offset)}:{raw_word}[r{offset // width},c{offset % width}]")
    return " | ".join(parts)


def hit_sort_key(hit: ELSHit) -> tuple[int, int, int]:
    return (abs(hit.skip), hit.skip, min(hit.start_offset, hit.end_offset))


def format_counter(counter: Counter[str], limit: int = 8) -> str:
    return "; ".join(f"{key}={value}" for key, value in counter.most_common(limit))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    reviews: list[CorpusReview],
    summary_rows: list[dict[str, object]],
    path_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Gog Promoted Exact-Center Source Review",
        "",
        "This report follows up the promoted original-language exact-center finding:",
        "Greek `γωγ` centered on open `Γὼγ` at `REV 20:8` in `TCG_NT`.",
        "It checks the same exact-center condition directly against Greek NT sources",
        "without exporting every full-span hit.",
        "",
        "## Reproduce",
        "",
        "```bash",
        command_line(args),
        "```",
        "",
        "## Bottom Line",
        "",
    ]
    lines.extend(bottom_line(reviews))
    lines.extend(summary_table(summary_rows))
    lines.extend(path_table(path_rows))
    lines.extend(read_lines())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def bottom_line(reviews: list[CorpusReview]) -> list[str]:
    exact_sources = [review.label for review in reviews if review.hits]
    zero_sources = [review.label for review in reviews if review.surface_words and not review.hits]
    absent_sources = [review.label for review in reviews if not review.surface_words]
    lines = [
        f"- sources with exact-center `γωγ` paths: {', '.join(exact_sources) if exact_sources else 'none'}",
        f"- sources with open `γωγ` but no exact-center path: {', '.join(zero_sources) if zero_sources else 'none'}",
        f"- sources where normalized open `γωγ` was absent: {', '.join(absent_sources) if absent_sources else 'none'}",
        "- `TCG_NT` has four exact-center paths: skip `±17` inside `REV 20:8`, and skip `±4568` spanning `REV 18:16` / `REV 20:8` / `REV 22:8`.",
        "- This is a contextually meaningful centered-self occurrence: hidden `γωγ` centers on open `Gog` in the Gog/Magog verse across all compared sources.",
        "- Frequency strength must be reported separately because the term is only three letters and the surface word supplies the center anchor.",
        "",
    ]
    return lines


def summary_table(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "## Source Comparison",
        "",
        "| Corpus | Letters | Max skip | Surface centers | Exact-center paths | Center refs | Skip values | Read |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['corpus']} | {int(row['letters']):,} | {int(row['max_skip']):,} | "
            f"{int(row['surface_word_centers']):,} | {int(row['exact_center_paths']):,} | "
            f"{md_cell(row['center_refs'])} | `{row['skip_values']}` | {md_cell(row['read'])} |"
        )
    lines.append("")
    return lines


def path_table(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "## Exact-Center Paths",
        "",
        "| Corpus | Path | Skip | Span | Matrix | Letter path |",
        "| --- | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        span = f"{row['start_ref']} -> {row['center_ref']} -> {row['end_ref']}"
        matrix = f"{row['rows_spanned']} rows @ width {row['row_width']}"
        lines.append(
            f"| {row['corpus']} | {row['path_rank']} | {row['skip']} | {md_cell(span)} | "
            f"{md_cell(matrix)} | {md_cell(row['letter_path'])} |"
        )
    lines.append("")
    return lines


def read_lines() -> list[str]:
    return [
        "## Read",
        "",
        "- This direct scan asks whether the hidden `γωγ` path centers on an open surface `γωγ` word.",
        "- The existence of that centered-self occurrence is the finding to preserve in the final report.",
        "- It does not claim frequency significance by itself; that question belongs to matched controls and source-version comparison.",
        "- Because `γωγ` is length 3, the report should show both axes: contextual relevance and frequency/control strength.",
        "",
    ]


def command_line(args: argparse.Namespace) -> str:
    corpora = " ".join(f"--corpus {value}" for value in args.corpus)
    return (
        "python3 -m scripts.build_gog_promoted_exact_center_source_review "
        f"--term {args.term} --min-skip {args.min_skip} --max-skip-mode {args.max_skip_mode} "
        f"{corpora} --out {args.out} --paths-out {args.paths_out} "
        f"--markdown-out {args.markdown_out} --manifest-out {args.manifest_out}"
    )


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary_rows: list[dict[str, object]],
    path_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_gog_promoted_exact_center_source_review",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "git_commit": git_commit(),
        "summary_rows": len(summary_rows),
        "path_rows": len(path_rows),
        "inputs": {
            "term": args.term,
            "min_skip": args.min_skip,
            "max_skip_mode": args.max_skip_mode,
            "corpus": args.corpus,
        },
        "outputs": {
            "out": str(args.out),
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
