#!/usr/bin/env python3
"""Find ELS paths that cross canonical/deuterocanon book boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import Corpus, load_corpus
from els.search import build_hit, iter_els_query_matches_by_lanes, normalize_for_corpus


DEFAULT_TERMS = [
    Path("terms/theological_terms.csv"),
    Path("terms/prophetic_terms.csv"),
    Path("terms/greek_nt_claim_terms.csv"),
]
DEFAULT_OUT = Path("reports/apocrypha_bridge_candidates/bridge_candidates.csv")
DEFAULT_SUMMARY = Path("reports/apocrypha_bridge_candidates/summary.csv")
DEFAULT_MARKDOWN = Path("docs/APOCRYPHA_BRIDGE_CANDIDATES.md")
DEFAULT_MANIFEST = Path("reports/apocrypha_bridge_candidates/manifest.json")

APOCRYPHA_BOOKS = {
    "TOB",
    "JDT",
    "ESG",
    "WIS",
    "SIR",
    "BAR",
    "LJE",
    "S3Y",
    "SUS",
    "BEL",
    "DAG",
    "1MA",
    "2MA",
    "3MA",
    "4MA",
    "1ES",
    "2ES",
    "MAN",
    "ODA",
    "PS2",
}

FIELDNAMES = [
    "rank",
    "corpus",
    "term_ids",
    "concepts",
    "categories",
    "normalized_term",
    "term_length",
    "skip",
    "direction",
    "bridge_type",
    "start_ref",
    "center_ref",
    "end_ref",
    "start_book",
    "center_book",
    "end_book",
    "canonical_books",
    "apocrypha_books",
    "class_path",
    "letter_path",
    "center_word",
    "center_normalized_word",
]

SUMMARY_FIELDNAMES = [
    "metric",
    "value",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.terms is None:
        args.terms = list(DEFAULT_TERMS)
    corpus = load_corpus(args.config)
    term_records = read_term_records(args.terms, corpus, min_length=args.min_term_length)
    rows = find_bridge_rows(corpus, term_records, args)
    summary = summarize(rows, term_records, corpus, args)
    write_csv(args.out, rows, FIELDNAMES)
    write_csv(args.summary_out, summary, SUMMARY_FIELDNAMES)
    write_markdown(args.markdown_out, rows, summary, args)
    write_manifest(args.manifest_out, args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-label", default="LXX")
    parser.add_argument("--config", type=Path, default=Path("configs/example_ebible_grclxx.toml"))
    parser.add_argument("--terms", type=Path, action="append")
    parser.add_argument("--language", default="greek")
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=250)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--min-term-length", type=int, default=4)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--max-rows", type=int, default=0, help="0 means no row cap")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_term_records(
    paths: list[Path],
    corpus: Corpus,
    *,
    min_length: int,
) -> dict[str, list[dict[str, str]]]:
    records: dict[str, list[dict[str, str]]] = {}
    seen_ids: set[str] = set()
    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                if row.get("language") != corpus.language:
                    continue
                term_id = row.get("term_id", "")
                if term_id in seen_ids:
                    continue
                seen_ids.add(term_id)
                normalized = normalize_for_corpus(corpus, row.get("term", ""))
                if len(normalized) < min_length:
                    continue
                record = {
                    "term_id": term_id,
                    "concept": row.get("concept", ""),
                    "category": row.get("category", ""),
                    "term": row.get("term", ""),
                    "normalized_term": normalized,
                    "term_source": str(path),
                }
                records.setdefault(normalized, []).append(record)
    return records


def find_bridge_rows(
    corpus: Corpus,
    term_records: dict[str, list[dict[str, str]]],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    queries = {query: [query] for query in term_records}
    for query, skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        queries,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.jobs,
    ):
        hit = build_hit(corpus, query, query, skip, start, end)
        positions = hit_positions(hit.start_offset, hit.skip, len(query))
        letter_rows = [letter_provenance(corpus, position, index) for index, position in enumerate(positions, 1)]
        classes = [str(row["source_class"]) for row in letter_rows]
        if "canonical" not in classes or "apocrypha" not in classes:
            continue
        canonical_books = sorted({str(row["book"]) for row in letter_rows if row["source_class"] == "canonical"})
        apocrypha_books = sorted({str(row["book"]) for row in letter_rows if row["source_class"] == "apocrypha"})
        row = {
            "rank": 0,
            "corpus": args.corpus_label,
            "term_ids": join_unique(record["term_id"] for record in term_records[query]),
            "concepts": join_unique(record["concept"] for record in term_records[query]),
            "categories": join_unique(record["category"] for record in term_records[query]),
            "normalized_term": query,
            "term_length": len(query),
            "skip": hit.skip,
            "direction": hit.direction,
            "bridge_type": classify_bridge(classes),
            "start_ref": hit.start_ref,
            "center_ref": hit.center_ref,
            "end_ref": hit.end_ref,
            "start_book": letter_rows[0]["book"],
            "center_book": corpus.verses[corpus.position_to_verse[hit.center_offset]].book,
            "end_book": letter_rows[-1]["book"],
            "canonical_books": ";".join(canonical_books),
            "apocrypha_books": ";".join(apocrypha_books),
            "class_path": "".join("C" if value == "canonical" else "A" for value in classes),
            "letter_path": ";".join(format_letter(row) for row in letter_rows),
            "center_word": hit.center_word,
            "center_normalized_word": hit.center_normalized_word,
        }
        rows.append(row)
    return rank_bridge_rows(rows, max_rows=args.max_rows)


def rank_bridge_rows(rows: list[dict[str, object]], *, max_rows: int = 0) -> list[dict[str, object]]:
    ranked = sorted(rows, key=bridge_row_sort_key)
    if max_rows:
        ranked = ranked[:max_rows]
    for rank, row in enumerate(ranked, 1):
        row["rank"] = rank
    return ranked


def bridge_row_sort_key(row: dict[str, object]) -> tuple[object, ...]:
    skip = int(row["skip"])
    positions = letter_path_positions(str(row.get("letter_path", "")))
    low = min(positions) if positions else str(row["start_ref"])
    high = max(positions) if positions else str(row["end_ref"])
    return (
        abs(skip),
        0 if skip > 0 else 1,
        low,
        high,
        str(row["normalized_term"]),
        str(row["class_path"]),
    )


def letter_path_positions(letter_path: str) -> list[int]:
    positions = []
    for part in letter_path.split(";"):
        try:
            positions.append(int(part.rsplit(":", 1)[1]))
        except (IndexError, ValueError):
            continue
    return positions


def hit_positions(start: int, skip: int, length: int) -> list[int]:
    return [start + index * skip for index in range(length)]


def letter_provenance(corpus: Corpus, position: int, term_index: int) -> dict[str, object]:
    verse = corpus.verses[corpus.position_to_verse[position]]
    word = corpus.word_at(position)
    return {
        "term_index": term_index,
        "position": position,
        "letter": corpus.text[position],
        "book": verse.book,
        "ref": verse.ref,
        "source_class": "apocrypha" if verse.book in APOCRYPHA_BOOKS else "canonical",
        "word": word.raw_word if word else "",
    }


def classify_bridge(classes: list[str]) -> str:
    transitions = sum(1 for left, right in zip(classes, classes[1:]) if left != right)
    if transitions > 1:
        return "multi_segment_bridge"
    if classes[0] == "canonical" and classes[-1] == "apocrypha":
        return "canonical_to_apocrypha"
    if classes[0] == "apocrypha" and classes[-1] == "canonical":
        return "apocrypha_to_canonical"
    if classes[0] == "canonical":
        return "canonical_apocrypha_canonical"
    return "apocrypha_canonical_apocrypha"


def format_letter(row: dict[str, object]) -> str:
    return (
        f"{row['term_index']}:{row['letter']}@{row['ref']}"
        f":{row['source_class']}:{row['position']}"
    )


def summarize(
    rows: list[dict[str, object]],
    term_records: dict[str, list[dict[str, str]]],
    corpus: Corpus,
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    bridge_types = Counter(str(row["bridge_type"]) for row in rows)
    terms = {str(row["normalized_term"]) for row in rows}
    apoc_books = set()
    for row in rows:
        apoc_books.update(part for part in str(row["apocrypha_books"]).split(";") if part)
    summary = [
        {"metric": "corpus", "value": args.corpus_label},
        {"metric": "corpus_letters", "value": len(corpus.text)},
        {"metric": "queries_tested", "value": len(term_records)},
        {"metric": "min_skip", "value": args.min_skip},
        {"metric": "max_skip", "value": args.max_skip},
        {"metric": "direction", "value": args.direction},
        {"metric": "jobs", "value": args.jobs},
        {"metric": "bridge_rows", "value": len(rows)},
        {"metric": "terms_with_bridge_rows", "value": len(terms)},
        {"metric": "apocrypha_books_touched", "value": len(apoc_books)},
    ]
    for bridge_type, count in sorted(bridge_types.items()):
        summary.append({"metric": f"bridge_type:{bridge_type}", "value": count})
    return summary


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    lines = [
        f"# {args.corpus_label} Apocrypha Bridge Candidates",
        "",
        "Status: bounded bridge-candidate scan. This is not a claim report.",
        "",
        "A bridge candidate is an ELS path whose matched letters include at least",
        "one canonical-book letter and at least one deuterocanon/apocrypha-book",
        "letter in the declared expanded stream.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Summary",
        "",
    ]
    for row in summary:
        lines.append(f"- {row['metric']}: {row['value']}")

    lines.extend(
        [
            "",
            "## Top Bridge Rows",
            "",
            "| Rank | Type | Term | Skip | Start | Center | End | Apocrypha books | Class path |",
            "| ---: | --- | --- | ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows[:50]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["rank"]),
                    f"`{escape_md(str(row['bridge_type']))}`",
                    f"`{escape_md(str(row['normalized_term']))}`",
                    str(row["skip"]),
                    escape_md(str(row["start_ref"])),
                    escape_md(str(row["center_ref"])),
                    escape_md(str(row["end_ref"])),
                    escape_md(str(row["apocrypha_books"])),
                    f"`{escape_md(str(row['class_path']))}`",
                ]
            )
            + " |"
        )
    if len(rows) > 50:
        lines.append(f"| ... | ... | ... | ... | ... | ... | ... | ... | {len(rows) - 50} more rows in CSV |")

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- These are bridge candidates, not significance claims.",
            f"- The current {args.corpus_label} stream is tested in its declared",
            "  source order, so this first pass mostly tests the first",
            "  canonical/apocrypha boundary rather than a manuscript-specific",
            "  insertion model.",
            "- Removing the apocrypha/deuterocanon letters would break the expanded-stream ELS path.",
            "- The next control should insert comparable non-Bible blocks at the same boundary positions.",
            "- Letter-level provenance is in the CSV `letter_path` column.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_apocrypha_bridge_candidates",
        "version": __version__,
        "generated_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "commit": git_commit(),
        "inputs": {
            "config": str(args.config),
            "terms": [str(path) for path in args.terms],
            "jobs": args.jobs,
        },
        "outputs": {
            "rows": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "row_count": len(rows),
        "summary": summary,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reproduce_command(args: argparse.Namespace) -> str:
    terms = " ".join(f"--terms {path}" for path in args.terms)
    return (
        "python3 -m scripts.analyze_apocrypha_bridge_candidates "
        f"--corpus-label {args.corpus_label} --config {args.config} {terms} "
        f"--min-skip {args.min_skip} --max-skip {args.max_skip} "
        f"--direction {args.direction} --min-term-length {args.min_term_length} "
        f"--jobs {args.jobs} "
        f"--out {args.out} --summary-out {args.summary_out} "
        f"--markdown-out {args.markdown_out} --manifest-out {args.manifest_out}"
    )


def join_unique(values: Any) -> str:
    seen: list[str] = []
    for value in values:
        text = str(value)
        if text and text not in seen:
            seen.append(text)
    return ";".join(seen)


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
