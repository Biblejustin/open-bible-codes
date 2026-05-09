#!/usr/bin/env python3
"""Convert WRR-style plain-text rabbi/date lists into repo term CSV rows."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


FIELDNAMES = ["term_id", "concept", "category", "language", "term", "notes"]


@dataclass(frozen=True)
class WrrRecord:
    index: int
    appellations: tuple[str, ...]
    dates: tuple[str, ...]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    records = parse_wrr_records(args.source.read_text(encoding=args.encoding))
    rows = term_rows(
        records,
        list_label=args.list_label,
        language=args.language,
        source_note=args.source_note,
        include_undated=args.include_undated,
    )
    write_rows(args.out, rows)
    print(args.out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--list-label", default="wrr2")
    parser.add_argument("--language", default="michigan")
    parser.add_argument(
        "--source-note",
        default="external WRR plain-text list; verify against primary paper before claiming reproduction",
    )
    parser.add_argument(
        "--include-undated",
        action="store_true",
        help="Keep appellation rows for records with no date rows.",
    )
    return parser


def parse_wrr_records(text: str) -> list[WrrRecord]:
    tokens = clean_wrr_text(text).split()
    index = first_record_index(tokens)
    records: list[WrrRecord] = []
    record_number = 1
    while index < len(tokens):
        if index + 1 >= len(tokens):
            raise ValueError(f"trailing token without count pair at token {index}: {tokens[index]!r}")
        if not tokens[index].isdigit() or not tokens[index + 1].isdigit():
            raise ValueError(
                f"expected appellation/date count pair at token {index}: "
                f"{tokens[index]!r} {tokens[index + 1]!r}"
            )
        appellation_count = int(tokens[index])
        date_count = int(tokens[index + 1])
        index += 2
        next_index = index + appellation_count + date_count
        if next_index > len(tokens):
            raise ValueError(f"record {record_number} count exceeds remaining tokens")
        appellations = tuple(tokens[index : index + appellation_count])
        dates = tuple(tokens[index + appellation_count : next_index])
        records.append(WrrRecord(record_number, appellations, dates))
        record_number += 1
        index = next_index
    return records


def clean_wrr_text(text: str) -> str:
    """Remove known prose annotations around ANU WRR-style record data."""
    body = text.split("Note:", 1)[0]
    return body.replace("[See note]", " ")


def first_record_index(tokens: list[str]) -> int:
    for index in range(max(0, len(tokens) - 1)):
        if tokens[index].isdigit() and tokens[index + 1].isdigit():
            return index
    raise ValueError("no WRR record count pair found")


def term_rows(
    records: list[WrrRecord],
    *,
    list_label: str,
    language: str,
    source_note: str,
    include_undated: bool = False,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for record in records:
        if not record.dates and not include_undated:
            continue
        concept = f"{list_label.upper()} {record.index:02d}"
        for app_index, appellation in enumerate(record.appellations, start=1):
            rows.append(
                {
                    "term_id": f"{list_label}_{record.index:02d}_app_{app_index:02d}",
                    "concept": concept,
                    "category": "wrr_appellation",
                    "language": language,
                    "term": appellation,
                    "notes": source_note,
                }
            )
        for date_index, date in enumerate(record.dates, start=1):
            rows.append(
                {
                    "term_id": f"{list_label}_{record.index:02d}_date_{date_index:02d}",
                    "concept": concept,
                    "category": "wrr_date",
                    "language": language,
                    "term": date,
                    "notes": source_note,
                }
            )
    return rows


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
