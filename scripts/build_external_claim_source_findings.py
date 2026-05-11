#!/usr/bin/env python3
"""Build a concise findings layer for external-source ELS term runs."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.term_display import display_term


DEFAULT_COUNTS_SUMMARY = Path("reports/external_claim_source_counts/summary.csv")
DEFAULT_ALL_CODES_SUMMARY = Path(
    "reports/external_claim_source_all_codes/surface_all_codes_summary.csv"
)
DEFAULT_TRIAGE_QUEUE = Path("reports/external_claim_source_all_codes/triage_queue.csv")
DEFAULT_MARKDOWN = Path("docs/EXTERNAL_CLAIM_SOURCE_FINDINGS.md")
DEFAULT_MANIFEST = Path("reports/external_claim_source_all_codes/findings.manifest.json")

CONTROL_CORPORA = {
    "HEB_AHAD_HAAM",
    "HEB_BIALIK",
    "HEB_BRENNER",
    "GRK_ILIAD",
    "GRK_ODYSSEY",
    "GRK_HERODOTUS",
    "ENG_MOBY_DICK",
    "ENG_SHAKESPEARE",
    "ENG_WAR_AND_PEACE",
}

SUMMARY_FIELDS = (
    "hit_count",
    "context_hit_count",
    "exact_center_word_hits",
    "same_concept_center_word_hits",
    "same_category_center_word_hits",
    "exact_center_hits",
    "same_concept_center_hits",
    "same_category_center_hits",
    "exact_span_hits",
    "same_concept_span_hits",
    "same_category_span_hits",
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    count_rows = read_rows(args.counts_summary)
    summary_rows = read_rows(args.all_codes_summary)
    queue_rows = read_rows(args.triage_queue)
    findings = build_findings(count_rows, summary_rows, queue_rows)
    write_markdown(args.markdown_out, args, findings)
    write_manifest(args.manifest_out, args, findings, started)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts-summary", type=Path, default=DEFAULT_COUNTS_SUMMARY)
    parser.add_argument("--all-codes-summary", type=Path, default=DEFAULT_ALL_CODES_SUMMARY)
    parser.add_argument("--triage-queue", type=Path, default=DEFAULT_TRIAGE_QUEUE)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--top", type=int, default=12)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_findings(
    count_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    queue_rows: list[dict[str, str]],
) -> dict[str, Any]:
    corpus_summary = summarize_by_corpus_class(summary_rows)
    return {
        "count_rows": len(count_rows),
        "count_total_hits": sum(int_value(row, "total_hits") for row in count_rows),
        "count_term_sets": len({row.get("term_set", "") for row in count_rows}),
        "count_corpora": len({row.get("corpus", "") for row in count_rows}),
        "all_codes_summary_rows": len(summary_rows),
        "triage_rows": len(queue_rows),
        "corpus_summary": corpus_summary,
        "queue_bucket_counts": dict(Counter(row.get("bucket", "") for row in queue_rows)),
        "top_bible_center_word_exact_terms": top_terms(
            summary_rows,
            corpus_class_filter="bible",
            field="exact_center_word_hits",
        ),
        "top_control_center_word_exact_terms": top_terms(
            summary_rows,
            corpus_class_filter="control",
            field="exact_center_word_hits",
        ),
        "top_bible_queue_rows": top_queue_rows(queue_rows, require_bible=True),
        "top_control_queue_rows": top_queue_rows(queue_rows, require_control=True),
    }


def summarize_by_corpus_class(rows: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {
        "bible": empty_summary_bucket(),
        "control": empty_summary_bucket(),
    }
    terms_by_class: dict[str, set[str]] = {"bible": set(), "control": set()}
    corpora_by_class: dict[str, set[str]] = {"bible": set(), "control": set()}
    for row in rows:
        label = corpus_class(row.get("corpus", ""))
        bucket = summary[label]
        terms_by_class[label].add(row.get("term_id", ""))
        corpora_by_class[label].add(row.get("corpus", ""))
        bucket["rows"] += 1
        for field in SUMMARY_FIELDS:
            bucket[field] += int_value(row, field)
    for label, bucket in summary.items():
        bucket["terms"] = len({term for term in terms_by_class[label] if term})
        bucket["corpora"] = len({corpus for corpus in corpora_by_class[label] if corpus})
        bucket["center_word_related_hits"] = (
            bucket["same_concept_center_word_hits"] + bucket["same_category_center_word_hits"]
        )
        bucket["center_verse_related_hits"] = (
            bucket["same_concept_center_hits"] + bucket["same_category_center_hits"]
        )
        bucket["span_context_hits"] = (
            bucket["exact_span_hits"]
            + bucket["same_concept_span_hits"]
            + bucket["same_category_span_hits"]
        )
    return summary


def empty_summary_bucket() -> dict[str, Any]:
    return {field: 0 for field in ("rows", *SUMMARY_FIELDS)}


def top_terms(
    rows: list[dict[str, str]],
    *,
    corpus_class_filter: str,
    field: str,
    limit: int = 12,
) -> list[dict[str, Any]]:
    by_term: dict[str, dict[str, Any]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        if corpus_class(row.get("corpus", "")) != corpus_class_filter:
            continue
        term_id = row.get("term_id", "")
        if not term_id:
            continue
        bucket = by_term[term_id]
        if "corpora" not in bucket:
            bucket["corpora"] = set()
        bucket["term_id"] = term_id
        bucket["concept"] = row.get("concept", "")
        bucket["category"] = row.get("category", "")
        bucket["normalized_term"] = row.get("normalized_term", "")
        bucket["value"] += int_value(row, field)
        bucket["hit_count"] += int_value(row, "hit_count")
        bucket["corpora"].add(row.get("corpus", ""))
    ranked = []
    for bucket in by_term.values():
        row = dict(bucket)
        row["corpora"] = sorted(corpus for corpus in bucket["corpora"] if corpus)
        ranked.append(row)
    return sorted(
        ranked,
        key=lambda row: (-int(row["value"]), -int(row["hit_count"]), row["term_id"]),
    )[:limit]


def top_queue_rows(
    rows: list[dict[str, str]],
    *,
    require_bible: bool = False,
    require_control: bool = False,
    limit: int = 12,
) -> list[dict[str, str]]:
    selected = []
    for row in rows:
        corpora = split_corpora(row.get("present_corpora", ""))
        if require_bible and not any(corpus_class(corpus) == "bible" for corpus in corpora):
            continue
        if require_control and not any(corpus_class(corpus) == "control" for corpus in corpora):
            continue
        selected.append(row)
    return sorted(
        selected,
        key=lambda row: (
            int_value(row, "overall_rank"),
            int_value(row, "bucket_rank"),
            row.get("term_id", ""),
        ),
    )[:limit]


def split_corpora(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def corpus_class(corpus: str) -> str:
    return "control" if corpus in CONTROL_CORPORA else "bible"


def write_markdown(path: Path, args: argparse.Namespace, findings: dict[str, Any]) -> None:
    top = args.top
    bible = findings["corpus_summary"]["bible"]
    control = findings["corpus_summary"]["control"]
    lines = [
        "# External Claim Source Findings",
        "",
        "Concise findings layer over the external-source count baseline and relaxed",
        "all-codes collection. This document does not reproduce any outside claim;",
        "it states what the current shared pipeline detected and how Bible rows",
        "compare with language-matched secular controls.",
        "",
        "## Inputs",
        "",
        f"- Counts summary: `{args.counts_summary}`",
        f"- All-codes summary: `{args.all_codes_summary}`",
        f"- Triage queue: `{args.triage_queue}`",
        "",
        "## Main Read",
        "",
        "- External-source terms do produce many hidden paths under skip 2..100.",
        "- Bible and secular-control corpora both produce high-volume rows, especially for short/common forms.",
        "- Same center-word rows exist and should be reviewed as occurrences.",
        "- Claim-grade reproduction still requires source-specific geometry and locked controls.",
        "",
        "## Bible Vs Control Summary",
        "",
        "| Class | Corpora | Terms | Summary rows | Hidden hits | Context hits | Center word same | Center word related |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        summary_row("Bible", bible),
        summary_row("Controls", control),
        "",
        "## Top Bible Center-Word Exact Terms",
        "",
        "| Rank | Term | Corpora | Center-word same hits | Hidden hits |",
        "| ---: | --- | --- | ---: | ---: |",
    ]
    for index, row in enumerate(findings["top_bible_center_word_exact_terms"][:top], start=1):
        lines.append(term_row(index, row))
    lines.extend(
        [
            "",
            "## Top Control Center-Word Exact Terms",
            "",
            "| Rank | Term | Corpora | Center-word same hits | Hidden hits |",
            "| ---: | --- | --- | ---: | ---: |",
        ]
    )
    for index, row in enumerate(findings["top_control_center_word_exact_terms"][:top], start=1):
        lines.append(term_row(index, row))
    lines.extend(
        [
            "",
            "## Top Bible Triage Rows",
            "",
            "| Rank | Bucket | Scope | Term | Center | Present corpora |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for row in findings["top_bible_queue_rows"][:top]:
        lines.append(queue_row(row))
    lines.extend(
        [
            "",
            "## Top Control Triage Rows",
            "",
            "| Rank | Bucket | Scope | Term | Center | Present corpora |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for row in findings["top_control_queue_rows"][:top]:
        lines.append(queue_row(row))
    lines.extend(
        [
            "",
            "## Triage Bucket Counts",
            "",
            "| Bucket | Rows |",
            "| --- | ---: |",
        ]
    )
    for bucket, count in sorted(
        findings["queue_bucket_counts"].items(),
        key=lambda item: (-item[1], item[0]),
    ):
        lines.append(f"| `{bucket}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Cautions",
            "",
            "- This is a screening/findings layer, not a claim-reproduction layer.",
            "- Repeated concepts across multiple source term files can duplicate the same normalized form.",
            "- Center-word exact rows are occurrence facts; frequency and controls still govern evidential weight.",
            "- Longer source claims require source-specific matrix geometry, not only ELS hit counting.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def summary_row(label: str, bucket: dict[str, Any]) -> str:
    return (
        f"| {label} | {bucket['corpora']:,} | {bucket['terms']:,} | {bucket['rows']:,} | "
        f"{bucket['hit_count']:,} | {bucket['context_hit_count']:,} | "
        f"{bucket['exact_center_word_hits']:,} | {bucket['center_word_related_hits']:,} |"
    )


def term_row(index: int, row: dict[str, Any]) -> str:
    term = f"{row['term_id']} {display_term(row.get('normalized_term', ''), english=row.get('concept', ''))}"
    return (
        f"| {index} | {md_cell(term)} | {md_cell(', '.join(row.get('corpora', [])))} | "
        f"{int(row.get('value', 0)):,} | {int(row.get('hit_count', 0)):,} |"
    )


def queue_row(row: dict[str, str]) -> str:
    term = f"{row.get('term_id', '')} {display_term(row.get('normalized_term', ''), english=row.get('concept', ''))}"
    center = (
        f"{row.get('center_ref', '')} "
        f"{display_term(row.get('center_normalized_word', ''))}"
    )
    return (
        "| "
        + " | ".join(
            [
                row.get("overall_rank", ""),
                f"`{row.get('bucket', '')}`",
                f"`{row.get('presence_scope', '')}`",
                md_cell(term),
                md_cell(center),
                md_cell(row.get("present_corpora", "")),
            ]
        )
        + " |"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    findings: dict[str, Any],
    started: float,
) -> None:
    payload = {
        "tool": "build_external_claim_source_findings",
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "git_commit": git_commit(),
        "inputs": {
            "counts_summary": str(args.counts_summary),
            "all_codes_summary": str(args.all_codes_summary),
            "triage_queue": str(args.triage_queue),
        },
        "outputs": {
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "count_rows": findings["count_rows"],
        "count_total_hits": findings["count_total_hits"],
        "all_codes_summary_rows": findings["all_codes_summary_rows"],
        "triage_rows": findings["triage_rows"],
        "corpus_summary": findings["corpus_summary"],
        "queue_bucket_counts": findings["queue_bucket_counts"],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def int_value(row: dict[str, Any], field: str) -> int:
    try:
        return int(float(row.get(field, 0) or 0))
    except (TypeError, ValueError):
        return 0


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
