# Cities Unreadable PDF OCR Review Checklist

Status: no-input OCR review checklist. This groups ignored local page-image and OCR-text sidecars into review order and creates contact sheets.
It does not track OCR text, repair text, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.

Reproduce:

```bash
python3 -m scripts.build_cities_unreadable_pdf_ocr_review_checklist --packet reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_packet.csv --contact-sheet-out reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_contact_sheet.png --contact-sheet-dir reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/contact_sheets --out reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_checklist.csv --summary-out reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_checklist_summary.csv --markdown-out docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_CHECKLIST.md --manifest-out reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_checklist.manifest.json
```

## Summary

- Checklist rows: 7.
- PDF rows: 7.
- Pages total: 41.
- Pages with OCR text: 39.
- Pages without OCR text: 2.
- OCR text signal chars: 54324.
- OCR words: 15019.
- OCR lines: 1563.
- Label contact sheets: 7.
- All-pages contact sheet: `reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_contact_sheet.png`.
- Boundary: OCR review checklist only; contact sheets and OCR text sidecars are ignored local review aids; no OCR text in tracked files, no repaired text, no source-row import, no city normalization, no ELS, no compactness, no p-level

![Cities unreadable PDF OCR contact sheet](../reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_contact_sheet.png)

## Checklist

| Rank | Label | Lane | Pages | With text | Empty | Low-signal pages | Contact sheet | Priority | Next action |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | cities_pdf_dp365a_p1_4 | `encoding_or_ocr_candidate` | 4 | 2 | 2 | 3;4 | [sheet](../reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/contact_sheets/cities_pdf_dp365a_p1_4.png) | 1_empty_or_low_ocr_pages | inspect page images for OCR-empty pages 3,4 before any OCR sidecar use |
| 2 | cities_pdf_dp365a_p12_17 | `encoding_or_ocr_candidate` | 6 | 6 | 0 |  | [sheet](../reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/contact_sheets/cities_pdf_dp365a_p12_17.png) | 2_encoding_or_ocr_candidate | compare OCR sidecars against page images before treating garbled extraction as replaceable |
| 3 | cities_pdf_dp365a_p5_11 | `encoding_or_ocr_candidate` | 7 | 7 | 0 | 1 | [sheet](../reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/contact_sheets/cities_pdf_dp365a_p5_11.png) | 2_encoding_or_ocr_candidate | compare low-signal OCR pages 1 against page images before any source-row use |
| 4 | cities_pdf_dp365a_appendix_6 | `ocr_image_only_pdf` | 2 | 2 | 0 |  | [sheet](../reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/contact_sheets/cities_pdf_dp365a_appendix_6.png) | 3_aumann_ocr_image_only | compare OCR sidecars against page images before any Aumann source-row decision |
| 5 | cities_pdf_dp365a_appendix_7 | `ocr_image_only_pdf` | 5 | 5 | 0 |  | [sheet](../reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/contact_sheets/cities_pdf_dp365a_appendix_7.png) | 3_aumann_ocr_image_only | compare OCR sidecars against page images before any Aumann source-row decision |
| 6 | cities_pdf_dp365a_part_2_p105_111 | `ocr_image_only_pdf` | 7 | 7 | 0 |  | [sheet](../reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/contact_sheets/cities_pdf_dp365a_part_2_p105_111.png) | 3_aumann_ocr_image_only | compare OCR sidecars against page images before any Aumann source-row decision |
| 7 | cities_pdf_wrr | `ocr_image_only_pdf` | 10 | 10 | 0 |  | [sheet](../reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/contact_sheets/cities_pdf_wrr.png) | 4_context_pdf | review as context paper; do not import source rows without separate source decision |

## Boundary

- Contact sheets are visual review aids only.
- OCR sidecars remain ignored local files and are not tracked source text.
- Source-row decisions require separate citable decision records.
- No row here changes source admissibility or creates city-name rows.
