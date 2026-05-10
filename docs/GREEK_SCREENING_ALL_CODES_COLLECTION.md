# Greek Screening All-Codes Collection

This report intentionally keeps every hidden-path ELS row from the surface-context collection and then flags same-word, related-center, center-verse, and span context. It is a collection index, not a claim-grade filter.

## Inputs

- Hits: `reports/greek_screening_all_codes/surface_all_codes.csv`
- Summary: `reports/greek_screening_all_codes/surface_all_codes_summary.csv`
- Report DB: `reports/db/open_bible_codes.duckdb`
- Corpora: `BYZ_NT, SBLGNT, TCG_NT, TR_NT`

## Collection Counts

| Metric | Count |
| --- | ---: |
| Terms represented | 484 |
| Corpus-term summary rows | 2,024 |
| Hidden-path rows retained | 352,681 |
| Total hits from summary | 352,681 |
| Any surface-context hits | 66,997 |
| Center word contains same term | 222 |
| Center word contains related term | 1,524 |
| Center verse contains same term | 5,683 |
| Center verse contains related term | 28,096 |
| Hit span contains same/related term | 73,326 |

## Context Labels

| Best context | Rows |
| --- | ---: |
| `hidden_path_only` | 285,684 |
| `same_category_span` | 29,017 |
| `same_category_center` | 25,576 |
| `exact_span` | 6,721 |
| `exact_center` | 5,683 |

## Top Terms

| Term | Concept | Hidden hits | Center word same | Center word related | Center verse same | Center verse related | Span context |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `blood_g` | Blood | 36,750 | 38 | 118 | 1,398 | 2,338 | 7,967 |
| `nato_g` | NATO | 36,345 | 79 | 48 | 1,606 | 1,357 | 6,663 |
| `temple_g` | Temple | 35,617 | 4 | 74 | 97 | 1,521 | 3,563 |
| `son_g` | Son | 22,294 | 29 | 134 | 645 | 2,022 | 6,038 |
| `zion_g` | Zion | 19,934 | 2 | 171 | 134 | 1,966 | 4,407 |
| `haima_gnt` | Blood | 18,375 | 19 | 30 | 699 | 809 | 3,227 |
| `china_g` | China | 16,489 | 0 | 74 | 33 | 1,156 | 2,644 |
| `iran_g` | Iran | 15,745 | 4 | 39 | 93 | 1,109 | 2,703 |
| `shelah_g` | Shelah | 13,936 | 0 | 117 | 12 | 2,712 | 5,363 |
| `lasha_g` | Lasha | 9,878 | 1 | 64 | 57 | 1,682 | 3,601 |
| `obal_g` | Obal | 9,229 | 0 | 92 | 0 | 1,778 | 3,558 |
| `elam_g` | Elam | 9,158 | 0 | 55 | 14 | 1,213 | 2,587 |
| `levi_g` | Levi | 8,271 | 1 | 40 | 9 | 444 | 986 |
| `aram_g` | Aram | 6,876 | 1 | 76 | 30 | 1,238 | 2,602 |
| `asher_g` | Asher | 6,282 | 0 | 20 | 18 | 358 | 763 |
| `god_g` | God | 6,186 | 12 | 10 | 350 | 127 | 1,225 |
| `amen_g` | Amen | 5,552 | 1 | 1 | 195 | 17 | 456 |
| `resen_g` | Resen | 3,824 | 0 | 26 | 0 | 744 | 1,353 |
| `lion_g` | Lion | 3,783 | 0 | 6 | 19 | 101 | 320 |
| `adam_g` | Adam | 3,748 | 0 | 42 | 9 | 424 | 911 |
| `hell_hades_g` | Hades | 3,585 | 0 | 3 | 3 | 12 | 47 |
| `seba_g` | Seba | 2,788 | 0 | 39 | 13 | 593 | 1,140 |
| `titus_emperor_g` | Titus | 2,252 | 0 | 0 | 1 | 1 | 25 |
| `titus_g` | Titus | 2,252 | 0 | 0 | 1 | 148 | 414 |
| `serpent_g` | Serpent | 2,163 | 0 | 0 | 0 | 21 | 45 |
| `boils_g` | Boils | 2,042 | 0 | 3 | 0 | 116 | 276 |
| `sores_g` | Sores | 2,042 | 0 | 3 | 0 | 116 | 276 |
| `otho_g` | Otho | 2,038 | 0 | 0 | 1 | 0 | 7 |
| `vance_g` | Vance | 1,971 | 0 | 0 | 0 | 16 | 67 |
| `cush_g` | Cush | 1,930 | 2 | 5 | 65 | 326 | 838 |

## Read

This output is deliberately broad. Hidden-path-only rows are retained for
inspection. Same-center-word rows are a narrower subset. Same-concept and
same-category center-word rows are related-surface prompts, not automatic
interpretations. Claim-grade filtering still belongs in the controlled
reports.
