# WRR Source Visual Review Notes

Status: visual triage notes only. These are not a locked primary
transcription and not a WRR reproduction.

Source reviewed: `reports/wrr_1994/wrr_1994_paper.pdf`, Table 2 page
render `reports/wrr_1994/wrr_primary_table2_page-06.png`.

## Current Reads

| Queue term | Row | Visual read | Triage read |
| --- | ---: | --- | --- |
| `wrr2_23_app_04` `Y@QBHLWY` | 23 | Row visibly contains `יעקב הלוי`. | OCR miss, not obvious source absence. |
| `wrr2_23_app_05` `MHRYSGL` | 23 | Row visibly contains `מהר"י סג"ל`. | OCR miss, not obvious source absence. |
| `wrr2_30_app_05` `B@LY$RLBB` | 30 | Row visibly contains `ישר לבב`; the visible crop does not clearly show the `בעל` prefix. | Source/title-prefix rule needs review. |
| `wrr2_28_app_04` `B@LPNYM$H` | 28 | Row visibly contains `פני משה`; the visible crop does not clearly show the `בעל` prefix. | Source/title-prefix rule needs review. |
| `wrr2_32_app_04` `$LMHMXLMA` | 32 | Bottom row crop clearly shows `רבי שלמה`; the captured row area does not clearly show full `שלמה מחלמא`. | Needs wider crop or row-boundary/source review. |
| `wrr2_27_date_01` `/+Z/T$RY` | 27 | Row visibly contains `ט"ז תשרי` forms. | OCR-near-match case; page image should be checked before treating as source difference. |
| `wrr2_27_app_06` `M$HZKWTW` | 27 | Row visibly contains Moses/Zechut forms; OCR near match is one edit from imported term. | OCR-near-match case; page image should be checked before treating as source difference. |

## Implication

- The current `ocr_not_matched_with_variant_lead` bucket is mixed.
- Some top rows are plain OCR misses against visible primary-page text.
- Some rows are not simple source errors; they look like title/prefix
  normalization questions, especially `B@L...` terms.
- None of these notes authorize changing WRR terms or claiming reproduction.
  They only narrow the next source-lock work.
