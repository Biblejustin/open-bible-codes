"""Shared public-release hygiene helpers."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


FORBIDDEN_ACCOUNT_PART = "sp" + "lunk"
FORBIDDEN_ACCOUNT_TERMS = ("justin-" + FORBIDDEN_ACCOUNT_PART, FORBIDDEN_ACCOUNT_PART)
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


def forbidden_hits(text: str) -> set[str]:
    lowered = text.lower()
    return {term for term in FORBIDDEN_ACCOUNT_TERMS if term in lowered}


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


def remote_owner_failures(remotes: list[str], *, owner: str = DEFAULT_OWNER, repo: str = DEFAULT_REPO) -> list[str]:
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
