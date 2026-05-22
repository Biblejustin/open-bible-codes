#!/usr/bin/env python3
"""Join WRR zero-hit variant leads to current blocked pair rows."""

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
DEFAULT_OUT = Path("reports/wrr_1994/wrr_variant_gap_impact.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/wrr_variant_gap_impact_summary.csv")
DEFAULT_MD = Path("docs/WRR_VARIANT_GAP_IMPACT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_variant_gap_impact.manifest.json")

DETAIL_FIELDNAMES = [
    "run_label",
    "pair_id",
    "concept",
    "reason",
    "row_ocr_pair_status",
    "impact_status",
    "blocking_term_ids",
    "blocking_terms",
    "blocking_term_variant_hits",
    "blocking_term_variant_rules",
    "read",
]

SUMMARY_FIELDNAMES = [
    "run_label",
    "impact_status",
    "pairs",
    "row_ocr_pair_statuses",
    "top_concepts",
]

REASON_APP = "ordinary_missing_appellation_hits"
REASON_DATE = "ordinary_missing_date_hits"
REASON_BOTH = "ordinary_missing_both_terms"


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    blocked_rows = read_rows(args.blocked_pairs)
    variant_rows = read_rows(args.variants)
    variant_index = best_variants_by_term(variant_rows)
    detail_rows = build_detail_rows(blocked_rows, variant_index)
    summary_rows = build_summary_rows(detail_rows)
    write_csv(args.out, DETAIL_FIELDNAMES, detail_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, summary_rows, detail_rows, args)
    write_manifest(args.manifest_out, args, detail_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocked-pairs", type=Path, default=DEFAULT_BLOCKED_PAIRS)
    parser.add_argument("--variants", type=Path, default=DEFAULT_VARIANTS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


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


def build_detail_rows(
    blocked_rows: list[dict[str, str]],
    variant_index: dict[str, list[dict[str, str]]],
) -> list[dict[str, object]]:
    out = []
    for row in blocked_rows:
        blockers = blocking_terms(row)
        if not blockers:
            continue
        hits = [variant_index.get(term_id, []) for _side, term_id, _term in blockers]
        impact = impact_status(hits)
        out.append(
            {
                "run_label": row.get("run_label", ""),
                "pair_id": row.get("pair_id", ""),
                "concept": row.get("concept", ""),
                "reason": row.get("reason", ""),
                "row_ocr_pair_status": row.get("row_ocr_pair_status", ""),
                "impact_status": impact,
                "blocking_term_ids": ";".join(term_id for _side, term_id, _term in blockers),
                "blocking_terms": ";".join(term for _side, _term_id, term in blockers),
                "blocking_term_variant_hits": ";".join(best_hit_text(term_rows) for term_rows in hits),
                "blocking_term_variant_rules": ";".join(best_rule_text(term_rows) for term_rows in hits),
                "read": read_for_impact(impact),
            }
        )
    return sorted(
        out,
        key=lambda row: (
            str(row["run_label"]),
            str(row["impact_status"]),
            str(row["concept"]),
            str(row["pair_id"]),
        ),
    )


def blocking_terms(row: dict[str, str]) -> list[tuple[str, str, str]]:
    reason = row.get("reason", "")
    blockers: list[tuple[str, str, str]] = []
    if reason in {REASON_APP, REASON_BOTH}:
        blockers.append(
            (
                "appellation",
                row.get("appellation_term_id", ""),
                row.get("appellation_term", ""),
            )
        )
    if reason in {REASON_DATE, REASON_BOTH}:
        blockers.append(("date", row.get("date_term_id", ""), row.get("date_term", "")))
    return [(side, term_id, term) for side, term_id, term in blockers if term_id]


def impact_status(variant_lists: list[list[dict[str, str]]]) -> str:
    hit_flags = [bool(rows) for rows in variant_lists]
    if all(hit_flags):
        return "all_blocking_terms_have_variant_hit"
    if any(hit_flags):
        return "some_blocking_terms_have_variant_hit"
    return "no_blocking_term_variant_hit"


def best_hit_text(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "0"
    return str(int_or_zero(rows[0].get("variant_hit_count", "")))


def best_rule_text(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "none"
    row = rows[0]
    return f"{row.get('variant_rule', '')}:{row.get('variant_normalized', '')}"


def read_for_impact(impact: str) -> str:
    if impact == "all_blocking_terms_have_variant_hit":
        return "all current zero-hit blockers have simple variant leads; diagnostic only"
    if impact == "some_blocking_terms_have_variant_hit":
        return "some current zero-hit blockers have simple variant leads; diagnostic only"
    return "no simple one-edit variant lead for the current zero-hit blockers"


def build_summary_rows(detail_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    counts: Counter[tuple[str, str]] = Counter()
    ocr: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    concepts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for row in detail_rows:
        key = (str(row["run_label"]), str(row["impact_status"]))
        counts[key] += 1
        ocr[key][str(row.get("row_ocr_pair_status", ""))] += 1
        concepts[key][str(row.get("concept", ""))] += 1
    return [
        {
            "run_label": run_label,
            "impact_status": impact,
            "pairs": count,
            "row_ocr_pair_statuses": format_counter(ocr[(run_label, impact)]),
            "top_concepts": format_top_counter(concepts[(run_label, impact)], limit=5),
        }
        for (run_label, impact), count in sorted(counts.items())
    ]


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    detail_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    best_label = best_run_label(detail_rows)
    best_summary = [row for row in summary_rows if row["run_label"] == best_label]
    top_pairs = [
        row
        for row in detail_rows
        if row["run_label"] == best_label
        and row["impact_status"] != "no_blocking_term_variant_hit"
    ][:12]
    lines = [
        "# WRR Variant Gap Impact",
        "",
        "Status: diagnostic-only join from current blocked WRR pair rows to",
        "zero-hit one-edit variant leads. It is not a source correction, not a",
        "term replacement, and not a WRR reproduction.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_variant_gap_impact "
            f"--blocked-pairs {args.blocked_pairs} "
            f"--variants {args.variants} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Best Current Run",
        "",
        f"- Best run label: `{best_label}`.",
        "",
        "| Impact status | Pairs | Row OCR pair statuses | Top concepts |",
        "| --- | ---: | --- | --- |",
    ]
    for row in best_summary:
        lines.append(
            "| `{impact_status}` | {pairs} | `{row_ocr_pair_statuses}` | `{top_concepts}` |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Top Variant-Lead Blocked Pairs",
            "",
            "| Pair | Concept | Reason | Blocking terms | Variant hits | Variant rules |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in top_pairs:
        lines.append(
            "| `{pair_id}` | `{concept}` | `{reason}` | `{blocking_terms}` | "
            "`{blocking_term_variant_hits}` | `{blocking_term_variant_rules}` |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This only prioritizes source-review work.",
            "- A variant lead does not make the original pair valid.",
            "- Claim-grade work still needs source transcription and pair-rule locks.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def best_run_label(detail_rows: list[dict[str, object]]) -> str:
    defined_order = ("all_lanes_cap1000", "all_lanes_cap1000_program", "all_lanes_cap250")
    labels = {str(row["run_label"]) for row in detail_rows}
    for label in defined_order:
        if label in labels:
            return label
    return sorted(labels)[-1] if labels else ""


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    detail_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": "analyze_wrr_variant_gap_impact",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "blocked_pairs": str(args.blocked_pairs),
            "variants": str(args.variants),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
        "detail_rows": len(detail_rows),
        "summary_rows": len(summary_rows),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def format_counter(counter: Counter[str]) -> str:
    return ", ".join(f"{counter[key]} {key}" for key in sorted(counter))


def format_top_counter(counter: Counter[str], *, limit: int) -> str:
    return ", ".join(
        f"{key} {count}" for key, count in counter.most_common(limit) if key
    )


def int_or_zero(value: str) -> int:
    if value in ("", None):
        return 0
    return int(float(value))


if __name__ == "__main__":
    raise SystemExit(main())
