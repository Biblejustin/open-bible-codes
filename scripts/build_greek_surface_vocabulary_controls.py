#!/usr/bin/env python3
"""Build a generated Greek surface-vocabulary control term list."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, load_corpus
from els.normalization import normalize_greek


SOURCE_TERMS = Path("terms/greek_surface_prospective_terms.csv")
SELECTED = Path("reports/greek_surface_length4_followup/selected_patterns.csv")
OUT_DIR = Path("reports/greek_surface_length4_vocab_controls")
TERMS_OUT = OUT_DIR / "terms.csv"
MD_OUT = Path("docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROLS.md")
MANIFEST_OUT = OUT_DIR / "terms.manifest.json"
DEFAULT_CORPORA = {
    "TR_NT": Path("configs/example_ebible_grctr.toml"),
    "BYZ_NT": Path("configs/example_ebible_grcmt.toml"),
    "TCG_NT": Path("configs/example_ebible_grctcgnt.toml"),
    "SBLGNT": Path("configs/example_sblgnt.toml"),
}

TERM_FIELDNAMES = ["term_id", "concept", "category", "language", "term", "notes"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus_configs = parse_corpus_args(args.corpus)
    source_terms = read_rows(args.source_terms)
    selected_rows = read_rows(args.selected)
    target_rows = selected_target_rows(source_terms, selected_rows)
    corpora = {label: load_corpus(path) for label, path in corpus_configs.items()}
    control_rows, vocabulary_summary = vocabulary_control_rows(
        corpora,
        target_rows,
        min_length=args.min_length,
        max_length=args.max_length,
        min_sources=args.min_sources,
    )
    term_rows = [*target_rows, *control_rows]
    write_rows(args.out, TERM_FIELDNAMES, term_rows)
    write_markdown(args.markdown_out, target_rows, control_rows, vocabulary_summary, args)
    write_manifest(
        args,
        corpus_configs,
        target_rows,
        control_rows,
        vocabulary_summary,
        started,
    )
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-terms", type=Path, default=SOURCE_TERMS)
    parser.add_argument("--selected", type=Path, default=SELECTED)
    parser.add_argument("--corpus", action="append", default=[])
    parser.add_argument("--min-length", type=int, default=4)
    parser.add_argument("--max-length", type=int, default=4)
    parser.add_argument("--min-sources", type=int, default=4)
    parser.add_argument("--out", type=Path, default=TERMS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def parse_corpus_args(values: list[str]) -> dict[str, Path]:
    if not values:
        return dict(DEFAULT_CORPORA)
    output = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected LABEL=path corpus value: {value}")
        label, path = value.split("=", 1)
        output[label] = Path(path)
    return output


def selected_target_rows(
    source_terms: list[dict[str, str]],
    selected_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    selected_ids = {row["term_id"] for row in selected_rows}
    by_id = {row["term_id"]: row for row in source_terms}
    missing = sorted(selected_ids - set(by_id))
    if missing:
        raise SystemExit("selected term IDs missing from source terms: " + ", ".join(missing))
    rows = []
    for term_id in sorted(selected_ids):
        source = by_id[term_id]
        rows.append(
            {
                "term_id": source["term_id"],
                "concept": source["concept"],
                "category": source["category"],
                "language": "greek",
                "term": source["term"],
                "notes": append_note(
                    source.get("notes", ""),
                    "selected length-4 target retained for vocabulary-control run",
                ),
            }
        )
    return rows


def vocabulary_control_rows(
    corpora: dict[str, Corpus],
    target_rows: list[dict[str, str]],
    *,
    min_length: int,
    max_length: int,
    min_sources: int,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    verse_refs_by_word = word_verse_refs_by_label(corpora)
    target_terms = {normalize_greek(row["term"]) for row in target_rows}
    source_counts = Counter(
        sum(bool(refs_by_label.get(label)) for label in corpora)
        for refs_by_label in verse_refs_by_word.values()
    )
    candidates = []
    for normalized, refs_by_label in verse_refs_by_word.items():
        if normalized in target_terms:
            continue
        if not min_length <= len(normalized) <= max_length:
            continue
        present_sources = sum(bool(refs_by_label.get(label)) for label in corpora)
        if present_sources < min_sources:
            continue
        candidates.append(normalized)
    rows = [
        vocabulary_control_row(index, normalized, verse_refs_by_word[normalized])
        for index, normalized in enumerate(sorted(candidates), start=1)
    ]
    return rows, {
        "corpus_labels": sorted(corpora),
        "unique_normalized_words": len(verse_refs_by_word),
        "source_presence_counts": dict(sorted(source_counts.items())),
        "target_terms_excluded": sorted(target_terms),
        "control_terms": len(rows),
        "min_length": min_length,
        "max_length": max_length,
        "min_sources": min_sources,
    }


def word_verse_refs_by_label(
    corpora: dict[str, Corpus],
) -> dict[str, dict[str, set[str]]]:
    refs_by_word: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for label, corpus in corpora.items():
        for word in corpus.words:
            normalized = word.normalized_word
            if normalized:
                refs_by_word[normalized][label].add(word.ref)
    return refs_by_word


def vocabulary_control_row(
    index: int,
    normalized: str,
    refs_by_label: dict[str, set[str]],
) -> dict[str, str]:
    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:8]
    verse_counts = "/".join(
        f"{label}:{len(refs_by_label[label])}" for label in sorted(refs_by_label)
    )
    return {
        "term_id": f"gsvocab_{index:04d}_{digest}",
        "concept": f"Surface vocabulary {normalized}",
        "category": f"surface_vocabulary_control_{digest}",
        "language": "greek",
        "term": normalized,
        "notes": f"generated normalized Greek surface vocabulary control; verse_counts={verse_counts}",
    }


def append_note(existing: str, note: str) -> str:
    existing = existing.strip()
    if not existing:
        return note
    return f"{existing}; {note}"


def write_markdown(
    path: Path,
    target_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
    vocabulary_summary: dict[str, object],
    args: argparse.Namespace,
) -> None:
    preview = control_rows[:25]
    lines = [
        "# Greek Surface Length-4 Vocabulary Controls",
        "",
        "Status: generated real-word control universe; no claim.",
        "",
        "This file documents the generated term list used to broaden the length-4",
        "Greek surface controls. The generated CSV lives under ignored `reports/`",
        "output because it is derived from local corpus files.",
        "",
        "## Inputs",
        "",
        f"- Source terms: `{args.source_terms}`",
        f"- Selected targets: `{args.selected}`",
        f"- Output term CSV: `{args.out}`",
        "",
        "## Rule",
        "",
        f"- include selected target terms from the locked length-4 follow-up;",
        f"- add normalized Greek surface words with length {args.min_length}..{args.max_length};",
        f"- require presence in at least {args.min_sources} compared Greek NT sources;",
        "- exclude generated controls with the same normalized spelling as a selected target;",
        "- give each generated control its own category so same-category surface",
        "  context does not inflate the hit output.",
        "",
        "## Counts",
        "",
        f"- selected target terms: {len(target_rows):,}",
        f"- generated control terms: {len(control_rows):,}",
        f"- unique normalized surface words scanned: {vocabulary_summary['unique_normalized_words']:,}",
        "",
        "## Selected Targets",
        "",
        "| Term ID | Term | Concept |",
        "| --- | --- | --- |",
    ]
    for row in target_rows:
        lines.append(f"| `{row['term_id']}` | `{normalize_greek(row['term'])}` | {row['concept']} |")
    lines.extend(
        [
            "",
            "## Control Preview",
            "",
            "| Term ID | Term | Notes |",
            "| --- | --- | --- |",
        ]
    )
    for row in preview:
        lines.append(f"| `{row['term_id']}` | `{row['term']}` | {row['notes']} |")
    if len(control_rows) > len(preview):
        lines.extend(
            [
                "",
                f"Preview only; {len(control_rows) - len(preview):,} additional control rows are in `{args.out}`.",
            ]
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "This broadens the control universe for the length-4 follow-up. It is still",
            "post-discovery, but it avoids making the result depend on the much smaller",
            "declared screening-term file.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    corpus_configs: dict[str, Path],
    target_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
    vocabulary_summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": "build_greek_surface_vocabulary_controls",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "source_terms": str(args.source_terms),
        "selected": str(args.selected),
        "corpora": {label: str(path) for label, path in corpus_configs.items()},
        "target_rows": len(target_rows),
        "control_rows": len(control_rows),
        "vocabulary_summary": vocabulary_summary,
        "outputs": [
            str(args.out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
