from types import SimpleNamespace

from scripts import analyze_kjva_crosswire_candidate_source as analyzer


def _args() -> SimpleNamespace:
    return SimpleNamespace(project_api=analyzer.PROJECT_API)


def test_analyze_metadata_marks_possible_kjva_candidate() -> None:
    project = analyzer.JsonFetch(status="fetched", data={"default_branch": "master"})
    tree = analyzer.JsonFetch(
        status="fetched",
        data={
            "items": [
                {"path": "README.md", "type": "blob"},
                {"path": "kjv.osis.xml", "type": "blob"},
                {"path": "kjva.osis.xml", "type": "blob"},
                {"path": "kjvdc.xml", "type": "blob"},
                {"path": "kjvfull2kjva.sh", "type": "blob"},
            ],
        },
    )
    readme = analyzer.JsonFetch(
        status="fetched",
        data={
            "blob_id": "abc",
            "size": 100,
            "content": "UGF0aHMga2p2ZGMueG1sIGtqdmEub3Npcy54bWwgUHVibGljIERvbWFpbg==",
        },
    )

    row = analyzer.analyze_metadata(_args(), project, tree, readme, "master")

    assert row["source_audit_status"] == "possible_independent_kjva_candidate_needs_text_audit"
    assert row["kjva_osis_path_present"] is True
    assert row["kjvdc_xml_path_present"] is True
    assert row["verse_numbered_import_ready"] is False
    assert row["source_lock_ready_status"] == "not_source_lock_ready"


def test_analyze_metadata_requires_kjva_and_kjvdc_paths() -> None:
    project = analyzer.JsonFetch(status="fetched", data={"default_branch": "master"})
    tree = analyzer.JsonFetch(
        status="fetched",
        data={"items": [{"path": "kjv.osis.xml", "type": "blob"}]},
    )
    readme = analyzer.JsonFetch(status="fetched", data={"content": ""})

    row = analyzer.analyze_metadata(_args(), project, tree, readme, "master")

    assert row["source_audit_status"] == "source_candidate_not_confirmed"
    assert row["result_ready_status"] == "not_result_ready"


def test_build_summary_keeps_non_result_boundary() -> None:
    row = {
        "project_fetch_status": "fetched",
        "tree_fetch_status": "fetched",
        "readme_fetch_status": "fetched",
        "source_audit_status": "possible_independent_kjva_candidate_needs_text_audit",
        "kjva_osis_path_present": True,
        "kjvdc_xml_path_present": True,
        "source_lock_ready_status": "not_source_lock_ready",
        "verse_numbered_import_ready": False,
        "result_ready_status": "not_result_ready",
    }

    summary = analyzer.build_summary([row])

    assert summary["metadata_fetches_ok"] == 1
    assert summary["possible_independent_kjva_candidates"] == 1
    assert summary["source_lock_ready_pages"] == 0
    assert summary["result_ready_pages"] == 0
    assert summary["claim_status"] == "source_status_only_not_result_bearing"
