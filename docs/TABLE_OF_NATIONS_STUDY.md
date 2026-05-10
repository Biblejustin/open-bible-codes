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
- Skipped terms: 5 short Hebrew names under length 3: `נח` (Noach; English: Noah), `שם` (Shem; English: Shem), `חם` (Cham; English: Ham), `חת` (Chet; English: Heth), and `מש` (Mash; English: Mash).
- MT WLC total hits: 567,491.
- LXX total hits: 140,438.
- TR NT total hits: 44,307.
- SBLGNT total hits: 43,657.

Top MT WLC hits:

- Javan: `יון` (Yavan; English: Javan/Greece), 68,556.
- Aram: `ארם` (Aram; English: Aram), 44,295.
- Mesha: `משא` (Mesha; English: Mesha), 37,409.
- Hivite: `חוי` (Chivvi; English: Hivite), 34,677.
- Madai: `מדי` (Madai; English: Media), 30,544.

Top LXX hits:

- Noah: `νωε` (Noe; English: Noah), 49,559.
- Hul: `ουλ` (Oul; English: Hul), 33,797.
- Shem: `σημ` (Sem; English: Shem), 19,590.
- Shelah: `σαλα` (Sala; English: Shelah), 8,046.
- Ham: `χαμ` (Cham; English: Ham), 4,680.

Longer-name MT WLC leaders:

- Lehabim: `להבים` (Lehabim; English: Lehabim), 373.
- Nineveh: `נינוה` (Nineveh; English: Nineveh), 281.
- Elishah: `אלישה` (Elishah; English: Elishah), 276.
- Ludim: `לודים` (Ludim; English: Ludim), 270.
- Havilah: `חוילה` (Havilah; English: Havilah), 200.

Longer-name LXX leaders:

- Elishah: `ελισα` (Elisa; English: Elishah), 489.
- Javan: `ιωυαν` (Iouan; English: Javan), 431.
- Havilah: `ευιλα` (Euila; English: Havilah), 408.
- Admah: `αδαμα` (Adama; English: Admah), 204.
- Mesha: `μασση` (Masse; English: Mesha), 184.

Cautions:

- Raw ELS counts only.
- Many names are short or common roots, so they create noise.
- Some Genesis 10 names are ordinary biblical names/place names elsewhere.
- LXX differs from MT in some names, including Cainan and Rodians.
- Skip 1 is excluded, so ordinary Genesis 10 surface occurrences are not counted in this report.
