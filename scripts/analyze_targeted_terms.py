#!/usr/bin/env python3
"""Build compact review tables for selected public-baseline target terms."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els.term_display import display_center, display_term


TARGET_CONCEPTS = (
    "Iran",
    "Trump",
    "Vance",
    "Netanyahu",
    "Gog",
    "Magog",
    "Russia",
    "Europe",
    "Turkey",
    "Germany",
)
TARGET_ORDER = {concept: index for index, concept in enumerate(TARGET_CONCEPTS)}
CORPUS_ORDER = {"MT_WLC": 0, "LXX": 1, "TR_NT": 2, "SBLGNT": 3}

BASE = Path("reports/protocols/public_baseline")
COUNT_FILES = [
    ("modern_names_dates", BASE / "modern_names_dates_counts.csv"),
    ("prophetic_terms", BASE / "prophetic_terms_counts.csv"),
]
TERM_SOURCE_BY_SET = {
    "modern_names_dates": "terms/modern_names_dates.csv",
    "prophetic_terms": "terms/prophetic_terms.csv",
}
CONTROLS = Path("reports/els_controls_summary.csv")
SURFACE_SUMMARY = BASE / "surface_context_summary.csv"
SURFACE_HITS = BASE / "surface_context_hits.csv"
EXTENSION_TOPS = [
    BASE / "surface_context_extensions_tr_nt_top.csv",
    BASE / "surface_context_extensions_sblgnt_top.csv",
]

SUMMARY_OUT = Path("reports/targeted_terms_summary.csv")
EXAMPLES_OUT = Path("reports/targeted_terms_examples.csv")
MD_OUT = Path("reports/targeted_terms.md")
DOCS_OUT = Path("docs/TARGETED_TERMS_FINDINGS.md")
MANIFEST_OUT = Path("reports/targeted_terms.manifest.json")

SUMMARY_FIELDNAMES = [
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
    "count_status",
    "control_observed_hits",
    "control_combined_min_p_ge",
    "control_combined_min_q_value",
    "control_significance_band",
    "control_flags",
    "surface_context_hit_count",
    "surface_exact_center_hits",
    "surface_exact_span_hits",
    "surface_same_category_center_hits",
    "surface_same_category_span_hits",
    "best_surface_ref",
    "best_surface_context",
    "best_surface_center_word",
    "extension_top_rows",
    "best_extension_sequence",
    "best_extension_phrase",
    "best_extension_ref",
    "read",
]

EXAMPLE_FIELDNAMES = [
    "example_type",
    "concept",
    "corpus",
    "term_id",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_ref",
    "end_ref",
    "center_ref",
    "center_word",
    "best_context",
    "extension_type",
    "extended_sequence",
    "matched_examples",
    "matched_refs",
    "source_file",
]


def main() -> int:
    count_rows = read_target_count_rows()
    controls = {
        (row["corpus"], row["term_set"], row["term_id"]): row
        for row in read_rows(CONTROLS)
    }
    surface_summary = {
        (row["corpus"], row["term_source"], row["term_id"]): row
        for row in read_rows(SURFACE_SUMMARY)
    }
    surface_hits = grouped_surface_hits(count_rows)
    extension_hits = grouped_extension_hits(count_rows)

    summary_rows: list[dict[str, object]] = []
    example_rows: list[dict[str, object]] = []
    for count_row in sorted(count_rows, key=count_sort_key):
        key = count_key(count_row)
        surface_key = surface_key_from_count(count_row)
        surface_examples = surface_hits.get(key, [])[:3]
        extension_examples = extension_hits.get(key, [])[:3]
        summary_rows.append(
            summary_row(
                count_row,
                controls.get(key, {}),
                surface_summary.get(surface_key, {}),
                surface_examples,
                extension_examples,
            )
        )
        example_rows.extend(surface_example_rows(count_row, surface_examples))
        example_rows.extend(extension_example_rows(count_row, extension_examples))

    write_rows(SUMMARY_OUT, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(EXAMPLES_OUT, EXAMPLE_FIELDNAMES, example_rows)
    write_markdown(MD_OUT, summary_rows, example_rows)
    write_markdown(DOCS_OUT, summary_rows, example_rows)
    write_manifest(summary_rows, example_rows)

    print(SUMMARY_OUT)
    print(EXAMPLES_OUT)
    print(MD_OUT)
    print(MANIFEST_OUT)
    return 0


def read_target_count_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for term_set, path in COUNT_FILES:
        for row in read_rows(path):
            if row["concept"] not in TARGET_ORDER:
                continue
            row = dict(row)
            row["term_set"] = term_set
            row["term_source"] = TERM_SOURCE_BY_SET[term_set]
            row["source_file"] = str(path)
            rows.append(row)
    return rows


def grouped_surface_hits(count_rows: list[dict[str, str]]) -> dict[tuple[str, str, str], list[dict[str, str]]]:
    wanted = {surface_key_from_count(row): count_key(row) for row in count_rows}
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in read_rows(SURFACE_HITS):
        surface_key = (row["corpus"], row["term_source"], row["term_id"])
        count_row_key = wanted.get(surface_key)
        if count_row_key is not None:
            grouped[count_row_key].append(row)
    for rows in grouped.values():
        rows.sort(key=surface_hit_sort_key)
    return grouped


def grouped_extension_hits(count_rows: list[dict[str, str]]) -> dict[tuple[str, str, str], list[dict[str, str]]]:
    targets_by_corpus_norm: dict[tuple[str, str], list[tuple[str, str, str]]] = defaultdict(list)
    for row in count_rows:
        targets_by_corpus_norm[(row["corpus"], row["normalized_term"])].append(
            count_key(row)
        )

    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for path in EXTENSION_TOPS:
        for row in read_rows(path):
            keys = targets_by_corpus_norm.get((row["corpus"], row["normalized_term"]), [])
            for key in keys:
                row = dict(row)
                row["source_file"] = str(path)
                grouped[key].append(row)
    for rows in grouped.values():
        rows.sort(key=extension_hit_sort_key)
    return grouped


def summary_row(
    count_row: dict[str, str],
    control: dict[str, str],
    surface: dict[str, str],
    surface_examples: list[dict[str, str]],
    extension_examples: list[dict[str, str]],
) -> dict[str, object]:
    best_surface = surface_examples[0] if surface_examples else {}
    best_extension = extension_examples[0] if extension_examples else {}
    return {
        "concept": count_row["concept"],
        "corpus": count_row["corpus"],
        "term_set": count_row["term_set"],
        "term_id": count_row["term_id"],
        "category": count_row["category"],
        "term_language": count_row["term_language"],
        "term": count_row["term"],
        "normalized_term": count_row["normalized_term"],
        "normalized_length": count_row["normalized_length"],
        "hit_count": count_row["hit_count"],
        "count_status": count_row["status"],
        "control_observed_hits": control.get("observed_hits", ""),
        "control_combined_min_p_ge": control.get("combined_min_p_ge", ""),
        "control_combined_min_q_value": control.get("combined_min_q_value", ""),
        "control_significance_band": control.get("significance_band", ""),
        "control_flags": control.get("flags", ""),
        "surface_context_hit_count": surface.get("context_hit_count", ""),
        "surface_exact_center_hits": surface.get("exact_center_hits", ""),
        "surface_exact_span_hits": surface.get("exact_span_hits", ""),
        "surface_same_category_center_hits": surface.get("same_category_center_hits", ""),
        "surface_same_category_span_hits": surface.get("same_category_span_hits", ""),
        "best_surface_ref": ref_span(best_surface),
        "best_surface_context": best_surface.get("best_context", ""),
        "best_surface_center_word": best_surface.get("center_word", ""),
        "extension_top_rows": len(extension_examples),
        "best_extension_sequence": best_extension.get("extended_sequence", ""),
        "best_extension_phrase": first_example(best_extension.get("matched_examples", "")),
        "best_extension_ref": ref_span(best_extension),
        "read": read_label(count_row, control, surface, extension_examples),
    }


def surface_example_rows(
    count_row: dict[str, str],
    examples: list[dict[str, str]],
) -> list[dict[str, object]]:
    rows = []
    for row in examples:
        rows.append(
            {
                "example_type": "surface_context",
                "concept": count_row["concept"],
                "corpus": row["corpus"],
                "term_id": row["term_id"],
                "term": row["term"],
                "normalized_term": row["normalized_term"],
                "skip": row["skip"],
                "direction": row["direction"],
                "start_ref": row["start_ref"],
                "end_ref": row["end_ref"],
                "center_ref": row["center_ref"],
                "center_word": row["center_word"],
                "best_context": row["best_context"],
                "extension_type": "",
                "extended_sequence": "",
                "matched_examples": "",
                "matched_refs": "",
                "source_file": str(SURFACE_HITS),
            }
        )
    return rows


def extension_example_rows(
    count_row: dict[str, str],
    examples: list[dict[str, str]],
) -> list[dict[str, object]]:
    rows = []
    for row in examples:
        rows.append(
            {
                "example_type": "extension_top",
                "concept": count_row["concept"],
                "corpus": row["corpus"],
                "term_id": count_row["term_id"],
                "term": row["term"],
                "normalized_term": row["normalized_term"],
                "skip": row["skip"],
                "direction": row["direction"],
                "start_ref": row["start_ref"],
                "end_ref": row["end_ref"],
                "center_ref": row["center_ref"],
                "center_word": row["center_word"],
                "best_context": "",
                "extension_type": row["extension_type"],
                "extended_sequence": row["extended_sequence"],
                "matched_examples": row["matched_examples"],
                "matched_refs": row["matched_refs"],
                "source_file": row.get("source_file", ""),
            }
        )
    return rows


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    example_rows: list[dict[str, object]],
) -> None:
    lines = [
        "# Targeted Terms Report",
        "",
        "Targets: " + ", ".join(TARGET_CONCEPTS) + ".",
        "",
        "This report joins raw counts, controls, NT surface context, and filtered NT extension-top rows. It is a screening artifact, not a significance claim.",
        "",
        "## Controls Read",
        "",
        "Controls remain weak for claim-making: rows with low uncorrected p-values still carry flags such as `few_letter_controls`, `few_term_controls`, `huge_search_space`, and `uncorrected_only`.",
        "",
        "## Concept Summary",
        "",
        "| Concept | Best raw count | Best control band | Surface context rows | Extension top rows | Read |",
        "| --- | ---: | --- | ---: | ---: | --- |",
    ]
    for concept in TARGET_CONCEPTS:
        rows = [row for row in summary_rows if row["concept"] == concept]
        if not rows:
            continue
        best_count = max(rows, key=lambda row: int(row["hit_count"] or 0))
        surface_total = sum(int_or_zero(row["surface_context_hit_count"]) for row in rows)
        extension_total = sum(int(row["extension_top_rows"]) for row in rows)
        bands = sorted({str(row["control_significance_band"]) for row in rows if row["control_significance_band"]})
        lines.append(
            "| "
            + " | ".join(
                [
                    concept,
                    (
                        f"{best_count['corpus']} `{best_count['term_id']}` "
                        f"{display_target_term(best_count)} {best_count['hit_count']}"
                    ),
                    ", ".join(bands) or "",
                    str(surface_total),
                    str(extension_total),
                    concept_read(concept, rows),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Term Rows", ""])
    for concept in TARGET_CONCEPTS:
        rows = [row for row in summary_rows if row["concept"] == concept]
        if not rows:
            continue
        lines.extend(
            [
                f"### {concept}",
                "",
                "| Corpus | Term ID | Term | Hits | Control | Surface | Extension | Read |",
                "| --- | --- | --- | ---: | --- | ---: | ---: | --- |",
            ]
        )
        for row in rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["corpus"]),
                        f"`{row['term_id']}`",
                        display_target_term(row),
                        str(row["hit_count"]),
                        str(row["control_significance_band"] or ""),
                        str(row["surface_context_hit_count"] or 0),
                        str(row["extension_top_rows"]),
                        str(row["read"]),
                    ]
                )
                + " |"
            )
        lines.append("")

    lines.extend(["## Best Examples", ""])
    for example_type in ("surface_context", "extension_top"):
        examples = [row for row in example_rows if row["example_type"] == example_type]
        lines.extend(
            [
                f"### {example_type}",
                "",
                "| Concept | Corpus | Term | Skip | Span | Center | Detail |",
                "| --- | --- | --- | ---: | --- | --- | --- |",
            ]
        )
        for row in examples[:40]:
            detail = row["best_context"] if example_type == "surface_context" else first_example(str(row["matched_examples"]))
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["concept"]),
                        str(row["corpus"]),
                        display_target_term(row),
                        str(row["skip"]),
                        f"{row['start_ref']}-{row['end_ref']}",
                        display_center(str(row["center_ref"]), str(row["center_word"])),
                        str(detail),
                    ]
                )
                + " |"
            )
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def display_target_term(row: dict[str, object]) -> str:
    term = str(row.get("normalized_term") or row.get("term") or "")
    concept = str(row.get("concept") or "")
    return display_term(term, english=concept)


def read_label(
    count_row: dict[str, str],
    control: dict[str, str],
    surface: dict[str, str],
    extension_examples: list[dict[str, str]],
) -> str:
    hit_count = int_or_zero(count_row.get("hit_count", ""))
    normalized_length = int_or_zero(count_row.get("normalized_length", ""))
    band = control.get("significance_band", "")
    if hit_count == 0:
        return "absent"
    if band == "uncorrected_p_le_0.05":
        return "uncorrected only; needs stronger controls"
    if normalized_length <= 4 and hit_count > 1000:
        return "high count, likely short-form density"
    if extension_examples:
        return "has filtered extension-top row"
    if int_or_zero(surface.get("context_hit_count", "")):
        return "has NT surface context"
    return "counted, not unusual"


def concept_read(concept: str, rows: list[dict[str, object]]) -> str:
    if concept in {"Gog", "Magog"}:
        return "review as pair/proximity, not raw counts"
    if concept in {"Trump", "Vance", "Netanyahu"}:
        return "modern-name screen; controls first"
    if concept == "Iran":
        return "good target, but Greek term is short"
    if any(row["control_significance_band"] == "uncorrected_p_le_0.05" for row in rows):
        return "uncorrected screen only"
    return "no robust signal"


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


def write_manifest(
    summary_rows: list[dict[str, object]],
    example_rows: list[dict[str, object]],
) -> None:
    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_OUT.write_text(
        json.dumps(
            {
                "tool": "targeted_terms_report",
                "created_utc": datetime.now(UTC).isoformat(),
                "targets": list(TARGET_CONCEPTS),
                "summary_rows": len(summary_rows),
                "example_rows": len(example_rows),
                "inputs": [
                    *(str(path) for _label, path in COUNT_FILES),
                    str(CONTROLS),
                    str(SURFACE_SUMMARY),
                    str(SURFACE_HITS),
                    *(str(path) for path in EXTENSION_TOPS),
                ],
                "outputs": [
                    str(SUMMARY_OUT),
                    str(EXAMPLES_OUT),
                    str(MD_OUT),
                    str(DOCS_OUT),
                    str(MANIFEST_OUT),
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def count_sort_key(row: dict[str, str]) -> tuple[int, str, int, str]:
    return (
        TARGET_ORDER[row["concept"]],
        row["term_id"],
        CORPUS_ORDER.get(row["corpus"], 99),
        row["term_set"],
    )


def count_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (row["corpus"], row["term_set"], row["term_id"])


def surface_key_from_count(row: dict[str, str]) -> tuple[str, str, str]:
    return (row["corpus"], row["term_source"], row["term_id"])


def surface_hit_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    return (
        {
            "exact_center": 0,
            "exact_span": 1,
            "same_concept_center": 2,
            "same_concept_span": 3,
            "same_category_center": 4,
            "same_category_span": 5,
        }.get(row.get("best_context", ""), 99),
        abs(int_or_zero(row.get("skip", ""))),
        min(int_or_zero(row.get("start_offset", "")), int_or_zero(row.get("end_offset", ""))),
    )


def extension_hit_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    return (
        -int_or_zero(row.get("extension_score", "")),
        -int_or_zero(row.get("extension_length", "")),
        abs(int_or_zero(row.get("skip", ""))),
    )


def ref_span(row: dict[str, str]) -> str:
    if not row:
        return ""
    start = row.get("start_ref", "")
    end = row.get("end_ref", "")
    if not start:
        return ""
    return start if not end or end == start else f"{start}-{end}"


def first_example(value: str) -> str:
    return value.split(";", 1)[0].strip() if value else ""


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


if __name__ == "__main__":
    raise SystemExit(main())
