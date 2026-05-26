import csv
from pathlib import Path

from scripts import check_wrr_source_audit_doc as check


def test_current_wrr_source_audit_doc_passes() -> None:
    assert check.validate_source_audit_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_audit_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_local_lock_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_AUDIT.md"
    text = "\n".join(
        phrase
        for phrase in check.REQUIRED_PHRASES
        if "keep_all_working_source" not in phrase
    )
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_source_audit_doc(doc)

    assert any("keep_all_working_source" in failure for failure in failures)


def test_stale_missing_implementation_language_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_AUDIT.md"
    doc.write_text(
        "\n".join(check.REQUIRED_PHRASES)
        + "\nfuture corrected-distance implementation\n",
        encoding="utf-8",
    )

    failures = check.validate_source_audit_doc(doc)

    assert any("stale phrase" in failure for failure in failures)


def test_validate_source_audit_accepts_matching_csvs(tmp_path: Path) -> None:
    failures = check.validate_source_audit_doc(
        _doc(tmp_path),
        locked_method_report=_locked_method_report(tmp_path),
        method_status=_method_status(tmp_path),
        manual_summary=_manual_summary(tmp_path),
    )

    assert failures == []


def test_validate_source_audit_rejects_locked_method_drift(tmp_path: Path) -> None:
    failures = check.validate_source_audit_doc(
        _doc(tmp_path),
        locked_method_report=_locked_method_report(
            tmp_path,
            bad_key=("lock", "Pair universe"),
        ),
        method_status=_method_status(tmp_path),
        manual_summary=_manual_summary(tmp_path),
    )

    assert any("('lock', 'Pair universe') value drifted" in failure for failure in failures)


def test_validate_source_audit_rejects_method_status_drift(tmp_path: Path) -> None:
    failures = check.validate_source_audit_doc(
        _doc(tmp_path),
        locked_method_report=_locked_method_report(tmp_path),
        method_status=_method_status(tmp_path, bad_area="Pair universe"),
        manual_summary=_manual_summary(tmp_path),
    )

    assert any("Pair universe status drifted" in failure for failure in failures)


def test_validate_source_audit_rejects_manual_summary_drift(tmp_path: Path) -> None:
    failures = check.validate_source_audit_doc(
        _doc(tmp_path),
        locked_method_report=_locked_method_report(tmp_path),
        method_status=_method_status(tmp_path),
        manual_summary=_manual_summary(tmp_path, bad_lane="method_pair_universe"),
    )

    assert any("method_pair_universe action_terms drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--doc", str(tmp_path / "missing.md")])

    assert code == 1
    assert "WRR source-audit doc failure" in capsys.readouterr().err


def _doc(tmp_path: Path) -> Path:
    path = tmp_path / "WRR_SOURCE_AUDIT.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")
    return path


def _locked_method_report(
    tmp_path: Path,
    *,
    bad_key: tuple[str, str] | None = None,
) -> Path:
    path = tmp_path / "wrr_locked_method_report.csv"
    fieldnames = ["section", "item", "value", "status", "evidence", "source"]
    rows = []
    for key, (value, status) in check.EXPECTED_LOCKED_METHOD_ROWS.items():
        section, item = key
        rows.append(
            {
                "section": section,
                "item": item,
                "value": "changed" if key == bad_key else value,
                "status": status,
                "evidence": "evidence",
                "source": "source.csv",
            }
        )
    return _write_csv(path, fieldnames, rows)


def _method_status(tmp_path: Path, *, bad_area: str | None = None) -> Path:
    path = tmp_path / "wrr_method_status.csv"
    fieldnames = ["decision_area", "status", "current_read", "evidence", "next_action"]
    rows = []
    for area, status in check.EXPECTED_METHOD_STATUS.items():
        rows.append(
            {
                "decision_area": area,
                "status": "changed" if area == bad_area else status,
                "current_read": "current",
                "evidence": "; ".join(
                    check.EXPECTED_METHOD_EVIDENCE_SNIPPETS.get(area, ("evidence",))
                ),
                "next_action": "next",
            }
        )
    return _write_csv(path, fieldnames, rows)


def _manual_summary(tmp_path: Path, *, bad_lane: str | None = None) -> Path:
    path = tmp_path / "wrr_manual_decision_register_summary.csv"
    fieldnames = [
        "decision_lane",
        "decision_rows",
        "action_terms",
        "residual_pairs",
        "frontier_pairs",
        "review_state",
    ]
    rows = []
    for lane, expected in check.EXPECTED_MANUAL_SUMMARY.items():
        decision_rows, action_terms, residual_pairs, frontier_pairs, review_state = expected
        rows.append(
            {
                "decision_lane": lane,
                "decision_rows": decision_rows,
                "action_terms": "99" if lane == bad_lane else action_terms,
                "residual_pairs": residual_pairs,
                "frontier_pairs": frontier_pairs,
                "review_state": review_state,
            }
        )
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
