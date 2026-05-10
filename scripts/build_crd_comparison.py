#!/usr/bin/env python3
"""Build comparison summaries from a CRD density matrix."""

from __future__ import annotations

import argparse
import csv
import heapq
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from els.report_db import default_table_name, fetch_dicts, quote_identifier, sanitize_table_name, verify_table_current


DEFAULT_OUT_DIR = Path("reports/crd")
DEFAULT_DENSITY = DEFAULT_OUT_DIR / "density_matrix.csv"
DEFAULT_CLASSIFIED = DEFAULT_OUT_DIR / "classified_hits.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_REPORT = Path("docs/CRD_REPORT.md")

PER_TERM_FIELDNAMES = [
    "classifier_mode",
    "term_id",
    "term",
    "language",
    "corpus",
    "corpus_class",
    "density_rank",
    "density_per_million",
    "relevance_rate",
    "total_centered_hits",
    "relevant_centered_hits",
]

BIBLE_CONTROL_FIELDNAMES = [
    "classifier_mode",
    "term_id",
    "term",
    "language",
    "bible_max_density",
    "bible_max_corpus",
    "secular_max_density",
    "secular_max_corpus",
    "ratio",
    "exceeds_secular_max",
]

EDITION_META_FIELDNAMES = [
    "classifier_mode",
    "corpus",
    "corpus_class",
    "ranked_terms",
    "best_rank_count",
    "mean_rank",
    "median_rank",
]

AGREEMENT_FIELDNAMES = [
    "scope",
    "term_id",
    "term",
    "language",
    "corpus",
    "agreement_rate",
    "agreement_kappa",
    "deterministic_only_relevant_count",
    "llm_only_relevant_count",
    "disagreement_count",
]

SCOPE_FIELDNAMES = [
    "classifier_mode",
    "corpus_class",
    "term_id",
    "term",
    "language",
    "match_scope",
    "relevant_hit_count",
]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    outputs = build_crd_comparison(
        density_matrix=args.density_matrix,
        classified_hits=args.classified_hits,
        manifest=args.manifest,
        out_dir=args.out_dir,
        markdown_out=args.markdown_out,
        db=args.db,
        classified_table=args.classified_table,
    )
    for value in outputs.values():
        print(value)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--density-matrix", type=Path, default=DEFAULT_DENSITY)
    parser.add_argument("--classified-hits", type=Path, default=DEFAULT_CLASSIFIED)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--db", type=Path, help="Read large classified-hit examples/agreement from DuckDB.")
    parser.add_argument(
        "--classified-table",
        help="DuckDB classified-hit table name. Defaults to a name derived from --classified-hits.",
    )
    return parser


def build_crd_comparison(
    *,
    density_matrix: Path,
    classified_hits: Path,
    manifest: Path,
    out_dir: Path,
    markdown_out: Path,
    db: Path | None = None,
    classified_table: str = "",
) -> dict[str, str]:
    rows = read_rows(density_matrix)
    table = classified_table or default_table_name(classified_hits)
    if db is not None:
        verify_table_current(db_path=db, table_name=table, source_path=classified_hits)
    hit_examples = (
        relevant_examples_from_db(db, table)
        if db is not None
        else relevant_examples_from_file(classified_hits)
        if classified_hits.exists()
        else []
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    per_term = per_term_rankings(rows)
    bible_control = bible_vs_control_summary(rows)
    edition_meta = edition_meta_summary(rows)
    relevance_scope = relevance_scope_summary(
        classified_hits if classified_hits.exists() else None,
        db=db,
        classified_table=table,
    )
    agreement = classifier_agreement_summary(
        rows,
        classified_hits if classified_hits.exists() else None,
        db=db,
        classified_table=table,
    )

    per_term_out = out_dir / "per_term_rankings.csv"
    bible_control_out = out_dir / "bible_vs_control_summary.csv"
    edition_meta_out = out_dir / "edition_meta_summary.csv"
    agreement_out = out_dir / "classifier_agreement_summary.csv"
    relevance_scope_out = out_dir / "relevance_scope_summary.csv"
    write_rows(per_term_out, PER_TERM_FIELDNAMES, per_term)
    write_rows(bible_control_out, BIBLE_CONTROL_FIELDNAMES, bible_control)
    write_rows(edition_meta_out, EDITION_META_FIELDNAMES, edition_meta)
    write_rows(agreement_out, AGREEMENT_FIELDNAMES, agreement)
    write_rows(relevance_scope_out, SCOPE_FIELDNAMES, relevance_scope)
    write_markdown(markdown_out, rows, hit_examples, bible_control, edition_meta, agreement, relevance_scope, manifest)
    return {
        "per_term_rankings": str(per_term_out),
        "bible_vs_control_summary": str(bible_control_out),
        "edition_meta_summary": str(edition_meta_out),
        "classifier_agreement_summary": str(agreement_out),
        "relevance_scope_summary": str(relevance_scope_out),
        "markdown": str(markdown_out),
    }


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def per_term_rankings(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["classifier_mode"], row["term_id"])].append(row)
    out: list[dict[str, Any]] = []
    for values in grouped.values():
        ranked = sorted(values, key=lambda row: float_value(row.get("density_per_million")), reverse=True)
        for rank, row in enumerate(ranked, start=1):
            out.append(
                {
                    "classifier_mode": row["classifier_mode"],
                    "term_id": row["term_id"],
                    "term": row["term"],
                    "language": row["language"],
                    "corpus": row["corpus"],
                    "corpus_class": row["corpus_class"],
                    "density_rank": rank,
                    "density_per_million": row["density_per_million"],
                    "relevance_rate": row["relevance_rate"],
                    "total_centered_hits": row["total_centered_hits"],
                    "relevant_centered_hits": row["relevant_centered_hits"],
                }
            )
    return out


def bible_vs_control_summary(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["classifier_mode"], row["term_id"])].append(row)
    out: list[dict[str, Any]] = []
    for values in grouped.values():
        bible_rows = [row for row in values if row.get("corpus_class") == "bible"]
        secular_rows = [row for row in values if row.get("corpus_class") == "secular_control"]
        best_bible = max_density_row(bible_rows)
        best_secular = max_density_row(secular_rows)
        first = values[0]
        bible_density = float_value(best_bible.get("density_per_million") if best_bible else "")
        secular_density = float_value(best_secular.get("density_per_million") if best_secular else "")
        out.append(
            {
                "classifier_mode": first["classifier_mode"],
                "term_id": first["term_id"],
                "term": first["term"],
                "language": first["language"],
                "bible_max_density": format_float(bible_density),
                "bible_max_corpus": best_bible.get("corpus", "") if best_bible else "",
                "secular_max_density": format_float(secular_density),
                "secular_max_corpus": best_secular.get("corpus", "") if best_secular else "",
                "ratio": format_float(bible_density / secular_density) if secular_density else "",
                "exceeds_secular_max": str(bool(bible_rows and bible_density > secular_density)).lower(),
            }
        )
    return sorted(out, key=lambda row: (row["classifier_mode"], row["term_id"]))


def max_density_row(rows: list[dict[str, str]]) -> dict[str, str] | None:
    if not rows:
        return None
    return max(rows, key=lambda row: float_value(row.get("density_per_million")))


def edition_meta_summary(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    ranks = per_term_rankings(rows)
    by_edition: dict[tuple[str, str], list[int]] = defaultdict(list)
    edition_class: dict[tuple[str, str], str] = {}
    for row in ranks:
        key = (str(row["classifier_mode"]), str(row["corpus"]))
        by_edition[key].append(int(row["density_rank"]))
        edition_class[key] = str(row["corpus_class"])
    out: list[dict[str, Any]] = []
    for (mode, corpus), values in sorted(by_edition.items()):
        sorted_values = sorted(values)
        out.append(
            {
                "classifier_mode": mode,
                "corpus": corpus,
                "corpus_class": edition_class[(mode, corpus)],
                "ranked_terms": len(values),
                "best_rank_count": sum(1 for value in values if value == 1),
                "mean_rank": format_float(sum(values) / len(values)),
                "median_rank": format_float(median(sorted_values)),
            }
        )
    return out


def classifier_agreement_summary(
    density_rows: list[dict[str, str]],
    classified_hits: Path | None,
    *,
    db: Path | None = None,
    classified_table: str = "",
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for row in density_rows:
        if not row.get("agreement_rate"):
            continue
        key = (row["term_id"], row["corpus"])
        if key in seen:
            continue
        seen.add(key)
        disagreement = int_value(row.get("deterministic_only_relevant_count")) + int_value(
            row.get("llm_only_relevant_count")
        )
        out.append(
            {
                "scope": "term_corpus",
                "term_id": row["term_id"],
                "term": row["term"],
                "language": row["language"],
                "corpus": row["corpus"],
                "agreement_rate": row["agreement_rate"],
                "agreement_kappa": row["agreement_kappa"],
                "deterministic_only_relevant_count": row["deterministic_only_relevant_count"],
                "llm_only_relevant_count": row["llm_only_relevant_count"],
                "disagreement_count": disagreement,
            }
        )
    if out:
        overall = (
            overall_agreement_from_db(db, classified_table) if db is not None else overall_agreement_from_file(classified_hits)
        )
        out.insert(0, overall)
    return sorted(out, key=lambda row: (row["scope"] != "overall", -int_value(row["disagreement_count"])))


def relevance_scope_summary(
    classified_hits: Path | None,
    *,
    db: Path | None = None,
    classified_table: str = "",
) -> list[dict[str, Any]]:
    return (
        relevance_scope_summary_from_db(db, classified_table)
        if db is not None
        else relevance_scope_summary_from_file(classified_hits)
    )


def relevance_scope_summary_from_file(classified_hits: Path | None) -> list[dict[str, Any]]:
    if classified_hits is None or not classified_hits.exists():
        return []
    counts: dict[tuple[str, str, str, str, str, str], int] = defaultdict(int)
    with classified_hits.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("is_relevant") != "true":
                continue
            scope = row.get("surface_match_scope") or row.get("relevance_type") or "unknown"
            key = (
                row.get("classifier_mode", ""),
                row.get("corpus_class", ""),
                row.get("term_id", ""),
                row.get("term", ""),
                row.get("language", ""),
                scope,
            )
            counts[key] += 1
    return relevance_scope_rows(counts)


def relevance_scope_summary_from_db(db: Path | None, table: str) -> list[dict[str, Any]]:
    if db is None:
        return []
    qtable = quote_identifier(sanitize_table_name(table))
    rows = fetch_dicts(
        db_path=db,
        query=f"""
            SELECT
                classifier_mode,
                corpus_class,
                term_id,
                term,
                language,
                CASE
                    WHEN surface_match_scope IS NOT NULL AND surface_match_scope != '' THEN surface_match_scope
                    WHEN relevance_type IS NOT NULL AND relevance_type != '' THEN relevance_type
                    ELSE 'unknown'
                END AS match_scope,
                count(*) AS relevant_hit_count
            FROM {qtable}
            WHERE is_relevant = 'true'
            GROUP BY 1, 2, 3, 4, 5, 6
        """,
    )
    counts = {
        (
            str(row.get("classifier_mode", "")),
            str(row.get("corpus_class", "")),
            str(row.get("term_id", "")),
            str(row.get("term", "")),
            str(row.get("language", "")),
            str(row.get("match_scope", "")),
        ): int_value(row.get("relevant_hit_count"))
        for row in rows
    }
    return relevance_scope_rows(counts)


def relevance_scope_rows(counts: dict[tuple[str, str, str, str, str, str], int]) -> list[dict[str, Any]]:
    rows = [
        {
            "classifier_mode": key[0],
            "corpus_class": key[1],
            "term_id": key[2],
            "term": key[3],
            "language": key[4],
            "match_scope": key[5],
            "relevant_hit_count": value,
        }
        for key, value in counts.items()
    ]
    return sorted(rows, key=lambda row: (scope_rank(str(row["match_scope"])), -int(row["relevant_hit_count"]), row["term_id"]))


def scope_rank(scope: str) -> int:
    order = {
        "center_word": 0,
        "center_verse": 1,
        "span": 2,
        "verse_ref_match": 3,
        "concept_match": 4,
    }
    return order.get(scope, 99)


def overall_agreement_from_file(classified_hits: Path | None) -> dict[str, Any]:
    if classified_hits is None or not classified_hits.exists():
        return empty_agreement_row("overall")
    by_hit: dict[str, dict[str, bool]] = defaultdict(dict)
    with classified_hits.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("classifier_mode") in {"deterministic", "llm"}:
                by_hit[row["hit_id"]][row["classifier_mode"]] = row.get("is_relevant") == "true"
    pairs = [values for values in by_hit.values() if "deterministic" in values and "llm" in values]
    total = len(pairs)
    if not total:
        return empty_agreement_row("overall")
    agree = sum(1 for values in pairs if values["deterministic"] == values["llm"])
    det_only = sum(1 for values in pairs if values["deterministic"] and not values["llm"])
    llm_only = sum(1 for values in pairs if values["llm"] and not values["deterministic"])
    return {
        "scope": "overall",
        "term_id": "",
        "term": "",
        "language": "",
        "corpus": "",
        "agreement_rate": format_float(agree / total),
        "agreement_kappa": "",
        "deterministic_only_relevant_count": det_only,
        "llm_only_relevant_count": llm_only,
        "disagreement_count": det_only + llm_only,
    }


def overall_agreement_from_db(db: Path | None, table: str) -> dict[str, Any]:
    if db is None:
        return empty_agreement_row("overall")
    qtable = quote_identifier(sanitize_table_name(table))
    rows = fetch_dicts(
        db_path=db,
        query=f"""
            WITH paired AS (
                SELECT
                    hit_id,
                    max(CASE WHEN classifier_mode = 'deterministic' THEN is_relevant END) AS deterministic_relevant,
                    max(CASE WHEN classifier_mode = 'llm' THEN is_relevant END) AS llm_relevant
                FROM {qtable}
                WHERE classifier_mode IN ('deterministic', 'llm')
                GROUP BY hit_id
                HAVING deterministic_relevant IS NOT NULL AND llm_relevant IS NOT NULL
            )
            SELECT
                count(*) AS total,
                sum(CASE WHEN deterministic_relevant = llm_relevant THEN 1 ELSE 0 END) AS agree,
                sum(CASE WHEN deterministic_relevant = 'true' AND llm_relevant != 'true' THEN 1 ELSE 0 END) AS det_only,
                sum(CASE WHEN llm_relevant = 'true' AND deterministic_relevant != 'true' THEN 1 ELSE 0 END) AS llm_only
            FROM paired
        """,
    )
    if not rows or int_value(rows[0].get("total")) == 0:
        return empty_agreement_row("overall")
    total = int_value(rows[0]["total"])
    agree = int_value(rows[0]["agree"])
    det_only = int_value(rows[0]["det_only"])
    llm_only = int_value(rows[0]["llm_only"])
    return {
        "scope": "overall",
        "term_id": "",
        "term": "",
        "language": "",
        "corpus": "",
        "agreement_rate": format_float(agree / total),
        "agreement_kappa": "",
        "deterministic_only_relevant_count": det_only,
        "llm_only_relevant_count": llm_only,
        "disagreement_count": det_only + llm_only,
    }


def empty_agreement_row(scope: str) -> dict[str, Any]:
    return {
        "scope": scope,
        "term_id": "",
        "term": "",
        "language": "",
        "corpus": "",
        "agreement_rate": "",
        "agreement_kappa": "",
        "deterministic_only_relevant_count": "",
        "llm_only_relevant_count": "",
        "disagreement_count": "",
    }


def write_markdown(
    path: Path,
    density_rows: list[dict[str, str]],
    hit_examples: list[dict[str, str]],
    bible_control: list[dict[str, Any]],
    edition_meta: list[dict[str, Any]],
    agreement: list[dict[str, Any]],
    relevance_scope: list[dict[str, Any]],
    manifest_path: Path,
) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    zero_secular_rows = sum(1 for row in bible_control if float_value(str(row.get("secular_max_density", ""))) == 0)
    lines = [
        "# CRD Report",
        "",
        "Status: generated from the Centered-Relevance Density matrix.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "python3 -m scripts.run_crd_density protocols/centered_relevance_density.toml --resume",
        "python3 -m scripts.build_crd_comparison",
        "```",
        "",
        "## Summary",
        "",
        f"- density rows: {len(density_rows)}",
        f"- term/control comparison rows: {len(bible_control)}",
        f"- edition summary rows: {len(edition_meta)}",
        f"- classifier agreement rows: {len(agreement)}",
        f"- rows with secular max density = 0: {zero_secular_rows}",
        f"- manifest status: {manifest.get('status', '')}",
        "",
        "## Bible vs Secular Controls",
        "",
        "| Classifier | Term | Bible max | Secular max | Ratio | Exceeds secular max |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in ranked_bible_control_rows(bible_control)[:25]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["classifier_mode"]),
                    f"`{row['term_id']}`",
                    str(row["bible_max_density"]),
                    str(row["secular_max_density"]),
                    str(row["ratio"]),
                    str(row["exceeds_secular_max"]),
                ]
            )
            + " |"
        )
    finite_rows = finite_ratio_rows(bible_control)
    if finite_rows:
        lines.extend(
            [
                "",
                "## Top Finite Bible-Vs-Control Ratios",
                "",
                "| Classifier | Term | Bible max | Bible corpus | Secular max | Secular corpus | Ratio |",
                "| --- | --- | ---: | --- | ---: | --- | ---: |",
            ]
        )
        for row in finite_rows[:25]:
            lines.append(bible_control_detail_row(row))
    zero_rows = zero_secular_bible_rows(bible_control)
    if zero_rows:
        lines.extend(
            [
                "",
                "## Top Bible Hits With Secular Max Zero",
                "",
                "| Classifier | Term | Bible max | Bible corpus |",
                "| --- | --- | ---: | --- |",
            ]
        )
        for row in zero_rows[:25]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["classifier_mode"]),
                        f"`{row['term_id']}`",
                        str(row["bible_max_density"]),
                        str(row["bible_max_corpus"]),
                    ]
                )
                + " |"
            )
    if relevance_scope:
        lines.extend(
            [
                "",
                "## Relevance Scope Summary",
                "",
                "| Classifier | Corpus class | Term | Scope | Relevant hits |",
                "| --- | --- | --- | --- | ---: |",
            ]
        )
        for row in relevance_scope[:25]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["classifier_mode"]),
                        str(row["corpus_class"]),
                        f"`{row['term_id']}`",
                        str(row["match_scope"]),
                        str(row["relevant_hit_count"]),
                    ]
                )
                + " |"
            )
    lines.extend(
        [
            "",
            "## Representative Relevant Centers",
            "",
            "| Term | Corpus | Center ref | Center word | Type | Scope | Matched keyword | Skip |",
            "| --- | --- | --- | --- | --- | --- | --- | ---: |",
        ]
    )
    for row in hit_examples[:25]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.get('term_id', '')}`",
                    row.get("corpus", ""),
                    row.get("center_ref", ""),
                    row.get("center_word", ""),
                    row.get("relevance_type", ""),
                    row.get("surface_match_scope", ""),
                    row.get("matched_surface_keyword", ""),
                    row.get("skip", ""),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- CRD is a density screen, not a claim promotion engine.",
            "- Deterministic mode only reports locked exact dictionary matches.",
            "- Concept-code matches require explicit surface/context concept fields; hidden-term metadata alone is not counted.",
            "- Secular-control zeroes can reflect dictionary vocabulary and context coverage, not only signal strength.",
            "- LLM and parallel modes require audit-log review before interpretation.",
            "- Interpret results only against the dictionary and preregistration hashes recorded in the manifest.",
        ]
    )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def ranked_bible_control_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            row.get("exceeds_secular_max") != "true",
            row.get("ratio") == "",
            -float_value(str(row.get("ratio", ""))),
            -float_value(str(row.get("bible_max_density", ""))),
            str(row.get("term_id", "")),
        ),
    )


def finite_ratio_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        [row for row in rows if row.get("exceeds_secular_max") == "true" and row.get("ratio")],
        key=lambda row: (-float_value(str(row.get("ratio", ""))), str(row.get("term_id", ""))),
    )


def zero_secular_bible_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        [
            row
            for row in rows
            if row.get("exceeds_secular_max") == "true"
            and not row.get("ratio")
            and float_value(str(row.get("bible_max_density", ""))) > 0
        ],
        key=lambda row: (-float_value(str(row.get("bible_max_density", ""))), str(row.get("term_id", ""))),
    )


def bible_control_detail_row(row: dict[str, Any]) -> str:
    return (
        "| "
        + " | ".join(
            [
                str(row["classifier_mode"]),
                f"`{row['term_id']}`",
                str(row["bible_max_density"]),
                str(row["bible_max_corpus"]),
                str(row["secular_max_density"]),
                str(row["secular_max_corpus"]),
                str(row["ratio"]),
            ]
        )
        + " |"
    )


def relevant_examples_from_file(path: Path, *, limit: int = 25) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = (row for row in csv.DictReader(handle) if row.get("is_relevant") == "true")
        return heapq.nsmallest(limit, rows, key=relevant_example_key)


def relevant_examples_from_db(db: Path, table: str, *, limit: int = 25) -> list[dict[str, str]]:
    qtable = quote_identifier(sanitize_table_name(table))
    return fetch_dicts(
        db_path=db,
        query=f"""
            SELECT *
            FROM {qtable}
            WHERE is_relevant = 'true'
            ORDER BY term_id, corpus, center_ref, abs(try_cast(skip AS INTEGER)), hit_id
            LIMIT {int(limit)}
        """,
    )


def relevant_example_key(row: dict[str, str]) -> tuple[str, str, str, int]:
    return (
        row.get("term_id", ""),
        row.get("corpus", ""),
        row.get("center_ref", ""),
        abs(int_value(row.get("skip"))),
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def float_value(value: str | None) -> float:
    try:
        return float(value or 0)
    except ValueError:
        return 0.0


def int_value(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


def format_float(value: float) -> str:
    return f"{value:.9g}"


def median(values: list[int]) -> float:
    if not values:
        return 0.0
    middle = len(values) // 2
    if len(values) % 2:
        return float(values[middle])
    return (values[middle - 1] + values[middle]) / 2


if __name__ == "__main__":
    raise SystemExit(main())
