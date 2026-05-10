# Prophetic Terms Study

Term list:

- `terms/prophetic_terms.csv`

Scope:

- Biblical empires and places often used in prophetic interpretation.
- Rulers and figures such as Cyrus, Darius, Nebuchadnezzar, Gog, Magog, biblical kings, prophets, apostles, and NT-era figures.
- Apocalyptic symbols and judgment terms such as beast, dragon, horn, mark, seal, trumpet, throne, scroll, sevenfold Revelation motifs, abomination, desolation, wrath, famine, war, sword, plagues, earthquake, fire, blood, darkness, and smoke.
- Revelation and prophecy title phrases such as Alpha and Omega, I Am, New Jerusalem, Tree of Life, Lake of Fire, and Second Death.
- Exodus plague terms, Revelation figures, and liturgical/apocalyptic phrases are included for coverage.
- Hebrew and Greek rows are separate.
- Alternate spellings are explicit rows when they represent different declared forms.
- The expanded list has not been rerun yet.

Command:

```bash
python3 -m els batch \
  --terms terms/prophetic_terms.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --corpus LXX=configs/example_ebible_grclxx.toml \
  --corpus TR_NT=configs/example_ebible_grctr.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --min-skip 2 --max-skip 50 \
  --min-term-length 3 \
  --out reports/prophetic_terms_counts.csv \
  --manifest-out reports/prophetic_terms_counts.manifest.json
```

Outputs:

- `reports/prophetic_terms_counts.csv`
- `reports/prophetic_terms_counts.manifest.json`

Prior public baseline result before expanded additions:

- Rows: 174 result rows.
- Counted terms: 170.
- Skipped terms: 4 short terms under length 3.
- MT WLC total hits: 278,440.
- LXX total hits: 12,108.
- TR NT total hits: 3,221.
- SBLGNT total hits: 3,267.

Top MT WLC hits:

- Greece: `יון` (Yavan; English: Javan/Greece), 68,556.
- Lawlessness: `און` (aven; English: lawlessness/iniquity), 45,249.
- Media: `מדי` (Madai; English: Media), 30,544.
- Babylon: `בבל` (Bavel; English: Babylon), 26,849.
- Beast: `חיה` (chayah; English: beast/living creature), 25,639.

Top Greek hits:

- LXX: Zion `σιων` (Sion; English: Zion) 5,083; Elam `ελαμ` (Elam; English: Elam) 1,946; Gog `γωγ` (Gog; English: Gog) 1,800.
- TR NT: Zion `σιων` (Sion; English: Zion) 1,289; Gog `γωγ` (Gog; English: Gog) 594; Elam `ελαμ` (Elam; English: Elam) 555.
- SBLGNT: Zion `σιων` (Sion; English: Zion) 1,292; Elam `ελαμ` (Elam; English: Elam) 603; Gog `γωγ` (Gog; English: Gog) 572.

Cautions:

- This list is a declared screening list, not an interpretation.
- Short terms such as `תו` (tav; English: mark/sign), `עד` (ed; English: witness), and `צר` (tsar; English: foe/adversary) are intentionally present for audit but skipped by default count settings.
- Some terms overlap with the theological and Table-of-Nations lists; overlap is useful for sensitivity checks but raw counts should not be double-read as independent evidence.
