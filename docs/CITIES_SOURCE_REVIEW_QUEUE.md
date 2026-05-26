# Cities Source Review Queue

Status: source-review triage only. This joins the PDF recovery probe and
recovered-PDF text audit into next-action buckets. It does not run OCR,
normalize city names, run ELS searches, compute compactness, or verify
p-levels.

## Summary

- Rows queued: 35.

| Lane | Rows | Families | Source pages | Next action |
| --- | ---: | --- | --- | --- |
| `review_extractable_text` | 5 | aumann_committee:3; gans_communities:2 | torah_code_experiment_cities_aumann:3; torah_code_experiment_cities_gans:2 | review extracted text headings and table scope before any city-row normalization |
| `ocr_image_only_pdf` | 4 | aumann_committee:3; other:1 | torah_code_experiment_cities_aumann:4 | OCR or page-image review needed before source rows can be inspected |
| `encoding_or_ocr_candidate` | 3 | aumann_committee:3 | torah_code_experiment_cities_aumann:3 | try alternate extraction or OCR; current text stream is not source-ready |
| `recover_missing_pdf` | 23 | aumann_committee:20; simon_mckay:3 | torah_code_experiment_cities;torah_code_experiment_cities_aumann:1; torah_code_experiment_cities_aumann:19; torah_code_experiment_cities_simon_mckay:3 | manual live/archive recovery needed before text or source-row review |

## Queue

| Priority | Lane | Label | Family | Text status | Pages | Text chars | Blocker | URL |
| ---: | --- | --- | --- | --- | ---: | ---: | --- | --- |
| 1 | `review_extractable_text` | cities_pdf_dp_365_1 | aumann_committee | extractable_text | 2 | 6903 | source review still needed | [url](https://www.torah-code.org/experiments/dp_365_1.pdf) |
| 1 | `review_extractable_text` | cities_pdf_dp_365_2 | aumann_committee | extractable_text | 2 | 6087 | source review still needed | [url](https://www.torah-code.org/experiments/dp_365_2.pdf) |
| 1 | `review_extractable_text` | cities_pdf_dp_365_4 | aumann_committee | extractable_text | 2 | 5456 | source review still needed | [url](https://www.torah-code.org/experiments/dp_365_4.pdf) |
| 1 | `review_extractable_text` | cities_pdf_communities_data | gans_communities | extractable_text | 8 | 18135 | source review still needed | [url](https://www.torah-code.org/papers/communities_data.pdf) |
| 1 | `review_extractable_text` | cities_pdf_gans | gans_communities | extractable_text | 5 | 19499 | source review still needed | [url](https://www.torah-code.org/papers/gans.pdf) |
| 2 | `ocr_image_only_pdf` | cities_pdf_dp365a_appendix_6 | aumann_committee | zero_extractable_text | 2 | 0 | no extractable text from recovered PDF | [url](https://www.torah-code.org/experiments/dp365A_appendix_6.pdf) |
| 2 | `ocr_image_only_pdf` | cities_pdf_dp365a_appendix_7 | aumann_committee | zero_extractable_text | 5 | 0 | no extractable text from recovered PDF | [url](https://www.torah-code.org/experiments/dp365A_appendix_7.pdf) |
| 2 | `ocr_image_only_pdf` | cities_pdf_dp365a_part_2_p105_111 | aumann_committee | zero_extractable_text | 7 | 0 | no extractable text from recovered PDF | [url](https://www.torah-code.org/experiments/dp365A_part_2_p105-111.pdf) |
| 2 | `ocr_image_only_pdf` | cities_pdf_wrr | other | zero_extractable_text | 10 | 0 | no extractable text from recovered PDF | [url](https://www.torah-code.org/experiments/WRR.pdf) |
| 3 | `encoding_or_ocr_candidate` | cities_pdf_dp365a_p12_17 | aumann_committee | extractable_but_garbled_or_nonlatin | 6 | 1991 | pdftotext output is garbled or non-Latin | [url](https://www.torah-code.org/experiments/dp365A_p12-17.pdf) |
| 3 | `encoding_or_ocr_candidate` | cities_pdf_dp365a_p1_4 | aumann_committee | extractable_but_garbled_or_nonlatin | 4 | 460 | pdftotext output is garbled or non-Latin | [url](https://www.torah-code.org/experiments/dp365A_p1-4.pdf) |
| 3 | `encoding_or_ocr_candidate` | cities_pdf_dp365a_p5_11 | aumann_committee | extractable_but_garbled_or_nonlatin | 7 | 2913 | pdftotext output is garbled or non-Latin | [url](https://www.torah-code.org/experiments/dp365A_p5-11.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_gans_original_report | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/papers/gans_original_report.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp364_appendix_3 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp364_appendix_3.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp364_appendix_4 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp364_appendix_4.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp364_appendix_5 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp364_appendix_5.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp364_short | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp364_short.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_appendix_1 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_appendix_1.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_appendix_2 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_appendix_2.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_appendix_3 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_appendix_3.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_appendix_4 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_appendix_4.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_appendix_5 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_appendix_5.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_p17_24 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_p17-24.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_part_2_p111_130 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_part_2_p111-130.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_part_2_p131_139 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_part_2_p131-139.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_part_2_p140_143 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_part_2_p140-143.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_part_2_p144_152 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_part_2_p144-152.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_part_2_p153_159 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_part_2_p153-159.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_part_2_p90_96 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_part_2_p90-96.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_part_2_p97_105 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_part_2_p97-105.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp365a_part_2_preface | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp365A_part_2_preface.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_dp_365_3 | aumann_committee | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/dp_365_3.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_cities_comparison | simon_mckay | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/cities_comparison.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_margcities | simon_mckay | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/Margcities.pdf) |
| 4 | `recover_missing_pdf` | cities_pdf_margoliot_cities_data | simon_mckay | not_audited |  |  | no usable PDF recovered | [url](https://www.torah-code.org/experiments/Margoliot_Cities_Data.pdf) |

## Use Boundary

This queue is planning metadata. It does not decide source admissibility,
does not create city-name rows, and does not make any result-bearing claim.
Any later result protocol must separately lock source rows, normalization,
filters, Genesis text, skip caps, compactness metric, and controls.

The extractable-text role review in `docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md`
separates the five readable PDFs into data-table, method-context, and
commentary/critique lanes without changing this queue's boundary. The
data-table lane now points at `docs/GANS_COMMUNITIES_SOURCE_AUDIT.md` for
existing source-shape coverage only: 66 records and 210 community rows, with no
source-row import.
