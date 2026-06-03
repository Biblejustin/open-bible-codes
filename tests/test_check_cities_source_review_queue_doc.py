import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
import shutil
from pathlib import Path

from scripts import check_cities_source_review_queue_doc as check


def test_current_cities_source_review_queue_doc_passes() -> None:
    assert check.validate_cities_source_review_queue_doc(check.DEFAULT_DOC) == []


def test_detects_missing_boundary_phrase(tmp_path: Path) -> None:
    _, queue, summary, manifest = copy_current_outputs(tmp_path)
    doc = tmp_path / "queue.md"
    doc.write_text("# Cities Source Review Queue\n", encoding="utf-8")

    failures = check.validate_cities_source_review_queue_doc(
        doc,
        queue,
        summary,
        manifest,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_detects_lane_count_mismatch(tmp_path: Path) -> None:
    doc, queue, summary, manifest = copy_current_outputs(tmp_path)
    fieldnames, summary_rows = read_csv(summary)
    summary_rows[0]["rows"] = "99"
    write_csv(summary, fieldnames, summary_rows)

    failures = check.validate_cities_source_review_queue_doc(
        doc,
        queue,
        summary,
        manifest,
    )

    assert any("summary rows drifted" in failure for failure in failures)


def test_detects_queue_row_drift(tmp_path: Path) -> None:
    doc, queue, summary, manifest = copy_current_outputs(tmp_path)
    fieldnames, queue_rows = read_csv(queue)
    queue_rows[0]["lane"] = "recover_missing_pdf"
    write_csv(queue, fieldnames, queue_rows)

    failures = check.validate_cities_source_review_queue_doc(
        doc,
        queue,
        summary,
        manifest,
    )

    assert any("queue rows drifted" in failure for failure in failures)


def test_detects_queue_fieldname_drift(tmp_path: Path) -> None:
    doc, queue, summary, manifest = copy_current_outputs(tmp_path)
    fieldnames, queue_rows = read_csv(queue)
    write_csv(queue, fieldnames[:-1], [{k: v for k, v in row.items() if k != "claim_boundary"} for row in queue_rows])

    failures = check.validate_cities_source_review_queue_doc(
        doc,
        queue,
        summary,
        manifest,
    )

    assert any("fieldnames drifted" in failure for failure in failures)


def test_detects_manifest_drift(tmp_path: Path) -> None:
    doc, queue, summary, manifest = copy_current_outputs(tmp_path)
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["rows"]["queue"] = 99
    manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_cities_source_review_queue_doc(
        doc,
        queue,
        summary,
        manifest,
    )

    assert any("rows drifted" in failure for failure in failures)


def copy_current_outputs(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    doc = tmp_path / "queue.md"
    queue = tmp_path / "queue.csv"
    summary = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"
    shutil.copyfile(check.DEFAULT_DOC, doc)
    shutil.copyfile(check.DEFAULT_QUEUE, queue)
    shutil.copyfile(check.DEFAULT_SUMMARY, summary)
    shutil.copyfile(check.DEFAULT_MANIFEST, manifest)
    return doc, queue, summary, manifest


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
