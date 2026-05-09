# Version-Presence Hit Export

`scripts.export_version_presence_hits` converts exact version-presence pattern
rows into ordinary ELS hit rows. This bridges the version-presence reports into
the existing same-skip extension tooling.

Use case:

1. Run an exact version-presence protocol.
2. Select all-source, multi-source, or source-specific pattern rows.
3. Reconstruct per-corpus hit rows from the stored offsets.
4. Feed those rows into `edls extensions` to test letters before and after the
   hit at the same signed interval.

## Hebrew Example

```bash
python3 -m scripts.export_version_presence_hits \
  --patterns reports/hebrew_screening_version_presence/hit_patterns.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --corpus UHB=configs/example_uhb.toml \
  --presence-scope present_all_observed_sources \
  --max-patterns-per-term 3 \
  --out reports/version_presence_extensions/hebrew_hits.csv \
  --manifest-out reports/version_presence_extensions/hebrew_hits.manifest.json
```

Then run extensions per corpus:

```bash
python3 -m els extensions \
  --config configs/example_oshb_wlc.toml \
  --hits reports/version_presence_extensions/hebrew_hits.csv \
  --corpus-label MT_WLC \
  --max-before 12 --max-after 12 \
  --phrase-words 4 \
  --include-both-sided \
  --max-extensions-per-hit 20 \
  --out reports/version_presence_extensions/hebrew_extensions_mt_wlc.csv
```

## Greek Example

```bash
python3 -m scripts.export_version_presence_hits \
  --patterns reports/greek_screening_version_presence/hit_patterns.csv \
  --corpus TR_NT=configs/example_ebible_grctr.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --presence-scope present_all_observed_sources \
  --max-patterns-per-term 3 \
  --out reports/version_presence_extensions/greek_hits.csv \
  --manifest-out reports/version_presence_extensions/greek_hits.manifest.json
```

## Notes

- Default scope is `present_all_observed_sources`.
- Add repeated `--presence-scope` flags to include multiple buckets.
- Add repeated `--term-id`, `--concept`, or `--category` flags for targeted
  queues.
- Use `--max-patterns-per-term` to avoid letting dense short terms dominate the
  extension queue.
- Exported rows include the original `term_id`, `concept`, `category`, and
  source-distribution fields, but `edls extensions` only needs the ordinary hit
  fields.

## Caution

This export does not create new hits. It reconstructs rows from already
recorded exact pattern offsets. Extension matches remain review material only:
they need surface-context review and controls before any interpretation.
