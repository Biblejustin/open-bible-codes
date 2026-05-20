#!/usr/bin/env python3
"""Simulate the Torah-code.org research ELS level-1 model."""

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
from els.wrr import cylindrical_letter_distance_squared, ordinary_els_offsets, wrr_row_widths
from scripts.simulate_torah_code_research_model import (
    format_float,
    interpretation,
    left_tail_p_value,
    median,
)


DEFAULT_OUT = Path("reports/torah_code_research_model/els_level1.csv")
DEFAULT_MD = Path("docs/TORAH_CODE_RESEARCH_ELS_MODEL_SIMULATION.md")
DEFAULT_MANIFEST = Path("reports/torah_code_research_model/els_manifest.json")
SOURCE_URL = "https://www.torah-code.org/research/research_3c.html"
STAT_SOURCE_URL = "https://www.torah-code.org/research/research_12.shtml"
EPSILON = 1e-12
STATISTICS = (
    "arithmetic_mean",
    "geometric_mean",
    "harmonic_mean",
    "order_trimmed_mean",
)
FIELDNAMES = [
    "els_count",
    "left_word_length",
    "right_word_length",
    "text_length",
    "max_skip",
    "row_width_count",
    "moved_fraction",
    "compactness_factor",
    "statistic",
    "replicates",
    "seed",
    "alpha",
    "null_usable",
    "alternative_usable",
    "null_comparable_distance_mean",
    "alternative_comparable_distance_mean",
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
class ElsOccurrence:
    start: int
    skip: int
    word_length: int

    def offsets(self) -> tuple[int, ...]:
        return ordinary_els_offsets(self.start, self.skip, self.word_length)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    validate_args(args)
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
    parser.add_argument("--els-count", type=int, action="append", default=[])
    parser.add_argument("--left-word-length", type=int, default=5)
    parser.add_argument("--right-word-length", type=int, default=6)
    parser.add_argument("--text-length", type=int, default=5000)
    parser.add_argument("--max-skip", type=int, default=120)
    parser.add_argument("--row-width-count", type=int, default=10)
    parser.add_argument("--moved-fraction", type=float, action="append", default=[])
    parser.add_argument("--compactness-factor", type=float, action="append", default=[])
    parser.add_argument("--replicates", type=int, default=200)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20260520)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_args(args: argparse.Namespace) -> None:
    if args.replicates < 1:
        raise SystemExit("--replicates must be >= 1")
    if args.text_length < 10:
        raise SystemExit("--text-length must be >= 10")
    if args.left_word_length < 2 or args.right_word_length < 2:
        raise SystemExit("word lengths must be >= 2")
    if args.max_skip < 1:
        raise SystemExit("--max-skip must be >= 1")
    if args.row_width_count < 1:
        raise SystemExit("--row-width-count must be >= 1")
    if not 0 < args.alpha < 1:
        raise SystemExit("--alpha must be between 0 and 1")


def run_grid(args: argparse.Namespace) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    els_counts = args.els_count or [10]
    moved_fractions = args.moved_fraction or [0.25, 0.50]
    compactness_factors = args.compactness_factor or [0.25, 0.50, 0.75]
    for els_count in els_counts:
        for moved_fraction in moved_fractions:
            for compactness_factor in compactness_factors:
                rows.extend(
                    summarize_setting(
                        els_count=els_count,
                        left_word_length=args.left_word_length,
                        right_word_length=args.right_word_length,
                        text_length=args.text_length,
                        max_skip=args.max_skip,
                        row_width_count=args.row_width_count,
                        moved_fraction=moved_fraction,
                        compactness_factor=compactness_factor,
                        replicates=args.replicates,
                        alpha=args.alpha,
                        seed=setting_seed(
                            args.seed,
                            els_count,
                            moved_fraction,
                            compactness_factor,
                            args.max_skip,
                        ),
                    )
                )
    return rows


def setting_seed(
    base_seed: int,
    els_count: int,
    moved_fraction: float,
    compactness_factor: float,
    max_skip: int,
) -> int:
    return (
        int(base_seed)
        + els_count * 100_000
        + max_skip * 1_000
        + int(round(moved_fraction * 1_000)) * 10
        + int(round(compactness_factor * 1_000))
    )


def summarize_setting(
    *,
    els_count: int,
    left_word_length: int,
    right_word_length: int,
    text_length: int,
    max_skip: int,
    row_width_count: int,
    moved_fraction: float,
    compactness_factor: float,
    replicates: int,
    alpha: float,
    seed: int,
) -> list[dict[str, str]]:
    if els_count < 1:
        raise ValueError("els_count must be >= 1")
    if not 0 <= moved_fraction <= 1:
        raise ValueError("moved_fraction must be between 0 and 1")
    if not 0 <= compactness_factor <= 1:
        raise ValueError("compactness_factor must be between 0 and 1")
    rng = random.Random(seed)
    null_runs = []
    alternative_runs = []
    for _ in range(replicates):
        left = random_els_set(
            rng,
            count=els_count,
            word_length=left_word_length,
            text_length=text_length,
            max_skip=max_skip,
        )
        right = random_els_set(
            rng,
            count=els_count,
            word_length=right_word_length,
            text_length=text_length,
            max_skip=max_skip,
        )
        null_runs.append(meeting_statistics(left, right, row_width_count=row_width_count))

        alt_left = random_els_set(
            rng,
            count=els_count,
            word_length=left_word_length,
            text_length=text_length,
            max_skip=max_skip,
        )
        alt_right = random_els_set(
            rng,
            count=els_count,
            word_length=right_word_length,
            text_length=text_length,
            max_skip=max_skip,
        )
        alternative_runs.append(
            meeting_statistics(
                alt_left,
                move_toward_best_meetings(
                    alt_left,
                    alt_right,
                    moved_fraction=moved_fraction,
                    compactness_factor=compactness_factor,
                    text_length=text_length,
                    row_width_count=row_width_count,
                    rng=rng,
                ),
                row_width_count=row_width_count,
            )
        )
    return [
        summarize_statistic(
            statistic=statistic,
            null_runs=null_runs,
            alternative_runs=alternative_runs,
            els_count=els_count,
            left_word_length=left_word_length,
            right_word_length=right_word_length,
            text_length=text_length,
            max_skip=max_skip,
            row_width_count=row_width_count,
            moved_fraction=moved_fraction,
            compactness_factor=compactness_factor,
            replicates=replicates,
            seed=seed,
            alpha=alpha,
        )
        for statistic in STATISTICS
    ]


def random_els_set(
    rng: random.Random,
    *,
    count: int,
    word_length: int,
    text_length: int,
    max_skip: int,
) -> tuple[ElsOccurrence, ...]:
    return tuple(
        random_els(rng, word_length=word_length, text_length=text_length, max_skip=max_skip)
        for _ in range(count)
    )


def random_els(
    rng: random.Random,
    *,
    word_length: int,
    text_length: int,
    max_skip: int,
) -> ElsOccurrence:
    for _ in range(1_000):
        start = rng.randint(0, text_length - word_length)
        skips = valid_skip_values(start, word_length=word_length, text_length=text_length, max_skip=max_skip)
        if skips:
            return ElsOccurrence(start=start, skip=rng.choice(skips), word_length=word_length)
    candidates = [
        (start, skip)
        for start in range(text_length)
        for skip in valid_skip_values(
            start,
            word_length=word_length,
            text_length=text_length,
            max_skip=max_skip,
        )
    ]
    if not candidates:
        raise ValueError("no valid ELS positions for requested text/word/skip settings")
    start, skip = rng.choice(candidates)
    return ElsOccurrence(start=start, skip=skip, word_length=word_length)


def valid_skip_values(
    start: int,
    *,
    word_length: int,
    text_length: int,
    max_skip: int,
) -> tuple[int, ...]:
    values = []
    for skip in range(1, max_skip + 1):
        last = start + (word_length - 1) * skip
        if last < text_length:
            values.append(skip)
    return tuple(values)


def resonant_row_widths(
    left_skip: int,
    right_skip: int,
    *,
    row_width_count: int,
) -> tuple[int, ...]:
    left = set(wrr_row_widths(left_skip, count=row_width_count))
    right = set(wrr_row_widths(right_skip, count=row_width_count))
    return tuple(sorted(left & right))


def els_pair_distance(
    left: ElsOccurrence,
    right: ElsOccurrence,
    *,
    row_width_count: int,
) -> float | None:
    widths = resonant_row_widths(left.skip, right.skip, row_width_count=row_width_count)
    if not widths:
        return None
    left_offsets = left.offsets()
    right_offsets = right.offsets()
    return min(
        hausdorff_cylinder_distance(left_offsets, right_offsets, row_width)
        for row_width in widths
    )


def hausdorff_cylinder_distance(
    left_offsets: tuple[int, ...],
    right_offsets: tuple[int, ...],
    row_width: int,
) -> float:
    left_to_right = max(nearest_cylinder_distance(offset, right_offsets, row_width) for offset in left_offsets)
    right_to_left = max(nearest_cylinder_distance(offset, left_offsets, row_width) for offset in right_offsets)
    return max(left_to_right, right_to_left)


def nearest_cylinder_distance(
    offset: int,
    candidates: tuple[int, ...],
    row_width: int,
) -> float:
    return math.sqrt(
        min(cylindrical_letter_distance_squared(offset, candidate, row_width) for candidate in candidates)
    )


def nearest_meeting_distances(
    left: tuple[ElsOccurrence, ...],
    right: tuple[ElsOccurrence, ...],
    *,
    row_width_count: int,
) -> list[float]:
    distances = []
    for occurrence in left:
        distance = nearest_pair_distance(occurrence, right, row_width_count=row_width_count)
        if distance is not None:
            distances.append(distance)
    for occurrence in right:
        distance = nearest_pair_distance(occurrence, left, row_width_count=row_width_count)
        if distance is not None:
            distances.append(distance)
    return distances


def nearest_pair_distance(
    occurrence: ElsOccurrence,
    candidates: tuple[ElsOccurrence, ...],
    *,
    row_width_count: int,
) -> float | None:
    distances = [
        distance
        for candidate in candidates
        if (distance := els_pair_distance(occurrence, candidate, row_width_count=row_width_count)) is not None
    ]
    return min(distances) if distances else None


def move_toward_best_meetings(
    fixed: tuple[ElsOccurrence, ...],
    moving: tuple[ElsOccurrence, ...],
    *,
    moved_fraction: float,
    compactness_factor: float,
    text_length: int,
    row_width_count: int,
    rng: random.Random,
) -> tuple[ElsOccurrence, ...]:
    move_count = round(len(moving) * moved_fraction)
    selected = set(rng.sample(range(len(moving)), k=move_count)) if move_count else set()
    moved = []
    for index, occurrence in enumerate(moving):
        if index not in selected:
            moved.append(occurrence)
            continue
        best = best_meeting(occurrence, fixed, row_width_count=row_width_count)
        moved.append(
            move_els_toward(
                occurrence,
                best,
                compactness_factor=compactness_factor,
                text_length=text_length,
            )
            if best is not None
            else occurrence
        )
    return tuple(moved)


def best_meeting(
    occurrence: ElsOccurrence,
    candidates: tuple[ElsOccurrence, ...],
    *,
    row_width_count: int,
) -> ElsOccurrence | None:
    best: tuple[float, ElsOccurrence] | None = None
    for candidate in candidates:
        distance = els_pair_distance(occurrence, candidate, row_width_count=row_width_count)
        if distance is None:
            continue
        if best is None or distance < best[0]:
            best = (distance, candidate)
    return best[1] if best is not None else None


def move_els_toward(
    occurrence: ElsOccurrence,
    target: ElsOccurrence,
    *,
    compactness_factor: float,
    text_length: int,
) -> ElsOccurrence:
    desired = round(target.start + compactness_factor * (occurrence.start - target.start))
    return ElsOccurrence(
        start=clamp_start(
            desired,
            skip=occurrence.skip,
            word_length=occurrence.word_length,
            text_length=text_length,
        ),
        skip=occurrence.skip,
        word_length=occurrence.word_length,
    )


def clamp_start(
    start: int,
    *,
    skip: int,
    word_length: int,
    text_length: int,
) -> int:
    low = 0
    high = text_length - 1 - (word_length - 1) * skip
    if high < low:
        raise ValueError("skip/word length cannot fit in text")
    return max(low, min(high, start))


def meeting_statistics(
    left: tuple[ElsOccurrence, ...],
    right: tuple[ElsOccurrence, ...],
    *,
    row_width_count: int,
) -> dict[str, float | int | None]:
    distances = nearest_meeting_distances(left, right, row_width_count=row_width_count)
    stats: dict[str, float | int | None] = {"comparable_distances": len(distances)}
    stats.update(statistic_values(distances))
    return stats


def statistic_values(distances: list[float]) -> dict[str, float | None]:
    if not distances:
        return {statistic: None for statistic in STATISTICS}
    ordered = sorted(distances)
    trimmed = ordered[1:] if len(ordered) > 1 else ordered
    return {
        "arithmetic_mean": mean(distances),
        "geometric_mean": math.exp(mean(math.log(max(value, EPSILON)) for value in distances)),
        "harmonic_mean": len(distances) / sum(1 / max(value, EPSILON) for value in distances),
        "order_trimmed_mean": mean(trimmed),
    }


def summarize_statistic(
    *,
    statistic: str,
    null_runs: list[dict[str, float | int | None]],
    alternative_runs: list[dict[str, float | int | None]],
    els_count: int,
    left_word_length: int,
    right_word_length: int,
    text_length: int,
    max_skip: int,
    row_width_count: int,
    moved_fraction: float,
    compactness_factor: float,
    replicates: int,
    seed: int,
    alpha: float,
) -> dict[str, str]:
    null_values = numeric_values(null_runs, statistic)
    alternative_values = numeric_values(alternative_runs, statistic)
    if not null_values or not alternative_values:
        raise ValueError(f"no usable {statistic} values; increase row_width_count or reduce max_skip")
    p_values = [left_tail_p_value(null_values, value) for value in alternative_values]
    power = sum(1 for value in p_values if value <= alpha) / len(p_values)
    lower_than_mean = sum(1 for value in alternative_values if value < mean(null_values)) / len(
        alternative_values
    )
    shift = mean(null_values) - mean(alternative_values)
    return {
        "els_count": str(els_count),
        "left_word_length": str(left_word_length),
        "right_word_length": str(right_word_length),
        "text_length": str(text_length),
        "max_skip": str(max_skip),
        "row_width_count": str(row_width_count),
        "moved_fraction": format_float(moved_fraction),
        "compactness_factor": format_float(compactness_factor),
        "statistic": statistic,
        "replicates": str(replicates),
        "seed": str(seed),
        "alpha": format_float(alpha),
        "null_usable": str(len(null_values)),
        "alternative_usable": str(len(alternative_values)),
        "null_comparable_distance_mean": format_float(comparable_distance_mean(null_runs)),
        "alternative_comparable_distance_mean": format_float(comparable_distance_mean(alternative_runs)),
        "null_mean": format_float(mean(null_values)),
        "null_stdev": format_float(pstdev(null_values)),
        "alternative_mean": format_float(mean(alternative_values)),
        "alternative_stdev": format_float(pstdev(alternative_values)),
        "mean_shift": format_float(shift),
        "power_p_le_alpha": format_float(power),
        "median_null_p_value": format_float(median(p_values)),
        "alternative_lower_than_null_mean_rate": format_float(lower_than_mean),
        "interpretation": interpretation(power, shift),
    }


def numeric_values(rows: list[dict[str, float | int | None]], key: str) -> list[float]:
    return [float(value) for row in rows if (value := row[key]) is not None]


def comparable_distance_mean(rows: list[dict[str, float | int | None]]) -> float:
    return mean(float(row["comparable_distances"]) for row in rows)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    strongest = sorted(rows, key=lambda row: float(row["power_p_le_alpha"]), reverse=True)[:12]
    lines = [
        "# Torah-Code ELS Model Simulation",
        "",
        "Status: simulation harness; not a Torah-code result.",
        "",
        "Source leads:",
        "",
        f"- `{SOURCE_URL}`",
        f"- `{STAT_SOURCE_URL}`",
        "",
        "This implements a level-1 ELS analogue of the research-program model:",
        "two random ELS sets are generated under a null model; under the",
        "alternative, a declared fraction of the second set is translated toward",
        "its best resonant-cylinder meeting in the first set.",
        "",
        "The implementation uses the repo's WRR row-width helper as a transparent",
        "resonance proxy: candidate cylinder sizes are the intersection of the",
        "first row widths derived from each ELS skip. Pair distance is the best",
        "symmetric Hausdorff letter distance across those shared cylinder sizes.",
        "",
        "Statistics compared here are arithmetic, geometric, harmonic, and a simple",
        "trimmed order-statistic mean. The source statistic-selection page mentions",
        "a Fisher linear discriminant over order statistics, but does not provide",
        "weights here; that remains a later upgrade.",
        "",
        "Reproduce with:",
        "",
        "```bash",
        "python3 -m scripts.simulate_torah_code_research_els_model",
        "```",
        "",
        "## Settings",
        "",
        f"- replicates per setting: `{args.replicates}`",
        f"- alpha: `{format_float(args.alpha)}`",
        f"- base seed: `{args.seed}`",
        f"- text length: `{args.text_length}`",
        f"- max skip: `{args.max_skip}`",
        f"- row-width count: `{args.row_width_count}`",
        "",
        "## Strongest Settings",
        "",
        "| N | moved fraction | factor | statistic | null mean | alternative mean | power | read |",
        "| ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |",
    ]
    for row in strongest:
        lines.append(
            "| {els_count} | {moved_fraction} | {compactness_factor} | {statistic} | "
            "{null_mean} | {alternative_mean} | {power_p_le_alpha} | {interpretation} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- This is model-design scaffolding only.",
            "- It does not test real Torah text.",
            "- It translates generated ELS start positions; it does not require",
            "  the moved ELS to spell a real word in a real corpus.",
            "- The resonant-cylinder definition is explicit and reproducible but",
            "  narrower than a complete source-method reconstruction.",
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
        "source_urls": [SOURCE_URL, STAT_SOURCE_URL],
        "args": {
            "els_count": args.els_count,
            "left_word_length": args.left_word_length,
            "right_word_length": args.right_word_length,
            "text_length": args.text_length,
            "max_skip": args.max_skip,
            "row_width_count": args.row_width_count,
            "moved_fraction": args.moved_fraction,
            "compactness_factor": args.compactness_factor,
            "replicates": args.replicates,
            "alpha": args.alpha,
            "seed": args.seed,
        },
        "rows": len(rows),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
