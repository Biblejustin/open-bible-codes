# Next Prospective Study Lock

Status: planning lock for the next result-producing phase. This document does
not run a search and does not promote any result to a claim.

Locked on top of report assembly commit: `ce39e9a`.

## Purpose

The current report has enough source-audit material. The next useful step is
not another broad source expansion. It is a small locked candidate bundle with
fixed sources, fixed rules, and explicit labels separating:

1. occurrence-first findings that should be listed because they happened;
2. post-discovery review candidates that can be stress-tested but cannot become
   original prospective discoveries;
3. one future prospective lane that must be locked before it produces new
   results.

## Non-Negotiable Boundaries

- Raw hit count is never enough for promotion.
- Hidden-path-only rows are valid rows, but surface echo and center relevance
  must be labeled separately.
- A hidden term centered on itself or on a related surface context is listed as
  an occurrence even when controls caution against frequency promotion.
- Source-version absence is data, not automatic failure.
- Post-discovery rows may become review candidates, not original discoveries.
- Source-audit pages define future tests; they are not findings.

## Track 1: Occurrence-First Findings

This track is report presentation over existing locked artifacts. It is not a
new search.

Primary input:

- `docs/FINAL_REPORT_HIGHLIGHTS.md`
- `reports/centered_occurrence_index/presence_summary.csv`

Rows to carry forward:

| Term | Center | Corpora | Required read |
| --- | --- | --- | --- |
| `γωγ` | Rev 20:8 `Gog` | BYZ_NT; SBLGNT; TCG_NT; TR_NT | occurrence-first highlight; frequency-cautioned; not claim |
| `ישוע` | Ezra 10:18 `יֵשׁ֤וּעַ` | UHB | occurrence listed; background-pressure caution |
| `משיח` | 2 Sam 1:21 `מָשִׁ֥יחַ` | EBIBLE_WLC | occurrence listed; background-pressure caution |
| `ιησουσ` | Joshua 8:3 `Ἰησοῦς` | LXX | occurrence listed; referent caution because this is Joshua-context in LXX |
| `jesus` | Matthew 4:10 `Jesus` | KJV | occurrence listed; English translation screen is secondary |

Success criterion:

- final reader-facing report lists the occurrence and its caution together.

Failure criterion:

- final report treats frequency caution as a reason to hide the occurrence, or
  treats occurrence as claim-level evidence.

## Track 2: Post-Discovery Controlled Review Candidates

This track may rerun or summarize existing locked follow-ups. It cannot create
original prospective discovery language.

### Greek `δοξα` / `δοξανωσ`

Registered row:

- `δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ`

Sources:

- `TR_NT`
- `BYZ_NT`
- `TCG_NT`
- `SBLGNT`

Locked protocol:

- `protocols/doxa_four_source_confirmatory_followup.toml`

Allowed status if reproduced:

- `claim_followup_review_candidate`

Disallowed status:

- `claim`
- `proof`
- `original prospective discovery`

### Hebrew `יום יהוה` / `היומיהוה`

Registered row family:

- selected `יום יהוה` -> `היומיהוה` compound-extension key

Sources:

- `EBIBLE_WLC`
- `MAM`
- `MT_WLC`
- `UHB`
- `UXLC`

Locked protocol:

- `protocols/all_codes_compound_extension_confirmatory.toml`

Allowed status if reproduced:

- `post_screen_confirmatory_review_candidate`

Disallowed status:

- `claim`
- `proof`
- `original prospective discovery`

### KJVA Apocrypha/Deuterocanon Bridge Terms

Registered term file:

- `terms/kjv_apocrypha_bridge_confirmatory_terms.csv`

Registered normalized English terms:

`nato`, `seba`, `sign`, `eber`, `satan`, `moab`, `sidon`, `sivan`, `gallus`,
`otho`, `seal`, `house`, `tomb`, `noah`, `abib`.

Source:

- `KJVA` from `configs/example_ebible_engkjv_apocrypha.toml`

Locked protocol:

- `protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml`

Allowed status if reproduced:

- `post_screen_confirmatory_review_candidate`

Disallowed status:

- `claim`
- `proof`
- `original prospective discovery`

## Track 3: Completed Fresh Prospective Lane

The next fresh result-producing lane was the Gog/Magog pair-control study. It
has now run under the locked design. It did not produce a
`prospective_controlled_review_candidate`.

Lane profile:

- `gog_magog_pair_controls` in `configs/prospective_study_lanes.json`

Registered artifacts:

- `docs/GOG_MAGOG_PAIR_PROSPECTIVE_PREREGISTRATION.md`
- `docs/GOG_MAGOG_PAIR_PROSPECTIVE_REPORT.md`
- `terms/gog_magog_pair_prospective_terms.csv`
- `protocols/gog_magog_pair_prospective.toml`
- `reports/study_locks/gog_magog_pair_prospective.manifest.json`
- `reports/study_locks/gog_magog_pair_prospective.preflight.json`

Fixed source labels:

- `MT_WLC` from `configs/example_oshb_wlc.toml`
- `UHB` from `configs/example_uhb.toml`

Fixed search settings:

- skip range: `2..100`
- direction: `both`
- minimum normalized length: `3`
- candidate type: same-chapter, same-signed-skip pair rows
- correction: Benjamini-Hochberg across registered pair tests

Required control shape:

- length-matched prophetic-symbol pair controls;
- synthetic null pairs;
- no unregistered extra terms after seeing output.

Candidate rule:

- Gog/Magog pair compactness must beat matched prophetic-symbol and synthetic
  pair baselines under the locked rule.

Observed outcome:

- target rows occurred in MT_WLC and UHB;
- both target rows were `not_unusual` under pair controls;
- synthetic length-matched 3+4 Hebrew pairs often matched or exceeded target
  close-pair density;
- no `prospective_controlled_review_candidate` was produced.

Allowed status if future rerun reproduces this result:

- negative/weak controlled prospective result

Disallowed status:

- `claim`
- `proof`
- `prophecy confirmed`

## Next Allowed Commands

Safe non-result-producing checks:

```bash
python3 -m scripts.check_prospective_study_lanes
python3 -m scripts.scaffold_prospective_study --profile gog_magog_pair_controls --print-command
```

Allowed post-discovery reruns with existing locks:

```bash
python3 -m scripts.run_protocol protocols/doxa_four_source_confirmatory_followup.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_compound_extension_confirmatory.toml --resume
python3 -m scripts.run_protocol protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml --resume
```

Completed run command:

```bash
python3 -m scripts.run_protocol protocols/gog_magog_pair_prospective.toml --resume
```

## Final Report Placement

The final report should separate these layers:

1. occurrence-first highlights;
2. controlled post-discovery review candidates;
3. weak/negative findings;
4. under-specified public source queue;
5. completed negative Gog/Magog prospective pair-control study.

This separation is required so the report does not confuse "observed
occurrence", "controlled review candidate", "source-audit term", and "claim".
