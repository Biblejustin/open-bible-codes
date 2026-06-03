"""Lock the skip predicate that lets a fresh clone run the unit suite green."""

from __future__ import annotations

from pathlib import Path

from tests._skip_helpers import REPO_ROOT, is_missing_generated_artifact


def test_filenotfound_under_data_is_artifact() -> None:
    exc = FileNotFoundError(
        2, "No such file or directory", str(REPO_ROOT / "data/processed/ebible/grctr.csv")
    )
    assert is_missing_generated_artifact(exc) is True


def test_filenotfound_under_reports_is_artifact() -> None:
    exc = FileNotFoundError(
        2, "No such file or directory", str(REPO_ROOT / "reports/critical_omission_breaks_summary.csv")
    )
    assert is_missing_generated_artifact(exc) is True


def test_filenotfound_for_tracked_source_is_not_artifact() -> None:
    # A missing tracked source file is a real bug, not absent local data.
    exc = FileNotFoundError(2, "No such file or directory", str(REPO_ROOT / "els/corpus.py"))
    assert is_missing_generated_artifact(exc) is False


def test_assertion_error_is_not_artifact() -> None:
    assert is_missing_generated_artifact(AssertionError("expected 202, got 558")) is False


def test_unrelated_filenotfound_is_not_artifact() -> None:
    exc = FileNotFoundError(2, "No such file or directory", "/tmp/somewhere/else.csv")
    assert is_missing_generated_artifact(exc) is False


def test_none_is_not_artifact() -> None:
    assert is_missing_generated_artifact(None) is False


def test_message_only_filenotfound_under_data_is_artifact() -> None:
    # Some raisers don't set .filename; fall back to the message string.
    exc = FileNotFoundError(f"missing {REPO_ROOT / 'data/raw/oshb/wlc'}")
    assert is_missing_generated_artifact(exc) is True
