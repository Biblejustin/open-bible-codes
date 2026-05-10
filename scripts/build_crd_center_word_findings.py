#!/usr/bin/env python3
"""Build tracked CRD exact center-word findings from local CRD artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any, cast

from els.term_display import KNOWN_TERMS, display_term, normalized_script_key
from scripts.build_crd_center_word_presence import build_presence_rows


DEFAULT_SELF_HITS = Path("reports/crd_self_surface/center_word_hits.csv")
DEFAULT_CONCEPT_HITS = Path("reports/crd_concept_surface/center_word_hits.csv")
DEFAULT_SELF_SUMMARY = Path("reports/crd_self_surface/center_word_bible_vs_control_summary.csv")
DEFAULT_CONCEPT_SUMMARY = Path("reports/crd_concept_surface/center_word_bible_vs_control_summary.csv")
DEFAULT_SELF_PRESENCE = Path("reports/crd_self_surface/center_word_presence.csv")
DEFAULT_SELF_VS_CONCEPT_OUT = Path("docs/CRD_CENTER_WORD_SELF_VS_CONCEPT_FINDINGS.md")
DEFAULT_VERSION_PRESENCE_OUT = Path("docs/CRD_CENTER_WORD_VERSION_PRESENCE_FINDINGS.md")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    self_hits = read_dicts(args.self_hits)
    concept_hits = read_dicts(args.concept_hits)
    self_summary = read_dicts(args.self_summary)
    concept_summary = read_dicts(args.concept_summary)
    presence_rows = (
        read_dicts(args.self_presence)
        if args.self_presence.exists()
        else build_presence_rows(args.self_hits, args.self_summary, sample_refs=args.sample_refs)
    )

    args.self_vs_concept_out.parent.mkdir(parents=True, exist_ok=True)
    args.version_presence_out.parent.mkdir(parents=True, exist_ok=True)
    args.self_vs_concept_out.write_text(
        self_vs_concept_markdown(self_hits, concept_hits, self_summary, concept_summary),
        encoding="utf-8",
    )
    args.version_presence_out.write_text(version_presence_markdown(presence_rows, self_hits), encoding="utf-8")
    print(args.self_vs_concept_out)
    print(args.version_presence_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-hits", type=Path, default=DEFAULT_SELF_HITS)
    parser.add_argument("--concept-hits", type=Path, default=DEFAULT_CONCEPT_HITS)
    parser.add_argument("--self-summary", type=Path, default=DEFAULT_SELF_SUMMARY)
    parser.add_argument("--concept-summary", type=Path, default=DEFAULT_CONCEPT_SUMMARY)
    parser.add_argument("--self-presence", type=Path, default=DEFAULT_SELF_PRESENCE)
    parser.add_argument("--self-vs-concept-out", type=Path, default=DEFAULT_SELF_VS_CONCEPT_OUT)
    parser.add_argument("--version-presence-out", type=Path, default=DEFAULT_VERSION_PRESENCE_OUT)
    parser.add_argument("--sample-refs", type=int, default=6)
    return parser


def self_vs_concept_markdown(
    self_hits: list[dict[str, str]],
    concept_hits: list[dict[str, str]],
    self_summary: list[dict[str, str]],
    concept_summary: list[dict[str, str]],
) -> str:
    self_keys = hit_key_set(self_hits)
    concept_keys = hit_key_set(concept_hits)
    summary_changes = changed_summary_rows(self_summary, concept_summary)
    secular_changes = [
        row
        for row in summary_changes
        if row["bible_changed"] == "false"
        and row["exceeds_changed"] == "false"
        and (row["self_secular_max_density"] != row["concept_secular_max_density"])
    ]
    presence_counts = presence_counts_from_hits(self_hits)
    language_counts = term_language_counts_from_hits(self_hits)
    corpus_count_distribution = Counter(str(len(corpora)) for corpora in presence_counts.values())
    lines = [
        "# CRD Center-Word Self Vs Concept Findings",
        "",
        "Status: local comparison generated from ignored outputs under `reports/crd_self_surface/` and `reports/crd_concept_surface/`.",
        "",
        "## Scope",
        "",
        "This comparison checks whether the broader concept-surface CRD dictionary changes the strict exact center-word result relative to the self-surface dictionary.",
        "",
        "Self-surface means hidden `X` is centered on visible `X`.",
        "",
        "Concept-surface means hidden `X` is centered on a visible spelling from the same committed `(language, concept)` group.",
        "",
        "The exact `center_word` subset is stricter than both verse-level and span-level relevance, because the matched surface keyword must be the centered visible word.",
        "",
        "## Result",
        "",
        "The Bible exact center-word hit set is identical in the self-surface and concept-surface runs."
        if self_keys == concept_keys
        else "The Bible exact center-word hit set differs between the self-surface and concept-surface runs.",
        "",
        f"- self-surface Bible exact center-word rows: {len(self_keys):,}",
        f"- concept-surface Bible exact center-word rows: {len(concept_keys):,}",
        f"- matching row key set: {str(self_keys == concept_keys).lower()}",
        f"- self-only Bible rows: {len(self_keys - concept_keys):,}",
        f"- concept-only Bible rows: {len(concept_keys - self_keys):,}",
        "",
        "The center-word density summaries are also effectively stable:",
        "",
        f"- term rows compared: {len(index_by_term(self_summary)):,}",
        f"- rows with changed summary values: {len(summary_changes):,}",
        f"- rows with changed Bible max density or Bible max corpus: {sum(row['bible_changed'] == 'true' for row in summary_changes):,}",
        f"- rows with changed `exceeds_secular_max`: {sum(row['exceeds_changed'] == 'true' for row in summary_changes):,}",
        f"- rows with changed secular max density or corpus: {sum(row['secular_changed'] == 'true' for row in summary_changes):,}",
    ]
    if secular_changes:
        lines.extend(
            [
                "",
                "The changed rows are secular-control changes only:",
                "",
                "| Term | Language | Self secular max | Self secular corpus | Concept secular max | Concept secular corpus |",
                "| --- | --- | ---: | --- | ---: | --- |",
            ]
        )
        for row in secular_changes[:20]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        term_cell(row),
                        md(row["language"]),
                        row["self_secular_max_density"],
                        md(row["self_secular_max_corpus"]),
                        row["concept_secular_max_density"],
                        md(row["concept_secular_max_corpus"]),
                    ]
                )
                + " |"
            )
    lines.extend(
        [
            "",
            "The exact center-word version-presence view contains:",
            "",
            f"- exact center-word term rows: {len(presence_counts):,}",
            f"- exact center-word hit rows: {len(self_hits):,}",
            f"- language distribution: {format_named_counts(language_counts)}",
            f"- corpus-count distribution: {format_corpus_count_distribution(corpus_count_distribution)}",
            "",
            "## Interpretation",
            "",
            "For the strict exact center-word question, concept-surface expansion did not add Bible hits and did not change any exceedance decisions. That means the current exact center-word Bible signal can be reviewed from the self-surface output without losing any concept-surface Bible rows.",
            "",
            "Concept-surface remains useful for broader center-verse and span review, but exact center-word reporting should stay separated from those wider scopes.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def version_presence_markdown(rows: list[dict[str, str]], hit_rows: list[dict[str, str]]) -> str:
    language_counts = Counter(row["language"] for row in rows)
    corpus_counts = Counter(row["corpus_count"] for row in rows)
    exceeding = [row for row in rows if row.get("exceeds_secular_max") == "true"]
    distinct_rows = distinct_surface_rows(rows, hit_rows)
    distinct_hit_path_count = len(distinct_surface_hit_paths(hit_rows))
    lines = [
        "# CRD Center-Word Version Presence Findings",
        "",
        "Status: local summary generated from ignored CRD exact center-word outputs.",
        "",
        "## Scope",
        "",
        "This report summarizes which Bible edition labels contain exact center-word CRD hits. It uses the self-surface exact center-word subset because the concept-surface run has the same Bible exact center-word row keys.",
        "",
        "This answers a source-distribution question: a centered pattern may be source-specific, multi-version, or broadly stable. The report does not require every pattern to appear in every edition.",
        "",
        "## Outputs",
        "",
        "- self-surface presence CSV: `reports/crd_self_surface/center_word_presence.csv`",
        "- self-surface presence Markdown: `reports/crd_self_surface/center_word_presence.md`",
        "- concept-surface presence CSV: `reports/crd_concept_surface/center_word_presence.csv`",
        "- concept-surface presence Markdown: `reports/crd_concept_surface/center_word_presence.md`",
        "",
        "## Reproduce",
        "",
        "```bash",
        "make crd-self-surface-center-word-presence",
        "make crd-concept-surface-center-word-presence",
        "make crd-center-word-findings",
        "```",
        "",
        "## Summary",
        "",
        f"- exact center-word term rows: {len(rows):,}",
        f"- distinct normalized surface forms: {len(distinct_rows):,}",
        f"- exact center-word hit rows: {sum(int(row['center_word_rows']) for row in rows):,}",
        f"- distinct normalized surface hit paths: {distinct_hit_path_count:,}",
        f"- terms exceeding secular max in the center-word-only summary: {len(exceeding):,}",
        f"- language distribution: {format_named_counts(language_counts)}",
        f"- corpus-count distribution: {format_corpus_count_distribution(corpus_counts)}",
        "",
        "## Strongest Distinct Surface Forms",
        "",
        "This table collapses duplicate term IDs that use the same normalized hidden spelling. The raw term-row table remains below.",
        "",
        "| Term | Language | Term rows | Unique paths | Corpus count | Corpora | Exceeds secular max | Bible max | Secular max |",
        "| --- | --- | ---: | ---: | ---: | --- | --- | ---: | ---: |",
    ]
    for row in distinct_rows[:20]:
        lines.append(
            "| "
            + " | ".join(
                [
                    term_cell(row),
                    md(row["language"]),
                    row["term_row_count"],
                    row["center_word_rows"],
                    row["corpus_count"],
                    md(row["corpora"].replace(";", "; ")),
                    row["exceeds_secular_max"],
                    row["bible_max_density"],
                    row["secular_max_density"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Strongest Multi-Version Rows",
            "",
            "| Term | Language | Rows | Corpus count | Corpora | Exceeds secular max | Bible max | Secular max |",
            "| --- | --- | ---: | ---: | --- | --- | ---: | ---: |",
        ]
    )
    for row in rows[:20]:
        lines.append(
            "| "
            + " | ".join(
                [
                    term_cell(row),
                    md(row["language"]),
                    row["center_word_rows"],
                    row["corpus_count"],
                    md(row["corpora"].replace(";", "; ")),
                    row["exceeds_secular_max"],
                    row["bible_max_density"],
                    row["secular_max_density"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Exact center-word presence is not all-or-nothing across editions.",
            "- Multi-version rows are useful for stability review, not automatic claim promotion.",
            "- Single-version rows remain visible because source-specific patterns are part of the stated hypothesis.",
            "- Bible-vs-control density remains necessary even when an exact center-word hit looks contextually strong.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def hit_key_set(rows: list[dict[str, str]]) -> set[str]:
    return {row["hit_id"] for row in rows if row.get("corpus_class") == "bible" and row.get("hit_id")}


def index_by_term(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["term_id"]: row for row in rows}


def changed_summary_rows(self_summary: list[dict[str, str]], concept_summary: list[dict[str, str]]) -> list[dict[str, str]]:
    self_by_term = index_by_term(self_summary)
    concept_by_term = index_by_term(concept_summary)
    rows: list[dict[str, str]] = []
    for term_id in sorted(set(self_by_term) & set(concept_by_term)):
        self_row = self_by_term[term_id]
        concept_row = concept_by_term[term_id]
        bible_changed = (
            self_row.get("bible_max_density") != concept_row.get("bible_max_density")
            or self_row.get("bible_max_corpus") != concept_row.get("bible_max_corpus")
        )
        secular_changed = (
            self_row.get("secular_max_density") != concept_row.get("secular_max_density")
            or self_row.get("secular_max_corpus") != concept_row.get("secular_max_corpus")
        )
        exceeds_changed = self_row.get("exceeds_secular_max") != concept_row.get("exceeds_secular_max")
        if bible_changed or secular_changed or exceeds_changed:
            rows.append(
                {
                    "term_id": term_id,
                    "term": self_row.get("term", ""),
                    "concept": self_row.get("concept", ""),
                    "language": self_row.get("language", ""),
                    "self_secular_max_density": self_row.get("secular_max_density", ""),
                    "self_secular_max_corpus": self_row.get("secular_max_corpus", ""),
                    "concept_secular_max_density": concept_row.get("secular_max_density", ""),
                    "concept_secular_max_corpus": concept_row.get("secular_max_corpus", ""),
                    "bible_changed": str(bible_changed).lower(),
                    "secular_changed": str(secular_changed).lower(),
                    "exceeds_changed": str(exceeds_changed).lower(),
                }
            )
    return rows


def presence_counts_from_hits(rows: list[dict[str, str]]) -> dict[str, set[str]]:
    by_term: dict[str, set[str]] = {}
    for row in rows:
        by_term.setdefault(row["term_id"], set()).add(row.get("corpus", ""))
    return by_term


def term_language_counts_from_hits(rows: list[dict[str, str]]) -> Counter[str]:
    languages_by_term: dict[str, str] = {}
    for row in rows:
        languages_by_term.setdefault(row["term_id"], row.get("language", ""))
    return Counter(language for language in languages_by_term.values() if language)


def distinct_surface_rows(rows: list[dict[str, str]], hit_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = normalized_surface_group_key(row)
        if not key[1]:
            continue
        group = groups.setdefault(
            key,
            {
                "term": row.get("term", ""),
                "term_id": "",
                "concept": row.get("concept", ""),
                "language": row.get("language", ""),
                "term_ids": set(),
                "center_word_rows": 0,
                "corpora": set(),
                "exceeds_secular_max": False,
                "bible_max_density": 0.0,
                "secular_max_density": 0.0,
            },
        )
        term_ids = cast(set[str], group["term_ids"])
        corpora = cast(set[str], group["corpora"])
        if row.get("term_id"):
            term_ids.add(row["term_id"])
        corpora.update(part for part in row.get("corpora", "").split(";") if part)
        group["center_word_rows"] = int(group["center_word_rows"]) + int(row.get("center_word_rows") or 0)
        group["exceeds_secular_max"] = bool(group["exceeds_secular_max"]) or row.get("exceeds_secular_max") == "true"
        group["bible_max_density"] = max(float(group["bible_max_density"]), parse_number(row.get("bible_max_density", "")))
        group["secular_max_density"] = max(
            float(group["secular_max_density"]),
            parse_number(row.get("secular_max_density", "")),
        )

    hit_paths_by_group: dict[tuple[str, str], set[tuple[str, ...]]] = {}
    for row in hit_rows:
        key = normalized_surface_group_key(row)
        if not key[1]:
            continue
        hit_paths_by_group.setdefault(key, set()).add(distinct_surface_hit_path_key(row))

    collapsed: list[dict[str, str]] = []
    for key, group in groups.items():
        term_ids = sorted(cast(set[str], group["term_ids"]))
        corpora = sorted(cast(set[str], group["corpora"]))
        unique_paths = len(hit_paths_by_group.get(key, set())) or int(group["center_word_rows"])
        collapsed.append(
            {
                "term": str(group["term"]),
                "term_id": ", ".join(term_ids[:3]) + (", ..." if len(term_ids) > 3 else ""),
                "concept": str(group["concept"]),
                "language": str(group["language"]),
                "term_row_count": str(len(term_ids)),
                "center_word_rows": str(unique_paths),
                "corpus_count": str(len(corpora)),
                "corpora": ";".join(corpora),
                "exceeds_secular_max": str(bool(group["exceeds_secular_max"])).lower(),
                "bible_max_density": format_number(float(group["bible_max_density"])),
                "secular_max_density": format_number(float(group["secular_max_density"])),
            }
        )
    return sorted(
        collapsed,
        key=lambda row: (
            int(row["corpus_count"]),
            int(row["center_word_rows"]),
            parse_number(row["bible_max_density"]),
            row["term"],
        ),
        reverse=True,
    )


def normalized_surface_group_key(row: dict[str, str]) -> tuple[str, str]:
    language = row.get("language", "")
    term = row.get("term", "")
    script_key = normalized_script_key(term)
    if script_key:
        return language, script_key
    return language, "".join(char.lower() for char in term if char.isalnum())


def distinct_surface_hit_paths(rows: list[dict[str, str]]) -> set[tuple[str, ...]]:
    return {
        distinct_surface_hit_path_key(row)
        for row in rows
        if row.get("corpus_class", "bible") == "bible"
    }


def distinct_surface_hit_path_key(row: dict[str, str]) -> tuple[str, ...]:
    language, term_key = normalized_surface_group_key(row)
    return (
        language,
        term_key,
        row.get("corpus", ""),
        row.get("skip", ""),
        row.get("direction", ""),
        row.get("start_ref", ""),
        row.get("center_ref", ""),
        row.get("end_ref", ""),
        row.get("center_normalized_word", ""),
    )


def parse_number(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def format_number(value: float) -> str:
    if value == 0:
        return "0"
    return f"{value:.9g}"


def term_cell(row: dict[str, str]) -> str:
    term = row.get("term", "")
    term_id = row.get("term_id", "")
    if term:
        english = None if normalized_script_key(term) in KNOWN_TERMS else row.get("concept") or None
        return md(f"{display_term(term, english=english)}<br>`{term_id}`")
    return f"`{md(term_id)}`"


def format_named_counts(counter: Counter[str]) -> str:
    return ", ".join(f"{key.title()} {value:,}" for key, value in counter.most_common() if key)


def format_corpus_count_distribution(counter: Counter[str]) -> str:
    parts = []
    for key, value in sorted(counter.items(), key=lambda item: int(item[0]), reverse=True):
        noun = "term" if value == 1 else "terms"
        label_noun = "corpus label" if key == "1" else "corpus labels"
        parts.append(f"{value:,} {noun} in {key} {label_noun}")
    return ", ".join(parts)


def md(value: str) -> str:
    return value.replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
