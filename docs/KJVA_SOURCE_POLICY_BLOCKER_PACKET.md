# KJVA Source Policy Blocker Packet

Status: source-policy blocker packet only.

This is not an ELS result, not a corpus import, not a source-use approval, not a source lock, and not a result-bearing replication.
It narrows current KJVA source-policy options and names the blockers that remain before any new result-bearing run.
It does not commit Bible text, choose a final source text, replace current eBible KJVA, or authorize a split-source run.

## Summary

- Policy option rows: 5.
- Blocker rows: 7.
- Policy-ready options: 2.
- Blocked options: 3.
- Checksum records ready: 2.
- Split-source role sidecar written: 1.
- Current rerun locked: 1.
- Source-use ready pages: 0.
- Gutenberg Sirach gap refs: `SIR 44:23`.
- Gutenberg Prayer of Manasseh markers: 0/15.
- Hakkaac length-drift verses: 1.
- Source-lock ready: 0.
- Result-ready: 0.
- Claim status: `source_policy_blocker_packet_only_not_result_bearing`.

## Policy Options

| Option | Source stream | Status | Allowed use | Blocked use | Blocker summary |
| --- | --- | --- | --- | --- | --- |
| `current_ebible_rerun_only` | current eBible KJV + Apocrypha | `policy_ready` | rerun and reproduce current KJVA work by checksum/order/count sidecar | independent replication claim or silent source replacement | not independent-source-ready |
| `project_gutenberg_only_candidate` | Project Gutenberg eBook 30 plus eBook 124 | `blocked` | candidate stream with checksum identifiers and count evidence | source-locked or result-bearing stream | Sirach gap SIR 44:23; MAN markers 0/15 |
| `project_gutenberg_hakkaac_split_candidate` | Project Gutenberg plus Hakkaac | `blocked` | planning-only split-source candidate with written roles/order | result-bearing split-source stream | source-use, SIR 19:1 drift, Prayer of Manasseh, term/control, and study-lock blockers remain |
| `hakkaac_primary_stream` | Hakkaac KJV Apocrypha | `blocked` | marker and collation witness only | primary tracked corpus or source-text authority | current approval does not authorize tracked source text or result-bearing corpus use |
| `defer_new_kjva_replication` | no new independent KJVA stream | `policy_ready` | continue audit/planning while current prospective KJVA lane remains negative | new result-bearing replication | fresh term/control/study-lock sidecar still absent |

## Blockers

| Blocker | Area | Status | Evidence | Required before result | Needs choice | Affects letter stream |
| --- | --- | --- | --- | --- | ---: | ---: |
| `source_use_policy_lock` | source use | `blocked` | Gutenberg source-use ready pages=0; Hakkaac remains witness-only. | explicit source-use policy names which external source may supply result-bearing text, if any | 1 | 1 |
| `gutenberg_sirach_44_23_marker_gap` | Sirach marker gap | `blocked` | Gutenberg marker gap refs=SIR 44:23; missing count=1. | citable policy explains whether to keep Gutenberg blocked, exclude/patch nothing, or use witness evidence | 1 | 1 |
| `gutenberg_prayer_of_manasseh_boundary` | Prayer of Manasseh boundary | `blocked` | Gutenberg source markers=0; local markers=15. | cited marked source, exclusion policy, or boundary rule exists before results | 1 | 1 |
| `hakkaac_sirach_19_1_length_drift` | Hakkaac/local drift | `blocked` | Hakkaac length-drift verses=1; exact book streams=13/14. | source policy chooses the locked normalized stream or keeps Hakkaac witness-only | 1 | 1 |
| `verse_map_and_collation_lock` | verse map and collation | `blocked` | No result-bearing verse map or full independent-source collation lock exists. | verse mapping and collation sidecar exists for the selected source stream | 0 | 1 |
| `term_control_study_lock` | study lock | `blocked` | No fresh term lock, control lock, leakage audit, or study-lock sidecar exists for a new KJVA run. | fresh preregistered term/control/study-lock package exists before output | 1 | 1 |
| `role_sidecar_complete_but_not_sufficient` | source roles | `closed_as_planning_only` | role rows=7; blocker rows=6; role sidecar written=True. | remaining blockers close; role sidecar alone never authorizes results | 0 | 1 |

## Boundary

This packet is a blocker summary, not a decision to run KJVA results.
The only policy-ready path here is current-source rerun and continued deferral of new result-bearing KJVA work.
Any new independent KJVA result run still needs source-use, source-text, drift/boundary, verse-map/collation, term/control, and study-lock decisions before output.
No Bible text is written to tracked outputs.
It does not change any KJVA bridge result status.
