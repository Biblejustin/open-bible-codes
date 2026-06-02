import pytest

from scripts import check_study_lock_manifest as check
from els.protocol_runner import path_fingerprint


def locked_manifest() -> dict:
    return {
        "status": "locked",
        "git": {"dirty": False},
        "missing_paths": [],
        "settings": {"skip_range": "2..50", "direction": "both"},
        "locked_paths": [{"path": "terms/example.csv", "type": "file", "sha256": "abc"}],
    }


def test_validate_manifest_accepts_locked_clean_manifest() -> None:
    failures = check.validate_manifest(
        locked_manifest(),
        required_settings=["skip_range", "direction"],
        allow_dirty=False,
        verify_paths=False,
    )

    assert failures == []


def test_read_manifest_rejects_invalid_json(tmp_path) -> None:
    path = tmp_path / "lock.manifest.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(ValueError, match="is invalid JSON"):
        check.read_manifest(path)


def test_read_manifest_rejects_non_object_json(tmp_path) -> None:
    path = tmp_path / "lock.manifest.json"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="JSON root must be an object"):
        check.read_manifest(path)


def test_validate_manifest_rejects_dirty_manifest_by_default() -> None:
    manifest = locked_manifest()
    manifest["git"]["dirty"] = True

    failures = check.validate_manifest(
        manifest,
        required_settings=[],
        allow_dirty=False,
        verify_paths=False,
    )

    assert "git dirty-state is true" in failures


def test_validate_manifest_allows_dirty_with_flag() -> None:
    manifest = locked_manifest()
    manifest["git"]["dirty"] = True

    failures = check.validate_manifest(
        manifest,
        required_settings=[],
        allow_dirty=True,
        verify_paths=False,
    )

    assert failures == []


def test_validate_manifest_requires_named_settings() -> None:
    failures = check.validate_manifest(
        locked_manifest(),
        required_settings=["control_budget"],
        allow_dirty=False,
        verify_paths=False,
    )

    assert "missing required setting: control_budget" in failures


def test_validate_manifest_rejects_missing_paths() -> None:
    manifest = locked_manifest()
    manifest["missing_paths"] = ["terms/missing.csv"]

    failures = check.validate_manifest(
        manifest,
        required_settings=[],
        allow_dirty=False,
        verify_paths=False,
    )

    assert "manifest has missing paths: terms/missing.csv" in failures


def test_validate_manifest_accepts_unchanged_locked_path(tmp_path) -> None:
    source = tmp_path / "terms.csv"
    source.write_text("term_id,term\nx,δοξα\n", encoding="utf-8")
    manifest = locked_manifest()
    manifest["locked_paths"] = [path_fingerprint(str(source))]

    failures = check.validate_manifest(
        manifest,
        required_settings=[],
        allow_dirty=False,
    )

    assert failures == []


def test_validate_manifest_ignores_file_mtime_churn(tmp_path) -> None:
    source = tmp_path / "terms.csv"
    source.write_text("term_id,term\nx,δοξα\n", encoding="utf-8")
    locked = path_fingerprint(str(source))
    source.touch()
    manifest = locked_manifest()
    manifest["locked_paths"] = [locked]

    failures = check.validate_manifest(
        manifest,
        required_settings=[],
        allow_dirty=False,
    )

    assert failures == []


def test_validate_manifest_rejects_changed_locked_path(tmp_path) -> None:
    source = tmp_path / "terms.csv"
    source.write_text("term_id,term\nx,δοξα\n", encoding="utf-8")
    locked = path_fingerprint(str(source))
    source.write_text("term_id,term\nx,ανομια\n", encoding="utf-8")
    manifest = locked_manifest()
    manifest["locked_paths"] = [locked]

    failures = check.validate_manifest(
        manifest,
        required_settings=[],
        allow_dirty=False,
    )

    assert f"locked path changed: {locked['path']}" in failures


def test_validate_manifest_ignores_directory_mtime_churn(tmp_path) -> None:
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    child = source_dir / "terms.csv"
    child.write_text("term_id,term\nx,δοξα\n", encoding="utf-8")
    locked = path_fingerprint(str(source_dir))
    child.touch()
    manifest = locked_manifest()
    manifest["locked_paths"] = [locked]

    failures = check.validate_manifest(
        manifest,
        required_settings=[],
        allow_dirty=False,
    )

    assert failures == []


def test_validate_manifest_rejects_changed_directory_content(tmp_path) -> None:
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    child = source_dir / "terms.csv"
    child.write_text("term_id,term\nx,δοξα\n", encoding="utf-8")
    locked = path_fingerprint(str(source_dir))
    child.write_text("term_id,term\nx,ανομ\n", encoding="utf-8")
    manifest = locked_manifest()
    manifest["locked_paths"] = [locked]

    failures = check.validate_manifest(
        manifest,
        required_settings=[],
        allow_dirty=False,
    )

    assert f"locked path changed: {locked['path']}" in failures


def test_validate_manifest_accepts_legacy_directory_fingerprint(tmp_path) -> None:
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    child = source_dir / "terms.csv"
    child.write_text("term_id,term\nx,δοξα\n", encoding="utf-8")
    locked = path_fingerprint(str(source_dir))
    legacy_locked = dict(locked)
    legacy_locked["tree_sha256"] = str(locked["legacy_tree_sha256"])
    del legacy_locked["legacy_tree_sha256"]
    manifest = locked_manifest()
    manifest["locked_paths"] = [legacy_locked]

    failures = check.validate_manifest(
        manifest,
        required_settings=[],
        allow_dirty=False,
    )

    assert failures == []
