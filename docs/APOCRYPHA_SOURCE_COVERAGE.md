# Apocrypha Source Coverage

Status: source-coverage audit for completed apocrypha/deuterocanon
bridge review layers. This is not an ELS result.

## Reproduce

```bash
python3 -m scripts.audit_apocrypha_coverage --corpus LXX=configs/example_ebible_grclxx.toml --corpus KJV=configs/example_ebible_engkjv.toml --corpus KJVA=configs/example_ebible_engkjv_apocrypha.toml --out reports/apocrypha_coverage/coverage.csv --markdown-out docs/APOCRYPHA_SOURCE_COVERAGE.md --manifest-out reports/apocrypha_coverage/manifest.json
```

## Corpus Coverage Summary

| Corpus | Language | Present books | Verses | Normalized letters |
| --- | --- | ---: | ---: | ---: |
| `LXX` | greek | 16 | 5695 | 560880 |
| `KJV` | english | 0 | 0 | 0 |
| `KJVA` | english | 14 | 5720 | 593090 |

## Book Coverage

| Book | Name | LXX | KJV | KJVA |
| --- | --- | ---: | ---: | ---: |
| `TOB` | Tobit | 245 verses / 26759 letters | absent | 244 verses / 27672 letters |
| `JDT` | Judith | 339 verses / 45291 letters | absent | 339 verses / 46135 letters |
| `ESG` | Greek Esther / Esther additions | 219 verses / 29881 letters | absent | 105 verses / 11729 letters |
| `WIS` | Wisdom of Solomon | 437 verses / 37455 letters | absent | 436 verses / 46054 letters |
| `SIR` | Sirach / Ecclesiasticus | 1378 verses / 99371 letters | absent | 1393 verses / 117144 letters |
| `BAR` | Baruch | 141 verses / 12760 letters | absent | 213 verses / 20907 letters |
| `LJE` | Letter of Jeremiah | 72 verses / 6511 letters | absent | absent |
| `S3Y` | Song of the Three Young Men | 66 verses / 5485 letters | absent | 68 verses / 5557 letters |
| `SUS` | Susanna | 64 verses / 5772 letters | absent | 64 verses / 5965 letters |
| `BEL` | Bel and the Dragon | 42 verses / 4218 letters | absent | 42 verses / 4349 letters |
| `DAG` | Greek Daniel / Daniel additions | 357 verses / 45763 letters | absent | absent |
| `1MA` | 1 Maccabees | 917 verses / 94204 letters | absent | 924 verses / 100207 letters |
| `2MA` | 2 Maccabees | 481 verses / 43754 letters | absent | 555 verses / 71567 letters |
| `3MA` | 3 Maccabees | 227 verses / 29445 letters | absent | absent |
| `4MA` | 4 Maccabees | absent | absent | absent |
| `1ES` | 1 Esdras | 430 verses / 46256 letters | absent | 448 verses / 50099 letters |
| `2ES` | 2 Esdras | 280 verses / 27955 letters | absent | 874 verses / 83930 letters |
| `MAN` | Prayer of Manasseh | absent | absent | 15 verses / 1775 letters |
| `ODA` | Odes | absent | absent | absent |
| `PS2` | Psalm 151 | absent | absent | absent |

## Read

- The current eBible GRCLXX source already contains a substantial Greek
  deuterocanon/apocrypha block.
- The current eBible KJV source in this repo is a 66-book KJV stream and
  does not contain a KJV Apocrypha block.
- The eBible KJV + Apocrypha source is tracked as a separate corpus path
  so English apocrypha runs do not silently alter prior KJV baselines.
- Bridge-completion work can start with the existing LXX deuterocanon
  before adding new manuscript/source families.
- Any added source should get a separate license/provenance audit before
  being included in claim-facing runs.
