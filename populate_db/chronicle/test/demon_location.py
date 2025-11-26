"""
Demon location population script for Seattle Test Chronicle.

Creates Bastions, Reliquaries, and other demon-significant locations.
"""

from accounts.models import Profile
from game.models import Chronicle
from locations.models.core import LocationModel
from locations.models.demon import Bastion, Reliquary


def populate_demon_locations():
    """Create all Demon locations for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # EARTHBOUND SITES
    # =========================================================================

    # The Foundation Church
    foundation_church, created = Reliquary.objects.get_or_create(
        name="St. Michael's Church (The Foundation)",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A century-old church built unknowingly over an Earthbound
binding site. The Foundation - an ancient demon bound to the bedrock beneath -
has slowly corrupted the congregation through dreams of righteous fury. The
parishioners believe themselves especially devout, unaware that their passion
serves something far older than their faith.

The church basement contains The Foundation's altar, hidden behind what appears
to be a maintenance closet. Those who discover it rarely remember clearly, their
minds sliding away from comprehension. The binding extends throughout the
building's structure, making demolition inadvisable.

The Foundation's influence spreads slowly, turning good intentions toward
destructive ends. Charitable works become crusades, community spirit becomes
tribal warfare, and the faithful dream of purifying flames.""",
            "reliquary_type": "location",
            "location_size": "Large church building with basement",
            "max_health_levels": 20,
            "current_health_levels": 20,
            "soak_rating": 5,
            "has_pervasiveness": True,
            "has_manifestation": True,
            "manifestation_range": 100,
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Earthbound Site: {foundation_church.name}")

    # The Resonance - Tech Campus
    resonance_campus, created = Reliquary.objects.get_or_create(
        name="Prometheus Tech Campus (The Resonance)",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A sprawling tech campus built over the binding site of The
Resonance, an Earthbound demon that feeds on ambition and stress. The demon's
influence seeps through the parking garage into the dreams of overworked employees,
offering revelatory insights that come with terrible prices.

Workers at the campus report unusually vivid dreams, breakthrough ideas that
arrive fully formed, and a drive to succeed that burns brighter than healthy.
The company's innovative products carry subtle influence that spreads The
Resonance's reach to every user.

The binding site lies beneath the oldest parking structure, where strange
symbols appear in the concrete and security cameras occasionally capture
impossible shadows. Maintenance crews who investigate too closely tend to
find new, better jobs elsewhere.""",
            "reliquary_type": "location",
            "location_size": "Corporate campus with underground parking",
            "max_health_levels": 25,
            "current_health_levels": 25,
            "soak_rating": 6,
            "has_pervasiveness": True,
            "has_manifestation": True,
            "manifestation_range": 200,
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Earthbound Site: {resonance_campus.name}")

    # The Frequency - Radio Tower
    frequency_tower, created = Reliquary.objects.get_or_create(
        name="KEXP Radio Tower (The Frequency)",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The radio tower that houses KEXP's transmitter also
broadcasts The Frequency's subliminal influence across Seattle. The Earthbound
demon has bound itself to the electromagnetic emissions, riding radio waves
into the dreams of everyone within range.

Late-night listeners sometimes hear music that wasn't broadcast, voices that
speak directly to their deepest desires, and advertisements for services that
don't exist in the mortal world. The station's employees experience unusual
creativity and disturbing dreams, which most attribute to the irregular hours.

The binding centers on the transmission equipment itself. The tower cannot
be decommissioned without releasing The Frequency - a possibility that certain
Fallen discuss in worried whispers.""",
            "reliquary_type": "location",
            "location_size": "Radio station and transmission tower",
            "max_health_levels": 15,
            "current_health_levels": 15,
            "soak_rating": 4,
            "has_pervasiveness": True,
            "has_manifestation": True,
            "manifestation_range": 50000,  # City-wide broadcast range
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Earthbound Site: {frequency_tower.name}")

    # =========================================================================
    # FACTION MEETING PLACES
    # =========================================================================

    # Stern Hospice - Reconciler Territory
    stern_hospice, created = Bastion.objects.get_or_create(
        name="Stern Memorial Hospice",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Michael Stern, host to the Reconciler leader Nazriel,
operates this hospice as both genuine charitable work and gathering place for
Fallen who seek redemption. The dying are treated with compassion, their final
days eased by care that sometimes borders on the miraculous.

The hospice serves as informal headquarters for the Reconciler faction. Demons
who wish to discuss philosophy, seek guidance, or simply exist among those who
share their hope gather in the meditation garden or the chapel. Nazriel's presence
suffuses the place with calm purpose.

The mortal staff know only that Dr. Stern is unusually dedicated and that his
patients' families often speak of peaceful deaths and inexplicable comfort.""",
            "ritual_strength": 4,
            "warding_level": 3,
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Faction Site: {stern_hospice.name}")

    # Victoria Tower - Faustian Territory
    victoria_tower, created = Bastion.objects.get_or_create(
        name="Victoria Tower",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Victoria Chen's corporate headquarters serves as the
Faustian faction's power base in Seattle. The tower houses legitimate business
operations alongside facilities for more esoteric dealings. Those who seek
power come here to bargain, and the Faustians are always willing to deal.

The building's upper floors contain ritual spaces disguised as executive
conference rooms, where pacts are sealed and prices negotiated. The security
is both physical and supernatural - mortals who attempt corporate espionage
find their efforts inexplicably frustrated.

Belial, who wears Victoria Chen, has made this tower a monument to ambition.
Every deal struck here feeds the Faustian agenda, whether the participants
realize the true nature of their bargains or not.""",
            "ritual_strength": 5,
            "warding_level": 4,
            "shroud": 7,
        },
    )
    if created:
        print(f"  Created Faction Site: {victoria_tower.name}")

    # Underground Bunker - Luciferan Territory
    luciferan_bunker, created = Bastion.objects.get_or_create(
        name="The Armory",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Somewhere beneath Seattle - the exact location shared only
among trusted Luciferans - lies the faction's armory and war room. The bunker
was constructed during Cold War paranoia and abandoned when its purpose was
forgotten. The Luciferans found it perfect for their needs.

The Armory stores weapons both mundane and reliquary, tactical plans for the
war against Heaven, and training facilities where Fallen practice combat arts
forgotten since the Rebellion. Azazel coordinates operations from here, planning
the next phase in a conflict that has lasted since creation.

Access requires proof of Luciferan loyalty. Other factions know the Armory exists
but not its location - a secret the Luciferans guard with lethal dedication.""",
            "ritual_strength": 3,
            "warding_level": 5,
            "shroud": 8,
        },
    )
    if created:
        print(f"  Created Faction Site: {luciferan_bunker.name}")

    # Blackwood Investigations - Cryptic Territory
    blackwood_office, created = Bastion.objects.get_or_create(
        name="Blackwood Investigations",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Sarah Blackwood's private investigation firm serves as
cover for Cryptic operations. The office appears ordinary - cluttered desks,
filing cabinets, the usual detective agency aesthetic - but the case files
contain information about matters far stranger than cheating spouses.

The Cryptics use this location to share discoveries, analyze patterns, and
coordinate their endless search for truth. Hasmed, wearing Sarah Blackwood,
has made this place a clearinghouse for mysteries - both those the Fallen
create and those they work to unravel.

The office's real value lies in its filing systems, which contain cross-referenced
information about supernatural activity throughout the Pacific Northwest. Those
who seek knowledge come here first, paying the Cryptics' price for information.""",
            "ritual_strength": 2,
            "warding_level": 2,
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Faction Site: {blackwood_office.name}")

    # =========================================================================
    # OTHER SIGNIFICANT LOCATIONS
    # =========================================================================

    # Puget Sound - Dagon's Domain
    dagon_domain, created = LocationModel.objects.get_or_create(
        name="The Voice Beneath (Puget Sound)",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Something ancient dwells in the deepest waters of Puget
Sound. Dagon, called The Voice Beneath, was bound here before European contact,
perhaps before humanity itself. The Earthbound's influence extends throughout
the Sound, touching every vessel that sails these waters.

Fishermen tell stories of impossible catches, of voices in the fog, of boats
that sail home alone after their crews vanish. The indigenous peoples knew
to avoid certain waters, knowledge that the settlers dismissed as superstition.
They learned better, though the lessons were costly.

The Fallen avoid Puget Sound when possible. Dagon's power is vast and alien,
following rules older than the Rebellion. Those who have attempted communication
returned changed, speaking of bargains too terrible to accept and prices already
paid.""",
            "shroud": 3,
            "gauntlet": 3,
        },
    )
    if created:
        print(f"  Created Domain: {dagon_domain.name}")

    # Museum Storage - Reliquary Cache
    museum_storage, created = LocationModel.objects.get_or_create(
        name="Museum of History Storage Facility",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Museum of History's off-site storage facility contains
more than dusty artifacts and forgotten donations. Among the catalogued items
lie several objects with demonic connections - reliquaries whose purpose has
been forgotten, artifacts touched by Earthbound influence, and items carried
by hosts long since dead.

The Fallen know of this cache and maintain careful watch over its contents.
Some items are too dangerous to remove; others await the right moment for
retrieval. The museum staff occasionally report strange dreams after working
late in certain sections.

Retrieving items from storage requires navigating both mundane security and
the attention of interested parties. More than one factional dispute has
played out in these climate-controlled corridors.""",
            "shroud": 6,
        },
    )
    if created:
        print(f"  Created Location: {museum_storage.name}")

    print("Demon locations populated successfully.")

    return {
        "earthbound": [foundation_church, resonance_campus, frequency_tower],
        "factions": [stern_hospice, victoria_tower, luciferan_bunker, blackwood_office],
        "other": [dagon_domain, museum_storage],
    }


if __name__ == "__main__":
    populate_demon_locations()
