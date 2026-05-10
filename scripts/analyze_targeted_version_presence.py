#!/usr/bin/env python3
"""Join targeted exact version presence, paired controls, and extension rows."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.normalization import normalize_text
from els.term_display import display_term


DEFAULT_TERMS = [Path("terms/modern_names_dates.csv"), Path("terms/prophetic_terms.csv")]
DEFAULT_HEBREW_SUMMARY = Path("reports/hebrew_screening_version_presence/term_summary.csv")
DEFAULT_GREEK_SUMMARY = Path("reports/greek_screening_version_presence/term_summary.csv")
DEFAULT_HEBREW_PATTERNS = Path("reports/hebrew_screening_version_presence/hit_patterns.csv")
DEFAULT_GREEK_PATTERNS = Path("reports/greek_screening_version_presence/hit_patterns.csv")
DEFAULT_CONTROLS = Path("reports/targeted_paired_controls_summary.csv")
DEFAULT_REPRESENTATIVE_CONTROLS: Path | None = None
DEFAULT_EXTENSION_SUMMARIES = [
    "MT_WLC=reports/version_presence_extensions/extensions_hebrew_mt_wlc_summary.csv",
    "UHB=reports/version_presence_extensions/extensions_hebrew_uhb_summary.csv",
    "TR_NT=reports/version_presence_extensions/extensions_greek_tr_nt_summary.csv",
    "SBLGNT=reports/version_presence_extensions/extensions_greek_sblgnt_summary.csv",
]
DEFAULT_EXTENSION_TOPS = [
    "MT_WLC=reports/version_presence_extensions/extensions_hebrew_mt_wlc_top.csv",
    "UHB=reports/version_presence_extensions/extensions_hebrew_uhb_top.csv",
    "TR_NT=reports/version_presence_extensions/extensions_greek_tr_nt_top.csv",
    "SBLGNT=reports/version_presence_extensions/extensions_greek_sblgnt_top.csv",
]

SUMMARY_OUT = Path("reports/targeted_version_presence_summary.csv")
EXAMPLES_OUT = Path("reports/targeted_version_presence_examples.csv")
CONTROL_TARGETS_OUT = Path("reports/targeted_version_presence_control_targets.csv")
MD_OUT = Path("reports/targeted_version_presence.md")
MANIFEST_OUT = Path("reports/targeted_version_presence.manifest.json")

DEFAULT_TARGET_TERM_IDS = (
    "trump_h",
    "trump_g",
    "donald_trump_h",
    "vance_h",
    "vance_alt_h",
    "vance_g",
    "netanyahu_h",
    "netanyahu_g",
    "iran_h",
    "iran_g",
    "russia_h",
    "russia_g",
    "france_h",
    "france_g",
    "europe_h",
    "europe_g",
    "germany_h",
    "germany_g",
    "turkey_h",
    "turkey_alt_h",
    "turkey_g",
    "america_h",
    "america_g",
    "united_states_h",
    "united_states_g",
    "united_states_america_h",
    "united_states_america_g",
    "usa_abbrev_h",
    "usa_abbrev_g",
    "united_nations_h",
    "united_nations_g",
    "united_nations_acronym_h",
    "united_nations_acronym_g",
    "european_union_h",
    "european_union_g",
    "nato_h",
    "nato_g",
    "confederacy_h",
    "confederacy_g",
    "alliance_h",
    "alliance_g",
    "coalition_h",
    "coalition_g",
    "cowboy_h",
    "cowboy_g",
    "catering_h",
    "catering_g",
    "cowboy_catering_h",
    "cowboy_catering_g",
    "simsberry_h",
    "simsberry_g",
    "simscorner_h",
    "simscorner_g",
    "gog_h",
    "gog_g",
    "magog_h",
    "magog_g",
    "hamas_h",
    "hamas_g",
)

SUMMARY_FIELDNAMES = [
    "language",
    "concept",
    "term_id",
    "category",
    "term",
    "normalized_term",
    "normalized_length",
    "exact_observed_corpora",
    "exact_hit_counts_by_corpus",
    "exact_total_hits",
    "exact_unique_patterns",
    "exact_all_source_patterns",
    "exact_leningrad_patterns",
    "exact_multi_source_patterns",
    "exact_source_specific_patterns",
    "exact_read",
    "paired_control_available",
    "paired_control_corpora",
    "paired_best_band",
    "paired_best_p",
    "paired_best_q",
    "paired_best_read",
    "representative_control_available",
    "representative_control_corpora",
    "representative_best_band",
    "representative_best_p",
    "representative_best_q",
    "representative_best_read",
    "extension_summary_rows",
    "extension_corpora",
    "extension_strong_plus_term_rows",
    "extension_best_row",
    "overall_read",
]

EXAMPLE_FIELDNAMES = [
    "language",
    "concept",
    "term_id",
    "term",
    "normalized_term",
    "example_type",
    "presence_scope",
    "skip",
    "direction",
    "span",
    "center_ref",
    "present_corpora",
    "absent_corpora",
    "center_words_by_corpus",
    "source_file",
]

CONTROL_TARGET_FIELDNAMES = [
    "concept",
    "corpus",
    "term_set",
    "term_id",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "normalized_length",
    "hit_count",
    "status",
]

REPRESENTATIVE_CORPORA = {
    "hebrew": ("MT_WLC", "UHB"),
    "greek": ("TR_NT", "SBLGNT"),
}

SCOPE_ORDER = {
    "present_all_observed_sources": 0,
    "present_all_leningrad_streams": 1,
    "present_multiple_sources": 2,
    "source_specific": 3,
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    term_paths = args.terms or DEFAULT_TERMS
    extension_summary_values = args.extension_summary or DEFAULT_EXTENSION_SUMMARIES
    extension_top_values = args.extension_top or DEFAULT_EXTENSION_TOPS
    exact_by_id = read_exact_summaries(args.hebrew_summary, args.greek_summary)
    selected_ids = selected_term_ids(args, exact_by_id)
    terms = read_selected_terms(term_paths, selected_ids)
    controls_by_id = group_controls(args.paired_controls)
    representative_controls_by_id = group_controls(args.representative_controls)
    extension_summaries = group_extension_summaries(extension_summary_values)
    extension_tops = group_extension_tops(extension_top_values)
    examples = pattern_examples(
        args.hebrew_patterns,
        args.greek_patterns,
        selected_ids,
        args.max_examples_per_scope,
    )

    summary_rows = build_summary_rows(
        selected_ids,
        terms,
        exact_by_id,
        controls_by_id,
        representative_controls_by_id,
        extension_summaries,
        extension_tops,
    )
    control_target_rows = build_control_target_rows(summary_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.examples_out, EXAMPLE_FIELDNAMES, examples)
    write_rows(args.control_targets_out, CONTROL_TARGET_FIELDNAMES, control_target_rows)
    write_markdown(
        args.markdown_out,
        summary_rows,
        examples,
        title=args.markdown_title,
        description=args.markdown_description,
    )
    write_manifest(
        args,
        selected_ids,
        term_paths,
        extension_summary_values,
        extension_top_values,
        summary_rows,
        examples,
        control_target_rows,
        started,
    )

    print(args.summary_out)
    print(args.examples_out)
    print(args.control_targets_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, action="append", default=None)
    parser.add_argument("--term-id", action="append", default=None)
    parser.add_argument(
        "--all-exact-term-ids",
        action="store_true",
        help="Use every term_id present in the exact-summary inputs instead of the built-in targeted list.",
    )
    parser.add_argument("--hebrew-summary", type=Path, default=DEFAULT_HEBREW_SUMMARY)
    parser.add_argument("--greek-summary", type=Path, default=DEFAULT_GREEK_SUMMARY)
    parser.add_argument("--hebrew-patterns", type=Path, default=DEFAULT_HEBREW_PATTERNS)
    parser.add_argument("--greek-patterns", type=Path, default=DEFAULT_GREEK_PATTERNS)
    parser.add_argument("--paired-controls", type=Path, default=DEFAULT_CONTROLS)
    parser.add_argument(
        "--representative-controls",
        type=Path,
        default=DEFAULT_REPRESENTATIVE_CONTROLS,
        help="Optional paired-control summary using the same skip band as version presence.",
    )
    parser.add_argument(
        "--extension-summary",
        action="append",
        default=None,
        help="Labeled extension summary in LABEL=path form; repeatable.",
    )
    parser.add_argument(
        "--extension-top",
        action="append",
        default=None,
        help="Labeled strong extension top file in LABEL=path form; repeatable.",
    )
    parser.add_argument("--max-examples-per-scope", type=int, default=2)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--examples-out", type=Path, default=EXAMPLES_OUT)
    parser.add_argument("--control-targets-out", type=Path, default=CONTROL_TARGETS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--markdown-title", default="Targeted Version Presence Review")
    parser.add_argument(
        "--markdown-description",
        default=(
            "This generated report joins exact version-presence summaries, "
            "available paired controls, and bounded version-presence extension "
            "rows for the requested modern/geopolitical/local targets."
        ),
    )
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def selected_term_ids(
    args: argparse.Namespace,
    exact_by_id: dict[str, dict[str, str]],
) -> tuple[str, ...]:
    if not args.all_exact_term_ids:
        return tuple(args.term_id or DEFAULT_TARGET_TERM_IDS)
    exact_ids = tuple(exact_by_id)
    if not args.term_id:
        return exact_ids
    allowed = set(args.term_id)
    return tuple(term_id for term_id in exact_ids if term_id in allowed)


def read_selected_terms(paths: list[Path], selected_ids: tuple[str, ...]) -> dict[str, dict[str, str]]:
    allowed = set(selected_ids)
    terms: dict[str, dict[str, str]] = {}
    for path in paths:
        for row in read_rows(path):
            term_id = row.get("term_id", "")
            if term_id not in allowed or term_id in terms:
                continue
            language = row.get("language", "")
            normalized = normalize_text(row.get("term", ""), language) if language else ""
            terms[term_id] = {
                "term_id": term_id,
                "concept": row.get("concept", ""),
                "category": row.get("category", ""),
                "language": language,
                "term": row.get("term", ""),
                "normalized_term": normalized,
                "normalized_length": str(len(normalized)),
            }
    return terms


def read_exact_summaries(hebrew_path: Path, greek_path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for language, path in (("hebrew", hebrew_path), ("greek", greek_path)):
        for row in read_rows(path):
            row = dict(row)
            row["language"] = language
            rows[row["term_id"]] = row
    return rows


def group_controls(path: Path | None) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    if path is None:
        return grouped
    for row in read_rows(path):
        grouped[row["term_id"]].append(row)
    return grouped


def group_extension_summaries(values: list[str]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for label, path in labeled_paths(values):
        for row in read_rows(path):
            row = dict(row)
            row["corpus"] = row.get("corpus", label) or label
            grouped[row["normalized_term"]].append(row)
    for rows in grouped.values():
        rows.sort(key=extension_summary_sort_key)
    return grouped


def group_extension_tops(values: list[str]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for label, path in labeled_paths(values):
        for row in read_rows(path):
            row = dict(row)
            row["corpus"] = row.get("corpus", label) or label
            grouped[row["normalized_term"]].append(row)
    for rows in grouped.values():
        rows.sort(key=extension_top_sort_key)
    return grouped


def labeled_paths(values: list[str]) -> list[tuple[str, Path]]:
    paths: list[tuple[str, Path]] = []
    for value in values:
        if "=" not in value:
            path = Path(value)
            paths.append((path.stem, path))
            continue
        label, path = value.split("=", 1)
        paths.append((label, Path(path)))
    return paths


def build_summary_rows(
    selected_ids: tuple[str, ...],
    terms: dict[str, dict[str, str]],
    exact_by_id: dict[str, dict[str, str]],
    controls_by_id: dict[str, list[dict[str, str]]],
    representative_controls_by_id: dict[str, list[dict[str, str]]] | None,
    extension_summaries: dict[str, list[dict[str, str]]],
    extension_tops: dict[str, list[dict[str, str]]],
) -> list[dict[str, object]]:
    representative_controls_by_id = representative_controls_by_id or {}
    rows: list[dict[str, object]] = []
    for term_id in selected_ids:
        term = terms.get(term_id)
        exact = exact_by_id.get(term_id, {})
        if term is None and not exact:
            continue
        meta = term or exact_to_term(exact)
        normalized = exact.get("normalized_term") or meta.get("normalized_term", "")
        controls = controls_by_id.get(term_id, [])
        representative_controls = representative_controls_by_id.get(term_id, [])
        ext_summary_rows = extension_summaries.get(normalized, [])
        ext_top_rows = extension_tops.get(normalized, [])
        rows.append(
            summary_row(
                meta,
                exact,
                controls,
                representative_controls,
                ext_summary_rows,
                ext_top_rows,
            )
        )
    return rows


def exact_to_term(exact: dict[str, str]) -> dict[str, str]:
    return {
        "term_id": exact.get("term_id", ""),
        "concept": exact.get("concept", ""),
        "category": exact.get("category", ""),
        "language": exact.get("language", ""),
        "term": exact.get("term", ""),
        "normalized_term": exact.get("normalized_term", ""),
        "normalized_length": str(len(exact.get("normalized_term", ""))),
    }


def summary_row(
    term: dict[str, str],
    exact: dict[str, str],
    controls: list[dict[str, str]],
    representative_controls: list[dict[str, str]],
    extension_rows: list[dict[str, str]],
    extension_top_rows: list[dict[str, str]],
) -> dict[str, object]:
    control = best_control(controls)
    representative_control = best_control(representative_controls)
    exact_status = exact_read(term, exact)
    control_status = control_read(control, controls)
    representative_control_status = representative_control_read(
        representative_control,
        representative_controls,
    )
    extension_status = extension_read(extension_rows, extension_top_rows)
    return {
        "language": term.get("language", exact.get("language", "")),
        "concept": term.get("concept", exact.get("concept", "")),
        "term_id": term.get("term_id", exact.get("term_id", "")),
        "category": term.get("category", exact.get("category", "")),
        "term": term.get("term", exact.get("term", "")),
        "normalized_term": exact.get("normalized_term") or term.get("normalized_term", ""),
        "normalized_length": len(exact.get("normalized_term") or term.get("normalized_term", "")),
        "exact_observed_corpora": exact.get("observed_corpora", ""),
        "exact_hit_counts_by_corpus": exact.get("hit_counts_by_corpus", ""),
        "exact_total_hits": int_or_zero(exact.get("total_hits", "")),
        "exact_unique_patterns": int_or_zero(exact.get("unique_patterns", "")),
        "exact_all_source_patterns": int_or_zero(exact.get("all_observed_patterns", "")),
        "exact_leningrad_patterns": int_or_zero(exact.get("all_leningrad_patterns", "")),
        "exact_multi_source_patterns": int_or_zero(exact.get("multi_source_patterns", "")),
        "exact_source_specific_patterns": int_or_zero(exact.get("source_specific_patterns", "")),
        "exact_read": exact_status,
        "paired_control_available": "yes" if controls else "no",
        "paired_control_corpora": ",".join(sorted({row.get("corpus", "") for row in controls if row.get("corpus")})),
        "paired_best_band": control.get("paired_band", ""),
        "paired_best_p": control.get("combined_min_p_ge", ""),
        "paired_best_q": control.get("combined_min_q_value", ""),
        "paired_best_read": control_status,
        "representative_control_available": "yes" if representative_controls else "no",
        "representative_control_corpora": ",".join(
            sorted({row.get("corpus", "") for row in representative_controls if row.get("corpus")})
        ),
        "representative_best_band": representative_control.get("paired_band", ""),
        "representative_best_p": representative_control.get("combined_min_p_ge", ""),
        "representative_best_q": representative_control.get("combined_min_q_value", ""),
        "representative_best_read": representative_control_status,
        "extension_summary_rows": len(extension_rows),
        "extension_corpora": ",".join(sorted({row.get("corpus", "") for row in extension_rows if row.get("corpus")})),
        "extension_strong_plus_term_rows": len(extension_top_rows),
        "extension_best_row": format_extension_row(extension_rows[0]) if extension_rows else "",
        "overall_read": overall_read(
            exact_status,
            control_status,
            extension_status,
            representative_control_status,
        ),
    }


def build_control_target_rows(summary_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in summary_rows:
        normalized = str(row["normalized_term"])
        if len(normalized) < 4:
            continue
        counts = parse_hit_counts(str(row["exact_hit_counts_by_corpus"]))
        for corpus in REPRESENTATIVE_CORPORA.get(str(row["language"]), ()):
            hit_count = counts.get(corpus, 0)
            if hit_count <= 0:
                continue
            rows.append(
                {
                    "concept": row["concept"],
                    "corpus": corpus,
                    "term_set": "targeted_version_presence",
                    "term_id": row["term_id"],
                    "category": row["category"],
                    "term_language": row["language"],
                    "term": row["term"],
                    "normalized_term": normalized,
                    "normalized_length": len(normalized),
                    "hit_count": hit_count,
                    "status": "counted",
                }
            )
    return rows


def parse_hit_counts(value: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for part in value.split(";"):
        part = part.strip()
        if not part or ":" not in part:
            continue
        corpus, raw_count = part.split(":", 1)
        counts[corpus.strip()] = int_or_zero(raw_count.strip())
    return counts


def best_control(rows: list[dict[str, str]]) -> dict[str, str]:
    if not rows:
        return {}
    return sorted(rows, key=control_sort_key)[0]


def control_sort_key(row: dict[str, str]) -> tuple[float, float, str]:
    return (
        float_or_one(row.get("combined_min_q_value", "")),
        float_or_one(row.get("combined_min_p_ge", "")),
        row.get("corpus", ""),
    )


def exact_read(term: dict[str, str], exact: dict[str, str]) -> str:
    normalized = exact.get("normalized_term") or term.get("normalized_term", "")
    if len(normalized) < 4:
        return "below exact-version screen minimum length"
    if not exact:
        return "not found in exact-version summary"
    if int_or_zero(exact.get("total_hits", "")) == 0:
        return "absent in capped exact-version screen"
    if int_or_zero(exact.get("all_observed_patterns", "")):
        return "has all-source exact patterns"
    if int_or_zero(exact.get("all_leningrad_patterns", "")):
        return "has Leningrad-family exact patterns"
    if int_or_zero(exact.get("multi_source_patterns", "")):
        return "has multi-source exact patterns"
    return "source-specific exact patterns only"


def control_read(best: dict[str, str], controls: list[dict[str, str]]) -> str:
    if not controls:
        return "not run in targeted paired controls"
    if best.get("paired_band") == "not_unusual":
        return "not unusual under paired controls"
    if best.get("paired_band"):
        return f"{best['paired_band']}; inspect before claim"
    return "paired control row present"


def representative_control_read(best: dict[str, str], controls: list[dict[str, str]]) -> str:
    if not controls:
        return "not run in representative paired controls"
    if best.get("paired_band") == "not_unusual":
        return "not unusual under representative controls"
    if best.get("paired_band") == "paired_uncorrected_p_le_0.05":
        return "uncorrected representative-control screen only"
    if best.get("paired_band"):
        return f"{best['paired_band']}; inspect before claim"
    return "representative control row present"


def extension_read(extension_rows: list[dict[str, str]], extension_top_rows: list[dict[str, str]]) -> str:
    if extension_top_rows:
        return "has strong plus-term extension top rows"
    if extension_rows:
        return "has before/after-only phrase extension rows"
    return "no strict phrase-extension summary row"


def overall_read(
    exact_status: str,
    control_status: str,
    extension_status: str,
    representative_control_status: str = "",
) -> str:
    if "below" in exact_status:
        return "not comparable in exact-version matrix because normalized form is short"
    if "absent" in exact_status or "not found" in exact_status:
        return "absent or unsummarized in exact-version matrix"
    if "source-specific" in exact_status:
        return "source-specific exact rows only; needs controls and context before interpretation"
    if "multi-source" in exact_status:
        return "multi-source exact rows only; not all-source stable"
    if "not unusual under representative controls" in representative_control_status:
        return "version-stable where present, but representative controls do not support a claim"
    if "uncorrected representative-control" in representative_control_status:
        return "uncorrected representative-control screen only; no adjusted support"
    if "not unusual" in control_status:
        return "version-stable where present, but paired controls do not support a claim"
    if "not run" in control_status:
        return "version-distribution row only; needs paired controls before interpretation"
    if "strong plus-term" in extension_status:
        return "extension review candidate; still needs controls and context"
    return "screening row only"


def format_extension_row(row: dict[str, str]) -> str:
    return (
        f"{row.get('corpus', '')} {row.get('extension_type', '')} "
        f"skip={row.get('skip', '')} match={row.get('match_kind', '')} "
        f"max_len={row.get('max_extension_length', '')}"
    ).strip()


def pattern_examples(
    hebrew_path: Path,
    greek_path: Path,
    selected_ids: tuple[str, ...],
    max_per_scope: int,
) -> list[dict[str, object]]:
    selected = set(selected_ids)
    by_term_scope: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for language, path in (("hebrew", hebrew_path), ("greek", greek_path)):
        for row in read_rows(path):
            if row.get("term_id") not in selected:
                continue
            row = dict(row)
            row["language"] = language
            by_term_scope[(row["term_id"], row.get("presence_scope", ""))].append(row)
    examples: list[dict[str, object]] = []
    for key, rows in by_term_scope.items():
        rows.sort(key=pattern_sort_key)
        for row in rows[:max_per_scope]:
            examples.append(example_row(row))
    return sorted(examples, key=example_sort_key)


def example_row(row: dict[str, str]) -> dict[str, object]:
    span = row.get("start_ref", "")
    if row.get("end_ref") and row["end_ref"] != row.get("start_ref", ""):
        span = f"{span}-{row['end_ref']}"
    return {
        "language": row.get("language", ""),
        "concept": row.get("concept", ""),
        "term_id": row.get("term_id", ""),
        "term": row.get("term", ""),
        "normalized_term": row.get("normalized_term", ""),
        "example_type": "exact_pattern",
        "presence_scope": row.get("presence_scope", ""),
        "skip": row.get("skip", ""),
        "direction": row.get("direction", ""),
        "span": span,
        "center_ref": row.get("center_ref", ""),
        "present_corpora": row.get("present_corpora", ""),
        "absent_corpora": row.get("absent_corpora", ""),
        "center_words_by_corpus": row.get("center_words_by_corpus", ""),
        "source_file": "",
    }


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    examples: list[dict[str, object]],
    *,
    title: str = "Targeted Version Presence Review",
    description: str = (
        "This generated report joins exact version-presence summaries, "
        "available paired controls, and bounded version-presence extension rows "
        "for the requested modern/geopolitical/local targets."
    ),
) -> None:
    control_targets = build_control_target_rows(summary_rows)
    representative_counts = representative_read_counts(summary_rows)
    lines = [
        f"# {title}",
        "",
        description,
        "",
        "It is a screening report, not a significance claim.",
        "",
        "## Summary",
        "",
        "| Metric | Rows |",
        "| --- | ---: |",
        f"| Target rows | {len(summary_rows)} |",
        f"| Rows with all-source exact patterns | {sum(1 for row in summary_rows if int(row['exact_all_source_patterns']) > 0)} |",
        f"| Rows absent or unsummarized | {sum(1 for row in summary_rows if int(row['exact_total_hits']) == 0)} |",
        f"| Rows with paired controls | {sum(1 for row in summary_rows if row['paired_control_available'] == 'yes')} |",
        f"| Rows with representative controls | {sum(1 for row in summary_rows if row['representative_control_available'] == 'yes')} |",
        f"| Representative control target rows | {len(control_targets)} |",
        f"| Rows with strong plus-term extension tops | {sum(1 for row in summary_rows if int(row['extension_strong_plus_term_rows']) > 0)} |",
        "",
        "## Current Read",
        "",
        *representative_current_read_lines(summary_rows, representative_counts),
        "",
        "## Rows",
        "",
        "| Language | Concept | Term ID | Normalized | Exact total | All-source | Source-specific | Control | Rep control | Extensions | Read |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["language"]),
                    str(row["concept"]),
                    f"`{row['term_id']}`",
                    display_term(
                        str(row["normalized_term"]),
                        english=str(row.get("concept", "")),
                    ),
                    str(row["exact_total_hits"]),
                    str(row["exact_all_source_patterns"]),
                    str(row["exact_source_specific_patterns"]),
                    str(row["paired_best_band"] or row["paired_best_read"]),
                    str(row["representative_best_band"] or row["representative_best_read"]),
                    str(row["extension_summary_rows"]),
                    str(row["overall_read"]),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Exact Pattern Examples", ""])
    lines.extend(
        [
            "| Language | Concept | Term ID | Scope | Skip | Span | Present | Absent |",
            "| --- | --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in examples[:120]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["language"]),
                    str(row["concept"]),
                    f"`{row['term_id']}`",
                    f"`{row['presence_scope']}`",
                    str(row["skip"]),
                    str(row["span"]),
                    str(row["present_corpora"]),
                    str(row["absent_corpora"]),
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def representative_read_counts(summary_rows: list[dict[str, object]]) -> dict[str, int]:
    counts = {
        "not_run": 0,
        "not_unusual": 0,
        "uncorrected": 0,
        "adjusted": 0,
        "other": 0,
    }
    for row in summary_rows:
        read = str(row.get("representative_best_read", ""))
        band = str(row.get("representative_best_band", ""))
        if "not run" in read:
            counts["not_run"] += 1
        elif band == "not_unusual" or "not unusual" in read:
            counts["not_unusual"] += 1
        elif "uncorrected" in read or band == "paired_uncorrected_p_le_0.05":
            counts["uncorrected"] += 1
        elif band.startswith("paired_q_"):
            counts["adjusted"] += 1
        else:
            counts["other"] += 1
    return counts


def representative_current_read_lines(
    summary_rows: list[dict[str, object]],
    counts: dict[str, int],
) -> list[str]:
    absent = [
        f"`{row['term_id']}`"
        for row in summary_rows
        if int(row["exact_total_hits"]) == 0
    ]
    lines = [
        (
            "Representative paired controls are available for "
            f"{len(summary_rows) - counts['not_run']} rows. "
            f"{counts['not_unusual']} rows are not unusual under those controls; "
            f"{counts['uncorrected']} rows only clear an uncorrected p<=0.05 screen; "
            f"{counts['adjusted']} rows have adjusted representative-control support."
        ),
        (
            "Use the uncorrected rows as review prompts only. "
            "They did not survive the row-family correction in this generated table."
        ),
    ]
    if absent:
        lines.extend(
            [
                "No exact patterns were found in the capped exact-version matrix for: "
                + ", ".join(absent)
                + ".",
            ]
        )
    return lines


def write_manifest(
    args: argparse.Namespace,
    selected_ids: tuple[str, ...],
    term_paths: list[Path],
    extension_summary_values: list[str],
    extension_top_values: list[str],
    summary_rows: list[dict[str, object]],
    examples: list[dict[str, object]],
    control_target_rows: list[dict[str, object]],
    started: float,
) -> None:
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "selected_term_ids": list(selected_ids),
        "summary_rows": len(summary_rows),
        "example_rows": len(examples),
        "control_target_rows": len(control_target_rows),
        "inputs": [
            *(str(path) for path in term_paths),
            str(args.hebrew_summary),
            str(args.greek_summary),
            str(args.hebrew_patterns),
            str(args.greek_patterns),
            str(args.paired_controls),
            *((str(args.representative_controls),) if args.representative_controls else ()),
            *extension_summary_values,
            *extension_top_values,
        ],
        "outputs": {
            "summary": str(args.summary_out),
            "examples": str(args.examples_out),
            "control_targets": str(args.control_targets_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pattern_sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    return (
        SCOPE_ORDER.get(row.get("presence_scope", ""), 99),
        abs(int_or_zero(row.get("skip", ""))),
        row.get("center_ref", ""),
    )


def example_sort_key(row: dict[str, object]) -> tuple[str, str, int, int]:
    return (
        str(row["language"]),
        str(row["term_id"]),
        SCOPE_ORDER.get(str(row["presence_scope"]), 99),
        abs(int_or_zero(row["skip"])),
    )


def extension_summary_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    return (
        -int_or_zero(row.get("max_extension_length", "")),
        -int_or_zero(row.get("max_match_count", "")),
        abs(int_or_zero(row.get("skip", ""))),
    )


def extension_top_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    return (
        -int_or_zero(row.get("extension_score", "")),
        -int_or_zero(row.get("extension_length", "")),
        abs(int_or_zero(row.get("skip", ""))),
    )


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


def float_or_one(value: object) -> float:
    if value in ("", None):
        return 1.0
    return float(str(value))


if __name__ == "__main__":
    raise SystemExit(main())
