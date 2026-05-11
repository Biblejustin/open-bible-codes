"""Reader-facing display helpers for Hebrew and Greek report terms."""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path
import unicodedata


KNOWN_TERMS: dict[str, tuple[str, str]] = {
    "γωγ": ("Gog", "Gog"),
    "ιησουσ": ("Iesous", "Jesus/Joshua"),
    "αιμα": ("haima", "blood"),
    "ναιμανο": ("naimano", "hidden extension form from haima"),
    "δοξα": ("doxa", "glory"),
    "δοξανωσ": ("doxanos", "hidden extension form from doxa"),
    "ισαακ": ("Isaak", "Isaac"),
    "τερασ": ("teras", "wonder"),
    "ανομια": ("anomia", "lawlessness"),
    "υιοσ": ("huios", "son"),
    "ουουιοσ": ("ouhuios", "hidden extension form from huios"),
    "ειουιοσ": ("eiouios", "hidden extension form from huios"),
    "μαρια": ("Maria", "Mary"),
    "ταφοσ": ("taphos", "tomb"),
    "σωτηρ": ("soter", "savior"),
    "ανεστη": ("aneste", "he is risen"),
    "κρισισ": ("krisis", "judgment"),
    "σοφια": ("sophia", "wisdom"),
    "ιουδασ": ("Ioudas", "Judas"),
    "κυριοσ": ("kyrios", "Lord"),
    "κυριου": ("kyriou", "Lord"),
    "πετροσ": ("Petros", "Peter"),
    "θηριον": ("therion", "beast"),
    "δρακων": ("drakon", "dragon"),
    "αδουηλ": ("adouel", "Aduel"),
    "αββα": ("abba", "Abba"),
    "αθανασιαν": ("athanasian", "immortality"),
    "αιματι": ("haimati", "blood"),
    "ακηκοαμεν": ("akekoamen", "we have heard"),
    "αλλα": ("alla", "but"),
    "αληθειασ": ("aletheias", "truth"),
    "αμαρτιαισ": ("hamartiais", "sins"),
    "ανανιηλ": ("ananiel", "Ananiel"),
    "ανθρωπου": ("anthropou", "man/human"),
    "ανδρα": ("andra", "man"),
    "απειθουσι": ("apeithousi", "disobedient"),
    "απειθουσιν": ("apeithousin", "disobedient"),
    "απιστουσιν": ("apistousin", "unbelieving"),
    "αποκαταστησει": ("apokatastesei", "will restore"),
    "αποκριθεισ": ("apokritheis", "having answered"),
    "αριστοβουλου": ("aristoboulou", "Aristobulus"),
    "ασηραυτη": ("aseraute", "Asher, this"),
    "αφθαρσιαν": ("aphtharsian", "incorruption"),
    "αυτου": ("autou", "of him"),
    "αυτουσ": ("autous", "them"),
    "αυτην": ("auten", "her/it"),
    "αυτω": ("auto", "to him"),
    "ιωαννησ": ("Ioannes", "John"),
    "πιλατοσ": ("Pilatos", "Pilate"),
    "χριστοσ": ("Christos", "Christ"),
    "ερχεται": ("erchetai", "he is coming"),
    "ουδεποτε": ("oudepote", "never"),
    "ναοσ": ("naos", "temple"),
    "θεοσ": ("theos", "God"),
    "σιων": ("Sion", "Zion"),
    "φωσ": ("phos", "light"),
    "νομοσ": ("nomos", "law"),
    "αμνοσ": ("amnos", "lamb"),
    "ελαμ": ("Elam", "Elam"),
    "ελκη": ("elke", "boils/sores"),
    "ενεμεσσαρου": ("enemessarou", "Enemessar"),
    "επιφανη": ("epiphane", "manifest/glorious"),
    "επορευομην": ("eporeuomen", "I walked"),
    "εγω": ("ego", "I"),
    "εκ": ("ek", "from"),
    "νωε": ("Noe", "Noah"),
    "ουλ": ("Oul", "Hul"),
    "σημ": ("Sem", "Shem"),
    "σαλα": ("Sala", "Shelah"),
    "χαμ": ("Cham", "Ham"),
    "ελισα": ("Elisa", "Elishah"),
    "ιωυαν": ("Iouan", "Javan"),
    "ευιλα": ("Euila", "Havilah"),
    "αδαμα": ("Adama", "Admah"),
    "μασση": ("Masse", "Mesha"),
    "βασιλεωσ": ("basileos", "king"),
    "βαβυλωνι": ("babuloni", "Babylon"),
    "βαβυλων": ("babulon", "Babylon"),
    "βαβυλωνοσ": ("babulonos", "Babylon"),
    "βουλομαι": ("boulomai", "I want"),
    "βουλει": ("boulei", "you want"),
    "βουληται": ("bouletai", "he wills"),
    "γαβαηλ": ("gabael", "Gabael"),
    "γεγεννημαι": ("gegennemai", "I was born"),
    "δεξιων": ("dexion", "right side"),
    "δε": ("de", "but/and"),
    "δησητε": ("desete", "you bind"),
    "διαφθοραν": ("diaphthoran", "corruption"),
    "διερχομαι": ("dierchomai", "I pass through"),
    "δογματιζεσθε": ("dogmatizesthe", "you submit to decrees"),
    "δυναμουμενοι": ("dunamoumenoi", "being strengthened"),
    "δικαιον": ("dikaion", "righteous"),
    "δικαιωματα": ("dikaiomata", "ordinances"),
    "δικαιοσυνησ": ("dikaiosunes", "righteousness"),
    "δουλου": ("doulou", "servant"),
    "ηχμαλωτευθη": ("echmaloteuthe", "was taken captive"),
    "εδειραν": ("edeiran", "they beat"),
    "εθερισαντων": ("etherisanton", "having harvested"),
    "εθνων": ("ethnon", "nations"),
    "ειναι": ("einai", "to be"),
    "εισελθη": ("eiselthe", "enter"),
    "εισελθοντεσ": ("eiselthontes", "having entered"),
    "εκλεκτον": ("eklekton", "chosen"),
    "εκτησαμην": ("ektesamen", "I acquired"),
    "ελθοντεσ": ("elthontes", "having come"),
    "ελεημοσυνην": ("eleemosunen", "alms"),
    "θανατοσ": ("thanatos", "death"),
    "θανατου": ("thanatou", "death"),
    "θερισαντων": ("therisanton", "having harvested"),
    "θισβησ": ("thisbes", "Thisbe"),
    "και": ("kai", "and"),
    "καρδιαν": ("kardian", "heart"),
    "καρδιαισ": ("kardiais", "hearts"),
    "καταπατησετε": ("katapatesete", "you will trample"),
    "καταισχυνθη": ("kataischunthe", "be put to shame"),
    "καισαροσ": ("kaisaros", "Caesar"),
    "κεραια": ("keraia", "stroke of a letter"),
    "κτισισ": ("ktisis", "creation"),
    "λαλησει": ("lalesei", "he will speak"),
    "λεγω": ("lego", "I say"),
    "λογων": ("logon", "words"),
    "λυστροισ": ("lustrois", "Lystra"),
    "μακεδονιαν": ("makedonian", "Macedonia"),
    "μαριαμ": ("mariam", "Mary"),
    "μαριαν": ("marian", "Mary"),
    "μαρθαν": ("marthan", "Martha"),
    "ματταθα": ("mattatha", "Mattatha"),
    "μανθανουσι": ("manthanousi", "they learn"),
    "μετακαλεσομαι": ("metakalesomai", "I will summon"),
    "μια": ("mia", "one"),
    "μη": ("me", "not"),
    "μοι": ("moi", "to me"),
    "μωρα": ("mora", "foolish things"),
    "νεφθαλιμ": ("nephthalim", "Naphtali"),
    "νεανισκοι": ("neaniskoi", "young men"),
    "οδοισ": ("odois", "ways"),
    "ονον": ("onon", "donkey"),
    "αχρι": ("achri", "until"),
    "ευρειν": ("heurein", "to find"),
    "εξενεγκαντεσ": ("exenegkantes", "having carried out"),
    "ιππων": ("hippon", "horses"),
    "τετραρχουντοσ": ("tetrarchountos", "being tetrarch"),
    "τετρααρχουντοσ": ("tetraarchountos", "being tetrarch"),
    "παντα": ("panta", "all"),
    "παταξω": ("pataxo", "I will strike"),
    "παιδιον": ("paidion", "child"),
    "παντεσ": ("pantes", "all"),
    "παντων": ("panton", "of all"),
    "παρακλησισ": ("paraklesis", "comfort/encouragement"),
    "παραμενω": ("parameno", "I remain"),
    "παραμυθησωνται": ("paramuthesontai", "be comforted"),
    "παραμυθιον": ("paramuthion", "comfort"),
    "παρεδωκα": ("paredoka", "I delivered"),
    "παροιμιαν": ("paroimian", "figure of speech/proverb"),
    "πιλατου": ("pilatou", "Pilate"),
    "πνευμα": ("pneuma", "spirit"),
    "ποδασ": ("podas", "feet"),
    "πολιτειαν": ("politeian", "citizenship/commonwealth"),
    "πολλαισ": ("pollais", "many"),
    "πορευθητι": ("poreutheti", "go"),
    "πρασσοντεσ": ("prassontes", "practicing"),
    "πραυσ": ("praus", "gentle"),
    "πριν": ("prin", "before"),
    "προσ": ("pros", "toward"),
    "προσταγματα": ("prostagmata", "commandments"),
    "σπερματοσ": ("spermatos", "seed/descendant"),
    "σπουδασατε": ("spoudasate", "be diligent"),
    "στρατευομεθα": ("strateuometha", "we wage war"),
    "συνεκλεκτη": ("suneklekte", "co-elect"),
    "συνειδησεωσ": ("suneideseos", "conscience"),
    "σαλαθιηλ": ("salathiel", "Salathiel"),
    "σαβαωθ": ("sabaoth", "Sabaoth"),
    "στεφανον": ("stephanon", "crown"),
    "σιμων": ("simon", "Simon"),
    "σκανδαλον": ("skandalon", "stumbling block"),
    "ταρσεα": ("tarsea", "of Tarsus"),
    "ταλαιπωρια": ("talaiporia", "misery"),
    "τασ": ("tas", "the"),
    "ταυτη": ("taute", "to this/in this"),
    "τησ": ("tes", "of the"),
    "τη": ("te", "to the/in the"),
    "την": ("ten", "the"),
    "τιμη": ("time", "honor"),
    "τοισ": ("tois", "to the"),
    "του": ("tou", "of the"),
    "τουσ": ("tous", "the/those"),
    "τουτο": ("touto", "this"),
    "τοσουτον": ("tosouton", "so much"),
    "τωβιηλ": ("tobiel", "Tobiel"),
    "τωβιτ": ("tobit", "Tobit"),
    "υμιν": ("umin", "to you"),
    "υμεισ": ("umeis", "you"),
    "υμασ": ("umas", "you"),
    "υιον": ("uion", "son"),
    "υπερανω": ("uperano", "above"),
    "εμου": ("emou", "of me"),
    "εμοι": ("emoi", "to me"),
    "εν": ("en", "in"),
    "ενιαυτον": ("eniauton", "year"),
    "ει": ("ei", "if/you are"),
    "εισ": ("eis", "into/for"),
    "επι": ("epi", "on/upon"),
    "επτα": ("epta", "seven"),
    "επιβεβηκωσ": ("epibebekos", "having mounted"),
    "εσθιει": ("esthiei", "eats"),
    "εφη": ("ephe", "he said"),
    "εχετε": ("echete", "you have"),
    "εργα": ("erga", "works"),
    "εσχατη": ("eschate", "last"),
    "ευροντεσ": ("heurontes", "having found"),
    "ημεραισ": ("hemerais", "days"),
    "ηγεμονευοντοσ": ("egemoneuontos", "governing"),
    "ην": ("en", "was"),
    "ιδου": ("idou", "behold"),
    "ιδων": ("idon", "having seen"),
    "ινα": ("hina", "that"),
    "ιωτα": ("iota", "iota"),
    "οντεσ": ("ontes", "being"),
    "οιδαμεν": ("oidamen", "we know"),
    "ου": ("ou", "not"),
    "ουρανοισ": ("ouranois", "heavens"),
    "ουρανοσ": ("ouranos", "heaven"),
    "ουν": ("oun", "therefore"),
    "ουτε": ("oute", "nor"),
    "ωρασ": ("oras", "hour"),
    "ωσ": ("hos", "as"),
    "ωσπερ": ("hosper", "just as"),
    "ζωην": ("zoen", "life"),
    "ζησασα": ("zesasa", "having lived"),
    "χαιρει": ("chairei", "rejoices"),
    "χαιρειν": ("chairein", "greetings"),
    "χαλινων": ("chalinon", "bridles"),
    "χριστω": ("christo", "Christ"),
    "φαρισαιοσ": ("pharisaios", "Pharisee"),
    "αγγελου": ("aggelou", "angel"),
    "γωνιασ": ("gonias", "corner"),
    "καλουσα": ("kalousa", "calling"),
    "ישוע": ("Yeshua", "Yeshua/Jeshua"),
    "יהוה": ("YHWH", "YHWH"),
    "ישראל": ("Yisrael", "Israel"),
    "אלהים": ("Elohim", "God/Elohim"),
    "אדני": ("Adonai", "Lord"),
    "משיח": ("Mashiach", "Messiah/anointed one"),
    "גוג": ("Gog", "Gog"),
    "מגוג": ("Magog", "Magog"),
    "יוםיהוה": ("yom YHWH", "day of YHWH"),
    "יומיהוה": ("yom YHWH", "day of YHWH"),
    "היומיהוה": ("hayom YHWH", "the day of YHWH"),
    "ויהוה": ("ve-YHWH", "and YHWH"),
    "ליהוה": ("le-YHWH", "to/for YHWH"),
    "אור": ("or", "light"),
    "מות": ("mavet", "death"),
    "אמת": ("emet", "truth"),
    "משה": ("Moshe", "Moses"),
    "דוד": ("David", "David"),
    "מלך": ("melekh", "king"),
    "נח": ("Noach", "Noah"),
    "שם": ("Shem", "Shem"),
    "חם": ("Cham", "Ham"),
    "חת": ("Chet", "Heth"),
    "מש": ("Mash", "Mash"),
    "יון": ("Yavan", "Javan/Greece"),
    "ארם": ("Aram", "Aram"),
    "משא": ("Mesha", "Mesha"),
    "חוי": ("Chivvi", "Hivite"),
    "מדי": ("Madai", "Media"),
    "להבים": ("Lehabim", "Lehabim"),
    "נינוה": ("Nineveh", "Nineveh"),
    "אלישה": ("Elishah", "Elishah"),
    "לודים": ("Ludim", "Ludim"),
    "חוילה": ("Havilah", "Havilah"),
    "און": ("aven", "lawlessness/iniquity"),
    "בבל": ("Bavel", "Babylon"),
    "ירושלם": ("Yerushalem", "Jerusalem"),
    "ירושלים": ("Yerushalayim", "Jerusalem"),
    "ביתיהוה": ("beit YHWH", "house of YHWH"),
    "לביתיהוה": ("le-beit YHWH", "to the house of YHWH"),
    "בריתיהוה": ("berit YHWH", "covenant of YHWH"),
    "פרס": ("Paras", "Persia"),
    "חיה": ("chayah", "beast/living creature"),
    "חזון": ("chazon", "vision"),
    "דריוש": ("Daryavesh", "Darius"),
    "כורש": ("Koresh", "Cyrus"),
    "קרן": ("qeren", "horn"),
    "קרנ": ("qeren", "horn"),
    "נביא": ("navi", "prophet"),
    "כסא": ("kisse", "throne"),
    "ציון": ("Tziyon", "Zion"),
    "ציונ": ("Tziyon", "Zion"),
    "פסח": ("Pesach", "Passover"),
    "מלכות": ("malkhut", "kingdom"),
    "חבורה": ("chabburah", "stripe/wound"),
    "עון": ("avon", "iniquity"),
    "עונ": ("avon", "iniquity"),
    "שמע": ("shema", "hear"),
    "לחם": ("lechem", "bread"),
    "לחמ": ("lechem", "bread"),
    "ארץ": ("eretz", "earth/land"),
    "ארצ": ("eretz", "earth/land"),
    "עבד": ("eved", "servant"),
    "קבר": ("qever", "grave"),
    "רגם": ("ragam", "stone"),
    "רגמ": ("ragam", "stone"),
    "שמים": ("shamayim", "heavens"),
    "שמימ": ("shamayim", "heavens"),
    "ברזל": ("barzel", "iron"),
    "זהב": ("zahav", "gold"),
    "כסף": ("kesef", "silver"),
    "נחשת": ("nechoshet", "bronze/copper"),
    "חותם": ("chotam", "seal"),
    "אדון": ("adon", "lord/master"),
    "תו": ("tav", "mark/sign"),
    "תנין": ("tannin", "dragon/sea monster"),
    "עד": ("ed", "witness"),
    "צר": ("tsar", "foe/adversary"),
    "ענן": ("anan", "cloud"),
    "יין": ("yayin", "wine"),
    "יהודה": ("Yehudah", "Judah"),
    "חסד": ("chesed", "mercy/steadfast love"),
    "יעקב": ("Yaakov", "Jacob"),
    "צדק": ("tzedek", "righteousness/Jupiter"),
    "שלמה": ("Shlomo", "Solomon"),
    "שלל": ("shalal", "spoil/plunder"),
    "ספר": ("sefer", "book/Sephar"),
    "שממה": ("shemamah", "desolation"),
    "קדש": ("qodesh", "holiness/sacred"),
    "נפש": ("nefesh", "soul/life"),
    "דבר": ("davar", "word/matter"),
    "שטה": ("shittah", "acacia"),
    "חוכמה": ("chokhmah", "wisdom"),
    "ערומימ": ("arumim", "crafty/shrewd"),
    "במרומימ": ("ba-meromim", "in the heights"),
    "מצרימ": ("Mitzrayim", "Egypt"),
    "במשא": ("be-massa", "in bearing/song service"),
    "המשררימ": ("ha-meshorerim", "the singers"),
    "ישבו": ("yashvu", "they dwelt/sat"),
    "איש": ("ish", "man"),
    "בנהדד": ("Ben-Hadad", "Ben-Hadad"),
    "ואתהמזרקות": ("ve-et ha-mizraqot", "and the basins"),
    "אתכמ": ("etkhem", "you"),
    "עליכ": ("alekha", "upon you"),
    "ארבעה": ("arbaah", "four"),
    "אתשמו": ("et shemo", "his name"),
    "ויקמ": ("vayaqom", "and he arose"),
    "זכרנא": ("zekhor na", "remember, please"),
    "לענות": ("la-anot", "to answer/afflict"),
    "תזעק": ("tizak", "she cries out"),
    "יפתה": ("yifteh", "will be enticed"),
    "שיפוח": ("she-yafuach", "until it breathes/blows"),
    "בתוכ": ("betokh", "in the midst"),
    "לעלה": ("le-olah", "for a burnt offering"),
    "בנישראל": ("bnei Yisrael", "children of Israel"),
    "הדבר": ("ha-davar", "the word/matter"),
    "שבה": ("shuvah", "return"),
    "כה": ("koh", "thus"),
    "ושבעימ": ("ve-shivim", "and seventy"),
    "ושנימ": ("ve-shenayim", "and two"),
    "עלהשמימ": ("alah shamayim", "went up to heaven"),
}

TERM_FILES_DIR = Path(__file__).resolve().parents[1] / "terms"

GREEK_MAP = {
    "α": "a",
    "β": "b",
    "γ": "g",
    "δ": "d",
    "ε": "e",
    "ζ": "z",
    "η": "e",
    "θ": "th",
    "ι": "i",
    "κ": "k",
    "λ": "l",
    "μ": "m",
    "ν": "n",
    "ξ": "x",
    "ο": "o",
    "π": "p",
    "ρ": "r",
    "σ": "s",
    "ς": "s",
    "τ": "t",
    "υ": "u",
    "φ": "ph",
    "χ": "ch",
    "ψ": "ps",
    "ω": "o",
}

HEBREW_MAP = {
    "א": "",
    "ב": "b",
    "ג": "g",
    "ד": "d",
    "ה": "h",
    "ו": "w",
    "ז": "z",
    "ח": "ch",
    "ט": "t",
    "י": "y",
    "כ": "k",
    "ך": "k",
    "ל": "l",
    "מ": "m",
    "ם": "m",
    "נ": "n",
    "ן": "n",
    "ס": "s",
    "ע": "",
    "פ": "p",
    "ף": "p",
    "צ": "ts",
    "ץ": "ts",
    "ק": "q",
    "ר": "r",
    "ש": "sh",
    "ת": "t",
}


def display_term(value: str, *, english: str | None = None, transliteration: str | None = None) -> str:
    """Return a Markdown display string with transliteration and English gloss when useful."""
    text = value.strip()
    if not text:
        return ""
    if not (contains_hebrew(text) or contains_greek(text)):
        return f"`{text}`"

    key = normalized_script_key(text)
    known_transliteration, fallback_english = known_term_display(key)
    transliteration = transliteration or known_transliteration or transliterate(text)
    gloss = english or fallback_english
    if gloss:
        return f"`{text}` ({transliteration}; English: {gloss})"
    return f"`{text}` ({transliteration})"


def known_term_display(key: str) -> tuple[str, str]:
    """Return display metadata for a normalized script key."""
    if key in KNOWN_TERMS:
        return KNOWN_TERMS[key]
    return csv_known_terms().get(key, ("", ""))


@lru_cache(maxsize=1)
def csv_known_terms() -> dict[str, tuple[str, str]]:
    """Load unambiguous Hebrew/Greek term concepts from committed term CSVs.

    Report builders often only have a normalized term value by the time they
    render Markdown. This fallback keeps those searched terms reader-facing
    without guessing for ambiguous duplicate entries.
    """
    if not TERM_FILES_DIR.exists():
        return {}

    concepts_by_key: dict[str, set[str]] = {}
    for path in sorted(TERM_FILES_DIR.glob("*.csv")):
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    term = row.get("term", "").strip()
                    concept = row.get("concept", "").strip()
                    if not term or not concept:
                        continue
                    if not (contains_hebrew(term) or contains_greek(term)):
                        continue
                    key = normalized_script_key(term)
                    if key:
                        concepts_by_key.setdefault(key, set()).add(concept)
        except (OSError, csv.Error, UnicodeDecodeError):
            continue

    return {key: ("", sorted(concepts)[0]) for key, concepts in concepts_by_key.items() if len(concepts) == 1}


def display_center(ref: str, center_word: str) -> str:
    if contains_hebrew(center_word) or contains_greek(center_word):
        return " ".join(part for part in [ref, display_term(center_word)] if part)
    return " ".join(part for part in [ref, center_word] if part)


def contains_hebrew(value: str) -> bool:
    return any("\u0590" <= char <= "\u05ff" for char in value)


def contains_greek(value: str) -> bool:
    return any("\u0370" <= char <= "\u03ff" or "\u1f00" <= char <= "\u1fff" for char in value)


def transliterate(value: str) -> str:
    key = normalized_script_key(value)
    if contains_greek(value):
        return "".join(GREEK_MAP.get(char, char if char.isspace() else "") for char in key).strip()
    if contains_hebrew(value):
        return "".join(HEBREW_MAP.get(char, char if char.isspace() else "") for char in key).strip()
    return value


def normalized_script_key(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.lower())
    chars = []
    for char in decomposed:
        if unicodedata.combining(char):
            continue
        if char == "ς":
            chars.append("σ")
        elif ("\u0590" <= char <= "\u05ff" or "\u0370" <= char <= "\u03ff") and (
            unicodedata.category(char).startswith("L")
        ):
            chars.append(char)
    return "".join(chars)
