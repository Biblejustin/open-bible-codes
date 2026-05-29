import csv
import json
import shutil
import tempfile
from pathlib import Path

from scripts import check_kjva_apocrypha_bridge_prospective_boundary as check


def test_current_kjva_apocrypha_bridge_prospective_boundary_passes() -> None:
    assert check.validate_kjva_apocrypha_bridge_prospective_boundary() == []


def test_candidate_row_drift_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = copy_current_inputs(Path(tmp))
        fieldnames, rows = read_csv(paths["candidates"])
        rows[0]["normalized_term"] = "judith"
        write_csv(paths["candidates"], fieldnames, rows)

        failures = validate(paths)

        assert any("candidate normalized_term" in failure for failure in failures)


def test_significant_q_value_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = copy_current_inputs(Path(tmp))
        fieldnames, rows = read_csv(paths["term_summary"])
        rows[0]["q_ge"] = "0.05"
        write_csv(paths["term_summary"], fieldnames, rows)

        failures = validate(paths)

        assert any("crosses q_ge threshold" in failure for failure in failures)


def test_nonbible_control_boundary_drift_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = copy_current_inputs(Path(tmp))
        fieldnames, rows = read_csv(paths["nonbible_control_summary"])
        for row in rows:
            if row["control_label"] == "MOBY_DICK":
                row["bridge_rows"] = "0"
        write_csv(paths["nonbible_control_summary"], fieldnames, rows)

        failures = validate(paths)

        assert any("controls >= observed total is 0" in failure for failure in failures)


def test_ready_for_preflight_profile_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = copy_current_inputs(Path(tmp))
        payload = json.loads(paths["profiles"].read_text(encoding="utf-8"))
        payload["profiles"][0]["status"] = "ready_for_preflight"
        paths["profiles"].write_text(json.dumps(payload), encoding="utf-8")

        failures = validate(paths)

        assert any("ready_for_preflight lane" in failure for failure in failures)


def test_doc_phrase_drift_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = copy_current_inputs(Path(tmp))
        text = paths["controls_doc"].read_text(encoding="utf-8").replace(
            "terms with BH q_ge <= 0.05: 0",
            "terms with BH q_ge <= 0.05: 1",
        )
        paths["controls_doc"].write_text(text, encoding="utf-8")

        failures = validate(paths)

        assert any("missing phrase" in failure for failure in failures)


def copy_current_inputs(root: Path) -> dict[str, Path]:
    paths = {
        "terms": root / "terms.csv",
        "candidates": root / "bridge_candidates.csv",
        "bridge_summary": root / "bridge_summary.csv",
        "term_summary": root / "term_summary.csv",
        "nonbible_control_summary": root / "control_summary.csv",
        "nonbible_term_summary": root / "nonbible_term_summary.csv",
        "profiles": root / "profiles.json",
        "candidates_doc": root / "candidates.md",
        "controls_doc": root / "controls.md",
        "nonbible_doc": root / "nonbible.md",
    }
    defaults = {
        "terms": check.DEFAULT_TERMS,
        "candidates": check.DEFAULT_CANDIDATES,
        "bridge_summary": check.DEFAULT_BRIDGE_SUMMARY,
        "term_summary": check.DEFAULT_TERM_SUMMARY,
        "nonbible_control_summary": check.DEFAULT_NONBIBLE_CONTROL_SUMMARY,
        "nonbible_term_summary": check.DEFAULT_NONBIBLE_TERM_SUMMARY,
        "profiles": check.DEFAULT_PROFILES,
        "candidates_doc": check.DEFAULT_CANDIDATES_DOC,
        "controls_doc": check.DEFAULT_CONTROLS_DOC,
        "nonbible_doc": check.DEFAULT_NONBIBLE_DOC,
    }
    for key, source in defaults.items():
        shutil.copyfile(source, paths[key])
    return paths


def validate(paths: dict[str, Path]) -> list[str]:
    return check.validate_kjva_apocrypha_bridge_prospective_boundary(
        terms=paths["terms"],
        candidates=paths["candidates"],
        bridge_summary=paths["bridge_summary"],
        term_summary=paths["term_summary"],
        nonbible_control_summary=paths["nonbible_control_summary"],
        nonbible_term_summary=paths["nonbible_term_summary"],
        profiles=paths["profiles"],
        candidates_doc=paths["candidates_doc"],
        controls_doc=paths["controls_doc"],
        nonbible_doc=paths["nonbible_doc"],
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
