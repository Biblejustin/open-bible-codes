# Cities Recovered PDF Text Audit

Status: source-shape audit only. This reads text from PDFs recovered by
`docs/CITIES_PDF_RECOVERY_PROBE.md`; it does not run OCR, normalize city
names, run ELS searches, compute compactness, or verify p-levels.

## Summary

| Item | Count |
| --- | ---: |
| recovered PDF rows audited | 12 |
| extractable text rows | 5 |
| zero-text rows | 4 |
| garbled/non-Latin extract rows | 3 |
| Gans/community family rows | 2 |
| Aumann committee family rows | 9 |
| other family rows | 1 |

## Protocol Anchors

Found anchors: 5 of 5.

| Anchor | Label | Status | Diagnostic |
| --- | --- | --- | --- |
| gans_communities_data_title | cities_pdf_communities_data | found | Gans/Inbal/Bombach communities data title found |
| gans_paper_title | cities_pdf_gans | found | Gans/Inbal/Bombach paper title found |
| aumann_personal_perspective | cities_pdf_dp_365_1 | found | Aumann personal-perspective title found |
| furstenberg_personal_perspective | cities_pdf_dp_365_2 | found | Furstenberg personal-perspective title found |
| witztum_critique_title | cities_pdf_dp_365_4 | found | Witztum critique title found |

## Rows

| Label | Family | Text status | Pages | Text chars | SHA-256 | Source URL |
| --- | --- | --- | ---: | ---: | --- | --- |
| cities_pdf_wrr | other | zero_extractable_text | 10 | 0 | `a63419d9f20ba23f` | [url](https://www.torah-code.org/experiments/WRR.pdf) |
| cities_pdf_dp365a_appendix_6 | aumann_committee | zero_extractable_text | 2 | 0 | `5d9949a0a348bcd9` | [url](https://www.torah-code.org/experiments/dp365A_appendix_6.pdf) |
| cities_pdf_dp365a_appendix_7 | aumann_committee | zero_extractable_text | 5 | 0 | `7b7e2015bb628417` | [url](https://www.torah-code.org/experiments/dp365A_appendix_7.pdf) |
| cities_pdf_dp365a_p1_4 | aumann_committee | extractable_but_garbled_or_nonlatin | 4 | 460 | `90fb6ff653d2fc97` | [url](https://www.torah-code.org/experiments/dp365A_p1-4.pdf) |
| cities_pdf_dp365a_p12_17 | aumann_committee | extractable_but_garbled_or_nonlatin | 6 | 1991 | `127d829147cbc1ec` | [url](https://www.torah-code.org/experiments/dp365A_p12-17.pdf) |
| cities_pdf_dp365a_p5_11 | aumann_committee | extractable_but_garbled_or_nonlatin | 7 | 2913 | `e89e869d452f4294` | [url](https://www.torah-code.org/experiments/dp365A_p5-11.pdf) |
| cities_pdf_dp365a_part_2_p105_111 | aumann_committee | zero_extractable_text | 7 | 0 | `248d3ff6a9fd1042` | [url](https://www.torah-code.org/experiments/dp365A_part_2_p105-111.pdf) |
| cities_pdf_dp_365_1 | aumann_committee | extractable_text | 2 | 6903 | `ae09dc718ad2e798` | [url](https://www.torah-code.org/experiments/dp_365_1.pdf) |
| cities_pdf_dp_365_2 | aumann_committee | extractable_text | 2 | 6087 | `5301f21fa3c1b5b8` | [url](https://www.torah-code.org/experiments/dp_365_2.pdf) |
| cities_pdf_dp_365_4 | aumann_committee | extractable_text | 2 | 5456 | `4dc4119f30430dc2` | [url](https://www.torah-code.org/experiments/dp_365_4.pdf) |
| cities_pdf_communities_data | gans_communities | extractable_text | 8 | 18135 | `ac0b221064e144ca` | [url](https://www.torah-code.org/papers/communities_data.pdf) |
| cities_pdf_gans | gans_communities | extractable_text | 5 | 19499 | `212cb24f918b9a41` | [url](https://www.torah-code.org/papers/gans.pdf) |

## Use Boundary

Rows with extractable text are now separated from image-only or garbled
PDFs for future source-review planning. This audit does not decide which
texts are admissible for a result-bearing protocol. Any later protocol
must separately lock source rows, normalization, filters, Genesis text,
skip caps, compactness metric, and controls before ELS work.

The follow-up queue in `docs/CITIES_SOURCE_REVIEW_QUEUE.md` turns these
text-shape statuses into review lanes without changing this source-shape
boundary. `docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md` further separates the five
readable PDFs by source-review role.
`docs/CITIES_UNREADABLE_PDF_REVIEW.md` separately routes the seven recovered
but unreadable PDFs into OCR/image-only or encoding-or-OCR planning lanes
without running OCR.
`docs/CITIES_UNREADABLE_PDF_OCR_FEASIBILITY.md` then records OCR feasibility
counts for those seven rows without storing OCR text in tracked files.
`docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_PACKET.md` creates ignored local
page-image and OCR-text sidecars and tracks only review paths/counts/status.
