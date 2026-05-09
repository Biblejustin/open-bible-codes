# Modern Names And Dates

Purpose:

- Check whether modern transliterations such as Trump, Vance, Netanyahu, Europe, European Union, United Nations, Germany, France, Turkey, Russia, United States variants, and local terms appear as ELS terms.
- Check whether date encodings appear near those name ELS hits.

Term list:

- `terms/modern_names_dates.csv`

Commands:

```bash
python3 -m els batch \
  --terms terms/modern_names_dates.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --corpus LXX=configs/lxx_codex_bible.local.toml \
  --corpus TR_NT=configs/tr_codex_bible.local.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --min-skip 2 --max-skip 50 \
  --out reports/modern_names_dates_counts.csv \
  --manifest-out reports/modern_names_dates_counts.manifest.json

python3 -m els pairs \
  --terms terms/modern_names_dates.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --corpus LXX=configs/lxx_codex_bible.local.toml \
  --corpus TR_NT=configs/tr_codex_bible.local.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --left-category modern_names \
  --right-category dates \
  --min-skip 2 --max-skip 50 \
  --max-gap 500 \
  --out reports/modern_name_date_pairs.csv \
  --summary-out reports/modern_name_date_pairs_summary.csv \
  --manifest-out reports/modern_name_date_pairs.manifest.json
```

Date encoding:

- Jewish year shorthand: `5785` -> `תשפה`; this omits the 5000 by normal convention.
- Gregorian compact thousands: `2024` -> `בכד`; punctuation/thousands mark removed.
- Pure additive gematria: `2024` -> `תתתתתכד`; value is literally 2024 by letter totals.

Helper:

```bash
python3 -m els gematria-year 2024
```

Cautions:

- `2024`, `2025`, etc. do not exist as digits in normalized Bible streams.
- Date terms use explicit encodings. Hebrew year letters (`תשפה`) are cleaner than spelled-out Gregorian year words.
- Modern-name spellings are transliterations, not inspired spellings.
- Modern-place spellings mix direct country names, common acronyms, and modern Hebrew/Greek forms; short acronyms are noisy.
- Gog and Magog live in `terms/prophetic_terms.csv` and `terms/table_of_nations.csv`; they are not duplicated here as modern places.
- `local_terms` rows include pastor-business and church-location screening terms for false-positive sensitivity, not interpretive categories.
- Middle East, Asia, Vatican, and modern-event rows are transliteration screening terms and may collide with ordinary biblical words.
- Nearness in this first pass means closest center in one-dimensional letter stream, with span gap <= 500 letters.
- Pair rows now also export overlap, same-center-ref, same-center-chapter,
  same-signed-skip, same-absolute-skip, skip-distance, span-union, and
  compactness-score fields. `compactness_score = span_gap + center_distance`;
  lower is closer.
- Pass `--row-width` to add a WRR-style cylindrical table distance; see
  `docs/PAIR_COMPACTNESS.md`.
- Nearness does not imply statistical significance.

Run results:

Counts file:

- `reports/modern_names_dates_counts.csv`

Pair files:

- `reports/modern_name_date_pairs.csv`
- `reports/modern_name_date_pairs_summary.csv`

Focused name counts, skips 2 through 50:

| Term | MT_WLC | LXX | TR_NT | SBLGNT |
|---|---:|---:|---:|---:|
| Trump / `טראמפ` / `τραμπ` | 4 | 57 | 23 | 12 |
| Vance / `ואנס` / `βανς` | 331 | 1,338 | 252 | 259 |
| Vance alt / `ווענס` | 12 | n/a | n/a | n/a |
| Netanyahu / `נתניהו` / `νετανιαχου` | 8 | 0 | 0 | 0 |
| Iran / `איראן` / `ιραν` | 210 | 7,179 | 1,988 | 1,983 |
| Persia / `פרס` / `περσια` | 907 | 24 | 7 | 6 |

Hebrew date count summary:

| Date encoding | Term | MT_WLC hits |
|---|---|---:|
| 2026 compact | `בכו` | 26,640 |
| 2025 compact | `בכה` | 20,985 |
| 2024 compact | `בכד` | 6,818 |
| 2027 compact | `בכז` | 1,899 |
| 5786 Jewish-year shorthand | `תשפו` | 489 |
| 5785 Jewish-year shorthand | `תשפה` | 378 |
| 5784 Jewish-year shorthand | `תשפד` | 136 |
| 5787 Jewish-year shorthand | `תשפז` | 34 |
| 2025 additive full value | `תתתתתכה` | 1 |
| 2027 additive full value | `תתתתתכז` | 1 |
| 2024 additive full value | `תתתתתכד` | 0 |
| 2026 additive full value | `תתתתתכו` | 0 |

Focused name/date proximity, MT_WLC, max span gap 500:

| Pair | Best span gap | Best center distance | Notes |
|---|---:|---:|---|
| Trump ↔ 5786 / `תשפו` | 0 | 34.5 | Leviticus 14:11 region |
| Trump ↔ 5785 / `תשפה` | 0 | 59.0 | Deuteronomy 16:16-18 region |
| Netanyahu ↔ 5786 / `תשפו` | 176 | 288.0 | Ezekiel 10 region |
| Netanyahu ↔ 5785 / `תשפה` | 221 | 373.5 | nearest under current rule |
| Vance ↔ 5784 / `תשפד` | 0 | 0.5 | many overlaps; term/date are short |
| Vance ↔ 5785 / `תשפה` | 0 | 11.0 | many overlaps; term/date are short |
| Vance ↔ 5786 / `תשפו` | 0 | 4.0 | many overlaps; term/date are short |

Interpretive note:

- Short transliterations and compact year encodings produce many near hits.
- Compact Gregorian encodings (`בכו`, `בכה`) are especially frequent because they are only three letters.
- The additive full-value encodings are stricter but mostly absent.

Iran/Persia related-name checks:

| Corpus | Pair | Summary |
|---|---|---|
| MT_WLC | Iran + Gaza | 45 overlaps; 433 same-chapter; best gap 0 |
| MT_WLC | Persia + Gaza | 175 overlaps; 1,843 same-chapter; best gap 0 |
| MT_WLC | Israel + Iran | 12 overlaps; 41 same-chapter; best gap 0 |
| MT_WLC | Israel + Persia | 25 overlaps; 126 same-chapter; best gap 0 |
| MT_WLC | Hamas + Iran | 7 overlaps; 31 same-chapter; best gap 0 |
| MT_WLC | Hamas + Persia | 33 overlaps; 144 same-chapter; best gap 0 |
| MT_WLC | Trump + Iran | no overlap; 1 same-chapter; best gap 148 |
| MT_WLC | Trump + Persia | 1 overlap; 5 same-chapter; best gap 0 |
| MT_WLC | Netanyahu + Iran | no overlap; 1 same-chapter; best gap 318 |
| MT_WLC | Netanyahu + Persia | 1 overlap; 3 same-chapter; best gap 0 |
| LXX | Trump + Iran | 31 overlaps; 205 same-chapter; best gap 0 |
| TR_NT | Trump + Iran | 7 overlaps; 60 same-chapter; best gap 0 |
| SBLGNT | Trump + Iran | 5 overlaps; 34 same-chapter; best gap 0 |

Iran caveat:

- Greek `ιραν` is only four normalized letters and extremely common as an ELS pattern.
- Hebrew `פרס` / Persia is biblical and short, so it is very noisy.
- These are raw co-occurrence counts, not statistical controls.
