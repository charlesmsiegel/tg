"""
Mage location population script for Seattle Test Chronicle.

Creates Tradition Chantries, Technocratic Constructs, and Nodes.
"""

from accounts.models import Profile
from characters.models.mage.faction import MageFaction
from characters.models.mage.resonance import Resonance
from game.models import Chronicle
from locations.models.mage import Chantry, Library, Node


def populate_mage_locations():
    """Create all Mage locations for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # Get factions
    traditions = MageFaction.objects.get(name="Traditions")
    order_of_hermes = MageFaction.objects.get(name="Order of Hermes")
    akashic = MageFaction.objects.get(name="Akashayana")
    celestial_chorus = MageFaction.objects.get(name="Celestial Chorus")
    virtual_adepts = MageFaction.objects.get(name="Virtual Adepts")
    technocracy = MageFaction.objects.get(name="Technocratic Union")
    nwo = MageFaction.objects.get(name="New World Order")
    progenitors = MageFaction.objects.get(name="Progenitors")
    iteration_x = MageFaction.objects.get(name="Iteration X")
    syndicate = MageFaction.objects.get(name="Syndicate")

    # Get resonances for nodes
    dynamic_res, _ = Resonance.objects.get_or_create(name="Dynamic")
    creative_res, _ = Resonance.objects.get_or_create(name="Creative")
    ordered_res, _ = Resonance.objects.get_or_create(name="Ordered")
    entropic_res, _ = Resonance.objects.get_or_create(name="Entropic")
    mystical_res, _ = Resonance.objects.get_or_create(name="Mystical")
    technological_res, _ = Resonance.objects.get_or_create(name="Technological")
    serene_res, _ = Resonance.objects.get_or_create(name="Serene")
    focused_res, _ = Resonance.objects.get_or_create(name="Focused")
    dark_res, _ = Resonance.objects.get_or_create(name="Dark")
    primal_res, _ = Resonance.objects.get_or_create(name="Primal")
    aquatic_res, _ = Resonance.objects.get_or_create(name="Aquatic")
    ecstatic_res, _ = Resonance.objects.get_or_create(name="Ecstatic")

    # =========================================================================
    # TRADITION CHANTRIES
    # =========================================================================

    # The Cross House - Primary Tradition Chantry
    cross_house, created = Chantry.objects.get_or_create(
        name="The Cross House",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A sprawling Victorian mansion on Capitol Hill that serves as
Seattle's primary Tradition Chantry. Led by Archmagus Solomon Cross of the Order of Hermes,
the building's interior is spatially expanded far beyond its external dimensions.

The chantry contains extensive library facilities, ritual chambers for each Tradition
represented, comfortable living quarters for resident mages, and a carefully warded garden
that serves as a minor node. The mansion is heavily protected against scrying and intrusion,
with layered wards maintained by the resident Hermetics.

Representatives from most Traditions maintain quarters here, though the Virtual Adepts
prefer their Digital Sanctum and some Dreamspeakers find the urban environment uncomfortable.""",
            "faction": order_of_hermes,
            "leadership_type": "council_of_elders",
            "season": "summer",
            "chantry_type": "diplomatic",
            "total_points": 45,
            "gauntlet": 4,
        },
    )
    if created:
        print(f"  Created Chantry: {cross_house.name}")

    # The Temple of Inner Light - Akashic/Chorus Chantry
    temple_inner_light, created = Chantry.objects.get_or_create(
        name="The Temple of Inner Light",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A shared chantry in Seattle's International District, jointly
maintained by the Akashayana and Celestial Chorus. The building appears to be a wellness
center offering meditation classes and spiritual counseling to the public.

Behind the public facade lies a smaller but deeply spiritual sanctum. The interior contains
a martial arts dojo, multi-faith prayer rooms, and a small library of Eastern mystical texts.
Dr. Yuki Tanaka of the Akashic Brotherhood and Dr. Hassan Al-Rashid of the Celestial Chorus
share leadership, emphasizing contemplation and inner development over the political
maneuvering common to larger chantries.

A meditation chamber in the basement serves as a Mind/Prime aspected node, though it requires
stillness and focus to tap effectively.""",
            "faction": akashic,
            "leadership_type": "teachers",
            "season": "autumn",
            "chantry_type": "healing",
            "total_points": 25,
            "gauntlet": 5,
        },
    )
    if created:
        print(f"  Created Chantry: {temple_inner_light.name}")

    # The Digital Sanctum - Virtual Adept Chantry
    digital_sanctum, created = Chantry.objects.get_or_create(
        name="The Digital Sanctum",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A chantry that exists primarily in the Digital Web, with physical
access points scattered across Seattle's tech sector. The primary server farm is housed in a
nondescript SODO warehouse maintained by the Virtual Adept known as Nexus.

The Digital Sanctum is more concept than location - members access it from any networked
device, meeting in elaborate virtual spaces that shift according to collective will. The
physical warehouse contains backup servers, emergency hardware, and a small living space
for the rare occasions when meatspace presence is required.

The chantry's decentralized nature makes it remarkably resistant to physical assault, though
it requires constant vigilance against Technocratic intrusion in the Digital Web.""",
            "faction": virtual_adepts,
            "leadership_type": "anarchy",
            "season": "spring",
            "chantry_type": "research",
            "total_points": 30,
            "gauntlet": 6,
        },
    )
    if created:
        print(f"  Created Chantry: {digital_sanctum.name}")

    # =========================================================================
    # TECHNOCRATIC CONSTRUCTS
    # =========================================================================

    # Prometheus Labs - Progenitor Construct
    prometheus_labs, created = Chantry.objects.get_or_create(
        name="Prometheus Labs",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A Progenitor Construct disguised as a biotech research campus
in South Lake Union. Multiple buildings connected by underground tunnels house genetics
laboratories, bio-enhancement facilities, and a small Dimensional Science division.

Director Dr. Elena Vasquez oversees a staff of Enlightened Scientists and loyal employees,
conducting research into human enhancement, disease eradication, and less savory projects
involving Reality Deviant biology. The campus maintains a spotless public reputation, with
several legitimate medical breakthroughs emerging from its authorized research divisions.

The underground levels contain holding facilities for study subjects and secure storage
for samples that would raise uncomfortable questions if discovered.""",
            "faction": progenitors,
            "leadership_type": "single_deacon",
            "season": "summer",
            "chantry_type": "research",
            "total_points": 50,
            "gauntlet": 7,
        },
    )
    if created:
        print(f"  Created Construct: {prometheus_labs.name}")

    # Hayes Tower - NWO Construct
    hayes_tower, created = Chantry.objects.get_or_create(
        name="Hayes Tower",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An NWO Construct occupying floors 40-45 of a downtown corporate
high-rise. The building's legitimate tenants have no idea that their neighbors maintain
one of the Pacific Northwest's primary surveillance hubs.

Director Marcus Hayes commands a network of agents monitoring Seattle's Reality Deviants.
The facility contains state-of-the-art surveillance equipment, data analysis centers,
interrogation facilities disguised as conference rooms, and a small cadre of Men in Black
ready for rapid deployment.

The Construct's cover as a "data analytics firm" is maintained by shell companies and
careful information management. Visitors to the restricted floors experience subtle
conditioning that discourages curiosity.""",
            "faction": nwo,
            "leadership_type": "single_deacon",
            "season": "winter",
            "chantry_type": "fortress",
            "total_points": 55,
            "gauntlet": 8,
        },
    )
    if created:
        print(f"  Created Construct: {hayes_tower.name}")

    # Site 7 - Iteration X Field Installation
    site_7, created = Chantry.objects.get_or_create(
        name="Site 7",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An Iteration X field installation whose location is classified
even among the Technocracy. Rumors suggest it's mobile - possibly a converted cargo ship
that moves through Puget Sound, or an underground bunker accessed through different entry
points.

Site 7 houses HIT Mark production and maintenance facilities, deploying cyborg operatives
for enforcement actions throughout the region. The installation is commanded by a rotating
series of officers, making it difficult for outsiders to track its leadership.

The few Traditionalists who've encountered Site 7's operatives and survived describe
encounters with cutting-edge combat technology and emotionless precision.""",
            "faction": iteration_x,
            "leadership_type": "meritocracy",
            "season": "winter",
            "chantry_type": "war",
            "total_points": 40,
            "gauntlet": 9,
        },
    )
    if created:
        print(f"  Created Construct: {site_7.name}")

    # Federal Building Annex - Syndicate Construct
    federal_annex, created = Chantry.objects.get_or_create(
        name="Federal Building Annex",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A Syndicate Construct hidden within legitimate government
offices in downtown Seattle. The facility handles economic warfare, funding allocation
for Technocratic operations, and financial tracking of Reality Deviants.

The Construct maintains a skeleton crew of operatives who appear to be ordinary federal
employees. Their work involves manipulating markets to fund Technocratic operations,
tracking unusual financial activity that might indicate supernatural involvement, and
ensuring that the economic foundations of the Consensus remain stable.

Though smaller than other Constructs, the Federal Building Annex wields considerable
influence through its control of regional Technocratic finances.""",
            "faction": syndicate,
            "leadership_type": "panel",
            "season": "autumn",
            "chantry_type": "library",
            "total_points": 30,
            "gauntlet": 7,
        },
    )
    if created:
        print(f"  Created Construct: {federal_annex.name}")

    # =========================================================================
    # NODES
    # =========================================================================

    # Pike Place Market Node
    pike_place_node, created = Node.objects.get_or_create(
        name="Pike Place Market Node",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Quintessence flows from the creative energy of artists,
musicians, and dreamers who gather at Pike Place Market. The node manifests in the
Market's oldest section, near the brass pig statue that has absorbed decades of
creative intent and tourist wonder.

Tass forms as small copper coins that appear in the pig's donation slots,
distinguishable from ordinary coins by their warm glow visible to those with
Prime sight. The node is technically neutral ground, though the Traditions maintain
informal stewardship.""",
            "rank": 3,
            "size": 1,  # LARGE - Small Building
            "ratio": 0,  # NORMAL - 0.5 split
            "quintessence_form": "Creative inspiration during artistic performances",
            "tass_form": "Glowing copper coins near the brass pig",
            "gauntlet": 5,
        },
    )
    if created:
        pike_place_node.set_rank(3)
        pike_place_node.update_output()
        pike_place_node.add_resonance(creative_res)
        pike_place_node.add_resonance(dynamic_res)
        pike_place_node.add_resonance(creative_res)
        pike_place_node.save()
        print(f"  Created Node: {pike_place_node.name}")

    # Space Needle Ley Nexus
    space_needle_node, created = Node.objects.get_or_create(
        name="Space Needle Ley Nexus",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A convergence of three major ley lines at the Space Needle,
making it one of the most powerful nodes in the Pacific Northwest. The structure itself
acts as a focusing lens, gathering and concentrating the mystical energies that flow
through Seattle.

The node is heavily contested. Tradition mages have maintained subtle influence over
the site since its construction, but Technocratic interests view the iconic landmark
as rightfully theirs. The current uneasy truce involves shared access during specific
hours, enforced by mutual observation.

Quintessence manifests as vertigo-inducing moments of clarity at the observation deck.
Tass forms as tiny crystal formations on the exterior structure, visible only to those
with magical sight and requiring considerable effort to harvest.""",
            "rank": 4,
            "size": 2,  # HUGE - Large Building
            "ratio": 1,  # LARGE - 0.75 quintessence
            "quintessence_form": "Moments of transcendent clarity at the observation deck",
            "tass_form": "Crystal formations on the tower's exterior",
            "gauntlet": 4,
        },
    )
    if created:
        space_needle_node.set_rank(4)
        space_needle_node.update_output()
        space_needle_node.add_resonance(ordered_res)
        space_needle_node.add_resonance(technological_res)
        space_needle_node.add_resonance(dynamic_res)
        space_needle_node.add_resonance(mystical_res)
        space_needle_node.save()
        print(f"  Created Node: {space_needle_node.name}")

    # Underground Seattle Node
    underground_node, created = Node.objects.get_or_create(
        name="Underground Seattle Node",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Dark quintessence pools in the buried streets of old Seattle,
where the city's original ground level was raised after the Great Fire of 1889. The
energy here carries echoes of the dead, the forgotten, and secrets buried along with
the old city.

The node is unstable and dangerous, its power fluctuating with the moon phases and the
emotional state of Seattle's dead. Euthanatos and Dreamspeakers have the easiest time
working with its energy, while Hermetic formalism struggles against its chaotic nature.

Tass manifests as dark, oily residue that collects in the lowest points of the
underground tunnels. Harvesting it requires venturing into areas the tour groups
never see.""",
            "rank": 2,
            "size": 2,  # HUGE - Large Building (extensive underground area)
            "ratio": 2,  # HUGE - 1.0 all tass
            "quintessence_form": "Whispers from the buried dead",
            "tass_form": "Dark oily residue in the deepest tunnels",
            "gauntlet": 6,
        },
    )
    if created:
        underground_node.set_rank(2)
        underground_node.update_output()
        underground_node.add_resonance(entropic_res)
        underground_node.add_resonance(dark_res)
        underground_node.save()
        print(f"  Created Node: {underground_node.name}")

    # Maestro's Rave Temple
    rave_temple_node, created = Node.objects.get_or_create(
        name="Maestro's Rave Temple",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A node created and maintained through ecstatic dance energy,
housed in a converted warehouse that hosts the legendary underground raves organized
by the Cult of Ecstasy mage known as Maestro. The node only fully manifests during
events, when hundreds of dancers achieve collective altered states.

Between events, the warehouse appears mundane, but residual energy lingers in the
walls and floor. The Cult of Ecstasy maintains exclusive stewardship, using the
node to fuel transformative experiences and occasionally recruit promising Sleepers
showing signs of Awakening.

Tass forms as pills that materialize in the DJ booth during peak moments - they
appear identical to certain party drugs but contain pure, crystallized ecstasy
in the magical sense.""",
            "rank": 3,
            "size": 1,  # LARGE - Small Building
            "ratio": -1,  # SMALL - 0.25 quintessence, mostly tass
            "quintessence_form": "Collective euphoria during dance events",
            "tass_form": "Pills materializing in the DJ booth",
            "gauntlet": 5,
        },
    )
    if created:
        rave_temple_node.set_rank(3)
        rave_temple_node.update_output()
        rave_temple_node.add_resonance(ecstatic_res)
        rave_temple_node.add_resonance(dynamic_res)
        rave_temple_node.add_resonance(creative_res)
        rave_temple_node.save()
        print(f"  Created Node: {rave_temple_node.name}")

    # Puget Sound Deep Node
    puget_sound_node, created = Node.objects.get_or_create(
        name="Puget Sound Deep Node",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Something powerful slumbers in the deepest waters of Puget
Sound. Divers report unusual currents, strange bioluminescence, and an overwhelming
sense of ancient presence in certain areas. Mages who've attempted to study the node
directly have returned... changed.

The node's rating is uncertain because no one has successfully mapped it. Water-aspected
energy radiates outward, affecting the tides and weather in subtle ways. The Verbena
claim it connects to primal forces older than human civilization.

Whatever tass the node produces lies far beneath the waves. The few samples recovered
resemble black pearls that sing faintly of depths and drowning.""",
            "rank": 5,
            "size": 2,  # HUGE
            "ratio": 2,  # All tass (inaccessible quintessence)
            "quintessence_form": "Unknown - direct access dangerous",
            "tass_form": "Black pearls that sing of drowning",
            "gauntlet": 3,
        },
    )
    if created:
        puget_sound_node.set_rank(5)
        puget_sound_node.update_output()
        puget_sound_node.add_resonance(primal_res)
        puget_sound_node.add_resonance(aquatic_res)
        puget_sound_node.add_resonance(entropic_res)
        puget_sound_node.add_resonance(dark_res)
        puget_sound_node.add_resonance(primal_res)
        puget_sound_node.save()
        print(f"  Created Node: {puget_sound_node.name}")

    # Cross House Garden Node
    garden_node, created = Node.objects.get_or_create(
        name="Cross House Garden Node",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A small but carefully tended node in the warded gardens of
the Cross House Chantry. The Order of Hermes has cultivated this node for decades,
shaping its resonance through ritual gardening and precise geometric plantings.

The garden appears as an English formal garden to mundane eyes, but magical sight
reveals complex patterns that channel and refine quintessence. The node provides
a reliable, if modest, source of power for the chantry's defensive wards and
ongoing research.

Tass manifests as morning dew that collects on specific plants, glowing faintly
with captured starlight.""",
            "rank": 2,
            "size": 0,  # NORMAL - Average Room
            "ratio": 0,  # NORMAL - balanced
            "quintessence_form": "Refined energy from geometric garden patterns",
            "tass_form": "Glowing morning dew on ritual plants",
            "gauntlet": 4,
            "parent": cross_house,
        },
    )
    if created:
        garden_node.set_rank(2)
        garden_node.update_output()
        garden_node.add_resonance(ordered_res)
        garden_node.add_resonance(mystical_res)
        garden_node.save()
        print(f"  Created Node: {garden_node.name}")

    # Temple Meditation Chamber Node
    meditation_node, created = Node.objects.get_or_create(
        name="Temple Meditation Chamber Node",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A Mind and Prime aspected node in the basement meditation
chamber of the Temple of Inner Light. The node requires stillness and focused
meditation to tap effectively - impatient mages find it yields nothing.

The chamber is a simple space with cushions arranged in a circle around a small
fountain. Years of collective meditation have saturated the room with serene
energy. Those who meditate here report unusual clarity and occasional glimpses
of enlightenment.

Tass forms as clear water that accumulates in the fountain beyond what its
mechanism can explain. The water must be collected during deep meditation or
it evaporates instantly.""",
            "rank": 2,
            "size": -1,  # SMALL - Small Room
            "ratio": 1,  # LARGE - mostly quintessence
            "quintessence_form": "Clarity achieved through deep meditation",
            "tass_form": "Pure water appearing in the fountain",
            "gauntlet": 5,
            "parent": temple_inner_light,
        },
    )
    if created:
        meditation_node.set_rank(2)
        meditation_node.update_output()
        meditation_node.add_resonance(serene_res)
        meditation_node.add_resonance(focused_res)
        meditation_node.save()
        print(f"  Created Node: {meditation_node.name}")

    print("Mage locations populated successfully.")

    return {
        "chantries": [cross_house, temple_inner_light, digital_sanctum],
        "constructs": [prometheus_labs, hayes_tower, site_7, federal_annex],
        "nodes": [
            pike_place_node,
            space_needle_node,
            underground_node,
            rave_temple_node,
            puget_sound_node,
            garden_node,
            meditation_node,
        ],
    }


if __name__ == "__main__":
    populate_mage_locations()
