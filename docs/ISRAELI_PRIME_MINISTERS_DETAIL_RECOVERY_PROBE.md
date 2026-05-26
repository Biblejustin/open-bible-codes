# Israeli Prime Ministers Detail Recovery Probe

Status: live-source recovery probe only. This does not run ELS searches,
does not modify the cached WRR source bundle, and does not infer missing
detail-page data.

## Summary

| Item | Count |
| --- | ---: |
| missing detail pages probed | 4 |
| rows where expected title appeared | 0 |
| redirected rows | 4 |
| final URL is Torah-code root | 4 |
| canonical URL is Torah-code root | 4 |
| unrelated slot/gambling markers | 4 |
| usable detail pages | 0 |

Current recovery status: `no_detail_pages_recovered`.

## Probe Rows

| Page | Expected title | HTTP | Redirected | Final Root | Expected Text | Spam Marker | Bytes | SHA-256 | Status |
| ---: | --- | ---: | --- | --- | --- | --- | ---: | --- | --- |
| 9 | Benjamin Netanyahu | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unrecovered_detail_page |
| 10 | Ehud Barak | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unrecovered_detail_page |
| 11 | Ariel Sharon | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unrecovered_detail_page |
| 12 | Ehud Olmert | 200 | True | True | False | True | 629155 | `d60a59519b55bcff` | unrecovered_detail_page |

## Source Boundary

This probe checks current live URLs for the four missing detail pages:
`israeli_prime_ministers_9.html` through `_12.html`. A row is treated
as usable only when the download contains the expected prime-minister
title, does not end at the Torah-code root URL, does not declare the
site root as canonical, and lacks unrelated spam markers.

If these pages remain unrecovered, the Israeli prime-ministers lane stays
source-shape only. Do not run a result-bearing protocol from inferred
detail pages.
