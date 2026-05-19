#!/usr/bin/env python3
"""Build a WRR2 pair eligibility review table from current audit outputs."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


TERMS = Path("reports/wrr_1994/wrr2_terms.csv")
COUNTS = Path("reports/wrr_1994/wrr2_genesis_counts.csv")
SKIP_CAPS = Path("reports/wrr_1994/wrr2_skip_caps.csv")
PAIR_SUMMARY = Path("reports/wrr_1994/wrr2_genesis_pair_audit_summary.csv")
OUT = Path("reports/wrr_1994/wrr2_pair_eligibility_table.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_pair_eligibility_summary.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_pair_eligibility_table.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_pair_eligibility_table.manifest.json")

APP_CATEGORY = "wrr_appellation"
DATE_CATEGORY = "wrr_date"
WNP_DISPUTED_ZACUT_CONCEPT = "WRR2 27"
WNP_DISPUTED_ZACUT_TERMS = frozenset({"ZKWTA", "ZKWTW", "M$HZKWTA", "M$HZKWTW"})

FIELDNAMES = [
    "pair_id",
    "concept",
    "appellation_term_id",
    "appellation_term",
    "appellation_normalized",
    "appellation_length",
    "appellation_hit_count",
    "appellation_skip_cap",
    "appellation_target_reached",
    "date_term_id",
    "date_term",
    "date_normalized",
    "date_length",
    "date_hit_count",
    "date_skip_cap",
    "date_target_reached",
    "same_record_pair",
    "appellation_min_length_ok",
    "appellation_wrr_length_ok",
    "date_wrr_length_ok",
    "length_filtered_pair_ok",
    "wnp_disputed_zacut_appellation",
    "candidate_lane",
    "pair_review_status",
    "all_pairs_within_gap",
    "strict_pairs_within_gap",
    "best_span_gap",
    "best_center_distance",
    "best_example_wrr_alpha",
    "eligibility_notes",
]

SUMMARY_FIELDNAMES = [
    "pairs",
    "concepts",
    "appellation_min_length_pairs",
    "length_filtered_pairs",
    "wnp_disputed_zacut_pairs",
    "zero_hit_pairs",
    "pairs_with_skip_cap_target_unreached",
    "pairs_with_close_hits",
    "pairs_with_strict_hits",
    "expected_published_pairs",
    "gap_appellation_min_length_to_expected",
    "gap_length_filtered_to_expected",
    "status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    terms = read_rows(args.terms)
    counts = {row["term_id"]: row for row in read_rows(args.counts)}
    skip_caps = {row["term_id"]: row for row in read_optional_rows(args.skip_caps)}
    pair_summary = pair_summary_by_key(read_optional_rows(args.pair_summary))
    rows = build_pair_rows(
        terms,
        counts,
        skip_caps,
        pair_summary,
        app_min_length=args.appellation_min_term_length,
        min_length=args.min_term_length,
        max_length=args.max_term_length,
    )
    summary = summarize(rows, expected_published_pairs=args.expected_published_pairs)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary, args)
    if args.manifest_out:
        write_manifest(args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, default=TERMS)
    parser.add_argument("--counts", type=Path, default=COUNTS)
    parser.add_argument("--skip-caps", type=Path, default=SKIP_CAPS)
    parser.add_argument("--pair-summary", type=Path, default=PAIR_SUMMARY)
    parser.add_argument("--appellation-min-term-length", type=int, default=5)
    parser.add_argument("--min-term-length", type=int, default=5)
    parser.add_argument("--max-term-length", type=int, default=8)
    parser.add_argument("--expected-published-pairs", type=int, default=163)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_optional_rows(path: Path | None) -> list[dict[str, str]]:
    if not path or not path.exists():
        return []
    return read_rows(path)


def pair_summary_by_key(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row.get("appellation_term_id", ""), row.get("date_term_id", "")): row
        for row in rows
    }


def build_pair_rows(
    terms: list[dict[str, str]],
    counts: dict[str, dict[str, str]],
    skip_caps: dict[str, dict[str, str]],
    pair_summary: dict[tuple[str, str], dict[str, str]],
    *,
    app_min_length: int,
    min_length: int,
    max_length: int,
) -> list[dict[str, object]]:
    terms_by_concept: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in terms:
        terms_by_concept[row.get("concept", "")].append(row)

    rows: list[dict[str, object]] = []
    for concept in sorted(terms_by_concept):
        concept_terms = terms_by_concept[concept]
        apps = sorted(
            (row for row in concept_terms if row.get("category") == APP_CATEGORY),
            key=lambda row: row.get("term_id", ""),
        )
        dates = sorted(
            (row for row in concept_terms if row.get("category") == DATE_CATEGORY),
            key=lambda row: row.get("term_id", ""),
        )
        for app in apps:
            for date in dates:
                rows.append(
                    build_pair_row(
                        app,
                        date,
                        counts,
                        skip_caps,
                        pair_summary.get((app["term_id"], date["term_id"]), {}),
                        app_min_length=app_min_length,
                        min_length=min_length,
                        max_length=max_length,
                    )
                )
    return rows


def build_pair_row(
    app: dict[str, str],
    date: dict[str, str],
    counts: dict[str, dict[str, str]],
    skip_caps: dict[str, dict[str, str]],
    pair_metrics: dict[str, str],
    *,
    app_min_length: int,
    min_length: int,
    max_length: int,
) -> dict[str, object]:
    app_count = counts.get(app["term_id"], {})
    date_count = counts.get(date["term_id"], {})
    app_skip = skip_caps.get(app["term_id"], {})
    date_skip = skip_caps.get(date["term_id"], {})
    app_length = int_or_zero(app_count.get("normalized_length"))
    date_length = int_or_zero(date_count.get("normalized_length"))
    app_min_ok = app_length >= app_min_length
    app_wrr_length_ok = min_length <= app_length <= max_length
    date_wrr_length_ok = min_length <= date_length <= max_length
    length_filtered_ok = app_wrr_length_ok and date_wrr_length_ok
    wnp_disputed = is_wnp_disputed_zacut_appellation(app)
    app_target_reached = app_skip.get("target_reached", "")
    date_target_reached = date_skip.get("target_reached", "")
    notes = eligibility_notes(
        app_length=app_length,
        date_length=date_length,
        app_min_ok=app_min_ok,
        app_wrr_length_ok=app_wrr_length_ok,
        date_wrr_length_ok=date_wrr_length_ok,
        app_hits=int_or_zero(app_count.get("hit_count")),
        date_hits=int_or_zero(date_count.get("hit_count")),
        app_target_reached=app_target_reached,
        date_target_reached=date_target_reached,
        wnp_disputed=wnp_disputed,
    )
    return {
        "pair_id": f"{app['term_id']}__{date['term_id']}",
        "concept": app.get("concept", ""),
        "appellation_term_id": app["term_id"],
        "appellation_term": app.get("term", ""),
        "appellation_normalized": app_count.get("normalized_term", ""),
        "appellation_length": app_length,
        "appellation_hit_count": int_or_zero(app_count.get("hit_count")),
        "appellation_skip_cap": app_skip.get("skip_cap", ""),
        "appellation_target_reached": app_target_reached,
        "date_term_id": date["term_id"],
        "date_term": date.get("term", ""),
        "date_normalized": date_count.get("normalized_term", ""),
        "date_length": date_length,
        "date_hit_count": int_or_zero(date_count.get("hit_count")),
        "date_skip_cap": date_skip.get("skip_cap", ""),
        "date_target_reached": date_target_reached,
        "same_record_pair": True,
        "appellation_min_length_ok": app_min_ok,
        "appellation_wrr_length_ok": app_wrr_length_ok,
        "date_wrr_length_ok": date_wrr_length_ok,
        "length_filtered_pair_ok": length_filtered_ok,
        "wnp_disputed_zacut_appellation": wnp_disputed,
        "candidate_lane": candidate_lane(app_min_ok, length_filtered_ok),
        "pair_review_status": pair_review_status(wnp_disputed),
        "all_pairs_within_gap": int_or_zero(pair_metrics.get("all_pairs_within_gap")),
        "strict_pairs_within_gap": int_or_zero(pair_metrics.get("strict_pairs_within_gap")),
        "best_span_gap": pair_metrics.get("best_span_gap", ""),
        "best_center_distance": pair_metrics.get("best_center_distance", ""),
        "best_example_wrr_alpha": pair_metrics.get("best_example_wrr_alpha", ""),
        "eligibility_notes": "; ".join(notes),
    }


def is_wnp_disputed_zacut_appellation(row: dict[str, str]) -> bool:
    return (
        row.get("concept") == WNP_DISPUTED_ZACUT_CONCEPT
        and row.get("category") == APP_CATEGORY
        and row.get("term") in WNP_DISPUTED_ZACUT_TERMS
    )


def candidate_lane(app_min_ok: bool, length_filtered_ok: bool) -> str:
    if not app_min_ok:
        return "excluded_by_appellation_min_length"
    if length_filtered_ok:
        return "length_5_8_smoke_candidate"
    return "appellation_min_length_candidate"


def pair_review_status(wnp_disputed: bool) -> str:
    if wnp_disputed:
        return "diagnostic_exclusion_candidate_not_locked"
    return "needs_primary_source_pair_rule"


def eligibility_notes(
    *,
    app_length: int,
    date_length: int,
    app_min_ok: bool,
    app_wrr_length_ok: bool,
    date_wrr_length_ok: bool,
    app_hits: int,
    date_hits: int,
    app_target_reached: object,
    date_target_reached: object,
    wnp_disputed: bool,
) -> list[str]:
    notes: list[str] = []
    if not app_min_ok:
        notes.append(f"appellation length {app_length} below minimum")
    if not app_wrr_length_ok:
        notes.append("appellation outside 5..8 smoke lane")
    if not date_wrr_length_ok:
        notes.append(f"date length {date_length} outside 5..8 smoke lane")
    if app_hits == 0:
        notes.append("appellation has zero Genesis hits at smoke cap")
    if date_hits == 0:
        notes.append("date has zero Genesis hits at smoke cap")
    if app_target_reached not in ("", None) and not truthy(app_target_reached):
        notes.append("appellation expected-count skip cap target not reached")
    if date_target_reached not in ("", None) and not truthy(date_target_reached):
        notes.append("date expected-count skip cap target not reached")
    if wnp_disputed:
        notes.append("WNP Zacut dispute diagnostic only; not an exclusion rule")
    if not notes:
        notes.append("eligible for source-rule review")
    return notes


def summarize(rows: list[dict[str, object]], *, expected_published_pairs: int) -> dict[str, object]:
    app_min_pairs = sum(1 for row in rows if bool(row["appellation_min_length_ok"]))
    length_pairs = sum(1 for row in rows if bool(row["length_filtered_pair_ok"]))
    return {
        "pairs": len(rows),
        "concepts": len({row["concept"] for row in rows}),
        "appellation_min_length_pairs": app_min_pairs,
        "length_filtered_pairs": length_pairs,
        "wnp_disputed_zacut_pairs": sum(
            1 for row in rows if bool(row["wnp_disputed_zacut_appellation"])
        ),
        "zero_hit_pairs": sum(
            1
            for row in rows
            if int_or_zero(row["appellation_hit_count"]) == 0
            or int_or_zero(row["date_hit_count"]) == 0
        ),
        "pairs_with_skip_cap_target_unreached": sum(
            1
            for row in rows
            if target_unreached(row["appellation_target_reached"])
            or target_unreached(row["date_target_reached"])
        ),
        "pairs_with_close_hits": sum(1 for row in rows if int_or_zero(row["all_pairs_within_gap"]) > 0),
        "pairs_with_strict_hits": sum(
            1 for row in rows if int_or_zero(row["strict_pairs_within_gap"]) > 0
        ),
        "expected_published_pairs": expected_published_pairs,
        "gap_appellation_min_length_to_expected": expected_published_pairs - app_min_pairs,
        "gap_length_filtered_to_expected": expected_published_pairs - length_pairs,
        "status": "lock_prep_only_not_canonical",
    }


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    args: argparse.Namespace,
) -> None:
    top_review = sorted(
        rows,
        key=lambda row: (
            str(row["pair_review_status"]) != "diagnostic_exclusion_candidate_not_locked",
            not bool(row["appellation_min_length_ok"]),
            not bool(row["length_filtered_pair_ok"]),
            -int_or_zero(row["all_pairs_within_gap"]),
            str(row["pair_id"]),
        ),
    )[:25]
    lines = [
        "# WRR2 Pair Eligibility Table",
        "",
        "Status: lock-prep table for source-rule review, not a canonical WRR pair set.",
        "",
        "This joins imported WRR2 term rows, Genesis count smoke output, expected-count skip caps, and nearest-pair audit metrics.",
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
            "## Review Rows",
            "",
            "| Pair | Concept | Lane | Status | App len | Date len | Close | Strict | Notes |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in top_review:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['pair_id']}`",
                    str(row["concept"]),
                    str(row["candidate_lane"]),
                    str(row["pair_review_status"]),
                    str(row["appellation_length"]),
                    str(row["date_length"]),
                    str(row["all_pairs_within_gap"]),
                    str(row["strict_pairs_within_gap"]),
                    str(row["eligibility_notes"]).replace("|", "\\|"),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Rules Used",
            "",
            f"- Appellation minimum length: `{args.appellation_min_term_length}`.",
            f"- Smoke length lane: `{args.min_term_length}..{args.max_term_length}` for both appellation and date terms.",
            "- WNP Zacut rows are flagged as diagnostics only, not excluded.",
            "- Current table remains `lock_prep_only_not_canonical` until a citable primary-source pair rule resolves the 163-distance set.",
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
        "inputs": {
            "terms": str(args.terms),
            "counts": str(args.counts),
            "skip_caps": str(args.skip_caps),
            "pair_summary": str(args.pair_summary),
        },
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


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def target_unreached(value: object) -> bool:
    return value not in ("", None) and not truthy(value)


if __name__ == "__main__":
    raise SystemExit(main())
