#!/usr/bin/env python3
"""Build a WRR claim-blocker packet from current readiness artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_READINESS = Path("reports/wrr_1994/wrr_claim_readiness.csv")
DEFAULT_LOCK_OPTIONS = Path("reports/wrr_1994/wrr_lock_options.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_METHOD_STATUS = Path("reports/wrr_1994/wrr_method_status.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_claim_blocker_packet.csv")
DEFAULT_MD = Path("docs/WRR_CLAIM_BLOCKER_PACKET.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_claim_blocker_packet.manifest.json")

FIELDNAMES = [
    "decision_area",
    "current_status",
    "ready",
    "blocker",
    "current_read",
    "available_options",
    "source_review_flags",
    "no_input_next",
    "input_needed",
]


INPUT_NEEDED = {
    "Pair universe": "select pair-universe/source-review policy",
    "D(w) skip-cap formula": "select printed WRR formula or reported WRR-program formula",
    "Corrected distance c(w,w')": "requires locked pair universe and D(w) formula first",
    "Aggregate statistic and permutation": "requires locked pair universe, D(w), and full corrected-distance run first",
}

NO_INPUT_NEXT = {
    "Pair universe": (
        "diagnostic review can continue, but claim-grade reproduction must not "
        "promote a pair universe without source policy"
    ),
    "D(w) skip-cap formula": (
        "keep printed/program sensitivity visible; do not pick final formula "
        "without source policy"
    ),
    "Corrected distance c(w,w')": (
        "diagnostic full-lane runs can continue only as diagnostics until upstream "
        "locks exist"
    ),
    "Aggregate statistic and permutation": (
        "keep date-label permutation diagnostics separate from WRR reproduction "
        "language"
    ),
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    readiness_rows = read_rows(args.readiness)
    lock_rows = read_rows(args.lock_options)
    source_rows = read_rows(args.source_queue)
    method_rows = read_rows(args.method_status)
    packet_rows = build_packet_rows(readiness_rows, lock_rows, source_rows, method_rows)
    write_csv(args.out, packet_rows)
    write_markdown(args.markdown_out, packet_rows, source_rows, args)
    write_manifest(args.manifest_out, args, packet_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readiness", type=Path, default=DEFAULT_READINESS)
    parser.add_argument("--lock-options", type=Path, default=DEFAULT_LOCK_OPTIONS)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--method-status", type=Path, default=DEFAULT_METHOD_STATUS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_packet_rows(
    readiness_rows: list[dict[str, str]],
    lock_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    method_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    options_by_area = group_lock_options(lock_rows)
    method_by_area = {row.get("decision_area", ""): row for row in method_rows}
    source_flags = source_flag_summary(source_rows)
    out = []
    for row in readiness_rows:
        area = row.get("decision_area", "")
        if row.get("ready", "") == "true":
            continue
        out.append(
            {
                "decision_area": area,
                "current_status": row.get("status", ""),
                "ready": row.get("ready", ""),
                "blocker": row.get("blocker", ""),
                "current_read": method_by_area.get(area, {}).get("current_read", ""),
                "available_options": options_by_area.get(area, ""),
                "source_review_flags": source_flags if area == "Pair universe" else "",
                "no_input_next": NO_INPUT_NEXT.get(area, ""),
                "input_needed": INPUT_NEEDED.get(area, ""),
            }
        )
    return out


def group_lock_options(rows: list[dict[str, str]]) -> dict[str, str]:
    grouped: dict[str, list[str]] = {}
    for row in rows:
        area = row.get("area", "")
        if not area:
            continue
        grouped.setdefault(area, []).append(
            f"{row.get('option', '')} [{row.get('status', '')}]"
        )
    return {area: "; ".join(options) for area, options in grouped.items()}


def source_flag_summary(rows: list[dict[str, str]]) -> str:
    counter = Counter(
        flag
        for row in rows
        for flag in row.get("source_review_flags", "").split(";")
        if flag
    )
    if not counter:
        return ""
    total = sum(counter.values())
    parts = ", ".join(f"{counter[flag]} {flag}" for flag in sorted(counter))
    return f"{total} flagged queued terms: {parts}"


def flagged_source_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    flagged = [row for row in rows if row.get("source_review_flags")]
    return sorted(flagged, key=lambda row: int_or_zero(row.get("priority_rank", "")))


def write_markdown(
    path: Path,
    packet_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# WRR Claim Blocker Packet",
        "",
        "Status: no-input diagnostics exhausted for claim-grade WRR reproduction.",
        "",
        "This packet does not choose disputed WRR method policy. It gathers the",
        "claim-readiness blockers, current lock options, and WNP/context source",
        "queue flags into one handoff artifact.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_claim_blocker_packet "
            f"--readiness {args.readiness} "
            f"--lock-options {args.lock_options} "
            f"--source-queue {args.source_queue} "
            f"--method-status {args.method_status} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Blockers",
        "",
        "| Area | Status | Blocker | Input needed |",
        "| --- | --- | --- | --- |",
    ]
    for row in packet_rows:
        lines.append(
            "| {area} | `{status}` | {blocker} | {input_needed} |".format(
                area=markdown_cell(row["decision_area"]),
                status=markdown_cell(row["current_status"]),
                blocker=markdown_cell(row["blocker"]),
                input_needed=markdown_cell(row["input_needed"]),
            )
        )
    lines.extend(
        [
            "",
            "## No-Input Boundary",
            "",
            "| Area | Current read | Available options | No-input next |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in packet_rows:
        lines.append(
            "| {area} | {current_read} | {options} | {no_input_next} |".format(
                area=markdown_cell(row["decision_area"]),
                current_read=markdown_cell(row["current_read"]),
                options=markdown_cell(row["available_options"]),
                no_input_next=markdown_cell(row["no_input_next"]),
            )
        )
    flagged_rows = flagged_source_rows(source_rows)
    if flagged_rows:
        lines.extend(
            [
                "",
                "## Flagged Source-Review Rows",
                "",
                "| Rank | Term id | Term | Bucket | Flags | Action |",
                "| ---: | --- | --- | --- | --- | --- |",
            ]
        )
        for row in flagged_rows:
            lines.append(
                "| {rank} | `{term_id}` | `{term}` | `{bucket}` | `{flags}` | {action} |".format(
                    rank=markdown_cell(row.get("priority_rank", "")),
                    term_id=markdown_cell(row.get("term_id", "")),
                    term=markdown_cell(row.get("term", "")),
                    bucket=markdown_cell(row.get("review_bucket", "")),
                    flags=markdown_cell(row.get("source_review_flags", "")),
                    action=markdown_cell(row.get("source_review_action", "")),
                )
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a decision packet, not a reproduction result.",
            "- Further diagnostics can stay useful, but claim-grade wording requires a source policy.",
            "- No pair exclusion or D(w) formula is chosen here.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_claim_blocker_packet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "blocker_rows": len(rows),
        "inputs": {
            "readiness": str(args.readiness),
            "lock_options": str(args.lock_options),
            "source_queue": str(args.source_queue),
            "method_status": str(args.method_status),
        },
        "outputs": {
            "out": str(args.out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
