# Synthetic Extension Match Review

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `synthetic_extension_match_review`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only synthetic_extension_match_review`
- Generated summary: `reports/synthetic_extension_match_review_summary.csv`
- Generated markdown: `reports/synthetic_extension_match_review.md`
- Generated manifest: `reports/synthetic_extension_match_review.manifest.json`
- Output size: 3 review rows
- Runtime observed: 0.515s through the protocol runner

This reviews the synthetic extension control rows that matched or exceeded target any-type extension scores.

## Main Read

All 3 synthetic match rows are ELS-only at the hit span. The matched phrase exists elsewhere in the corpus, not as surface text in the synthetic hit/extension passage.

| Corpus | Target | Synthetic | Center | Surface checks | Matched phrase |
| --- | --- | --- | --- | --- | --- |
| SBLGNT | `υιος` (huios; English: son) / `ουουιοσ` (ouhuios; English: hidden extension form from huios) | `ασατ` (asat; English: synthetic query) / `πασατου` (pasatou; English: synthetic extension) | Acts 23:34 `ἐπερωτήσας` (eperotesas; English: having questioned) | center query=no; hit query=no; extension phrase=no | `πᾶσα⸃ τοῦ` (pasa tou; English: all/every of the) at Acts 27:20 |
| SBLGNT | `υιος` (huios; English: son) / `ουουιοσ` (ouhuios; English: hidden extension form from huios) | `οθει` (othei; English: synthetic query) / `τοθειον` (totheion; English: synthetic extension) | Acts 22:27 `χιλίαρχος` (chiliarchos; English: commander) | center query=no; hit query=no; extension phrase=no | `τὸ θεῖον` (to theion; English: the divine) at Acts 17:29 |
| TR_NT | `δοξα` (doxa; English: glory) / `δοξανωσ` (doxanos; English: hidden extension form from doxa) | `τινα` (tina; English: someone/something) / `απαρτιναι` (apartinai; English: synthetic extension) | LUK 1:74 `ἀφόβως` (aphobos; English: without fear) | center query=no; hit query=no; extension phrase=no | `ἀπ ἄρτι Ναὶ` (ap arti nai; English: from now, yes) at REV 14:13 |

## Verdict

The synthetic matches explain why broad any-type synthetic scoring can compete with target rows. They do not weaken the exact same-type result directly, but they do show that same-skip phrase-extension scoring can generate convincing-looking hidden phrases from random strings.

## Caution

This is a control review, not a claim review. The synthetic rows are intentionally meaningless strings. Their value is showing baseline behavior for the scoring method.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only synthetic_extension_match_review
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
