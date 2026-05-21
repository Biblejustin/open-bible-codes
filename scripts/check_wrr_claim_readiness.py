#!/usr/bin/env python3
"""Check whether WRR work is ready for claim-grade reproduction language."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_STATUS = Path("reports/wrr_1994/wrr_method_status.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_claim_readiness.csv")
DEFAULT_MD = Path("docs/WRR_CLAIM_READINESS.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_claim_readiness.manifest.json")

REQUIRED_AREAS = {
    "Pair universe": {"locked", "source_locked"},
    "D(w) skip-cap formula": {"locked", "source_locked"},
    "Corrected distance c(w,w')": {"full_run_locked", "defined_full_run"},
    "Aggregate statistic and permutation": {"permutation_locked", "claim_grade_ready"},
}

FIELDNAMES = [
    "decision_area",
    "status",
    "required_statuses",
    "ready",
    "blocker",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    status_rows = read_rows(args.status)
    rows = readiness_rows(status_rows)
    write_rows(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    if args.manifest_out:
        write_manifest(args, rows, started)
    print(args.out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    if args.require_ready and not all_ready(rows):
        for row in rows:
            if row["ready"] != "true":
                print(f"WRR claim readiness blocker: {row['blocker']}")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="Exit nonzero unless every required WRR decision area is claim-ready.",
    )
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def readiness_rows(status_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_area = {row.get("decision_area", ""): row for row in status_rows}
    rows: list[dict[str, str]] = []
    for area, allowed_statuses in REQUIRED_AREAS.items():
        status = by_area.get(area, {}).get("status", "")
        ready = status in allowed_statuses
        required = ",".join(sorted(allowed_statuses))
        rows.append(
            {
                "decision_area": area,
                "status": status,
                "required_statuses": required,
                "ready": str(ready).lower(),
                "blocker": "" if ready else blocker_text(area, status, required),
            }
        )
    return rows


def blocker_text(area: str, status: str, required: str) -> str:
    if not status:
        return f"{area}: missing from method-status matrix; requires one of {required}"
    return f"{area}: status {status} is not claim-ready; requires one of {required}"


def all_ready(rows: list[dict[str, str]]) -> bool:
    return all(row["ready"] == "true" for row in rows)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    ready = all_ready(rows)
    lines = [
        "# WRR Claim Readiness",
        "",
        f"Status: {'ready' if ready else 'blocked'} for claim-grade WRR reproduction language.",
        "",
        "This gate does not decide disputed WRR method questions. It only records",
        "whether the method-status matrix has the required locked statuses.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.check_wrr_claim_readiness "
            f"--status {args.status} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Gate",
        "",
        "| Area | Current status | Required status | Ready | Blocker |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["decision_area"]),
                    f"`{markdown_cell(row['status'])}`",
                    f"`{markdown_cell(row['required_statuses'])}`",
                    f"`{row['ready']}`",
                    markdown_cell(row["blocker"]),
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "status": "ready" if all_ready(rows) else "blocked",
        "input": str(args.status),
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
