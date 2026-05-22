#!/usr/bin/env python3
"""Validate WRR manual-decision records against the current register."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DEFAULT_RECORDS = Path("data/study/mappings/wrr_manual_decision_records.csv")
DEFAULT_REGISTER_DOC = Path("docs/WRR_MANUAL_DECISION_REGISTER.md")

REQUIRED_COLUMNS = (
    "decision_id",
    "register_decision_rank",
    "decision_lane",
    "review_state",
    "decision_target",
    "source_checklist",
    "decision_status",
    "selected_action",
    "evidence_citation",
    "evidence_summary",
    "locked_by",
    "locked_at",
    "notes",
)

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

REGISTER_HEADER = (
    "Rank",
    "Lane",
    "State",
    "Target",
    "Concept",
    "Row",
    "Terms",
    "Pairs",
    "Frontier",
    "Checklist",
    "Next manual action",
)


@dataclass(frozen=True)
class RegisterDecision:
    rank: int
    lane: str
    state: str
    target: str
    checklist: str


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_decision_records(args.records, args.register_doc)
    if failures:
        for failure in failures:
            print(f"WRR manual decision records failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR manual decision records ok: {args.records}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS)
    parser.add_argument("--register-doc", type=Path, default=DEFAULT_REGISTER_DOC)
    return parser


def validate_decision_records(records: Path, register_doc: Path) -> list[str]:
    failures: list[str] = []
    if not records.exists():
        return [f"{records} is missing"]
    register, register_failures = load_register_decisions(register_doc)
    failures.extend(register_failures)

    with records.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        missing = sorted(set(REQUIRED_COLUMNS) - set(fieldnames))
        if missing:
            return [f"{records} missing required columns: {', '.join(missing)}"]
        rows = list(reader)

    seen_ids: set[str] = set()
    seen_ranks: set[int] = set()
    for row_number, row in enumerate(rows, start=2):
        failures.extend(
            validate_row(records, row_number, row, register, seen_ids, seen_ranks)
        )
    return failures


def load_register_decisions(register_doc: Path) -> tuple[dict[int, RegisterDecision], list[str]]:
    if not register_doc.exists():
        return {}, [f"{register_doc} is missing"]
    decisions: dict[int, RegisterDecision] = {}
    in_decision_table = False
    for line in register_doc.read_text(encoding="utf-8").splitlines():
        cells = parse_markdown_row(line)
        if not cells:
            if in_decision_table:
                break
            continue
        if tuple(cells[: len(REGISTER_HEADER)]) == REGISTER_HEADER:
            in_decision_table = True
            continue
        if not in_decision_table or cells[0].startswith("---"):
            continue
        try:
            rank = int(cells[0])
        except ValueError:
            continue
        decisions[rank] = RegisterDecision(
            rank=rank,
            lane=strip_code(cells[1]),
            state=strip_code(cells[2]),
            target=strip_code(cells[3]),
            checklist=strip_code(cells[9]),
        )
    if not decisions:
        return {}, [f"{register_doc} has no decision register rows"]
    return decisions, []


def parse_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def validate_row(
    records: Path,
    row_number: int,
    row: dict[str, str | None],
    register: dict[int, RegisterDecision],
    seen_ids: set[str],
    seen_ranks: set[int],
) -> list[str]:
    failures: list[str] = []
    if None in row:
        failures.append(f"{records}:{row_number} has extra unheadered columns")

    decision_id = clean(row.get("decision_id"))
    if decision_id in seen_ids:
        failures.append(f"{records}:{row_number} duplicate decision_id: {decision_id}")
    seen_ids.add(decision_id)

    rank_text = clean(row.get("register_decision_rank"))
    try:
        rank = int(rank_text)
    except ValueError:
        failures.append(f"{records}:{row_number} register_decision_rank must be integer")
        rank = -1

    if rank in seen_ranks:
        failures.append(f"{records}:{row_number} duplicate register_decision_rank: {rank}")
    seen_ranks.add(rank)

    expected_id = f"wrr_decision_{rank:03d}"
    if rank > 0 and decision_id != expected_id:
        failures.append(
            f"{records}:{row_number} decision_id must be {expected_id} for rank {rank}"
        )

    expected = register.get(rank)
    if rank > 0 and expected is None:
        failures.append(f"{records}:{row_number} rank {rank} not in manual register")
    elif expected is not None:
        failures.extend(validate_register_match(records, row_number, row, expected))

    for column in (
        "decision_status",
        "selected_action",
        "evidence_citation",
        "evidence_summary",
        "locked_by",
    ):
        if is_placeholder(row.get(column)):
            failures.append(f"{records}:{row_number} placeholder value for {column}")

    evidence_summary = clean(row.get("evidence_summary"))
    if evidence_summary and len(evidence_summary) < 20:
        failures.append(f"{records}:{row_number} evidence_summary is too short")

    locked_at = clean(row.get("locked_at"))
    try:
        date.fromisoformat(locked_at)
    except ValueError:
        failures.append(f"{records}:{row_number} locked_at must be ISO date")

    return failures


def validate_register_match(
    records: Path,
    row_number: int,
    row: dict[str, str | None],
    expected: RegisterDecision,
) -> list[str]:
    checks = (
        ("decision_lane", expected.lane),
        ("review_state", expected.state),
        ("decision_target", expected.target),
        ("source_checklist", expected.checklist),
    )
    failures: list[str] = []
    for column, expected_value in checks:
        value = clean(row.get(column))
        if value != expected_value:
            failures.append(
                f"{records}:{row_number} {column} must match register: {expected_value}"
            )
    return failures


def strip_code(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def is_placeholder(value: str | None) -> bool:
    return clean(value).casefold() in PLACEHOLDER_VALUES


def clean(value: str | None) -> str:
    return (value or "").strip()


if __name__ == "__main__":
    raise SystemExit(main())
