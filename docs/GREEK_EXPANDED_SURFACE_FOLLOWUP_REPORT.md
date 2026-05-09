# Greek Expanded Surface Follow-Up Report

Status: post_screen_surface_followup_review_candidate, not a claim.

This report gathers the tightened Greek exact-center surface rows,
letter-path audit, and all-available real-word controls into one
post-screen follow-up read.

## Run

| Field | Value |
| --- | --- |
| Local report build commit | recorded in local manifest only |
| Letter-path protocol | `protocols/greek_expanded_surface_letter_paths.toml` |
| Control protocol | `protocols/greek_expanded_surface_available_control_evaluation.toml` |
| Letter-path status | `success` |
| Control status | `success` |

For resumed protocol runs, this subreport can remain cached. The build
commit is recorded in the local manifest; the top-level
`reports/real_report_run/summary.md` records the current assembly commit.

## Registered Post-Screen Rows

| Term | Concept | Center | Skip | Direction | p_ge | q | Matched controls |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: |
| `ισαακ` | Isaac | Heb 11:9 | -7 | backward | 0.030303 | 0.032258 | 32 |
| `ανομια` | Lawlessness | Matt 7:23 | 20 | forward | 0.032258 | 0.032258 | 30 |
| `τερασ` | Wonder | Heb 9:11 | -13 | backward | 0.030303 | 0.032258 | 32 |

## Letter-Path Audit

| Term | Corpus | Sequence | Center word | Path refs |
| --- | --- | --- | --- | --- |
| `ισαακ` | TR_NT | `ισαακ` | `κατοικήσας` | HEB 11:9 |
| `ισαακ` | BYZ_NT | `ισαακ` | `κατοικησασ` | HEB 11:9 |
| `ισαακ` | TCG_NT | `ισαακ` | `κατοικήσας` | HEB 11:9 |
| `ισαακ` | SBLGNT | `ισαακ` | `κατοικήσας` | Heb 11:9 |
| `τερασ` | TR_NT | `τερασ` | `χειροποιήτου` | HEB 9:11 |
| `τερασ` | BYZ_NT | `τερασ` | `χειροποιητου` | HEB 9:11 |
| `τερασ` | TCG_NT | `τερασ` | `χειροποιήτου,` | HEB 9:11 |
| `τερασ` | SBLGNT | `τερασ` | `χειροποιήτου,` | Heb 9:11 |
| `ανομια` | TR_NT | `ανομια` | `Οὐδέποτε` | MAT 7:22; MAT 7:23 |
| `ανομια` | BYZ_NT | `ανομια` | `ουδεποτε` | MAT 7:22; MAT 7:23 |
| `ανομια` | TCG_NT | `ανομια` | `Οὐδέποτε` | MAT 7:22; MAT 7:23 |
| `ανομια` | SBLGNT | `ανομια` | `Οὐδέποτε` | Matt 7:22; Matt 7:23 |

## Follow-Up Checks

| Criterion | Result | Note |
| --- | --- | --- |
| All selected terms have paths in all four Greek NT source labels | pass | BYZ_NT, SBLGNT, TCG_NT, TR_NT |
| All reconstructed paths spell the normalized term | pass | 12 path rows |
| All selected terms have all-available controls | pass | 3 control rows |
| No all-available matched control reaches observed all-source count | pass | controls_ge_observed_all_source == 0 |
| Study-level q <= 0.05 within this follow-up table | pass | min 0.032258; max 0.032258 |
| Post-screen boundary stated | pass | follow-up report says this is not prospective discovery |

## Interpretation

This is stronger triage evidence than the first 10-control pass because
the all-available non-selected same-length control pool has study-level
q = 0.032258 for the selected rows.

It is still post-screen. It does not establish a claim, proof, prophecy,
or statistical discovery. A stronger claim would require a prospective
study whose term list, selection rule, control pool, and correction plan
were fixed before the rows were discovered.
