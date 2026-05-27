import json
from pathlib import Path

from scripts import check_public_release_hygiene as check


def test_main_writes_pass_payload_with_allow_dirty(tmp_path: Path, monkeypatch) -> None:
    patch_hygiene(monkeypatch, git_status=[" M README.md"])
    out = tmp_path / "hygiene.json"

    code = check.main(["--allow-dirty", "--out", str(out)])

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert code == 0
    assert payload["status"] == "passed"
    assert payload["allow_dirty"] is True
    assert payload["expected_owner"] == "Biblejustin"


def test_main_fails_on_dirty_tree_without_allow_dirty(
    tmp_path: Path, monkeypatch
) -> None:
    patch_hygiene(monkeypatch, git_status=[" M README.md"])
    out = tmp_path / "hygiene.json"

    code = check.main(["--out", str(out)])

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert code == 1
    assert "git working tree is not clean" in payload["failures"]


def test_main_reports_remote_owner_failure(tmp_path: Path, monkeypatch) -> None:
    patch_hygiene(
        monkeypatch,
        remotes=["origin\thttps://github.com/Other/open-bible-codes.git (fetch)"],
    )
    out = tmp_path / "hygiene.json"

    code = check.main(["--allow-dirty", "--out", str(out)])

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert code == 1
    assert "no remote points to Biblejustin/open-bible-codes" in payload["failures"]


def patch_hygiene(
    monkeypatch,
    *,
    git_status: list[str] | None = None,
    remotes: list[str] | None = None,
) -> None:
    def fake_run_git(root: Path, *args: str) -> list[str]:
        if args == ("status", "--short"):
            return git_status or []
        if args == ("remote", "-v"):
            return remotes or [
                "origin\thttps://github.com/Biblejustin/open-bible-codes.git (fetch)",
                "origin\thttps://github.com/Biblejustin/open-bible-codes.git (push)",
            ]
        return []

    monkeypatch.setattr(check, "run_git", fake_run_git)
    monkeypatch.setattr(check, "git_tracked_paths", lambda root: ["README.md"])
    monkeypatch.setattr(check, "risky_tracked_paths", lambda paths: [])
    monkeypatch.setattr(check, "scan_tracked_for_forbidden_account", lambda root, paths: [])
    monkeypatch.setattr(check, "scan_tracked_for_secret_patterns", lambda root, paths: [])
