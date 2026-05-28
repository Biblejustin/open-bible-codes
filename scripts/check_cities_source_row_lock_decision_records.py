#!/usr/bin/env python3
"""Validate Cities source-row lock decision records."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path


DEFAULT_RECORDS = Path("data/study/mappings/cities_source_row_lock_decisions.csv")
DEFAULT_EVIDENCE_PACKET = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_packet.csv"
)

REQUIRED_COLUMNS = (
    "decision_id",
    "queue_lock_rank",
    "label",
    "page_number",
    "page_class",
    "decision_status",
    "selected_action",
    "evidence_citation",
    "evidence_summary",
    "locked_by",
    "locked_at",
    "notes",
)

MATCH_COLUMNS = (
    "queue_lock_rank",
    "label",
    "page_number",
    "page_class",
)

ALLOWED_STATUSES = {
    "unrecorded",
    "locked",
    "deferred_no_lock",
}

ALLOWED_ACTIONS = {
    "",
    "no_source_row_import",
    "source_row_lock_ready",
    "exclude_page_from_source_rows",
    "deferred_no_lock",
}

LOCKED_ACTIONS = {
    "no_source_row_import",
    "source_row_lock_ready",
    "exclude_page_from_source_rows",
}

PLACEHOLDER_VALUES = {
    "",
    "na",
    "n/a",
    "none",
    "pending",
    "review",
    "todo",
    "tbd",
    "unknown",
    "needs review",
    "needs_review",
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_decision_records(args.records, args.evidence_packet)
    if failures:
        for failure in failures:
            print(
                f"Cities source-row lock decision records failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-row lock decision records ok: {args.records}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS)
    parser.add_argument("--evidence-packet", type=Path, default=DEFAULT_EVIDENCE_PACKET)
    return parser


def validate_decision_records(
    records: Path,
    evidence_packet: Path,
) -> list[str]:
    failures: list[str] = []
    if not records.exists():
        return [f"{records} is missing"]

    evidence_rows, evidence_failures = load_evidence_rows(evidence_packet)
    failures.extend(evidence_failures)

    with records.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        missing = sorted(set(REQUIRED_COLUMNS) - set(fieldnames))
        if missing:
            return [f"{records} missing required columns: {', '.join(missing)}"]
        extra = sorted(set(fieldnames) - set(REQUIRED_COLUMNS))
        if extra:
            return [f"{records} has unexpected columns: {', '.join(extra)}"]
        rows = list(reader)

    seen_ids: set[str] = set()
    seen_ranks: set[int] = set()
    for row_number, row in enumerate(rows, start=2):
        failures.extend(
            validate_row(records, row_number, row, evidence_rows, seen_ids, seen_ranks)
        )
    return failures


def load_evidence_rows(path: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    if not path.exists():
        return {}, [f"{path} is missing"]
    rows: dict[str, dict[str, str]] = {}
    failures: list[str] = []
    for row_number, row in enumerate(read_csv(path), start=2):
        decision_id = clean(row.get("decision_id"))
        if not decision_id:
            failures.append(f"{path}:{row_number} missing decision_id")
            continue
        if decision_id in rows:
            failures.append(f"{path}:{row_number} duplicate decision_id: {decision_id}")
        rows[decision_id] = row
    if len(rows) != 14:
        failures.append(f"{path} has {len(rows)} evidence rows, expected 14")
    return rows, failures


def validate_row(
    records: Path,
    row_number: int,
    row: dict[str, str | None],
    evidence_rows: dict[str, dict[str, str]],
    seen_ids: set[str],
    seen_ranks: set[int],
) -> list[str]:
    failures: list[str] = []
    if None in row:
        failures.append(f"{records}:{row_number} has extra unheadered columns")

    if contains_source_script(" ".join(clean(value) for value in row.values())):
        failures.append(f"{records}:{row_number} appears to contain source-script text")

    decision_id = clean(row.get("decision_id"))
    if decision_id in seen_ids:
        failures.append(f"{records}:{row_number} duplicate decision_id: {decision_id}")
    seen_ids.add(decision_id)

    rank = parse_rank(records, row_number, clean(row.get("queue_lock_rank")), failures)
    if rank in seen_ranks:
        failures.append(f"{records}:{row_number} duplicate queue_lock_rank: {rank}")
    seen_ranks.add(rank)

    expected_id = f"cities_source_row_lock_{rank:03d}"
    if rank > 0 and decision_id != expected_id:
        failures.append(
            f"{records}:{row_number} decision_id must be {expected_id} for rank {rank}"
        )

    evidence = evidence_rows.get(decision_id)
    if evidence is None:
        failures.append(f"{records}:{row_number} decision_id not in evidence packet")
    else:
        failures.extend(validate_evidence_match(records, row_number, row, evidence))

    status = clean(row.get("decision_status"))
    action = clean(row.get("selected_action"))
    if status not in ALLOWED_STATUSES:
        failures.append(f"{records}:{row_number} unsupported decision_status: {status}")
    if action not in ALLOWED_ACTIONS:
        failures.append(f"{records}:{row_number} unsupported selected_action: {action}")

    failures.extend(
        validate_status_action(records, row_number, row, status, action, decision_id)
    )
    return failures


def parse_rank(
    records: Path,
    row_number: int,
    rank_text: str,
    failures: list[str],
) -> int:
    try:
        rank = int(rank_text)
    except ValueError:
        failures.append(f"{records}:{row_number} queue_lock_rank must be integer")
        return -1
    if rank < 1 or rank > 14:
        failures.append(f"{records}:{row_number} queue_lock_rank out of range: {rank}")
    return rank


def validate_evidence_match(
    records: Path,
    row_number: int,
    row: dict[str, str | None],
    evidence: dict[str, str],
) -> list[str]:
    failures: list[str] = []
    for column in MATCH_COLUMNS:
        value = clean(row.get(column))
        expected = clean(evidence.get(column))
        if value != expected:
            failures.append(
                f"{records}:{row_number} {column} must match evidence packet: {expected}"
            )
    return failures


def validate_status_action(
    records: Path,
    row_number: int,
    row: dict[str, str | None],
    status: str,
    action: str,
    decision_id: str,
) -> list[str]:
    failures: list[str] = []
    if status == "unrecorded":
        if action:
            failures.append(
                f"{records}:{row_number} unrecorded row must not select an action"
            )
        return failures

    if status == "locked" and action not in LOCKED_ACTIONS:
        failures.append(f"{records}:{row_number} locked row needs a locked action")
    if status == "deferred_no_lock" and action != "deferred_no_lock":
        failures.append(
            f"{records}:{row_number} deferred_no_lock row must select deferred_no_lock"
        )

    for column in (
        "evidence_citation",
        "evidence_summary",
        "locked_by",
    ):
        if is_placeholder(row.get(column)):
            failures.append(f"{records}:{row_number} placeholder value for {column}")

    evidence_summary = clean(row.get("evidence_summary"))
    if evidence_summary and len(evidence_summary) < 30:
        failures.append(f"{records}:{row_number} evidence_summary is too short")

    citation = clean(row.get("evidence_citation"))
    if citation and not cites_evidence_packet(citation):
        failures.append(
            f"{records}:{row_number} evidence_citation must cite evidence packet or page image"
        )
    if decision_id and decision_id not in " ".join((citation, evidence_summary)):
        failures.append(
            f"{records}:{row_number} evidence_citation or evidence_summary must name {decision_id}"
        )

    locked_at = clean(row.get("locked_at"))
    try:
        date.fromisoformat(locked_at)
    except ValueError:
        failures.append(f"{records}:{row_number} locked_at must be ISO date")

    return failures


def cites_evidence_packet(value: str) -> bool:
    return (
        "docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md" in value
        or "reports/cities_pdf_recovery_probe/" in value
        or "page_images/" in value
    )


def contains_source_script(text: str) -> bool:
    for char in text:
        code = ord(char)
        if 0x0590 <= code <= 0x05FF or 0x0370 <= code <= 0x03FF:
            return True
    return False


def is_placeholder(value: str | None) -> bool:
    return clean(value).casefold() in PLACEHOLDER_VALUES


def clean(value: str | None) -> str:
    return (value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
