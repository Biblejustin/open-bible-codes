import csv
from pathlib import Path
from types import SimpleNamespace

from scripts import analyze_pericope_inverse_check as inverse


def test_pericope_refs_for_sbl_style_corpus(tmp_path: Path, monkeypatch) -> None:
    override = tmp_path / "critical_consensus.csv"
    with override.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ref", "passage"])
        writer.writeheader()
        writer.writerow({"ref": "John 8:6", "passage": "Pericope Adulterae"})
        writer.writerow({"ref": "Mark 16:9", "passage": "Longer Ending of Mark"})
    corpus = SimpleNamespace(verses=[SimpleNamespace(ref="John 8:6")])
    monkeypatch.setattr(inverse, "OVERRIDE", override)

    assert inverse.pericope_refs_for_corpus(corpus) == {"John 8:6"}

