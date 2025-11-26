"""
Seattle Test Chronicle - Wraith Major NPCs

Creates major Wraith NPCs who hold positions of power:
Hierarchy officials, Anacreon, Legates, and Renegade leaders.

Run with: python manage.py shell < populate_db/chronicle/test/wraith_npc.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Wraith data must be loaded (guilds, legions)
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
# HIERARCHY LEADERSHIP - SEATTLE NECROPOLIS
# =============================================================================

HIERARCHY_LEADERSHIP = [
    {
        "name": "Anacreon Victoria",
        "concept": "Ruler of Seattle's Shadowlands",
        "guild": "Masquers",
        "life_date": "1842-1889",
        "description": "Anacreon Victoria has ruled Seattle's Necropolis since the Great Fire of 1889 "
                       "that killed her mortal form. She maintains order through a network of informants "
                       "and a reputation for brutal efficiency. Her Haunt is the ruins of what was once "
                       "Seattle's original city hall, preserved in the Shadowlands beneath Pioneer Square. "
                       "She enforces the Dictum Mortuum absolutely and has destroyed Renegades without mercy.",
        "strength": 3, "dexterity": 4, "stamina": 4,
        "charisma": 4, "manipulation": 5, "appearance": 4,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 5, "empathy": 3, "expression": 4, "intimidation": 5,
        "leadership": 5, "subterfuge": 5,
        "etiquette": 5, "melee": 3, "stealth": 3,
        "academics": 4, "enigmas": 3, "investigation": 4, "law": 4, "politics": 5, "occult": 4,
        "willpower": 10, "pathos": 10,
    },
    {
        "name": "Marshal Constantine",
        "concept": "Enforcer of the Dictum Mortuum",
        "guild": "Monitors",
        "life_date": "1880-1918",
        "description": "Marshal Constantine leads the Legion forces in Seattle, hunting those who would "
                       "breach the Dictum Mortuum or traffic with the living inappropriately. A veteran "
                       "of the Great War, he died in the influenza pandemic and found purpose enforcing "
                       "law among the dead. His efficiency is legendary; his mercy is not.",
        "strength": 4, "dexterity": 4, "stamina": 5,
        "charisma": 3, "manipulation": 3, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 5, "athletics": 4, "awareness": 4, "brawl": 4, "intimidation": 5, "streetwise": 4,
        "firearms": 4, "melee": 5, "stealth": 4,
        "investigation": 5, "law": 4, "occult": 3,
        "willpower": 9, "pathos": 8,
    },
    {
        "name": "Legate Sophia Chen",
        "concept": "Diplomatic liaison to other supernatural factions",
        "guild": "Sandmen",
        "life_date": "1920-1962",
        "description": "Legate Sophia serves as the Anacreon's diplomatic voice, maintaining the fragile "
                       "truces with other supernatural factions. She died during an assassination meant "
                       "for someone else, and her unfinished business is untangling the conspiracy that "
                       "killed her. Her ability to influence the dreams of the living makes her invaluable.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 5, "manipulation": 5, "appearance": 4,
        "perception": 4, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 4, "empathy": 5, "expression": 5, "leadership": 4, "subterfuge": 5,
        "etiquette": 5, "performance": 3,
        "academics": 4, "investigation": 4, "law": 3, "politics": 5, "occult": 3,
        "willpower": 8, "pathos": 9,
    },
]

# =============================================================================
# GUILD MASTERS
# =============================================================================

GUILD_MASTERS = [
    {
        "name": "The Architect",
        "concept": "Artificer guild master who shapes the Shadowlands",
        "guild": "Artificers",
        "life_date": "1860-1910",
        "description": "The Architect was a builder of the original Seattle, and he continues building "
                       "in the Shadowlands. His soulforged structures provide the Necropolis with its "
                       "infrastructure, and his knowledge of shaping plasm is unmatched. He charges "
                       "dearly for his services but delivers masterwork.",
        "strength": 3, "dexterity": 5, "stamina": 3,
        "charisma": 2, "manipulation": 3, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 4,
        "alertness": 3, "awareness": 4, "expression": 3,
        "crafts": 5, "melee": 2,
        "academics": 4, "enigmas": 5, "occult": 4, "science": 4,
        "willpower": 8, "pathos": 8,
    },
    {
        "name": "Sister Mercy",
        "concept": "Usurer guild master who trades in emotions",
        "guild": "Usurers",
        "life_date": "1890-1935",
        "description": "Sister Mercy was a nurse who died treating tuberculosis patients. Now she trades "
                       "in the currencies of the dead—emotions, memories, and Pathos itself. Her prices "
                       "seem fair until you realize what you've given away. She maintains the Necropolis's "
                       "economy with a gentle smile that never reaches her eyes.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 4, "manipulation": 5, "appearance": 4,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 4, "awareness": 5, "empathy": 5, "expression": 3, "subterfuge": 5,
        "etiquette": 4,
        "academics": 3, "enigmas": 4, "medicine": 4, "occult": 4,
        "willpower": 9, "pathos": 10,
    },
]

# =============================================================================
# RENEGADE LEADERS
# =============================================================================

RENEGADES = [
    {
        "name": "The Prophet",
        "concept": "Renegade leader preaching against the Hierarchy",
        "guild": "Oracles",
        "life_date": "1950-1999",
        "description": "The Prophet leads Seattle's Renegade faction, preaching that the Hierarchy has "
                       "betrayed the dead by collaborating with the forces of Oblivion. His visions of "
                       "the future show a coming storm that will reshape the Shadowlands. The Anacreon "
                       "has put a bounty on his corpus, but his followers hide him well.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 5, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 4, "awareness": 5, "empathy": 4, "expression": 5, "leadership": 5, "subterfuge": 4,
        "stealth": 4,
        "enigmas": 5, "occult": 5, "politics": 3,
        "willpower": 8, "pathos": 9,
    },
]

# =============================================================================
# SPECTRE THREATS
# =============================================================================

SPECTRES = [
    {
        "name": "The Whisper in the Depths",
        "concept": "Malfean servant lurking in Seattle's Nihils",
        "guild": None,
        "life_date": "Unknown",
        "description": "Something ancient sleeps in the Nihil beneath Puget Sound, and The Whisper is "
                       "its herald. This Spectre recruits the newly dead before the Hierarchy can reach "
                       "them, promising power and revenge. Those who listen find themselves sliding toward "
                       "Oblivion. Even the Anacreon fears what might emerge if the Whisper succeeds.",
        "strength": 5, "dexterity": 4, "stamina": 5,
        "charisma": 3, "manipulation": 5, "appearance": 1,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 5, "awareness": 5, "intimidation": 5, "subterfuge": 5,
        "stealth": 5,
        "enigmas": 5, "occult": 5,
        "willpower": 10, "pathos": 0,
    },
]


def create_hierarchy_npcs(chronicle, st_user):
    """Create Hierarchy leadership NPCs."""
    print("\n--- Creating Hierarchy Leadership ---")

    for data in HIERARCHY_LEADERSHIP:
        guild = Guild.objects.filter(name=data.get("guild")).first()

        wraith, created = Wraith.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "guild": guild,
                "life_date": data.get("life_date", ""),
            },
        )
        if created:
            apply_wraith_stats(wraith, data)
            print(f"  Created: {wraith.name}")
        else:
            print(f"  Already exists: {wraith.name}")


def create_guild_masters(chronicle, st_user):
    """Create Guild master NPCs."""
    print("\n--- Creating Guild Masters ---")

    for data in GUILD_MASTERS:
        guild = Guild.objects.filter(name=data.get("guild")).first()

        wraith, created = Wraith.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "guild": guild,
                "life_date": data.get("life_date", ""),
            },
        )
        if created:
            apply_wraith_stats(wraith, data)
            print(f"  Created: {wraith.name} ({data['guild']})")
        else:
            print(f"  Already exists: {wraith.name}")


def create_renegade_npcs(chronicle, st_user):
    """Create Renegade NPCs."""
    print("\n--- Creating Renegade Leaders ---")

    for data in RENEGADES:
        guild = Guild.objects.filter(name=data.get("guild")).first()

        wraith, created = Wraith.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "guild": guild,
                "life_date": data.get("life_date", ""),
            },
        )
        if created:
            apply_wraith_stats(wraith, data)
            print(f"  Created: {wraith.name}")
        else:
            print(f"  Already exists: {wraith.name}")


def create_spectre_npcs(chronicle, st_user):
    """Create Spectre threat NPCs."""
    print("\n--- Creating Spectre Threats ---")

    for data in SPECTRES:
        wraith, created = Wraith.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "life_date": data.get("life_date", ""),
            },
        )
        if created:
            apply_wraith_stats(wraith, data)
            print(f"  Created: {wraith.name}")
        else:
            print(f"  Already exists: {wraith.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Wraith Major NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_hierarchy_npcs(chronicle, st_user)
    create_guild_masters(chronicle, st_user)
    create_renegade_npcs(chronicle, st_user)
    create_spectre_npcs(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Wraith major NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
