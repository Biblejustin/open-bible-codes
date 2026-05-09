# Hebrew Control Version Presence

This is the tracked summary for the Hebrew null/frequency control exact-hit
version-presence run:

```bash
python3 -m scripts.run_protocol protocols/hebrew_control_version_presence.toml --resume
```

## Scope

- Term sources: `terms/null_controls.csv`, `terms/frequency_anchors.csv`
- Corpora: `MT_WLC`, `UXLC`, `EBIBLE_WLC`, `MAM`, `UHB`
- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `4`
- Max hits: `100` per term per corpus

## Output

Ignored local outputs:

- `reports/hebrew_control_version_presence/hit_patterns.csv`
- `reports/hebrew_control_version_presence/term_summary.csv`
- `reports/hebrew_control_version_presence/hebrew_control_version_presence.md`
- `reports/hebrew_control_version_presence/manifest.json`

Latest run:

- Runtime: `22.086s`
- Declared Hebrew control rows: `23`
- Summarized rows after minimum length filter: `13`
- Hit records: `3,741`
- Exact pattern rows: `981`

Pattern scope counts:

| Scope | Pattern rows |
| --- | ---: |
| `present_all_observed_sources` | 526 |
| `present_all_leningrad_streams` | 139 |
| `present_multiple_sources` | 146 |
| `source_specific` | 170 |

## Current Read

Controls also create stable exact ref-key patterns across all five Hebrew
streams:

- Scrambled YHWH / `וההי`: 27 all-source exact patterns.
- Scrambled Messiah / `חישמ`: 91 all-source exact patterns.
- Scrambled Torah / `הרות`: 86 all-source exact patterns.
- Scrambled Israel / `לרשאי`: 81 all-source exact patterns.
- Nonsense 5a / `בגדהו`: 23 all-source exact patterns.

That means exact version stability is mainly a reproducibility filter. It does
not distinguish meaningful terms from controls.

## Caution

Use version-presence reports to separate shared, Leningrad-family, multi-source,
and source-specific rows. Do not use them as claim evidence without matched
controls, context review, and correction across the screened list.
