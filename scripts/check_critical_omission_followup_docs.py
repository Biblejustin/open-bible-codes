#!/usr/bin/env python3
"""Validate critical-omission follow-up docs keep required report shape."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_SECTIONS = ("## Setup", "## Method", "## Results", "## Cautions")
SUMMARY_REQUIRED_COLUMNS = (
    "term_id",
    "term",
    "normalized_term",
    "tr_hits",
    "broken_removed_letter_hits",
    "broken_spacing_hits",
    "broken_total_hits",
    "preserved_across_omission_hits",
)
EXAMPLE_REQUIRED_COLUMNS = (
    "term_id",
    "normalized_term",
    "skip",
    "direction",
    "start_ref",
    "end_ref",
    "break_type",
)
BY_VERSE_REQUIRED_COLUMNS = ("omitted_ref", "norm_length", "broken_total_hits")
CROSS_REQUIRED_COLUMNS = (
    "term_id",
    "sbl_status",
    "byz_status",
    "tcg_status",
    "cross_tradition_class",
)
NULL_SUMMARY_REQUIRED_COLUMNS = (
    "observed_total",
    "null_min",
    "null_median",
    "null_max",
    "p_ge",
    "p_le",
    "shuffles",
    "term_rows",
    "stat_rows",
)
LENGTH_REQUIRED_COLUMNS = (
    "term_id",
    "normalized_length",
    "total_tr_hits",
    "broken_hits",
    "break_rate",
    "naive_expected_break_rate",
    "ratio",
)


@dataclass(frozen=True)
class DocRule:
    path: Path
    required_phrases: tuple[str, ...]


DOC_RULES = (
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS.md"),
        (
            "# Critical Omission Breaks",
            "`reports/critical_omission_breaks_summary.csv`",
            "Broken total: 558.",
            "Deleted blocks used: 18.",
            "Raw break counts are not significance tests.",
        ),
    ),
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS_REVERSE.md"),
        (
            "# Critical Omission Breaks Reverse",
            "`reports/critical_omission_breaks_reverse_summary.csv`",
            "Spliced blocks: 18.",
            "Broken example rows: 237.",
            "Raw break counts are not significance tests.",
        ),
    ),
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS_CROSS_TRADITION.md"),
        (
            "# Critical Omission Breaks Cross Tradition",
            "`reports/critical_omission_breaks_cross_tradition.csv`",
            "Current output rows: 558",
            "`preserved_by_byz_and_tcg`: 163.",
            "This is a robustness screen, not a textual-critical stemma.",
        ),
    ),
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS_NULL.md"),
        (
            "# Critical Omission Breaks Null",
            "`reports/critical_omission_breaks_null/summary.csv`",
            "Observed breaks: 558.",
            "Greater-or-equal tail: 0.9910.",
            "Raw break counts are not significance tests.",
        ),
    ),
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS_LENGTH_STRATIFIED.md"),
        (
            "# Critical Omission Breaks Length Stratified",
            "`reports/critical_omission_breaks_length_stratified.csv`",
            "Current output rows: 458.",
            "`naive_expected_break_rate = L * D / N`",
            "Raw break counts are not significance tests.",
        ),
    ),
    DocRule(
        Path("docs/CRITICAL_OMISSION_BREAKS_PERICOPE_OVERRIDE.md"),
        (
            "# Critical Omission Breaks Pericope Override",
            "`reports/critical_omission_breaks_pericope_override_summary.csv`",
            "Broken example rows: 1,185.",
            "## Other Disputed Passages",
            "Raw break counts are not significance tests.",
        ),
    ),
)

PERICOPE_PASSAGES = (
    ("Pericope Adulterae", "pericope_adulterae"),
    ("Longer Ending of Mark", "longer_ending_of_mark"),
    ("Gethsemane angel and bloody sweat", "gethsemane_angel_and_bloody_sweat"),
    ("Father forgive them", "father_forgive_them"),
    ("Comma Johanneum", "comma_johanneum"),
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_critical_omission_docs(args.root)
    if failures:
        for failure in failures:
            print(f"critical-omission doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"critical-omission docs ok: {args.root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser


def validate_critical_omission_docs(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []
    doc_texts: dict[Path, str] = {}
    for rule in DOC_RULES:
        doc = root / rule.path
        if not doc.exists():
            failures.append(f"{rule.path} is missing")
            continue
        normalized_text = normalize_space(doc.read_text(encoding="utf-8"))
        doc_texts[rule.path] = normalized_text
        for section in REQUIRED_SECTIONS:
            if normalize_space(section) not in normalized_text:
                failures.append(f"{rule.path} missing section: {section}")
        for phrase in rule.required_phrases:
            if normalize_space(phrase) not in normalized_text:
                failures.append(f"{rule.path} missing phrase: {phrase}")
    if failures:
        return failures
    failures.extend(validate_report_artifacts(root, doc_texts))
    return failures


def validate_report_artifacts(root: Path, doc_texts: dict[Path, str]) -> list[str]:
    failures: list[str] = []
    validate_original_break_artifacts(root, doc_texts, failures)
    validate_reverse_artifacts(root, doc_texts, failures)
    validate_cross_tradition_artifacts(root, doc_texts, failures)
    validate_null_artifacts(root, doc_texts, failures)
    validate_length_stratified_artifacts(root, doc_texts, failures)
    validate_pericope_artifacts(root, doc_texts, failures)
    return failures


def validate_original_break_artifacts(
    root: Path, doc_texts: dict[Path, str], failures: list[str]
) -> None:
    doc = Path("docs/CRITICAL_OMISSION_BREAKS.md")
    summary, examples, by_verse, manifest = read_break_run(
        root,
        failures,
        summary=Path("reports/critical_omission_breaks_summary.csv"),
        examples=Path("reports/critical_omission_breaks_examples.csv"),
        by_verse=Path("reports/critical_omission_breaks_by_verse.csv"),
        manifest=Path("reports/critical_omission_breaks.manifest.json"),
    )
    if summary is None or examples is None or by_verse is None or manifest is None:
        return
    totals = break_totals(summary, Path("reports/critical_omission_breaks_summary.csv"), failures)
    require_equal(
        failures,
        "critical_omission_breaks term_rows",
        manifest.get("term_rows"),
        len(summary),
    )
    require_equal(
        failures,
        "critical_omission_breaks deleted_blocks_used",
        manifest.get("deleted_blocks_used"),
        len(by_verse),
    )
    require_equal(
        failures,
        "critical_omission_breaks broken_example_rows",
        manifest.get("broken_example_rows"),
        len(examples),
    )
    require_equal(failures, "critical_omission_breaks broken total", totals["broken"], len(examples))
    require_doc_phrase(doc_texts, doc, f"Greek term rows checked: {format_int(len(summary))}.", failures)
    require_doc_phrase(
        doc_texts,
        doc,
        f"Ref-missing verses: {format_int(int(manifest['ref_missing_verses']))}.",
        failures,
    )
    require_doc_phrase(
        doc_texts,
        doc,
        f"Deleted blocks used: {format_int(int(manifest['deleted_blocks_used']))}.",
        failures,
    )
    require_doc_phrase(
        doc_texts,
        doc,
        f"Deleted letters used: {format_int(int(manifest['deleted_letters_used']))}.",
        failures,
    )
    require_doc_phrase(doc_texts, doc, f"Broken total: {format_int(totals['broken'])}.", failures)
    require_doc_phrase(
        doc_texts,
        doc,
        f"Broken by removed ELS letter: {format_int(totals['removed'])}.",
        failures,
    )
    require_doc_phrase(
        doc_texts,
        doc,
        f"Broken by spacing only: {format_int(totals['spacing'])}.",
        failures,
    )
    require_doc_phrase(
        doc_texts,
        doc,
        f"Preserved across deleted block: {format_int(totals['preserved'])}.",
        failures,
    )


def validate_reverse_artifacts(
    root: Path, doc_texts: dict[Path, str], failures: list[str]
) -> None:
    doc = Path("docs/CRITICAL_OMISSION_BREAKS_REVERSE.md")
    summary, examples, by_verse, manifest = read_break_run(
        root,
        failures,
        summary=Path("reports/critical_omission_breaks_reverse_summary.csv"),
        examples=Path("reports/critical_omission_breaks_reverse_examples.csv"),
        by_verse=Path("reports/critical_omission_breaks_reverse_by_verse.csv"),
        manifest=Path("reports/critical_omission_breaks_reverse.manifest.json"),
    )
    if summary is None or examples is None or by_verse is None or manifest is None:
        return
    totals = break_totals(
        summary, Path("reports/critical_omission_breaks_reverse_summary.csv"), failures
    )
    require_equal(failures, "critical_omission_breaks_reverse summary total", totals["broken"], len(examples))
    require_equal(failures, "critical_omission_breaks_reverse spliced_blocks", manifest.get("spliced_blocks"), len(by_verse))
    require_equal(
        failures,
        "critical_omission_breaks_reverse broken_example_rows",
        manifest.get("broken_example_rows"),
        len(examples),
    )
    require_doc_phrase(
        doc_texts,
        doc,
        f"Spliced blocks: {format_int(int(manifest['spliced_blocks']))}.",
        failures,
    )
    require_doc_phrase(
        doc_texts,
        doc,
        f"Broken example rows: {format_int(len(examples))}.",
        failures,
    )


def validate_cross_tradition_artifacts(
    root: Path, doc_texts: dict[Path, str], failures: list[str]
) -> None:
    doc = Path("docs/CRITICAL_OMISSION_BREAKS_CROSS_TRADITION.md")
    csv_path = Path("reports/critical_omission_breaks_cross_tradition.csv")
    rows = read_csv_rows(root, csv_path, failures, CROSS_REQUIRED_COLUMNS)
    manifest = read_json_object(
        root, Path("reports/critical_omission_breaks_cross_tradition.manifest.json"), failures
    )
    if rows is None or manifest is None:
        return
    require_equal(failures, "critical_omission_breaks_cross_tradition rows", manifest.get("rows"), len(rows))
    require_doc_phrase(doc_texts, doc, f"Current output rows: {format_int(len(rows))}", failures)
    class_counts = Counter(row["cross_tradition_class"] for row in rows)
    for class_name in (
        "preserved_by_byz_and_tcg",
        "preserved_by_byz",
        "preserved_by_tcg",
        "tr_specific_under_equivalent_offsets",
    ):
        require_doc_phrase(
            doc_texts,
            doc,
            f"`{class_name}`: {format_int(class_counts.get(class_name, 0))}.",
            failures,
        )
    for column, label in (("byz_status", "BYZ_NT"), ("tcg_status", "TCG_NT")):
        status_counts = Counter(row[column] for row in rows)
        for status in (
            "preserved_equivalent_offsets",
            "ref_missing",
            "coordinate_mismatch",
            "not_preserved_equivalent_offsets",
        ):
            require_doc_phrase(
                doc_texts,
                doc,
                f"{label} {status.replace('_', ' ')}: {format_int(status_counts.get(status, 0))}.",
                failures,
            )


def validate_null_artifacts(
    root: Path, doc_texts: dict[Path, str], failures: list[str]
) -> None:
    doc = Path("docs/CRITICAL_OMISSION_BREAKS_NULL.md")
    summary_path = Path("reports/critical_omission_breaks_null/summary.csv")
    distribution_path = Path("reports/critical_omission_breaks_null/null_distribution.csv")
    per_block_path = Path("reports/critical_omission_breaks_null/null_per_block.csv")
    summary_rows = read_csv_rows(root, summary_path, failures, NULL_SUMMARY_REQUIRED_COLUMNS)
    distribution = read_csv_rows(root, distribution_path, failures, ("shuffle_index", "broken_total_hits"))
    per_block = read_csv_rows(root, per_block_path, failures, ("block_index", "ref", "observed_breaks"))
    manifest = read_json_object(root, Path("reports/critical_omission_breaks_null/manifest.json"), failures)
    if summary_rows is None or distribution is None or per_block is None or manifest is None:
        return
    require_equal(failures, f"{summary_path} row count", len(summary_rows), 1)
    if not summary_rows:
        return
    summary = summary_rows[0]
    observed_total = int(summary["observed_total"])
    shuffles = int(summary["shuffles"])
    null_values = [int(row["broken_total_hits"]) for row in distribution]
    require_equal(failures, "critical_omission_breaks_null observed_total", manifest.get("observed_total"), observed_total)
    require_equal(failures, "critical_omission_breaks_null shuffles", manifest.get("shuffles"), shuffles)
    require_equal(failures, "critical_omission_breaks_null distribution rows", len(distribution), shuffles)
    require_equal(failures, "critical_omission_breaks_null per-block rows", len(per_block), manifest.get("actual_blocks"))
    if null_values:
        sorted_values = sorted(null_values)
        require_equal(failures, "critical_omission_breaks_null null_min", int(summary["null_min"]), sorted_values[0])
        require_equal(
            failures,
            "critical_omission_breaks_null null_median",
            int(summary["null_median"]),
            sorted_values[len(sorted_values) // 2],
        )
        require_equal(failures, "critical_omission_breaks_null null_max", int(summary["null_max"]), sorted_values[-1])
    require_doc_phrase(
        doc_texts,
        doc,
        f"Current {shuffles}-shuffle protocol run:",
        failures,
    )
    require_doc_phrase(doc_texts, doc, f"Observed breaks: {format_int(observed_total)}.", failures)
    require_doc_phrase(
        doc_texts,
        doc,
        f"Null min/median/max: {summary['null_min']} / {summary['null_median']} / {summary['null_max']}.",
        failures,
    )
    require_doc_phrase(doc_texts, doc, f"Greater-or-equal tail: {float(summary['p_ge']):.4f}.", failures)
    require_doc_phrase(doc_texts, doc, f"Lesser-or-equal tail: {float(summary['p_le']):.4f}.", failures)


def validate_length_stratified_artifacts(
    root: Path, doc_texts: dict[Path, str], failures: list[str]
) -> None:
    doc = Path("docs/CRITICAL_OMISSION_BREAKS_LENGTH_STRATIFIED.md")
    rows = read_csv_rows(
        root,
        Path("reports/critical_omission_breaks_length_stratified.csv"),
        failures,
        LENGTH_REQUIRED_COLUMNS,
    )
    manifest = read_json_object(
        root,
        Path("reports/critical_omission_breaks_length_stratified.manifest.json"),
        failures,
    )
    if rows is None or manifest is None:
        return
    require_equal(failures, "critical_omission_breaks_length_stratified rows", manifest.get("rows"), len(rows))
    require_doc_phrase(doc_texts, doc, f"Current output rows: {format_int(len(rows))}.", failures)
    require_doc_phrase(
        doc_texts,
        doc,
        "`naive_expected_break_rate = L * D / N`",
        failures,
    )


def validate_pericope_artifacts(
    root: Path, doc_texts: dict[Path, str], failures: list[str]
) -> None:
    doc = Path("docs/CRITICAL_OMISSION_BREAKS_PERICOPE_OVERRIDE.md")
    summary, examples, by_verse, manifest = read_break_run(
        root,
        failures,
        summary=Path("reports/critical_omission_breaks_pericope_override_summary.csv"),
        examples=Path("reports/critical_omission_breaks_pericope_override_examples.csv"),
        by_verse=Path("reports/critical_omission_breaks_pericope_override_by_verse.csv"),
        manifest=Path("reports/critical_omission_breaks_pericope_override.manifest.json"),
    )
    if summary is None or examples is None or by_verse is None or manifest is None:
        return
    totals = break_totals(
        summary,
        Path("reports/critical_omission_breaks_pericope_override_summary.csv"),
        failures,
    )
    require_equal(failures, "critical_omission_breaks_pericope term_rows", manifest.get("term_rows"), len(summary))
    require_equal(failures, "critical_omission_breaks_pericope deleted_blocks_used", manifest.get("deleted_blocks_used"), len(by_verse))
    require_equal(failures, "critical_omission_breaks_pericope broken_example_rows", manifest.get("broken_example_rows"), len(examples))
    require_equal(failures, "critical_omission_breaks_pericope broken total", totals["broken"], len(examples))
    require_doc_phrase(doc_texts, doc, f"Term rows: {format_int(len(summary))}.", failures)
    require_doc_phrase(
        doc_texts,
        doc,
        f"Deleted blocks used: {format_int(int(manifest['deleted_blocks_used']))}.",
        failures,
    )
    require_doc_phrase(
        doc_texts,
        doc,
        f"Deleted letters used: {format_int(int(manifest['deleted_letters_used']))}.",
        failures,
    )
    require_doc_phrase(
        doc_texts,
        doc,
        f"Broken example rows: {format_int(len(examples))}.",
        failures,
    )
    validate_pericope_passage_summaries(root, doc_texts, failures)
    validate_pericope_cohort_summaries(root, doc_texts, failures)
    validate_pericope_inverse(root, doc_texts, failures)


def validate_pericope_passage_summaries(
    root: Path, doc_texts: dict[Path, str], failures: list[str]
) -> None:
    doc = Path("docs/CRITICAL_OMISSION_BREAKS_PERICOPE_OVERRIDE.md")
    for label, slug in PERICOPE_PASSAGES:
        summary_path = Path(
            f"reports/critical_omission_breaks_treat_as_deleted_{slug}_pericope_override_summary.csv"
        )
        examples_path = Path(
            f"reports/critical_omission_breaks_treat_as_deleted_{slug}_pericope_override_examples.csv"
        )
        summary = read_csv_rows(root, summary_path, failures, SUMMARY_REQUIRED_COLUMNS)
        examples = read_csv_rows(root, examples_path, failures, EXAMPLE_REQUIRED_COLUMNS)
        if summary is None or examples is None:
            continue
        broken = break_totals(summary, summary_path, failures)["broken"]
        require_equal(failures, f"{summary_path} broken total", broken, len(examples))
        require_doc_phrase(
            doc_texts,
            doc,
            f"{label}: {format_int(len(summary))} term rows, {format_int(broken)} broken hits.",
            failures,
        )


def validate_pericope_cohort_summaries(
    root: Path, doc_texts: dict[Path, str], failures: list[str]
) -> None:
    doc = Path("docs/CRITICAL_OMISSION_BREAKS_PERICOPE_OVERRIDE.md")
    generic_rows, generic_broken = read_summary_and_examples_count(
        root,
        failures,
        Path("reports/critical_omission_breaks_pericope_generic_summary.csv"),
        Path("reports/critical_omission_breaks_pericope_generic_examples.csv"),
    )
    if generic_rows is not None and generic_broken is not None:
        require_doc_phrase(
            doc_texts,
            doc,
            f"Generic-only run: {format_int(generic_rows)} term rows, {format_int(generic_broken)} broken example rows.",
            failures,
        )
    rows, broken = read_summary_and_examples_count(
        root,
        failures,
        Path("reports/critical_omission_breaks_treat_as_deleted_pericope_adulterae_pericope_generic_summary.csv"),
        Path("reports/critical_omission_breaks_treat_as_deleted_pericope_adulterae_pericope_generic_examples.csv"),
    )
    if rows is not None and broken is not None:
        require_doc_phrase(
            doc_texts,
            doc,
            f"Generic-only Pericope Adulterae passage summary: {format_int(rows)} term rows, {format_int(broken)} broken hits.",
            failures,
        )
    thematic_rows, thematic_broken = read_summary_and_examples_count(
        root,
        failures,
        Path("reports/critical_omission_breaks_pericope_thematic_summary.csv"),
        Path("reports/critical_omission_breaks_pericope_thematic_examples.csv"),
    )
    if thematic_rows is not None and thematic_broken is not None:
        require_doc_phrase(
            doc_texts,
            doc,
            f"Pericope-thematic-only run: {format_int(thematic_rows)} term rows, {format_int(thematic_broken)} broken example row.",
            failures,
        )
    rows, broken = read_summary_and_examples_count(
        root,
        failures,
        Path("reports/critical_omission_breaks_treat_as_deleted_pericope_adulterae_pericope_thematic_summary.csv"),
        Path("reports/critical_omission_breaks_treat_as_deleted_pericope_adulterae_pericope_thematic_examples.csv"),
    )
    if rows is not None and broken is not None:
        require_doc_phrase(
            doc_texts,
            doc,
            f"Pericope-thematic-only Pericope Adulterae passage summary: {format_int(rows)} term row, {format_int(broken)} broken hit.",
            failures,
        )
    control_summary = read_csv_rows(
        root,
        Path("reports/critical_omission_breaks_pericope_frequency_controls_summary.csv"),
        failures,
        SUMMARY_REQUIRED_COLUMNS,
    )
    control_examples = read_csv_rows(
        root,
        Path("reports/critical_omission_breaks_pericope_frequency_controls_examples.csv"),
        failures,
        EXAMPLE_REQUIRED_COLUMNS,
    )
    if control_summary is not None and control_examples is not None:
        control_broken = break_totals(
            control_summary,
            Path("reports/critical_omission_breaks_pericope_frequency_controls_summary.csv"),
            failures,
        )["broken"]
        require_equal(failures, "pericope frequency control broken total", control_broken, len(control_examples))
        frequency_rows = [
            row
            for row in control_summary
            if row.get("term_source") == "terms/pericope_adulterae_frequency_controls.csv"
        ]
        frequency_broken = sum_int(
            frequency_rows,
            "broken_total_hits",
            Path("reports/critical_omission_breaks_pericope_frequency_controls_summary.csv"),
            failures,
        )
        require_doc_phrase(doc_texts, doc, f"Term rows: {format_int(len(control_summary))}.", failures)
        require_doc_phrase(
            doc_texts,
            doc,
            f"Broken example rows: {format_int(len(control_examples))}.",
            failures,
        )
        require_doc_phrase(
            doc_texts,
            doc,
            f"Frequency-control rows: {format_int(len(frequency_rows))}.",
            failures,
        )
        require_doc_phrase(
            doc_texts,
            doc,
            f"Frequency-control broken hits: {format_int(frequency_broken)}.",
            failures,
        )
    for label, slug in PERICOPE_PASSAGES[:2]:
        rows, broken = read_summary_and_examples_count(
            root,
            failures,
            Path(
                f"reports/critical_omission_breaks_treat_as_deleted_{slug}_pericope_frequency_controls_summary.csv"
            ),
            Path(
                f"reports/critical_omission_breaks_treat_as_deleted_{slug}_pericope_frequency_controls_examples.csv"
            ),
        )
        if rows is not None and broken is not None:
            require_doc_phrase(
                doc_texts,
                doc,
                f"{label} passage summary: {format_int(rows)} term rows, {format_int(broken)} broken hits.",
                failures,
            )


def validate_pericope_inverse(
    root: Path, doc_texts: dict[Path, str], failures: list[str]
) -> None:
    doc = Path("docs/CRITICAL_OMISSION_BREAKS_PERICOPE_OVERRIDE.md")
    rows = read_csv_rows(
        root,
        Path("reports/critical_omission_breaks_pericope_inverse.csv"),
        failures,
        ("corpus", "documented_jesus_center_hits", "broken_after_removal", "status"),
    )
    manifest = read_json_object(
        root,
        Path("reports/critical_omission_breaks_pericope_inverse.manifest.json"),
        failures,
    )
    if rows is None or manifest is None:
        return
    require_equal(failures, "critical_omission_breaks_pericope_inverse rows", manifest.get("rows"), len(rows))
    for row in rows:
        require_doc_phrase(
            doc_texts,
            doc,
            f"{row['corpus']}: {row['documented_jesus_center_hits']} documented hit, destroyed after Pericope removal.",
            failures,
        )


def read_break_run(
    root: Path,
    failures: list[str],
    *,
    summary: Path,
    examples: Path,
    by_verse: Path,
    manifest: Path,
) -> tuple[list[dict[str, str]] | None, list[dict[str, str]] | None, list[dict[str, str]] | None, dict[str, Any] | None]:
    return (
        read_csv_rows(root, summary, failures, SUMMARY_REQUIRED_COLUMNS),
        read_csv_rows(root, examples, failures, EXAMPLE_REQUIRED_COLUMNS),
        read_csv_rows(root, by_verse, failures, BY_VERSE_REQUIRED_COLUMNS),
        read_json_object(root, manifest, failures),
    )


def read_summary_and_examples_count(
    root: Path,
    failures: list[str],
    summary_path: Path,
    examples_path: Path,
) -> tuple[int | None, int | None]:
    summary = read_csv_rows(root, summary_path, failures, SUMMARY_REQUIRED_COLUMNS)
    examples = read_csv_rows(root, examples_path, failures, EXAMPLE_REQUIRED_COLUMNS)
    if summary is None or examples is None:
        return None, None
    broken = break_totals(summary, summary_path, failures)["broken"]
    require_equal(failures, f"{summary_path} broken total", broken, len(examples))
    return len(summary), broken


def read_csv_rows(
    root: Path,
    relative: Path,
    failures: list[str],
    required_columns: tuple[str, ...],
) -> list[dict[str, str]] | None:
    path = root / relative
    if not path.exists():
        failures.append(f"{relative} is missing")
        return None
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        missing = [column for column in required_columns if column not in fieldnames]
        if missing:
            failures.append(f"{relative} missing columns: {', '.join(missing)}")
        return list(reader)


def read_json_object(root: Path, relative: Path, failures: list[str]) -> dict[str, Any] | None:
    path = root / relative
    if not path.exists():
        failures.append(f"{relative} is missing")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"{relative} is invalid JSON: {exc}")
        return None
    if not isinstance(data, dict):
        failures.append(f"{relative} JSON root must be an object")
        return None
    return data


def break_totals(rows: list[dict[str, str]], source: Path, failures: list[str]) -> dict[str, int]:
    return {
        "removed": sum_int(rows, "broken_removed_letter_hits", source, failures),
        "spacing": sum_int(rows, "broken_spacing_hits", source, failures),
        "broken": sum_int(rows, "broken_total_hits", source, failures),
        "preserved": sum_int(rows, "preserved_across_omission_hits", source, failures),
    }


def sum_int(
    rows: list[dict[str, str]], column: str, source: Path, failures: list[str]
) -> int:
    total = 0
    for index, row in enumerate(rows, start=2):
        try:
            total += int(row[column])
        except (KeyError, ValueError):
            failures.append(f"{source} has non-integer {column} at CSV row {index}")
    return total


def require_equal(failures: list[str], label: str, actual: object, expected: object) -> None:
    if actual != expected:
        failures.append(f"{label} is {actual}, expected {expected}")


def require_doc_phrase(
    doc_texts: dict[Path, str],
    doc: Path,
    phrase: str,
    failures: list[str],
) -> None:
    if normalize_space(phrase) not in doc_texts[doc]:
        failures.append(f"{doc} missing artifact-derived phrase: {phrase}")


def format_int(value: int) -> str:
    return f"{value:,}"


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
