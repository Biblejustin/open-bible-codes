# Gospel People And Genealogy Prospective Preregistration

Status: locked prospective cohort design. No result-producing run is valid for
this study unless the lock manifest and preflight both pass before the run.

## Study Identity

| Field | Value |
| --- | --- |
| Study name | `gospel_people_genealogy_prospective` |
| Study status | prospective cohort screen with prior-overlap audit |
| Preregistration commit | recorded by `reports/study_locks/gospel_people_genealogy_prospective.manifest.json` |
| Lock manifest | `reports/study_locks/gospel_people_genealogy_prospective.manifest.json` |
| Preflight artifact | `reports/study_locks/gospel_people_genealogy_prospective.preflight.json` |
| Protocol | `protocols/gospel_people_genealogy_prospective.toml` |
| Report document | `docs/GOSPEL_PEOPLE_GENEALOGY_PROSPECTIVE_REPORT.md` |

## Question

Do declared Gospel people, disciples, Gospel women, and Christ-genealogy names
produce exact ELS version-presence patterns under fixed skip `2..100`,
direction `both`, minimum normalized length `4`, and representative
length-matched controls?

This is a review-candidate study. It may identify rows worth inspection. It
may not produce claim, prophecy-confirmation, or conclusive-evidence language.

## Term List

Locked term file:

- `terms/gospel_people_genealogy_prospective_terms.csv`

Term cohort:

- Matthew/Luke genealogy names in Greek;
- selected Hebrew consonantal equivalents for genealogy names;
- the Twelve and disciple-associated Greek names;
- named Gospel women in Greek;
- other named Gospel people in Greek;
- selected Hebrew/Aramaic equivalents where conventional consonantal forms are
  meaningful.

Rules:

- Greek and Hebrew rows are analyzed separately in language-compatible corpora;
- minimum normalized length is `4`, so short names remain in the locked file
  but are outside the exact-version matrix and control target set;
- no term may be added after report outputs are inspected;
- prior-overlap audit rows, if any, stay visible and prevent original-discovery
  wording for those exact forms.

## Source Texts

Greek source labels:

- `LXX`: `configs/example_ebible_grclxx.toml`
- `TR_NT`: `configs/example_ebible_grctr.toml`
- `BYZ_NT`: `configs/example_ebible_grcmt.toml`
- `TCG_NT`: `configs/example_ebible_grctcgnt.toml`
- `SBLGNT`: `configs/example_sblgnt.toml`

Hebrew source labels:

- `MT_WLC`: `configs/example_oshb_wlc.toml`
- `UXLC`: `configs/example_uxlc.toml`
- `EBIBLE_WLC`: `configs/example_ebible_hebwlc.toml`
- `MAM`: `configs/example_mam.toml`
- `UHB`: `configs/example_uhb.toml`

Greek NT labels are the primary Greek comparison family. LXX is included as a
Greek background and bridge witness for genealogy names. MT-family sources are
the Hebrew comparison family.

## Locked Settings

| Setting | Value |
| --- | --- |
| Skip range | `2..100` |
| Direction | `both` |
| Minimum normalized length | `4` |
| Candidate selection rule | all exact term IDs from the locked term file that pass the length gate |
| Context rule | exact version-presence row with start, center, end refs and center words |
| Representative control budget | `500` term-shuffle plus `500` random controls for MT_WLC, UHB, TR_NT, and SBLGNT rows with observed hits |
| Correction method | Benjamini-Hochberg over representative-control rows |
| Random seed | `20260527` |
| Extension rows | not joined in this study |
| Claim language | disallowed |

## Prior-Overlap Audit

Before interpreting results, run:

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/gospel_people_genealogy_prospective_terms.csv \
  --evidence reports/centered_occurrence_index/presence_summary.csv \
  --evidence reports/final_report_highlights/highlights.csv \
  --min-normalized-length 4 \
  --exact-only \
  --out reports/study_locks/gospel_people_genealogy_prior_overlap_audit.csv
```

This audit is not a clean-term exclusion gate. It is a warning layer. Exact
prior-overlap rows may be reported, but they cannot be called original
prospective discoveries.

## Lock Manifest

Build:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name gospel_people_genealogy_prospective \
  --path docs/GOSPEL_PEOPLE_GENEALOGY_PROSPECTIVE_PREREGISTRATION.md \
  --path terms/gospel_people_genealogy_prospective_terms.csv \
  --path protocols/gospel_people_genealogy_prospective.toml \
  --path scripts/analyze_hit_version_presence.py \
  --path scripts/analyze_hebrew_hit_version_presence.py \
  --path scripts/analyze_targeted_version_presence.py \
  --path scripts/analyze_targeted_paired_controls.py \
  --path configs/example_ebible_grclxx.toml \
  --path configs/example_ebible_grctr.toml \
  --path configs/example_ebible_grcmt.toml \
  --path configs/example_ebible_grctcgnt.toml \
  --path configs/example_sblgnt.toml \
  --path configs/example_oshb_wlc.toml \
  --path configs/example_uxlc.toml \
  --path configs/example_ebible_hebwlc.toml \
  --path configs/example_mam.toml \
  --path configs/example_uhb.toml \
  --setting skip_range=2..100 \
  --setting direction=both \
  --setting min_normalized_length=4 \
  --setting controls=500_term_shuffle_500_random_representative \
  --setting correction=benjamini_hochberg \
  --setting source_set=Greek_LXX_TR_BYZ_TCG_SBLGNT_and_Hebrew_MT_UXLC_EBIBLE_MAM_UHB \
  --setting seed=20260527 \
  --out reports/study_locks/gospel_people_genealogy_prospective.manifest.json
```

Validate:

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/GOSPEL_PEOPLE_GENEALOGY_PROSPECTIVE_PREREGISTRATION.md \
  --manifest reports/study_locks/gospel_people_genealogy_prospective.manifest.json \
  --protocol protocols/gospel_people_genealogy_prospective.toml \
  --out reports/study_locks/gospel_people_genealogy_prospective.preflight.json
```

Only after both commands pass may this run execute:

```bash
python3 -m scripts.run_protocol protocols/gospel_people_genealogy_prospective.toml --resume
```

## Output Paths

- `reports/gospel_people_genealogy_prospective/greek_hit_patterns.csv`
- `reports/gospel_people_genealogy_prospective/greek_term_summary.csv`
- `reports/gospel_people_genealogy_prospective/hebrew_hit_patterns.csv`
- `reports/gospel_people_genealogy_prospective/hebrew_term_summary.csv`
- `reports/gospel_people_genealogy_prospective/initial_summary.csv`
- `reports/gospel_people_genealogy_prospective/control_targets.csv`
- `reports/gospel_people_genealogy_prospective/paired_controls_summary.csv`
- `reports/gospel_people_genealogy_prospective/controlled_summary.csv`
- `docs/GOSPEL_PEOPLE_GENEALOGY_PROSPECTIVE_REPORT.md`

## Primary Outcome

Primary row-level outcome:

- exact term/version-presence rows joined to representative paired-control
  status for MT_WLC, UHB, TR_NT, and SBLGNT target rows.

Primary study-level outcome:

- count of rows with adjusted representative-control support, if any, after
  Benjamini-Hochberg correction.

## Candidate Labels

Allowed labels:

- `prospective_review_queue_candidate`;
- `prospective_controlled_review_candidate`;
- `source_specific_review_candidate`;
- `prior_overlap_review_material`;
- `review_hold`;
- `not_reproducible`.

Disallowed labels:

- `confirmed_code`;
- `conclusive evidence`;
- `prophecy`;
- `statistical discovery`;
- `claim`.

## Failure Criteria

The study fails to produce a controlled review candidate if:

- lock manifest validation fails;
- preflight fails;
- no candidate rows meet the registered length and exact-version rules;
- representative controls are not favorable after correction;
- examples, context, or letter paths cannot be generated;
- the result depends on unregistered terms, spellings, sources, skip ranges, or
  broadened matching rules.

All observed rows must still be reported, including weak, negative,
source-specific, prior-overlap, or frequency-cautioned rows.

## Reporting Rules

The report must include:

- command or protocol used;
- git commit;
- lock manifest path;
- preflight path;
- term count;
- source labels;
- row counts at each stage;
- representative-control p/q values;
- examples and warning flags;
- explicit statement that the run is review material, not conclusive evidence
  of meaning.

## Interpretation Boundary

This study may identify review candidates. It cannot establish theological,
prophetic, historical, or statistical claims by itself.
