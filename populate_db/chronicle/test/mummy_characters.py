"""
Seattle Test Chronicle - Mummy Characters

Creates Mummy (Amenti) characters for the test chronicle.
Assigns characters to appropriate cults (using generic Group model) based on DESIGN.md.

Run with: python manage.py shell < populate_db/chronicle/test/mummy_characters.py
"""

from django.contrib.auth.models import User

from characters.models.core import Group
from characters.models.mummy import Dynasty, Mummy
from game.models import Chronicle


# Character definitions
# Webs: isis (Preservers), osiris (Judges), horus (Protectors), maat (Seers), thoth (Scholars)
# Hekau - Universal: alchemy, celestial, effigy, necromancy, nomenclature
# Hekau - Web: ushabti (isis), judge (osiris), phoenix (horus), vision (maat), divination (thoth)

MUMMIES = [
    {
        "username": "xXShadowWolfXx",
        "name": "Ankh-ef-en-Khonsu",
        "ancient_name": "Ankh-ef-en-Khonsu",
        "web": "maat",
        "dynasty": "Twelfth Dynasty",
        "cult": "The Keepers of Ma'at",
        "is_leader": True,
        "concept": "Ancient priest of Khonsu reborn as museum curator",
        "incarnation": 5,
        "years_since_rebirth": 15,
        "death_in_first_life": "Died peacefully after decades of service to Khonsu",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 3,
        "perception": 4,
        "intelligence": 5,
        "wits": 3,
        # Abilities: 13/9/5
        "academics": 4,
        "occult": 4,
        "investigation": 2,
        "alertness": 2,
        "expression": 2,
        "leadership": 2,
        "etiquette": 2,
        "subterfuge": 2,
        # Backgrounds (5 points)
        "resources": 2,
        "contacts": 2,
        "remembrance": 1,
        # Mummy stats
        "balance": 7,
        "sekhem": 3,
        # Hekau (3 dots starting)
        "vision": 2,
        "celestial": 1,
        # Virtues
        "conviction": 3,
        "restraint": 3,
    },
    {
        "username": "CrypticMoon",
        "name": "Kherpheres",
        "ancient_name": "Kherpheres",
        "web": "thoth",
        "dynasty": "Ptolemaic Dynasty",
        "cult": "The House of Scrolls",
        "is_leader": True,
        "concept": "Scholar-priest of Thoth reborn as university librarian",
        "incarnation": 4,
        "years_since_rebirth": 20,
        "death_in_first_life": "Died defending sacred texts from destruction",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 3,
        "appearance": 2,
        "perception": 4,
        "intelligence": 5,
        "wits": 4,
        # Abilities: 13/9/5
        "academics": 5,
        "investigation": 3,
        "occult": 3,
        "computer": 2,
        "alertness": 2,
        "expression": 2,
        "enigmas": 2,
        # Backgrounds (5 points)
        "resources": 2,
        "contacts": 2,
        "remembrance": 1,
        # Mummy stats
        "balance": 7,
        "sekhem": 3,
        # Hekau
        "divination": 2,
        "nomenclature": 1,
        # Virtues
        "conviction": 4,
        "restraint": 2,
    },
    {
        "username": "NightOwl_42",
        "name": "Senenmut",
        "ancient_name": "Senenmut",
        "web": "maat",
        "dynasty": "Eighteenth Dynasty",
        "cult": "The Keepers of Ma'at",
        "is_leader": False,
        "concept": "Architect of Hatshepsut's temple reborn as structural engineer",
        "incarnation": 3,
        "years_since_rebirth": 10,
        "death_in_first_life": "Died mysteriously after Hatshepsut's death",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 5,
        "wits": 4,
        # Abilities: 13/9/5
        "crafts": 4,
        "science": 3,
        "academics": 3,
        "technology": 2,
        "computer": 2,
        "alertness": 2,
        "investigation": 2,
        # Backgrounds (5 points)
        "resources": 3,
        "contacts": 2,
        # Mummy stats
        "balance": 6,
        "sekhem": 2,
        # Hekau
        "vision": 1,
        "effigy": 1,
        # Virtues
        "conviction": 3,
        "restraint": 3,
    },
    {
        "username": "pixel_witch",
        "name": "Meritaten",
        "ancient_name": "Meritaten",
        "web": "isis",
        "dynasty": "Eighteenth Dynasty",
        "cult": "The Awakening",
        "is_leader": False,
        "concept": "Princess and priestess slowly awakening to past lives",
        "incarnation": 2,
        "years_since_rebirth": 3,
        "death_in_first_life": "Died young during political upheaval",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 2,
        "appearance": 4,
        "perception": 3,
        "intelligence": 3,
        "wits": 3,
        # Abilities: 13/9/5
        "alertness": 3,
        "empathy": 2,
        "expression": 2,
        "academics": 2,
        "investigation": 2,
        "etiquette": 2,
        "stealth": 2,
        "athletics": 1,
        "occult": 1,
        # Backgrounds (5 points)
        "resources": 1,
        "contacts": 2,
        "remembrance": 2,
        # Mummy stats (lower - newly awakened)
        "balance": 6,
        "sekhem": 1,
        # Hekau
        "ushabti": 1,
        # Virtues
        "conviction": 2,
        "restraint": 3,
    },
    {
        "username": "ByteSlayer",
        "name": "Ramesses-ankh",
        "ancient_name": "Ramesses-ankh",
        "web": "horus",
        "dynasty": "Nineteenth Dynasty",
        "cult": "The Lions of Sekhmet",
        "is_leader": True,
        "concept": "Ancient warrior reborn as MMA fighter",
        "incarnation": 4,
        "years_since_rebirth": 8,
        "death_in_first_life": "Died in battle against Sea Peoples",
        # Attributes: 7/5/3
        "strength": 4,
        "dexterity": 4,
        "stamina": 4,
        "charisma": 2,
        "manipulation": 1,
        "appearance": 2,
        "perception": 3,
        "intelligence": 2,
        "wits": 3,
        # Abilities: 13/9/5
        "brawl": 4,
        "melee": 3,
        "athletics": 3,
        "alertness": 3,
        "intimidation": 2,
        "dodge": 2,
        "survival": 1,
        # Backgrounds (5 points)
        "resources": 2,
        "fame": 2,
        "allies": 1,
        # Mummy stats
        "balance": 5,
        "sekhem": 2,
        # Hekau
        "phoenix": 2,
        # Virtues
        "conviction": 3,
        "restraint": 2,
    },
    {
        "username": "gh0st_in_shell",
        "name": "Nefertari",
        "ancient_name": "Nefertari",
        "web": "osiris",
        "dynasty": "Eleventh Dynasty",
        "cult": "The House of Scrolls",
        "is_leader": False,
        "concept": "Scribe of Osiris reborn as forensic accountant",
        "incarnation": 5,
        "years_since_rebirth": 12,
        "death_in_first_life": "Died peacefully after long service to temple",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 3,
        "appearance": 2,
        "perception": 4,
        "intelligence": 5,
        "wits": 4,
        # Abilities: 13/9/5
        "investigation": 4,
        "academics": 3,
        "computer": 3,
        "finance": 3,
        "alertness": 2,
        "subterfuge": 2,
        "law": 2,
        # Backgrounds (5 points)
        "resources": 2,
        "contacts": 2,
        "remembrance": 1,
        # Mummy stats
        "balance": 7,
        "sekhem": 3,
        # Hekau
        "judge": 2,
        "necromancy": 1,
        # Virtues
        "conviction": 4,
        "restraint": 2,
    },
    {
        "username": "Zephyr_Storm",
        "name": "Imhotep-ka",
        "ancient_name": "Imhotep-ka",
        "web": "maat",
        "dynasty": "Fourth Dynasty",
        "cult": "The Keepers of Ma'at",
        "is_leader": False,
        "concept": "Architect and healer reborn as city planner",
        "incarnation": 6,
        "years_since_rebirth": 25,
        "death_in_first_life": "Died honored as a sage and healer",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 2,
        "perception": 4,
        "intelligence": 5,
        "wits": 3,
        # Abilities: 13/9/5
        "academics": 4,
        "medicine": 3,
        "crafts": 3,
        "science": 2,
        "occult": 2,
        "alertness": 2,
        "leadership": 2,
        "politics": 1,
        # Backgrounds (5 points)
        "resources": 2,
        "influence": 2,
        "contacts": 1,
        # Mummy stats
        "balance": 8,
        "sekhem": 3,
        # Hekau
        "vision": 2,
        "alchemy": 1,
        # Virtues
        "conviction": 3,
        "restraint": 4,
    },
    {
        "username": "n00b_hunter",
        "name": "Ahkenaten-ba",
        "ancient_name": "Ahkenaten-ba",
        "web": "thoth",
        "dynasty": "Modern Awakened",
        "cult": "The Awakening",
        "is_leader": False,
        "concept": "Scribe just beginning to remember past lives",
        "incarnation": 1,
        "years_since_rebirth": 1,
        "death_in_first_life": "Unclear - memories still fragmented",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 3,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "expression": 2,
        "academics": 2,
        "computer": 2,
        "alertness": 2,
        "empathy": 2,
        "streetwise": 2,
        "performance": 1,
        "crafts": 1,
        # Backgrounds (5 points) - fewer as new mummy
        "resources": 1,
        "contacts": 2,
        "allies": 2,
        # Mummy stats (lowest - barely awakened)
        "balance": 5,
        "sekhem": 1,
        # Hekau (just awakening)
        "divination": 1,
        # Virtues
        "conviction": 2,
        "restraint": 2,
    },
    {
        "username": "ElectricDreamer",
        "name": "Djehutymes",
        "ancient_name": "Djehutymes",
        "web": "thoth",
        "dynasty": "Twelfth Dynasty",
        "cult": "The House of Scrolls",
        "is_leader": False,
        "concept": "Dream-interpreter of Pharaoh reborn as sleep therapist",
        "incarnation": 4,
        "years_since_rebirth": 18,
        "death_in_first_life": "Died in old age, honored for prophetic dreams",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 3,
        "appearance": 3,
        "perception": 5,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "medicine": 3,
        "empathy": 3,
        "occult": 3,
        "expression": 2,
        "academics": 2,
        "alertness": 3,
        "investigation": 2,
        # Backgrounds (5 points)
        "resources": 2,
        "contacts": 2,
        "remembrance": 1,
        # Mummy stats
        "balance": 7,
        "sekhem": 3,
        # Hekau
        "divination": 2,
        "celestial": 1,
        # Virtues
        "conviction": 3,
        "restraint": 3,
    },
    {
        "username": "void_whisper",
        "name": "Sekhmet-hotep",
        "ancient_name": "Sekhmet-hotep",
        "web": "horus",
        "dynasty": "Nineteenth Dynasty",
        "cult": "The Lions of Sekhmet",
        "is_leader": False,
        "concept": "Warrior-priestess of Sekhmet trying to break cycles of violence",
        "incarnation": 5,
        "years_since_rebirth": 7,
        "death_in_first_life": "Died in ritual sacrifice to Sekhmet",
        # Attributes: 7/5/3
        "strength": 3,
        "dexterity": 3,
        "stamina": 3,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 3,
        "wits": 3,
        # Abilities: 13/9/5
        "medicine": 4,
        "brawl": 2,
        "melee": 2,
        "empathy": 3,
        "alertness": 3,
        "occult": 2,
        "intimidation": 2,
        # Backgrounds (5 points)
        "resources": 2,
        "allies": 2,
        "contacts": 1,
        # Mummy stats
        "balance": 6,
        "sekhem": 2,
        # Hekau
        "phoenix": 1,
        "necromancy": 1,
        # Virtues
        "conviction": 2,
        "restraint": 3,
    },
]


def get_chronicle_and_st():
    """Get the Seattle Test Chronicle and its ST user."""
    chronicle = Chronicle.objects.filter(name="Seattle Test Chronicle").first()
    if not chronicle:
        print("ERROR: Seattle Test Chronicle not found. Run base.py first.")
        return None, None

    st_user = User.objects.filter(username="DarkMaster99").first()
    if not st_user:
        print("ERROR: ST user DarkMaster99 not found. Run base.py first.")
        return None, None

    return chronicle, st_user


def apply_stats(character, data, stat_list):
    """Apply stats from data dict to character."""
    for stat in stat_list:
        if stat in data:
            setattr(character, stat, data[stat])


def create_mummies(chronicle, st_user):
    """Create Mummy characters and assign to cults (Groups)."""
    print("\n--- Creating Mummy Characters ---")

    # Cache dynasties and cults (Groups)
    dynasties = {d.name: d for d in Dynasty.objects.all()}
    # Mummy cults use generic Group model as per groups.py
    cults = {
        g.name: g
        for g in Group.objects.filter(chronicle=chronicle)
        if "House" in g.name or "Keepers" in g.name or "Lions" in g.name or "Awakening" in g.name
    }

    attributes = [
        "strength",
        "dexterity",
        "stamina",
        "charisma",
        "manipulation",
        "appearance",
        "perception",
        "intelligence",
        "wits",
    ]
    abilities = [
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "awareness",
        "leadership",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "performance",
        "stealth",
        "survival",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "occult",
        "politics",
        "science",
        "technology",
        "enigmas",
        "law",
        "finance",
        "dodge",
    ]
    backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "resources",
        "retainers",
        "cult",
        "tomb",
        "rank",
        "remembrance",
        "vessel",
        "artifact",
        "influence",
        "fame",
    ]
    hekau = [
        "alchemy",
        "celestial",
        "effigy",
        "necromancy",
        "nomenclature",
        "ushabti",
        "judge",
        "phoenix",
        "vision",
        "divination",
    ]

    for data in MUMMIES:
        # Get or create user
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            print(f"  WARNING: User {data['username']} not found, skipping {data['name']}")
            continue

        # Get dynasty
        dynasty = dynasties.get(data["dynasty"])

        # Create or get mummy
        mummy, created = Mummy.objects.get_or_create(
            name=data["name"],
            owner=user,
            defaults={
                "chronicle": chronicle,
                "web": data["web"],
                "dynasty": dynasty,
                "ancient_name": data.get("ancient_name", ""),
                "incarnation": data.get("incarnation", 1),
                "years_since_rebirth": data.get("years_since_rebirth", 0),
                "death_in_first_life": data.get("death_in_first_life", ""),
                "concept": data.get("concept", ""),
                "npc": False,
            },
        )

        if created:
            # Apply stats
            apply_stats(mummy, data, attributes)
            apply_stats(mummy, data, abilities)
            apply_stats(mummy, data, backgrounds)
            apply_stats(mummy, data, hekau)

            # Set mummy-specific stats
            mummy.balance = data.get("balance", 5)
            mummy.sekhem = data.get("sekhem", 1)
            mummy.ba = mummy.sekhem * 10  # Ba pool = Sekhem * 10
            mummy.ka_rating = mummy.sekhem * 10

            # Set virtues
            mummy.conviction = data.get("conviction", 1)
            mummy.restraint = data.get("restraint", 1)

            mummy.willpower = 3
            mummy.save()
            print(f"  Created mummy: {data['name']} ({data['web']}, {data['dynasty']})")
        else:
            print(f"  Mummy already exists: {data['name']}")

        # Assign to cult (Group)
        cult_name = data.get("cult")
        if cult_name and cult_name in cults:
            cult = cults[cult_name]
            if mummy not in cult.members.all():
                cult.members.add(mummy)
                print(f"    Added to cult: {cult_name}")

            if data.get("is_leader"):
                cult.leader = mummy
                cult.save()
                print(f"    Set as cult leader")


def main():
    """Run the full Mummy character setup."""
    print("=" * 60)
    print("Seattle Test Chronicle - Mummy Character Setup")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()
    if not chronicle or not st_user:
        return

    create_mummies(chronicle, st_user)

    # Summary
    print("\n" + "=" * 60)
    print("Mummy character setup complete!")
    print(f"Mummies: {Mummy.objects.filter(chronicle=chronicle).count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    # When run via `python manage.py shell < script.py`
    main()
