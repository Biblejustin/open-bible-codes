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
| Terms represented | 573 |
| Corpus-term summary rows | 2,380 |
| Hidden-path rows retained | 481,912 |
| Total hits from summary | 481,912 |
| Any surface-context hits | 82,518 |
| Center word contains same term | 294 |
| Center word contains related term | 1,954 |
| Center verse contains same term | 6,641 |
| Center verse contains related term | 34,733 |
| Hit span contains same/related term | 89,789 |

## Context Labels

| Best context | Rows |
| --- | ---: |
| `hidden_path_only` | 399,394 |
| `same_category_span` | 36,101 |
| `same_category_center` | 31,914 |
| `exact_span` | 7,862 |
| `exact_center` | 6,641 |

## Top Terms

| Term | Concept | Hidden hits | Center word same | Center word related | Center verse same | Center verse related | Span context |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `αννα` (anna; English: Hannah) | Hannah | 45,600 | 14 | 290 | 164 | 4,314 | 9,662 |
| `αιμα` (haima; English: Blood) | Blood | 36,750 | 38 | 118 | 1,398 | 2,338 | 7,967 |
| `νατο` (nato; English: NATO) | NATO | 36,345 | 79 | 48 | 1,606 | 1,357 | 6,663 |
| `ναοσ` (naos; English: Temple) | Temple | 35,617 | 4 | 9 | 97 | 223 | 767 |
| `ναοσ` (naos; English: Temple) | Temple | 35,617 | 4 | 78 | 97 | 1,618 | 3,774 |
| `υιοσ` (huios; English: Son) | Son | 22,294 | 29 | 134 | 645 | 2,022 | 6,038 |
| `σιων` (Sion; English: Zion) | Zion | 19,934 | 2 | 171 | 134 | 1,966 | 4,407 |
| `αιμα` (haima; English: Blood) | Blood | 18,375 | 19 | 30 | 699 | 809 | 3,227 |
| `κινα` (kina; English: China) | China | 16,489 | 0 | 74 | 33 | 1,156 | 2,644 |
| `ιραν` (iran; English: Iran) | Iran | 15,745 | 4 | 39 | 93 | 1,109 | 2,703 |
| `λεια` (leia; English: Leah) | Leah | 15,339 | 45 | 81 | 597 | 1,390 | 4,254 |
| `σαλα` (Sala; English: Shelah) | Shelah | 13,936 | 0 | 117 | 12 | 2,712 | 5,363 |
| `παισ` (pais; English: Servant) | Servant | 13,832 | 8 | 15 | 71 | 131 | 407 |
| `δασα` (dasa; English: Lasha) | Lasha | 9,878 | 1 | 64 | 57 | 1,682 | 3,601 |
| `ευαλ` (eual; English: Obal) | Obal | 9,229 | 0 | 92 | 0 | 1,778 | 3,558 |
| `ελαμ` (Elam; English: Elam) | Elam | 9,158 | 0 | 55 | 14 | 1,213 | 2,587 |
| `λευι` (leui; English: Levi) | Levi | 8,271 | 1 | 40 | 9 | 444 | 986 |
| `αραμ` (aram; English: Aram) | Aram | 6,876 | 1 | 76 | 30 | 1,238 | 2,602 |
| `ασηρ` (aser; English: Asher) | Asher | 6,282 | 0 | 20 | 18 | 358 | 763 |
| `θεοσ` (theos; English: God) | God | 6,186 | 12 | 18 | 350 | 196 | 1,383 |
| `αμην` (amen; English: Amen) | Amen | 5,552 | 1 | 1 | 195 | 17 | 456 |
| `ωσηε` (osee; English: Hosea) | Hosea | 5,024 | 0 | 6 | 1 | 77 | 165 |
| `αμωσ` (amos; English: Amos) | Amos | 4,239 | 1 | 4 | 1 | 50 | 164 |
| `δαση` (dase; English: Resen) | Resen | 3,824 | 0 | 26 | 0 | 744 | 1,353 |
| `λεων` (leon; English: Lion) | Lion | 3,783 | 0 | 6 | 19 | 101 | 320 |
| `αδαμ` (adam; English: Adam) | Adam | 3,748 | 0 | 42 | 9 | 424 | 911 |
| `αδησ` (ades; English: Hades) | Hades | 3,585 | 0 | 3 | 3 | 12 | 47 |
| `σαβα` (saba; English: Seba) | Seba | 2,788 | 0 | 39 | 13 | 593 | 1,140 |
| `τιτοσ` (titos; English: Titus) | Titus | 2,252 | 0 | 0 | 1 | 1 | 25 |
| `τιτοσ` (titos; English: Titus) | Titus | 2,252 | 0 | 0 | 1 | 148 | 414 |

## Read

This output is deliberately broad. Hidden-path-only rows are retained for
inspection. Same-center-word rows are a narrower subset. Same-concept and
same-category center-word rows are related-surface prompts, not automatic
interpretations. Claim-grade filtering still belongs in the controlled
reports.
