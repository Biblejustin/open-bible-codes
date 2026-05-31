from types import SimpleNamespace

from scripts import analyze_kjva_open_bibles_candidate_source as analyzer


def _args() -> SimpleNamespace:
    return SimpleNamespace(repo_api=analyzer.REPO_API)


def test_analyze_metadata_marks_kjv_only_status() -> None:
    repo = analyzer.JsonFetch(status="fetched", data={"default_branch": "master", "license": None})
    tree = analyzer.JsonFetch(
        status="fetched",
        data={
            "truncated": False,
            "tree": [
                {"path": "eng-kjv.osis.xml", "type": "blob"},
                {"path": "README.md", "type": "blob"},
            ],
        },
    )
    readme = analyzer.JsonFetch(
        status="fetched",
        data={
            "sha": "abc",
            "content": "ZW5nLWtqdi5vc2lzLnhtbCBQdWJsaWMgRG9tYWlu",
        },
    )

    row = analyzer.analyze_metadata(_args(), repo, tree, readme, "master")

    assert row["source_audit_status"] == "kjv_only_not_kjva_source_candidate"
    assert row["kjv_path_count"] == 1
    assert row["apocrypha_path_count"] == 0
    assert row["verse_numbered_import_ready"] is False


def test_analyze_metadata_detects_possible_apocrypha_candidate() -> None:
    repo = analyzer.JsonFetch(status="fetched", data={"default_branch": "master"})
    tree = analyzer.JsonFetch(
        status="fetched",
        data={"tree": [{"path": "eng-kjv-apocrypha.osis.xml", "type": "blob"}]},
    )
    readme = analyzer.JsonFetch(status="fetched", data={"content": ""})

    row = analyzer.analyze_metadata(_args(), repo, tree, readme, "master")

    assert row["source_audit_status"] == "possible_kjva_candidate_needs_text_audit"
    assert row["apocrypha_path_count"] == 1
    assert row["result_ready_status"] == "not_result_ready"


def test_build_summary_keeps_non_result_boundary() -> None:
    row = {
        "repo_fetch_status": "fetched",
        "tree_fetch_status": "fetched",
        "readme_fetch_status": "fetched",
        "kjv_path_count": 1,
        "apocrypha_path_count": 0,
        "deuterocanon_path_count": 0,
        "verse_numbered_import_ready": False,
        "result_ready_status": "not_result_ready",
    }

    summary = analyzer.build_summary([row])

    assert summary["metadata_fetches_ok"] == 1
    assert summary["kjv_paths"] == 1
    assert summary["apocrypha_paths"] == 0
    assert summary["result_ready_pages"] == 0
    assert summary["claim_status"] == "source_status_only_not_result_bearing"
