"""
Wraith location population script for Seattle Test Chronicle.

Creates Haunts, Necropolis areas, Nihils, and other Shadowlands locations.
"""

from accounts.models import Profile
from game.models import Chronicle
from locations.models.core import LocationModel
from locations.models.wraith import Haunt, Necropolis, Nihil


def populate_wraith_locations():
    """Create all Wraith locations for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # NECROPOLIS
    # =========================================================================

    # Seattle Necropolis - Main Hierarchy stronghold
    seattle_necropolis, created = Necropolis.objects.get_or_create(
        name="Seattle Necropolis",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Seattle's Hierarchy headquarters occupies the Shadowlands
reflection of Pioneer Square's underground city. The buried streets that mortals
tour by day become a vast bureaucratic complex by night, where Anacreon Victoria
administers the affairs of the local dead.

The Necropolis extends far beyond the physical underground, reaching into the
Tempest-touched depths where older structures and forgotten souls dwell. The
architecture shifts between the original 1880s buildings and stranger geometries
that reflect the collective memory of Seattle's dead.

Legates and officials conduct the business of the Hierarchy here - registering
new wraiths, adjudicating disputes, assigning duties, and maintaining the uneasy
peace that keeps the Shadowlands from collapsing into chaos.""",
            "shroud": 4,
        },
    )
    if created:
        print(f"  Created Necropolis: {seattle_necropolis.name}")

    # =========================================================================
    # HAUNTS
    # =========================================================================

    # Thomas Blackwood's Speakeasy
    blackwood_speakeasy, created = Haunt.objects.get_or_create(
        name="Blackwood's Speakeasy",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Preserved exactly as it was the night Thomas Blackwood
died in a police raid in 1925, this underground speakeasy exists in a pocket of
frozen time within the Shadowlands. The jazz still plays, the drinks still pour,
and Blackwood himself tends bar for the restless dead.

The speakeasy serves as neutral ground in the Shadowlands, a place where Hierarchy
and Renegades alike can meet without violence. The prohibition-era ambiance attracts
wraiths from across Seattle's history, each finding something familiar in the
timeless atmosphere.

Thomas's great-granddaughter owns the building above, unknowingly serving as one
of his Fetters. He watches over her with fierce protectiveness, and woe betide any
wraith who threatens his family.""",
            "rank": 3,
            "shroud_rating": 3,
            "haunt_type": "place_of_tragedy",
            "haunt_size": "house",
            "faith_resonance": "Nostalgia, defiance, family loyalty",
            "attracts_ghosts": True,
            "shroud": 3,
        },
    )
    if created:
        print(f"  Created Haunt: {blackwood_speakeasy.name}")

    # Pike Place Ghost Market
    ghost_market, created = Haunt.objects.get_or_create(
        name="Pike Place Ghost Market",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Shadowlands reflection of Pike Place Market operates
as a bizarre bazaar where wraiths trade in memories, emotions, and stranger
currencies. Stalls sell Fetters, pathos, and artifacts from the living world
alongside goods that exist only in the lands of the dead.

The market draws wraiths from throughout the region, making it both a vital
economic hub and a dangerous place where the unwary can lose more than they
bargained for. Slavers sometimes lurk at the edges, seeking vulnerable souls
to drag into servitude.

The living market above generates constant emotional energy that bleeds through
the Shroud, feeding the ghostly commerce below. Some stalls have existed since
before Seattle burned in 1889.""",
            "rank": 3,
            "shroud_rating": 4,
            "haunt_type": "other",
            "haunt_size": "mansion",
            "faith_resonance": "Commerce, creativity, desperation",
            "attracts_ghosts": True,
            "shroud": 4,
        },
    )
    if created:
        print(f"  Created Haunt: {ghost_market.name}")

    # Seattle War Memorial
    war_memorial, created = Haunt.objects.get_or_create(
        name="Seattle War Memorial",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The war memorial in downtown Seattle serves as a potent
Haunt where the spirits of fallen soldiers gather. Multiple wraiths maintain
Fetters here, their names carved in stone or held in the memories of those who
visit to pay respects.

Corporal James Murphy's name is misspelled on one panel - a bureaucratic error
that binds him more tightly than accurate commemoration ever could. He stands
eternal guard here, protecting newer wraiths from Spectres and helping them
understand their new existence.

On Memorial Day and Veterans Day, the Shroud grows thin as collective mourning
strengthens the connection between living and dead. These times are both
dangerous and sacred.""",
            "rank": 2,
            "shroud_rating": 4,
            "haunt_type": "sacred_site",
            "haunt_size": "house",
            "faith_resonance": "Honor, sacrifice, remembered grief",
            "attracts_ghosts": True,
            "shroud": 4,
        },
    )
    if created:
        print(f"  Created Haunt: {war_memorial.name}")

    # Maritime Museum
    maritime_museum, created = Haunt.objects.get_or_create(
        name="Maritime Museum",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Maritime Museum houses artifacts from Seattle's
seafaring history, including Captain Henrik Johansson's ship's bell - the Fetter
that binds his spirit to the mortal world. The museum's Shadowlands reflection
echoes with the sounds of waves and distant fog horns.

Captain Johansson has made this place his territory, protecting it from less
honorable wraiths who would strip the museum of its emotional resonance. He
shares the space with other nautical ghosts, maintaining the traditions of
the sea even in death.

Artifacts in the museum occasionally manifest in the Shadowlands, allowing
wraiths to interact with physical history. Some pieces carry their own ghosts -
ships that sank with all hands, bells that tolled for the lost.""",
            "rank": 2,
            "shroud_rating": 4,
            "haunt_type": "other",
            "haunt_size": "mansion",
            "faith_resonance": "Seafaring tradition, loss at sea, maritime honor",
            "attracts_ghosts": True,
            "shroud": 4,
        },
    )
    if created:
        print(f"  Created Haunt: {maritime_museum.name}")

    # Seattle PD Evidence Room
    evidence_room, created = Haunt.objects.get_or_create(
        name="Seattle PD Cold Case Files",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Deep in Seattle PD's evidence storage, boxes of cold case
files contain the last physical traces of unsolved crimes. Jane Doe #47 maintains
her Fetter here - a case file from the 1970s that represents her only identity
in death as in life.

The evidence room's Shadowlands reflection is a maze of sorrow and injustice,
where the unresolved dead drift between boxes containing the fragments of their
stories. Jane has taken it upon herself to help these spirits find resolution,
solving in death the mysteries that eluded investigators in life.

The living investigators sense something in this room - a chill, a feeling of
being watched. Some listen to the whispers and follow leads they cannot explain.
Others ignore them, and the cold cases grow colder.""",
            "rank": 2,
            "shroud_rating": 5,
            "haunt_type": "crime_scene",
            "haunt_size": "apartment",
            "faith_resonance": "Justice denied, identity lost, persistent memory",
            "attracts_ghosts": True,
            "shroud": 5,
        },
    )
    if created:
        print(f"  Created Haunt: {evidence_room.name}")

    # =========================================================================
    # NIHILS
    # =========================================================================

    # Puget Sound Nihil
    puget_nihil, created = Nihil.objects.get_or_create(
        name="Puget Sound Nihil",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Something vast and terrible lurks in the Nihil that
opens in the deepest waters of Puget Sound. The Whisper in the Depths - a Spectre
of terrifying power - emerges from this wound in reality, and darker things
move in the Tempest-waters beyond.

The Nihil pulses with entropy, drawing in unwary wraiths and occasionally
vomiting forth horrors from the Labyrinth. The Hierarchy maintains a cordon
around its known extent, but the boundaries shift with the tides.

Some whisper that the Nihil connects to something older than the Shadowlands
themselves - a presence that waited in the deep waters before humanity came
to these shores. Whether this is Malfean influence or something stranger,
none can say.""",
            "shroud": 2,
        },
    )
    if created:
        print(f"  Created Nihil: {puget_nihil.name}")

    # Great Fire Memorial Nihil
    fire_nihil, created = Nihil.objects.get_or_create(
        name="Great Fire Memorial Nihil",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Where the Great Fire of 1889 burned hottest, a small
Nihil remains - a scar in the Shadowlands marking the mass death that occurred
here. The Nihil is small and relatively stable, but it serves as a reminder
of how quickly disaster can create passages to the Tempest.

New wraiths sometimes emerge here, drawn through by the fire's lingering
resonance. The Hierarchy stations watchers to greet (or capture) such arrivals.
Occasionally, something worse crawls out - echoes of those who died in terror
and flame, twisted into Spectral forms.

On the anniversary of the fire, the Nihil flares brighter, and the screams
of the burning can be heard throughout the Shadowlands.""",
            "shroud": 4,
        },
    )
    if created:
        print(f"  Created Nihil: {fire_nihil.name}")

    # =========================================================================
    # OTHER SHADOWLANDS LOCATIONS
    # =========================================================================

    # Underground Seattle Byways
    underground_byways, created = LocationModel.objects.get_or_create(
        name="Underground Seattle Byways",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Safe routes through the Necropolis, maintained by the
Hierarchy for official travel and by Renegades for escape. The byways wind
through the buried city, connecting Haunts and avoiding the most dangerous
areas of the Shadowlands.

Knowledge of the byways is valuable currency among Seattle's dead. The Hierarchy
controls the official maps, but Renegades have discovered alternate routes that
bypass checkpoints and surveillance. Neutral guides offer their services for
appropriate compensation.

The byways shift over time as the Shadowlands respond to changes in the living
city above. Construction projects can open new passages or close familiar ones
without warning.""",
            "shroud": 4,
        },
    )
    if created:
        print(f"  Created Byway: {underground_byways.name}")

    # Waterfront Shadows
    waterfront_shadows, created = LocationModel.objects.get_or_create(
        name="Waterfront Shadows",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The Shadowlands along Elliott Bay's waterfront are
treacherous territory. The boundary between land and sea creates unstable
passages, and the proximity to the Puget Sound Nihil means Spectres patrol
these areas more frequently than most.

Wraiths who fell into the harbor, drowned in accidents, or went down with
their ships haunt these waters. Most are harmless, lost in their final moments.
Some have become predators, dragging the unwary into the dark waters.

The Hierarchy advises against travel here without escort. The Renegades
use the waterfront as an escape route, willing to risk the dangers for
freedom from Hierarchy control.""",
            "shroud": 3,
        },
    )
    if created:
        print(f"  Created Location: {waterfront_shadows.name}")

    print("Wraith locations populated successfully.")

    return {
        "necropolis": [seattle_necropolis],
        "haunts": [
            blackwood_speakeasy,
            ghost_market,
            war_memorial,
            maritime_museum,
            evidence_room,
        ],
        "nihils": [puget_nihil, fire_nihil],
        "other": [underground_byways, waterfront_shadows],
    }


if __name__ == "__main__":
    populate_wraith_locations()
