#!/usr/bin/env python3
"""Join WRR pair rows to checked perturbation exact-match diagnostics."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


PAIR_TABLE = Path("reports/wrr_1994/wrr2_pair_eligibility_table.csv")
PERTURBATIONS = Path("reports/wrr_1994/wrr2_perturbation_diagnostics.csv")
OUT = Path("reports/wrr_1994/wrr2_perturbation_pair_readiness.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_perturbation_pair_readiness_summary.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_perturbation_pair_readiness.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_perturbation_pair_readiness.manifest.json")

FIELDNAMES = [
    "pair_id",
    "concept",
    "candidate_lane",
    "appellation_term_id",
    "date_term_id",
    "appellation_checked_hits",
    "date_checked_hits",
    "appellation_min_in_bounds",
    "date_min_in_bounds",
    "appellation_min_exact",
    "date_min_exact",
    "appellation_read",
    "date_read",
    "perturbation_readiness_status",
    "perturbation_notes",
]

SUMMARY_FIELDNAMES = [
    "pairs",
    "length_5_8_smoke_candidate_pairs",
    "pairs_outside_diagnostic_scope",
    "pairs_missing_diagnostic",
    "pairs_missing_checked_hits",
    "pairs_under_10_in_bound",
    "pairs_under_10_exact_matches",
    "pairs_ready",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    pair_rows = read_rows(args.pair_table)
    perturbations = {row["term_id"]: row for row in read_rows(args.perturbations)}
    rows = build_pair_rows(pair_rows, perturbations)
    summary = summarize(rows)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary)
    if args.manifest_out:
        write_manifest(args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair-table", type=Path, default=PAIR_TABLE)
    parser.add_argument("--perturbations", type=Path, default=PERTURBATIONS)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_pair_rows(
    pair_rows: list[dict[str, str]],
    perturbations: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    rows = []
    for pair in pair_rows:
        app = perturbations.get(pair["appellation_term_id"])
        date = perturbations.get(pair["date_term_id"])
        status, notes = pair_status(pair["candidate_lane"], app, date)
        rows.append(
            {
                "pair_id": pair["pair_id"],
                "concept": pair["concept"],
                "candidate_lane": pair["candidate_lane"],
                "appellation_term_id": pair["appellation_term_id"],
                "date_term_id": pair["date_term_id"],
                "appellation_checked_hits": field_or_empty(app, "checked_hits"),
                "date_checked_hits": field_or_empty(date, "checked_hits"),
                "appellation_min_in_bounds": field_or_empty(
                    app,
                    "min_in_bounds_perturbations",
                ),
                "date_min_in_bounds": field_or_empty(date, "min_in_bounds_perturbations"),
                "appellation_min_exact": field_or_empty(
                    app,
                    "min_exact_perturbation_matches",
                ),
                "date_min_exact": field_or_empty(date, "min_exact_perturbation_matches"),
                "appellation_read": field_or_empty(app, "read"),
                "date_read": field_or_empty(date, "read"),
                "perturbation_readiness_status": status,
                "perturbation_notes": notes,
            }
        )
    return rows


def pair_status(
    candidate_lane: str,
    app: dict[str, str] | None,
    date: dict[str, str] | None,
) -> tuple[str, str]:
    if candidate_lane != "length_5_8_smoke_candidate":
        return "outside_diagnostic_scope", f"candidate lane {candidate_lane} not checked"
    if app is None or date is None:
        return "missing_diagnostic", missing_note(app, date)

    app_hits = int_or_zero(app.get("checked_hits"))
    date_hits = int_or_zero(date.get("checked_hits"))
    if app_hits == 0 or date_hits == 0:
        return "missing_checked_hits", missing_hit_note(app_hits, date_hits)

    app_in_bound = int_or_zero(app.get("min_in_bounds_perturbations"))
    date_in_bound = int_or_zero(date.get("min_in_bounds_perturbations"))
    if app_in_bound < 10 or date_in_bound < 10:
        return "under_10_in_bound", f"min in-bound {min(app_in_bound, date_in_bound)}"

    app_exact = int_or_zero(app.get("min_exact_perturbation_matches"))
    date_exact = int_or_zero(date.get("min_exact_perturbation_matches"))
    if app_exact < 10 or date_exact < 10:
        return "under_10_exact_matches", f"min exact {min(app_exact, date_exact)}"

    return "ready", "checked hits have >=10 exact perturbed matches on both terms"


def missing_note(app: dict[str, str] | None, date: dict[str, str] | None) -> str:
    missing = []
    if app is None:
        missing.append("appellation")
    if date is None:
        missing.append("date")
    return "missing diagnostic: " + ",".join(missing)


def missing_hit_note(app_hits: int, date_hits: int) -> str:
    missing = []
    if app_hits == 0:
        missing.append("appellation")
    if date_hits == 0:
        missing.append("date")
    return "no checked hits: " + ",".join(missing)


def field_or_empty(row: dict[str, str] | None, key: str) -> str:
    if row is None:
        return ""
    return row.get(key, "")


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "pairs": len(rows),
        "length_5_8_smoke_candidate_pairs": count_where(
            rows,
            "candidate_lane",
            "length_5_8_smoke_candidate",
        ),
        "pairs_outside_diagnostic_scope": count_where(
            rows,
            "perturbation_readiness_status",
            "outside_diagnostic_scope",
        ),
        "pairs_missing_diagnostic": count_where(
            rows,
            "perturbation_readiness_status",
            "missing_diagnostic",
        ),
        "pairs_missing_checked_hits": count_where(
            rows,
            "perturbation_readiness_status",
            "missing_checked_hits",
        ),
        "pairs_under_10_in_bound": count_where(
            rows,
            "perturbation_readiness_status",
            "under_10_in_bound",
        ),
        "pairs_under_10_exact_matches": count_where(
            rows,
            "perturbation_readiness_status",
            "under_10_exact_matches",
        ),
        "pairs_ready": count_where(
            rows,
            "perturbation_readiness_status",
            "ready",
        ),
    }


def count_where(rows: list[dict[str, object]], key: str, value: str) -> int:
    return sum(1 for row in rows if row.get(key) == value)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: dict[str, object],
) -> None:
    lines = [
        "# WRR2 Perturbation Pair Readiness",
        "",
        "This joins the lock-prep pair table to the checked perturbation diagnostic.",
        "It is not a corrected-distance run; it only identifies whether checked",
        "ordinary hits currently satisfy the minimum exact-perturbation condition",
        "needed before pair-level perturbed `Q(x,y,z)` can be meaningful.",
        "",
        "## Summary",
        "",
        "| Item | Count |",
        "| --- | ---: |",
    ]
    for key in SUMMARY_FIELDNAMES:
        lines.append(f"| `{key}` | {summary[key]} |")
    lines.extend(
        [
            "",
            "## Status Counts",
            "",
            "| Status | Pairs |",
            "| --- | ---: |",
        ]
    )
    for status, count in sorted(status_counts(rows).items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(
        [
            "",
            "## First Rows",
            "",
            "| Pair | Lane | App exact | Date exact | Status |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in rows[:20]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['pair_id']}`",
                    f"`{row['candidate_lane']}`",
                    str(row["appellation_min_exact"]),
                    str(row["date_min_exact"]),
                    f"`{row['perturbation_readiness_status']}`",
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def status_counts(rows: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        status = str(row["perturbation_readiness_status"])
        counts[status] = counts.get(status, 0) + 1
    return counts


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "pair_table": str(args.pair_table),
        "perturbations": str(args.perturbations),
        "rows": len(rows),
        "summary": summary,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
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
