# Word-Skip Term Audit

Opt-in full normalized surface-word token audit over declared Hebrew phrases.

This is not an ordinary letter-ELS path search. Each pattern consumes
full normalized surface-word tokens at a declared word interval. It
widens the review surface and needs matched controls before claim language.

## Bottom Line

- hit rows: 3,235
- summarized rows: 27
- corpora with hits: 8
- terms with hits: 4

## Summary Rows

| Pattern | Corpus | Term | Hits | Capped | F/B | Word skip | Center refs sample |
| --- | --- | --- | ---: | --- | ---: | --- | --- |
| `word_skip_ELS` | `EBIBLE_WLC` | `בני ישראל` (bnyyshrl; English: Children Israel) | 200 | `yes` | 200/0 | 1-1 | 1CH 2:1;1KI 14:24;1KI 19:10;1KI 19:14;1KI 21:26;1KI 6:13;1KI 9:21;1SA 17:53;1SA 2:28;1SA 7:4 |
| `word_skip_ELS` | `EBIBLE_WLC` | `יהוה אמר` (yhwhmr; English: YHWH Said) | 200 | `no` | 73/127 | 1-5 | 1CH 17:4;1CH 17:7;1CH 21:10;1CH 21:18;1CH 27:23;1KI 11:31;1KI 12:24;1KI 13:2;1KI 13:21;1KI 17:14 |
| `word_skip_ELS` | `EBIBLE_WLC` | `מלכ ישראל` (mlkyshrl; English: King Israel) | 88 | `no` | 58/30 | 1-5 | 1KI 14:19;1KI 15:9;1KI 20:20;1KI 20:21;1KI 20:41;1KI 22:26;1KI 22:30;1KI 22:41;1KI 22:9;1SA 24:15 |
| `word_skip_ELS` | `EBIBLE_WLC` | `ארצ מצרימ` (rtsmtsrym; English: Land Egypt) | 13 | `no` | 9/4 | 1-4 | 1KI 5:1;EZK 20:36;EZK 20:8;EZK 29:14;EZK 32:15;GEN 45:18;GEN 47:13;GEN 47:6;ISA 19:19;JER 42:14 |
| `word_skip_ELS` | `HEB_AHAD_HAAM` | `בני ישראל` (bnyyshrl; English: Children Israel) | 81 | `no` | 73/8 | 1-5 | PBY Ahad Ha'am |
| `word_skip_ELS` | `HEB_AHAD_HAAM` | `מלכ ישראל` (mlkyshrl; English: King Israel) | 3 | `no` | 1/2 | 1-5 | PBY Ahad Ha'am |
| `word_skip_ELS` | `HEB_BIALIK` | `בני ישראל` (bnyyshrl; English: Children Israel) | 120 | `no` | 98/22 | 1-5 | PBY Bialik |
| `word_skip_ELS` | `HEB_BIALIK` | `מלכ ישראל` (mlkyshrl; English: King Israel) | 54 | `no` | 45/9 | 1-5 | PBY Bialik |
| `word_skip_ELS` | `HEB_BIALIK` | `ארצ מצרימ` (rtsmtsrym; English: Land Egypt) | 14 | `no` | 13/1 | 1-2 | PBY Bialik |
| `word_skip_ELS` | `HEB_BRENNER` | `בני ישראל` (bnyyshrl; English: Children Israel) | 96 | `no` | 91/5 | 1-5 | PBY Brenner |
| `word_skip_ELS` | `HEB_BRENNER` | `מלכ ישראל` (mlkyshrl; English: King Israel) | 2 | `no` | 2/0 | 1-2 | PBY Brenner |
| `word_skip_ELS` | `MAM` | `בני ישראל` (bnyyshrl; English: Children Israel) | 200 | `yes` | 200/0 | 1-1 | 1 Chr 2:1;1 Kgs 14:24;1 Kgs 19:10;1 Kgs 19:14;1 Kgs 21:26;1 Kgs 6:13;1 Kgs 9:21;1 Sam 17:53;1 Sam 2:28;1 Sam 7:4 |
| `word_skip_ELS` | `MAM` | `יהוה אמר` (yhwhmr; English: YHWH Said) | 200 | `no` | 71/129 | 1-5 | 1 Chr 21:18;1 Kgs 11:31;1 Kgs 12:24;1 Kgs 13:2;1 Kgs 13:21;1 Kgs 17:14;1 Kgs 20:13;1 Kgs 20:42;1 Kgs 21:19;1 Kgs 8:11 |
| `word_skip_ELS` | `MAM` | `מלכ ישראל` (mlkyshrl; English: King Israel) | 88 | `no` | 58/30 | 1-5 | 1 Kgs 14:19;1 Kgs 15:9;1 Kgs 20:20;1 Kgs 20:21;1 Kgs 20:41;1 Kgs 22:26;1 Kgs 22:30;1 Kgs 22:41;1 Kgs 22:9;1 Sam 24:14 |
| `word_skip_ELS` | `MAM` | `ארצ מצרימ` (rtsmtsrym; English: Land Egypt) | 13 | `no` | 9/4 | 1-4 | 1 Kgs 5:1;Ezek 20:36;Ezek 20:8;Ezek 29:14;Ezek 32:15;Gen 45:18;Gen 47:13;Gen 47:6;Isa 19:19;Jer 42:14 |
| `word_skip_ELS` | `MT_WLC` | `בני ישראל` (bnyyshrl; English: Children Israel) | 200 | `yes` | 200/0 | 1-1 | Exod 10:20;Exod 10:23;Exod 11:10;Exod 11:7;Exod 12:27;Exod 12:28;Exod 12:31;Exod 12:37;Exod 12:40;Exod 12:42 |
| `word_skip_ELS` | `MT_WLC` | `מלכ ישראל` (mlkyshrl; English: King Israel) | 200 | `no` | 186/14 | 1-5 | 1Chr 11:2;1Chr 1:43;1Chr 29:25;1Chr 29:26;1Chr 29:27;1Chr 5:17;1Kgs 11:37;1Kgs 11:42;1Kgs 14:14;1Kgs 15:16 |
| `word_skip_ELS` | `MT_WLC` | `יהוה אמר` (yhwhmr; English: YHWH Said) | 200 | `no` | 131/69 | 1-5 | 1Chr 21:18;1Kgs 11:2;1Kgs 11:31;1Kgs 12:24;1Kgs 13:2;1Kgs 13:21;1Kgs 14:7;1Kgs 17:14;1Kgs 20:13;1Kgs 20:14 |
| `word_skip_ELS` | `MT_WLC` | `ארצ מצרימ` (rtsmtsrym; English: Land Egypt) | 81 | `no` | 69/12 | 1-5 | 1Kgs 5:1;1Sam 27:8;2Chr 9:26;Exod 10:12;Exod 10:13;Exod 10:14;Exod 10:15;Exod 10:21;Exod 10:22;Exod 11:6 |
| `word_skip_ELS` | `UHB` | `בני ישראל` (bnyyshrl; English: Children Israel) | 200 | `yes` | 200/0 | 1-1 | 1CH 2:1;1KI 14:24;1KI 19:10;1KI 19:14;1KI 21:26;1KI 6:13;1KI 9:21;1SA 17:53;1SA 2:28;1SA 7:4 |
| `word_skip_ELS` | `UHB` | `יהוה אמר` (yhwhmr; English: YHWH Said) | 200 | `no` | 73/127 | 1-5 | 1CH 17:4;1CH 17:7;1CH 21:10;1CH 21:18;1CH 27:23;1KI 11:31;1KI 12:24;1KI 13:2;1KI 13:21;1KI 17:14 |
| `word_skip_ELS` | `UHB` | `מלכ ישראל` (mlkyshrl; English: King Israel) | 88 | `no` | 58/30 | 1-5 | 1KI 14:19;1KI 15:9;1KI 20:20;1KI 20:21;1KI 20:41;1KI 22:26;1KI 22:30;1KI 22:41;1KI 22:9;1SA 24:14 |
| `word_skip_ELS` | `UHB` | `ארצ מצרימ` (rtsmtsrym; English: Land Egypt) | 13 | `no` | 9/4 | 1-4 | 1KI 4:21;EZK 20:36;EZK 20:8;EZK 29:14;EZK 32:15;GEN 45:18;GEN 47:13;GEN 47:6;ISA 19:19;JER 42:14 |
| `word_skip_ELS` | `UXLC` | `בני ישראל` (bnyyshrl; English: Children Israel) | 200 | `yes` | 200/0 | 1-1 | Ex 10:20;Ex 10:23;Ex 11:10;Ex 11:7;Ex 12:27;Ex 12:28;Ex 12:31;Ex 12:37;Ex 12:40;Ex 12:42 |
| `word_skip_ELS` | `UXLC` | `מלכ ישראל` (mlkyshrl; English: King Israel) | 200 | `no` | 186/14 | 1-5 | 1 Chr 11:2;1 Chr 1:43;1 Chr 29:25;1 Chr 29:26;1 Chr 29:27;1 Chr 5:17;1 Kings 11:37;1 Kings 11:42;1 Kings 14:14;1 Kings 15:16 |
| `word_skip_ELS` | `UXLC` | `יהוה אמר` (yhwhmr; English: YHWH Said) | 200 | `no` | 131/69 | 1-5 | 1 Chr 21:18;1 Kings 11:2;1 Kings 11:31;1 Kings 12:24;1 Kings 13:2;1 Kings 13:21;1 Kings 14:7;1 Kings 17:14;1 Kings 20:13;1 Kings 20:14 |
| `word_skip_ELS` | `UXLC` | `ארצ מצרימ` (rtsmtsrym; English: Land Egypt) | 81 | `no` | 69/12 | 1-5 | 1 Kings 5:1;1 Sam 27:8;2 Chr 9:26;Ex 10:12;Ex 10:13;Ex 10:14;Ex 10:15;Ex 10:21;Ex 10:22;Ex 11:6 |

## Read

- Acrostic means first letters of normalized words.
- Telestic means last letters of normalized words.
- `word_skip_ELS` means full normalized surface-word tokens, not first/last letters.
- Word skip is the interval between consumed surface words. Consecutive-word rows have word skip 1.
- Backward means the consumed word-edge or word-token sequence reads the target term in reverse.
- `Capped=yes` means `hits` may be a floor because at least one direction reached its per-term limit.

