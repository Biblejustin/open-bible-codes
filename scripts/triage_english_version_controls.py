#!/usr/bin/env python3
"""Compare English target-version hits against merged open control corpora."""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path


DEFAULT_TARGET_PRESENCE = Path("reports/biblegateway_english_versions/version_presence.csv")
DEFAULT_CONTROL_PRESENCE = [
    Path("reports/ebible_english_controls/version_presence.csv"),
    Path("reports/door43_english_controls/version_presence.csv"),
    Path("reports/oet_english_controls/version_presence.csv"),
    Path("reports/otb_english_controls/version_presence.csv"),
    Path("reports/openbible_english_controls/version_presence.csv"),
    Path("reports/odr_english_controls/version_presence.csv"),
]
DEFAULT_TARGET_VERSIONS = Path("reports/biblegateway_english_versions/included_versions.csv")
DEFAULT_CONTROL_VERSIONS = [
    Path("reports/ebible_english_controls/included_versions.csv"),
    Path("reports/door43_english_controls/included_versions.csv"),
    Path("reports/oet_english_controls/included_versions.csv"),
    Path("reports/otb_english_controls/included_versions.csv"),
    Path("reports/openbible_english_controls/included_versions.csv"),
    Path("reports/odr_english_controls/included_versions.csv"),
]
DEFAULT_OUT_DIR = Path("reports/english_version_control_triage")

FIELDNAMES = [
    "term_set",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "normalized_length",
    "triage_flag",
    "score",
    "target_presence_scope",
    "target_present_count",
    "target_observed_count",
    "target_present_rate",
    "target_total_hits",
    "target_max_corpus",
    "target_present_corpora",
    "target_only_present_count",
    "target_only_present_corpora",
    "target_present_full",
    "target_present_nt",
    "target_present_ot",
    "target_present_partial",
    "control_presence_scope",
    "control_present_count",
    "control_observed_count",
    "control_present_rate",
    "control_total_hits",
    "control_max_corpus",
    "control_present_corpora",
    "control_present_full",
    "control_present_nt",
    "control_present_ot",
    "control_present_partial",
    "target_minus_control_rate",
    "read",
]

TOP_TERMS_FIELDNAMES = ["term_id", "concept", "category", "language", "term", "notes"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    control_presence_paths = args.control_presence or DEFAULT_CONTROL_PRESENCE
    control_version_paths = args.control_versions or DEFAULT_CONTROL_VERSIONS
    target_rows = read_keyed_rows(args.target_presence)
    control_rows = read_merged_keyed_rows(control_presence_paths)
    target_versions = read_versions(args.target_versions)
    control_versions = read_merged_versions(control_version_paths)
    triage_rows = build_triage_rows(
        target_rows,
        control_rows,
        target_versions,
        control_versions,
        args,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    write_rows(args.out, triage_rows, FIELDNAMES)
    top_terms = select_context_terms(triage_rows, args.context_term_count)
    write_top_terms(args.terms_out, top_terms)
    write_markdown(
        args.markdown_out,
        triage_rows,
        top_terms,
        target_versions,
        control_versions,
        args,
    )
    write_manifest(args, triage_rows, top_terms, started)
    print(args.out)
    print(args.markdown_out)
    print(args.terms_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-presence", type=Path, default=DEFAULT_TARGET_PRESENCE)
    parser.add_argument("--control-presence", type=Path, action="append", default=[])
    parser.add_argument("--target-versions", type=Path, default=DEFAULT_TARGET_VERSIONS)
    parser.add_argument("--control-versions", type=Path, action="append", default=[])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR / "triage.csv")
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_OUT_DIR / "triage.md")
    parser.add_argument("--terms-out", type=Path, default=DEFAULT_OUT_DIR / "context_seed_terms.csv")
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_OUT_DIR / "triage.manifest.json")
    parser.add_argument("--min-length", type=int, default=4)
    parser.add_argument("--rare-control-count", type=int, default=2)
    parser.add_argument("--rare-control-rate", type=float, default=0.10)
    parser.add_argument("--context-term-count", type=int, default=12)
    return parser


def read_keyed_rows(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["term_id"]: dict(row) for row in csv.DictReader(handle)}


def read_merged_keyed_rows(paths: list[Path]) -> dict[str, dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                grouped.setdefault(row["term_id"], []).append(dict(row))
    return {term_id: merge_presence_rows(rows) for term_id, rows in grouped.items()}


def merge_presence_rows(rows: list[dict[str, str]]) -> dict[str, str]:
    base = dict(rows[0])
    observed = unique_ordered(
        corpus
        for row in rows
        for corpus in parse_corpora(row.get("observed_corpora", ""))
    )
    present = unique_ordered(
        corpus
        for row in rows
        for corpus in parse_corpora(row.get("present_corpora", ""))
    )
    present_set = set(present)
    absent = [corpus for corpus in observed if corpus not in present_set]
    hit_counts = {}
    for row in rows:
        hit_counts.update(parse_hit_counts(row.get("hit_counts_by_corpus", "")))
    max_corpus = ""
    max_hit_count = 0
    if hit_counts:
        max_corpus, max_hit_count = max(hit_counts.items(), key=lambda item: item[1])
    base.update(
        {
            "observed_corpora": ",".join(observed),
            "observed_corpus_count": str(len(observed)),
            "present_corpora": ",".join(present),
            "absent_corpora": ",".join(absent),
            "presence_scope": merged_presence_scope(len(present), len(observed)),
            "total_hits": str(sum(hit_counts.values())),
            "max_hit_count": str(max_hit_count),
            "max_corpus": max_corpus,
            "hit_counts_by_corpus": "; ".join(
                f"{corpus}:{hit_counts[corpus]}" for corpus in observed if corpus in hit_counts
            ),
        }
    )
    return base


def read_versions(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["label"]: dict(row) for row in csv.DictReader(handle)}


def read_merged_versions(paths: list[Path]) -> dict[str, dict[str, str]]:
    versions: dict[str, dict[str, str]] = {}
    for path in paths:
        versions.update(read_versions(path))
    return versions


def build_triage_rows(
    target_rows: dict[str, dict[str, str]],
    control_rows: dict[str, dict[str, str]],
    target_versions: dict[str, dict[str, str]],
    control_versions: dict[str, dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    rows = []
    for term_id, target in target_rows.items():
        control = control_rows.get(term_id, empty_control_row(target))
        target_present = parse_corpora(target.get("present_corpora", ""))
        control_present = parse_corpora(control.get("present_corpora", ""))
        target_only_present = [
            corpus for corpus in target_present if corpus not in set(control_present)
        ]
        target_observed = int_value(target.get("observed_corpus_count"))
        control_observed = int_value(control.get("observed_corpus_count"))
        target_rate = rate(len(target_present), target_observed)
        control_rate = rate(len(control_present), control_observed)
        delta = target_rate - control_rate
        length = int_value(target.get("normalized_length"))
        flag = triage_flag(
            length=length,
            target_present_count=len(target_present),
            target_observed_count=target_observed,
            control_present_count=len(control_present),
            control_present_rate=control_rate,
            delta=delta,
            args=args,
        )
        score = triage_score(
            length=length,
            target_present_count=len(target_present),
            target_rate=target_rate,
            target_only_present_count=len(target_only_present),
            control_present_count=len(control_present),
            control_rate=control_rate,
            delta=delta,
        )
        row = {
            "term_set": target.get("term_set", ""),
            "term_id": term_id,
            "concept": target.get("concept", ""),
            "category": target.get("category", ""),
            "normalized_term": target.get("normalized_term", ""),
            "normalized_length": length,
            "triage_flag": flag,
            "score": f"{score:.4f}",
            "target_presence_scope": target.get("presence_scope", ""),
            "target_present_count": len(target_present),
            "target_observed_count": target_observed,
            "target_present_rate": f"{target_rate:.4f}",
            "target_total_hits": int_value(target.get("total_hits")),
            "target_max_corpus": target.get("max_corpus", ""),
            "target_present_corpora": ",".join(target_present),
            "target_only_present_count": len(target_only_present),
            "target_only_present_corpora": ",".join(target_only_present),
            "target_present_full": coverage_labels(target_present, target_versions, {"full", "with_apocrypha"}),
            "target_present_nt": coverage_labels(target_present, target_versions, {"nt"}),
            "target_present_ot": coverage_labels(
                target_present,
                target_versions,
                {"ot", "ot_apocrypha", "torah"},
            ),
            "target_present_partial": coverage_labels(target_present, target_versions, {"partial"}),
            "control_presence_scope": control.get("presence_scope", ""),
            "control_present_count": len(control_present),
            "control_observed_count": control_observed,
            "control_present_rate": f"{control_rate:.4f}",
            "control_total_hits": int_value(control.get("total_hits")),
            "control_max_corpus": control.get("max_corpus", ""),
            "control_present_corpora": ",".join(control_present),
            "control_present_full": coverage_labels(control_present, control_versions, {"full", "with_apocrypha"}),
            "control_present_nt": coverage_labels(control_present, control_versions, {"nt"}),
            "control_present_ot": coverage_labels(
                control_present,
                control_versions,
                {"ot", "ot_apocrypha", "torah"},
            ),
            "control_present_partial": coverage_labels(control_present, control_versions, {"partial"}),
            "target_minus_control_rate": f"{delta:.4f}",
            "read": read_label(flag, length, len(target_present), len(control_present)),
        }
        rows.append(row)
    return sorted(rows, key=triage_sort_key)


def empty_control_row(target: dict[str, str]) -> dict[str, str]:
    return {
        "presence_scope": "missing_from_control_report",
        "present_corpora": "",
        "observed_corpus_count": "0",
        "total_hits": "0",
        "max_corpus": "",
        "normalized_length": target.get("normalized_length", "0"),
    }


def parse_corpora(value: str) -> list[str]:
    return [item for item in value.split(",") if item]


def parse_hit_counts(value: str) -> dict[str, int]:
    counts = {}
    for item in value.split(";"):
        if ":" not in item:
            continue
        label, raw_count = item.split(":", 1)
        counts[label.strip()] = int_value(raw_count.strip())
    return counts


def unique_ordered(values: object) -> list[str]:
    seen = set()
    ordered = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def merged_presence_scope(present_count: int, observed_count: int) -> str:
    if observed_count <= 0 or present_count <= 0:
        return "absent_all_observed_sources"
    if present_count == observed_count:
        return "present_all_observed_sources"
    return "source_specific"


def int_value(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def triage_flag(
    *,
    length: int,
    target_present_count: int,
    target_observed_count: int,
    control_present_count: int,
    control_present_rate: float,
    delta: float,
    args: argparse.Namespace,
) -> str:
    if target_present_count == 0:
        return "no_target_hits"
    if length < args.min_length:
        return "hold_short_term"
    target_multi_floor = max(2, math.ceil(target_observed_count * 0.15))
    if control_present_count == 0 and target_present_count >= target_multi_floor:
        return "target_multi_control_absent"
    if control_present_count == 0:
        return "source_specific_control_absent"
    if (
        control_present_count <= args.rare_control_count
        or control_present_rate <= args.rare_control_rate
    ) and delta > 0:
        return "target_control_rare"
    if delta >= 0.20:
        return "target_skewed"
    if delta <= -0.20:
        return "control_heavier"
    return "broad_or_noisy"


def triage_score(
    *,
    length: int,
    target_present_count: int,
    target_rate: float,
    target_only_present_count: int,
    control_present_count: int,
    control_rate: float,
    delta: float,
) -> float:
    score = delta
    score += min(length, 12) * 0.01
    score += min(target_present_count, 6) * 0.015
    score += min(target_only_present_count, 4) * 0.04
    if control_present_count == 0:
        score += 0.30
    elif control_present_count <= 2:
        score += 0.18
    if target_rate >= 0.15 and control_rate <= 0.10:
        score += 0.12
    return score


def coverage_labels(
    labels: list[str],
    versions: dict[str, dict[str, str]],
    coverage_values: set[str],
) -> str:
    return ",".join(
        label
        for label in labels
        if versions.get(label, {}).get("coverage", "") in coverage_values
    )


def read_label(flag: str, length: int, target_present: int, control_present: int) -> str:
    if flag == "hold_short_term":
        return "short term; likely high-noise"
    if flag == "target_multi_control_absent":
        return "target multi-source hit; absent in controls"
    if flag == "source_specific_control_absent":
        return "single target-source hit; absent in controls"
    if flag == "target_control_rare":
        return "target hit with rare control support"
    if flag == "target_skewed":
        return "target rate higher than control rate"
    if flag == "control_heavier":
        return "control rate higher than target rate"
    if target_present and control_present:
        return "broad hit; needs stronger filter"
    return "no target hit"


def triage_sort_key(row: dict[str, object]) -> tuple[int, float, int, int, str]:
    flag_order = {
        "target_multi_control_absent": 0,
        "source_specific_control_absent": 1,
        "target_control_rare": 2,
        "target_skewed": 3,
        "broad_or_noisy": 4,
        "control_heavier": 5,
        "hold_short_term": 6,
        "no_target_hits": 7,
    }
    return (
        flag_order.get(str(row["triage_flag"]), 9),
        -float(row["score"]),
        -int(row["normalized_length"]),
        int(row["control_present_count"]),
        str(row["term_id"]),
    )


def select_context_terms(rows: list[dict[str, object]], limit: int) -> list[dict[str, object]]:
    selected = []
    seen_terms = set()
    preferred = {
        "target_multi_control_absent",
        "target_control_rare",
        "source_specific_control_absent",
        "target_skewed",
    }
    for row in rows:
        if str(row["triage_flag"]) not in preferred:
            continue
        if (
            str(row["triage_flag"]) != "source_specific_control_absent"
            and int(row.get("target_only_present_count", 0)) == 0
        ):
            continue
        normalized = str(row["normalized_term"])
        if normalized in seen_terms:
            continue
        seen_terms.add(normalized)
        selected.append(row)
        if len(selected) >= limit:
            break
    return selected


def write_rows(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_top_terms(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TOP_TERMS_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "term_id": row["term_id"],
                    "concept": row["concept"],
                    "category": row["category"],
                    "language": "english",
                    "term": row["concept"] or row["normalized_term"],
                    "notes": f"triage_flag={row['triage_flag']}; score={row['score']}",
                }
            )


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    top_terms: list[dict[str, object]],
    target_versions: dict[str, dict[str, str]],
    control_versions: dict[str, dict[str, str]],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flag_counts = Counter(str(row["triage_flag"]) for row in rows)
    lines = [
        "# English Version Control Triage",
        "",
        "This report compares the available BibleGateway-overlap English versions",
        "against the merged open/CC English control set. It is a triage report,",
        "not a statistical claim.",
        "",
        "## Inputs",
        "",
        f"- Target presence: `{args.target_presence}`",
        f"- Control presence: `{', '.join(str(path) for path in (args.control_presence or DEFAULT_CONTROL_PRESENCE))}`",
        f"- Target versions: {len(target_versions)}",
        f"- Control versions: {len(control_versions)}",
        "",
        "## Corpus Coverage",
        "",
        coverage_table("Target", target_versions),
        "",
        coverage_table("Control", control_versions),
        "",
        "## Triage Counts",
        "",
        "| Flag | Terms |",
        "| --- | ---: |",
    ]
    for flag, count in sorted(flag_counts.items()):
        lines.append(f"| `{flag}` | {count} |")
    lines.extend(
        [
            "",
            "## Strongest Rows",
            "",
            "| Term | Flag | Target | Control | Delta | Score | Read |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows[:40]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['term_id']}` {row['concept']} (`{row['normalized_term']}`)",
                    f"`{row['triage_flag']}`",
                    f"{row['target_present_count']}/{row['target_observed_count']}",
                    f"{row['control_present_count']}/{row['control_observed_count']}",
                    str(row["target_minus_control_rate"]),
                    str(row["score"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Context Seed Terms",
            "",
            f"Seed term file: `{args.terms_out}`",
            "",
            "| Term | Flag | Target Corpora | Control Corpora |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in top_terms:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['term_id']}` {row['concept']} (`{row['normalized_term']}`)",
                    f"`{row['triage_flag']}`",
                    str(row["target_present_corpora"]),
                    str(row["control_present_corpora"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Cautions",
            "",
            "- Short terms are held even when they have high hit counts.",
            "- Partial corpora can create false absence. Check coverage fields before",
            "  interpreting an absence.",
            "- A target-skewed row is only a queue item for context review.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def coverage_table(title: str, versions: dict[str, dict[str, str]]) -> str:
    counts = Counter(row.get("coverage", "") or "unknown" for row in versions.values())
    lines = [
        f"### {title}",
        "",
        "| Coverage | Count | Labels |",
        "| --- | ---: | --- |",
    ]
    for coverage, count in sorted(counts.items()):
        labels = ",".join(
            label
            for label, row in sorted(versions.items())
            if (row.get("coverage", "") or "unknown") == coverage
        )
        lines.append(f"| `{coverage}` | {count} | {labels} |")
    return "\n".join(lines)


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    top_terms: list[dict[str, object]],
    started: float,
) -> None:
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "tool": "triage_english_version_controls",
        "created_utc": datetime.now(UTC).isoformat(),
        "target_presence": str(args.target_presence.resolve()),
        "control_presence": [str(path.resolve()) for path in (args.control_presence or DEFAULT_CONTROL_PRESENCE)],
        "target_versions": str(args.target_versions.resolve()),
        "control_versions": [str(path.resolve()) for path in (args.control_versions or DEFAULT_CONTROL_VERSIONS)],
        "rows": len(rows),
        "context_seed_terms": len(top_terms),
        "seconds": round(time.perf_counter() - started, 3),
        "outputs": [str(args.out), str(args.markdown_out), str(args.terms_out)],
    }
    args.manifest_out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
