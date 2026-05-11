# External Claim Source Findings

Concise findings layer over the external-source count baseline and relaxed
all-codes collection. This document does not reproduce any outside claim;
it states what the current shared pipeline detected and how Bible rows
compare with language-matched secular controls.

## Inputs

- Counts summary: `reports/external_claim_source_counts/summary.csv`
- All-codes summary: `reports/external_claim_source_all_codes/surface_all_codes_summary.csv`
- Triage queue: `reports/external_claim_source_all_codes/triage_queue.csv`

## Main Read

- External-source terms do produce many hidden paths under skip 2..100.
- Bible and secular-control corpora both produce high-volume rows, especially for short/common forms.
- Same center-word rows exist and should be reviewed as occurrences.
- Claim-grade reproduction still requires source-specific geometry and locked controls.

## Bible Vs Control Summary

| Class | Corpora | Terms | Summary rows | Hidden hits | Context hits | Center word same | Center word related |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bible | 12 | 513 | 2,169 | 2,756,328 | 1,427,353 | 12,009 | 61,307 |
| Controls | 9 | 513 | 1,539 | 5,687,447 | 5,687,385 | 2,034 | 70,273 |

## Top Bible Center-Word Exact Terms

| Rank | Term | Corpora | Center-word same hits | Hidden hits |
| ---: | --- | --- | ---: | ---: |
| 1 | bns_esther_yhwh_h `יהוה` (YHWH; English: YHWH Esther Acrostic) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 3,329 | 108,320 |
| 2 | cc_yhwh_h `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 3,329 | 108,320 |
| 3 | twn_yhwh_h `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 3,329 | 108,320 |
| 4 | bco_thin_e `thin` | KJV, KJVA | 290 | 48,263 |
| 5 | cc_levites_h `לוימ` (lwym; English: Levites) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 186 | 90,647 |
| 6 | mt_levites_h `לוימ` (lwym; English: Levites) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 186 | 90,647 |
| 7 | twn_levites_h `לוימ` (lwym; English: Levites) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 186 | 90,647 |
| 8 | bcd_saul_h `שאול` (shwl; English: Saul) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 137 | 37,020 |
| 9 | cc_elohim_h `אלהימ` (lhym; English: Elohim) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 121 | 5,286 |
| 10 | cc_israel_h `ישראל` (Yisrael; English: Israel) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 83 | 2,104 |
| 11 | twn_israel_h `ישראל` (Yisrael; English: Israel) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 83 | 2,104 |
| 12 | cc_for_my_sons_h `לבני` (lbny; English: For My Sons) | EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC | 78 | 25,530 |

## Top Control Center-Word Exact Terms

| Rank | Term | Corpora | Center-word same hits | Hidden hits |
| ---: | --- | --- | ---: | ---: |
| 1 | bco_thin_e `thin` | ENG_MOBY_DICK, ENG_SHAKESPEARE, ENG_WAR_AND_PEACE | 303 | 38,881 |
| 2 | cc_mary_h `מרימ` (mrym; English: Mary) | HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER | 206 | 113,480 |
| 3 | mt_mary_h `מרימ` (mrym; English: Mary) | HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER | 206 | 113,480 |
| 4 | twn_mary_h `מרימ` (mrym; English: Mary) | HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER | 206 | 113,480 |
| 5 | cc_torah_h `תורה` (twrh; English: Torah) | HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER | 108 | 75,823 |
| 6 | twn_torah_h `תורה` (twrh; English: Torah) | HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER | 108 | 75,823 |
| 7 | bco_rent_e `rent` | ENG_MOBY_DICK, ENG_SHAKESPEARE, ENG_WAR_AND_PEACE | 71 | 65,066 |
| 8 | cc_israel_h `ישראל` (Yisrael; English: Israel) | HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER | 54 | 3,473 |
| 9 | twn_israel_h `ישראל` (Yisrael; English: Israel) | HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER | 54 | 3,473 |
| 10 | cc_jonah_h `יונה` (ywnh; English: Jonah) | HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER | 38 | 142,099 |
| 11 | mt_jonah_h `יונה` (ywnh; English: Jonah) | HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER | 38 | 142,099 |
| 12 | twn_louis_h `לואי` (lwy; English: Louis) | HEB_AHAD_HAAM, HEB_BIALIK, HEB_BRENNER | 37 | 157,461 |

## Top Bible Triage Rows

| Rank | Bucket | Scope | Term | Center | Present corpora |
| ---: | --- | --- | --- | --- | --- |
| 1 | `center_word_exact` | `multi_source` | cc_evil_fire_h `אשרע` (shr; English: Evil Fire) | 2Chr 3:15 `אשרעלראשו` (shrlrshw) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 2 | `center_word_exact` | `multi_source` | bns_esther_yhwh_h `יהוה` (YHWH; English: YHWH Esther Acrostic) | 1Chr 26:27 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 3 | `center_word_exact` | `multi_source` | cc_yhwh_h `יהוה` (YHWH; English: YHWH) | 1Chr 26:27 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 4 | `center_word_exact` | `multi_source` | twn_yhwh_h `יהוה` (YHWH; English: YHWH) | 1Chr 26:27 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 5 | `center_word_exact` | `multi_source` | bns_esther_yhwh_h `יהוה` (YHWH; English: YHWH Esther Acrostic) | 1Chr 28:20 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 6 | `center_word_exact` | `multi_source` | cc_yhwh_h `יהוה` (YHWH; English: YHWH) | 1Chr 28:20 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 7 | `center_word_exact` | `multi_source` | twn_yhwh_h `יהוה` (YHWH; English: YHWH) | 1Chr 28:20 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 8 | `center_word_exact` | `multi_source` | bns_esther_yhwh_h `יהוה` (YHWH; English: YHWH Esther Acrostic) | 1Kgs 10:5 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 9 | `center_word_exact` | `multi_source` | cc_yhwh_h `יהוה` (YHWH; English: YHWH) | 1Kgs 10:5 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 10 | `center_word_exact` | `multi_source` | twn_yhwh_h `יהוה` (YHWH; English: YHWH) | 1Kgs 10:5 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 11 | `center_word_exact` | `multi_source` | bns_esther_yhwh_h `יהוה` (YHWH; English: YHWH Esther Acrostic) | 1Sam 26:11 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |
| 12 | `center_word_exact` | `multi_source` | cc_yhwh_h `יהוה` (YHWH; English: YHWH) | 1Sam 26:11 `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC |

## Top Control Triage Rows

| Rank | Bucket | Scope | Term | Center | Present corpora |
| ---: | --- | --- | --- | --- | --- |
| 110 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Brenner `עבדותעולמ` (bdwtwlm) | HEB_BRENNER |
| 111 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Brenner `לעבדו` (lbdw) | HEB_BRENNER |
| 112 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Bialik `ועבדו` (wbdw) | HEB_BIALIK |
| 113 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Bialik `ולמשועבדו` (wlmshwbdw) | HEB_BIALIK |
| 115 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Bialik `לאתעבד` (ltbd) | HEB_BIALIK |
| 116 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Brenner `עבדותעולמ` (bdwtwlm) | HEB_BRENNER |
| 117 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Bialik `ותעבדהו` (wtbdhw) | HEB_BIALIK |
| 118 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Brenner `עבד` (bd) | HEB_BRENNER |
| 119 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Bialik `משתעבדות` (mshtbdwt) | HEB_BIALIK |
| 120 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Brenner `המשועבד` (hmshwbd) | HEB_BRENNER |
| 123 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Bialik `עבדו` (bdw) | HEB_BIALIK |
| 124 | `center_word_same_concept` | `source_specific` | twn_obed_h `עובד` (wbd; English: Obed) | PBY Bialik `כעבדימ` (kbdym) | HEB_BIALIK |

## Triage Bucket Counts

| Bucket | Rows |
| --- | ---: |
| `center_verse_exact` | 100 |
| `center_verse_same_category` | 100 |
| `center_verse_same_concept` | 100 |
| `center_word_exact` | 100 |
| `center_word_same_category` | 100 |
| `hidden_path_only` | 100 |
| `span_exact` | 100 |
| `span_same_category` | 100 |
| `span_same_concept` | 100 |
| `center_word_same_concept` | 26 |

## Cautions

- This is a screening/findings layer, not a claim-reproduction layer.
- Repeated concepts across multiple source term files can duplicate the same normalized form.
- Center-word exact rows are occurrence facts; frequency and controls still govern evidential weight.
- Longer source claims require source-specific matrix geometry, not only ELS hit counting.
