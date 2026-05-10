# Common Bible Codes / ELS Test

Run date: 2026-05-03

Source used for this check:

- Koren Torah files from Brendan McKay's data page.
- Format: Michigan-Claremont Hebrew transliteration.
- Raw files kept under `data/raw/koren/`, ignored by git.

Commands:

```bash
python3 -m unittest discover -s tests
python3 -m els stats --config configs/example_michigan_torah.toml
python3 -m els search --config configs/example_michigan_torah.toml --term תורה --min-skip 50 --max-skip 50 --out reports/torah_skip50.csv
python3 -m els search --config configs/example_michigan_torah.toml --term HRWT --min-skip 50 --max-skip 50 --direction forward --out reports/hrwt_forward50.csv
python3 -m els search --config configs/example_michigan_torah.toml --term HRWT --min-skip 49 --max-skip 49 --direction forward --out reports/hrwt_forward49.csv
python3 -m els search --config configs/example_michigan_torah.toml --term יהוה --min-skip 8 --max-skip 8 --direction forward --out reports/yhwh_skip8.csv
python3 -m els matrix --config configs/example_michigan_torah.toml --hits reports/torah_skip50.csv --out reports/torah_skip50_matrix_letters.csv --summary-out reports/torah_skip50_matrix_summary.csv
```

Corpus:

| Book | Letters |
|---|---:|
| Genesis | 78,064 |
| Exodus | 63,529 |
| Leviticus | 44,790 |
| Numbers | 63,530 |
| Deuteronomy | 54,892 |
| Total | 304,805 |

Common pattern check:

| Claim | Found | Book letters | Refs | Hits in book |
|---|---:|---|---|---:|
| Genesis `תורה` (Torah; English: Torah) / `TWRH`, skip +50 | yes | 6 -> 156 | Genesis 1:1 -> Genesis 1:5 | 3 |
| Exodus `תורה` (Torah; English: Torah) / `TWRH`, skip +50 | yes | 8 -> 158 | Exodus 1:1 -> Exodus 1:6 | 7 |
| Leviticus `יהוה` (YHWH; English: YHWH) / `YHWH`, skip +8 | yes | 2 -> 26 | Leviticus 1:1 -> Leviticus 1:1 | 7 |
| Numbers reverse `תורה` (Torah; English: Torah) / `HRWT`, skip +50 | yes | 14 -> 164 | Numbers 1:1 -> Numbers 1:3 | 3 |
| Deuteronomy reverse `תורה` (Torah; English: Torah) / `HRWT`, skip +49 | yes | 279 -> 426 | Deuteronomy 1:5 -> Deuteronomy 1:8 | 2 |

Small count-only shuffled control, 200 shuffles:

| Term/skip | Observed | Shuffle avg | Shuffle range | p >= observed |
|---|---:|---:|---|---:|
| `TWRH`, +/-50 | 32 | 19.68 | 9-34 | 0.010 |
| `HRWT`, +50 | 13 | 9.80 | 1-18 | 0.184 |
| `HRWT`, +49 | 4 | 10.43 | 2-18 | 0.995 |
| `YHWH`, +8 | 36 | 27.09 | 14-43 | 0.075 |

Notes:

- These controls only compare total hit counts after letter shuffling.
- They do not test the stronger book-start placement claim.
- Reports are ignored by git because generated reports can contain source-derived text.

Matrix audit:

- `reports/torah_skip50_matrix_summary.csv` currently has 32 hit-summary rows.
- `reports/torah_skip50_matrix_letters.csv` currently has 128 letter-path rows.
- The first Genesis `TWRH` hit at skip `+50` occupies one column when wrapped
  at row width `50`: rows `0..3`, column `5`, centered on `Genesis 1:3`.

Greek sanity check:

```bash
python3 -m els search --config configs/greek_codex_bible.local.toml --term Ιησους --min-skip 2 --max-skip 50 --out reports/greek_iesous_skip2_50.csv
```

Result: 46 hits over the local LXX+TR Greek stream. This is only an engine check, not a commonly standardized Greek ELS claim.
