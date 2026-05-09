# Hebrew Hit Version Presence

This is the tracked summary for the capped exact-hit version-presence screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_hit_version_presence.toml --resume
```

## Scope

- Term source: `terms/modern_names_dates.csv`
- Term filter: focused Hebrew rows for modern geopolitical, local, and recent-person names
- Corpora: `MT_WLC`, `UXLC`, `EBIBLE_WLC`, `MAM`, `UHB`
- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `4`
- Max hits: `200` per term per corpus

The report groups hits by exact ref-key pattern:

`term_id + normalized_term + signed_skip + direction + canonical start/center/end refs`

Offsets stay in the raw CSV because the underlying source streams can differ
even when the same canonical ref-key pattern appears.

## Output

Ignored local outputs:

- `reports/hebrew_hit_version_presence/hit_patterns.csv`
- `reports/hebrew_hit_version_presence/term_summary.csv`
- `reports/hebrew_hit_version_presence/hebrew_hit_version_presence.md`
- `reports/hebrew_hit_version_presence/manifest.json`

Latest run:

- Runtime: `21.953s`
- Terms observed: `22`
- Hit records: `4,767`
- Exact pattern rows: `1,202`
- Summary rows: `21`

Pattern scope counts:

| Scope | Pattern rows |
| --- | ---: |
| `present_all_observed_sources` | 749 |
| `present_all_leningrad_streams` | 187 |
| `present_multiple_sources` | 22 |
| `source_specific` | 244 |

## Current Read

Many exact ref-key rows are stable across all five Hebrew streams. This mostly
means those short transliterated strings sit in shared consonantal text. It does
not make modern-name claims stronger by itself.

The most stable high-count rows are short or abbreviation-like forms:

- `ארהב` / USA abbreviation
- `ואנס` / Vance
- `איראנ` / Iran
- `צרפת` / France
- `רוסיה` / Russia

Longer phrase/local rows remain absent in this capped scan:

- Donald Trump
- United States
- United States of America
- United Nations
- European Union
- Cowboy Catering
- Simsberry
- Simscorner

## Caution

This is a capped hit-presence matrix, not a significance test. The cap can hide
later hits for dense terms, and exact ref-key agreement does not prove textual
identity or interpretive meaning. Use the CSVs to pick stable review rows, then
apply controls before making any claim.
