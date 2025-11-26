"""
Werewolf location population script for Seattle Test Chronicle.

Creates Caerns and significant Garou locations.
"""

from accounts.models import Profile
from game.models import Chronicle
from locations.models.core import LocationModel
from locations.models.werewolf import Caern


def populate_werewolf_locations():
    """Create all Werewolf locations for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # CAERNS
    # =========================================================================

    # Cougar Mountain Caern - Main Sept Caern
    cougar_mountain, created = Caern.objects.get_or_create(
        name="Cougar Mountain Caern",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The heart of the Sept of the Emerald Shadow, this Level 4
Caern of Falcon crowns Cougar Mountain in the Issaquah Alps. The bawn extends across
miles of protected wilderness, carefully maintained to appear as ordinary parkland
to human visitors.

The caern heart lies in a hidden valley accessible only through spirit paths or
by those who know the physical trails. A great standing stone marks the center,
carved with ancient glyphs predating European contact. The indigenous peoples who
first honored this place passed their guardianship to the Garou centuries ago.

Storm's-Fury serves as Warder, defending the caern with legendary ferocity. The
Sept Alpha Howls-at-Thunder holds moots here during the full moon, when the veil
between worlds grows thin and the spirits draw close to counsel their children.

Moon bridges connect to allied septs along the Pacific Coast, though travel requires
the Master of Rite's blessing.""",
            "rank": 4,
            "caern_type": "leadership",
        },
    )
    if created:
        print(f"  Created Caern: {cougar_mountain.name}")

    # Discovery Park Sacred Grove - Urban Caern
    discovery_park, created = Caern.objects.get_or_create(
        name="Discovery Park Sacred Grove",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A smaller urban caern hidden within Discovery Park's
wilderness areas, this Level 2 Caern of Urban serves the Glass Walkers and
city-dwelling Garou. The caern manifests where forest meets city, drawing power
from Seattle's technological energy.

The Glass Walkers maintain this site as a bridge between the concrete jungle
and the wild places. The spirits here are strange hybrids - nature spirits that
have adapted to urban existence, technological spirits that remember their
elemental origins.

The gauntlet here is thinner than in most urban areas, making it valuable for
Garou who need Umbral access without traveling to the mountains. However, the
taint of the Weaver is strong, and prolonged exposure can unbalance even
experienced Theurges.""",
            "rank": 2,
            "caern_type": "urban",
        },
    )
    if created:
        print(f"  Created Caern: {discovery_park.name}")

    # =========================================================================
    # PACK TERRITORIES (Using base LocationModel)
    # =========================================================================

    # Silicon Fangs Territory
    silicon_territory, created = LocationModel.objects.get_or_create(
        name="SODO Tech Corridor Territory",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Silicon Fangs pack claims the tech corridors of SODO
as their hunting ground. Server farms, startup offices, and the new tech workers
who inhabit them fall under their protection.

The Glass Walkers understand that the Wyrm corrupts through technology as easily
as through pollution. They monitor the data centers for signs of Pattern Spider
infestation, corporate Pentex subsidiaries, and the subtle taint that spreads
through networks.

Pack dens are hidden in converted industrial spaces, their true nature concealed
behind legitimate business fronts. The spirits here speak in code and data packets,
requiring special gifts to understand.""",
            "gauntlet": 7,
        },
    )
    if created:
        print(f"  Created Territory: {silicon_territory.name}")

    # The Wardens Territory
    wardens_territory, created = LocationModel.objects.get_or_create(
        name="Industrial District Patrol Zone",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Wardens pack ranges through Seattle's industrial
district, watching for Wyrm corruption in factories, chemical plants, and
transportation hubs. This unglamorous territory suits the pack's pragmatic
approach to the war.

Cuts-Through-Steel leads regular patrols, investigating reports of toxic
dumping, workplace accidents that suggest Bane activity, and the subtle
signs of Pentex operations. The work is dirty and dangerous, but essential.

The Umbral reflection here is blighted by decades of industrial pollution,
manifesting as toxic spirits and twisted elementals. The pack has learned
to navigate these hostile spirit-scape, sometimes even recruiting reformed
spirits to their cause.""",
            "gauntlet": 8,
        },
    )
    if created:
        print(f"  Created Territory: {wardens_territory.name}")

    # The Forgotten Territory
    forgotten_territory, created = LocationModel.objects.get_or_create(
        name="Capitol Hill Homeless Camps",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Breaks-the-Chain and the outcast Garou protect Seattle's
homeless population from supernatural predators. The encampments under bridges
and in forgotten corners of the city are their territory.

The Bone Gnawers have always championed the dispossessed, and in Seattle they
continue this tradition. The pack knows every shelter, every soup kitchen, every
warm grate where their charges seek refuge. Vampires who hunt here learn painful
lessons about pack territory.

The spirits of poverty and resilience respond to Bone Gnawer rituals, providing
warnings about danger and guidance through the urban wilderness. Old Pete's
food truck serves as mobile neutral ground and message drop.""",
            "gauntlet": 6,
        },
    )
    if created:
        print(f"  Created Territory: {forgotten_territory.name}")

    # =========================================================================
    # UMBRAL LOCATIONS
    # =========================================================================

    # Space Needle Penumbra
    space_needle_penumbra, created = LocationModel.objects.get_or_create(
        name="Space Needle Penumbra",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Umbral reflection of Seattle's iconic Space Needle
serves as an observation post and thin-gauntlet crossing point. The structure
appears in the Penumbra as a great spire of woven light and steel, its observation
deck offering views across the entire Umbral cityscape.

Sept scouts maintain informal watch here, monitoring both the physical and spiritual
activity below. The thin gauntlet makes stepping sideways relatively easy, though
the location's prominence means Banes also know of its value.

Pattern Spiders frequently repair the webs that connect the tower to Seattle's
infrastructure. The Glass Walkers have negotiated an uneasy truce with these
Weaver-spirits, trading information for passage.""",
            "gauntlet": 4,
        },
    )
    if created:
        print(f"  Created Umbral Location: {space_needle_penumbra.name}")

    # Puget Sound Umbral Depths
    puget_depths, created = LocationModel.objects.get_or_create(
        name="Puget Sound Umbral Depths",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Something ancient dwells in the Umbral reflection of
Puget Sound. The Theurges speak of it in whispers - a presence that predates
the Garou Nation, perhaps predates humanity itself. The deeper waters glow
with an eerie phosphorescence that has nothing to do with natural bioluminescence.

Watches-the-Void has sensed wrongness emanating from the depths, patterns that
don't fit any known spirit taxonomy. The Uktena elders recall legends of
something bound beneath the waters, something the indigenous peoples knew
to avoid.

Travel through these Umbral waters is discouraged. The few who have attempted
deep exploration returned changed, speaking of vast shapes moving in the
darkness and voices that offered terrible bargains.""",
            "gauntlet": 3,
        },
    )
    if created:
        print(f"  Created Umbral Location: {puget_depths.name}")

    # Mount Rainier Moon Bridge
    rainier_bridge, created = LocationModel.objects.get_or_create(
        name="Mount Rainier Moon Bridge Point",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A seasonal moon bridge connects Cougar Mountain Caern to
powerful mountain spirits at Mount Rainier. The bridge forms only during certain
lunar phases and weather conditions, requiring careful timing for travel.

The journey across the bridge takes travelers through realms of wind and snow,
past the courts of mountain spirits who demand tribute for passage. Those who
complete the journey may petition the great spirits for gifts and wisdom, though
such boons come with obligations.

The Master of Rite Speaks-with-Ancestors coordinates bridge openings with allied
spirits. Unsanctioned crossings risk losing travelers in the mountain spirits'
eternal storms.""",
            "gauntlet": 2,
        },
    )
    if created:
        print(f"  Created Umbral Location: {rainier_bridge.name}")

    # =========================================================================
    # KINFOLK LOCATIONS
    # =========================================================================

    # Mike Donovan's Forge
    donovans_forge, created = LocationModel.objects.get_or_create(
        name="Donovan's Metalworks",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Mike Donovan's metalworking shop appears to be an ordinary
custom fabrication business. In truth, it's one of the few places in the Pacific
Northwest where fetishes and klaives can be properly crafted and maintained.

Donovan is Get of Fenris Kinfolk, trained by his father and grandfather in the
sacred art of spirit-forging. The shop's back room contains a ritual forge blessed
by fire spirits, where the Rite of Spirit Awakening can bind spirits into weapons
and tools.

Garou come from distant septs seeking Donovan's services. He asks no payment
except the stories of how his creations serve Gaia. The walls display photographs
of warriors who wielded his work - some still fighting, many fallen but not
forgotten.""",
            "gauntlet": 5,
        },
    )
    if created:
        print(f"  Created Kinfolk Location: {donovans_forge.name}")

    # Old Pete's Food Truck
    petes_truck, created = LocationModel.objects.get_or_create(
        name="Old Pete's Food Truck",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Old Pete's food truck moves through Seattle serving hot
meals to whoever needs them. The truck is blessed by spirits of generosity and
sustenance, making it neutral ground respected by all Garou factions.

Pete himself is elderly Bone Gnawer Kinfolk who has served the Sept for decades.
He knows more about Seattle's supernatural geography than many Garou, and his
truck's unpredictable route often brings him to places where he's needed.

Messages can be left with Pete, guaranteed to reach their intended recipients.
Disputes have been settled over his coffee. Garou who fight near the truck
find themselves suddenly very interested in resolving their differences
peacefully over a hot meal.""",
            "gauntlet": 6,
        },
    )
    if created:
        print(f"  Created Kinfolk Location: {petes_truck.name}")

    print("Werewolf locations populated successfully.")

    return {
        "caerns": [cougar_mountain, discovery_park],
        "territories": [silicon_territory, wardens_territory, forgotten_territory],
        "umbral": [space_needle_penumbra, puget_depths, rainier_bridge],
        "kinfolk": [donovans_forge, petes_truck],
    }


if __name__ == "__main__":
    populate_werewolf_locations()
