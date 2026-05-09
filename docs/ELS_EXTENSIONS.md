# ELS Extensions

Purpose:

- Check letters immediately before and after an ELS hit on the same signed skip lane.
- Compare those added letters against any normalized surface word or short phrase in the same corpus.
- Flag possible compound words or phrase extensions without predeclaring every possible adjacent term.

Command:

```bash
python3 -m els extensions \
  --config configs/example_oshb_wlc.toml \
  --hits reports/search_hits.csv \
  --max-before 12 \
  --max-after 12 \
  --phrase-words 4 \
  --out reports/search_hit_extensions.csv \
  --manifest-out reports/search_hit_extensions.manifest.json
```

For multi-corpus term CSV workflows, first produce a labeled hit file with
`surface-context --include-all`, then run `extensions` once per corpus label:

```bash
python3 -m els surface-context \
  --terms terms/modern_names_dates.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --min-skip 2 --max-skip 100 \
  --max-hits-per-term 25 \
  --include-all \
  --out reports/modern_extension_screen/surface_context_hits.csv

python3 -m els extensions \
  --config configs/example_sblgnt.toml \
  --hits reports/modern_extension_screen/surface_context_hits.csv \
  --corpus-label SBLGNT \
  --include-both-sided \
  --out reports/modern_extension_screen/extensions_sblgnt.csv
```

Repeatable modern-term screen:

```bash
python3 -m scripts.run_protocol protocols/modern_focus_extensions.toml --resume
```

Optional:

```bash
python3 -m els extensions \
  --config configs/example_oshb_wlc.toml \
  --hits reports/search_hits.csv \
  --include-both-sided \
  --max-extensions-per-hit 20 \
  --out reports/search_hit_extensions.csv
```

Summary:

```bash
python3 -m els extension-summary \
  --extensions reports/search_hit_extensions.csv \
  --min-extension-length 3 \
  --min-term-length 4 \
  --match-kind-prefix phrase_ \
  --exclude-term ουλ \
  --top 100 \
  --out reports/search_hit_extensions_summary.csv \
  --top-out reports/search_hit_extensions_top.csv \
  --manifest-out reports/search_hit_extensions_summary.manifest.json
```

Output:

- Original hit fields.
- Same-skip extension type: before match, after match, before plus term, term plus after, or both-sided.
- Added before/after letters.
- Extended normalized sequence.
- Matched word or phrase examples from the corpus.
- Extension start/end offsets and refs.

Summary output:

- Grouped counts by corpus, term, skip, direction, extension type, side, and match kind.
- Unique extended sequence counts per group.
- Maximum extension length and maximum surface match count per group.
- Optional top file with strongest compound extension rows.
- Default `--min-extension-length 2` removes noisy one-letter extensions.
- Optional `--min-term-length`, `--match-kind-prefix`, and `--exclude-term` reduce short-term noise before ranking.

Review:

- See `docs/EXTENSION_TOP_HITS_REVIEW.md` for a first-pass review of the TR NT and SBLGNT protocol top rows.

Cautions:

- Backward hits extend in backward ELS order.
- The lexicon is surface-text derived from the same corpus, not a dictionary.
- Phrase matching removes spaces because the ELS stream removes spaces.
- This is a screening aid, not evidence of significance by itself.
