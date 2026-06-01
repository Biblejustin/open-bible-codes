# KJVA Hakkaac Source-Lock Decision Packet

Status: decision packet only.

This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.
It converts Hakkaac marker coverage and ignored-local collation evidence into explicit source-lock decisions and blockers.
It does not commit Bible text, normalize Bible text into a tracked corpus, replace the current eBible KJVA source, or authorize a split-source run.

## Summary

- Decision rows: 9.
- Policy-ready rows: 3.
- Recommended-but-not-locked rows: 2.
- Blocked rows: 3.
- Candidate-not-locked rows: 1.
- Exact normalized verse matches: 5719/5720.
- Length-drift verses: 1.
- Exact book stream matches: 13/14.
- Book stream drift books: 1.
- Exact blocker rows: 16/16.
- Exact marker books: 14/14.
- Source-lock ready: 0.
- Result-ready sources: 0.
- Claim status: `decision_packet_only_not_result_bearing`.

## Recommendation

Keep Hakkaac as candidate evidence only until a separate source-use lock is written.
Keep current eBible KJVA as the rerun baseline until a fresh independent source lock is complete.
Do not patch either source automatically for `SIR 19:1`.
Do not combine Project Gutenberg plus Hakkaac into a result-bearing split-source stream without a written source-order and source-role sidecar.

## Drift Rows

| Ref | Status | Local letters | Hakkaac letters | Delta | First diff offset | Recommendation |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `SIR 19:1` | `length_drift` | 107 | 108 | 1 | 17 | `keep_named_drift_until_source_policy_lock` |

## Book Read

| Book | Exact verses | Length-drift verses | Stream status |
| --- | ---: | ---: | --- |
| `TOB` | 244 | 0 | `exact_normalized_stream_match` |
| `JDT` | 339 | 0 | `exact_normalized_stream_match` |
| `ESG` | 105 | 0 | `exact_normalized_stream_match` |
| `WIS` | 436 | 0 | `exact_normalized_stream_match` |
| `SIR` | 1392 | 1 | `stream_drift` |
| `BAR` | 213 | 0 | `exact_normalized_stream_match` |
| `S3Y` | 68 | 0 | `exact_normalized_stream_match` |
| `SUS` | 64 | 0 | `exact_normalized_stream_match` |
| `BEL` | 42 | 0 | `exact_normalized_stream_match` |
| `1MA` | 924 | 0 | `exact_normalized_stream_match` |
| `2MA` | 555 | 0 | `exact_normalized_stream_match` |
| `1ES` | 448 | 0 | `exact_normalized_stream_match` |
| `MAN` | 15 | 0 | `exact_normalized_stream_match` |
| `2ES` | 874 | 0 | `exact_normalized_stream_match` |

## Decision Rows

| Decision | Area | Status | Recommendation | Blocker |
| --- | --- | --- | --- | --- |
| `source_use_boundary` | source use | `candidate_not_locked` | Keep Hakkaac as candidate evidence unless a separate source-use lock is written. | Current approval does not authorize tracked source text or result-bearing corpus use. |
| `raw_text_retention` | text retention | `policy_ready` | Keep raw Hakkaac verse text under ignored data/private output; commit only hashes, counts, lengths, refs, and decisions. |  |
| `marker_coverage` | marker coverage | `policy_ready` | Use Hakkaac marker coverage as non-text evidence that all 14 tracked Apocrypha/deuterocanon books are represented. |  |
| `gutenberg_blocker_rows` | Gutenberg blockers | `recommended_policy_not_locked` | Use Hakkaac as non-text corroboration for the Gutenberg Sirach 44:23 and Prayer of Manasseh marker blockers. | This corroborates blockers but does not make either source stream ready. |
| `collation_strength` | collation strength | `recommended_policy_not_locked` | Treat Hakkaac as a strong external witness for the current eBible KJVA Apocrypha stream, subject to the one drift row. | One verse has normalized length drift. |
| `sirach_19_1_drift` | Sirach drift | `blocked` | Do not patch either source automatically; keep SIR 19:1 as a named drift until a source policy chooses which normalized stream to lock. | One normalized-letter length drift changes the ELS letter stream. |
| `split_source_policy` | split-source policy | `blocked` | Do not combine Project Gutenberg plus Hakkaac into a result-bearing split-source stream without a written source-order and source-role policy. | Split-source roles affect reproducibility, source order, and source provenance. |
| `current_ebible_reference` | current eBible KJVA | `policy_ready` | Keep current eBible KJVA as the rerun baseline until a fresh independent source lock is complete. |  |
| `result_boundary` | result boundary | `blocked` | Do not run a result-bearing KJVA bridge replication from Hakkaac or split-source evidence yet. | Source-lock prerequisites remain open. |

## Boundary

This packet is a planning and audit artifact.
It does not choose final source text, create verse mappings, perform result-bearing ELS searches, lock terms, lock controls, or authorize a new KJVA bridge run.
No Bible text is written to tracked outputs.
It does not change any KJVA bridge result status.
