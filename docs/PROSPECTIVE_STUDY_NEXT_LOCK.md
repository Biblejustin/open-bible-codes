# Next Prospective Study Lock

Status: historical planning lock and closeout map. This document does not run
a search and does not promote any result to a claim.

Initial planning lock recorded after report assembly commit: `ce39e9a`.
Current lane status is generated from `configs/prospective_study_lanes.json`
in `docs/PROSPECTIVE_LANE_STATUS.md`.

## Purpose

The current report has enough source-audit material. This document records the
candidate bundle and its completed follow-up lanes, with fixed sources, fixed
rules, and explicit labels separating:

1. occurrence-first findings that should be listed because they happened;
2. post-discovery review candidates that can be stress-tested but cannot become
   original prospective discoveries;
3. completed prospective lanes that must not be rebranded as new discoveries;
4. the current boundary that no tracked lane remains `ready_for_preflight`.

## Non-Negotiable Boundaries

- Raw hit count is never enough for promotion.
- Hidden-path-only rows are valid rows, but surface echo and center relevance
  must be labeled separately.
- A hidden term centered on itself or on a related surface context is listed as
  an occurrence even when controls caution against frequency promotion.
- Source-version absence is data, not automatic failure.
- Post-discovery rows may become review candidates, not original discoveries.
- Source-audit pages define future tests; they are not findings.
- New result-producing work now needs a fresh term/source target set and a
  clean prospective lock.

## Track 1: Occurrence-First Findings

This track is report presentation over existing locked artifacts. It is not a
new search.

Primary input:

- `docs/FINAL_REPORT_HIGHLIGHTS.md`
- `reports/centered_occurrence_index/presence_summary.csv`

Rows to carry forward:

| Term | Center | Corpora | Required read |
| --- | --- | --- | --- |
| `γωγ` (Gog; English: Gog) | Rev 20:8 `Gog` | BYZ_NT; SBLGNT; TCG_NT; TR_NT | occurrence-first highlight; frequency-cautioned; not claim |
| `ישוע` (Yeshua; English: Yeshua/Jeshua) | Ezra 10:18 `יֵשׁ֤וּעַ` (Yeshua; English: Yeshua/Jeshua) | UHB | occurrence listed; background-pressure caution |
| `משיח` (Mashiach; English: Messiah/anointed one) | 2 Sam 1:21 `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) | EBIBLE_WLC | occurrence listed; background-pressure caution |
| `ιησουσ` (Iesous; English: Jesus/Joshua) | Joshua 8:3 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | LXX | occurrence listed; referent caution because this is Joshua-context in LXX |
| `jesus` | Matthew 4:10 `Jesus` | KJV | occurrence listed; English translation screen is secondary |

Success criterion:

- final reader-facing report lists the occurrence and its caution together.

Failure criterion:

- final report treats frequency caution as a reason to hide the occurrence, or
  treats occurrence as claim-grade evidence.

## Track 2: Post-Discovery Controlled Review Candidates

This track may rerun or summarize existing locked follow-ups. It cannot create
original prospective discovery language.

### Greek `δοξα` (doxa; English: glory) / `δοξανωσ` (doxanos; English: hidden extension form from doxa)

Registered row:

- `δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ` (doxa / doxanos; English: glory / hidden extension form from doxa)

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
- `conclusive evidence`
- `original prospective discovery`

### Hebrew `יום יהוה` (yom YHWH; English: day of YHWH) / `היומיהוה` (hayom YHWH; English: the day of YHWH)

Registered row family:

- selected `יום יהוה` (yom YHWH; English: day of YHWH) -> `היומיהוה` (hayom YHWH; English: the day of YHWH) compound-extension key

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
- `conclusive evidence`
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
- `conclusive evidence`
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
- `conclusive evidence`
- `prophecy-confirmation wording`

## Track 4: Completed Clean-Lock Expansion

The later clean-lock expansion added fresh Greek surface terms and Hebrew
concordance terms after earlier evidence rows were excluded. It produced review
queues, not claim-ready rows.

Primary artifacts:

- `docs/CLEAN_LOCK_RESULTS_SUMMARY.md`
- `docs/GREEK_SURFACE_NEW_TERMS_CONTEXT_REVIEW.md`
- `docs/HEBREW_CONCORDANCE_UNCORRECTED_SCREENING_AUDIT.md`
- `docs/STRICT_FOLLOWUP_GATE_SUMMARY.md`

Observed outcome:

- Greek surface new terms: 5 controlled rows reached `q <= 0.05`;
- manual context review found local surface-context/self-lexeme effects;
- Hebrew concordance words: 87 uncorrected-only representative-control prompts;
- Hebrew concordance words: 0 adjusted-support terms;
- strict follow-up gate: 0 Greek surface rows and 0 Hebrew concordance rows
  are claim-ready.

Allowed status:

- audit material
- triage list
- negative strict-gate result

Disallowed status:

- `claim`
- `conclusive evidence`
- `prospective_controlled_review_candidate`

## Next Allowed Commands

Safe non-result-producing checks:

```bash
python3 -m scripts.check_prospective_study_lanes
python3 -m scripts.scaffold_prospective_study --list-profiles
python3 -m scripts.build_prospective_lane_status
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
