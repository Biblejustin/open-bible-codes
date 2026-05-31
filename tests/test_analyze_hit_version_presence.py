from scripts import analyze_hebrew_hit_version_presence
from scripts import analyze_hit_version_presence


def test_generic_entrypoint_reuses_hebrew_version_presence_main() -> None:
    assert analyze_hit_version_presence.main is analyze_hebrew_hit_version_presence.main
