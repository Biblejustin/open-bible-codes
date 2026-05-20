#!/usr/bin/env python3
"""Reconcile imported WRR2 pair counts against source-record structure."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.import_wrr_terms import parse_wrr_records


SOURCE = Path("reports/wrr_1994/WRR2.txt")
TERMS = Path("reports/wrr_1994/wrr2_terms.csv")
COUNTS = Path("reports/wrr_1994/wrr2_genesis_counts.csv")
OUT = Path("reports/wrr_1994/wrr2_pair_table_reconciliation.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_pair_table_reconciliation.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_pair_table_reconciliation.manifest.json")

APP_CATEGORY = "wrr_appellation"
DATE_CATEGORY = "wrr_date"
WNP_DISPUTED_ZACUT_CONCEPT = "WRR2 27"
WNP_DISPUTED_ZACUT_TERMS = frozenset({"ZKWTA", "ZKWTW", "M$HZKWTA", "M$HZKWTW"})

FIELDNAMES = [
    "concept",
    "appellation_rows",
    "date_rows",
    "same_record_pairs",
    "appellation_min_length_pairs",
    "wnp_disputed_zacut_appellation_rows",
    "wnp_disputed_zacut_appellation_min_length_pairs",
    "length_filtered_appellation_rows",
    "length_filtered_date_rows",
    "length_filtered_pairs",
    "wnp_disputed_zacut_length_filtered_pairs",
    "pairs_dropped_by_appellation_length",
    "pairs_dropped_by_date_length",
    "pairs_dropped_by_both_lengths",
]

SUMMARY_FIELDNAMES = [
    "source_records",
    "source_undated_records",
    "source_appellations",
    "source_dates",
    "source_same_record_pairs",
    "imported_concepts",
    "imported_appellation_rows",
    "imported_date_rows",
    "imported_same_record_pairs",
    "appellation_min_length",
    "appellation_min_length_same_record_pairs",
    "wnp_disputed_zacut_appellation_rows",
    "wnp_disputed_zacut_appellation_min_length_pair_delta",
    "appellation_min_length_pairs_after_wnp_disputed_zacut_excluded",
    "appellation_min_length_gap_after_wnp_disputed_zacut_excluded",
    "one_zacut_appellation_min_length_pair_delta",
    "appellation_min_length_pairs_after_one_zacut_appellation_excluded",
    "appellation_min_length_gap_after_one_zacut_appellation_excluded",
    "length_filter_min",
    "length_filter_max",
    "length_filtered_appellation_rows",
    "length_filtered_date_rows",
    "length_filtered_same_record_pairs",
    "wnp_disputed_zacut_length_filtered_pair_delta",
    "length_filtered_pairs_after_wnp_disputed_zacut_excluded",
    "length_filtered_gap_after_wnp_disputed_zacut_excluded",
    "pairs_dropped_by_appellation_length",
    "pairs_dropped_by_date_length",
    "pairs_dropped_by_both_lengths",
    "expected_published_pairs",
    "appellation_min_length_gap_to_expected",
    "imported_pair_gap_to_expected",
    "length_filtered_gap_to_expected",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    source_records = parse_wrr_records(args.source.read_text(encoding=args.encoding))
    term_rows = read_rows(args.terms)
    count_rows = {row["term_id"]: row for row in read_rows(args.counts)}
    concept_rows = reconcile_concepts(
        term_rows,
        count_rows,
        min_length=args.min_term_length,
        max_length=args.max_term_length,
        app_min_length=args.appellation_min_term_length,
    )
    summary = summarize(source_records, concept_rows, args)
    write_rows(args.out, FIELDNAMES, concept_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, concept_rows, summary)
    if args.manifest_out:
        write_manifest(args, concept_rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--terms", type=Path, default=TERMS)
    parser.add_argument("--counts", type=Path, default=COUNTS)
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--min-term-length", type=int, default=5)
    parser.add_argument("--max-term-length", type=int, default=8)
    parser.add_argument("--appellation-min-term-length", type=int, default=5)
    parser.add_argument("--expected-published-pairs", type=int, default=163)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def reconcile_concepts(
    term_rows: list[dict[str, str]],
    count_rows: dict[str, dict[str, str]],
    *,
    min_length: int,
    max_length: int,
    app_min_length: int,
) -> list[dict[str, object]]:
    rows_by_concept: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in term_rows:
        rows_by_concept[row.get("concept", "")].append(row)

    output = []
    for concept, rows in rows_by_concept.items():
        apps = [row for row in rows if row.get("category") == APP_CATEGORY]
        dates = [row for row in rows if row.get("category") == DATE_CATEGORY]
        app_min_ok = [row for row in apps if length_at_least(row, count_rows, app_min_length)]
        app_ok = [row for row in apps if length_in_range(row, count_rows, min_length, max_length)]
        date_ok = [row for row in dates if length_in_range(row, count_rows, min_length, max_length)]
        disputed_apps = [row for row in apps if is_wnp_disputed_zacut_appellation(row)]
        disputed_app_min_ok = [row for row in app_min_ok if is_wnp_disputed_zacut_appellation(row)]
        disputed_app_ok = [row for row in app_ok if is_wnp_disputed_zacut_appellation(row)]
        drop_app = 0
        drop_date = 0
        drop_both = 0
        for app in apps:
            for date in dates:
                app_out = not length_in_range(app, count_rows, min_length, max_length)
                date_out = not length_in_range(date, count_rows, min_length, max_length)
                if app_out and date_out:
                    drop_both += 1
                elif app_out:
                    drop_app += 1
                elif date_out:
                    drop_date += 1
        output.append(
            {
                "concept": concept,
                "appellation_rows": len(apps),
                "date_rows": len(dates),
                "same_record_pairs": len(apps) * len(dates),
                "appellation_min_length_pairs": len(app_min_ok) * len(dates),
                "wnp_disputed_zacut_appellation_rows": len(disputed_apps),
                "wnp_disputed_zacut_appellation_min_length_pairs": len(disputed_app_min_ok)
                * len(dates),
                "length_filtered_appellation_rows": len(app_ok),
                "length_filtered_date_rows": len(date_ok),
                "length_filtered_pairs": len(app_ok) * len(date_ok),
                "wnp_disputed_zacut_length_filtered_pairs": len(disputed_app_ok) * len(date_ok),
                "pairs_dropped_by_appellation_length": drop_app,
                "pairs_dropped_by_date_length": drop_date,
                "pairs_dropped_by_both_lengths": drop_both,
            }
        )
    return sorted(output, key=lambda row: str(row["concept"]))


def is_wnp_disputed_zacut_appellation(row: dict[str, str]) -> bool:
    return (
        row.get("concept") == WNP_DISPUTED_ZACUT_CONCEPT
        and row.get("category") == APP_CATEGORY
        and row.get("term") in WNP_DISPUTED_ZACUT_TERMS
    )


def length_at_least(
    row: dict[str, str],
    count_rows: dict[str, dict[str, str]],
    min_length: int,
) -> bool:
    length = int_or_zero(count_rows.get(row["term_id"], {}).get("normalized_length"))
    return length >= min_length


def length_in_range(
    row: dict[str, str],
    count_rows: dict[str, dict[str, str]],
    min_length: int,
    max_length: int,
) -> bool:
    length = int_or_zero(count_rows.get(row["term_id"], {}).get("normalized_length"))
    return min_length <= length <= max_length


def summarize(source_records, rows: list[dict[str, object]], args: argparse.Namespace) -> dict[str, object]:
    source_pairs = sum(len(record.appellations) * len(record.dates) for record in source_records)
    imported_pairs = sum_int(rows, "same_record_pairs")
    app_min_pairs = sum_int(rows, "appellation_min_length_pairs")
    length_pairs = sum_int(rows, "length_filtered_pairs")
    zacut_app_min_delta = sum_int(rows, "wnp_disputed_zacut_appellation_min_length_pairs")
    zacut_length_delta = sum_int(rows, "wnp_disputed_zacut_length_filtered_pairs")
    one_zacut_delta = one_zacut_appellation_pair_delta(rows)
    app_min_after_zacut = app_min_pairs - zacut_app_min_delta
    app_min_after_one_zacut = app_min_pairs - one_zacut_delta
    length_after_zacut = length_pairs - zacut_length_delta
    return {
        "source_records": len(source_records),
        "source_undated_records": sum(1 for record in source_records if not record.dates),
        "source_appellations": sum(len(record.appellations) for record in source_records),
        "source_dates": sum(len(record.dates) for record in source_records),
        "source_same_record_pairs": source_pairs,
        "imported_concepts": len(rows),
        "imported_appellation_rows": sum_int(rows, "appellation_rows"),
        "imported_date_rows": sum_int(rows, "date_rows"),
        "imported_same_record_pairs": imported_pairs,
        "appellation_min_length": args.appellation_min_term_length,
        "appellation_min_length_same_record_pairs": app_min_pairs,
        "wnp_disputed_zacut_appellation_rows": sum_int(rows, "wnp_disputed_zacut_appellation_rows"),
        "wnp_disputed_zacut_appellation_min_length_pair_delta": zacut_app_min_delta,
        "appellation_min_length_pairs_after_wnp_disputed_zacut_excluded": app_min_after_zacut,
        "appellation_min_length_gap_after_wnp_disputed_zacut_excluded": args.expected_published_pairs
        - app_min_after_zacut,
        "one_zacut_appellation_min_length_pair_delta": one_zacut_delta,
        "appellation_min_length_pairs_after_one_zacut_appellation_excluded": app_min_after_one_zacut,
        "appellation_min_length_gap_after_one_zacut_appellation_excluded": args.expected_published_pairs
        - app_min_after_one_zacut,
        "length_filter_min": args.min_term_length,
        "length_filter_max": args.max_term_length,
        "length_filtered_appellation_rows": sum_int(rows, "length_filtered_appellation_rows"),
        "length_filtered_date_rows": sum_int(rows, "length_filtered_date_rows"),
        "length_filtered_same_record_pairs": length_pairs,
        "wnp_disputed_zacut_length_filtered_pair_delta": zacut_length_delta,
        "length_filtered_pairs_after_wnp_disputed_zacut_excluded": length_after_zacut,
        "length_filtered_gap_after_wnp_disputed_zacut_excluded": args.expected_published_pairs
        - length_after_zacut,
        "pairs_dropped_by_appellation_length": sum_int(rows, "pairs_dropped_by_appellation_length"),
        "pairs_dropped_by_date_length": sum_int(rows, "pairs_dropped_by_date_length"),
        "pairs_dropped_by_both_lengths": sum_int(rows, "pairs_dropped_by_both_lengths"),
        "expected_published_pairs": args.expected_published_pairs,
        "appellation_min_length_gap_to_expected": args.expected_published_pairs - app_min_pairs,
        "imported_pair_gap_to_expected": args.expected_published_pairs - imported_pairs,
        "length_filtered_gap_to_expected": args.expected_published_pairs - length_pairs,
    }


def one_zacut_appellation_pair_delta(rows: list[dict[str, object]]) -> int:
    for row in rows:
        if row.get("concept") == WNP_DISPUTED_ZACUT_CONCEPT:
            if int_or_zero(row.get("wnp_disputed_zacut_appellation_min_length_pairs")):
                return int_or_zero(row.get("date_rows"))
    return 0


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: dict[str, object],
) -> None:
    lines = [
        "# WRR2 Pair Table Reconciliation",
        "",
        "This report reconciles the imported WRR2 source-record structure against",
        "the length-filtered pair rows used by the repo smoke audit. It does not",
        "resolve the published WRR second-list distance table; it makes the current",
        "mismatch explicit.",
        "",
        "## Summary",
        "",
        "| Item | Count |",
        "| --- | ---: |",
    ]
    for key in SUMMARY_FIELDNAMES:
        lines.append(f"| `{key}` | {summary[key]} |")
    lines.extend(
        [
            "",
            "## Zacut Diagnostic",
            "",
            "The downloaded WNP/McKay-Bar-Natan critique pages dispute four Rabbi II-27",
            "Moshe Zacut variants: `ZKWT)`, `ZKWTW`, `M$H ZKWT)`, and `M$H ZKWTW`.",
            "In the imported source these correspond to `ZKWTA`, `ZKWTW`, `M$HZKWTA`,",
            "and `M$HZKWTW`. This section is diagnostic only; those pages are not used",
            "as a source rule for pre-filtering the candidate set.",
            "",
            "| Diagnostic | Count |",
            "| --- | ---: |",
            f"| WNP-disputed Zacut appellation rows | {summary['wnp_disputed_zacut_appellation_rows']} |",
            f"| Pair delta if all WNP-disputed Zacut rows are excluded after appellation length >= min | {summary['wnp_disputed_zacut_appellation_min_length_pair_delta']} |",
            f"| Appellation length >= min pairs after all WNP-disputed Zacut rows excluded | {summary['appellation_min_length_pairs_after_wnp_disputed_zacut_excluded']} |",
            f"| Gap to expected after all WNP-disputed Zacut rows excluded | {summary['appellation_min_length_gap_after_wnp_disputed_zacut_excluded']} |",
            f"| Pair delta from one length-eligible Zacut appellation exclusion | {summary['one_zacut_appellation_min_length_pair_delta']} |",
            f"| Appellation length >= min pairs after one Zacut appellation exclusion | {summary['appellation_min_length_pairs_after_one_zacut_appellation_excluded']} |",
            f"| Gap to expected after one Zacut appellation exclusion | {summary['appellation_min_length_gap_after_one_zacut_appellation_excluded']} |",
            "",
            "## Largest Pair Losses Under Length Filter",
            "",
            "| Concept | Source pairs | App length >= min pairs | WNP-disputed Zacut app-min pairs | Length-filtered pairs | WNP-disputed Zacut length-filtered pairs | Dropped app | Dropped date | Dropped both |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in sorted(
        rows,
        key=lambda item: (
            -(
                int(item["pairs_dropped_by_appellation_length"])
                + int(item["pairs_dropped_by_date_length"])
                + int(item["pairs_dropped_by_both_lengths"])
            ),
            str(item["concept"]),
        ),
    )[:20]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["concept"]),
                    str(row["same_record_pairs"]),
                    str(row["appellation_min_length_pairs"]),
                    str(row["wnp_disputed_zacut_appellation_min_length_pairs"]),
                    str(row["length_filtered_pairs"]),
                    str(row["wnp_disputed_zacut_length_filtered_pairs"]),
                    str(row["pairs_dropped_by_appellation_length"]),
                    str(row["pairs_dropped_by_date_length"]),
                    str(row["pairs_dropped_by_both_lengths"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Caution",
            "",
            "The imported secondary WRR2 file currently yields 182 raw source-record",
            "combinations against the source-cited WRR 163-distance sample. Filtering out",
            "only appellations shorter than 5 letters gives 165 rows, while the repo's",
            "5..8 length filter yields only 86 rows. Do not treat the current pair",
            "audit as a replication until the candidate set and corrected-distance",
            "eligibility path are implemented. The Zacut diagnostic above is a",
            "source-audit clue, not an exclusion rule.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "source": str(args.source),
        "terms": str(args.terms),
        "counts": str(args.counts),
        "summary": summary,
        "rows": len(rows),
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sum_int(rows: list[dict[str, object]], key: str) -> int:
    return sum(int_or_zero(row.get(key)) for row in rows)


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


if __name__ == "__main__":
    raise SystemExit(main())
