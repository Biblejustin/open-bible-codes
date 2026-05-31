from scripts import bootstrap_public_sources


def test_outputs_exist_checks_all_paths(tmp_path, monkeypatch) -> None:
    (tmp_path / "done.txt").write_text("ok\n", encoding="utf-8")
    monkeypatch.setattr(bootstrap_public_sources, "ROOT", tmp_path)

    assert bootstrap_public_sources.outputs_exist(["done.txt"])
    assert not bootstrap_public_sources.outputs_exist(["done.txt", "missing.txt"])

