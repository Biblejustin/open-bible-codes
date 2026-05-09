#!/usr/bin/env python3
"""Run protocol benchmarks and write repeatable timing reports."""

from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
from els.protocol_runner import atomic_write_text


@dataclass(frozen=True)
class RunRecord:
    kind: str
    index: int
    seconds: float
    return_code: int
    status: str
    manifest_path: str
    step_seconds: dict[str, float]
    stdout_tail: str
    stderr_tail: str


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.runs < 1:
        parser.error("--runs must be >= 1")
    if args.warmup < 0:
        parser.error("--warmup must be >= 0")

    label = args.label or safe_name(Path(args.protocol).stem)
    out_dir = resolve_path(args.out_dir)
    manifest_dir = resolve_path(args.manifest_dir) if args.manifest_dir else out_dir / f"{label}_manifests"
    json_out = resolve_path(args.json_out) if args.json_out else out_dir / f"{label}_benchmark.json"
    md_out = resolve_path(args.md_out) if args.md_out else out_dir / f"{label}_benchmark.md"

    records: list[RunRecord] = []
    for index in range(1, args.warmup + 1):
        records.append(run_once(args, manifest_dir, label, kind="warmup", index=index))
    for index in range(1, args.runs + 1):
        records.append(run_once(args, manifest_dir, label, kind="measure", index=index))

    payload = benchmark_payload(args, label, records, json_out, md_out)
    if not args.no_write:
        atomic_write_text(json_out, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        atomic_write_text(md_out, render_markdown(payload))
    print_summary(payload, json_out, md_out, write_outputs=not args.no_write)
    failed = [record for record in records if record.return_code != 0]
    return failed[0].return_code if failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Benchmark a protocol with repeated full runs and median timing output."
    )
    parser.add_argument("protocol", nargs="?", default="protocols/public_baseline.toml")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--warmup", type=int, default=0)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--only", action="append", help="run one step id; repeatable")
    parser.add_argument("--label")
    parser.add_argument("--out-dir", default="reports/benchmarks")
    parser.add_argument("--manifest-dir")
    parser.add_argument("--json-out")
    parser.add_argument("--md-out")
    parser.add_argument("--no-write", action="store_true")
    return parser


def run_once(
    args: argparse.Namespace,
    manifest_dir: Path,
    label: str,
    *,
    kind: str,
    index: int,
) -> RunRecord:
    manifest_path = manifest_dir / f"{label}_{kind}_{index}.manifest.json"
    command = [
        sys.executable,
        "scripts/run_protocol.py",
        args.protocol,
        "--manifest-out",
        str(manifest_path),
    ]
    for step_id in args.only or []:
        command.extend(["--only", step_id])
    if args.resume:
        command.append("--resume")

    start = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    seconds = round(time.perf_counter() - start, 3)
    status = "missing_manifest"
    step_seconds: dict[str, float] = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        status = str(manifest.get("status", "unknown"))
        step_seconds = {
            str(step["id"]): float(step.get("duration_seconds", 0.0))
            for step in manifest.get("steps", [])
        }
    return RunRecord(
        kind=kind,
        index=index,
        seconds=seconds,
        return_code=completed.returncode,
        status=status,
        manifest_path=relative_or_absolute(manifest_path),
        step_seconds=step_seconds,
        stdout_tail=tail(completed.stdout),
        stderr_tail=tail(completed.stderr),
    )


def benchmark_payload(
    args: argparse.Namespace,
    label: str,
    records: list[RunRecord],
    json_out: Path,
    md_out: Path,
) -> dict[str, Any]:
    measured = [record for record in records if record.kind == "measure"]
    seconds = [record.seconds for record in measured]
    return {
        "tool": "benchmark_protocol",
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "label": label,
        "protocol": args.protocol,
        "runs": args.runs,
        "warmup": args.warmup,
        "resume": bool(args.resume),
        "only": args.only or [],
        "json_out": relative_or_absolute(json_out),
        "md_out": relative_or_absolute(md_out),
        "summary": summary_stats(seconds),
        "step_medians": step_medians(measured),
        "records": [asdict(record) for record in records],
    }


def summary_stats(values: list[float]) -> dict[str, float | int]:
    if not values:
        return {"count": 0}
    return {
        "count": len(values),
        "median": round(statistics.median(values), 3),
        "mean": round(statistics.mean(values), 3),
        "min": round(min(values), 3),
        "max": round(max(values), 3),
        "stdev": round(statistics.pstdev(values), 3) if len(values) > 1 else 0.0,
    }


def step_medians(records: list[RunRecord]) -> list[dict[str, float | str | int]]:
    step_order: list[str] = []
    by_step: dict[str, list[float]] = {}
    for record in records:
        for step_id, seconds in record.step_seconds.items():
            if step_id not in by_step:
                step_order.append(step_id)
                by_step[step_id] = []
            by_step[step_id].append(seconds)
    rows = [
        {
            "step": step_id,
            "runs": len(by_step[step_id]),
            "median_seconds": round(statistics.median(by_step[step_id]), 3),
            "min_seconds": round(min(by_step[step_id]), 3),
            "max_seconds": round(max(by_step[step_id]), 3),
        }
        for step_id in step_order
    ]
    return sorted(rows, key=lambda row: float(row["median_seconds"]), reverse=True)


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Protocol Benchmark",
        "",
        f"- protocol: `{payload['protocol']}`",
        f"- git commit: `{payload['git_commit']}`",
        f"- runs: `{payload['runs']}`",
        f"- warmup: `{payload['warmup']}`",
        f"- resume: `{payload['resume']}`",
        f"- generated UTC: `{payload['generated_utc']}`",
        "",
        "## Summary",
        "",
        "| metric | value |",
        "| --- | ---: |",
    ]
    for key in ("median", "mean", "min", "max", "stdev"):
        if key in summary:
            lines.append(f"| {key} seconds | {summary[key]:.3f} |")
    lines.extend(
        [
            "",
            "## Runs",
            "",
            "| kind | run | seconds | return code | status | manifest |",
            "| --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for record in payload["records"]:
        lines.append(
            "| {kind} | {index} | {seconds:.3f} | {return_code} | {status} | `{manifest_path}` |".format(
                **record
            )
        )
    lines.extend(
        [
            "",
            "## Step Medians",
            "",
            "| step | runs | median seconds | min | max |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in payload["step_medians"]:
        lines.append(
            "| {step} | {runs} | {median_seconds:.3f} | {min_seconds:.3f} | {max_seconds:.3f} |".format(
                **row
            )
        )
    return "\n".join(lines) + "\n"


def print_summary(
    payload: dict[str, Any],
    json_out: Path,
    md_out: Path,
    *,
    write_outputs: bool,
) -> None:
    summary = payload["summary"]
    print(
        "median={median:.3f}s mean={mean:.3f}s min={min:.3f}s max={max:.3f}s".format(
            **summary
        )
    )
    if write_outputs:
        print(relative_or_absolute(json_out))
        print(relative_or_absolute(md_out))


def git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return "unknown"
    return completed.stdout.strip() or "unknown"


def resolve_path(raw: str) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        return ROOT / path
    return path


def relative_or_absolute(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def safe_name(value: str) -> str:
    safe = "".join(char if char.isalnum() or char in "._-" else "_" for char in value)
    return safe or "protocol"


def tail(value: str, limit: int = 4000) -> str:
    if len(value) <= limit:
        return value
    return value[-limit:]


if __name__ == "__main__":
    raise SystemExit(main())
