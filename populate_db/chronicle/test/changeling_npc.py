"""
Seattle Test Chronicle - Changeling Major NPCs

Creates major Changeling NPCs who hold positions of power:
Freehold leadership, Court nobles, and House representatives.

Run with: python manage.py shell < populate_db/chronicle/test/changeling_npc.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Changeling data must be loaded (kith, arts, realms)
"""

from django.contrib.auth.models import User

from characters.models.changeling.changeling import Changeling
from characters.models.changeling.kith import Kith
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_changeling_stats(changeling, data):
    """Apply stats to a Changeling NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(changeling, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "brawl", "empathy", "expression",
                    "intimidation", "kenning", "leadership", "streetwise", "subterfuge",
                    "crafts", "drive", "etiquette", "firearms", "larceny", "melee",
                    "performance", "stealth", "survival", "technology",
                    "academics", "computer", "enigmas", "gremayre", "investigation",
                    "law", "linguistics", "medicine", "occult", "politics", "science"]:
        if ability in data:
            setattr(changeling, ability, data[ability])

    if "glamour" in data:
        changeling.glamour = data["glamour"]
    if "banality" in data:
        changeling.banality = data["banality"]
    if "willpower" in data:
        changeling.willpower = data["willpower"]

    changeling.save()


# =============================================================================
# FREEHOLD LEADERSHIP - THE EMERALD COURT
# =============================================================================

FREEHOLD_LEADERSHIP = [
    {
        "name": "Duke Rowan of the Emerald Throne",
        "concept": "Sidhe Duke ruling Seattle's freehold",
        "kith": "Sidhe",
        "seeming": "grump",
        "court": "seelie",
        "description": "Duke Rowan has held the Emerald Throne for three decades, the longest rule in the "
                       "freehold's history. His domain is the Pike Place Market, where the dreams of "
                       "tourists and artists feed a powerful balefire. He rules with elegance and "
                       "political acumen, balancing Seelie traditions with the realities of the modern "
                       "age. The tech industry's growth has brought both opportunity and Banality to his realm.",
        "strength": 3, "dexterity": 4, "stamina": 3,
        "charisma": 5, "manipulation": 4, "appearance": 5,
        "perception": 4, "intelligence": 5, "wits": 5,
        "alertness": 3, "empathy": 4, "expression": 4, "kenning": 5, "leadership": 5, "subterfuge": 4,
        "etiquette": 5, "melee": 4, "performance": 3,
        "academics": 4, "enigmas": 4, "gremayre": 5, "law": 4, "politics": 5,
        "glamour": 9, "banality": 3, "willpower": 9,
    },
    {
        "name": "Countess Lysandra Moonshadow",
        "concept": "Unseelie Sidhe countess and rival to the Duke",
        "kith": "Sidhe",
        "seeming": "grump",
        "court": "unseelie",
        "description": "Countess Lysandra leads the Unseelie Court in Seattle, maintaining an uneasy "
                       "alliance with Duke Rowan while pursuing her own agenda. Her domain is the "
                       "underground—literally, the old Seattle beneath Pioneer Square, and figuratively, "
                       "the city's nightlife. She believes the Seelie way is dying and that only the "
                       "Unseelie embrace of change can save the Kithain.",
        "strength": 3, "dexterity": 4, "stamina": 3,
        "charisma": 4, "manipulation": 5, "appearance": 5,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 4, "awareness": 3, "empathy": 3, "intimidation": 4, "kenning": 4, "leadership": 4, "subterfuge": 5,
        "etiquette": 4, "stealth": 4,
        "enigmas": 4, "gremayre": 4, "occult": 3, "politics": 5,
        "glamour": 8, "banality": 3, "willpower": 8,
    },
    {
        "name": "Baron Ironwright",
        "concept": "Nocker baron overseeing the crafters",
        "kith": "Nocker",
        "seeming": "grump",
        "court": "unseelie",
        "description": "Baron Ironwright holds title over Seattle's maker community, both mortal and fae. "
                       "His junkyard workshop produces impossible devices, and his approval is required "
                       "for any major chimerical construction in the freehold. He's surly, brilliant, "
                       "and absolutely essential to the realm's infrastructure.",
        "strength": 4, "dexterity": 5, "stamina": 4,
        "charisma": 2, "manipulation": 3, "appearance": 2,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 3, "awareness": 2, "kenning": 4, "streetwise": 3,
        "crafts": 5, "drive": 3, "melee": 3, "technology": 5,
        "academics": 3, "computer": 4, "enigmas": 5, "gremayre": 4, "science": 5,
        "glamour": 8, "banality": 4, "willpower": 8,
    },
]

# =============================================================================
# HOUSE REPRESENTATIVES
# =============================================================================

HOUSE_REPS = [
    {
        "name": "Lord Aldric Gwydion",
        "concept": "House Gwydion diplomat seeking unity",
        "kith": "Sidhe",
        "seeming": "grump",
        "court": "seelie",
        "description": "Lord Aldric represents House Gwydion's interests in Seattle, advocating for "
                       "traditional values while acknowledging the need for adaptation. He serves as "
                       "the Duke's chief counselor and troubleshooter, handling problems before they "
                       "become crises. His legendary patience is matched only by his skill with a blade.",
        "strength": 3, "dexterity": 4, "stamina": 3,
        "charisma": 4, "manipulation": 4, "appearance": 4,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 3, "empathy": 4, "expression": 3, "kenning": 4, "leadership": 4, "subterfuge": 3,
        "etiquette": 5, "melee": 5,
        "academics": 3, "enigmas": 3, "gremayre": 4, "law": 4, "politics": 4,
        "glamour": 7, "banality": 3, "willpower": 7,
    },
    {
        "name": "Lady Morgaine Ailil",
        "concept": "House Ailil schemer working the shadows",
        "kith": "Sidhe",
        "seeming": "grump",
        "court": "unseelie",
        "description": "Lady Morgaine represents House Ailil, though 'represent' suggests more transparency "
                       "than she employs. Her schemes within schemes keep even the Countess guessing, "
                       "and her network of informants rivals the Sluagh. She wants power, but her ultimate "
                       "goals remain hidden even from those who think they know her.",
        "strength": 2, "dexterity": 4, "stamina": 2,
        "charisma": 4, "manipulation": 5, "appearance": 4,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 3, "empathy": 3, "kenning": 4, "subterfuge": 5,
        "etiquette": 4, "larceny": 3, "stealth": 4,
        "enigmas": 4, "gremayre": 4, "investigation": 4, "politics": 5,
        "glamour": 7, "banality": 3, "willpower": 8,
    },
]

# =============================================================================
# COMMONER LEADERS
# =============================================================================

COMMONER_LEADERS = [
    {
        "name": "Grandmother Moss",
        "concept": "Boggan elder who remembers before the Sundering",
        "kith": "Boggan",
        "seeming": "grump",
        "court": "seelie",
        "description": "Grandmother Moss is old—old enough to remember the Shattering, old enough to have "
                       "helped build the first freehold in what would become Seattle. She cares for the "
                       "lost and forgotten changelings, maintains the hospitality traditions, and knows "
                       "secrets the Sidhe have forgotten. Her cottage exists somewhere between Pike Place "
                       "and the Dreaming.",
        "strength": 2, "dexterity": 3, "stamina": 4,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 5, "empathy": 5, "kenning": 5, "leadership": 3, "streetwise": 3,
        "crafts": 5, "etiquette": 4,
        "academics": 3, "enigmas": 5, "gremayre": 5, "medicine": 4, "occult": 4,
        "glamour": 9, "banality": 2, "willpower": 9,
    },
    {
        "name": "The King of Whispers",
        "concept": "Sluagh information broker who knows everyone's secrets",
        "kith": "Sluagh",
        "seeming": "grump",
        "court": "unseelie",
        "description": "No one knows the King of Whispers' true name, only that they've been trading secrets "
                       "in Seattle since before the tech boom. Their network of listeners extends throughout "
                       "the freehold, and nothing said in shadow escapes their notice. They sell information "
                       "to all sides, maintaining neutrality through necessity—everyone needs them.",
        "strength": 2, "dexterity": 4, "stamina": 2,
        "charisma": 2, "manipulation": 5, "appearance": 2,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 5, "awareness": 4, "empathy": 4, "kenning": 4, "streetwise": 4, "subterfuge": 5,
        "larceny": 4, "stealth": 5,
        "academics": 4, "enigmas": 5, "gremayre": 4, "investigation": 5, "occult": 4, "politics": 4,
        "glamour": 7, "banality": 4, "willpower": 8,
    },
]


def create_freehold_leadership(chronicle, st_user):
    """Create Freehold leadership NPCs."""
    print("\n--- Creating Freehold Leadership ---")

    for data in FREEHOLD_LEADERSHIP:
        kith = Kith.objects.filter(name=data["kith"]).first()

        changeling, created = Changeling.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "kith": kith,
                "seeming": data.get("seeming", ""),
                "court": data.get("court", ""),
            },
        )
        if created:
            apply_changeling_stats(changeling, data)
            print(f"  Created: {changeling.name}")
        else:
            print(f"  Already exists: {changeling.name}")


def create_house_reps(chronicle, st_user):
    """Create House representative NPCs."""
    print("\n--- Creating House Representatives ---")

    for data in HOUSE_REPS:
        kith = Kith.objects.filter(name=data["kith"]).first()

        changeling, created = Changeling.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "kith": kith,
                "seeming": data.get("seeming", ""),
                "court": data.get("court", ""),
            },
        )
        if created:
            apply_changeling_stats(changeling, data)
            print(f"  Created: {changeling.name}")
        else:
            print(f"  Already exists: {changeling.name}")


def create_commoner_leaders(chronicle, st_user):
    """Create Commoner leader NPCs."""
    print("\n--- Creating Commoner Leaders ---")

    for data in COMMONER_LEADERS:
        kith = Kith.objects.filter(name=data["kith"]).first()

        changeling, created = Changeling.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "kith": kith,
                "seeming": data.get("seeming", ""),
                "court": data.get("court", ""),
            },
        )
        if created:
            apply_changeling_stats(changeling, data)
            print(f"  Created: {changeling.name}")
        else:
            print(f"  Already exists: {changeling.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Changeling Major NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_freehold_leadership(chronicle, st_user)
    create_house_reps(chronicle, st_user)
    create_commoner_leaders(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Changeling major NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
