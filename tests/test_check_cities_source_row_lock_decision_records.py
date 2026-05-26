import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_cities_source_row_lock_decision_records as check


class CitiesSourceRowLockDecisionRecordsTests(unittest.TestCase):
    def test_current_header_only_records_pass(self) -> None:
        self.assertEqual(
            check.validate_decision_records(
                check.DEFAULT_RECORDS,
                check.DEFAULT_EVIDENCE_PACKET,
            ),
            [],
        )

    def test_populated_locked_record_must_match_evidence_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = root / "records.csv"
            evidence = root / "evidence.csv"
            write_records(
                records,
                [
                    record_row(
                        "1",
                        decision_status="locked",
                        selected_action="source_row_lock_ready",
                        evidence_citation=(
                            "docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md "
                            "row cities_source_row_lock_001"
                        ),
                        evidence_summary=(
                            "Reviewed packet metadata and page-image evidence; "
                            "source-row lock is ready without transcribing row text."
                        ),
                        locked_by="reviewer",
                        locked_at="2026-05-26",
                    )
                ],
            )
            write_evidence(evidence, [evidence_row("1")])

            self.assertEqual(check.validate_decision_records(records, evidence), [])

    def test_populated_record_rejects_mismatch_and_placeholder_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = root / "records.csv"
            evidence = root / "evidence.csv"
            row = record_row(
                "1",
                decision_status="locked",
                selected_action="source_row_lock_ready",
                evidence_citation="todo",
                evidence_summary="short",
                locked_by="reviewer",
                locked_at="2026/05/26",
            )
            row["page_class"] = "wrong_class"
            write_records(records, [row])
            write_evidence(evidence, [evidence_row("1")])

            failures = check.validate_decision_records(records, evidence)

            self.assertIn(
                f"{records}:2 page_class must match evidence packet: table_candidate_page",
                failures,
            )
            self.assertIn(f"{records}:2 placeholder value for evidence_citation", failures)
            self.assertIn(f"{records}:2 evidence_summary is too short", failures)
            self.assertIn(f"{records}:2 locked_at must be ISO date", failures)

    def test_rejects_source_script_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = root / "records.csv"
            evidence = root / "evidence.csv"
            row = record_row("1")
            row["notes"] = "source text אבג"
            write_records(records, [row])
            write_evidence(evidence, [evidence_row("1")])

            failures = check.validate_decision_records(records, evidence)

            self.assertIn(
                f"{records}:2 appears to contain source-script text",
                failures,
            )

    def test_unrecorded_row_cannot_select_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = root / "records.csv"
            evidence = root / "evidence.csv"
            write_records(
                records,
                [
                    record_row(
                        "1",
                        decision_status="unrecorded",
                        selected_action="source_row_lock_ready",
                    )
                ],
            )
            write_evidence(evidence, [evidence_row("1")])

            failures = check.validate_decision_records(records, evidence)

            self.assertIn(
                f"{records}:2 unrecorded row must not select an action",
                failures,
            )

    def test_deferred_status_must_use_deferred_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = root / "records.csv"
            evidence = root / "evidence.csv"
            write_records(
                records,
                [
                    record_row(
                        "1",
                        decision_status="deferred_no_lock",
                        selected_action="no_source_row_import",
                        evidence_citation=(
                            "reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/"
                            "page_images/cities_pdf_dp365a_p5_11_p003.png"
                        ),
                        evidence_summary=(
                            "Reviewed the page-image evidence and deferred this source-row "
                            "lock without importing or transcribing source text."
                        ),
                        locked_by="reviewer",
                        locked_at="2026-05-26",
                    )
                ],
            )
            write_evidence(evidence, [evidence_row("1")])

            failures = check.validate_decision_records(records, evidence)

            self.assertIn(
                f"{records}:2 deferred_no_lock row must select deferred_no_lock",
                failures,
            )


def record_row(
    rank: str,
    *,
    decision_status: str = "unrecorded",
    selected_action: str = "",
    evidence_citation: str = "",
    evidence_summary: str = "",
    locked_by: str = "",
    locked_at: str = "",
) -> dict[str, str]:
    return {
        "decision_id": f"cities_source_row_lock_{int(rank):03d}",
        "queue_lock_rank": rank,
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "decision_status": decision_status,
        "selected_action": selected_action,
        "evidence_citation": evidence_citation,
        "evidence_summary": evidence_summary,
        "locked_by": locked_by,
        "locked_at": locked_at,
        "notes": "test row",
    }


def evidence_row(rank: str) -> dict[str, str]:
    return {
        "evidence_rank": rank,
        "decision_id": f"cities_source_row_lock_{int(rank):03d}",
        "queue_lock_rank": rank,
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "family": "aumann_committee",
        "page_class": "table_candidate_page",
        "visual_page_role": "prose_with_source_table_page",
        "source_url": "https://example.test/source.pdf",
        "selected_source": "archive",
        "selected_path": "reports/source.pdf",
        "source_sha256": "abc123",
        "pdf_pages": "7",
        "page_image_path": "reports/page.png",
        "record_decision_status": "unrecorded",
        "record_selected_action": "",
        "evidence_prompt": "cite evidence",
        "evidence_required": "verify evidence",
        "source_row_use": "no_source_row_use",
        "current_decision": "no_source_row_import",
        "claim_boundary": "diagnostic evidence packet only",
    }


def write_records(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_evidence(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0])
    for index in range(len(rows) + 1, 15):
        rows.append(evidence_row(str(index)))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
