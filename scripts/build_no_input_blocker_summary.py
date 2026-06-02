#!/usr/bin/env python3
"""Build a consolidated no-input blocker summary across current handoff lanes."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_WRR_STATUS = Path("reports/wrr_1994/wrr_no_input_handoff_status.csv")
DEFAULT_WRR_SUMMARY = Path("reports/wrr_1994/wrr_no_input_handoff_status_summary.csv")
DEFAULT_CITIES_STATUS = Path("reports/cities_no_input_handoff_status/status.csv")
DEFAULT_CITIES_SUMMARY = Path("reports/cities_no_input_handoff_status/summary.csv")
DEFAULT_KJVA_STATUS = Path("reports/kjva_no_input_handoff_status/status.csv")
DEFAULT_KJVA_SUMMARY = Path("reports/kjva_no_input_handoff_status/summary.csv")
DEFAULT_OUT = Path("reports/no_input_blocker_summary/status.csv")
DEFAULT_SUMMARY_OUT = Path("reports/no_input_blocker_summary/summary.csv")
DEFAULT_MD = Path("docs/NO_INPUT_BLOCKER_SUMMARY.md")
DEFAULT_MANIFEST = Path("reports/no_input_blocker_summary/manifest.json")

LANE_FIELDNAMES = [
    "lane_id",
    "lane_name",
    "status_rows",
    "manual_input_needed_rows",
    "result_allowed",
    "primary_blocker",
    "next_human_input",
    "source_status",
    "summary_source",
    "status_source",
]

SUMMARY_FIELDNAMES = [
    "lane_rows",
    "total_status_rows",
    "total_manual_input_needed_rows",
    "result_allowed_lanes",
    "blocked_result_lanes",
    "wrr_remaining_gap",
    "cities_pending_transcription_rows",
    "kjva_blocked_gate_rows",
    "claim_boundary",
]

CLAIM_BOUNDARY = "no_result_bearing_work_without_manual_or_citable_input"


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    inputs = LoadedInputs(
        wrr_status=read_rows(args.wrr_status),
        wrr_summary=first_row(read_rows(args.wrr_summary)),
        cities_status=read_rows(args.cities_status),
        cities_summary=first_row(read_rows(args.cities_summary)),
        kjva_status=read_rows(args.kjva_status),
        kjva_summary=first_row(read_rows(args.kjva_summary)),
    )
    lanes = build_lane_rows(inputs, args)
    summary = build_summary(lanes, inputs)
    write_csv(args.out, LANE_FIELDNAMES, lanes)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, lanes)
    write_manifest(args.manifest_out, args, summary, lanes, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


class LoadedInputs:
    def __init__(
        self,
        *,
        wrr_status: list[dict[str, str]],
        wrr_summary: dict[str, str],
        cities_status: list[dict[str, str]],
        cities_summary: dict[str, str],
        kjva_status: list[dict[str, str]],
        kjva_summary: dict[str, str],
    ) -> None:
        self.wrr_status = wrr_status
        self.wrr_summary = wrr_summary
        self.cities_status = cities_status
        self.cities_summary = cities_summary
        self.kjva_status = kjva_status
        self.kjva_summary = kjva_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wrr-status", type=Path, default=DEFAULT_WRR_STATUS)
    parser.add_argument("--wrr-summary", type=Path, default=DEFAULT_WRR_SUMMARY)
    parser.add_argument("--cities-status", type=Path, default=DEFAULT_CITIES_STATUS)
    parser.add_argument("--cities-summary", type=Path, default=DEFAULT_CITIES_SUMMARY)
    parser.add_argument("--kjva-status", type=Path, default=DEFAULT_KJVA_STATUS)
    parser.add_argument("--kjva-summary", type=Path, default=DEFAULT_KJVA_SUMMARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_lane_rows(
    inputs: LoadedInputs, args: argparse.Namespace
) -> list[dict[str, str]]:
    return [
        {
            "lane_id": "wrr",
            "lane_name": "WRR exact-reproduction follow-up",
            "status_rows": str(len(inputs.wrr_status)),
            "manual_input_needed_rows": inputs.wrr_summary.get(
                "manual_input_needed_rows", "0"
            ),
            "result_allowed": bool_csv(inputs.wrr_summary.get("new_result_allowed")),
            "primary_blocker": (
                f"{inputs.wrr_summary.get('remaining_gap', '0')} published defined "
                "distances remain unresolved"
            ),
            "next_human_input": (
                "citable source-policy, row-transcription, page-image, or "
                "method/pair-universe decisions"
            ),
            "source_status": inputs.wrr_summary.get("claim_boundary", ""),
            "summary_source": str(args.wrr_summary),
            "status_source": str(args.wrr_status),
        },
        {
            "lane_id": "cities",
            "lane_name": "Cities source-row follow-up",
            "status_rows": str(len(inputs.cities_status)),
            "manual_input_needed_rows": inputs.cities_summary.get(
                "manual_input_needed_rows", "0"
            ),
            "result_allowed": bool_csv(inputs.cities_summary.get("result_allowed")),
            "primary_blocker": (
                f"{inputs.cities_summary.get('pending_transcription_rows', '0')} "
                "source rows still need verified transcription"
            ),
            "next_human_input": (
                "readable source-row transcription, source-row import decisions, "
                "normalization rules, preregistration, and controls"
            ),
            "source_status": inputs.cities_summary.get("claim_status", ""),
            "summary_source": str(args.cities_summary),
            "status_source": str(args.cities_status),
        },
        {
            "lane_id": "kjva",
            "lane_name": "KJVA independent-source follow-up",
            "status_rows": str(len(inputs.kjva_status)),
            "manual_input_needed_rows": inputs.kjva_summary.get(
                "manual_input_needed_rows", "0"
            ),
            "result_allowed": bool_csv(inputs.kjva_summary.get("result_allowed")),
            "primary_blocker": (
                f"{inputs.kjva_summary.get('blocked_gate_rows', '0')} next-result "
                "gates remain blocked"
            ),
            "next_human_input": (
                "source-use policy, locked text stream, verse-map/collation, "
                "fresh terms, leakage audit, fixed controls, and study lock"
            ),
            "source_status": inputs.kjva_summary.get("claim_status", ""),
            "summary_source": str(args.kjva_summary),
            "status_source": str(args.kjva_status),
        },
    ]


def build_summary(
    lanes: list[dict[str, str]], inputs: LoadedInputs
) -> dict[str, Any]:
    result_allowed_lanes = sum(1 for row in lanes if row["result_allowed"] == "1")
    return {
        "lane_rows": len(lanes),
        "total_status_rows": sum_int(lanes, "status_rows"),
        "total_manual_input_needed_rows": sum_int(lanes, "manual_input_needed_rows"),
        "result_allowed_lanes": result_allowed_lanes,
        "blocked_result_lanes": len(lanes) - result_allowed_lanes,
        "wrr_remaining_gap": inputs.wrr_summary.get("remaining_gap", "0"),
        "cities_pending_transcription_rows": inputs.cities_summary.get(
            "pending_transcription_rows", "0"
        ),
        "kjva_blocked_gate_rows": inputs.kjva_summary.get("blocked_gate_rows", "0"),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_markdown(
    path: Path, summary: dict[str, Any], lanes: list[dict[str, str]]
) -> None:
    lines = [
        "# No-Input Blocker Summary",
        "",
        "Status: consolidated blocker map.",
        "",
        "This is not a new result, not a statistical claim, not a source-text lock, "
        "and not permission to run result-bearing follow-ups.",
        "It joins the current WRR, Cities, and KJVA no-input handoff packets so the "
        "remaining human or citable-input blockers stay visible in one place.",
        "",
        "## Summary",
        "",
        f"- Lane rows: {summary['lane_rows']}.",
        f"- Total status rows: {summary['total_status_rows']}.",
        f"- Total manual-input-needed rows: {summary['total_manual_input_needed_rows']}.",
        f"- Result-allowed lanes: {summary['result_allowed_lanes']}.",
        f"- Blocked result lanes: {summary['blocked_result_lanes']}.",
        f"- WRR remaining defined-distance gap: {summary['wrr_remaining_gap']}.",
        "- Cities pending transcription rows: "
        f"{summary['cities_pending_transcription_rows']}.",
        f"- KJVA blocked next-result gates: {summary['kjva_blocked_gate_rows']}.",
        f"- Claim boundary: `{summary['claim_boundary']}`.",
        "",
        "## Blocker Rows",
        "",
        "| Lane | Status rows | Manual-input rows | Result allowed | Primary blocker | Next input |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in lanes:
        lines.append(
            "| {lane_name} | {status_rows} | {manual_input_needed_rows} | "
            "{result_allowed} | {primary_blocker} | {next_human_input} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Cautions",
            "",
            "- This page summarizes blockers; it does not close any blocker.",
            "- `Result allowed` must remain 0 before any result-bearing follow-up.",
            "- OCR, crop, source-candidate, and diagnostic packets are review aids only.",
            "- Citable source policy or human-readable source review is still required.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, Any],
    lanes: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "scripts.build_no_input_blocker_summary",
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "els_version": __version__,
        "claim_boundary": "no-input blocker summary only; no result-bearing output",
        "text_retention": "no Bible text written to tracked outputs",
        "inputs": {
            "wrr_status": str(args.wrr_status),
            "wrr_summary": str(args.wrr_summary),
            "cities_status": str(args.cities_status),
            "cities_summary": str(args.cities_summary),
            "kjva_status": str(args.kjva_status),
            "kjva_summary": str(args.kjva_summary),
        },
        "outputs": {
            "status": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
        "summary": summary,
        "lane_rows": len(lanes),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def first_row(rows: list[dict[str, str]]) -> dict[str, str]:
    return rows[0] if rows else {}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def sum_int(rows: list[dict[str, Any]], key: str) -> int:
    return sum(int(str(row.get(key, "0") or "0")) for row in rows)


def bool_csv(value: str | None) -> str:
    return "1" if str(value).strip().lower() in {"1", "true", "yes"} else "0"


if __name__ == "__main__":
    raise SystemExit(main())
