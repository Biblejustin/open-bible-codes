#!/usr/bin/env python3
"""Build the tracked report for the four-source doxa claim follow-up."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.statistics import numeric_value
from els.term_display import display_term


OUT_DIR = Path("reports/doxa_four_source_claim_followup")
PAIRED_SUMMARY = OUT_DIR / "paired_controls_summary.csv"
CONTEXT_SUMMARY = OUT_DIR / "context_review_summary.csv"
PROTOCOL_MANIFEST = OUT_DIR / "protocol_run.manifest.json"
REPORT_OUT = Path("docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md")
MANIFEST_OUT = OUT_DIR / "report.manifest.json"
TARGET_KEY = "δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ"
BASE_TERM = "δοξα"
EXTENDED_SEQUENCE = "δοξανωσ"
MATCHED_PHRASE = "δόξαν ὡς"
CENTER_SURFACE = "δοξάζηται"
MATCHED_PHRASE_DISPLAY = display_term(MATCHED_PHRASE, english="glory as", transliteration="doxan hos")
EXPECTED_CORPORA = ("BYZ_NT", "SBLGNT", "TCG_NT", "TR_NT")
DEFAULT_TERM_CONTROL_SAMPLES = 5000
DEFAULT_RANDOM_CONTROL_SAMPLES = 5000
DEFAULT_REPORT_TITLE = "Doxa Four-Source Claim Follow-Up Report"
DEFAULT_PREREGISTRATION_DOC = "docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_PREREGISTRATION.md"
DEFAULT_PROTOCOL_PATH = "protocols/doxa_four_source_claim_followup.toml"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paired_rows = read_rows(args.paired_summary)
    context_rows = read_rows(args.context_summary)
    protocol_manifest = read_json(args.protocol_manifest)
    run_commit = args.run_commit or git_commit()
    prereg_commit = args.preregistration_commit or run_commit
    report = build_report(
        paired_rows=paired_rows,
        context_rows=context_rows,
        protocol_manifest=protocol_manifest,
        run_commit=run_commit,
        prereg_commit=prereg_commit,
        report_title=args.report_title,
        preregistration_doc=args.preregistration_doc,
        protocol_path=args.protocol_path,
        term_control_samples=args.term_control_samples,
        random_control_samples=args.random_control_samples,
        report_out=args.report_out,
    )
    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    args.report_out.write_text(report, encoding="utf-8")
    write_manifest(
        args.manifest_out,
        run_commit=run_commit,
        prereg_commit=prereg_commit,
        paired_rows=paired_rows,
        context_rows=context_rows,
        protocol_manifest=protocol_manifest,
        report_out=args.report_out,
    )
    print(args.report_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paired-summary", type=Path, default=PAIRED_SUMMARY)
    parser.add_argument("--context-summary", type=Path, default=CONTEXT_SUMMARY)
    parser.add_argument("--protocol-manifest", type=Path, default=PROTOCOL_MANIFEST)
    parser.add_argument("--report-out", type=Path, default=REPORT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    parser.add_argument("--run-commit")
    parser.add_argument("--preregistration-commit")
    parser.add_argument("--report-title", default=DEFAULT_REPORT_TITLE)
    parser.add_argument("--preregistration-doc", default=DEFAULT_PREREGISTRATION_DOC)
    parser.add_argument("--protocol-path", default=DEFAULT_PROTOCOL_PATH)
    parser.add_argument("--term-control-samples", type=int, default=DEFAULT_TERM_CONTROL_SAMPLES)
    parser.add_argument("--random-control-samples", type=int, default=DEFAULT_RANDOM_CONTROL_SAMPLES)
    return parser


def build_report(
    *,
    paired_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
    protocol_manifest: dict[str, Any],
    run_commit: str,
    prereg_commit: str,
    report_title: str = DEFAULT_REPORT_TITLE,
    preregistration_doc: str = DEFAULT_PREREGISTRATION_DOC,
    protocol_path: str = DEFAULT_PROTOCOL_PATH,
    term_control_samples: int = DEFAULT_TERM_CONTROL_SAMPLES,
    random_control_samples: int = DEFAULT_RANDOM_CONTROL_SAMPLES,
    report_out: Path = REPORT_OUT,
) -> str:
    rows = sorted(paired_rows, key=lambda row: row["corpus"])
    contexts_by_corpus = {row["corpus"]: row for row in context_rows}
    output_dir = default_output_dir_for_report(report_out)
    criteria = criteria_results(rows, context_rows, str(output_dir / "letter_paths.md"))
    status = followup_status(criteria)
    lines = [
        f"# {report_title}",
        "",
        f"Status: {status}, not a claim.",
        "",
        f"This report records the locked {term_control_samples}/{random_control_samples}",
        "follow-up after",
        f"`{preregistration_doc}` was added.",
        "",
        "## Run",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Preregistration commit | `{prereg_commit}` |",
        "| Local report build commit | recorded in local manifest only |",
        f"| Command | `python3 -m scripts.run_protocol {protocol_path} --resume` |",
        f"| Protocol | `{protocol_path}` |",
        "| Paired controls completed UTC | recorded in local manifests only |",
        "| Context review completed UTC | recorded in local manifests only |",
        "| Analysis runtime | recorded in local manifests only |",
        f"| Protocol status | {protocol_manifest.get('status', '')} |",
        "| Paired-control runtime | recorded in local manifests only |",
        "| Context-review runtime | recorded in local manifests only |",
        "",
        "Volatile completion timestamps and runtimes are recorded in the local",
        "ignored manifests, not in tracked Markdown. The build commit is recorded",
        "in the local manifest; the top-level",
        "`reports/real_report_run/summary.md` records the current assembly commit.",
        "",
        "Generated local outputs:",
        "",
        f"- `{output_dir / 'paired_controls_summary.csv'}`",
        f"- `{output_dir / 'paired_controls_examples.csv'}`",
        f"- `{output_dir / 'paired_controls.md'}`",
        f"- `{output_dir / 'context_review_summary.csv'}`",
        f"- `{output_dir / 'context_review.md'}`",
        f"- `{output_dir / 'letter_paths.md'}`",
        f"- `{output_dir / 'protocol_run.manifest.json'}`",
        "",
        "## Registered Candidate",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Base term | {display_term(BASE_TERM, english='glory')} |",
        f"| Extension key | {display_extension_key()} |",
        "| Skip | `21` |",
        "| Direction | `forward` |",
        "| Extension type | `term_plus_after` |",
        f"| Extended normalized sequence | {display_term(EXTENDED_SEQUENCE)} |",
        f"| Matched phrase | {MATCHED_PHRASE_DISPLAY} |",
        "| Center passage | 2 Thessalonians 3:1 |",
        "| Matched phrase reference | John 1:14 / JHN 1:14 |",
        "",
        "No alternate spelling, skip, direction, extension length, or nearby row was used.",
        "",
        "## Controls",
        "",
        "Fixed control settings:",
        "",
        f"- {term_control_samples} shuffled-term controls per row",
        f"- {random_control_samples} same-length random controls per row",
        "- same corpus",
        "- same skip",
        "- same direction",
        "- same extension settings",
        "- target list deduped",
        "",
        "P-value floor:",
        "",
        f"- shuffled-term controls: `1 / {term_control_samples + 1} = {empirical_floor(term_control_samples)}`",
        f"- same-length random controls: `1 / {random_control_samples + 1} = {empirical_floor(random_control_samples)}`",
        "",
        "## Results",
        "",
        "| Corpus | Center | Matched ref | Score | Term-any p | Random-any p | Combined p | Combined q | All-control q | Flags |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        context = contexts_by_corpus.get(row["corpus"], {})
        lines.append(
            "| "
            + " | ".join(
                [
                    row["corpus"],
                    context.get("center_ref", ""),
                    row.get("matched_refs", ""),
                    row.get("observed_score", ""),
                    row.get("term_any_p_ge", ""),
                    row.get("random_any_p_ge", ""),
                    row.get("combined_min_p", ""),
                    row.get("combined_min_q", ""),
                    row.get("all_controls_max_q", ""),
                    f"`{row.get('flags', '')}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Context And Audit",
            "",
            "The base term has exact-center surface context through the surface form",
            f"{display_term(CENTER_SURFACE, english='may be glorified')} in 2 Thessalonians 3:1.",
            "",
            f"The full hidden extension sequence {display_term(EXTENDED_SEQUENCE)} maps to the phrase",
            f"{MATCHED_PHRASE_DISPLAY}. This follow-up treats hidden-path-only material as meaningful",
            "review material, not as a failure. A same-span surface echo would be a",
            "stronger subtype, but it is not required by this registered study.",
            "",
            "Context reads:",
            "",
            "| Corpus | Center | Hit refs | Context read |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in sorted(context_rows, key=lambda row: row["corpus"]):
        lines.append(
            "| "
            + " | ".join(
                [
                    row["corpus"],
                    f"{row['center_ref']} {display_term(row['center_word'])}",
                    row["hit_refs"],
                    row["context_read"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Audit paths are saved in:",
            "",
            f"- `{output_dir / 'letter_paths.md'}`",
            "",
            "## Preregistration Check",
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
            "This is a post-discovery follow-up. It is not an original prospective",
            "discovery.",
            "",
            f"Current status: `{status}`.",
            "",
            "This does not support:",
            "",
            "- `confirmed_code`",
            "- `proof`",
            "- `prophecy`",
            "- `statistical discovery`",
            "",
            "The result remains limited even if the registered criteria pass. The base",
            "term is short, the row was selected after discovery, and ELS phrase",
            "extensions can produce convincing-looking hidden strings from controls.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def default_output_dir_for_report(report_out: Path) -> Path:
    if report_out == REPORT_OUT:
        return OUT_DIR
    if report_out.parent.name == "docs":
        return Path("reports") / report_out.stem.lower().replace("_report", "")
    return report_out.parent


def display_extension_key() -> str:
    return (
        f"base={display_term(BASE_TERM, english='glory')}; skip=21; direction=forward; "
        f"type=term_plus_after; extended={display_term(EXTENDED_SEQUENCE)}"
    )


def empirical_floor(samples: int) -> str:
    return f"{1 / (samples + 1):.8g}"


def criteria_results(
    paired_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
    letter_paths_path: str = "reports/doxa_four_source_claim_followup/letter_paths.md",
) -> list[tuple[str, str, str]]:
    corpora = tuple(sorted(row["corpus"] for row in paired_rows))
    context_corpora = tuple(sorted(row["corpus"] for row in context_rows))
    all_q_pass = all(q_passes(row.get("combined_min_q", "")) for row in paired_rows)
    all_center_exact = all(row.get("center_exact") == "True" for row in context_rows)
    return [
        (
            "Exact extension key remains present in all four sources",
            pass_fail(corpora == EXPECTED_CORPORA),
            ", ".join(corpora) if corpora else "none",
        ),
        (
            "All four rows retain exact-center base-term surface context",
            pass_fail(context_corpora == EXPECTED_CORPORA and all_center_exact),
            ", ".join(context_corpora) if context_corpora else "none",
        ),
        (
            "`combined_min_q <= 0.01` in all four rows",
            pass_fail(bool(paired_rows) and all_q_pass),
            q_range_read(paired_rows),
        ),
        (
            "Saved examples and letter paths generated",
            pass_fail(context_corpora == EXPECTED_CORPORA),
            f"`{letter_paths_path}`",
        ),
        (
            "Full phrase location reported",
            "pass",
            "hidden-path-only unless a context row says otherwise",
        ),
        (
            "Warning flags reported",
            pass_fail(all(row.get("flags") for row in paired_rows)),
            "; ".join(sorted({row.get("flags", "") for row in paired_rows if row.get("flags")})),
        ),
        (
            "Post-discovery status stated",
            "pass",
            "reported as follow-up, not prospective discovery",
        ),
    ]


def followup_status(criteria: list[tuple[str, str, str]]) -> str:
    if all(result == "pass" for _, result, _ in criteria):
        return "claim_followup_review_candidate"
    return "review_hold"


def q_passes(value: str) -> bool:
    q_value = numeric_value(value)
    return q_value is not None and q_value <= 0.01


def q_range_read(rows: list[dict[str, str]]) -> str:
    values = [
        numeric_value(row.get("combined_min_q", ""))
        for row in rows
        if numeric_value(row.get("combined_min_q", "")) is not None
    ]
    if not values:
        return "no q values"
    return f"min {min(values):.6g}; max {max(values):.6g}"


def pass_fail(condition: bool) -> str:
    return "pass" if condition else "fail"


def write_manifest(
    path: Path,
    *,
    run_commit: str,
    prereg_commit: str,
    paired_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
    protocol_manifest: dict[str, Any],
    report_out: Path,
) -> None:
    payload = {
        "tool": "build_doxa_four_source_claim_followup_report",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "run_commit": run_commit,
        "preregistration_commit": prereg_commit,
        "target_key": TARGET_KEY,
        "paired_rows": len(paired_rows),
        "context_rows": len(context_rows),
        "protocol_status": protocol_manifest.get("status", ""),
        "outputs": [str(report_out), str(path)],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
