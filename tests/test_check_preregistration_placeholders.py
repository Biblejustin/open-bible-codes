from scripts import check_preregistration_placeholders as check


def test_find_placeholders_reports_line_and_column(tmp_path) -> None:
    prereg = tmp_path / "study.md"
    prereg.write_text("Study name | `[name]`\nSkip range | `2..50`\n", encoding="utf-8")

    hits = check.find_placeholders(prereg, allowed=set())

    assert len(hits) == 1
    assert hits[0].line_number == 1
    assert hits[0].placeholder == "[name]"


def test_find_placeholders_honors_allow_list(tmp_path) -> None:
    prereg = tmp_path / "study.md"
    prereg.write_text("Expected output: reports/[name]/[output].csv\n", encoding="utf-8")

    hits = check.find_placeholders(prereg, allowed={"[output]"})

    assert [hit.placeholder for hit in hits] == ["[name]"]


def test_find_placeholders_ignores_markdown_task_markers(tmp_path) -> None:
    prereg = tmp_path / "study.md"
    prereg.write_text("- [x] Locked\n- [ ] Reviewer sign-off pending\n", encoding="utf-8")

    hits = check.find_placeholders(prereg, allowed=set())

    assert hits == []


def test_main_fails_for_unresolved_placeholders(tmp_path, capsys) -> None:
    prereg = tmp_path / "study.md"
    prereg.write_text("Protocol: `protocols/[protocol].toml`\n", encoding="utf-8")

    code = check.main([str(prereg)])

    assert code == 1
    assert "[protocol]" in capsys.readouterr().out


def test_main_fails_for_stale_template_phrases(tmp_path, capsys) -> None:
    prereg = tmp_path / "study.md"
    prereg.write_text("Status: template; copy before use.\n", encoding="utf-8")

    code = check.main([str(prereg)])

    out = capsys.readouterr().out
    assert code == 1
    assert "stale preregistration template phrase" in out
    assert "Status: template" in out


def test_main_passes_without_placeholders(tmp_path, capsys) -> None:
    prereg = tmp_path / "study.md"
    prereg.write_text("Protocol: `protocols/fixed.toml`\n", encoding="utf-8")

    code = check.main([str(prereg)])

    assert code == 0
    assert "ok" in capsys.readouterr().out
