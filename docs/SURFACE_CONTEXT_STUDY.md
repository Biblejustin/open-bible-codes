# Surface Context Study

Question:

- Which ELS hits have surface text context near the hit?
- Does the key term appear in the center verse?
- Does the key term appear between the hit start and end refs?
- Do same-concept or same-category terms appear in those places?

Command:

```bash
python3 -m els surface-context \
  --terms terms/theological_terms.csv \
  --terms terms/modern_names_dates.csv \
  --terms terms/table_of_nations.csv \
  --terms terms/prophetic_terms.csv \
  --corpus TR_NT=configs/tr_codex_bible.local.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --min-skip 2 --max-skip 50 \
  --out reports/surface_context_hits.csv \
  --summary-out reports/surface_context_summary.csv \
  --manifest-out reports/surface_context.manifest.json
```

Outputs:

- `reports/surface_context_hits.csv`
- `reports/surface_context_summary.csv`
- `reports/surface_context.manifest.json`
- `reports/surface_context_exact_hits.csv`
- `reports/surface_context_center_exact_hits.csv`

Definitions:

- `center_exact`: ELS key term appears as normal surface text in center verse.
- `span_exact`: ELS key term appears as normal surface text in any verse between start and end refs.
- `center_same_concept`: another term-list row with same concept appears in center verse.
- `span_same_concept`: another same-concept term appears between start and end refs.
- `center_same_category`: another term in same category appears in center verse.
- `span_same_category`: another term in same category appears between start and end refs.

Greek NT Results With Prophetic Terms:

- Corpora: TR NT and SBLGNT.
- Term rows: theology, modern names/dates, Table of Nations, prophetic terms.
- Skip range: 2..50, both directions.
- Contextual hit rows: 26,474.
- Exact-key contextual hits: 6,616.
- Exact-key center-verse hits: 4,644.

By Corpus:

- TR contextual hits: 13,310.
- SBLGNT contextual hits: 13,164.
- TR center exact: 2,329.
- SBLGNT center exact: 2,315.

Top Exact-Center Terms:

- Hul (`ουλ` [Oul; English: Hul]): TR 1,091; SBLGNT 1,059.
- Shem (`σημ` [Sem; English: Shem]): TR 648; SBLGNT 614.
- Noah (`νωε` [Noe; English: Noah]): TR 188; SBLGNT 154.
- Blood (`αιμα` [haima; English: blood]): TR 109; SBLGNT 99.
- Son (`υιοσ` [huios; English: son]): TR 103; SBLGNT 77.
- God (`θεοσ` [theos; English: God]): TR 49; SBLGNT 46.
- Gog (`γωγ` [Gog; English: Gog]): TR 22; SBLGNT 26.

Cautions:

- Same-category is broad and noisy.
- Exact center/span are cleaner first-pass filters.
- This is lexical context, not semantic interpretation.
- No statistical significance test yet.
