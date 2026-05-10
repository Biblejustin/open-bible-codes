#!/usr/bin/env python3
"""Public-release hygiene checks for tracked files and Git remotes."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.release_hygiene import (
    DEFAULT_OWNER,
    DEFAULT_REPO,
    FORBIDDEN_ACCOUNT_TERMS,
    format_finding,
    git_tracked_paths,
    remote_owner_failures,
    risky_tracked_paths,
    scan_tracked_for_forbidden_account,
    scan_tracked_for_secret_patterns,
)


OUT = Path("reports/public_release_hygiene.json")


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    root = Path.cwd()
    failures: list[str] = []

    git_status = run_git(root, "status", "--short")
    if git_status and not args.allow_dirty:
        failures.append("git working tree is not clean")

    remotes = git_remotes(root)
    remote_failures = remote_owner_failures(remotes, owner=args.owner, repo=args.repo)
    failures.extend(remote_failures)

    tracked_paths = git_tracked_paths(root)
    risky_paths = risky_tracked_paths(tracked_paths)
    if risky_paths:
        failures.append("risky tracked paths: " + ", ".join(risky_paths[:10]))

    forbidden_text_hits = scan_tracked_for_forbidden_account(root, tracked_paths)
    if forbidden_text_hits:
        failures.append("forbidden account text in tracked files: " + ", ".join(forbidden_text_hits[:10]))

    secret_hits = scan_tracked_for_secret_patterns(root, tracked_paths)
    if secret_hits:
        failures.append(
            "high-confidence secret patterns in tracked files: "
            + ", ".join(format_finding(hit) for hit in secret_hits[:10])
        )

    payload = {
        "tool": "check_public_release_hygiene",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "status": "failed" if failures else "passed",
        "output_path": str(args.out),
        "allow_dirty": args.allow_dirty,
        "expected_owner": args.owner,
        "expected_repo": args.repo,
        "git_status_lines": git_status,
        "git_remotes": remotes,
        "tracked_path_count": len(tracked_paths),
        "risky_tracked_paths": risky_paths,
        "forbidden_account_terms": FORBIDDEN_ACCOUNT_TERMS,
        "forbidden_text_hits": forbidden_text_hits,
        "secret_pattern_hits": [hit.as_dict() for hit in secret_hits],
        "failures": failures,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.out)
    if failures:
        for failure in failures:
            print(f"public-release hygiene failure: {failure}")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--out", type=Path, default=OUT)
    return parser


def git_remotes(root: Path) -> list[str]:
    return run_git(root, "remote", "-v")


def run_git(root: Path, *args: str) -> list[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout.strip()
    if not output:
        return []
    return output.splitlines()


if __name__ == "__main__":
    raise SystemExit(main())
