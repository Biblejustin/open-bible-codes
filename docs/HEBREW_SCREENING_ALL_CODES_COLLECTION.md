# Hebrew Screening All-Codes Collection

This report intentionally keeps every hidden-path ELS row from the surface-context collection and then flags same-word, related-center, center-verse, and span context. It is a collection index, not a claim-grade filter.

## Inputs

- Hits: `reports/hebrew_screening_all_codes/surface_all_codes.csv`
- Summary: `reports/hebrew_screening_all_codes/surface_all_codes_summary.csv`
- Report DB: `reports/db/open_bible_codes.duckdb`
- Corpora: `EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC`

## Collection Counts

| Metric | Count |
| --- | ---: |
| Terms represented | 628 |
| Corpus-term summary rows | 3,340 |
| Hidden-path rows retained | 3,196,917 |
| Total hits from summary | 3,196,917 |
| Any surface-context hits | 1,628,286 |
| Center word contains same term | 9,008 |
| Center word contains related term | 87,005 |
| Center verse contains same term | 114,172 |
| Center verse contains related term | 833,004 |
| Hit span contains same/related term | 1,720,777 |

## Context Labels

| Best context | Rows |
| --- | ---: |
| `hidden_path_only` | 1,568,631 |
| `same_category_center` | 809,688 |
| `same_category_span` | 616,592 |
| `exact_center` | 114,172 |
| `exact_span` | 87,024 |
| `same_concept_span` | 515 |
| `same_concept_center` | 295 |

## Top Terms

| Term | Concept | Hidden hits | Center word same | Center word related | Center verse same | Center verse related | Span context |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `yhwh_h` | YHWH | 216,640 | 6,658 | 2,401 | 83,838 | 25,087 | 205,559 |
| `mary_h` | Mary | 108,806 | 102 | 2,257 | 1,414 | 24,667 | 52,512 |
| `prophet_h` | Prophet | 83,913 | 153 | 1,624 | 1,662 | 17,441 | 43,302 |
| `love_h` | Love | 79,150 | 20 | 1,123 | 314 | 11,890 | 24,029 |
| `peace_h` | Peace | 75,338 | 180 | 985 | 1,462 | 11,138 | 25,125 |
| `iyyar_h` | Iyyar | 72,657 | 0 | 1,471 | 35 | 17,865 | 39,974 |
| `rome_h` | Rome | 69,341 | 6 | 1,645 | 217 | 16,567 | 38,090 |
| `worthy_h` | Worthy | 68,787 | 0 | 207 | 90 | 3,372 | 10,170 |
| `elam_h` | Elam | 62,028 | 0 | 3,315 | 140 | 27,741 | 44,938 |
| `otho_h` | Otho | 58,270 | 16 | 0 | 670 | 10 | 1,803 |
| `jubilee_h` | Jubilee | 58,070 | 14 | 174 | 123 | 2,246 | 6,459 |
| `elul_h` | Elul | 57,414 | 8 | 1,146 | 274 | 14,415 | 32,520 |
| `lion_h` | Lion | 52,033 | 0 | 2,654 | 146 | 26,544 | 44,300 |
| `amorite_h` | Amorite | 49,829 | 54 | 4,363 | 3,731 | 34,827 | 55,743 |
| `bibi_h` | Bibi | 49,308 | 0 | 11 | 249 | 270 | 1,460 |
| `rome_alt_h` | Rome | 47,072 | 0 | 1,028 | 42 | 11,161 | 24,976 |
| `heaven_h` | Heaven | 46,923 | 121 | 81 | 1,361 | 1,045 | 6,217 |
| `jobab_h` | Jobab | 46,688 | 0 | 3,831 | 127 | 31,266 | 43,752 |
| `abyss_h` | Abyss | 46,075 | 10 | 2,219 | 75 | 23,746 | 39,993 |
| `moab_h` | Moab | 44,467 | 32 | 886 | 645 | 9,681 | 23,996 |
| `shoah_h` | Shoah | 41,491 | 0 | 95 | 4 | 1,240 | 3,758 |
| `hell_sheol_h` | Sheol | 37,020 | 137 | 62 | 1,420 | 728 | 4,997 |
| `paul_h` | Paul | 37,020 | 137 | 416 | 1,420 | 5,470 | 13,951 |
| `beaten_h` | Beaten | 36,228 | 0 | 91 | 65 | 1,681 | 5,203 |
| `desolation_h` | Desolation | 34,908 | 22 | 2,038 | 140 | 20,638 | 31,545 |
| `maharal_h` | Maharal | 34,750 | 0 | 0 | 0 | 130 | 344 |
| `oak_h` | Oak | 33,896 | 1 | 60 | 84 | 703 | 2,439 |
| `berea_h` | Berea | 33,467 | 11 | 712 | 255 | 7,827 | 17,756 |
| `temple_h` | Temple | 32,867 | 12 | 813 | 517 | 10,380 | 22,841 |
| `law_h` | Law | 32,524 | 20 | 771 | 204 | 7,245 | 17,261 |

## Read

This output is deliberately broad. Hidden-path-only rows are retained for
inspection. Same-center-word rows are a narrower subset. Same-concept and
same-category center-word rows are related-surface prompts, not automatic
interpretations. Claim-grade filtering still belongs in the controlled
reports.
