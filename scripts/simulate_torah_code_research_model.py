#!/usr/bin/env python3
"""Simulate the Torah-code.org research geometric level-1 model."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean, pstdev

from els import __version__


DEFAULT_OUT = Path("reports/torah_code_research_model/geometric_level1.csv")
DEFAULT_MD = Path("docs/TORAH_CODE_RESEARCH_MODEL_SIMULATION.md")
DEFAULT_MANIFEST = Path("reports/torah_code_research_model/manifest.json")
SOURCE_URL = "https://www.torah-code.org/research/research_3.html"
FIELDNAMES = [
    "point_count",
    "moved_fraction",
    "closeness_factor",
    "replicates",
    "seed",
    "alpha",
    "null_mean",
    "null_stdev",
    "alternative_mean",
    "alternative_stdev",
    "mean_shift",
    "power_p_le_alpha",
    "median_null_p_value",
    "alternative_lower_than_null_mean_rate",
    "interpretation",
]


@dataclass(frozen=True)
class Point:
    x: float
    y: float


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.replicates < 1:
        raise SystemExit("--replicates must be >= 1")
    rows = run_grid(args)
    write_rows(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args.manifest_out, args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--point-count", type=int, action="append", default=[])
    parser.add_argument("--moved-fraction", type=float, action="append", default=[])
    parser.add_argument("--closeness-factor", type=float, action="append", default=[])
    parser.add_argument("--replicates", type=int, default=200)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20260520)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def run_grid(args: argparse.Namespace) -> list[dict[str, str]]:
    point_counts = args.point_count or [10, 25, 50]
    moved_fractions = args.moved_fraction or [0.10, 0.25, 0.50]
    closeness_factors = args.closeness_factor or [0.25, 0.50, 0.75]
    rows: list[dict[str, str]] = []
    for point_count in point_counts:
        for moved_fraction in moved_fractions:
            for closeness_factor in closeness_factors:
                rows.append(
                    summarize_setting(
                        point_count=point_count,
                        moved_fraction=moved_fraction,
                        closeness_factor=closeness_factor,
                        replicates=args.replicates,
                        alpha=args.alpha,
                        seed=setting_seed(
                            args.seed,
                            point_count,
                            moved_fraction,
                            closeness_factor,
                        ),
                    )
                )
    return rows


def setting_seed(
    base_seed: int,
    point_count: int,
    moved_fraction: float,
    closeness_factor: float,
) -> int:
    return (
        int(base_seed)
        + point_count * 10_000
        + int(round(moved_fraction * 1_000)) * 100
        + int(round(closeness_factor * 1_000))
    )


def summarize_setting(
    *,
    point_count: int,
    moved_fraction: float,
    closeness_factor: float,
    replicates: int,
    alpha: float,
    seed: int,
) -> dict[str, str]:
    if point_count < 1:
        raise ValueError("point_count must be >= 1")
    if not 0 <= moved_fraction <= 1:
        raise ValueError("moved_fraction must be between 0 and 1")
    if not 0 <= closeness_factor <= 1:
        raise ValueError("closeness_factor must be between 0 and 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    rng = random.Random(seed)
    null_stats = [
        compactness_statistic(random_points(rng, point_count), random_points(rng, point_count))
        for _ in range(replicates)
    ]
    alt_stats = []
    for _ in range(replicates):
        fixed = random_points(rng, point_count)
        moving = random_points(rng, point_count)
        alt_stats.append(
            compactness_statistic(
                fixed,
                move_toward_nearest(
                    fixed,
                    moving,
                    moved_fraction=moved_fraction,
                    closeness_factor=closeness_factor,
                    rng=rng,
                ),
            )
        )
    p_values = [left_tail_p_value(null_stats, value) for value in alt_stats]
    power = sum(1 for value in p_values if value <= alpha) / replicates
    lower_than_mean = sum(1 for value in alt_stats if value < mean(null_stats)) / replicates
    shift = mean(null_stats) - mean(alt_stats)
    return {
        "point_count": str(point_count),
        "moved_fraction": format_float(moved_fraction),
        "closeness_factor": format_float(closeness_factor),
        "replicates": str(replicates),
        "seed": str(seed),
        "alpha": format_float(alpha),
        "null_mean": format_float(mean(null_stats)),
        "null_stdev": format_float(pstdev(null_stats)),
        "alternative_mean": format_float(mean(alt_stats)),
        "alternative_stdev": format_float(pstdev(alt_stats)),
        "mean_shift": format_float(shift),
        "power_p_le_alpha": format_float(power),
        "median_null_p_value": format_float(median(p_values)),
        "alternative_lower_than_null_mean_rate": format_float(lower_than_mean),
        "interpretation": interpretation(power, shift),
    }


def random_points(rng: random.Random, count: int) -> tuple[Point, ...]:
    return tuple(Point(rng.random(), rng.random()) for _ in range(count))


def move_toward_nearest(
    fixed: tuple[Point, ...],
    moving: tuple[Point, ...],
    *,
    moved_fraction: float,
    closeness_factor: float,
    rng: random.Random,
) -> tuple[Point, ...]:
    move_count = round(len(moving) * moved_fraction)
    selected = set(rng.sample(range(len(moving)), k=move_count)) if move_count else set()
    moved: list[Point] = []
    for index, point in enumerate(moving):
        if index not in selected:
            moved.append(point)
            continue
        target = nearest_point(point, fixed)
        distance_factor = rng.random() * closeness_factor
        moved.append(
            Point(
                target.x + distance_factor * (point.x - target.x),
                target.y + distance_factor * (point.y - target.y),
            )
        )
    return tuple(moved)


def compactness_statistic(fixed: tuple[Point, ...], moving: tuple[Point, ...]) -> float:
    return mean(math.sqrt(squared_distance(point, nearest_point(point, fixed))) for point in moving)


def nearest_point(point: Point, candidates: tuple[Point, ...]) -> Point:
    if not candidates:
        raise ValueError("candidates must not be empty")
    return min(candidates, key=lambda candidate: squared_distance(point, candidate))


def squared_distance(left: Point, right: Point) -> float:
    return (left.x - right.x) ** 2 + (left.y - right.y) ** 2


def left_tail_p_value(null_stats: list[float], observed: float) -> float:
    return (sum(1 for value in null_stats if value <= observed) + 1) / (len(null_stats) + 1)


def median(values: list[float]) -> float:
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def interpretation(power: float, shift: float) -> str:
    if shift <= 0:
        return "no_compactness_shift"
    if power >= 0.8:
        return "high_power_for_declared_model"
    if power >= 0.5:
        return "moderate_power_for_declared_model"
    return "low_power_for_declared_model"


def format_float(value: float) -> str:
    return f"{value:.6g}"


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    strongest = sorted(rows, key=lambda row: float(row["power_p_le_alpha"]), reverse=True)[:10]
    lines = [
        "# Torah-Code Research Model Simulation",
        "",
        "Status: simulation harness; not a Torah-code result.",
        "",
        "Source lead:",
        "",
        f"- `{SOURCE_URL}`",
        "",
        "This implements the first geometric level-1 model described by the",
        "Torah-code.org research-program page. Each run compares two independent",
        "uniform point sets in the unit square against an alternative where a",
        "declared fraction of the second set is moved toward its nearest point in",
        "the first set. The statistic is mean nearest-neighbor distance from the",
        "second set to the first set; smaller values mean more compact meetings.",
        "",
        "The page does not specify a final test statistic, so this harness is a",
        "transparent power/sanity check for one simple statistic, not a source",
        "replication claim.",
        "",
        "Reproduce with:",
        "",
        "```bash",
        "python3 -m scripts.simulate_torah_code_research_model",
        "```",
        "",
        "## Settings",
        "",
        f"- replicates per setting: `{args.replicates}`",
        f"- alpha: `{format_float(args.alpha)}`",
        f"- base seed: `{args.seed}`",
        "",
        "## Strongest Settings",
        "",
        "| N | moved fraction | closeness factor | null mean | alternative mean | power | read |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in strongest:
        lines.append(
            "| {point_count} | {moved_fraction} | {closeness_factor} | {null_mean} | "
            "{alternative_mean} | {power_p_le_alpha} | {interpretation} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- This is model-design scaffolding only.",
            "- It uses Euclidean unit-square distance.",
            "- It interprets the page's movement description as a distance factor",
            "  sampled uniformly from `[0, closeness_factor]`.",
            "- ELS cylinder geometry remains separate work.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "source_url": SOURCE_URL,
        "args": {
            "point_count": args.point_count,
            "moved_fraction": args.moved_fraction,
            "closeness_factor": args.closeness_factor,
            "replicates": args.replicates,
            "alpha": args.alpha,
            "seed": args.seed,
        },
        "rows": len(rows),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
