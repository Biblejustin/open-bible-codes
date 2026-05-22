#!/usr/bin/env python3
"""Build a WRR source-review queue from blocked pairs and variant leads."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_BLOCKED_PAIRS = Path("reports/wrr_1994/wrr_defined_gap_blocked_pairs.csv")
DEFAULT_VARIANTS = Path("reports/wrr_1994/wrr_zero_hit_variant_probe.csv")
DEFAULT_ROW_OCR = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/wrr_source_review_queue_summary.csv")
DEFAULT_MD = Path("docs/WRR_SOURCE_REVIEW_QUEUE.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_source_review_queue.manifest.json")

BEST_RUN_ORDER = ("all_lanes_cap1000", "all_lanes_cap1000_program", "all_lanes_cap250")

REASON_APP = "ordinary_missing_appellation_hits"
REASON_DATE = "ordinary_missing_date_hits"
REASON_BOTH = "ordinary_missing_both_terms"

QUEUE_FIELDNAMES = [
    "run_label",
    "priority_rank",
    "review_bucket",
    "term_side",
    "term_id",
    "term",
    "normalized",
    "concepts",
    "row_numbers",
    "row_ocr_status",
    "row_ocr_column",
    "row_ocr_match_basis",
    "row_ocr_text_normalized",
    "blocking_pairs",
    "blocking_reasons",
    "best_variant_hit_count",
    "best_variant_rule",
    "best_variant_normalized",
    "pair_ids",
    "read",
]

SUMMARY_FIELDNAMES = [
    "run_label",
    "review_bucket",
    "terms",
    "blocking_pairs",
    "variant_hit_total",
    "row_ocr_statuses",
]

BUCKET_READS = {
    "ocr_not_matched_with_variant_lead": (
        "OCR did not match imported term and a simple variant has Genesis hits; "
        "check source transcription first"
    ),
    "ocr_matched_with_variant_lead": (
        "OCR matched imported term and a simple variant has Genesis hits; "
        "check normalization/rule assumptions without changing source text"
    ),
    "ocr_not_matched_no_variant_lead": (
        "OCR did not match imported term and no simple variant lead exists; "
        "check source transcription or row alignment"
    ),
    "ocr_matched_no_variant_lead": (
        "OCR matched imported term but no simple variant lead exists; likely "
        "method/pair-universe blocker, not quick source correction"
    ),
    "ocr_unknown_with_variant_lead": (
        "Row OCR status is unknown and a simple variant has Genesis hits; "
        "check source row and normalization"
    ),
    "ocr_unknown_no_variant_lead": (
        "Row OCR status is unknown and no simple variant lead exists; check "
        "source row before deeper method work"
    ),
}

BUCKET_ORDER = {
    "ocr_not_matched_with_variant_lead": 0,
    "ocr_matched_with_variant_lead": 1,
    "ocr_not_matched_no_variant_lead": 2,
    "ocr_unknown_with_variant_lead": 3,
    "ocr_matched_no_variant_lead": 4,
    "ocr_unknown_no_variant_lead": 5,
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    blocked_rows = read_rows(args.blocked_pairs)
    variant_rows = read_rows(args.variants)
    row_ocr_rows = keyed_rows(read_rows(args.row_ocr), "term_id") if args.row_ocr.exists() else {}
    run_label = args.run_label or best_run_label(blocked_rows)
    queue_rows = build_queue_rows(blocked_rows, best_variants_by_term(variant_rows), row_ocr_rows, run_label)
    summary_rows = build_summary_rows(queue_rows)
    write_csv(args.out, QUEUE_FIELDNAMES, queue_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, queue_rows, summary_rows, args, run_label)
    write_manifest(args.manifest_out, args, run_label, queue_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocked-pairs", type=Path, default=DEFAULT_BLOCKED_PAIRS)
    parser.add_argument("--variants", type=Path, default=DEFAULT_VARIANTS)
    parser.add_argument("--row-ocr", type=Path, default=DEFAULT_ROW_OCR)
    parser.add_argument("--run-label", default="")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def best_run_label(rows: list[dict[str, str]]) -> str:
    labels = {row.get("run_label", "") for row in rows}
    for label in BEST_RUN_ORDER:
        if label in labels:
            return label
    return sorted(labels)[-1] if labels else ""


def best_variants_by_term(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if int_or_zero(row.get("variant_hit_count", "")) <= 0:
            continue
        grouped[row.get("term_id", "")].append(row)
    return {
        term_id: sorted(
            term_rows,
            key=lambda row: (
                -int_or_zero(row.get("variant_hit_count", "")),
                row.get("variant_rule", ""),
                row.get("variant_normalized", ""),
            ),
        )
        for term_id, term_rows in grouped.items()
    }


def build_queue_rows(
    blocked_rows: list[dict[str, str]],
    variant_index: dict[str, list[dict[str, str]]],
    row_ocr_rows: dict[str, dict[str, str]],
    run_label: str,
) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, object]] = {}
    for row in blocked_rows:
        if row.get("run_label", "") != run_label:
            continue
        for side, term_id, term, normalized in blocking_terms(row):
            item = grouped.setdefault(
                term_id,
                {
                    "run_label": run_label,
                    "term_side": side,
                    "term_id": term_id,
                    "term": term,
                    "normalized": normalized,
                    "concepts": set(),
                    "pair_ids": set(),
                    "blocking_reasons": Counter(),
                },
            )
            cast_set(item["concepts"]).add(row.get("concept", ""))
            cast_set(item["pair_ids"]).add(row.get("pair_id", ""))
            cast_counter(item["blocking_reasons"])[row.get("reason", "")] += 1

    out = []
    for term_id, item in grouped.items():
        ocr = row_ocr_rows.get(term_id, {})
        variants = variant_index.get(term_id, [])
        best_variant = variants[0] if variants else {}
        best_hits = int_or_zero(best_variant.get("variant_hit_count", ""))
        ocr_status = ocr.get("row_ocr_status", "unknown") or "unknown"
        bucket = review_bucket(ocr_status, best_hits)
        pair_ids = sorted(cast_set(item["pair_ids"]))
        concepts = sorted(cast_set(item["concepts"]))
        reasons = cast_counter(item["blocking_reasons"])
        out.append(
            {
                "run_label": run_label,
                "priority_rank": 0,
                "review_bucket": bucket,
                "term_side": item["term_side"],
                "term_id": term_id,
                "term": item["term"],
                "normalized": item["normalized"],
                "concepts": ";".join(concepts),
                "row_numbers": ocr.get("row_number", ""),
                "row_ocr_status": ocr_status,
                "row_ocr_column": ocr.get("column", ""),
                "row_ocr_match_basis": ocr.get("match_basis", ""),
                "row_ocr_text_normalized": ocr.get("row_ocr_text_normalized", ""),
                "blocking_pairs": len(pair_ids),
                "blocking_reasons": format_counter(reasons),
                "best_variant_hit_count": best_hits,
                "best_variant_rule": best_variant.get("variant_rule", "none"),
                "best_variant_normalized": best_variant.get("variant_normalized", ""),
                "pair_ids": ";".join(pair_ids),
                "read": BUCKET_READS[bucket],
            }
        )
    out.sort(key=queue_sort_key)
    for index, row in enumerate(out, start=1):
        row["priority_rank"] = index
    return out


def blocking_terms(row: dict[str, str]) -> list[tuple[str, str, str, str]]:
    reason = row.get("reason", "")
    blockers: list[tuple[str, str, str, str]] = []
    if reason in {REASON_APP, REASON_BOTH}:
        blockers.append(
            (
                "appellation",
                row.get("appellation_term_id", ""),
                row.get("appellation_term", ""),
                row.get("appellation_normalized", ""),
            )
        )
    if reason in {REASON_DATE, REASON_BOTH}:
        blockers.append(
            (
                "date",
                row.get("date_term_id", ""),
                row.get("date_term", ""),
                row.get("date_normalized", ""),
            )
        )
    return [(side, term_id, term, normalized) for side, term_id, term, normalized in blockers if term_id]


def review_bucket(row_ocr_status: str, best_variant_hit_count: int) -> str:
    has_variant = best_variant_hit_count > 0
    if row_ocr_status == "not_matched":
        return "ocr_not_matched_with_variant_lead" if has_variant else "ocr_not_matched_no_variant_lead"
    if row_ocr_status == "matched":
        return "ocr_matched_with_variant_lead" if has_variant else "ocr_matched_no_variant_lead"
    return "ocr_unknown_with_variant_lead" if has_variant else "ocr_unknown_no_variant_lead"


def queue_sort_key(row: dict[str, object]) -> tuple[int, int, int, str]:
    return (
        BUCKET_ORDER.get(str(row["review_bucket"]), 99),
        -int(row["blocking_pairs"]),
        -int(row["best_variant_hit_count"]),
        str(row["term_id"]),
    )


def build_summary_rows(queue_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in queue_rows:
        grouped[(str(row["run_label"]), str(row["review_bucket"]))].append(row)
    out = []
    for (run_label, bucket), rows in sorted(grouped.items(), key=lambda item: (item[0][0], BUCKET_ORDER.get(item[0][1], 99))):
        statuses = Counter(str(row["row_ocr_status"]) for row in rows)
        out.append(
            {
                "run_label": run_label,
                "review_bucket": bucket,
                "terms": len(rows),
                "blocking_pairs": sum(int(row["blocking_pairs"]) for row in rows),
                "variant_hit_total": sum(int(row["best_variant_hit_count"]) for row in rows),
                "row_ocr_statuses": format_counter(statuses),
            }
        )
    return out


def write_markdown(
    path: Path,
    queue_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
    run_label: str,
) -> None:
    lines = [
        "# WRR Source Review Queue",
        "",
        "Status: diagnostic-only source-review triage from current blocked",
        "WRR pair rows, row-aligned OCR probe output, and zero-hit one-edit",
        "variant leads. It is not a source correction, not a term replacement,",
        "and not a WRR reproduction.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_source_review_queue "
            f"--blocked-pairs {args.blocked_pairs} "
            f"--variants {args.variants} "
            f"--row-ocr {args.row_ocr} "
            f"--run-label {run_label} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Queue",
        "",
        f"- Run label: `{run_label}`.",
        f"- Terms queued: {len(queue_rows)}.",
        "",
        "| Bucket | Terms | Blocking pairs | Variant hit total | Row OCR statuses |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| `{review_bucket}` | {terms} | {blocking_pairs} | {variant_hit_total} | "
            "`{row_ocr_statuses}` |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Top Review Targets",
            "",
            "| Rank | Term id | Side | Term | Row OCR | Blocking pairs | Variant hits | Best variant | Read |",
            "| ---: | --- | --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in queue_rows[:20]:
        lines.append(
            "| {priority_rank} | `{term_id}` | `{term_side}` | `{term}` | `{row_ocr_status}` | "
            "{blocking_pairs} | {best_variant_hit_count} | `{best_variant_rule}:{best_variant_normalized}` | "
            "{read} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## OCR Context For Top Targets",
            "",
            "| Rank | Term id | Normalized term | Row OCR normalized text |",
            "| ---: | --- | --- | --- |",
        ]
    )
    for row in queue_rows[:12]:
        lines.append(
            "| {priority_rank} | `{term_id}` | `{normalized}` | `{row_ocr_text}` |".format(
                row_ocr_text=truncate_text(str(row.get("row_ocr_text_normalized", "")), 80),
                **row,
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Review queue ranks source-transcription and normalization checks.",
            "- Variant leads do not validate the original blocked pairs.",
            "- OCR matches are probe evidence only, not claim-grade primary transcription.",
            "- Locked source rows and pair rules are still required before reproduction language.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    run_label: str,
    queue_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": "build_wrr_source_review_queue",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "run_label": run_label,
        "inputs": {
            "blocked_pairs": str(args.blocked_pairs),
            "variants": str(args.variants),
            "row_ocr": str(args.row_ocr),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
        "queue_rows": len(queue_rows),
        "summary_rows": len(summary_rows),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def keyed_rows(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows if row.get(key, "")}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def cast_set(value: object) -> set[str]:
    if not isinstance(value, set):
        raise TypeError("expected set")
    return value


def cast_counter(value: object) -> Counter[str]:
    if not isinstance(value, Counter):
        raise TypeError("expected Counter")
    return value


def format_counter(counter: Counter[str]) -> str:
    return ", ".join(f"{counter[key]} {key}" for key in sorted(counter) if key)


def truncate_text(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def int_or_zero(value: str | None) -> int:
    if value in ("", None):
        return 0
    return int(float(value))


if __name__ == "__main__":
    raise SystemExit(main())
