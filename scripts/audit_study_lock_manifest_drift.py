#!/usr/bin/env python3
"""Audit historical study-lock manifests without failing on expected drift."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els.protocol_runner import path_fingerprints
from scripts.check_study_lock_manifest import read_manifest, validate_manifest


DEFAULT_MANIFEST_DIR = Path("reports/study_locks")
DEFAULT_OUT_DIR = Path("reports/study_lock_manifest_drift_audit")
DEFAULT_OUT = DEFAULT_OUT_DIR / "manifest_drift_audit.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MARKDOWN = Path("docs/STUDY_LOCK_MANIFEST_DRIFT_AUDIT.md")
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
FIELDNAMES = [
    "manifest_path",
    "name",
    "created_utc",
    "git_commit",
    "git_dirty",
    "status",
    "locked_path_count",
    "missing_path_count",
    "audit_status",
    "structural_failures",
    "fingerprint_failures",
]
SUMMARY_FIELDNAMES = ["metric", "value"]
AUDIT_STATUSES = ("current", "fingerprint_drift", "structural_fail")
LOCK_TOOL = "build_study_lock_manifest"


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = audit_manifest_dir(args.manifest_dir)
    summary = summarize_rows(rows)
    write_csv(args.out, FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows(summary))
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.write_text(
        render_markdown(rows, summary, args.manifest_dir, args.out, args.summary_out),
        encoding="utf-8",
    )
    write_manifest(args.manifest_out, args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-dir", type=Path, default=DEFAULT_MANIFEST_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def audit_manifest_dir(manifest_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(manifest_dir.glob("*.manifest.json")):
        try:
            payload = read_manifest(path)
        except (OSError, json.JSONDecodeError) as exc:
            rows.append(error_row(path, f"could not read manifest: {exc}"))
            continue
        if payload.get("tool") != LOCK_TOOL:
            continue
        rows.append(classify_manifest(path, payload))
    return rows


def classify_manifest(path: Path, payload: dict[str, Any]) -> dict[str, str]:
    structural_failures = validate_manifest(
        payload,
        required_settings=[],
        allow_dirty=False,
        verify_paths=False,
    )
    full_failures = validate_manifest(
        payload,
        required_settings=[],
        allow_dirty=False,
        verify_paths=True,
    )
    fingerprint_failures = [
        failure for failure in full_failures if failure not in structural_failures
    ]
    if structural_failures:
        audit_status = "structural_fail"
    elif fingerprint_failures:
        audit_status = "fingerprint_drift"
    else:
        audit_status = "current"

    git = payload.get("git", {})
    locked_paths = payload.get("locked_paths", [])
    missing_paths = payload.get("missing_paths", [])
    return {
        "manifest_path": path.as_posix(),
        "name": str(payload.get("name", "")),
        "created_utc": str(payload.get("created_utc", "")),
        "git_commit": str(git.get("commit", "")) if isinstance(git, dict) else "",
        "git_dirty": str(bool(git.get("dirty"))) if isinstance(git, dict) else "",
        "status": str(payload.get("status", "")),
        "locked_path_count": str(len(locked_paths) if isinstance(locked_paths, list) else 0),
        "missing_path_count": str(len(missing_paths) if isinstance(missing_paths, list) else 0),
        "audit_status": audit_status,
        "structural_failures": "; ".join(structural_failures),
        "fingerprint_failures": "; ".join(fingerprint_failures),
    }


def error_row(path: Path, failure: str) -> dict[str, str]:
    return {
        "manifest_path": path.as_posix(),
        "name": "",
        "created_utc": "",
        "git_commit": "",
        "git_dirty": "",
        "status": "",
        "locked_path_count": "0",
        "missing_path_count": "0",
        "audit_status": "structural_fail",
        "structural_failures": failure,
        "fingerprint_failures": "",
    }


def summarize_rows(rows: list[dict[str, str]]) -> dict[str, int]:
    counts = Counter(row["audit_status"] for row in rows)
    summary = {"total_manifests": len(rows)}
    for status in AUDIT_STATUSES:
        summary[status] = counts.get(status, 0)
    return summary


def summary_rows(summary: dict[str, int]) -> list[dict[str, str]]:
    return [
        {"metric": metric, "value": str(value)}
        for metric, value in summary.items()
    ]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def render_markdown(
    rows: list[dict[str, str]],
    summary: dict[str, int],
    manifest_dir: Path,
    out: Path,
    summary_out: Path,
) -> str:
    lines = [
        "# Study Lock Manifest Drift Audit",
        "",
        "Status: historical audit, not a prospective approval.",
        "",
        "This audit lists historical study-lock manifests and separates current",
        "manifests from stale fingerprints or structural lock failures.",
        "A drifted historical manifest is not a failed result.",
        "It means the old lock no longer validates against the current workspace",
        "and must not be reused as a fresh prospective lock.",
        "",
        "## Inputs",
        "",
        f"- Manifest directory: `{manifest_dir.as_posix()}`",
        f"- Row output: `{out.as_posix()}`",
        f"- Summary output: `{summary_out.as_posix()}`",
        "",
        "## Summary",
        "",
        f"- total_manifests: {summary['total_manifests']}",
    ]
    for status in AUDIT_STATUSES:
        lines.append(f"- {status}: {summary[status]}")

    lines.extend(
        [
            "",
            "## Manifest Rows",
            "",
            "| Manifest | Name | Status | Audit status | Structural failures | Fingerprint failures |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                markdown_cell(value)
                for value in [
                    f"`{row['manifest_path']}`",
                    row["name"],
                    row["status"],
                    row["audit_status"],
                    row["structural_failures"] or "none",
                    row["fingerprint_failures"] or "none",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `current` means the manifest still validates against current files.",
            "- `fingerprint_drift` means the lock structure is usable, but at least",
            "  one locked file or directory changed since the lock was built.",
            "- `structural_fail` means the manifest was dirty, incomplete, missing",
            "  paths, unlocked, unreadable, or otherwise invalid as a lock.",
            "- Use `scripts.check_study_lock_manifest` for one fresh, study-specific",
            "  manifest before a result-producing prospective run.",
            "",
        ]
    )
    return "\n".join(lines)


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary: dict[str, int],
    started: float,
) -> None:
    input_paths = [
        row["manifest_path"]
        for row in rows
        if row["manifest_path"]
    ]
    output_paths = [
        args.out.as_posix(),
        args.summary_out.as_posix(),
        args.markdown_out.as_posix(),
    ]
    payload = {
        "tool": "audit_study_lock_manifest_drift",
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "args": {
            "manifest_dir": args.manifest_dir.as_posix(),
            "out": args.out.as_posix(),
            "summary_out": args.summary_out.as_posix(),
            "markdown_out": args.markdown_out.as_posix(),
            "manifest_out": args.manifest_out.as_posix(),
        },
        "summary": summary,
        "inputs": path_fingerprints(input_paths),
        "outputs": path_fingerprints(output_paths),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
