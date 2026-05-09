#!/usr/bin/env python3
"""Build the Gog/Magog prospective pair-control report."""

from __future__ import annotations

import argparse
import csv
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path("reports/gog_magog_pair_prospective")
TARGET_SUMMARY = ROOT / "target_summary.csv"
BASELINE_SUMMARY = ROOT / "pair_baselines_summary.csv"
SYNTHETIC_MT_WLC = ROOT / "synthetic_mt_wlc_comparison.csv"
SYNTHETIC_UHB = ROOT / "synthetic_uhb_comparison.csv"
OUT = Path("docs/GOG_MAGOG_PAIR_PROSPECTIVE_REPORT.md")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    target_rows = read_rows(args.target_summary)
    baseline_rows = read_rows(args.baseline_summary)
    synthetic_rows = []
    for label, path in (("MT_WLC", args.synthetic_mt_wlc), ("UHB", args.synthetic_uhb)):
        synthetic_rows.extend({**row, "corpus": label} for row in read_rows(path))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        report_markdown(target_rows, baseline_rows, synthetic_rows),
        encoding="utf-8",
    )
    print(args.out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-summary", type=Path, default=TARGET_SUMMARY)
    parser.add_argument("--baseline-summary", type=Path, default=BASELINE_SUMMARY)
    parser.add_argument("--synthetic-mt-wlc", type=Path, default=SYNTHETIC_MT_WLC)
    parser.add_argument("--synthetic-uhb", type=Path, default=SYNTHETIC_UHB)
    parser.add_argument("--out", type=Path, default=OUT)
    return parser


def report_markdown(
    target_rows: list[dict[str, str]],
    baseline_rows: list[dict[str, str]],
    synthetic_rows: list[dict[str, str]],
) -> str:
    lines = [
        "# Gog/Magog Pair Prospective Report",
        "",
        f"Generated: {datetime.now(UTC).isoformat()}",
        "",
        "Status: prospective controlled review output, not a claim.",
        "",
        *outcome_lines(target_rows, synthetic_rows),
        "",
        "Locked rule: Hebrew `גוג` / `מגוג`, MT_WLC and UHB only, skip `2..100`, direction `both`, same chapter, same signed skip, max gap `500`.",
        "",
        "## Target Pair Controls",
        "",
        "| Corpus | Left hits | Right hits | Close pairs | Overlaps | Best gap | Term p_ge | Random p_ge | Combined q | Band | Read |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in target_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.get("corpus", ""),
                    row.get("left_hits", ""),
                    row.get("right_hits", ""),
                    row.get("observed_pairs_within_gap", ""),
                    row.get("observed_overlap_pairs", ""),
                    row.get("observed_best_span_gap", ""),
                    row.get("term_pairs_p_ge", ""),
                    row.get("random_pairs_p_ge", ""),
                    row.get("combined_min_q", ""),
                    f"`{row.get('pair_band', '')}`",
                    row.get("read", ""),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Declared Pair Baselines",
            "",
            "| Pair | Corpus | Close pairs | Overlaps | Best gap | Read |",
            "| --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in baseline_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.get("pair_label", ""),
                    row.get("corpus", ""),
                    row.get("observed_pairs_within_gap", ""),
                    row.get("observed_overlap_pairs", ""),
                    row.get("observed_best_span_gap", ""),
                    row.get("read", ""),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Synthetic Length-Matched Baselines",
            "",
            "| Corpus | Target | Target close | Synthetic close mean | Synthetic >= target | p_ge | Read |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in synthetic_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.get("corpus", ""),
                    row.get("target_pair", ""),
                    row.get("target_pairs_within_gap", ""),
                    row.get("synthetic_pairs_mean", ""),
                    row.get("synthetic_pairs_ge_target", ""),
                    row.get("synthetic_pairs_p_ge", ""),
                    row.get("read", ""),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read Standard",
            "",
            "List every observed pair result. Treat a successful row only as `prospective_controlled_review_candidate` if it beats declared pair baselines and synthetic length-matched baselines under this locked design.",
            "",
            "Do not call the result proof, prophecy confirmation, or claim-level evidence.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def outcome_lines(
    target_rows: list[dict[str, str]],
    synthetic_rows: list[dict[str, str]],
) -> list[str]:
    control_failure = any(row.get("pair_band") == "not_unusual" for row in target_rows)
    synthetic_failure = any(
        "can match or exceed" in row.get("read", "") for row in synthetic_rows
    )
    if control_failure or synthetic_failure:
        return [
            "## Outcome",
            "",
            "No `prospective_controlled_review_candidate` is produced. The target pair occurs, including strict overlap examples, but it does not beat the locked paired and synthetic controls.",
        ]
    return [
        "## Outcome",
        "",
        "The registered thresholds require manual review because the target pair was not rejected by the locked paired and synthetic controls.",
    ]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
