# Cities Unreadable PDF OCR Feasibility

Status: OCR feasibility only. This runs local OCR against the seven
recovered unreadable Cities PDFs and records only counts/status. It does
not store OCR text in tracked files, repair text, import source rows,
normalize city names, run ELS searches, compute compactness, or verify
p-levels.

## Summary

- Rows reviewed: 7.
- Rows with OCR text: 7.
- Pages attempted: 41.
- Pages with OCR text: 39.
- OCR text signal chars: 54324.
- OCR text detected rows: 7.
- Low OCR text rows: 0.
- OCR empty rows: 0.
- OCR error rows: 0.

## Rows

| Label | Lane | Pages attempted | Pages with text | Signal chars | Avg chars/page | Status | URL |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| cities_pdf_dp365a_p12_17 | `encoding_or_ocr_candidate` | 6 | 6 | 7576 | 1262.7 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_p12-17.pdf) |
| cities_pdf_dp365a_p1_4 | `encoding_or_ocr_candidate` | 4 | 2 | 2123 | 530.8 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_p1-4.pdf) |
| cities_pdf_dp365a_p5_11 | `encoding_or_ocr_candidate` | 7 | 7 | 4740 | 677.1 | ocr_text_detected | [url](https://www.torah-code.org/experiments/dp365A_p5-11.pdf) |
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

Follow-up review packet: `docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_PACKET.md`
creates ignored local page-image and OCR-text sidecars for those 41 pages
and tracks only paths/counts/status.
