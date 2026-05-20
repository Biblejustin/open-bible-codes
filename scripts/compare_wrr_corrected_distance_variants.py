#!/usr/bin/env python3
"""Compare WRR corrected-distance smoke summary variants."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


OUT = Path("reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_corrected_distance_variant_comparison.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_corrected_distance_variant_comparison.manifest.json")

FIELDNAMES = [
    "variant",
    "summary_path",
    "pairs",
    "candidate_lane",
    "search_max_skip",
    "skip_cap_mode",
    "skip_cap_formula",
    "minimum_valid",
    "defined_corrected_distances",
    "ordinary_not_valid_pairs",
    "under_minimum_valid_pairs",
    "min_corrected_distance",
    "min_corrected_pair_id",
    "max_pair_valid_perturbations",
    "status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_variant_rows(args.variant)
    write_rows(args.out, rows)
    write_markdown(args.markdown_out, rows)
    if args.manifest_out:
        write_manifest(args, rows, started)
    print(args.out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--variant",
        action="append",
        required=True,
        help="Variant in label=summary.csv form.",
    )
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_variant_rows(variants: list[str]) -> list[dict[str, str]]:
    rows = []
    for variant in variants:
        label, path = parse_variant(variant)
        summary = read_summary(path)
        row = {field: summary.get(field, "") for field in FIELDNAMES}
        row["variant"] = label
        row["summary_path"] = str(path)
        rows.append(row)
    return rows


def parse_variant(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise ValueError("--variant must use label=summary.csv")
    label, path = value.split("=", 1)
    label = label.strip()
    if not label:
        raise ValueError("variant label must not be empty")
    return label, Path(path)


def read_summary(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError(f"expected exactly one summary row in {path}")
    return rows[0]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        "# WRR2 Corrected Distance Variant Comparison",
        "",
        "This compares corrected-distance smoke summaries under alternate skip-cap",
        "settings. It is a decision aid only; it does not lock the WRR method.",
        "",
        "| Variant | Pairs | Defined c | Ordinary invalid | Under 10 valid | Max valid | Status |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['variant']}`",
                    row["pairs"],
                    row["defined_corrected_distances"],
                    row["ordinary_not_valid_pairs"],
                    row["under_minimum_valid_pairs"],
                    row["max_pair_valid_perturbations"],
                    f"`{row['status']}`",
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(args: argparse.Namespace, rows: list[dict[str, str]], started: float) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "variants": [row["variant"] for row in rows],
        "rows": len(rows),
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
