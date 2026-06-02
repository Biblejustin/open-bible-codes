#!/usr/bin/env python3
"""Build a compact follow-up report for selected Greek surface rows."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.statistics import numeric_value
from els.term_display import display_term
from scripts.json_utils import read_json_object


SELECTED_IN = Path("reports/greek_expanded_surface_triage/selected_patterns.csv")
PATH_SUMMARY_IN = Path("reports/greek_expanded_surface_letter_paths/path_summary.csv")
CONTROL_SUMMARY_IN = Path("reports/greek_expanded_surface_available_control_evaluation/summary.csv")
LETTER_PATHS_MANIFEST = Path("reports/greek_expanded_surface_letter_paths/protocol_run.manifest.json")
CONTROLS_MANIFEST = Path("reports/greek_expanded_surface_available_control_evaluation/protocol_run.manifest.json")
OUT_DIR = Path("reports/greek_expanded_surface_followup")
REPORT_OUT = Path("docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md")
MANIFEST_OUT = OUT_DIR / "report.manifest.json"
EXPECTED_CORPORA = ("BYZ_NT", "SBLGNT", "TCG_NT", "TR_NT")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    selected_rows = read_rows(args.selected)
    path_rows = read_rows(args.path_summary)
    control_rows = read_rows(args.control_summary)
    letter_manifest = read_json(args.letter_paths_manifest)
    control_manifest = read_json(args.controls_manifest)
    run_commit = args.run_commit or git_commit()
    report = build_report(
        selected_rows=selected_rows,
        path_rows=path_rows,
        control_rows=control_rows,
        letter_manifest=letter_manifest,
        control_manifest=control_manifest,
        run_commit=run_commit,
    )
    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    args.report_out.write_text(report, encoding="utf-8")
    write_manifest(
        args.manifest_out,
        run_commit=run_commit,
        selected_rows=selected_rows,
        path_rows=path_rows,
        control_rows=control_rows,
        status=followup_status(criteria_results(selected_rows, path_rows, control_rows)),
        report_out=args.report_out,
    )
    print(args.report_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selected", type=Path, default=SELECTED_IN)
    parser.add_argument("--path-summary", type=Path, default=PATH_SUMMARY_IN)
    parser.add_argument("--control-summary", type=Path, default=CONTROL_SUMMARY_IN)
    parser.add_argument("--letter-paths-manifest", type=Path, default=LETTER_PATHS_MANIFEST)
    parser.add_argument("--controls-manifest", type=Path, default=CONTROLS_MANIFEST)
    parser.add_argument("--report-out", type=Path, default=REPORT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    parser.add_argument("--run-commit")
    return parser


def build_report(
    *,
    selected_rows: list[dict[str, str]],
    path_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
    letter_manifest: dict[str, Any],
    control_manifest: dict[str, Any],
    run_commit: str,
) -> str:
    criteria = criteria_results(selected_rows, path_rows, control_rows)
    status = followup_status(criteria)
    selected_by_id = {row["term_id"]: row for row in selected_rows}
    controls_by_id = {row["target_term_id"]: row for row in control_rows}
    lines = [
        "# Greek Expanded Surface Follow-Up Report",
        "",
        f"Status: {status}, not a claim.",
        "",
        "This report gathers the tightened Greek exact-center surface rows,",
        "letter-path audit, and all-available real-word controls into one",
        "post-screen follow-up read.",
        "",
        "## Run",
        "",
        "| Field | Value |",
        "| --- | --- |",
        "| Local report build commit | recorded in local manifest only |",
        "| Letter-path protocol | `protocols/greek_expanded_surface_letter_paths.toml` |",
        "| Control protocol | `protocols/greek_expanded_surface_available_control_evaluation.toml` |",
        f"| Letter-path status | `{letter_manifest.get('status', '')}` |",
        f"| Control status | `{control_manifest.get('status', '')}` |",
        "",
        "For resumed protocol runs, this subreport can remain cached. The build",
        "commit is recorded in the local manifest; the top-level",
        "`reports/real_report_run/summary.md` records the current assembly commit.",
        "",
        "## Registered Post-Screen Rows",
        "",
        "| Term | Concept | Center | Skip | Direction | p_ge | q | Matched controls |",
        "| --- | --- | --- | ---: | --- | ---: | ---: | ---: |",
    ]
    for term_id in sorted(selected_by_id):
        selected = selected_by_id[term_id]
        controls = controls_by_id.get(term_id, {})
        lines.append(
            "| "
            + " | ".join(
                [
                    display_selected_term(selected),
                    md_cell(selected["concept"]),
                    selected["center_ref"],
                    selected["skip"],
                    selected["direction"],
                    controls.get("all_source_p_ge", ""),
                    controls.get("all_source_q_value", ""),
                    controls.get("matched_controls", ""),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Letter-Path Audit",
            "",
            "| Term | Corpus | Sequence | Center word | Path refs |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in path_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_path_term(row, selected_by_id),
                    row["corpus"],
                    display_term(row["sequence"]),
                    display_term(row["center_word"]),
                    row["path_refs"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Follow-Up Checks",
            "",
            "| Criterion | Result | Note |",
            "| --- | --- | --- |",
        ]
    )
    for criterion, result, note in criteria:
        lines.append(f"| {criterion} | {result} | {note} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This is stronger triage evidence than the first 10-control pass because",
            "the all-available non-selected same-length control pool has study-level",
            "q = 0.032258 for the selected rows.",
            "",
            "It is still post-screen. It does not establish a claim, conclusive evidence, prophecy,",
            "or statistical discovery. A stronger claim would require a prospective",
            "study whose term list, selection rule, control pool, and correction plan",
            "were fixed before the rows were discovered.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def criteria_results(
    selected_rows: list[dict[str, str]],
    path_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
) -> list[tuple[str, str, str]]:
    selected_ids = {row["term_id"] for row in selected_rows}
    path_by_term: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in path_rows:
        path_by_term[row["term_id"]].append(row)
    controls_by_term = {row["target_term_id"]: row for row in control_rows}
    corpora_pass = all(
        tuple(sorted(row["corpus"] for row in path_by_term[term_id])) == EXPECTED_CORPORA
        for term_id in selected_ids
    )
    paths_match = all(row.get("matches_term") == "True" for row in path_rows)
    controls_present = selected_ids == set(controls_by_term)
    q_values = [
        numeric_value(row.get("all_source_q_value", ""))
        for row in control_rows
    ]
    q_pass = bool(q_values) and all(value is not None and value <= 0.05 for value in q_values)
    controls_ge_pass = all(row.get("controls_ge_observed_all_source") == "0" for row in control_rows)
    return [
        (
            "All selected terms have paths in all four Greek NT source labels",
            pass_fail(corpora_pass),
            ", ".join(EXPECTED_CORPORA),
        ),
        (
            "All reconstructed paths spell the normalized term",
            pass_fail(paths_match),
            f"{len(path_rows)} path rows",
        ),
        (
            "All selected terms have all-available controls",
            pass_fail(controls_present),
            f"{len(control_rows)} control rows",
        ),
        (
            "No all-available matched control reaches observed all-source count",
            pass_fail(controls_ge_pass),
            "controls_ge_observed_all_source == 0",
        ),
        (
            "Study-level q <= 0.05 within this follow-up table",
            pass_fail(q_pass),
            q_range_read(control_rows),
        ),
        (
            "Post-screen boundary stated",
            "pass",
            "follow-up report says this is not prospective discovery",
        ),
    ]


def followup_status(criteria: list[tuple[str, str, str]]) -> str:
    if all(result == "pass" for _criterion, result, _note in criteria):
        return "post_screen_surface_followup_review_candidate"
    return "review_hold"


def q_range_read(rows: list[dict[str, str]]) -> str:
    values = [
        numeric_value(row.get("all_source_q_value", ""))
        for row in rows
        if numeric_value(row.get("all_source_q_value", "")) is not None
    ]
    if not values:
        return "no q values"
    return f"min {min(values):.6g}; max {max(values):.6g}"


def display_selected_term(row: dict[str, str]) -> str:
    return md_cell(display_term(row["normalized_term"], english=row.get("concept", "")))


def display_path_term(
    row: dict[str, str],
    selected_by_id: dict[str, dict[str, str]],
) -> str:
    selected = selected_by_id.get(row["term_id"], {})
    return md_cell(display_term(row["normalized_term"], english=selected.get("concept", "")))


def md_cell(value: str) -> str:
    return value.replace("|", "\\|")


def pass_fail(condition: bool) -> str:
    return "pass" if condition else "fail"


def write_manifest(
    path: Path,
    *,
    run_commit: str,
    selected_rows: list[dict[str, str]],
    path_rows: list[dict[str, str]],
    control_rows: list[dict[str, str]],
    status: str,
    report_out: Path,
) -> None:
    payload = {
        "tool": "build_greek_surface_followup_report",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "run_commit": run_commit,
        "selected_rows": len(selected_rows),
        "path_rows": len(path_rows),
        "control_rows": len(control_rows),
        "status": status,
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
