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
    "row_ocr_hebrew_normalized",
    "concepts",
    "row_numbers",
    "row_ocr_status",
    "row_ocr_column",
    "row_ocr_match_basis",
    "row_ocr_text_normalized",
    "row_ocr_near_match_distance",
    "row_ocr_near_match_text",
    "blocking_pairs",
    "blocking_reasons",
    "best_variant_hit_count",
    "best_variant_rule",
    "best_variant_normalized",
    "source_review_flags",
    "source_review_note",
    "source_review_action",
    "visual_review_note",
    "visual_review_action",
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
    "source_review_flags",
]

WNP_CONTEXT = {
    ("WRR2 27", "appellation", "ZKWTA"): (
        "wnp_disputed_zacut_appellation",
        "WNP argues primary Zacut form is ZKWT and removes ZKWTA/ZKWTW-derived forms.",
        "diagnostic flag only; do not exclude without source-lock policy",
    ),
    ("WRR2 27", "appellation", "ZKWTW"): (
        "wnp_disputed_zacut_appellation",
        "WNP argues primary Zacut form is ZKWT and removes ZKWTA/ZKWTW-derived forms.",
        "diagnostic flag only; do not exclude without source-lock policy",
    ),
    ("WRR2 27", "appellation", "M$HZKWTA"): (
        "wnp_disputed_zacut_appellation",
        "WNP argues primary Zacut form is ZKWT and removes M$HZKWTA/M$HZKWTW.",
        "diagnostic flag only; do not exclude without source-lock policy",
    ),
    ("WRR2 27", "appellation", "M$HZKWTW"): (
        "wnp_disputed_zacut_appellation",
        "WNP argues primary Zacut form is ZKWT and removes M$HZKWTA/M$HZKWTW.",
        "diagnostic flag only; do not exclude without source-lock policy",
    ),
    ("WRR2 30", "appellation", "Y$RLBB"): (
        "wnp_book_title_appellation_dispute",
        "WNP argues Y$RLBB is a book title, not a valid Ricchi appellation.",
        "source/title-prefix rule review before source correction",
    ),
    ("WRR2 30", "appellation", "B@LY$RLBB"): (
        "wnp_book_title_appellation_dispute",
        "WNP argues Y$RLBB is a book title, not a valid Ricchi appellation.",
        "source/title-prefix rule review; visual notes show title text without visible B@L prefix",
    ),
    ("WRR2 32", "appellation", "$LMHMXLMA"): (
        "wnp_chelm_spelling_context",
        "WNP discusses CLMA/CILMA spelling variants and $LMH CLMA forms.",
        "source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass",
    ),
    ("WRR2 32", "appellation", "$LMHMX@LMA"): (
        "wnp_chelm_spelling_context",
        "WNP discusses CLMA/CILMA spelling variants and $LMH CLMA forms.",
        "source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass",
    ),
}

VISUAL_CONTEXT_BY_TERM_ID = {
    "wrr2_23_app_04": (
        "primary page row visibly contains Yaakov Ha-Levi wording; row OCR missed it",
        "treat as visual OCR miss until a locked transcription says otherwise",
    ),
    "wrr2_23_app_05": (
        "primary page row visibly contains Maharil Segal wording; row OCR missed it",
        "treat as visual OCR miss until a locked transcription says otherwise",
    ),
    "wrr2_30_app_05": (
        "primary Hebrew name cell visibly contains Yosher Levav text without visible B@L prefix",
        "review title-prefix/appellation rule before any source correction",
    ),
    "wrr2_28_app_04": (
        "primary Hebrew name cell visibly contains Pnei Moshe text without visible B@L prefix",
        "review title-prefix/appellation rule before any source correction",
    ),
    "wrr2_32_app_04": (
        "English label says of-Chelm; visible primary Hebrew cell supports Rabbi Shelomo only in this pass",
        "review source/pair rule before using this as a Hebrew-cell match",
    ),
    "wrr2_27_date_01": (
        "primary page row visibly contains 16 Tishri date forms; row OCR has near match",
        "check page image before treating as source difference",
    ),
    "wrr2_27_app_06": (
        "primary page row visibly contains Moshe/Zacut forms; row OCR has near match",
        "check WNP Zacut dispute and page image before treating as source difference",
    ),
    "wrr2_19_app_11": (
        "primary page row visibly contains Maharit/Trani forms including Yosef Trani; row OCR has one-edit near match",
        "keep as page-image near-match until a locked transcription resolves the aleph spelling",
    ),
    "wrr2_19_app_12": (
        "primary page row visibly contains Maharit/Trani forms including Matrani/Mitrani variants; row OCR has one-edit near match",
        "keep as page-image near-match until a locked transcription resolves the aleph spelling",
    ),
    "wrr2_31_app_07": (
        "primary page row visibly contains Rabbi Shalom Sharabi forms including Sar Shalom and MaharaSHaSH; exact SMSh form is not settled by this crop",
        "keep as page-image or pair-rule review before any source correction",
    ),
}

BUCKET_READS = {
    "ocr_not_matched_with_variant_lead": (
        "OCR did not match imported term and a simple variant has Genesis hits; "
        "check source transcription first"
    ),
    "ocr_near_match_with_variant_lead": (
        "OCR has a one-edit near match and a simple variant has Genesis hits; "
        "check the page image before treating this as a source difference"
    ),
    "ocr_matched_with_variant_lead": (
        "OCR matched imported term and a simple variant has Genesis hits; "
        "check normalization/rule assumptions without changing source text"
    ),
    "ocr_not_matched_no_variant_lead": (
        "OCR did not match imported term and no simple variant lead exists; "
        "check source transcription or row alignment"
    ),
    "ocr_near_match_no_variant_lead": (
        "OCR has a one-edit near match but no simple variant lead exists; "
        "check the page image before deeper method work"
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
    "ocr_near_match_with_variant_lead": 1,
    "ocr_matched_with_variant_lead": 2,
    "ocr_not_matched_no_variant_lead": 3,
    "ocr_near_match_no_variant_lead": 4,
    "ocr_unknown_with_variant_lead": 5,
    "ocr_matched_no_variant_lead": 6,
    "ocr_unknown_no_variant_lead": 7,
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
        ocr_text = ocr.get("row_ocr_text_normalized", "")
        hebrew_normalized = ocr.get("hebrew_normalized", "")
        near_distance, near_text = best_near_match(hebrew_normalized, ocr_text)
        bucket = review_bucket(ocr_status, best_hits, near_distance)
        pair_ids = sorted(cast_set(item["pair_ids"]))
        concepts = sorted(cast_set(item["concepts"]))
        reasons = cast_counter(item["blocking_reasons"])
        flags, note, action = source_review_context(
            concepts,
            str(item["term_side"]),
            str(item["term"]),
        )
        visual_note, visual_action = visual_review_context(term_id)
        out.append(
            {
                "run_label": run_label,
                "priority_rank": 0,
                "review_bucket": bucket,
                "term_side": item["term_side"],
                "term_id": term_id,
                "term": item["term"],
                "normalized": item["normalized"],
                "row_ocr_hebrew_normalized": hebrew_normalized,
                "concepts": ";".join(concepts),
                "row_numbers": ocr.get("row_number", ""),
                "row_ocr_status": ocr_status,
                "row_ocr_column": ocr.get("column", ""),
                "row_ocr_match_basis": ocr.get("match_basis", ""),
                "row_ocr_text_normalized": ocr_text,
                "row_ocr_near_match_distance": "" if near_distance is None else near_distance,
                "row_ocr_near_match_text": near_text,
                "blocking_pairs": len(pair_ids),
                "blocking_reasons": format_counter(reasons),
                "best_variant_hit_count": best_hits,
                "best_variant_rule": best_variant.get("variant_rule", "none"),
                "best_variant_normalized": best_variant.get("variant_normalized", ""),
                "source_review_flags": flags,
                "source_review_note": note,
                "source_review_action": action,
                "visual_review_note": visual_note,
                "visual_review_action": visual_action,
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


def review_bucket(
    row_ocr_status: str,
    best_variant_hit_count: int,
    near_match_distance: int | None = None,
) -> str:
    has_variant = best_variant_hit_count > 0
    near_match = near_match_distance is not None and 0 < near_match_distance <= 1
    if row_ocr_status == "not_matched":
        if near_match:
            return "ocr_near_match_with_variant_lead" if has_variant else "ocr_near_match_no_variant_lead"
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
        flags = Counter(
            flag
            for row in rows
            for flag in str(row.get("source_review_flags", "")).split(";")
            if flag
        )
        out.append(
            {
                "run_label": run_label,
                "review_bucket": bucket,
                "terms": len(rows),
                "blocking_pairs": sum(int(row["blocking_pairs"]) for row in rows),
                "variant_hit_total": sum(int(row["best_variant_hit_count"]) for row in rows),
                "row_ocr_statuses": format_counter(statuses),
                "source_review_flags": format_counter(flags),
            }
        )
    return out


def source_review_context(
    concepts: list[str],
    term_side: str,
    term: str,
) -> tuple[str, str, str]:
    matches = [
        WNP_CONTEXT[(concept, term_side, term)]
        for concept in concepts
        if (concept, term_side, term) in WNP_CONTEXT
    ]
    if not matches:
        return "", "", ""
    flags = sorted({flag for flag, _note, _action in matches})
    notes = sorted({note for _flag, note, _action in matches})
    actions = sorted({action for _flag, _note, action in matches})
    return ";".join(flags), " ".join(notes), " ".join(actions)


def visual_review_context(term_id: str) -> tuple[str, str]:
    return VISUAL_CONTEXT_BY_TERM_ID.get(term_id, ("", ""))


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
        "variant leads, with local WNP critique flags where applicable. It is",
        "not a source correction, not a term replacement, and not a WRR",
        "reproduction.",
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
        "| Bucket | Terms | Blocking pairs | Variant hit total | Row OCR statuses | Source flags |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| `{review_bucket}` | {terms} | {blocking_pairs} | {variant_hit_total} | "
            "`{row_ocr_statuses}` | {source_flags} |".format(
                source_flags=markdown_code_or_blank(str(row.get("source_review_flags", ""))),
                **row,
            )
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
            "| Rank | Term id | Hebrew-normalized term | Row OCR normalized text |",
            "| ---: | --- | --- | --- |",
        ]
    )
    for row in queue_rows[:12]:
        lines.append(
            "| {priority_rank} | `{term_id}` | `{row_ocr_hebrew_normalized}` | "
            "`{row_ocr_text}` |".format(
                row_ocr_text=truncate_text(str(row.get("row_ocr_text_normalized", "")), 80),
                **row,
            )
        )
    lines.extend(
        [
            "",
            "## OCR Near Matches For Top Targets",
            "",
            "| Rank | Term id | Distance | Near OCR text |",
            "| ---: | --- | ---: | --- |",
        ]
    )
    for row in queue_rows[:12]:
        lines.append(
            "| {priority_rank} | `{term_id}` | {row_ocr_near_match_distance} | "
            "`{row_ocr_near_match_text}` |".format(**row)
        )
    visual_rows = [row for row in queue_rows if row.get("visual_review_note")]
    if visual_rows:
        lines.extend(
            [
                "",
                "## Visual Triage Notes For Queued Terms",
                "",
                "| Rank | Term id | Note | Action |",
                "| ---: | --- | --- | --- |",
            ]
        )
        for row in visual_rows:
            lines.append(
                "| {priority_rank} | `{term_id}` | {visual_review_note} | "
                "{visual_review_action} |".format(**row)
            )
    flagged_rows = [row for row in queue_rows if row.get("source_review_flags")]
    if flagged_rows:
        lines.extend(
            [
                "",
                "## WNP Context For Queued Terms",
                "",
                "| Rank | Term id | Flags | Note | Action |",
                "| ---: | --- | --- | --- | --- |",
            ]
        )
        for row in flagged_rows:
            lines.append(
                "| {priority_rank} | `{term_id}` | `{source_review_flags}` | "
                "{source_review_note} | {source_review_action} |".format(**row)
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Review queue ranks source-transcription and normalization checks.",
            "- Variant leads do not validate the original blocked pairs.",
            "- WNP flags are diagnostic context only, not exclusion rules.",
            "- Visual-review notes do not exclude pairs automatically.",
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


def markdown_code_or_blank(value: str) -> str:
    return f"`{value}`" if value else ""


def best_near_match(needle: str, haystack: str, max_distance: int = 2) -> tuple[int | None, str]:
    if not needle or not haystack:
        return None, ""
    if needle in haystack:
        return 0, needle
    best_distance: int | None = None
    best_text = ""
    best_length_delta: int | None = None
    min_len = max(1, len(needle) - max_distance)
    max_len = min(len(haystack), len(needle) + max_distance)
    for size in range(min_len, max_len + 1):
        for start in range(0, len(haystack) - size + 1):
            candidate = haystack[start : start + size]
            distance = levenshtein_distance(needle, candidate, max_distance=max_distance)
            if distance is None:
                continue
            length_delta = abs(len(candidate) - len(needle))
            if (
                best_distance is None
                or distance < best_distance
                or (distance == best_distance and length_delta < int(best_length_delta or 0))
            ):
                best_distance = distance
                best_length_delta = length_delta
                best_text = candidate
                if distance == 0:
                    return best_distance, best_text
    return best_distance, best_text


def levenshtein_distance(a: str, b: str, max_distance: int) -> int | None:
    previous = list(range(len(b) + 1))
    for index_a, char_a in enumerate(a, start=1):
        current = [index_a]
        row_min = current[0]
        for index_b, char_b in enumerate(b, start=1):
            cost = 0 if char_a == char_b else 1
            current.append(
                min(
                    previous[index_b] + 1,
                    current[index_b - 1] + 1,
                    previous[index_b - 1] + cost,
                )
            )
            row_min = min(row_min, current[-1])
        if row_min > max_distance:
            return None
        previous = current
    distance = previous[-1]
    return distance if distance <= max_distance else None


def int_or_zero(value: str | None) -> int:
    if value in ("", None):
        return 0
    return int(float(value))


if __name__ == "__main__":
    raise SystemExit(main())
