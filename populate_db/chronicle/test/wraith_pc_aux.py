"""
Seattle Test Chronicle - Wraith PC Auxiliary NPCs

Creates wraith NPCs to support PC Backgrounds like Contacts, Allies, and Memoriam connections.
These are owned by the ST and represent the NPCs that PCs interact with through their backgrounds.

Note: Wraith backgrounds are different - they're mostly about other wraiths and connections
to the Shadowlands rather than mortal contacts.

Run with: python manage.py shell < populate_db/chronicle/test/wraith_pc_aux.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run wraith_characters.py first (creates PCs)
"""

from django.contrib.auth.models import User

from characters.models.wraith.wraith import Wraith
from characters.models.wraith.guild import Guild
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_wraith_stats(wraith, data):
    """Apply stats to a Wraith NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(wraith, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "empathy", "expression",
                    "intimidation", "leadership", "streetwise", "subterfuge",
                    "crafts", "drive", "etiquette", "firearms", "melee", "performance",
                    "larceny", "stealth", "survival", "technology",
                    "academics", "computer", "enigmas", "investigation", "law",
                    "linguistics", "medicine", "occult", "politics", "science"]:
        if ability in data:
            setattr(wraith, ability, data[ability])

    if "willpower" in data:
        wraith.willpower = data["willpower"]
    if "pathos" in data:
        wraith.pathos = data["pathos"]
    if "corpus" in data:
        wraith.corpus = data["corpus"]

    wraith.save()


# =============================================================================
# WRAITH CONTACT NPCs - Other wraiths who provide information in the Shadowlands
# =============================================================================

# Sergeant Major William Price's Contacts (2 dots) - Veterans community spirits
PRICE_CONTACTS = [
    {
        "name": "Private First Class Johnny 'Two-Step' Morales",
        "concept": "Vietnam veteran wraith who watches over the homeless vets",
        "guild": "Monitors",
        "life_date": "1951-1970",
        "description": "Died in Da Nang. Now keeps watch over Seattle's homeless veterans, "
                       "helping those close to death cross over peacefully. Knows every veteran spirit in the city.",
        "strength": 3, "dexterity": 3, "stamina": 3,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 2, "wits": 3,
        "alertness": 4, "athletics": 3, "awareness": 3, "brawl": 3, "empathy": 2,
        "firearms": 4, "melee": 2, "stealth": 3, "survival": 3,
        "willpower": 6, "pathos": 6,
    },
    {
        "name": "Lieutenant Commander Helena Frost",
        "concept": "Navy nurse wraith who comforts the dying",
        "guild": "Usurers",
        "life_date": "1920-1944",
        "description": "Served in the Pacific theater. Her Fetter is the Pearl Harbor memorial, "
                       "but she travels to Seattle often to help newly deceased veterans.",
        "strength": 2, "dexterity": 3, "stamina": 2,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 4, "intelligence": 3, "wits": 3,
        "alertness": 3, "awareness": 3, "empathy": 5, "expression": 2,
        "etiquette": 3, "medicine": 4, "investigation": 2, "occult": 2,
        "willpower": 7, "pathos": 7,
    },
]

# Jane Doe #47's Contacts (2 dots) - Cold case connections
JANE_CONTACTS = [
    {
        "name": "Detective Frank Callahan",
        "concept": "Ghost of murdered detective who never solved his last case",
        "guild": "Monitors",
        "life_date": "1935-1978",
        "description": "Was killed investigating organized crime. Now haunts the Seattle PD evidence room, "
                       "gathering information that might help solve cold cases—including Jane's.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 5, "intelligence": 4, "wits": 4,
        "alertness": 4, "awareness": 3, "empathy": 2, "intimidation": 3, "streetwise": 3,
        "investigation": 5, "law": 3, "politics": 2,
        "willpower": 7, "pathos": 5,
    },
    {
        "name": "Mary 'Bloody Mary' Chen",
        "concept": "Murder victim wraith who collects others' stories",
        "guild": "Masquers",
        "life_date": "1967-1989",
        "description": "Killed by a serial killer who was never caught. Now gathers the stories "
                       "of murdered wraiths, hoping to find patterns that lead to justice.",
        "strength": 2, "dexterity": 3, "stamina": 2,
        "charisma": 3, "manipulation": 4, "appearance": 3,
        "perception": 4, "intelligence": 3, "wits": 4,
        "alertness": 3, "awareness": 4, "empathy": 4, "subterfuge": 3,
        "performance": 3, "investigation": 4, "occult": 2,
        "willpower": 6, "pathos": 6,
    },
]

# =============================================================================
# WRAITH ALLY NPCs - Members of The Watch circle (mutual support)
# =============================================================================

# Circle allies - wraiths who support each other
WATCH_ALLIES = [
    {
        "name": "Sister Agnes",
        "concept": "Nun wraith who helps newly dead process their existence",
        "guild": "Usurers",
        "life_date": "1898-1962",
        "description": "Died of old age after a lifetime of service. Now helps newly dead wraiths "
                       "understand their condition and find peace. The Watch's spiritual anchor.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 2, "appearance": 3,
        "perception": 4, "intelligence": 3, "wits": 3,
        "alertness": 2, "awareness": 4, "empathy": 5, "expression": 3,
        "etiquette": 3, "occult": 4, "academics": 2,
        "willpower": 8, "pathos": 8,
    },
    {
        "name": "Raymond 'The Fixer' Brooks",
        "concept": "Gangster wraith who knows how to get things done",
        "guild": "Sandmen",
        "life_date": "1915-1952",
        "description": "Was a small-time fixer in Seattle's criminal underground. His connections "
                       "and street smarts still serve him well in the Shadowlands.",
        "strength": 3, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 4, "appearance": 2,
        "perception": 3, "intelligence": 3, "wits": 4,
        "alertness": 3, "brawl": 2, "intimidation": 3, "streetwise": 5, "subterfuge": 4,
        "larceny": 3, "melee": 2, "politics": 3,
        "willpower": 6, "pathos": 5,
    },
]

# =============================================================================
# MENTOR-LIKE NPCs - Elder wraiths who guide the PCs
# =============================================================================

ELDER_WRAITHS = [
    {
        "name": "The Librarian",
        "concept": "Ancient wraith who maintains knowledge of Seattle's dead",
        "for_circle": "The Watch",
        "guild": "Oracles",
        "life_date": "1802-1889",
        "description": "One of the oldest wraiths in Seattle. Maintains a vast mental library "
                       "of the city's dead and their stories. Advises The Watch on matters of history and lore.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 5, "intelligence": 5, "wits": 4,
        "alertness": 3, "awareness": 5, "empathy": 3, "expression": 4,
        "enigmas": 5, "occult": 5, "academics": 5, "investigation": 4,
        "willpower": 9, "pathos": 9,
    },
    {
        "name": "Captain Angus MacLeod",
        "concept": "Pioneer-era wraith who knows the Underworld's secrets",
        "for_circle": "The Mourners",
        "guild": "Harbingers",
        "life_date": "1820-1882",
        "description": "Scottish sailor who helped build Seattle. Has navigated the Tempest "
                       "for over a century and knows safe paths through the storm.",
        "strength": 3, "dexterity": 3, "stamina": 4,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 5, "intelligence": 3, "wits": 4,
        "alertness": 4, "athletics": 3, "awareness": 4, "brawl": 3, "leadership": 3,
        "crafts": 3, "melee": 3, "survival": 4, "occult": 4, "enigmas": 3,
        "willpower": 8, "pathos": 7,
    },
]


def create_contact_npcs(chronicle, st_user):
    """Create Contact NPCs for wraith PCs."""
    print("\n--- Creating Wraith Contact NPCs ---")

    all_contacts = [
        ("Sgt. Maj. William Price", PRICE_CONTACTS),
        ("Jane Doe #47", JANE_CONTACTS),
    ]

    for pc_name, contacts in all_contacts:
        print(f"\nContacts for {pc_name}:")
        for contact_data in contacts:
            guild = Guild.objects.filter(name=contact_data.get("guild")).first()

            wraith, created = Wraith.objects.get_or_create(
                name=contact_data["name"],
                owner=st_user,
                defaults={
                    "concept": contact_data["concept"],
                    "description": contact_data.get("description", ""),
                    "chronicle": chronicle,
                    "npc": True,
                    "status": "App",
                    "guild": guild,
                    "life_date": contact_data.get("life_date", ""),
                },
            )
            if created:
                apply_wraith_stats(wraith, contact_data)
                print(f"  Created: {wraith.name}")
            else:
                print(f"  Already exists: {wraith.name}")


def create_ally_npcs(chronicle, st_user):
    """Create Ally NPCs for wraith PCs (circle members)."""
    print("\n--- Creating Wraith Ally NPCs ---")

    print("\nThe Watch Circle Allies:")
    for ally_data in WATCH_ALLIES:
        guild = Guild.objects.filter(name=ally_data.get("guild")).first()

        wraith, created = Wraith.objects.get_or_create(
            name=ally_data["name"],
            owner=st_user,
            defaults={
                "concept": ally_data["concept"],
                "description": ally_data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "guild": guild,
                "life_date": ally_data.get("life_date", ""),
            },
        )
        if created:
            apply_wraith_stats(wraith, ally_data)
            print(f"  Created: {wraith.name}")
        else:
            print(f"  Already exists: {wraith.name}")


def create_elder_npcs(chronicle, st_user):
    """Create elder wraith NPCs who guide circles."""
    print("\n--- Creating Elder Wraith NPCs ---")

    for elder_data in ELDER_WRAITHS:
        guild = Guild.objects.filter(name=elder_data.get("guild")).first()

        wraith, created = Wraith.objects.get_or_create(
            name=elder_data["name"],
            owner=st_user,
            defaults={
                "concept": elder_data["concept"],
                "description": elder_data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "guild": guild,
                "life_date": elder_data.get("life_date", ""),
            },
        )
        if created:
            apply_wraith_stats(wraith, elder_data)
            print(f"  Created elder: {wraith.name} (for {elder_data['for_circle']})")
        else:
            print(f"  Already exists: {wraith.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Wraith PC Auxiliary NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_contact_npcs(chronicle, st_user)
    create_ally_npcs(chronicle, st_user)
    create_elder_npcs(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Wraith auxiliary NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
