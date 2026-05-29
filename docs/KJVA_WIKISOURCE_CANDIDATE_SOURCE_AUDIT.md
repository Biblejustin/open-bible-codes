# KJVA Wikisource Candidate Source Audit

Status: source-status audit only. This is not an ELS result, not a
corpus import, and not a claim-ready replication.

## Setup

This audit checks whether the Wikisource Ballantyne KJV + Apocrypha
candidate can be named as a future source candidate. It fetches the
page, records metadata and source markers, and does not retain or
commit Bible text.

Primary candidate:

- https://en.wikisource.org/wiki/The_Holy_Bible,_containing_the_Old_%26_New_Testament_%26_the_Apocrypha

## Findings

- Source pages checked: 1.
- Fetched pages: 1.
- Pages with Apocrypha marker: 1.
- Pages with public-domain marker: 1.
- Verse-numbered import ready pages: 0.
- Result-ready pages: 0.

This is useful only as a source-candidate check. A future KJVA
replication still needs lawful text import, verse mapping, book-order
lock, collation against the current eBible KJVA source family, checksum
record, term lock, and study-lock sidecar before any ELS run.

## Parsed Shape

| Item | Count |
| --- | ---: |
| source pages | 1 |
| fetched pages | 1 |
| source-candidate pages | 1 |
| verse import ready pages | 0 |
| result ready pages | 0 |
| Apocrypha marker pages | 1 |
| public-domain marker pages | 1 |

## Page Status

| Source | Fetch | Bytes | Title | Apocrypha | KJV | 1769 | Ballantyne | Public Domain | Status |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| wikisource_ballantyne_1911_kjva | fetched | 79785 | The Holy Bible, containing the Old & New Testament & the Apocrypha - Wikisource, the free online library | True | True | True | True | True | source_candidate_needs_import |

## Protocol Anchors

Found anchors: 4 of 4.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| wikisource | `page_fetch_status_recorded` | found | fetch status recorded for the Wikisource candidate |
| wikisource | `apocrypha_marker_recorded` | found | Apocrypha marker presence is recorded without retaining text |
| wikisource | `verse_import_not_ready` | found | no verse-numbered import is declared ready |
| wikisource | `result_not_ready` | found | no result-bearing replication is declared ready |

## Use Boundary

This audit does not import Bible text, normalize verses, run ELS
searches, evaluate controls, or upgrade the completed KJVA bridge
lane. It only records whether the Wikisource page remains a
metadata-level candidate for future source work.
