#!/usr/bin/env python3
"""Build a compact review report for selected all-codes rows."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.term_display import display_term
from scripts.json_utils import read_json_object


SELECTED_IN = Path("reports/all_codes_followup_selection/selected_rows.csv")
PATH_SUMMARY_IN = Path("reports/all_codes_followup_letter_paths/path_summary.csv")
LETTER_PATHS_IN = Path("reports/all_codes_followup_letter_paths/letter_paths.csv")
EXTENSIONS_SUMMARY_IN = Path("reports/all_codes_followup_extensions/summary.csv")
EXTENSIONS_MANIFEST_IN = Path("reports/all_codes_followup_extensions/manifest.json")
SELECTION_MANIFEST_IN = Path("reports/all_codes_followup_selection/manifest.json")
PATH_MANIFEST_IN = Path("reports/all_codes_followup_letter_paths/manifest.json")
OUT_DIR = Path("reports/all_codes_followup_review")
SUMMARY_OUT = OUT_DIR / "review_summary.csv"
REPORT_OUT = Path("docs/ALL_CODES_FOLLOWUP_REVIEW.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"

SUMMARY_FIELDNAMES = [
    "selection_rank",
    "source_queue",
    "bucket",
    "review_class",
    "review_status",
    "presence_scope",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "skip",
    "direction",
    "center_ref",
    "center_word",
    "center_normalized_word",
    "best_context",
    "path_corpora",
    "path_rows",
    "letter_rows",
    "path_mismatch_rows",
    "extension_rows",
    "compound_extension",
    "max_extension_length",
    "best_extension_type",
    "best_extended_sequence",
    "best_extension_kind",
    "best_extension_corpus",
    "control_band",
    "control_p",
    "control_q",
    "control_read",
    "review_note",
]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    selected_rows = read_rows(args.selected)
    path_rows = read_rows(args.path_summary)
    letter_rows = read_rows(args.letter_paths)
    extension_rows = read_rows(args.extensions_summary)
    selection_manifest = read_json(args.selection_manifest)
    path_manifest = read_json(args.path_manifest)
    extensions_manifest = read_json(args.extensions_manifest)
    run_commit = args.run_commit or git_commit()
    summary_rows = build_summary_rows(selected_rows, path_rows, letter_rows, extension_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    report = build_report(
        summary_rows=summary_rows,
        selection_manifest=selection_manifest,
        path_manifest=path_manifest,
        extensions_manifest=extensions_manifest,
        run_commit=run_commit,
    )
    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    args.report_out.write_text(report, encoding="utf-8")
    write_manifest(
        args.manifest_out,
        run_commit=run_commit,
        summary_rows=summary_rows,
        selected_rows=selected_rows,
        path_rows=path_rows,
        letter_rows=letter_rows,
        extension_rows=extension_rows,
        report_out=args.report_out,
        summary_out=args.summary_out,
    )
    print(args.summary_out)
    print(args.report_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selected", type=Path, default=SELECTED_IN)
    parser.add_argument("--path-summary", type=Path, default=PATH_SUMMARY_IN)
    parser.add_argument("--letter-paths", type=Path, default=LETTER_PATHS_IN)
    parser.add_argument("--extensions-summary", type=Path, default=EXTENSIONS_SUMMARY_IN)
    parser.add_argument("--selection-manifest", type=Path, default=SELECTION_MANIFEST_IN)
    parser.add_argument("--path-manifest", type=Path, default=PATH_MANIFEST_IN)
    parser.add_argument("--extensions-manifest", type=Path, default=EXTENSIONS_MANIFEST_IN)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--report-out", type=Path, default=REPORT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    parser.add_argument("--run-commit")
    return parser


def build_summary_rows(
    selected_rows: list[dict[str, str]],
    path_rows: list[dict[str, str]],
    letter_rows: list[dict[str, str]],
    extension_rows: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    paths_by_rank = group_by(path_rows, "selection_rank")
    letters_by_rank = group_by(letter_rows, "selection_rank")
    extensions_by_rank = group_by(extension_rows or [], "selection_rank")
    output = []
    for row in selected_rows:
        rank = row["selection_rank"]
        paths = paths_by_rank.get(rank, [])
        letters = letters_by_rank.get(rank, [])
        extension = first_or_empty(extensions_by_rank.get(rank, []))
        path_corpora = sorted({path["audit_corpus"] for path in paths})
        mismatch_count = sum(path.get("matches_term") != "True" for path in paths)
        bucket = row.get("bucket", "")
        output.append(
            {
                "selection_rank": rank,
                "source_queue": row.get("source_queue", ""),
                "bucket": bucket,
                "review_class": review_class(bucket),
                "review_status": review_status(bucket, mismatch_count),
                "presence_scope": row.get("presence_scope", ""),
                "term_id": row.get("term_id", ""),
                "concept": row.get("concept", ""),
                "category": row.get("category", ""),
                "normalized_term": row.get("normalized_term", ""),
                "skip": row.get("skip", ""),
                "direction": row.get("direction", ""),
                "center_ref": row.get("center_ref", ""),
                "center_word": row.get("center_word", ""),
                "center_normalized_word": row.get("center_normalized_word", ""),
                "best_context": row.get("best_context", ""),
                "path_corpora": ",".join(path_corpora),
                "path_rows": str(len(paths)),
                "letter_rows": str(len(letters)),
                "path_mismatch_rows": str(mismatch_count),
                "extension_rows": extension.get("extension_rows", "0"),
                "compound_extension": str(is_compound_extension(extension)),
                "max_extension_length": extension.get("max_extension_length", "0"),
                "best_extension_type": extension.get("best_extension_type", ""),
                "best_extended_sequence": extension.get("best_extended_sequence", ""),
                "best_extension_kind": extension.get("best_match_kind", ""),
                "best_extension_corpus": extension.get("best_audit_corpus", ""),
                "control_band": row.get("control_band", ""),
                "control_p": row.get("control_p", ""),
                "control_q": row.get("control_q", ""),
                "control_read": row.get("control_read", ""),
                "review_note": review_note(row, path_corpora, extension),
            }
        )
    return output


def review_class(bucket: str) -> str:
    mapping = {
        "center_word_exact": "same_surface_word_at_center",
        "center_word_same_concept": "related_surface_word_at_center_same_concept",
        "center_word_same_category": "related_surface_word_at_center_same_category",
        "center_verse_exact": "center_verse_contains_term",
        "center_verse_same_concept": "center_verse_contains_related_concept",
        "center_verse_same_category": "center_verse_contains_related_category",
        "span_exact": "span_contains_term",
        "span_same_concept": "span_contains_related_concept",
        "span_same_category": "span_contains_related_category",
        "hidden_path_only": "hidden_path_only",
    }
    return mapping.get(bucket, "unclassified")


def review_status(bucket: str, mismatch_count: int) -> str:
    if mismatch_count:
        return "audit_hold"
    if bucket == "center_word_exact":
        return "strongest_manual_review"
    if bucket.startswith("center_word_same_"):
        return "related_center_word_review"
    if bucket.startswith("center_verse_"):
        return "center_verse_context_review"
    if bucket.startswith("span_"):
        return "span_context_review"
    if bucket == "hidden_path_only":
        return "hidden_path_review"
    return "manual_review"


def review_note(
    row: dict[str, str],
    path_corpora: list[str],
    extension: dict[str, str] | None = None,
) -> str:
    bucket = row.get("bucket", "")
    scope = row.get("presence_scope", "")
    extension_text = extension_note(extension or {})
    if bucket == "hidden_path_only":
        return (
            f"{scope}; no surface echo required; paths audited in {len(path_corpora)} corpora"
            f"{extension_text}"
        )
    if bucket == "center_word_exact":
        return f"{scope}; hidden term centered on same normalized surface word{extension_text}"
    if bucket.startswith("center_word_same_"):
        return f"{scope}; center surface word is related by concept/category flag{extension_text}"
    if bucket.startswith("center_verse_"):
        return f"{scope}; center verse carries exact/related surface context{extension_text}"
    if bucket.startswith("span_"):
        return f"{scope}; start-to-end span carries exact/related surface context{extension_text}"
    return f"{scope}{extension_text}"


def extension_note(extension: dict[str, str]) -> str:
    if not extension or int_value(extension.get("extension_rows", "")) == 0:
        return ""
    best_type = extension.get("best_extension_type", "")
    best_sequence = extension.get("best_extended_sequence", "")
    best_corpus = extension.get("best_audit_corpus", "")
    if is_compound_extension(extension):
        return (
            "; compound same-skip extension "
            f"{display_with_fallback(best_sequence, 'hidden extension sequence')} "
            f"in {best_corpus}"
        )
    return (
        "; adjacent same-skip extension "
        f"{display_with_fallback(best_sequence, 'hidden extension fragment')} "
        f"in {best_corpus} ({best_type})"
    )


def build_report(
    *,
    summary_rows: list[dict[str, str]],
    selection_manifest: dict[str, Any],
    path_manifest: dict[str, Any],
    run_commit: str,
    extensions_manifest: dict[str, Any] | None = None,
) -> str:
    extensions_manifest = extensions_manifest or {}
    queue_counts = Counter(row["source_queue"] for row in summary_rows)
    class_counts = Counter(row["review_class"] for row in summary_rows)
    status_counts = Counter(row["review_status"] for row in summary_rows)
    compound_count = sum(row["compound_extension"] == "True" for row in summary_rows)
    lines = [
        "# All-Codes Follow-Up Review",
        "",
        "Status: manual review packet, not a claim.",
        "",
        "This combines the compact all-codes follow-up selection with reconstructed",
        "letter paths. It keeps both categories visible: hidden-path-only rows and",
        "the rarer rows where the hidden path is centered on, or near, related",
        "surface wording.",
        "",
        "## Run",
        "",
        "| Field | Value |",
        "| --- | --- |",
        "| Local report build commit | recorded in local manifest only |",
        "| Selection protocol | `protocols/all_codes_followup_selection.toml` |",
        "| Letter-path protocol | `protocols/all_codes_followup_letter_paths.toml` |",
        f"| Selection rows | {selection_manifest.get('selected_rows', len(summary_rows)):,} |",
        f"| Path rows | {path_manifest.get('summary_rows', 0):,} |",
        f"| Letter rows | {path_manifest.get('letter_rows', 0):,} |",
        f"| Path mismatches | {path_manifest.get('mismatches', 0):,} |",
        f"| Rows with same-skip extensions | {extensions_manifest.get('selected_rows_with_extensions', 0):,} |",
        f"| Rows with compound same-skip extensions | {extensions_manifest.get('selected_rows_with_compound_extensions', compound_count):,} |",
        f"| Extension rows | {extensions_manifest.get('extension_rows', 0):,} |",
        "",
        "For resumed protocol runs, this subreport can remain cached. The build",
        "commit is recorded in the local manifest; the top-level",
        "`reports/real_report_run/summary.md` records the current assembly commit.",
        "",
        "## Counts",
        "",
        "| Group | Count |",
        "| --- | ---: |",
    ]
    for label, count in sorted(queue_counts.items()):
        lines.append(f"| queue `{label}` | {count:,} |")
    for label, count in sorted(status_counts.items()):
        lines.append(f"| status `{label}` | {count:,} |")
    lines.extend(
        [
            "",
            "| Review class | Rows |",
            "| --- | ---: |",
        ]
    )
    for label, count in sorted(class_counts.items()):
        lines.append(f"| `{label}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Review Rows",
            "",
            "| Rank | Queue | Status | Term | Concept | Skip | Center | Center word | Corpora | Best extension | Note |",
            "| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for row in summary_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["selection_rank"],
                    row["source_queue"],
                    f"`{row['review_status']}`",
                    display_term(row["normalized_term"], english=row["concept"]),
                    row["concept"],
                    row["skip"],
                    row["center_ref"],
                    center_word_display(row),
                    row["path_corpora"],
                    extension_cell(row),
                    row["review_note"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "These rows are a human-review work queue. The strongest manual-review",
            "subtype is `center_word_exact`, where the hidden word is centered on the",
            "same normalized surface word. Related center-word, center-verse, and",
            "span-context rows are weaker but still useful for review. Hidden-path-only",
            "rows stay in the packet because an open-text echo is not required for an",
            "ELS candidate.",
            "",
            "Same-skip extension rows show that a hidden lane can be extended into a",
            "surface-attested word or phrase. Compound extensions contain the hidden",
            "term plus adjacent before/after letters. Adjacent-only extensions are",
            "logged but weaker because they do not contain the hidden term.",
            "",
            "Original-language report cells use committed glossary entries when one",
            "is available. When no locked gloss exists for an inflected surface word",
            "or short extension fragment, the English parenthetical is a descriptive",
            "review fallback, not a lexical translation.",
            "",
            "This report does not add statistical support. It packages rows for",
            "inspection after the broad screen.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def group_by(rows: list[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row[key]].append(row)
    return grouped


def first_or_empty(rows: list[dict[str, str]]) -> dict[str, str]:
    return rows[0] if rows else {}


def is_compound_extension(extension: dict[str, str]) -> bool:
    return extension.get("best_extension_type", "") in {
        "before_plus_term",
        "term_plus_after",
        "before_plus_term_plus_after",
    }


def extension_cell(row: dict[str, str]) -> str:
    if row.get("best_extended_sequence", ""):
        return (
            f"{display_with_fallback(row['best_extended_sequence'], 'hidden extension sequence')} "
            f"({row['best_extension_type']}; {row['best_extension_corpus']})"
        )
    return ""


def center_word_display(row: dict[str, str]) -> str:
    fallback = center_word_gloss(row)
    return display_with_fallback(row.get("center_word", ""), fallback)


def center_word_gloss(row: dict[str, str]) -> str:
    concept = row.get("concept", "").strip()
    if row.get("center_word_exact") == "True" and concept:
        return concept
    if concept:
        return f"center surface word in {concept} review row"
    return "center surface word"


def display_with_fallback(value: str, fallback_english: str) -> str:
    rendered = display_term(value)
    if "English:" in rendered or not fallback_english:
        return rendered
    return display_term(value, english=fallback_english)


def int_value(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def write_manifest(
    path: Path,
    *,
    run_commit: str,
    summary_rows: list[dict[str, str]],
    selected_rows: list[dict[str, str]],
    path_rows: list[dict[str, str]],
    letter_rows: list[dict[str, str]],
    extension_rows: list[dict[str, str]],
    report_out: Path,
    summary_out: Path,
) -> None:
    payload = {
        "tool": "build_all_codes_followup_report",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "run_commit": run_commit,
        "selected_rows": len(selected_rows),
        "summary_rows": len(summary_rows),
        "path_rows": len(path_rows),
        "letter_rows": len(letter_rows),
        "extension_summary_rows": len(extension_rows),
        "path_mismatch_rows": sum(int(row["path_mismatch_rows"]) for row in summary_rows),
        "rows_with_extensions": sum(int_value(row["extension_rows"]) > 0 for row in summary_rows),
        "rows_with_compound_extensions": sum(
            row["compound_extension"] == "True" for row in summary_rows
        ),
        "review_status_counts": dict(
            sorted(Counter(row["review_status"] for row in summary_rows).items())
        ),
        "review_class_counts": dict(
            sorted(Counter(row["review_class"] for row in summary_rows).items())
        ),
        "outputs": [str(summary_out), str(report_out), str(path)],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return read_json_object(path)


def git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
