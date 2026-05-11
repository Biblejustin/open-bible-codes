# External Claim Source All-Codes Collection

This report keeps every length-4+ hidden-path ELS row from supplemental external-source claim and critique term lists across Bible and language-matched secular-control corpora. It is a collection index, not a claim-grade result.

## Inputs

- Hits: `reports/external_claim_source_all_codes/surface_all_codes.csv`
- Summary: `reports/external_claim_source_all_codes/surface_all_codes_summary.csv`
- Report DB: `reports/db/open_bible_codes.duckdb`
- Corpora: `BYZ_NT, EBIBLE_WLC, ENG_MOBY_DICK, ENG_SHAKESPEARE, ENG_WAR_AND_PEACE, GRK_HERODOTUS, GRK_ILIAD, GRK_ODYSSEY, HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER, KJV, KJVA, LXX, MAM, MT_WLC, SBLGNT, TCG_NT, TR_NT, UHB, UXLC`

## Collection Counts

| Metric | Count |
| --- | ---: |
| Terms represented | 513 |
| Corpus-term summary rows | 3,708 |
| Hidden-path rows retained | 8,443,775 |
| Total hits from summary | 8,443,775 |
| Any surface-context hits | 7,114,738 |
| Center word contains same term | 14,043 |
| Center word contains related term | 131,580 |
| Center verse contains same term | 5,817,284 |
| Center verse contains related term | 10,063,317 |
| Hit span contains same/related term | 16,743,038 |

## Context Labels

| Best context | Rows |
| --- | ---: |
| `exact_center` | 5,817,284 |
| `hidden_path_only` | 1,329,037 |
| `same_category_center` | 613,470 |
| `same_category_span` | 564,963 |
| `exact_span` | 117,813 |
| `same_concept_span` | 622 |
| `same_concept_center` | 586 |

## Top Terms

| Term | Concept | Hidden hits | Center word same | Center word related | Center verse same | Center verse related | Span context |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `יהוה` (YHWH; English: YHWH Esther Acrostic) | YHWH Esther Acrostic | 366,726 | 3,332 | 0 | 300,325 | 0 | 330,257 |
| `יהוה` (YHWH; English: YHWH) | YHWH | 366,726 | 3,332 | 7,060 | 300,325 | 578,782 | 964,193 |
| `יהוה` (YHWH; English: YHWH) | YHWH | 366,726 | 3,332 | 7,865 | 300,325 | 576,008 | 961,088 |
| `לוימ` (lwym; English: Levites) | Levites | 289,416 | 209 | 6,804 | 200,665 | 430,157 | 668,490 |
| `לוימ` (lwym; English: Levites) | Levites | 289,416 | 209 | 7,359 | 200,665 | 433,123 | 670,957 |
| `לוימ` (lwym; English: Levites) | Levites | 289,416 | 209 | 5,956 | 200,665 | 426,876 | 664,585 |
| `לואי` (lwy; English: Louis) | Louis | 243,999 | 37 | 0 | 157,837 | 126,727 | 285,494 |
| `יונה` (ywnh; English: Jonah) | Jonah | 199,026 | 48 | 4,474 | 142,430 | 303,381 | 466,844 |
| `יונה` (ywnh; English: Jonah) | Jonah | 199,026 | 48 | 4,823 | 142,430 | 305,017 | 468,231 |
| `מריה` (mryh; English: Moriah) | Moriah | 167,973 | 26 | 3,992 | 117,528 | 249,135 | 394,377 |
| `מריה` (mryh; English: Moriah) | Moriah | 167,973 | 26 | 4,372 | 117,528 | 250,837 | 396,382 |
| `מריה` (mryh; English: Moriah) | Moriah | 167,973 | 26 | 3,502 | 117,528 | 247,371 | 392,093 |
| `מרימ` (mrym; English: Mary) | Mary | 167,883 | 257 | 3,961 | 114,187 | 247,062 | 384,223 |
| `מרימ` (mrym; English: Mary) | Mary | 167,883 | 257 | 4,267 | 114,187 | 248,550 | 385,420 |
| `מרימ` (mrym; English: Mary) | Mary | 167,883 | 257 | 3,496 | 114,187 | 245,329 | 382,461 |
| `מתיה` (mtyh; English: Matthias) | Matthias | 155,352 | 10 | 3,560 | 106,849 | 230,776 | 355,193 |
| `מתיה` (mtyh; English: Matthias) | Matthias | 155,352 | 10 | 3,892 | 106,849 | 232,114 | 356,224 |
| `מתיה` (mtyh; English: Matthias) | Matthias | 155,352 | 10 | 3,155 | 106,849 | 229,492 | 353,535 |
| `אללה` (llh; English: Allah) | Allah | 129,699 | 0 | 0 | 84,874 | 84,759 | 169,882 |
| `תומא` (twm; English: Thomas) | Thomas | 129,190 | 0 | 3,056 | 86,508 | 188,002 | 289,023 |
| `תומא` (twm; English: Thomas) | Thomas | 129,190 | 0 | 3,298 | 86,508 | 188,936 | 289,820 |
| `תומא` (twm; English: Thomas) | Thomas | 129,190 | 0 | 2,775 | 86,508 | 186,797 | 287,451 |
| `rent` | Rent | 128,368 | 77 | 1,078 | 65,862 | 74,687 | 149,880 |
| `שילה` (shylh; English: Shiloh) | Shiloh | 124,169 | 4 | 2,837 | 82,270 | 179,317 | 276,092 |
| `שילה` (shylh; English: Shiloh) | Shiloh | 124,169 | 4 | 3,184 | 82,270 | 180,725 | 277,290 |
| `שואה` (shwh; English: Holocaust) | Holocaust | 123,462 | 2 | 235 | 81,975 | 165,444 | 250,486 |
| `שואה` (shwh; English: Holocaust) | Holocaust | 123,462 | 2 | 2 | 81,975 | 115,366 | 197,417 |
| `אלונ` (lwn; English: Oak) | Oak | 108,799 | 8 | 1,819 | 74,987 | 85,127 | 171,661 |
| `תורה` (twrh; English: Torah) | Torah | 108,347 | 128 | 2,054 | 76,027 | 165,374 | 251,502 |
| `תורה` (twrh; English: Torah) | Torah | 108,347 | 128 | 2,243 | 76,027 | 165,319 | 251,494 |

## Read

This output is deliberately broad. Hidden-path-only rows are retained for
inspection. Same-center-word rows are a narrower subset. Same-concept and
same-category center-word rows are related-surface prompts, not automatic
interpretations. Claim-grade filtering still belongs in the controlled
reports.
