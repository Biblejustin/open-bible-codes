# KJVA Source Candidate Status

Status: source-status rollup only. This is not an ELS result, not a
corpus import, not a source lock, and not a claim-ready replication.

## Setup

This page collects the current KJVA/apocrypha source-candidate state in one
place. It summarizes source status from the current local config, the
current eBible KJVA source-lock sidecar, the
metadata-only source-candidate audits already tracked in this repository, the
heading-level Project Gutenberg coverage probe, the Project Gutenberg
source-lock prep count comparison, the source-lock decision packet, the
source-lock blocker packet, the Hakkaac boundary-candidate audit, the
Hakkaac full-marker coverage audit, the Hakkaac ignored-local collation
audit, the Hakkaac source-lock decision packet, the split-source role sidecar,
the source-policy blocker packet, and the next-result gate.

This rollup does not import Bible text, normalize verses, run ELS searches,
evaluate controls, or upgrade the completed KJVA bridge lane.

## Current Read

- Ready independent KJVA replication sources: 0.
- Possible independent KJVA metadata candidates: 2.
- Public-domain split KJV+Apocrypha coverage candidates needing collation: 1.
- Result-ready sources: 0.
- source-lock ready sources: 0.

No result-bearing KJVA replication is source-ready yet. Current KJVA bridge
outputs remain review material, and the completed KJVA prospective bridge lane
remains negative under its registered controls. The next-result gate records
11 gate rows: only current-source rerun reproducibility is ready, 10 gates are
blocked, and new result-bearing KJVA output is not allowed.

## Source Matrix

| Source | Current status | Why it matters | Next need |
| --- | --- | --- | --- |
| current eBible KJV + Apocrypha source family | usable rerun source | This is the current local KJVA/apocrypha corpus family in `configs/example_ebible_engkjv_apocrypha.toml`. The source-coverage audit records 14 apocrypha/deuterocanon books, 5720 verses, and 593090 normalized letters for `KJVA`. The current eBible KJVA source-lock sidecar freezes the rerun baseline by CSV SHA-256 `f4f4549c7323de20a6cdd7aa74aeae32d184b2b6a1a51cd41390540efd710360`, full 80-book order, 36822 verses, 14 apocrypha/deuterocanon books, and 5720 apocrypha/deuterocanon verses. It can reproduce or rerun current KJVA work, but it is not an independent replication source. | Keep as current-source rerun lane only unless a new study lock says otherwise. |
| CrossWire GitLab KJV/KJVA | possible independent metadata candidate | The metadata audit found `kjva.osis.xml` and `kjvdc.xml` path names in the CrossWire GitLab KJV repository. Its config metadata records `DistributionLicense=GPL` for KJVA and general public distribution wording for the DC-only file, while also preserving Crown rights language. This makes it a stronger future source candidate than a KJV-only repository, but no local source import, verse mapping, collation, checksum lock, or source-use decision exists yet. | License/source-use decision, local ignored text import if allowed, verse mapping, book-order lock, collation against current eBible KJVA, checksums, term lock, and study-lock sidecar. |
| Project Gutenberg eBook 30 + eBook 124 | public-domain-USA split KJV+Apocrypha coverage candidate | The eBook 30 RDF metadata records `The Bible, King James Version, Complete`; the eBook 124 RDF metadata records `Deuterocanonical Books of the Bible Apocrypha`; both record `Public domain in the USA.` and plain-text UTF-8 format URLs. The heading-level coverage probe found 66 KJV book headings in eBook 30, 14 tracked KJVA Apocrypha/deuterocanon coverage rows in eBook 124, one extra source heading for the Epistle of Jeremiah, 31102 KJV verse markers, and 5704 Apocrypha/deuterocanon verse-like markers with mixed marker shapes. The source-lock prep count comparison found exact verse-count agreement for all 66 KJV books and 12 of 14 tracked Apocrypha/deuterocanon books after Baruch is read together with the separate Epistle of Jeremiah source section; the remaining count drifts are Sirach at one fewer marker and Prayer of Manasseh with no body verse markers. The Gutenberg checksum sidecar records RDF and plain-text SHA-256 identifiers for eBook 30 and eBook 124 as candidate identifiers only, with 2 checksum records ready but 0 source-use ready pages and 0 verse-import ready pages. The source-lock decision packet recommends Gutenberg source order for an independent Project Gutenberg replication stream, rolling the separate Epistle of Jeremiah source section into BAR for KJVA book-code compatibility, and blocking source lock until Sirach and Prayer of Manasseh receive citable non-text collation decisions. The source-lock blocker packet narrows those blockers: the Sirach marker-only gap is `SIR 44:23`, and the detected Prayer of Manasseh source section has 0 body markers against 15 local markers. The Hakkaac boundary-candidate audit found visible markers for Sirach 44:23 and Prayer of Manasseh 1..15 with a public-domain note, but it remains a candidate audit only, not a source lock. The Hakkaac full-marker coverage audit found exact marker-count agreement for all 14 tracked Apocrypha/deuterocanon books, 5720 source markers, 5720 local markers, 173 chapter rows, and 0 chapter drift rows, but it also remains a marker-coverage audit only. The Hakkaac ignored-local collation audit found 5719 of 5720 exact normalized verse matches, one `SIR 19:1` one-letter normalized length drift, 13 of 14 exact book-stream matches, exact `SIR 44:23` and `MAN 1:1..15` blocker rows, and no tracked Bible text. The Hakkaac source-lock decision packet keeps Hakkaac as candidate evidence only, keeps current eBible KJVA as the rerun baseline, names `SIR 19:1` as a blocked drift decision, and blocks Project Gutenberg plus Hakkaac split-source use without a source-order and source-role sidecar. The split-source role sidecar now writes that role/order boundary as planning-only evidence: Gutenberg is the future primary candidate stream, Hakkaac is marker/collation witness-only, current eBible remains rerun-only, and no result-bearing source lock is ready. The source-policy blocker packet now aggregates the current source-policy choices: 5 policy option rows, 7 blocker rows, 2 policy-ready options, and 3 blocked options. Only the current eBible rerun path and deferral of new KJVA result work are policy-ready; Project Gutenberg-only, Project Gutenberg plus Hakkaac, and Hakkaac-primary streams remain blocked, with no source lock ready. This makes it a possible split-source replication candidate, but no source-use lock, `SIR 19:1` drift decision, term lock, controls, or study-lock sidecar exists yet. | Source policy lock, Baruch/Epistle handling decision, Sirach `SIR 19:1` drift decision, Prayer of Manasseh boundary decision, term lock, controls, and study-lock sidecar. |
| Wikisource Ballantyne 1911 KJV + Apocrypha | metadata-level future source candidate | The source audit found a public-domain KJV + Apocrypha page with markers. The book-coverage probe found 36 existing KJV book links, 30 KJV redlinks, and 0 apocrypha/deuterocanon book links on the parsed main-page book table. No verse-numbered import, collation, checksum, or book-order lock exists here. | Lawful import decision, apocrypha/deuterocanon coverage source, verse mapping, book-order lock, collation against current eBible KJVA, checksums, term lock, and study-lock sidecar. |
| `seven1m/open-bibles` | KJV-only metadata candidate | The audit found KJV OSIS metadata, but current tree metadata does not show apocrypha or deuterocanon coverage. It is not a KJVA/apocrypha source candidate for current bridge replication work. | No KJVA bridge use unless a separate lawful apocrypha source is found and audited. |

## Audit Links

- `docs/KJVA_APOCRYPHA_BRIDGE_NEXT_REPLICATION_DESIGN.md`
- `docs/APOCRYPHA_SOURCE_COVERAGE.md`
- `docs/KJVA_CURRENT_SOURCE_LOCK_SIDECAR.md`
- `docs/KJVA_CROSSWIRE_CANDIDATE_SOURCE_AUDIT.md`
- `docs/KJVA_GUTENBERG_CANDIDATE_SOURCE_AUDIT.md`
- `docs/KJVA_GUTENBERG_BOOK_COVERAGE_PROBE.md`
- `docs/KJVA_GUTENBERG_CANDIDATE_CHECKSUM_SIDECAR.md`
- `docs/KJVA_GUTENBERG_SOURCE_LOCK_PREP.md`
- `docs/KJVA_GUTENBERG_SOURCE_LOCK_DECISION_PACKET.md`
- `docs/KJVA_GUTENBERG_SOURCE_LOCK_BLOCKER_PACKET.md`
- `docs/KJVA_HAKKAAC_APOCRYPHA_BOUNDARY_CANDIDATE.md`
- `docs/KJVA_HAKKAAC_APOCRYPHA_MARKER_COVERAGE.md`
- `docs/KJVA_HAKKAAC_APOCRYPHA_COLLATION_AUDIT.md`
- `docs/KJVA_HAKKAAC_SOURCE_LOCK_DECISION_PACKET.md`
- `docs/KJVA_GUTENBERG_HAKKAAC_SPLIT_SOURCE_ROLE_SIDECAR.md`
- `docs/KJVA_SOURCE_POLICY_BLOCKER_PACKET.md`
- `docs/KJVA_NEXT_RESULT_GATE.md`
- `docs/KJVA_WIKISOURCE_CANDIDATE_SOURCE_AUDIT.md`
- `docs/KJVA_WIKISOURCE_BOOK_COVERAGE_PROBE.md`
- `docs/KJVA_OPEN_BIBLES_CANDIDATE_SOURCE_AUDIT.md`

## Required Before Any Future Result Run

A future KJVA/apocrypha bridge replication needs these locks before output:

- exact source stream
- license/source-use decision
- verse mapping
- book-order decision
- source-role sidecar for any split-source run
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
any KJVA result status. It also points to the next-result gate, which blocks a
new KJVA result until source policy, source text, verse map, collation,
drift/boundary, fresh terms, leakage audit, fixed controls, and study lock all
pass.
