import json
from pathlib import Path

from scripts import build_public_reader_package as package
from scripts import check_project_findings_overview_doc as overview_check
from scripts import check_public_reader_package as check


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
            "Reader path:\n\n"
            "- start here: `docs/START_HERE.md`\n"
            + "\n".join(
                f"- {phrase}" for phrase in overview_check.READER_PATH_REQUIREMENTS[path]
            )
            + "\nreads 4 candidate-source audit rows with 0 verse-import-ready "
            "candidate pages and 0 result-ready candidate pages, records result "
            "allowed 0\n"
            + "\n"
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
            "Use `docs/REMAINING_WORK_REGISTER.md`, "
            "`docs/WRR_NO_INPUT_HANDOFF_STATUS.md`, "
            "`docs/KJVA_NO_INPUT_HANDOFF_STATUS.md`, and "
            "`docs/CITIES_NO_INPUT_HANDOFF_STATUS.md`.\n"
        )
    if path == Path("docs/REAL_REPORT_RUN.md"):
        return (
            "# Real Report Run\n\n"
            "Reader role: use `docs/START_HERE.md` and `docs/FINAL_REPORT.md`.\n"
            + "\n\n".join(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH[path])
            + "\n"
        )
    if path in check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH:
        return (
            f"# {path.name}\n\n"
            + "\n\n".join(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH[path])
            + "\n"
        )
    return f"# {path.name}\n\nbody\n"


def _default_report_text(path: Path) -> str:
    if path == Path("reports/real_report_run/summary.md"):
        return (
            "# report\n\n"
            + "\n\n".join(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH[path])
            + "\n"
        )
    if path.suffix == ".md":
        return "# report\n\nbody\n"
    return "{}\n"


def _build_package(root: Path, monkeypatch) -> Path:
    monkeypatch.chdir(root)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, _default_report_text(path))
    out_dir = Path("reports/public_reader_package")
    package.build_public_reader_package(out_dir=out_dir)
    return out_dir


def test_generated_public_reader_package_passes(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)

    assert check.validate_public_reader_package(out_dir) == []


def test_detects_manifest_hash_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    (out_dir / "docs/START_HERE.md").write_text("# changed\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert any("sha256 drifted" in failure for failure in failures)
    assert any("byte count drifted" in failure for failure in failures)


def test_detects_manifest_file_count_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["file_count"] = 999
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert any("file_count drifted" in failure for failure in failures)


def test_detects_manifest_git_head_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["git_head"] = "stale"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert any(
        "package_manifest.json git_head drifted: stale !=" in failure
        for failure in failures
    )


def test_detects_packaged_real_report_summary_commit_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    full_head = "abcdef0123456789abcdef0123456789abcdef01"
    monkeypatch.setattr(check.builder, "git_head", lambda: full_head)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["git_head"] = full_head
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{out_dir}/reports/real_report_run/summary.md commit stamp drifted: "
        "expected Commit: `abcdef0`"
    ) in failures


def test_detects_packaged_real_report_manifest_commit_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    full_head = "abcdef0123456789abcdef0123456789abcdef01"
    monkeypatch.setattr(check.builder, "git_head", lambda: full_head)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["git_head"] = full_head
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{out_dir}/reports/real_report_run/manifest.json commit stamp drifted: "
        "None != abcdef0"
    ) in failures


def test_detects_missing_required_manifest_source(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"] = [
        item
        for item in manifest["files"]
        if item["source"] != "docs/CLAIM_CATALOG.md"
    ]
    manifest["file_count"] = len(manifest["files"])
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert (
        "required package source missing from manifest: docs/CLAIM_CATALOG.md"
        in failures
    )


def test_detects_missing_required_packaged_phrase_for_each_guarded_doc(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    for relative_path, required_phrases in check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH.items():
        package_path = out_dir / relative_path
        original = package_path.read_text(encoding="utf-8")
        package_path.write_text("# stale\n", encoding="utf-8")

        failures = check.validate_public_reader_package(out_dir)

        for phrase in required_phrases:
            assert f"{package_path} missing packaged phrase: {phrase}" in failures
        package_path.write_text(original, encoding="utf-8")


def test_detects_default_doc_without_packaged_phrase_guard(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    guarded = dict(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH)
    guarded.pop(Path("docs/CRITICAL_OMISSION_BREAKS_NULL.md"))
    monkeypatch.setattr(check, "REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH", guarded)

    failures = check.validate_public_reader_package(out_dir)

    assert (
        "default package doc lacks required phrase guard: "
        "docs/CRITICAL_OMISSION_BREAKS_NULL.md"
    ) in failures


def test_detects_packaged_phrase_guard_path_not_in_manifest(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    guarded = dict(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH)
    guarded[Path("docs/MISSING_FROM_PACKAGE.md")] = ("required phrase",)
    monkeypatch.setattr(check, "REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH", guarded)

    failures = check.validate_public_reader_package(out_dir)

    assert (
        "required packaged phrase guard path not in manifest: "
        "docs/MISSING_FROM_PACKAGE.md"
    ) in failures


def test_detects_missing_packaged_file(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    (out_dir / "docs/START_HERE.md").unlink()

    failures = check.validate_public_reader_package(out_dir)

    assert any("docs/START_HERE.md is missing" in failure for failure in failures)


def test_detects_unsafe_manifest_package_path(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][0]["package_path"] = "../outside.md"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert any(
        "unsafe manifest package path: ../outside.md" in failure
        for failure in failures
    )


def test_detects_manifest_package_mapping_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][0]["package_path"] = "README.md"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert any(
        "manifest package path does not match source mapping: "
        "README.md -> README.md (expected docs/REPOSITORY_README.md)" in failure
        for failure in failures
    )


def test_detects_unmanifested_extra_file(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    _write(out_dir / "stale_extra.md", "# stale\n")

    failures = check.validate_public_reader_package(out_dir)

    assert "unexpected package file: stale_extra.md" in failures


def test_detects_unsafe_manifest_source_path(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][0]["source"] = "../outside.md"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert "unsafe manifest source path: ../outside.md" in failures


def test_detects_forbidden_manifest_source_path(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][0]["source"] = "data/raw/source.md"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert "forbidden manifest source path: data/raw/source.md" in failures


def test_detects_package_readme_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    readme = out_dir / "README.md"
    text = readme.read_text(encoding="utf-8")
    readme.write_text(
        text.replace("Package files:", "Package file list:"),
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert f"{readme} content drifted from manifest" in failures


def test_detects_reader_package_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    reader_package = out_dir / "reader_package.md"
    text = reader_package.read_text(encoding="utf-8")
    reader_package.write_text(
        text.replace("Source: `docs/START_HERE.md`", "Source: `docs/MISSING.md`"),
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert f"{reader_package} content drifted from package files" in failures
