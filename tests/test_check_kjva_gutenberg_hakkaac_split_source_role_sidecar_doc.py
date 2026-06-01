import csv
import json

from scripts import build_kjva_gutenberg_hakkaac_split_source_role_sidecar as sidecar
from scripts import check_kjva_gutenberg_hakkaac_split_source_role_sidecar_doc as check


def _write_csv(path, fieldnames, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _valid_roles() -> list[dict[str, str]]:
    statuses = {
        "current_ebible_rerun_baseline": "policy_ready",
        "gutenberg_kjv_component": "recommended_policy_not_locked",
        "gutenberg_apocrypha_component": "blocked",
        "gutenberg_lje_baruch_rollup": "recommended_policy_not_locked",
        "hakkaac_marker_collation_witness": "candidate_not_locked",
        "split_stream_boundary": "blocked",
        "tracked_text_retention_boundary": "policy_ready",
    }
    rows = []
    for role_id, status in statuses.items():
        rows.append(
            {
                "role_id": role_id,
                "source_family": "source",
                "component": "component",
                "source_role": "role",
                "order_role": "order",
                "lock_status": status,
                "allowed_use": "allowed",
                "blocked_use": "blocked",
                "evidence_summary": "evidence",
                "next_action": "next",
                "result_boundary": "not_result_bearing",
            }
        )
    return rows


def _valid_blockers() -> list[dict[str, str]]:
    return [
        {
            "blocker_id": blocker_id,
            "area": "area",
            "current_status": "blocked",
            "evidence_summary": "evidence",
            "blocked_until": "later",
            "affects_letter_stream": "True",
            "result_boundary": "not_result_bearing",
        }
        for blocker_id in [
            "sirach_44_23_gutenberg_marker_gap",
            "manasseh_unmarked_gutenberg_section",
            "sirach_19_1_hakkaac_length_drift",
            "hakkaac_source_use_boundary",
            "split_source_result_boundary",
            "gutenberg_source_stream_boundary",
        ]
    ]


def _valid_summary() -> dict[str, str]:
    return {
        "role_rows": "7",
        "blocker_rows": "6",
        "policy_ready_rows": "2",
        "recommended_policy_rows": "2",
        "blocked_rows": "2",
        "candidate_not_locked_rows": "1",
        "current_rerun_locked": "True",
        "split_source_role_sidecar_written": "True",
        "local_apocrypha_order": check.EXPECTED_LOCAL_ORDER,
        "gutenberg_apocrypha_order": check.EXPECTED_GUTENBERG_ORDER,
        "future_independent_order_recommendation": (
            "use_gutenberg_source_order_for_independent_replication"
        ),
        "hakkaac_exact_marker_books": "14",
        "hakkaac_exact_normalized_verse_matches": "5719",
        "hakkaac_length_drift_verses": "1",
        "gutenberg_sirach_gap_refs": "SIR 44:23",
        "gutenberg_manasseh_source_markers": "0",
        "gutenberg_manasseh_local_markers": "15",
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "split_source_role_sidecar_only_not_result_bearing",
    }


def test_checker_accepts_generated_sidecar_doc(tmp_path) -> None:
    roles = _valid_roles()
    blockers = _valid_blockers()
    summary = _valid_summary()
    doc = tmp_path / "KJVA_GUTENBERG_HAKKAAC_SPLIT_SOURCE_ROLE_SIDECAR.md"
    roles_csv = tmp_path / "roles.csv"
    blockers_csv = tmp_path / "blockers.csv"
    summary_csv = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"

    sidecar.write_markdown(doc, summary, roles, blockers)
    _write_csv(roles_csv, sidecar.ROLE_FIELDNAMES, roles)
    _write_csv(blockers_csv, sidecar.BLOCKER_FIELDNAMES, blockers)
    _write_csv(summary_csv, sidecar.SUMMARY_FIELDNAMES, [summary])
    manifest.write_text(
        json.dumps(
            {
                "claim_boundary": "split-source role sidecar only; no ELS result",
                "text_retention": "no Bible text written to tracked outputs",
                "outputs": {"markdown": str(doc)},
            }
        ),
        encoding="utf-8",
    )

    assert (
        check.validate_kjva_gutenberg_hakkaac_split_source_role_sidecar_doc(
            doc,
            roles=roles_csv,
            blockers=blockers_csv,
            summary=summary_csv,
            manifest=manifest,
        )
        == []
    )


def test_checker_rejects_result_ready_overclaim(tmp_path) -> None:
    doc = tmp_path / "sidecar.md"
    doc.write_text(
        "# KJVA Gutenberg Hakkaac Split-Source Role Sidecar\n\n"
        "This result-bearing replication is ready.\n",
        encoding="utf-8",
    )

    failures = check.validate_kjva_gutenberg_hakkaac_split_source_role_sidecar_doc(
        doc,
        roles=None,
        blockers=None,
        summary=None,
        manifest=None,
    )

    assert any("overclaim" in failure or "missing phrase" in failure for failure in failures)
