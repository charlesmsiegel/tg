"""
Seattle Test Chronicle - Hunter Major NPCs

Creates major Hunter NPCs who hold positions of influence:
Regional network leaders, Messengers, and veteran hunters.

Run with: python manage.py shell < populate_db/chronicle/test/hunter_npc.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Hunter data must be loaded (creeds, edges)
"""

from django.contrib.auth.models import User

from characters.models.hunter.hunter import Hunter
from characters.models.hunter.creed import Creed
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_hunter_stats(hunter, data):
    """Apply stats to a Hunter NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(hunter, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "dodge", "empathy",
                    "expression", "intimidation", "intuition", "leadership", "streetwise",
                    "subterfuge", "crafts", "demolitions", "drive", "etiquette",
                    "firearms", "larceny", "melee", "performance", "security", "stealth",
                    "survival", "technology", "academics", "bureaucracy", "computer",
                    "finance", "investigation", "law", "linguistics", "medicine",
                    "occult", "politics", "research", "science"]:
        if ability in data:
            setattr(hunter, ability, data[ability])

    if "willpower" in data:
        hunter.willpower = data["willpower"]
    if "conviction" in data:
        hunter.conviction = data["conviction"]
    if "vision" in data:
        hunter.vision = data["vision"]
    if "zeal" in data:
        hunter.zeal = data["zeal"]

    hunter.save()


# =============================================================================
# REGIONAL NETWORK LEADERS
# =============================================================================

NETWORK_LEADERS = [
    {
        "name": "Samuel 'Prophet' Washington",
        "concept": "Visionary who coordinates Pacific Northwest hunters",
        "creed": "Visionary",
        "description": "Prophet was Imbued fifteen years ago during a vampire attack on his church. "
                       "His visions showed him the scope of the supernatural threat, and he's spent "
                       "the years since building a network that spans from Seattle to Portland to Vancouver. "
                       "He coordinates intel, arranges safe houses, and ensures hunters don't step on each "
                       "other's operations. His visions still guide him, though they've grown darker lately.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 4,
        "alertness": 4, "awareness": 5, "empathy": 4, "expression": 4, "leadership": 5, "subterfuge": 3,
        "drive": 2, "firearms": 3,
        "academics": 3, "investigation": 4, "occult": 5, "politics": 3,
        "willpower": 8, "conviction": 5, "vision": 4, "zeal": 2,
    },
    {
        "name": "Lisa 'Aegis' Chen",
        "concept": "Defender who protects hunter safe houses",
        "creed": "Defender",
        "description": "Aegis runs three safe houses in Seattle where hunters can recover, regroup, and "
                       "resupply. Her Imbuing came when she defended her family from a werewolf attack; "
                       "she lost two brothers but saved the rest. Now she protects other hunters like family. "
                       "Her houses are warded, stocked, and monitored. Monsters have learned not to attack "
                       "them directly.",
        "strength": 3, "dexterity": 3, "stamina": 4,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 4,
        "alertness": 5, "athletics": 3, "awareness": 4, "brawl": 3, "empathy": 3, "leadership": 3,
        "firearms": 4, "melee": 3, "security": 5, "survival": 3,
        "investigation": 3, "medicine": 3, "occult": 3,
        "willpower": 8, "conviction": 5, "vision": 2, "zeal": 3,
    },
    {
        "name": "Victor 'Executioner' Reyes",
        "concept": "Avenger who leads strike teams against monsters",
        "creed": "Avenger",
        "description": "Executioner doesn't coordinate or protect—he kills. His Imbuing came during a "
                       "mage attack that destroyed his life, and he's been destroying supernatural lives "
                       "ever since. He leads Seattle's most aggressive hunter cell, taking on targets "
                       "others consider suicide missions. His body is scarred, his mind is focused, and "
                       "his kill count is legendary. He answers to Prophet but operates independently.",
        "strength": 4, "dexterity": 4, "stamina": 4,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 5,
        "alertness": 5, "athletics": 4, "awareness": 3, "brawl": 5, "dodge": 4, "intimidation": 4,
        "firearms": 5, "melee": 5, "stealth": 4, "survival": 4,
        "investigation": 3, "occult": 3,
        "willpower": 9, "conviction": 3, "vision": 1, "zeal": 6,
    },
]

# =============================================================================
# MESSENGERS AND HERALDS
# =============================================================================

MESSENGERS = [
    {
        "name": "The Voice",
        "concept": "Mysterious herald who first contacted Seattle's Imbued",
        "creed": "Visionary",
        "description": "The Voice appeared to Seattle's first Imbued in 1999, speaking through static "
                       "on their phones and screens. They've never appeared in person, but their messages "
                       "guide the network. Some believe they're a powerful hunter; others think they're "
                       "something else entirely. The Voice knows things they shouldn't, sees threats before "
                       "they materialize, and vanishes when questioned too closely.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 4, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 5, "empathy": 3, "expression": 4, "intuition": 5, "subterfuge": 4,
        "technology": 4,
        "computer": 5, "investigation": 5, "occult": 5,
        "willpower": 9, "conviction": 4, "vision": 6, "zeal": 1,
    },
]

# =============================================================================
# VETERAN HUNTERS
# =============================================================================

VETERANS = [
    {
        "name": "Margaret 'Grandmother' Stone",
        "concept": "Innocent elder who provides guidance and healing",
        "creed": "Innocent",
        "description": "Grandmother Stone was Imbued at age sixty-five while volunteering at a homeless "
                       "shelter. She saw something feeding on the vulnerable and intervened. Now eighty, "
                       "she provides counsel to younger hunters, heals their wounds both physical and spiritual, "
                       "and reminds them why they fight. Her conviction that monsters can be redeemed makes "
                       "her controversial, but her results speak for themselves.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 5, "manipulation": 2, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 4,
        "alertness": 3, "awareness": 5, "empathy": 5, "expression": 4, "intuition": 4, "leadership": 3,
        "etiquette": 3,
        "academics": 3, "medicine": 4, "occult": 4,
        "willpower": 8, "conviction": 6, "vision": 3, "zeal": 1,
    },
    {
        "name": "Michael 'Hammer' O'Brien",
        "concept": "Martyr who has sacrificed everything for the hunt",
        "creed": "Martyr",
        "description": "Hammer lost his family, his career, his health, and most of his sanity to the hunt. "
                       "He's been Imbued for twenty years and shows every one of them. His body is failing "
                       "but his spirit remains unbroken. He takes the missions no one else will, absorbs "
                       "punishment that would kill lesser hunters, and never, ever backs down. He's looking "
                       "for one last fight worth dying in.",
        "strength": 3, "dexterity": 3, "stamina": 5,
        "charisma": 2, "manipulation": 1, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 4,
        "alertness": 4, "athletics": 3, "awareness": 4, "brawl": 4, "dodge": 3, "intimidation": 3,
        "firearms": 4, "melee": 4, "survival": 4,
        "investigation": 3, "medicine": 2, "occult": 4,
        "willpower": 10, "conviction": 4, "vision": 2, "zeal": 5,
    },
    {
        "name": "Dr. Patricia Cole",
        "concept": "Judge who determines which monsters can be spared",
        "creed": "Judge",
        "description": "Dr. Cole was a criminal psychologist before her Imbuing. Now she applies her "
                       "analytical skills to monsters, determining which pose true threats and which "
                       "might be left alone—or even rehabilitated. Her judgments are controversial but "
                       "informed by decades of studying the supernatural. She's created a database of "
                       "monster behaviors that has saved many hunter lives.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 3, "awareness": 4, "empathy": 4, "expression": 3, "intuition": 4, "subterfuge": 3,
        "etiquette": 3,
        "academics": 5, "computer": 3, "investigation": 5, "medicine": 3, "occult": 5, "research": 5,
        "willpower": 8, "conviction": 5, "vision": 3, "zeal": 2,
    },
]


def create_network_leaders(chronicle, st_user):
    """Create network leader NPCs."""
    print("\n--- Creating Network Leaders ---")

    for data in NETWORK_LEADERS:
        creed = Creed.objects.filter(name=data["creed"]).first()

        hunter, created = Hunter.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "creed": creed,
            },
        )
        if created:
            apply_hunter_stats(hunter, data)
            print(f"  Created: {hunter.name} ({data['creed']})")
        else:
            print(f"  Already exists: {hunter.name}")


def create_messengers(chronicle, st_user):
    """Create Messenger NPCs."""
    print("\n--- Creating Messengers ---")

    for data in MESSENGERS:
        creed = Creed.objects.filter(name=data["creed"]).first()

        hunter, created = Hunter.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "creed": creed,
            },
        )
        if created:
            apply_hunter_stats(hunter, data)
            print(f"  Created: {hunter.name}")
        else:
            print(f"  Already exists: {hunter.name}")


def create_veterans(chronicle, st_user):
    """Create veteran hunter NPCs."""
    print("\n--- Creating Veteran Hunters ---")

    for data in VETERANS:
        creed = Creed.objects.filter(name=data["creed"]).first()

        hunter, created = Hunter.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "creed": creed,
            },
        )
        if created:
            apply_hunter_stats(hunter, data)
            print(f"  Created: {hunter.name} ({data['creed']})")
        else:
            print(f"  Already exists: {hunter.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Hunter Major NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_network_leaders(chronicle, st_user)
    create_messengers(chronicle, st_user)
    create_veterans(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Hunter major NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
