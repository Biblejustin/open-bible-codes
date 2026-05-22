# American Presidents Source Audit

Status: source-shape audit only. This is not an ELS result, not a
statistical test, and not a claim-ready replication.

## Sources

- Data PDF: `https://www.torah-code.org/experiments/americanpresidents_nasi_data.pdf`
- Transliteration rules PDF: `https://www.torah-code.org/experiments/english_hebrew_transliteration_rule.pdf`
- Data SHA-256: `90d2d1938cb481155c6b90a0b8504d9cab3cada4a771e65a7fb769789f778a40`
- Rules SHA-256: `e77d931f3364961ef29dff5a55ab3b8d190311d8c14ce9f0b37cca6bf9e4d020`

## Parsed Shape

| Item | Count |
| --- | ---: |
| data PDF pages from extracted text | 5 |
| rules PDF pages from extracted text | 4 |
| data records | 42 |
| record index minimum | 1 |
| record index maximum | 42 |
| last-name spelling rows | 140 |
| last-name plus initial spelling rows | 152 |
| total spelling rows | 292 |
| maximum spelling rows per record | 16 |
| records with initial-only continuation lines | 6 |

## Protocol Anchors

Found anchors: 9 of 9.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| data | `president_number_column` | found | numbered president data table found |
| data | `last_name_spellings_column` | found | last-name spelling column found |
| data | `initial_spellings_column` | found | initial-spelling column found |
| rules | `english_to_hebrew_title` | found | transliteration rule title found |
| rules | `consonant_mapping_table` | found | consonant mapping table found |
| rules | `vowel_variability_rule` | found | vowel variability rule found |
| rules | `final_vowel_explicit_rule` | found | final-vowel rule found |
| rules | `basic_name_and_initial_variations` | found | initial-variant rule found |
| rules | `double_consonant_variations` | found | double-consonant rule found |

## Use Boundary

This audit only verifies that the data and transliteration-rule sources can
be parsed into a stable source-shape summary. It does not normalize Hebrew
spellings, choose among variants, define controls, compute ELS hits, or
compare against random baselines.

Next result-bearing step, if chosen later: write a separate preregistered
American-presidents protocol that freezes the source rows, transliteration
policy, Genesis/Torah text, skip caps, compactness metric, and controls
before any ELS search.
