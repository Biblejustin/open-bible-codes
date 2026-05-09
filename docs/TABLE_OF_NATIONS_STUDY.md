# Table Of Nations Study

Term list:

- `terms/table_of_nations.csv`

Scope:

- Names and places from Genesis 10.
- Hebrew names use MT spellings from OSHB WLC.
- Greek names use local LXX spellings from Genesis 10 where possible.
- Two-letter names are kept in the term file but skipped in default count runs.

Command:

```bash
python3 -m els batch \
  --terms terms/table_of_nations.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --corpus LXX=configs/lxx_codex_bible.local.toml \
  --corpus TR_NT=configs/tr_codex_bible.local.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --min-skip 2 --max-skip 50 \
  --min-term-length 3 \
  --out reports/table_of_nations_counts.csv \
  --manifest-out reports/table_of_nations_counts.manifest.json
```

Output:

- `reports/table_of_nations_counts.csv`
- `reports/table_of_nations_counts.manifest.json`

Results:

- Rows: 364 result rows.
- Counted terms: 359.
- Skipped terms: 5 short Hebrew names under length 3 (`נח`, `שם`, `חם`, `חת`, `מש`).
- MT WLC total hits: 567,491.
- LXX total hits: 140,438.
- TR NT total hits: 44,307.
- SBLGNT total hits: 43,657.

Top MT WLC hits:

- Javan (`יון`): 68,556.
- Aram (`ארם`): 44,295.
- Mesha (`משא`): 37,409.
- Hivite (`חוי`): 34,677.
- Madai (`מדי`): 30,544.

Top LXX hits:

- Noah (`νωε`): 49,559.
- Hul (`ουλ`): 33,797.
- Shem (`σημ`): 19,590.
- Shelah (`σαλα`): 8,046.
- Ham (`χαμ`): 4,680.

Longer-name MT WLC leaders:

- Lehabim (`להבים`): 373.
- Nineveh (`נינוה`): 281.
- Elishah (`אלישה`): 276.
- Ludim (`לודים`): 270.
- Havilah (`חוילה`): 200.

Longer-name LXX leaders:

- Elishah (`ελισα`): 489.
- Javan (`ιωυαν`): 431.
- Havilah (`ευιλα`): 408.
- Admah (`αδαμα`): 204.
- Mesha (`μασση`): 184.

Cautions:

- Raw ELS counts only.
- Many names are short or common roots, so they create noise.
- Some Genesis 10 names are ordinary biblical names/place names elsewhere.
- LXX differs from MT in some names, including Cainan and Rodians.
- Skip 1 is excluded, so ordinary Genesis 10 surface occurrences are not counted in this report.
