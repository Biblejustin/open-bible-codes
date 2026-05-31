import runpy
import sys

import pytest

from scripts import download_ebible_usfm


def test_wrapper_injects_grctcgnt_source(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_main() -> int:
        calls.append(sys.argv[:])
        return 7

    monkeypatch.setattr(download_ebible_usfm, "main", fake_main)
    monkeypatch.setattr(sys, "argv", ["download_ebible_grctcgnt"])

    with pytest.raises(SystemExit) as exc:
        runpy.run_module("scripts.download_ebible_grctcgnt", run_name="__main__")

    assert exc.value.code == 7
    assert calls[0][1:3] == ["--source", "grctcgnt"]

