import json
import tempfile
import unittest
from pathlib import Path

from els.protocol_runner import (
    expanded_input_paths,
    format_parallel_progress,
    load_protocol,
    normalize_python_argv,
    progress_interval_seconds,
    run_protocol,
    step_outputs_exist,
)


class ProtocolRunnerTests(unittest.TestCase):
    def test_normalize_python_argv_converts_scripts_to_modules(self) -> None:
        self.assertEqual(
            normalize_python_argv(["scripts/analyze_word_counts.py", "--flag"]),
            ["-m", "scripts.analyze_word_counts", "--flag"],
        )

    def test_normalize_python_argv_leaves_other_commands(self) -> None:
        self.assertEqual(
            normalize_python_argv(["-m", "els", "stats"]),
            ["-m", "els", "stats"],
        )

    def test_format_parallel_progress_orders_active_steps(self) -> None:
        self.assertEqual(
            format_parallel_progress([("beta", 2.25), ("alpha", 1.0)]),
            "== progress active: alpha 1.0s, beta 2.2s ==",
        )

    def test_progress_interval_defaults_and_validates(self) -> None:
        self.assertEqual(progress_interval_seconds({}), 30.0)
        self.assertEqual(progress_interval_seconds({"progress_interval_seconds": 0}), 0.0)
        with self.assertRaises(ValueError):
            progress_interval_seconds({"progress_interval_seconds": -1})

    def test_load_protocol_validates_steps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "protocol.toml"
            path.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        "",
                        "[[steps]]",
                        'id = "one"',
                        'argv = ["-c", "print(1)"]',
                    ]
                ),
                encoding="utf-8",
            )

            protocol = load_protocol(path)

        self.assertEqual(protocol["name"], "sample")
        self.assertEqual(protocol["steps"][0]["id"], "one")

    def test_load_protocol_validates_boolean_step_flags(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for flag in ("always_run", "allow_failure", "python"):
                path = root / f"{flag}.toml"
                path.write_text(
                    "\n".join(
                        [
                            'name = "sample"',
                            "",
                            "[[steps]]",
                            'id = "one"',
                            'argv = ["-c", "print(1)"]',
                            f'{flag} = "false"',
                        ]
                    ),
                    encoding="utf-8",
                )
                with self.subTest(flag=flag):
                    with self.assertRaisesRegex(ValueError, f"{flag} must be a boolean"):
                        load_protocol(path)

    def test_run_protocol_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            protocol_path = root / "protocol.toml"
            protocol_path.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        f'manifest_out = "{manifest}"',
                        "",
                        "[[steps]]",
                        'id = "one"',
                        'argv = ["-c", "print(1)"]',
                    ]
                ),
                encoding="utf-8",
            )

            exit_code = run_protocol(protocol_path)
            data = json.loads(manifest.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["steps"][0]["id"], "one")
        self.assertIn("duration_seconds", data)
        self.assertEqual(data["timing_summary"]["ran_steps"], 1)
        self.assertEqual(data["timing_summary"]["skipped_steps"], 0)
        self.assertEqual(data["timing_summary"]["slowest_steps"][0]["id"], "one")

    def test_run_protocol_resume_skips_existing_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "out.txt"
            manifest = root / "manifest.json"
            protocol_path = root / "protocol.toml"
            code = (
                "from pathlib import Path; "
                f"Path({str(existing)!r}).write_text('already here', encoding='utf-8')"
            )
            protocol_path.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        f'manifest_out = "{manifest}"',
                        "",
                        "[[steps]]",
                        'id = "one"',
                        f'argv = ["-c", {json.dumps(code)}]',
                        f'outputs = ["{existing}"]',
                    ]
                ),
                encoding="utf-8",
            )

            existing.write_text("already here", encoding="utf-8")
            run_protocol(protocol_path)
            exit_code = run_protocol(protocol_path, resume=True)
            data = json.loads(manifest.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertTrue(data["steps"][0]["skipped"])
        self.assertEqual(data["timing_summary"]["ran_steps"], 0)
        self.assertEqual(data["timing_summary"]["skipped_steps"], 1)

    def test_run_protocol_always_run_ignores_resume_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "out.txt"
            counter = root / "counter.txt"
            manifest = root / "manifest.json"
            protocol_path = root / "protocol.toml"
            code = (
                "from pathlib import Path; "
                f"counter = Path({str(counter)!r}); "
                "count = int(counter.read_text(encoding='utf-8')) if counter.exists() else 0; "
                "counter.write_text(str(count + 1), encoding='utf-8'); "
                f"Path({str(output)!r}).write_text(str(count + 1), encoding='utf-8')"
            )
            protocol_path.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        f'manifest_out = "{manifest}"',
                        "",
                        "[[steps]]",
                        'id = "one"',
                        "always_run = true",
                        f'argv = ["-c", {json.dumps(code)}]',
                        f'outputs = ["{output}"]',
                    ]
                ),
                encoding="utf-8",
            )

            first_exit_code = run_protocol(protocol_path, resume=True)
            second_exit_code = run_protocol(protocol_path, resume=True)
            data = json.loads(manifest.read_text(encoding="utf-8"))
            final_counter = counter.read_text(encoding="utf-8")

        self.assertEqual(first_exit_code, 0)
        self.assertEqual(second_exit_code, 0)
        self.assertFalse(data["steps"][0]["skipped"])
        self.assertTrue(data["steps"][0]["always_run"])
        self.assertEqual(final_counter, "2")
        self.assertEqual(data["timing_summary"]["ran_steps"], 1)
        self.assertEqual(data["timing_summary"]["skipped_steps"], 0)

    def test_run_protocol_resume_requires_matching_integrity_stamp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "out.txt"
            counter = root / "counter.txt"
            manifest = root / "manifest.json"
            protocol_path = root / "protocol.toml"
            code = (
                "from pathlib import Path; "
                f"counter = Path({str(counter)!r}); "
                "count = int(counter.read_text(encoding='utf-8')) if counter.exists() else 0; "
                "counter.write_text(str(count + 1), encoding='utf-8'); "
                f"Path({str(output)!r}).write_text('complete', encoding='utf-8')"
            )
            protocol_path.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        f'manifest_out = "{manifest}"',
                        "",
                        "[[steps]]",
                        'id = "one"',
                        f'argv = ["-c", {json.dumps(code)}]',
                        f'outputs = ["{output}"]',
                    ]
                ),
                encoding="utf-8",
            )

            output.write_text("partial", encoding="utf-8")
            exit_code = run_protocol(protocol_path, resume=True)
            first_run = json.loads(manifest.read_text(encoding="utf-8"))

            second_exit_code = run_protocol(protocol_path, resume=True)
            second_run = json.loads(manifest.read_text(encoding="utf-8"))

            output.write_text("tampered", encoding="utf-8")
            third_exit_code = run_protocol(protocol_path, resume=True)
            third_run = json.loads(manifest.read_text(encoding="utf-8"))
            final_counter = counter.read_text(encoding="utf-8")
            final_output = output.read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertFalse(first_run["steps"][0]["skipped"])
        self.assertEqual(second_exit_code, 0)
        self.assertTrue(second_run["steps"][0]["skipped"])
        self.assertEqual(third_exit_code, 0)
        self.assertFalse(third_run["steps"][0]["skipped"])
        self.assertEqual(final_counter, "2")
        self.assertEqual(final_output, "complete")

    def test_run_protocol_resume_reruns_when_input_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "in.txt"
            output = root / "out.txt"
            counter = root / "counter.txt"
            manifest = root / "manifest.json"
            protocol_path = root / "protocol.toml"
            code = (
                "from pathlib import Path; "
                f"source = Path({str(input_path)!r}); "
                f"target = Path({str(output)!r}); "
                f"counter = Path({str(counter)!r}); "
                "count = int(counter.read_text(encoding='utf-8')) if counter.exists() else 0; "
                "counter.write_text(str(count + 1), encoding='utf-8'); "
                "target.write_text(source.read_text(encoding='utf-8'), encoding='utf-8')"
            )
            protocol_path.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        f'manifest_out = "{manifest}"',
                        "",
                        "[[steps]]",
                        'id = "one"',
                        f'argv = ["-c", {json.dumps(code)}]',
                        f'inputs = ["{input_path}"]',
                        f'outputs = ["{output}"]',
                    ]
                ),
                encoding="utf-8",
            )

            input_path.write_text("first", encoding="utf-8")
            first_exit_code = run_protocol(protocol_path, resume=True)
            run_protocol(protocol_path, resume=True)
            input_path.write_text("second", encoding="utf-8")
            third_exit_code = run_protocol(protocol_path, resume=True)
            data = json.loads(manifest.read_text(encoding="utf-8"))
            final_counter = counter.read_text(encoding="utf-8")
            final_output = output.read_text(encoding="utf-8")

        self.assertEqual(first_exit_code, 0)
        self.assertEqual(third_exit_code, 0)
        self.assertFalse(data["steps"][0]["skipped"])
        self.assertEqual(final_counter, "2")
        self.assertEqual(final_output, "second")

    def test_run_protocol_resume_reruns_when_corpus_source_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.csv"
            config = root / "corpus.toml"
            output = root / "out.txt"
            counter = root / "counter.txt"
            manifest = root / "manifest.json"
            protocol_path = root / "protocol.toml"
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'format = "csv"',
                        'path = "source.csv"',
                    ]
                ),
                encoding="utf-8",
            )
            code = (
                "from pathlib import Path; "
                f"source = Path({str(source)!r}); "
                f"target = Path({str(output)!r}); "
                f"counter = Path({str(counter)!r}); "
                "count = int(counter.read_text(encoding='utf-8')) if counter.exists() else 0; "
                "counter.write_text(str(count + 1), encoding='utf-8'); "
                "target.write_text(source.read_text(encoding='utf-8'), encoding='utf-8')"
            )
            protocol_path.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        f'manifest_out = "{manifest}"',
                        "",
                        "[[steps]]",
                        'id = "one"',
                        f'argv = ["-c", {json.dumps(code)}]',
                        f'inputs = ["{config}"]',
                        f'outputs = ["{output}"]',
                    ]
                ),
                encoding="utf-8",
            )

            source.write_text("first", encoding="utf-8")
            run_protocol(protocol_path, resume=True)
            run_protocol(protocol_path, resume=True)
            source.write_text("second", encoding="utf-8")
            run_protocol(protocol_path, resume=True)
            data = json.loads(manifest.read_text(encoding="utf-8"))
            final_counter = counter.read_text(encoding="utf-8")
            final_output = output.read_text(encoding="utf-8")

        self.assertFalse(data["steps"][0]["skipped"])
        self.assertEqual(final_counter, "2")
        self.assertEqual(final_output, "second")

    def test_expanded_input_paths_includes_corpus_source_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.csv"
            config = root / "corpus.toml"
            source.write_text("ref,book,chapter,verse,text\n", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'format = "csv"',
                        'path = "source.csv"',
                    ]
                ),
                encoding="utf-8",
            )

            paths = expanded_input_paths({"inputs": [str(config)]})

        self.assertEqual(paths, [str(config), str(source.resolve())])

    def test_run_protocol_fails_when_expected_output_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            missing = root / "missing.txt"
            manifest = root / "manifest.json"
            protocol_path = root / "protocol.toml"
            protocol_path.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        f'manifest_out = "{manifest}"',
                        "",
                        "[[steps]]",
                        'id = "one"',
                        'argv = ["-c", "print(1)"]',
                        f'outputs = ["{missing}"]',
                    ]
                ),
                encoding="utf-8",
            )

            exit_code = run_protocol(protocol_path)
            data = json.loads(manifest.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 2)
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["steps"][0]["return_code"], 2)

    def test_run_protocol_parallel_group_writes_manifest_in_step_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first.txt"
            second = root / "second.txt"
            manifest = root / "manifest.json"
            protocol_path = root / "protocol.toml"
            first_code = (
                "from pathlib import Path; "
                f"Path({str(first)!r}).write_text('1', encoding='utf-8')"
            )
            second_code = (
                "from pathlib import Path; "
                f"Path({str(second)!r}).write_text('2', encoding='utf-8')"
            )
            protocol_path.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        "max_parallel = 2",
                        f'manifest_out = "{manifest}"',
                        "",
                        "[[steps]]",
                        'id = "first"',
                        'parallel_group = "work"',
                        f'argv = ["-c", "{first_code}"]',
                        f'outputs = ["{first}"]',
                        "",
                        "[[steps]]",
                        'id = "second"',
                        'parallel_group = "work"',
                        f'argv = ["-c", "{second_code}"]',
                        f'outputs = ["{second}"]',
                    ]
                ),
                encoding="utf-8",
            )

            exit_code = run_protocol(protocol_path)
            data = json.loads(manifest.read_text(encoding="utf-8"))

            self.assertEqual(first.read_text(encoding="utf-8"), "1")
            self.assertEqual(second.read_text(encoding="utf-8"), "2")

        self.assertEqual(exit_code, 0)
        self.assertEqual([step["id"] for step in data["steps"]], ["first", "second"])
        self.assertEqual(data["steps"][0]["parallel_group"], "work")
        self.assertEqual(data["timing_summary"]["ran_steps"], 2)

    def test_step_outputs_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "out.txt"
            output.write_text("x", encoding="utf-8")

            self.assertTrue(step_outputs_exist({"outputs": [str(output)]}))
            self.assertFalse(step_outputs_exist({"outputs": [str(output) + ".missing"]}))


if __name__ == "__main__":
    unittest.main()
