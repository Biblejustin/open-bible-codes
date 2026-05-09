#!/usr/bin/env python3
"""Summarize Greek exact-center extension patterns across source versions."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.statistics import numeric_value


DEFAULT_PRESENCE_FILES = {
    "two_source": Path("reports/greek_exact_center_cohort/pattern_presence.csv"),
    "three_source": Path("reports/greek_exact_center_three_source/pattern_presence.csv"),
    "four_source": Path("reports/greek_exact_center_four_source/pattern_presence.csv"),
}
DEFAULT_CONTROL_FILES = [
    Path("reports/greek_exact_center_four_source/paired_controls_summary.csv"),
    Path("reports/greek_exact_center_three_source/paired_controls_summary.csv"),
    Path("reports/sblgnt_source_only_exact_center/paired_controls_summary.csv"),
    Path("reports/byz_source_only_exact_center/paired_controls_summary.csv"),
]
SUMMARY_OUT = Path("reports/greek_pattern_versions/summary.csv")
MD_OUT = Path("reports/greek_pattern_versions/summary.md")
MANIFEST_OUT = Path("reports/greek_pattern_versions/manifest.json")

FIELDNAMES = [
    "overlap_key",
    "normalized_term",
    "skip",
    "direction",
    "extension_type",
    "extended_sequence",
    "two_source_presence",
    "three_source_presence",
    "four_source_presence",
    "current_present_corpora",
    "current_absent_corpora",
    "current_scope",
    "controlled_corpora",
    "best_q",
    "status",
    "read",
]


@dataclass(frozen=True)
class PresenceEntry:
    study: str
    row: dict[str, str]


@dataclass(frozen=True)
class ControlEntry:
    source_file: str
    row: dict[str, str]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    presence_entries = read_presence_files(args)
    control_entries = read_control_files(args.control_file)
    summary_rows = summarize_patterns(presence_entries, control_entries)
    write_rows(args.summary_out, summary_rows)
    write_markdown(args.markdown_out, summary_rows, args)
    write_manifest(args, presence_entries, control_entries, len(summary_rows), started)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--two-source-presence", type=Path, default=DEFAULT_PRESENCE_FILES["two_source"])
    parser.add_argument(
        "--three-source-presence",
        type=Path,
        default=DEFAULT_PRESENCE_FILES["three_source"],
    )
    parser.add_argument(
        "--four-source-presence",
        type=Path,
        default=DEFAULT_PRESENCE_FILES["four_source"],
    )
    parser.add_argument("--control-file", action="append", type=Path, default=DEFAULT_CONTROL_FILES)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_presence_files(args: argparse.Namespace) -> list[PresenceEntry]:
    entries: list[PresenceEntry] = []
    for study, path in [
        ("two_source", args.two_source_presence),
        ("three_source", args.three_source_presence),
        ("four_source", args.four_source_presence),
    ]:
        if not path.exists():
            continue
        for row in read_csv(path):
            entries.append(PresenceEntry(study=study, row=row))
    return entries


def read_control_files(paths: list[Path]) -> list[ControlEntry]:
    entries: list[ControlEntry] = []
    for path in paths:
        if not path.exists():
            continue
        for row in read_csv(path):
            entries.append(ControlEntry(source_file=str(path), row=row))
    return entries


def summarize_patterns(
    presence_entries: list[PresenceEntry],
    control_entries: list[ControlEntry],
) -> list[dict[str, object]]:
    presence_by_key: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for entry in presence_entries:
        presence_by_key[entry.row["overlap_key"]][entry.study] = entry.row
    controls_by_key: dict[str, list[ControlEntry]] = defaultdict(list)
    for entry in control_entries:
        controls_by_key[entry.row["overlap_key"]].append(entry)
    keys = sorted(set(presence_by_key) | set(controls_by_key))
    rows = [
        summary_row(key, presence_by_key.get(key, {}), controls_by_key.get(key, []))
        for key in keys
    ]
    return sorted(rows, key=summary_sort_key)


def summary_row(
    key: str,
    presence: dict[str, dict[str, str]],
    controls: list[ControlEntry],
) -> dict[str, object]:
    current = presence.get("four_source") or presence.get("three_source") or presence.get("two_source") or {}
    parts = key.split("|")
    current_controls = controls_for_current_presence(current, controls)
    controlled_corpora = sorted({entry.row["corpus"] for entry in current_controls})
    best_q = best_control_q(current_controls)
    status = status_for(current, controls, best_q)
    return {
        "overlap_key": key,
        "normalized_term": current.get("normalized_term") or part(parts, 0),
        "skip": current.get("skip") or part(parts, 1),
        "direction": current.get("direction") or part(parts, 2),
        "extension_type": current.get("extension_type") or part(parts, 3),
        "extended_sequence": current.get("extended_sequence") or part(parts, 4),
        "two_source_presence": presence_cell(presence.get("two_source")),
        "three_source_presence": presence_cell(presence.get("three_source")),
        "four_source_presence": presence_cell(presence.get("four_source")),
        "current_present_corpora": current.get("present_corpora", ""),
        "current_absent_corpora": current.get("absent_corpora", ""),
        "current_scope": current.get("scope", ""),
        "controlled_corpora": ",".join(controlled_corpora),
        "best_q": format_float(best_q),
        "status": status,
        "read": read_label(status, current, controls),
    }


def presence_cell(row: dict[str, str] | None) -> str:
    if row is None:
        return ""
    missing = row.get("absent_corpora", "")
    if missing:
        return f"{row.get('present_corpora', '')}; missing {missing}"
    return row.get("present_corpora", "")


def best_control_q(controls: list[ControlEntry]) -> float | None:
    values = [numeric_value(entry.row.get("combined_min_q")) for entry in controls]
    numeric = [value for value in values if value is not None]
    if not numeric:
        return None
    return min(numeric)


def controls_for_current_presence(
    current: dict[str, str],
    controls: list[ControlEntry],
) -> list[ControlEntry]:
    if not current:
        return controls
    present = set(split_cell(current.get("present_corpora", "")))
    matched = [
        entry
        for entry in controls
        if control_presence(entry.row) == present
    ]
    return matched or controls


def control_presence(row: dict[str, str]) -> set[str]:
    overlap_corpora = row.get("overlap_corpora", "")
    if overlap_corpora:
        return set(split_cell(overlap_corpora))
    corpus = row.get("corpus", "")
    return {corpus} if corpus else set()


def status_for(
    current: dict[str, str],
    controls: list[ControlEntry],
    best_q: float | None,
) -> str:
    if best_q is None or best_q > 0.01:
        return "presence_only"
    current_scope = current.get("scope", "")
    present = set(split_cell(current.get("present_corpora", "")))
    if current_scope == "all_sources" and len(present) >= 4:
        return "four_source_controlled_review_candidate"
    if current_scope in {"all_sources", "multi_source"} and len(present) > 1:
        return "multi_source_controlled_review_candidate"
    return "source_specific_review_candidate"


def read_label(
    status: str,
    current: dict[str, str],
    controls: list[ControlEntry],
) -> str:
    if status == "four_source_controlled_review_candidate":
        return "strongest review queue item; still hidden-path and not a claim"
    if status == "multi_source_controlled_review_candidate":
        return "multi-source review queue item; inspect source-family distribution"
    if status == "source_specific_review_candidate":
        return "version-specific review queue item; source-only boundary applies"
    if current:
        return "presence row without favorable controls"
    if controls:
        return "control row without current presence matrix entry"
    return "unclassified"


def summary_sort_key(row: dict[str, object]) -> tuple[int, str, str]:
    status_order = {
        "four_source_controlled_review_candidate": 0,
        "multi_source_controlled_review_candidate": 1,
        "source_specific_review_candidate": 2,
        "presence_only": 3,
    }
    return (
        status_order.get(str(row["status"]), 9),
        str(row["normalized_term"]),
        str(row["overlap_key"]),
    )


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Greek Pattern Version Summary",
        "",
        "This report merges exact-center extension pattern-presence matrices and",
        "row-local control summaries. It asks which exact patterns appear in which",
        "Greek NT source texts, not whether every pattern appears in every source.",
        "",
        "## Inputs",
        "",
        f"- Two-source presence: `{args.two_source_presence}`",
        f"- Three-source presence: `{args.three_source_presence}`",
        f"- Four-source presence: `{args.four_source_presence}`",
        "",
        "## Current Pattern Status",
        "",
        "| Pattern | Current presence | Missing | Controlled corpora | Best q | Status | Read |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['overlap_key']}`",
                    str(row["current_present_corpora"]),
                    str(row["current_absent_corpora"]),
                    str(row["controlled_corpora"]),
                    str(row["best_q"]),
                    f"`{row['status']}`",
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
            "This is a review-queue summary. A source-specific row can be worth",
            "examining inside that source while still being much weaker than a",
            "cross-source row. Hidden-path rows are not claims.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    presence_entries: list[PresenceEntry],
    control_entries: list[ControlEntry],
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_greek_pattern_versions",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "presence_entries": len(presence_entries),
        "control_entries": len(control_entries),
        "rows": rows,
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def split_cell(value: str) -> list[str]:
    return [item for item in value.split(",") if item]


def part(parts: list[str], index: int) -> str:
    if index >= len(parts):
        return ""
    return parts[index]


def format_float(value: float | None) -> str:
    if value is None:
        return ""
    return str(round(value, 6))


if __name__ == "__main__":
    raise SystemExit(main())
