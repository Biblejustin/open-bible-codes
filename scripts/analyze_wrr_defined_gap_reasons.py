#!/usr/bin/env python3
"""Classify why current WRR pairs fail to define corrected distances."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_PAIR_SUMMARY = Path("reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv")
DEFAULT_PAIR_TABLE = Path("reports/wrr_1994/wrr2_pair_eligibility_table.csv")
DEFAULT_ROW_OCR = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv")
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
DEFAULT_OUT = Path("reports/wrr_1994/wrr_defined_gap_reasons.csv")
DEFAULT_TERM_OUT = Path("reports/wrr_1994/wrr_defined_gap_term_burden.csv")
DEFAULT_MD = Path("docs/WRR_DEFINED_GAP_REASON_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_defined_gap_reason_audit.manifest.json")

LABEL_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

STATUS_DEFINED = "defined"
STATUS_ORDINARY_NOT_VALID = "ordinary_not_valid"
STATUS_UNDER_MINIMUM = "under_minimum_valid_perturbations"

REASON_DEFINED = "defined"
REASON_UNDER_MINIMUM = "under_minimum_valid_perturbations"
REASON_ORDINARY_NO_APPELLATION = "ordinary_missing_appellation_hits"
REASON_ORDINARY_NO_DATE = "ordinary_missing_date_hits"
REASON_ORDINARY_NO_BOTH = "ordinary_missing_both_terms"
REASON_ORDINARY_NO_SHARED_DEFINED = "ordinary_hits_present_no_shared_defined_triple"
REASON_ORDINARY_TRIPLE_ONLY = "ordinary_triple_missing_but_other_perturbations_shared"
REASON_OTHER = "other_status"

REASON_READS = {
    REASON_DEFINED: "corrected distance currently defined",
    REASON_UNDER_MINIMUM: "ordinary pair exists but fewer than minimum valid perturbations",
    REASON_ORDINARY_NO_APPELLATION: "ordinary pair blocked because appellation has zero ordinary hits in this run",
    REASON_ORDINARY_NO_DATE: "ordinary pair blocked because date has zero ordinary hits in this run",
    REASON_ORDINARY_NO_BOTH: "ordinary pair blocked because both terms have zero ordinary hits in this run",
    REASON_ORDINARY_NO_SHARED_DEFINED: "ordinary hits exist, but no shared defined perturbation triple is present",
    REASON_ORDINARY_TRIPLE_ONLY: "non-ordinary perturbations overlap, but ordinary triple is not valid",
    REASON_OTHER: "status outside current classifier",
}

SUMMARY_FIELDNAMES = [
    "run_label",
    "source_path",
    "reason",
    "pairs",
    "source_cited_defined_distances",
    "run_defined",
    "run_gap_to_source_cited",
    "read",
]

TERM_FIELDNAMES = [
    "run_label",
    "term_side",
    "term_id",
    "term",
    "normalized",
    "ordinary_hits",
    "defined_perturbed_rows",
    "triples_with_defined_rows",
    "ordinary_not_valid_pairs",
    "concepts",
    "candidate_lanes",
    "pair_ids",
    "row_ocr_status",
    "row_ocr_column",
    "row_ocr_match_basis",
    "reasons",
]


@dataclass(frozen=True)
class RunSpec:
    label: str
    path: Path


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    expected_defined = expected_defined_count(read_one_row(args.pair_summary))
    pair_rows = keyed_rows(read_rows(args.pair_table), key="pair_id")
    row_ocr_rows = keyed_rows(read_rows(args.row_ocr), key="term_id") if args.row_ocr.exists() else {}
    run_specs = parse_run_specs(args.run)
    summary_rows: list[dict[str, object]] = []
    term_rows: list[dict[str, object]] = []
    for run in run_specs:
        rows = enrich_corrected_rows(read_rows(run.path), pair_rows)
        summary_rows.extend(summarize_run(run, rows, expected_defined))
        term_rows.extend(term_burden_rows(run, rows, row_ocr_rows))
    write_csv(args.out, SUMMARY_FIELDNAMES, summary_rows)
    write_csv(args.term_out, TERM_FIELDNAMES, term_rows)
    write_markdown(args.markdown_out, summary_rows, term_rows, args)
    write_manifest(args.manifest_out, args, run_specs, summary_rows, term_rows, started)
    print(args.out)
    print(args.term_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair-summary", type=Path, default=DEFAULT_PAIR_SUMMARY)
    parser.add_argument("--pair-table", type=Path, default=DEFAULT_PAIR_TABLE)
    parser.add_argument("--row-ocr", type=Path, default=DEFAULT_ROW_OCR)
    parser.add_argument(
        "--run",
        action="append",
        default=[],
        help="Corrected-distance run as label=path. Defaults to current all-lane diagnostics.",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--term-out", type=Path, default=DEFAULT_TERM_OUT)
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
) -> list[dict[str, object]]:
    reasons = Counter(reason_for_row(row) for row in rows)
    run_defined = reasons[REASON_DEFINED]
    return [
        {
            "run_label": run.label,
            "source_path": str(run.path),
            "reason": reason,
            "pairs": reasons[reason],
            "source_cited_defined_distances": expected_defined,
            "run_defined": run_defined,
            "run_gap_to_source_cited": expected_defined - run_defined,
            "read": REASON_READS.get(reason, REASON_READS[REASON_OTHER]),
        }
        for reason in sorted(reasons, key=reason_sort_key)
    ]


def reason_sort_key(reason: str) -> tuple[int, str]:
    order = {
        REASON_DEFINED: 0,
        REASON_ORDINARY_NO_APPELLATION: 1,
        REASON_ORDINARY_NO_DATE: 2,
        REASON_ORDINARY_NO_BOTH: 3,
        REASON_UNDER_MINIMUM: 4,
        REASON_ORDINARY_NO_SHARED_DEFINED: 5,
        REASON_ORDINARY_TRIPLE_ONLY: 6,
        REASON_OTHER: 7,
    }
    return (order.get(reason, 99), reason)


def reason_for_row(row: dict[str, str]) -> str:
    status = row.get("corrected_distance_status", "")
    if status == STATUS_DEFINED:
        return REASON_DEFINED
    if status == STATUS_UNDER_MINIMUM:
        return REASON_UNDER_MINIMUM
    if status != STATUS_ORDINARY_NOT_VALID:
        return REASON_OTHER
    app_hits = int_value(row.get("appellation_ordinary_hits", ""))
    date_hits = int_value(row.get("date_ordinary_hits", ""))
    valid_perturbations = int_value(row.get("pair_valid_perturbations", ""))
    if app_hits == 0 and date_hits == 0:
        return REASON_ORDINARY_NO_BOTH
    if app_hits == 0:
        return REASON_ORDINARY_NO_APPELLATION
    if date_hits == 0:
        return REASON_ORDINARY_NO_DATE
    if valid_perturbations == 0:
        return REASON_ORDINARY_NO_SHARED_DEFINED
    return REASON_ORDINARY_TRIPLE_ONLY


def term_burden_rows(
    run: RunSpec,
    rows: list[dict[str, str]],
    row_ocr_rows: dict[str, dict[str, str]] | None = None,
) -> list[dict[str, object]]:
    buckets: dict[tuple[str, str], dict[str, object]] = {}
    reasons: dict[tuple[str, str], set[str]] = defaultdict(set)
    contexts: dict[tuple[str, str], dict[str, set[str]]] = defaultdict(
        lambda: {"concepts": set(), "candidate_lanes": set(), "pair_ids": set()}
    )
    counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        reason = reason_for_row(row)
        if row.get("corrected_distance_status") != STATUS_ORDINARY_NOT_VALID:
            continue
        for side in contributing_sides(row, reason):
            key = (side, row[f"{side}_term_id"])
            counts[key] += 1
            reasons[key].add(reason)
            contexts[key]["concepts"].add(row.get("concept", ""))
            contexts[key]["candidate_lanes"].add(row.get("candidate_lane", ""))
            contexts[key]["pair_ids"].add(row.get("pair_id", ""))
            buckets[key] = {
                "run_label": run.label,
                "term_side": side,
                "term_id": row.get(f"{side}_term_id", ""),
                "term": row.get(f"{side}_term", ""),
                "normalized": row.get(f"{side}_normalized", ""),
                "ordinary_hits": row.get(f"{side}_ordinary_hits", ""),
                "defined_perturbed_rows": row.get(f"{side}_defined_perturbed_rows", ""),
                "triples_with_defined_rows": row.get(f"{side}_triples_with_defined_rows", ""),
            }
    out = []
    for key, count in counts.items():
        row = dict(buckets[key])
        ocr_row = (row_ocr_rows or {}).get(str(row["term_id"]), {})
        row["ordinary_not_valid_pairs"] = count
        row["concepts"] = joined_context(contexts[key]["concepts"])
        row["candidate_lanes"] = joined_context(contexts[key]["candidate_lanes"])
        row["pair_ids"] = joined_context(contexts[key]["pair_ids"])
        row["row_ocr_status"] = ocr_row.get("row_ocr_status", "")
        row["row_ocr_column"] = ocr_row.get("column", "")
        row["row_ocr_match_basis"] = ocr_row.get("match_basis", "")
        row["reasons"] = ";".join(sorted(reasons[key], key=reason_sort_key))
        out.append(row)
    return sorted(
        out,
        key=lambda row: (
            str(row["run_label"]),
            -int(row["ordinary_not_valid_pairs"]),
            str(row["term_side"]),
            str(row["term_id"]),
        ),
    )


def contributing_sides(row: dict[str, str], reason: str) -> tuple[str, ...]:
    if reason == REASON_ORDINARY_NO_APPELLATION:
        return ("appellation",)
    if reason == REASON_ORDINARY_NO_DATE:
        return ("date",)
    if reason == REASON_ORDINARY_NO_BOTH:
        return ("appellation", "date")
    if reason in (REASON_ORDINARY_NO_SHARED_DEFINED, REASON_ORDINARY_TRIPLE_ONLY):
        return ("appellation", "date")
    return ()


def joined_context(values: set[str]) -> str:
    return ";".join(sorted(value for value in values if value))


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    term_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    best = best_run(summary_rows)
    lines = [
        "# WRR Defined Gap Reason Audit",
        "",
        "Status: diagnostic-only failure taxonomy for the current WRR all-lane",
        "corrected-distance outputs. It is not a WRR reproduction.",
        "",
        "This report classifies why current rows fail the `c(w,w')` definedness",
        "gate. It uses existing corrected-distance outputs and does not run a",
        "new ELS search.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_defined_gap_reasons "
            f"--pair-summary {args.pair_summary} "
            f"--pair-table {args.pair_table} "
            f"--row-ocr {args.row_ocr} "
            f"--out {args.out} "
            f"--term-out {args.term_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Reason Counts",
        "",
        "| Run | Reason | Pairs | Run defined | Gap to source-cited count | Read |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| {run_label} | `{reason}` | {pairs} | {run_defined} | "
            "{run_gap_to_source_cited} | {read} |".format(**row)
        )
    if best:
        best_label = str(best["run_label"])
        best_terms = [row for row in term_rows if row["run_label"] == best_label][:12]
        lines.extend(
            [
                "",
                "## Best Current Run",
                "",
                (
                    f"- `{best_label}` defines {best['run_defined']} of "
                    f"{best['source_cited_defined_distances']} source-cited distances."
                ),
                f"- Gap to the source-cited count remains {best['run_gap_to_source_cited']}.",
                best_read(summary_rows, best_label),
                row_ocr_burden_read(term_rows, best_label),
                "",
                "## Top Ordinary-Missing Terms In Best Run",
                "",
                "| Side | Term id | Concepts | Term | Row OCR | Ordinary hits | Defined rows | Pairs blocked | Reasons |",
                "| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for row in best_terms:
            lines.append(
                "| {term_side} | `{term_id}` | `{concepts}` | `{term}` | `{row_ocr_status}` | "
                "{ordinary_hits} | {defined_perturbed_rows} | "
                "{ordinary_not_valid_pairs} | `{reasons}` |".format(**row)
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- A row can only define corrected distance when the ordinary pair is valid",
            "  and the minimum perturbation count is met.",
            "- Zero ordinary hits for an imported appellation or date term is a source",
            "  alignment problem before it is a permutation problem.",
            "- Row OCR status is inherited from the existing Table 2 row-aligned",
            "  OCR probe; it is triage evidence, not verified primary transcription.",
            "- This audit narrows the next WRR work toward term normalization, source",
            "  row boundaries, and the final pair-universe rule.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def best_run(summary_rows: list[dict[str, object]]) -> dict[str, object] | None:
    defined_rows = [row for row in summary_rows if row["reason"] == REASON_DEFINED]
    return max(defined_rows, key=lambda row: int(row["run_defined"]), default=None)


def best_read(summary_rows: list[dict[str, object]], run_label: str) -> str:
    by_reason = {
        str(row["reason"]): int(row["pairs"])
        for row in summary_rows
        if row["run_label"] == run_label
    }
    ordinary_missing = sum(
        by_reason.get(reason, 0)
        for reason in (
            REASON_ORDINARY_NO_APPELLATION,
            REASON_ORDINARY_NO_DATE,
            REASON_ORDINARY_NO_BOTH,
        )
    )
    under_minimum = by_reason.get(REASON_UNDER_MINIMUM, 0)
    return (
        f"- Ordinary-missing rows total {ordinary_missing}; under-minimum rows total "
        f"{under_minimum}."
    )


def row_ocr_burden_read(term_rows: list[dict[str, object]], run_label: str) -> str:
    rows = [row for row in term_rows if row["run_label"] == run_label]
    if not rows:
        return "- Row-OCR burden summary unavailable."
    unweighted: Counter[str] = Counter(str(row.get("row_ocr_status", "") or "missing") for row in rows)
    weighted: Counter[str] = Counter()
    for row in rows:
        weighted[str(row.get("row_ocr_status", "") or "missing")] += int(
            row["ordinary_not_valid_pairs"]
        )
    return (
        "- Row-OCR term burden: "
        f"{format_counter(unweighted)} contributing terms; "
        f"{format_counter(weighted)} blocked-pair contributions."
    )


def format_counter(counter: Counter[str]) -> str:
    return ", ".join(f"{counter[key]} {key}" for key in sorted(counter))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise ValueError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def keyed_rows(rows: list[dict[str, str]], *, key: str) -> dict[str, dict[str, str]]:
    out = {}
    for row in rows:
        value = row.get(key, "")
        if not value:
            raise ValueError(f"row missing {key}")
        if value in out:
            raise ValueError(f"duplicate {key}: {value}")
        out[value] = row
    return out


def int_value(value: str) -> int:
    if value in ("", None):
        return 0
    return int(float(value))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    runs: list[RunSpec],
    summary_rows: list[dict[str, object]],
    term_rows: list[dict[str, object]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "tool": "analyze_wrr_defined_gap_reasons",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "pair_summary": str(args.pair_summary),
            "pair_table": str(args.pair_table),
            "row_ocr": str(args.row_ocr),
            "runs": {run.label: str(run.path) for run in runs},
        },
        "outputs": {
            "out": str(args.out),
            "term_out": str(args.term_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
        "summary_rows": len(summary_rows),
        "term_rows": len(term_rows),
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
