# Hebrew Screening Version Presence

This is the tracked summary for the broader Hebrew exact-hit version-presence
screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_screening_version_presence.toml --resume
```

## Scope

- Term sources:
  - `terms/theological_terms.csv`
  - `terms/modern_names_dates.csv`
  - `terms/table_of_nations.csv`
  - `terms/prophetic_terms.csv`
  - `terms/hebrew_claim_terms.csv`
  - `terms/biblical_tribes.csv`
  - `terms/biblical_festivals.csv`
  - `terms/biblical_calendar.csv`
- Duplicate term IDs across files: keep first selected row
- Corpora: `MT_WLC`, `UXLC`, `EBIBLE_WLC`, `MAM`, `UHB`
- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `4`
- Max hits: `50` per term per corpus

The report groups hits by exact ref-key pattern:

`term_id + normalized_term + signed skip + direction + canonical start/center/end refs`

## Output

Ignored local outputs:

- `reports/hebrew_screening_version_presence/hit_patterns.csv`
- `reports/hebrew_screening_version_presence/term_summary.csv`
- `reports/hebrew_screening_version_presence/hebrew_screening_version_presence.md`
- `reports/hebrew_screening_version_presence/manifest.json`

Latest run:

- Runtime: `23.257s` protocol step time
- Analyzer duration: `23.130s`
- Selected terms: `557`
- Summary rows after length filter: `417`
- Hit records: `60,630`
- Exact pattern rows: `15,099`

This run uses bulk multi-query capped extraction plus corpus-level workers. It
still caps at 50 hits per term per corpus, but the selected capped hits can
differ from the older term-by-term run because the bulk path scans by skip/lane
rather than by one term at a time.

Pattern scope counts:

| Scope | Pattern rows |
| --- | ---: |
| `present_all_observed_sources` | 9,432 |
| `present_all_leningrad_streams` | 2,166 |
| `present_multiple_sources` | 901 |
| `source_specific` | 2,600 |

Source-specific rows:

| Source | Rows |
| --- | ---: |
| `UHB` | 1,222 |
| `MAM` | 1,082 |
| `UXLC` | 182 |
| `EBIBLE_WLC` | 60 |
| `MT_WLC` | 54 |

## High-Stability Rows

The strongest all-source rows are short forms that hit the per-corpus cap of
50. Their total capped hit count is therefore `250`, not a full corpus count.

| Term | Normalized | Total capped hits | Exact patterns | All-source patterns |
| --- | --- | ---: | ---: | ---: |
| `damascus_h` | `דמשק` (dmshq; English: Damascus) | 250 | 51 | 49 |
| `5786_jewish_h` | `תשפו` (tshpw; English: Hebrew year 5786) | 250 | 54 | 47 |
| `faith_h` | `אמונה` (mwnh; English: Faith) | 250 | 53 | 47 |
| `manasseh_h` | `מנשה` (mnshh; English: Manasseh) | 250 | 52 | 47 |
| `manasseh_tribe_h` | `מנשה` (mnshh; English: Manasseh Tribe) | 250 | 52 | 47 |
| `5784_jewish_h` | `תשפד` (tshpd; English: Hebrew year 5784) | 250 | 54 | 46 |
| `athens_h` | `אתונה` (twnh; English: Athens) | 250 | 55 | 46 |
| `calneh_h` | `כלנה` (klnh; English: Calneh) | 250 | 54 | 46 |
| `canaan_h` | `כנענ` (knn; English: Canaan) | 250 | 51 | 46 |
| `france_h` | `צרפת` (tsrpt; English: France) | 250 | 54 | 46 |

## Modern And Local Rows

Selected rows from the modern/local additions:

| Term | Normalized | Total capped hits | All-source | Leningrad-family | Multi-source | Source-specific |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `france_h` | `צרפת` (tsrpt; English: France) | 250 | 46 | 3 | 1 | 4 |
| `iran_h` | `איראנ` (yrn; English: Iran) | 250 | 44 | 5 | 1 | 6 |
| `vance_h` | `ואנס` (wns; English: Vance) | 250 | 43 | 6 | 1 | 9 |
| `russia_h` | `רוסיה` (rwsyh; English: Russia) | 250 | 31 | 18 | 1 | 21 |
| `netanyahu_h` | `נתניהו` (ntnyhw; English: Netanyahu) | 131 | 15 | 12 | 0 | 11 |
| `europe_h` | `אירופה` (yrwph; English: Europe) | 105 | 10 | 10 | 2 | 10 |
| `america_h` | `אמריקה` (mryqh; English: America) | 59 | 6 | 6 | 0 | 5 |
| `cowboy_h` | `קאובוי` (qwbwy; English: Cowboy) | 62 | 8 | 4 | 0 | 7 |
| `germany_h` | `גרמניה` (grmnyh; English: Germany) | 38 | 3 | 5 | 0 | 4 |
| `trump_h` | `טראמפ` (trmp; English: Trump) | 31 | 6 | 0 | 0 | 1 |
| `turkey_h` | `טורקיה` (twrqyh; English: Turkey) | 5 | 1 | 0 | 0 | 0 |
| `united_states_h` | `ארצותהברית` (rtswthbryt; English: United States) | 0 | 0 | 0 | 0 | 0 |
| `united_states_america_h` | `ארצותהבריתשלאמריקה` (rtswthbrytshlmryqh; English: United States Of America) | 0 | 0 | 0 | 0 | 0 |
| `united_nations_h` | `האומותהמאוחדות` (hwmwthmwchdwt; English: United Nations) | 0 | 0 | 0 | 0 | 0 |
| `european_union_h` | `האיחודהאירופי` (hychwdhyrwpy; English: European Union) | 0 | 0 | 0 | 0 | 0 |
| `catering_h` | `קייטרינג` (qyytryng; English: Catering) | 0 | 0 | 0 | 0 | 0 |
| `cowboy_catering_h` | `קאובויקייטרינג` (qwbwyqyytryng; English: Cowboy Catering) | 0 | 0 | 0 | 0 | 0 |
| `simsberry_h` | `סימסברי` (symsbry; English: Simsberry) | 0 | 0 | 0 | 0 | 0 |
| `simscorner_h` | `סימסקורנר` (symsqwrnr; English: Simscorner) | 0 | 0 | 0 | 0 | 0 |

## Current Read

The broader Hebrew matrix reinforces the earlier Hebrew read:

- exact ref-key stability is common across MT-family sources;
- short 4-5 letter forms dominate all-source rows;
- most source-specific behavior comes from `UHB` and `MAM`;
- longer modern/local phrases remain absent in this capped scan.

This report is useful for selecting stable Hebrew review rows. It does not
score significance and does not make modern-name or theological claims by
itself.
