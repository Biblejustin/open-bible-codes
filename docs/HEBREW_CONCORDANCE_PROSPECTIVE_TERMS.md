# Hebrew Concordance Prospective Terms

Status: term-source registration and screening note, not a result report.

On 2026-05-21, an open Hebrew concordance/lexicon source lane was added for future prospective work.

## Sources

- OpenScriptures StrongHebrewG XML: public-domain Strong's Hebrew dictionary headwords.
- STEP Bible TAHOT: CC BY 4.0 lexical tags used as an occurrence cross-check.

The raw tracked term file is `terms/hebrew_concordance_prospective_terms.csv`.
The clean tracked lock file is `terms/hebrew_concordance_prospective_terms_clean_lock.csv`.
Raw source files remain ignored under `data/raw/`.

## Build Rule

Rows are included when all of these are true:

- a Hebrew, Aramaic, or proper-name headword is present in StrongHebrewG;
- normalized Hebrew length is at least 4 letters;
- the Strong's id appears as a main lexical tag in STEP TAHOT;
- normalized Hebrew surface is unique in the generated file.

## Counts

| File | Raw rows | Normalized duplicate rows |
| --- | ---: | ---: |
| `terms/hebrew_concordance_prospective_terms.csv` | 3843 | 0 |

Category split:

| Category | Rows |
| --- | ---: |
| `strong_proper_names` | 1787 |
| `strong_nouns` | 1725 |
| `strong_adjectives` | 295 |
| `strong_particles_other` | 21 |
| `strong_verbs` | 15 |

## Prior-Evidence Screen

The file was screened against existing term pools and prior report evidence before any result-producing prospective run.

| File | Screened rows | Skipped short rows | Prior-overlap matches | Clean candidates |
| --- | ---: | ---: | ---: | ---: |
| `terms/hebrew_concordance_prospective_terms.csv` | 3843 | 0 | 636 | 3577 |

The ignored audit artifacts were written under `reports/study_locks/`:

- `hebrew_concordance_prospective_terms.prior_evidence_audit.*`
- `hebrew_concordance_prospective_terms.clean_candidates.*`

## Interpretation

- The concordance-derived raw list is now a tracked study input.
- The raw list is not a clean prospective lock because 266 rows overlap prior evidence.
- The clean lock file was re-audited with zero prior-evidence matches.
- A result-producing run should use the clean locked candidate set.
- `docs/PROSPECTIVE_LANE_STATUS.md` marks this lane ready for lock manifest and preflight.
