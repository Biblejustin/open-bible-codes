#!/usr/bin/env python3
"""Build target-summary rows for English seed survivor paired controls."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path


DEFAULT_AUDIT_SUMMARY = Path("reports/english_seed_survivor_audit/summary.csv")
DEFAULT_OUT = Path("reports/english_seed_survivor_targets/target_summary.csv")
DEFAULT_MANIFEST = Path("reports/english_seed_survivor_targets/manifest.json")

FIELDNAMES = [
    "corpus",
    "term_set",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "hit_count",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = build_rows(read_rows(args.audit_summary))
    write_rows(args.out, rows)
    write_manifest(args, rows, started)
    print(args.out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-summary", type=Path, default=DEFAULT_AUDIT_SUMMARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_rows(audit_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows_by_key: dict[tuple[str, str], dict[str, str]] = {}
    for row in audit_rows:
        key = (row["corpus"], row["term_id"])
        if key in rows_by_key:
            continue
        rows_by_key[key] = {
            "corpus": row["corpus"],
            "term_set": "english_seed_followup_survivors",
            "term_id": row["term_id"],
            "concept": row["concept"],
            "category": row["category"],
            "term_language": "english",
            "term": row["term"],
            "normalized_term": row["normalized_term"],
            "hit_count": row["term_shuffle_observed"],
        }
    return sorted(rows_by_key.values(), key=lambda row: (row["corpus"], row["term_id"]))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "build_english_seed_survivor_targets",
        "created_utc": datetime.now(UTC).isoformat(),
        "audit_summary": str(args.audit_summary),
        "rows": len(rows),
        "seconds": round(time.perf_counter() - started, 3),
        "outputs": [str(args.out), str(args.manifest_out)],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
