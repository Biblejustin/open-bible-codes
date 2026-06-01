#!/usr/bin/env python3
"""Validate a generated public-reader package against its manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_public_reader_package as builder


DEFAULT_PACKAGE_DIR = builder.DEFAULT_OUT_DIR
REQUIRED_GENERATED_FILES = (
    Path("README.md"),
    Path("package_manifest.json"),
    Path("reader_package.md"),
)
REAL_REPORT_SUMMARY_SOURCE = Path("reports/real_report_run/summary.md")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_public_reader_package(args.package_dir)
    if failures:
        for failure in failures:
            print(f"public-reader package failure: {failure}", file=sys.stderr)
        return 1
    print(f"public-reader package ok: {args.package_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", type=Path, default=DEFAULT_PACKAGE_DIR)
    return parser


def validate_public_reader_package(
    package_dir: Path = DEFAULT_PACKAGE_DIR,
) -> list[str]:
    failures: list[str] = []
    if not package_dir.exists():
        return [f"{package_dir} is missing"]
    if package_dir.is_symlink():
        failures.append(f"{package_dir} is a symlink")
    if not package_dir.is_dir():
        failures.append(f"{package_dir} is not a directory")
        return failures

    for generated in REQUIRED_GENERATED_FILES:
        path = package_dir / generated
        if not path.exists():
            failures.append(f"{path} is missing")
        elif path.is_symlink():
            failures.append(f"{path} is a symlink")
        elif not path.is_file():
            failures.append(f"{path} is not a file")

    manifest_path = package_dir / "package_manifest.json"
    if not manifest_path.exists() or not manifest_path.is_file():
        return failures

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"{manifest_path} is invalid JSON: {exc}")
        return failures

    failures.extend(validate_manifest_metadata(manifest, package_dir))
    failures.extend(validate_manifest_files(manifest, package_dir))
    failures.extend(validate_packaged_real_report_summary(manifest, package_dir))
    failures.extend(validate_generated_package_readme(manifest, package_dir))
    failures.extend(validate_generated_reader_package(manifest, package_dir))
    failures.extend(validate_no_unmanifested_files(manifest, package_dir))
    return failures


def validate_manifest_metadata(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    failures: list[str] = []
    current_git_head = builder.git_head()
    if manifest.get("git_head") != current_git_head:
        failures.append(
            f"{package_dir}/package_manifest.json git_head drifted: "
            f"{manifest.get('git_head')} != {current_git_head}"
        )
    if "no raw source texts" not in str(manifest.get("package_boundary", "")):
        failures.append(f"{package_dir}/package_manifest.json missing package boundary")
    if "validated before packaging" not in str(manifest.get("reader_path_guard", "")):
        failures.append(f"{package_dir}/package_manifest.json missing reader guard")
    if manifest.get("package_start_paths") != [
        path.as_posix() for path in builder.PACKAGE_START_PATHS
    ]:
        failures.append(f"{package_dir}/package_manifest.json package start paths drifted")
    expected_reader_sources = {
        "full_doc": [path.as_posix() for path in builder.READER_LINK_SOURCE_PATHS],
        "marked_sections": {
            path.as_posix(): marker
            for path, marker in builder.READER_LINK_SECTION_MARKERS.items()
        },
    }
    if manifest.get("reader_link_sources") != expected_reader_sources:
        failures.append(f"{package_dir}/package_manifest.json reader-link sources drifted")
    files = manifest.get("files")
    if not isinstance(files, list):
        failures.append(f"{package_dir}/package_manifest.json files must be a list")
    elif manifest.get("file_count") != len(files):
        failures.append(
            f"{package_dir}/package_manifest.json file_count drifted: "
            f"{manifest.get('file_count')} != {len(files)}"
        )
    return failures


def validate_manifest_files(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    failures: list[str] = []
    files = manifest.get("files")
    if not isinstance(files, list):
        return failures
    seen_sources: set[str] = set()
    seen_package_paths: set[str] = set()
    for index, item in enumerate(files):
        if not isinstance(item, dict):
            failures.append(f"manifest file row {index} is not an object")
            continue
        source = str(item.get("source", ""))
        package_path_text = str(item.get("package_path", ""))
        failures.extend(validate_manifest_file_row_shape(index, item))
        failures.extend(validate_manifest_source_path(source))
        if source in seen_sources:
            failures.append(f"duplicate manifest source: {source}")
        seen_sources.add(source)
        if package_path_text in seen_package_paths:
            failures.append(f"duplicate manifest package path: {package_path_text}")
        seen_package_paths.add(package_path_text)
        if not package_path_text:
            continue
        package_path = Path(package_path_text)
        if package_path.is_absolute() or ".." in package_path.parts:
            failures.append(f"unsafe manifest package path: {package_path_text}")
            continue
        failures.extend(validate_manifest_package_mapping(source, package_path_text))
        path = package_dir / package_path
        failures.extend(validate_packaged_file(path, item))
    source_set = {str(item.get("source", "")) for item in files if isinstance(item, dict)}
    for path in builder.PACKAGE_START_PATHS:
        if path.as_posix() not in source_set:
            failures.append(f"package start source missing from manifest: {path}")
    for source in required_manifest_sources():
        if source not in source_set:
            failures.append(f"required package source missing from manifest: {source}")
    return failures


def required_manifest_sources() -> list[str]:
    paths = [*builder.DEFAULT_DOC_PATHS]
    paths.extend(path for path in builder.DEFAULT_REPORT_PATHS if path.exists())
    return sorted(path.as_posix() for path in paths)


def validate_manifest_package_mapping(
    source: str,
    package_path_text: str,
) -> list[str]:
    source_path = Path(source)
    if source_path.is_absolute() or ".." in source_path.parts:
        return []
    expected = builder.SOURCE_PACKAGE_PATH_OVERRIDES.get(source_path, source_path)
    if package_path_text != expected.as_posix():
        return [
            "manifest package path does not match source mapping: "
            f"{source} -> {package_path_text} (expected {expected.as_posix()})"
        ]
    return []


def validate_no_unmanifested_files(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    files = manifest.get("files")
    if not isinstance(files, list):
        return []
    expected = {path.as_posix() for path in REQUIRED_GENERATED_FILES}
    for item in files:
        if isinstance(item, dict):
            package_path = item.get("package_path")
            if isinstance(package_path, str):
                expected.add(package_path)
    failures: list[str] = []
    for path in package_dir.rglob("*"):
        if path.is_dir() and not path.is_symlink():
            continue
        relative = path.relative_to(package_dir).as_posix()
        if relative not in expected:
            failures.append(f"unexpected package file: {relative}")
    return failures


def validate_packaged_real_report_summary(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    git_head = manifest.get("git_head")
    if not isinstance(git_head, str) or not git_head:
        return []
    files = manifest.get("files")
    if not isinstance(files, list):
        return []
    for item in files:
        if not isinstance(item, dict):
            continue
        if item.get("source") != REAL_REPORT_SUMMARY_SOURCE.as_posix():
            continue
        package_path_text = item.get("package_path")
        if not isinstance(package_path_text, str):
            return []
        package_path = Path(package_path_text)
        if package_path.is_absolute() or ".." in package_path.parts:
            return []
        path = package_dir / package_path
        if not path.exists() or path.is_symlink() or not path.is_file():
            return []
        expected = f"Commit: `{git_head[:7]}`"
        if expected not in path.read_text(encoding="utf-8"):
            return [f"{path} commit stamp drifted: expected {expected}"]
        return []
    return []


def validate_generated_package_readme(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    readme = package_dir / "README.md"
    if not readme.exists() or readme.is_symlink() or not readme.is_file():
        return []
    actual = readme.read_text(encoding="utf-8")
    expected = expected_package_readme_text(manifest)
    if actual != expected:
        return [f"{readme} content drifted from manifest"]
    return []


def expected_package_readme_text(manifest: dict[str, Any]) -> str:
    lines = [
        "# Public Reader Package",
        "",
        "Status: generated package over whitelisted docs and formal report summary.",
        "Reader-path guard: project findings overview, package start paths, and configured reader-link sources validated before packaging.",
        "It contains no raw Bible source files and no local database artifacts.",
        "",
        "Start with:",
        "",
        *[
            f"{index}. `{path.as_posix()}`"
            for index, path in enumerate(builder.PACKAGE_START_PATHS, start=1)
        ],
        "",
        "Package files:",
        "",
        "| Source | Package path | Bytes | SHA-256 |",
        "| --- | --- | ---: | --- |",
    ]
    files = manifest.get("files")
    if isinstance(files, list):
        for item in files:
            if not isinstance(item, dict):
                continue
            lines.append(
                f"| `{item.get('source', '')}` | `{item.get('package_path', '')}` | "
                f"{item.get('bytes', '')} | `{item.get('sha256', '')}` |"
            )
    return "\n".join(lines).rstrip() + "\n"


def validate_generated_reader_package(
    manifest: dict[str, Any],
    package_dir: Path,
) -> list[str]:
    reader_package = package_dir / "reader_package.md"
    if (
        not reader_package.exists()
        or reader_package.is_symlink()
        or not reader_package.is_file()
    ):
        return []
    failures: list[str] = []
    expected = expected_reader_package_text(manifest, package_dir, failures)
    if failures:
        return failures
    actual = reader_package.read_text(encoding="utf-8")
    if actual != expected:
        failures.append(f"{reader_package} content drifted from package files")
    return failures


def expected_reader_package_text(
    manifest: dict[str, Any],
    package_dir: Path,
    failures: list[str],
) -> str:
    lines = [
        "# Public Reader Package",
        "",
        "This concatenates the reader-path docs and formal report summary.",
        "",
    ]
    files = manifest.get("files")
    if not isinstance(files, list):
        return "\n".join(lines).rstrip() + "\n"
    for item in files:
        if not isinstance(item, dict):
            continue
        source = str(item.get("source", ""))
        package_path_text = str(item.get("package_path", ""))
        if not package_path_text.endswith(".md"):
            continue
        package_path = Path(package_path_text)
        if package_path.is_absolute() or ".." in package_path.parts:
            continue
        path = package_dir / package_path
        if path.is_symlink() or not path.exists() or not path.is_file():
            failures.append(f"cannot validate reader package source section: {path}")
            continue
        lines.extend(
            [
                "",
                "---",
                "",
                f"Source: `{source}`",
                "",
                path.read_text(encoding="utf-8").rstrip(),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def validate_manifest_file_row_shape(
    index: int,
    item: dict[str, Any],
) -> list[str]:
    failures: list[str] = []
    for key in ("source", "package_path", "bytes", "sha256"):
        if key not in item:
            failures.append(f"manifest file row {index} missing {key}")
    if "sha256" in item and not is_hex_sha256(str(item["sha256"])):
        failures.append(f"manifest file row {index} has invalid sha256")
    if "bytes" in item and not isinstance(item["bytes"], int):
        failures.append(f"manifest file row {index} bytes must be an integer")
    return failures


def validate_manifest_source_path(source: str) -> list[str]:
    if not source:
        return ["manifest file row has empty source"]
    path = Path(source)
    failures: list[str] = []
    if path.is_absolute() or ".." in path.parts:
        failures.append(f"unsafe manifest source path: {source}")
    if path.suffix.lower() not in {".md", ".json"}:
        failures.append(f"unsupported manifest source suffix: {source}")
    if builder.is_forbidden_source(path):
        failures.append(f"forbidden manifest source path: {source}")
    return failures


def validate_packaged_file(path: Path, item: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"{path} is missing"]
    if path.is_symlink():
        failures.append(f"{path} is a symlink")
    if not path.is_file():
        failures.append(f"{path} is not a file")
        return failures
    data = path.read_bytes()
    if item.get("bytes") != len(data):
        failures.append(f"{path} byte count drifted")
    digest = hashlib.sha256(data).hexdigest()
    if item.get("sha256") != digest:
        failures.append(f"{path} sha256 drifted")
    return failures


def is_hex_sha256(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


if __name__ == "__main__":
    raise SystemExit(main())
