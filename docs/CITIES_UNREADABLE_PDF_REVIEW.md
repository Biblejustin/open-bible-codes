# Cities Unreadable PDF Review

Status: OCR/encoding planning only. This classifies recovered Cities PDFs
that are image-only or garbled by text extraction. It does not run OCR,
repair text, import source rows, normalize city names, run ELS searches,
compute compactness, or verify p-levels.

## Summary

- Unreadable rows reviewed: 7.
- OCR/image-only rows: 4.
- Encoding-or-OCR candidate rows: 3.
- Aumann committee rows: 6.
- Other-family rows: 1.
- Pages needing review: 41.
- Garbled text chars: 5364.

## Rows

| Label | Family | Lane | Text status | Pages | Text chars | Role hint | Route | Next action | URL |
| --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| cities_pdf_dp365a_p12_17 | aumann_committee | `encoding_or_ocr_candidate` | extractable_but_garbled_or_nonlatin | 6 | 1991 | aumann_committee_recovered_segment | alternate_extraction_or_ocr_fallback | try alternate extraction; if still garbled, run OCR before source-role classification | [url](https://www.torah-code.org/experiments/dp365A_p12-17.pdf) |
| cities_pdf_dp365a_p1_4 | aumann_committee | `encoding_or_ocr_candidate` | extractable_but_garbled_or_nonlatin | 4 | 460 | aumann_committee_recovered_segment | alternate_extraction_or_ocr_fallback | try alternate extraction; if still garbled, run OCR before source-role classification | [url](https://www.torah-code.org/experiments/dp365A_p1-4.pdf) |
| cities_pdf_dp365a_p5_11 | aumann_committee | `encoding_or_ocr_candidate` | extractable_but_garbled_or_nonlatin | 7 | 2913 | aumann_committee_recovered_segment | alternate_extraction_or_ocr_fallback | try alternate extraction; if still garbled, run OCR before source-role classification | [url](https://www.torah-code.org/experiments/dp365A_p5-11.pdf) |
| cities_pdf_dp365a_appendix_6 | aumann_committee | `ocr_image_only_pdf` | zero_extractable_text | 2 | 0 | aumann_committee_recovered_segment | page_image_or_ocr_review | inspect page images and run OCR before source-role classification | [url](https://www.torah-code.org/experiments/dp365A_appendix_6.pdf) |
| cities_pdf_dp365a_appendix_7 | aumann_committee | `ocr_image_only_pdf` | zero_extractable_text | 5 | 0 | aumann_committee_recovered_segment | page_image_or_ocr_review | inspect page images and run OCR before source-role classification | [url](https://www.torah-code.org/experiments/dp365A_appendix_7.pdf) |
| cities_pdf_dp365a_part_2_p105_111 | aumann_committee | `ocr_image_only_pdf` | zero_extractable_text | 7 | 0 | aumann_committee_recovered_segment | page_image_or_ocr_review | inspect page images and run OCR before source-role classification | [url](https://www.torah-code.org/experiments/dp365A_part_2_p105-111.pdf) |
| cities_pdf_wrr | other | `ocr_image_only_pdf` | zero_extractable_text | 10 | 0 | wrr_context_paper | page_image_or_ocr_review | inspect page images and run OCR before source-role classification | [url](https://www.torah-code.org/experiments/WRR.pdf) |

## Use Boundary

This review is planning metadata for the seven recovered but unreadable
Cities PDFs. It does not repair the PDFs, create OCR text, decide source
admissibility, create city-name rows, or make a result-bearing claim.
Any later OCR output must be reviewed and locked before source-row
normalization or ELS work.
