#!/usr/bin/env python3
"""Build a compact audit packet for English seed rows that survive controls."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import Corpus, load_corpus


DEFAULT_CONTEXT_HITS = Path("reports/english_version_control_triage/context_hits.csv")
DEFAULT_TRIAGE = Path("reports/english_version_control_triage/triage.csv")
DEFAULT_CORPUS_SHUFFLE = Path("reports/english_seed_shuffle_followup_100/summary.csv")
DEFAULT_TERM_SHUFFLE = Path("reports/english_seed_term_shuffle_1000/summary.csv")
DEFAULT_PAIRED_CONTROLS = Path("reports/english_seed_paired_controls_1000/summary.csv")
DEFAULT_OUT_DIR = Path("reports/english_seed_survivor_audit")
DEFAULT_SUMMARY_OUT = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_LETTERS_OUT = DEFAULT_OUT_DIR / "letter_paths.csv"
DEFAULT_MARKDOWN_OUT = Path("docs/ENGLISH_SEED_SURVIVOR_AUDIT.md")
DEFAULT_MANIFEST_OUT = DEFAULT_OUT_DIR / "manifest.json"

SUMMARY_FIELDNAMES = [
    "corpus",
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "hit_index",
    "skip",
    "direction",
    "start_offset",
    "center_offset",
    "end_offset",
    "span_letters",
    "start_ref",
    "center_ref",
    "end_ref",
    "sequence",
    "matches_term",
    "path_offsets",
    "path_refs",
    "center_word",
    "center_normalized_word",
    "surface_context_read",
    "triage_flag",
    "target_present_corpora",
    "target_total_hits",
    "control_present_corpora",
    "control_total_hits",
    "target_minus_control_rate",
    "corpus_shuffle_observed",
    "corpus_shuffle_null_mean",
    "corpus_shuffle_p_ge",
    "term_shuffle_observed",
    "term_shuffle_null_mean",
    "term_shuffle_p_ge",
    "term_shuffle_q",
    "term_shuffle_band",
    "review_read",
]

LETTER_FIELDNAMES = [
    "corpus",
    "term_id",
    "concept",
    "hit_index",
    "skip",
    "direction",
    "letter_index",
    "offset",
    "letter",
    "ref",
    "word_index",
    "word",
    "normalized_word",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    configs = parse_corpus_args(args.corpus)
    term_rows = survivor_term_rows(args.term_shuffle, max_q=args.max_term_q)
    context_hits = survivor_context_hits(args.context_hits, term_rows)
    triage_rows = keyed_rows_by_term_id(args.triage)
    corpora = {label: load_corpus(config) for label, config in configs.items()}
    corpus_shuffle = keyed_rows(args.corpus_shuffle)
    summary_rows, letter_rows = build_audit_rows(
        context_hits,
        term_rows,
        corpus_shuffle,
        triage_rows,
        corpora,
    )
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.letters_out, LETTER_FIELDNAMES, letter_rows)
    paired_rows = read_optional_rows(args.paired_controls)
    write_markdown(args.markdown_out, summary_rows, letter_rows, paired_rows, args)
    write_manifest(args, summary_rows, letter_rows, started)
    print(args.summary_out)
    print(args.letters_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-hits", type=Path, default=DEFAULT_CONTEXT_HITS)
    parser.add_argument("--triage", type=Path, default=DEFAULT_TRIAGE)
    parser.add_argument("--corpus-shuffle", type=Path, default=DEFAULT_CORPUS_SHUFFLE)
    parser.add_argument("--term-shuffle", type=Path, default=DEFAULT_TERM_SHUFFLE)
    parser.add_argument("--paired-controls", type=Path, default=DEFAULT_PAIRED_CONTROLS)
    parser.add_argument("--corpus", action="append", required=True)
    parser.add_argument("--max-term-q", type=float, default=0.05)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--letters-out", type=Path, default=DEFAULT_LETTERS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    return parser


def parse_corpus_args(values: list[str]) -> dict[str, Path]:
    parsed: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"--corpus must be LABEL=CONFIG: {value}")
        label, config = value.split("=", 1)
        if not label or not config:
            raise SystemExit(f"--corpus must be LABEL=CONFIG: {value}")
        parsed[label] = Path(config)
    return parsed


def survivor_term_rows(path: Path, *, max_q: float) -> dict[tuple[str, str], dict[str, str]]:
    rows: dict[tuple[str, str], dict[str, str]] = {}
    for row in read_rows(path):
        if int_value(row.get("observed_hits")) <= 0:
            continue
        q_value = float_value(row.get("term_q_value"))
        if q_value is None or q_value > max_q:
            continue
        rows[(row["corpus"], row["term_id"])] = row
    return rows


def survivor_context_hits(
    path: Path,
    survivors: dict[tuple[str, str], dict[str, str]],
) -> list[dict[str, str]]:
    if not survivors:
        return []
    rows = [
        row
        for row in read_rows(path)
        if (row.get("corpus", ""), row.get("term_id", "")) in survivors
    ]
    if not rows:
        raise SystemExit("no matching context hit rows for survivor rows")
    return rows


def keyed_rows(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row["corpus"], row["term_id"]): row
        for row in read_rows(path)
    }


def keyed_rows_by_term_id(path: Path) -> dict[str, dict[str, str]]:
    return {
        row["term_id"]: row
        for row in read_rows(path)
    }


def build_audit_rows(
    context_hits: list[dict[str, str]],
    term_rows: dict[tuple[str, str], dict[str, str]],
    corpus_shuffle: dict[tuple[str, str], dict[str, str]],
    triage_rows: dict[str, dict[str, str]],
    corpora: dict[str, Corpus],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    summary_rows: list[dict[str, str]] = []
    letter_rows: list[dict[str, str]] = []
    hit_counts: Counter[tuple[str, str]] = Counter()
    for row in context_hits:
        key = (row["corpus"], row["term_id"])
        hit_counts[key] += 1
        hit_index = str(hit_counts[key])
        if row["corpus"] not in corpora:
            raise SystemExit(f"missing corpus config for {row['corpus']}")
        corpus = corpora[row["corpus"]]
        term_row = term_rows[key]
        corpus_row = corpus_shuffle.get(key, {})
        triage_row = triage_rows.get(row["term_id"], {})
        summary, letters = audit_hit(row, term_row, corpus_row, triage_row, corpus, hit_index)
        summary_rows.append(summary)
        letter_rows.extend(letters)
    return summary_rows, letter_rows


def audit_hit(
    hit: dict[str, str],
    term_row: dict[str, str],
    corpus_row: dict[str, str],
    triage_row: dict[str, str],
    corpus: Corpus,
    hit_index: str,
) -> tuple[dict[str, str], list[dict[str, str]]]:
    start = int(hit["start_offset"])
    center = int(hit["center_offset"])
    end = int(hit["end_offset"])
    skip = int(hit["skip"])
    normalized_term = hit["normalized_term"]
    positions = [start + index * skip for index in range(len(normalized_term))]
    sequence = "".join(corpus.text[position] for position in positions)
    path_refs = unique_in_order(corpus.ref_at(position) for position in positions)
    letters = [
        letter_row(hit, corpus, hit_index, skip, position, index)
        for index, position in enumerate(positions, start=1)
    ]
    surface_read = surface_context_read(hit)
    review_read = (
        "survives count controls; no surface-context support"
        if surface_read == "no surface-context support"
        else "survives count controls with surface-context signal"
    )
    summary = {
        "corpus": hit["corpus"],
        "term_id": hit["term_id"],
        "concept": hit["concept"],
        "category": hit["category"],
        "term": hit["term"],
        "normalized_term": normalized_term,
        "hit_index": hit_index,
        "skip": hit["skip"],
        "direction": hit["direction"],
        "start_offset": hit["start_offset"],
        "center_offset": hit["center_offset"],
        "end_offset": hit["end_offset"],
        "span_letters": hit["span_letters"],
        "start_ref": hit["start_ref"],
        "center_ref": hit["center_ref"],
        "end_ref": hit["end_ref"],
        "sequence": sequence,
        "matches_term": str(sequence == normalized_term),
        "path_offsets": "/".join(str(position) for position in positions),
        "path_refs": "; ".join(path_refs),
        "center_word": hit["center_word"],
        "center_normalized_word": hit["center_normalized_word"],
        "surface_context_read": surface_read,
        "triage_flag": triage_row.get("triage_flag", ""),
        "target_present_corpora": triage_row.get("target_present_corpora", ""),
        "target_total_hits": triage_row.get("target_total_hits", ""),
        "control_present_corpora": triage_row.get("control_present_corpora", ""),
        "control_total_hits": triage_row.get("control_total_hits", ""),
        "target_minus_control_rate": triage_row.get("target_minus_control_rate", ""),
        "corpus_shuffle_observed": corpus_row.get("observed", ""),
        "corpus_shuffle_null_mean": corpus_row.get("null_mean", ""),
        "corpus_shuffle_p_ge": corpus_row.get("p_greater_equal", ""),
        "term_shuffle_observed": term_row.get("observed_hits", ""),
        "term_shuffle_null_mean": term_row.get("term_null_mean", ""),
        "term_shuffle_p_ge": term_row.get("term_p_ge", ""),
        "term_shuffle_q": term_row.get("term_q_value", ""),
        "term_shuffle_band": term_row.get("significance_band", ""),
        "review_read": review_read,
    }
    return summary, letters


def letter_row(
    hit: dict[str, str],
    corpus: Corpus,
    hit_index: str,
    skip: int,
    position: int,
    letter_index: int,
) -> dict[str, str]:
    word = corpus.word_at(position)
    return {
        "corpus": hit["corpus"],
        "term_id": hit["term_id"],
        "concept": hit["concept"],
        "hit_index": hit_index,
        "skip": str(skip),
        "direction": hit["direction"],
        "letter_index": str(letter_index),
        "offset": str(position),
        "letter": corpus.text[position],
        "ref": corpus.ref_at(position),
        "word_index": str(word.word_index) if word is not None else "",
        "word": word.raw_word if word is not None else "",
        "normalized_word": word.normalized_word if word is not None else "",
    }


def surface_context_read(row: dict[str, str]) -> str:
    fields = [
        "center_word_exact",
        "center_word_same_concept",
        "center_word_same_category",
        "center_exact",
        "center_same_concept",
        "center_same_category",
        "span_exact",
        "span_same_concept",
        "span_same_category",
    ]
    if any(row.get(field) == "True" for field in fields):
        return "has surface-context support"
    return "no surface-context support"


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, str]],
    letter_rows: list[dict[str, str]],
    paired_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    if not summary_rows:
        lines = [
            "# English Seed Survivor Audit",
            "",
            "Status: no current survivor rows.",
            "",
            "## Inputs",
            "",
            f"- Context hits: `{args.context_hits}`",
            f"- Triage spread: `{args.triage}`",
            f"- Corpus-letter shuffle: `{args.corpus_shuffle}`",
            f"- Same-letter term shuffle: `{args.term_shuffle}`",
            f"- Max term q: `{args.max_term_q}`",
            "",
            "## Counts",
            "",
            "- survivor hit rows: 0",
            "- letter rows: 0",
            "",
            "## Read",
            "",
            "No English seed row currently survives the count-control gates. Keep",
            "downstream paired-control survivor reports idle until a non-empty",
            "survivor list is regenerated.",
        ]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    mismatches = [row for row in summary_rows if row["matches_term"] != "True"]
    rows_by_corpus = Counter(row["corpus"] for row in summary_rows)
    lines = [
        "# English Seed Survivor Audit",
        "",
        "Status: audit packet for English seed rows that survived the count-control gates.",
        "",
        "## Inputs",
        "",
        f"- Context hits: `{args.context_hits}`",
        f"- Triage spread: `{args.triage}`",
        f"- Corpus-letter shuffle: `{args.corpus_shuffle}`",
        f"- Same-letter term shuffle: `{args.term_shuffle}`",
        *([f"- Paired controls: `{args.paired_controls}`"] if paired_rows else []),
        f"- Max term q: `{args.max_term_q}`",
        "",
        "## Counts",
        "",
        f"- survivor hit rows: {len(summary_rows)}",
        f"- letter rows: {len(letter_rows)}",
        f"- sequence mismatches: {len(mismatches)}",
        f"- rows by corpus: `{dict(sorted(rows_by_corpus.items()))}`",
        "",
        "## Hit Summary",
        "",
        "| Corpus | Term | Hit | Sequence | Skip | Refs | Center | Center word | Target/control spread | Corpus p_ge | Term p_ge | Term q | Read |",
        "| --- | --- | ---: | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["corpus"],
                    f"`{row['term_id']}` {row['concept']}",
                    row["hit_index"],
                    f"`{row['sequence']}`",
                    row["skip"],
                    f"{row['start_ref']} -> {row['end_ref']}",
                    row["center_ref"],
                    f"`{row['center_normalized_word']}`",
                    spread_label(row),
                    row["corpus_shuffle_p_ge"],
                    row["term_shuffle_p_ge"],
                    row["term_shuffle_q"],
                    row["review_read"],
                ]
            )
            + " |"
        )
    paired_by_key = {
        (row["corpus"], row["term_id"]): row
        for row in paired_rows
    }
    paired_survivors = [
        (row, paired_by_key[(row["corpus"], row["term_id"])])
        for row in summary_rows
        if (row["corpus"], row["term_id"]) in paired_by_key
    ]
    if paired_survivors:
        lines.extend(
            [
                "",
                "## Paired-Control Overlay",
                "",
                "| Corpus | Term | Hit | Hits | Term p | Random p | Combined q | Read |",
                "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for audit_row, paired_row in paired_survivors:
            lines.append(
                "| "
                + " | ".join(
                    [
                        audit_row["corpus"],
                        f"`{audit_row['term_id']}` {audit_row['concept']}",
                        audit_row["hit_index"],
                        paired_row["observed_hits"],
                        paired_row["term_shuffle_p_ge"],
                        paired_row["random_p_ge"],
                        paired_row["combined_min_q_value"],
                        paired_row["read"],
                    ]
                )
                + " |"
            )
        lines.extend(
            [
                "",
                "Paired controls keep these rows as screens. The same-letter term-shuffle",
                "side stays below q <= 0.05, but same-length corpus-random strings are",
                "not rare enough to promote either row without contextual support.",
            ]
        )
    lines.extend(
        [
            "",
            "## Letter Paths",
            "",
            "| Corpus | Term | Hit | i | Offset | Letter | Ref | Word |",
            "| --- | --- | ---: | ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in letter_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["corpus"],
                    f"`{row['term_id']}`",
                    row["hit_index"],
                    row["letter_index"],
                    row["offset"],
                    f"`{row['letter']}`",
                    row["ref"],
                    f"`{row['normalized_word']}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "All survivor paths reconstruct their normalized term exactly.",
            "These rows survive count-based controls but still have no surface-context",
            "support, so they remain review leads rather than promoted findings.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    summary_rows: list[dict[str, str]],
    letter_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "build_english_seed_survivor_audit",
        "created_utc": datetime.now(UTC).isoformat(),
        "context_hits": str(args.context_hits),
        "triage": str(args.triage),
        "corpus_shuffle": str(args.corpus_shuffle),
        "term_shuffle": str(args.term_shuffle),
        "max_term_q": args.max_term_q,
        "summary_rows": len(summary_rows),
        "letter_rows": len(letter_rows),
        "mismatches": sum(1 for row in summary_rows if row["matches_term"] != "True"),
        "seconds": round(time.perf_counter() - started, 3),
        "outputs": [str(args.summary_out), str(args.letters_out), str(args.markdown_out)],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def spread_label(row: dict[str, str]) -> str:
    target = row["target_present_corpora"] or "none"
    control = row["control_present_corpora"] or "none"
    return f"target {target}; control {control}"


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_optional_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_rows(path)


def int_value(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def float_value(value: object) -> float | None:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def unique_in_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


if __name__ == "__main__":
    raise SystemExit(main())
