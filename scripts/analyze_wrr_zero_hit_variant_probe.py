#!/usr/bin/env python3
"""Probe simple variants for WRR imported terms with zero Genesis hits."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import load_corpus
from els.search import count_els_terms_by_lanes


DEFAULT_CONFIG = Path("configs/example_koren_genesis.toml")
DEFAULT_COUNTS = Path("reports/wrr_1994/wrr2_genesis_counts.csv")
DEFAULT_ROW_OCR = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_zero_hit_variant_probe.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/wrr_zero_hit_variant_probe_summary.csv")
DEFAULT_MD = Path("docs/WRR_ZERO_HIT_VARIANT_PROBE.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_zero_hit_variant_probe.manifest.json")

DETAIL_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "smoke_hit_count",
    "row_ocr_status",
    "variant_rule",
    "variant_normalized",
    "variant_length",
    "variant_hit_count",
    "max_skip",
    "read",
]

SUMMARY_FIELDNAMES = [
    "category",
    "zero_terms",
    "terms_with_variant_hit",
    "terms_without_variant_hit",
    "best_variant_total_hits",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    counts_rows = read_rows(args.counts)
    row_ocr_rows = keyed_rows(read_rows(args.row_ocr), "term_id") if args.row_ocr.exists() else {}
    zero_rows = selected_zero_rows(counts_rows, args.category)
    variants_by_term = {row["term_id"]: generate_variants(row["normalized_term"]) for row in zero_rows}
    variant_queries = sorted({variant for variants in variants_by_term.values() for _, variant in variants})
    corpus = load_corpus(args.config)
    counts = count_els_terms_by_lanes(
        corpus.text,
        variant_queries,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.jobs,
    )
    detail_rows = detail_output_rows(
        zero_rows,
        row_ocr_rows,
        variants_by_term,
        counts,
        max_skip=args.max_skip,
        top_variants=args.top_variants,
    )
    summary_rows = summary_output_rows(zero_rows, detail_rows)
    write_csv(args.out, DETAIL_FIELDNAMES, detail_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, summary_rows, detail_rows, args)
    write_manifest(args.manifest_out, args, zero_rows, detail_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--counts", type=Path, default=DEFAULT_COUNTS)
    parser.add_argument("--row-ocr", type=Path, default=DEFAULT_ROW_OCR)
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=1000)
    parser.add_argument("--direction", choices=("forward", "backward", "both"), default="both")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--top-variants", type=int, default=3)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def selected_zero_rows(
    rows: list[dict[str, str]],
    categories: list[str],
) -> list[dict[str, str]]:
    selected_categories = set(categories)
    out = []
    for row in rows:
        if selected_categories and row.get("category", "") not in selected_categories:
            continue
        if row.get("status") != "counted":
            continue
        if int_or_zero(row.get("hit_count", "")) != 0:
            continue
        if not row.get("normalized_term", ""):
            continue
        out.append(row)
    return sorted(out, key=lambda row: (row.get("category", ""), row.get("term_id", "")))


def generate_variants(normalized: str) -> list[tuple[str, str]]:
    variants: dict[str, str] = {"original": normalized}
    for index, char in enumerate(normalized):
        deleted = normalized[:index] + normalized[index + 1 :]
        if len(deleted) >= 3:
            rule = "delete_mater" if char in {"W", "Y"} else "delete_one"
            variants.setdefault(f"{rule}@{index + 1}", deleted)
        if char == ")":
            variants.setdefault(f"swap_aleph_ayin@{index + 1}", replace_at(normalized, index, "("))
        elif char == "(":
            variants.setdefault(f"swap_ayin_aleph@{index + 1}", replace_at(normalized, index, ")"))
    return [(rule, variant) for rule, variant in variants.items()]


def replace_at(value: str, index: int, char: str) -> str:
    return value[:index] + char + value[index + 1 :]


def detail_output_rows(
    zero_rows: list[dict[str, str]],
    row_ocr_rows: dict[str, dict[str, str]],
    variants_by_term: dict[str, list[tuple[str, str]]],
    counts: dict[str, int],
    *,
    max_skip: int,
    top_variants: int,
) -> list[dict[str, object]]:
    out = []
    for row in zero_rows:
        term_id = row["term_id"]
        variants = variants_by_term[term_id]
        ranked = sorted(
            (
                (rule, variant, counts.get(variant, 0))
                for rule, variant in variants
                if counts.get(variant, 0) > 0
            ),
            key=lambda item: (-item[2], item[0], item[1]),
        )[:top_variants]
        if not ranked:
            ranked = [("none_found", row["normalized_term"], 0)]
        for rule, variant, hit_count in ranked:
            out.append(detail_row(row, row_ocr_rows, rule, variant, hit_count, max_skip))
    return out


def detail_row(
    row: dict[str, str],
    row_ocr_rows: dict[str, dict[str, str]],
    rule: str,
    variant: str,
    hit_count: int,
    max_skip: int,
) -> dict[str, object]:
    status = row_ocr_rows.get(row["term_id"], {}).get("row_ocr_status", "") or "missing"
    read = "variant has raw ELS hits; source transcription still not changed"
    if rule == "original":
        read = "original term has raw ELS hits at the wider diagnostic cap"
    elif rule == "none_found":
        read = "no simple one-edit variant produced raw ELS hits"
    return {
        "term_id": row["term_id"],
        "concept": row.get("concept", ""),
        "category": row.get("category", ""),
        "term": row.get("term", ""),
        "normalized_term": row.get("normalized_term", ""),
        "smoke_hit_count": row.get("hit_count", ""),
        "row_ocr_status": status,
        "variant_rule": rule,
        "variant_normalized": variant,
        "variant_length": len(variant),
        "variant_hit_count": hit_count,
        "max_skip": max_skip,
        "read": read,
    }


def summary_output_rows(
    zero_rows: list[dict[str, str]],
    detail_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    zero_by_category: Counter[str] = Counter(row.get("category", "") for row in zero_rows)
    hits_by_category: defaultdict[str, set[str]] = defaultdict(set)
    hit_totals: Counter[str] = Counter()
    for row in detail_rows:
        category = str(row["category"])
        if int(row["variant_hit_count"]) <= 0:
            continue
        hits_by_category[category].add(str(row["term_id"]))
        hit_totals[category] += int(row["variant_hit_count"])
    out = []
    for category, zero_count in sorted(zero_by_category.items()):
        with_hit = len(hits_by_category[category])
        out.append(
            {
                "category": category,
                "zero_terms": zero_count,
                "terms_with_variant_hit": with_hit,
                "terms_without_variant_hit": zero_count - with_hit,
                "best_variant_total_hits": hit_totals[category],
            }
        )
    return out


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    detail_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    top_rows = sorted(
        [row for row in detail_rows if int(row["variant_hit_count"]) > 0],
        key=lambda row: (-int(row["variant_hit_count"]), str(row["term_id"]), str(row["variant_rule"])),
    )[:12]
    lines = [
        "# WRR Zero-Hit Variant Probe",
        "",
        "Status: diagnostic-only one-edit probe for imported WRR2 terms with zero",
        "Genesis hits in the count smoke run. It is not a source correction and",
        "not a WRR reproduction.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_zero_hit_variant_probe "
            f"--config {args.config} "
            f"--counts {args.counts} "
            f"--row-ocr {args.row_ocr} "
            f"--min-skip {args.min_skip} "
            f"--max-skip {args.max_skip} "
            f"--direction {args.direction} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        "| Category | Zero terms | With variant hit | Without variant hit | Variant hit total |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            "| {category} | {zero_terms} | {terms_with_variant_hit} | "
            "{terms_without_variant_hit} | {best_variant_total_hits} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Top Variant Hits",
            "",
            "| Term id | Concept | Rule | Original | Variant | Row OCR | Hits |",
            "| --- | --- | --- | --- | --- | --- | ---: |",
        ]
    )
    for row in top_rows:
        lines.append(
            "| `{term_id}` | `{concept}` | `{variant_rule}` | `{normalized_term}` | "
            "`{variant_normalized}` | `{row_ocr_status}` | {variant_hit_count} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Variant hits are leads for source-normalization review only.",
            "- A hit here does not authorize replacing a WRR term or promoting a claim.",
            "- Rows with row OCR matched but zero original hits remain source-rule",
            "  and normalization questions before any permutation question.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    zero_rows: list[dict[str, str]],
    detail_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": "analyze_wrr_zero_hit_variant_probe",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "config": str(args.config),
            "counts": str(args.counts),
            "row_ocr": str(args.row_ocr),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "zero_terms": len(zero_rows),
        "detail_rows": len(detail_rows),
        "summary_rows": len(summary_rows),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def keyed_rows(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows if row.get(key)}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def int_or_zero(value: str) -> int:
    if value in ("", None):
        return 0
    return int(float(value))


if __name__ == "__main__":
    raise SystemExit(main())
