# KJVA Source Candidate Status

Status: source-status rollup only. This is not an ELS result, not a
corpus import, not a source lock, and not a claim-ready replication.

## Setup

This page collects the current KJVA/apocrypha source-candidate state in one
place. It summarizes source status from the current local config and the three
metadata-only source-candidate audits already tracked in this repository.

This rollup does not import Bible text, normalize verses, run ELS searches,
evaluate controls, or upgrade the completed KJVA bridge lane.

## Current Read

- Ready independent KJVA replication sources: 0.
- Possible independent KJVA metadata candidates: 1.
- Result-ready sources: 0.
- source-lock ready sources: 0.

No result-bearing KJVA replication is source-ready yet. Current KJVA bridge
outputs remain review material, and the completed KJVA prospective bridge lane
remains negative under its registered controls.

## Source Matrix

| Source | Current status | Why it matters | Next need |
| --- | --- | --- | --- |
| current eBible KJV + Apocrypha source family | usable rerun source | This is the current local KJVA/apocrypha corpus family in `configs/example_ebible_engkjv_apocrypha.toml`. The source-coverage audit records 14 apocrypha/deuterocanon books, 5720 verses, and 593090 normalized letters for `KJVA`. It can reproduce or rerun current KJVA work, but it is not an independent replication source. | Keep as current-source rerun lane only unless a new study lock says otherwise. |
| CrossWire GitLab KJV/KJVA | possible independent metadata candidate | The metadata audit found `kjva.osis.xml` and `kjvdc.xml` path names in the CrossWire GitLab KJV repository. This makes it a stronger future source candidate than a KJV-only repository, but no local source import, verse mapping, collation, checksum lock, or source-use decision exists yet. | License/source-use decision, local ignored text import if allowed, verse mapping, book-order lock, collation against current eBible KJVA, checksums, term lock, and study-lock sidecar. |
| Wikisource Ballantyne 1911 KJV + Apocrypha | metadata-level future source candidate | The source audit found a public-domain KJV + Apocrypha page with markers. The book-coverage probe found 36 existing KJV book links, 30 KJV redlinks, and 0 apocrypha/deuterocanon book links on the parsed main-page book table. No verse-numbered import, collation, checksum, or book-order lock exists here. | Lawful import decision, apocrypha/deuterocanon coverage source, verse mapping, book-order lock, collation against current eBible KJVA, checksums, term lock, and study-lock sidecar. |
| `seven1m/open-bibles` | KJV-only metadata candidate | The audit found KJV OSIS metadata, but current tree metadata does not show apocrypha or deuterocanon coverage. It is not a KJVA/apocrypha source candidate for current bridge replication work. | No KJVA bridge use unless a separate lawful apocrypha source is found and audited. |

## Audit Links

- `docs/KJVA_APOCRYPHA_BRIDGE_NEXT_REPLICATION_DESIGN.md`
- `docs/APOCRYPHA_SOURCE_COVERAGE.md`
- `docs/KJVA_CROSSWIRE_CANDIDATE_SOURCE_AUDIT.md`
- `docs/KJVA_WIKISOURCE_CANDIDATE_SOURCE_AUDIT.md`
- `docs/KJVA_WIKISOURCE_BOOK_COVERAGE_PROBE.md`
- `docs/KJVA_OPEN_BIBLES_CANDIDATE_SOURCE_AUDIT.md`

## Required Before Any Future Result Run

A future KJVA/apocrypha bridge replication needs these locks before output:

- exact source stream
- license/source-use decision
- verse mapping
- book-order decision
- source checksum record
- collation against the current eBible KJVA source family
- fresh term lock
- leakage audit
- study-lock sidecar
- fixed controls

## Use Boundary

This rollup is a guardrail document. It prevents the metadata-only source
audits from being read as replication-ready work. It does not add a new
corpus, does not add new terms, does not create candidates, and does not change
any KJVA result status.
