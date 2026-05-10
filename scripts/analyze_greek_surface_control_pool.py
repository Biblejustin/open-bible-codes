#!/usr/bin/env python3
"""Build real-word surface-frequency control pools for Greek surface triage rows."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, load_corpus
from els.normalization import normalize_greek, normalize_text
from els.search import AhoAutomaton
from els.term_display import display_term


TERMS_IN = Path("terms/greek_expanded_prospective_terms.csv")
SELECTED_IN = Path("reports/greek_expanded_surface_triage/selected_patterns.csv")
OUT_DIR = Path("reports/greek_expanded_surface_control_pool")
FREQUENCIES_OUT = OUT_DIR / "term_surface_frequencies.csv"
MATCHED_OUT = OUT_DIR / "matched_controls.csv"
MD_OUT = Path("docs/GREEK_EXPANDED_SURFACE_CONTROL_POOL.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"
DEFAULT_CORPORA = {
    "TR_NT": Path("configs/example_ebible_grctr.toml"),
    "BYZ_NT": Path("configs/example_ebible_grcmt.toml"),
    "TCG_NT": Path("configs/example_ebible_grctcgnt.toml"),
    "SBLGNT": Path("configs/example_sblgnt.toml"),
}

FREQUENCY_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "normalized_length",
    "selected_target",
    "surface_verses_tr_nt",
    "surface_verses_byz_nt",
    "surface_verses_tcg_nt",
    "surface_verses_sblgnt",
    "surface_verse_sum",
    "surface_verse_min",
    "surface_verse_max",
    "all_source_surface_present",
]

MATCHED_FIELDNAMES = [
    "target_term_id",
    "target_concept",
    "target_normalized_term",
    "control_term_id",
    "control_concept",
    "control_normalized_term",
    "normalized_length",
    "target_surface_vector",
    "control_surface_vector",
    "target_surface_verse_sum",
    "control_surface_verse_sum",
    "surface_sum_delta",
    "surface_vector_l1_delta",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus_configs = parse_corpus_args(args.corpus)
    term_rows = read_rows(args.terms)
    selected_ids = {row["term_id"] for row in read_rows(args.selected)}
    frequencies = surface_frequency_rows(term_rows, selected_ids, corpus_configs)
    matched = matched_control_rows(
        frequencies,
        selected_ids,
        top_n=args.top_controls,
    )
    write_rows(args.frequencies_out, FREQUENCY_FIELDNAMES, frequencies)
    write_rows(args.matched_out, MATCHED_FIELDNAMES, matched)
    write_markdown(args.markdown_out, frequencies, matched, args)
    write_manifest(args, corpus_configs, frequencies, matched, started)
    print(args.frequencies_out)
    print(args.matched_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, default=TERMS_IN)
    parser.add_argument("--selected", type=Path, default=SELECTED_IN)
    parser.add_argument("--corpus", action="append", default=[])
    parser.add_argument("--top-controls", type=int, default=10)
    parser.add_argument("--title", default="Greek Expanded Surface Control Pool")
    parser.add_argument(
        "--max-markdown-controls",
        type=int,
        help="cap closest-control rows shown in markdown; CSV output is unchanged",
    )
    parser.add_argument("--frequencies-out", type=Path, default=FREQUENCIES_OUT)
    parser.add_argument("--matched-out", type=Path, default=MATCHED_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def parse_corpus_args(values: list[str]) -> dict[str, Path]:
    if not values:
        return dict(DEFAULT_CORPORA)
    output = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected LABEL=path corpus value: {value}")
        label, path = value.split("=", 1)
        output[label] = Path(path)
    return output


def surface_frequency_rows(
    term_rows: list[dict[str, str]],
    selected_ids: set[str],
    corpus_configs: dict[str, Path],
) -> list[dict[str, str]]:
    terms_by_pattern: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in term_rows:
        normalized = normalize_greek(row["term"])
        if normalized:
            terms_by_pattern[normalized].append(row)
    counts_by_term: dict[str, Counter[str]] = {
        row["term_id"]: Counter() for row in term_rows
    }
    automaton = build_automaton(terms_by_pattern)
    for label, config in corpus_configs.items():
        corpus = load_corpus(config)
        add_surface_counts(label, corpus, terms_by_pattern, automaton, counts_by_term)
    return sorted(
        [
            frequency_row(row, counts_by_term[row["term_id"]], selected_ids)
            for row in term_rows
        ],
        key=lambda row: (
            row["selected_target"] != "True",
            int(row["normalized_length"]),
            -int(row["surface_verse_sum"]),
            row["term_id"],
        ),
    )


def build_automaton(terms_by_pattern: dict[str, list[dict[str, str]]]) -> AhoAutomaton:
    automaton = AhoAutomaton()
    for pattern in terms_by_pattern:
        automaton.add(pattern, pattern)
    automaton.build()
    return automaton


def add_surface_counts(
    label: str,
    corpus: Corpus,
    terms_by_pattern: dict[str, list[dict[str, str]]],
    automaton: AhoAutomaton,
    counts_by_term: dict[str, Counter[str]],
) -> None:
    for verse in corpus.verses:
        normalized = normalize_text(
            verse.raw_text,
            corpus.language,
            keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
        )
        for pattern in set(automaton.find_outputs(normalized)):
            for term in terms_by_pattern[pattern]:
                counts_by_term[term["term_id"]][label] += 1


def frequency_row(
    term: dict[str, str],
    counts: Counter[str],
    selected_ids: set[str],
) -> dict[str, str]:
    normalized = normalize_greek(term["term"])
    vector = surface_vector(counts)
    return {
        "term_id": term["term_id"],
        "concept": term["concept"],
        "category": term["category"],
        "term": term["term"],
        "normalized_term": normalized,
        "normalized_length": str(len(normalized)),
        "selected_target": str(term["term_id"] in selected_ids),
        "surface_verses_tr_nt": str(vector[0]),
        "surface_verses_byz_nt": str(vector[1]),
        "surface_verses_tcg_nt": str(vector[2]),
        "surface_verses_sblgnt": str(vector[3]),
        "surface_verse_sum": str(sum(vector)),
        "surface_verse_min": str(min(vector)),
        "surface_verse_max": str(max(vector)),
        "all_source_surface_present": str(all(value > 0 for value in vector)),
    }


def matched_control_rows(
    frequencies: list[dict[str, str]],
    selected_ids: set[str],
    *,
    top_n: int,
) -> list[dict[str, str]]:
    by_id = {row["term_id"]: row for row in frequencies}
    targets = [by_id[term_id] for term_id in sorted(selected_ids) if term_id in by_id]
    rows = []
    for target in targets:
        candidates = matched_candidates(target, frequencies)
        for candidate in candidates[:top_n]:
            rows.append(matched_row(target, candidate))
    return rows


def matched_candidates(
    target: dict[str, str],
    frequencies: list[dict[str, str]],
) -> list[dict[str, str]]:
    target_length = target["normalized_length"]
    return sorted(
        [
            candidate
            for candidate in frequencies
            if candidate["term_id"] != target["term_id"]
            and candidate["selected_target"] != "True"
            and candidate["normalized_length"] == target_length
            and candidate["all_source_surface_present"] == "True"
        ],
        key=lambda candidate: (
            vector_l1_delta(target, candidate),
            abs(int(target["surface_verse_sum"]) - int(candidate["surface_verse_sum"])),
            candidate["term_id"],
        ),
    )


def matched_row(target: dict[str, str], control: dict[str, str]) -> dict[str, str]:
    return {
        "target_term_id": target["term_id"],
        "target_concept": target["concept"],
        "target_normalized_term": target["normalized_term"],
        "control_term_id": control["term_id"],
        "control_concept": control["concept"],
        "control_normalized_term": control["normalized_term"],
        "normalized_length": target["normalized_length"],
        "target_surface_vector": vector_text(target),
        "control_surface_vector": vector_text(control),
        "target_surface_verse_sum": target["surface_verse_sum"],
        "control_surface_verse_sum": control["surface_verse_sum"],
        "surface_sum_delta": str(
            abs(int(target["surface_verse_sum"]) - int(control["surface_verse_sum"]))
        ),
        "surface_vector_l1_delta": str(vector_l1_delta(target, control)),
        "read": "candidate real-word control; run ELS surface statistic only after freezing pool",
    }


def surface_vector(counts: Counter[str]) -> tuple[int, int, int, int]:
    return (
        counts.get("TR_NT", 0),
        counts.get("BYZ_NT", 0),
        counts.get("TCG_NT", 0),
        counts.get("SBLGNT", 0),
    )


def row_vector(row: dict[str, str]) -> tuple[int, int, int, int]:
    return (
        int(row["surface_verses_tr_nt"]),
        int(row["surface_verses_byz_nt"]),
        int(row["surface_verses_tcg_nt"]),
        int(row["surface_verses_sblgnt"]),
    )


def vector_text(row: dict[str, str]) -> str:
    return "/".join(str(value) for value in row_vector(row))


def vector_l1_delta(left: dict[str, str], right: dict[str, str]) -> int:
    return sum(abs(a - b) for a, b in zip(row_vector(left), row_vector(right), strict=True))


def write_markdown(
    path: Path,
    frequencies: list[dict[str, str]],
    matched: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    selected = [row for row in frequencies if row["selected_target"] == "True"]
    controls_by_target = Counter(row["target_term_id"] for row in matched)
    all_source_terms = sum(row["all_source_surface_present"] == "True" for row in frequencies)
    lines = [
        f"# {args.title}",
        "",
        "Status: real-word control-pool construction; no ELS control statistic yet.",
        "",
        "This report prepares fair controls for the tighter expanded Greek surface",
        "triage. It counts normalized surface-substring verse frequency for every",
        "term in the expanded Greek prospective list, then selects same-length real",
        "Greek terms with the closest surface-frequency vectors across TR_NT,",
        "BYZ_NT, TCG_NT, and SBLGNT.",
        "Selected target terms are excluded from the control candidate pool.",
        "",
        "## Inputs",
        "",
        f"- Terms: `{args.terms}`",
        f"- Selected triage rows: `{args.selected}`",
        "",
        "## Surface-Frequency Scope",
        "",
        f"- terms measured: {len(frequencies):,}",
        f"- all-source surface-present terms: {all_source_terms:,}",
        f"- selected targets: {len(selected):,}",
        f"- matched controls per target requested: {args.top_controls:,}",
        "",
        "## Selected Targets",
        "",
        "| Term | Concept | Length | Surface verse vector | Sum | Controls found |",
        "| --- | --- | ---: | --- | ---: | ---: |",
    ]
    for row in selected:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_term(row["normalized_term"], english=row["concept"]),
                    row["concept"],
                    row["normalized_length"],
                    vector_text(row),
                    row["surface_verse_sum"],
                    str(controls_by_target[row["term_id"]]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Closest Controls",
            "",
            "| Target | Control | Control concept | Surface vector | Sum delta | Vector delta |",
            "| --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    markdown_limit = getattr(args, "max_markdown_controls", None)
    markdown_matched = matched if markdown_limit is None else matched[:markdown_limit]
    for row in markdown_matched:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_term(
                        row["target_normalized_term"],
                        english=row["target_concept"],
                    ),
                    display_term(
                        row["control_normalized_term"],
                        english=row["control_concept"],
                    ),
                    row["control_concept"],
                    row["control_surface_vector"],
                    row["surface_sum_delta"],
                    row["surface_vector_l1_delta"],
                ]
            )
            + " |"
        )
    if markdown_limit is not None and len(matched) > markdown_limit:
        lines.extend(
            [
                "",
                f"Markdown preview capped at {markdown_limit:,} controls; full matched-control rows: {len(matched):,}.",
            ]
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "This is a control-pool report, not a significance test. It uses the same",
            "normalized substring rule as the current surface-context path and avoids",
            "the bad control design of comparing surface-context rows against random",
            "strings. The next step can freeze one matched-control set per target and",
            "then run the ELS exact-center surface statistic against those real-word",
            "controls.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    corpus_configs: dict[str, Path],
    frequencies: list[dict[str, str]],
    matched: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_greek_surface_control_pool",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "terms": str(args.terms),
        "selected": str(args.selected),
        "corpora": {label: str(path) for label, path in corpus_configs.items()},
        "frequency_rows": len(frequencies),
        "matched_rows": len(matched),
        "max_markdown_controls": args.max_markdown_controls,
        "outputs": [
            str(args.frequencies_out),
            str(args.matched_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
