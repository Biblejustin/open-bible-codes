import json
import re
from pathlib import Path

import pytest

from scripts import build_public_reader_package as package
from scripts import check_project_findings_overview_doc as overview_check


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _default_doc_text(path: Path) -> str:
    if path == overview_check.DEFAULT_DOC:
        lines = ["# Open Bible Codes Findings Overview", ""]
        lines.extend(overview_check.REQUIRED_HEADINGS)
        lines.extend(overview_check.REQUIRED_PHRASES)
        lines.extend(f"`{reference}`" for reference in overview_check.REQUIRED_REFERENCES)
        return "\n\n".join(lines) + "\n"
    if path == overview_check.DEFAULT_README:
        return (
            "# README\n\n"
            "whole-project findings overview: `docs/PROJECT_FINDINGS_OVERVIEW.md`\n"
        )
    if path == overview_check.DEFAULT_START_HERE:
        return (
            "# Start Here\n\n"
            "1. `docs/PROJECT_FINDINGS_OVERVIEW.md` for the whole-project findings summary.\n\n"
            "no current row should be presented as a public claim\n"
        )
    return f"# {path.name}\n\nbody\n"


def test_builds_reader_package_from_whitelisted_docs(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")

    copied = package.build_public_reader_package(out_dir=Path("reports/public_reader_package"))

    manifest = json.loads(
        Path("reports/public_reader_package/package_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(copied) == len(package.DEFAULT_DOC_PATHS) + len(package.DEFAULT_REPORT_PATHS)
    assert manifest["file_count"] == len(copied)
    assert manifest["package_boundary"].startswith("whitelisted docs")
    assert manifest["reader_path_guard"].startswith("project findings overview")
    assert Path("reports/public_reader_package/docs/START_HERE.md").exists()
    assert Path("reports/public_reader_package/docs/PROJECT_FINDINGS_OVERVIEW.md").exists()
    assert Path("reports/public_reader_package/docs/WRR_NO_INPUT_HANDOFF_STATUS.md").exists()
    assert Path("reports/public_reader_package/docs/KJVA_NO_INPUT_HANDOFF_STATUS.md").exists()
    assert Path("reports/public_reader_package/docs/CITIES_NO_INPUT_HANDOFF_STATUS.md").exists()
    assert Path("reports/public_reader_package/docs/STRONGEST_CANDIDATE_DEEP_DIVE.md").exists()
    assert Path("reports/public_reader_package/docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md").exists()
    assert Path("reports/public_reader_package/reader_package.md").exists()
    reader_package = Path(
        "reports/public_reader_package/reader_package.md"
    ).read_text(encoding="utf-8")
    assert "Source: `docs/START_HERE.md`" in reader_package
    assert "Source: `docs/PROJECT_FINDINGS_OVERVIEW.md`" in reader_package
    package_readme = Path("reports/public_reader_package/README.md").read_text(
        encoding="utf-8"
    )
    assert "Reader-path guard: project findings overview" in package_readme
    assert "7. `docs/WRR_NO_INPUT_HANDOFF_STATUS.md`" in package_readme
    assert "8. `docs/KJVA_NO_INPUT_HANDOFF_STATUS.md`" in package_readme
    assert "9. `docs/CITIES_NO_INPUT_HANDOFF_STATUS.md`" in package_readme


def test_reader_package_includes_project_findings_references() -> None:
    package_docs = set(package.DEFAULT_DOC_PATHS)
    for reference in overview_check.REQUIRED_REFERENCES:
        assert Path(reference) in package_docs


def test_reader_package_includes_no_input_handoff_references() -> None:
    package_docs = set(package.DEFAULT_DOC_PATHS)
    reader_sources = (
        Path("README.md"),
        Path("docs/PROJECT_FINDINGS_OVERVIEW.md"),
        Path("docs/FINAL_REPORT.md"),
        Path("docs/REAL_REPORT_RUN.md"),
    )
    for source in reader_sources:
        text = source.read_text(encoding="utf-8")
        for reference in sorted(set(re.findall(r"`(docs/[^`]*NO_INPUT_HANDOFF[^`]*\.md)`", text))):
            assert Path(reference) in package_docs


def test_reader_package_includes_start_here_references() -> None:
    package_paths = set(package.DEFAULT_DOC_PATHS) | set(package.DEFAULT_REPORT_PATHS)
    text = Path("docs/START_HERE.md").read_text(encoding="utf-8")
    references = sorted(set(package.PACKAGED_READER_LINK_RE.findall(text)))
    assert references
    for reference in references:
        assert Path(reference) in package_paths


def test_refuses_stale_project_findings_overview(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    _write(overview_check.DEFAULT_DOC, "# Broken Overview\n\nbody\n")

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(out_dir=Path("reports/public_reader_package"))

    assert "reader package input validation failed" in str(excinfo.value)
    assert "missing heading: ## Short Answer" in str(excinfo.value)


def test_refuses_unpackaged_start_here_reference(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")
    _write(
        overview_check.DEFAULT_START_HERE,
        "# Start Here\n\n"
        "1. `docs/PROJECT_FINDINGS_OVERVIEW.md` for the whole-project findings summary.\n"
        "2. `docs/NOT_IN_PACKAGE.md` for a missing package doc.\n\n"
        "no current row should be presented as a public claim\n",
    )

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(out_dir=Path("reports/public_reader_package"))

    assert "reader package input validation failed" in str(excinfo.value)
    assert (
        "docs/START_HERE.md references docs/NOT_IN_PACKAGE.md "
        "but package does not include it"
    ) in str(excinfo.value)


def test_refuses_raw_source_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _write(Path("data/raw/private.txt"), "raw\n")

    with pytest.raises(ValueError):
        package.copy_checked_file(
            Path("data/raw/private.txt"),
            Path("reports/public_reader_package/data/raw/private.txt"),
        )
