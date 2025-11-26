"""
Seattle Test Chronicle - Werewolf PC Auxiliary NPCs

Creates mortal, Kinfolk, and Garou NPCs to support PC Backgrounds like Contacts, Allies, Kinfolk, Mentors.
These are owned by the ST and represent the NPCs that PCs interact with through their backgrounds.

Run with: python manage.py shell < populate_db/chronicle/test/werewolf_pc_aux.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run werewolf_characters.py first (creates PCs)
"""

from django.contrib.auth.models import User

from characters.models.werewolf.garou import Garou
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.tribe import Tribe
from characters.models.werewolf.wtahuman import WtAHuman
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_human_stats(human, data):
    """Apply stats to a WtAHuman or Kinfolk NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(human, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "empathy", "expression",
                    "intimidation", "leadership", "primal_urge", "streetwise", "subterfuge",
                    "animal_ken", "crafts", "drive", "etiquette", "firearms", "melee",
                    "performance", "larceny", "stealth", "survival",
                    "academics", "computer", "enigmas", "investigation", "law",
                    "linguistics", "medicine", "occult", "politics", "rituals", "science", "technology"]:
        if ability in data:
            setattr(human, ability, data[ability])

    if "willpower" in data:
        human.willpower = data["willpower"]

    human.save()


# =============================================================================
# KINFOLK NPCs - Relatives who carry the Garou gene
# =============================================================================

# Kinfolk for the chronicle (mentioned in DESIGN.md)
KINFOLK_NPCS = [
    {
        "name": "Sarah Morningkill",
        "concept": "IT security specialist with corporate access",
        "tribe": "Glass Walkers",
        "breed": "homid",
        "relation": "Cousin to Runs-Through-Fire",
        "description": "Works at a major Seattle tech firm in their security division. "
                       "Provides the pack with insider access to corporate networks and intel. "
                       "Secretly channels company resources to support Garou operations.",
        "strength": 1, "dexterity": 3, "stamina": 2,
        "charisma": 2, "manipulation": 3, "appearance": 3,
        "perception": 4, "intelligence": 4, "wits": 3,
        "alertness": 2, "subterfuge": 3, "computer": 5, "technology": 4, "investigation": 3,
        "willpower": 5,
    },
    {
        "name": "Old Pete",
        "concept": "Street-wise food truck operator and information network",
        "tribe": "Bone Gnawers",
        "breed": "homid",
        "relation": "Pack's honorary uncle",
        "description": "Elderly Kinfolk who runs a beloved food truck that serves both humans and Garou. "
                       "His truck stops are neutral ground, and everyone owes him favors. "
                       "Knows everything happening on Seattle's streets.",
        "strength": 2, "dexterity": 2, "stamina": 3,
        "charisma": 4, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 2, "wits": 4,
        "alertness": 4, "empathy": 3, "streetwise": 5, "drive": 3, "survival": 3,
        "willpower": 6,
    },
    {
        "name": "Mike Donovan",
        "concept": "Fetish craftsman and metalworker",
        "tribe": "Get of Fenris",
        "breed": "homid",
        "relation": "Blood relative to Cuts-Through-Steel",
        "description": "Runs a metalworking shop that secretly crafts klaives and other fetishes for the Garou. "
                       "One of the few humans trusted with the sacred work. "
                       "His forge has been blessed by spirits.",
        "strength": 4, "dexterity": 3, "stamina": 4,
        "charisma": 2, "manipulation": 1, "appearance": 2,
        "perception": 3, "intelligence": 3, "wits": 2,
        "alertness": 2, "athletics": 2, "brawl": 2, "crafts": 5, "melee": 2, "occult": 3,
        "willpower": 6,
    },
    {
        "name": "Rosa Martinez",
        "concept": "Environmental lawyer fighting corporate polluters",
        "tribe": "Children of Gaia",
        "breed": "homid",
        "relation": "Sister to Heals-the-Wounded",
        "description": "Environmental lawyer who takes on cases against corporations destroying natural habitats. "
                       "Fights the Wyrm's servants in court while her pack fights them in the Umbra. "
                       "Connected to activist networks across the Pacific Northwest.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 3, "intelligence": 4, "wits": 3,
        "empathy": 3, "expression": 3, "subterfuge": 2, "etiquette": 2, "law": 5, "politics": 3,
        "willpower": 5,
    },
    {
        "name": "Tommy Whitefeather",
        "concept": "Wendigo Kinfolk and cultural preservationist",
        "tribe": "Wendigo",
        "breed": "homid",
        "relation": "Nephew to Chases-the-Wind",
        "description": "Works at a Native American cultural center, preserving tribal traditions and history. "
                       "Helps maintain the connection between the Wendigo and their mortal kin. "
                       "Suspicious of outsiders but fiercely loyal to family.",
        "strength": 2, "dexterity": 2, "stamina": 3,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 3, "wits": 3,
        "alertness": 2, "empathy": 2, "crafts": 3, "survival": 3, "academics": 2, "occult": 3,
        "willpower": 5,
    },
]

# =============================================================================
# CONTACT NPCs - Mortals who provide information
# =============================================================================

# Runs-Through-Fire's Contacts (2 dots)
FIRE_CONTACTS = [
    {
        "name": "Captain Maya Rodriguez",
        "concept": "Fire department captain with a debt to pay",
        "description": "Runs-Through-Fire saved her team during his First Change fire. "
                       "Now provides access to fire investigation reports and emergency response info.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 3, "wits": 3,
        "alertness": 3, "athletics": 2, "leadership": 3, "drive": 2, "medicine": 2, "investigation": 2,
        "willpower": 5,
    },
    {
        "name": "Eddie 'Scanner' Park",
        "concept": "Emergency radio enthusiast and first responder tracker",
        "description": "Retired EMT who monitors all emergency frequencies as a hobby. "
                       "Knows when and where things go wrong in Seattle before anyone else.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 3,
        "alertness": 4, "computer": 2, "technology": 4, "medicine": 2, "investigation": 2,
        "willpower": 4,
    },
]

# Silicon Dreams' Contacts (2 dots)
SILICON_CONTACTS = [
    {
        "name": "Vanessa Cole",
        "concept": "Tech journalist with sources at every company",
        "description": "Writes for a major tech blog. Knows about unreleased products, corporate scandals, "
                       "and the secrets that tech companies try to hide. Trades info for exclusives.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 3, "intelligence": 3, "wits": 4,
        "alertness": 2, "empathy": 3, "expression": 4, "subterfuge": 2, "computer": 3, "investigation": 3,
        "willpower": 4,
    },
    {
        "name": "Marcus Webb Jr.",
        "concept": "Social media influencer with a massive following",
        "description": "Has millions of followers and knows how to make anything go viral. "
                       "Useful for spreading information—or disinformation—quickly.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 4, "appearance": 4,
        "perception": 2, "intelligence": 2, "wits": 3,
        "empathy": 2, "expression": 4, "subterfuge": 3, "performance": 3, "computer": 3, "technology": 2,
        "willpower": 3,
    },
]

# =============================================================================
# ALLY NPCs - Mortals who actively help
# =============================================================================

# Breaks-the-Chain's Ally (1 dot)
CHAIN_ALLIES = [
    {
        "name": "Darnell Jackson",
        "concept": "Former gang member trying to go straight",
        "description": "Breaks-the-Chain helped him escape gang life. Now runs a community youth center "
                       "and provides intel on gang activities when needed. Absolutely loyal.",
        "strength": 3, "dexterity": 3, "stamina": 3,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 2, "wits": 4,
        "alertness": 3, "athletics": 2, "brawl": 3, "streetwise": 4, "leadership": 2, "melee": 2,
        "willpower": 5,
    },
]

# =============================================================================
# MENTOR NPCs - Elder Garou who teach PCs
# =============================================================================

MENTOR_GAROU = [
    {
        "name": "Silver-Tongue-Speaks",
        "concept": "Elder Uktena theurge and spiritual guide",
        "for_pc": "Whispers-to-Stars",
        "tribe": "Uktena",
        "auspice": "Theurge",
        "breed": "homid",
        "rank": 4,
        "description": "Ancient Uktena who has walked the spirit paths for over a century. "
                       "Teaches the ways of binding and negotiating with spirits. "
                       "Carries secrets that could change the balance of power in Seattle.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 4, "appearance": 2,
        "perception": 5, "intelligence": 4, "wits": 4,
        "alertness": 3, "awareness": 5, "empathy": 3, "subterfuge": 3,
        "enigmas": 5, "occult": 5, "rituals": 4,
        "gnosis": 8, "rage": 4, "willpower": 8,
    },
    {
        "name": "Sees-Beyond-Stars",
        "concept": "Stargazer elder and meditation master",
        "for_pc": "Dreamwalker",
        "tribe": "Stargazers",
        "auspice": "Theurge",
        "breed": "homid",
        "rank": 4,
        "description": "Stargazer elder who has mastered the balance between Rage and inner peace. "
                       "Teaches Dreamwalker the paths of enlightenment and the mysteries of the Umbra. "
                       "Recently returned from decades of meditation in the Himalayas.",
        "strength": 2, "dexterity": 4, "stamina": 3,
        "charisma": 4, "manipulation": 2, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 4, "awareness": 5, "empathy": 4, "expression": 3,
        "enigmas": 5, "occult": 4, "rituals": 3,
        "gnosis": 9, "rage": 3, "willpower": 9,
    },
]


def create_kinfolk_npcs(chronicle, st_user):
    """Create Kinfolk NPCs for werewolf PCs."""
    print("\n--- Creating Kinfolk NPCs ---")

    for kinfolk_data in KINFOLK_NPCS:
        tribe = Tribe.objects.filter(name=kinfolk_data["tribe"]).first()

        kinfolk, created = Kinfolk.objects.get_or_create(
            name=kinfolk_data["name"],
            owner=st_user,
            defaults={
                "concept": kinfolk_data["concept"],
                "description": kinfolk_data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "tribe": tribe,
                "breed": kinfolk_data.get("breed", "homid"),
                "relation": kinfolk_data.get("relation", ""),
            },
        )
        if created:
            apply_human_stats(kinfolk, kinfolk_data)
            print(f"  Created: {kinfolk.name} ({kinfolk_data['tribe']} Kinfolk)")
        else:
            print(f"  Already exists: {kinfolk.name}")


def create_contact_npcs(chronicle, st_user):
    """Create Contact NPCs for werewolf PCs."""
    print("\n--- Creating Contact NPCs ---")

    all_contacts = [
        ("Runs-Through-Fire", FIRE_CONTACTS),
        ("Silicon Dreams", SILICON_CONTACTS),
    ]

    for pc_name, contacts in all_contacts:
        print(f"\nContacts for {pc_name}:")
        for contact_data in contacts:
            human, created = WtAHuman.objects.get_or_create(
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
    """Create Ally NPCs for werewolf PCs."""
    print("\n--- Creating Ally NPCs ---")

    all_allies = [
        ("Breaks-the-Chain", CHAIN_ALLIES),
    ]

    for pc_name, allies in all_allies:
        print(f"\nAllies for {pc_name}:")
        for ally_data in allies:
            human, created = WtAHuman.objects.get_or_create(
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


def create_mentor_npcs(chronicle, st_user):
    """Create Mentor NPCs (elder Garou) for werewolf PCs."""
    print("\n--- Creating Mentor NPCs ---")

    for mentor_data in MENTOR_GAROU:
        tribe = Tribe.objects.filter(name=mentor_data["tribe"]).first()

        garou, created = Garou.objects.get_or_create(
            name=mentor_data["name"],
            owner=st_user,
            defaults={
                "concept": mentor_data["concept"],
                "description": mentor_data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "tribe": tribe,
                "breed": mentor_data.get("breed", "homid"),
                "auspice": mentor_data.get("auspice", ""),
                "rank": mentor_data.get("rank", 1),
            },
        )
        if created:
            # Apply attributes and abilities
            for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                         "appearance", "perception", "intelligence", "wits"]:
                if attr in mentor_data:
                    setattr(garou, attr, mentor_data[attr])

            for ability in ["alertness", "athletics", "awareness", "brawl", "empathy",
                            "expression", "intimidation", "leadership", "primal_urge",
                            "streetwise", "subterfuge", "animal_ken", "crafts", "drive",
                            "etiquette", "firearms", "melee", "performance", "larceny",
                            "stealth", "survival", "academics", "computer", "enigmas",
                            "investigation", "law", "linguistics", "medicine", "occult",
                            "politics", "rituals", "science", "technology"]:
                if ability in mentor_data:
                    setattr(garou, ability, mentor_data[ability])

            if "gnosis" in mentor_data:
                garou.gnosis = mentor_data["gnosis"]
            if "rage" in mentor_data:
                garou.rage = mentor_data["rage"]
            if "willpower" in mentor_data:
                garou.willpower = mentor_data["willpower"]

            garou.save()
            print(f"  Created mentor: {garou.name} (for {mentor_data['for_pc']})")
        else:
            print(f"  Already exists: {garou.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Werewolf PC Auxiliary NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_kinfolk_npcs(chronicle, st_user)
    create_contact_npcs(chronicle, st_user)
    create_ally_npcs(chronicle, st_user)
    create_mentor_npcs(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Werewolf auxiliary NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
