# Study Lock Manifests

Status: workflow note for future prospective studies.

Use `scripts.build_study_lock_manifest` before any result-producing prospective
run. The manifest records the exact files and settings that were locked before
searching.

Preregistration template:

- `docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md`

Optional scaffold helper:

```bash
python3 -m scripts.scaffold_prospective_study \
  --name greek_surface_future_study \
  --language greek \
  --source TR_NT=configs/example_ebible_grctr.toml \
  --source BYZ_NT=configs/example_ebible_grcmt.toml \
  --source TCG_NT=configs/example_ebible_grctcgnt.toml \
  --source SBLGNT=configs/example_sblgnt.toml \
  --skip-range 2..50 \
  --direction both \
  --min-normalized-length 5
```

The scaffold helper writes a draft preregistration document only. It does not
create a term file, create a protocol, build a lock manifest, or run a search.

Current readiness profiles can prefill the same scaffold, but they are now
historical/status records. Do not use a completed profile as a new
claim-producing lane without first creating a genuinely new term/source target
set and a new clean lock.

```bash
python3 -m scripts.scaffold_prospective_study --list-profiles
python3 -m scripts.check_prospective_study_lanes
```

Profiles are stored in `configs/prospective_study_lanes.json`. They are planning
defaults/status records only. `scripts.check_prospective_study_lanes` validates
profile shape and source-config paths, but it does not decide which lane to run.
Review and edit any generated preregistration before building a lock manifest.

After filling a study-specific preregistration document, run:

```bash
python3 -m scripts.check_preregistration_placeholders \
  docs/[GREEK_SURFACE_FUTURE_STUDY_PREREGISTRATION].md
```

The placeholder checker fails on leftover bracket tokens such as `[name]`,
`[protocol]`, or `[metric]`. Use it before building the lock manifest so the
manifest records a completed preregistration, not a draft template.

For a genuinely new prospective discovery list, run a term-leakage audit before
preflight:

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/[future-term-file].csv \
  --evidence reports/<prior-evidence>.csv \
  --min-normalized-length 5 \
  --out reports/study_locks/greek_surface_future_study.term_audit.csv \
  --fail-on-match
```

The audit sidecar summary can be required during preflight. Skip this guard only
for studies explicitly framed as confirmatory follow-up or post-discovery
review.

If the audit finds prior-evidence overlaps, filter them before locking a new
discovery list:

```bash
python3 -m scripts.filter_prospective_terms \
  --candidate terms/[future-term-file].csv \
  --audit reports/study_locks/greek_surface_future_study.term_audit.csv \
  --out terms/[future-term-file-clean].csv
```

Before a result-producing run, combine the checks:

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/[GREEK_SURFACE_FUTURE_STUDY_PREREGISTRATION].md \
  --manifest reports/study_locks/greek_surface_future_study.manifest.json \
  --protocol protocols/[greek_surface_future_study].toml \
  --clean-term-audit reports/study_locks/greek_surface_future_study.term_audit.csv.summary.json \
  --out reports/study_locks/greek_surface_future_study.preflight.json
```

The prospective preflight also checks release hygiene before a run: remotes must
point at `Biblejustin/open-bible-codes`, forbidden account text must not appear
in remotes or tracked/repository files, risky generated artifacts must not be
tracked, and high-confidence secret-token patterns fail the run.

Use a study-specific `--out` path and pass that same file to the final report
builder. If `--out` is omitted, the tool derives that path from the manifest
name. For a historical locked run, do not add a preflight step to the locked
protocol after results exist; that changes the protocol fingerprint and makes
the original lock manifest fail validation.

The current target-readiness matrix is tracked in
`docs/PROSPECTIVE_STUDY_READINESS.md`.

## Command Shape

```bash
python3 -m scripts.build_study_lock_manifest \
  --name greek_surface_future_study \
  --path terms/[future-term-file].csv \
  --path protocols/[future-protocol].toml \
  --path configs/example_ebible_grctr.toml \
  --path configs/example_ebible_grcmt.toml \
  --path configs/example_ebible_grctcgnt.toml \
  --path configs/example_sblgnt.toml \
  --setting skip_range=2..50 \
  --setting direction=both \
  --setting min_normalized_length=5 \
  --setting controls=5000_shuffled_term_and_5000_random \
  --setting correction=benjamini_hochberg \
  --out reports/study_locks/greek_surface_future_study.manifest.json
```

By default, corpus config TOML files are expanded to include their referenced
source files. Use `--no-expand-corpus-configs` only for a narrow tooling smoke
test, not for real preregistration.

## Required Manifest Fields

The manifest includes:

- tool and EDLS version;
- generated UTC timestamp;
- git commit and dirty-state;
- requested paths;
- locked file and directory fingerprints;
- missing paths, if any;
- locked non-file settings;
- notes supplied at command time.

## Interpretation

A lock manifest is not a result. It is evidence that the study inputs were
fixed before a search ran. If the git dirty-state is true, commit first and
rebuild the manifest before treating a study as prospective.

Before running the study, validate the lock:

```bash
python3 -m scripts.check_study_lock_manifest \
  reports/study_locks/greek_surface_future_study.manifest.json \
  --required-setting skip_range \
  --required-setting direction \
  --required-setting min_normalized_length \
  --required-setting controls \
  --required-setting correction
```

The checker fails if the manifest is not locked, has missing paths, was created
from a dirty git tree, lacks required settings, or any locked file/directory
fingerprint no longer matches the current workspace.

New directory fingerprints are content-aware: file names, entry kinds, file
sizes, and file SHA-256 values are locked. The checker still accepts older
directory fingerprints that used the earlier mtime-based tree hash so historical
locks remain readable, but new study locks should be rebuilt with the current
tool before they are treated as prospective evidence.
