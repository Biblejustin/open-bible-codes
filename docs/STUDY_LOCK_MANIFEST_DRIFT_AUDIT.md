# Study Lock Manifest Drift Audit

Status: historical audit, not a prospective approval.

This audit lists historical study-lock manifests and separates current
manifests from stale fingerprints or structural lock failures.
A drifted historical manifest is not a failed result.
It means the old lock no longer validates against the current workspace
and must not be reused as a fresh prospective lock.

## Inputs

- Manifest directory: `reports/study_locks`
- Row output: `reports/study_lock_manifest_drift_audit/manifest_drift_audit.csv`
- Summary output: `reports/study_lock_manifest_drift_audit/summary.csv`

## Summary

- total_manifests: 14
- current: 1
- fingerprint_drift: 9
- structural_fail: 4

## Manifest Rows

| Manifest | Name | Status | Audit status | Structural failures | Fingerprint failures |
| --- | --- | --- | --- | --- | --- |
| `reports/study_locks/compound_extension_prospective.manifest.json` | compound_extension_prospective | locked | fingerprint_drift | none | locked path changed: docs/COMPOUND_EXTENSION_PROSPECTIVE_PREREGISTRATION.md |
| `reports/study_locks/drift_checker_smoke.manifest.json` | drift_checker_smoke | locked | structural_fail | git dirty-state is true | locked path changed: docs/STUDY_LOCK_MANIFESTS.md |
| `reports/study_locks/gog_magog_pair_prospective.manifest.json` | gog_magog_pair_prospective | locked | fingerprint_drift | none | locked path changed: docs/GOG_MAGOG_PAIR_PROSPECTIVE_PREREGISTRATION.md; locked path changed: scripts/analyze_gog_magog_pairs.py; locked path changed: scripts/analyze_pair_baselines.py; locked path changed: scripts/build_gog_magog_pair_prospective_report.py |
| `reports/study_locks/gospel_people_genealogy_prospective.manifest.json` | gospel_people_genealogy_prospective | locked | current | none | none |
| `reports/study_locks/greek_lexicon_extension_prospective.manifest.json` | greek_lexicon_extension_prospective | locked | fingerprint_drift | none | locked path changed: docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_PREREGISTRATION.md; locked path changed: docs/GREEK_LEXICON_PROSPECTIVE_SOURCE.md; locked path changed: protocols/greek_lexicon_extension_prospective_lock.toml |
| `reports/study_locks/greek_surface_new_terms.manifest.json` | greek_surface_new_terms | locked | fingerprint_drift | none | locked path changed: docs/GREEK_SURFACE_NEW_TERMS_PREREGISTRATION.md; locked path changed: protocols/greek_surface_new_terms.toml |
| `reports/study_locks/greek_surface_prospective.manifest.json` | greek_surface_prospective | locked | fingerprint_drift | none | locked path changed: docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md; locked path changed: protocols/greek_surface_prospective.toml |
| `reports/study_locks/greek_surface_standard_checker_smoke.manifest.json` | greek_surface_standard_checker_smoke | locked | structural_fail | git dirty-state is true | locked path changed: docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md; locked path changed: docs/STUDY_LOCK_MANIFESTS.md |
| `reports/study_locks/greek_surface_standard_smoke.manifest.json` | greek_surface_standard_smoke | locked | structural_fail | git dirty-state is true | locked path changed: docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md; locked path changed: docs/STUDY_LOCK_MANIFESTS.md |
| `reports/study_locks/hebrew_concordance_words_prospective.manifest.json` | hebrew_concordance_words_prospective | locked | fingerprint_drift | none | locked path changed: docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_PREREGISTRATION.md |
| `reports/study_locks/hebrew_modern_geopolitical_presence.manifest.json` | hebrew_modern_geopolitical_presence | locked | fingerprint_drift | none | locked path changed: docs/HEBREW_MODERN_GEOPOLITICAL_PRESENCE_PREREGISTRATION.md; locked path changed: protocols/hebrew_modern_geopolitical_prospective.toml |
| `reports/study_locks/hebrew_theology_prospective.manifest.json` | hebrew_theology_prospective | locked | fingerprint_drift | none | locked path changed: docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md; locked path changed: protocols/hebrew_theology_prospective.toml |
| `reports/study_locks/local_terms_negative_appendix.manifest.json` | local_terms_negative_appendix | locked | fingerprint_drift | none | locked path changed: docs/LOCAL_TERMS_NEGATIVE_APPENDIX_PREREGISTRATION.md |
| `reports/study_locks/preflight_smoke.manifest.json` | preflight_smoke | locked | structural_fail | git dirty-state is true | locked path changed: docs/GREEK_EXPANDED_PROSPECTIVE_PREREGISTRATION.md |

## Interpretation

- `current` means the manifest still validates against current files.
- `fingerprint_drift` means the lock structure is usable, but at least
  one locked file or directory changed since the lock was built.
- `structural_fail` means the manifest was dirty, incomplete, missing
  paths, unlocked, unreadable, or otherwise invalid as a lock.
- Use `scripts.check_study_lock_manifest` for one fresh, study-specific
  manifest before a result-producing prospective run.
