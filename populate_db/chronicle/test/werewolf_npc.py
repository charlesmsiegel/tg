"""
Seattle Test Chronicle - Werewolf Major NPCs

Creates major Garou NPCs who hold positions of power:
Sept Alpha, Sept Elders, Warder, Master of the Rite, and tribal leaders.

Run with: python manage.py shell < populate_db/chronicle/test/werewolf_npc.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Werewolf data must be loaded (tribes, auspices, gifts)
"""

from django.contrib.auth.models import User

from characters.models.werewolf.garou import Garou
from characters.models.werewolf.tribe import Tribe
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_garou_stats(garou, data):
    """Apply stats to a Garou NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(garou, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "empathy", "expression",
                    "intimidation", "leadership", "primal_urge", "streetwise", "subterfuge",
                    "animal_ken", "crafts", "drive", "etiquette", "firearms", "melee",
                    "performance", "larceny", "stealth", "survival",
                    "academics", "computer", "enigmas", "investigation", "law",
                    "linguistics", "medicine", "occult", "politics", "rituals", "science", "technology"]:
        if ability in data:
            setattr(garou, ability, data[ability])

    if "gnosis" in data:
        garou.gnosis = data["gnosis"]
    if "rage" in data:
        garou.rage = data["rage"]
    if "willpower" in data:
        garou.willpower = data["willpower"]
    if "rank" in data:
        garou.rank = data["rank"]

    garou.save()


# =============================================================================
# SEPT OF THE EMERALD SHADOW - PRIMARY SEPT
# =============================================================================

SEPT_LEADERSHIP = [
    {
        "name": "Howls-at-Thunder",
        "concept": "Silver Fang Alpha of the Sept of the Emerald Shadow",
        "tribe": "Silver Fangs",
        "auspice": "Ahroun",
        "breed": "homid",
        "rank": 5,
        "description": "Howls-at-Thunder has led the Sept of the Emerald Shadow for fifteen years, a record in "
                       "these tumultuous times. His pure breeding is undeniable, and his tactical brilliance "
                       "has seen the sept through Wyrm incursions and Pentex attacks alike. He maintains the "
                       "Caern at Cougar Mountain, a powerful place of Falcon's blessing. His relationship "
                       "with the tech-focused Glass Walkers is strained, but he recognizes their value.",
        "strength": 4, "dexterity": 4, "stamina": 5,
        "charisma": 5, "manipulation": 3, "appearance": 4,
        "perception": 4, "intelligence": 3, "wits": 4,
        "alertness": 4, "athletics": 4, "brawl": 5, "empathy": 2, "expression": 3, "intimidation": 5,
        "leadership": 5, "primal_urge": 4,
        "melee": 5, "etiquette": 4, "survival": 4,
        "enigmas": 3, "occult": 3, "politics": 4, "rituals": 4,
        "gnosis": 7, "rage": 7, "willpower": 9,
    },
    {
        "name": "Weaves-the-Web",
        "concept": "Glass Walker elder who bridges tradition and technology",
        "tribe": "Glass Walkers",
        "auspice": "Philodox",
        "breed": "homid",
        "rank": 5,
        "description": "Weaves-the-Web is the elder Glass Walker representative and Sept Councilor. She's spent "
                       "decades proving that technology and Gaia aren't enemies, and her pack's victories "
                       "against Pentex's digital operations have silenced most critics. Her den is a converted "
                       "warehouse in SODO, filled with servers that touch the CyberRealm.",
        "strength": 3, "dexterity": 4, "stamina": 3,
        "charisma": 4, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 3, "empathy": 4, "expression": 3, "leadership": 4, "primal_urge": 3,
        "subterfuge": 4,
        "computer": 5, "etiquette": 3, "technology": 5,
        "enigmas": 4, "investigation": 4, "law": 3, "politics": 4, "rituals": 3, "science": 4,
        "gnosis": 8, "rage": 4, "willpower": 8,
    },
    {
        "name": "Storm's-Fury",
        "concept": "Get of Fenris Warder who guards the Caern",
        "tribe": "Get of Fenris",
        "auspice": "Ahroun",
        "breed": "homid",
        "rank": 4,
        "description": "Storm's-Fury guards the Caern at Cougar Mountain with ferocious dedication. No Wyrm "
                       "creature has breached the bawn since she took the position, and three Black Spiral "
                       "packs have died trying. Her legendary berserker rages are both feared and respected. "
                       "She demands excellence from the younger Ahroun and accepts no excuses.",
        "strength": 5, "dexterity": 4, "stamina": 5,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 5,
        "alertness": 5, "athletics": 5, "brawl": 5, "intimidation": 5, "primal_urge": 5,
        "melee": 5, "stealth": 3, "survival": 4,
        "enigmas": 2, "occult": 2, "rituals": 3,
        "gnosis": 5, "rage": 9, "willpower": 8,
    },
    {
        "name": "Speaks-with-Ancestors",
        "concept": "Uktena Master of the Rite",
        "tribe": "Uktena",
        "auspice": "Theurge",
        "breed": "lupus",
        "rank": 5,
        "description": "Speaks-with-Ancestors is the sept's Master of the Rite, responsible for all sacred "
                       "ceremonies. She walked the spirit paths when Seattle was still forest, and she knows "
                       "secrets that make even the Alpha uncomfortable. Her rites bind powerful spirits to "
                       "the sept's service, and her prophecies, when she shares them, always prove accurate.",
        "strength": 2, "dexterity": 4, "stamina": 3,
        "charisma": 3, "manipulation": 3, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 4, "awareness": 5, "empathy": 4, "expression": 3, "primal_urge": 5, "subterfuge": 3,
        "stealth": 4, "survival": 5,
        "enigmas": 5, "linguistics": 3, "medicine": 3, "occult": 5, "rituals": 5,
        "gnosis": 9, "rage": 4, "willpower": 9,
    },
    {
        "name": "Keeper-of-Ways",
        "concept": "Wendigo Gatekeeper who controls Umbral access",
        "tribe": "Wendigo",
        "auspice": "Theurge",
        "breed": "homid",
        "rank": 4,
        "description": "Keeper-of-Ways guards the Caern's moon bridges and Umbral pathways. His knowledge of "
                       "the Near Umbra around Seattle is unmatched, and he can sense when the Gauntlet "
                       "thins dangerously. He maintains old alliances with the Nunnehi, though tension "
                       "between the tribes' claims on the land runs deep.",
        "strength": 3, "dexterity": 3, "stamina": 4,
        "charisma": 3, "manipulation": 3, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 4,
        "alertness": 4, "awareness": 5, "empathy": 3, "primal_urge": 4, "streetwise": 2,
        "survival": 5, "stealth": 4,
        "enigmas": 5, "occult": 5, "rituals": 4,
        "gnosis": 8, "rage": 5, "willpower": 7,
    },
]

# =============================================================================
# TRIBAL ELDERS
# =============================================================================

TRIBAL_ELDERS = [
    {
        "name": "Iron-in-Soul",
        "concept": "Get of Fenris elder advocating total war on Pentex",
        "tribe": "Get of Fenris",
        "auspice": "Philodox",
        "breed": "homid",
        "rank": 5,
        "description": "Iron-in-Soul leads the Get of Fenris presence in Seattle and pushes for direct "
                       "action against Pentex's local operations. He believes the Silicon Pact was a mistake "
                       "that allowed the Wyrm to entrench in the tech industry. His pack operates out of "
                       "Mike Donovan's metalworking shop, crafting weapons for the war.",
        "strength": 5, "dexterity": 3, "stamina": 5,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 4, "athletics": 4, "brawl": 5, "intimidation": 4, "leadership": 4, "primal_urge": 4,
        "crafts": 4, "firearms": 3, "melee": 5, "survival": 4,
        "enigmas": 2, "law": 3, "occult": 2, "politics": 3, "rituals": 3,
        "gnosis": 6, "rage": 7, "willpower": 8,
    },
    {
        "name": "Walks-the-City-Spirit",
        "concept": "Bone Gnawer elder who knows every back alley",
        "tribe": "Bone Gnawers",
        "auspice": "Ragabash",
        "breed": "homid",
        "rank": 4,
        "description": "Walks-the-City-Spirit has lived on Seattle's streets since before it was a city. She "
                       "knows every homeless camp, every squat, every place the lost and forgotten gather. "
                       "Her network of kinfolk and allies among the homeless sees everything the powerful "
                       "try to hide. The Alpha consults her before any operation in the urban jungle.",
        "strength": 2, "dexterity": 4, "stamina": 4,
        "charisma": 3, "manipulation": 4, "appearance": 2,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 5, "awareness": 4, "empathy": 4, "streetwise": 5, "subterfuge": 5, "primal_urge": 3,
        "larceny": 4, "stealth": 5, "survival": 5,
        "enigmas": 3, "investigation": 4, "occult": 3, "politics": 3, "rituals": 3,
        "gnosis": 7, "rage": 4, "willpower": 7,
    },
    {
        "name": "Sings-the-Old-Ways",
        "concept": "Children of Gaia peacekeeper between factions",
        "tribe": "Children of Gaia",
        "auspice": "Galliard",
        "breed": "homid",
        "rank": 4,
        "description": "Sings-the-Old-Ways serves as mediator between the more aggressive tribes and those "
                       "seeking peace. Her songs carry the weight of Garou history, reminding all of what "
                       "they fight for. She works with environmental activists and Rosa Martinez to fight "
                       "the Wyrm through mortal legal systems as well as claws.",
        "strength": 3, "dexterity": 3, "stamina": 3,
        "charisma": 5, "manipulation": 3, "appearance": 4,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 3, "awareness": 4, "empathy": 5, "expression": 5, "leadership": 4, "primal_urge": 3,
        "performance": 5, "etiquette": 3,
        "academics": 3, "enigmas": 4, "law": 2, "occult": 4, "politics": 4, "rituals": 4,
        "gnosis": 7, "rage": 4, "willpower": 8,
    },
    {
        "name": "Hides-the-Path",
        "concept": "Shadow Lord elder with ambitions beyond Seattle",
        "tribe": "Shadow Lords",
        "auspice": "Philodox",
        "breed": "homid",
        "rank": 5,
        "description": "Hides-the-Path commands the Shadow Lords of the Pacific Northwest, and his influence "
                       "extends from Seattle to Portland to Vancouver. He supports the Alpha publicly while "
                       "building his own power base quietly. Some whisper he's positioning himself for "
                       "leadership when Howls-at-Thunder inevitably falls in battle.",
        "strength": 3, "dexterity": 4, "stamina": 3,
        "charisma": 4, "manipulation": 5, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 3, "empathy": 3, "expression": 3, "intimidation": 4,
        "leadership": 5, "primal_urge": 4, "subterfuge": 5,
        "etiquette": 4, "stealth": 4,
        "enigmas": 4, "investigation": 4, "law": 4, "occult": 4, "politics": 5, "rituals": 4,
        "gnosis": 7, "rage": 5, "willpower": 9,
    },
]

# =============================================================================
# BLACK SPIRAL DANCER THREATS
# =============================================================================

BSD_THREATS = [
    {
        "name": "Whispers-of-Malfeas",
        "concept": "Black Spiral Dancer pack leader corrupting from within",
        "tribe": "Black Spiral Dancers",
        "auspice": "Theurge",
        "breed": "metis",
        "rank": 4,
        "description": "Whispers-of-Malfeas leads a pack of Black Spiral Dancers that has infiltrated the "
                       "areas around Seattle. Rather than direct attack, they corrupt Kinfolk, taint potential "
                       "cubs before First Change, and desecrate minor spirit sites. Their Hive is hidden "
                       "somewhere in the Cascade foothills, location unknown despite years of searching.",
        "strength": 4, "dexterity": 4, "stamina": 4,
        "charisma": 3, "manipulation": 5, "appearance": 1,
        "perception": 5, "intelligence": 4, "wits": 4,
        "alertness": 4, "awareness": 5, "empathy": 2, "intimidation": 4, "primal_urge": 5, "subterfuge": 5,
        "stealth": 5, "survival": 4,
        "enigmas": 5, "occult": 5, "rituals": 5,
        "gnosis": 8, "rage": 6, "willpower": 8,
    },
]


def create_sept_leadership(chronicle, st_user):
    """Create Sept leadership NPCs."""
    print("\n--- Creating Sept Leadership ---")

    for data in SEPT_LEADERSHIP:
        tribe = Tribe.objects.filter(name=data["tribe"]).first()

        garou, created = Garou.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "tribe": tribe,
                "auspice": data.get("auspice", ""),
                "breed": data.get("breed", "homid"),
                "rank": data.get("rank", 1),
            },
        )
        if created:
            apply_garou_stats(garou, data)
            print(f"  Created: {garou.name} ({data['tribe']})")
        else:
            print(f"  Already exists: {garou.name}")


def create_tribal_elders(chronicle, st_user):
    """Create tribal elder NPCs."""
    print("\n--- Creating Tribal Elders ---")

    for data in TRIBAL_ELDERS:
        tribe = Tribe.objects.filter(name=data["tribe"]).first()

        garou, created = Garou.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "tribe": tribe,
                "auspice": data.get("auspice", ""),
                "breed": data.get("breed", "homid"),
                "rank": data.get("rank", 1),
            },
        )
        if created:
            apply_garou_stats(garou, data)
            print(f"  Created: {garou.name} ({data['tribe']} Elder)")
        else:
            print(f"  Already exists: {garou.name}")


def create_bsd_threats(chronicle, st_user):
    """Create Black Spiral Dancer threat NPCs."""
    print("\n--- Creating Black Spiral Dancer Threats ---")

    for data in BSD_THREATS:
        tribe = Tribe.objects.filter(name=data["tribe"]).first()

        garou, created = Garou.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "tribe": tribe,
                "auspice": data.get("auspice", ""),
                "breed": data.get("breed", "homid"),
                "rank": data.get("rank", 1),
            },
        )
        if created:
            apply_garou_stats(garou, data)
            print(f"  Created: {garou.name} (BSD Threat)")
        else:
            print(f"  Already exists: {garou.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Werewolf Major NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_sept_leadership(chronicle, st_user)
    create_tribal_elders(chronicle, st_user)
    create_bsd_threats(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Werewolf major NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
