# Israeli Prime Ministers Source Audit

Status: source-shape audit only. This is not an ELS result, not a
statistical test, and not a claim-ready replication.

## Sources

- Main page: `https://www.torah-code.org/experiments/israeli_prime_ministers.shtml`
- Keyword PDF: `https://www.torah-code.org/experiments/Israeli_prime_ministers.pdf`
- Detail pages: `https://www.torah-code.org/experiments/israeli_prime_ministers_1.html` through `_8.html`
- Main SHA-256: `4e31e4ab43ac3bc02568f065ba7a8bf3a746c9d62738a779bb26ab026dba4a19`
- PDF SHA-256: `6186edac84d0e31563865086af02a63690717d61918f93e3ca43fe7fece73b67`

## Parsed Shape

| Item | Count |
| --- | ---: |
| PDF pages from extracted text | 2 |
| PDF prime-minister rows | 12 |
| PDF row index minimum | 1 |
| PDF row index maximum | 12 |
| PDF prime-minister phrase keyword rows | 6 |
| PDF name-keyword rows | 37 |
| machine PDF keyword rows extracted | 43 |
| HTML detail pages found | 8 |
| HTML detail pages with keyword labels | 8 |
| machine HTML detail rows extracted | 8 |
| detail-page gap against PDF rows | 4 |

## Protocol Anchors

Found anchors: 6 of 6.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| main_html | `twelve_people_statement` | found | main page states source population size |
| main_html | `expected_els_10` | found | expected-ELS setting found |
| main_html | `trials_10000` | found | trial count found |
| main_html | `reported_p_level_6_of_10000` | found | reported p-level text found |
| pdf | `pdf_prime_minister_table` | found | PDF prime-minister keyword table found |
| detail_html | `detail_keyword_pages` | found | detail pages with keyword labels found |

## Use Boundary

This audit verifies source shape and exports PDF keyword rows plus HTML
detail-page keyword labels. It also exposes a source-coverage gap: the
PDF lists 12 prime-minister rows, while the downloaded detail-page
sequence has keyword labels for 8 pages. This should be treated as
missing detail-source coverage, not inferred data.

No term normalization, ELS search, compactness calculation, random-placement
control, or p-level verification is performed here.
