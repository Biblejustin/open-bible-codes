#!/usr/bin/env python3
"""Build the tracked report for the expanded Greek prospective screen."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.term_display import display_term
from scripts.json_utils import read_json_object


OUT_DIR = Path("reports/greek_expanded_prospective_exact_center")
SURFACE_SUMMARY = OUT_DIR / "surface_context_summary.csv"
PATTERN_PRESENCE = OUT_DIR / "pattern_presence.csv"
PROTOCOL_MANIFEST = OUT_DIR / "protocol_run.manifest.json"
REPORT_OUT = Path("docs/GREEK_EXPANDED_PROSPECTIVE_REPORT.md")
MANIFEST_OUT = OUT_DIR / "report.manifest.json"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    surface_rows = read_rows(args.surface_summary)
    pattern_rows = read_rows(args.pattern_presence)
    protocol_manifest = read_json(args.protocol_manifest)
    commit = args.run_commit or git_commit()
    report = build_report(
        surface_rows=surface_rows,
        pattern_rows=pattern_rows,
        protocol_manifest=protocol_manifest,
        commit=commit,
    )
    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    args.report_out.write_text(report, encoding="utf-8")
    write_manifest(
        args.manifest_out,
        commit=commit,
        surface_rows=len(surface_rows),
        pattern_rows=len(pattern_rows),
        protocol_manifest=protocol_manifest,
        report_out=args.report_out,
    )
    print(args.report_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface-summary", type=Path, default=SURFACE_SUMMARY)
    parser.add_argument("--pattern-presence", type=Path, default=PATTERN_PRESENCE)
    parser.add_argument("--protocol-manifest", type=Path, default=PROTOCOL_MANIFEST)
    parser.add_argument("--report-out", type=Path, default=REPORT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    parser.add_argument("--run-commit")
    return parser


def build_report(
    *,
    surface_rows: list[dict[str, str]],
    pattern_rows: list[dict[str, str]],
    protocol_manifest: dict[str, Any],
    commit: str,
) -> str:
    surface = surface_counts(surface_rows)
    pattern = pattern_counts(pattern_rows)
    doxa_display = display_term("δοξα", english="glory")
    lines = [
        "# Greek Expanded Prospective Report",
        "",
        "Status: prospective screen complete; no claim.",
        "",
        "This report records the first run after",
        "`docs/GREEK_EXPANDED_PROSPECTIVE_PREREGISTRATION.md` and",
        "`terms/greek_expanded_prospective_terms.csv` were committed.",
        "",
        "## Run",
        "",
        "| Field | Value |",
        "| --- | --- |",
        "| Local report build commit | recorded in local manifest only |",
        "| Command | `python3 -m scripts.run_protocol protocols/greek_expanded_prospective_exact_center.toml --resume` |",
        "| Protocol | `protocols/greek_expanded_prospective_exact_center.toml` |",
        "| Started UTC | recorded in local manifest only |",
        "| Ended UTC | recorded in local manifest only |",
        "| Runtime | recorded in local manifest only |",
        f"| Status | {protocol_manifest.get('status', '')} |",
        "",
        "Volatile completion timestamps and runtimes are recorded in the local",
        "ignored manifests, not in tracked Markdown.",
        "",
        "For resumed protocol runs, this subreport can remain cached. The build",
        "commit is recorded in the local manifest; top-level",
        "assembly reports record their own current commit.",
        "",
        "## Locked Scope",
        "",
        "| Field | Value |",
        "| --- | --- |",
        "| Term file | `terms/greek_expanded_prospective_terms.csv` |",
        f"| Term rows | {term_count(surface_rows):,} |",
        "| Prior exact-center cohort terms | excluded by normalized Greek form |",
        "| Corpora | TR_NT, BYZ_NT, TCG_NT, SBLGNT |",
        "| Skip range | `2..50` |",
        "| Direction | both |",
        "| Minimum term length | 4 |",
        "| Extension phrase length | up to 4 words |",
        "| Top rows per corpus | 3000 |",
        "",
        "## Surface-Context Counts",
        "",
        "| Corpus | Raw hits | Context hits | Exact-center hits | Exact-span hits |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for corpus in sorted(surface):
        row = surface[corpus]
        lines.append(
            f"| {corpus} | {row['hit_count']:,} | {row['context_hit_count']:,} | "
            f"{row['exact_center_hits']:,} | {row['exact_span_hits']:,} |"
        )
    lines.extend(
        [
            "",
            "Top exact-center surface terms:",
            "",
            "| Corpus | Term | Concept | Exact-center hits |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for row in top_exact_center_rows(surface_rows, limit_per_corpus=5):
        lines.append(
            f"| {row['corpus']} | {display_report_term(row)} | {md_cell(row['concept'])} | "
            f"{int(row['exact_center_hits']):,} |"
        )
    lines.extend(
        [
            "",
            "## Phrase-Extension Pattern Matrix",
            "",
            "| Scope | Patterns |",
            "| --- | ---: |",
        ]
    )
    if pattern["scope_counts"]:
        for scope, count in sorted(pattern["scope_counts"].items()):
            lines.append(f"| `{scope}` | {count:,} |")
    else:
        lines.append("| none | 0 |")
    lines.extend(
        [
            "",
            f"Total exact-center phrase-extension patterns: {len(pattern_rows):,}.",
            "",
            "## Read",
            "",
            "The prospective expanded screen produced exact-center surface hits, but no",
            "same-skip phrase-extension rows survived the locked exact-center pattern",
            "presence filter. Under the preregistered routing rules, no row enters the",
            "control queue from this run.",
            "",
            "This is a useful negative result. It means the stricter phrase-extension",
            "gate is selective when applied to 291 new Greek terms, and the previous",
            f"{doxa_display} row was not trivially reproduced by a larger nearby term list.",
            "",
            "## Follow-Up Boundary",
            "",
            "No controls are needed for this phrase-extension screen because the locked",
            "pattern matrix produced zero rows. A separate exact-center surface prospective",
            "study was later run under its own preregistration and stayed negative under the",
            "registered length >= 5 primary rule.",
            "",
            "Do not promote raw exact-center surface hits from this run as claims. Any new",
            "result-producing surface study needs a fresh term/source target set and a clean",
            "prospective lock.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def surface_counts(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for row in rows:
        target = counts.setdefault(
            row["corpus"],
            {
                "hit_count": 0,
                "context_hit_count": 0,
                "exact_center_hits": 0,
                "exact_span_hits": 0,
            },
        )
        for key in target:
            target[key] += int(row[key])
    return counts


def pattern_counts(rows: list[dict[str, str]]) -> dict[str, Counter[str]]:
    return {"scope_counts": Counter(row["scope"] for row in rows)}


def top_exact_center_rows(
    rows: list[dict[str, str]],
    *,
    limit_per_corpus: int,
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    corpora = sorted({row["corpus"] for row in rows})
    for corpus in corpora:
        corpus_rows = [
            row
            for row in rows
            if row["corpus"] == corpus and int(row["exact_center_hits"]) > 0
        ]
        output.extend(
            sorted(
                corpus_rows,
                key=lambda row: (-int(row["exact_center_hits"]), row["term_id"]),
            )[:limit_per_corpus]
        )
    return output


def term_count(rows: list[dict[str, str]]) -> int:
    return len({row["term_id"] for row in rows})


def display_report_term(row: dict[str, str]) -> str:
    return md_cell(display_term(row["normalized_term"], english=row.get("concept", "")))


def md_cell(value: str) -> str:
    return value.replace("|", "\\|")


def write_manifest(
    path: Path,
    *,
    commit: str,
    surface_rows: int,
    pattern_rows: int,
    protocol_manifest: dict[str, Any],
    report_out: Path,
) -> None:
    payload = {
        "tool": "build_greek_expanded_prospective_report",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "commit": commit,
        "surface_rows": surface_rows,
        "pattern_rows": pattern_rows,
        "protocol_status": protocol_manifest.get("status", ""),
        "outputs": [str(report_out), str(path)],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
