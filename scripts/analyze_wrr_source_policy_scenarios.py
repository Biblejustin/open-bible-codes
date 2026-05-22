#!/usr/bin/env python3
"""Analyze diagnostic WRR source-policy scenario impact."""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_PAIR_TABLE = Path("reports/wrr_1994/wrr2_pair_eligibility_table.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_source_policy_scenarios.csv")
DEFAULT_PAIR_OUT = Path("reports/wrr_1994/wrr_source_policy_scenario_pairs.csv")
DEFAULT_TERM_IMPACT_OUT = Path("reports/wrr_1994/wrr_source_policy_term_impacts.csv")
DEFAULT_MD = Path("docs/WRR_SOURCE_POLICY_SCENARIOS.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_source_policy_scenarios.manifest.json")

WNP_DISPUTED_ZACUT_FLAG = "wnp_disputed_zacut_appellation"

SUMMARY_FIELDNAMES = [
    "scenario",
    "policy_type",
    "source_policy_selected",
    "excluded_source_review_flags",
    "review_only_flags",
    "excluded_terms",
    "excluded_pairs",
    "review_only_terms",
    "review_only_pairs",
    "remaining_pairs",
    "remaining_appellation_min_length_pairs",
    "remaining_length_filtered_pairs",
    "remaining_non_rabbi_title_length_filtered_pairs",
    "remaining_wnp_disputed_zacut_pairs",
    "gap_to_source_cited_163_after_appellation_min_length",
    "gap_to_source_cited_163_after_length_filtered",
    "diagnostic_read",
]

PAIR_FIELDNAMES = [
    "scenario",
    "scenario_action",
    "pair_id",
    "concept",
    "appellation_term_id",
    "appellation_term",
    "date_term_id",
    "date_term",
    "source_review_flags",
    "flagged_term_ids",
    "reason",
    "candidate_lane",
    "appellation_min_length_ok",
    "length_filtered_pair_ok",
    "pair_review_status",
]

TERM_IMPACT_FIELDNAMES = [
    "term_id",
    "term",
    "term_side",
    "concepts",
    "flags",
    "basis",
    "source_review_action",
    "affected_pairs",
    "affected_appellation_min_length_pairs",
    "affected_length_filtered_pairs",
    "remaining_pairs_if_excluded",
    "remaining_appellation_min_length_pairs_if_excluded",
    "remaining_length_filtered_pairs_if_excluded",
    "gap_to_source_cited_163_after_appellation_min_length_if_excluded",
    "closes_appellation_min_length_gap_to_163",
    "diagnostic_read",
]


@dataclass(frozen=True)
class Scenario:
    name: str
    policy_type: str
    excluded_flags: frozenset[str]
    review_only_flags: frozenset[str]
    exclude_any_flag: bool
    read: str


SCENARIOS = [
    Scenario(
        name="keep_all_working_source",
        policy_type="baseline",
        excluded_flags=frozenset(),
        review_only_flags=frozenset(),
        exclude_any_flag=False,
        read="current working source; no source-review exclusions",
    ),
    Scenario(
        name="exclude_wnp_zacut_only",
        policy_type="diagnostic_exclusion",
        excluded_flags=frozenset({WNP_DISPUTED_ZACUT_FLAG}),
        review_only_flags=frozenset(),
        exclude_any_flag=False,
        read="diagnostic only; excludes WNP-disputed Zacut appellations",
    ),
    Scenario(
        name="exclude_book_title_only",
        policy_type="diagnostic_exclusion",
        excluded_flags=frozenset({"wnp_book_title_appellation_dispute"}),
        review_only_flags=frozenset(),
        exclude_any_flag=False,
        read="diagnostic only; excludes WNP book-title appellation dispute",
    ),
    Scenario(
        name="review_chelm_spelling_only",
        policy_type="review_only",
        excluded_flags=frozenset(),
        review_only_flags=frozenset({"wnp_chelm_spelling_context"}),
        exclude_any_flag=False,
        read="review only; Chelm spelling context changes no pair counts",
    ),
    Scenario(
        name="exclude_all_source_review_flags",
        policy_type="diagnostic_exclusion",
        excluded_flags=frozenset(),
        review_only_flags=frozenset(),
        exclude_any_flag=True,
        read="diagnostic only; excludes every currently flagged source-review term",
    ),
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    pair_rows = read_rows(args.pair_table)
    source_rows = read_rows(args.source_queue)
    term_index = build_flagged_term_index(pair_rows, source_rows)
    summary_rows, pair_detail_rows = analyze_scenarios(
        pair_rows,
        term_index,
        expected_pairs=args.expected_published_pairs,
    )
    term_impact_rows = build_term_impact_rows(
        pair_rows,
        term_index,
        expected_pairs=args.expected_published_pairs,
    )
    write_csv(args.out, SUMMARY_FIELDNAMES, summary_rows)
    write_csv(args.pair_out, PAIR_FIELDNAMES, pair_detail_rows)
    write_csv(args.term_impact_out, TERM_IMPACT_FIELDNAMES, term_impact_rows)
    write_markdown(
        args.markdown_out,
        summary_rows,
        pair_detail_rows,
        term_impact_rows,
        term_index,
        args,
    )
    write_manifest(
        args.manifest_out,
        args,
        summary_rows,
        pair_detail_rows,
        term_impact_rows,
        term_index,
        started,
    )
    print(args.out)
    print(args.pair_out)
    print(args.term_impact_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair-table", type=Path, default=DEFAULT_PAIR_TABLE)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--expected-published-pairs", type=int, default=163)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--pair-out", type=Path, default=DEFAULT_PAIR_OUT)
    parser.add_argument("--term-impact-out", type=Path, default=DEFAULT_TERM_IMPACT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def analyze_scenarios(
    pair_rows: list[dict[str, str]],
    term_index: dict[str, dict[str, object]],
    *,
    expected_pairs: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    summary_rows = []
    pair_detail_rows = []
    for scenario in SCENARIOS:
        excluded_pairs: set[str] = set()
        excluded_terms: set[str] = set()
        review_pairs: set[str] = set()
        review_terms: set[str] = set()
        excluded_flags: set[str] = set()
        for row in pair_rows:
            pair_flags = flags_for_pair(row, term_index)
            flagged_terms = flagged_term_ids_for_pair(row, term_index)
            exclusion_flags = exclusion_flags_for_scenario(pair_flags, scenario)
            review_flags = pair_flags & scenario.review_only_flags
            if exclusion_flags:
                pair_id = row.get("pair_id", "")
                excluded_pairs.add(pair_id)
                excluded_terms.update(flagged_terms_for_flags(row, term_index, exclusion_flags))
                excluded_flags.update(exclusion_flags)
                pair_detail_rows.append(
                    build_pair_detail_row(
                        scenario,
                        row,
                        "excluded",
                        exclusion_flags,
                        flagged_terms,
                    )
                )
            elif review_flags:
                pair_id = row.get("pair_id", "")
                review_pairs.add(pair_id)
                review_terms.update(flagged_terms_for_flags(row, term_index, review_flags))
                pair_detail_rows.append(
                    build_pair_detail_row(
                        scenario,
                        row,
                        "review_only_no_exclusion",
                        review_flags,
                        flagged_terms,
                    )
                )
        remaining = [row for row in pair_rows if row.get("pair_id", "") not in excluded_pairs]
        app_min_remaining = count_truthy(remaining, "appellation_min_length_ok")
        length_remaining = count_truthy(remaining, "length_filtered_pair_ok")
        summary_rows.append(
            {
                "scenario": scenario.name,
                "policy_type": scenario.policy_type,
                "source_policy_selected": "false",
                "excluded_source_review_flags": ";".join(sorted(excluded_flags)),
                "review_only_flags": ";".join(sorted(scenario.review_only_flags)),
                "excluded_terms": len(excluded_terms),
                "excluded_pairs": len(excluded_pairs),
                "review_only_terms": len(review_terms),
                "review_only_pairs": len(review_pairs),
                "remaining_pairs": len(remaining),
                "remaining_appellation_min_length_pairs": app_min_remaining,
                "remaining_length_filtered_pairs": length_remaining,
                "remaining_non_rabbi_title_length_filtered_pairs": count_non_rabbi_length(remaining),
                "remaining_wnp_disputed_zacut_pairs": count_truthy(
                    remaining,
                    "wnp_disputed_zacut_appellation",
                ),
                "gap_to_source_cited_163_after_appellation_min_length": (
                    expected_pairs - app_min_remaining
                ),
                "gap_to_source_cited_163_after_length_filtered": expected_pairs - length_remaining,
                "diagnostic_read": scenario.read,
            }
        )
    return summary_rows, pair_detail_rows


def build_term_impact_rows(
    pair_rows: list[dict[str, str]],
    term_index: dict[str, dict[str, object]],
    *,
    expected_pairs: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    flagged_terms = sorted(
        (
            term
            for term in term_index.values()
            if cast_set(term.get("flags", set()))
        ),
        key=lambda term: str(term.get("term_id", "")),
    )
    for term in flagged_terms:
        term_id = str(term.get("term_id", ""))
        affected = [
            row
            for row in pair_rows
            if term_id in {row.get("appellation_term_id", ""), row.get("date_term_id", "")}
        ]
        affected_ids = {row.get("pair_id", "") for row in affected}
        remaining = [row for row in pair_rows if row.get("pair_id", "") not in affected_ids]
        app_min_remaining = count_truthy(remaining, "appellation_min_length_ok")
        gap = expected_pairs - app_min_remaining
        closes_gap = app_min_remaining == expected_pairs
        rows.append(
            {
                "term_id": term_id,
                "term": term.get("term", ""),
                "term_side": term.get("term_side", ""),
                "concepts": ";".join(sorted(cast_set(term.get("concepts", set())))),
                "flags": ";".join(sorted(cast_set(term.get("flags", set())))),
                "basis": ";".join(sorted(cast_set(term.get("basis", set())))),
                "source_review_action": term.get("source_review_action", ""),
                "affected_pairs": len(affected),
                "affected_appellation_min_length_pairs": count_truthy(
                    affected,
                    "appellation_min_length_ok",
                ),
                "affected_length_filtered_pairs": count_truthy(
                    affected,
                    "length_filtered_pair_ok",
                ),
                "remaining_pairs_if_excluded": len(remaining),
                "remaining_appellation_min_length_pairs_if_excluded": app_min_remaining,
                "remaining_length_filtered_pairs_if_excluded": count_truthy(
                    remaining,
                    "length_filtered_pair_ok",
                ),
                "gap_to_source_cited_163_after_appellation_min_length_if_excluded": gap,
                "closes_appellation_min_length_gap_to_163": str(closes_gap).lower(),
                "diagnostic_read": (
                    "single-term exclusion closes >=5 count gap"
                    if closes_gap
                    else "single-term diagnostic only; keep_all_working_source remains selected"
                ),
            }
        )
    return rows


def build_flagged_term_index(
    pair_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
) -> dict[str, dict[str, object]]:
    index: dict[str, dict[str, object]] = {}
    for row in source_rows:
        term_id = row.get("term_id", "")
        flags = split_flags(row.get("source_review_flags", ""))
        if not term_id or not flags:
            continue
        item = index.setdefault(term_id, base_term_item(term_id))
        cast_set(item["flags"]).update(flags)
        cast_set(item["basis"]).add("source_queue")
        item["term"] = row.get("term", "") or item["term"]
        item["term_side"] = row.get("term_side", "") or item["term_side"]
        item["source_review_action"] = (
            row.get("source_review_action", "") or item["source_review_action"]
        )
        cast_set(item["concepts"]).update(split_semicolon(row.get("concepts", "")))
    for row in pair_rows:
        remember_pair_terms(index, row)
        if not truthy(row.get("wnp_disputed_zacut_appellation", "")):
            continue
        term_id = row.get("appellation_term_id", "")
        item = index.setdefault(term_id, base_term_item(term_id))
        cast_set(item["flags"]).add(WNP_DISPUTED_ZACUT_FLAG)
        cast_set(item["basis"]).add("pair_table_wnp_flag")
        item["term"] = row.get("appellation_term", "") or item["term"]
        item["term_side"] = "appellation"
        cast_set(item["concepts"]).add(row.get("concept", ""))
    return index


def base_term_item(term_id: str) -> dict[str, object]:
    return {
        "term_id": term_id,
        "term": "",
        "term_side": "",
        "concepts": set(),
        "flags": set(),
        "basis": set(),
        "source_review_action": "",
    }


def remember_pair_terms(index: dict[str, dict[str, object]], row: dict[str, str]) -> None:
    for side, term_id_key, term_key in [
        ("appellation", "appellation_term_id", "appellation_term"),
        ("date", "date_term_id", "date_term"),
    ]:
        term_id = row.get(term_id_key, "")
        if not term_id:
            continue
        item = index.setdefault(term_id, base_term_item(term_id))
        item["term"] = row.get(term_key, "") or item["term"]
        item["term_side"] = side if not item["term_side"] else item["term_side"]
        cast_set(item["concepts"]).add(row.get("concept", ""))


def exclusion_flags_for_scenario(flags: set[str], scenario: Scenario) -> set[str]:
    if scenario.exclude_any_flag:
        return set(flags)
    return set(flags & scenario.excluded_flags)


def flags_for_pair(row: dict[str, str], term_index: dict[str, dict[str, object]]) -> set[str]:
    flags = set()
    for term_id in [row.get("appellation_term_id", ""), row.get("date_term_id", "")]:
        flags.update(cast_set(term_index.get(term_id, {}).get("flags", set())))
    return flags


def flagged_term_ids_for_pair(
    row: dict[str, str],
    term_index: dict[str, dict[str, object]],
) -> set[str]:
    out = set()
    for term_id in [row.get("appellation_term_id", ""), row.get("date_term_id", "")]:
        if cast_set(term_index.get(term_id, {}).get("flags", set())):
            out.add(term_id)
    return out


def flagged_terms_for_flags(
    row: dict[str, str],
    term_index: dict[str, dict[str, object]],
    flags: set[str],
) -> set[str]:
    out = set()
    for term_id in [row.get("appellation_term_id", ""), row.get("date_term_id", "")]:
        term_flags = cast_set(term_index.get(term_id, {}).get("flags", set()))
        if term_flags & flags:
            out.add(term_id)
    return out


def build_pair_detail_row(
    scenario: Scenario,
    row: dict[str, str],
    action: str,
    flags: set[str],
    flagged_terms: set[str],
) -> dict[str, object]:
    return {
        "scenario": scenario.name,
        "scenario_action": action,
        "pair_id": row.get("pair_id", ""),
        "concept": row.get("concept", ""),
        "appellation_term_id": row.get("appellation_term_id", ""),
        "appellation_term": row.get("appellation_term", ""),
        "date_term_id": row.get("date_term_id", ""),
        "date_term": row.get("date_term", ""),
        "source_review_flags": ";".join(sorted(flags)),
        "flagged_term_ids": ";".join(sorted(flagged_terms)),
        "reason": ";".join(sorted(flags)),
        "candidate_lane": row.get("candidate_lane", ""),
        "appellation_min_length_ok": row.get("appellation_min_length_ok", ""),
        "length_filtered_pair_ok": row.get("length_filtered_pair_ok", ""),
        "pair_review_status": row.get("pair_review_status", ""),
    }


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    pair_detail_rows: list[dict[str, object]],
    term_impact_rows: list[dict[str, object]],
    term_index: dict[str, dict[str, object]],
    args: argparse.Namespace,
) -> None:
    flagged_terms = sorted(
        (
            term
            for term in term_index.values()
            if cast_set(term.get("flags", set()))
        ),
        key=lambda term: str(term.get("term_id", "")),
    )
    lines = [
        "# WRR Source Policy Scenario Impact",
        "",
        "Status: scenario impact for selected keep_all_working_source policy.",
        "",
        "This report counts what would happen to the current WRR2 pair-eligibility",
        "table under several named source-review policies. The selected working",
        "policy keeps all imported WRR2 same-record pairs; exclusion scenarios are not applied.",
        "Visual-review notes remain triage only and do not exclude pairs automatically.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_source_policy_scenarios "
            f"--pair-table {args.pair_table} "
            f"--source-queue {args.source_queue} "
            f"--expected-published-pairs {args.expected_published_pairs} "
            f"--out {args.out} "
            f"--pair-out {args.pair_out} "
            f"--term-impact-out {args.term_impact_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        "| Scenario | Type | Excl pairs | Review pairs | Remain >=5 | Remain 5..8 | Gap >=5 vs 163 | Gap 5..8 vs 163 |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            "| {scenario} | `{policy_type}` | {excluded_pairs} | {review_only_pairs} | "
            "{app_min} | {length_filtered} | {gap_app} | {gap_len} |".format(
                scenario=markdown_cell(row["scenario"]),
                policy_type=markdown_cell(row["policy_type"]),
                excluded_pairs=row["excluded_pairs"],
                review_only_pairs=row["review_only_pairs"],
                app_min=row["remaining_appellation_min_length_pairs"],
                length_filtered=row["remaining_length_filtered_pairs"],
                gap_app=row["gap_to_source_cited_163_after_appellation_min_length"],
                gap_len=row["gap_to_source_cited_163_after_length_filtered"],
            )
        )
    lines.extend(
        [
            "",
            "## Flagged Terms",
            "",
            "| Term id | Term | Side | Flags | Basis | Action |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for term in flagged_terms:
        lines.append(
            "| `{term_id}` | `{term}` | `{side}` | `{flags}` | `{basis}` | {action} |".format(
                term_id=markdown_cell(term.get("term_id", "")),
                term=markdown_cell(term.get("term", "")),
                side=markdown_cell(term.get("term_side", "")),
                flags=markdown_cell(";".join(sorted(cast_set(term.get("flags", set()))))),
                basis=markdown_cell(";".join(sorted(cast_set(term.get("basis", set()))))),
                action=markdown_cell(str(term.get("source_review_action", ""))),
            )
        )
    lines.extend(
        [
            "",
            "## Single-Term Impact",
            "",
            "| Term id | Term | Flags | Affected pairs | Remain >=5 if excluded | Gap vs 163 | Read |",
            "| --- | --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in term_impact_rows:
        lines.append(
            "| `{term_id}` | `{term}` | `{flags}` | {affected} | {remaining} | {gap} | {read} |".format(
                term_id=markdown_cell(row["term_id"]),
                term=markdown_cell(row["term"]),
                flags=markdown_cell(row["flags"]),
                affected=row["affected_pairs"],
                remaining=row["remaining_appellation_min_length_pairs_if_excluded"],
                gap=row["gap_to_source_cited_163_after_appellation_min_length_if_excluded"],
                read=markdown_cell(row["diagnostic_read"]),
            )
        )
    lines.extend(
        [
            "",
            "## Impact Rows",
            "",
            "| Scenario | Action | Pair | Concept | Flags | Lane |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in pair_detail_rows[:40]:
        lines.append(
            "| `{scenario}` | `{action}` | `{pair}` | {concept} | `{flags}` | `{lane}` |".format(
                scenario=markdown_cell(row["scenario"]),
                action=markdown_cell(row["scenario_action"]),
                pair=markdown_cell(row["pair_id"]),
                concept=markdown_cell(row["concept"]),
                flags=markdown_cell(row["source_review_flags"]),
                lane=markdown_cell(row["candidate_lane"]),
            )
        )
    if len(pair_detail_rows) > 40:
        lines.append(f"| ... | ... | {len(pair_detail_rows) - 40} more rows | ... | ... | ... |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `keep_all_working_source` is the selected working source policy.",
            "- Exclusion scenarios show count impact only; they are not selected policies.",
            "- `review_chelm_spelling_only` keeps pair counts stable and records review scope.",
            "- Visual-review notes remain triage only and do not exclude pairs automatically.",
            "- Claim-grade WRR language still needs full corrected distances and aggregate/permutation lock.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary_rows: list[dict[str, object]],
    pair_detail_rows: list[dict[str, object]],
    term_impact_rows: list[dict[str, object]],
    term_index: dict[str, dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "pair_table": str(args.pair_table),
            "source_queue": str(args.source_queue),
        },
        "expected_published_pairs": args.expected_published_pairs,
        "scenarios": [row["scenario"] for row in summary_rows],
        "flagged_terms": sum(
            1 for term in term_index.values() if cast_set(term.get("flags", set()))
        ),
        "impact_rows": len(pair_detail_rows),
        "term_impact_rows": len(term_impact_rows),
        "outputs": {
            "csv": str(args.out),
            "pair_csv": str(args.pair_out),
            "term_impact_csv": str(args.term_impact_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def count_truthy(rows: list[dict[str, str]], key: str) -> int:
    return sum(1 for row in rows if truthy(row.get(key, "")))


def count_non_rabbi_length(rows: list[dict[str, str]]) -> int:
    return sum(
        1
        for row in rows
        if truthy(row.get("length_filtered_pair_ok", ""))
        and not truthy(row.get("appellation_starts_with_rabbi_title", ""))
    )


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def split_flags(value: str) -> set[str]:
    return set(split_semicolon(value))


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def cast_set(value: object) -> set[str]:
    if isinstance(value, set):
        return value
    if isinstance(value, frozenset):
        return set(value)
    if isinstance(value, (list, tuple)):
        return {str(item) for item in value}
    if value in ("", None):
        return set()
    return {str(value)}


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
