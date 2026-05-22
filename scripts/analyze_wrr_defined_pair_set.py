#!/usr/bin/env python3
"""Audit which WRR working pairs currently yield defined corrected distances."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_PAIR_SUMMARY = Path("reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv")
DEFAULT_PAIR_TABLE = Path("reports/wrr_1994/wrr2_pair_eligibility_table.csv")
DEFAULT_RUNS = (
    (
        "all_lanes_cap250",
        Path("reports/wrr_1994/direct_all/wrr2_corrected_distance_all_lanes_250.csv"),
    ),
    (
        "all_lanes_cap1000",
        Path("reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged.csv"),
    ),
    (
        "all_lanes_cap1000_program",
        Path(
            "reports/wrr_1994/direct_all/highcap_1000_program/"
            "wrr2_corrected_distance_all_lanes_merged.csv"
        ),
    ),
)
DEFAULT_OUT = Path("reports/wrr_1994/wrr_defined_pair_set_audit.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv")
DEFAULT_MD = Path("docs/WRR_DEFINED_PAIR_SET_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_defined_pair_set_audit.manifest.json")

LABEL_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

STATUS_DEFINED = "defined"
STATUS_ORDINARY_NOT_VALID = "ordinary_not_valid"
STATUS_UNDER_MINIMUM = "under_minimum_valid_perturbations"

SUMMARY_FIELDNAMES = [
    "run_label",
    "source_path",
    "pairs",
    "defined",
    "ordinary_not_valid",
    "under_minimum_valid",
    "other_statuses",
    "source_cited_defined_distances",
    "defined_gap_to_source_cited",
    "status",
]

DETAIL_FIELDNAMES = [
    "run_label",
    "group",
    "value",
    "pairs",
    "defined",
    "ordinary_not_valid",
    "under_minimum_valid",
    "other_statuses",
    "source_cited_defined_distances",
    "defined_gap_to_source_cited",
    "read",
]

BREAKDOWN_FIELDS = (
    "candidate_lane",
    "pair_review_status",
    "wnp_disputed_zacut_appellation",
)


@dataclass(frozen=True)
class RunSpec:
    label: str
    path: Path


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    expected_defined = expected_defined_count(read_one_row(args.pair_summary))
    pair_rows = keyed_rows(read_rows(args.pair_table), key="pair_id")
    run_specs = parse_run_specs(args.run)
    summary_rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []
    for run in run_specs:
        corrected_rows = enrich_corrected_rows(read_rows(run.path), pair_rows)
        summary_rows.append(summarize_run(run, corrected_rows, expected_defined))
        detail_rows.extend(breakdown_run(run, corrected_rows, expected_defined))
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_csv(args.out, DETAIL_FIELDNAMES, detail_rows)
    write_markdown(args.markdown_out, summary_rows, detail_rows, args)
    write_manifest(args.manifest_out, args, run_specs, summary_rows, detail_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair-summary", type=Path, default=DEFAULT_PAIR_SUMMARY)
    parser.add_argument("--pair-table", type=Path, default=DEFAULT_PAIR_TABLE)
    parser.add_argument(
        "--run",
        action="append",
        default=[],
        help="Corrected-distance run as label=path. Defaults to current all-lane diagnostics.",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def parse_run_specs(values: list[str]) -> list[RunSpec]:
    if not values:
        return [RunSpec(label, path) for label, path in DEFAULT_RUNS]
    runs = []
    seen = set()
    for value in values:
        if "=" not in value:
            raise ValueError("--run must be formatted as label=path")
        label, path = value.split("=", 1)
        if not LABEL_RE.match(label):
            raise ValueError(f"invalid run label: {label}")
        if label in seen:
            raise ValueError(f"duplicate run label: {label}")
        seen.add(label)
        runs.append(RunSpec(label, Path(path)))
    return runs


def expected_defined_count(pair_summary_row: dict[str, str]) -> int:
    value = pair_summary_row.get("expected_published_pairs", "")
    if value == "":
        raise ValueError("pair summary missing expected_published_pairs")
    return int(value)


def enrich_corrected_rows(
    corrected_rows: list[dict[str, str]],
    pair_rows: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    enriched = []
    for row in corrected_rows:
        pair_id = row.get("pair_id", "")
        if not pair_id:
            raise ValueError("corrected-distance row missing pair_id")
        merged = dict(pair_rows.get(pair_id, {}))
        merged.update(row)
        enriched.append(merged)
    return enriched


def summarize_run(
    run: RunSpec,
    rows: list[dict[str, str]],
    expected_defined: int,
) -> dict[str, object]:
    counts = status_counts(rows)
    defined = counts[STATUS_DEFINED]
    return {
        "run_label": run.label,
        "source_path": str(run.path),
        "pairs": len(rows),
        "defined": defined,
        "ordinary_not_valid": counts[STATUS_ORDINARY_NOT_VALID],
        "under_minimum_valid": counts[STATUS_UNDER_MINIMUM],
        "other_statuses": other_status_count(rows, counts),
        "source_cited_defined_distances": expected_defined,
        "defined_gap_to_source_cited": expected_defined - defined,
        "status": "diagnostic_only_not_wrr_reproduction",
    }


def breakdown_run(
    run: RunSpec,
    rows: list[dict[str, str]],
    expected_defined: int,
) -> list[dict[str, object]]:
    detail_rows = []
    for field in BREAKDOWN_FIELDS:
        values = sorted({row.get(field, "") or "missing" for row in rows})
        for value in values:
            group_rows = [row for row in rows if (row.get(field, "") or "missing") == value]
            counts = status_counts(group_rows)
            defined = counts[STATUS_DEFINED]
            detail_rows.append(
                {
                    "run_label": run.label,
                    "group": field,
                    "value": value,
                    "pairs": len(group_rows),
                    "defined": defined,
                    "ordinary_not_valid": counts[STATUS_ORDINARY_NOT_VALID],
                    "under_minimum_valid": counts[STATUS_UNDER_MINIMUM],
                    "other_statuses": other_status_count(group_rows, counts),
                    "source_cited_defined_distances": expected_defined,
                    "defined_gap_to_source_cited": expected_defined - defined,
                    "read": "diagnostic subgroup only; not a source-locked pair rule",
                }
            )
    return detail_rows


def status_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    return {
        STATUS_DEFINED: sum(1 for row in rows if row.get("corrected_distance_status") == STATUS_DEFINED),
        STATUS_ORDINARY_NOT_VALID: sum(
            1 for row in rows if row.get("corrected_distance_status") == STATUS_ORDINARY_NOT_VALID
        ),
        STATUS_UNDER_MINIMUM: sum(
            1 for row in rows if row.get("corrected_distance_status") == STATUS_UNDER_MINIMUM
        ),
    }


def other_status_count(rows: list[dict[str, str]], counts: dict[str, int]) -> int:
    return len(rows) - sum(counts.values())


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise ValueError(f"{path} must contain exactly one data row; found {len(rows)}")
    return rows[0]


def keyed_rows(rows: list[dict[str, str]], *, key: str) -> dict[str, dict[str, str]]:
    keyed = {}
    for row in rows:
        value = row.get(key, "")
        if not value:
            raise ValueError(f"row missing key field: {key}")
        if value in keyed:
            raise ValueError(f"duplicate {key}: {value}")
        keyed[value] = row
    return keyed


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    detail_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    best = max(summary_rows, key=lambda row: int(row["defined"]))
    expected = int(best["source_cited_defined_distances"])
    best_defined = int(best["defined"])
    lines = [
        "# WRR Defined Pair-Set Audit",
        "",
        "Status: diagnostic-only pair-universe pressure audit, not a WRR reproduction.",
        "",
        "This report joins the current working pair table to existing direct",
        "corrected-distance outputs. It asks which imported same-record pairs",
        "currently produce defined `c(w,w')` values and how far those counts remain",
        "from the source-cited second-list distance count.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_defined_pair_set "
            f"--pair-summary {args.pair_summary} "
            f"--pair-table {args.pair_table} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Run Summary",
        "",
        "| Run | Pairs | Defined | Gap to source-cited count | Ordinary not valid | Under minimum | Other | Status |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| {run_label} | {pairs} | {defined} | {defined_gap_to_source_cited} | "
            "{ordinary_not_valid} | {under_minimum_valid} | {other_statuses} | {status} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Candidate-Lane Breakdown",
            "",
            "| Run | Candidate lane | Pairs | Defined | Ordinary not valid | Under minimum |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows_for_group(detail_rows, "candidate_lane"):
        lines.append(
            "| {run_label} | `{value}` | {pairs} | {defined} | "
            "{ordinary_not_valid} | {under_minimum_valid} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Review-Status Breakdown",
            "",
            "| Run | Review status | Pairs | Defined | Ordinary not valid | Under minimum |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows_for_group(detail_rows, "pair_review_status"):
        lines.append(
            "| {run_label} | `{value}` | {pairs} | {defined} | "
            "{ordinary_not_valid} | {under_minimum_valid} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## WNP Zacut Diagnostic Breakdown",
            "",
            "| Run | WNP Zacut flag | Pairs | Defined | Ordinary not valid | Under minimum |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows_for_group(detail_rows, "wnp_disputed_zacut_appellation"):
        lines.append(
            "| {run_label} | `{value}` | {pairs} | {defined} | "
            "{ordinary_not_valid} | {under_minimum_valid} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            f"- Best current run: `{best['run_label']}` defines {best_defined} of {expected}.",
            f"- Gap to the source-cited count remains {expected - best_defined}.",
            "- The missing mass is ordinary-not-valid, not an under-minimum-valid edge case.",
            "- Candidate-lane and WNP-Zacut rows are diagnostic pressure only; they do",
            "  not establish a source-locked pair rule.",
            "- Claim language stays blocked by `docs/WRR_CLAIM_READINESS.md`.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def rows_for_group(rows: list[dict[str, object]], group: str) -> list[dict[str, object]]:
    return [row for row in rows if row["group"] == group]


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    run_specs: list[RunSpec],
    summary_rows: list[dict[str, object]],
    detail_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_wrr_defined_pair_set",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "pair_summary": str(args.pair_summary),
            "pair_table": str(args.pair_table),
            "runs": {run.label: str(run.path) for run in run_specs},
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
        },
        "summary_rows": len(summary_rows),
        "detail_rows": len(detail_rows),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
