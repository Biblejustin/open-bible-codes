# Prospective Lane Status

Status: planning index, not a result report.

This page is generated from `configs/prospective_study_lanes.json`.
It lists which lanes are completed, blocked, or waiting on a new lock.

## Lanes

| Lane | Status | Read | Term file | Protocol | Report |
| --- | --- | --- | --- | --- | --- |
| `greek_surface_new_terms` | `ready_for_preflight` | ready for lock manifest and preflight | `terms/greek_surface_new_terms_clean_lock.csv` | `protocols/greek_surface_new_terms.toml` | `docs/GREEK_SURFACE_NEW_TERMS_REPORT.md` |
| `hebrew_modern_geopolitical_presence` | `completed_negative_controlled_result` | completed negative controlled result | `terms/hebrew_modern_geopolitical_prospective_terms.csv` | `protocols/hebrew_modern_geopolitical_prospective.toml` | `docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md` |
| `gog_magog_pair_controls` | `completed_negative_weak_controlled_result` | completed weak or negative controlled result | `terms/gog_magog_pair_prospective_terms.csv` | `protocols/gog_magog_pair_prospective.toml` | `docs/GOG_MAGOG_PAIR_PROSPECTIVE_REPORT.md` |
| `compound_extension_prospective` | `ready_for_preflight` | ready for lock manifest and preflight | `terms/compound_extension_prospective_terms_clean_lock.csv` | `protocols/compound_extension_prospective.toml` | `docs/COMPOUND_EXTENSION_PROSPECTIVE_REPORT.md` |
| `hebrew_concordance_words_prospective` | `ready_for_preflight` | ready for lock manifest and preflight | `terms/hebrew_concordance_prospective_terms_clean_lock.csv` | `protocols/hebrew_concordance_words_prospective.toml` | `docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_REPORT.md` |
| `local_terms_negative_appendix` | `completed_negative_curiosity_appendix` | completed negative curiosity appendix | `terms/local_terms_appendix.csv` | `protocols/local_terms_appendix.toml` | `docs/LOCAL_TERMS_APPENDIX_REPORT.md` |

## Blocked Lanes

| Lane | Needed input | Boundary |
| --- | --- | --- |

## Safe Commands

```bash
python3 -m scripts.check_prospective_study_lanes
python3 -m scripts.scaffold_prospective_study --list-profiles
python3 -m scripts.build_prospective_lane_status
```

## Interpretation Rules

- A lane marked blocked must not produce result-bearing outputs yet.
- Completed negative lanes can be rerun for reproducibility, not promoted.
- Post-discovery lanes stay review-only unless a fresh prospective lock is created first.
- This document summarizes planning state from `configs/prospective_study_lanes.json`; it does not change study status.
