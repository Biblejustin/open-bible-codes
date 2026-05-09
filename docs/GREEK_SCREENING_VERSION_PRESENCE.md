# Greek Screening Version Presence

This is the tracked summary for the broader Greek exact-hit version-presence
screen:

```bash
python3 -m scripts.run_protocol protocols/greek_screening_version_presence.toml --resume
```

## Scope

- Term sources:
  - `terms/theological_terms.csv`
  - `terms/modern_names_dates.csv`
  - `terms/table_of_nations.csv`
  - `terms/prophetic_terms.csv`
  - `terms/greek_nt_claim_terms.csv`
  - `terms/biblical_tribes.csv`
  - `terms/biblical_festivals.csv`
- Duplicate term IDs across files: keep first selected row
- Corpora: `TR_NT`, `BYZ_NT`, `TCG_NT`, `SBLGNT`
- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `4`
- Max hits: `50` per term per corpus

The report groups hits by exact ref-key pattern:

`term_id + normalized_term + signed_skip + direction + canonical start/center/end refs`

## Output

Ignored local outputs:

- `reports/greek_screening_version_presence/hit_patterns.csv`
- `reports/greek_screening_version_presence/term_summary.csv`
- `reports/greek_screening_version_presence/greek_screening_version_presence.md`
- `reports/greek_screening_version_presence/manifest.json`

Latest run:

- Runtime: `13.238s` protocol step time
- Analyzer duration: `13.133s`
- Selected terms: `413`
- Summary rows after length filter: `398`
- Hit records: `22,501`
- Exact pattern rows: `11,103`

This run uses bulk multi-query capped extraction plus corpus-level workers. It
still caps at 50 hits per term per corpus, but the selected capped hits can
differ from the older term-by-term run because the bulk path scans by skip/lane
rather than by one term at a time.

Pattern scope counts:

| Scope | Pattern rows |
| --- | ---: |
| `present_all_observed_sources` | 2,192 |
| `present_multiple_sources` | 3,416 |
| `source_specific` | 5,495 |

Source-specific rows:

| Source | Rows |
| --- | ---: |
| `SBLGNT` | 2,631 |
| `BYZ_NT` | 1,268 |
| `TR_NT` | 1,017 |
| `TCG_NT` | 579 |

## High-Stability Rows

The strongest all-source rows are dense 4-letter or short transliteration forms.
Many hit the per-corpus cap of 50, so their totals should be read as capped
screening counts, not complete counts.

| Term | Normalized | Total capped hits | Exact patterns | All-source patterns |
| --- | --- | ---: | ---: | ---: |
| `aram_g` | `αραμ` | 200 | 59 | 45 |
| `god_g` | `θεοσ` | 200 | 58 | 42 |
| `asher_g` | `ασηρ` | 200 | 61 | 41 |
| `lasha_g` | `δασα` | 200 | 62 | 41 |
| `amen_g` | `αμην` | 200 | 61 | 40 |
| `lion_g` | `λεων` | 200 | 60 | 40 |
| `hell_hades_g` | `αδησ` | 200 | 65 | 39 |
| `seba_g` | `σαβα` | 200 | 63 | 39 |
| `shelah_g` | `σαλα` | 200 | 64 | 39 |
| `boils_g` | `ελκη` | 200 | 63 | 38 |

## Modern And Local Rows

Selected rows from the modern/local additions:

| Term | Normalized | Total capped hits | All-source | Multi-source | Source-specific |
| --- | --- | ---: | ---: | ---: | ---: |
| `nato_g` | `νατο` | 200 | 38 | 10 | 22 |
| `iran_g` | `ιραν` | 200 | 38 | 14 | 12 |
| `russia_g` | `ρωσια` | 200 | 17 | 38 | 43 |
| `magog_g` | `μαγωγ` | 15 | 2 | 1 | 5 |
| `france_g` | `γαλλια` | 7 | 0 | 1 | 5 |
| `turkey_g` | `τουρκια` | 5 | 0 | 2 | 1 |
| `europe_g` | `ευρωπη` | 3 | 0 | 0 | 3 |
| `germany_g` | `γερμανια` | 0 | 0 | 0 | 0 |
| `america_g` | `αμερικη` | 0 | 0 | 0 | 0 |
| `united_states_g` | `ηνωμενεσπολιτειεσ` | 0 | 0 | 0 | 0 |
| `united_nations_g` | `ηνωμεναεθνη` | 0 | 0 | 0 | 0 |
| `european_union_g` | `ευρωπαικηενωση` | 0 | 0 | 0 | 0 |
| `cowboy_g` | `καουμποι` | 0 | 0 | 0 | 0 |
| `catering_g` | `κετερινγκ` | 0 | 0 | 0 | 0 |
| `simsberry_g` | `σιμσμπερι` | 0 | 0 | 0 | 0 |
| `simscorner_g` | `σιμσκορνερ` | 0 | 0 | 0 | 0 |

## Current Read

The broader Greek exact-hit screen confirms the narrower Greek claim/control
read:

- short normalized Greek forms produce many exact-hit rows;
- all-source rows are common enough to be useful for review queues;
- source-specific rows are also common, especially in `SBLGNT`;
- long modern phrases and local terms remain absent in this scan.

This report helps answer which Greek NT editions contain the same exact pattern.
It does not make the rows meaningful by itself. Use row-local controls and
context review before promoting any hit.
