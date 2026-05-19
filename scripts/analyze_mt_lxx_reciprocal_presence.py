#!/usr/bin/env python3
"""Compare concept-level ELS presence between MT Hebrew and LXX Greek."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

from els import __version__
from els.corpus import Corpus, load_corpus
from els.term_display import display_term
from scripts.analyze_hebrew_hit_version_presence import (
    CorpusSource,
    HitRecord,
    TermRow,
    canonical_ref,
    collect_hits_from_sources,
    parse_labeled_corpus_sources,
    read_terms,
)


DEFAULT_HEBREW_CORPUS = "MT_WLC=configs/example_oshb_wlc.toml"
DEFAULT_LXX_CORPUS = "LXX=configs/example_ebible_grclxx.toml"
DEFAULT_TERM_FILES = [
    Path("terms/theological_terms.csv"),
    Path("terms/prophetic_terms.csv"),
    Path("terms/biblical_tribes.csv"),
    Path("terms/biblical_festivals.csv"),
    Path("terms/biblical_calendar.csv"),
    Path("terms/biblical_narrative_names.csv"),
    Path("terms/biblical_prophets_cohort.csv"),
    Path("terms/eschatology_expanded_terms.csv"),
    Path("terms/isaiah53_servant_cohort.csv"),
    Path("terms/tabernacle_temple_terms.csv"),
    Path("terms/daniel_statue_metals.csv"),
    Path("terms/maccabean_apocrypha_names.csv"),
    Path("terms/frequency_anchors.csv"),
    Path("terms/null_controls.csv"),
]
OUT_DIR = Path("reports/mt_lxx_reciprocal_presence")
SUMMARY_OUT = OUT_DIR / "concept_summary.csv"
HITS_OUT = OUT_DIR / "hit_comparison.csv"
MD_OUT = Path("docs/MT_LXX_RECIPROCAL_PRESENCE.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"

SUMMARY_FIELDNAMES = [
    "concept",
    "category",
    "hebrew_term_ids",
    "greek_term_ids",
    "hebrew_terms",
    "greek_terms",
    "mt_hit_count",
    "lxx_hit_count",
    "mt_unique_center_refs",
    "lxx_unique_center_refs",
    "common_center_refs",
    "common_chapters",
    "mt_only_aligned_refs",
    "lxx_only_aligned_refs",
    "mt_unaligned_refs",
    "lxx_unaligned_refs",
    "presence_class",
    "read",
]

HIT_FIELDNAMES = [
    "side",
    "concept",
    "term_id",
    "category",
    "term",
    "normalized_term",
    "corpus",
    "skip",
    "direction",
    "start_ref",
    "center_ref",
    "end_ref",
    "counterpart_status",
    "counterpart_scope",
    "read",
]


@dataclass(frozen=True)
class CorpusRefs:
    verse_refs: frozenset[str]
    chapter_refs: frozenset[str]


@dataclass(frozen=True)
class HitView:
    side: str
    concept: str
    term_id: str
    category: str
    term: str
    normalized_term: str
    corpus: str
    skip: int
    direction: str
    start_ref: str
    center_ref: str
    end_ref: str


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    term_paths = args.terms or DEFAULT_TERM_FILES
    hebrew_terms = read_terms(
        term_paths,
        language="hebrew",
        concepts=args.concept,
        categories=args.category,
        term_ids=args.term_id,
        duplicate_policy="first",
    )
    greek_terms = read_terms(
        term_paths,
        language="greek",
        concepts=args.concept,
        categories=args.category,
        term_ids=args.term_id,
        duplicate_policy="first",
    )
    if not args.include_unpaired_concepts:
        paired = paired_concepts(hebrew_terms, greek_terms)
        hebrew_terms = [term for term in hebrew_terms if term.concept in paired]
        greek_terms = [term for term in greek_terms if term.concept in paired]

    mt_sources = parse_labeled_corpus_sources([args.hebrew_corpus])
    lxx_sources = parse_labeled_corpus_sources([args.lxx_corpus])
    mt_records = collect_language_hits(mt_sources, hebrew_terms, args)
    lxx_records = collect_language_hits(lxx_sources, greek_terms, args)
    mt_hits = hit_views("MT", mt_records)
    lxx_hits = hit_views("LXX", lxx_records)

    mt_refs = load_corpus_refs(mt_sources[0])
    lxx_refs = load_corpus_refs(lxx_sources[0])
    summary_rows = reciprocal_summary_rows(
        hebrew_terms,
        greek_terms,
        mt_hits,
        lxx_hits,
        mt_refs,
        lxx_refs,
    )
    comparison_rows = reciprocal_hit_rows(mt_hits, lxx_hits, mt_refs, lxx_refs)

    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.hits_out, HIT_FIELDNAMES, comparison_rows)
    write_markdown(args.markdown_out, summary_rows, comparison_rows, args)
    write_manifest(
        args,
        term_paths,
        mt_sources,
        lxx_sources,
        hebrew_terms,
        greek_terms,
        mt_hits,
        lxx_hits,
        started,
    )
    print(args.summary_out)
    print(args.hits_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, action="append", default=None)
    parser.add_argument("--concept", action="append", default=None)
    parser.add_argument("--category", action="append", default=None)
    parser.add_argument("--term-id", action="append", default=None)
    parser.add_argument("--include-unpaired-concepts", action="store_true")
    parser.add_argument("--hebrew-corpus", default=DEFAULT_HEBREW_CORPUS)
    parser.add_argument("--lxx-corpus", default=DEFAULT_LXX_CORPUS)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=100)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--min-term-length", type=int, default=3)
    parser.add_argument("--max-hits-per-term", type=int, default=100)
    parser.add_argument("--corpus-jobs", type=int, default=1)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--hits-out", type=Path, default=HITS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def paired_concepts(hebrew_terms: list[TermRow], greek_terms: list[TermRow]) -> set[str]:
    hebrew = {term.concept for term in hebrew_terms if term.concept}
    greek = {term.concept for term in greek_terms if term.concept}
    return hebrew & greek


def collect_language_hits(
    sources: list[CorpusSource],
    terms: list[TermRow],
    args: argparse.Namespace,
) -> list[HitRecord]:
    if not terms:
        return []
    collect_args = SimpleNamespace(
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        min_term_length=args.min_term_length,
        max_hits_per_term=args.max_hits_per_term,
        corpus_jobs=args.corpus_jobs,
    )
    records, _observed, _lookup, _normalized, _metadata = collect_hits_from_sources(
        sources,
        terms,
        collect_args,
    )
    return records


def hit_views(side: str, records: list[HitRecord]) -> list[HitView]:
    views: list[HitView] = []
    for record in records:
        hit = record.hit
        views.append(
            HitView(
                side=side,
                concept=record.term.concept,
                term_id=record.term.term_id,
                category=record.term.category,
                term=record.term.term,
                normalized_term=record.normalized_term,
                corpus=record.corpus,
                skip=hit.skip,
                direction=hit.direction,
                start_ref=canonical_ref(hit.start_ref),
                center_ref=canonical_ref(hit.center_ref),
                end_ref=canonical_ref(hit.end_ref),
            )
        )
    return views


def load_corpus_refs(source: CorpusSource) -> CorpusRefs:
    return corpus_refs(load_corpus(source.path))


def corpus_refs(corpus: Corpus) -> CorpusRefs:
    verse_refs = frozenset(canonical_ref(verse.ref) for verse in corpus.verses)
    chapter_refs = frozenset(chapter_ref(ref) for ref in verse_refs if chapter_ref(ref))
    return CorpusRefs(verse_refs=verse_refs, chapter_refs=chapter_refs)


def chapter_ref(ref: str) -> str:
    if not ref or " " not in ref or ":" not in ref:
        return ""
    book, rest = ref.rsplit(" ", 1)
    chapter = rest.split(":", 1)[0]
    try:
        return f"{book} {int(chapter)}"
    except ValueError:
        return ""


def reciprocal_summary_rows(
    hebrew_terms: list[TermRow],
    greek_terms: list[TermRow],
    mt_hits: list[HitView],
    lxx_hits: list[HitView],
    mt_refs: CorpusRefs,
    lxx_refs: CorpusRefs,
) -> list[dict[str, object]]:
    terms_by_concept = terms_grouped_by_concept(hebrew_terms, greek_terms)
    mt_by_concept = hits_grouped_by_concept(mt_hits)
    lxx_by_concept = hits_grouped_by_concept(lxx_hits)
    concepts = sorted(set(terms_by_concept) | set(mt_by_concept) | set(lxx_by_concept))
    rows = [
        reciprocal_summary_row(
            concept,
            terms_by_concept.get(concept, {"hebrew": [], "greek": []}),
            mt_by_concept.get(concept, []),
            lxx_by_concept.get(concept, []),
            mt_refs,
            lxx_refs,
        )
        for concept in concepts
    ]
    return sorted(rows, key=summary_sort_key)


def terms_grouped_by_concept(
    hebrew_terms: list[TermRow],
    greek_terms: list[TermRow],
) -> dict[str, dict[str, list[TermRow]]]:
    grouped: dict[str, dict[str, list[TermRow]]] = defaultdict(lambda: {"hebrew": [], "greek": []})
    for term in hebrew_terms:
        grouped[term.concept]["hebrew"].append(term)
    for term in greek_terms:
        grouped[term.concept]["greek"].append(term)
    return grouped


def hits_grouped_by_concept(hits: list[HitView]) -> dict[str, list[HitView]]:
    grouped: dict[str, list[HitView]] = defaultdict(list)
    for hit in hits:
        grouped[hit.concept].append(hit)
    return grouped


def reciprocal_summary_row(
    concept: str,
    terms: dict[str, list[TermRow]],
    mt_hits: list[HitView],
    lxx_hits: list[HitView],
    mt_refs: CorpusRefs,
    lxx_refs: CorpusRefs,
) -> dict[str, object]:
    mt_center_refs = {hit.center_ref for hit in mt_hits if hit.center_ref}
    lxx_center_refs = {hit.center_ref for hit in lxx_hits if hit.center_ref}
    mt_chapters = {chapter_ref(ref) for ref in mt_center_refs if chapter_ref(ref)}
    lxx_chapters = {chapter_ref(ref) for ref in lxx_center_refs if chapter_ref(ref)}
    common_refs = mt_center_refs & lxx_center_refs
    common_chapters = mt_chapters & lxx_chapters
    mt_only_aligned = {ref for ref in mt_center_refs - lxx_center_refs if ref in lxx_refs.verse_refs}
    lxx_only_aligned = {ref for ref in lxx_center_refs - mt_center_refs if ref in mt_refs.verse_refs}
    mt_unaligned = mt_center_refs - lxx_refs.verse_refs
    lxx_unaligned = lxx_center_refs - mt_refs.verse_refs
    presence = concept_presence_class(
        mt_hit_count=len(mt_hits),
        lxx_hit_count=len(lxx_hits),
        common_refs=common_refs,
        common_chapters=common_chapters,
    )
    hebrew_terms = terms.get("hebrew", [])
    greek_terms = terms.get("greek", [])
    categories = sorted({term.category for term in hebrew_terms + greek_terms if term.category})
    return {
        "concept": concept,
        "category": ",".join(categories),
        "hebrew_term_ids": ",".join(term.term_id for term in hebrew_terms),
        "greek_term_ids": ",".join(term.term_id for term in greek_terms),
        "hebrew_terms": "; ".join(term.term for term in hebrew_terms),
        "greek_terms": "; ".join(term.term for term in greek_terms),
        "mt_hit_count": len(mt_hits),
        "lxx_hit_count": len(lxx_hits),
        "mt_unique_center_refs": len(mt_center_refs),
        "lxx_unique_center_refs": len(lxx_center_refs),
        "common_center_refs": len(common_refs),
        "common_chapters": len(common_chapters),
        "mt_only_aligned_refs": len(mt_only_aligned),
        "lxx_only_aligned_refs": len(lxx_only_aligned),
        "mt_unaligned_refs": len(mt_unaligned),
        "lxx_unaligned_refs": len(lxx_unaligned),
        "presence_class": presence,
        "read": concept_read(presence, len(common_refs), len(common_chapters)),
    }


def concept_presence_class(
    *,
    mt_hit_count: int,
    lxx_hit_count: int,
    common_refs: set[str],
    common_chapters: set[str],
) -> str:
    if common_refs:
        return "mt_lxx_common_verse"
    if common_chapters:
        return "mt_lxx_common_chapter"
    if mt_hit_count and lxx_hit_count:
        return "both_present_different_loci"
    if mt_hit_count:
        return "mt_only_lxx_absent"
    if lxx_hit_count:
        return "lxx_only_mt_absent"
    return "absent_both_in_capped_scan"


def concept_read(presence: str, common_refs: int, common_chapters: int) -> str:
    if presence == "mt_lxx_common_verse":
        return f"concept has reciprocal MT/LXX ELS centers in {common_refs} shared verse ref(s)"
    if presence == "mt_lxx_common_chapter":
        return f"concept has reciprocal MT/LXX ELS centers in {common_chapters} shared chapter(s)"
    if presence == "both_present_different_loci":
        return "concept appears in both traditions, but not at the same aligned verse/chapter"
    if presence == "mt_only_lxx_absent":
        return "MT has capped-scan ELS hits; LXX counterpart has none"
    if presence == "lxx_only_mt_absent":
        return "LXX has capped-scan ELS hits; MT counterpart has none"
    return "no hits in either side under current caps"


def reciprocal_hit_rows(
    mt_hits: list[HitView],
    lxx_hits: list[HitView],
    mt_refs: CorpusRefs,
    lxx_refs: CorpusRefs,
) -> list[dict[str, object]]:
    mt_by_concept = hits_grouped_by_concept(mt_hits)
    lxx_by_concept = hits_grouped_by_concept(lxx_hits)
    rows: list[dict[str, object]] = []
    for hit in mt_hits:
        rows.append(hit_comparison_row(hit, lxx_by_concept.get(hit.concept, []), lxx_refs))
    for hit in lxx_hits:
        rows.append(hit_comparison_row(hit, mt_by_concept.get(hit.concept, []), mt_refs))
    return sorted(rows, key=hit_sort_key)


def hit_comparison_row(
    hit: HitView,
    counterpart_hits: list[HitView],
    counterpart_refs: CorpusRefs,
) -> dict[str, object]:
    status, scope = counterpart_status(hit, counterpart_hits, counterpart_refs)
    return {
        "side": hit.side,
        "concept": hit.concept,
        "term_id": hit.term_id,
        "category": hit.category,
        "term": hit.term,
        "normalized_term": hit.normalized_term,
        "corpus": hit.corpus,
        "skip": hit.skip,
        "direction": hit.direction,
        "start_ref": hit.start_ref,
        "center_ref": hit.center_ref,
        "end_ref": hit.end_ref,
        "counterpart_status": status,
        "counterpart_scope": scope,
        "read": hit_read(hit.side, status, scope),
    }


def counterpart_status(
    hit: HitView,
    counterpart_hits: list[HitView],
    counterpart_refs: CorpusRefs,
) -> tuple[str, str]:
    if hit.center_ref not in counterpart_refs.verse_refs:
        chapter = chapter_ref(hit.center_ref)
        if chapter and chapter in counterpart_refs.chapter_refs:
            return "alignment_broken_verse", "chapter_exists"
        return "alignment_broken_chapter", "chapter_absent"
    counterpart_center_refs = {other.center_ref for other in counterpart_hits}
    if hit.center_ref in counterpart_center_refs:
        return "mt_lxx_common" if hit.side == "MT" else "lxx_mt_common", "verse"
    hit_chapter = chapter_ref(hit.center_ref)
    counterpart_chapters = {chapter_ref(other.center_ref) for other in counterpart_hits}
    if hit_chapter and hit_chapter in counterpart_chapters:
        return "mt_lxx_common" if hit.side == "MT" else "lxx_mt_common", "chapter"
    return ("mt_only_lxx_absent" if hit.side == "MT" else "lxx_only_mt_absent"), "aligned_ref"


def hit_read(side: str, status: str, scope: str) -> str:
    if status.startswith("alignment_broken"):
        return f"{side} hit cannot be directly compared at {scope}"
    if status in {"mt_lxx_common", "lxx_mt_common"}:
        return f"counterpart concept hit present at same {scope}"
    if status == "mt_only_lxx_absent":
        return "MT hit center aligns to LXX ref, but no LXX concept hit there"
    if status == "lxx_only_mt_absent":
        return "LXX hit center aligns to MT ref, but no MT concept hit there"
    return "unclassified reciprocal state"


def summary_sort_key(row: dict[str, object]) -> tuple[int, str]:
    order = {
        "mt_lxx_common_verse": 0,
        "mt_lxx_common_chapter": 1,
        "both_present_different_loci": 2,
        "mt_only_lxx_absent": 3,
        "lxx_only_mt_absent": 4,
        "absent_both_in_capped_scan": 5,
    }
    return (order.get(str(row["presence_class"]), 99), str(row["concept"]))


def hit_sort_key(row: dict[str, object]) -> tuple[str, str, str, int, str]:
    return (
        str(row["concept"]),
        str(row["side"]),
        str(row["counterpart_status"]),
        int(row["skip"]),
        str(row["center_ref"]),
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    comparison_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    scope_counts = defaultdict(int)
    for row in summary_rows:
        scope_counts[str(row["presence_class"])] += 1
    hit_status_counts = defaultdict(int)
    for row in comparison_rows:
        hit_status_counts[str(row["counterpart_status"])] += 1
    lines = [
        "# MT-LXX Reciprocal Presence",
        "",
        "This report compares concept-level ELS presence between one Hebrew MT",
        "corpus and one Greek LXX corpus. Because MT and LXX differ by language,",
        "alphabet, text length, translation choices, and sometimes verse alignment,",
        "this is not a same-letter or same-skip comparison. The comparison unit is",
        "concept + aligned center verse/chapter.",
        "",
        "## Scope",
        "",
        f"- Hebrew corpus: `{args.hebrew_corpus}`",
        f"- LXX corpus: `{args.lxx_corpus}`",
        f"- Skip range: `{args.min_skip}..{args.max_skip}`",
        f"- Direction: `{args.direction}`",
        f"- Minimum normalized term length: `{args.min_term_length}`",
        f"- Max hits per term per corpus: `{args.max_hits_per_term}`",
        f"- Term files: `{', '.join(str(path) for path in (args.terms or DEFAULT_TERM_FILES))}`",
        "",
        "## Concept Presence Classes",
        "",
        "| Class | Concepts |",
        "| --- | ---: |",
    ]
    for key in [
        "mt_lxx_common_verse",
        "mt_lxx_common_chapter",
        "both_present_different_loci",
        "mt_only_lxx_absent",
        "lxx_only_mt_absent",
        "absent_both_in_capped_scan",
    ]:
        lines.append(f"| `{key}` | {scope_counts[key]} |")
    lines.extend(
        [
            "",
            "## Hit Counterpart Status",
            "",
            "| Status | Hits |",
            "| --- | ---: |",
        ]
    )
    for key, count in sorted(hit_status_counts.items()):
        lines.append(f"| `{key}` | {count} |")
    lines.extend(
        [
            "",
            "## Concepts Needing Review",
            "",
            "| Concept | Hebrew | Greek | MT hits | LXX hits | Common verses | Common chapters | Class | Read |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in summary_rows[:120]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["concept"]),
                    display_term_list(str(row["hebrew_terms"]), str(row["concept"])),
                    display_term_list(str(row["greek_terms"]), str(row["concept"])),
                    str(row["mt_hit_count"]),
                    str(row["lxx_hit_count"]),
                    str(row["common_center_refs"]),
                    str(row["common_chapters"]),
                    f"`{row['presence_class']}`",
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "A `mt_only_lxx_absent` or `lxx_only_mt_absent` row means the counterpart",
            "concept was not found at the aligned locus under this run's term list,",
            "skip range, and cap. It does not mean a literal original-language letter",
            "sequence was mechanically broken across traditions. A row marked",
            "`alignment_broken_*` means the center locus could not be compared cleanly",
            "because the counterpart corpus lacks that exact verse or chapter key.",
            "",
            "Use this report to identify reciprocal review candidates. Claim-level",
            "language still requires locked terms, locked alignment rules, matched",
            "controls, and multiple-comparison correction.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def display_term_list(terms: str, concept: str) -> str:
    parts = [part.strip() for part in terms.split(";") if part.strip()]
    if not parts:
        return ""
    return "; ".join(display_term(part, english=concept) for part in parts[:3])


def write_manifest(
    args: argparse.Namespace,
    term_paths: list[Path],
    mt_sources: list[CorpusSource],
    lxx_sources: list[CorpusSource],
    hebrew_terms: list[TermRow],
    greek_terms: list[TermRow],
    mt_hits: list[HitView],
    lxx_hits: list[HitView],
    started: float,
) -> None:
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "script": "scripts.analyze_mt_lxx_reciprocal_presence",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "terms": [str(path) for path in term_paths],
        "hebrew_corpus": [f"{source.label}={source.path}" for source in mt_sources],
        "lxx_corpus": [f"{source.label}={source.path}" for source in lxx_sources],
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "min_term_length": args.min_term_length,
        "max_hits_per_term": args.max_hits_per_term,
        "hebrew_terms_selected": len(hebrew_terms),
        "greek_terms_selected": len(greek_terms),
        "mt_hits": len(mt_hits),
        "lxx_hits": len(lxx_hits),
    }
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
