# Hebrew Theology All-Codes Collection

This report intentionally keeps every hidden-path ELS row from the surface-context collection and then flags same-word, related-center, center-verse, and span context. It is a collection index, not a claim-grade filter.

## Inputs

- Hits: `reports/hebrew_theology_all_codes/surface_all_codes.csv`
- Summary: `reports/hebrew_theology_all_codes/surface_all_codes_summary.csv`
- Report DB: `reports/db/open_bible_codes.duckdb`
- Corpora: `EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC`

## Collection Counts

| Metric | Count |
| --- | ---: |
| Terms represented | 20 |
| Corpus-term summary rows | 100 |
| Hidden-path rows retained | 305,353 |
| Total hits from summary | 305,353 |
| Any surface-context hits | 90,685 |
| Center word contains same term | 3,634 |
| Center word contains related term | 473 |
| Center verse contains same term | 44,420 |
| Center verse contains related term | 5,183 |
| Hit span contains same/related term | 91,060 |

## Context Labels

| Best context | Rows |
| --- | ---: |
| `hidden_path_only` | 214,668 |
| `exact_center` | 44,420 |
| `exact_span` | 34,006 |
| `same_category_span` | 7,118 |
| `same_category_center` | 5,141 |

## Top Terms

| Term | Concept | Hidden hits | Center word same | Center word related | Center verse same | Center verse related | Span context |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `htp_yhwh_h` | YHWH | 108,320 | 3,329 | 0 | 41,919 | 0 | 71,851 |
| `htp_love_h` | Love | 39,575 | 10 | 83 | 157 | 669 | 2,082 |
| `htp_peace_h` | Peace | 37,669 | 90 | 6 | 731 | 108 | 2,191 |
| `htp_torah_h` | Torah | 32,524 | 20 | 354 | 204 | 3,846 | 9,395 |
| `htp_yeshua_h` | Yeshua | 27,142 | 11 | 0 | 189 | 71 | 955 |
| `htp_covenant_h` | Covenant | 21,429 | 66 | 11 | 517 | 90 | 1,520 |
| `htp_messiah_h` | Messiah | 12,864 | 1 | 4 | 43 | 81 | 454 |
| `htp_wisdom_h` | Wisdom | 7,218 | 5 | 0 | 52 | 57 | 431 |
| `htp_glory_h` | Glory | 6,979 | 5 | 14 | 161 | 237 | 1,086 |
| `htp_faith_h` | Faith | 3,171 | 0 | 1 | 5 | 1 | 48 |
| `htp_salvation_h` | Salvation | 2,180 | 0 | 0 | 5 | 0 | 40 |
| `htp_savior_h` | Savior | 2,150 | 0 | 0 | 0 | 9 | 49 |
| `htp_israel_h` | Israel | 2,104 | 83 | 0 | 403 | 10 | 879 |
| `htp_kingdom_h` | Kingdom | 1,515 | 14 | 0 | 34 | 0 | 75 |
| `htp_redemption_h` | Redemption | 513 | 0 | 0 | 0 | 4 | 4 |
| `htp_lamb_of_god_h` | Lamb Of God | 0 | 0 | 0 | 0 | 0 | 0 |
| `htp_mercy_h` | Mercy | 0 | 0 | 0 | 0 | 0 | 0 |
| `htp_son_of_god_h` | Son Of God | 0 | 0 | 0 | 0 | 0 | 0 |
| `htp_truth_h` | Truth | 0 | 0 | 0 | 0 | 0 | 0 |
| `htp_yeshua_messiah_h` | Yeshua Messiah | 0 | 0 | 0 | 0 | 0 | 0 |

## Read

This output is deliberately broad. Hidden-path-only rows are retained for
inspection. Same-center-word rows are a narrower subset. Same-concept and
same-category center-word rows are related-surface prompts, not automatic
interpretations. Claim-grade filtering still belongs in the controlled
reports.
