#!/usr/bin/env python3
"""Public-release hygiene checks for tracked files and Git remotes."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.preflight_real_report_run import FORBIDDEN_ACCOUNT_TERMS, forbidden_hits


OUT = Path("reports/public_release_hygiene.json")
DEFAULT_OWNER = "Biblejustin"
DEFAULT_REPO = "open-bible-codes"
ALLOWED_TRACKED_REPORTS = {"reports/.gitkeep"}
RISKY_SUFFIXES = {
    ".db",
    ".duckdb",
    ".key",
    ".p12",
    ".pem",
    ".pfx",
    ".sqlite",
    ".sqlite3",
}
RISKY_PATH_NAME_PARTS = {
    "credential",
    "credentials",
    "password",
    "secret",
    "secrets",
    "token",
    "tokens",
}
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("github_fine_grained_token", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("github_classic_token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}")),
    ("openai_secret_key", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
    ("private_key_block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
)


@dataclass(frozen=True)
class TextFinding:
    path: str
    line: int
    kind: str

    def as_dict(self) -> dict[str, object]:
        return {"path": self.path, "line": self.line, "kind": self.kind}


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


def git_tracked_paths(root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0 or not completed.stdout:
        return []
    return [path.decode("utf-8") for path in completed.stdout.split(b"\0") if path]


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


def remote_owner_failures(remotes: list[str], *, owner: str, repo: str) -> list[str]:
    if not remotes:
        return ["no git remotes configured"]
    failures: list[str] = []
    joined = "\n".join(remotes)
    remote_forbidden_hits = forbidden_hits(joined)
    if remote_forbidden_hits:
        failures.append(
            "forbidden account text found in git remotes: "
            + ", ".join(sorted(remote_forbidden_hits))
        )
    expected = f"github.com/{owner.lower()}/{repo.lower()}"
    expected_alt = f"github.com:{owner.lower()}/{repo.lower()}"
    normalized = "\n".join(normalize_remote(remote) for remote in remotes)
    if expected not in normalized and expected_alt not in normalized:
        failures.append(f"no remote points to {owner}/{repo}")
    return failures


def normalize_remote(remote: str) -> str:
    text = remote.strip().lower()
    if text.endswith(".git"):
        text = text[:-4]
    return text


def risky_tracked_paths(paths: list[str]) -> list[str]:
    risky: list[str] = []
    for path in paths:
        path_obj = Path(path)
        lower_path = path.lower()
        lower_name = path_obj.name.lower()
        if lower_path in ALLOWED_TRACKED_REPORTS:
            continue
        if lower_path.startswith("reports/"):
            risky.append(path)
            continue
        if lower_path.startswith(("data/raw/", "data/processed/", "data/cache/")):
            risky.append(path)
            continue
        if lower_name == ".env" or lower_name.startswith(".env."):
            risky.append(path)
            continue
        if path_obj.suffix.lower() in RISKY_SUFFIXES:
            risky.append(path)
            continue
        if any(part in lower_name for part in RISKY_PATH_NAME_PARTS):
            risky.append(path)
    return risky


def scan_tracked_for_forbidden_account(root: Path, paths: list[str]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        text = read_text(root / path)
        if text is None:
            continue
        found = forbidden_hits(text)
        if found:
            hits.append(f"{path}:{','.join(sorted(found))}")
    return hits


def scan_tracked_for_secret_patterns(root: Path, paths: list[str]) -> list[TextFinding]:
    hits: list[TextFinding] = []
    for path in paths:
        text = read_text(root / path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for kind, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    hits.append(TextFinding(path=path, line=line_number, kind=kind))
    return hits


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data:
        return None
    return data.decode("utf-8", errors="ignore")


def format_finding(finding: TextFinding) -> str:
    return f"{finding.path}:{finding.line}:{finding.kind}"


if __name__ == "__main__":
    raise SystemExit(main())
