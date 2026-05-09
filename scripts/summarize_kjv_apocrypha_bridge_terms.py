#!/usr/bin/env python3
"""Summarize KJVA apocrypha bridge terms against term-level controls."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from els import __version__


DEFAULT_CANDIDATES = Path("reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv")
DEFAULT_CONTEXT = Path("reports/kjv_apocrypha_bridge_context/context.csv")
DEFAULT_CONTROLS = Path("reports/kjv_apocrypha_bridge_controls/term_summary.csv")
DEFAULT_SHUFFLED_SUMMARY = Path("reports/kjv_apocrypha_bridge_shuffled_controls_250/summary.csv")
DEFAULT_TERM_SHUFFLED_SUMMARY = Path("reports/kjv_apocrypha_bridge_term_shuffled_controls_1000/term_summary.csv")
DEFAULT_OUT = Path("reports/kjv_apocrypha_bridge_term_review/term_review.csv")
DEFAULT_MARKDOWN = Path("docs/KJV_APOCRYPHA_BRIDGE_TERM_REVIEW.md")
DEFAULT_MANIFEST = Path("reports/kjv_apocrypha_bridge_term_review/manifest.json")

FIELDNAMES = [
    "rank",
    "normalized_term",
    "term_ids",
    "concepts",
    "categories",
    "observed_bridge_rows",
    "canonical_to_apocrypha",
    "apocrypha_to_canonical",
    "multi_segment_bridge",
    "control_max_bridge_rows",
    "control_counts",
    "observed_minus_control_max",
    "observed_gt_all_controls",
    "center_word_exact",
    "center_word_same_concept",
    "center_word_same_category",
    "center_verse_exact",
    "center_verse_same_concept",
    "center_verse_same_category",
    "span_exact",
    "span_same_concept",
    "span_same_category",
    "hidden_path_only",
    "sample_refs",
]

CONTEXT_BUCKETS = [
    "center_word_exact",
    "center_word_same_concept",
    "center_word_same_category",
    "center_verse_exact",
    "center_verse_same_concept",
    "center_verse_same_category",
    "span_exact",
    "span_same_concept",
    "span_same_category",
    "hidden_path_only",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = summarize_terms(
        read_rows(args.candidates),
        read_rows(args.context),
        read_rows(args.controls),
    )
    shuffled = read_summary(args.shuffled_summary)
    term_shuffled = summarize_term_shuffled(read_rows_if_exists(args.term_shuffled_summary))
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, shuffled, term_shuffled, args)
    write_manifest(args.manifest_out, rows, shuffled, term_shuffled, args, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT)
    parser.add_argument("--controls", type=Path, default=DEFAULT_CONTROLS)
    parser.add_argument("--shuffled-summary", type=Path, default=DEFAULT_SHUFFLED_SUMMARY)
    parser.add_argument("--term-shuffled-summary", type=Path, default=DEFAULT_TERM_SHUFFLED_SUMMARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_rows_if_exists(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_rows(path)


def read_summary(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return {row["metric"]: row["value"] for row in read_rows(path)}


def summarize_term_shuffled(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        return {}
    sample_counts = {row.get("samples", "") for row in rows if row.get("samples")}
    return {
        "terms": len(rows),
        "samples": next(iter(sample_counts)) if len(sample_counts) == 1 else "",
        "observed_gt_sample_max": sum(row["observed_gt_sample_max"] == "True" for row in rows),
        "p_le_0_05": sum(float(row["p_ge"]) <= 0.05 for row in rows),
        "p_le_0_01": sum(float(row["p_ge"]) <= 0.01 for row in rows),
        "q_le_0_05": sum(float(row.get("q_ge", "1") or "1") <= 0.05 for row in rows),
        "min_q": min(float(row.get("q_ge", "1") or "1") for row in rows),
        "top_terms": [row["normalized_term"] for row in rows[:12]],
    }


def summarize_terms(
    candidate_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    by_term: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in candidate_rows:
        by_term[row["normalized_term"]].append(row)

    context_by_term: dict[str, Counter[str]] = defaultdict(Counter)
    for row in context_rows:
        context_by_term[row["normalized_term"]][row["context_bucket"]] += 1

    controls_by_term: dict[str, dict[str, int]] = defaultdict(dict)
    for row in control_rows:
        controls_by_term[row["normalized_term"]][row["control_label"]] = int(row["bridge_rows"] or 0)

    output: list[dict[str, object]] = []
    for term, rows in by_term.items():
        first = rows[0]
        bridge_types = Counter(row["bridge_type"] for row in rows)
        control_counts = controls_by_term.get(term, {})
        control_max = max(control_counts.values(), default=0)
        observed = len(rows)
        context_counts = context_by_term.get(term, Counter())
        output.append(
            {
                "normalized_term": term,
                "term_ids": first["term_ids"],
                "concepts": first["concepts"],
                "categories": first["categories"],
                "observed_bridge_rows": observed,
                "canonical_to_apocrypha": bridge_types["canonical_to_apocrypha"],
                "apocrypha_to_canonical": bridge_types["apocrypha_to_canonical"],
                "multi_segment_bridge": bridge_types["multi_segment_bridge"],
                "control_max_bridge_rows": control_max,
                "control_counts": format_control_counts(control_counts),
                "observed_minus_control_max": observed - control_max,
                "observed_gt_all_controls": str(observed > control_max),
                **{bucket: context_counts[bucket] for bucket in CONTEXT_BUCKETS},
                "sample_refs": sample_refs(rows),
            }
        )

    output.sort(
        key=lambda row: (
            row["observed_gt_all_controls"] != "True",
            -int(row["observed_minus_control_max"]),
            -int(row["observed_bridge_rows"]),
            str(row["normalized_term"]),
        )
    )
    for index, row in enumerate(output, start=1):
        row["rank"] = index
    return output


def format_control_counts(counts: dict[str, int]) -> str:
    return ";".join(f"{label}:{counts[label]}" for label in sorted(counts))


def sample_refs(rows: Iterable[dict[str, str]], *, limit: int = 5) -> str:
    refs: list[str] = []
    seen: set[str] = set()
    for row in rows:
        ref = f"{row['start_ref']}->{row['center_ref']}->{row['end_ref']}"
        if ref in seen:
            continue
        seen.add(ref)
        refs.append(ref)
        if len(refs) >= limit:
            break
    return "; ".join(refs)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    shuffled: dict[str, str],
    term_shuffled: dict[str, object],
    args: argparse.Namespace,
) -> None:
    gt_controls = sum(1 for row in rows if row["observed_gt_all_controls"] == "True")
    any_context = sum(1 for row in rows if any(int(row[bucket]) for bucket in CONTEXT_BUCKETS[:-1]))
    term_shuffled_samples = str(term_shuffled.get("samples") or "term-level") if term_shuffled else "term-level"
    term_shuffled_label = (
        f"{term_shuffled_samples}-sample term-level"
        if term_shuffled_samples.isdigit()
        else "term-level"
    )
    lines = [
        "# KJVA Apocrypha Bridge Term Review",
        "",
        "Status: term-level review aid. This is not a claim report.",
        "",
        "This report ranks KJVA apocrypha/deuterocanon bridge terms by observed",
        "bridge rows, same-length non-Bible term-control counts, and surface-context",
        "buckets. The 250-sample shuffled-insertion control is total-level, not",
        "term-level, so it is cited as background calibration. The separate",
        f"{term_shuffled_label} shuffled control is summarized below as",
        "post-screen per-term calibration.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Summary",
        "",
        f"- bridge terms reviewed: {len(rows)}",
        f"- terms above all same-length non-Bible term controls: {gt_controls}",
        f"- terms with any center/span context bucket beyond hidden_path_only: {any_context}",
    ]
    if shuffled:
        lines.extend(
            [
                f"- 250-sample shuffled total rows: observed {shuffled.get('observed_bridge_rows', '')}; "
                f"shuffled min/mean/max {shuffled.get('sample_min', '')} / "
                f"{shuffled.get('sample_mean', '')} / {shuffled.get('sample_max', '')}; "
                f"p_ge {shuffled.get('p_ge', '')}",
            ]
        )
    if term_shuffled:
        lines.extend(
            [
                f"- {term_shuffled_label} shuffled controls: "
                f"{term_shuffled.get('observed_gt_sample_max', '')} of "
                f"{term_shuffled.get('terms', '')} terms above every shuffled sample; "
                f"{term_shuffled.get('p_le_0_05', '')} terms with unadjusted p_ge <= 0.05; "
                f"{term_shuffled.get('q_le_0_05', '')} terms with BH q_ge <= 0.05",
            ]
        )
    lines.extend(
        [
            "",
            "## Top Terms",
            "",
            "| Rank | Term | Concept | Observed | Control max | Delta | Context hits | Sample refs |",
            "| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows[:50]:
        context_hits = sum(int(row[bucket]) for bucket in CONTEXT_BUCKETS[:-1])
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["rank"]),
                    f"`{row['normalized_term']}`",
                    str(row["concepts"]),
                    str(row["observed_bridge_rows"]),
                    str(row["control_max_bridge_rows"]),
                    str(row["observed_minus_control_max"]),
                    str(context_hits),
                    str(row["sample_refs"]).replace("|", "\\|"),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- `observed_gt_all_controls` means the term count is above Shakespeare, War",
            "  and Peace, and Moby-Dick replacement-block term counts.",
            "- Context buckets mark occurrence and review priority; they do not by",
            "  themselves establish statistical significance.",
            "- Bridge terms are still post-screen candidates unless a narrower",
            "  prospective term list and term-level controls are locked before running.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    rows: list[dict[str, object]],
    shuffled: dict[str, str],
    term_shuffled: dict[str, object],
    args: argparse.Namespace,
    started: float,
) -> None:
    payload = {
        "tool": "summarize_kjv_apocrypha_bridge_terms",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "args": manifest_args(args),
        "term_rows": len(rows),
        "terms_above_all_controls": sum(1 for row in rows if row["observed_gt_all_controls"] == "True"),
        "shuffled_summary": shuffled,
        "term_shuffled_summary": term_shuffled,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def manifest_args(args: argparse.Namespace) -> dict[str, object]:
    return {key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()}


def reproduce_command(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.summarize_kjv_apocrypha_bridge_terms "
        f"--candidates {args.candidates} "
        f"--context {args.context} "
        f"--controls {args.controls} "
        f"--shuffled-summary {args.shuffled_summary} "
        f"--term-shuffled-summary {args.term_shuffled_summary} "
        f"--out {args.out} "
        f"--markdown-out {args.markdown_out} "
        f"--manifest-out {args.manifest_out}"
    )


def git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


if __name__ == "__main__":
    raise SystemExit(main())
