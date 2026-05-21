#!/usr/bin/env python3
"""Build a compact tracked report for a paired-control pilot run."""

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
from els.statistics import numeric_value
from els.term_display import display_term


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    full_targets = read_rows(args.full_targets)
    pilot_targets = read_rows(args.pilot_targets)
    controls = read_rows(args.controls)
    report = build_report(
        full_targets=full_targets,
        pilot_targets=pilot_targets,
        controls=controls,
        title=args.title,
        description=args.description,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding="utf-8")
    write_manifest(args, full_targets, pilot_targets, controls, started)
    print(args.out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-targets", type=Path, required=True)
    parser.add_argument("--pilot-targets", type=Path, required=True)
    parser.add_argument("--controls", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, required=True)
    parser.add_argument("--title", default="Control Pilot Report")
    parser.add_argument(
        "--description",
        default=(
            "This report summarizes a deterministic paired-control pilot over a "
            "fixed subset of a larger representative-control target table."
        ),
    )
    return parser


def build_report(
    *,
    full_targets: list[dict[str, str]],
    pilot_targets: list[dict[str, str]],
    controls: list[dict[str, str]],
    title: str,
    description: str,
) -> str:
    band_counts = Counter(row.get("paired_band", "") for row in controls)
    corpus_counts = Counter(row.get("corpus", "") for row in pilot_targets)
    q_rows = [row for row in controls if leq(row.get("combined_min_q_value"), 0.05)]
    p_rows = [row for row in controls if leq(row.get("combined_min_p_ge"), 0.05)]
    samples = sample_summary(controls)
    lines = [
        f"# {title}",
        "",
        "Status: paired-control pilot complete; no claim.",
        "",
        description,
        "",
        "This pilot is calibration and triage material only. It does not replace",
        "the full registered representative-control run.",
        "",
        "## Scope",
        "",
        "| Metric | Rows |",
        "| --- | ---: |",
        f"| Full control target rows | {len(full_targets):,} |",
        f"| Pilot target rows | {len(pilot_targets):,} |",
        f"| Control result rows | {len(controls):,} |",
        f"| Pilot share of full target table | {pilot_share(len(pilot_targets), len(full_targets))} |",
        f"| Term-shuffle samples per row | {samples.get('term_shuffle_samples', '')} |",
        f"| Random samples per row | {samples.get('random_samples', '')} |",
        "",
        "## Pilot Corpus Counts",
        "",
        "| Corpus | Rows |",
        "| --- | ---: |",
    ]
    for corpus, count in sorted(corpus_counts.items()):
        lines.append(f"| `{corpus}` | {count:,} |")
    lines.extend(["", "## Control Bands", "", "| Band | Rows |", "| --- | ---: |"])
    for band, count in sorted(band_counts.items()):
        lines.append(f"| `{band}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Statistical Read",
            "",
            f"- rows with uncorrected `combined_min_p_ge <= 0.05`: {len(p_rows):,}",
            f"- rows with adjusted `combined_min_q_value <= 0.05`: {len(q_rows):,}",
            "- rows here are pilot rows only; use them to decide whether a full run is worth the cost.",
            "",
            "## Most Notable Pilot Rows",
            "",
            "| Corpus | Term | Concept | Hits | Term p | Random p | Combined q | Band | Read |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in sorted(controls, key=control_sort_key)[:40]:
        lines.append(
            "| "
            + " | ".join(
                [
                    row.get("corpus", ""),
                    display_term(row.get("normalized_term", ""), english=row.get("concept", "")),
                    md_cell(row.get("concept", "")),
                    row.get("observed_hits", ""),
                    row.get("term_shuffle_p_ge", ""),
                    row.get("random_p_ge", ""),
                    row.get("combined_min_q_value", ""),
                    f"`{row.get('paired_band', '')}`",
                    md_cell(row.get("read", "")),
                ]
            )
            + " |"
        )
    return "\n".join(lines).rstrip() + "\n"


def sample_summary(rows: list[dict[str, str]]) -> dict[str, str]:
    if not rows:
        return {}
    return {
        "term_shuffle_samples": rows[0].get("term_shuffle_samples", ""),
        "random_samples": rows[0].get("random_samples", ""),
    }


def pilot_share(pilot_count: int, full_count: int) -> str:
    if not full_count:
        return ""
    return f"{pilot_count / full_count:.2%}"


def control_sort_key(row: dict[str, str]) -> tuple[float, float, int, str, str]:
    q_value = numeric_value(row.get("combined_min_q_value"))
    p_value = numeric_value(row.get("combined_min_p_ge"))
    return (
        1.0 if q_value is None else q_value,
        1.0 if p_value is None else p_value,
        -int_or_zero(row.get("observed_hits")),
        row.get("corpus", ""),
        row.get("term_id", ""),
    )


def leq(value: object, threshold: float) -> bool:
    numeric = numeric_value(value)
    return numeric is not None and numeric <= threshold


def write_manifest(
    args: argparse.Namespace,
    full_targets: list[dict[str, str]],
    pilot_targets: list[dict[str, str]],
    controls: list[dict[str, str]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "tool": "build_control_pilot_report",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "full_targets": str(args.full_targets),
        "pilot_targets": str(args.pilot_targets),
        "controls": str(args.controls),
        "out": str(args.out),
        "full_target_rows": len(full_targets),
        "pilot_target_rows": len(pilot_targets),
        "control_rows": len(controls),
        "seconds": round(time.perf_counter() - started, 3),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


if __name__ == "__main__":
    raise SystemExit(main())
