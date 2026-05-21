# Greek Surface New Terms Control Pool

Status: real-word control-pool construction; no ELS control statistic yet.

This report prepares fair controls for the tighter expanded Greek surface
triage. It counts normalized surface-substring verse frequency for every
term in the expanded Greek prospective list, then selects same-length real
Greek terms with the closest surface-frequency vectors across TR_NT,
BYZ_NT, TCG_NT, and SBLGNT.
Selected target terms are excluded from the control candidate pool.

## Inputs

- Terms: `terms/greek_surface_new_terms_clean_lock.csv`
- Selected triage rows: `reports/greek_surface_new_terms/selected_patterns.csv`

## Surface-Frequency Scope

- terms measured: 236
- all-source surface-present terms: 205
- selected targets: 5
- matched controls per target requested: 999

## Selected Targets

| Term | Concept | Length | Surface verse vector | Sum | Controls found |
| --- | --- | ---: | --- | ---: | ---: |
| `ονομα` (onoma; English: Name) | ὄνομα | 5 | 220/220/220/219 | 879 | 50 |
| `σοφια` (sophia; English: wisdom) | σοφία | 5 | 50/50/50/50 | 200 | 50 |
| `θυσια` (thusia; English: Sacrifice) | θυσία | 5 | 47/47/47/46 | 187 | 50 |
| `οικοσ` (oikos; English: House) | οἶκος | 5 | 19/19/19/19 | 76 | 50 |
| `σκηνη` (skene; English: Tabernacle) | σκηνή | 5 | 16/15/15/15 | 61 | 50 |

## Closest Controls

| Target | Control | Control concept | Surface vector | Sum delta | Vector delta |
| --- | --- | --- | --- | ---: | ---: |
| `σοφια` (sophia; English: wisdom) | `γραφη` (graphe) | γραφή | 59/45/45/43 | 8 | 26 |
| `σοφια` (sophia; English: wisdom) | `εργον` (ergon) | ἔργον | 40/40/40/39 | 41 | 41 |
| `σοφια` (sophia; English: wisdom) | `μητηρ` (meter) | μήτηρ | 34/34/34/33 | 65 | 65 |
| `σοφια` (sophia; English: wisdom) | `λογοσ` (logos; English: Word) | λόγος | 68/67/67/66 | 68 | 68 |
| `σοφια` (sophia; English: wisdom) | `τροφη` (trophe) | τροφή | 33/33/33/33 | 68 | 68 |
| `σοφια` (sophia; English: wisdom) | `σιμων` (simon; English: Simon the Zealot) | Simon the Zealot | 70/70/70/69 | 79 | 79 |
| `σοφια` (sophia; English: wisdom) | `ελλην` (ellen) | Ἕλλην | 30/30/30/28 | 82 | 82 |
| `σοφια` (sophia; English: wisdom) | `εορτη` (eorte) | ἑορτή | 25/25/25/23 | 102 | 102 |
| `σοφια` (sophia; English: wisdom) | `στομα` (stoma) | στόμα | 76/76/76/75 | 103 | 103 |
| `σοφια` (sophia; English: wisdom) | `βουλη` (boule) | βουλή | 23/23/23/23 | 108 | 108 |
| `σοφια` (sophia; English: wisdom) | `πολισ` (polis) | πόλις | 23/21/21/21 | 114 | 114 |
| `σοφια` (sophia; English: wisdom) | `κρινω` (krino) | κρίνω | 21/20/20/21 | 118 | 118 |
| `σοφια` (sophia; English: wisdom) | `ηλιοσ` (elios) | ἥλιος | 19/19/19/19 | 124 | 124 |
| `σοφια` (sophia; English: wisdom) | `ιπποσ` (ippos) | ἵππος | 19/18/18/18 | 127 | 127 |
| `σοφια` (sophia; English: wisdom) | `αρτοσ` (artos; English: Bread) | ἄρτος | 18/18/18/18 | 128 | 128 |
| `σοφια` (sophia; English: wisdom) | `ελεοσ` (eleos; English: Mercy) | ἔλεος | 15/15/15/19 | 136 | 136 |
| `σοφια` (sophia; English: wisdom) | `πετρα` (petra) | πέτρα | 15/15/15/15 | 140 | 140 |
| `σοφια` (sophia; English: wisdom) | `εθνοσ` (ethnos) | ἔθνος | 15/15/15/15 | 140 | 140 |
| `σοφια` (sophia; English: wisdom) | `ραββι` (rabbi) | ῥαββί | 15/15/15/15 | 140 | 140 |
| `σοφια` (sophia; English: wisdom) | `φοβοσ` (phobos) | φόβος | 14/14/14/14 | 144 | 144 |
| `σοφια` (sophia; English: wisdom) | `μαρθα` (martha; English: Martha) | Martha | 12/12/12/12 | 152 | 152 |
| `σοφια` (sophia; English: wisdom) | `αγιοσ` (agios) | ἅγιος | 10/12/12/11 | 155 | 155 |
| `σοφια` (sophia; English: wisdom) | `φιλοσ` (philos) | φίλος | 11/11/11/11 | 156 | 156 |
| `σοφια` (sophia; English: wisdom) | `κλινη` (kline) | κλίνη | 11/11/11/11 | 156 | 156 |
| `σοφια` (sophia; English: wisdom) | `μελχι` (melchi; English: Melchi) | Melchi | 11/11/11/10 | 157 | 157 |
| `σοφια` (sophia; English: wisdom) | `λιθοσ` (lithos; English: Stone) | λίθος | 10/10/10/11 | 159 | 159 |
| `σοφια` (sophia; English: wisdom) | `ελπισ` (elpis) | ἐλπίς | 10/10/10/10 | 160 | 160 |
| `σοφια` (sophia; English: wisdom) | `γαμοσ` (gamos) | γάμος | 8/8/8/8 | 168 | 168 |
| `σοφια` (sophia; English: wisdom) | `φιαλη` (phiale) | φιάλη | 7/7/7/7 | 172 | 172 |
| `σοφια` (sophia; English: wisdom) | `δωρον` (doron) | δῶρον | 7/7/7/7 | 172 | 172 |
| `σοφια` (sophia; English: wisdom) | `μωρια` (moria) | μωρία | 6/6/6/6 | 176 | 176 |
| `σοφια` (sophia; English: wisdom) | `ζηλοσ` (zelos) | ζῆλος | 5/5/5/8 | 177 | 177 |
| `σοφια` (sophia; English: wisdom) | `αχειμ` (acheim; English: Achim) | Achim | 4/4/4/3 | 185 | 185 |
| `σοφια` (sophia; English: wisdom) | `ανθοσ` (anthos) | ἄνθος | 3/3/3/3 | 188 | 188 |
| `σοφια` (sophia; English: wisdom) | `εσρωμ` (esrom; English: Hezron) | Hezron | 3/3/3/3 | 188 | 188 |
| `σοφια` (sophia; English: wisdom) | `νοσοσ` (nosos) | νόσος | 3/2/2/2 | 191 | 191 |
| `σοφια` (sophia; English: wisdom) | `αγροσ` (agros) | ἀγρός | 2/2/2/2 | 192 | 192 |
| `σοφια` (sophia; English: wisdom) | `φαρεσ` (phares; English: Perez) | Perez | 2/2/2/2 | 192 | 192 |
| `σοφια` (sophia; English: wisdom) | `θαμαρ` (thamar; English: Tamar) | Tamar | 2/2/2/2 | 192 | 192 |
| `σοφια` (sophia; English: wisdom) | `ιωραμ` (ioram; English: Joram) | Joram | 1/1/2/1 | 195 | 195 |
| `σοφια` (sophia; English: wisdom) | `ορκοσ` (orkos) | ὅρκος | 1/1/1/1 | 196 | 196 |
| `σοφια` (sophia; English: wisdom) | `υπνοσ` (upnos) | ὕπνος | 1/1/1/1 | 196 | 196 |
| `σοφια` (sophia; English: wisdom) | `τοξον` (toxon) | τόξον | 1/1/1/1 | 196 | 196 |
| `σοφια` (sophia; English: wisdom) | `λογχη` (logche) | λόγχη | 1/1/1/1 | 196 | 196 |
| `σοφια` (sophia; English: wisdom) | `ραχαβ` (rachab; English: Rahab) | Rahab | 1/1/1/1 | 196 | 196 |
| `σοφια` (sophia; English: wisdom) | `οζιασ` (ozias; English: Uzziah) | Uzziah | 1/1/1/1 | 196 | 196 |
| `σοφια` (sophia; English: wisdom) | `σαδωκ` (sadok; English: Zadok) | Zadok | 1/1/1/1 | 196 | 196 |
| `σοφια` (sophia; English: wisdom) | `πατηρ` (pater; English: Father) | πατήρ | 107/106/106/106 | 225 | 225 |
| `σοφια` (sophia; English: wisdom) | `χαρισ` (charis) | χάρις | 146/147/147/146 | 386 | 386 |
| `σοφια` (sophia; English: wisdom) | `αγαπη` (agape; English: Love) | ἀγάπη | 188/188/188/186 | 550 | 550 |
| `θυσια` (thusia; English: Sacrifice) | `γραφη` (graphe) | γραφή | 59/45/45/43 | 5 | 19 |
| `θυσια` (thusia; English: Sacrifice) | `εργον` (ergon) | ἔργον | 40/40/40/39 | 28 | 28 |
| `θυσια` (thusia; English: Sacrifice) | `μητηρ` (meter) | μήτηρ | 34/34/34/33 | 52 | 52 |
| `θυσια` (thusia; English: Sacrifice) | `τροφη` (trophe) | τροφή | 33/33/33/33 | 55 | 55 |
| `θυσια` (thusia; English: Sacrifice) | `ελλην` (ellen) | Ἕλλην | 30/30/30/28 | 69 | 69 |
| `θυσια` (thusia; English: Sacrifice) | `λογοσ` (logos; English: Word) | λόγος | 68/67/67/66 | 81 | 81 |
| `θυσια` (thusia; English: Sacrifice) | `εορτη` (eorte) | ἑορτή | 25/25/25/23 | 89 | 89 |
| `θυσια` (thusia; English: Sacrifice) | `σιμων` (simon; English: Simon the Zealot) | Simon the Zealot | 70/70/70/69 | 92 | 92 |
| `θυσια` (thusia; English: Sacrifice) | `βουλη` (boule) | βουλή | 23/23/23/23 | 95 | 95 |
| `θυσια` (thusia; English: Sacrifice) | `πολισ` (polis) | πόλις | 23/21/21/21 | 101 | 101 |
| `θυσια` (thusia; English: Sacrifice) | `κρινω` (krino) | κρίνω | 21/20/20/21 | 105 | 105 |
| `θυσια` (thusia; English: Sacrifice) | `ηλιοσ` (elios) | ἥλιος | 19/19/19/19 | 111 | 111 |
| `θυσια` (thusia; English: Sacrifice) | `ιπποσ` (ippos) | ἵππος | 19/18/18/18 | 114 | 114 |
| `θυσια` (thusia; English: Sacrifice) | `αρτοσ` (artos; English: Bread) | ἄρτος | 18/18/18/18 | 115 | 115 |
| `θυσια` (thusia; English: Sacrifice) | `στομα` (stoma) | στόμα | 76/76/76/75 | 116 | 116 |
| `θυσια` (thusia; English: Sacrifice) | `ελεοσ` (eleos; English: Mercy) | ἔλεος | 15/15/15/19 | 123 | 123 |
| `θυσια` (thusia; English: Sacrifice) | `πετρα` (petra) | πέτρα | 15/15/15/15 | 127 | 127 |
| `θυσια` (thusia; English: Sacrifice) | `εθνοσ` (ethnos) | ἔθνος | 15/15/15/15 | 127 | 127 |
| `θυσια` (thusia; English: Sacrifice) | `ραββι` (rabbi) | ῥαββί | 15/15/15/15 | 127 | 127 |
| `θυσια` (thusia; English: Sacrifice) | `φοβοσ` (phobos) | φόβος | 14/14/14/14 | 131 | 131 |
| `θυσια` (thusia; English: Sacrifice) | `μαρθα` (martha; English: Martha) | Martha | 12/12/12/12 | 139 | 139 |
| `θυσια` (thusia; English: Sacrifice) | `αγιοσ` (agios) | ἅγιος | 10/12/12/11 | 142 | 142 |
| `θυσια` (thusia; English: Sacrifice) | `φιλοσ` (philos) | φίλος | 11/11/11/11 | 143 | 143 |
| `θυσια` (thusia; English: Sacrifice) | `κλινη` (kline) | κλίνη | 11/11/11/11 | 143 | 143 |
| `θυσια` (thusia; English: Sacrifice) | `μελχι` (melchi; English: Melchi) | Melchi | 11/11/11/10 | 144 | 144 |
| `θυσια` (thusia; English: Sacrifice) | `λιθοσ` (lithos; English: Stone) | λίθος | 10/10/10/11 | 146 | 146 |
| `θυσια` (thusia; English: Sacrifice) | `ελπισ` (elpis) | ἐλπίς | 10/10/10/10 | 147 | 147 |
| `θυσια` (thusia; English: Sacrifice) | `γαμοσ` (gamos) | γάμος | 8/8/8/8 | 155 | 155 |
| `θυσια` (thusia; English: Sacrifice) | `φιαλη` (phiale) | φιάλη | 7/7/7/7 | 159 | 159 |
| `θυσια` (thusia; English: Sacrifice) | `δωρον` (doron) | δῶρον | 7/7/7/7 | 159 | 159 |
| `θυσια` (thusia; English: Sacrifice) | `μωρια` (moria) | μωρία | 6/6/6/6 | 163 | 163 |
| `θυσια` (thusia; English: Sacrifice) | `ζηλοσ` (zelos) | ζῆλος | 5/5/5/8 | 164 | 164 |
| `θυσια` (thusia; English: Sacrifice) | `αχειμ` (acheim; English: Achim) | Achim | 4/4/4/3 | 172 | 172 |
| `θυσια` (thusia; English: Sacrifice) | `ανθοσ` (anthos) | ἄνθος | 3/3/3/3 | 175 | 175 |
| `θυσια` (thusia; English: Sacrifice) | `εσρωμ` (esrom; English: Hezron) | Hezron | 3/3/3/3 | 175 | 175 |
| `θυσια` (thusia; English: Sacrifice) | `νοσοσ` (nosos) | νόσος | 3/2/2/2 | 178 | 178 |
| `θυσια` (thusia; English: Sacrifice) | `αγροσ` (agros) | ἀγρός | 2/2/2/2 | 179 | 179 |
| `θυσια` (thusia; English: Sacrifice) | `φαρεσ` (phares; English: Perez) | Perez | 2/2/2/2 | 179 | 179 |
| `θυσια` (thusia; English: Sacrifice) | `θαμαρ` (thamar; English: Tamar) | Tamar | 2/2/2/2 | 179 | 179 |
| `θυσια` (thusia; English: Sacrifice) | `ιωραμ` (ioram; English: Joram) | Joram | 1/1/2/1 | 182 | 182 |
| `θυσια` (thusia; English: Sacrifice) | `ορκοσ` (orkos) | ὅρκος | 1/1/1/1 | 183 | 183 |
| `θυσια` (thusia; English: Sacrifice) | `υπνοσ` (upnos) | ὕπνος | 1/1/1/1 | 183 | 183 |
| `θυσια` (thusia; English: Sacrifice) | `τοξον` (toxon) | τόξον | 1/1/1/1 | 183 | 183 |
| `θυσια` (thusia; English: Sacrifice) | `λογχη` (logche) | λόγχη | 1/1/1/1 | 183 | 183 |
| `θυσια` (thusia; English: Sacrifice) | `ραχαβ` (rachab; English: Rahab) | Rahab | 1/1/1/1 | 183 | 183 |
| `θυσια` (thusia; English: Sacrifice) | `οζιασ` (ozias; English: Uzziah) | Uzziah | 1/1/1/1 | 183 | 183 |
| `θυσια` (thusia; English: Sacrifice) | `σαδωκ` (sadok; English: Zadok) | Zadok | 1/1/1/1 | 183 | 183 |
| `θυσια` (thusia; English: Sacrifice) | `πατηρ` (pater; English: Father) | πατήρ | 107/106/106/106 | 238 | 238 |
| `θυσια` (thusia; English: Sacrifice) | `χαρισ` (charis) | χάρις | 146/147/147/146 | 399 | 399 |
| `θυσια` (thusia; English: Sacrifice) | `αγαπη` (agape; English: Love) | ἀγάπη | 188/188/188/186 | 563 | 563 |
| `ονομα` (onoma; English: Name) | `αγαπη` (agape; English: Love) | ἀγάπη | 188/188/188/186 | 129 | 129 |
| `ονομα` (onoma; English: Name) | `χαρισ` (charis) | χάρις | 146/147/147/146 | 293 | 293 |
| `ονομα` (onoma; English: Name) | `πατηρ` (pater; English: Father) | πατήρ | 107/106/106/106 | 454 | 454 |
| `ονομα` (onoma; English: Name) | `στομα` (stoma) | στόμα | 76/76/76/75 | 576 | 576 |
| `ονομα` (onoma; English: Name) | `σιμων` (simon; English: Simon the Zealot) | Simon the Zealot | 70/70/70/69 | 600 | 600 |
| `ονομα` (onoma; English: Name) | `λογοσ` (logos; English: Word) | λόγος | 68/67/67/66 | 611 | 611 |
| `ονομα` (onoma; English: Name) | `γραφη` (graphe) | γραφή | 59/45/45/43 | 687 | 687 |
| `ονομα` (onoma; English: Name) | `εργον` (ergon) | ἔργον | 40/40/40/39 | 720 | 720 |
| `ονομα` (onoma; English: Name) | `μητηρ` (meter) | μήτηρ | 34/34/34/33 | 744 | 744 |
| `ονομα` (onoma; English: Name) | `τροφη` (trophe) | τροφή | 33/33/33/33 | 747 | 747 |
| `ονομα` (onoma; English: Name) | `ελλην` (ellen) | Ἕλλην | 30/30/30/28 | 761 | 761 |
| `ονομα` (onoma; English: Name) | `εορτη` (eorte) | ἑορτή | 25/25/25/23 | 781 | 781 |
| `ονομα` (onoma; English: Name) | `βουλη` (boule) | βουλή | 23/23/23/23 | 787 | 787 |
| `ονομα` (onoma; English: Name) | `πολισ` (polis) | πόλις | 23/21/21/21 | 793 | 793 |
| `ονομα` (onoma; English: Name) | `κρινω` (krino) | κρίνω | 21/20/20/21 | 797 | 797 |
| `ονομα` (onoma; English: Name) | `ηλιοσ` (elios) | ἥλιος | 19/19/19/19 | 803 | 803 |
| `ονομα` (onoma; English: Name) | `ιπποσ` (ippos) | ἵππος | 19/18/18/18 | 806 | 806 |
| `ονομα` (onoma; English: Name) | `αρτοσ` (artos; English: Bread) | ἄρτος | 18/18/18/18 | 807 | 807 |
| `ονομα` (onoma; English: Name) | `ελεοσ` (eleos; English: Mercy) | ἔλεος | 15/15/15/19 | 815 | 815 |
| `ονομα` (onoma; English: Name) | `πετρα` (petra) | πέτρα | 15/15/15/15 | 819 | 819 |
| `ονομα` (onoma; English: Name) | `εθνοσ` (ethnos) | ἔθνος | 15/15/15/15 | 819 | 819 |
| `ονομα` (onoma; English: Name) | `ραββι` (rabbi) | ῥαββί | 15/15/15/15 | 819 | 819 |
| `ονομα` (onoma; English: Name) | `φοβοσ` (phobos) | φόβος | 14/14/14/14 | 823 | 823 |
| `ονομα` (onoma; English: Name) | `μαρθα` (martha; English: Martha) | Martha | 12/12/12/12 | 831 | 831 |
| `ονομα` (onoma; English: Name) | `αγιοσ` (agios) | ἅγιος | 10/12/12/11 | 834 | 834 |
| `ονομα` (onoma; English: Name) | `φιλοσ` (philos) | φίλος | 11/11/11/11 | 835 | 835 |
| `ονομα` (onoma; English: Name) | `κλινη` (kline) | κλίνη | 11/11/11/11 | 835 | 835 |
| `ονομα` (onoma; English: Name) | `μελχι` (melchi; English: Melchi) | Melchi | 11/11/11/10 | 836 | 836 |
| `ονομα` (onoma; English: Name) | `λιθοσ` (lithos; English: Stone) | λίθος | 10/10/10/11 | 838 | 838 |
| `ονομα` (onoma; English: Name) | `ελπισ` (elpis) | ἐλπίς | 10/10/10/10 | 839 | 839 |
| `ονομα` (onoma; English: Name) | `γαμοσ` (gamos) | γάμος | 8/8/8/8 | 847 | 847 |
| `ονομα` (onoma; English: Name) | `φιαλη` (phiale) | φιάλη | 7/7/7/7 | 851 | 851 |
| `ονομα` (onoma; English: Name) | `δωρον` (doron) | δῶρον | 7/7/7/7 | 851 | 851 |
| `ονομα` (onoma; English: Name) | `μωρια` (moria) | μωρία | 6/6/6/6 | 855 | 855 |
| `ονομα` (onoma; English: Name) | `ζηλοσ` (zelos) | ζῆλος | 5/5/5/8 | 856 | 856 |
| `ονομα` (onoma; English: Name) | `αχειμ` (acheim; English: Achim) | Achim | 4/4/4/3 | 864 | 864 |
| `ονομα` (onoma; English: Name) | `ανθοσ` (anthos) | ἄνθος | 3/3/3/3 | 867 | 867 |
| `ονομα` (onoma; English: Name) | `εσρωμ` (esrom; English: Hezron) | Hezron | 3/3/3/3 | 867 | 867 |
| `ονομα` (onoma; English: Name) | `νοσοσ` (nosos) | νόσος | 3/2/2/2 | 870 | 870 |
| `ονομα` (onoma; English: Name) | `αγροσ` (agros) | ἀγρός | 2/2/2/2 | 871 | 871 |
| `ονομα` (onoma; English: Name) | `φαρεσ` (phares; English: Perez) | Perez | 2/2/2/2 | 871 | 871 |
| `ονομα` (onoma; English: Name) | `θαμαρ` (thamar; English: Tamar) | Tamar | 2/2/2/2 | 871 | 871 |
| `ονομα` (onoma; English: Name) | `ιωραμ` (ioram; English: Joram) | Joram | 1/1/2/1 | 874 | 874 |
| `ονομα` (onoma; English: Name) | `ορκοσ` (orkos) | ὅρκος | 1/1/1/1 | 875 | 875 |
| `ονομα` (onoma; English: Name) | `υπνοσ` (upnos) | ὕπνος | 1/1/1/1 | 875 | 875 |
| `ονομα` (onoma; English: Name) | `τοξον` (toxon) | τόξον | 1/1/1/1 | 875 | 875 |
| `ονομα` (onoma; English: Name) | `λογχη` (logche) | λόγχη | 1/1/1/1 | 875 | 875 |
| `ονομα` (onoma; English: Name) | `ραχαβ` (rachab; English: Rahab) | Rahab | 1/1/1/1 | 875 | 875 |
| `ονομα` (onoma; English: Name) | `οζιασ` (ozias; English: Uzziah) | Uzziah | 1/1/1/1 | 875 | 875 |
| `ονομα` (onoma; English: Name) | `σαδωκ` (sadok; English: Zadok) | Zadok | 1/1/1/1 | 875 | 875 |
| `οικοσ` (oikos; English: House) | `ηλιοσ` (elios) | ἥλιος | 19/19/19/19 | 0 | 0 |
| `οικοσ` (oikos; English: House) | `ιπποσ` (ippos) | ἵππος | 19/18/18/18 | 3 | 3 |
| `οικοσ` (oikos; English: House) | `αρτοσ` (artos; English: Bread) | ἄρτος | 18/18/18/18 | 4 | 4 |
| `οικοσ` (oikos; English: House) | `κρινω` (krino) | κρίνω | 21/20/20/21 | 6 | 6 |
| `οικοσ` (oikos; English: House) | `πολισ` (polis) | πόλις | 23/21/21/21 | 10 | 10 |
| `οικοσ` (oikos; English: House) | `ελεοσ` (eleos; English: Mercy) | ἔλεος | 15/15/15/19 | 12 | 12 |
| `οικοσ` (oikos; English: House) | `πετρα` (petra) | πέτρα | 15/15/15/15 | 16 | 16 |
| `οικοσ` (oikos; English: House) | `βουλη` (boule) | βουλή | 23/23/23/23 | 16 | 16 |
| `οικοσ` (oikos; English: House) | `εθνοσ` (ethnos) | ἔθνος | 15/15/15/15 | 16 | 16 |
| `οικοσ` (oikos; English: House) | `ραββι` (rabbi) | ῥαββί | 15/15/15/15 | 16 | 16 |
| `οικοσ` (oikos; English: House) | `φοβοσ` (phobos) | φόβος | 14/14/14/14 | 20 | 20 |
| `οικοσ` (oikos; English: House) | `εορτη` (eorte) | ἑορτή | 25/25/25/23 | 22 | 22 |
| `οικοσ` (oikos; English: House) | `μαρθα` (martha; English: Martha) | Martha | 12/12/12/12 | 28 | 28 |
| `οικοσ` (oikos; English: House) | `αγιοσ` (agios) | ἅγιος | 10/12/12/11 | 31 | 31 |
| `οικοσ` (oikos; English: House) | `φιλοσ` (philos) | φίλος | 11/11/11/11 | 32 | 32 |
| `οικοσ` (oikos; English: House) | `κλινη` (kline) | κλίνη | 11/11/11/11 | 32 | 32 |
| `οικοσ` (oikos; English: House) | `μελχι` (melchi; English: Melchi) | Melchi | 11/11/11/10 | 33 | 33 |
| `οικοσ` (oikos; English: House) | `λιθοσ` (lithos; English: Stone) | λίθος | 10/10/10/11 | 35 | 35 |
| `οικοσ` (oikos; English: House) | `ελπισ` (elpis) | ἐλπίς | 10/10/10/10 | 36 | 36 |
| `οικοσ` (oikos; English: House) | `ελλην` (ellen) | Ἕλλην | 30/30/30/28 | 42 | 42 |
| `οικοσ` (oikos; English: House) | `γαμοσ` (gamos) | γάμος | 8/8/8/8 | 44 | 44 |
| `οικοσ` (oikos; English: House) | `φιαλη` (phiale) | φιάλη | 7/7/7/7 | 48 | 48 |
| `οικοσ` (oikos; English: House) | `δωρον` (doron) | δῶρον | 7/7/7/7 | 48 | 48 |
| `οικοσ` (oikos; English: House) | `μωρια` (moria) | μωρία | 6/6/6/6 | 52 | 52 |
| `οικοσ` (oikos; English: House) | `ζηλοσ` (zelos) | ζῆλος | 5/5/5/8 | 53 | 53 |
| `οικοσ` (oikos; English: House) | `τροφη` (trophe) | τροφή | 33/33/33/33 | 56 | 56 |
| `οικοσ` (oikos; English: House) | `μητηρ` (meter) | μήτηρ | 34/34/34/33 | 59 | 59 |
| `οικοσ` (oikos; English: House) | `αχειμ` (acheim; English: Achim) | Achim | 4/4/4/3 | 61 | 61 |
| `οικοσ` (oikos; English: House) | `ανθοσ` (anthos) | ἄνθος | 3/3/3/3 | 64 | 64 |
| `οικοσ` (oikos; English: House) | `εσρωμ` (esrom; English: Hezron) | Hezron | 3/3/3/3 | 64 | 64 |
| `οικοσ` (oikos; English: House) | `νοσοσ` (nosos) | νόσος | 3/2/2/2 | 67 | 67 |
| `οικοσ` (oikos; English: House) | `αγροσ` (agros) | ἀγρός | 2/2/2/2 | 68 | 68 |
| `οικοσ` (oikos; English: House) | `φαρεσ` (phares; English: Perez) | Perez | 2/2/2/2 | 68 | 68 |
| `οικοσ` (oikos; English: House) | `θαμαρ` (thamar; English: Tamar) | Tamar | 2/2/2/2 | 68 | 68 |
| `οικοσ` (oikos; English: House) | `ιωραμ` (ioram; English: Joram) | Joram | 1/1/2/1 | 71 | 71 |
| `οικοσ` (oikos; English: House) | `ορκοσ` (orkos) | ὅρκος | 1/1/1/1 | 72 | 72 |
| `οικοσ` (oikos; English: House) | `υπνοσ` (upnos) | ὕπνος | 1/1/1/1 | 72 | 72 |
| `οικοσ` (oikos; English: House) | `τοξον` (toxon) | τόξον | 1/1/1/1 | 72 | 72 |
| `οικοσ` (oikos; English: House) | `λογχη` (logche) | λόγχη | 1/1/1/1 | 72 | 72 |
| `οικοσ` (oikos; English: House) | `ραχαβ` (rachab; English: Rahab) | Rahab | 1/1/1/1 | 72 | 72 |
| `οικοσ` (oikos; English: House) | `οζιασ` (ozias; English: Uzziah) | Uzziah | 1/1/1/1 | 72 | 72 |
| `οικοσ` (oikos; English: House) | `σαδωκ` (sadok; English: Zadok) | Zadok | 1/1/1/1 | 72 | 72 |
| `οικοσ` (oikos; English: House) | `εργον` (ergon) | ἔργον | 40/40/40/39 | 83 | 83 |
| `οικοσ` (oikos; English: House) | `γραφη` (graphe) | γραφή | 59/45/45/43 | 116 | 116 |
| `οικοσ` (oikos; English: House) | `λογοσ` (logos; English: Word) | λόγος | 68/67/67/66 | 192 | 192 |
| `οικοσ` (oikos; English: House) | `σιμων` (simon; English: Simon the Zealot) | Simon the Zealot | 70/70/70/69 | 203 | 203 |
| `οικοσ` (oikos; English: House) | `στομα` (stoma) | στόμα | 76/76/76/75 | 227 | 227 |
| `οικοσ` (oikos; English: House) | `πατηρ` (pater; English: Father) | πατήρ | 107/106/106/106 | 349 | 349 |
| `οικοσ` (oikos; English: House) | `χαρισ` (charis) | χάρις | 146/147/147/146 | 510 | 510 |
| `οικοσ` (oikos; English: House) | `αγαπη` (agape; English: Love) | ἀγάπη | 188/188/188/186 | 674 | 674 |
| `σκηνη` (skene; English: Tabernacle) | `πετρα` (petra) | πέτρα | 15/15/15/15 | 1 | 1 |
| `σκηνη` (skene; English: Tabernacle) | `εθνοσ` (ethnos) | ἔθνος | 15/15/15/15 | 1 | 1 |
| `σκηνη` (skene; English: Tabernacle) | `ραββι` (rabbi) | ῥαββί | 15/15/15/15 | 1 | 1 |
| `σκηνη` (skene; English: Tabernacle) | `ελεοσ` (eleos; English: Mercy) | ἔλεος | 15/15/15/19 | 3 | 5 |
| `σκηνη` (skene; English: Tabernacle) | `φοβοσ` (phobos) | φόβος | 14/14/14/14 | 5 | 5 |
| `σκηνη` (skene; English: Tabernacle) | `αρτοσ` (artos; English: Bread) | ἄρτος | 18/18/18/18 | 11 | 11 |
| `σκηνη` (skene; English: Tabernacle) | `ιπποσ` (ippos) | ἵππος | 19/18/18/18 | 12 | 12 |
| `σκηνη` (skene; English: Tabernacle) | `μαρθα` (martha; English: Martha) | Martha | 12/12/12/12 | 13 | 13 |
| `σκηνη` (skene; English: Tabernacle) | `ηλιοσ` (elios) | ἥλιος | 19/19/19/19 | 15 | 15 |
| `σκηνη` (skene; English: Tabernacle) | `αγιοσ` (agios) | ἅγιος | 10/12/12/11 | 16 | 16 |
| `σκηνη` (skene; English: Tabernacle) | `φιλοσ` (philos) | φίλος | 11/11/11/11 | 17 | 17 |
| `σκηνη` (skene; English: Tabernacle) | `κλινη` (kline) | κλίνη | 11/11/11/11 | 17 | 17 |
| `σκηνη` (skene; English: Tabernacle) | `μελχι` (melchi; English: Melchi) | Melchi | 11/11/11/10 | 18 | 18 |
| `σκηνη` (skene; English: Tabernacle) | `λιθοσ` (lithos; English: Stone) | λίθος | 10/10/10/11 | 20 | 20 |
| `σκηνη` (skene; English: Tabernacle) | `ελπισ` (elpis) | ἐλπίς | 10/10/10/10 | 21 | 21 |
| `σκηνη` (skene; English: Tabernacle) | `κρινω` (krino) | κρίνω | 21/20/20/21 | 21 | 21 |
| `σκηνη` (skene; English: Tabernacle) | `πολισ` (polis) | πόλις | 23/21/21/21 | 25 | 25 |
| `σκηνη` (skene; English: Tabernacle) | `γαμοσ` (gamos) | γάμος | 8/8/8/8 | 29 | 29 |
| `σκηνη` (skene; English: Tabernacle) | `βουλη` (boule) | βουλή | 23/23/23/23 | 31 | 31 |
| `σκηνη` (skene; English: Tabernacle) | `φιαλη` (phiale) | φιάλη | 7/7/7/7 | 33 | 33 |
| `σκηνη` (skene; English: Tabernacle) | `δωρον` (doron) | δῶρον | 7/7/7/7 | 33 | 33 |
| `σκηνη` (skene; English: Tabernacle) | `εορτη` (eorte) | ἑορτή | 25/25/25/23 | 37 | 37 |
| `σκηνη` (skene; English: Tabernacle) | `μωρια` (moria) | μωρία | 6/6/6/6 | 37 | 37 |
| `σκηνη` (skene; English: Tabernacle) | `ζηλοσ` (zelos) | ζῆλος | 5/5/5/8 | 38 | 38 |
| `σκηνη` (skene; English: Tabernacle) | `αχειμ` (acheim; English: Achim) | Achim | 4/4/4/3 | 46 | 46 |
| `σκηνη` (skene; English: Tabernacle) | `ανθοσ` (anthos) | ἄνθος | 3/3/3/3 | 49 | 49 |
| `σκηνη` (skene; English: Tabernacle) | `εσρωμ` (esrom; English: Hezron) | Hezron | 3/3/3/3 | 49 | 49 |
| `σκηνη` (skene; English: Tabernacle) | `νοσοσ` (nosos) | νόσος | 3/2/2/2 | 52 | 52 |
| `σκηνη` (skene; English: Tabernacle) | `αγροσ` (agros) | ἀγρός | 2/2/2/2 | 53 | 53 |
| `σκηνη` (skene; English: Tabernacle) | `φαρεσ` (phares; English: Perez) | Perez | 2/2/2/2 | 53 | 53 |
| `σκηνη` (skene; English: Tabernacle) | `θαμαρ` (thamar; English: Tamar) | Tamar | 2/2/2/2 | 53 | 53 |
| `σκηνη` (skene; English: Tabernacle) | `ιωραμ` (ioram; English: Joram) | Joram | 1/1/2/1 | 56 | 56 |
| `σκηνη` (skene; English: Tabernacle) | `ορκοσ` (orkos) | ὅρκος | 1/1/1/1 | 57 | 57 |
| `σκηνη` (skene; English: Tabernacle) | `ελλην` (ellen) | Ἕλλην | 30/30/30/28 | 57 | 57 |
| `σκηνη` (skene; English: Tabernacle) | `υπνοσ` (upnos) | ὕπνος | 1/1/1/1 | 57 | 57 |
| `σκηνη` (skene; English: Tabernacle) | `τοξον` (toxon) | τόξον | 1/1/1/1 | 57 | 57 |
| `σκηνη` (skene; English: Tabernacle) | `λογχη` (logche) | λόγχη | 1/1/1/1 | 57 | 57 |
| `σκηνη` (skene; English: Tabernacle) | `ραχαβ` (rachab; English: Rahab) | Rahab | 1/1/1/1 | 57 | 57 |
| `σκηνη` (skene; English: Tabernacle) | `οζιασ` (ozias; English: Uzziah) | Uzziah | 1/1/1/1 | 57 | 57 |
| `σκηνη` (skene; English: Tabernacle) | `σαδωκ` (sadok; English: Zadok) | Zadok | 1/1/1/1 | 57 | 57 |
| `σκηνη` (skene; English: Tabernacle) | `τροφη` (trophe) | τροφή | 33/33/33/33 | 71 | 71 |
| `σκηνη` (skene; English: Tabernacle) | `μητηρ` (meter) | μήτηρ | 34/34/34/33 | 74 | 74 |
| `σκηνη` (skene; English: Tabernacle) | `εργον` (ergon) | ἔργον | 40/40/40/39 | 98 | 98 |
| `σκηνη` (skene; English: Tabernacle) | `γραφη` (graphe) | γραφή | 59/45/45/43 | 131 | 131 |
| `σκηνη` (skene; English: Tabernacle) | `λογοσ` (logos; English: Word) | λόγος | 68/67/67/66 | 207 | 207 |
| `σκηνη` (skene; English: Tabernacle) | `σιμων` (simon; English: Simon the Zealot) | Simon the Zealot | 70/70/70/69 | 218 | 218 |
| `σκηνη` (skene; English: Tabernacle) | `στομα` (stoma) | στόμα | 76/76/76/75 | 242 | 242 |
| `σκηνη` (skene; English: Tabernacle) | `πατηρ` (pater; English: Father) | πατήρ | 107/106/106/106 | 364 | 364 |
| `σκηνη` (skene; English: Tabernacle) | `χαρισ` (charis) | χάρις | 146/147/147/146 | 525 | 525 |
| `σκηνη` (skene; English: Tabernacle) | `αγαπη` (agape; English: Love) | ἀγάπη | 188/188/188/186 | 689 | 689 |

## Read

This is a control-pool report, not a significance test. It uses the same
normalized substring rule as the current surface-context path and avoids
the bad control design of comparing surface-context rows against random
strings. The next step can freeze one matched-control set per target and
then run the ELS exact-center surface statistic against those real-word
controls.
