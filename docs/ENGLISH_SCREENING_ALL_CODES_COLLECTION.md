# English KJV Screening All-Codes Collection

This report intentionally keeps every hidden-path ELS row from the surface-context collection and then flags same-word, related-center, center-verse, and span context. It is a collection index, not a claim-grade filter.

## Inputs

- Hits: `reports/english_screening_all_codes/surface_all_codes.csv`
- Summary: `reports/english_screening_all_codes/surface_all_codes_summary.csv`
- Report DB: `reports/db/open_bible_codes.duckdb`
- Corpora: `KJV`

## Collection Counts

| Metric | Count |
| --- | ---: |
| Terms represented | 693 |
| Corpus-term summary rows | 693 |
| Hidden-path rows retained | 666,378 |
| Total hits from summary | 666,378 |
| Any surface-context hits | 192,745 |
| Center word contains same term | 521 |
| Center word contains related term | 5,843 |
| Center verse contains same term | 17,300 |
| Center verse contains related term | 101,229 |
| Hit span contains same/related term | 212,344 |

## Context Labels

| Best context | Rows |
| --- | ---: |
| `hidden_path_only` | 473,633 |
| `same_category_center` | 92,668 |
| `same_category_span` | 69,767 |
| `exact_center` | 17,300 |
| `exact_span` | 13,010 |

## Top Terms

| Term | Concept | Hidden hits | Center word same | Center word related | Center verse same | Center verse related | Span context |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `heth` | Heth | 62,273 | 95 | 549 | 4,790 | 9,698 | 27,563 |
| `otho` | Otho | 30,851 | 0 | 1 | 424 | 195 | 1,362 |
| `nato` | NATO | 27,042 | 0 | 257 | 150 | 4,984 | 8,665 |
| `noah` | Noah | 24,538 | 3 | 274 | 80 | 5,247 | 9,607 |
| `heal` | Heal | 23,995 | 5 | 0 | 563 | 0 | 1,091 |
| `nero` | Nero | 22,308 | 0 | 1 | 166 | 434 | 1,377 |
| `nero` | Nero | 22,308 | 0 | 139 | 166 | 2,316 | 4,361 |
| `hand` | Hand | 16,712 | 45 | 260 | 3,270 | 5,292 | 14,601 |
| `seal` | Seal | 15,971 | 1 | 12 | 80 | 440 | 1,023 |
| `seal` | Seal | 15,971 | 1 | 92 | 80 | 2,147 | 4,279 |
| `seal` | Seal | 15,971 | 1 | 56 | 80 | 980 | 2,026 |
| `star` | Star | 15,885 | 1 | 109 | 59 | 2,002 | 3,899 |
| `horn` | Horn | 15,038 | 5 | 92 | 98 | 1,758 | 3,521 |
| `adar` | Adar | 12,649 | 1 | 183 | 31 | 3,351 | 5,618 |
| `iran` | Iran | 11,859 | 0 | 123 | 45 | 2,317 | 3,937 |
| `amen` | Amen | 11,851 | 5 | 0 | 162 | 18 | 362 |
| `geta` | Geta | 11,416 | 0 | 0 | 7 | 209 | 436 |
| `hail` | Hail | 11,334 | 1 | 97 | 22 | 1,618 | 3,024 |
| `eyes` | Eyes | 10,719 | 11 | 76 | 365 | 1,072 | 2,855 |
| `shem` | Shem | 10,139 | 7 | 85 | 80 | 2,096 | 4,054 |
| `aids` | AIDS | 9,208 | 3 | 32 | 98 | 461 | 1,176 |
| `teeth` | Teeth | 9,011 | 1 | 78 | 21 | 1,080 | 2,361 |
| `eber` | Eber | 8,194 | 1 | 84 | 31 | 1,658 | 3,116 |
| `isis` | ISIS | 8,077 | 0 | 1 | 156 | 82 | 499 |
| `lion` | Lion | 7,803 | 4 | 51 | 56 | 876 | 1,861 |
| `rome` | Rome | 7,648 | 0 | 204 | 44 | 2,976 | 4,948 |
| `tyre` | Tyre | 7,599 | 0 | 269 | 12 | 3,170 | 4,824 |
| `edom` | Edom | 7,332 | 1 | 187 | 79 | 2,610 | 4,391 |
| `mash` | Mash | 7,018 | 1 | 69 | 12 | 1,519 | 2,761 |
| `elam` | Elam | 6,695 | 0 | 155 | 62 | 2,409 | 4,068 |

## Read

This output is deliberately broad. Hidden-path-only rows are retained for
inspection. Same-center-word rows are a narrower subset. Same-concept and
same-category center-word rows are related-surface prompts, not automatic
interpretations. Claim-grade filtering still belongs in the controlled
reports.
