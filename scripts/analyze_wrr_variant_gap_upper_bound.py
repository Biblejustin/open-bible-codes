#!/usr/bin/env python3
"""Bound how much simple WRR variant leads could close the defined-distance gap."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_DEFINED_PAIR_SUMMARY = Path("reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv")
DEFAULT_VARIANT_GAP_SUMMARY = Path("reports/wrr_1994/wrr_variant_gap_impact_summary.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_variant_gap_upper_bound.csv")
DEFAULT_MD = Path("docs/WRR_VARIANT_GAP_UPPER_BOUND.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_variant_gap_upper_bound.manifest.json")

ALL_VARIANT = "all_blocking_terms_have_variant_hit"
SOME_VARIANT = "some_blocking_terms_have_variant_hit"
NO_VARIANT = "no_blocking_term_variant_hit"


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    defined_rows = read_rows(args.defined_pair_summary)
    variant_rows = read_rows(args.variant_gap_summary)
    rows = build_rows(defined_rows, variant_rows)
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args.manifest_out, args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--defined-pair-summary", type=Path, default=DEFAULT_DEFINED_PAIR_SUMMARY)
    parser.add_argument("--variant-gap-summary", type=Path, default=DEFAULT_VARIANT_GAP_SUMMARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_rows(
    defined_rows: list[dict[str, str]],
    variant_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    variant_by_run: dict[str, dict[str, dict[str, str]]] = {}
    for row in variant_rows:
        variant_by_run.setdefault(row["run_label"], {})[row["impact_status"]] = row

    out: list[dict[str, str]] = []
    for row in defined_rows:
        run_label = row["run_label"]
        statuses = variant_by_run.get(run_label, {})
        all_variant = int(statuses.get(ALL_VARIANT, {}).get("pairs", "0") or 0)
        some_variant = int(statuses.get(SOME_VARIANT, {}).get("pairs", "0") or 0)
        no_variant = int(statuses.get(NO_VARIANT, {}).get("pairs", "0") or 0)
        defined = int(row["defined"])
        expected = int(row["source_cited_defined_distances"])
        gap = int(row["defined_gap_to_source_cited"])
        upper_defined = defined + all_variant
        residual_gap = max(0, expected - upper_defined)
        out.append(
            {
                "run_label": run_label,
                "source_cited_defined_distances": str(expected),
                "current_defined_distances": str(defined),
                "current_gap_to_source_cited": str(gap),
                "blocked_pairs_all_terms_with_simple_variant": str(all_variant),
                "blocked_pairs_some_terms_with_simple_variant": str(some_variant),
                "blocked_pairs_no_terms_with_simple_variant": str(no_variant),
                "max_additional_distances_if_all_simple_variant_leads_were_valid": str(all_variant),
                "upper_bound_defined_distances": str(upper_defined),
                "residual_gap_after_simple_variant_upper_bound": str(residual_gap),
                "gap_coverage_percent": format_percent(all_variant, gap),
                "status": "diagnostic_upper_bound_not_source_correction",
                "read": read_label(residual_gap, all_variant),
            }
        )
    return out


def read_label(residual_gap: int, all_variant: int) -> str:
    if all_variant == 0:
        return "simple one-edit variant leads do not cover any current gap rows"
    if residual_gap > 0:
        return "simple one-edit variant leads cannot close the current defined-distance gap"
    return "simple one-edit variant leads could close the count gap only as an upper bound, not as source evidence"


def format_percent(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return ""
    return f"{(numerator / denominator) * 100:.2f}"


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    best = best_row(rows)
    lines = [
        "# WRR Variant Gap Upper Bound",
        "",
        "Status: diagnostic-only upper bound. This does not replace terms, does",
        "not authorize source corrections, and is not a WRR reproduction.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_variant_gap_upper_bound "
            f"--defined-pair-summary {args.defined_pair_summary} "
            f"--variant-gap-summary {args.variant_gap_summary} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Upper-Bound Table",
        "",
        "| Run | Current defined | Gap to 163 | All blockers have simple variant | Some blockers | No blockers | Upper-bound defined | Residual gap | Gap coverage % | Read |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| {run_label} | {current_defined_distances} | {current_gap_to_source_cited} | "
            "{blocked_pairs_all_terms_with_simple_variant} | "
            "{blocked_pairs_some_terms_with_simple_variant} | "
            "{blocked_pairs_no_terms_with_simple_variant} | "
            "{upper_bound_defined_distances} | "
            "{residual_gap_after_simple_variant_upper_bound} | "
            "{gap_coverage_percent} | {read} |".format(**row)
        )
    if best:
        lines.extend(
            [
                "",
                "## Current Read",
                "",
                f"- Best current run: `{best['run_label']}`.",
                f"- Current defined distances: {best['current_defined_distances']} of {best['source_cited_defined_distances']}.",
                f"- Simple one-edit variant leads cover all blockers for at most {best['blocked_pairs_all_terms_with_simple_variant']} blocked pairs.",
                f"- Even if every covered simple variant lead were valid source evidence, the upper bound is {best['upper_bound_defined_distances']} defined distances.",
                f"- Residual gap after that upper bound: {best['residual_gap_after_simple_variant_upper_bound']}.",
                "- Therefore simple one-edit variants alone cannot explain the full 163-distance count gap under the current run.",
                "- This is source-review triage only; accepting any variant still requires a citable source rule.",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def best_row(rows: list[dict[str, str]]) -> dict[str, str] | None:
    if not rows:
        return None
    return min(
        rows,
        key=lambda row: (
            int(row["residual_gap_after_simple_variant_upper_bound"]),
            -int(row["current_defined_distances"]),
            row["run_label"],
        ),
    )


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": "analyze_wrr_variant_gap_upper_bound",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "defined_pair_summary": str(args.defined_pair_summary),
            "variant_gap_summary": str(args.variant_gap_summary),
        },
        "outputs": {
            "out": str(args.out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
        "rows": len(rows),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
