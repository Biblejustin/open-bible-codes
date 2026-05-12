#!/usr/bin/env python3
"""Build a readable report for broad-search surface-context follow-up."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import load_corpus
from els.term_display import display_term


SUMMARY = Path("reports/windows_cpu/broad_2_500/followup_surface_context_full_context_summary.csv")
HITS = Path("reports/windows_cpu/broad_2_500/followup_surface_context_full_context.csv")
CONTROL_SUMMARY = SUMMARY
CONTROL_HITS = HITS
OUT = Path("docs/WINDOWS_CPU_BROAD_2_500_SURFACE_FOLLOWUP.md")
MANIFEST_OUT = Path("reports/windows_cpu/broad_2_500/followup_surface_report.manifest.json")
DEFAULT_CORPUS_CONFIGS = {
    "MT_WLC": Path("configs/example_oshb_wlc.toml"),
    "UXLC": Path("configs/example_uxlc.toml"),
    "MAM": Path("configs/example_mam.toml"),
    "EBIBLE_WLC": Path("configs/example_ebible_hebwlc.toml"),
    "UHB": Path("configs/example_uhb.toml"),
    "LXX": Path("configs/example_ebible_grclxx.toml"),
    "TR_NT": Path("configs/example_ebible_grctr.toml"),
    "BYZ_NT": Path("configs/example_ebible_grcmt.toml"),
    "TCG_NT": Path("configs/example_ebible_grctcgnt.toml"),
    "SBLGNT": Path("configs/example_sblgnt.toml"),
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    summary_rows = read_rows(args.summary)
    hit_rows = read_rows(args.hits)
    control_summary_rows = read_rows(args.control_summary) if args.control_summary.exists() else []
    control_hit_rows = read_rows(args.control_hits) if args.control_hits.exists() else []
    if args.control_summary == args.summary:
        control_summary_rows = [row for row in summary_rows if corpus_class(row.get("corpus", "")) == "control"]
        summary_rows = [row for row in summary_rows if corpus_class(row.get("corpus", "")) == "bible"]
    if args.control_hits == args.hits:
        control_hit_rows = [row for row in hit_rows if corpus_class(row.get("corpus", "")) == "control"]
        hit_rows = [row for row in hit_rows if corpus_class(row.get("corpus", "")) == "bible"]
    write_markdown(args.out, summary_rows, hit_rows, control_summary_rows, control_hit_rows, args)
    write_manifest(args.manifest_out, args, summary_rows, hit_rows, control_summary_rows, control_hit_rows, started)
    print(args.out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=SUMMARY)
    parser.add_argument("--hits", type=Path, default=HITS)
    parser.add_argument("--control-summary", type=Path, default=CONTROL_SUMMARY)
    parser.add_argument("--control-hits", type=Path, default=CONTROL_HITS)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    parser.add_argument("--title", default="Windows CPU Broad 2..500 Surface Follow-Up")
    parser.add_argument("--summary-limit", type=int, default=30)
    parser.add_argument("--hidden-only-limit", type=int, default=20)
    parser.add_argument(
        "--corpus-config",
        action="append",
        default=[],
        help="Corpus config as LABEL=path. Defaults cover the broad follow-up Bible corpora.",
    )
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, str]],
    hit_rows: list[dict[str, str]],
    control_summary_rows: list[dict[str, str]],
    control_hit_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exact_center_word_hits = [row for row in hit_rows if is_true(row.get("center_word_exact"))]
    control_exact_center_word_hits = [
        row for row in control_hit_rows if is_true(row.get("center_word_exact"))
    ]
    center_verses = center_verse_lookup(exact_center_word_hits, corpus_configs(args.corpus_config))
    context_rows = [row for row in summary_rows if int_value(row.get("context_hit_count")) > 0]
    control_context_rows = [
        row for row in control_summary_rows if int_value(row.get("context_hit_count")) > 0
    ]
    hidden_only_rows = [
        row
        for row in summary_rows
        if int_value(row.get("hit_count")) > 0 and int_value(row.get("context_hit_count")) == 0
    ]
    by_corpus = Counter(row["corpus"] for row in hit_rows)
    lines = [
        f"# {args.title}",
        "",
        "This is a full contextual follow-up to the Windows CPU broad `2..500`",
        "Bible-control comparison. It uses the 30 strongest original-language",
        "Bible-over-control rows as a review queue, then runs `surface-context`",
        "without a per-term hit cap. The summary counts all hidden hits in scope;",
        "the hit CSV writes context-bearing rows rather than exporting every hit.",
        "",
        "## Scope",
        "",
        f"- summary input: `{args.summary}`",
        f"- hit input: `{args.hits}`",
        f"- summary rows: {len(summary_rows)}",
        f"- context hit rows written: {len(hit_rows)}",
        f"- summary rows with any surface context: {len(context_rows)}",
        f"- exact center-word hit rows: {len(exact_center_word_hits)}",
        f"- corpora represented in context hit rows: {len(by_corpus)}",
        f"- control summary rows: {len(control_summary_rows)}",
        f"- control context hit rows written: {len(control_hit_rows)}",
        f"- control exact center-word hit rows: {len(control_exact_center_word_hits)}",
        "",
        "## Main Read",
        "",
        "- Exact center-word hits are rare but present in this full contextual follow-up.",
        "- The matched non-Bible controls produced zero exact center-word hits under the same uncapped summary rules.",
        "- The Jesus/Joshua rows share the same normalized Greek spelling (`ιησουσ`), so referent review matters.",
        "- The `Bashan` rows are morphological/substring matches to torment language, not the place name Bashan.",
        "- Summary rows with context count zero are still retained as hidden-path-only evidence.",
        "- This is a complete summary count for the selected terms and corpora, not a full row export of every hit.",
        "",
        "## Bible Vs Control Surface Follow-Up",
        "",
        "| Cohort | Summary rows | Context hit rows written | Rows with context | Exact center-word hit rows |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| Bible corpora | {len(summary_rows)} | {len(hit_rows)} | {len(context_rows)} | {len(exact_center_word_hits)} |",
        f"| Non-Bible controls | {len(control_summary_rows)} | {len(control_hit_rows)} | {len(control_context_rows)} | {len(control_exact_center_word_hits)} |",
        "",
        "## Exact Center-Word Hits",
        "",
        "| Term | Corpus | Skip | Center | Surface word | Center verse text | Path | Context refs |",
        "| --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in exact_center_word_hits:
        lines.append(exact_hit_row(row, center_verses))
    lines.extend(
        [
            "",
            "## Highest Surface-Context Summary Rows",
            "",
            "| Term | Corpus | Hidden hits counted | Context hits | Exact center-word | Exact center | Exact span | Same-category span |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in sorted(context_rows, key=context_sort_key, reverse=True)[: args.summary_limit]:
        lines.append(summary_row(row))
    lines.extend(
        [
            "",
            "## Highest Control Surface-Context Rows",
            "",
            "Controls still produce many center/span surface-context rows. What they",
            "did not produce in this full pass is an exact center-word row.",
            "",
            "| Term | Corpus | Hidden hits counted | Context hits | Exact center-word | Exact center | Exact span | Same-category span |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in sorted(control_context_rows, key=context_sort_key, reverse=True)[: args.summary_limit]:
        lines.append(summary_row(row))
    lines.extend(
        [
            "",
            "## Hidden-Path-Only Summary Rows",
            "",
            "These summary rows had hidden hits in the full contextual follow-up but no exact,",
            "same-concept, or same-category surface-context promotion.",
            "",
            "| Term | Corpus | Hidden hits counted | Exact center-word | Context hits |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in sorted(hidden_only_rows, key=lambda item: int_value(item["hit_count"]), reverse=True)[
        : args.hidden_only_limit
    ]:
        lines.append(
            "| "
            + " | ".join(
                [
                    term_cell(row),
                    row["corpus"],
                    row["hit_count"],
                    row["exact_center_word_hits"],
                    row["context_hit_count"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Corpus Hit Rows",
            "",
            "| Corpus | Context hit rows written |",
            "| --- | ---: |",
        ]
    )
    for corpus, count in by_corpus.most_common():
        lines.append(f"| {corpus} | {count} |")
    lines.extend(
        [
            "",
            "## Caution",
            "",
            "This follow-up intentionally keeps hidden-path-only rows. The meaningful",
            "next distinction is not frequency alone; it is whether a hidden path is",
            "centered on the same word, a related word, a relevant center verse, or",
            "only present as a hidden sequence without surface support.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def exact_hit_row(
    row: dict[str, str],
    center_verses: dict[tuple[str, str], str] | None = None,
) -> str:
    path = f"{row['start_ref']} -> {row['end_ref']}"
    center = f"{row['center_ref']}"
    refs = row.get("span_exact_refs") or row.get("span_same_category_refs") or ""
    center_text = ""
    if center_verses is not None:
        center_text = center_verses.get((row["corpus"], row["center_ref"]), "")
    return (
        f"| {term_cell(row)} | {row['corpus']} | {row['skip']} | {center} "
        f"| `{row['center_word']}` | {markdown_cell(center_text)} | {path} | {refs} |"
    )


def summary_row(row: dict[str, str]) -> str:
    return (
        f"| {term_cell(row)} | {row['corpus']} | {row['hit_count']} | {row['context_hit_count']} "
        f"| {row['exact_center_word_hits']} | {row['exact_center_hits']} "
        f"| {row['exact_span_hits']} | {row['same_category_span_hits']} |"
    )


def term_cell(row: dict[str, str]) -> str:
    return f"`{row['term_id']}` {display_term(row['normalized_term'], english=row['concept'])}"


def corpus_configs(values: list[str]) -> dict[str, Path]:
    configs = dict(DEFAULT_CORPUS_CONFIGS)
    for value in values:
        label, separator, path = value.partition("=")
        if not separator:
            raise ValueError(f"corpus config must be LABEL=path: {value}")
        configs[label] = Path(path)
    return configs


def corpus_class(corpus_label: str) -> str:
    return "control" if corpus_label.startswith(("HEB_", "GRK_", "ENG_")) else "bible"


def center_verse_lookup(
    rows: list[dict[str, str]],
    configs: dict[str, Path],
) -> dict[tuple[str, str], str]:
    wanted_by_corpus: dict[str, set[str]] = {}
    for row in rows:
        wanted_by_corpus.setdefault(row["corpus"], set()).add(row["center_ref"])
    output = {}
    for corpus_label, refs in wanted_by_corpus.items():
        config = configs.get(corpus_label)
        if config is None or not config.exists():
            continue
        corpus = load_corpus(config)
        verses_by_ref = {verse.ref: verse.raw_text for verse in corpus.verses}
        for ref in refs:
            output[(corpus_label, ref)] = verses_by_ref.get(ref, "")
    return output


def markdown_cell(value: str, *, limit: int = 180) -> str:
    compact = " ".join(value.split())
    if len(compact) > limit:
        compact = compact[: limit - 1].rstrip() + "…"
    return compact.replace("|", "\\|")


def context_sort_key(row: dict[str, str]) -> tuple[int, int, int, int]:
    return (
        int_value(row.get("exact_center_word_hits")),
        int_value(row.get("exact_center_hits")),
        int_value(row.get("context_hit_count")),
        int_value(row.get("hit_count")),
    )


def is_true(value: object) -> bool:
    return str(value) == "True"


def int_value(value: object) -> int:
    if value in {None, ""}:
        return 0
    return int(str(value))


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary_rows: list[dict[str, str]],
    hit_rows: list[dict[str, str]],
    control_summary_rows: list[dict[str, str]],
    control_hit_rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "script": "scripts/build_broad_surface_followup_report.py",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "summary": str(args.summary),
        "hits": str(args.hits),
        "control_summary": str(args.control_summary),
        "control_hits": str(args.control_hits),
        "summary_rows": len(summary_rows),
        "hit_rows": len(hit_rows),
        "control_summary_rows": len(control_summary_rows),
        "control_hit_rows": len(control_hit_rows),
        "out": str(args.out),
        "git_commit": git_commit(),
        "seconds": round(time.perf_counter() - started, 3),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
