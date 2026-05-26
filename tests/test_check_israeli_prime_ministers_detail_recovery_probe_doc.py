import csv
import json
from pathlib import Path

from scripts import check_israeli_prime_ministers_detail_recovery_probe_doc as check


def test_current_israeli_prime_ministers_detail_recovery_doc_passes() -> None:
    assert check.validate_detail_recovery_doc(check.DEFAULT_DOC) == []


def test_missing_israeli_prime_ministers_detail_recovery_doc_fails(tmp_path) -> None:
    failures = check.validate_detail_recovery_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_incomplete_israeli_prime_ministers_detail_recovery_doc_fails(tmp_path) -> None:
    doc = tmp_path / "probe.md"
    doc.write_text("# Israeli Prime Ministers Detail Recovery Probe\n", encoding="utf-8")

    failures = check.validate_detail_recovery_doc(doc)

    assert any("missing phrase" in failure for failure in failures)
    assert any("missing probe pages" in failure for failure in failures)


def test_validate_israeli_detail_recovery_accepts_matching_data(tmp_path) -> None:
    paths = _paths(tmp_path)
    failures = check.validate_detail_recovery_doc(
        _doc(tmp_path),
        rows=_rows_csv(paths["rows"]),
        summary=_summary_csv(paths["summary"]),
        manifest=_manifest(paths),
    )

    assert failures == []


def test_validate_israeli_detail_recovery_rejects_row_drift(tmp_path) -> None:
    paths = _paths(tmp_path)
    failures = check.validate_detail_recovery_doc(
        _doc(tmp_path),
        rows=_rows_csv(paths["rows"], bad_page="9"),
        summary=_summary_csv(paths["summary"]),
        manifest=_manifest(paths),
    )

    assert any("page 9 expected_title_present drifted" in failure for failure in failures)


def test_validate_israeli_detail_recovery_rejects_summary_drift(tmp_path) -> None:
    paths = _paths(tmp_path)
    failures = check.validate_detail_recovery_doc(
        _doc(tmp_path),
        rows=_rows_csv(paths["rows"]),
        summary=_summary_csv(paths["summary"], bad_key="usable_detail_pages"),
        manifest=_manifest(paths),
    )

    assert any("usable_detail_pages drifted" in failure for failure in failures)


def test_validate_israeli_detail_recovery_rejects_manifest_drift(tmp_path) -> None:
    paths = _paths(tmp_path)
    failures = check.validate_detail_recovery_doc(
        _doc(tmp_path),
        rows=_rows_csv(paths["rows"]),
        summary=_summary_csv(paths["summary"]),
        manifest=_manifest(paths, bad_claim=True),
    )

    assert any("claim_boundary drifted" in failure for failure in failures)


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "doc": tmp_path / "ISRAELI_PRIME_MINISTERS_DETAIL_RECOVERY_PROBE.md",
        "rows": tmp_path / "detail_recovery_probe.csv",
        "summary": tmp_path / "detail_recovery_probe_summary.csv",
        "manifest": tmp_path / "detail_recovery_probe.manifest.json",
    }


def _doc(tmp_path: Path) -> Path:
    path = tmp_path / "ISRAELI_PRIME_MINISTERS_DETAIL_RECOVERY_PROBE.md"
    lines = list(check.REQUIRED_PHRASES)
    for page, title in check.EXPECTED_ROWS.items():
        lines.append(
            f"| {page} | {title} | 200 | True | True | False | True | "
            f"{check.EXPECTED_BYTES} | `{check.EXPECTED_SHA16}` | "
            "unrecovered_detail_page |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _rows_csv(path: Path, *, bad_page: str | None = None) -> Path:
    rows = []
    for page, title in check.EXPECTED_ROWS.items():
        snapshot = (
            "reports/israeli_prime_ministers_detail_recovery_probe/"
            f"snapshots/israeli_prime_ministers_{page}.html"
        )
        rows.append(
            {
                "page_index": page,
                "expected_title": title,
                "requested_url": (
                    "https://www.torah-code.org/experiments/"
                    f"israeli_prime_ministers_{page}.html"
                ),
                "final_url": check.EXPECTED_CANONICAL,
                "redirected": "True",
                "http_status": "200",
                "path": snapshot,
                "bytes": check.EXPECTED_BYTES,
                "sha256": check.EXPECTED_SHA256,
                "title": check.EXPECTED_TITLE,
                "canonical": check.EXPECTED_CANONICAL,
                "expected_title_present": "True" if page == bad_page else "False",
                "canonical_is_root": "True",
                "final_url_is_root": "True",
                "spam_marker_present": "True",
                "usable_status": "unrecovered_detail_page",
            }
        )
    return _write_csv(path, check.builder.ROW_FIELDNAMES, rows)


def _summary_csv(path: Path, *, bad_key: str | None = None) -> Path:
    row = dict(check.EXPECTED_SUMMARY)
    if bad_key is not None:
        row[bad_key] = "99"
    return _write_csv(path, check.builder.SUMMARY_FIELDNAMES, [row])


def _manifest(paths: dict[str, Path], *, bad_claim: bool = False) -> Path:
    paths["manifest"].write_text(
        json.dumps(
            {
                "tool": "build_israeli_prime_ministers_detail_recovery_probe.py",
                "rows": len(check.EXPECTED_ROWS),
                "summary": {
                    key: int(value) if value.isdigit() else value
                    for key, value in check.EXPECTED_SUMMARY.items()
                },
                "outputs": {
                    "csv": str(paths["rows"]),
                    "summary": str(paths["summary"]),
                    "markdown": str(paths["doc"]),
                    "manifest": str(paths["manifest"]),
                },
                "claim_boundary": (
                    "changed" if bad_claim else check.EXPECTED_CLAIM_BOUNDARY
                ),
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return paths["manifest"]


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path
