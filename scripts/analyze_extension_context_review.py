#!/usr/bin/env python3
"""Build manual context review rows for strict NT extension overlaps."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, VerseSpan, load_corpus
from els.normalization import normalize_text


BASE = Path("reports/protocols/public_baseline")
TOP_FILES = [
    BASE / "surface_context_extensions_tr_nt_top.csv",
    BASE / "surface_context_extensions_sblgnt_top.csv",
]
CONTROL_SUMMARY = Path("reports/extension_overlap_controls_summary.csv")
SURFACE_CONTEXT_HITS = BASE / "surface_context_hits.csv"
CORPUS_CONFIGS = {
    "TR_NT": Path("configs/example_ebible_grctr.toml"),
    "BYZ_NT": Path("configs/example_ebible_grcmt.toml"),
    "TCG_NT": Path("configs/example_ebible_grctcgnt.toml"),
    "SBLGNT": Path("configs/example_sblgnt.toml"),
}

SUMMARY_OUT = Path("reports/extension_context_review_summary.csv")
MD_OUT = Path("reports/extension_context_review.md")
LETTER_PATHS_OUT = Path("reports/extension_letter_paths.md")
MANIFEST_OUT = Path("reports/extension_context_review.manifest.json")

FIELDNAMES = [
    "overlap_key",
    "corpus",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "extension_type",
    "extended_sequence",
    "matched_examples",
    "matched_refs",
    "control_band",
    "combined_min_p",
    "combined_min_q",
    "term_id",
    "concept",
    "category",
    "best_context",
    "center_exact",
    "center_same_concept",
    "center_same_category",
    "span_exact",
    "span_same_concept",
    "span_same_category",
    "center_same_concept_terms",
    "center_same_category_terms",
    "span_exact_refs",
    "span_same_concept_refs",
    "span_same_category_refs",
    "promotion_gate",
    "start_offset",
    "end_offset",
    "extension_start_offset",
    "extension_end_offset",
    "hit_refs",
    "extension_refs",
    "center_ref",
    "center_word",
    "center_normalized_word",
    "center_has_term_surface",
    "hit_span_has_term_surface",
    "extension_span_has_matched_phrase_surface",
    "center_verse_text",
    "hit_verse_text",
    "extension_verse_text",
    "previous_verse_text",
    "next_verse_text",
    "letter_path",
    "context_read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    top_rows = read_rows_many(args.top_file or TOP_FILES)
    controls = read_controls(args.controls)
    surface_context = read_surface_context(args.surface_context_hits)
    targets = selected_review_rows(top_rows, surface_context, args)
    if args.require_control_row:
        targets = rows_with_controls(targets, controls)
    corpora = load_needed_corpora(targets)
    rows = [
        context_row(row, corpora[row["corpus"]], controls, surface_context)
        for row in targets
    ]
    rows.sort(key=lambda row: (row["overlap_key"], row["corpus"]))
    write_rows(args.summary_out, rows)
    write_markdown(args.markdown_out, rows, args.title, args.description)
    write_letter_paths(args.letter_paths_out, rows, corpora, args.title, args.description)
    write_manifest(args, len(top_rows), len(targets), len(rows), started)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.letter_paths_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-file", action="append", type=Path)
    parser.add_argument("--controls", type=Path, default=CONTROL_SUMMARY)
    parser.add_argument("--surface-context-hits", type=Path, default=SURFACE_CONTEXT_HITS)
    parser.add_argument("--require-center-exact", action="store_true")
    parser.add_argument(
        "--require-control-row",
        action="store_true",
        help="review only rows present in the controls summary",
    )
    parser.add_argument("--dedupe-targets", action="store_true")
    parser.add_argument("--title", default="Extension Context Review")
    parser.add_argument(
        "--description",
        default="Manual context review for strict TR_NT/SBLGNT extension overlaps.",
    )
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--letter-paths-out", type=Path, default=LETTER_PATHS_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows_many(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows.extend(csv.DictReader(handle))
    return rows


def selected_review_rows(
    rows: list[dict[str, str]],
    surface_context: dict[tuple[str, ...], dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    if args.require_center_exact:
        return exact_center_rows(rows, surface_context, dedupe=args.dedupe_targets)
    return strict_cross_corpus_overlap_rows(rows)


def exact_center_rows(
    rows: list[dict[str, str]],
    surface_context: dict[tuple[str, ...], dict[str, str]],
    *,
    dedupe: bool,
) -> list[dict[str, str]]:
    output = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        surface_row = surface_context.get(surface_context_key(row), {})
        if not is_true(surface_row.get("center_exact", "")):
            continue
        copied = dict(row)
        copied["overlap_key"] = overlap_key(row)
        dedupe_key = (copied["corpus"], copied["overlap_key"])
        if dedupe and dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        output.append(copied)
    return output


def strict_cross_corpus_overlap_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[overlap_key(row)].append(row)
    output: list[dict[str, str]] = []
    for key, group in groups.items():
        if len({row["corpus"] for row in group}) < 2:
            continue
        seen_corpora: set[str] = set()
        for row in group:
            corpus = row["corpus"]
            if corpus in seen_corpora:
                continue
            seen_corpora.add(corpus)
            copied = dict(row)
            copied["overlap_key"] = key
            output.append(copied)
    return output


def overlap_key(row: dict[str, str]) -> str:
    return "|".join(
        row.get(field, "")
        for field in [
            "normalized_term",
            "skip",
            "direction",
            "extension_type",
            "extended_sequence",
            "matched_normalized",
        ]
    )


def read_controls(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {
            (row["corpus"], row["overlap_key"]): row
            for row in csv.DictReader(handle)
        }


def rows_with_controls(
    rows: list[dict[str, str]],
    controls: dict[tuple[str, str], dict[str, str]],
) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if (row["corpus"], row.get("overlap_key", overlap_key(row))) in controls
    ]


def read_surface_context(path: Path) -> dict[tuple[str, ...], dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {surface_context_key(row): row for row in csv.DictReader(handle)}


def surface_context_key(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row.get("corpus", ""),
        row.get("term", ""),
        row.get("normalized_term", ""),
        row.get("skip", ""),
        row.get("start_offset", ""),
        row.get("end_offset", ""),
        row.get("center_offset", ""),
    )


def load_needed_corpora(rows: list[dict[str, str]]) -> dict[str, Corpus]:
    corpora = {}
    for corpus_label in sorted({row["corpus"] for row in rows}):
        corpora[corpus_label] = load_corpus(CORPUS_CONFIGS[corpus_label])
    return corpora


def context_row(
    row: dict[str, str],
    corpus: Corpus,
    controls: dict[tuple[str, str], dict[str, str]],
    surface_context: dict[tuple[str, ...], dict[str, str]],
) -> dict[str, str]:
    control = controls.get((row["corpus"], row["overlap_key"]), {})
    surface_row = surface_context.get(surface_context_key(row), {})
    hit_verses = verses_for_offsets(
        corpus,
        safe_int(row["start_offset"]),
        safe_int(row["end_offset"]),
    )
    extension_verses = verses_for_offsets(
        corpus,
        safe_int(row["extension_start_offset"]),
        safe_int(row["extension_end_offset"]),
    )
    center_verse = verse_for_offset(corpus, safe_int(row["center_offset"]))
    previous_verse = adjacent_verse(corpus, center_verse, -1)
    next_verse = adjacent_verse(corpus, center_verse, 1)
    normalized_term = row["normalized_term"]
    matched_normalized = row["matched_normalized"]
    center_norm = normalize_text(center_verse.raw_text, corpus.language)
    hit_norm = normalize_text(" ".join(verse.raw_text for verse in hit_verses), corpus.language)
    extension_norm = normalize_text(
        " ".join(verse.raw_text for verse in extension_verses),
        corpus.language,
    )
    center_has_term = normalized_term in center_norm
    hit_has_term = normalized_term in hit_norm
    extension_has_phrase = matched_normalized in extension_norm
    return {
        "overlap_key": row["overlap_key"],
        "corpus": row["corpus"],
        "term": row["term"],
        "normalized_term": normalized_term,
        "skip": row["skip"],
        "direction": row["direction"],
        "extension_type": row["extension_type"],
        "extended_sequence": row["extended_sequence"],
        "matched_examples": row["matched_examples"],
        "matched_refs": row["matched_refs"],
        "control_band": control.get("extension_band", ""),
        "combined_min_p": control.get("combined_min_p", ""),
        "combined_min_q": control.get("combined_min_q", ""),
        "term_id": surface_row.get("term_id", ""),
        "concept": surface_row.get("concept", ""),
        "category": surface_row.get("category", ""),
        "best_context": surface_row.get("best_context", ""),
        "center_exact": surface_row.get("center_exact", ""),
        "center_same_concept": surface_row.get("center_same_concept", ""),
        "center_same_category": surface_row.get("center_same_category", ""),
        "span_exact": surface_row.get("span_exact", ""),
        "span_same_concept": surface_row.get("span_same_concept", ""),
        "span_same_category": surface_row.get("span_same_category", ""),
        "center_same_concept_terms": surface_row.get("center_same_concept_terms", ""),
        "center_same_category_terms": surface_row.get("center_same_category_terms", ""),
        "span_exact_refs": surface_row.get("span_exact_refs", ""),
        "span_same_concept_refs": surface_row.get("span_same_concept_refs", ""),
        "span_same_category_refs": surface_row.get("span_same_category_refs", ""),
        "promotion_gate": promotion_gate(surface_row),
        "start_offset": row["start_offset"],
        "end_offset": row["end_offset"],
        "extension_start_offset": row["extension_start_offset"],
        "extension_end_offset": row["extension_end_offset"],
        "hit_refs": refs_cell(hit_verses),
        "extension_refs": refs_cell(extension_verses),
        "center_ref": center_verse.ref,
        "center_word": row.get("center_word", ""),
        "center_normalized_word": row.get("center_normalized_word", ""),
        "center_has_term_surface": yes_no(center_has_term),
        "hit_span_has_term_surface": yes_no(hit_has_term),
        "extension_span_has_matched_phrase_surface": yes_no(extension_has_phrase),
        "center_verse_text": center_verse.raw_text,
        "hit_verse_text": verses_cell(hit_verses),
        "extension_verse_text": verses_cell(extension_verses),
        "previous_verse_text": verse_cell(previous_verse),
        "next_verse_text": verse_cell(next_verse),
        "letter_path": letter_path(
            corpus,
            row["extended_sequence"],
            safe_int(row["extension_start_offset"]),
            safe_int(row["skip"]),
        ),
        "context_read": context_read(center_has_term, hit_has_term, extension_has_phrase),
    }


def verses_for_offsets(corpus: Corpus, first: int, second: int) -> tuple[VerseSpan, ...]:
    low, high = sorted((first, second))
    start_index = corpus.position_to_verse[low]
    end_index = corpus.position_to_verse[high]
    return tuple(corpus.verses[start_index : end_index + 1])


def verse_for_offset(corpus: Corpus, offset: int) -> VerseSpan:
    return corpus.verses[corpus.position_to_verse[offset]]


def adjacent_verse(corpus: Corpus, verse: VerseSpan, delta: int) -> VerseSpan | None:
    index = corpus.position_to_verse[verse.norm_start]
    adjacent_index = index + delta
    if adjacent_index < 0 or adjacent_index >= len(corpus.verses):
        return None
    return corpus.verses[adjacent_index]


def letter_path(corpus: Corpus, sequence: str, start_offset: int, skip: int) -> str:
    parts = []
    for index, letter in enumerate(sequence):
        offset = start_offset + index * skip
        if offset < 0 or offset >= len(corpus.text):
            break
        parts.append(f"{letter}@{corpus.ref_at(offset)}:{offset}")
    return ";".join(parts)


def context_read(
    center_has_term: bool,
    hit_has_term: bool,
    extension_has_phrase: bool,
) -> str:
    if extension_has_phrase:
        return "matched phrase appears as surface text in extension span"
    if center_has_term:
        return "base normalized string appears in center verse surface text"
    if hit_has_term:
        return "base normalized string appears in hit-span surface text"
    return "ELS-only at hit span; matched phrase appears elsewhere in corpus"


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    title: str,
    description: str,
) -> None:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["overlap_key"]].append(row)
    lines = [
        f"# {title}",
        "",
        description,
        "",
        "## Summary",
        "",
        "| Read | Rows |",
        "| --- | ---: |",
    ]
    read_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        read_counts[row["context_read"]] += 1
    for read, count in sorted(read_counts.items()):
        lines.append(f"| {read} | {count} |")
    lines.extend(["", "## Promotion Gates", "", "| Gate | Rows |", "| --- | ---: |"])
    gate_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        gate_counts[row["promotion_gate"]] += 1
    for gate, count in sorted(gate_counts.items()):
        lines.append(f"| `{gate}` | {count} |")
    for key, group in sorted(grouped.items()):
        lines.extend(["", f"## `{key}`", ""])
        lines.extend(
            [
                "| Corpus | Center | Hit refs | Gate | Surface checks | Control |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in sorted(group, key=lambda item: item["corpus"]):
            checks = (
                f"center term={row['center_has_term_surface']}; "
                f"hit term={row['hit_span_has_term_surface']}; "
                f"extension phrase={row['extension_span_has_matched_phrase_surface']}"
            )
            control = f"{row['control_band']} q={row['combined_min_q']}"
            lines.append(
                "| "
                + " | ".join(
                    [
                        row["corpus"],
                        f"{row['center_ref']} `{row['center_word']}`",
                        row["hit_refs"],
                        f"`{row['promotion_gate']}`",
                        checks,
                        control,
                    ]
                )
                + " |"
            )
        lines.extend(["", "Context excerpts:"])
        for row in sorted(group, key=lambda item: item["corpus"]):
            lines.append("")
            lines.append(f"- {row['corpus']} {row['center_ref']}: {row['center_verse_text']}")
            if row["hit_verse_text"] != row["center_verse_text"]:
                lines.append(f"  Hit span: {row['hit_verse_text']}")
            if row["extension_verse_text"] != row["hit_verse_text"]:
                lines.append(f"  Extension span: {row['extension_verse_text']}")
            lines.append(f"  Read: {row['context_read']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_letter_paths(
    path: Path,
    rows: list[dict[str, str]],
    corpora: dict[str, Corpus],
    title: str,
    description: str,
) -> None:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["overlap_key"]].append(row)
    lines = [
        f"# {title} Letter Paths",
        "",
        description,
        "",
        "Role legend: `term` = declared base ELS term; `after`/`before` = same-skip extension letters.",
    ]
    for key, group in sorted(grouped.items()):
        lines.extend(["", f"## `{key}`"])
        for row in sorted(group, key=lambda item: item["corpus"]):
            corpus = corpora[row["corpus"]]
            lines.extend(
                [
                    "",
                    f"### {row['corpus']} {row['hit_refs']}",
                    "",
                    f"- ELS: `{row['extended_sequence']}`",
                    f"- Skip: `{row['skip']}` {row['direction']}",
                    f"- Center: {row['center_ref']} `{row['center_word']}`",
                    f"- Context read: {row['context_read']}",
                    "",
                    "| # | Role | Letter | Offset | Ref | Surface word |",
                    "| ---: | --- | --- | ---: | --- | --- |",
                ]
            )
            for item in letter_diagram_rows(corpus, row):
                lines.append(
                    "| "
                    + " | ".join(
                        [
                            str(item["index"]),
                            item["role"],
                            f"`{item['letter']}`",
                            str(item["offset"]),
                            item["ref"],
                            item["surface_word"],
                        ]
                    )
                    + " |"
                )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def letter_diagram_rows(corpus: Corpus, row: dict[str, str]) -> list[dict[str, object]]:
    sequence = row["extended_sequence"]
    start_offset = safe_int(row["extension_start_offset"])
    skip = safe_int(row["skip"])
    roles = letter_roles(
        sequence=sequence,
        normalized_term=row["normalized_term"],
        extension_type=row["extension_type"],
    )
    output = []
    for index, letter in enumerate(sequence):
        offset = start_offset + index * skip
        if offset < 0 or offset >= len(corpus.text):
            break
        word = corpus.word_at(offset)
        output.append(
            {
                "index": index + 1,
                "role": roles[index] if index < len(roles) else "unknown",
                "letter": letter,
                "offset": offset,
                "ref": corpus.ref_at(offset),
                "surface_word": word.raw_word if word is not None else "",
            }
        )
    return output


def letter_roles(
    *,
    sequence: str,
    normalized_term: str,
    extension_type: str,
) -> list[str]:
    roles = ["unknown"] * len(sequence)
    term_length = len(normalized_term)
    if extension_type == "term_plus_after":
        for index in range(len(sequence)):
            roles[index] = "term" if index < term_length else "after"
        return roles
    if extension_type == "before_plus_term":
        term_start = max(0, len(sequence) - term_length)
        for index in range(len(sequence)):
            roles[index] = "before" if index < term_start else "term"
        return roles
    if extension_type == "before_plus_term_plus_after":
        term_start = sequence.find(normalized_term)
        if term_start < 0:
            return roles
        term_end = term_start + term_length
        for index in range(len(sequence)):
            if index < term_start:
                roles[index] = "before"
            elif index < term_end:
                roles[index] = "term"
            else:
                roles[index] = "after"
        return roles
    return roles


def write_manifest(
    args: argparse.Namespace,
    input_rows: int,
    targets: int,
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_extension_context_review",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "top_files": [str(path) for path in (args.top_file or TOP_FILES)],
        "controls": str(args.controls),
        "surface_context_hits": str(args.surface_context_hits),
        "require_center_exact": args.require_center_exact,
        "require_control_row": args.require_control_row,
        "dedupe_targets": args.dedupe_targets,
        "title": args.title,
        "description": args.description,
        "input_rows": input_rows,
        "targets": targets,
        "rows": rows,
        "outputs": [
            str(args.summary_out),
            str(args.markdown_out),
            str(args.letter_paths_out),
            str(args.manifest_out),
        ],
        "seconds": round(time.perf_counter() - started, 3),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def refs_cell(verses: tuple[VerseSpan, ...]) -> str:
    return "-".join([verses[0].ref, verses[-1].ref]) if len(verses) > 1 else verses[0].ref


def verses_cell(verses: tuple[VerseSpan, ...]) -> str:
    return " | ".join(verse_cell(verse) for verse in verses)


def verse_cell(verse: VerseSpan | None) -> str:
    if verse is None:
        return ""
    return f"{verse.ref}: {verse.raw_text}"


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def promotion_gate(surface_row: dict[str, str]) -> str:
    if is_true(surface_row.get("center_exact", "")):
        return "promote_exact_center"
    if is_true(surface_row.get("center_same_concept", "")):
        return "promote_same_concept_center"
    if is_true(surface_row.get("span_exact", "")):
        return "review_exact_span"
    if is_true(surface_row.get("span_same_concept", "")):
        return "review_same_concept_span"
    if is_true(surface_row.get("center_same_category", "")):
        return "hold_same_category_only"
    if is_true(surface_row.get("span_same_category", "")):
        return "hold_same_category_span_only"
    return "hold_no_surface_context"


def is_true(value: str) -> bool:
    return str(value).strip().lower() == "true"


def safe_int(value: str) -> int:
    return int(value)


if __name__ == "__main__":
    raise SystemExit(main())
