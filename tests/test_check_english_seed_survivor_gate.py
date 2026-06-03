import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import shutil
import tempfile
from pathlib import Path

from scripts import check_english_seed_survivor_gate as check


def test_current_english_seed_survivor_gate_passes() -> None:
    assert check.validate_english_seed_survivor_gate() == []


def test_survivor_row_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = copy_current_inputs(Path(tmp))
        append_row(
            paths["survivors"],
            {
                "term_id": "eng_demo",
                "concept": "Demo",
                "category": "demo",
                "language": "english",
                "term": "demo",
                "notes": "should fail",
            },
        )

        failures = validate(paths)

        assert any("survivor row" in failure for failure in failures)


def test_followup_threshold_crossing_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = copy_current_inputs(Path(tmp))
        fieldnames, rows = read_csv(paths["followup_summary"])
        rows[0]["p_greater_equal"] = "0.05"
        write_csv(paths["followup_summary"], fieldnames, rows)

        failures = validate(paths)

        assert any("crosses survivor threshold" in failure for failure in failures)


def test_downstream_row_fails_when_gate_is_empty() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = copy_current_inputs(Path(tmp))
        append_row(
            paths["paired_summary"],
            {
                "concept": "Demo",
                "corpus": "ERV",
                "term_set": "english_seed_followup_survivors",
                "term_id": "eng_demo",
            },
        )

        failures = validate(paths)

        assert any("paired-control summary has 1 row" in failure for failure in failures)


def test_missing_doc_phrase_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = copy_current_inputs(Path(tmp))
        text = paths["survivor_audit_doc"].read_text(encoding="utf-8").replace(
            "Status: no current survivor rows.",
            "Status: drifted.",
        )
        paths["survivor_audit_doc"].write_text(text, encoding="utf-8")

        failures = validate(paths)

        assert any("missing phrase" in failure for failure in failures)


def copy_current_inputs(root: Path) -> dict[str, Path]:
    paths = {
        "followup_summary": root / "followup.csv",
        "survivors": root / "survivors.csv",
        "followup_doc": root / "followup.md",
        "term_shuffle_summary": root / "term_shuffle.csv",
        "survivor_audit_summary": root / "audit_summary.csv",
        "survivor_audit_letter_paths": root / "letter_paths.csv",
        "survivor_audit_doc": root / "audit.md",
        "target_summary": root / "target_summary.csv",
        "paired_summary": root / "paired_summary.csv",
        "paired_examples": root / "paired_examples.csv",
        "paired_doc": root / "paired.md",
    }
    defaults = {
        "followup_summary": check.DEFAULT_FOLLOWUP_SUMMARY,
        "survivors": check.DEFAULT_SURVIVORS,
        "followup_doc": check.DEFAULT_FOLLOWUP_DOC,
        "term_shuffle_summary": check.DEFAULT_TERM_SHUFFLE_SUMMARY,
        "survivor_audit_summary": check.DEFAULT_SURVIVOR_AUDIT_SUMMARY,
        "survivor_audit_letter_paths": check.DEFAULT_SURVIVOR_AUDIT_LETTER_PATHS,
        "survivor_audit_doc": check.DEFAULT_SURVIVOR_AUDIT_DOC,
        "target_summary": check.DEFAULT_TARGET_SUMMARY,
        "paired_summary": check.DEFAULT_PAIRED_SUMMARY,
        "paired_examples": check.DEFAULT_PAIRED_EXAMPLES,
        "paired_doc": check.DEFAULT_PAIRED_DOC,
    }
    for key, source in defaults.items():
        shutil.copyfile(source, paths[key])
    return paths


def validate(paths: dict[str, Path]) -> list[str]:
    return check.validate_english_seed_survivor_gate(
        followup_summary=paths["followup_summary"],
        survivors=paths["survivors"],
        followup_doc=paths["followup_doc"],
        term_shuffle_summary=paths["term_shuffle_summary"],
        survivor_audit_summary=paths["survivor_audit_summary"],
        survivor_audit_letter_paths=paths["survivor_audit_letter_paths"],
        survivor_audit_doc=paths["survivor_audit_doc"],
        target_summary=paths["target_summary"],
        paired_summary=paths["paired_summary"],
        paired_examples=paths["paired_examples"],
        paired_doc=paths["paired_doc"],
    )


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def append_row(path: Path, row: dict[str, str]) -> None:
    fieldnames, rows = read_csv(path)
    rows.append(row)
    write_csv(path, fieldnames, rows)
