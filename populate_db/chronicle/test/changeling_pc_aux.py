"""
Seattle Test Chronicle - Changeling PC Auxiliary NPCs

Creates mortal and changeling NPCs to support PC Backgrounds like Contacts, Allies, Mentors, Dreamers.
These are owned by the ST and represent the NPCs that PCs interact with through their backgrounds.

Run with: python manage.py shell < populate_db/chronicle/test/changeling_pc_aux.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run changeling_characters.py first (creates PCs)
"""

from django.contrib.auth.models import User

from characters.models.changeling.changeling import Changeling
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.changeling.kith import Kith
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_human_stats(human, data):
    """Apply stats to a CtDHuman NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(human, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "brawl", "empathy", "expression",
                    "intimidation", "kenning", "leadership", "streetwise", "subterfuge",
                    "crafts", "drive", "etiquette", "firearms", "larceny", "melee",
                    "performance", "stealth", "survival", "technology",
                    "academics", "computer", "enigmas", "gremayre", "investigation",
                    "law", "linguistics", "medicine", "occult", "politics", "science"]:
        if ability in data:
            setattr(human, ability, data[ability])

    if "willpower" in data:
        human.willpower = data["willpower"]

    human.save()


# =============================================================================
# CONTACT NPCs - Mortals who provide information to changeling PCs
# =============================================================================

# Neon's Contacts (3 dots) - Club scene
NEON_CONTACTS = [
    {
        "name": "DJ Phosphor",
        "concept": "Underground club promoter with every guest list",
        "description": "Runs the biggest underground parties in Seattle. Knows everyone in the club scene "
                       "and can get anyone into anywhere. Thinks he's lucky—doesn't know Neon blesses his events.",
        "strength": 2, "dexterity": 2, "stamina": 3,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 2, "intelligence": 2, "wits": 4,
        "empathy": 2, "expression": 3, "streetwise": 4, "subterfuge": 2, "performance": 4, "technology": 3,
        "willpower": 4,
    },
    {
        "name": "Claudia 'The Velvet' Monroe",
        "concept": "Burlesque performer and scene gossip",
        "description": "Performs at upscale venues and underground shows alike. Her ears catch every whisper "
                       "of gossip in Seattle's nightlife. Nothing happens in the scene without her knowing.",
        "strength": 1, "dexterity": 4, "stamina": 2,
        "charisma": 4, "manipulation": 3, "appearance": 5,
        "perception": 4, "intelligence": 3, "wits": 3,
        "alertness": 3, "empathy": 4, "expression": 4, "subterfuge": 3, "performance": 5, "etiquette": 2,
        "willpower": 4,
    },
    {
        "name": "Marcus 'Mix' Taylor",
        "concept": "Bartender at the hottest clubs",
        "description": "Works at three different venues. People tell bartenders everything, "
                       "and Mix has a perfect memory for secrets. Trades info for tips.",
        "strength": 2, "dexterity": 3, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 3,
        "perception": 4, "intelligence": 3, "wits": 4,
        "alertness": 3, "empathy": 3, "streetwise": 3, "subterfuge": 2, "crafts": 3,
        "willpower": 4,
    },
]

# Hollow's Contacts (3 dots) - Urban exploration community
HOLLOW_CONTACTS = [
    {
        "name": "Alex 'Crawlspace' Kim",
        "concept": "Urban explorer and tunnel expert",
        "description": "Knows every abandoned tunnel, forgotten basement, and hidden space in Seattle. "
                       "His maps are legendary in the urbex community. Fearless but practical.",
        "strength": 2, "dexterity": 4, "stamina": 3,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 5, "intelligence": 3, "wits": 4,
        "alertness": 4, "athletics": 3, "streetwise": 3, "larceny": 3, "stealth": 4, "survival": 3,
        "willpower": 5,
    },
    {
        "name": "Sarah 'Lens' Nakamura",
        "concept": "Urban exploration photographer and archivist",
        "description": "Documents abandoned spaces before they're demolished. Has photographed places "
                       "that no longer exist. Her archive is a treasure trove of Seattle's hidden history.",
        "strength": 1, "dexterity": 3, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 3,
        "perception": 4, "intelligence": 4, "wits": 3,
        "alertness": 3, "expression": 4, "crafts": 3, "technology": 3, "academics": 3, "investigation": 3,
        "willpower": 4,
    },
    {
        "name": "Derek 'Ghost' O'Brien",
        "concept": "Security guard who looks the other way",
        "description": "Works security at various properties. For a fee, provides schedules, codes, "
                       "and turns off cameras. Has helped Hollow access a dozen 'secure' locations.",
        "strength": 3, "dexterity": 2, "stamina": 3,
        "charisma": 2, "manipulation": 3, "appearance": 2,
        "perception": 3, "intelligence": 2, "wits": 3,
        "alertness": 3, "streetwise": 3, "subterfuge": 2, "larceny": 2, "security": 4,
        "willpower": 4,
    },
]

# =============================================================================
# ALLY NPCs - Mortals who actively help changeling PCs
# =============================================================================

# Widget's Allies (2 dots) - Coffee shop regulars
WIDGET_ALLIES = [
    {
        "name": "Jamie Torres",
        "concept": "Aspiring novelist who writes in the cafe daily",
        "description": "Writes fantasy novels that unknowingly channel changeling themes. "
                       "A regular at Widget's cafe who'd do anything for his favorite barista.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 4, "wits": 3,
        "empathy": 3, "expression": 5, "computer": 3, "academics": 3, "investigation": 2,
        "willpower": 4,
    },
    {
        "name": "Professor Elena Vasquez",
        "concept": "Folklore professor and mythology enthusiast",
        "description": "Teaches folklore at the local university. Her academic knowledge of fairy tales "
                       "is extensive—and occasionally uncomfortably accurate about changeling society.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 3,
        "empathy": 2, "expression": 4, "academics": 5, "occult": 3, "investigation": 3,
        "willpower": 5,
    },
]

# =============================================================================
# DREAMER NPCs - Mortals who provide Glamour
# =============================================================================

# Pixel's Dreamers (1 dot) - Arcade regulars
PIXEL_DREAMERS = [
    {
        "name": "Kevin 'Speedrun' Park",
        "concept": "Competitive gamer chasing the perfect run",
        "description": "His pure dedication to mastering games generates glamour. "
                       "Unknowingly draws changelings to watch his attempts at impossible feats.",
        "strength": 1, "dexterity": 4, "stamina": 2,
        "charisma": 2, "manipulation": 1, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 5,
        "alertness": 3, "computer": 4, "technology": 3,
        "willpower": 5,
    },
]

# Widget's Dreamers (2 dots) - Cafe patrons
WIDGET_DREAMERS = [
    {
        "name": "Maya Chen",
        "concept": "Indie game developer with boundless creativity",
        "description": "Works on her game in the cafe every day. Her creative passion "
                       "and constant 'what if' thinking makes her a rich source of glamour.",
        "strength": 1, "dexterity": 3, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 3,
        "perception": 3, "intelligence": 4, "wits": 4,
        "expression": 4, "crafts": 4, "computer": 5, "technology": 3,
        "willpower": 4,
    },
    {
        "name": "Theo Washington",
        "concept": "Children's book illustrator who never grew up",
        "description": "Creates whimsical illustrations full of wonder. His childlike imagination "
                       "makes him one of the most potent glamour sources in the neighborhood.",
        "strength": 1, "dexterity": 4, "stamina": 2,
        "charisma": 4, "manipulation": 1, "appearance": 3,
        "perception": 4, "intelligence": 3, "wits": 3,
        "empathy": 3, "expression": 5, "crafts": 5, "academics": 2,
        "willpower": 4,
    },
]

# =============================================================================
# MENTOR NPCs - Elder changelings who guide PCs
# =============================================================================

MENTOR_CHANGELINGS = [
    {
        "name": "Grandfather Tinkerton",
        "concept": "Elder nocker and master craftsman",
        "for_pc": "Sprocket (mentoring Forge)",
        "kith": "Nocker",
        "seeming": "grump",
        "court": "unseelie",
        "description": "Has been building impossible machines for over a century. His workshop "
                       "exists partly in the Dreaming. Teaches that the best revenge on reality "
                       "is to force it to accept your creations.",
        "strength": 2, "dexterity": 5, "stamina": 2,
        "charisma": 2, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 4,
        "alertness": 2, "kenning": 4, "crafts": 5, "technology": 5, "science": 4, "enigmas": 3,
        "glamour": 8, "banality": 3, "willpower": 7,
    },
    {
        "name": "Lady Silvermist",
        "concept": "Sidhe noble and keeper of lost stories",
        "for_pc": "Lord Ashford",
        "kith": "Sidhe",
        "seeming": "grump",
        "court": "seelie",
        "description": "An ancient sidhe who remembers the Sundering. Collects and protects stories "
                       "that the Dreaming might otherwise forget. Elegant, proud, and deeply sad.",
        "strength": 2, "dexterity": 3, "stamina": 2,
        "charisma": 5, "manipulation": 4, "appearance": 5,
        "perception": 4, "intelligence": 4, "wits": 4,
        "empathy": 4, "expression": 4, "kenning": 5, "etiquette": 5, "academics": 4, "occult": 4,
        "glamour": 9, "banality": 2, "willpower": 8,
    },
]


def create_contact_npcs(chronicle, st_user):
    """Create Contact NPCs for changeling PCs."""
    print("\n--- Creating Contact NPCs ---")

    all_contacts = [
        ("Neon", NEON_CONTACTS),
        ("Hollow", HOLLOW_CONTACTS),
    ]

    for pc_name, contacts in all_contacts:
        print(f"\nContacts for {pc_name}:")
        for contact_data in contacts:
            human, created = CtDHuman.objects.get_or_create(
                name=contact_data["name"],
                owner=st_user,
                defaults={
                    "concept": contact_data["concept"],
                    "description": contact_data.get("description", ""),
                    "chronicle": chronicle,
                    "npc": True,
                    "status": "App",
                },
            )
            if created:
                apply_human_stats(human, contact_data)
                print(f"  Created: {human.name}")
            else:
                print(f"  Already exists: {human.name}")


def create_ally_npcs(chronicle, st_user):
    """Create Ally NPCs for changeling PCs."""
    print("\n--- Creating Ally NPCs ---")

    all_allies = [
        ("Widget", WIDGET_ALLIES),
    ]

    for pc_name, allies in all_allies:
        print(f"\nAllies for {pc_name}:")
        for ally_data in allies:
            human, created = CtDHuman.objects.get_or_create(
                name=ally_data["name"],
                owner=st_user,
                defaults={
                    "concept": ally_data["concept"],
                    "description": ally_data.get("description", ""),
                    "chronicle": chronicle,
                    "npc": True,
                    "status": "App",
                },
            )
            if created:
                apply_human_stats(human, ally_data)
                print(f"  Created: {human.name}")
            else:
                print(f"  Already exists: {human.name}")


def create_dreamer_npcs(chronicle, st_user):
    """Create Dreamer NPCs for changeling PCs."""
    print("\n--- Creating Dreamer NPCs ---")

    all_dreamers = [
        ("Pixel", PIXEL_DREAMERS),
        ("Widget", WIDGET_DREAMERS),
    ]

    for pc_name, dreamers in all_dreamers:
        print(f"\nDreamers for {pc_name}:")
        for dreamer_data in dreamers:
            human, created = CtDHuman.objects.get_or_create(
                name=dreamer_data["name"],
                owner=st_user,
                defaults={
                    "concept": dreamer_data["concept"],
                    "description": dreamer_data.get("description", ""),
                    "chronicle": chronicle,
                    "npc": True,
                    "status": "App",
                },
            )
            if created:
                apply_human_stats(human, dreamer_data)
                print(f"  Created: {human.name}")
            else:
                print(f"  Already exists: {human.name}")


def create_mentor_npcs(chronicle, st_user):
    """Create Mentor NPCs (elder changelings) for changeling PCs."""
    print("\n--- Creating Mentor NPCs ---")

    for mentor_data in MENTOR_CHANGELINGS:
        kith = Kith.objects.filter(name=mentor_data["kith"]).first()

        changeling, created = Changeling.objects.get_or_create(
            name=mentor_data["name"],
            owner=st_user,
            defaults={
                "concept": mentor_data["concept"],
                "description": mentor_data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "kith": kith,
                "seeming": mentor_data.get("seeming", ""),
                "court": mentor_data.get("court", ""),
            },
        )
        if created:
            # Apply attributes and abilities
            for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                         "appearance", "perception", "intelligence", "wits"]:
                if attr in mentor_data:
                    setattr(changeling, attr, mentor_data[attr])

            for ability in ["alertness", "athletics", "brawl", "empathy", "expression",
                            "intimidation", "kenning", "leadership", "streetwise", "subterfuge",
                            "crafts", "drive", "etiquette", "firearms", "larceny", "melee",
                            "performance", "stealth", "survival", "technology",
                            "academics", "computer", "enigmas", "gremayre", "investigation",
                            "law", "linguistics", "medicine", "occult", "politics", "science"]:
                if ability in mentor_data:
                    setattr(changeling, ability, mentor_data[ability])

            if "glamour" in mentor_data:
                changeling.glamour = mentor_data["glamour"]
            if "banality" in mentor_data:
                changeling.banality = mentor_data["banality"]
            if "willpower" in mentor_data:
                changeling.willpower = mentor_data["willpower"]

            changeling.save()
            print(f"  Created mentor: {changeling.name} (for {mentor_data['for_pc']})")
        else:
            print(f"  Already exists: {changeling.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Changeling PC Auxiliary NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_contact_npcs(chronicle, st_user)
    create_ally_npcs(chronicle, st_user)
    create_dreamer_npcs(chronicle, st_user)
    create_mentor_npcs(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Changeling auxiliary NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
