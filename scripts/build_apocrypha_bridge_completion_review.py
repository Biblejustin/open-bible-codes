#!/usr/bin/env python3
"""Build a review packet for apocrypha bridge-completion candidates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from els import __version__
from els.report_index import write_text_if_changed
from els.term_display import display_term


DEFAULT_INPUTS = [
    "LXX=reports/apocrypha_bridge_candidates/bridge_candidates.csv",
    "KJVA=reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv",
]
DEFAULT_OUT = Path("reports/apocrypha_bridge_completion_review/completion_rows.csv")
DEFAULT_SUMMARY = Path("reports/apocrypha_bridge_completion_review/summary.csv")
DEFAULT_MARKDOWN = Path("docs/APOCRYPHA_BRIDGE_COMPLETION_REVIEW.md")
DEFAULT_MANIFEST = Path("reports/apocrypha_bridge_completion_review/manifest.json")

LETTER_RE = re.compile(r"^(?P<index>\d+):(?P<letter>.+)@(?P<ref>.+):(?P<class>canonical|apocrypha):(?P<position>-?\d+)$")

FIELDNAMES = [
    "source",
    "source_rank",
    "bridge_type",
    "term_ids",
    "concepts",
    "categories",
    "normalized_term",
    "term_length",
    "skip",
    "direction",
    "start_ref",
    "center_ref",
    "end_ref",
    "apocrypha_books",
    "class_path",
    "canonical_letter_count",
    "apocrypha_completion_count",
    "canonical_fraction",
    "completion_fraction",
    "canonical_partial_pattern",
    "apocrypha_completion_pattern",
    "canonical_letters",
    "apocrypha_completion_letters",
    "canonical_letter_indexes",
    "apocrypha_completion_indexes",
    "center_word",
    "center_normalized_word",
    "canonical_only_complete",
    "expanded_stream_complete",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


@dataclass(frozen=True)
class CandidateInput:
    source: str
    path: Path


@dataclass(frozen=True)
class LetterStep:
    index: int
    letter: str
    ref: str
    source_class: str
    position: int


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_specs = args.input if args.input is not None else DEFAULT_INPUTS
    inputs = [parse_input_spec(value) for value in input_specs]
    rows = build_completion_rows(inputs)
    summary = summarize(rows, inputs)
    write_csv(args.out, rows, FIELDNAMES)
    write_csv(args.summary_out, summary, SUMMARY_FIELDNAMES)
    write_markdown(args.markdown_out, rows, summary, inputs)
    write_manifest(args.manifest_out, inputs, args, rows, summary)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", help="SOURCE=bridge_candidates.csv")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def parse_input_spec(value: str) -> CandidateInput:
    if "=" not in value:
        raise ValueError(f"input must be SOURCE=path: {value}")
    source, path = value.split("=", 1)
    source = source.strip()
    if not source:
        raise ValueError(f"input source is empty: {value}")
    return CandidateInput(source=source, path=Path(path))


def build_completion_rows(inputs: Iterable[CandidateInput]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in inputs:
        if not item.path.exists():
            continue
        with item.path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for source_row in reader:
                letter_steps = parse_letter_path(source_row.get("letter_path", ""))
                if not letter_steps:
                    continue
                row = completion_row(item.source, source_row, letter_steps)
                if row["expanded_stream_complete"] == "yes" and row["canonical_only_complete"] == "no":
                    rows.append(row)
    return sorted(rows, key=completion_sort_key)


def completion_row(source: str, row: dict[str, str], letter_steps: list[LetterStep]) -> dict[str, object]:
    term_length = int(row.get("term_length") or len(row.get("normalized_term", "")))
    canonical_steps = [step for step in letter_steps if step.source_class == "canonical"]
    apocrypha_steps = [step for step in letter_steps if step.source_class == "apocrypha"]
    canonical_count = len(canonical_steps)
    apocrypha_count = len(apocrypha_steps)
    canonical_indexes = [step.index for step in canonical_steps]
    apocrypha_indexes = [step.index for step in apocrypha_steps]
    return {
        "source": source,
        "source_rank": row.get("rank", ""),
        "bridge_type": row.get("bridge_type", ""),
        "term_ids": row.get("term_ids", ""),
        "concepts": row.get("concepts", ""),
        "categories": row.get("categories", ""),
        "normalized_term": row.get("normalized_term", ""),
        "term_length": term_length,
        "skip": row.get("skip", ""),
        "direction": row.get("direction", ""),
        "start_ref": row.get("start_ref", ""),
        "center_ref": row.get("center_ref", ""),
        "end_ref": row.get("end_ref", ""),
        "apocrypha_books": row.get("apocrypha_books", ""),
        "class_path": row.get("class_path", ""),
        "canonical_letter_count": canonical_count,
        "apocrypha_completion_count": apocrypha_count,
        "canonical_fraction": fraction(canonical_count, term_length),
        "completion_fraction": fraction(apocrypha_count, term_length),
        "canonical_partial_pattern": pattern(letter_steps, "canonical"),
        "apocrypha_completion_pattern": pattern(letter_steps, "apocrypha"),
        "canonical_letters": "".join(step.letter for step in canonical_steps),
        "apocrypha_completion_letters": "".join(step.letter for step in apocrypha_steps),
        "canonical_letter_indexes": join_ints(canonical_indexes),
        "apocrypha_completion_indexes": join_ints(apocrypha_indexes),
        "center_word": row.get("center_word", ""),
        "center_normalized_word": row.get("center_normalized_word", ""),
        "canonical_only_complete": "yes" if canonical_count == term_length else "no",
        "expanded_stream_complete": "yes" if canonical_count + apocrypha_count == term_length else "no",
    }


def parse_letter_path(value: str) -> list[LetterStep]:
    steps: list[LetterStep] = []
    for part in value.split(";"):
        part = part.strip()
        if not part:
            continue
        match = LETTER_RE.match(part)
        if match is None:
            raise ValueError(f"cannot parse letter_path part: {part}")
        steps.append(
            LetterStep(
                index=int(match.group("index")),
                letter=match.group("letter"),
                ref=match.group("ref"),
                source_class=match.group("class"),
                position=int(match.group("position")),
            )
        )
    return sorted(steps, key=lambda step: step.index)


def pattern(steps: list[LetterStep], source_class: str) -> str:
    return "".join(step.letter if step.source_class == source_class else "." for step in steps)


def fraction(count: int, total: int) -> str:
    if total <= 0:
        return "0.000000"
    return f"{count / total:.6f}"


def join_ints(values: Iterable[int]) -> str:
    return ";".join(str(value) for value in values)


def completion_sort_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        str(row["source"]),
        int(row["apocrypha_completion_count"]),
        abs(int(row["skip"])),
        int(row["source_rank"]),
        str(row["normalized_term"]),
    )


def summarize(rows: list[dict[str, object]], inputs: list[CandidateInput]) -> list[dict[str, object]]:
    source_counts = Counter(str(row["source"]) for row in rows)
    bridge_counts = Counter((str(row["source"]), str(row["bridge_type"])) for row in rows)
    completion_counts = Counter((str(row["source"]), str(row["apocrypha_completion_count"])) for row in rows)
    term_counts = {
        source: len({str(row["normalized_term"]) for row in rows if row["source"] == source})
        for source in sorted(source_counts)
    }
    summary: list[dict[str, object]] = [
        {"metric": "input_files", "value": len(inputs)},
        {"metric": "completion_rows", "value": len(rows)},
        {"metric": "terms_with_completion_rows", "value": len({str(row["normalized_term"]) for row in rows})},
    ]
    for source, count in sorted(source_counts.items()):
        summary.append({"metric": f"source:{source}:completion_rows", "value": count})
        summary.append({"metric": f"source:{source}:terms_with_completion_rows", "value": term_counts[source]})
    for (source, bridge_type), count in sorted(bridge_counts.items()):
        summary.append({"metric": f"source:{source}:bridge_type:{bridge_type}", "value": count})
    for (source, completion_count), count in sorted(completion_counts.items(), key=lambda item: (item[0][0], int(item[0][1]))):
        summary.append({"metric": f"source:{source}:apocrypha_completion_letters:{completion_count}", "value": count})
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
    inputs: list[CandidateInput],
) -> None:
    lines = [
        "# Apocrypha Bridge Completion Review",
        "",
        "Status: derived review packet. This is not a claim report.",
        "",
        "This report restates existing bridge candidates as completion rows:",
        "the expanded stream supplies a full ELS, while the canonical-only",
        "letters would leave a partial path under the same skip and direction.",
        "",
        "## Inputs",
        "",
    ]
    for item in inputs:
        lines.append(f"- {item.source}: `{item.path}`")
    lines.extend(["", "## Summary", ""])
    for row in summary:
        lines.append(f"- {row['metric']}: {row['value']}")
    lines.extend(
        [
            "",
            "## Shortest Completion Rows By Source",
            "",
        ]
    )
    source_order = [item.source for item in inputs]
    for source in source_order:
        source_rows = [row for row in rows if row["source"] == source]
        if not source_rows:
            continue
        lines.extend(
            [
                "",
                f"### {source}",
                "",
                "| Source rank | Term | Skip | Type | Start | Center | End | Canonical partial | Apocrypha completion | Completion indexes | Center word |",
                "| ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in source_rows[:40]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["source_rank"]),
                        display_term(str(row["normalized_term"]), english=str(row["concepts"]).split(";")[0] or None),
                        str(row["skip"]),
                        f"`{escape_md(str(row['bridge_type']))}`",
                        escape_md(str(row["start_ref"])),
                        escape_md(str(row["center_ref"])),
                        escape_md(str(row["end_ref"])),
                        f"`{escape_md(str(row['canonical_partial_pattern']))}`",
                        f"`{escape_md(str(row['apocrypha_completion_pattern']))}`",
                        escape_md(str(row["apocrypha_completion_indexes"])),
                        escape_md(str(row["center_word"])),
                    ]
                )
                + " |"
            )
        if len(source_rows) > 40:
            lines.append(
                f"| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | {len(source_rows) - 40} more rows in CSV |"
            )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- `canonical_partial_pattern` preserves canonical-text letters and marks apocrypha-supplied letters with `.`.",
            "- `apocrypha_completion_pattern` preserves the apocrypha/deuterocanon letters that complete the ELS and marks canonical letters with `.`.",
            "- Every row here is complete in the expanded stream and incomplete in canonical-only text under the same path.",
            "- This report records that the bridge-completion event exists; significance still depends on the paired non-Bible and shuffled-insertion controls.",
        ]
    )
    write_text_if_changed(path, "\n".join(lines).rstrip() + "\n")


def write_manifest(
    path: Path,
    inputs: list[CandidateInput],
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> None:
    payload = {
        "tool": "build_apocrypha_bridge_completion_review",
        "version": __version__,
        "commit": git_commit(),
        "inputs": [
            {
                "source": item.source,
                "path": str(item.path),
                "sha256": sha256_file(item.path) if item.path.exists() else "",
            }
            for item in inputs
        ],
        "outputs": {
            "rows": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "row_count": len(rows),
        "summary": summary,
    }
    write_text_if_changed(path, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
