#!/usr/bin/env python3
"""Build a WRR method-status matrix from current audit outputs."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_TEXT_SOURCE = Path("reports/wrr_1994/koren_genesis_text_source.csv")
DEFAULT_PAIR_SUMMARY = Path("reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv")
DEFAULT_TABLE2_BRIDGE_SUMMARY = Path("reports/wrr_1994/wrr_table2_source_bridge_summary.csv")
DEFAULT_SKIP_SUMMARY = Path("reports/wrr_1994/wrr2_skip_caps_summary.csv")
DEFAULT_VARIANTS = Path("reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv")
DEFAULT_PRIMARY_RESULT_TABLE = Path("reports/wrr_1994/wrr_primary_result_table.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_method_status.csv")
DEFAULT_MD = Path("docs/WRR_METHOD_STATUS.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_method_status.manifest.json")

FIELDNAMES = [
    "decision_area",
    "status",
    "current_read",
    "evidence",
    "next_action",
]

SOURCE_ANCHORS = [
    {
        "topic": "WRR printed D(w) formula",
        "source": "WRR 1994 Appendix A.4",
        "read": "Uses a term-specific skip bound chosen so the expected ELS count is 10; printed window count uses (D - 1)(2L - (k - 1)(D + 2)).",
    },
    {
        "topic": "WRR second-list filtered sample",
        "source": "WRR 1994 Appendix A.3",
        "read": "Restricts words to length 5..8 for the corrected-distance calculation and reports 298 word pairs before later defined-distance filtering.",
    },
    {
        "topic": "WRR permutation count",
        "source": "WRR 1994 main text and Appendix A.6",
        "read": "Uses 999,999 random permutations of the 32 personalities for significance calculations.",
    },
    {
        "topic": "Program formula mismatch",
        "source": "MBBK 1999 Appendix A",
        "read": "Reports that WRR programs used (D - 1)(2L - (k - 1)D), not the printed WRR 1994 formula.",
    },
    {
        "topic": "Corrected-distance definedness",
        "source": "MBBK 1999 Appendix A and Gans communities method section",
        "read": (
            "Treats c(w,w') as defined only when the ordinary perturbation is defined and at least 10 "
            "perturbation values are defined; MBBK uses greater-than-or-equal ranking while extracted "
            "WRR 1994 text has strict greater-than wording in one passage."
        ),
    },
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    text_row = read_one_row(args.text_source)
    pair_row = read_one_row(args.pair_summary)
    table2_bridge_row = read_one_row(args.table2_bridge_summary)
    skip_row = read_one_row(args.skip_summary)
    variant_rows = read_rows(args.corrected_distance_variants)
    primary_result_rows = read_rows(args.primary_result_table)
    rows = build_status_rows(
        text_row,
        pair_row,
        skip_row,
        variant_rows,
        primary_result_rows,
        table2_bridge_row,
    )
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text-source", type=Path, default=DEFAULT_TEXT_SOURCE)
    parser.add_argument("--pair-summary", type=Path, default=DEFAULT_PAIR_SUMMARY)
    parser.add_argument("--table2-bridge-summary", type=Path, default=DEFAULT_TABLE2_BRIDGE_SUMMARY)
    parser.add_argument("--skip-summary", type=Path, default=DEFAULT_SKIP_SUMMARY)
    parser.add_argument("--corrected-distance-variants", type=Path, default=DEFAULT_VARIANTS)
    parser.add_argument("--primary-result-table", type=Path, default=DEFAULT_PRIMARY_RESULT_TABLE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise ValueError(f"expected exactly one row in {path}")
    return rows[0]


def build_status_rows(
    text_row: dict[str, str],
    pair_row: dict[str, str],
    skip_row: dict[str, str],
    variant_rows: list[dict[str, str]],
    primary_result_rows: list[dict[str, str]] | None = None,
    table2_bridge_row: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    return [
        {
            "decision_area": "Genesis text stream",
            "status": "locally_locked",
            "current_read": "Koren Genesis stream has stable local fingerprint for smoke work.",
            "evidence": (
                f"{text_row.get('normalized_letters', '')} normalized letters; "
                f"{text_row.get('verse_count', '')} verses; normalized SHA-256 "
                f"{text_row.get('normalized_text_sha256', '')}"
            ),
            "next_action": "Cross-check against primary WRR text-source statement before claiming reproduction.",
        },
        {
            "decision_area": "WRR2 term source",
            "status": "secondary_source_imported",
            "current_read": "ANU/McKay WRR2 plain text is imported for audit, not treated as primary-paper ground truth.",
            "evidence": (
                table2_bridge_evidence(table2_bridge_row)
                + "; "
                f"{pair_row.get('source_records', '')} source records; "
                f"{pair_row.get('source_appellations', '')} appellations; "
                f"{pair_row.get('source_dates', '')} date rows; "
                f"{pair_row.get('source_undated_records', '')} undated records skipped"
            ),
            "next_action": "Cross-check imported spellings and dates against primary paper table or citable transcription.",
        },
        {
            "decision_area": "Pair universe",
            "status": "open",
            "current_read": "The 163 count is best treated as defined-distance output, not raw pair count.",
            "evidence": (
                f"{pair_row.get('source_same_record_pairs', '')} raw same-record pairs; "
                f"{pair_row.get('appellation_min_length_same_record_pairs', '')} after appellation length >= "
                f"{pair_row.get('appellation_min_length', '')}; "
                f"{pair_row.get('length_filtered_same_record_pairs', '')} in current length "
                f"{pair_row.get('length_filter_min', '')}..{pair_row.get('length_filter_max', '')} smoke lane; "
                f"{pair_row.get('expected_published_pairs', '')} cited second-list distances; "
                "298 paper-stated candidate word pairs"
            ),
            "next_action": "Derive final pair set from source-backed corrected-distance eligibility, not raw counts alone.",
        },
        {
            "decision_area": "D(w) skip-cap formula",
            "status": "open",
            "current_read": "Printed and reported-program formulas are both implemented; final choice remains source decision.",
            "evidence": (
                f"{skip_row.get('rows', '')} length-filtered rows; "
                f"{skip_row.get('program_cap_lt_printed', '')} program caps below printed; "
                f"{skip_row.get('program_cap_eq_printed', '')} equal caps; "
                f"{skip_row.get('target_unreached_rows', '')} rows do not reach target expected hits"
            ),
            "next_action": "Choose printed-paper formula or reported-program formula before final corrected-distance run.",
        },
        corrected_distance_status(variant_rows),
        aggregate_status(primary_result_rows or []),
    ]


def corrected_distance_status(variant_rows: list[dict[str, str]]) -> dict[str, str]:
    if not variant_rows:
        return {
            "decision_area": "Corrected distance c(w,w')",
            "status": "missing",
            "current_read": "No corrected-distance variant rows supplied.",
            "evidence": "",
            "next_action": "Run corrected-distance smoke before method review.",
        }
    defined_counts = [int_value(row.get("defined_corrected_distances", "")) for row in variant_rows]
    max_valid = max(int_value(row.get("max_pair_valid_perturbations", "")) for row in variant_rows)
    variants = ", ".join(
        f"{row.get('variant', '')}: {row.get('defined_corrected_distances', '')} defined"
        for row in variant_rows
    )
    return {
        "decision_area": "Corrected distance c(w,w')",
        "status": "smoke_only",
        "current_read": "Smoke driver exists, but current candidate lane produces no defined corrected distances.",
        "evidence": f"{variants}; maximum valid perturbation count {max_valid}; total defined {sum(defined_counts)}",
        "next_action": "Optimize and rerun over final pair universe after D(w) and source rows are locked.",
    }


def aggregate_status(primary_result_rows: list[dict[str, str]]) -> dict[str, str]:
    genesis = next(
        (row for row in primary_result_rows if row.get("label") == "G" and row.get("status") == "found"),
        None,
    )
    if genesis is None:
        return {
            "decision_area": "Aggregate statistic and permutation",
            "status": "not_built",
            "current_read": "P1/P2 arithmetic helpers exist, but no claim-grade P1..P4 or date-permutation runner exists.",
            "evidence": "No primary Table 3 source-result row was supplied; no current protocol step computes full WRR aggregate scores or permutation ranks from defined c-values.",
            "next_action": "Implement only after final pair universe and corrected-distance values are locked.",
        }
    control_summary = ", ".join(
        f"{row.get('label', '')} p0={row.get('bonferroni_p0', '')}"
        for row in primary_result_rows
        if row.get("label") != "G" and row.get("status") == "found"
    )
    return {
        "decision_area": "Aggregate statistic and permutation",
        "status": "source_locked_not_built",
        "current_read": "Published Table 3 ranks are source-audited, but local claim-grade P1..P4 and date-permutation runners are not built.",
        "evidence": (
            f"Source Table 3: G min {genesis.get('min_statistic', '')} rank "
            f"{genesis.get('min_rank', '')}, p0={genesis.get('bonferroni_p0', '')}; "
            f"controls: {control_summary}; no local aggregate recomputation from defined c-values"
        ),
        "next_action": "Implement only after final pair universe and corrected-distance values are locked.",
    }


def int_value(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    lines = [
        "# WRR Method Status",
        "",
        "Status: current audit matrix; not a WRR reproduction.",
        "",
        "This file summarizes what the current local WRR work has locked and what",
        "still needs source or implementation work before any reproduction claim.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_method_status "
            f"--text-source {args.text_source} "
            f"--pair-summary {args.pair_summary} "
            f"--table2-bridge-summary {args.table2_bridge_summary} "
            f"--skip-summary {args.skip_summary} "
            f"--corrected-distance-variants {args.corrected_distance_variants} "
            f"--primary-result-table {args.primary_result_table} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Matrix",
        "",
        "| Area | Status | Current read | Evidence | Next action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["decision_area"]),
                    f"`{markdown_cell(row['status'])}`",
                    markdown_cell(row["current_read"]),
                    markdown_cell(row["evidence"]),
                    markdown_cell(row["next_action"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Source Anchors",
            "",
            "| Topic | Source | Current read |",
            "| --- | --- | --- |",
        ]
    )
    for row in SOURCE_ANCHORS:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["topic"]),
                    markdown_cell(row["source"]),
                    markdown_cell(row["read"]),
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def table2_bridge_evidence(row: dict[str, str] | None) -> str:
    if not row:
        return "primary Table 2 bridge not supplied"
    return (
        f"{row.get('primary_rows_found', '')}/{row.get('primary_rows', '')} primary Table 2 "
        f"English row labels found; {row.get('secondary_records', '')} secondary records; "
        f"{row.get('primary_hebrew_cells_verified', '')} primary Hebrew cells verified"
    )


def write_manifest(args: argparse.Namespace, rows: list[dict[str, str]], started: float) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "text_source": str(args.text_source),
            "pair_summary": str(args.pair_summary),
            "table2_bridge_summary": str(args.table2_bridge_summary),
            "skip_summary": str(args.skip_summary),
            "corrected_distance_variants": str(args.corrected_distance_variants),
            "primary_result_table": str(args.primary_result_table),
        },
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
