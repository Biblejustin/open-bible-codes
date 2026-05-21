#!/usr/bin/env python3
"""Build user-requested Greek and Hebrew prospective term files."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

from els.normalization import normalize_text


GREEK_OUT = Path("terms/greek_surface_new_terms.csv")
HEBREW_OUT = Path("terms/compound_extension_prospective_terms.csv")

SOURCE = "user requested 2026-05-21 before result-producing prospective run"

USER_GREEK_TERMS = """
θεός, κύριος, Ἰησοῦς, χριστός, πνεῦμα, ψυχή, ζωή, λόγος,
εὐαγγέλιον, ἀγάπη, πίστις, δικαιοσύνη, νόμος, χάρις, ἁμαρτία,
μετάνοια, ἀνάστασις, ἐκκλησία, διαθήκη, σοφία, δόξα, ἄγγελος,
ἀλήθεια, εἰρήνη, ἐλπίς, φῶς, σκότος, σωτηρία, σάρξ, ἔλεος,
αἷμα, βασιλεία, βασιλεύς, ἱερεύς, ναός, θυσιαστήριον, θυσία,
ἀμνός, πρόβατον, ποιμήν, δοῦλος, υἱός, πατήρ, ἀδελφός, γυνή,
ἄνθρωπος, καρδία, νοῦς, στόμα, χείρ, πρόσωπον, ὄνομα, ἅγιος,
καθαρός, ἀκάθαρτος, πονηρός, ἀγαθός, θάνατος, ᾅδης, πῦρ, ὕδωρ,
ἄρτος, οἶνος, ἔλαιον, κρίνω, ὀργή, φόβος, χαρά, προσευχή,
προσκυνέω, αἰνέω, εὐλογία, κατάρα, ἐντολή, διδαχή, μαθητής,
προφήτης, ἀπόστολος, πρεσβύτερος, μυστήριον, δύναμις, ἐξουσία,
σημεῖον, ἔργον, κόσμος, οὐρανός, γῆ, θάλασσα, ὄρος, ἔρημος,
πόλις, Ἰερουσαλήμ, Ἰσραήλ, Ἰούδα, Σιών, Αἴγυπτος, Βαβυλών,
Δαυίδ, Μωυσῆς, Ἀβραάμ, σπέρμα, ἐπαγγελία, κληρονομία, ἀρχή,
ἡμέρα, νύξ, πρωΐ, ἑσπέρα, σάββατον, πάσχα, ἑορτή, νηστεία,
βάπτισμα, ἄφεσις, λύτρωσις, ἱλαστήριον, σταυρός, στέφανος,
θρόνος, βῆμα, παραβολή, θεραπεία, νόσος, τυφλός, πτωχός,
πλούσιος, χήρα, ὀρφανός, ξένος, ἐχθρός, φίλος, νύμφη, νυμφίος,
γάμος, οἶκος, τέκνον, μήτηρ, θυγάτηρ, παρθένος, γέννησις, κτίσις,
καινός, παλαιός, ὁδός, πύλη, πέτρα, λίθος, ξύλον, καρπός, ἄμπελος,
θερισμός, ἀγρός, μάχαιρα, θυρεός, σάλπιγξ, βίβλος, σφραγίς,
ἀστήρ, ἥλιος, σελήνη, νεφέλη, ὑετός, ποταμός, πηγή, φρέαρ, φυλακή,
πύργος, χρυσός, ἄργυρος, εἴδωλον, εἰκών, δαιμόνιον, διάβολος,
Σατανᾶς, δράκων, ὄφις, θηρίον, χάραγμα, ἀριθμός, μάρτυς, μαρτυρία,
γνῶσις, σύνεσις, βουλή, θέλημα, ἐκλεκτός, κλῆσις, ἁγιασμός,
δικαίωσις, υἱοθεσία, κοινωνία, καταλλαγή, πειρασμός, ὑπομονή,
μακροθυμία, πραΰτης, ταπεινοφροσύνη, ὑπερηφανία, ἐγκράτεια, μέθη,
φθόνος, ἔρις, μῖσος, ἐπιθυμία, πορνεία, μοιχεία, φόνος, κλοπή,
ψεῦδος, δόλος, ὑπόκρισις, βλασφημία, γραφή, ψαλμός, προφητεία,
ὅρασις, ἐνύπνιον, ὅρκος, εὐχή, σκηνή, κιβωτός, καταπέτασμα,
θυμίαμα, ὁλοκαύτωμα, δεκάτη, ἀπαρχή, ἄζυμος, περιτομή, ῥάβδος,
γραμματεύς, Φαρισαῖος, Σαδδουκαῖος, τελώνης, ἑκατόνταρχος,
στρατιώτης, ἡγεμών, Καῖσαρ, βασίλισσα, φυλή, λαός, ἔθνος, Ῥώμη,
Γαλιλαία, Σαμάρεια, Ἰορδάνης, Βηθλεέμ, Ναζαρέτ, Χαναάν, Ἀσσυρία,
Μωάβ, Ἐδώμ, Φυλιστιίμ, Ἕλλην, Δαμασκός, Νινευή, Σόδομα, Γόμορρα,
ζῷον, πετεινόν, ἰχθύς, ἑρπετόν, χόρτος, ἄνθος, γάλα, μέλι, ἅλας,
ζύμη, ποτήριον, λύχνος, λυχνία, ἱμάτιον, κεφαλή, ὀφθαλμός, πούς,
οὖς, φωνή, κραυγή, ᾠδή, ὕπνος, μέτρον, στάθμιον, πόλεμος, στρατιά,
τόξον, λόγχη, ἅρμα, ἵππος, αἰχμαλωσία, λιμός, πληγή, σεισμός,
ἄβυσσος, λάκκος, λίμνη, ἀπώλεια, ἐκδίκησις, φιάλη, ἱππεύς, κέρας,
μεσίτης, εὐαγγελιστής, ἐπίσκοπος, διάκονος, λειτουργός, οἰκονόμος,
διδάσκαλος, ῥαββί, συναγωγή, πλησίον, θλῖψις, διωγμός, παράκλησις,
σπλάγχνον, ἐλεημοσύνη, φιλοξενία, σῶμα, ἔτος, ὥρα, καιρός, χρόνος,
τιμή, ἀνήρ, βρέφος, νεανίας, κύων, ῥίζα, ἄνεμος, σκιά, θύρα, κώμη,
δῶρον, μισθός, τροφή, σῖτος, συκῆ, κρίνον, κλίνη, σάκκος, σανδάλιον,
γλῶσσα, χείλος, θρίξ, ὀστοῦν, κοιλία, δάκτυλος, γόνυ, πτέρυξ,
συνείδησις, λύπη, παράπτωμα, ἀνομία, πονηρία, ἀπιστία, μωρία,
σκάνδαλον, πλεονεξία, ζῆλος, μέριμνα, πνευματικός, ἐλευθερία,
δουλεία, ἀποκάλυψις, παρρησία
"""

GOSPEL_GREEK_NAMES = [
    ("jesus_g", "Jesus", "gospel_core_names", "Ἰησοῦς"),
    ("mary_mother_g", "Mary mother of Jesus / Mary of Bethany", "gospel_women", "Μαρία"),
    ("mary_magdalene_g", "Mary Magdalene", "gospel_women", "Μαρία Μαγδαληνή"),
    ("mary_of_clopas_g", "Mary of Clopas", "gospel_women", "Μαρία Κλωπᾶ"),
    ("mary_of_bethany_g", "Mary of Bethany", "gospel_women", "Μαρία"),
    ("martha_g", "Martha", "gospel_women", "Μάρθα"),
    ("elizabeth_g", "Elizabeth", "gospel_women", "Ἐλισάβετ"),
    ("anna_prophetess_g", "Anna prophetess", "gospel_women", "Ἄννα"),
    ("joanna_g", "Joanna", "gospel_women", "Ἰωάννα"),
    ("susanna_g", "Susanna", "gospel_women", "Σουσάννα"),
    ("salome_g", "Salome", "gospel_women", "Σαλώμη"),
    ("herodias_g", "Herodias", "gospel_women", "Ἡρῳδιάς"),
    ("tamar_g", "Tamar", "christ_genealogy", "Θάμαρ"),
    ("rahab_g", "Rahab", "christ_genealogy", "Ῥαχάβ"),
    ("ruth_g", "Ruth", "christ_genealogy", "Ῥούθ"),
    ("bathsheba_g", "Wife of Uriah", "christ_genealogy", "Οὐρίου"),
    ("joseph_husband_mary_g", "Joseph husband of Mary / Joseph of Arimathea", "christ_genealogy", "Ἰωσήφ"),
    ("abraham_g", "Abraham", "christ_genealogy", "Ἀβραάμ"),
    ("isaac_g", "Isaac", "christ_genealogy", "Ἰσαάκ"),
    ("jacob_g", "Jacob", "christ_genealogy", "Ἰακώβ"),
    ("judah_g", "Judah", "christ_genealogy", "Ἰούδας"),
    ("perez_g", "Perez", "christ_genealogy", "Φαρές"),
    ("hezron_g", "Hezron", "christ_genealogy", "Ἑσρώμ"),
    ("ram_g", "Ram", "christ_genealogy", "Ἀράμ"),
    ("amminadab_g", "Amminadab", "christ_genealogy", "Ἀμιναδάβ"),
    ("nahshon_g", "Nahshon", "christ_genealogy", "Ναασσών"),
    ("salmon_g", "Salmon", "christ_genealogy", "Σαλμών"),
    ("boaz_g", "Boaz", "christ_genealogy", "Βοές"),
    ("obed_g", "Obed", "christ_genealogy", "Ἰωβήδ"),
    ("jesse_g", "Jesse", "christ_genealogy", "Ἰεσσαί"),
    ("david_g", "David", "christ_genealogy", "Δαυίδ"),
    ("solomon_g", "Solomon", "christ_genealogy", "Σολομών"),
    ("rehoboam_g", "Rehoboam", "christ_genealogy", "Ῥοβοάμ"),
    ("abijah_g", "Abijah", "christ_genealogy", "Ἀβιά"),
    ("asa_g", "Asa", "christ_genealogy", "Ἀσά"),
    ("jehoshaphat_g", "Jehoshaphat", "christ_genealogy", "Ἰωσαφάτ"),
    ("joram_g", "Joram", "christ_genealogy", "Ἰωράμ"),
    ("uzziah_g", "Uzziah", "christ_genealogy", "Ὀζίας"),
    ("jotham_g", "Jotham", "christ_genealogy", "Ἰωαθάμ"),
    ("ahaz_g", "Ahaz", "christ_genealogy", "Ἄχαζ"),
    ("hezekiah_g", "Hezekiah", "christ_genealogy", "Ἑζεκίας"),
    ("manasseh_g", "Manasseh", "christ_genealogy", "Μανασσῆς"),
    ("amos_g", "Amos/Amon", "christ_genealogy", "Ἀμώς"),
    ("josiah_g", "Josiah", "christ_genealogy", "Ἰωσίας"),
    ("jeconiah_g", "Jeconiah", "christ_genealogy", "Ἰεχονίας"),
    ("shealtiel_g", "Shealtiel", "christ_genealogy", "Σαλαθιήλ"),
    ("zerubbabel_g", "Zerubbabel", "christ_genealogy", "Ζοροβάβελ"),
    ("abiud_g", "Abiud", "christ_genealogy", "Ἀβιούδ"),
    ("eliakim_genealogy_g", "Eliakim", "christ_genealogy", "Ἐλιακείμ"),
    ("azor_g", "Azor", "christ_genealogy", "Ἀζώρ"),
    ("zadok_g", "Zadok", "christ_genealogy", "Σαδώκ"),
    ("achim_g", "Achim", "christ_genealogy", "Ἀχείμ"),
    ("eliud_g", "Eliud", "christ_genealogy", "Ἐλιούδ"),
    ("eleazar_g", "Eleazar", "christ_genealogy", "Ἐλεάζαρ"),
    ("matthan_g", "Matthan", "christ_genealogy", "Ματθάν"),
    ("heli_g", "Heli", "christ_genealogy", "Ἡλί"),
    ("matthat_g", "Matthat", "christ_genealogy", "Ματθάτ"),
    ("levi_genealogy_g", "Levi", "christ_genealogy", "Λευί"),
    ("melchi_g", "Melchi", "christ_genealogy", "Μελχί"),
    ("jannai_g", "Jannai", "christ_genealogy", "Ἰανναί"),
    ("zachariah_g", "Zachariah", "gospel_people", "Ζαχαρίας"),
    ("john_baptist_g", "John the Baptist / John son of Zebedee", "gospel_people", "Ἰωάννης"),
    ("simeon_g", "Simeon", "gospel_people", "Συμεών"),
    ("lazarus_g", "Lazarus", "gospel_people", "Λάζαρος"),
    ("nicodemus_g", "Nicodemus", "gospel_people", "Νικόδημος"),
    ("joseph_arimathea_g", "Joseph of Arimathea", "gospel_people", "Ἰωσήφ"),
    ("caiaphas_g", "Caiaphas", "gospel_people", "Καϊάφας"),
    ("annas_g", "Annas", "gospel_people", "Ἅννας"),
    ("herod_g", "Herod", "gospel_people", "Ἡρῴδης"),
    ("pilate_g", "Pilate", "gospel_people", "Πιλᾶτος"),
    ("barabbas_g", "Barabbas", "gospel_people", "Βαραββᾶς"),
    ("simon_cyrene_g", "Simon of Cyrene", "gospel_people", "Σίμων Κυρηναῖος"),
    ("cleopas_g", "Cleopas", "gospel_people", "Κλεοπᾶς"),
    ("bartimaeus_g", "Bartimaeus", "gospel_people", "Βαρτιμαῖος"),
    ("zacchaeus_g", "Zacchaeus", "gospel_people", "Ζακχαῖος"),
    ("simon_peter_g", "Simon Peter", "disciples", "Σίμων Πέτρος"),
    ("andrew_g", "Andrew", "disciples", "Ἀνδρέας"),
    ("james_zebedee_g", "James son of Zebedee", "disciples", "Ἰάκωβος"),
    ("john_zebedee_g", "John son of Zebedee", "disciples", "Ἰωάννης"),
    ("philip_g", "Philip", "disciples", "Φίλιππος"),
    ("bartholomew_g", "Bartholomew", "disciples", "Βαρθολομαῖος"),
    ("thomas_g", "Thomas", "disciples", "Θωμᾶς"),
    ("matthew_g", "Matthew", "disciples", "Ματθαῖος"),
    ("james_alphaeus_g", "James son of Alphaeus", "disciples", "Ἰάκωβος"),
    ("thaddaeus_g", "Thaddaeus", "disciples", "Θαδδαῖος"),
    ("simon_zealot_g", "Simon the Zealot", "disciples", "Σίμων"),
    ("judas_iscariot_g", "Judas Iscariot", "disciples", "Ἰούδας Ἰσκαριώτης"),
]

HEBREW_TERMS = [
    ("jesus_h", "Jesus/Yeshua", "gospel_core_names", "ישוע"),
    ("christ_messiah_h", "Christ/Messiah", "gospel_core_names", "משיח"),
    ("mary_h", "Mary", "gospel_women", "מרים"),
    ("mary_magdalene_h", "Mary Magdalene", "gospel_women", "מרים מגדלית"),
    ("martha_h", "Martha", "gospel_women", "מרתא"),
    ("elizabeth_h", "Elizabeth", "gospel_women", "אלישבע"),
    ("anna_h", "Anna/Hannah", "gospel_women", "חנה"),
    ("joanna_h", "Joanna", "gospel_women", "יוחנה"),
    ("susanna_h", "Susanna", "gospel_women", "שושנה"),
    ("salome_h", "Salome", "gospel_women", "שלומית"),
    ("tamar_h", "Tamar", "christ_genealogy", "תמר"),
    ("rahab_h", "Rahab", "christ_genealogy", "רחב"),
    ("ruth_h", "Ruth", "christ_genealogy", "רות"),
    ("bathsheba_h", "Bathsheba", "christ_genealogy", "בת שבע"),
    ("joseph_h", "Joseph husband of Mary / Joseph of Arimathea", "christ_genealogy", "יוסף"),
    ("abraham_h", "Abraham", "christ_genealogy", "אברהם"),
    ("isaac_h", "Isaac", "christ_genealogy", "יצחק"),
    ("jacob_h", "Jacob/James", "christ_genealogy", "יעקב"),
    ("judah_h", "Judah", "christ_genealogy", "יהודה"),
    ("perez_h", "Perez", "christ_genealogy", "פרץ"),
    ("hezron_h", "Hezron", "christ_genealogy", "חצרון"),
    ("ram_h", "Ram", "christ_genealogy", "רם"),
    ("amminadab_h", "Amminadab", "christ_genealogy", "עמינדב"),
    ("nahshon_h", "Nahshon", "christ_genealogy", "נחשון"),
    ("salmon_h", "Salmon", "christ_genealogy", "שלמון"),
    ("boaz_h", "Boaz", "christ_genealogy", "בעז"),
    ("obed_h", "Obed", "christ_genealogy", "עובד"),
    ("jesse_h", "Jesse", "christ_genealogy", "ישי"),
    ("david_h", "David", "christ_genealogy", "דוד"),
    ("solomon_h", "Solomon", "christ_genealogy", "שלמה"),
    ("rehoboam_h", "Rehoboam", "christ_genealogy", "רחבעם"),
    ("abijah_h", "Abijah", "christ_genealogy", "אביה"),
    ("asa_h", "Asa", "christ_genealogy", "אסא"),
    ("jehoshaphat_h", "Jehoshaphat", "christ_genealogy", "יהושפט"),
    ("joram_h", "Joram", "christ_genealogy", "יורם"),
    ("uzziah_h", "Uzziah", "christ_genealogy", "עזיה"),
    ("jotham_h", "Jotham", "christ_genealogy", "יותם"),
    ("ahaz_h", "Ahaz", "christ_genealogy", "אחז"),
    ("hezekiah_h", "Hezekiah", "christ_genealogy", "חזקיה"),
    ("manasseh_h", "Manasseh", "christ_genealogy", "מנשה"),
    ("amos_h", "Amos/Amon", "christ_genealogy", "אמון"),
    ("josiah_h", "Josiah", "christ_genealogy", "יאשיה"),
    ("jeconiah_h", "Jeconiah", "christ_genealogy", "יכניה"),
    ("shealtiel_h", "Shealtiel", "christ_genealogy", "שאלתיאל"),
    ("zerubbabel_h", "Zerubbabel", "christ_genealogy", "זרובבל"),
    ("eliakim_h", "Eliakim", "christ_genealogy", "אליקים"),
    ("eleazar_h", "Eleazar/Lazarus", "christ_genealogy", "אלעזר"),
    ("matthan_h", "Matthan", "christ_genealogy", "מתן"),
    ("john_h", "John", "gospel_people", "יוחנן"),
    ("zachariah_h", "Zachariah", "gospel_people", "זכריה"),
    ("simeon_h", "Simeon", "gospel_people", "שמעון"),
    ("lazarus_h", "Lazarus", "gospel_people", "אלעזר"),
    ("nicodemus_h", "Nicodemus", "gospel_people", "נקדימון"),
    ("caiaphas_h", "Caiaphas", "gospel_people", "קיפא"),
    ("annas_h", "Annas", "gospel_people", "חנן"),
    ("herod_h", "Herod", "gospel_people", "הורדוס"),
    ("pilate_h", "Pilate", "gospel_people", "פילטוס"),
    ("barabbas_h", "Barabbas", "gospel_people", "בר אבא"),
    ("simon_cyrene_h", "Simon of Cyrene", "gospel_people", "שמעון הקירני"),
    ("cleopas_h", "Cleopas", "gospel_people", "קלופס"),
    ("zacchaeus_h", "Zacchaeus", "gospel_people", "זכי"),
    ("simon_peter_h", "Simon Peter", "disciples", "שמעון פטרוס"),
    ("andrew_h", "Andrew", "disciples", "אנדרי"),
    ("james_h", "James", "disciples", "יעקב"),
    ("philip_h", "Philip", "disciples", "פיליפוס"),
    ("bartholomew_h", "Bartholomew", "disciples", "ברתולמי"),
    ("thomas_h", "Thomas", "disciples", "תומא"),
    ("matthew_h", "Matthew", "disciples", "מתתיה"),
    ("thaddaeus_h", "Thaddaeus", "disciples", "תדי"),
    ("judas_iscariot_h", "Judas Iscariot", "disciples", "יהודה איש קריות"),
]


@dataclass(frozen=True)
class Term:
    term_id: str
    concept: str
    category: str
    language: str
    term: str
    notes: str


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    greek_terms = build_greek_terms()
    hebrew_terms = build_hebrew_terms()
    write_terms(args.greek_out, greek_terms)
    write_terms(args.hebrew_out, hebrew_terms)
    print(f"{args.greek_out}: {len(greek_terms)}")
    print(f"{args.hebrew_out}: {len(hebrew_terms)}")
    return 0


def parser() -> argparse.ArgumentParser:
    parse = argparse.ArgumentParser()
    parse.add_argument("--greek-out", type=Path, default=GREEK_OUT)
    parse.add_argument("--hebrew-out", type=Path, default=HEBREW_OUT)
    return parse


def build_greek_terms() -> list[Term]:
    rows: list[Term] = []
    seen: set[str] = set()
    seen_ids: set[str] = set()
    for term_id, concept, category, raw in GOSPEL_GREEK_NAMES:
        normalized = normalize_text(raw, "greek")
        if not normalized or normalized in seen:
            continue
        unique_id = f"user_{term_id}"
        if unique_id in seen_ids:
            continue
        seen.add(normalized)
        seen_ids.add(unique_id)
        rows.append(
            Term(
                term_id=unique_id,
                concept=concept,
                category=category,
                language="greek",
                term=raw,
                notes=SOURCE,
            )
        )
    for index, raw in enumerate(split_user_terms(USER_GREEK_TERMS), start=1):
        normalized = normalize_text(raw, "greek")
        if not normalized or normalized in seen:
            continue
        unique_id = f"user_greek_term_{index:03d}_g"
        if unique_id in seen_ids:
            continue
        seen.add(normalized)
        seen_ids.add(unique_id)
        rows.append(
            Term(
                term_id=unique_id,
                concept=raw,
                category="user_supplied_greek_terms",
                language="greek",
                term=raw,
                notes=SOURCE,
            )
        )
    return rows


def build_hebrew_terms() -> list[Term]:
    rows: list[Term] = []
    seen: set[str] = set()
    seen_ids: set[str] = set()
    for term_id, concept, category, raw in HEBREW_TERMS:
        normalized = normalize_text(raw, "hebrew")
        if not normalized or normalized in seen:
            continue
        unique_id = f"user_{term_id}"
        if unique_id in seen_ids:
            continue
        seen.add(normalized)
        seen_ids.add(unique_id)
        rows.append(
            Term(
                term_id=unique_id,
                concept=concept,
                category=category,
                language="hebrew",
                term=raw,
                notes=SOURCE,
            )
        )
    return rows


def split_user_terms(raw: str) -> list[str]:
    return [part.strip() for part in raw.replace("\n", " ").split(",") if part.strip()]


def write_terms(path: Path, terms: list[Term]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["term_id", "concept", "category", "language", "term", "notes"],
            lineterminator="\n",
        )
        writer.writeheader()
        for term in terms:
            writer.writerow(term.__dict__)


if __name__ == "__main__":
    raise SystemExit(main())
