#!/usr/bin/env python3
"""Preflight a locked prospective study before any result-producing run."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from scripts import check_preregistration_placeholders as prereg_check
from scripts import check_study_lock_manifest as lock_check
from scripts import preflight_real_report_run as report_preflight
from scripts.release_hygiene import (
    format_finding,
    git_tracked_paths,
    remote_owner_failures,
    risky_tracked_paths,
    scan_tracked_for_forbidden_account,
    scan_tracked_for_secret_patterns,
)


DEFAULT_REQUIRED_SETTINGS = [
    "skip_range",
    "direction",
    "min_normalized_length",
    "controls",
    "correction",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    out_path = args.out or default_out_path(args.manifest)
    root = Path.cwd()
    failures: list[str] = []

    git_status = report_preflight.git_status_short(root)
    if git_status and not args.allow_dirty:
        failures.append("git working tree is not clean")

    remotes = report_preflight.git_remotes(root)
    remote_failures = remote_owner_failures(remotes)
    failures.extend(remote_failures)

    forbidden_repo_hits = report_preflight.scan_forbidden_terms(root)
    if forbidden_repo_hits:
        failures.append(
            "forbidden account text found in repository files: "
            + ", ".join(forbidden_repo_hits[:5])
        )

    tracked_paths = git_tracked_paths(root)
    risky_paths = risky_tracked_paths(tracked_paths)
    if risky_paths:
        failures.append("risky tracked paths: " + ", ".join(risky_paths[:10]))

    forbidden_tracked_hits = scan_tracked_for_forbidden_account(root, tracked_paths)
    if forbidden_tracked_hits:
        failures.append(
            "forbidden account text in tracked files: "
            + ", ".join(forbidden_tracked_hits[:10])
        )

    secret_hits = scan_tracked_for_secret_patterns(root, tracked_paths)
    if secret_hits:
        failures.append(
            "high-confidence secret patterns in tracked files: "
            + ", ".join(format_finding(hit) for hit in secret_hits[:10])
        )

    placeholder_rows = placeholder_failures(args.preregistration)
    if placeholder_rows:
        failures.append(f"unresolved preregistration placeholders: {len(placeholder_rows)}")

    manifest_failures: list[str] = []
    manifest_payload: dict[str, Any] | None = None
    required_settings = required_settings_for(args)
    if not args.manifest.exists():
        manifest_failures.append(f"manifest does not exist: {args.manifest}")
    else:
        try:
            manifest_payload = lock_check.read_manifest(args.manifest)
            manifest_failures = lock_check.validate_manifest(
                manifest_payload,
                required_settings=required_settings,
                allow_dirty=args.allow_dirty,
                verify_paths=not args.no_verify_paths,
            )
        except (OSError, ValueError) as exc:
            manifest_failures.append(f"manifest could not be read: {exc}")
    failures.extend(f"lock manifest: {failure}" for failure in manifest_failures)

    protocol_result = protocol_dry_run(args.protocol)
    if protocol_result and protocol_result["returncode"] != 0:
        failures.append(f"protocol dry-run failed: {args.protocol}")

    term_audit_failures = clean_term_audit_failures(args.clean_term_audit)
    failures.extend(f"clean term audit: {failure}" for failure in term_audit_failures)

    payload = {
        "tool": "preflight_prospective_study",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "status": "failed" if failures else "passed",
        "output_path": str(out_path),
        "allow_dirty": args.allow_dirty,
        "preregistration": str(args.preregistration),
        "manifest": str(args.manifest),
        "protocol": str(args.protocol) if args.protocol else "",
        "required_settings": required_settings,
        "git_status_lines": git_status,
        "git_remotes": remotes,
        "remote_failures": remote_failures,
        "forbidden_repo_hits": forbidden_repo_hits,
        "tracked_path_count": len(tracked_paths),
        "risky_tracked_paths": risky_paths,
        "forbidden_tracked_hits": forbidden_tracked_hits,
        "secret_pattern_hits": [hit.as_dict() for hit in secret_hits],
        "placeholder_hits": placeholder_rows,
        "manifest_name": manifest_payload.get("name") if manifest_payload else "",
        "manifest_status": manifest_payload.get("status") if manifest_payload else "",
        "manifest_failures": manifest_failures,
        "protocol_dry_run": protocol_result,
        "clean_term_audits": [str(path) for path in args.clean_term_audit],
        "term_audit_failures": term_audit_failures,
        "failures": failures,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    if failures:
        for failure in failures:
            print(f"prospective preflight failure: {failure}")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preregistration", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--protocol", type=Path)
    parser.add_argument("--required-setting", action="append", default=[])
    parser.add_argument("--no-default-required-settings", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--no-verify-paths", action="store_true")
    parser.add_argument(
        "--clean-term-audit",
        type=Path,
        action="append",
        default=[],
        help="Audit summary JSON from scripts.audit_prospective_terms that must have status=passed.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Defaults to <manifest-dir>/<manifest-name-without-.manifest>.preflight.json.",
    )
    return parser


def default_out_path(manifest: Path) -> Path:
    name = manifest.name
    if name.endswith(".manifest.json"):
        stem = name[: -len(".manifest.json")]
    else:
        stem = manifest.stem
    return manifest.with_name(f"{stem}.preflight.json")


def required_settings_for(args: argparse.Namespace) -> list[str]:
    settings = [] if args.no_default_required_settings else list(DEFAULT_REQUIRED_SETTINGS)
    settings.extend(args.required_setting)
    return dedupe(settings)


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def placeholder_failures(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return [{"path": str(path), "line": 0, "column": 0, "placeholder": "missing file"}]
    return [
        {
            "path": str(hit.path),
            "line": hit.line_number,
            "column": hit.column_number,
            "placeholder": hit.placeholder,
        }
        for hit in prereg_check.find_placeholders(path, allowed=set())
    ]


def protocol_dry_run(protocol: Path | None) -> dict[str, Any] | None:
    if protocol is None:
        return None
    if not protocol.exists():
        return {"returncode": 1, "stdout": "", "stderr": f"protocol does not exist: {protocol}"}
    completed = subprocess.run(
        [sys.executable, "-m", "scripts.run_protocol", str(protocol), "--dry-run"],
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def clean_term_audit_failures(paths: list[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        if not path.exists():
            failures.append(f"missing audit summary: {path}")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"could not read audit summary {path}: {exc}")
            continue
        if payload.get("status") != "passed":
            failures.append(
                f"{path} status={payload.get('status', '')} match_rows={payload.get('match_rows', '')}"
            )
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
