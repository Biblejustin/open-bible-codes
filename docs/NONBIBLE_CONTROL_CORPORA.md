# Non-Bible Control Corpora

## Scope

These corpora are large non-Bible background texts for checking whether ELS
patterns are distinctive to Bible corpora or also appear in unrelated texts of
the same language.

They are not interpretive evidence by themselves. They are screening controls.

## Sources

### Hebrew

All three Hebrew controls use the Project Ben-Yehuda public-domain dump,
`txt_stripped` plaintext without niqqud:

| Corpus label | Source | Config |
| --- | --- | --- |
| `HEB_PBY_BIALIK` | Haim Nahman Bialik author directory `p89` | `configs/nonbible_hebrew_pby_bialik.toml` |
| `HEB_PBY_BRENNER` | Yosef Haim Brenner author directory `p66` | `configs/nonbible_hebrew_pby_brenner.toml` |
| `HEB_PBY_AHAD_HAAM` | Ahad Ha'am author directory `p23` | `configs/nonbible_hebrew_pby_ahad_haam.toml` |

Project Ben-Yehuda states the dump contains public-domain Hebrew works and may
be freely reused.

### Greek

All three Greek controls use PerseusDL `canonical-greekLit` TEI XML:

| Corpus label | Source | Config |
| --- | --- | --- |
| `GRC_PERSEUS_ILIAD` | Homer, Iliad | `configs/nonbible_greek_perseus_iliad.toml` |
| `GRC_PERSEUS_ODYSSEY` | Homer, Odyssey | `configs/nonbible_greek_perseus_odyssey.toml` |
| `GRC_PERSEUS_HERODOTUS` | Herodotus, Histories | `configs/nonbible_greek_perseus_herodotus.toml` |

The PerseusDL repository says contents are CC BY-SA 4.0 unless otherwise
indicated.

### English

All three English controls use Project Gutenberg public-domain-in-the-USA UTF-8
plain text with Gutenberg boilerplate stripped:

| Corpus label | Source | Config |
| --- | --- | --- |
| `ENG_PG_SHAKESPEARE` | Complete Works of William Shakespeare | `configs/nonbible_english_pg_shakespeare.toml` |
| `ENG_PG_WAR_PEACE` | War and Peace | `configs/nonbible_english_pg_war_and_peace.toml` |
| `ENG_PG_MOBY_DICK` | Moby Dick | `configs/nonbible_english_pg_moby_dick.toml` |

## Local Validation Sizes

Initial local import produced these normalized letter counts:

| Corpus | Language | Normalized letters |
| --- | --- | ---: |
| `HEB_PBY_BIALIK` | Hebrew | 5,715,999 |
| `HEB_PBY_BRENNER` | Hebrew | 5,571,301 |
| `HEB_PBY_AHAD_HAAM` | Hebrew | 2,758,185 |
| `GRC_PERSEUS_ILIAD` | Greek | 552,073 |
| `GRC_PERSEUS_ODYSSEY` | Greek | 427,052 |
| `GRC_PERSEUS_HERODOTUS` | Greek | 962,235 |
| `ENG_PG_SHAKESPEARE` | English | 4,057,221 |
| `ENG_PG_WAR_PEACE` | English | 2,516,913 |
| `ENG_PG_MOBY_DICK` | English | 955,178 |

## Download

Download all controls:

```bash
python3 -m scripts.download_nonbible_controls
```

Download one language:

```bash
python3 -m scripts.download_nonbible_controls --language hebrew
python3 -m scripts.download_nonbible_controls --language greek
python3 -m scripts.download_nonbible_controls --language english
```

Raw and processed control texts stay ignored under `data/raw/` and
`data/processed/`. Each processed text receives a manifest with source URL,
license note, raw-file hashes, and processed-file hash.

## Run

Count declared terms against all nine controls at skip `2..100`, direction
`both`:

```bash
python3 -m scripts.run_protocol protocols/nonbible_control_counts.toml --resume
```

This uses the same language filtering as Bible corpora:

- Hebrew and Michigan terms run against Hebrew controls.
- Greek terms run against Greek controls.
- English terms run against English controls.

Initial local protocol timing:

- `protocols/nonbible_control_counts.toml --resume`
- elapsed: `39.692s`
- outputs: ignored CSV/manifest files under `reports/nonbible_controls/`

The pilot run immediately shows why these controls matter: short forms such as
Hebrew `יהוה` (YHWH; English: YHWH), scrambled `וההי` (w-h-h-y; English: scrambled YHWH control), English `son`, and ordinary four-letter strings
produce large counts in non-Bible corpora too. Treat short-form hits as
background-noise candidates unless they survive stricter controls.

## Cautions

These controls are language-background checks. They do not control for every
textual feature that can affect ELS density, such as corpus length, genre,
authorial vocabulary, spelling standardization, verse segmentation, or the
source text's alphabet inventory. Use them alongside shuffled-letter,
shuffled-term, and length-matched controls.
