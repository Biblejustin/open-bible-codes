import json
from pathlib import Path

from scripts import build_study_lock_manifest as lock


def test_build_payload_fingerprints_existing_paths(tmp_path) -> None:
    source = tmp_path / "terms.csv"
    source.write_text("term_id,term\nx,δοξα\n", encoding="utf-8")

    paths = lock.resolve_lock_paths([str(source)], expand_corpus_configs=False)
    payload = lock.build_payload(
        name="demo",
        raw_paths=[str(source)],
        lock_paths=paths,
        notes=["fixed term list"],
        settings={"skip_range": "2..50"},
        missing=[],
        expand_corpus_configs=False,
        started=0.0,
    )

    assert payload["status"] == "locked"
    assert payload["name"] == "demo"
    assert payload["notes"] == ["fixed term list"]
    assert payload["settings"] == {"skip_range": "2..50"}
    assert "commit" in payload["git"]
    assert payload["locked_paths"][0]["type"] == "file"
    assert payload["locked_paths"][0]["sha256"]


def test_missing_paths_are_reported_without_fingerprints(tmp_path) -> None:
    missing = tmp_path / "missing.csv"

    payload = lock.build_payload(
        name="demo",
        raw_paths=[str(missing)],
        lock_paths=[str(missing)],
        notes=[],
        settings={},
        missing=[str(missing)],
        expand_corpus_configs=False,
        started=0.0,
    )

    assert payload["status"] == "failed"
    assert payload["missing_paths"] == [str(missing)]
    assert payload["locked_paths"] == []


def test_main_writes_manifest(tmp_path) -> None:
    source = tmp_path / "protocol.toml"
    source.write_text('name = "demo"\n', encoding="utf-8")
    out = tmp_path / "lock.json"

    code = lock.main(
        [
            "--name",
            "demo",
            "--path",
            str(source),
            "--out",
            str(out),
            "--setting",
            "skip_range=2..50",
            "--no-expand-corpus-configs",
        ]
    )

    assert code == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["status"] == "locked"
    assert payload["settings"] == {"skip_range": "2..50"}
    assert payload["locked_paths"][0]["path"] == str(source)


def test_parse_settings_rejects_values_without_key_value_separator() -> None:
    try:
        lock.parse_settings(["skip_range"])
    except ValueError as exc:
        assert "KEY=VALUE" in str(exc)
    else:
        raise AssertionError("expected ValueError")
