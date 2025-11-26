"""
Mage item population script for Seattle Test Chronicle.

Creates Libraries, Grimoires, Artifacts, Talismans, Charms, and Periapts for Chantries.
"""

from accounts.models import Profile
from characters.models.mage.faction import MageFaction
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from core.models import Language
from game.models import Chronicle
from items.models.mage import Artifact, Charm, Grimoire, Periapt, Talisman
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

    # =========================================================================
    # TALISMANS - Powerful multi-effect items
    # =========================================================================

    # Cross House Talisman
    hermetic_staff, created = Talisman.objects.get_or_create(
        name="The Staff of Seven Seals",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An ancient Hermetic staff passed down through the Cross
House leadership for generations. The ebony wood is inlaid with silver sigils
representing the seven classical planets, each seal containing a bound effect.

The staff serves as the ceremonial focus for the chantry's most important
rituals. Only the ranking Hermetic mage may wield it, and its powers respond
to proper invocations in Enochian.

The Seven Seals contain effects for warding, scrying, elemental manipulation,
healing, banishment, communication, and temporal perception. Each can be
activated independently or combined for greater workings.""",
            "rank": 5,
            "arete": 4,
        },
    )
    if created:
        hermetic_staff.add_resonance("Structured", 4)
        hermetic_staff.add_resonance("Ancient", 3)
        print(f"  Created Talisman: {hermetic_staff.name}")

    # Akashic Talisman
    jade_bracers, created = Talisman.objects.get_or_create(
        name="Bracers of the Perfected Form",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A pair of jade bracers carved with flowing script in
archaic Chinese. The bracers were crafted by an Akashic master who achieved
legendary status through martial perfection.

When worn during combat, the bracers enhance the wearer's physical capabilities
and allow access to ancient fighting techniques encoded in the jade itself.
The bracers also provide protection against physical and spiritual attacks.

Dr. Yuki Tanaka inherited the bracers from her sifu and considers them both
a responsibility and an honor to carry.""",
            "rank": 4,
            "arete": 3,
        },
    )
    if created:
        jade_bracers.add_resonance("Disciplined", 3)
        jade_bracers.add_resonance("Martial", 3)
        print(f"  Created Talisman: {jade_bracers.name}")

    # Technocratic Talisman
    neural_interface, created = Talisman.objects.get_or_create(
        name="MNEME Neural Interface v7.2",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A classified Iteration X/NWO collaborative project, the
MNEME interface connects directly to the user's neural pathways, allowing
enhanced mental processing and direct data access through the Net.

The device appears as a small implant behind the ear with a subtle indicator
light. When activated, it provides computational assistance, memory enhancement,
and limited mind-to-mind communication with other MNEME users.

Only high-clearance operatives are authorized for MNEME implantation. The
procedures are carefully documented and the devices are registered.""",
            "rank": 4,
            "arete": 3,
        },
    )
    if created:
        neural_interface.add_resonance("Digital", 4)
        neural_interface.add_resonance("Structured", 2)
        print(f"  Created Talisman: {neural_interface.name}")

    # =========================================================================
    # ARTIFACTS - Single powerful effect items
    # =========================================================================

    # Hermetic Artifact
    scrying_mirror, created = Artifact.objects.get_or_create(
        name="The Mirror of Distant Sight",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An oval mirror framed in silver, its surface perfectly
reflective yet somehow seeming to contain depths beyond the physical glass.
The mirror allows its user to perceive distant locations, provided they have
a sympathetic link to the target.

The Mirror was created in Prague during the height of Hermetic influence there
and has served as a primary scrying tool for the Cross House since its founding.
Proper use requires ritual preparation and significant quintessence expenditure.

Users report that the mirror sometimes shows images unbidden - visions of
places or events of significance to the viewer.""",
            "rank": 4,
        },
    )
    if created:
        scrying_mirror.add_resonance("Revealing", 3)
        scrying_mirror.add_resonance("Mysterious", 2)
        print(f"  Created Artifact: {scrying_mirror.name}")

    # Virtual Adept Artifact
    reality_compiler, created = Artifact.objects.get_or_create(
        name="The Reality Compiler",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A custom-built server rack that processes reality
modifications through code. The hardware appears mundane, but the software
running on it is anything but - a collaborative project by some of the most
talented Virtual Adepts in the Traditions.

The Compiler allows users to write Effects as code, compiling them into
functional magic. The interface is complex, requiring both programming skill
and magical understanding, but the results can be precisely controlled.

The Digital Sanctum maintains the Compiler as their primary operational tool,
using it for everything from security to research to combat support.""",
            "rank": 5,
        },
    )
    if created:
        reality_compiler.add_resonance("Digital", 5)
        reality_compiler.add_resonance("Innovative", 3)
        print(f"  Created Artifact: {reality_compiler.name}")

    # Celestial Chorus Artifact
    choir_bell, created = Artifact.objects.get_or_create(
        name="The Bell of Sacred Harmony",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A bronze bell inscribed with prayers in Hebrew, Latin,
and Arabic. When rung with proper intention, the bell produces a tone that
resonates with the divine, creating a space of sacred peace.

Within the bell's influence, violence becomes difficult, lies are exposed, and
the faithful feel the presence of something greater. The effect extends
approximately one hundred feet from the bell's location.

The Temple of Inner Light uses the bell during interfaith ceremonies and to
create sanctuaries during times of crisis. Its power is strongest when
multiple faiths pray together in its presence.""",
            "rank": 4,
        },
    )
    if created:
        choir_bell.add_resonance("Sacred", 4)
        choir_bell.add_resonance("Harmonious", 3)
        print(f"  Created Artifact: {choir_bell.name}")

    # Progenitor Artifact
    gene_sequencer, created = Artifact.objects.get_or_create(
        name="BioMatrix Rapid Sequencer",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An advanced genetic analysis and modification device that
exists decades ahead of public technology. The Sequencer can analyze DNA in
real-time, identify modifications, and suggest optimization pathways.

Prometheus Labs uses the Sequencer for research, diagnosis, and treatment
planning. The device can identify supernatural contamination in genetic
material and suggest protocols for correction.

The Sequencer requires considerable expertise to operate and is restricted
to senior researchers with appropriate clearance.""",
            "rank": 4,
        },
    )
    if created:
        gene_sequencer.add_resonance("Clinical", 3)
        gene_sequencer.add_resonance("Analytical", 3)
        print(f"  Created Artifact: {gene_sequencer.name}")

    # =========================================================================
    # CHARMS - Lesser items with specific effects
    # =========================================================================

    # Communication Charm
    whisper_stones, created = Charm.objects.get_or_create(
        name="Stones of Distant Whispers",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A set of twelve smooth river stones, each marked with a
unique sigil. Paired stones can transmit whispered messages across any distance,
allowing secure communication between mages.

The Cross House distributes these stones to members who may need to communicate
during operations. Messages are one-way and require both stones to be activated
simultaneously.

The stones were created as a collaborative project between Hermetic and
Virtual Adept mages, combining traditional enchantment with communication
theory.""",
            "rank": 2,
            "arete": 2,
        },
    )
    if created:
        whisper_stones.add_resonance("Connected", 2)
        print(f"  Created Charm: {whisper_stones.name}")

    # Protection Charm
    aegis_amulets, created = Charm.objects.get_or_create(
        name="Aegis Amulets",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Simple silver pendants blessed with protective magic. Each
amulet provides limited protection against supernatural attack, warning its
wearer of danger and providing minor magical resistance.

The chantries keep a supply of these amulets for new members and visiting
mages. While not powerful, they represent the community's commitment to
protecting its members.

Creating the amulets is often a teaching exercise for apprentice mages
learning Prime and Forces.""",
            "rank": 2,
            "arete": 2,
        },
    )
    if created:
        aegis_amulets.add_resonance("Protective", 2)
        print(f"  Created Charm: {aegis_amulets.name}")

    # Technocratic Charm
    hud_glasses, created = Charm.objects.get_or_create(
        name="Enhanced Reality Glasses",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Standard-issue eyewear for Technocratic field operatives.
The glasses overlay useful information on the wearer's field of vision:
threat assessment, communication status, and basic sensor readings.

The glasses connect to Union databases through secure channels, allowing
real-time information access and coordination with other operatives. They
can also record observations for later analysis.

These devices are considered basic equipment and are provided to all field
personnel upon assignment.""",
            "rank": 2,
            "arete": 2,
        },
    )
    if created:
        hud_glasses.add_resonance("Analytical", 2)
        print(f"  Created Charm: {hud_glasses.name}")

    # =========================================================================
    # PERIAPTS - Quintessence storage devices
    # =========================================================================

    # Traditional Periapt
    quintessence_flask, created = Periapt.objects.get_or_create(
        name="Flask of Captured Dawn",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A crystal flask that glows faintly with internal light.
The flask was created to capture and store quintessence from sunrise rituals,
preserving the energy for later use.

The Cross House maintains several such flasks, using them to fuel major
rituals and as emergency reserves. Proper filling requires performing a
specific ritual at the moment of sunrise from an elevated location.

The light within pulses gently, growing brighter as more quintessence is
stored and dimmer as reserves are depleted.""",
            "rank": 3,
            "arete": 3,
            "max_charges": 15,
            "current_charges": 10,
            "is_consumable": False,
        },
    )
    if created:
        quintessence_flask.add_resonance("Radiant", 3)
        print(f"  Created Periapt: {quintessence_flask.name}")

    # Natural Periapt
    heartwood_stone, created = Periapt.objects.get_or_create(
        name="Heartwood Stone",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A piece of petrified wood from an ancient tree that once
stood at a Node. The stone naturally accumulates quintessence from its
environment, storing it until needed by its keeper.

The stone is warm to the touch and seems to pulse with life despite its
mineral nature. It responds particularly well to Life and Spirit magic,
releasing its energy more freely for such workings.

The Temple of Inner Light considers the stone sacred and uses it primarily
for healing rituals and communion with nature spirits.""",
            "rank": 3,
            "arete": 3,
            "max_charges": 12,
            "current_charges": 8,
            "is_consumable": False,
        },
    )
    if created:
        heartwood_stone.add_resonance("Vital", 3)
        heartwood_stone.add_resonance("Ancient", 2)
        print(f"  Created Periapt: {heartwood_stone.name}")

    # Technocratic Periapt
    primal_cell, created = Periapt.objects.get_or_create(
        name="Primal Energy Cell Mark IV",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A cylindrical device resembling a large battery, the
Primal Energy Cell stores refined quintessence in a stable, portable format.
The cell can be connected to other devices or used to power Procedures directly.

The Technocracy issues these cells to field teams for extended operations
away from established facilities. The cells can be recharged at any Union
installation with appropriate equipment.

Current generation cells are significantly more stable than earlier versions,
which had an unfortunate tendency to discharge unexpectedly.""",
            "rank": 3,
            "arete": 3,
            "max_charges": 20,
            "current_charges": 15,
            "is_consumable": False,
        },
    )
    if created:
        primal_cell.add_resonance("Stabilized", 3)
        primal_cell.add_resonance("Technical", 2)
        print(f"  Created Periapt: {primal_cell.name}")

    # Consumable Periapt
    tass_collection, created = Periapt.objects.get_or_create(
        name="Discovery Park Tass Reserve",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A collection of tass harvested from the Discovery Park
Node over time. The tass takes the form of small, luminescent dewdrops that
form on the grass during certain astronomical alignments.

The dewdrops can be consumed directly for quintessence or used as components
in ritual magic. Their nature as natural tass makes them particularly
compatible with Tradition magic.

The chantries maintain this reserve for emergencies and important workings,
replenishing it during harvest periods throughout the year.""",
            "rank": 2,
            "arete": 2,
            "max_charges": 25,
            "current_charges": 18,
            "is_consumable": True,
        },
    )
    if created:
        tass_collection.add_resonance("Natural", 2)
        tass_collection.add_resonance("Luminescent", 2)
        print(f"  Created Periapt: {tass_collection.name}")

    print("Mage items populated successfully.")

    return {
        "libraries": [
            cross_library,
            temple_library,
            digital_library,
            prometheus_library,
            nwo_library,
        ],
        "talismans": [hermetic_staff, jade_bracers, neural_interface],
        "artifacts": [scrying_mirror, reality_compiler, choir_bell, gene_sequencer],
        "charms": [whisper_stones, aegis_amulets, hud_glasses],
        "periapts": [quintessence_flask, heartwood_stone, primal_cell, tass_collection],
    }


if __name__ == "__main__":
    populate_mage_items()
