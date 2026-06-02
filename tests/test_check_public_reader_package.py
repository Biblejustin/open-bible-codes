import json
from pathlib import Path

from scripts import build_public_reader_package as package
from scripts import check_project_findings_overview_doc as overview_check
from scripts import check_public_reader_package as check


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _default_doc_text(path: Path) -> str:
    if path == overview_check.DEFAULT_DOC:
        lines = ["# Open Bible Codes Findings Overview", ""]
        lines.extend(overview_check.REQUIRED_HEADINGS)
        lines.extend(overview_check.REQUIRED_PHRASES)
        lines.extend(f"`{reference}`" for reference in overview_check.REQUIRED_REFERENCES)
        lines.extend(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH[path])
        return "\n\n".join(lines) + "\n"
    if path == overview_check.DEFAULT_README:
        return (
            "# README\n\n"
            "Reader path:\n\n"
            "- start here: `docs/START_HERE.md`\n"
            + "\n".join(
                f"- {phrase}" for phrase in overview_check.READER_PATH_REQUIREMENTS[path]
            )
            + "\nreads 4 candidate-source audit rows with 0 verse-import-ready "
            "candidate pages and 0 result-ready candidate pages, records result "
            "allowed 0\n"
            + "\n"
        )
    if path == overview_check.DEFAULT_START_HERE:
        return (
            "# Start Here\n\n"
            + "\n".join(overview_check.READER_PATH_REQUIREMENTS[path])
            + "\n"
        )
    if path == Path("docs/FINAL_REPORT.md"):
        return (
            "# Final Report\n\n"
            "## Reader Path\n\n"
            "Read `docs/START_HERE.md`, then `docs/PROJECT_FINDINGS_OVERVIEW.md`.\n"
            "Use `docs/REMAINING_WORK_REGISTER.md`, "
            "`docs/WRR_NO_INPUT_HANDOFF_STATUS.md`, "
            "`docs/KJVA_NO_INPUT_HANDOFF_STATUS.md`, and "
            "`docs/CITIES_NO_INPUT_HANDOFF_STATUS.md`.\n"
            + "\n".join(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH[path])
            + "\n"
        )
    if path == Path("docs/REAL_REPORT_RUN.md"):
        return (
            "# Real Report Run\n\n"
            "Reader role: use `docs/START_HERE.md` and `docs/FINAL_REPORT.md`.\n"
            + "\n\n".join(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH[path])
            + "\n"
        )
    if path in check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH:
        return (
            f"# {path.name}\n\n"
            + "\n\n".join(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH[path])
            + "\n"
        )
    return f"# {path.name}\n\nbody\n"


def _default_report_text(path: Path) -> str:
    if path == Path("reports/real_report_run/summary.md"):
        return (
            "# report\n\n"
            + "\n\n".join(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH[path])
            + "\n"
        )
    if path == Path("reports/real_report_run/preflight.json"):
        return json.dumps(
            {
                "status": "passed",
                "allow_dirty": False,
                "git_status_lines": [],
                "risky_tracked_paths": [],
                "git_remotes": [
                    "origin\thttps://github.com/Biblejustin/open-bible-codes.git (fetch)"
                ],
                "git_commit": check.builder.git_head()[:7],
            },
            indent=2,
        ) + "\n"
    if path == Path("reports/real_report_run/manifest.json"):
        return json.dumps(
            {
                **check.REQUIRED_REAL_REPORT_MANIFEST_FIELDS,
                "commit": check.builder.git_head()[:7],
            },
            indent=2,
        ) + "\n"
    if path == Path("reports/real_report_run/protocol_run.manifest.json"):
        steps = [
            {
                "id": step_id,
                "return_code": 0,
                "skipped": step_id not in {"preflight", "real_report_summary"},
            }
            for step_id in check.REQUIRED_REAL_REPORT_PROTOCOL_STEP_IDS
        ]
        for step in steps:
            if step["id"] != "real_report_summary":
                continue
            step["inputs"] = [
                "reports/wrr_1994/wrr_no_input_handoff_status_summary.csv",
                "reports/wrr_1994/wrr_no_input_handoff_status.manifest.json",
                "reports/cities_no_input_handoff_status/summary.csv",
                "reports/cities_no_input_handoff_status/manifest.json",
                "reports/kjva_no_input_handoff_status/summary.csv",
                "reports/kjva_no_input_handoff_status/manifest.json",
                "reports/external_claim_source_counts/summary.csv",
                "reports/external_claim_source_counts/summary.manifest.json",
                "reports/external_claim_source_all_codes/surface_all_codes_summary.csv",
                "reports/external_claim_source_all_codes/summary.manifest.json",
                "reports/external_claim_source_all_codes/triage_queue.csv",
                "reports/external_claim_source_all_codes/triage.manifest.json",
                "reports/external_claim_source_all_codes/findings.manifest.json",
            ]
            step["outputs"] = [
                "reports/real_report_run/summary.md",
                "reports/real_report_run/manifest.json",
            ]
        return json.dumps(
            {
                "tool": "run_protocol",
                "protocol": "real_report_run",
                "status": "success",
                "dry_run": False,
                "steps": steps,
            },
            indent=2,
        ) + "\n"
    if path.suffix == ".md":
        return "# report\n\nbody\n"
    return "{}\n"


def _build_package(root: Path, monkeypatch) -> Path:
    monkeypatch.chdir(root)
    for path in package.DEFAULT_DOC_PATHS:
        _write(path, _default_doc_text(path))
    for path in package.DEFAULT_REPORT_PATHS:
        _write(path, _default_report_text(path))
    out_dir = Path("reports/public_reader_package")
    package.build_public_reader_package(out_dir=out_dir)
    return out_dir


def test_generated_public_reader_package_passes(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)

    assert check.validate_public_reader_package(out_dir) == []


def test_detects_manifest_hash_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    (out_dir / "docs/START_HERE.md").write_text("# changed\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert any("sha256 drifted" in failure for failure in failures)
    assert any("byte count drifted" in failure for failure in failures)


def test_detects_manifest_file_count_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["file_count"] = 999
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert any("file_count drifted" in failure for failure in failures)


def test_detects_non_object_package_manifest(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest_path.write_text("[]\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert failures == [f"{manifest_path} JSON root must be an object"]


def test_detects_manifest_git_head_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["git_head"] = "stale"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert any(
        "package_manifest.json git_head drifted: stale !=" in failure
        for failure in failures
    )


def test_detects_packaged_real_report_summary_commit_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    full_head = "abcdef0123456789abcdef0123456789abcdef01"
    monkeypatch.setattr(check.builder, "git_head", lambda: full_head)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["git_head"] = full_head
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{out_dir}/reports/real_report_run/summary.md commit stamp drifted: "
        "expected Commit: `abcdef0`"
    ) in failures


def test_detects_packaged_real_report_manifest_commit_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    full_head = "abcdef0123456789abcdef0123456789abcdef01"
    monkeypatch.setattr(check.builder, "git_head", lambda: full_head)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["git_head"] = full_head
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{out_dir}/reports/real_report_run/manifest.json commit stamp drifted: "
        " != abcdef0"
    ) in failures


def test_detects_non_object_packaged_real_report_manifest(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    manifest_path.write_text("[]\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert f"{manifest_path} JSON root must be an object" in failures


def test_detects_packaged_real_report_manifest_result_boundary_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["kjva_no_input_handoff_result_allowed"] = "1"
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{manifest_path} kjva_no_input_handoff_result_allowed drifted: 1 != 0"
    ) in failures


def test_detects_packaged_real_report_manifest_cities_boundary_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["cities_no_input_handoff_result_allowed"] = "1"
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{manifest_path} cities_no_input_handoff_result_allowed drifted: 1 != 0"
    ) in failures


def test_detects_packaged_real_report_manifest_external_claim_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["external_claim_all_codes_triage_rows"] = 925
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{manifest_path} external_claim_all_codes_triage_rows drifted: 925 != 926"
    ) in failures


def test_detects_packaged_real_report_manifest_step_tahot_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["step_tahot"]["real_counts"]["source_only"] = 464
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert any(
        failure.startswith(f"{manifest_path} step_tahot drifted:")
        for failure in failures
    )


def test_detects_packaged_real_report_manifest_unguarded_key(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["new_result_rows"] = 1
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{manifest_path} has unguarded real-report manifest key: new_result_rows"
    ) in failures


def test_detects_packaged_real_report_manifest_all_codes_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["all_codes_followup_letter_path_mismatches"] = 1
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{manifest_path} all_codes_followup_letter_path_mismatches drifted: 1 != 0"
    ) in failures


def test_detects_packaged_real_report_manifest_greek_surface_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["surface_queue_pattern_rows"] = 160
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{manifest_path} surface_queue_pattern_rows drifted: 160 != 161"
    ) in failures


def test_detects_packaged_real_report_manifest_wrr_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["wrr_pair_audit_len_5_8_rows"] = 21
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{manifest_path} wrr_pair_audit_len_5_8_rows drifted: 21 != 22"
    ) in failures


def test_detects_packaged_real_report_manifest_centered_occurrence_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["centered_occurrence_presence_rows"] = 811
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{manifest_path} centered_occurrence_presence_rows drifted: 811 != 812"
    ) in failures


def test_detects_packaged_real_report_manifest_matrix_summary_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["matrix_cluster_term_pair_control_rows"] = 94
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{manifest_path} matrix_cluster_term_pair_control_rows drifted: 94 != 95"
    ) in failures


def test_detects_packaged_real_report_manifest_kjva_bridge_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "reports/real_report_run/manifest.json"
    report_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_manifest["kjva_apocrypha_bridge_prospective_terms_q_le_0_05"] = 1
    manifest_path.write_text(
        json.dumps(report_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{manifest_path} kjva_apocrypha_bridge_prospective_terms_q_le_0_05 "
        "drifted: 1 != 0"
    ) in failures


def test_detects_packaged_real_report_preflight_status_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    preflight_path = out_dir / "reports/real_report_run/preflight.json"
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    preflight["status"] = "failed"
    preflight_path.write_text(json.dumps(preflight, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{preflight_path} status drifted: failed != passed"
    ) in failures


def test_detects_packaged_real_report_protocol_manifest_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    protocol_path = out_dir / "reports/real_report_run/protocol_run.manifest.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    protocol["steps"][0]["skipped"] = True
    protocol_path.write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert f"{protocol_path} preflight step did not run cleanly" in failures


def test_detects_packaged_real_report_protocol_missing_current_step(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    protocol_path = out_dir / "reports/real_report_run/protocol_run.manifest.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    missing_step = "greek_surface_length4_followup"
    protocol["steps"] = [
        step for step in protocol["steps"] if step["id"] != missing_step
    ]
    protocol_path.write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert f"{protocol_path} missing protocol step: {missing_step}" in failures


def test_detects_packaged_real_report_protocol_unexpected_step(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    protocol_path = out_dir / "reports/real_report_run/protocol_run.manifest.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    protocol["steps"].append({"id": "stale_removed_step", "return_code": 0})
    protocol_path.write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{protocol_path} has unexpected protocol step: stale_removed_step"
        in failures
    )


def test_detects_packaged_real_report_protocol_duplicate_step(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    protocol_path = out_dir / "reports/real_report_run/protocol_run.manifest.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    protocol["steps"].append(dict(protocol["steps"][0]))
    protocol_path.write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert f"{protocol_path} has duplicate protocol step: preflight" in failures


def test_reports_invalid_real_report_protocol_source_toml(tmp_path) -> None:
    protocol_path = tmp_path / "real_report_run.toml"
    _write(protocol_path, "[[steps]\nid = 'ok'\n[[steps]\n")

    step_ids, failures = check._load_real_report_protocol_requirements(protocol_path)

    assert step_ids == ()
    assert len(failures) == 1
    assert str(protocol_path) in failures[0]
    assert "invalid TOML" in failures[0]


def test_reports_malformed_real_report_protocol_source_steps(tmp_path) -> None:
    protocol_path = tmp_path / "real_report_run.toml"
    _write(protocol_path, 'steps = "not-a-list"\n')

    step_ids, failures = check._load_real_report_protocol_requirements(protocol_path)

    assert step_ids == ()
    assert failures == (f"{protocol_path} steps must be a list",)


def test_detects_packaged_real_report_protocol_manifest_summary_input_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    protocol_path = out_dir / "reports/real_report_run/protocol_run.manifest.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    for step in protocol["steps"]:
        if step["id"] == "real_report_summary":
            step["inputs"] = []
            break
    protocol_path.write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{protocol_path} real_report_summary missing no-input handoff inputs"
        in failures
    )


def test_detects_packaged_real_report_protocol_manifest_lineage_step_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    protocol_path = out_dir / "reports/real_report_run/protocol_run.manifest.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    for step in protocol["steps"]:
        if step["id"] == "external_claim_source_counts":
            step["return_code"] = 1
            break
    protocol_path.write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert f"{protocol_path} external_claim_source_counts step failed" in failures


def test_detects_packaged_real_report_protocol_manifest_external_claim_input_drift(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    protocol_path = out_dir / "reports/real_report_run/protocol_run.manifest.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    for step in protocol["steps"]:
        if step["id"] == "real_report_summary":
            step["inputs"] = [
                value
                for value in step["inputs"]
                if not str(value).startswith("reports/external_claim_source")
            ]
            break
    protocol_path.write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert (
        f"{protocol_path} real_report_summary missing external-claim inputs"
        in failures
    )


def test_detects_missing_required_manifest_source(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"] = [
        item
        for item in manifest["files"]
        if item["source"] != "docs/CLAIM_CATALOG.md"
    ]
    manifest["file_count"] = len(manifest["files"])
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert (
        "required package source missing from manifest: docs/CLAIM_CATALOG.md"
        in failures
    )


def test_detects_missing_required_packaged_phrase_for_each_guarded_doc(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    for relative_path, required_phrases in check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH.items():
        package_path = out_dir / relative_path
        original = package_path.read_text(encoding="utf-8")
        package_path.write_text("# stale\n", encoding="utf-8")

        failures = check.validate_public_reader_package(out_dir)

        for phrase in required_phrases:
            assert f"{package_path} missing packaged phrase: {phrase}" in failures
        package_path.write_text(original, encoding="utf-8")


def test_detects_default_doc_without_packaged_phrase_guard(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    guarded = dict(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH)
    guarded.pop(Path("docs/CRITICAL_OMISSION_BREAKS_NULL.md"))
    monkeypatch.setattr(check, "REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH", guarded)

    failures = check.validate_public_reader_package(out_dir)

    assert (
        "default package doc lacks required phrase guard: "
        "docs/CRITICAL_OMISSION_BREAKS_NULL.md"
    ) in failures


def test_detects_packaged_phrase_guard_path_not_in_manifest(
    tmp_path,
    monkeypatch,
) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    guarded = dict(check.REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH)
    guarded[Path("docs/MISSING_FROM_PACKAGE.md")] = ("required phrase",)
    monkeypatch.setattr(check, "REQUIRED_PACKAGED_PHRASES_BY_PACKAGE_PATH", guarded)

    failures = check.validate_public_reader_package(out_dir)

    assert (
        "required packaged phrase guard path not in manifest: "
        "docs/MISSING_FROM_PACKAGE.md"
    ) in failures


def test_detects_missing_packaged_file(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    (out_dir / "docs/START_HERE.md").unlink()

    failures = check.validate_public_reader_package(out_dir)

    assert any("docs/START_HERE.md is missing" in failure for failure in failures)


def test_detects_unsafe_manifest_package_path(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][0]["package_path"] = "../outside.md"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert any(
        "unsafe manifest package path: ../outside.md" in failure
        for failure in failures
    )


def test_detects_manifest_package_mapping_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][0]["package_path"] = "README.md"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert any(
        "manifest package path does not match source mapping: "
        "README.md -> README.md (expected docs/REPOSITORY_README.md)" in failure
        for failure in failures
    )


def test_detects_unmanifested_extra_file(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    _write(out_dir / "stale_extra.md", "# stale\n")

    failures = check.validate_public_reader_package(out_dir)

    assert "unexpected package file: stale_extra.md" in failures


def test_detects_unsafe_manifest_source_path(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][0]["source"] = "../outside.md"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert "unsafe manifest source path: ../outside.md" in failures


def test_detects_forbidden_manifest_source_path(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    manifest_path = out_dir / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][0]["source"] = "data/raw/source.md"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_public_reader_package(out_dir)

    assert "forbidden manifest source path: data/raw/source.md" in failures


def test_detects_package_readme_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    readme = out_dir / "README.md"
    text = readme.read_text(encoding="utf-8")
    readme.write_text(
        text.replace("Package files:", "Package file list:"),
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert f"{readme} content drifted from manifest" in failures


def test_detects_reader_package_drift(tmp_path, monkeypatch) -> None:
    out_dir = _build_package(tmp_path, monkeypatch)
    reader_package = out_dir / "reader_package.md"
    text = reader_package.read_text(encoding="utf-8")
    reader_package.write_text(
        text.replace("Source: `docs/START_HERE.md`", "Source: `docs/MISSING.md`"),
        encoding="utf-8",
    )

    failures = check.validate_public_reader_package(out_dir)

    assert f"{reader_package} content drifted from package files" in failures
