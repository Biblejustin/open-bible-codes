import csv
import json

from scripts import build_kjva_source_policy_blocker_packet as packet
from scripts import check_kjva_source_policy_blocker_packet_doc as check


def _write_csv(path, fieldnames, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _valid_options() -> list[dict[str, str]]:
    statuses = {
        "current_ebible_rerun_only": "policy_ready",
        "project_gutenberg_only_candidate": "blocked",
        "project_gutenberg_hakkaac_split_candidate": "blocked",
        "hakkaac_primary_stream": "blocked",
        "defer_new_kjva_replication": "policy_ready",
    }
    return [
        {
            "option_id": option_id,
            "source_stream": "source",
            "status": status,
            "allowed_use": "allowed",
            "blocked_use": "blocked",
            "evidence_summary": "evidence",
            "blocker_summary": "blocker",
            "next_action": "next",
            "result_boundary": "not_result_bearing",
        }
        for option_id, status in statuses.items()
    ]


def _valid_blockers() -> list[dict[str, str]]:
    rows = []
    for blocker_id in check.REQUIRED_BLOCKER_IDS:
        rows.append(
            {
                "blocker_id": blocker_id,
                "area": "area",
                "status": (
                    "closed_as_planning_only"
                    if blocker_id == "role_sidecar_complete_but_not_sufficient"
                    else "blocked"
                ),
                "evidence_summary": "evidence",
                "required_before_result": "required",
                "needs_user_or_source_policy_choice": "True",
                "affects_letter_stream": "True",
                "result_boundary": "not_result_bearing",
            }
        )
    return rows


def _valid_summary() -> dict[str, object]:
    return {
        "policy_option_rows": "5",
        "blocker_rows": "7",
        "policy_ready_options": "2",
        "blocked_options": "3",
        "checksum_records_ready": "2",
        "split_source_role_sidecar_written": True,
        "current_rerun_locked": True,
        "source_use_ready_pages": "0",
        "gutenberg_sirach_gap_refs": "SIR 44:23",
        "gutenberg_manasseh_source_markers": "0",
        "gutenberg_manasseh_local_markers": "15",
        "hakkaac_length_drift_verses": "1",
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "source_policy_blocker_packet_only_not_result_bearing",
    }


def test_checker_accepts_generated_packet_doc(tmp_path) -> None:
    options = _valid_options()
    blockers = _valid_blockers()
    summary = _valid_summary()
    doc = tmp_path / "KJVA_SOURCE_POLICY_BLOCKER_PACKET.md"
    options_csv = tmp_path / "policy_options.csv"
    blockers_csv = tmp_path / "blockers.csv"
    summary_csv = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"

    packet.write_markdown(doc, summary, options, blockers)
    _write_csv(options_csv, packet.OPTION_FIELDNAMES, options)
    _write_csv(blockers_csv, packet.BLOCKER_FIELDNAMES, blockers)
    _write_csv(summary_csv, packet.SUMMARY_FIELDNAMES, [summary])
    manifest.write_text(
        json.dumps(
            {
                "claim_boundary": "source-policy blocker packet only; no ELS result",
                "text_retention": "no Bible text written to tracked outputs",
                "summary": {"result_ready": False},
                "outputs": {"markdown": str(doc)},
            }
        ),
        encoding="utf-8",
    )

    assert (
        check.validate_kjva_source_policy_blocker_packet_doc(
            doc,
            options=options_csv,
            blockers=blockers_csv,
            summary=summary_csv,
            manifest=manifest,
        )
        == []
    )


def test_checker_rejects_claim_report_overclaim(tmp_path) -> None:
    doc = tmp_path / "packet.md"
    doc.write_text(
        "# KJVA Source Policy Blocker Packet\n\nThis claim report proves readiness.\n",
        encoding="utf-8",
    )

    failures = check.validate_kjva_source_policy_blocker_packet_doc(
        doc,
        options=None,
        blockers=None,
        summary=None,
        manifest=None,
    )

    assert any("overclaim" in failure or "missing phrase" in failure for failure in failures)
