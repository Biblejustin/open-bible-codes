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
            "whole-project findings overview: `docs/PROJECT_FINDINGS_OVERVIEW.md`\n\n"
            "Reader path:\n\n"
            "- start here: `docs/START_HERE.md`\n"
            "- whole-project findings overview: `docs/PROJECT_FINDINGS_OVERVIEW.md`\n"
        )
    if path == overview_check.DEFAULT_START_HERE:
        return (
            "# Start Here\n\n"
            + "\n".join(overview_check.READER_PATH_REQUIREMENTS[path])
            + "\n"
        )
    if path == Path("docs/FINAL_REPORT.md"):
        return (
            "# Final Report\n\n"
            "## Reader Path\n\n"
            "Read `docs/START_HERE.md`, then `docs/PROJECT_FINDINGS_OVERVIEW.md`.\n"
        )
    if path == Path("docs/REAL_REPORT_RUN.md"):
        return (
            "# Real Report Run\n\n"
            "Reader role: use `docs/START_HERE.md` and `docs/FINAL_REPORT.md`.\n"
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
    assert manifest["package_start_paths"] == [
        path.as_posix() for path in package.PACKAGE_START_PATHS
    ]
    assert manifest["reader_link_sources"]["full_doc"] == [
        path.as_posix() for path in package.READER_LINK_SOURCE_PATHS
    ]
    assert manifest["reader_link_sources"]["marked_sections"] == {
        path.as_posix(): marker
        for path, marker in package.READER_LINK_SECTION_MARKERS.items()
    }
    assert Path("reports/public_reader_package/docs/START_HERE.md").exists()
    assert Path("reports/public_reader_package/docs/REPOSITORY_README.md").exists()
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
    assert "Source: `README.md`" in reader_package
    assert "Source: `docs/START_HERE.md`" in reader_package
    assert "Source: `docs/PROJECT_FINDINGS_OVERVIEW.md`" in reader_package
    package_readme = Path("reports/public_reader_package/README.md").read_text(
        encoding="utf-8"
    )
    assert "Reader-path guard: project findings overview, package start paths" in (
        package_readme
    )
    assert "`README.md` | `docs/REPOSITORY_README.md`" in package_readme
    for index, path in enumerate(package.PACKAGE_START_PATHS, start=1):
        assert f"{index}. `{path.as_posix()}`" in package_readme


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
        references = sorted(
            set(re.findall(r"`(docs/[^`]*NO_INPUT_HANDOFF[^`]*\.md)`", text))
        )
        for reference in references:
            assert Path(reference) in package_docs


def test_reader_package_start_paths_are_packaged() -> None:
    package_paths = set(package.DEFAULT_DOC_PATHS) | set(package.DEFAULT_REPORT_PATHS)
    for path in package.PACKAGE_START_PATHS:
        assert path in package_paths


def test_reader_package_includes_start_here_references() -> None:
    package_paths = set(package.DEFAULT_DOC_PATHS) | set(package.DEFAULT_REPORT_PATHS)
    text = Path("docs/START_HERE.md").read_text(encoding="utf-8")
    references = sorted(set(package.PACKAGED_READER_LINK_RE.findall(text)))
    assert references
    for reference in references:
        assert Path(reference) in package_paths


def test_reader_package_includes_readme_reader_path_references() -> None:
    package_paths = set(package.DEFAULT_DOC_PATHS) | set(package.DEFAULT_REPORT_PATHS)
    text = Path("README.md").read_text(encoding="utf-8")
    section = package.extract_marked_section(text, "Reader path:")
    references = sorted(set(package.PACKAGED_READER_LINK_RE.findall(section)))
    assert references
    for reference in references:
        assert Path(reference) in package_paths


def test_reader_package_includes_final_report_reader_path_references() -> None:
    package_paths = set(package.DEFAULT_DOC_PATHS) | set(package.DEFAULT_REPORT_PATHS)
    text = Path("docs/FINAL_REPORT.md").read_text(encoding="utf-8")
    section = package.extract_marked_section(text, "## Reader Path")
    references = sorted(set(package.PACKAGED_READER_LINK_RE.findall(section)))
    assert references
    for reference in references:
        assert Path(reference) in package_paths


def test_reader_package_includes_real_report_reader_role_references() -> None:
    package_paths = set(package.DEFAULT_DOC_PATHS) | set(package.DEFAULT_REPORT_PATHS)
    text = Path("docs/REAL_REPORT_RUN.md").read_text(encoding="utf-8")
    section = package.extract_marked_section(text, "Reader role:")
    references = sorted(set(package.PACKAGED_READER_LINK_RE.findall(section)))
    assert references
    for reference in references:
        assert Path(reference) in package_paths


def test_refuses_stale_project_findings_overview(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")
    _write(overview_check.DEFAULT_DOC, "# Broken Overview\n\nbody\n")

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(out_dir=Path("reports/public_reader_package"))

    assert "reader package input validation failed" in str(excinfo.value)
    assert "missing heading: ## Short Answer" in str(excinfo.value)


def test_refuses_missing_start_path_after_report_filtering(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(out_dir=Path("reports/public_reader_package"))

    assert "reader package input validation failed" in str(excinfo.value)
    assert (
        "package start path missing from inputs: reports/real_report_run/summary.md"
    ) in str(excinfo.value)


def test_refuses_duplicate_package_sources(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(
            out_dir=Path("reports/public_reader_package"),
            extra_docs=[Path("docs/START_HERE.md")],
        )

    assert "reader package input validation failed" in str(excinfo.value)
    assert "duplicate package source: docs/START_HERE.md" in str(excinfo.value)


def test_refuses_json_extra_doc_sources(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")
    _write(Path("docs/extra.json"), "{}\n")

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(
            out_dir=Path("reports/public_reader_package"),
            extra_docs=[Path("docs/extra.json")],
        )

    assert "reader package input validation failed" in str(excinfo.value)
    assert "doc package source must be markdown: docs/extra.json" in str(excinfo.value)


def test_refuses_untracked_extra_doc_sources(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")
    _write(Path("docs/extra.md"), "# Extra\n")
    monkeypatch.setattr(package, "is_inside_git_work_tree", lambda: True)
    monkeypatch.setattr(
        package,
        "is_git_tracked",
        lambda path: path in set(package.DEFAULT_DOC_PATHS),
    )

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(
            out_dir=Path("reports/public_reader_package"),
            extra_docs=[Path("docs/extra.md")],
        )

    assert "reader package input validation failed" in str(excinfo.value)
    assert "doc package source is not tracked by git: docs/extra.md" in str(
        excinfo.value
    )


def test_refuses_extra_docs_outside_reader_doc_locations(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")
    _write(Path("data/README.md"), "# Data Notes\n")
    monkeypatch.setattr(package, "is_inside_git_work_tree", lambda: True)
    monkeypatch.setattr(package, "is_git_tracked", lambda path: True)

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(
            out_dir=Path("reports/public_reader_package"),
            extra_docs=[Path("data/README.md")],
        )

    assert "reader package input validation failed" in str(excinfo.value)
    assert (
        "doc package source must be README.md or docs/*.md: data/README.md"
    ) in str(excinfo.value)


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
        "8. `docs/WRR_NO_INPUT_HANDOFF_STATUS.md` for exact WRR source/method status.\n"
        "9. `docs/KJVA_NO_INPUT_HANDOFF_STATUS.md` for KJVA source-lock status.\n"
        "10. `docs/CITIES_NO_INPUT_HANDOFF_STATUS.md` for Cities source-chain status.\n\n"
        "no current row should be presented as a public claim\n",
    )

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(out_dir=Path("reports/public_reader_package"))

    assert "reader package input validation failed" in str(excinfo.value)
    assert (
        "docs/START_HERE.md references docs/NOT_IN_PACKAGE.md "
        "but package does not include it"
    ) in str(excinfo.value)


def test_refuses_start_here_without_reader_links(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")
    _write(
        overview_check.DEFAULT_START_HERE,
        "# Start Here\n\n"
        "No package links here.\n\n"
        "no current row should be presented as a public claim\n",
    )

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(out_dir=Path("reports/public_reader_package"))

    assert "reader package input validation failed" in str(excinfo.value)
    assert "docs/START_HERE.md has no packaged reader links" in str(excinfo.value)


def test_refuses_unpackaged_readme_reader_path_reference(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")
    _write(
        overview_check.DEFAULT_README,
        "# README\n\n"
        "whole-project findings overview: `docs/PROJECT_FINDINGS_OVERVIEW.md`\n\n"
        "Reader path:\n\n"
        "- start here: `docs/START_HERE.md`\n"
        "- missing doc: `docs/NOT_IN_PACKAGE.md`\n\n"
        "Repository navigation:\n\n"
        "- documentation index: `docs/INDEX.md`\n",
    )

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(out_dir=Path("reports/public_reader_package"))

    assert "reader package input validation failed" in str(excinfo.value)
    assert (
        "README.md reader path references docs/NOT_IN_PACKAGE.md "
        "but package does not include it"
    ) in str(excinfo.value)


def test_refuses_missing_readme_reader_path_marker(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")
    _write(
        overview_check.DEFAULT_README,
        "# README\n\n"
        "whole-project findings overview: `docs/PROJECT_FINDINGS_OVERVIEW.md`\n",
    )

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(out_dir=Path("reports/public_reader_package"))

    assert "reader package input validation failed" in str(excinfo.value)
    assert "README.md missing reader path marker: Reader path:" in str(excinfo.value)


def test_refuses_readme_reader_path_without_links(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, "# report\n\nbody\n" if path.suffix == ".md" else "{}\n")
    _write(
        overview_check.DEFAULT_README,
        "# README\n\n"
        "whole-project findings overview: `docs/PROJECT_FINDINGS_OVERVIEW.md`\n\n"
        "Reader path:\n\n"
        "- no package links here\n",
    )

    with pytest.raises(ValueError) as excinfo:
        package.build_public_reader_package(out_dir=Path("reports/public_reader_package"))

    assert "reader package input validation failed" in str(excinfo.value)
    assert "README.md reader path section has no packaged links" in str(excinfo.value)


def test_refuses_raw_source_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _write(Path("data/raw/private.txt"), "raw\n")

    with pytest.raises(ValueError):
        package.copy_checked_file(
            Path("data/raw/private.txt"),
            Path("reports/public_reader_package/data/raw/private.txt"),
        )


def test_refuses_absolute_package_source_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    absolute = tmp_path / "docs" / "absolute.md"
    _write(absolute, "# Absolute\n")

    with pytest.raises(ValueError) as excinfo:
        package.copy_checked_file(
            absolute,
            Path("reports/public_reader_package/docs/absolute.md"),
        )

    assert "refusing absolute package source path" in str(excinfo.value)


def test_refuses_parent_segment_package_source_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _write(Path("outside.md"), "# Outside\n")

    with pytest.raises(ValueError) as excinfo:
        package.copy_checked_file(
            Path("../outside.md"),
            Path("reports/public_reader_package/outside.md"),
        )

    assert "refusing package source path with parent segment" in str(excinfo.value)


def test_refuses_unsupported_package_source_suffix(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _write(Path("docs/notes.txt"), "notes\n")

    with pytest.raises(ValueError) as excinfo:
        package.copy_checked_file(
            Path("docs/notes.txt"),
            Path("reports/public_reader_package/docs/notes.txt"),
        )

    assert "refusing unsupported package source suffix" in str(excinfo.value)


def test_refuses_symlink_package_source_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _write(Path("outside.md"), "# Outside\n")
    Path("docs").mkdir(parents=True, exist_ok=True)
    Path("docs/link.md").symlink_to(Path("../outside.md"))

    with pytest.raises(ValueError) as excinfo:
        package.copy_checked_file(
            Path("docs/link.md"),
            Path("reports/public_reader_package/docs/link.md"),
        )

    assert "refusing symlink package source: docs/link.md" in str(excinfo.value)


def test_refuses_non_file_package_source_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    Path("docs/fake.md").mkdir(parents=True, exist_ok=True)

    with pytest.raises(ValueError) as excinfo:
        package.copy_checked_file(
            Path("docs/fake.md"),
            Path("reports/public_reader_package/docs/fake.md"),
        )

    assert "refusing non-file package source: docs/fake.md" in str(excinfo.value)


def test_refuses_symlink_package_destination_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _write(Path("docs/source.md"), "# Source\n")
    _write(Path("outside.md"), "# Outside\n")
    destination = Path("reports/public_reader_package/docs/source.md")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.symlink_to(Path("../../../outside.md"))

    with pytest.raises(ValueError) as excinfo:
        package.copy_checked_file(Path("docs/source.md"), destination)

    assert "refusing symlink package destination:" in str(excinfo.value)


def test_refuses_symlink_package_destination_ancestors(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    _write(Path("docs/source.md"), "# Source\n")
    outside = tmp_path / "outside"
    outside.mkdir()
    package_root = Path("reports/public_reader_package")
    package_root.mkdir(parents=True)
    (package_root / "docs").symlink_to(outside, target_is_directory=True)

    with pytest.raises(ValueError) as excinfo:
        package.copy_checked_file(
            Path("docs/source.md"),
            package_root / "docs/source.md",
            package_root=package_root,
        )

    assert "refusing symlink package destination ancestor:" in str(excinfo.value)


def test_refuses_symlink_package_output_root(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _write(Path("docs/source.md"), "# Source\n")
    outside = tmp_path / "outside"
    outside.mkdir()
    package_root = Path("reports/public_reader_package")
    package_root.parent.mkdir(parents=True)
    package_root.symlink_to(outside, target_is_directory=True)

    with pytest.raises(ValueError) as excinfo:
        package.copy_checked_file(
            Path("docs/source.md"),
            package_root / "docs/source.md",
            package_root=package_root,
        )

    assert "refusing symlink package output root:" in str(excinfo.value)
