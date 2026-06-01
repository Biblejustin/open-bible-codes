# KJVA Next Result Gate

Status: next-result gate only.

This is not an ELS result, not a corpus import, not a source-use approval, not a source lock, not a term lock, and not a study lock.
It records which gates are open or blocked before any future KJVA result-bearing run.
It allows only current-source rerun reproducibility, not a new independent KJVA result.

## Summary

- Gate rows: 11.
- Rerun-only ready rows: 1.
- Blocked rows: 10.
- Source-policy blocker rows: 7.
- Completed lane terms: 7.
- Completed lane observed bridge rows: 1.
- Completed lane significant terms: 0.
- Non-Bible controls at or above observed: 1.
- Source-lock ready: 0.
- Fresh terms ready: 0.
- Leakage audit ready: 0.
- Fixed controls ready: 0.
- Study-lock ready: 0.
- Result allowed: 0.
- Claim status: `kjva_next_result_gate_blocks_new_output`.

## Gates

| Gate | Area | Status | Evidence | Required before result |
| --- | --- | --- | --- | --- |
| `current_rerun_reproducibility` | rerun baseline | `rerun_only_ready` | current rerun locked=True; checksum records ready=2 | no new result requirement; rerun current eBible baseline only |
| `completed_lane_claim_gate` | completed KJVA prospective lane | `blocked` | terms=7; observed_bridge_rows=1; significant_terms=0; nonbible_controls_at_or_above=1 | new result may not reuse the completed negative prospective lane as claim evidence |
| `source_policy_lock` | source policy | `blocked` | source_policy_blockers=7; source_lock_ready=False | source-use and source-role policy must authorize any selected external source |
| `source_text_lock` | source text | `blocked` | no independent KJVA source text is source-locked for result-bearing use | selected source stream has checksum, text-retention, order, and source-use lock |
| `verse_map_collation_lock` | verse map and collation | `blocked` | no result-bearing verse map or full selected-source collation lock exists | selected stream has verse map and collation sidecar before output |
| `drift_boundary_lock` | drift and boundary | `blocked` | Sirach gap=SIR 44:23; MAN markers=0/15; Hakkaac drift verses=1 | Sirach, Prayer of Manasseh, and Hakkaac drift policies are locked before output |
| `fresh_term_lock` | terms | `blocked` | no fresh KJVA term list is locked for a new result-bearing run | fresh terms are preregistered before new output is seen |
| `leakage_audit_lock` | leakage audit | `blocked` | no leakage audit records new terms as independent from prior KJVA screens | term list is checked against prior KJVA bridge files and outputs |
| `fixed_controls_lock` | controls | `blocked` | no fixed control plan is locked for a new KJVA result-bearing run | shuffled and non-Bible controls are preregistered with sample counts |
| `study_lock_manifest` | study lock | `blocked` | no new KJVA study-lock manifest exists | source, term, leakage, controls, correction, and reporting rules are frozen |
| `result_allowed` | result permission | `blocked` | new KJVA result-bearing output is not allowed by current gates | all source and study gates pass before any new result run |

## Boundary

Current eBible KJVA reruns remain allowed for reproducibility only.
No new independent KJVA result-bearing run is allowed by this gate.
A future run still needs source policy, source text, verse map, collation, drift/boundary, fresh terms, leakage audit, fixed controls, and study-lock manifest gates to pass first.
No Bible text is written to tracked outputs.
It does not change any KJVA bridge result status.
