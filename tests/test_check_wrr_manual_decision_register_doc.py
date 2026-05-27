import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_manual_decision_register_doc as check


class WrrManualDecisionRegisterDocTests(unittest.TestCase):
    def test_validate_current_doc_passes(self) -> None:
        if not check.DEFAULT_DOC.exists():
            self.skipTest("generated doc not built yet")
        self.assertEqual(
            check.validate_manual_decision_register_doc(check.DEFAULT_DOC),
            [],
        )

    def test_validate_doc_requires_no_input_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "register.md"
            path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")

            self.assertEqual(
                check.validate_manual_decision_register_doc(
                    path,
                    register=None,
                    summary=None,
                ),
                [],
            )

    def test_validate_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "register.md"
            path.write_text("# WRR Manual Decision Register\n", encoding="utf-8")

            failures = check.validate_manual_decision_register_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])

    def test_validate_doc_reports_forbidden_decision_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "register.md"
            path.write_text(
                "\n".join(check.REQUIRED_PHRASES) + "\nselected correction\n",
                encoding="utf-8",
            )

            failures = check.validate_manual_decision_register_doc(path)

            self.assertEqual(
                failures,
                [f"{path} contains forbidden phrase: selected correction"],
            )

    def test_validate_doc_accepts_matching_csvs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            self.assertEqual(
                check.validate_manual_decision_register_doc(
                    doc,
                    register=_register_csv(root),
                    summary=_summary_csv(root),
                ),
                [],
            )

    def test_validate_doc_rejects_register_row_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_manual_decision_register_doc(
                doc,
                register=_register_csv(root, drop_last=True),
                summary=_summary_csv(root),
            )

            self.assertTrue(any("has 36 rows" in failure for failure in failures))

    def test_validate_doc_rejects_register_state_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_manual_decision_register_doc(
                doc,
                register=_register_csv(root, bad_state_rank=1),
                summary=_summary_csv(root),
            )

            self.assertTrue(any("review_state" in failure for failure in failures))

    def test_validate_doc_rejects_summary_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_manual_decision_register_doc(
                doc,
                register=_register_csv(root),
                summary=_summary_csv(root, bad_lane="method_pair_universe"),
            )

            self.assertTrue(
                any("method_pair_universe action_terms" in failure for failure in failures)
            )

    def test_validate_doc_rejects_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            payload = json.loads(check.DEFAULT_MANIFEST.read_text(encoding="utf-8"))
            payload["rows"] = 99
            manifest.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            failures = check.validate_manual_decision_register_doc(
                check.DEFAULT_DOC,
                register=None,
                summary=None,
                manifest=manifest,
            )

            self.assertTrue(any("rows drifted" in failure for failure in failures))


def _required_doc(root: Path) -> Path:
    path = root / "register.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")
    return path


def _register_csv(
    root: Path,
    *,
    drop_last: bool = False,
    bad_state_rank: int | None = None,
) -> Path:
    path = root / "register.csv"
    fieldnames = [
        "decision_rank",
        "decision_lane",
        "review_state",
        "decision_target",
        "concept",
        "row_number",
        "term_id",
        "term",
        "action_terms",
        "residual_pairs",
        "frontier_pairs",
        "required_decision_record",
        "source_checklist",
        "no_input_boundary",
        "allowed_without_input",
        "next_manual_action",
    ]
    rows: list[dict[str, str]] = []
    rank = 1
    for lane, locks in check.LANE_LOCKS.items():
        decision_rows = int(locks["decision_rows"])
        metric_values = {
            metric: _distribute(int(locks[metric]), decision_rows)
            for metric in ("action_terms", "residual_pairs", "frontier_pairs")
        }
        for offset in range(decision_rows):
            rows.append(
                {
                    "decision_rank": str(rank),
                    "decision_lane": lane,
                    "review_state": str(locks["review_state"]),
                    "decision_target": f"{lane} target {offset}",
                    "concept": f"WRR2 {rank:02d}",
                    "row_number": f"{rank:02d}",
                    "term_id": f"term_{rank:02d}",
                    "term": "TERM",
                    "action_terms": str(metric_values["action_terms"][offset]),
                    "residual_pairs": str(metric_values["residual_pairs"][offset]),
                    "frontier_pairs": str(metric_values["frontier_pairs"][offset]),
                    "required_decision_record": str(locks["required_decision_record"]),
                    "source_checklist": str(locks["source_checklist"]),
                    "no_input_boundary": check.NO_INPUT_BOUNDARY,
                    "allowed_without_input": check.ALLOWED_WITHOUT_INPUT,
                    "next_manual_action": "review",
                }
            )
            rank += 1
    if drop_last:
        rows = rows[:-1]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if bad_state_rank == int(row["decision_rank"]):
                row["review_state"] = "locked"
            writer.writerow(row)
    return path


def _summary_csv(root: Path, *, bad_lane: str | None = None) -> Path:
    path = root / "summary.csv"
    fieldnames = [
        "decision_lane",
        "decision_rows",
        "action_terms",
        "residual_pairs",
        "frontier_pairs",
        "review_state",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for lane, locks in check.LANE_LOCKS.items():
            action_terms = int(locks["action_terms"])
            if lane == bad_lane:
                action_terms += 1
            writer.writerow(
                {
                    "decision_lane": lane,
                    "decision_rows": str(locks["decision_rows"]),
                    "action_terms": str(action_terms),
                    "residual_pairs": str(locks["residual_pairs"]),
                    "frontier_pairs": str(locks["frontier_pairs"]),
                    "review_state": str(locks["review_state"]),
                }
            )
    return path


def _distribute(total: int, count: int) -> list[int]:
    base, remainder = divmod(total, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]


if __name__ == "__main__":
    unittest.main()
