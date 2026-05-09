import csv
import json
from pathlib import Path

from scripts import audit_prospective_terms as audit


def test_audit_flags_exact_normalized_reuse(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    evidence = tmp_path / "evidence.csv"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term", "notes"],
        [["new_doxa", "Doxa", "screen", "greek", "δόξα", ""]],
    )
    write_csv(
        evidence,
        ["term_id", "language", "normalized_term"],
        [["old_doxa", "greek", "δοξα"]],
    )

    candidates, skipped_candidates = audit.read_candidates([candidate], min_normalized_length=1)
    evidence_values, skipped_evidence = audit.read_evidence_values(
        [evidence],
        min_normalized_length=1,
    )
    rows = audit.audit_matches(
        candidates,
        evidence_values,
        include_substrings=True,
        min_substring_length=4,
        include_self=False,
    )

    assert skipped_candidates == 0
    assert skipped_evidence == 0
    assert rows[0]["relationship"] == "exact"
    assert rows[0]["severity"] == "block"
    assert rows[0]["candidate_normalized"] == "δοξα"


def test_audit_flags_candidate_containing_prior_evidence(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    evidence = tmp_path / "evidence.csv"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term"],
        [["new_extension", "Doxa Extension", "screen", "greek", "δοξανωσ"]],
    )
    write_csv(
        evidence,
        ["term_id", "language", "normalized_term"],
        [["old_doxa", "greek", "δοξα"]],
    )

    rows = audit.audit_matches(
        audit.read_candidates([candidate], min_normalized_length=1)[0],
        audit.read_evidence_values([evidence], min_normalized_length=1)[0],
        include_substrings=True,
        min_substring_length=4,
        include_self=False,
    )

    assert rows[0]["relationship"] == "candidate_contains_evidence"
    assert rows[0]["severity"] == "review"
    assert rows[0]["normalized"] == "δοξα"


def test_audit_infers_language_from_raw_evidence_value(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    evidence = tmp_path / "evidence.csv"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term"],
        [["new_israel", "Israel", "screen", "hebrew", "ישראל"]],
    )
    write_csv(
        evidence,
        ["term_id", "term"],
        [["old_israel", "יִשְׂרָאֵל"]],
    )

    rows = audit.audit_matches(
        audit.read_candidates([candidate], min_normalized_length=1)[0],
        audit.read_evidence_values([evidence], min_normalized_length=1)[0],
        include_substrings=True,
        min_substring_length=4,
        include_self=False,
    )

    assert rows[0]["language"] == "hebrew"
    assert rows[0]["relationship"] == "exact"


def test_main_writes_summary_and_can_fail_on_match(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    evidence = tmp_path / "evidence.csv"
    out = tmp_path / "audit.csv"
    summary = tmp_path / "audit.summary.json"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term"],
        [["new_doxa", "Doxa", "screen", "greek", "δοξα"]],
    )
    write_csv(
        evidence,
        ["term_id", "language", "normalized_term"],
        [["old_doxa", "greek", "δοξα"]],
    )

    code = audit.main(
        [
            "--candidate",
            str(candidate),
            "--evidence",
            str(evidence),
            "--out",
            str(out),
            "--summary-out",
            str(summary),
            "--fail-on-match",
        ]
    )

    assert code == 1
    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert payload["status"] == "matched"
    assert payload["match_rows"] == 1
    with out.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["candidate_term_id"] == "new_doxa"


def test_main_passes_when_no_overlap(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate.csv"
    evidence = tmp_path / "evidence.csv"
    out = tmp_path / "audit.csv"
    write_csv(
        candidate,
        ["term_id", "concept", "category", "language", "term"],
        [["new_truth", "Truth", "screen", "greek", "αληθεια"]],
    )
    write_csv(
        evidence,
        ["term_id", "language", "normalized_term"],
        [["old_doxa", "greek", "δοξα"]],
    )

    code = audit.main(
        [
            "--candidate",
            str(candidate),
            "--evidence",
            str(evidence),
            "--out",
            str(out),
            "--fail-on-match",
        ]
    )

    assert code == 0
    payload = json.loads((tmp_path / "audit.csv.summary.json").read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["match_rows"] == 0


def write_csv(path: Path, fieldnames: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(fieldnames)
        writer.writerows(rows)
