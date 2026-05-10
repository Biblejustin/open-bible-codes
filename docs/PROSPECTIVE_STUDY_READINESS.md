# Prospective Study Readiness

Status: planning aid. This file does not choose a study target or run a search.

The current next-phase lock is tracked in
`docs/PROSPECTIVE_STUDY_NEXT_LOCK.md`. That document freezes the report
presentation layer, post-discovery controlled review candidates, and the next
eligible fresh prospective lane.

Use this matrix to decide which next result-producing study to lock. Every lane
below must be converted into a study-specific preregistration document, lock
manifest, and protocol before any new result-producing run.

## Preflight Command

Before the lock, audit the candidate term list for reuse of prior evidence:

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/STUDY_TERMS.csv \
  --evidence reports/PRIOR_EVIDENCE.csv \
  --min-normalized-length 5 \
  --out reports/study_locks/STUDY.term_audit.csv \
  --fail-on-match
```

After a preregistration and lock manifest exist, run:

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/STUDY_PREREGISTRATION.md \
  --manifest reports/study_locks/STUDY.manifest.json \
  --protocol protocols/study.toml \
  --clean-term-audit reports/study_locks/STUDY.term_audit.csv.summary.json \
  --out reports/study_locks/STUDY.preflight.json
```

This checks:

- git working tree cleanliness;
- forbidden account text in remotes and repository files;
- unresolved preregistration placeholders;
- lock-manifest status, required settings, dirty-state, and path fingerprints;
- optional clean prospective-term audit summary;
- optional protocol dry-run.

If `--out` is omitted, the tool derives a study-specific path from the manifest
name, such as `reports/study_locks/STUDY.preflight.json`. Do not edit a locked
historical protocol only to add a preflight step, because the protocol file
itself is part of the lock manifest fingerprint.

## Candidate Lanes

Machine-readable lane profiles live in
`configs/prospective_study_lanes.json`. Use:

```bash
python3 -m scripts.check_prospective_study_lanes
python3 -m scripts.scaffold_prospective_study --list-profiles
python3 -m scripts.scaffold_prospective_study --profile PROFILE_ID --print-command
```

| Lane | Current evidence | What can be prospective? | Main risk |
| --- | --- | --- | --- |
| Greek `δοξα` (doxa; English: glory) extension follow-up | strongest controlled Greek review row; four-source support; 5000/5000 and 20000/20000 post-discovery follow-ups passed their registered review gates | no further claim-oriented doxa rerun is recommended without a genuinely new prospective design | already discovered; cannot be treated as original discovery |
| Greek surface rows `ανομια` (anomia; English: lawlessness), `ισαακ` (Isaak; English: Isaac), `τερασ` (teras; English: wonder) | post-screen surface rows with all-available matched controls q = `0.032258`; first locked surface prospective run was negative at length >= 5; second-cohort audit found 0 clean length >= 5 rows left in the existing expanded Greek pool | only a genuinely new source term file with clean prior-evidence audit; see `docs/GREEK_SURFACE_SECOND_COHORT_READINESS.md` | current rows and all previously tested cohort rows are prior evidence; reusing the same pool would be selection leakage |
| Greek length-4 surface rows | locked prospective run exposed `αμην` (amen; English: amen), `αραμ` (Aram; English: Aram), `ασηρ` (Aser; English: Asher), `δασα` (dasa; English: generated control-like form), `σαβα` (Saba; English: Sheba/Seba), `σιων` (Sion; English: Zion), and `χουσ` (Chous; English: Cush), but generated vocabulary controls overlap every target with q range `0.278607..0.905473` | no claim-oriented study recommended unless there is a separately justified short-term hypothesis | short-form density and control-pool selection dominate |
| Hebrew/modern/geopolitical exact-version study | completed locked source-distribution follow-up in `docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md`; no row survived adjusted representative controls | no further claim-oriented rerun is recommended without a materially new hypothesis or term source | many rows are short-form density; full phrases are mostly absent; representative controls explained the nonzero rows |
| Gog/Magog focused study | completed locked prospective run: target rows occurred in MT_WLC and UHB, but both were `not_unusual`; synthetic 3+4 Hebrew pairs often matched or exceeded target density | no further claim-oriented Gog/Magog rerun is recommended without a materially new hypothesis | short forms and pair-density baselines are strong confounders |
| All-codes compound-extension follow-up | relaxed all-codes screen found 8 selected rows with compound same-skip extensions containing the hidden term; 250/250 row-local controls leave 14 rows at min-q <= 0.05, 7 at min-q <= 0.10, and 22 not unusual, while conservative all-control q leaves only 2 rows at q <= 0.10 and none at q <= 0.05; a locked 5000/5000 confirmatory pass for the selected `יום יהוה` (yom YHWH; English: day of YHWH) -> `היומיהוה` (hayom YHWH; English: the day of YHWH) key keeps all five MT-family rows at conservative all-control q = 0.003599 | a fixed compound-extension study with predeclared term list, extension rule, and larger matched same-length/same-skip controls | current rows are post-screen discoveries from a broad queue; the 5000/5000 pass is confirmatory review, not prospective discovery |
| Local-term negative/curiosity study | completed locked curiosity appendix in `docs/LOCAL_TERMS_APPENDIX_REPORT.md`; Cowboy appears in Hebrew, while Catering, Simsberry, and Simscorner are absent under the fixed exact-version matrix | no further work needed unless new local terms are intentionally added as an appendix | mainly curiosity value; low theological relevance |

## Recommended Order

1. A second Greek surface prospective cohort only if a genuinely new term source
   is supplied; the existing expanded Greek pool is blocked by
   `docs/GREEK_SURFACE_SECOND_COHORT_READINESS.md`.
2. Hebrew/modern/geopolitical is complete and should stay as
   source-distribution review material unless a materially new hypothesis is
   supplied.
3. Gog/Magog should stay in negative/weak findings unless a materially new,
   separately locked hypothesis is supplied.
4. All-codes compound-extension follow-up only after a larger matched-control
   design is locked.
5. Local-term study is complete as a transparent negative/curiosity appendix.

## Minimum Lock Contents

Every lane should lock:

- term file path and exact normalized term count;
- source configs and compatible source labels;
- skip range and direction;
- minimum normalized length;
- hit cap, if any;
- surface/context rule;
- control design and sample budget;
- correction method;
- candidate labels and failure criteria;
- report output paths.
- clean prospective-term audit summary, unless the study is explicitly a
  confirmatory follow-up or post-discovery review.

## Non-Negotiable Boundary

Do not call a row a claim because it is hidden, version-stable, or visually
interesting. Claim-level language requires a study that was locked before the
result-producing run and survived the registered controls.
