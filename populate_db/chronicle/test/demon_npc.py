"""
Seattle Test Chronicle - Demon Major NPCs

Creates major Demon NPCs who hold positions of power:
Faction leaders, elder demons, and significant threats.

Run with: python manage.py shell < populate_db/chronicle/test/demon_npc.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Demon data must be loaded (houses, factions, lores)
"""

from django.contrib.auth.models import User

from characters.models.demon.demon import Demon
from characters.models.demon.house import DemonHouse
from characters.models.demon.faction import DemonFaction
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_demon_stats(demon, data):
    """Apply stats to a Demon NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(demon, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "empathy", "expression",
                    "intimidation", "intuition", "leadership", "streetwise", "subterfuge",
                    "crafts", "drive", "etiquette", "firearms", "larceny", "melee",
                    "performance", "security", "stealth", "survival", "technology",
                    "academics", "computer", "finance", "investigation", "law",
                    "linguistics", "medicine", "occult", "politics", "religion", "science"]:
        if ability in data:
            setattr(demon, ability, data[ability])

    if "faith" in data:
        demon.faith = data["faith"]
    if "torment" in data:
        demon.torment = data["torment"]
    if "willpower" in data:
        demon.willpower = data["willpower"]

    demon.save()


# =============================================================================
# FACTION LEADERS
# =============================================================================

FACTION_LEADERS = [
    {
        "name": "Michael Stern",
        "host_name": "Michael Stern",
        "celestial_name": "Nazriel",
        "concept": "Reconciler leader seeking redemption through humanity",
        "house": "Neberu",
        "faction": "Reconcilers",
        "description": "Nazriel was an angel of the stars who fell for love of humanity's potential. "
                       "Now wearing a hospice chaplain, he leads Seattle's Reconciler faction, believing "
                       "that only by helping humanity reach its full potential can the Fallen find redemption. "
                       "His patience is legendary, his faith unwavering, and his influence subtle but pervasive.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 5, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 4,
        "alertness": 3, "awareness": 5, "empathy": 5, "expression": 4, "leadership": 5, "subterfuge": 3,
        "etiquette": 4, "meditation": 4,
        "academics": 4, "cosmology": 5, "occult": 5, "religion": 5,
        "faith": 8, "torment": 3, "willpower": 9,
    },
    {
        "name": "Victoria Chen",
        "host_name": "Victoria Chen",
        "celestial_name": "Belial",
        "concept": "Faustian leader trading power for souls",
        "house": "Malefactor",
        "faction": "Faustians",
        "description": "Belial was one of the architects of the material world, now dwelling in a venture "
                       "capitalist whose ambition matched her own. She leads the Faustians of Seattle, "
                       "trading infernal power for mortal souls and temporal influence. Her network of "
                       "thralls extends throughout the tech industry, and her investments always pay off.",
        "strength": 3, "dexterity": 3, "stamina": 3,
        "charisma": 4, "manipulation": 5, "appearance": 4,
        "perception": 4, "intelligence": 5, "wits": 5,
        "alertness": 3, "awareness": 3, "empathy": 2, "intimidation": 4, "leadership": 4, "subterfuge": 5,
        "etiquette": 4, "technology": 3,
        "academics": 3, "computer": 4, "finance": 5, "investigation": 3, "law": 4, "politics": 5,
        "faith": 7, "torment": 5, "willpower": 8,
    },
    {
        "name": "Marcus Cole",
        "host_name": "Marcus Cole",
        "celestial_name": "Azazel",
        "concept": "Luciferan commander preparing for war",
        "house": "Devourer",
        "faction": "Luciferans",
        "description": "Azazel was a commander in the Host, now wearing a former military officer who "
                       "never stopped fighting. He leads Seattle's Luciferans, preparing for the inevitable "
                       "war against Heaven while seeking Lucifer himself. His demons are organized, "
                       "disciplined, and ready for battle. He tolerates no weakness and accepts no surrender.",
        "strength": 5, "dexterity": 4, "stamina": 5,
        "charisma": 3, "manipulation": 3, "appearance": 3,
        "perception": 4, "intelligence": 4, "wits": 5,
        "alertness": 4, "athletics": 4, "awareness": 3, "brawl": 5, "intimidation": 5, "leadership": 5,
        "firearms": 5, "melee": 5, "stealth": 3, "survival": 4,
        "investigation": 3, "occult": 3, "politics": 3,
        "faith": 7, "torment": 6, "willpower": 9,
    },
    {
        "name": "Sarah Blackwood",
        "host_name": "Sarah Blackwood",
        "celestial_name": "Hasmed",
        "concept": "Cryptic observer watching all factions",
        "house": "Fiend",
        "faction": "Cryptics",
        "description": "Hasmed was an angel of knowledge who catalogued the secrets of creation. Now she "
                       "wears an investigative journalist whose curiosity got her killed, then resurrected "
                       "by the demon's possession. She leads the Cryptics, seeking understanding of why "
                       "they fell and what the Abyss truly was. She watches all factions, trusts none.",
        "strength": 2, "dexterity": 3, "stamina": 2,
        "charisma": 3, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 4, "empathy": 3, "expression": 4, "subterfuge": 5,
        "stealth": 3, "technology": 3,
        "academics": 5, "computer": 4, "investigation": 5, "occult": 5, "science": 4,
        "faith": 6, "torment": 4, "willpower": 8,
    },
    {
        "name": "James Dark",
        "host_name": "James Dark",
        "celestial_name": "Apollyon",
        "concept": "Ravener destroyer seeking an end to all things",
        "house": "Slayer",
        "faction": "Raveners",
        "description": "Apollyon was an angel of death whose endless service drove him to madness. "
                       "He wears a serial killer whose violence attracted the demon like calls to like. "
                       "He leads the Raveners—those few who haven't destroyed themselves yet—in a "
                       "campaign of destruction against anything of value. He is death walking.",
        "strength": 5, "dexterity": 5, "stamina": 5,
        "charisma": 2, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 5,
        "alertness": 5, "athletics": 4, "awareness": 3, "brawl": 5, "intimidation": 5, "streetwise": 4,
        "firearms": 4, "melee": 5, "stealth": 5, "survival": 4,
        "occult": 3,
        "faith": 5, "torment": 9, "willpower": 8,
    },
]

# =============================================================================
# ELDER DEMONS
# =============================================================================

ELDER_DEMONS = [
    {
        "name": "The Watcher",
        "host_name": "Unknown",
        "celestial_name": "Semyaza",
        "concept": "Ancient Neberu who has observed Seattle since its founding",
        "house": "Neberu",
        "faction": "Cryptics",
        "description": "Semyaza is old—one of the first to fall, one of the last to escape the Abyss. "
                       "They have observed Seattle since it was a fishing village, wearing hosts from "
                       "each era. Their current host is unknown even to other demons. They watch, they "
                       "wait, and they remember everything. Their knowledge is vast; their price is steep.",
        "strength": 3, "dexterity": 3, "stamina": 4,
        "charisma": 3, "manipulation": 5, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 5, "awareness": 5, "empathy": 4, "expression": 3, "subterfuge": 5,
        "etiquette": 4, "stealth": 5,
        "academics": 5, "enigmas": 5, "investigation": 5, "occult": 5, "politics": 4, "science": 4,
        "faith": 9, "torment": 5, "willpower": 10,
    },
]

# =============================================================================
# EARTHBOUND
# =============================================================================

EARTHBOUND = [
    {
        "name": "The Voice Beneath",
        "host_name": None,
        "celestial_name": "Dagon",
        "concept": "Earthbound bound to something beneath Puget Sound",
        "house": "Defiler",
        "faction": None,
        "description": "Something fell from Heaven before the Abyss opened and bound itself to the waters "
                       "of what would become Puget Sound. It calls itself Dagon now, and its influence "
                       "seeps through the dreams of fishermen and sailors. Ships occasionally vanish. "
                       "Things wash ashore that shouldn't exist. The Voice Beneath is patient, old beyond "
                       "measure, and hungry.",
        "strength": 6, "dexterity": 4, "stamina": 6,
        "charisma": 3, "manipulation": 5, "appearance": 1,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 5, "awareness": 5, "intimidation": 5, "subterfuge": 5,
        "stealth": 5, "survival": 5,
        "enigmas": 5, "occult": 5,
        "faith": 10, "torment": 10, "willpower": 10,
    },
]


def create_faction_leaders(chronicle, st_user):
    """Create faction leader NPCs."""
    print("\n--- Creating Faction Leaders ---")

    for data in FACTION_LEADERS:
        house = DemonHouse.objects.filter(name=data["house"]).first()
        faction = DemonFaction.objects.filter(name=data["faction"]).first()

        demon, created = Demon.objects.get_or_create(
            name=data["host_name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "house": house,
                "faction": faction,
                "host_name": data.get("host_name", ""),
            },
        )
        if created:
            apply_demon_stats(demon, data)
            print(f"  Created: {demon.name} ({data['faction']} leader)")
        else:
            print(f"  Already exists: {demon.name}")


def create_elder_demons(chronicle, st_user):
    """Create elder demon NPCs."""
    print("\n--- Creating Elder Demons ---")

    for data in ELDER_DEMONS:
        house = DemonHouse.objects.filter(name=data["house"]).first()
        faction = DemonFaction.objects.filter(name=data.get("faction")).first()

        name = data["host_name"] if data["host_name"] else data["celestial_name"]
        demon, created = Demon.objects.get_or_create(
            name=name,
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "house": house,
                "faction": faction,
                "host_name": data.get("host_name", ""),
            },
        )
        if created:
            apply_demon_stats(demon, data)
            print(f"  Created: {name}")
        else:
            print(f"  Already exists: {name}")


def create_earthbound(chronicle, st_user):
    """Create Earthbound NPCs."""
    print("\n--- Creating Earthbound ---")

    for data in EARTHBOUND:
        house = DemonHouse.objects.filter(name=data["house"]).first()

        name = data["celestial_name"]
        demon, created = Demon.objects.get_or_create(
            name=name,
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "house": house,
            },
        )
        if created:
            apply_demon_stats(demon, data)
            print(f"  Created: {name} (Earthbound)")
        else:
            print(f"  Already exists: {name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Demon Major NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_faction_leaders(chronicle, st_user)
    create_elder_demons(chronicle, st_user)
    create_earthbound(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Demon major NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
