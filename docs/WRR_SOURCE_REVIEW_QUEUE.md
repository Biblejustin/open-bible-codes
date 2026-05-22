# WRR Source Review Queue

Status: diagnostic-only source-review triage from current blocked
WRR pair rows, row-aligned OCR probe output, and zero-hit one-edit
variant leads. It is not a source correction, not a term replacement,
and not a WRR reproduction.

Reproduce:

```bash
python3 -m scripts.build_wrr_source_review_queue --blocked-pairs reports/wrr_1994/wrr_defined_gap_blocked_pairs.csv --variants reports/wrr_1994/wrr_zero_hit_variant_probe.csv --row-ocr reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv --run-label all_lanes_cap1000 --out reports/wrr_1994/wrr_source_review_queue.csv --summary-out reports/wrr_1994/wrr_source_review_queue_summary.csv --markdown-out docs/WRR_SOURCE_REVIEW_QUEUE.md --manifest-out reports/wrr_1994/wrr_source_review_queue.manifest.json
```

## Current Queue

- Run label: `all_lanes_cap1000`.
- Terms queued: 97.

| Bucket | Terms | Blocking pairs | Variant hit total | Row OCR statuses |
| --- | ---: | ---: | ---: | --- |
| `ocr_not_matched_with_variant_lead` | 7 | 21 | 20 | `7 not_matched` |
| `ocr_matched_with_variant_lead` | 32 | 45 | 948 | `32 matched` |
| `ocr_not_matched_no_variant_lead` | 47 | 48 | 0 | `47 not_matched` |
| `ocr_matched_no_variant_lead` | 11 | 11 | 0 | `11 matched` |

## Top Review Targets

| Rank | Term id | Side | Term | Row OCR | Blocking pairs | Variant hits | Best variant | Read |
| ---: | --- | --- | --- | --- | ---: | ---: | --- | --- |
| 1 | `wrr2_27_date_01` | `date` | `/+Z/T$RY` | `not_matched` | 14 | 12 | `delete_one@1:ZT$RY` | OCR did not match imported term and a simple variant has Genesis hits; check source transcription first |
| 2 | `wrr2_27_app_06` | `appellation` | `M$HZKWTW` | `not_matched` | 2 | 1 | `delete_one@2:MHZKWTW` | OCR did not match imported term and a simple variant has Genesis hits; check source transcription first |
| 3 | `wrr2_23_app_04` | `appellation` | `Y@QBHLWY` | `not_matched` | 1 | 2 | `delete_one@2:YQBHLWY` | OCR did not match imported term and a simple variant has Genesis hits; check source transcription first |
| 4 | `wrr2_30_app_05` | `appellation` | `B@LY$RLBB` | `not_matched` | 1 | 2 | `delete_one@8:B(LY$RLB` | OCR did not match imported term and a simple variant has Genesis hits; check source transcription first |
| 5 | `wrr2_23_app_05` | `appellation` | `MHRYSGL` | `not_matched` | 1 | 1 | `delete_one@1:HRYSGL` | OCR did not match imported term and a simple variant has Genesis hits; check source transcription first |
| 6 | `wrr2_28_app_04` | `appellation` | `B@LPNYM$H` | `not_matched` | 1 | 1 | `delete_one@5:B(LPYM$H` | OCR did not match imported term and a simple variant has Genesis hits; check source transcription first |
| 7 | `wrr2_32_app_04` | `appellation` | `$LMHMXLMA` | `not_matched` | 1 | 1 | `delete_one@1:LMHMXLM)` | OCR did not match imported term and a simple variant has Genesis hits; check source transcription first |
| 8 | `wrr2_06_date_01` | `date` | `/KB/KSLW` | `matched` | 6 | 73 | `delete_one@4:KBKLW` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 9 | `wrr2_02_date_01` | `date` | `/YG/SYWN` | `matched` | 5 | 68 | `delete_one@2:YSYWN` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 10 | `wrr2_05_date_01` | `date` | `/Y+/NYSN` | `matched` | 2 | 28 | `delete_one@2:YNYSN` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 11 | `wrr2_27_app_04` | `appellation` | `M$HZKWT` | `matched` | 2 | 11 | `delete_one@4:M$HKWT` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 12 | `wrr2_27_app_05` | `appellation` | `M$HZKWTA` | `matched` | 2 | 1 | `delete_mater@6:M$HZKT)` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 13 | `wrr2_27_app_07` | `appellation` | `MHRMZKWT` | `matched` | 2 | 1 | `delete_one@5:MHRMKWT` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 14 | `wrr2_19_app_09` | `appellation` | `HMHRY+` | `matched` | 1 | 581 | `delete_one@6:HMHRY` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 15 | `wrr2_19_app_07` | `appellation` | `HMHRYM+` | `matched` | 1 | 38 | `delete_one@7:HMHRYM` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 16 | `wrr2_32_app_01` | `appellation` | `RBY$LMH` | `matched` | 1 | 27 | `delete_one@4:RBYLMH` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 17 | `wrr2_24_app_04` | `appellation` | `HRY@MDN` | `matched` | 1 | 16 | `delete_one@6:HRY(MN` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 18 | `wrr2_06_app_02` | `appellation` | `M@$YYHWH` | `matched` | 1 | 14 | `delete_one@2:M$YYHWH` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 19 | `wrr2_26_app_01` | `appellation` | `RBYMNXM` | `matched` | 1 | 10 | `delete_one@6:RBYMNM` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |
| 20 | `wrr2_19_app_01` | `appellation` | `RBYYWSP` | `matched` | 1 | 9 | `delete_one@6:RBYYWP` | OCR matched imported term and a simple variant has Genesis hits; check normalization/rule assumptions without changing source text |

## OCR Context For Top Targets

| Rank | Term id | Normalized term | Row OCR normalized text |
| ---: | --- | --- | --- |
| 1 | `wrr2_27_date_01` | `+ZT$RY` | `כותשריבטזתשרקטזבתשרייותשריביותשרירבתשרי` |
| 2 | `wrr2_27_app_06` | `M$HZKWTW` | `רבימשהזכותאזכותומשהזכותמשהזכותאמשהזכותמהרמזכותהרמיצ` |
| 3 | `wrr2_23_app_04` | `Y(QBHLWY` | `טלזלילולבכבבברכהרלתפולמלרילללהסכריל` |
| 4 | `wrr2_30_app_05` | `B(LY$RLBB` | `אחהערישרלבב` |
| 5 | `wrr2_23_app_05` | `MHRYSGL` | `טלזלילולבכבבברכהרלתפולמלרילללהסכריל` |
| 6 | `wrr2_28_app_04` | `B(LPNYM$H` | `מהרמזהמהרמזהמזליינקולרבימשהמרגליתפנימשה` |
| 7 | `wrr2_32_app_04` | `$LMHMXLM)` | `רבישלמהה` |
| 8 | `wrr2_06_date_01` | `KBKSLW` | `כבכסלובכבכסלוכבבכסלו` |
| 9 | `wrr2_02_date_01` | `YGSYWN` | `ייגסיונביייגסיוניגבסיונ` |
| 10 | `wrr2_05_date_01` | `Y+NYSN` | `יטניסנביטניסניטבניסנ` |
| 11 | `wrr2_27_app_04` | `M$HZKWT` | `רבימשהזכותאזכותומשהזכותמשהזכותאמשהזכותמהרמזכותהרמיצ` |
| 12 | `wrr2_27_app_05` | `M$HZKWT)` | `רבימשהזכותאזכותומשהזכותמשהזכותאמשהזכותמהרמזכותהרמיצ` |

## Interpretation

- Review queue ranks source-transcription and normalization checks.
- Variant leads do not validate the original blocked pairs.
- OCR matches are probe evidence only, not claim-grade primary transcription.
- Locked source rows and pair rules are still required before reproduction language.
