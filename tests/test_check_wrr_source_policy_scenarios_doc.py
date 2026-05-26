import csv
from pathlib import Path

from scripts import check_wrr_source_policy_scenarios_doc as check


def test_current_wrr_source_policy_scenarios_doc_passes() -> None:
    assert check.validate_source_policy_scenarios_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_policy_scenarios_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_exclusion_counts_fail(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_POLICY_SCENARIOS.md"
    phrases = [
        phrase
        for phrase in check.REQUIRED_PHRASES
        if "exclude_all_source_review_flags" not in phrase
    ]
    doc.write_text("\n".join(phrases) + "\n", encoding="utf-8")

    failures = check.validate_source_policy_scenarios_doc(doc)

    assert any("exclude_all_source_review_flags" in failure for failure in failures)


def test_validate_source_policy_scenarios_accepts_matching_csvs(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_source_policy_scenarios_doc(
        doc,
        scenarios=_scenarios_csv(tmp_path),
        term_impacts=_term_impacts_csv(tmp_path),
        scenario_pairs=_scenario_pairs_csv(tmp_path),
    )

    assert failures == []


def test_validate_source_policy_scenarios_rejects_scenario_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_source_policy_scenarios_doc(
        doc,
        scenarios=_scenarios_csv(tmp_path, bad_scenario="exclude_all_source_review_flags"),
        term_impacts=_term_impacts_csv(tmp_path),
        scenario_pairs=_scenario_pairs_csv(tmp_path),
    )

    assert any("exclude_all_source_review_flags excluded_pairs" in failure for failure in failures)


def test_validate_source_policy_scenarios_rejects_term_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_source_policy_scenarios_doc(
        doc,
        scenarios=_scenarios_csv(tmp_path),
        term_impacts=_term_impacts_csv(tmp_path, bad_term="wrr2_27_app_02"),
        scenario_pairs=_scenario_pairs_csv(tmp_path),
    )

    assert any("wrr2_27_app_02 affected_pairs" in failure for failure in failures)


def test_validate_source_policy_scenarios_rejects_pair_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_source_policy_scenarios_doc(
        doc,
        scenarios=_scenarios_csv(tmp_path),
        term_impacts=_term_impacts_csv(tmp_path),
        scenario_pairs=_scenario_pairs_csv(tmp_path, drop_last=True),
    )

    assert any("scenario/action counts drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR source-policy scenarios doc failure" in capsys.readouterr().err


def _doc(tmp_path: Path) -> Path:
    doc = tmp_path / "WRR_SOURCE_POLICY_SCENARIOS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return doc


def _scenarios_csv(tmp_path: Path, *, bad_scenario: str | None = None) -> Path:
    path = tmp_path / "scenarios.csv"
    fieldnames = [
        "scenario",
        "policy_type",
        "source_policy_selected",
        "excluded_terms",
        "excluded_pairs",
        "review_only_terms",
        "review_only_pairs",
        "remaining_pairs",
        "remaining_appellation_min_length_pairs",
        "remaining_length_filtered_pairs",
        "gap_to_source_cited_163_after_appellation_min_length",
        "gap_to_source_cited_163_after_length_filtered",
        "diagnostic_read",
    ]
    rows = []
    for scenario, expected in check.EXPECTED_SCENARIOS.items():
        row = {field: "" for field in fieldnames}
        row.update(expected)
        row["scenario"] = scenario
        row["source_policy_selected"] = "false"
        row["diagnostic_read"] = "diagnostic"
        if scenario == bad_scenario:
            row["excluded_pairs"] = "drifted"
        rows.append(row)
    return _write_csv(path, fieldnames, rows)


def _term_impacts_csv(tmp_path: Path, *, bad_term: str | None = None) -> Path:
    path = tmp_path / "term_impacts.csv"
    fieldnames = [
        "term_id",
        "term",
        "term_side",
        "flags",
        "affected_pairs",
        "remaining_appellation_min_length_pairs_if_excluded",
        "gap_to_source_cited_163_after_appellation_min_length_if_excluded",
        "closes_appellation_min_length_gap_to_163",
    ]
    rows = []
    for term_id, expected in check.EXPECTED_TERM_IMPACTS.items():
        term, flags, affected, remaining, gap, closes = expected
        rows.append(
            {
                "term_id": term_id,
                "term": term,
                "term_side": "appellation",
                "flags": flags,
                "affected_pairs": "drifted" if term_id == bad_term else affected,
                "remaining_appellation_min_length_pairs_if_excluded": remaining,
                "gap_to_source_cited_163_after_appellation_min_length_if_excluded": gap,
                "closes_appellation_min_length_gap_to_163": closes,
            }
        )
    return _write_csv(path, fieldnames, rows)


def _scenario_pairs_csv(tmp_path: Path, *, drop_last: bool = False) -> Path:
    path = tmp_path / "scenario_pairs.csv"
    fieldnames = [
        "scenario",
        "scenario_action",
        "pair_id",
        "source_review_flags",
        "flagged_term_ids",
        "pair_review_status",
    ]
    rows = []
    for (scenario, action), count in check.EXPECTED_SCENARIO_PAIR_COUNTS.items():
        for index in range(count):
            rows.append(
                {
                    "scenario": scenario,
                    "scenario_action": action,
                    "pair_id": f"{scenario}_{index}",
                    "source_review_flags": "wnp_disputed_zacut_appellation",
                    "flagged_term_ids": "term",
                    "pair_review_status": (
                        "diagnostic_exclusion_candidate_not_locked"
                        if action == "excluded"
                        else "needs_primary_source_pair_rule"
                    ),
                }
            )
    if drop_last:
        rows = rows[:-1]
    return _write_csv(path, fieldnames, rows)


def _write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> Path:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path
