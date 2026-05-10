# Gog/Magog Pair Prospective Preregistration

Status: locked prospective design. No result-producing run is valid for this
study unless the lock manifest and preflight both pass before the run.

## Hypothesis

The Hebrew `גוג` (Gog; English: Gog) / `מגוג` (Magog; English: Magog) ELS pair may show compact same-chapter,
same-signed-skip proximity in MT-family Hebrew Bible sources beyond matched
pair controls.

This is a review-candidate hypothesis only. A successful run may produce the
label `prospective_controlled_review_candidate`; it may not produce claim,
proof, or prophecy-confirmation language.

## Sources

Only these sources are eligible:

- `MT_WLC`: `configs/example_oshb_wlc.toml`
- `UHB`: `configs/example_uhb.toml`

No Greek, English, LXX, NT, Apocrypha, or non-Bible control source is part of
this locked lane.

## Term File

Registered term file:

- `terms/gog_magog_pair_prospective_terms.csv`

Target pair:

- left: `gog_h` = `גוג` (Gog; English: Gog)
- right: `magog_h` = `מגוג` (Magog; English: Magog)

Declared pair baselines:

- `cyrus_h` / `darius_h`
- `beast_h` / `dragon_h`
- `horn_h` / `seal_h`
- `vision_h` / `prophet_h`

No additional terms may be added after outputs are inspected.

## Search Settings

- skip range: `2..100`
- direction: `both`
- minimum normalized length: `3`
- max pair gap: `500`
- pair filter: same chapter and same signed skip
- random seed: `20260509`
- term-control samples: `500`
- random-control samples: `50`
- synthetic null samples: `100` per corpus
- multiple-testing correction: Benjamini-Hochberg over registered pair-control
  rows

## Control Design

Target pair controls:

- term-shuffle controls preserve each target word's letter multiset;
- random controls preserve target word lengths and draw from the corpus letter
  distribution;
- the target is compared against both control families.

Declared pair baselines:

- the target pair is compared with the fixed non-target pair list in the same
  sources under the same strict pair filter.

Synthetic length-matched baselines:

- each source receives `100` sampled 3+4 Hebrew letter pairs;
- each sampled pair uses the same skip range, direction, gap, and strict pair
  filter as the target;
- synthetic results are compared with `Gog/Magog` and `Beast/Dragon`.

## Success Rule

A result can be called `prospective_controlled_review_candidate` only if:

- both target source rows are present;
- the target pair is compact under the same-chapter and same-signed-skip rule;
- paired controls do not explain the target compactness;
- declared pair baselines and synthetic length-matched baselines do not match
  or exceed the target density in a way that makes the target ordinary.

## Failure Rule

The study fails to produce a review candidate if:

- either source has no target row;
- control p-values or q-values are not favorable;
- declared or synthetic baselines show that similar short pairs are common;
- the only interesting feature is raw hit count.

All observed rows must still be reported, including weak, negative, or
frequency-cautioned rows.

## Output Paths

- `reports/gog_magog_pair_prospective/target_summary.csv`
- `reports/gog_magog_pair_prospective/target_examples.csv`
- `reports/gog_magog_pair_prospective/target.md`
- `reports/gog_magog_pair_prospective/target.manifest.json`
- `reports/gog_magog_pair_prospective/pair_baselines_summary.csv`
- `reports/gog_magog_pair_prospective/pair_baselines_examples.csv`
- `reports/gog_magog_pair_prospective/pair_baselines.md`
- `reports/gog_magog_pair_prospective/pair_baselines.manifest.json`
- `reports/gog_magog_pair_prospective/synthetic_mt_wlc_summary.csv`
- `reports/gog_magog_pair_prospective/synthetic_mt_wlc_comparison.csv`
- `reports/gog_magog_pair_prospective/synthetic_mt_wlc.md`
- `reports/gog_magog_pair_prospective/synthetic_mt_wlc.manifest.json`
- `reports/gog_magog_pair_prospective/synthetic_uhb_summary.csv`
- `reports/gog_magog_pair_prospective/synthetic_uhb_comparison.csv`
- `reports/gog_magog_pair_prospective/synthetic_uhb.md`
- `reports/gog_magog_pair_prospective/synthetic_uhb.manifest.json`
- `docs/GOG_MAGOG_PAIR_PROSPECTIVE_REPORT.md`

## Run Gate

The run is blocked until these pass:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name gog_magog_pair_prospective \
  --path docs/GOG_MAGOG_PAIR_PROSPECTIVE_PREREGISTRATION.md \
  --path terms/gog_magog_pair_prospective_terms.csv \
  --path protocols/gog_magog_pair_prospective.toml \
  --path scripts/analyze_gog_magog_pairs.py \
  --path scripts/analyze_pair_baselines.py \
  --path scripts/analyze_synthetic_pair_baselines.py \
  --path scripts/build_gog_magog_pair_prospective_report.py \
  --path configs/example_oshb_wlc.toml \
  --path configs/example_uhb.toml \
  --setting skip_range=2..100 \
  --setting direction=both \
  --setting min_normalized_length=3 \
  --setting controls=500_term_shuffle_50_random_100_synthetic_per_corpus \
  --setting correction=benjamini_hochberg \
  --setting source_set=MT_WLC,UHB \
  --setting pair_filter=same_chapter_same_signed_skip \
  --setting max_gap=500 \
  --setting seed=20260509 \
  --out reports/study_locks/gog_magog_pair_prospective.manifest.json
```

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/GOG_MAGOG_PAIR_PROSPECTIVE_PREREGISTRATION.md \
  --manifest reports/study_locks/gog_magog_pair_prospective.manifest.json \
  --protocol protocols/gog_magog_pair_prospective.toml \
  --out reports/study_locks/gog_magog_pair_prospective.preflight.json
```

Only after both commands pass may this run execute:

```bash
python3 -m scripts.run_protocol protocols/gog_magog_pair_prospective.toml --resume
```
