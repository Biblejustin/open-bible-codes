# Cities Unreadable PDF OCR Feasibility

Status: OCR feasibility only. This runs local OCR against 12
recovered unreadable Cities PDF rows and records only counts/status. It does
not store OCR text in tracked files, repair text, import source rows,
normalize city names, run ELS searches, compute compactness, or verify
p-levels.

## Summary

- Rows reviewed: 12.
- Rows with OCR text: 11.
- Pages attempted: 61.
- Pages with OCR text: 59.
- OCR text signal chars: 70207.
- OCR text detected rows: 11.
- Low OCR text rows: 0.
- OCR empty rows: 0.
- OCR error rows: 0.

## Rows

| Label | Lane | Pages attempted | Pages with text | Signal chars | Avg chars/page | Status | URL |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| cities_pdf_dp365a_appendix_3 | `ocr_image_only_pdf` | 0 | 0 | 0 | 0.0 | no_pages_attempted | [url](https://www.torah-code.org/experiments/dp365A_appendix_3.pdf) |
| cities_pdf_dp365a_p12_17 | `encoding_or_ocr_candidate` | 6 | 6 | 7576 | 1262.7 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_p12-17.pdf) |
| cities_pdf_dp365a_p1_4 | `encoding_or_ocr_candidate` | 4 | 2 | 2123 | 530.8 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_p1-4.pdf) |
| cities_pdf_dp365a_p5_11 | `encoding_or_ocr_candidate` | 7 | 7 | 4740 | 677.1 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_p5-11.pdf) |
| cities_pdf_dp364_short | `ocr_image_only_pdf` | 6 | 6 | 7041 | 1173.5 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp364_short.pdf) |
| cities_pdf_dp365a_appendix_2 | `ocr_image_only_pdf` | 10 | 10 | 6404 | 640.4 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_appendix_2.pdf) |
| cities_pdf_dp365a_appendix_4 | `ocr_image_only_pdf` | 2 | 2 | 1430 | 715.0 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_appendix_4.pdf) |
| cities_pdf_dp365a_appendix_5 | `ocr_image_only_pdf` | 2 | 2 | 1008 | 504.0 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_appendix_5.pdf) |
| cities_pdf_dp365a_appendix_6 | `ocr_image_only_pdf` | 2 | 2 | 1283 | 641.5 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_appendix_6.pdf) |
| cities_pdf_dp365a_appendix_7 | `ocr_image_only_pdf` | 5 | 5 | 1382 | 276.4 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_appendix_7.pdf) |
| cities_pdf_dp365a_part_2_p105_111 | `ocr_image_only_pdf` | 7 | 7 | 6028 | 861.1 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_part_2_p105-111.pdf) |
| cities_pdf_wrr | `ocr_image_only_pdf` | 10 | 10 | 31192 | 3119.2 | ocr_text_detected | [url](https://www.torah-code.org/experiments/WRR.pdf) |

## Use Boundary

This probe records OCR feasibility metrics only. It does not publish OCR
text, repair text, decide source admissibility, create city-name rows,
or make a result-bearing claim. Any OCR text used later must be reviewed
against page images and locked before source-row normalization or ELS
work.
