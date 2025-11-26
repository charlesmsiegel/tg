"""
Seattle Test Chronicle - City Population

Creates the City of Seattle and assigns characters to it
using the characters M2M field.

Run with: python manage.py shell < populate_db/chronicle/test/city.py

Prerequisites:
- Run character scripts first (creates characters)
"""

from accounts.models import Profile
from characters.models.core.character import Character as CharacterModel
from locations.models.core.city import City
from game.models import Chronicle


def create_seattle_city():
    """Create Seattle as a City object with full details."""
    print("Creating City of Seattle...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    seattle, created = City.objects.get_or_create(
        name="Seattle",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Seattle, Washington - The Emerald City

A sprawling metropolis of over 700,000 mortals, Seattle serves as the stage for
supernatural conflict across multiple planes of existence. The city's rainy
climate, tech industry boom, and counter-culture history make it a uniquely
contested territory.

The Space Needle looms over a cityscape divided between gleaming corporate towers
and gritty underground passages. Pike Place Market teems with life both seen and
unseen, while the old underground tunnels beneath Pioneer Square hide secrets
dating back to the Great Fire of 1889.

For the supernatural beings who call Seattle home, the city represents opportunity
and danger in equal measure. The tech industry provides cover for reality hackers
and provides resources for those who can exploit it. The old forests of the
Cascades harbor ancient spirits and sacred caerns. The dead walk the halls of
historic buildings, bound by unfinished business. And in the shadows between
worlds, beings of dream and nightmare contest for the souls of the living.

Seattle is a city of contradictions - progressive yet haunted by its past,
modern yet steeped in mysticism, welcoming yet territorial. Those who thrive
here learn to navigate not just its streets, but its many overlapping realities.""",

            "population": 737015,  # 2022 census estimate

            "mood": """Melancholy and rain-soaked. The perpetual gray skies and drizzle
create an atmosphere of quiet introspection punctuated by bursts of creative energy.
There's a sense of isolation even in crowds - everyone rushing somewhere with
earbuds in, avoiding eye contact. Yet beneath the surface, passionate communities
form around art, music, tech, and stranger pursuits.""",

            "theme": """The collision of old and new. Ancient supernatural traditions
clash with modern technology. Historic grudges play out against the backdrop of
a city constantly reinventing itself. The theme explores how beings rooted in
the past adapt (or fail to adapt) to a world that changes faster every year.""",

            "media": """The Seattle Times covers mainstream news, while The Stranger
provides alternative coverage and cultural commentary. Local TV stations KING 5,
KOMO 4, and KIRO 7 compete for ratings. Tech blogs and podcasts proliferate,
many unknowingly brushing against supernatural topics. The Pike Place Market
News carries classified ads with very specific coded meanings for those who
know how to read them.""",

            "politicians": """Mayor: Sarah Chen (mortal, unknowing pawn of various factions)
City Council: A mix of progressives and moderates, several of whom have been
influenced by supernatural forces.
Police Chief: Marcus Williams (mortal, suspicious of 'weird cases')
King County Executive: David Reyes (mortal, connected to several hunting families)

The supernatural power brokers avoid direct political office but maintain
extensive influence through proxies, donations, and carefully applied pressure.""",
        },
    )

    if created:
        print(f"  Created City: {seattle.name}")
    else:
        print(f"  City already exists: {seattle.name}")

    return seattle


def assign_characters_to_city():
    """Assign all chronicle characters to Seattle."""
    print("\nAssigning Characters to Seattle...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        seattle = City.objects.get(name="Seattle", chronicle=chronicle)
    except City.DoesNotExist:
        print("  Error: Seattle city not found. Run create_seattle_city first.")
        return

    # Get all PC characters in the chronicle
    characters = CharacterModel.objects.filter(
        chronicle=chronicle,
        npc=False
    )

    assigned_count = 0
    skipped_count = 0

    for char in characters:
        if seattle.characters.filter(pk=char.pk).exists():
            skipped_count += 1
            continue

        seattle.characters.add(char)
        assigned_count += 1

    print(f"  Assigned {assigned_count} PCs to Seattle (skipped {skipped_count} existing)")

    # Also add important NPCs
    important_npcs = [
        "Prince Katrina Valdez",
        "Elder Speaks-With-Thunder",
        "High Priestess Morgan",
        "Duke Thornwood",
        "The Ferryman",
        "Archdeacon Malthus",
        "Hunter Cell Leader Stone",
        "Pharaoh Khafre",
    ]

    npc_assigned = 0
    for npc_name in important_npcs:
        try:
            npc = CharacterModel.objects.get(name=npc_name)
            if not seattle.characters.filter(pk=npc.pk).exists():
                seattle.characters.add(npc)
                npc_assigned += 1
        except CharacterModel.DoesNotExist:
            pass  # Skip if NPC doesn't exist

    print(f"  Assigned {npc_assigned} important NPCs to Seattle")

    # Print summary
    total = seattle.characters.count()
    print(f"\nSeattle now has {total} characters assigned")


def populate_city():
    """Main function to populate city data."""
    print("=" * 60)
    print("POPULATING CITY OF SEATTLE")
    print("=" * 60)

    create_seattle_city()
    assign_characters_to_city()

    print("\n" + "=" * 60)
    print("CITY POPULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_city()

populate_city()
