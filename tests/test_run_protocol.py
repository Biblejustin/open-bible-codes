import sys

from scripts import run_protocol as runner


def test_run_protocol_main_forwards_cli_options(monkeypatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_run_protocol(
        protocol: str,
        *,
        only: set[str],
        dry_run: bool,
        manifest_out: str,
        resume: bool,
    ) -> int:
        calls.append(
            {
                "protocol": protocol,
                "only": only,
                "dry_run": dry_run,
                "manifest_out": manifest_out,
                "resume": resume,
            }
        )
        return 9

    monkeypatch.setattr(runner, "run_protocol", fake_run_protocol)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_protocol",
            "protocols/demo.toml",
            "--only",
            "a",
            "--only",
            "b",
            "--dry-run",
            "--resume",
            "--manifest-out",
            "manifest.json",
        ],
    )

    assert runner.main() == 9
    assert calls == [
        {
            "protocol": "protocols/demo.toml",
            "only": {"a", "b"},
            "dry_run": True,
            "manifest_out": "manifest.json",
            "resume": True,
        }
    ]

