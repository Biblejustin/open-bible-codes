# Windows CPU Broad Skip 2..500 Bible-Control Findings

This report summarizes the Windows desktop CPU broad count sweep as a
language-matched Bible-vs-control comparison. The raw sweep is retained;
this layer only normalizes by legal ELS search positions and compares each
term against non-Bible corpora in the same language.

## Scope

- Count directory: `reports/windows_cpu/broad_2_500`
- Run manifest: `reports/windows_cpu/broad_2_500/broad_2_500.manifest.json`
- Skip range: `2..500`
- Direction: `both`
- Term sets: 22
- Corpora: 21
- Comparison rows: 2705
- Display filter in this markdown: normalized length >= 4

## Main Read

- Raw high-count rows are dominated by short forms, acronyms, and ordinary language density.
- The comparison CSV keeps all rows; this markdown highlights longer rows first.
- A zero-control row with one or two Bible hits is a queue item, not a claim.
- Null controls can also show favorable ratios; that is a warning against interpreting ratios alone.
- Any favorable row still needs centered-hit context, version distribution, and matched controls.

## Stronger Original-Language Bible-Over-Control Rows

| Term | Set | Bible max | Control max | Control median | Ratio vs max | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `jobab_g` `ιωβαβ` (iobab; English: Jobab) | table_of_nations | 0.038775 (LXX) | 0.011759 (GRK_ODYSSEY) | 0.008339 | 3.297426 | Bible max rate exceeds all observed controls |
| `probus_g` `προβοσ` (probos; English: Probus) | prophetic_terms | 0.014765 (SBLGNT) | 0.005213 (GRK_HERODOTUS) | 0.003638 | 2.832143 | Bible max rate exceeds all observed controls |
| `jacob_g` `ιακωβ` (iakob; English: Jacob) | theological_terms | 0.148998 (LXX) | 0.055248 (GRK_HERODOTUS) | 0.05273 | 2.696887 | Bible max rate exceeds all observed controls |
| `isaac_g` `ισαακ` (Isaak; English: Isaac) | theological_terms | 5.398393 (LXX) | 2.300615 (GRK_HERODOTUS) | 2.289229 | 2.3465 | Bible max rate exceeds all observed controls |
| `sabaoth_g` `σαβαωθ` (sabaoth; English: Lord Of Hosts) | theological_terms | 0.005386 (LXX) | 0.002353 (GRK_ODYSSEY) | 0.002085 | 2.288736 | Bible max rate exceeds all observed controls |
| `carinus_g` `καρινοσ` (karinos; English: Carinus) | prophetic_terms | 0.01185 (LXX) | 0.00546 (GRK_ILIAD) | 0.004172 | 2.17042 | Bible max rate exceeds all observed controls |
| `year_2001_additive_h` `תתתתתא` (ttttt; English: Gregorian 2001) | hebrew_claim_terms | 0.068429 (MAM) | 0.032262 (HEB_BIALIK) | 0.03162 | 2.121051 | Bible max rate exceeds all observed controls |
| `seba_g` `σαβα` (saba; English: Seba) | table_of_nations | 10.106896 (LXX) | 4.816796 (GRK_HERODOTUS) | 4.285579 | 2.098261 | Bible max rate exceeds all observed controls |
| `kittim_g` `κιτιοι` (kitioi; English: Kittim) | table_of_nations | 0.307358 (LXX) | 0.15119 (GRK_HERODOTUS) | 0.127075 | 2.032928 | Bible max rate exceeds all observed controls |
| `stauros_gnt` `σταυροσ` (stauros; English: Cross) | greek_nt_claim_terms | 0.014536 (TR_NT) | 0.007301 (GRK_HERODOTUS) | 0.00728 | 1.991035 | Bible max rate exceeds all observed controls |
| `cyrus_g` `κυροσ` (kuros; English: Cyrus) | prophetic_terms | 0.743195 (LXX) | 0.373945 (GRK_ODYSSEY) | 0.367973 | 1.987442 | Bible max rate exceeds all observed controls |
| `abimael_h` `אבימאל` (byml; English: Abimael) | table_of_nations | 0.274008 (MT_WLC) | 0.147197 (HEB_AHAD_HAAM) | 0.145532 | 1.861507 | Bible max rate exceeds all observed controls |
| `overcome_g` `νικαω` (nikao; English: Overcome) | prophetic_terms | 1.276715 (LXX) | 0.693208 (GRK_HERODOTUS) | 0.663676 | 1.84175 | Bible max rate exceeds all observed controls |
| `rosh_hashanah_h` `ראשהשנה` (rshhshnh; English: Rosh Hashanah) | biblical_festivals | 0.008391 (UHB) | 0.004559 (HEB_BIALIK) | 0.003418 | 1.84059 | Bible max rate exceeds all observed controls |
| `prophet_isaiah_g` `ησαιασ` (esaias; English: Isaiah) | biblical_prophets_cohort | 0.403587 (LXX) | 0.225911 (GRK_ODYSSEY) | 0.204367 | 1.786485 | Bible max rate exceeds all observed controls |
| `cainan_g` `καιναν` (kainan; English: Cainan) | table_of_nations | 0.363731 (LXX) | 0.203741 (GRK_ILIAD) | 0.197068 | 1.785259 | Bible max rate exceeds all observed controls |
| `syria_g` `συρια` (suria; English: Syria) | modern_names_dates | 2.248253 (LXX) | 1.260595 (GRK_ODYSSEY) | 1.220074 | 1.783485 | Bible max rate exceeds all observed controls |
| `witness_g` `μαρτυσ` (martus; English: Witness) | prophetic_terms | 0.059061 (SBLGNT) | 0.033366 (GRK_HERODOTUS) | 0.018191 | 1.770089 | Bible max rate exceeds all observed controls |
| `sabtah_g` `σαβαθα` (sabatha; English: Sabtah) | table_of_nations | 0.020826 (LXX) | 0.011766 (GRK_ODYSSEY) | 0.009384 | 1.769956 | Bible max rate exceeds all observed controls |
| `tacitus_g` `τακιτοσ` (takitos; English: Tacitus) | prophetic_terms | 0.029196 (TCG_NT) | 0.016687 (GRK_HERODOTUS) | 0.009419 | 1.749559 | Bible max rate exceeds all observed controls |
| `bashan_g` `βασαν` (basan; English: Bashan) | prophetic_terms | 0.705855 (LXX) | 0.404458 (GRK_HERODOTUS) | 0.308093 | 1.745188 | Bible max rate exceeds all observed controls |
| `krisis_gnt` `κρισισ` (krisis; English: Judgment) | greek_nt_claim_terms | 0.103769 (LXX) | 0.060031 (GRK_ILIAD) | 0.051092 | 1.728597 | Bible max rate exceeds all observed controls |
| `abraham_g` `αβρααμ` (abraam; English: Abraham) | theological_terms | 0.016158 (LXX) | 0.009413 (GRK_ODYSSEY) | 0.003638 | 1.716552 | Bible max rate exceeds all observed controls |
| `kyrios_gnt` `κυριοσ` (kyrios; English: Lord) | greek_nt_claim_terms | 0.072531 (LXX) | 0.04275 (GRK_HERODOTUS) | 0.028239 | 1.696616 | Bible max rate exceeds all observed controls |
| `josiah_g` `ιωσιασ` (iosias; English: Josiah) | prophetic_terms | 0.257449 (LXX) | 0.153275 (GRK_HERODOTUS) | 0.132796 | 1.679647 | Bible max rate exceeds all observed controls |
| `locust_g` `ακρισ` (akris; English: Locust) | prophetic_terms | 1.566094 (LXX) | 0.936039 (GRK_ODYSSEY) | 0.934602 | 1.673108 | Bible max rate exceeds all observed controls |
| `narrative_joshua_g` `ιησουσ` (Iesous; English: Joshua) | biblical_narrative_names | 0.14937 (LXX) | 0.091757 (GRK_HERODOTUS) | 0.08368 | 1.627897 | Bible max rate exceeds all observed controls |
| `dyn_jesus_g` `ιησουσ` (Iesous; English: Jesus) | dynamic_skip_focus_terms | 0.14937 (LXX) | 0.091757 (GRK_HERODOTUS) | 0.08368 | 1.627897 | Bible max rate exceeds all observed controls |
| `javan_g` `ιωυαν` (Iouan; English: Javan) | table_of_nations | 1.803773 (LXX) | 1.112259 (GRK_HERODOTUS) | 0.876416 | 1.621719 | Bible max rate exceeds all observed controls |
| `gaza_g` `γαζα` (gaza; English: Gaza) | modern_names_dates | 0.550314 (TR_NT) | 0.339866 (GRK_ILIAD) | 0.329066 | 1.61921 | Bible max rate exceeds all observed controls |

## English/KJV Secondary Rows

English rows are useful as translation evidence and as method pressure,
but absence or presence here does not decide the original-language hypothesis.

| Term | Set | Bible max | Control max | Control median | Ratio vs max | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `eng_abraham` `abraham` | english_search_terms | 0.003152 (KJVA) | 0.000797 (ENG_WAR_AND_PEACE) | 0.000494 | 3.956277 | Bible max rate exceeds all observed controls |
| `eng_judah` `judah` | english_search_terms | 0.025212 (KJVA) | 0.007164 (ENG_SHAKESPEARE) | 0.006301 | 3.519366 | Bible max rate exceeds all observed controls |
| `eng_elijah` `elijah` | english_search_terms | 0.008405 (KJVA) | 0.00239 (ENG_WAR_AND_PEACE) | 0.002101 | 3.51681 | Bible max rate exceeds all observed controls |
| `eng_jonah` `jonah` | english_search_terms | 0.107284 (KJV) | 0.032554 (ENG_MOBY_DICK) | 0.030385 | 3.295563 | Bible max rate exceeds all observed controls |
| `eng_john` `john` | english_search_terms | 1.258696 (KJV) | 0.382378 (ENG_SHAKESPEARE) | 0.346451 | 3.291762 | Bible max rate exceeds all observed controls |
| `eng_jerah` `jerah` | english_search_terms | 0.12532 (KJV) | 0.046689 (ENG_SHAKESPEARE) | 0.039827 | 2.684164 | Bible max rate exceeds all observed controls |
| `eng_javan` `javan` | english_search_terms | 0.014926 (KJV) | 0.005974 (ENG_WAR_AND_PEACE) | 0.005435 | 2.498559 | Bible max rate exceeds all observed controls |
| `eng_james` `james` | english_search_terms | 0.045712 (KJV) | 0.018774 (ENG_SHAKESPEARE) | 0.013652 | 2.434835 | Bible max rate exceeds all observed controls |
| `eng_trajan` `trajan` | english_search_terms | 0.007464 (KJV) | 0.003186 (ENG_WAR_AND_PEACE) | 0.00247 | 2.342348 | Bible max rate exceeds all observed controls |
| `eng_josiah` `josiah` | english_search_terms | 0.004728 (KJVA) | 0.002101 (ENG_MOBY_DICK) | 0.001593 | 2.250373 | Bible max rate exceeds all observed controls |
| `eng_jacob` `jacob` | english_search_terms | 0.005597 (KJV) | 0.002717 (ENG_SHAKESPEARE) | 0.0021 | 2.059898 | Bible max rate exceeds all observed controls |
| `eng_heth` `heth` | english_search_terms | 97.001671 (KJV) | 49.883669 (ENG_MOBY_DICK) | 49.116977 | 1.944558 | Bible max rate exceeds all observed controls |
| `eng_sheleph` `sheleph` | english_search_terms | 0.004043 (KJV) | 0.002101 (ENG_MOBY_DICK) | 0.001482 | 1.924087 | Bible max rate exceeds all observed controls |
| `eng_hannah` `hannah` | english_search_terms | 0.307881 (KJV) | 0.161713 (ENG_WAR_AND_PEACE) | 0.144956 | 1.903879 | Bible max rate exceeds all observed controls |
| `eng_japan` `japan` | english_search_terms | 0.018036 (KJV) | 0.009558 (ENG_WAR_AND_PEACE) | 0.008401 | 1.886932 | Bible max rate exceeds all observed controls |
| `eng_jesse` `jesse` | english_search_terms | 0.145532 (KJV) | 0.077709 (ENG_MOBY_DICK) | 0.075591 | 1.872778 | Bible max rate exceeds all observed controls |
| `eng_judas` `judas` | english_search_terms | 0.015548 (KJV) | 0.008399 (ENG_SHAKESPEARE) | 0.006301 | 1.851215 | Bible max rate exceeds all observed controls |
| `eng_nahshon` `nahshon` | english_search_terms | 0.015234 (KJVA) | 0.008365 (ENG_WAR_AND_PEACE) | 0.007355 | 1.821143 | Bible max rate exceeds all observed controls |
| `eng_joel` `joel` | english_search_terms | 0.968897 (KJV) | 0.544419 (ENG_SHAKESPEARE) | 0.437788 | 1.779692 | Bible max rate exceeds all observed controls |
| `eng_admah` `admah` | english_search_terms | 0.828416 (KJV) | 0.481505 (ENG_WAR_AND_PEACE) | 0.43823 | 1.720472 | Bible max rate exceeds all observed controls |

## Calibration Rows That Also Exceed Controls

These are not claim rows. They show why favorable Bible/control ratios
still need centered context, source sensitivity, and matched controls.

| Term | Set | Bible max | Control max | Control median | Ratio vs max | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `scrambled_iesous_g` `σιυοσηε` (siuosee; English: Scrambled Jesus) | null_controls | 0.016248 (SBLGNT) | 0.00728 (GRK_ILIAD) | 0.006258 | 2.231898 | Bible max rate exceeds all observed controls |
| `scrambled_kyrios_g` `συρικο` (suriko; English: Scrambled Lord) | null_controls | 0.083662 (LXX) | 0.037537 (GRK_HERODOTUS) | 0.025886 | 2.228792 | Bible max rate exceeds all observed controls |
| `oikos_g` `οικοσ` (oikos; English: House) | frequency_anchors | 3.129675 (LXX) | 1.921467 (GRK_ODYSSEY) | 1.914921 | 1.628794 | Bible max rate exceeds all observed controls |
| `scrambled_pneuma_g` `απνευμ` (apneum; English: Scrambled Spirit) | null_controls | 0.059576 (TR_NT) | 0.043659 (GRK_ILIAD) | 0.042358 | 1.364579 | Bible max rate exceeds all observed controls |
| `psyche_g` `ψυχη` (psuche; English: Soul) | frequency_anchors | 0.038054 (LXX) | 0.028206 (GRK_ODYSSEY) | 0.01454 | 1.349157 | Bible max rate exceeds all observed controls |
| `scrambled_elohim_h` `מהיאלמ` (mhylm; English: Scrambled Elohim) | null_controls | 0.406403 (EBIBLE_WLC) | 0.305297 (HEB_AHAD_HAAM) | 0.295022 | 1.331173 | Bible max rate exceeds all observed controls |
| `scrambled_israel_h` `לרשאי` (lrshy; English: Scrambled Israel) | null_controls | 1.817958 (UXLC) | 1.384923 (HEB_BIALIK) | 1.178596 | 1.312678 | Bible max rate exceeds all observed controls |
| `ouranos_g` `ουρανοσ` (ouranos; English: Heavens) | frequency_anchors | 0.020359 (BYZ_NT) | 0.018199 (GRK_ILIAD) | 0.009419 | 1.11868 | Bible max rate exceeds all observed controls |
| `scrambled_messiah_h` `חישמ` (chyshm; English: Scrambled Messiah) | null_controls | 10.808308 (EBIBLE_WLC) | 9.872865 (HEB_BIALIK) | 8.864729 | 1.094749 | Bible max rate exceeds all observed controls |
| `shamayim_h` `שמימ` (shamayim; English: Heavens) | frequency_anchors | 38.758961 (MAM) | 37.764721 (HEB_BIALIK) | 32.548945 | 1.026327 | Bible max rate exceeds all observed controls |
| `nonsense_6_a_h` `אבגדהו` (bgdhw; English: Nonsense 6a) | null_controls | 0.012569 (EBIBLE_WLC) | 0.012449 (HEB_BIALIK) | 0.009714 | 1.009662 | Bible max rate exceeds all observed controls |

## Bible-Only Low-Count Queue Rows

These rows have at least one Bible hit and zero observed language-matched
control hits in this broad count sweep, but the absolute Bible count is
below the low-count threshold.

| Term | Set | Bible corpus | Bible hits | Bible rate | Read |
| --- | --- | --- | ---: | ---: | --- |
| `eng_judith` `judith` | english_search_terms | KJV | 9 | 0.002799 | Bible-over-control low-count queue row |
| `eng_joktan` `joktan` | english_search_terms | KJV | 4 | 0.001244 | Bible-over-control low-count queue row |
| `covenant_g` `διαθηκη` (diatheke; English: Covenant) | theological_terms | LXX | 3 | 0.001077 | Bible-over-control low-count queue row |
| `eng_anthrax` `anthrax` | english_search_terms | KJVA | 2 | 0.000525 | Bible-over-control low-count queue row |
| `eng_kennedy` `kennedy` | english_search_terms | KJV | 2 | 0.000622 | Bible-over-control low-count queue row |
| `gomorrah_g` `γομορρα` (gomorra; English: Gomorrah) | prophetic_terms | TCG_NT | 2 | 0.00292 | Bible-over-control low-count queue row |
| `prophet_zephaniah_g` `σοφονιασ` (sophonias; English: Zephaniah) | biblical_prophets_cohort | BYZ_NT | 2 | 0.00291 | Bible-over-control low-count queue row |
| `aemilian_h` `אמיליאנוס` (mylynws; English: Aemilian) | prophetic_terms | MAM | 1 | 0.000835 | Bible-over-control low-count queue row |
| `alliance_g` `συμμαχια` (summachia; English: Alliance) | modern_names_dates | LXX | 1 | 0.000359 | Bible-over-control low-count queue row |
| `anastasis_gnt` `αναστασισ` (anastasis; English: Resurrection) | greek_nt_claim_terms | TCG_NT | 1 | 0.001461 | Bible-over-control low-count queue row |
| `barnabas_g` `βαρναβασ` (barnabas; English: Barnabas) | prophetic_terms | LXX | 1 | 0.000359 | Bible-over-control low-count queue row |
| `belshazzar_g` `βαλτασαρ` (baltasar; English: Belshazzar) | prophetic_terms | BYZ_NT | 1 | 0.001455 | Bible-over-control low-count queue row |
| `benjamin_g` `βενιαμιν` (beniamin; English: Benjamin) | biblical_tribes | LXX | 1 | 0.000359 | Bible-over-control low-count queue row |
| `bridegroom_g` `νυμφιοσ` (numphios; English: Bridegroom) | prophetic_terms | SBLGNT | 1 | 0.001477 | Bible-over-control low-count queue row |
| `calneh_g` `χαλαννη` (chalanne; English: Calneh) | table_of_nations | BYZ_NT | 1 | 0.001454 | Bible-over-control low-count queue row |
| `church_g` `εκκλησια` (ekklesia; English: Church) | theological_terms | LXX | 1 | 0.000359 | Bible-over-control low-count queue row |
| `commodus_g` `κομμοδοσ` (kommodos; English: Commodus) | prophetic_terms | BYZ_NT | 1 | 0.001455 | Bible-over-control low-count queue row |
| `corinth_g` `κορινθοσ` (korinthos; English: Corinth) | prophetic_terms | TR_NT | 1 | 0.001454 | Bible-over-control low-count queue row |
| `demon_g` `δαιμονιον` (daimonion; English: Demon) | theological_terms | BYZ_NT | 1 | 0.001455 | Bible-over-control low-count queue row |
| `egypt_g` `αιγυπτοσ` (aiguptos; English: Egypt) | prophetic_terms | TR_NT | 1 | 0.001454 | Bible-over-control low-count queue row |
| `eng_carthage` `carthage` | english_search_terms | KJVA | 1 | 0.000263 | Bible-over-control low-count queue row |
| `eng_goldameir` `goldameir` | english_search_terms | KJV | 1 | 0.000311 | Bible-over-control low-count queue row |
| `eng_hasmonean` `hasmonean` | english_search_terms | KJV | 1 | 0.000311 | Bible-over-control low-count queue row |
| `eng_rokeach` `rokeach` | english_search_terms | KJV | 1 | 0.000311 | Bible-over-control low-count queue row |
| `eng_sonofman` `sonofman` | english_search_terms | KJVA | 1 | 0.000263 | Bible-over-control low-count queue row |
| `eng_sonofman_2` `sonofman` | english_search_terms | KJVA | 1 | 0.000263 | Bible-over-control low-count queue row |
| `eng_tiberius` `tiberius` | english_search_terms | KJV | 1 | 0.000311 | Bible-over-control low-count queue row |
| `eng_togarmah` `togarmah` | english_search_terms | KJV | 1 | 0.000311 | Bible-over-control low-count queue row |
| `flies_plague_g` `κυνομυια` (kunomuia; English: Flies Plague) | prophetic_terms | LXX | 1 | 0.000359 | Bible-over-control low-count queue row |
| `galerius_g` `γαλεριοσ` (galerios; English: Galerius) | prophetic_terms | TR_NT | 1 | 0.001454 | Bible-over-control low-count queue row |

## Control-Background Rows

These rows are useful negative pressure: language-matched controls meet or
exceed the best Bible rate in this broad count sweep.

| Term | Set | Bible max | Control max | Control median | Ratio vs max | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `sabbath_g` `σαββατον` (sabbaton; English: Sabbath) | biblical_festivals | 0.0 (LXX) | 0.001043 (GRK_HERODOTUS) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `prophet_malachi_g` `μαλαχιασ` (malachias; English: Malachi) | biblical_prophets_cohort | 0.0 (LXX) | 0.001043 (GRK_HERODOTUS) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `prophet_zechariah_g` `ζαχαριασ` (zacharias; English: Zechariah) | biblical_prophets_cohort | 0.0 (LXX) | 0.001043 (GRK_HERODOTUS) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `naphtali_g` `νεφθαλιμ` (nephthalim; English: Naphtali) | biblical_tribes | 0.0 (LXX) | 0.001043 (GRK_HERODOTUS) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `dyn_catering_e` `catering` | dynamic_skip_focus_terms | 0.0 (KJV) | 0.000247 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_alliance` `alliance` | english_search_terms | 0.0 (KJV) | 0.000398 (ENG_WAR_AND_PEACE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_babylon` `babylon` | english_search_terms | 0.0 (KJV) | 0.000247 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_barnabas` `barnabas` | english_search_terms | 0.0 (KJV) | 0.000398 (ENG_WAR_AND_PEACE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_binladen` `binladen` | english_search_terms | 0.0 (KJV) | 0.000398 (ENG_WAR_AND_PEACE) | 0.000247 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_bruised` `bruised` | english_search_terms | 0.0 (KJV) | 0.001593 (ENG_WAR_AND_PEACE) | 0.000741 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_colossae` `colossae` | english_search_terms | 0.0 (KJV) | 0.001051 (ENG_MOBY_DICK) | 0.000247 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_cypress` `cypress` | english_search_terms | 0.0 (KJV) | 0.000494 (ENG_SHAKESPEARE) | 0.000398 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_domitian` `domitian` | english_search_terms | 0.0 (KJV) | 0.001195 (ENG_WAR_AND_PEACE) | 0.000247 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_eichmann` `eichmann` | english_search_terms | 0.0 (KJV) | 0.000741 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_eleazar` `eleazar` | english_search_terms | 0.0 (KJV) | 0.000398 (ENG_WAR_AND_PEACE) | 0.000247 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_example` `example` | english_search_terms | 0.0 (KJV) | 0.000247 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_galerius` `galerius` | english_search_terms | 0.0 (KJV) | 0.001051 (ENG_MOBY_DICK) | 0.000398 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_gematria` `gematria` | english_search_terms | 0.0 (KJV) | 0.000398 (ENG_WAR_AND_PEACE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_genocide` `genocide` | english_search_terms | 0.0 (KJV) | 0.000247 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_hamathite` `hamathite` | english_search_terms | 0.0 (KJV) | 0.000247 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_heisrisen` `heisrisen` | english_search_terms | 0.0 (KJV) | 0.000398 (ENG_WAR_AND_PEACE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_hiscross` `hiscross` | english_search_terms | 0.0 (KJV) | 0.000741 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_ironteeth` `ironteeth` | english_search_terms | 0.0 (KJV) | 0.000247 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_japheth` `japheth` | english_search_terms | 0.0 (KJV) | 0.001051 (ENG_MOBY_DICK) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_maximian` `maximian` | english_search_terms | 0.0 (KJV) | 0.000247 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_mosesrod` `mosesrod` | english_search_terms | 0.0 (KJV) | 0.000797 (ENG_WAR_AND_PEACE) | 0.000494 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_mothcode` `mothcode` | english_search_terms | 0.0 (KJV) | 0.000247 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_naphtali` `naphtali` | english_search_terms | 0.0 (KJV) | 0.001051 (ENG_MOBY_DICK) | 0.000247 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_nazarene` `nazarene` | english_search_terms | 0.0 (KJV) | 0.000247 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |
| `eng_newyork` `newyork` | english_search_terms | 0.0 (KJV) | 0.000247 (ENG_SHAKESPEARE) | 0.0 | 0.0 | control background equals or exceeds Bible max rate |

## Outputs

- comparison CSV: `reports/windows_cpu/broad_2_500/bible_control_comparison.csv`
- manifest: `reports/windows_cpu/broad_2_500/bible_control_comparison.manifest.json`

## Caution

This is still a broad count layer. It does not say that a hit is centered
on a relevant surface word, and it does not inspect the letter path. Use it
to select rows for centered/contextual review, not as final evidence.
