# STEP TAHOT Source Audit

Last run: 2026-05-05.

## Scope

This audit adds STEP Bible `TAHOT` as an optional Hebrew source and compares the
converted stream against the existing MT-family corpora. It is not part of the
public baseline and should not be treated as a pure Leningrad ketiv source.

Upstream TAHOT states that the selected text may follow qere, restore missing
text, and include LXX-preserved additions converted to Hebrew from BHS/BHK
apparatus. That makes it useful for "which patterns are in which versions?"
analysis, but it must be labeled separately.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/step_tahot_source_audit.toml --resume
```

The downloader writes ignored local source artifacts:

- `data/raw/step/tahot/`
- `data/processed/step/tahot.csv`
- `data/processed/step/tahot.manifest.json`

The comparison writes ignored reports:

- `reports/mt_version_comparison_step_tahot/summary.csv`
- `reports/mt_version_comparison_step_tahot/verse_differences.csv`
- `reports/mt_version_comparison_step_tahot/mt_version_comparison_step_tahot.md`
- `reports/mt_version_comparison_step_tahot/manifest.json`

## Import Check

`STEP_TAHOT` loads through the normal corpus path with:

| Metric | Value |
| --- | ---: |
| Books | 39 |
| Verses | 23,261 |
| Normalized letters | 1,197,732 |

The importer removes STEP punctuation suffixes after backslash separators before
normalization. This keeps paragraph markers `פ` and `ס` out of the ELS stream.
The pointed Hebrew is otherwise preserved in the processed CSV and normalized by
the regular Hebrew loader.

## Difference Summary

| Pair | Shared refs | Equal refs | Different refs | Left-only | Right-only |
| --- | ---: | ---: | ---: | ---: | ---: |
| `MT_WLC_vs_STEP_TAHOT` | 23,011 | 20,037 | 2,974 | 202 | 250 |
| `UXLC_vs_STEP_TAHOT` | 23,011 | 20,034 | 2,977 | 202 | 250 |
| `MAM_vs_STEP_TAHOT` | 23,001 | 19,217 | 3,784 | 201 | 260 |
| `EBIBLE_WLC_vs_STEP_TAHOT` | 23,011 | 20,037 | 2,974 | 202 | 250 |
| `UHB_vs_STEP_TAHOT` | 23,145 | 22,415 | 730 | 0 | 116 |

TAHOT is closest to UHB by this normalized verse comparison. That is expected
because both streams are translator-oriented derived MT-family data rather than
plain WLC packaging.

## Source-Type Counts

TAHOT word-row source-type prefixes in the converted stream:

| Prefix | Word rows |
| --- | ---: |
| `L` | 304,081 |
| `Q` | 1,309 |
| `X` | 152 |
| `R` | 27 |
| Other L-prefixed combinations | 69 |

`Q`, `R`, and `X` are the main reason this source should remain separately
labeled in version-presence work.

## Read

Add `STEP_TAHOT` to future version-presence protocols only when the question is
explicitly about source-family survival. Do not mix it into "all Leningrad"
counts or use it as a plain MT duplicate.

Focused modern/local exact-hit version-presence follow-up:
`docs/STEP_TAHOT_VERSION_PRESENCE_REVIEW.md`.
