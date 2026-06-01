#!/usr/bin/env python3
"""Build an ignored public-reader package from whitelisted docs only."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from scripts import check_project_findings_overview_doc


DEFAULT_OUT_DIR = Path("reports/public_reader_package")
DEFAULT_DOC_PATHS = (
    Path("README.md"),
    Path("docs/START_HERE.md"),
    Path("docs/PROJECT_FINDINGS_OVERVIEW.md"),
    Path("docs/FINAL_REPORT.md"),
    Path("docs/FINAL_REPORT_HIGHLIGHTS.md"),
    Path("docs/CLAIM_CATALOG.md"),
    Path("docs/CONSOLIDATED_FINDINGS.md"),
    Path("docs/STRONGEST_CANDIDATE_DEEP_DIVE.md"),
    Path("docs/REAL_REPORT_RUN.md"),
    Path("docs/REMAINING_WORK_REGISTER.md"),
    Path("docs/WRR_NO_INPUT_HANDOFF_STATUS.md"),
    Path("docs/KJVA_NO_INPUT_HANDOFF_STATUS.md"),
    Path("docs/CITIES_NO_INPUT_HANDOFF_STATUS.md"),
    Path("docs/PROSPECTIVE_STUDY_READINESS.md"),
    Path("docs/WRR_LOCKED_METHOD_REPORT.md"),
    Path("docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md"),
    Path("docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md"),
    Path("docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md"),
    Path("docs/CRITICAL_OMISSION_BREAKS_NULL.md"),
)
DEFAULT_REPORT_PATHS = (
    Path("reports/real_report_run/summary.md"),
    Path("reports/real_report_run/preflight.json"),
    Path("reports/real_report_run/manifest.json"),
    Path("reports/real_report_run/protocol_run.manifest.json"),
)
PACKAGE_START_PATHS = (
    Path("docs/START_HERE.md"),
    Path("docs/PROJECT_FINDINGS_OVERVIEW.md"),
    Path("docs/FINAL_REPORT.md"),
    Path("docs/FINAL_REPORT_HIGHLIGHTS.md"),
    Path("docs/CLAIM_CATALOG.md"),
    Path("docs/CONSOLIDATED_FINDINGS.md"),
    Path("docs/REAL_REPORT_RUN.md"),
    Path("docs/REMAINING_WORK_REGISTER.md"),
    Path("docs/STRONGEST_CANDIDATE_DEEP_DIVE.md"),
    Path("docs/WRR_NO_INPUT_HANDOFF_STATUS.md"),
    Path("docs/KJVA_NO_INPUT_HANDOFF_STATUS.md"),
    Path("docs/CITIES_NO_INPUT_HANDOFF_STATUS.md"),
    Path("reports/real_report_run/summary.md"),
)
READER_LINK_SOURCE_PATHS = (Path("docs/START_HERE.md"),)
READER_LINK_SECTION_MARKERS = {
    Path("README.md"): "Reader path:",
}
PACKAGED_READER_LINK_RE = re.compile(r"`((?:docs|reports)/[^`]+\.md)`")


@dataclass(frozen=True)
class CopiedFile:
    source: Path
    package_path: Path
    bytes: int
    sha256: str


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    build_public_reader_package(
        out_dir=args.out_dir,
        clean=not args.no_clean,
        extra_docs=args.extra_doc,
    )
    print(args.out_dir / "README.md")
    print(args.out_dir / "package_manifest.json")
    print(args.out_dir / "reader_package.md")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove the existing output directory before writing.",
    )
    parser.add_argument(
        "--extra-doc",
        type=Path,
        action="append",
        default=[],
        help="Additional tracked markdown doc to include.",
    )
    return parser


def build_public_reader_package(
    *,
    out_dir: Path = DEFAULT_OUT_DIR,
    clean: bool = True,
    extra_docs: list[Path] | None = None,
) -> list[CopiedFile]:
    if clean and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc_paths = [*DEFAULT_DOC_PATHS, *(extra_docs or [])]
    report_paths = [path for path in DEFAULT_REPORT_PATHS if path.exists()]
    validate_reader_package_inputs(doc_paths, report_paths)
    copied: list[CopiedFile] = []
    for source in doc_paths:
        copied.append(copy_checked_file(source, out_dir / source))
    for source in report_paths:
        copied.append(copy_checked_file(source, out_dir / source))

    write_package_readme(out_dir, copied)
    write_reader_package(out_dir, doc_paths, report_paths)
    write_manifest(out_dir, copied)
    return copied


def validate_reader_package_inputs(
    doc_paths: list[Path],
    report_paths: list[Path] | None = None,
) -> None:
    doc_set = set(doc_paths)
    report_set = set(report_paths or [])
    failures: list[str] = []
    overview_inputs = {
        check_project_findings_overview_doc.DEFAULT_DOC,
        check_project_findings_overview_doc.DEFAULT_README,
        check_project_findings_overview_doc.DEFAULT_START_HERE,
    }
    if overview_inputs.issubset(doc_set):
        failures.extend(
            check_project_findings_overview_doc.validate_project_findings_overview()
        )
    failures.extend(validate_packaged_reader_links(doc_set | report_set))
    if failures:
        raise ValueError(
            "reader package input validation failed: " + "; ".join(failures)
        )


def validate_packaged_reader_links(package_paths: set[Path]) -> list[str]:
    failures: list[str] = []
    for source in READER_LINK_SOURCE_PATHS:
        if source not in package_paths:
            continue
        if not source.exists():
            failures.append(f"{source} is missing")
            continue
        text = source.read_text(encoding="utf-8")
        references = sorted(set(PACKAGED_READER_LINK_RE.findall(text)))
        for reference in references:
            if Path(reference) not in package_paths:
                failures.append(
                    f"{source} references {reference} but package does not include it"
                )
    for source, marker in READER_LINK_SECTION_MARKERS.items():
        if source not in package_paths:
            continue
        if not source.exists():
            failures.append(f"{source} is missing")
            continue
        section = extract_marked_section(source.read_text(encoding="utf-8"), marker)
        references = sorted(set(PACKAGED_READER_LINK_RE.findall(section)))
        for reference in references:
            if Path(reference) not in package_paths:
                failures.append(
                    f"{source} reader path references {reference} "
                    "but package does not include it"
                )
    return failures


def extract_marked_section(text: str, marker: str) -> str:
    _, found, remainder = text.partition(marker)
    if not found:
        return ""
    section_lines: list[str] = []
    for line in remainder.splitlines():
        if not line.strip():
            if section_lines:
                break
            continue
        section_lines.append(line)
    return "\n".join(section_lines)


def copy_checked_file(source: Path, destination: Path) -> CopiedFile:
    if not source.exists():
        raise FileNotFoundError(f"missing package source: {source}")
    if is_forbidden_source(source):
        raise ValueError(f"refusing to package raw/source data path: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    data = destination.read_bytes()
    return CopiedFile(
        source=source,
        package_path=destination,
        bytes=len(data),
        sha256=hashlib.sha256(data).hexdigest(),
    )


def is_forbidden_source(path: Path) -> bool:
    parts = path.parts
    if parts[:2] in (("data", "raw"), ("data", "processed"), ("data", "private")):
        return True
    if path.suffix.lower() in {".csv", ".tsv", ".duckdb", ".pdf", ".epub", ".zip"}:
        return True
    return False


def write_package_readme(out_dir: Path, copied: list[CopiedFile]) -> None:
    lines = [
        "# Public Reader Package",
        "",
        "Status: generated package over whitelisted docs and formal report summary.",
        "Reader-path guard: project findings overview and reader links validated before packaging.",
        "It contains no raw Bible source files and no local database artifacts.",
        "",
        "Start with:",
        "",
        *[
            f"{index}. `{path.as_posix()}`"
            for index, path in enumerate(PACKAGE_START_PATHS, start=1)
        ],
        "",
        "Package files:",
        "",
        "| Source | Package path | Bytes | SHA-256 |",
        "| --- | --- | ---: | --- |",
    ]
    for item in copied:
        relative = item.package_path.relative_to(out_dir)
        lines.append(
            f"| `{item.source.as_posix()}` | `{relative.as_posix()}` | "
            f"{item.bytes} | `{item.sha256}` |"
        )
    (out_dir / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_reader_package(
    out_dir: Path,
    doc_paths: list[Path],
    report_paths: list[Path],
) -> None:
    lines = [
        "# Public Reader Package",
        "",
        "This concatenates the reader-path docs and formal report summary.",
        "",
    ]
    for source in [*doc_paths, *report_paths]:
        packaged = out_dir / source
        if not packaged.exists() or packaged.suffix != ".md":
            continue
        lines.extend(
            [
                "",
                "---",
                "",
                f"Source: `{source.as_posix()}`",
                "",
                packaged.read_text(encoding="utf-8").rstrip(),
                "",
            ]
        )
    (out_dir / "reader_package.md").write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
    )


def write_manifest(out_dir: Path, copied: list[CopiedFile]) -> None:
    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "git_head": git_head(),
        "package_boundary": "whitelisted docs and formal report summary only; no raw source texts",
        "reader_path_guard": (
            "project findings overview and README/START_HERE reader links validated before packaging"
        ),
        "file_count": len(copied),
        "files": [
            {
                "source": item.source.as_posix(),
                "package_path": item.package_path.relative_to(out_dir).as_posix(),
                "bytes": item.bytes,
                "sha256": item.sha256,
            }
            for item in copied
        ],
    }
    (out_dir / "package_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
