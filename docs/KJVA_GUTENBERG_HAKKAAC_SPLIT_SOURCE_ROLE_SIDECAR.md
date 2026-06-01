# KJVA Gutenberg Hakkaac Split-Source Role Sidecar

Status: split-source role sidecar only.

This is not an ELS result, not a corpus import, not a source lock, not a source-use approval, and not a result-bearing replication.
It writes the source roles and order boundary for the Project Gutenberg plus Hakkaac candidate path.
It does not commit Bible text, choose a final source text, replace current eBible KJVA, or authorize a split-source run.

## Summary

- Role rows: 7.
- Unresolved blocker rows: 6.
- Policy-ready role rows: 2.
- Recommended-but-not-locked role rows: 2.
- Blocked role rows: 2.
- Candidate-not-locked role rows: 1.
- Current eBible rerun baseline locked: 1.
- Split-source role sidecar written: 1.
- Hakkaac exact marker books: 14/14.
- Hakkaac exact normalized verse matches: 5719/5720.
- Hakkaac length-drift verses: 1.
- Gutenberg Sirach gap refs: `SIR 44:23`.
- Gutenberg Prayer of Manasseh markers: 0/15.
- Source-lock ready: 0.
- Result-ready: 0.
- Claim status: `split_source_role_sidecar_only_not_result_bearing`.

## Source Order

- Current local KJVA Apocrypha/deuterocanon order: `TOB;JDT;ESG;WIS;SIR;BAR;S3Y;SUS;BEL;1MA;2MA;1ES;MAN;2ES`.
- Project Gutenberg Apocrypha source order: `1ES;2ES;TOB;JDT;ESG;WIS;SIR;BAR;LJE_SOURCE;S3Y;SUS;BEL;MAN;1MA;2MA`.
- Future independent candidate order recommendation: `use_gutenberg_source_order_for_independent_replication`.
- Current eBible KJVA order remains the rerun baseline order only.

## Source Roles

| Role | Source family | Component | Source role | Order role | Status | Allowed use | Blocked use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `current_ebible_rerun_baseline` | current eBible KJV + Apocrypha | full KJVA stream | `rerun_baseline_only` | `current_local_order` | `policy_ready` | rerun and reproduce current KJVA work by checksum/order/count sidecar | independent replication source or silent replacement stream |
| `gutenberg_kjv_component` | Project Gutenberg eBook 30 | 66-book KJV component | `primary_kjv_candidate` | `gutenberg_canonical_component` | `recommended_policy_not_locked` | candidate component for a future independent stream | result-bearing import before source-use, verse-map, checksum, and collation locks |
| `gutenberg_apocrypha_component` | Project Gutenberg eBook 124 | Apocrypha/deuterocanon component | `primary_apocrypha_candidate` | `gutenberg_source_order` | `blocked` | candidate component after blocker policy is resolved | source-locked stream while Sirach and Prayer of Manasseh blockers remain |
| `gutenberg_lje_baruch_rollup` | Project Gutenberg eBook 124 | Epistle of Jeremiah source section | `component_metadata_rollup_candidate` | `roll_lje_source_into_bar_for_kjva_book_code` | `recommended_policy_not_locked` | document source-component metadata in a future independent stream | unlabeled merger without preregistered source-role metadata |
| `hakkaac_marker_collation_witness` | Hakkaac KJV Apocrypha | 14-book Apocrypha/deuterocanon witness | `marker_and_collation_witness_only` | `not_primary_order_source` | `candidate_not_locked` | non-text marker/collation corroboration and drift evidence | primary source text authority or tracked corpus import |
| `split_stream_boundary` | Project Gutenberg plus Hakkaac | future split-source candidate | `split_source_policy_boundary` | `gutenberg_order_if_future_independent_stream` | `blocked` | planning-only role map | result-bearing split-source run |
| `tracked_text_retention_boundary` | all KJVA source candidates | tracked outputs | `no_tracked_bible_text` | `not_applicable` | `policy_ready` | commit checksums, counts, refs, lengths, roles, and decisions | tracked raw Bible text |

## Unresolved Blockers

| Blocker | Area | Status | Evidence | Blocked until | Affects letter stream |
| --- | --- | --- | --- | --- | ---: |
| `sirach_44_23_gutenberg_marker_gap` | Sirach marker gap | `non_text_corroborated_not_source_locked` | Gutenberg marker list misses SIR 44:23; Hakkaac blocker rows exact 16/16. | a source policy decides whether Hakkaac can supply marker/text authority or Gutenberg remains blocked | 1 |
| `manasseh_unmarked_gutenberg_section` | Prayer of Manasseh boundary | `non_text_corroborated_not_source_locked` | Gutenberg MAN source markers 0; local markers 15; options sirach_defer_until_citable_collation;sirach_do_not_auto_insert_marker;manasseh_defer_until_citable_marked_source;manasseh_exclude_until_policy_lock;manasseh_manual_split_requires_review. | a cited marked source, exclusion policy, or boundary rule is locked before results | 1 |
| `sirach_19_1_hakkaac_length_drift` | Hakkaac/local drift | `blocked` | Hakkaac decision packet names SIR 19:1; 1 length-drift verse. | a cited source policy chooses which normalized stream to lock | 1 |
| `hakkaac_source_use_boundary` | source use | `candidate_not_locked` | Current approval does not authorize tracked source text or result-bearing corpus use. | source-use lock permits exactly stated role, or Hakkaac remains witness-only | 1 |
| `split_source_result_boundary` | split-source result boundary | `blocked` | Split-source roles affect reproducibility, source order, and source provenance. | source roles, source use, drift policy, term lock, control lock, and study lock all exist | 1 |
| `gutenberg_source_stream_boundary` | Gutenberg source stream | `candidate_not_locked` | No study-lock sidecar, verse map, collation, or source-use lock exists yet. | source-use, verse-map, collation, checksum, term, control, and study locks exist | 1 |

## Boundary

This sidecar closes only the missing written source-role/order boundary.
It does not close the source-use boundary, the `SIR 19:1` drift boundary, the Prayer of Manasseh boundary, or the future term/control/study-lock boundary.
No Bible text is written to tracked outputs.
It does not change any KJVA bridge result status.
