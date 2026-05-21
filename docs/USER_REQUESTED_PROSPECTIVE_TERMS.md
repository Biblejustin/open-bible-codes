# User-Requested Prospective Terms

Status: term-source registration and screening note, not a result report.

On 2026-05-21, a user-requested Gospel and Greek surface term source was added for future prospective work. The raw tracked term files are:

- `terms/greek_surface_new_terms.csv`
- `terms/compound_extension_prospective_terms.csv`

## Scope

The Greek file contains user-supplied Greek terms plus curated Greek Gospel names: the genealogy of Christ, disciples, named women in the Gospels, and other Gospel people.

The Hebrew file contains conventional Hebrew target spellings for Gospel/core names, the genealogy of Christ, disciples, named women in the Gospels, and other Gospel people. These spellings are registered as study-input targets, not as a source-critical judgment about every manuscript or transliteration tradition.

## Counts

| File | Raw rows | Normalized duplicate rows |
| --- | ---: | ---: |
| `terms/greek_surface_new_terms.csv` | 443 | 0 |
| `terms/compound_extension_prospective_terms.csv` | 68 | 0 |

## Prior-Evidence Screen

These files were screened against existing term pools and prior report evidence before any result-producing prospective run.

| File | Screened rows | Skipped short rows | Prior-overlap matches | Clean candidates |
| --- | ---: | ---: | ---: | ---: |
| `terms/greek_surface_new_terms.csv` | 371 | 72 | 3005 | 236 |
| `terms/compound_extension_prospective_terms.csv` | 36 | 32 | 13 | 27 |

The ignored audit artifacts were written under `reports/study_locks/`:

- `greek_surface_new_terms.prior_evidence_audit.*`
- `greek_surface_new_terms.clean_candidates.*`
- `compound_extension_prospective_terms.prior_evidence_audit.*`
- `compound_extension_prospective_terms.clean_candidates.*`

## Interpretation

- The raw lists are now tracked study inputs.
- The raw lists are not clean prospective locks because many rows overlap prior evidence.
- A result-producing run should use a clean locked candidate set or explicitly label overlapping rows as post-screen/review-only.
- `docs/PROSPECTIVE_LANE_STATUS.md` keeps the affected lanes blocked until a clean prospective lock is created.
