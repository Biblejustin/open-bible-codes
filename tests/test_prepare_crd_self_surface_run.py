import tempfile
import tomllib
import unittest
from pathlib import Path

from scripts.classify_centered_relevance import sha256_file
from scripts.prepare_crd_self_surface_run import main as prepare_main


class PrepareCRDSelfSurfaceRunTests(unittest.TestCase):
    def test_prepare_writes_locked_local_run_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            terms_dir = root / "terms"
            terms_dir.mkdir()
            (terms_dir / "demo.csv").write_text(
                "term_id,concept,category,language,term,notes\n"
                "term,Term,example,english,ace,test\n",
                encoding="utf-8",
            )
            base_protocol = root / "base.toml"
            base_protocol.write_text(base_protocol_text(root), encoding="utf-8")
            out_dir = root / "reports" / "crd_self_surface"

            exit_code = prepare_main(
                [
                    "--terms-dir",
                    str(terms_dir),
                    "--base-protocol",
                    str(base_protocol),
                    "--out-dir",
                    str(out_dir),
                ]
            )
            protocol = tomllib.loads((out_dir / "protocol.toml").read_text(encoding="utf-8"))
            dictionary = out_dir / "relevance_dictionary_self_surface.toml"
            queue_text = (out_dir / "relevance_review_queue.csv").read_text(encoding="utf-8")

            self.assertEqual(exit_code, 0)
            self.assertEqual(protocol["term_file"], str(out_dir / "terms_combined.csv"))
            self.assertEqual(protocol["relevance_dictionary_sha256"], sha256_file(dictionary))
            self.assertIn("ace", queue_text)

    def test_prepare_reports_invalid_base_protocol_toml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            terms_dir = root / "terms"
            terms_dir.mkdir()
            (terms_dir / "demo.csv").write_text(
                "term_id,concept,category,language,term,notes\n"
                "term,Term,example,english,ace,test\n",
                encoding="utf-8",
            )
            base_protocol = root / "base.toml"
            base_protocol.write_text("[broken\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "invalid TOML"):
                prepare_main(
                    [
                        "--terms-dir",
                        str(terms_dir),
                        "--base-protocol",
                        str(base_protocol),
                        "--out-dir",
                        str(root / "reports" / "crd_self_surface"),
                    ]
                )


def base_protocol_text(root: Path) -> str:
    return "\n".join(
        [
            'llm_model = "gpt-5"',
            'llm_model_version = "gpt-5"',
            'llm_provider = "openai"',
            'system_prompt_path = "prompts/crd_classifier_v1/system.md"',
            'system_prompt_sha256 = "system-sha"',
            'user_prompt_template_path = "prompts/crd_classifier_v1/user_template.md"',
            'user_prompt_template_sha256 = "user-sha"',
            "",
            "[[corpus_list]]",
            'label = "SYN"',
            f'config = "{root / "corpus.toml"}"',
            'corpus_class = "bible"',
            'language = "english"',
        ]
    )


if __name__ == "__main__":
    unittest.main()
