#!/usr/bin/env python3
"""Summarize exact extension pattern presence by source text."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.analyze_extension_context_review import overlap_key, surface_context_key


FIELDNAMES = [
    "overlap_key",
    "normalized_term",
    "skip",
    "direction",
    "extension_type",
    "extended_sequence",
    "matched_normalized",
    "corpus_count",
    "total_corpora",
    "present_corpora",
    "absent_corpora",
    "presence_pattern",
    "scope",
    "top_score",
    "top_extension_length",
    "matched_refs_by_corpus",
    "center_refs_by_corpus",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_rows_many(args.top_file)
    surface_context = read_surface_context(args.surface_context_hits)
    rows = selected_rows(
        rows,
        surface_context=surface_context,
        require_center_exact=args.require_center_exact,
        dedupe=args.dedupe_rows,
    )
    corpus_order = complete_corpus_order(args.corpus, rows)
    summary_rows = pattern_presence_rows(rows, corpus_order)
    write_rows(args.summary_out, summary_rows)
    write_markdown(args.markdown_out, summary_rows, corpus_order, args)
    write_manifest(args, len(rows), len(summary_rows), corpus_order, started)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-file", action="append", required=True, type=Path)
    parser.add_argument("--surface-context-hits", type=Path)
    parser.add_argument("--require-center-exact", action="store_true")
    parser.add_argument("--dedupe-rows", action="store_true")
    parser.add_argument(
        "--corpus",
        action="append",
        default=[],
        help="Corpus label to include in the presence matrix. Repeatable.",
    )
    parser.add_argument(
        "--title",
        default="Extension Pattern Presence",
    )
    parser.add_argument(
        "--description",
        default="Exact extension-key presence by source text.",
    )
    parser.add_argument("--summary-out", required=True, type=Path)
    parser.add_argument("--markdown-out", required=True, type=Path)
    parser.add_argument("--manifest-out", required=True, type=Path)
    return parser


def read_rows_many(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                copied = dict(row)
                copied["source_file"] = str(path)
                rows.append(copied)
    return rows


def read_surface_context(path: Path | None) -> dict[tuple[str, ...], dict[str, str]]:
    if path is None or not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {surface_context_key(row): row for row in csv.DictReader(handle)}


def selected_rows(
    rows: list[dict[str, str]],
    *,
    surface_context: dict[tuple[str, ...], dict[str, str]],
    require_center_exact: bool,
    dedupe: bool,
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        if require_center_exact and not center_exact(row, surface_context):
            continue
        copied = dict(row)
        copied["overlap_key"] = overlap_key(row)
        dedupe_key = (copied.get("corpus", ""), copied["overlap_key"])
        if dedupe and dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        output.append(copied)
    return output


def center_exact(
    row: dict[str, str],
    surface_context: dict[tuple[str, ...], dict[str, str]],
) -> bool:
    return surface_context.get(surface_context_key(row), {}).get("center_exact") == "True"


def complete_corpus_order(
    requested: list[str],
    rows: list[dict[str, str]],
) -> list[str]:
    output = list(dict.fromkeys(requested))
    for corpus in sorted({row.get("corpus", "") for row in rows if row.get("corpus", "")}):
        if corpus not in output:
            output.append(corpus)
    return output


def pattern_presence_rows(
    rows: list[dict[str, str]],
    corpus_order: list[str],
) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["overlap_key"]].append(row)
    output = [presence_row(key, group, corpus_order) for key, group in groups.items()]
    return sorted(
        output,
        key=lambda row: (
            -int(row["corpus_count"]),
            str(row["normalized_term"]),
            int_or_zero(row["skip"]),
            str(row["direction"]),
            str(row["extension_type"]),
            str(row["extended_sequence"]),
        ),
    )


def presence_row(
    key: str,
    group: list[dict[str, str]],
    corpus_order: list[str],
) -> dict[str, object]:
    first = group[0]
    present = ordered_corpora({row.get("corpus", "") for row in group}, corpus_order)
    absent = [corpus for corpus in corpus_order if corpus not in present]
    by_corpus = best_rows_by_corpus(group)
    top = max(group, key=lambda row: int_or_zero(row.get("extension_score")))
    return {
        "overlap_key": key,
        "normalized_term": first.get("normalized_term", ""),
        "skip": first.get("skip", ""),
        "direction": first.get("direction", ""),
        "extension_type": first.get("extension_type", ""),
        "extended_sequence": first.get("extended_sequence", ""),
        "matched_normalized": first.get("matched_normalized", ""),
        "corpus_count": len(present),
        "total_corpora": len(corpus_order),
        "present_corpora": ",".join(present),
        "absent_corpora": ",".join(absent),
        "presence_pattern": presence_pattern(present, corpus_order),
        "scope": scope_label(present, corpus_order),
        "top_score": int_or_zero(top.get("extension_score")),
        "top_extension_length": int_or_zero(top.get("extension_length")),
        "matched_refs_by_corpus": joined_by_corpus(by_corpus, "matched_refs", corpus_order),
        "center_refs_by_corpus": joined_by_corpus(by_corpus, "center_ref", corpus_order),
        "read": read_label(present, corpus_order),
    }


def best_rows_by_corpus(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for row in rows:
        corpus = row.get("corpus", "")
        current = output.get(corpus)
        if current is None or int_or_zero(row.get("extension_score")) > int_or_zero(
            current.get("extension_score")
        ):
            output[corpus] = row
    return output


def ordered_corpora(corpora: set[str], corpus_order: list[str]) -> list[str]:
    ordered = [corpus for corpus in corpus_order if corpus in corpora]
    ordered.extend(sorted(corpora - set(ordered)))
    return ordered


def presence_pattern(present: list[str], corpus_order: list[str]) -> str:
    present_set = set(present)
    return "".join("1" if corpus in present_set else "0" for corpus in corpus_order)


def scope_label(present: list[str], corpus_order: list[str]) -> str:
    if len(present) == len(corpus_order):
        return "all_sources"
    if len(present) > 1:
        return "multi_source"
    return "source_only"


def joined_by_corpus(
    by_corpus: dict[str, dict[str, str]],
    field: str,
    corpus_order: list[str],
) -> str:
    cells = []
    for corpus in corpus_order:
        value = by_corpus.get(corpus, {}).get(field, "")
        if value:
            cells.append(f"{corpus}:{value}")
    return "; ".join(cells)


def read_label(present: list[str], corpus_order: list[str]) -> str:
    present_set = set(present)
    if len(present) == len(corpus_order):
        return "present in every compared source"
    if present_set == {"BYZ_NT", "TCG_NT"}:
        return "related Byzantine-source pair; inspect as source-family pattern"
    if len(present) > 1:
        return "present in multiple sources; inspect source-family distribution"
    return "source-specific pattern; keep visible, do not discard"


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    corpus_order: list[str],
    args: argparse.Namespace,
) -> None:
    scope_counts = Counter(str(row["scope"]) for row in rows)
    count_counts = Counter(str(row["corpus_count"]) for row in rows)
    lines = [
        f"# {args.title}",
        "",
        args.description,
        "",
        "This report groups exact extension keys by source text. Absence in a",
        "source is treated as data, not as automatic failure.",
        "",
        "## Compared Sources",
        "",
        "- " + ", ".join(corpus_order),
        "",
        "## Scope Counts",
        "",
        "| Scope | Patterns |",
        "| --- | ---: |",
    ]
    for scope, count in sorted(scope_counts.items()):
        lines.append(f"| `{scope}` | {count} |")
    lines.extend(["", "| Source count | Patterns |", "| ---: | ---: |"])
    for source_count, count in sorted(count_counts.items(), key=lambda item: int(item[0])):
        lines.append(f"| {source_count} | {count} |")
    lines.extend(
        [
            "",
            "## Pattern Matrix",
            "",
            "| Pattern | Present | Missing | Scope | Top score | Read |",
            "| --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in rows[:80]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['overlap_key']}`",
                    str(row["present_corpora"]),
                    str(row["absent_corpora"]),
                    f"`{row['scope']}`",
                    str(row["top_score"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Caution",
            "",
            "This is a source-distribution view, not a control result. Use it to decide",
            "which patterns deserve version-specific review and controls.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    input_rows: int,
    output_rows: int,
    corpus_order: list[str],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_extension_presence",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "top_files": [str(path) for path in args.top_file],
        "surface_context_hits": str(args.surface_context_hits)
        if args.surface_context_hits is not None
        else "",
        "require_center_exact": args.require_center_exact,
        "dedupe_rows": args.dedupe_rows,
        "corpora": corpus_order,
        "input_rows": input_rows,
        "output_rows": output_rows,
        "outputs": [
            str(args.summary_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
        "seconds": round(time.perf_counter() - started, 3),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


if __name__ == "__main__":
    raise SystemExit(main())
