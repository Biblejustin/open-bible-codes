# English KJV Search

## Scope

This adds a public English KJV corpus path and a generated English screening
term list.

## Source

- Corpus config: `configs/example_ebible_engkjv.toml`
- Importer: `scripts/download_ebible_engkjv.py`
- Source package: eBible `eng-kjv2006` USFM ZIP
- Upstream details: `https://ebible.org/find/show.php?id=eng-kjv2006`

The upstream details page labels `eng-kjv2006` public domain and describes it
as the standardized 1769 King James / Authorized Version, protocanon only, with
Strong's numbers added. Raw and processed source text stays ignored under
`data/raw/` and `data/processed/`.

The KJV + Apocrypha source is separate:

- Corpus config: `configs/example_ebible_engkjv_apocrypha.toml`
- Importer: `scripts/download_ebible_engkjv_apocrypha.py`
- Source package: eBible `eng-kjv` USFM ZIP
- Upstream details: `https://ebible.org/find/show.php?id=eng-kjv`

Use `KJVA` only in protocols that explicitly intend to include the
Apocrypha/Deuterocanon; the existing `KJV` corpus remains 66-book.

## English Terms

`terms/english_search_terms.csv` is generated from the `concept` labels in the
declared Hebrew and Greek term files. Rebuild it after changing term concepts:

```bash
python3 -m scripts.build_english_search_terms
```

The generator skips concepts containing decimal digits because English
normalization removes digits from the ELS stream. If a date or number needs to
be searched in KJV, add a declared spelled-out English term such as
`nineteen forty eight`.

## Run

Standalone KJV screening:

```bash
python3 -m scripts.download_ebible_engkjv
python3 -m scripts.run_protocol protocols/english_kjv_screening.toml --resume
```

The broader `protocols/broad_search.toml` also includes:

- `--term-set english_search_terms=terms/english_search_terms.csv`
- `--corpus KJV=configs/example_ebible_engkjv.toml`

Language filtering keeps English terms on English corpora, Greek terms on Greek
corpora, and Hebrew/Michigan terms on Hebrew corpora.

## Pilot Validation

Initial local validation imported:

- letters: `3,223,225`
- verses: `31,102`

The standalone KJV screening protocol completed in `10.234s` on this machine
for skip `2..100`, direction `both`:

- rows: `693`
- counted rows: `689`
- zero rows: `309`
- total ELS hits: `2,229,701`

Selected screening counts from `reports/english_kjv_screening/`:

| Concept | Normalized | Hits |
| --- | --- | ---: |
| Jesus | `jesus` | 18 |
| Lord | `lord` | 4,707 |
| Torah | `torah` | 1,897 |
| YHWH | `yhwh` | 1,774 |
| Trump | `trump` | 31 |
| Donald Trump | `donaldtrump` | 0 |
| Netanyahu | `netanyahu` | 0 |
| Cowboy | `cowboy` | 1 |
| Cowboy Catering | `cowboycatering` | 0 |
| United States | `unitedstates` | 0 |
| Constantine I | `constantinei` | 0 |

These are raw ELS counts only. Short forms such as `lord`, `torah`, `yhwh`,
and `trump` need controls before they can be read as anything more than
screening output.

## Cautions

This is a screening list, not an interpretation. KJV uses English translation
surface forms, so a Hebrew source concept may need multiple English renderings
for a serious claim test. Example: `YHWH` can be screened as `YHWH`, but KJV
surface convention normally uses `LORD`.

## Private English Version Comparison

Local-only configs are available for user-supplied copyrighted English texts:

- `configs/local_nlt.toml`
- `configs/local_msg.toml`
- `configs/local_tpt.toml`
- `configs/local_niv.toml`

Place CSVs under `data/private/english/`; that path is ignored by git. Then run:

```bash
python3 -m scripts.run_protocol protocols/private_english_versions.toml --resume
```

See `docs/PRIVATE_ENGLISH_VERSIONS.md` for file format and copyright limits.

For the full BibleGateway English-version list, use:

```bash
python3 -m scripts.run_protocol protocols/biblegateway_english_versions.toml --resume
```

The manifest is `configs/biblegateway_english_versions.csv`. Missing local CSVs
are reported locally under `reports/biblegateway_english_versions/`.

For additional open/CC English controls, use:

```bash
python3 -m scripts.download_ebible_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/ebible_english_controls.toml --resume
python3 -m scripts.download_door43_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/door43_english_controls.toml --resume
python3 -m scripts.download_oet_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/oet_english_controls.toml --resume
python3 -m scripts.download_otb_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/otb_english_controls.toml --resume
python3 -m scripts.download_openbible_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/openbible_english_controls.toml --resume
python3 -m scripts.download_odr_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/odr_english_controls.toml --resume
python3 -m scripts.download_supplemental_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/supplemental_english_controls.toml --resume
```

Control manifests are `configs/ebible_english_controls.csv`,
`configs/door43_english_controls.csv`, `configs/oet_english_controls.csv`,
`configs/otb_english_controls.csv`, `configs/openbible_english_controls.csv`,
`configs/odr_english_controls.csv`, and
`configs/supplemental_english_controls.csv`.

Then compare the BibleGateway-overlap set against those controls:

```bash
python3 -m scripts.run_protocol protocols/english_version_control_triage.toml --resume
```

Main outputs:

- `reports/english_version_control_triage/triage.md`
- `reports/english_version_control_triage/context_review.md`
