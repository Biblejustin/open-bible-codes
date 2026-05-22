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
| `wrr2_30_app_05` `B@LY$RLBB` | 30 | Full page visibly contains `ישר לבב`; it does not visibly show the `בעל` prefix in the Hebrew name cell. Row OCR normalizes the name cell as `אחהערישרלבב`, not `בעלישרלבב`. | Source/title-prefix rule needs review. |
| `wrr2_28_app_04` `B@LPNYM$H` | 28 | Full page visibly contains `פני משה`; it does not visibly show the `בעל` prefix in the Hebrew name cell. Row OCR contains `רבי משה`, `מרגלית`, and `פני משה`, not `בעלפנימשה`. | Source/title-prefix rule needs review. |
| `wrr2_32_app_04` `$LMHMXLMA` | 32 | Full page and bottom row crop visibly show `רבי שלמה`; the primary Hebrew name cell does not visibly show full `שלמה מחלמא`. Row OCR normalizes the name cell as `רבישלמהה`. | Source/pair-rule review needed; the English row label says `of Chelm`, but the primary Hebrew cell is not enough by itself to verify this secondary Hebrew appellation. |
| `wrr2_27_date_01` `/+Z/T$RY` | 27 | Row visibly contains `ט"ז תשרי` forms. | OCR-near-match case; page image should be checked before treating as source difference. |
| `wrr2_27_app_06` `M$HZKWTW` | 27 | Row visibly contains Moses/Zechut forms; OCR near match is one edit from imported term. | OCR-near-match case; page image should be checked before treating as source difference. |

## Local WNP Critique Context

Source reviewed: `reports/wrr_1994/wnp_en.html`.

| Topic | Local source context | Triage read |
| --- | --- | --- |
| Rabbi II-27 Zacut forms | WNP argues the primary last-name form is `zkvt`, and removes `zkvta`, `zkvtv`, `mwh zkvta`, and `mwh zkvtv`. | The row-27 `M$HZKWTW` blocker is not just OCR noise; it is also a known disputed appellation-form issue. |
| Rabbi II-30 Yosher-Levav | WNP argues `ywr lbb` is a book title, not a valid appellation of Ricchi, and removes it. | The `B@LY$RLBB` blocker should be treated as a title/appellation-rule issue, not a simple OCR miss. |
| Rabbi II-32 Chelma | WNP argues `clma`/`cilma` spellings and `wlmh clma` forms are plausible appellations, while noting length-filter effects. | The `$LMHMXLMA` blocker needs source/pair-rule review, not dismissal from the cropped primary row alone. |

## Implication

- The current `ocr_not_matched_with_variant_lead` bucket is mixed.
- Some top rows are plain OCR misses against visible primary-page text.
- Some rows are not simple source errors; they look like title/prefix
  normalization questions, especially `B@L...` terms.
- Row 32 is a separate Hebrew-cell versus English-label issue: the page label
  gives `of Chelm`, while the visible Hebrew name cell only supports `רבי שלמה`
  in this visual/OCR pass.
- None of these notes authorize changing WRR terms or claiming reproduction.
  They only narrow the next source-lock work.
