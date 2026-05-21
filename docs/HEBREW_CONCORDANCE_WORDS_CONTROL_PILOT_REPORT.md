# Hebrew Concordance Words Control Pilot Report

Status: paired-control pilot complete; no claim.

This report summarizes a deterministic 200-row MT_WLC/UHB paired-control pilot for the Hebrew concordance clean-lock lane.

This pilot is calibration and triage material only. It does not replace
the full registered representative-control run.

## Scope

| Metric | Rows |
| --- | ---: |
| Full control target rows | 6,790 |
| Pilot target rows | 200 |
| Control result rows | 200 |
| Pilot share of full target table | 2.95% |
| Term-shuffle samples per row | 1000 |
| Random samples per row | 1000 |

## Pilot Corpus Counts

| Corpus | Rows |
| --- | ---: |
| `MT_WLC` | 100 |
| `UHB` | 100 |

## Control Bands

| Band | Rows |
| --- | ---: |
| `not_unusual` | 167 |
| `paired_uncorrected_p_le_0.05` | 33 |

## Statistical Read

- rows with uncorrected `combined_min_p_ge <= 0.05`: 33
- rows with adjusted `combined_min_q_value <= 0.05`: 0
- rows here are pilot rows only; use them to decide whether a full run is worth the cost.

## Most Notable Pilot Rows

| Corpus | Term | Concept | Hits | Term p | Random p | Combined q | Band | Read |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| UHB | `לויי` (lwyy; English: Levite = see Levi "joined to") | Levite = see Levi "joined to" | 25669 | 0.838162 | 0.012987 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `יראייה` (yryyh; English: Irijah = "Jehovah sees me") | Irijah = "Jehovah sees me" | 145 | 0.534466 | 0.012987 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `לויי` (lwyy; English: Levite = see Levi "joined to") | Levite = see Levi "joined to" | 25729 | 0.653347 | 0.013986 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `יהויריב` (yhwyryb; English: Jehoiarib = "Jehovah contends") | Jehoiarib = "Jehovah contends" | 13 | 0.235764 | 0.014985 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `ביתלבאות` (bytlbwt; English: Beth-lebaoth = "house of lionesses") | Beth-lebaoth = "house of lionesses" | 2 | 0.014985 | 0.021978 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `ימימה` (ymymh; English: Jemima = "day by day") | Jemima = "day by day" | 1868 | 0.427572 | 0.016983 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `ביתלבאות` (bytlbwt; English: Beth-lebaoth = "house of lionesses") | Beth-lebaoth = "house of lionesses" | 2 | 0.018981 | 0.016983 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `אימימ` (ymym; English: Emims = "terrors") | Emims = "terrors" | 1779 | 0.274725 | 0.017982 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `יושויה` (ywshwyh; English: Joshaviah = "Jehovah makes equal") | Joshaviah = "Jehovah makes equal" | 146 | 0.757243 | 0.021978 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `יוממ` (ywmm; English: adv) | adv | 20889 | 0.175824 | 0.022977 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `ימימה` (ymymh; English: Jemima = "day by day") | Jemima = "day by day" | 1863 | 0.43956 | 0.023976 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `יראייה` (yryyh; English: Irijah = "Jehovah sees me") | Irijah = "Jehovah sees me" | 147 | 0.504496 | 0.023976 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `יהויריב` (yhwyryb; English: Jehoiarib = "Jehovah contends") | Jehoiarib = "Jehovah contends" | 11 | 0.481518 | 0.025974 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `אימימ` (ymym; English: Emims = "terrors") | Emims = "terrors" | 1768 | 0.317682 | 0.026973 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `יושויה` (ywshwyh; English: Joshaviah = "Jehovah makes equal") | Joshaviah = "Jehovah makes equal" | 148 | 0.773227 | 0.026973 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `יוממ` (ywmm; English: adv) | adv | 20859 | 0.150849 | 0.028971 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `מאוי` (mwy; English: 1) desire) | 1) desire | 19314 | 0.21978 | 0.030969 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `נמואלי` (nmwly; English: Nemuelites = see Nemuel "day of God") | Nemuelites = see Nemuel "day of God" | 83 | 0.030969 | 0.060939 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `תקועי` (tqwy; English: Tekoite = see Tekoa "trumpet blast") | Tekoite = see Tekoa "trumpet blast" | 97 | 0.033966 | 0.672328 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `אויה` (wyh; English: 1) woe!) | 1) woe! | 19664 | 0.835165 | 0.035964 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `ימיני` (ymyny; English: 1) right, on the right, right hand) | 1) right, on the right, right hand | 1494 | 0.214785 | 0.035964 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `אויה` (wyh; English: 1) woe!) | 1) woe! | 19662 | 0.758242 | 0.036963 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `מאוי` (mwy; English: 1) desire) | 1) desire | 19329 | 0.264735 | 0.036963 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `יורי` (ywry; English: Jorai = "Jehovah has taught me") | Jorai = "Jehovah has taught me" | 19506 | 1.0 | 0.037962 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `יורי` (ywry; English: Jorai = "Jehovah has taught me") | Jorai = "Jehovah has taught me" | 19515 | 1.0 | 0.038961 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `ליליא` (lyly; English: 1) night) | 1) night | 1472 | 0.148851 | 0.038961 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `ימיני` (ymyny; English: 1) right, on the right, right hand) | 1) right, on the right, right hand | 1492 | 0.262737 | 0.043956 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `מהומה` (mhwmh; English: 1) tumult, confusion, disquietude, discomfiture, destruction, trouble, vexed, vexation) | 1) tumult, confusion, disquietude, discomfiture, destruction, trouble, vexed, vexation | 1318 | 0.888112 | 0.043956 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `אוריאל` (wryl; English: Uriel = "God (El) is my light") | Uriel = "God (El) is my light" | 99 | 0.061938 | 0.043956 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `אולי` (wly; English: 1) perhaps, peradventure) | 1) perhaps, peradventure | 17269 | 0.744256 | 0.044955 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `ליליא` (lyly; English: 1) night) | 1) night | 1469 | 0.132867 | 0.046953 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `אוריאל` (wryl; English: Uriel = "God (El) is my light") | Uriel = "God (El) is my light" | 94 | 0.12987 | 0.047952 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| UHB | `אויל` (wyl; English: 1) be foolish, foolish) | 1) be foolish, foolish | 17521 | 0.084915 | 0.04995 | 0.223689 | `paired_uncorrected_p_le_0.05` | uncorrected paired-control screen only |
| MT_WLC | `מלותי` (mlwty; English: Mallothi = "I have uttered") | Mallothi = "I have uttered" | 948 | 0.052947 | 0.101898 | 0.223689 | `not_unusual` | not unusual under paired controls |
| MT_WLC | `מהומה` (mhwmh; English: 1) tumult, confusion, disquietude, discomfiture, destruction, trouble, vexed, vexation) | 1) tumult, confusion, disquietude, discomfiture, destruction, trouble, vexed, vexation | 1317 | 0.884116 | 0.053946 | 0.223689 | `not_unusual` | not unusual under paired controls |
| UHB | `המיה` (hmyh; English: 1) sound, music (of instruments)) | 1) sound, music (of instruments) | 16735 | 1.0 | 0.055944 | 0.223689 | `not_unusual` | not unusual; short-form density remains likely |
| UHB | `ישוי` (yshwy; English: Ishui or Ishuai or Isui or Jesui = "he resembles me") | Ishui or Ishuai or Isui or Jesui = "he resembles me" | 16941 | 0.158841 | 0.056943 | 0.223689 | `not_unusual` | not unusual; short-form density remains likely |
| MT_WLC | `הוהמ` (hwhm; English: Hoham = "whom Jehovah impels") | Hoham = "whom Jehovah impels" | 15953 | 0.818182 | 0.056943 | 0.223689 | `not_unusual` | not unusual; short-form density remains likely |
| MT_WLC | `היממ` (hymm; English: Hemam = "exterminating") | Hemam = "exterminating" | 15998 | 0.66034 | 0.057942 | 0.223689 | `not_unusual` | not unusual; short-form density remains likely |
| MT_WLC | `מהלמה` (mhlmh; English: 1) strokes, blows) | 1) strokes, blows | 975 | 0.057942 | 0.093906 | 0.223689 | `not_unusual` | not unusual under paired controls |
