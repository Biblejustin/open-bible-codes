import csv
from pathlib import Path

from scripts.build_cipher_layered_pairs import (
    LayerHit,
    anchor_key,
    cipher_layered_pair_rows,
    main,
)


def hit(
    *,
    term_id: str = "babel_h",
    corpus_label: str = "MT_WLC",
    center_ref: str = "Jer 25:26",
    center_normalized_word: str = "בבל",
    skip: str = "7",
    transform: str = "",
) -> dict[str, str]:
    return {
        "corpus_label": corpus_label,
        "term_id": term_id,
        "concept": "Babylon",
        "center_ref": center_ref,
        "center_word": "בבל",
        "center_normalized_word": center_normalized_word,
        "skip": skip,
        "direction": "forward",
        "transform": transform,
    }


def test_anchor_key_uses_corpus_fallbacks() -> None:
    row = hit(corpus_label="")
    row["corpus"] = "MAM"

    assert anchor_key(row, ("corpus_label", "term_id")) == ("MAM", "babel_h")


def test_cipher_layered_pair_rows_match_same_anchor() -> None:
    plain = LayerHit(hit_index=1, layer="plain", row=hit(skip="7"))
    cipher = LayerHit(hit_index=1, layer="cipher", row=hit(skip="13", transform="hebrew_atbash"))

    rows = cipher_layered_pair_rows([plain], [cipher])

    assert len(rows) == 1
    assert rows[0]["term_id"] == "babel_h"
    assert rows[0]["plain_skip"] == "7"
    assert rows[0]["cipher_skip"] == "13"
    assert rows[0]["cipher_transform"] == "hebrew_atbash"


def test_cipher_layered_pair_rows_do_not_match_different_anchor() -> None:
    plain = LayerHit(hit_index=1, layer="plain", row=hit(center_ref="Jer 25:26"))
    cipher = LayerHit(hit_index=1, layer="cipher", row=hit(center_ref="Jer 51:41"))

    assert cipher_layered_pair_rows([plain], [cipher]) == []


def test_main_writes_pairs(tmp_path: Path) -> None:
    plain = tmp_path / "plain.csv"
    cipher = tmp_path / "cipher.csv"
    out = tmp_path / "pairs.csv"
    fieldnames = list(hit())
    with plain.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(hit(skip="7"))
    with cipher.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(hit(skip="13", transform="hebrew_albam"))

    assert main(["--plain-hits", str(plain), "--cipher-hits", str(cipher), "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "hebrew_albam" in text
    assert "babel_h" in text
