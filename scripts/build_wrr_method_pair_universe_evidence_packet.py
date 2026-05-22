#!/usr/bin/env python3
"""Build WRR method/pair-universe evidence packet for OCR-matched residuals."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_REMAINING_PACKET = Path("reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_COUNTS = Path("reports/wrr_1994/wrr2_genesis_counts.csv")
DEFAULT_CORRECTED_DISTANCE = Path(
    "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged.csv"
)
DEFAULT_OUT = Path("reports/wrr_1994/wrr_method_pair_universe_evidence_packet.csv")
DEFAULT_SUMMARY_OUT = Path(
    "reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv"
)
DEFAULT_MD = Path("docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_method_pair_universe_evidence_packet.manifest.json"
)

LANE = "method_or_pair_universe_review"
BOUNDARY = (
    "No source correction or method change is selected; OCR-matched zero-hit "
    "terms remain a method/pair-universe diagnostic."
)

PACKET_FIELDNAMES = [
    "run_label",
    "evidence_rank",
    "action_rank",
    "term_id",
    "term",
    "concept",
    "row_number",
    "pair_id",
    "date_term_id",
    "review_bucket",
    "blocking_reasons",
    "row_ocr_status",
    "base_skip_250_hit_count",
    "highcap_appellation_ordinary_hits",
    "highcap_date_ordinary_hits",
    "pair_valid_perturbations",
    "corrected_distance_status",
    "best_variant_hit_count",
    "best_variant_rule",
    "diagnostic_read",
    "no_input_boundary",
]

SUMMARY_FIELDNAMES = [
    "run_label",
    "action_terms",
    "residual_pairs",
    "frontier_pairs",
    "ocr_matched_terms",
    "zero_base_skip_250_terms",
    "zero_highcap_appellation_terms",
    "both_sides_zero_highcap_pairs",
    "no_variant_lead_terms",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    remaining_rows = read_rows(args.remaining_packet)
    source_rows = keyed_rows(read_rows(args.source_queue), "term_id")
    count_rows = keyed_rows(read_rows(args.counts), "term_id")
    cd_rows = keyed_rows(read_rows(args.corrected_distance), "pair_id")
    packet_rows = build_packet_rows(remaining_rows, source_rows, count_rows, cd_rows)
    summary_rows = build_summary_rows(packet_rows)
    write_csv(args.out, PACKET_FIELDNAMES, packet_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, packet_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, packet_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remaining-packet", type=Path, default=DEFAULT_REMAINING_PACKET)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--counts", type=Path, default=DEFAULT_COUNTS)
    parser.add_argument(
        "--corrected-distance", type=Path, default=DEFAULT_CORRECTED_DISTANCE
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_packet_rows(
    remaining_rows: list[dict[str, str]],
    source_rows: dict[str, dict[str, str]],
    count_rows: dict[str, dict[str, str]],
    cd_rows: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    rows = []
    for row in remaining_rows:
        if row.get("action_lane") != LANE:
            continue
        term_id = row.get("term_id", "")
        source = source_rows.get(term_id, {})
        pair_ids = split_values(source.get("pair_ids", ""))
        pair_id = pair_ids[0] if pair_ids else ""
        cd = cd_rows.get(pair_id, {})
        count = count_rows.get(term_id, {})
        rows.append(
            {
                "run_label": row.get("run_label", ""),
                "evidence_rank": int_or_zero(row.get("evidence_rank", "")),
                "action_rank": int_or_zero(row.get("action_rank", "")),
                "term_id": term_id,
                "term": row.get("term", ""),
                "concept": row.get("concept", ""),
                "row_number": row.get("row_number", ""),
                "pair_id": pair_id,
                "date_term_id": cd.get("date_term_id", ""),
                "review_bucket": source.get("review_bucket", row.get("review_buckets", "")),
                "blocking_reasons": source.get("blocking_reasons", ""),
                "row_ocr_status": row.get("row_ocr_status", ""),
                "base_skip_250_hit_count": int_or_zero(count.get("hit_count", "")),
                "highcap_appellation_ordinary_hits": int_or_zero(
                    cd.get("appellation_ordinary_hits", "")
                ),
                "highcap_date_ordinary_hits": int_or_zero(
                    cd.get("date_ordinary_hits", "")
                ),
                "pair_valid_perturbations": int_or_zero(
                    cd.get("pair_valid_perturbations", "")
                ),
                "corrected_distance_status": cd.get("corrected_distance_status", ""),
                "best_variant_hit_count": int_or_zero(row.get("best_variant_hit_count", "")),
                "best_variant_rule": row.get("best_variant_rule", ""),
                "diagnostic_read": diagnostic_read(row, count, cd),
                "no_input_boundary": BOUNDARY,
            }
        )
    rows.sort(
        key=lambda item: (
            -int(item["highcap_date_ordinary_hits"]),
            int(item["action_rank"]),
            str(item["term_id"]),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["evidence_rank"] = index
    return rows


def diagnostic_read(
    row: dict[str, str],
    count: dict[str, str],
    cd: dict[str, str],
) -> str:
    base_hits = int_or_zero(count.get("hit_count", ""))
    app_hits = int_or_zero(cd.get("appellation_ordinary_hits", ""))
    date_hits = int_or_zero(cd.get("date_ordinary_hits", ""))
    if base_hits == 0 and app_hits == 0 and date_hits == 0:
        return (
            "OCR matched the appellation, but both sides have zero high-cap "
            "ordinary hits in the current run; investigate method and pair universe."
        )
    if base_hits == 0 and app_hits == 0:
        return (
            "OCR matched the appellation, but the appellation has zero ordinary "
            "Genesis hits under current search rules; not a quick source correction."
        )
    return (
        "OCR matched the source row; remaining undefined status needs method or "
        "pair-universe review."
    )


def build_summary_rows(packet_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    if not packet_rows:
        return []
    run_label = str(packet_rows[0].get("run_label", ""))
    zero_base = sum(1 for row in packet_rows if int(row["base_skip_250_hit_count"]) == 0)
    zero_app = sum(
        1 for row in packet_rows if int(row["highcap_appellation_ordinary_hits"]) == 0
    )
    both_zero = sum(
        1
        for row in packet_rows
        if int(row["highcap_appellation_ordinary_hits"]) == 0
        and int(row["highcap_date_ordinary_hits"]) == 0
    )
    no_variant = sum(1 for row in packet_rows if int(row["best_variant_hit_count"]) == 0)
    return [
        {
            "run_label": run_label,
            "action_terms": len(packet_rows),
            "residual_pairs": len({str(row["pair_id"]) for row in packet_rows}),
            "frontier_pairs": sum(
                1 for row in packet_rows if int(row["pair_valid_perturbations"]) > 0
            ),
            "ocr_matched_terms": sum(
                1 for row in packet_rows if row.get("row_ocr_status") == "matched"
            ),
            "zero_base_skip_250_terms": zero_base,
            "zero_highcap_appellation_terms": zero_app,
            "both_sides_zero_highcap_pairs": both_zero,
            "no_variant_lead_terms": no_variant,
            "read": (
                "OCR matched all method-lane terms, but current Koren Genesis "
                "ordinary-hit search still leaves them undefined."
            ),
        }
    ]


def write_markdown(
    path: Path,
    packet_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    summary = summary_rows[0] if summary_rows else {}
    lines = [
        "# WRR Method/Pair-Universe Evidence Packet",
        "",
        "Status: diagnostic packet for OCR-matched WRR residual terms.",
        "It does not choose source corrections, method changes, or pair exclusions.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_method_pair_universe_evidence_packet "
            f"--remaining-packet {args.remaining_packet} "
            f"--source-queue {args.source_queue} "
            f"--counts {args.counts} "
            f"--corrected-distance {args.corrected_distance} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Method/pair-universe action terms: {summary.get('action_terms', 0)}.",
        f"- OCR-matched terms: {summary.get('ocr_matched_terms', 0)}.",
        f"- Zero skip-250 appellation counts: {summary.get('zero_base_skip_250_terms', 0)}.",
        f"- Zero high-cap appellation ordinary hits: {summary.get('zero_highcap_appellation_terms', 0)}.",
        f"- Both sides zero high-cap ordinary hits: {summary.get('both_sides_zero_highcap_pairs', 0)}.",
        f"- Boundary: {BOUNDARY}",
        "",
        "## Action Terms",
        "",
        "| Rank | Term id | Term | Pair | App hits 250 | App hits 1000 | Date hits 1000 | Valid perturbations | Status | Read |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in packet_rows:
        lines.append(
            "| {evidence_rank} | `{term_id}` | `{term}` | `{pair_id}` | "
            "{base_skip_250_hit_count} | {highcap_appellation_ordinary_hits} | "
            "{highcap_date_ordinary_hits} | {pair_valid_perturbations} | "
            "{corrected_distance_status} | {diagnostic_read} |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## No-Input Boundary",
            "",
            "- OCR match is not enough to define a WRR corrected distance.",
            "- Zero ordinary hits keep these rows in method or pair-universe review.",
            "- No row here changes the working source or excludes a pair automatically.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    packet_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_method_pair_universe_evidence_packet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "packet_rows": len(packet_rows),
        "summary_rows": len(summary_rows),
        "inputs": {
            "remaining_packet": str(args.remaining_packet),
            "source_queue": str(args.source_queue),
            "counts": str(args.counts),
            "corrected_distance": str(args.corrected_distance),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def keyed_rows(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def split_values(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def markdown_row(row: dict[str, object]) -> dict[str, str]:
    return {key: markdown_cell(value) for key, value in row.items()}


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
