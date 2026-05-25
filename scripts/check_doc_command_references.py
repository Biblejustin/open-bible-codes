#!/usr/bin/env python3
"""Validate documented command and source-file references still exist."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SCRIPT_MODULE_RE = re.compile(r"python3\s+-m\s+scripts\.([A-Za-z0-9_]+)")
PROTOCOL_RE = re.compile(r"protocols/[A-Za-z0-9_./\[\]{}-]+\.toml")
CONFIG_RE = re.compile(r"(?<![A-Za-z0-9_./-])configs/[A-Za-z0-9_./\[\]{}-]+\.toml")
TERM_RE = re.compile(r"(?<![A-Za-z0-9_./-])terms/[A-Za-z0-9_./\[\]{}-]+\.csv")
CLAIM_CSV_RE = re.compile(r"(?<![A-Za-z0-9_./-])claims/[A-Za-z0-9_./\[\]{}-]+\.csv")
MAPPING_CSV_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])data/study/mappings/[A-Za-z0-9_./\[\]{}-]+\.csv"
)
TREAT_AS_DELETED_CSV_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])protocols/treat_as_deleted/[A-Za-z0-9_./\[\]{}-]+\.csv"
)
REPORT_RE = re.compile(r"(?<![A-Za-z0-9_./-])reports/[A-Za-z0-9_./\[\]{}-]+\.(?:csv|json|md)")
DEFAULT_DOCS = (Path("README.md"), Path("docs"))
MISSING_REPORT_CONTEXT_MARKERS = (
    "example",
    "future",
    "generated",
    "ignored",
    "local",
    "new_prospective",
    "output",
    "outputs",
    "placeholder",
    "prior",
    "study.",
    "study_name",
    "such as",
    "template",
)


@dataclass(frozen=True)
class ExistingPathRule:
    regex: re.Pattern[str]
    label: str


EXISTING_PATH_RULES = (
    ExistingPathRule(PROTOCOL_RE, "protocol"),
    ExistingPathRule(CONFIG_RE, "config"),
    ExistingPathRule(TERM_RE, "term file"),
    ExistingPathRule(CLAIM_CSV_RE, "claim file"),
    ExistingPathRule(MAPPING_CSV_RE, "mapping file"),
    ExistingPathRule(TREAT_AS_DELETED_CSV_RE, "treat-as-deleted file"),
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_doc_command_references(args.root, args.doc)
    if failures:
        for failure in failures:
            print(f"doc command reference failure: {failure}", file=sys.stderr)
        return 1
    print(f"doc command references ok: {args.root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--doc",
        action="append",
        type=Path,
        default=[],
        help="Doc file or directory to scan. Defaults to README.md and docs/.",
    )
    return parser


def validate_doc_command_references(root: Path = Path("."), docs: list[Path] | None = None) -> list[str]:
    failures: list[str] = []
    for doc in iter_doc_paths(root, docs or list(DEFAULT_DOCS)):
        text = doc.read_text(encoding="utf-8")
        lines = text.splitlines()
        fenced_lines = fenced_code_lines(lines)
        relative_doc = doc.relative_to(root)
        for match in SCRIPT_MODULE_RE.finditer(text):
            module_name = match.group(1)
            module_path = root / "scripts" / f"{module_name}.py"
            if not module_path.exists():
                line = line_number(text, match.start())
                failures.append(
                    f"{relative_doc}:{line}: missing script module scripts.{module_name}"
                )
        failures.extend(validate_existing_path_rules(root, relative_doc, text))
        for match in REPORT_RE.finditer(text):
            report = match.group(0)
            if is_placeholder(report):
                continue
            report_path = root / report
            if report_path.exists():
                continue
            line = line_number(text, match.start())
            if line in fenced_lines:
                continue
            context = surrounding_text(lines, line).replace(report, "").lower()
            if any(marker in context for marker in MISSING_REPORT_CONTEXT_MARKERS):
                continue
            failures.append(f"{relative_doc}:{line}: unmarked missing report output {report}")
    return failures


def validate_existing_path_rules(root: Path, relative_doc: Path, text: str) -> list[str]:
    failures: list[str] = []
    for rule in EXISTING_PATH_RULES:
        for match in rule.regex.finditer(text):
            reference = match.group(0)
            if is_placeholder(reference):
                continue
            if (root / reference).exists():
                continue
            line = line_number(text, match.start())
            failures.append(f"{relative_doc}:{line}: missing {rule.label} {reference}")
    return failures


def iter_doc_paths(root: Path, docs: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for doc in docs:
        path = root / doc
        if not path.exists():
            continue
        if path.is_dir():
            paths.extend(sorted(path.glob("*.md")))
        else:
            paths.append(path)
    return paths


def is_placeholder(value: str) -> bool:
    return any(marker in value for marker in ("[", "]", "{", "}"))


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def fenced_code_lines(lines: list[str]) -> set[int]:
    inside = False
    fenced: set[int] = set()
    for index, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            inside = not inside
            fenced.add(index)
            continue
        if inside:
            fenced.add(index)
    return fenced


def surrounding_text(lines: list[str], line_number_: int, *, radius: int = 2) -> str:
    start = max(0, line_number_ - radius - 1)
    end = min(len(lines), line_number_ + radius)
    return " ".join(lines[start:end])


if __name__ == "__main__":
    raise SystemExit(main())
