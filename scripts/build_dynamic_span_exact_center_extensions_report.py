#!/usr/bin/env python3
"""Build a report for exact-center same-skip extension scans."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_DIR = Path("reports/dynamic_skip_focus/exact_center_extensions")
DEFAULT_MARKDOWN = Path("docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_EXTENSIONS.md")
DEFAULT_MANIFEST = DEFAULT_DIR / "report.manifest.json"
DEFAULT_TITLE = "Strong Full-Span Exact-Center Extensions"


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    data = load_report_data(args.input_dir)
    write_markdown(args.markdown_out, data, args)
    write_manifest(args.manifest_out, args, data, started)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--top", type=int, default=25)
    parser.add_argument(
        "--summary-row-limit",
        type=int,
        default=0,
        help="maximum phrase summary rows to print in markdown; 0 prints all rows",
    )
    return parser


def load_report_data(input_dir: Path) -> dict[str, Any]:
    manifests = []
    for path in sorted(input_dir.glob("extensions_*.manifest.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["corpus_label"] = corpus_label_from_manifest_path(path)
        manifests.append(manifest)
    summary_rows = read_many(sorted(input_dir.glob("summary_*.csv")))
    top_rows = read_many(sorted(input_dir.glob("top_*.csv")))
    return {
        "manifests": manifests,
        "summary_rows": summary_rows,
        "top_rows": sorted(top_rows, key=top_sort_key, reverse=True),
    }


def write_markdown(path: Path, data: dict[str, Any], args: argparse.Namespace) -> None:
    manifests = data["manifests"]
    summary_rows = data["summary_rows"]
    top_rows = data["top_rows"]
    total_hits = sum(int(manifest.get("hit_count", 0)) for manifest in manifests)
    total_extensions = sum(int(manifest.get("extension_count", 0)) for manifest in manifests)
    lines = [
        f"# {args.title}",
        "",
        "This report checks same-skip letters immediately before and after the",
        "exact-center paths. It asks whether an exact-centered hidden term",
        "can extend into a surface word or short phrase from the same corpus.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "python3 -m scripts.build_dynamic_span_exact_center_extension_hits ... # build hit-compatible exact-center input",
        "python3 -m els extensions ... # one run per corpus in the input directory",
        "python3 -m els extension-summary ... # one summary per corpus with --match-kind-prefix phrase_",
        reproduce_command(args),
        "```",
        "",
        "## Scope",
        "",
        f"- exact-center paths scanned for extensions: {total_hits:,}",
        f"- raw same-skip extension rows: {total_extensions:,}",
        f"- phrase-filtered summary groups: {len(summary_rows):,}",
        f"- strong phrase-extension rows: {len(top_rows):,}",
        f"- input directory: `{args.input_dir}`",
        "",
        "## Corpus Counts",
        "",
        "| Corpus | Exact-center paths | Raw extension rows | Phrase summary groups | Strong phrase rows |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for manifest in sorted(manifests, key=lambda item: item.get("corpus_label", "")):
        corpus = manifest.get("corpus_label", "")
        lines.append(
            f"| {corpus} | {int(manifest.get('hit_count', 0)):,} | "
            f"{int(manifest.get('extension_count', 0)):,} | "
            f"{sum(1 for row in summary_rows if row['corpus'] == corpus):,} | "
            f"{sum(1 for row in top_rows if row['corpus'] == corpus):,} |"
        )
    lines.extend(
        [
            "",
            "## Strong Phrase Rows",
            "",
            "| Corpus | Term | Center | Extension | Match kind | Match count | Matched examples |",
            "| --- | --- | --- | --- | --- | ---: | --- |",
        ]
    )
    if top_rows:
        for row in top_rows[: args.top]:
            lines.append(strong_row(row))
    else:
        lines.append("| none |  |  |  |  | 0 |  |")
    lines.extend(
        [
            "",
            "## Phrase Summary Rows",
            "",
            "| Corpus | Term | Skip | Direction | Type | Match kind | Rows | Max length | Max match count |",
            "| --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    sorted_summary_rows = sorted(summary_rows, key=summary_sort_key)
    summary_rows_to_print = sorted_summary_rows
    if args.summary_row_limit > 0:
        summary_rows_to_print = sorted_summary_rows[: args.summary_row_limit]
    for row in summary_rows_to_print:
        lines.append(summary_row(row))
    if len(summary_rows_to_print) < len(sorted_summary_rows):
        remaining = len(sorted_summary_rows) - len(summary_rows_to_print)
        lines.append(f"| ... | ... | ... | ... | ... | ... | ... | ... | {remaining:,} more rows in CSV |")
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- `Strong phrase rows` require the hidden term plus adjacent same-skip letters to match a surface phrase.",
            "- `Phrase summary rows` also include before-only or after-only phrase matches, which are weaker.",
            "- Strong phrase-extension rows remain post-screen review material; compare Bible and control reports before treating a row as notable.",
            "- This remains post-screen review material; matched phrases can occur elsewhere in the corpus and need manual context checks.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def strong_row(row: dict[str, str]) -> str:
    extension = f"`{row['extended_sequence']}` ({row['extension_type']})"
    return (
        f"| {row['corpus']} | `{row['normalized_term']}` | {row['center_ref']} | "
        f"{extension} | {row['match_kind']} | {int(row['match_count']):,} | "
        f"{md_cell(row['matched_examples'])} |"
    )


def summary_row(row: dict[str, str]) -> str:
    return (
        f"| {row['corpus']} | `{row['normalized_term']}` | {row['skip']} | {row['direction']} | "
        f"{row['extension_type']} | {row['match_kind']} | {int(row['rows']):,} | "
        f"{int(row['max_extension_length']):,} | {int(row['max_match_count']):,} |"
    )


def read_many(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows.extend(csv.DictReader(handle))
    return rows


def corpus_label_from_manifest_path(path: Path) -> str:
    label = path.name.removeprefix("extensions_").removesuffix(".manifest.json")
    overrides = {
        "ebible_wlc": "EBIBLE_WLC",
        "tcg_nt": "TCG_NT",
    }
    return overrides.get(label, label.upper())


def top_sort_key(row: dict[str, str]) -> tuple[int, int, int, str]:
    return (
        int(row.get("extension_score") or 0),
        int(row.get("extension_length") or 0),
        int(row.get("match_count") or 0),
        row.get("extended_sequence", ""),
    )


def summary_sort_key(row: dict[str, str]) -> tuple[str, str, int, str, str]:
    return (
        row.get("corpus", ""),
        row.get("normalized_term", ""),
        int(row.get("skip") or 0),
        row.get("direction", ""),
        row.get("extension_type", ""),
    )


def write_manifest(path: Path, args: argparse.Namespace, data: dict[str, Any], started: float) -> None:
    payload = {
        "script": "scripts/build_dynamic_span_exact_center_extensions_report.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "input_dir": str(args.input_dir),
        "markdown_out": str(args.markdown_out),
        "title": args.title,
        "summary_row_limit": args.summary_row_limit,
        "extension_manifests": len(data["manifests"]),
        "summary_rows": len(data["summary_rows"]),
        "top_rows": len(data["top_rows"]),
        "git_commit": git_commit(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def reproduce_command(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_dynamic_span_exact_center_extensions_report "
        f"--input-dir {args.input_dir} "
        f"--markdown-out {args.markdown_out} "
        f"--manifest-out {args.manifest_out} "
        f"--title {shell_quote(args.title)} "
        f"--top {args.top} "
        f"--summary-row-limit {args.summary_row_limit}"
    )


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
