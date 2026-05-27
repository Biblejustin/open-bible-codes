#!/usr/bin/env python3
"""Build a compact deep-dive packet for strongest current candidates."""

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


DEFAULT_CLAIM_CATALOG = Path("claims/claim_catalog.csv")
DEFAULT_DOXA_PAIRED = Path("reports/doxa_four_source_confirmatory_followup/paired_controls_summary.csv")
DEFAULT_DOXA_CONTEXT = Path("reports/doxa_four_source_confirmatory_followup/context_review_summary.csv")
DEFAULT_COMPOUND_SUMMARY = Path("reports/all_codes_compound_extension_confirmatory/summary.csv")
DEFAULT_GOG_OCCURRENCES = Path("reports/centered_occurrence_index/centered_occurrences.csv")
DEFAULT_GREEK_EXPANDED_CONTROLS = Path("reports/greek_expanded_surface_available_control_evaluation/summary.csv")
DEFAULT_GREEK_EXPANDED_SELECTED = Path("reports/greek_expanded_surface_triage/selected_patterns.csv")
DEFAULT_KJVA_CONFIRMATORY = Path("reports/kjv_apocrypha_bridge_confirmatory_controls_5000/term_summary.csv")
DEFAULT_KJVA_PROSPECTIVE = Path("reports/kjv_apocrypha_bridge_prospective/term_summary.csv")
DEFAULT_KJVA_PROSPECTIVE_BRIDGE = Path("reports/kjv_apocrypha_bridge_prospective/bridge_summary.csv")

DEFAULT_OUT = Path("reports/strongest_candidate_deep_dive/candidates.csv")
DEFAULT_MARKDOWN = Path("docs/STRONGEST_CANDIDATE_DEEP_DIVE.md")
DEFAULT_MANIFEST = Path("reports/strongest_candidate_deep_dive/manifest.json")

FIELDNAMES = [
    "rank",
    "candidate_id",
    "label",
    "language",
    "status",
    "decision",
    "evidence_read",
    "control_read",
    "context_read",
    "limit_read",
    "next_action",
    "primary_artifact",
    "supporting_artifacts",
]

CANDIDATE_IDS = [
    "doxa_exact_center_extension",
    "all_codes_yom_yhwh_compound_extension",
    "gog_rev_20_8_centered_occurrence",
    "greek_expanded_surface_followup",
    "kjva_apocrypha_bridge_boundary",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    candidates = build_candidates(args)
    write_csv(args.out, candidates)
    write_markdown(args.markdown_out, candidates, args)
    write_manifest(args.manifest_out, candidates, args, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-catalog", type=Path, default=DEFAULT_CLAIM_CATALOG)
    parser.add_argument("--doxa-paired", type=Path, default=DEFAULT_DOXA_PAIRED)
    parser.add_argument("--doxa-context", type=Path, default=DEFAULT_DOXA_CONTEXT)
    parser.add_argument("--compound-summary", type=Path, default=DEFAULT_COMPOUND_SUMMARY)
    parser.add_argument("--gog-occurrences", type=Path, default=DEFAULT_GOG_OCCURRENCES)
    parser.add_argument("--greek-expanded-controls", type=Path, default=DEFAULT_GREEK_EXPANDED_CONTROLS)
    parser.add_argument("--greek-expanded-selected", type=Path, default=DEFAULT_GREEK_EXPANDED_SELECTED)
    parser.add_argument("--kjva-confirmatory", type=Path, default=DEFAULT_KJVA_CONFIRMATORY)
    parser.add_argument("--kjva-prospective", type=Path, default=DEFAULT_KJVA_PROSPECTIVE)
    parser.add_argument("--kjva-prospective-bridge", type=Path, default=DEFAULT_KJVA_PROSPECTIVE_BRIDGE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_candidates(args: argparse.Namespace) -> list[dict[str, str]]:
    claims = {row.get("claim_id", ""): row for row in read_rows(args.claim_catalog)}
    rows = [
        build_doxa_row(claims, args),
        build_compound_row(claims, args),
        build_gog_row(claims, args),
        build_greek_expanded_row(claims, args),
        build_kjva_row(claims, args),
    ]
    for rank, row in enumerate(rows, start=1):
        row["rank"] = str(rank)
    return rows


def base_row(
    claims: dict[str, dict[str, str]],
    claim_id: str,
    *,
    label: str,
    language: str,
    decision: str,
    next_action: str,
    primary_artifact: str,
    supporting_artifacts: list[str],
) -> dict[str, str]:
    claim = claims.get(claim_id, {})
    return {
        "rank": "",
        "candidate_id": claim_id,
        "label": label,
        "language": language,
        "status": claim.get("status", ""),
        "decision": decision,
        "evidence_read": claim.get("current_reproduction", ""),
        "control_read": "",
        "context_read": "",
        "limit_read": claim.get("notes", ""),
        "next_action": next_action,
        "primary_artifact": primary_artifact,
        "supporting_artifacts": "; ".join(supporting_artifacts),
    }


def build_doxa_row(claims: dict[str, dict[str, str]], args: argparse.Namespace) -> dict[str, str]:
    paired = read_rows(args.doxa_paired)
    context = read_rows(args.doxa_context)
    corpora = sorted({row.get("corpus", "") for row in paired if row.get("corpus", "")})
    combined_q = max_float(row.get("combined_min_q", "") for row in paired)
    all_control_q = max_float(row.get("all_controls_max_q", "") for row in paired)
    samples = max_int(row.get("term_control_samples", "") for row in paired)
    random_samples = max_int(row.get("random_control_samples", "") for row in paired)
    first_context = context[0] if context else {}
    row = base_row(
        claims,
        "doxa_exact_center_extension",
        label="Greek doxa four-source exact-center extension",
        language="greek",
        decision="hold_after_clean_lock_extension_followup",
        next_action=(
            "Keep as post-discovery review material. Any new Greek extension work should start from a genuinely "
            "new clean term source with stricter function-word and context gates before search."
        ),
        primary_artifact="docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md",
        supporting_artifacts=[
            str(args.doxa_paired),
            str(args.doxa_context),
            "reports/doxa_four_source_confirmatory_followup/report.manifest.json",
        ],
    )
    row["control_read"] = (
        f"{len(corpora)} sources; {samples} term controls and {random_samples} random controls per source; "
        f"max combined q {fmt_float(combined_q)}; max all-control q {fmt_float(all_control_q)}."
    )
    row["context_read"] = (
        f"Exact-center context at {first_context.get('center_ref', '')} around "
        f"{first_context.get('center_word', '')}; base surface appears in center verse; "
        "full extension phrase is hidden-path-only."
    )
    return row


def build_compound_row(claims: dict[str, dict[str, str]], args: argparse.Namespace) -> dict[str, str]:
    summary = read_rows(args.compound_summary)
    corpora = sorted({row.get("corpus", "") for row in summary if row.get("corpus", "")})
    combined_q = max_float(row.get("combined_min_q", "") for row in summary)
    all_control_q = max_float(row.get("all_controls_max_q", "") for row in summary)
    term_samples = max_int(row.get("term_control_samples", "") for row in summary)
    random_samples = max_int(row.get("random_control_samples", "") for row in summary)
    first = summary[0] if summary else {}
    row = base_row(
        claims,
        "all_codes_yom_yhwh_compound_extension",
        label="Hebrew Day of YHWH compound extension",
        language="hebrew",
        decision="advance_after_doxa_or_pair_with_hebrew_lock",
        next_action=(
            "Lock a Hebrew compound-extension prospective cohort with the same source-family rule before adding "
            "or ranking new Hebrew extension rows."
        ),
        primary_artifact="docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md",
        supporting_artifacts=[
            str(args.compound_summary),
            "reports/all_codes_compound_extension_confirmatory/manifest.json",
            "reports/all_codes_compound_extension_confirmatory/examples.csv",
        ],
    )
    row["control_read"] = (
        f"{len(corpora)} MT-family sources; {term_samples} term controls and {random_samples} random controls per source; "
        f"max combined q {fmt_float(combined_q)}; max all-control q {fmt_float(all_control_q)}."
    )
    row["context_read"] = (
        f"Same overlap key across {first.get('overlap_corpora', '')}; skip {first.get('skip', '')} "
        f"{first.get('direction', '')}; extension {first.get('extended_sequence', '')}; "
        f"matched refs {first.get('matched_refs', '')}."
    )
    return row


def build_gog_row(claims: dict[str, dict[str, str]], args: argparse.Namespace) -> dict[str, str]:
    occurrences = [
        row
        for row in read_rows(args.gog_occurrences)
        if row.get("source_family") == "gog_source_review"
        and row.get("normalized_term") == "γωγ"
        and row.get("occurrence_type") == "centered_self_exact_word"
    ]
    corpora = sorted({row.get("corpus", "") for row in occurrences if row.get("corpus", "")})
    paths = sum(int_or_zero(row.get("exact_center_paths", "")) for row in occurrences)
    first = occurrences[0] if occurrences else {}
    row = base_row(
        claims,
        "gog_rev_20_8_centered_occurrence",
        label="Greek Gog centered on open Gog at Rev 20:8",
        language="greek",
        decision="hold_as_context_occurrence_not_claim",
        next_action=(
            "Keep in final occurrence list; any stronger promotion needs a longer Gog/Magog paired metric with "
            "declared controls."
        ),
        primary_artifact="docs/CENTERED_OCCURRENCE_INDEX.md",
        supporting_artifacts=[
            str(args.gog_occurrences),
            "reports/centered_occurrence_index/presence_summary.csv",
            "reports/centered_occurrence_index/manifest.json",
        ],
    )
    row["control_read"] = first.get("frequency_read", "")
    row["context_read"] = (
        f"{len(corpora)} Greek NT sources; {paths} exact-center paths; center {first.get('center_ref', '')} "
        f"{first.get('center_word', '')}; context {first.get('context_excerpt', '')}."
    )
    return row


def build_greek_expanded_row(claims: dict[str, dict[str, str]], args: argparse.Namespace) -> dict[str, str]:
    controls = read_rows(args.greek_expanded_controls)
    selected = read_rows(args.greek_expanded_selected)
    max_q = max_float(row.get("all_source_q_value", "") for row in controls)
    target_terms = len({row.get("target_normalized_term", "") for row in controls if row.get("target_normalized_term", "")})
    max_observed = max_int(row.get("observed_all_source_patterns", "") for row in controls)
    corpora = sorted(
        {
            part
            for row in selected
            for part in row.get("present_corpora", "").split(",")
            if part
        }
    )
    row = base_row(
        claims,
        "greek_expanded_surface_followup",
        label="Greek expanded exact-center surface follow-up",
        language="greek",
        decision="secondary_candidate_needs_prospective_surface_lock",
        next_action=(
            "Fold into next Greek prospective design only if terms, surface rule, and same-length control pool are "
            "frozen before observing candidates."
        ),
        primary_artifact="docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md",
        supporting_artifacts=[
            str(args.greek_expanded_controls),
            str(args.greek_expanded_selected),
            "reports/greek_expanded_surface_followup/report.manifest.json",
        ],
    )
    row["control_read"] = (
        f"{target_terms} selected terms; max observed all-source patterns {max_observed}; "
        f"max all-source q {fmt_float(max_q)} under all-available real-word controls."
    )
    row["context_read"] = (
        f"Selected terms appear across {', '.join(corpora)}; selected rows include Isaac, Wonder, and Lawlessness."
    )
    return row


def build_kjva_row(claims: dict[str, dict[str, str]], args: argparse.Namespace) -> dict[str, str]:
    confirmatory = read_rows(args.kjva_confirmatory)
    prospective = read_rows(args.kjva_prospective)
    bridge_summary = {row.get("metric", ""): row.get("value", "") for row in read_rows(args.kjva_prospective_bridge)}
    confirm_q_le_001 = sum(1 for row in confirmatory if float_or_none(row.get("q_ge", "")) is not None and float(row["q_ge"]) <= 0.01)
    confirm_gt_sample_max = sum(1 for row in confirmatory if row.get("observed_gt_sample_max", "").lower() == "true")
    prospective_q_le_005 = sum(1 for row in prospective if float_or_none(row.get("q_ge", "")) is not None and float(row["q_ge"]) <= 0.05)
    prospective_rows = int_or_zero(bridge_summary.get("bridge_rows", ""))
    row = base_row(
        claims,
        "kjva_apocrypha_bridge_boundary",
        label="KJVA Apocrypha bridge boundary",
        language="english",
        decision="do_not_promote_without_new_prospective_success",
        next_action=(
            "Treat as methods case study; do not promote unless a new prospective term lock produces independent "
            "control support."
        ),
        primary_artifact="docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md",
        supporting_artifacts=[
            str(args.kjva_confirmatory),
            str(args.kjva_prospective),
            str(args.kjva_prospective_bridge),
            "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md",
        ],
    )
    row["control_read"] = (
        f"Post-screen confirmatory: {confirm_q_le_001}/{len(confirmatory)} terms at q <= 0.01, "
        f"{confirm_gt_sample_max} above every shuffled sample. Prospective lock: {prospective_rows} bridge row, "
        f"{prospective_q_le_005}/{len(prospective)} terms at q <= 0.05."
    )
    row["context_read"] = (
        "Boundary mechanics reproduce, but current independent prospective bridge read is weak/negative."
    )
    return row


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(rows, args), encoding="utf-8")


def render_markdown(rows: list[dict[str, str]], args: argparse.Namespace) -> str:
    lines = [
        "# Strongest Candidate Review Packet",
        "",
        "Status: review packet over the strongest current rows. This page does not make any row a public claim.",
        "",
        "## Plain Read",
        "",
        f"- candidate rows: {len(rows)}",
        "- strongest current item: Greek doxa/glory extension",
        "- strongest Hebrew item: day of YHWH compound extension",
        "- clearest occurrence item: Greek Gog centered on open Gog in Revelation 20:8",
        "- strongest English/apocrypha item: KJV with Apocrypha bridge rows",
        "- main caution: these are review candidates, not settled findings",
        "",
        "Read this page as a shortlist for careful review. It shows what looks most worth studying next, and why each row still needs caution.",
        "",
        "## Ranked Candidates",
        "",
        "| Rank | Candidate | Decision | Control read | Limit | Next action |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["rank"],
                    f"`{escape_md(row['candidate_id'])}`",
                    f"`{escape_md(row['decision'])}`",
                    escape_md(row["control_read"]),
                    escape_md(row["limit_read"]),
                    escape_md(row["next_action"]),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Detail Rows", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['rank']}. {row['label']}",
                "",
                f"- Candidate ID: `{row['candidate_id']}`",
                f"- Status: `{row['status']}`",
                f"- Language: `{row['language']}`",
                f"- Evidence read: {row['evidence_read']}",
                f"- Control read: {row['control_read']}",
                f"- Context read: {row['context_read']}",
                f"- Limit: {row['limit_read']}",
                f"- Next action: {row['next_action']}",
                f"- Primary artifact: `{row['primary_artifact']}`",
                f"- Supporting artifacts: `{row['supporting_artifacts']}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Cautions",
            "",
            "- Strongest here means strongest current review candidate inside this repo, not evidence of design.",
            "- Post-discovery control support is useful for triage, but prospective locks carry more evidential weight.",
            "- Short terms, hidden-path-only extensions, translation-boundary effects, and source-family dependence remain separate risks.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_manifest(path: Path, rows: list[dict[str, str]], args: argparse.Namespace, started: float) -> None:
    payload = {
        "tool": "build_strongest_candidate_deep_dive",
        "version": __version__,
        "generated_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "commit": git_commit(),
        "inputs": {
            "claim_catalog": str(args.claim_catalog),
            "doxa_paired": str(args.doxa_paired),
            "doxa_context": str(args.doxa_context),
            "compound_summary": str(args.compound_summary),
            "gog_occurrences": str(args.gog_occurrences),
            "greek_expanded_controls": str(args.greek_expanded_controls),
            "greek_expanded_selected": str(args.greek_expanded_selected),
            "kjva_confirmatory": str(args.kjva_confirmatory),
            "kjva_prospective": str(args.kjva_prospective),
            "kjva_prospective_bridge": str(args.kjva_prospective_bridge),
        },
        "outputs": {
            "candidates": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "candidate_rows": len(rows),
        "candidate_ids": [row["candidate_id"] for row in rows],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def int_or_zero(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def max_int(values: Any) -> int:
    numbers = [int_or_zero(value) for value in values]
    return max(numbers) if numbers else 0


def float_or_none(value: object) -> float | None:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def max_float(values: Any) -> float:
    numbers = [value for value in (float_or_none(value) for value in values) if value is not None]
    return max(numbers) if numbers else 0.0


def fmt_float(value: float) -> str:
    return f"{value:.6g}"


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
