# Data

Raw texts stay out of git by default.

## CSV Shape

Minimum:

```csv
ref,text
Genesis 1:1,בראשית ברא אלהים את השמים ואת הארץ
```

Better:

```csv
ref,book,chapter,verse,text
Genesis 1:1,Genesis,1,1,בראשית ברא אלהים את השמים ואת הארץ
```

Greek same shape:

```csv
ref,book,chapter,verse,text
John 1:1,John,1,1,Ἐν ἀρχῇ ἦν ὁ λόγος
```

Normalization removes spaces, punctuation, accents, niqqud, and cantillation.
English normalization lowercases and keeps `a` through `z` only.

## eBible GRCLXX LXX

The public LXX importer writes this CSV shape from eBible USFM:

```bash
python3 scripts/download_ebible_grclxx.py
```

Outputs stay ignored by git:

- `data/raw/ebible/grclxx_usfm.zip`
- `data/processed/ebible/grclxx.csv`
- `data/processed/ebible/grclxx.manifest.json`

## eBible Greek Textus Receptus NT

The public TR importer uses the same CSV shape:

```bash
python3 scripts/download_ebible_grctr.py
```

Outputs stay ignored by git:

- `data/raw/ebible/grctr_usfm.zip`
- `data/processed/ebible/grctr.csv`
- `data/processed/ebible/grctr.manifest.json`

## eBible English KJV

The public KJV importer uses the same CSV shape:

```bash
python3 scripts/download_ebible_engkjv.py
```

Outputs stay ignored by git:

- `data/raw/ebible/eng-kjv2006_usfm.zip`
- `data/processed/ebible/eng-kjv2006.csv`
- `data/processed/ebible/eng-kjv2006.manifest.json`

## Non-Bible Control Corpora

Large non-Bible background corpora for Hebrew, Greek, and English can be
downloaded with:

```bash
python3 scripts/download_nonbible_controls.py
```

Outputs stay ignored by git:

- `data/raw/nonbible_controls/`
- `data/processed/nonbible_controls/`

Source details and corpus configs are documented in
`docs/NONBIBLE_CONTROL_CORPORA.md`.

## Michigan-Claremont Hebrew

Koren-style Hebrew files in Michigan-Claremont transliteration can use:

```toml
language = "michigan"

[[sources]]
format = "michigan_claremont"
path = "../data/raw/koren/genesis.koren.gz"
book = "Genesis"
book_number = 1
```

Search terms may be Hebrew Unicode or Michigan-Claremont:

```bash
python3 -m els search --config configs/example_michigan_torah.toml --term תורה --min-skip 50 --max-skip 50
python3 -m els search --config configs/example_michigan_torah.toml --term TWRH --min-skip 50 --max-skip 50
```
