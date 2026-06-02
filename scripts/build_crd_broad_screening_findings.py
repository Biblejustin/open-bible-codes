#!/usr/bin/env python3
"""Build tracked summaries for ignored broad CRD screening artifacts."""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import json
from math import isfinite
from pathlib import Path

from els.term_display import display_term
from scripts.json_utils import read_json_object


TERM_FILES_DIR = Path("terms")


@dataclass(frozen=True)
class RunPaths:
    label: str
    short_label: str
    report_path: Path
    docs_path: Path
    out_dir: Path
    prepare_target: str
    run_target: str
    report_target: str
    queue_target: str
    center_word_targets: tuple[str, ...]


SELF = RunPaths(
    label="Self-Surface",
    short_label="self",
    report_path=Path("reports/crd_self_surface/CRD_SELF_SURFACE_REPORT.md"),
    docs_path=Path("docs/CRD_SELF_SURFACE_BROAD_SCREENING_FINDINGS.md"),
    out_dir=Path("reports/crd_self_surface"),
    prepare_target="crd-self-surface-prepare",
    run_target="crd-self-surface-run",
    report_target="crd-self-surface-report",
    queue_target="crd-self-surface-queue",
    center_word_targets=(
        "crd-self-surface-center-word",
        "crd-self-surface-center-word-density",
        "crd-self-surface-center-word-queue",
        "crd-self-surface-center-word-packet",
        "crd-self-surface-center-word-presence",
    ),
)

CONCEPT = RunPaths(
    label="Concept-Surface",
    short_label="concept",
    report_path=Path("reports/crd_concept_surface/CRD_CONCEPT_SURFACE_REPORT.md"),
    docs_path=Path("docs/CRD_CONCEPT_SURFACE_BROAD_SCREENING_FINDINGS.md"),
    out_dir=Path("reports/crd_concept_surface"),
    prepare_target="crd-concept-surface-prepare",
    run_target="crd-concept-surface-run",
    report_target="crd-concept-surface-report",
    queue_target="crd-concept-surface-queue",
    center_word_targets=(
        "crd-concept-surface-center-word",
        "crd-concept-surface-center-word-density",
        "crd-concept-surface-center-word-queue",
        "crd-concept-surface-center-word-packet",
        "crd-concept-surface-center-word-presence",
    ),
)


def main() -> int:
    self_summary = read_summary(SELF)
    concept_summary = read_summary(CONCEPT)
    write_summary_doc(SELF, self_summary, concept_summary)
    write_summary_doc(CONCEPT, concept_summary, self_summary)
    print(SELF.docs_path)
    print(CONCEPT.docs_path)
    return 0


def read_summary(paths: RunPaths) -> dict[str, object]:
    out = paths.out_dir
    manifest = read_json_object(out / "manifest.json")
    density_rows = read_csv(out / "density_matrix.csv")
    comparison_rows = read_csv(out / "bible_vs_control_summary.csv")
    scope_rows = read_csv(out / "relevance_scope_summary.csv")
    review_rows = read_csv(out / "review_queue.csv")
    center_word_rows = read_csv(out / "center_word_hits.csv")
    center_word_summary = read_csv(out / "center_word_bible_vs_control_summary.csv")
    center_word_presence = read_csv(out / "center_word_presence.csv")

    language_counts = Counter(row["language"] for row in comparison_rows)
    language_exceeds = Counter(
        row["language"] for row in comparison_rows if truthy(row["exceeds_secular_max"])
    )
    scope_counts: Counter[tuple[str, str]] = Counter()
    for row in scope_rows:
        scope_counts[(row["corpus_class"], row["match_scope"])] += int(row["relevant_hit_count"])

    return {
        "manifest": manifest,
        "classified_size": (out / "classified_hits.csv").stat().st_size,
        "density_rows": len(density_rows),
        "classified_rows": sum(int(row["total_centered_hits"]) for row in density_rows),
        "nonzero_density_rows": sum(int(row["total_centered_hits"]) > 0 for row in density_rows),
        "corpora_count": len({row["corpus"] for row in density_rows}),
        "comparison_rows": len(comparison_rows),
        "comparison_exceeds": sum(truthy(row["exceeds_secular_max"]) for row in comparison_rows),
        "comparison_secular_zero": sum(
            to_float(row["secular_max_density"]) == 0 for row in comparison_rows
        ),
        "comparison_bible_positive_secular_zero": sum(
            to_float(row["bible_max_density"]) > 0 and to_float(row["secular_max_density"]) == 0
            for row in comparison_rows
        ),
        "language_counts": language_counts,
        "language_exceeds": language_exceeds,
        "scope_counts": scope_counts,
        "review_rows": len(review_rows),
        "review_terms": len({row["term_id"] for row in review_rows}),
        "review_scope_counts": Counter(row["surface_match_scope"] for row in review_rows),
        "center_word_rows": len(center_word_rows),
        "center_word_terms": len({row["term_id"] for row in center_word_rows}),
        "center_word_summary_rows": len(center_word_summary),
        "center_word_exceeds": sum(
            truthy(row["exceeds_secular_max"]) for row in center_word_summary
        ),
        "center_word_bible_positive_secular_zero": sum(
            to_float(row["bible_max_density"]) > 0 and to_float(row["secular_max_density"]) == 0
            for row in center_word_summary
        ),
        "center_word_language_counts": Counter(row["language"] for row in center_word_summary),
        "center_word_language_exceeds": Counter(
            row["language"] for row in center_word_summary if truthy(row["exceeds_secular_max"])
        ),
        "center_word_presence_rows": len(center_word_presence),
        "center_word_presence_hits": sum(int(row["center_word_rows"]) for row in center_word_presence),
        "center_word_presence_forms": len({row["term"] for row in center_word_presence}),
        "center_word_presence_corpus_count_distribution": Counter(
            int(row["corpus_count"]) for row in center_word_presence
        ),
        "top_finite_ratios": top_finite_ratios(comparison_rows),
        "top_bible_positive_secular_zero": top_bible_positive_secular_zero(comparison_rows),
        "top_center_word_ratios": top_finite_ratios(center_word_summary, limit=6),
        "top_center_word_zero": top_bible_positive_secular_zero(center_word_summary, limit=6),
        "density_by_key": {
            (row["term_id"], row["corpus"]): int(row["relevant_centered_hits"])
            for row in density_rows
        },
        "density_rows_by_key": {(row["term_id"], row["corpus"]): row for row in density_rows},
    }


def write_summary_doc(
    paths: RunPaths,
    current: dict[str, object],
    other: dict[str, object],
) -> None:
    manifest = current["manifest"]
    assert isinstance(manifest, dict)
    scope_sentence = (
        "the visible surface context contain that same term spelling"
        if paths.short_label == "self"
        else "the visible surface context contain any locked surface spelling with the same language and same concept"
    )
    mode_note = (
        "Self-surface means hidden `X` is centered near visible `X`."
        if paths.short_label == "self"
        else "Concept-surface means hidden `X` is centered near a committed same-concept spelling."
    )
    lines = [
        f"# CRD {paths.label} Broad Screening Findings",
        "",
        (
            f"Status: local deterministic broad screening run completed at "
            f"`{manifest['run_timestamp']}`. Raw artifacts stay under ignored "
            f"`{paths.out_dir}/`; `classified_hits.csv` is {format_gb(current['classified_size'])}."
        ),
        "",
        "## Scope",
        "",
        (
            "This run asks a deterministic centered-relevance question: when a hidden ELS term "
            f"is centered, does {scope_sentence}? It uses exact normalized dictionary matching "
            "only; no fuzzy matching, embeddings, or live interpretation are used."
        ),
        "",
        (
            "The run uses the same Bible and secular-control corpus list as the CRD protocol, "
            "with `skip_range = 2..100`, `direction = both`, `min_term_length = 3`, and "
            "`max_hits_per_term = 200`."
        ),
        "",
        (
            "The input term set combines all committed term CSVs except "
            "`terms/crd_placeholder_terms.csv`, deduped by first-seen `term_id`. "
            f"{mode_note}"
        ),
        "",
        "## Outputs",
        "",
        f"- protocol: `{paths.out_dir / 'protocol.toml'}`",
        f"- preregistration: `{paths.out_dir / f'CRD_{paths.short_label.upper()}_SURFACE_PREREGISTRATION.md'}`",
        f"- dictionary: `{paths.out_dir / f'relevance_dictionary_{paths.short_label}_surface.toml'}`",
        f"- density matrix: `{paths.out_dir / 'density_matrix.csv'}`",
        f"- classified hits: `{paths.out_dir / 'classified_hits.csv'}`",
        f"- comparison report: `{paths.report_path}`",
        f"- compact review queue: `{paths.out_dir / 'review_queue.csv'}`",
        f"- Bible exact center-word hits: `{paths.out_dir / 'center_word_hits.csv'}`",
        f"- exact center-word version presence: `{paths.out_dir / 'center_word_presence.md'}`",
        "",
        "## Reproduce",
        "",
        "```bash",
        f"make {paths.prepare_target}",
        f"python3 -m scripts.run_crd_density {paths.out_dir / 'protocol.toml'} --classifier-mode deterministic --resume --force-reset",
        "make report-db",
        f"make {paths.report_target}",
        f"make {paths.queue_target}",
        *[f"make {target}" for target in paths.center_word_targets],
        "make crd-broad-screening-findings",
        "make crd-center-word-findings",
        "```",
        "",
        "## Run Size",
        "",
        f"- density rows: {current['density_rows']:,}",
        f"- term/control comparison rows: {current['comparison_rows']:,}",
        f"- classified hit rows: {current['classified_rows']:,}",
        f"- corpora with output: {current['corpora_count']:,}",
        f"- nonzero `(term, corpus)` density rows: {current['nonzero_density_rows']:,}",
        f"- compact review queue rows: {current['review_rows']:,}",
        f"- compact review queue selected terms: {current['review_terms']:,}",
        f"- exact center-word review queue rows: {review_queue_count(paths.out_dir / 'center_word_review_queue.csv'):,}",
        f"- exact center-word review queue selected terms: {review_queue_terms(paths.out_dir / 'center_word_review_queue.csv'):,}",
        f"- runtime: {manifest['duration_seconds']:.3f} seconds",
        f"- API calls: {manifest['total_api_calls_made']}",
        f"- estimated API cost: {manifest['estimated_cost_usd']} USD",
        "",
        "## Headline Counts",
        "",
        (
            f"- `exceeds_secular_max = true`: {current['comparison_exceeds']:,} / "
            f"{current['comparison_rows']:,} terms"
        ),
        (
            f"- rows with secular max density = 0: {current['comparison_secular_zero']:,} / "
            f"{current['comparison_rows']:,} terms"
        ),
        (
            f"- rows with Bible max > 0 and secular max = 0: "
            f"{current['comparison_bible_positive_secular_zero']:,} / {current['comparison_rows']:,} terms"
        ),
        *language_lines(current["language_counts"], current["language_exceeds"]),
        "",
        (
            "Large numbers of secular-zero rows are review-priority flags, not automatic claim "
            "promotions. They can reflect dictionary vocabulary and control-corpus coverage."
        ),
        "",
        "## Surface Match Scope",
        "",
        "Relevant classified-hit rows by scope:",
        "",
        *scope_lines(current["scope_counts"]),
        "",
        "Compact review queue scope:",
        "",
        *counter_lines(current["review_scope_counts"]),
        "",
        (
            "The exact `center_word` scope is the strictest form: the hidden term is centered "
            "directly on the visible matching or same-concept word. `center_verse` and `span` "
            "remain broader contextual flags and should be reviewed separately."
        ),
        "",
        "## Strongest Finite Bible-Vs-Control Ratios",
        "",
        ratio_table(current["top_finite_ratios"]),
        "",
        "## Strongest Bible Hits With Secular Max Zero",
        "",
        zero_table(current["top_bible_positive_secular_zero"]),
        "",
        "## Exact Center-Word Subset",
        "",
        f"- Bible center-word rows: {current['center_word_rows']:,}",
        f"- distinct term IDs with Bible center-word rows: {current['center_word_terms']:,}",
        f"- exact center-word presence rows: {current['center_word_presence_rows']:,}",
        f"- distinct visible spellings in presence output: {current['center_word_presence_forms']:,}",
        (
            f"- center-word-only summary rows: {current['center_word_summary_rows']:,}; "
            f"`exceeds_secular_max = true`: {current['center_word_exceeds']:,}"
        ),
        (
            f"- Bible-positive / secular-zero center-word terms: "
            f"{current['center_word_bible_positive_secular_zero']:,}"
        ),
        *language_lines(
            current["center_word_language_counts"],
            current["center_word_language_exceeds"],
            prefix="center-word exceeds",
        ),
        f"- corpus-count distribution: {format_distribution(current['center_word_presence_corpus_count_distribution'])}",
        "",
        "Top finite center-word-only ratios:",
        "",
        ratio_table(current["top_center_word_ratios"]),
        "",
        "Top Bible-positive / secular-zero center-word terms:",
        "",
        zero_table(current["top_center_word_zero"]),
        "",
    ]

    if paths.short_label == "concept":
        lines.extend(concept_delta_section(current, other))

    lines.extend(
        [
            "## Interpretation Notes",
            "",
            f"- This run is about {paths.short_label}-surface coincidence; all broader interpretation remains downstream review.",
            "- The `center_word` subset is the clearest review surface and is reported separately from verse/span relevance.",
            "- Duplicate term IDs from different claim lists were deduped by first-seen ID for this local run, but duplicate concepts with different IDs remain visible.",
            "- The large classified-hit file is intentionally ignored; the DuckDB mirror is used for fast summaries.",
            "- LLM and parallel modes require audit-log review before interpretation.",
            "- Interpret results only against the dictionary and preregistration hashes recorded in the manifest.",
            "",
        ]
    )
    paths.docs_path.write_text("\n".join(lines), encoding="utf-8")


def concept_delta_section(concept: dict[str, object], self_summary: dict[str, object]) -> list[str]:
    concept_by_key = concept["density_by_key"]
    self_by_key = self_summary["density_by_key"]
    concept_rows = concept["density_rows_by_key"]
    assert isinstance(concept_by_key, dict)
    assert isinstance(self_by_key, dict)
    assert isinstance(concept_rows, dict)
    changed = []
    newly_nonzero = 0
    for key, concept_hits in concept_by_key.items():
        self_hits = int(self_by_key.get(key, 0))
        added = int(concept_hits) - self_hits
        if added != 0:
            changed.append((added, key, self_hits, int(concept_hits), concept_rows[key]))
        if self_hits == 0 and int(concept_hits) > 0:
            newly_nonzero += 1
    changed.sort(reverse=True, key=lambda item: item[0])
    lines = [
        "## Delta Versus Self-Surface Run",
        "",
        (
            f"The concept-surface dictionary changed {len(changed):,} `(term, corpus)` "
            f"density rows compared with self-surface and created {newly_nonzero:,} newly nonzero rows."
        ),
        "",
        "Largest increases by added relevant centered hits:",
        "",
        "| Term | Corpus | Concept | Self hits | Concept hits | Added hits |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    for added, _key, self_hits, concept_hits, row in changed[:10]:
        lines.append(
            "| "
            + " | ".join(
                [
                    term_cell(row),
                    row["corpus"],
                    row["concept"],
                    str(self_hits),
                    str(concept_hits),
                    str(added),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            (
                "Same-concept expansion broadens recall, but it also broadens control hits. "
                "Treat concept-surface rows as a review queue, not as stronger evidence by default."
            ),
            "",
        ]
    )
    return lines


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def truthy(value: str) -> bool:
    return value.strip().lower() == "true"


def to_float(value: str) -> float:
    if value.strip() == "":
        return 0.0
    return float(value)


def top_finite_ratios(rows: list[dict[str, str]], *, limit: int = 10) -> list[dict[str, str]]:
    finite_rows = []
    for row in rows:
        ratio_text = row.get("ratio", "")
        if not ratio_text:
            continue
        ratio = float(ratio_text)
        if isfinite(ratio):
            finite_rows.append(row)
    finite_rows.sort(key=lambda row: float(row["ratio"]), reverse=True)
    return finite_rows[:limit]


def top_bible_positive_secular_zero(rows: list[dict[str, str]], *, limit: int = 10) -> list[dict[str, str]]:
    zero_rows = [
        row
        for row in rows
        if to_float(row["bible_max_density"]) > 0 and to_float(row["secular_max_density"]) == 0
    ]
    zero_rows.sort(key=lambda row: float(row["bible_max_density"]), reverse=True)
    return zero_rows[:limit]


def ratio_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "| Term | Language | Bible max | Bible corpus | Secular max | Secular corpus | Ratio |",
        "| --- | --- | ---: | --- | ---: | --- | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    term_cell(row),
                    row["language"],
                    row["bible_max_density"],
                    row["bible_max_corpus"],
                    row["secular_max_density"],
                    row["secular_max_corpus"],
                    row["ratio"],
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def zero_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "| Term | Language | Bible max | Bible corpus |",
        "| --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join([term_cell(row), row["language"], row["bible_max_density"], row["bible_max_corpus"]])
            + " |"
        )
    return "\n".join(lines)


def term_cell(row: dict[str, str]) -> str:
    return f"{display_term(row['term'], english=term_concept(row) or None)}<br>`{row['term_id']}`"


def term_concept(row: dict[str, str]) -> str:
    return (
        row.get("concept", "").strip()
        or row.get("term_concept", "").strip()
        or term_concepts_by_id().get(row["term_id"], "")
    )


@lru_cache(maxsize=1)
def term_concepts_by_id() -> dict[str, str]:
    concepts: dict[str, str] = {}
    if not TERM_FILES_DIR.exists():
        return concepts
    for path in sorted(TERM_FILES_DIR.glob("*.csv")):
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                term_id = row.get("term_id", "").strip()
                concept = row.get("concept", "").strip()
                if term_id and concept and term_id not in concepts:
                    concepts[term_id] = concept
    return concepts


def language_lines(
    counts: Counter[str],
    exceeds: Counter[str],
    *,
    prefix: str = "exceeds",
) -> list[str]:
    languages = sorted(set(counts) | set(exceeds))
    return [
        f"- {language.title()} {prefix}: {exceeds.get(language, 0):,} / {counts.get(language, 0):,}"
        for language in languages
    ]


def scope_lines(scope_counts: Counter[tuple[str, str]]) -> list[str]:
    keys = [
        ("bible", "center_word"),
        ("bible", "center_verse"),
        ("bible", "span"),
        ("secular_control", "center_word"),
        ("secular_control", "center_verse"),
        ("secular_control", "span"),
    ]
    return [f"- `{corpus_class}.{scope}`: {scope_counts.get((corpus_class, scope), 0):,}" for corpus_class, scope in keys]


def counter_lines(counter: Counter[str]) -> list[str]:
    return [f"- `{key}`: {value:,}" for key, value in sorted(counter.items())]


def format_distribution(counter: Counter[int]) -> str:
    parts = []
    for corpus_count, count in sorted(counter.items(), reverse=True):
        noun = "term" if count == 1 else "terms"
        label_noun = "label" if corpus_count == 1 else "labels"
        parts.append(f"{count} {noun} in {corpus_count} corpus {label_noun}")
    return ", ".join(parts)


def format_gb(size: object) -> str:
    return f"{int(size) / 1_000_000_000:.2f} GB"


def review_queue_count(path: Path) -> int:
    return len(read_csv(path))


def review_queue_terms(path: Path) -> int:
    return len({row["term_id"] for row in read_csv(path)})


if __name__ == "__main__":
    raise SystemExit(main())
