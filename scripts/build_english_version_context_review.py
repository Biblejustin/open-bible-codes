#!/usr/bin/env python3
"""Build a short context-review report for English version triage hits."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path


DEFAULT_DIR = Path("reports/english_version_control_triage")


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    summary_rows = read_rows(args.summary)
    hit_rows = read_rows(args.hits)
    triage_rows = {row["term_id"]: row for row in read_rows(args.triage)}
    write_markdown(args.markdown_out, summary_rows, hit_rows, triage_rows, args)
    write_manifest(args, summary_rows, hit_rows, started)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--triage", type=Path, default=DEFAULT_DIR / "triage.csv")
    parser.add_argument("--summary", type=Path, default=DEFAULT_DIR / "context_summary.csv")
    parser.add_argument("--hits", type=Path, default=DEFAULT_DIR / "context_hits.csv")
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_DIR / "context_review.md")
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_DIR / "context_review.manifest.json")
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, str]],
    hit_rows: list[dict[str, str]],
    triage_rows: dict[str, dict[str, str]],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    context_hits = sum(int_value(row.get("context_hit_count")) for row in summary_rows)
    exact_center = sum(int_value(row.get("exact_center_hits")) for row in summary_rows)
    exact_center_word = sum(int_value(row.get("exact_center_word_hits")) for row in summary_rows)
    hit_summary_rows = [row for row in summary_rows if int_value(row.get("hit_count")) > 0]
    flag_counts = Counter(
        triage_rows.get(row["term_id"], {}).get("triage_flag", "unknown")
        for row in hit_summary_rows
    )

    lines = [
        "# English Version Context Review",
        "",
        "This report inspects the seed terms from the target-vs-control triage.",
        "",
        "## Gate Result",
        "",
        f"- term/corpus rows checked: {len(summary_rows)}",
        f"- rows with at least one ELS hit: {len(hit_summary_rows)}",
        f"- exported hit rows: {len(hit_rows)}",
        f"- surface-context hits: {context_hits}",
        f"- exact-center hits: {exact_center}",
        f"- exact-center-word hits: {exact_center_word}",
        "",
    ]
    if context_hits == 0:
        lines.append("Result: no seed term is promoted by surface-context review.")
    else:
        lines.append("Result: at least one seed term has surface-context support.")
    lines.extend(
        [
            "",
            "## Hit Rows By Triage Flag",
            "",
            "| Flag | Rows with hits |",
            "| --- | ---: |",
        ]
    )
    for flag, count in sorted(flag_counts.items()):
        lines.append(f"| `{flag}` | {count} |")
    lines.extend(
        [
            "",
            "## Exported Hit Contexts",
            "",
            "| Corpus | Term | Flag | Hits | Context Hits | First Span | Skip | Best Context |",
            "| --- | --- | --- | ---: | ---: | --- | ---: | --- |",
        ]
    )
    first_hits = first_hit_by_corpus_term(hit_rows)
    for row in sorted(hit_summary_rows, key=lambda item: (item["term_id"], item["corpus"])):
        key = (row["corpus"], row["term_id"])
        hit = first_hits.get(key, {})
        triage = triage_rows.get(row["term_id"], {})
        span = ""
        if hit:
            span = f"{hit.get('start_ref', '')} -> {hit.get('center_ref', '')} -> {hit.get('end_ref', '')}"
        lines.append(
            "| "
            + " | ".join(
                [
                    row["corpus"],
                    f"`{row['term_id']}` {row['concept']}",
                    f"`{triage.get('triage_flag', '')}`",
                    row["hit_count"],
                    row["context_hit_count"],
                    span,
                    hit.get("skip", ""),
                    hit.get("best_context", ""),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Files",
            "",
            f"- Summary CSV: `{args.summary}`",
            f"- Hit CSV: `{args.hits}`",
            f"- Triage CSV: `{args.triage}`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def first_hit_by_corpus_term(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    first: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        first.setdefault((row["corpus"], row["term_id"]), row)
    return first


def int_value(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def write_manifest(
    args: argparse.Namespace,
    summary_rows: list[dict[str, str]],
    hit_rows: list[dict[str, str]],
    started: float,
) -> None:
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "tool": "build_english_version_context_review",
        "created_utc": datetime.now(UTC).isoformat(),
        "summary": str(args.summary.resolve()),
        "hits": str(args.hits.resolve()),
        "triage": str(args.triage.resolve()),
        "summary_rows": len(summary_rows),
        "hit_rows": len(hit_rows),
        "seconds": round(time.perf_counter() - started, 3),
    }
    args.manifest_out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
