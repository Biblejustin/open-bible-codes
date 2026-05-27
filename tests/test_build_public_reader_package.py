import json
from pathlib import Path

import pytest

from scripts import build_public_reader_package as package


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_builds_reader_package_from_whitelisted_docs(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, f"# {path.name}\n\nbody\n")
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
    assert Path("reports/public_reader_package/docs/START_HERE.md").exists()
    assert Path("reports/public_reader_package/docs/PROJECT_FINDINGS_OVERVIEW.md").exists()
    assert Path("reports/public_reader_package/docs/STRONGEST_CANDIDATE_DEEP_DIVE.md").exists()
    assert Path("reports/public_reader_package/reader_package.md").exists()
    reader_package = Path(
        "reports/public_reader_package/reader_package.md"
    ).read_text(encoding="utf-8")
    assert "Source: `docs/START_HERE.md`" in reader_package
    assert "Source: `docs/PROJECT_FINDINGS_OVERVIEW.md`" in reader_package


def test_refuses_raw_source_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _write(Path("data/raw/private.txt"), "raw\n")

    with pytest.raises(ValueError):
        package.copy_checked_file(
            Path("data/raw/private.txt"),
            Path("reports/public_reader_package/data/raw/private.txt"),
        )
