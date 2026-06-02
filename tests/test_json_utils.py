from pathlib import Path

import pytest

from scripts.json_utils import read_json_object


def test_read_json_object_rejects_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(ValueError, match="is invalid JSON"):
        read_json_object(path)


def test_read_json_object_rejects_non_object_json(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="JSON root must be an object"):
        read_json_object(path)


def test_read_json_object_returns_object(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text('{"status": "completed"}', encoding="utf-8")

    assert read_json_object(path) == {"status": "completed"}
