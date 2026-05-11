# English KJV Screening All-Codes Collection

This report intentionally keeps every hidden-path ELS row from the surface-context collection and then flags same-word, related-center, center-verse, and span context. It is a collection index, not a claim-grade filter.

## Inputs

- Hits: `reports/english_screening_all_codes/surface_all_codes.csv`
- Summary: `reports/english_screening_all_codes/surface_all_codes_summary.csv`
- Report DB: `not used`
- Corpora: `KJV`

## Collection Counts

| Metric | Count |
| --- | ---: |
| Terms represented | 1,303 |
| Corpus-term summary rows | 1,303 |
| Hidden-path rows retained | 1,374,596 |
| Total hits from summary | 1,374,596 |
| Any surface-context hits | 322,059 |
| Center word contains same term | 908 |
| Center word contains related term | 9,217 |
| Center verse contains same term | 27,260 |
| Center verse contains related term | 169,292 |
| Hit span contains same/related term | 357,748 |

## Context Labels

| Best context | Rows |
| --- | ---: |
| `hidden_path_only` | 1,052,537 |
| `same_category_center` | 153,021 |
| `same_category_span` | 120,299 |
| `exact_center` | 27,260 |
| `exact_span` | 21,479 |

## Top Terms

| Term | Concept | Hidden hits | Center word same | Center word related | Center verse same | Center verse related | Span context |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `heth` | Heth | 62,273 | 95 | 549 | 4,790 | 9,698 | 27,563 |
| `tree` | Tree | 54,170 | 56 | 136 | 1,217 | 2,608 | 7,206 |
| `tree` | Tree | 54,170 | 56 | 284 | 1,217 | 6,590 | 13,534 |
| `eden` | Eden | 35,476 | 2 | 210 | 104 | 3,898 | 7,094 |
| `otho` | Otho | 30,851 | 0 | 176 | 424 | 4,127 | 8,460 |
| `otho` | Otho | 30,851 | 0 | 1 | 424 | 619 | 2,275 |
| `seed` | Seed | 29,311 | 7 | 198 | 332 | 3,526 | 7,188 |
| `seed` | Seed | 29,311 | 7 | 198 | 332 | 3,526 | 7,188 |
| `seed` | Seed | 29,311 | 7 | 221 | 332 | 3,981 | 8,109 |
| `rent` | Rent | 28,706 | 2 | 210 | 353 | 4,262 | 8,800 |
| `nato` | NATO | 27,042 | 0 | 145 | 150 | 3,288 | 6,280 |
| `nato` | NATO | 27,042 | 0 | 257 | 150 | 5,134 | 8,909 |
| `shot` | Shot | 25,133 | 0 | 4 | 22 | 96 | 257 |
| `noah` | Noah | 24,538 | 3 | 138 | 80 | 3,061 | 5,713 |
| `noah` | Noah | 24,538 | 3 | 277 | 80 | 5,327 | 9,752 |
| `heal` | Heal | 23,995 | 5 | 0 | 563 | 0 | 1,091 |
| `leah` | Leah | 23,788 | 1 | 58 | 25 | 1,111 | 2,165 |
| `nero` | Nero | 22,308 | 0 | 1 | 166 | 434 | 1,377 |
| `nero` | Nero | 22,308 | 0 | 139 | 166 | 2,316 | 4,361 |
| `thin` | Thin | 22,130 | 123 | 34 | 3,219 | 809 | 7,621 |
| `soot` | Soot | 20,843 | 0 | 148 | 6 | 3,189 | 6,247 |
| `hits` | Hits | 19,731 | 0 | 142 | 25 | 3,301 | 6,130 |
| `lane` | Lane | 19,122 | 0 | 137 | 1 | 2,876 | 5,341 |
| `hand` | Hand | 16,712 | 45 | 260 | 3,270 | 5,292 | 14,601 |
| `seal` | Seal | 15,971 | 1 | 12 | 80 | 440 | 1,023 |
| `seal` | Seal | 15,971 | 1 | 18 | 80 | 538 | 1,228 |
| `seal` | Seal | 15,971 | 1 | 92 | 80 | 2,147 | 4,279 |
| `seal` | Seal | 15,971 | 1 | 60 | 80 | 1,779 | 3,597 |
| `seal` | Seal | 15,971 | 1 | 56 | 80 | 980 | 2,026 |
| `star` | Star | 15,885 | 1 | 109 | 59 | 2,002 | 3,899 |

## Read

This output is deliberately broad. Hidden-path-only rows are retained for
inspection. Same-center-word rows are a narrower subset. Same-concept and
same-category center-word rows are related-surface prompts, not automatic
interpretations. Claim-grade filtering still belongs in the controlled
reports.
