# Under-Construction Experiment Source Audit

Status: source-status audit only. This is not an ELS result, not a
statistical test, and not a claim-ready replication.

## Parsed Shape

| Item | Count |
| --- | ---: |
| source files scanned | 6 |
| under-construction pages | 6 |
| pages linking PDFs | 0 |
| title mismatch pages | 4 |
| heading mismatch pages | 1 |
| Katrina mislabeled as Tsunami | True |

## Page Status

| Experiment | Title | Heading | Under Construction | Title Match | Heading Match |
| --- | --- | --- | --- | --- | --- |
| chumash | Torah Codes -- Cities | Chumash Experiment | True | False | True |
| twin_towers | Torah Codes -- Twin Towers | Twin Towers | True | True | True |
| tsunami | Torah Codes -- Tsunami | Tsunami | True | True | True |
| katrina | Torah Codes -- Tsunami | Tsunami | True | False | False |
| great_rabbis | Torah Codes -- Cities | Great Rabbis Experiment | True | False | True |
| son_rabbis | Torah Codes -- Cities | Son Rabbis Experiment | True | False | True |

## Protocol Anchors

Found anchors: 9 of 9.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| all_pages | `all_pages_under_construction` | found | all audited pages report Under Construction |
| all_pages | `no_pdf_data_links` | found | audited pages do not link source PDFs |
| katrina | `katrina_page_mislabeled_tsunami` | found | Katrina source file title/body is labeled Tsunami |
| chumash | `chumash_under_construction` | found | chumash page reports Under Construction |
| twin_towers | `twin_towers_under_construction` | found | twin_towers page reports Under Construction |
| tsunami | `tsunami_under_construction` | found | tsunami page reports Under Construction |
| katrina | `katrina_under_construction` | found | katrina page reports Under Construction |
| great_rabbis | `great_rabbis_under_construction` | found | great_rabbis page reports Under Construction |
| son_rabbis | `son_rabbis_under_construction` | found | son_rabbis page reports Under Construction |

## Use Boundary

These pages are status placeholders in this crawl. They should not supply
terms, controls, p-values, or source data unless a future source recovery
finds data-bearing pages and records fresh checksums.
