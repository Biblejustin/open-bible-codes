# Performance Notes

Observed on the local development machine on 2026-05-04. Times are wall-clock unless noted. Treat them as directional, because corpus cache warmth, CPU load, and worker scheduling affect runs.

## Summary

| Area | Before | After | Observed gain |
| --- | ---: | ---: | ---: |
| Synthetic multi-term Aho count, 300k Greek letters, 100 terms, skips 2-50 | 1.71s | 0.40s with `--jobs 4` | 4.3x |
| TR NT theological batch count, 52 terms, skips 2-50 | 4.08s | 0.92s with `--jobs 4` | 4.4x |
| Three separate TR NT batch term-set runs | 3.42s | 1.52s with `batch-many` | 2.3x |
| All public corpora, original three term sets, `batch-many` | 27.11s with `--jobs 1` | 8.72s with `--jobs 0` | 3.1x |
| Surface-context NT, TR + SBLGNT, original three term sets | 42.03s serial | 4.99s with chunked `--jobs 0` | 8.4x |
| Critical omission breaks, TR vs SBLGNT, three Greek term sets | 18.40s | 7.08s with bulk term matching | 2.6x |
| Word-count reports, all public corpora | 16.59s | 9.02s with cached annotations and faster CSV writes | 1.8x |
| Related-name pairs, all public corpora | 13.57s | 7.70s with shared skip lanes and bisect nearest hits | 1.8x |
| Gog/Magog pair controls, all public corpora | 60.48s | 22.21s with skip-hit jobs | 2.7x |
| Strict Gog/Magog pair controls, all public corpora | 49.23s | 12.33s with skip-hit jobs | 4.0x |
| Pair baselines, all public corpora | 45.27s | 9.71s with skip-hit jobs | 4.7x |
| Beast/Dragon one-corpus controls | 12.79s | 4.38s with skip-hit jobs | 2.9x |
| Synthetic pair baselines, MT_WLC | 13.81s | 5.47s with skip-hit jobs | 2.5x |
| Extension paired controls, public baseline 10/10 samples | 72.17s | 8.65s with batched control-query matching | 8.3x |
| Extension overlap controls, public baseline 50/50 samples | 64.85s | 4.16s with batched control-query matching | 15.6x |
| Exact-center extension controls, public baseline 200/200 samples | 83.59s | 3.66s with batched control-query matching | 22.8x |
| Exact-center cohort controls, public baseline 50/50 samples | 44.27s | 4.11s with batched control-query matching | 10.8x |
| Synthetic extension baselines, public baseline samples | 43.13s | 4.21s with batched synthetic-query matching | 10.2x |
| ELS controls, public baseline 3/25 shuffles | 42.95s | 30.30s with merged observed + shuffled-term scan | 1.4x |
| Hebrew screening exact-version presence, 557 terms, 5 MT-family corpora | 416.30s | 23.26s with bulk capped matching + `--corpus-jobs 0` | 17.9x |
| Greek screening exact-version presence, 413 terms, 4 NT corpora | 49.50s after bulk capped matching | 13.24s with `--corpus-jobs 0` | 3.7x |
| Wide focus Hebrew exact-version presence, 30 terms, 5 MT-family corpora, skips 2-250 | 266.70s | 56.24s with `--corpus-jobs 0` | 4.7x |
| Wide focus Greek exact-version presence, 27 terms, LXX + 4 NT corpora, skips 2-250 | 244.86s | 127.19s with `--corpus-jobs 0` | 1.9x |
| Full-span partition findings, 106 completed partition CSVs, about 15 GB | 325.36s cold scan | 0.35s warm summary cache | 929.6x |
| CRD self-surface center-word aggregation, 5.3 GB classified-hit CSV | 32.08s Python CSV scan | 0.10s DuckDB query | 320.8x |
| Apocrypha bridge study heavy steps | 649.21s serial defaults | 101.43s with `--jobs 0` | 6.4x |
| Full public baseline protocol, core analyses before ELS controls | 68.34s | 25.00s with protocol step parallelism and integrity stamps | 2.7x |
| Full public baseline protocol with ELS controls and original term sets | 25.00s core baseline | 46.17s including controls | new control coverage |
| Full public baseline protocol with prophetic terms | 46.17s before prophetic terms | 93.08s including prophetic terms | broader declared term coverage |
| OSHB WLC corpus load | 3.16s cold parse | 0.38s cache hit | 8.3x |

## Changes

- Reworked `find_els` around skip-lane scanning and reused lanes for forward/backward checks.
- Replaced repeated Python Aho fail-walks with a dense goto table.
- Encoded corpus text once per multi-term count, then scanned encoded strides.
- Added `--jobs` to `batch` and `batch-many` for parallel skip counting.
- Added `batch-many` so theological, modern names/dates, Table of Nations, and prophetic terms share each corpus scan.
- Added per-corpus timing to `batch-many` manifests.
- Added `--jobs` to `surface-context`, parallelizing per-term surface checks with process workers.
- Added bulk multi-term ELS matching for scripts that need hit metadata, cutting repeated full-corpus `find_els` passes.
- Cached word-count multiple annotations and display-word lookups, counted normalized content keys once, and switched large word-count report writes to a lean CSV writer.
- Shared skip lanes across related-name term scans and replaced nearest-hit linear search with bisect lookup.
- Added parallel skip-hit metadata collection for Gog/Magog-style pair controls,
  with repeated sample-pair metric caching and shared chapter caches.
- Reused the same skip-hit worker path for length-matched synthetic pair baselines.
- Batched extension-control sampled queries through one multi-query ELS automaton per target/skip instead of rescanning once per sampled query.
- Combined shuffled-term and random extension-control samples into the same
  target scan.
- Batched synthetic extension baseline queries the same way, while preserving repeated sampled-query rows.
- Batched exact version-presence hit extraction through one capped multi-query
  ELS pass per corpus instead of one `find_els` run per term.
- Added `--corpus-jobs` to exact version-presence analysis so independent
  corpora can be scanned concurrently.
- Chunked surface-context term workers so each worker shares skip lanes, and indexed surface-context term relationships once per corpus.
- Added a bulk AC surface-context path for single-worker runs while keeping C-level lane finds for parallel chunks.
- Added protocol-level parallel groups so independent analysis steps can run at the same time.
- Added ELS control reports using shuffled-letter and shuffled-term null models.
- Merged ELS-control observed counts into the shuffled-term count pass on the
  same corpus text.
- Added protocol timing summaries and printed slow-step tables.
- Added corpus pickle cache for repeated corpus loads.
- Added a per-partition summary cache for full-span dense report regeneration,
  keyed by partition CSV and manifest metadata.
- Added an optional DuckDB report database for dense ignored report artifacts,
  so repeated CRD filters/group-bys do not rescan 5 GB CSVs in Python.
- Added `--jobs` to apocrypha bridge-candidate and bridge-control scripts,
  then ran the apocrypha protocol with all available skip workers.

## Current Protocol Settings

`protocols/public_baseline.toml` uses:

- `max_parallel = 3`
- `progress_interval_seconds = 15`
- `batch-many --jobs 0`
- `surface-context --jobs 0`
- `analyze_els_controls.py --letter-shuffles 3 --term-shuffles 25 --jobs 0 --progress`

`--jobs 0` means use CPU count, capped by available skip or term work.
Corpus-level parallelism exists as `batch-many --corpus-jobs`; local
benchmarking showed `--corpus-jobs 1` remained the stable choice for the public
baseline batch step. Exact version-presence protocols use
`--corpus-jobs 0`, because each corpus scan is independent.

Bootstrap remains serial, the seven independent analysis steps run in the `analysis` parallel group, and report indexing remains serial after analysis outputs exist. A `max_parallel = 4` trial was similar in wall-clock time but caused more per-step contention, so the default uses 3.
Protocol runs print active-step heartbeats for long parallel groups. Set
`progress_interval_seconds = 0` to disable protocol heartbeats.
Multiprocessing defaults to `fork` on Linux for local speed, `forkserver` on
macOS when available to avoid fork-after-import fragility, and `spawn` on other
platforms. Set `EDLS_MULTIPROCESSING_START_METHOD` to override for portability
checks or local benchmarking.

Repeated protocol benchmarks can be captured with:

```bash
python3 -m scripts.benchmark_protocol protocols/public_baseline.toml --runs 3
```

The benchmark writes JSON and Markdown summaries under `reports/benchmarks/`.
Protocol resume uses per-step integrity stamps, so cached output must have both
the expected files and matching input/command/output fingerprints from a prior
successful run.

`protocols/apocrypha_bridge_study.toml` uses `--jobs 0` for the bridge
candidate scan, non-Bible bridge controls, and ordinary apocrypha-only count
comparison. On the local development machine this dropped the heavy apocrypha
steps from 649.21s with serial defaults to 101.43s:

| Step | Serial default | `--jobs 0` |
| --- | ---: | ---: |
| `bridge_candidates` | 138.87s | 23.08s |
| `bridge_controls` | 406.28s | 60.92s |
| `apocrypha_only_counts` | 104.07s | 17.58s |

`scripts/analyze_els_controls.py` took 30.30s protocol-only with `--jobs 0`
after merging observed counts into the shuffled-term scan; the same settings
took 135.45s with serial counting before the skip-job work. The control sample
is small by design for baseline speed, so strong candidates should be rerun
with more shuffles before interpretation.

## Latest Observed Protocol Hot Spots

Fresh full `public_baseline` protocol after current controls and optimization
work:

| Step | Time |
| --- | ---: |
| `els_controls` | 38.24s |
| `gog_magog_pairs` | 22.64s |
| `surface_context_nt` | 18.91s |
| `gog_magog_strict_pairs` | 12.28s |
| `batch_term_sets` | 11.16s |
| `targeted_paired_controls` | 10.81s |
| `critical_omission_breaks` | 9.75s |
| `pair_baselines` | 9.71s |
| `related_name_pairs` | 9.00s |
| `extension_paired_controls` | 8.46s |
| `synthetic_pair_baselines` | 5.46s |
| Full protocol resume run | 141.41s |

After extension-control batching, the public-baseline
`extension_paired_controls` step dropped from 72.17s to 8.65s with the same
10/10 sample settings.
The single-row 200/200 `extension_exact_center_controls` step dropped from
83.59s to 3.66s.
The cross-corpus `extension_overlap_controls` step dropped from 64.85s to
4.16s, and `extension_exact_center_cohort_controls` dropped from 44.27s to
4.11s.
`synthetic_extension_baselines` also dropped from 43.13s to 4.21s.
After skip-hit metadata jobs, `gog_magog_pairs` dropped from 60.48s to 22.21s,
`gog_magog_strict_pairs` dropped from 49.23s to 12.33s, `pair_baselines`
dropped from 45.27s to 9.71s, and one-corpus Beast/Dragon controls dropped
from 12.79s to 4.38s. `synthetic_pair_baselines` dropped from 13.81s to
5.47s with the same worker path.
After merging ELS-control observed and shuffled-term scans, `els_controls`
dropped from 42.95s to 30.30s.
After bulk capped matching, `hebrew_screening_version_presence` dropped from
416.30s to 109.20s. Corpus-level version-presence workers then dropped Hebrew
screening again from 109.20s to 23.26s, and dropped
`greek_screening_version_presence` from 49.50s to 13.24s.
After corpus-level version-presence workers, `wide_focus_exact_presence`
dropped from 266.70s to 56.24s for Hebrew and from 244.86s to 127.19s for
Greek.

Protocol-level parallelism:

| Setting | Full protocol time |
| --- | ---: |
| Before protocol step parallelism | 41.29s |
| `max_parallel = 2` | 30.11s |
| `max_parallel = 3` | 22.92s before integrity stamps, 25.00s after |
| `max_parallel = 4` | 23.18s |
| `max_parallel = 3` with ELS controls | 54.59s before input-aware stamps, 64.69s after input-aware stamps, 46.17s after hybrid surface-context, 93.08s after prophetic terms, 149.93s with the current full control/report stack, 141.41s on latest resume run |

Data CSV reports were unchanged by protocol-level parallelism. `reports/INDEX.md` and `reports/index.json` refresh because report index metadata is regenerated.

Critical omission direct/profiled runs:

- before: 18.77s under `cProfile`
- after: 7.69s under `cProfile`
- after: 7.24s direct wall-clock

Word-count direct/profiled runs:

- before: 29.70s under `cProfile`
- after: 15.18s under `cProfile`
- after: 9.22s direct wall-clock

Related-name pairs direct/profiled runs:

- before: 16.32s under `cProfile`
- after: 7.94s under `cProfile`
- after: 7.83s direct wall-clock

Fresh `surface_context_nt`:

- serial: 42.03s
- `--jobs 4`: 11.79s
- `--jobs 8`: 7.58s
- prior `--jobs 0`: 7.34s
- after chunked lanes/index arrays, `--jobs 0`: 5.36s direct
- after chunked lanes/index arrays, protocol run with `--jobs 0`: 4.99s
- `--jobs 1`: 41.94s before, 21.09s after
- after hybrid bulk AC path, `--jobs 1`: 17.09s direct
- after hybrid bulk AC path, `--jobs 0`: 4.82s direct
- after hybrid bulk AC path, protocol run with `--jobs 0`: 7.35s

Fresh `batch-many` across MT WLC, LXX, TR NT, and SBLGNT:

| Setting | Time |
| --- | ---: |
| `--jobs 1 --corpus-jobs 1` | 27.11s |
| `--jobs 2 --corpus-jobs 1` | 15.34s |
| `--jobs 4 --corpus-jobs 1` | 9.85s |
| `--jobs 6 --corpus-jobs 1` | 8.80s |
| `--jobs 0 --corpus-jobs 1` | 8.72s |

Corpus-level parallelism is intentionally not combined with per-corpus process workers. This avoids forking process pools from corpus worker threads. With serial per-corpus counting, corpus-level parallelism did not help locally:

| Setting | Time |
| --- | ---: |
| `--jobs 1 --corpus-jobs 1` | 26.46s |
| `--jobs 1 --corpus-jobs 2` | 27.18s |
| `--jobs 1 --corpus-jobs 4` | 27.14s |
