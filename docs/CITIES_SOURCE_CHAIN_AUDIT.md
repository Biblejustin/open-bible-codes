# Cities Source Chain Audit

Status: source-shape audit only. This is not an ELS result, not a
statistical test, and not a claim-ready replication.

## Parsed Shape

| Item | Count |
| --- | ---: |
| source files scanned | 13 |
| HTML files | 11 |
| `.pdf` named files | 8 |
| PDF-header files | 2 |
| PDF files with `pdfinfo` pages | 1 |
| PDF files with extractable text | 0 |
| `.pdf` files that are HTML wrappers | 6 |
| PDF-header files with parse errors | 1 |
| PDF files with no extracted text | 1 |
| Wayback job-failed wrapper files | 5 |
| HTML links | 879 |
| HTML PDF links | 36 |

## Protocol Anchors

Found anchors: 7 of 7.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| cities_main | `gans_original_p_level_6_of_1000000` | found | main page reports original Gans p-level |
| gans_page | `gans_revised_p_level_4_of_1000000` | found | Gans communities page reports revised p-level |
| aumann_page | `aumann_non_significant_result` | found | Aumann page reports non-significant experiments |
| simon_mckay_page | `simon_city_count_330` | found | Simon/McKay page reports 330 Margolioth city names |
| simon_mckay_page | `simon_used_count_197` | found | Simon/McKay page reports 197 used city names found in Margolioth |
| simon_mckay_page | `simon_length_filter_5_8` | found | Simon/McKay page reports 5..8 city-name length filter |
| downloaded_files | `html_wrappers_present` | found | some downloaded .pdf files are HTML wrappers |

## Use Boundary

This audit records which Cities source-chain files are actually usable local
sources. Several downloaded files with `.pdf` names are Wayback/HTML wrapper
pages, not PDFs; the local wrapper pages report failed Wayback save jobs.
Those files must not be treated as source data unless the underlying PDFs
are recovered and checksummed.

The isolated recovery probe in `docs/CITIES_PDF_RECOVERY_PROBE.md` checks the
35 linked Cities/Aumann/Simon-McKay PDF URLs against the live site and exact-URL
Wayback snapshots. It currently recovers 12 archived PDFs and leaves 23 PDF
links unrecovered; those recovered files are still source-shape inputs only.

No city-name rows are normalized, no ELS search is run, and no p-level is
verified here.
