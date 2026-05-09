#!/usr/bin/env python3
"""Remove audited prior-evidence overlaps from a prospective term file."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.normalization import normalize_text


DEFAULT_DROP_SEVERITIES = ("block", "review")
DEFAULT_OUT = Path("reports/study_locks/prospective_terms.filtered.csv")


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows, fieldnames = read_candidate_rows(args.candidate)
    audit_rows = read_audit_rows(args.audit)
    drop_severities = set(args.drop_severity or DEFAULT_DROP_SEVERITIES)
    drop_ids = audited_term_ids(
        audit_rows,
        candidate_path=args.candidate,
        drop_severities=drop_severities,
    )
    short_ids = short_term_ids(rows, min_normalized_length=args.min_normalized_length)
    all_drop_ids = drop_ids | short_ids
    kept_rows = [row for row in rows if row.get("term_id", "") not in all_drop_ids]
    dropped_rows = [row for row in rows if row.get("term_id", "") in all_drop_ids]
    write_candidate_rows(args.out, fieldnames, kept_rows)
    status = "passed" if len(kept_rows) >= args.min_remaining else "failed"
    summary_path = args.summary_out or args.out.with_suffix(args.out.suffix + ".summary.json")
    write_summary(
        summary_path,
        {
            "tool": "filter_prospective_terms",
            "edls_version": __version__,
            "generated_at": datetime.now(UTC).isoformat(),
            "duration_seconds": round(time.perf_counter() - started, 6),
            "status": status,
            "candidate": str(args.candidate),
            "audit": str(args.audit),
            "out": str(args.out),
            "drop_severities": sorted(drop_severities),
            "input_rows": len(rows),
            "output_rows": len(kept_rows),
            "dropped_rows": len(dropped_rows),
            "dropped_term_ids": sorted(all_drop_ids),
            "audit_dropped_term_ids": sorted(drop_ids),
            "short_dropped_term_ids": sorted(short_ids),
            "audit_severity_counts": dict(Counter(row.get("severity", "") for row in audit_rows)),
            "min_normalized_length": args.min_normalized_length,
            "min_remaining": args.min_remaining,
        },
    )
    print(args.out)
    print(summary_path)
    if status != "passed":
        print(
            "prospective term filter failure: "
            f"remaining rows {len(kept_rows)} < min_remaining {args.min_remaining}"
        )
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path)
    parser.add_argument("--min-normalized-length", type=int, default=1)
    parser.add_argument(
        "--drop-severity",
        action="append",
        default=[],
        help="Audit severity to remove. Defaults to block and review.",
    )
    parser.add_argument("--min-remaining", type=int, default=1)
    return parser


def short_term_ids(rows: list[dict[str, str]], *, min_normalized_length: int) -> set[str]:
    short_ids: set[str] = set()
    for row in rows:
        term_id = row.get("term_id", "")
        if not term_id:
            continue
        language = row.get("language", "")
        term = row.get("term", "")
        if len(normalize_text(term, language)) < min_normalized_length:
            short_ids.add(term_id)
    return short_ids


def read_candidate_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [{key: value or "" for key, value in row.items() if key is not None} for row in reader]
    if "term_id" not in fieldnames:
        raise ValueError(f"candidate file missing term_id column: {path}")
    return rows, fieldnames


def read_audit_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [
            {key: value or "" for key, value in row.items() if key is not None}
            for row in csv.DictReader(handle)
        ]


def audited_term_ids(
    audit_rows: list[dict[str, str]],
    *,
    candidate_path: Path,
    drop_severities: set[str],
) -> set[str]:
    return {
        row["candidate_term_id"]
        for row in audit_rows
        if row.get("severity", "") in drop_severities
        and row.get("candidate_term_id", "")
        and audit_row_matches_candidate(row, candidate_path)
    }


def audit_row_matches_candidate(row: dict[str, str], candidate_path: Path) -> bool:
    audit_path = row.get("candidate_file", "").strip()
    if not audit_path:
        return True
    return same_path(Path(audit_path), candidate_path)


def same_path(left: Path, right: Path) -> bool:
    return left.resolve(strict=False) == right.resolve(strict=False)


def write_candidate_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
