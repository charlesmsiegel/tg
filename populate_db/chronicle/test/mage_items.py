"""
Mage item population script for Seattle Test Chronicle.

Creates Libraries and Grimoires for Chantries.
"""

from accounts.models import Profile
from characters.models.mage.faction import MageFaction
from characters.models.mage.sphere import Sphere
from core.models import Language
from game.models import Chronicle
from items.models.mage import Grimoire
from locations.models.mage import Chantry, Library


def populate_mage_items():
    """Create Libraries and Grimoires for mage chantries."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # Get factions
    order_of_hermes = MageFaction.objects.get(name="Order of Hermes")
    akashic = MageFaction.objects.get(name="Akashayana")
    celestial_chorus = MageFaction.objects.get(name="Celestial Chorus")
    virtual_adepts = MageFaction.objects.get(name="Virtual Adepts")
    technocracy = MageFaction.objects.get(name="Technocratic Union")
    progenitors = MageFaction.objects.get(name="Progenitors")
    nwo = MageFaction.objects.get(name="New World Order")
    verbena = MageFaction.objects.get(name="Verbena")
    euthanatos = MageFaction.objects.get(name="Euthanatos")
    cult_of_ecstasy = MageFaction.objects.get(name="Cult of Ecstasy")

    # Get spheres
    forces = Sphere.objects.get(name="Forces")
    prime = Sphere.objects.get(name="Prime")
    spirit = Sphere.objects.get(name="Spirit")
    mind = Sphere.objects.get(name="Mind")
    life = Sphere.objects.get(name="Life")
    correspondence = Sphere.objects.get(name="Correspondence")
    time = Sphere.objects.get(name="Time")
    entropy = Sphere.objects.get(name="Entropy")
    matter = Sphere.objects.get(name="Matter")

    # Get languages
    latin, _ = Language.objects.get_or_create(name="Latin", defaults={"frequency": 50})
    english, _ = Language.objects.get_or_create(
        name="English", defaults={"frequency": 100}
    )
    greek, _ = Language.objects.get_or_create(name="Greek", defaults={"frequency": 40})
    sanskrit, _ = Language.objects.get_or_create(
        name="Sanskrit", defaults={"frequency": 30}
    )
    chinese, _ = Language.objects.get_or_create(
        name="Chinese", defaults={"frequency": 60}
    )
    arabic, _ = Language.objects.get_or_create(name="Arabic", defaults={"frequency": 45})
    hebrew, _ = Language.objects.get_or_create(name="Hebrew", defaults={"frequency": 35})

    # Get chantries
    cross_house = Chantry.objects.get(name="The Cross House", chronicle=chronicle)
    temple_inner_light = Chantry.objects.get(
        name="The Temple of Inner Light", chronicle=chronicle
    )
    digital_sanctum = Chantry.objects.get(
        name="The Digital Sanctum", chronicle=chronicle
    )
    prometheus_labs = Chantry.objects.get(name="Prometheus Labs", chronicle=chronicle)
    hayes_tower = Chantry.objects.get(name="Hayes Tower", chronicle=chronicle)

    # =========================================================================
    # CROSS HOUSE LIBRARY
    # =========================================================================

    cross_library, created = Library.objects.get_or_create(
        name="Cross House Library",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The primary library of Seattle's Tradition Chantry, maintained
by the Order of Hermes but accessible to all Tradition members. The collection spans
centuries and includes rare grimoires, historical texts, and practical manuals from
multiple Traditions.

The library occupies what appears to be a single large room, but Hermetic spatial magic
allows access to additional wings that exist in expanded space. Finding specific texts
requires understanding the cataloging system, which follows Hermetic principles rather
than any mundane organizational scheme.

Theodore Barnes, a Companion, serves as the primary librarian and can guide researchers
to relevant materials.""",
            "rank": 4,
            "faction": order_of_hermes,
            "parent": cross_house,
        },
    )
    if created:
        print(f"  Created Library: {cross_library.name}")

    # Grimoires for Cross House Library
    grimoires_data = [
        {
            "name": "Liber Lucis Hermeticae",
            "description": """A foundational text of Hermetic theory, written in Latin by
a Bonisagus magus in the 12th century. The grimoire covers Prime and Forces, explaining
the fundamental relationships between magical energy and elemental forces.

The leather-bound tome is illuminated with gold leaf and contains numerous diagrams
of ritual circles. Margin notes from generations of readers add practical insights
to the theoretical framework.""",
            "faction": order_of_hermes,
            "rank": 4,
            "language": latin,
            "date_written": 1150,
            "spheres": [prime, forces],
            "is_primer": False,
        },
        {
            "name": "The Unified Field Workbook",
            "description": """A modern compilation of Virtual Adept techniques for
manipulating Correspondence through digital interfaces. Written in accessible English
with code examples, this grimoire bridges Hermetic theory with practical hacking.

The text exists primarily as a heavily encrypted file, though a printed backup copy
resides in the library. The author, known only as "Zero Cool," updates the digital
version periodically with new techniques.""",
            "faction": virtual_adepts,
            "rank": 3,
            "language": english,
            "date_written": 2015,
            "spheres": [correspondence],
            "is_primer": False,
        },
        {
            "name": "Whispers from the Wheel",
            "description": """A Euthanatos text on Entropy and the nature of fate, written
by an Indian Thanatoic master. The grimoire uses poetic metaphor extensively, requiring
contemplation rather than linear study.

The pages are thin rice paper bound between carved bone covers. The text describes
techniques for reading the patterns of destiny and, when necessary, cutting threads
that have become tangled beyond repair.""",
            "faction": euthanatos,
            "rank": 3,
            "language": sanskrit,
            "date_written": 1780,
            "spheres": [entropy],
            "is_primer": False,
        },
        {
            "name": "Covenstead Chronicles",
            "description": """A Verbena teaching text covering Life magic through the
lens of seasonal cycles and natural processes. The grimoire emphasizes practical
applications: healing, shapeshifting, and communion with living things.

Written on vellum with pressed flowers marking important passages, this text has
been copied and expanded by Verbena practitioners for three centuries. The current
version includes insertions from multiple authors.""",
            "faction": verbena,
            "rank": 3,
            "language": english,
            "date_written": 1720,
            "spheres": [life],
            "is_primer": False,
        },
        {
            "name": "The Primer of Prime",
            "description": """An introductory text on Prime magic, designed to help newly
Awakened mages understand the fundamental nature of magical energy. The language is
deliberately simple, avoiding Tradition-specific jargon.

The grimoire covers basic quintessence manipulation, sensing magical energies, and
the dangers of Paradox. Multiple editions exist, each updated to address contemporary
paradigms.""",
            "faction": order_of_hermes,
            "rank": 2,
            "language": english,
            "date_written": 1995,
            "spheres": [prime],
            "is_primer": True,
        },
    ]

    for gdata in grimoires_data:
        grimoire, created = Grimoire.objects.get_or_create(
            name=gdata["name"],
            chronicle=chronicle,
            defaults={
                "owner": st_user,
                "description": gdata["description"],
                "rank": gdata["rank"],
                "faction": gdata["faction"],
                "language": gdata["language"],
                "date_written": gdata["date_written"],
                "is_primer": gdata.get("is_primer", False),
            },
        )
        if created:
            grimoire.spheres.set(gdata["spheres"])
            grimoire.save()
            cross_library.add_book(grimoire)
            print(f"    Created Grimoire: {grimoire.name}")

    # =========================================================================
    # TEMPLE OF INNER LIGHT LIBRARY
    # =========================================================================

    temple_library, created = Library.objects.get_or_create(
        name="Temple of Inner Light Library",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A smaller, specialized collection focusing on Eastern
mystical traditions and the relationship between mind, body, and spirit. The library
serves both the Akashic Brotherhood and Celestial Chorus members of the chantry.

The collection includes meditation manuals, philosophical treatises, and practical
texts on internal alchemy. Many works are handwritten copies of texts that exist
nowhere else in the West.""",
            "rank": 3,
            "faction": akashic,
            "parent": temple_inner_light,
        },
    )
    if created:
        print(f"  Created Library: {temple_library.name}")

    temple_grimoires = [
        {
            "name": "The Diamond Sutra of Do",
            "description": """An Akashic text on Mind magic and the achievement of mental
clarity through martial discipline. The grimoire describes meditation techniques,
physical exercises, and the philosophical framework that unites them.

Written in classical Chinese with extensive commentary in English, this version
was transcribed by Dr. Yuki Tanaka from an oral teaching tradition.""",
            "faction": akashic,
            "rank": 3,
            "language": chinese,
            "date_written": 1950,
            "spheres": [mind],
            "is_primer": False,
        },
        {
            "name": "Songs of the One",
            "description": """A Celestial Chorus primer on understanding the Divine through
Prime and Spirit magic. The grimoire presents techniques from multiple faith traditions,
emphasizing the underlying unity beneath different religious expressions.

The text includes hymns, prayers, and meditative practices from Christianity, Islam,
and Judaism, with extensive commentary on their magical applications.""",
            "faction": celestial_chorus,
            "rank": 2,
            "language": english,
            "date_written": 1985,
            "spheres": [prime, spirit],
            "is_primer": True,
        },
        {
            "name": "The Way of Moving Stillness",
            "description": """A rare text on Life and Mind magic as expressed through
martial arts and breath control. The grimoire describes techniques for enhancing
physical capabilities and achieving states of combat awareness that border on
precognition.

Handwritten by a master who claimed descent from Bodhidharma himself, the text
uses minimal words, relying heavily on diagrams of body positions and energy flows.""",
            "faction": akashic,
            "rank": 4,
            "language": chinese,
            "date_written": 1650,
            "spheres": [life, mind],
            "is_primer": False,
        },
    ]

    for gdata in temple_grimoires:
        grimoire, created = Grimoire.objects.get_or_create(
            name=gdata["name"],
            chronicle=chronicle,
            defaults={
                "owner": st_user,
                "description": gdata["description"],
                "rank": gdata["rank"],
                "faction": gdata["faction"],
                "language": gdata["language"],
                "date_written": gdata["date_written"],
                "is_primer": gdata.get("is_primer", False),
            },
        )
        if created:
            grimoire.spheres.set(gdata["spheres"])
            grimoire.save()
            temple_library.add_book(grimoire)
            print(f"    Created Grimoire: {grimoire.name}")

    # =========================================================================
    # DIGITAL SANCTUM LIBRARY
    # =========================================================================

    digital_library, created = Library.objects.get_or_create(
        name="Digital Sanctum Archive",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Virtual Adepts don't maintain a traditional library - instead,
their Archive exists as an encrypted distributed database spread across multiple servers
and backup systems worldwide. Access requires both technical skill and magical aptitude.

The Archive contains digital grimoires, code libraries with magical properties, and
extensive documentation on Digital Web exploration. Much of the content is collaboratively
written and constantly updated.""",
            "rank": 3,
            "faction": virtual_adepts,
            "parent": digital_sanctum,
        },
    )
    if created:
        print(f"  Created Library: {digital_library.name}")

    digital_grimoires = [
        {
            "name": "root_access.exe",
            "description": """A Virtual Adept grimoire on Correspondence magic as expressed
through network protocols and data transmission. The text is written as extensively
commented source code, teaching magical principles through programming metaphors.

The grimoire includes practical tools for Digital Web navigation and techniques for
perceiving connections between physical locations and their digital reflections.""",
            "faction": virtual_adepts,
            "rank": 3,
            "language": english,
            "date_written": 2020,
            "spheres": [correspondence],
            "is_primer": False,
        },
        {
            "name": "TimeSync Protocol v3.1",
            "description": """An experimental text on Time magic as understood through
computing concepts. The grimoire describes techniques for perceiving temporal patterns,
minor timeline manipulation, and the dangerous practice of "rolling back" events.

The document is heavily versioned, with different branches exploring alternative
theoretical approaches. Some branches are marked as "deprecated - caused Paradox.""",
            "faction": virtual_adepts,
            "rank": 4,
            "language": english,
            "date_written": 2018,
            "spheres": [time, correspondence],
            "is_primer": False,
        },
        {
            "name": "Reality Hacking 101",
            "description": """A primer for newly Awakened Virtual Adepts, explaining the
basic paradigm that reality is a simulation that can be modified with the right
techniques. Written in accessible language with plenty of pop culture references.

The grimoire covers Prime basics (understanding the "source code" of reality) and
introduces fundamental Correspondence concepts (the network topology of existence).""",
            "faction": virtual_adepts,
            "rank": 2,
            "language": english,
            "date_written": 2022,
            "spheres": [prime],
            "is_primer": True,
        },
    ]

    for gdata in digital_grimoires:
        grimoire, created = Grimoire.objects.get_or_create(
            name=gdata["name"],
            chronicle=chronicle,
            defaults={
                "owner": st_user,
                "description": gdata["description"],
                "rank": gdata["rank"],
                "faction": gdata["faction"],
                "language": gdata["language"],
                "date_written": gdata["date_written"],
                "is_primer": gdata.get("is_primer", False),
            },
        )
        if created:
            grimoire.spheres.set(gdata["spheres"])
            grimoire.save()
            digital_library.add_book(grimoire)
            print(f"    Created Grimoire: {grimoire.name}")

    # =========================================================================
    # PROMETHEUS LABS LIBRARY (Technocratic)
    # =========================================================================

    prometheus_library, created = Library.objects.get_or_create(
        name="Prometheus Research Archives",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Progenitors maintain extensive research archives covering
Enlightened Science applications to biology, genetics, and human enhancement. Access
is restricted by security clearance, with the most dangerous materials requiring
Director-level authorization.

The archives include both digital databases and physical specimens, some of which
qualify as Procedures in their own right. Research here focuses on practical
applications rather than theoretical exploration.""",
            "rank": 4,
            "faction": progenitors,
            "parent": prometheus_labs,
        },
    )
    if created:
        print(f"  Created Library: {prometheus_library.name}")

    progenitor_grimoires = [
        {
            "name": "GENE-MOD Protocol Suite",
            "description": """A comprehensive Progenitor text on Life magic expressed through
genetic modification techniques. The document covers approved procedures for human
enhancement, disease treatment, and the controversial "optimization" programs.

Written in clinical scientific language, the text includes extensive safety protocols
and warnings about Reality Deviant contamination of research subjects.""",
            "faction": progenitors,
            "rank": 4,
            "language": english,
            "date_written": 2019,
            "spheres": [life],
            "is_primer": False,
        },
        {
            "name": "Introduction to Enlightened Biology",
            "description": """A primer for newly recruited Progenitors, explaining how
biological systems can be understood and modified through Enlightened Science. The
text carefully avoids "superstitious" terminology while teaching genuine magical
techniques.

The grimoire includes laboratory exercises and emphasizes proper experimental
methodology and documentation standards.""",
            "faction": progenitors,
            "rank": 2,
            "language": english,
            "date_written": 2021,
            "spheres": [life],
            "is_primer": True,
        },
    ]

    for gdata in progenitor_grimoires:
        grimoire, created = Grimoire.objects.get_or_create(
            name=gdata["name"],
            chronicle=chronicle,
            defaults={
                "owner": st_user,
                "description": gdata["description"],
                "rank": gdata["rank"],
                "faction": gdata["faction"],
                "language": gdata["language"],
                "date_written": gdata["date_written"],
                "is_primer": gdata.get("is_primer", False),
            },
        )
        if created:
            grimoire.spheres.set(gdata["spheres"])
            grimoire.save()
            prometheus_library.add_book(grimoire)
            print(f"    Created Grimoire: {grimoire.name}")

    # =========================================================================
    # HAYES TOWER LIBRARY (NWO)
    # =========================================================================

    nwo_library, created = Library.objects.get_or_create(
        name="Hayes Tower Intelligence Archives",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The NWO maintains classified archives covering Mind procedures,
surveillance techniques, and conditioning protocols. Access requires security clearance
and a demonstrated need-to-know.

The archives include psychological profiles of known Reality Deviants, approved
interrogation procedures, and research into mass perception management. Some materials
are considered dangerous even for trained operatives.""",
            "rank": 3,
            "faction": nwo,
            "parent": hayes_tower,
        },
    )
    if created:
        print(f"  Created Library: {nwo_library.name}")

    nwo_grimoires = [
        {
            "name": "Operative's Handbook: Perception Management",
            "description": """A NWO field manual on Mind procedures for controlling and
modifying human perception. The text covers everything from subtle suggestion to
full memory reconstruction, with detailed protocols for minimizing Paradox.

The handbook emphasizes operational security and includes case studies of both
successful operations and cautionary failures.""",
            "faction": nwo,
            "rank": 3,
            "language": english,
            "date_written": 2017,
            "spheres": [mind],
            "is_primer": False,
        },
        {
            "name": "Reality Deviant Psychology",
            "description": """A clinical study of how Reality Deviants think and why their
beliefs persist despite evidence. The text is partly genuine psychological analysis
and partly a guide to exploiting those beliefs for interrogation and recruitment.

Includes detailed profiles of major Tradition paradigms and their psychological
vulnerabilities.""",
            "faction": nwo,
            "rank": 2,
            "language": english,
            "date_written": 2020,
            "spheres": [mind],
            "is_primer": True,
        },
    ]

    for gdata in nwo_grimoires:
        grimoire, created = Grimoire.objects.get_or_create(
            name=gdata["name"],
            chronicle=chronicle,
            defaults={
                "owner": st_user,
                "description": gdata["description"],
                "rank": gdata["rank"],
                "faction": gdata["faction"],
                "language": gdata["language"],
                "date_written": gdata["date_written"],
                "is_primer": gdata.get("is_primer", False),
            },
        )
        if created:
            grimoire.spheres.set(gdata["spheres"])
            grimoire.save()
            nwo_library.add_book(grimoire)
            print(f"    Created Grimoire: {grimoire.name}")

    print("Mage items populated successfully.")

    return {
        "libraries": [
            cross_library,
            temple_library,
            digital_library,
            prometheus_library,
            nwo_library,
        ],
    }


if __name__ == "__main__":
    populate_mage_items()
