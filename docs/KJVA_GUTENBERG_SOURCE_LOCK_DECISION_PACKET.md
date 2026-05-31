# KJVA Gutenberg Source-Lock Decision Packet

Status: decision packet only.

This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.
It converts the count-only Gutenberg source-lock prep into explicit source-lock decisions and blockers.
It does not commit Bible text, normalize Bible text, create a local corpus, or declare a source-lock-ready stream.

## Summary

- Decision rows: 10.
- Policy-ready rows: 2.
- Recommended-but-not-locked rows: 3.
- Blocked rows: 4.
- Candidate-not-locked rows: 1.
- Source-lock ready: 0.
- Result-ready sources: 0.
- Claim status: `decision_packet_only_not_result_bearing`.

## Recommendation

Use Project Gutenberg eBook 30 plus eBook 124 as the next independent KJVA candidate stream only after the remaining source-lock blockers close.
Use Gutenberg source order for an independent Project Gutenberg replication stream, and document that this differs from the current local KJVA order.
Roll the separate Epistle of Jeremiah source section into BAR for KJVA book-code compatibility while preserving source-component metadata.
Do not source-lock Sirach or Prayer of Manasseh until their count drifts have citable, non-text collation decisions.

## Source Order

- Local KJVA Apocrypha order: `TOB;JDT;ESG;WIS;SIR;BAR;S3Y;SUS;BEL;1MA;2MA;1ES;MAN;2ES`.
- Gutenberg Apocrypha source order: `1ES;2ES;TOB;JDT;ESG;WIS;SIR;BAR;LJE_SOURCE;S3Y;SUS;BEL;MAN;1MA;2MA`.
- Order recommendation: `use_gutenberg_source_order_for_independent_replication`.

## Count Evidence

- KJV exact count matches: 66/66.
- Apocrypha/deuterocanon exact count matches: 12/14.
- Apocrypha/deuterocanon count drifts: 2.
- Extra source sections: 1.

## Decision Rows

| Decision | Area | Status | Recommendation | Blocker |
| --- | --- | --- | --- | --- |
| `source_stream` | source stream | `candidate_not_locked` | Use Project Gutenberg eBook 30 plus eBook 124 as the next independent KJVA candidate stream, after the remaining verse-map blockers are closed. | No study-lock sidecar, verse map, collation, or source-use lock exists yet. |
| `raw_text_retention` | text retention | `policy_ready` | Keep raw Gutenberg text in ignored local cache or scan in memory only; commit checksums and counts, not Bible text. |  |
| `kjv_component` | KJV component | `recommended_policy_not_locked` | Treat the KJV component as count-ready for later collation, but not imported. | Count agreement is not text collation. |
| `apocrypha_component` | Apocrypha/deuterocanon component | `blocked` | Keep eBook 124 as the likely Apocrypha/deuterocanon source component, but block source lock until the two count drifts are resolved. | Sirach and Prayer of Manasseh do not have exact verse-marker agreement. |
| `book_order` | book order | `recommended_policy_not_locked` | Use Gutenberg source order for an independent Project Gutenberg replication stream, and document that this differs from current local KJVA order. | Book order affects ELS paths and must be preregistered before results. |
| `baruch_epistle` | Baruch/Epistle of Jeremiah | `recommended_policy_not_locked` | Roll the separate Epistle of Jeremiah source section into BAR for KJVA book-code compatibility while preserving source-component metadata. | Rollup policy must be named before a result-bearing run. |
| `sirach_count_drift` | Sirach count drift | `blocked` | Do not patch or infer the missing Sirach marker automatically. | One-verse marker drift needs citable collation. |
| `prayer_count_drift` | Prayer of Manasseh count drift | `blocked` | Do not split the unmarked prose automatically. | eBook 124 body text has no verse markers for Prayer of Manasseh. |
| `checksum_record` | checksums | `policy_ready` | Use those checksums as candidate source identifiers once the source stream is formally selected. |  |
| `result_boundary` | result boundary | `blocked` | Do not run result-bearing KJVA bridge replication from Gutenberg yet. | Source-lock prerequisites remain open. |

## Boundary

This packet is a planning and audit artifact. It does not choose final source text, create verse mappings, perform text collation, lock terms, lock controls, or authorize a result-bearing run.
It does not change any KJVA bridge result status.
