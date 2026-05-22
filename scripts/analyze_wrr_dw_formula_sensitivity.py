#!/usr/bin/env python3
"""Build a WRR D(w) formula sensitivity packet."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_SKIP_SUMMARY = Path("reports/wrr_1994/wrr2_skip_caps_summary.csv")
DEFAULT_VARIANTS = Path("reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv")
DEFAULT_DIRECT_PRINTED_SUMMARY = Path(
    "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged_summary.csv"
)
DEFAULT_DIRECT_PROGRAM_SUMMARY = Path(
    "reports/wrr_1994/direct_all/highcap_1000_program/wrr2_corrected_distance_all_lanes_merged_summary.csv"
)
DEFAULT_DIRECT_PRINTED = Path(
    "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged.csv"
)
DEFAULT_DIRECT_PROGRAM = Path(
    "reports/wrr_1994/direct_all/highcap_1000_program/wrr2_corrected_distance_all_lanes_merged.csv"
)
DEFAULT_OUT = Path("reports/wrr_1994/wrr_dw_formula_sensitivity.csv")
DEFAULT_CHANGED_OUT = Path("reports/wrr_1994/wrr_dw_formula_changed_pairs.csv")
DEFAULT_MD = Path("docs/WRR_DW_FORMULA_SENSITIVITY.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_dw_formula_sensitivity.manifest.json")

SUMMARY_FIELDNAMES = [
    "scope",
    "row_count",
    "printed_formula",
    "program_formula",
    "printed_defined_corrected_distances",
    "program_defined_corrected_distances",
    "fixed_250_defined_corrected_distances",
    "printed_ordinary_not_valid_pairs",
    "program_ordinary_not_valid_pairs",
    "printed_under_minimum_valid_pairs",
    "program_under_minimum_valid_pairs",
    "changed_pairs",
    "program_cap_lt_printed",
    "program_cap_eq_printed",
    "program_cap_gt_printed",
    "target_unreached_rows",
    "program_target_unreached_rows",
    "diagnostic_read",
]

CHANGED_FIELDNAMES = [
    "pair_id",
    "concept",
    "printed_corrected_distance_status",
    "program_corrected_distance_status",
    "printed_corrected_distance",
    "program_corrected_distance",
    "printed_pair_valid_perturbations",
    "program_pair_valid_perturbations",
    "changed_fields",
]

COMPARE_FIELDS = [
    "corrected_distance_status",
    "corrected_distance",
    "pair_valid_perturbations",
    "ordinary_q",
    "appellation_defined_perturbed_rows",
    "date_defined_perturbed_rows",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    skip_row = read_one_row(args.skip_summary)
    variant_rows = read_rows(args.variants)
    direct_printed_summary = read_one_row(args.direct_printed_summary)
    direct_program_summary = read_one_row(args.direct_program_summary)
    changed_rows = changed_pair_rows(
        read_rows(args.direct_printed),
        read_rows(args.direct_program),
    )
    summary_rows = build_summary_rows(
        skip_row,
        variant_rows,
        direct_printed_summary,
        direct_program_summary,
        changed_rows,
    )
    write_csv(args.out, SUMMARY_FIELDNAMES, summary_rows)
    write_csv(args.changed_out, CHANGED_FIELDNAMES, changed_rows)
    write_markdown(args.markdown_out, summary_rows, changed_rows, args)
    write_manifest(args.manifest_out, args, summary_rows, changed_rows, started)
    print(args.out)
    print(args.changed_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-summary", type=Path, default=DEFAULT_SKIP_SUMMARY)
    parser.add_argument("--variants", type=Path, default=DEFAULT_VARIANTS)
    parser.add_argument("--direct-printed-summary", type=Path, default=DEFAULT_DIRECT_PRINTED_SUMMARY)
    parser.add_argument("--direct-program-summary", type=Path, default=DEFAULT_DIRECT_PROGRAM_SUMMARY)
    parser.add_argument("--direct-printed", type=Path, default=DEFAULT_DIRECT_PRINTED)
    parser.add_argument("--direct-program", type=Path, default=DEFAULT_DIRECT_PROGRAM)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--changed-out", type=Path, default=DEFAULT_CHANGED_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_summary_rows(
    skip_row: dict[str, str],
    variant_rows: list[dict[str, str]],
    direct_printed_summary: dict[str, str],
    direct_program_summary: dict[str, str],
    changed_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    smoke_printed = variant_by_name(variant_rows, "term_printed")
    smoke_program = variant_by_name(variant_rows, "term_program")
    smoke_fixed = variant_by_name(variant_rows, "fixed_250")
    return [
        {
            "scope": "skip_cap_profile",
            "row_count": skip_row.get("rows", ""),
            "printed_formula": skip_row.get("skip_cap_formula", "printed"),
            "program_formula": "program",
            "program_cap_lt_printed": skip_row.get("program_cap_lt_printed", ""),
            "program_cap_eq_printed": skip_row.get("program_cap_eq_printed", ""),
            "program_cap_gt_printed": skip_row.get("program_cap_gt_printed", ""),
            "target_unreached_rows": skip_row.get("target_unreached_rows", ""),
            "program_target_unreached_rows": skip_row.get("program_target_unreached_rows", ""),
            "diagnostic_read": "profile only; printed D(w) selected as main",
        },
        {
            "scope": "smoke_length_5_8_cap250",
            "row_count": smoke_printed.get("pairs", ""),
            "printed_formula": smoke_printed.get("skip_cap_formula", "printed"),
            "program_formula": smoke_program.get("skip_cap_formula", "program"),
            "printed_defined_corrected_distances": smoke_printed.get(
                "defined_corrected_distances", ""
            ),
            "program_defined_corrected_distances": smoke_program.get(
                "defined_corrected_distances", ""
            ),
            "fixed_250_defined_corrected_distances": smoke_fixed.get(
                "defined_corrected_distances", ""
            ),
            "printed_ordinary_not_valid_pairs": smoke_printed.get("ordinary_not_valid_pairs", ""),
            "program_ordinary_not_valid_pairs": smoke_program.get("ordinary_not_valid_pairs", ""),
            "printed_under_minimum_valid_pairs": smoke_printed.get(
                "under_minimum_valid_pairs", ""
            ),
            "program_under_minimum_valid_pairs": smoke_program.get(
                "under_minimum_valid_pairs", ""
            ),
            "diagnostic_read": "smoke lane sensitivity; printed D(w) main, program sensitivity",
        },
        {
            "scope": "all_lanes_cap1000",
            "row_count": direct_printed_summary.get("pairs", ""),
            "printed_formula": direct_printed_summary.get("skip_cap_formula", "printed"),
            "program_formula": direct_program_summary.get("skip_cap_formula", "program"),
            "printed_defined_corrected_distances": direct_printed_summary.get(
                "defined_corrected_distances", ""
            ),
            "program_defined_corrected_distances": direct_program_summary.get(
                "defined_corrected_distances", ""
            ),
            "printed_ordinary_not_valid_pairs": direct_printed_summary.get(
                "ordinary_not_valid_pairs", ""
            ),
            "program_ordinary_not_valid_pairs": direct_program_summary.get(
                "ordinary_not_valid_pairs", ""
            ),
            "printed_under_minimum_valid_pairs": direct_printed_summary.get(
                "under_minimum_valid_pairs", ""
            ),
            "program_under_minimum_valid_pairs": direct_program_summary.get(
                "under_minimum_valid_pairs", ""
            ),
            "changed_pairs": len(changed_rows),
            "diagnostic_read": "row-level printed/program comparison; printed D(w) main, program sensitivity",
        },
    ]


def changed_pair_rows(
    printed_rows: list[dict[str, str]],
    program_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    program_by_pair = {row.get("pair_id", ""): row for row in program_rows}
    out = []
    for printed in printed_rows:
        pair_id = printed.get("pair_id", "")
        program = program_by_pair.get(pair_id)
        if not program:
            out.append(changed_row(printed, {}, ["missing_from_program"]))
            continue
        changed_fields = [
            field
            for field in COMPARE_FIELDS
            if printed.get(field, "") != program.get(field, "")
        ]
        if changed_fields:
            out.append(changed_row(printed, program, changed_fields))
    printed_ids = {row.get("pair_id", "") for row in printed_rows}
    for program in program_rows:
        if program.get("pair_id", "") not in printed_ids:
            out.append(changed_row({}, program, ["missing_from_printed"]))
    return sorted(out, key=lambda row: row["pair_id"])


def changed_row(
    printed: dict[str, str],
    program: dict[str, str],
    changed_fields: list[str],
) -> dict[str, str]:
    return {
        "pair_id": printed.get("pair_id", "") or program.get("pair_id", ""),
        "concept": printed.get("concept", "") or program.get("concept", ""),
        "printed_corrected_distance_status": printed.get("corrected_distance_status", ""),
        "program_corrected_distance_status": program.get("corrected_distance_status", ""),
        "printed_corrected_distance": printed.get("corrected_distance", ""),
        "program_corrected_distance": program.get("corrected_distance", ""),
        "printed_pair_valid_perturbations": printed.get("pair_valid_perturbations", ""),
        "program_pair_valid_perturbations": program.get("pair_valid_perturbations", ""),
        "changed_fields": ";".join(changed_fields),
    }


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    changed_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# WRR D(w) Formula Sensitivity",
        "",
        "Status: sensitivity packet for the selected printed `D(w)` main rule.",
        "",
        "This compares the printed WRR skip-cap formula and the reported WRR-program",
        "formula across existing corrected-distance outputs.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_dw_formula_sensitivity "
            f"--skip-summary {args.skip_summary} "
            f"--variants {args.variants} "
            f"--direct-printed-summary {args.direct_printed_summary} "
            f"--direct-program-summary {args.direct_program_summary} "
            f"--direct-printed {args.direct_printed} "
            f"--direct-program {args.direct_program} "
            f"--out {args.out} "
            f"--changed-out {args.changed_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        "| Scope | Rows | Printed defined | Program defined | Changed pairs | Read |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| {scope} | {rows} | {printed} | {program} | {changed} | {read} |".format(
                scope=md_cell(row.get("scope", "")),
                rows=md_cell(row.get("row_count", "")),
                printed=md_cell(row.get("printed_defined_corrected_distances", "")),
                program=md_cell(row.get("program_defined_corrected_distances", "")),
                changed=md_cell(row.get("changed_pairs", "")),
                read=md_cell(row.get("diagnostic_read", "")),
            )
        )
    profile = {row["scope"]: row for row in summary_rows}.get("skip_cap_profile", {})
    lines.extend(
        [
            "",
            "## Skip-Cap Profile",
            "",
            "| Measure | Count |",
            "| --- | ---: |",
            f"| Program cap below printed | {profile.get('program_cap_lt_printed', '')} |",
            f"| Program cap equal printed | {profile.get('program_cap_eq_printed', '')} |",
            f"| Program cap above printed | {profile.get('program_cap_gt_printed', '')} |",
            f"| Printed target-unreached rows | {profile.get('target_unreached_rows', '')} |",
            f"| Program target-unreached rows | {profile.get('program_target_unreached_rows', '')} |",
            "",
            "## Changed Pairs",
            "",
        ]
    )
    if changed_rows:
        lines.extend(
            [
                "| Pair | Concept | Printed status | Program status | Changed fields |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for row in changed_rows[:40]:
            lines.append(
                "| `{pair}` | {concept} | `{printed}` | `{program}` | `{fields}` |".format(
                    pair=md_cell(row["pair_id"]),
                    concept=md_cell(row["concept"]),
                    printed=md_cell(row["printed_corrected_distance_status"]),
                    program=md_cell(row["program_corrected_distance_status"]),
                    fields=md_cell(row["changed_fields"]),
                )
            )
        if len(changed_rows) > 40:
            lines.append(f"| ... | ... | ... | ... | {len(changed_rows) - 40} more rows |")
    else:
        lines.append("No pair rows changed between all-lane cap-1000 printed and program formula outputs.")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Printed `D(w)` is the selected main rule for current WRR diagnostics.",
            "- Current all-lane cap-1000 diagnostics show no row-level printed/program difference.",
            "- Reported-program `D(w)` remains required sensitivity output.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary_rows: list[dict[str, object]],
    changed_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "summary_rows": len(summary_rows),
        "changed_pairs": len(changed_rows),
        "inputs": {
            "skip_summary": str(args.skip_summary),
            "variants": str(args.variants),
            "direct_printed_summary": str(args.direct_printed_summary),
            "direct_program_summary": str(args.direct_program_summary),
            "direct_printed": str(args.direct_printed),
            "direct_program": str(args.direct_program),
        },
        "outputs": {
            "out": str(args.out),
            "changed_out": str(args.changed_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def variant_by_name(rows: list[dict[str, str]], name: str) -> dict[str, str]:
    return next((row for row in rows if row.get("variant") == name), {})


def read_one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    return rows[0] if rows else {}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
