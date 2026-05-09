# Theological Terms Study

Run date: 2026-05-03/04 UTC

Term list:

- `terms/theological_terms.csv`
- Expanded screening list. The count tables below predate latest additions.
- Hebrew and Greek rows are separate.
- Batch default skips terms shorter than 3 normalized letters.

Corpora:

| Label | Source | Language | Letters | Verses |
|---|---|---|---:|---:|
| `MT_WLC` | OSHB WLC XML | Hebrew | 1,213,239 | 23,213 |
| `LXX` | local Codex_bible LXX CSV | Greek | 2,318,846 | 22,909 |
| `TR_NT` | local Codex_bible TR CSV | Greek | 692,948 | 7,957 |
| `SBLGNT` | SBLGNT text files | Greek | 679,879 | 7,939 |

Command:

```bash
python3 -m els batch \
  --terms terms/theological_terms.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --corpus LXX=configs/lxx_codex_bible.local.toml \
  --corpus TR_NT=configs/tr_codex_bible.local.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --min-skip 2 --max-skip 50 \
  --out reports/theological_terms_counts_full.csv \
  --manifest-out reports/theological_terms_counts_full.manifest.json
```

Output:

- `reports/theological_terms_counts_full.csv`
- `reports/theological_terms_counts_full.manifest.json`

Top count summary:

| Corpus | Counted | Skipped | Zero-count terms | Top counted terms |
|---|---:|---:|---:|---|
| `MT_WLC` | 42 | 4 | 0 | `אור` 57,298; `מות` 54,322; `אמת` 40,182; `משה` 40,121; `מלך` 28,567 |
| `LXX` | 52 | 0 | 15 | `ναος` 14,330; `υιος` 10,590; `αιμα` 9,171; `σιων` 4,312; `φως` 3,422 |
| `TR_NT` | 52 | 0 | 16 | `ναος` 4,448; `υιος` 2,784; `αιμα` 2,234; `σιων` 1,268; `φως` 945 |
| `SBLGNT` | 52 | 0 | 18 | `ναος` 4,402; `υιος` 2,670; `αιμα` 2,212; `σιων` 1,292; `φως` 916 |

Largest TR vs SBLGNT count deltas:

| Concept | Term | TR | SBLGNT | Delta |
|---|---|---:|---:|---:|
| Son | `υιος` | 2,784 | 2,670 | +114 |
| God | `θεος` | 777 | 725 | +52 |
| Temple | `ναος` | 4,448 | 4,402 | +46 |
| Light | `φως` | 945 | 916 | +29 |
| Zion | `σιων` | 1,268 | 1,292 | -24 |
| Blood | `αιμα` | 2,234 | 2,212 | +22 |
| Law | `νομος` | 133 | 114 | +19 |
| Lamb | `αμνος` | 137 | 156 | -19 |
| Jesus | `ιησους` | 5 | 10 | -5 |

Notes:

- Counts are ELS counts for skips 2 through 50, both directions.
- Counts are not normalized by corpus length or letter frequencies.
- Zero-count terms can still appear as ordinary surface words at skip 1; this batch intentionally excluded skip 1.
- Reports are ignored by git because they are generated from source texts.
