#!/usr/bin/env python3
"""Compare apocrypha bridge candidates with non-Bible boundary controls."""

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
from els.search import iter_els_query_matches_by_lanes
from els.term_display import display_term

from scripts.analyze_apocrypha_bridge_candidates import (
    APOCRYPHA_BOOKS,
    DEFAULT_TERMS,
    classify_bridge,
    hit_positions,
    read_term_records,
)


DEFAULT_CANONICAL_CONFIG = Path("configs/example_ebible_grclxx.toml")
DEFAULT_CONTROLS = [
    "ILIAD=configs/nonbible_greek_perseus_iliad.toml",
    "ODYSSEY=configs/nonbible_greek_perseus_odyssey.toml",
    "HERODOTUS=configs/nonbible_greek_perseus_herodotus.toml",
]
DEFAULT_OBSERVED = Path("reports/apocrypha_bridge_candidates/bridge_candidates.csv")
DEFAULT_OUT = Path("reports/apocrypha_bridge_controls/control_summary.csv")
DEFAULT_TERM_OUT = Path("reports/apocrypha_bridge_controls/term_summary.csv")
DEFAULT_MARKDOWN = Path("docs/APOCRYPHA_BRIDGE_CONTROLS.md")
DEFAULT_MANIFEST = Path("reports/apocrypha_bridge_controls/manifest.json")

SUMMARY_FIELDNAMES = [
    "control_label",
    "bridge_rows",
    "terms_with_bridge_rows",
    "apocrypha_block_letters",
    "canonical_prefix_letters",
    "canonical_to_apocrypha",
    "apocrypha_to_canonical",
    "multi_segment_bridge",
]

TERM_FIELDNAMES = [
    "control_label",
    "normalized_term",
    "bridge_rows",
    "canonical_to_apocrypha",
    "apocrypha_to_canonical",
    "multi_segment_bridge",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.control is None:
        args.control = list(DEFAULT_CONTROLS)
    if args.terms is None:
        args.terms = list(DEFAULT_TERMS)
    canonical = load_corpus(args.canonical_config)
    boundary = boundary_offsets(canonical)
    term_records = read_term_records(args.terms, canonical, min_length=args.min_term_length)
    observed_rows = read_rows(args.observed)
    summary_rows = []
    term_rows = []
    for label, config in [parse_label_config(value) for value in args.control]:
        control = load_corpus(config)
        control_summary, control_terms = analyze_control(
            label,
            canonical,
            control,
            term_records,
            boundary,
            args,
        )
        summary_rows.append(control_summary)
        term_rows.extend(control_terms)
    write_csv(args.out, summary_rows, SUMMARY_FIELDNAMES)
    write_csv(args.term_out, term_rows, TERM_FIELDNAMES)
    write_markdown(args.markdown_out, summary_rows, term_rows, observed_rows, args)
    write_manifest(args.manifest_out, args, summary_rows, term_rows, observed_rows, started)
    print(args.out)
    print(args.term_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-label", default="LXX")
    parser.add_argument("--canonical-config", type=Path, default=DEFAULT_CANONICAL_CONFIG)
    parser.add_argument("--control", action="append")
    parser.add_argument("--terms", type=Path, action="append")
    parser.add_argument("--observed", type=Path, default=DEFAULT_OBSERVED)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=250)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--min-term-length", type=int, default=4)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--term-out", type=Path, default=DEFAULT_TERM_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def parse_label_config(value: str) -> tuple[str, Path]:
    if "=" not in value:
        path = Path(value)
        return path.stem, path
    label, config = value.split("=", 1)
    return label, Path(config)


def boundary_offsets(corpus: Corpus) -> dict[str, int]:
    first_apoc_verse = next(
        verse for verse in corpus.verses if verse.book in APOCRYPHA_BOOKS
    )
    first_apoc_offset = first_apoc_verse.norm_start
    apoc_letters = sum(
        verse.norm_length for verse in corpus.verses if verse.book in APOCRYPHA_BOOKS
    )
    return {
        "canonical_prefix_letters": first_apoc_offset,
        "apocrypha_block_letters": apoc_letters,
    }


def analyze_control(
    label: str,
    canonical: Corpus,
    control: Corpus,
    term_records: dict[str, list[dict[str, str]]],
    boundary: dict[str, int],
    args: argparse.Namespace,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    prefix_len = boundary["canonical_prefix_letters"]
    block_len = boundary["apocrypha_block_letters"]
    text = canonical.text[:prefix_len] + repeated_prefix(control.text, block_len)
    queries = {query: [query] for query in term_records}
    total_by_type: Counter[str] = Counter()
    term_by_type: dict[str, Counter[str]] = {}
    for query, skip, start, _end in iter_els_query_matches_by_lanes(
        text,
        queries,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.jobs,
    ):
        classes = position_classes(hit_positions(start, skip, len(query)), prefix_len)
        if "canonical" not in classes or "apocrypha" not in classes:
            continue
        bridge_type = classify_bridge(classes)
        total_by_type[bridge_type] += 1
        term_by_type.setdefault(query, Counter())[bridge_type] += 1

    total = sum(total_by_type.values())
    summary = {
        "control_label": label,
        "bridge_rows": total,
        "terms_with_bridge_rows": len(term_by_type),
        "apocrypha_block_letters": block_len,
        "canonical_prefix_letters": prefix_len,
        "canonical_to_apocrypha": total_by_type["canonical_to_apocrypha"],
        "apocrypha_to_canonical": total_by_type["apocrypha_to_canonical"],
        "multi_segment_bridge": total_by_type["multi_segment_bridge"],
    }
    term_rows = []
    for query, counts in sorted(term_by_type.items(), key=lambda item: (-sum(item[1].values()), item[0])):
        term_rows.append(
            {
                "control_label": label,
                "normalized_term": query,
                "bridge_rows": sum(counts.values()),
                "canonical_to_apocrypha": counts["canonical_to_apocrypha"],
                "apocrypha_to_canonical": counts["apocrypha_to_canonical"],
                "multi_segment_bridge": counts["multi_segment_bridge"],
            }
        )
    return summary, term_rows


def position_classes(positions: list[int], boundary_offset: int) -> list[str]:
    return ["canonical" if position < boundary_offset else "apocrypha" for position in positions]


def repeated_prefix(text: str, length: int) -> str:
    if not text:
        raise ValueError("control corpus has no normalized letters")
    repeats, remainder = divmod(length, len(text))
    return text * repeats + text[:remainder]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    term_rows: list[dict[str, object]],
    observed_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    observed_terms = {row["normalized_term"] for row in observed_rows}
    observed_by_type = Counter(row["bridge_type"] for row in observed_rows)
    observed_total = len(observed_rows)
    control_counts = [int(row["bridge_rows"]) for row in summary_rows]
    controls_ge = sum(1 for value in control_counts if value >= observed_total)
    lines = [
        f"# {args.canonical_label} Apocrypha Bridge Controls",
        "",
        f"Status: non-Bible boundary controls for the initial {args.canonical_label} apocrypha bridge scan.",
        "This is not a claim report.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Observed Bridge Baseline",
        "",
        f"- observed bridge rows: {observed_total}",
        f"- observed terms with bridge rows: {len(observed_terms)}",
    ]
    for bridge_type, count in sorted(observed_by_type.items()):
        lines.append(f"- observed {bridge_type}: {count}")
    lines.append(f"- non-Bible controls >= observed total: {controls_ge} of {len(control_counts)}")

    lines.extend(
        [
            "",
            "## Control Summary",
            "",
            "| Control | Bridge rows | Terms | C→A | A→C | Multi |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_md(str(row['control_label']))}`",
                    str(row["bridge_rows"]),
                    str(row["terms_with_bridge_rows"]),
                    str(row["canonical_to_apocrypha"]),
                    str(row["apocrypha_to_canonical"]),
                    str(row["multi_segment_bridge"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Top Control Terms",
            "",
            "| Control | Term | Bridge rows | C→A | A→C | Multi |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in sorted(term_rows, key=lambda item: (-int(item["bridge_rows"]), str(item["control_label"]), str(item["normalized_term"])))[:40]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_md(str(row['control_label']))}`",
                    display_term(str(row["normalized_term"])),
                    str(row["bridge_rows"]),
                    str(row["canonical_to_apocrypha"]),
                    str(row["apocrypha_to_canonical"]),
                    str(row["multi_segment_bridge"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            f"- These controls preserve the {args.canonical_label} canonical prefix",
            "  length and replace the apocrypha block with same-length non-Bible",
            "  control text.",
            "- A control match means the tested canonical/block boundary can generate",
            "  comparable cross-boundary ELS rows.",
            "- This does not answer manuscript-specific insertion order; it only tests",
            "  whether the first boundary scan is unusual against comparable",
            "  boundary opportunities.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary_rows: list[dict[str, object]],
    term_rows: list[dict[str, object]],
    observed_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_apocrypha_bridge_controls",
        "version": __version__,
        "generated_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "commit": git_commit(),
        "inputs": {
            "canonical_config": str(args.canonical_config),
            "controls": args.control,
            "terms": [str(path) for path in args.terms],
            "observed": str(args.observed),
            "jobs": args.jobs,
        },
        "outputs": {
            "summary": str(args.out),
            "term_summary": str(args.term_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "observed_rows": len(observed_rows),
        "control_rows": summary_rows,
        "term_rows": len(term_rows),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reproduce_command(args: argparse.Namespace) -> str:
    controls = " ".join(f"--control {value}" for value in args.control)
    terms = " ".join(f"--terms {path}" for path in args.terms)
    return (
        "python3 -m scripts.analyze_apocrypha_bridge_controls "
        f"--canonical-label {args.canonical_label} --canonical-config {args.canonical_config} "
        f"{controls} {terms} --observed {args.observed} "
        f"--min-skip {args.min_skip} --max-skip {args.max_skip} "
        f"--direction {args.direction} --min-term-length {args.min_term_length} "
        f"--jobs {args.jobs} "
        f"--out {args.out} --term-out {args.term_out} "
        f"--markdown-out {args.markdown_out} --manifest-out {args.manifest_out}"
    )


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
