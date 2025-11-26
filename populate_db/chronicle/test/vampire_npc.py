"""
Seattle Test Chronicle - Vampire Major NPCs

Creates major Vampire NPCs who hold positions of power in the city:
Prince, Primogen Council, Sheriff, Seneschal, Harpy, and other notable Kindred.

Run with: python manage.py shell < populate_db/chronicle/test/vampire_npc.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Vampire data must be loaded (clans, sects, disciplines)
"""

from django.contrib.auth.models import User

from characters.models.vampire.vampire import Vampire
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.sect import VampireSect
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_vampire_stats(vampire, data):
    """Apply stats to a Vampire NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(vampire, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "empathy", "expression",
                    "intimidation", "leadership", "streetwise", "subterfuge",
                    "animal_ken", "crafts", "drive", "etiquette", "firearms", "melee",
                    "performance", "larceny", "stealth", "survival",
                    "academics", "computer", "finance", "investigation", "law",
                    "linguistics", "medicine", "occult", "politics", "science", "technology"]:
        if ability in data:
            setattr(vampire, ability, data[ability])

    # Disciplines
    for discipline in ["animalism", "auspex", "celerity", "chimerstry", "daimoinon",
                       "dementation", "dominate", "fortitude", "melpominee", "mytherceria",
                       "necromancy", "obfuscate", "obtenebration", "obeah", "potence",
                       "presence", "protean", "quietus", "serpentis", "spiritus",
                       "thaumaturgy", "thanatosis", "valeren", "vicissitude"]:
        if discipline in data:
            setattr(vampire, discipline, data[discipline])

    if "willpower" in data:
        vampire.willpower = data["willpower"]
    if "humanity" in data:
        vampire.humanity = data["humanity"]
    if "generation_rating" in data:
        vampire.generation_rating = data["generation_rating"]

    vampire.save()


# =============================================================================
# CAMARILLA LEADERSHIP
# =============================================================================

PRINCE = {
    "name": "Prince Alexander Mercer",
    "concept": "Calculating Ventrue Prince who rules through economics",
    "clan": "Ventrue",
    "sect": "Camarilla",
    "generation_rating": 7,
    "description": "Prince Mercer seized Seattle's throne in 1962, using the World's Fair as cover for a carefully "
                   "orchestrated purge of his rivals. He rules through financial leverage rather than open force, "
                   "preferring his enemies indebted rather than destroyed. His domain is the downtown financial "
                   "district, and he meets petitioners in a penthouse atop one of Seattle's tallest buildings. "
                   "The Silicon Pact of 1995 was his masterstroke—binding the supernatural factions to protect "
                   "the tech industry that now fills his coffers.",
    "strength": 3, "dexterity": 3, "stamina": 3,
    "charisma": 4, "manipulation": 5, "appearance": 4,
    "perception": 4, "intelligence": 5, "wits": 5,
    "alertness": 3, "awareness": 3, "empathy": 3, "intimidation": 4, "leadership": 5, "subterfuge": 5,
    "etiquette": 5, "melee": 2, "firearms": 2,
    "academics": 4, "finance": 5, "law": 4, "politics": 5,
    "dominate": 5, "fortitude": 4, "presence": 4,
    "willpower": 9, "humanity": 5,
}

SENESCHAL = {
    "name": "Victoria Ashworth",
    "concept": "Toreador Seneschal who manages court politics with grace",
    "clan": "Toreador",
    "sect": "Camarilla",
    "generation_rating": 8,
    "description": "Lady Ashworth has served as Seneschal for three decades, handling the day-to-day affairs "
                   "of Kindred society while the Prince focuses on grand strategy. Her salons are legendary, "
                   "her memory for slights is encyclopedic, and her ability to smooth over conflicts has "
                   "prevented more than one blood hunt. She maintains Elysium at the Seattle Art Museum.",
    "strength": 2, "dexterity": 4, "stamina": 2,
    "charisma": 5, "manipulation": 5, "appearance": 5,
    "perception": 4, "intelligence": 4, "wits": 5,
    "alertness": 3, "awareness": 3, "empathy": 5, "expression": 4, "leadership": 4, "subterfuge": 5,
    "etiquette": 5, "performance": 4, "stealth": 2,
    "academics": 4, "investigation": 3, "law": 3, "politics": 5,
    "auspex": 4, "celerity": 3, "presence": 5,
    "willpower": 8, "humanity": 6,
}

SHERIFF = {
    "name": "Konstantin 'Stone' Petrov",
    "concept": "Brutal Brujah Sheriff who enforces the Prince's law",
    "clan": "Brujah",
    "sect": "Camarilla",
    "generation_rating": 8,
    "description": "Stone earned his name by surviving a Sabbat siege in the 1980s, standing alone against "
                   "a pack of Tzimisce for three nights. The Prince rewarded his loyalty with the Sheriff's "
                   "position, and Stone has held it with an iron fist ever since. His reputation for "
                   "violence keeps most problems from requiring his attention—most. He personally handles "
                   "any threat to the Masquerade.",
    "strength": 5, "dexterity": 4, "stamina": 5,
    "charisma": 2, "manipulation": 2, "appearance": 2,
    "perception": 4, "intelligence": 3, "wits": 4,
    "alertness": 4, "athletics": 4, "brawl": 5, "intimidation": 5, "streetwise": 4,
    "drive": 3, "firearms": 4, "melee": 5, "stealth": 3, "survival": 3,
    "investigation": 3, "law": 2,
    "celerity": 4, "potence": 5, "presence": 3,
    "willpower": 8, "humanity": 4,
}

HARPY = {
    "name": "Anastasia 'The Whisper' Volkov",
    "concept": "Malkavian Harpy whose madness reveals social truths",
    "clan": "Malkavian",
    "sect": "Camarilla",
    "generation_rating": 9,
    "description": "The Whisper earned her position by knowing secrets no one should know and sharing them "
                   "at the most devastating moments. Her derangement manifests as an inability to ignore "
                   "social lies—she sees through every pretense and delights in exposing hypocrisy. "
                   "Her favor can elevate a neonate to prominence; her disfavor can destroy centuries of reputation.",
    "strength": 2, "dexterity": 3, "stamina": 2,
    "charisma": 4, "manipulation": 5, "appearance": 4,
    "perception": 5, "intelligence": 4, "wits": 5,
    "alertness": 4, "awareness": 4, "empathy": 5, "expression": 4, "subterfuge": 5,
    "etiquette": 4, "performance": 3,
    "academics": 3, "investigation": 4, "politics": 5,
    "auspex": 5, "dementation": 4, "obfuscate": 3,
    "willpower": 7, "humanity": 5,
}

# =============================================================================
# PRIMOGEN COUNCIL
# =============================================================================

PRIMOGEN = [
    {
        "name": "Priscilla von Strauss",
        "concept": "Tremere Primogen and Regent of the Seattle Chantry",
        "clan": "Tremere",
        "sect": "Camarilla",
        "generation_rating": 7,
        "description": "Regent von Strauss has led the Seattle Chantry for over a century, turning it into "
                       "a center for researching the unique magical properties of the Pacific Northwest. "
                       "Her relationship with the Prince is strictly professional—they respect each other's power "
                       "without friendship. She knows more about Seattle's ley lines than any other Kindred.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 4,
        "alertness": 3, "awareness": 4, "empathy": 2, "intimidation": 3, "leadership": 4, "subterfuge": 4,
        "etiquette": 4, "melee": 2,
        "academics": 5, "investigation": 4, "occult": 5, "politics": 4, "science": 3,
        "auspex": 5, "dominate": 4, "thaumaturgy": 5,
        "willpower": 9, "humanity": 5,
    },
    {
        "name": "Marcus 'Old Man' Kincaid",
        "concept": "Nosferatu Primogen who controls Seattle's information networks",
        "clan": "Nosferatu",
        "sect": "Camarilla",
        "generation_rating": 8,
        "description": "Kincaid was old when Seattle was still a lumber town, and he knows every secret buried "
                       "in its foundations. The Nosferatu warrens beneath Pioneer Square are his domain, "
                       "and nothing moves through the city's underground without his knowledge. He trades "
                       "in information rather than favors, making him invaluable to the Prince.",
        "strength": 3, "dexterity": 3, "stamina": 4,
        "charisma": 2, "manipulation": 4, "appearance": 0,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 5, "awareness": 3, "streetwise": 5, "subterfuge": 4,
        "larceny": 3, "security": 4, "stealth": 5,
        "academics": 3, "computer": 4, "investigation": 5, "politics": 4,
        "animalism": 3, "obfuscate": 5, "potence": 3,
        "willpower": 8, "humanity": 6,
    },
    {
        "name": "Elise Fontaine",
        "concept": "Toreador Primogen and patron of Seattle's arts scene",
        "clan": "Toreador",
        "sect": "Camarilla",
        "generation_rating": 8,
        "description": "Elise came to Seattle following the grunge music explosion, believing new art was being born. "
                       "She stayed when she discovered the city's creative potential extended beyond music. "
                       "Her galleries showcase both mortal and Kindred artists, and her influence extends "
                       "throughout Seattle's cultural institutions.",
        "strength": 2, "dexterity": 4, "stamina": 2,
        "charisma": 5, "manipulation": 4, "appearance": 5,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 3, "empathy": 4, "expression": 5, "leadership": 3, "subterfuge": 3,
        "etiquette": 5, "performance": 4,
        "academics": 4, "investigation": 2, "politics": 4,
        "auspex": 4, "celerity": 3, "presence": 5,
        "willpower": 7, "humanity": 7,
    },
    {
        "name": "Aleksandr Volkov",
        "concept": "Gangrel Primogen who speaks for the wild places",
        "clan": "Gangrel",
        "sect": "Camarilla",
        "generation_rating": 8,
        "description": "Volkov represents the Gangrel who chose to remain with the Camarilla after the clan's "
                       "departure. He claims the wilderness around Seattle as his domain and serves as liaison "
                       "between the city Kindred and those who hunt in the surrounding forests. "
                       "His bestial features betray centuries of frenzy.",
        "strength": 4, "dexterity": 4, "stamina": 4,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 5, "intelligence": 3, "wits": 4,
        "alertness": 5, "athletics": 4, "awareness": 3, "brawl": 4, "intimidation": 3,
        "animal_ken": 4, "melee": 3, "stealth": 4, "survival": 5,
        "occult": 2,
        "animalism": 4, "fortitude": 4, "protean": 5,
        "willpower": 8, "humanity": 5,
    },
    {
        "name": "Jonathan Sterling",
        "concept": "Ventrue Primogen and the Prince's chief rival",
        "clan": "Ventrue",
        "sect": "Camarilla",
        "generation_rating": 8,
        "description": "Sterling believes he should be Prince and makes no secret of it. His power base in Seattle's "
                       "old money families predates Mercer's arrival, and he views the current Prince as an upstart. "
                       "He follows the laws of the Camarilla precisely, waiting for Mercer to make a mistake "
                       "he can exploit. Their rivalry keeps both sharp.",
        "strength": 3, "dexterity": 3, "stamina": 3,
        "charisma": 4, "manipulation": 5, "appearance": 3,
        "perception": 4, "intelligence": 4, "wits": 5,
        "alertness": 3, "empathy": 3, "intimidation": 4, "leadership": 4, "subterfuge": 5,
        "etiquette": 5, "firearms": 2, "melee": 2,
        "academics": 4, "finance": 5, "law": 4, "politics": 5,
        "dominate": 4, "fortitude": 3, "presence": 4,
        "willpower": 8, "humanity": 5,
    },
    {
        "name": "Father Matthias",
        "concept": "Malkavian Primogen who sees God in his madness",
        "clan": "Malkavian",
        "sect": "Camarilla",
        "generation_rating": 9,
        "description": "Father Matthias was a priest before his Embrace, and he remains one after—though his "
                       "congregation now consists of Kindred seeking guidance and mortals seeking confession "
                       "they'll never remember giving. His visions are terrifying and occasionally useful. "
                       "He maintains a church in Capitol Hill that serves as unofficial neutral ground.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 4,
        "alertness": 3, "awareness": 5, "empathy": 4, "expression": 4, "leadership": 3, "subterfuge": 2,
        "etiquette": 3,
        "academics": 4, "occult": 4, "politics": 3,
        "auspex": 5, "dementation": 4, "obfuscate": 3,
        "willpower": 8, "humanity": 7,
    },
]

# =============================================================================
# ANARCH LEADERSHIP
# =============================================================================

ANARCH_LEADERS = [
    {
        "name": "Red Jack",
        "concept": "Brujah Anarch leader who remembers the labor wars",
        "clan": "Brujah",
        "sect": "Anarch",
        "generation_rating": 9,
        "description": "Red Jack was a union organizer during the Everett Massacre of 1916, Embraced by a "
                       "Brujah who saw fire in him. He's led Seattle's Anarchs for decades, maintaining "
                       "an uneasy peace with the Camarilla while pushing for expanded rights. "
                       "His territory is the industrial waterfront and south Seattle.",
        "strength": 4, "dexterity": 3, "stamina": 4,
        "charisma": 4, "manipulation": 3, "appearance": 2,
        "perception": 3, "intelligence": 3, "wits": 4,
        "alertness": 3, "athletics": 3, "brawl": 4, "empathy": 2, "expression": 4, "intimidation": 3,
        "leadership": 4, "streetwise": 4,
        "drive": 3, "firearms": 3, "melee": 4,
        "academics": 2, "law": 2, "politics": 4,
        "celerity": 3, "potence": 4, "presence": 3,
        "willpower": 7, "humanity": 6,
    },
    {
        "name": "The Baroness",
        "concept": "Lasombra Anarch who carved her own domain from the night",
        "clan": "Lasombra",
        "sect": "Anarch",
        "generation_rating": 9,
        "description": "The Baroness defected from the Sabbat in the 1990s during a failed siege of Seattle. "
                       "Instead of joining the Camarilla, she claimed a domain among the Anarchs and has held "
                       "it ever since. Her mastery of shadow makes her dangerous, and her Sabbat survival skills "
                       "make her invaluable. She controls the U-District and its nightlife.",
        "strength": 3, "dexterity": 4, "stamina": 3,
        "charisma": 3, "manipulation": 4, "appearance": 4,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 4, "awareness": 3, "brawl": 3, "intimidation": 4, "leadership": 3, "subterfuge": 4,
        "etiquette": 2, "melee": 4, "stealth": 5,
        "occult": 3, "politics": 3,
        "dominate": 3, "obtenebration": 5, "potence": 3,
        "willpower": 8, "humanity": 4,
    },
]

# =============================================================================
# NOTABLE ELDERS AND THREATS
# =============================================================================

OTHER_NOTABLE = [
    {
        "name": "The Keeper",
        "concept": "Ancient Nosferatu who guards secrets beneath the city",
        "clan": "Nosferatu",
        "sect": "Camarilla",
        "generation_rating": 6,
        "description": "No one knows the Keeper's true name or age. They dwell in the deepest warrens beneath "
                       "Seattle, guarding relics and prisoners too dangerous to destroy. Even the Prince "
                       "must petition for an audience. The Keeper's whispers shape Kindred history—when they "
                       "choose to speak at all.",
        "strength": 4, "dexterity": 3, "stamina": 5,
        "charisma": 2, "manipulation": 5, "appearance": 0,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 5, "awareness": 5, "brawl": 3, "intimidation": 5, "streetwise": 4, "subterfuge": 5,
        "larceny": 4, "security": 5, "stealth": 5,
        "academics": 5, "investigation": 5, "occult": 5, "politics": 4,
        "animalism": 4, "obfuscate": 5, "potence": 4,
        "willpower": 10, "humanity": 4,
    },
    {
        "name": "Bishop Lucien Moreau",
        "concept": "Sabbat Bishop leading raids from the Canadian border",
        "clan": "Lasombra",
        "sect": "Sabbat",
        "generation_rating": 8,
        "description": "Bishop Moreau leads the Sabbat presence in the Pacific Northwest from a base in "
                       "Vancouver. His raids into Seattle are probing attacks, testing defenses and "
                       "recruiting disaffected Kindred. The Prince has placed a blood hunt on him, "
                       "but Moreau has evaded every attempt to destroy him.",
        "strength": 4, "dexterity": 4, "stamina": 4,
        "charisma": 4, "manipulation": 4, "appearance": 3,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 4, "athletics": 3, "brawl": 4, "empathy": 2, "intimidation": 5, "leadership": 5,
        "streetwise": 3, "subterfuge": 4,
        "firearms": 3, "melee": 4, "stealth": 3,
        "occult": 4, "politics": 4,
        "dominate": 4, "obtenebration": 5, "potence": 4,
        "willpower": 9, "humanity": 3,
    },
]


def create_leadership_npcs(chronicle, st_user):
    """Create Camarilla leadership NPCs."""
    print("\n--- Creating Camarilla Leadership ---")

    # Create Prince
    leadership = [("Prince", PRINCE), ("Seneschal", SENESCHAL), ("Sheriff", SHERIFF), ("Harpy", HARPY)]

    for title, data in leadership:
        clan = VampireClan.objects.filter(name=data["clan"]).first()
        sect = VampireSect.objects.filter(name=data["sect"]).first()

        vampire, created = Vampire.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "clan": clan,
                "sect": sect,
            },
        )
        if created:
            apply_vampire_stats(vampire, data)
            print(f"  Created {title}: {vampire.name}")
        else:
            print(f"  Already exists: {vampire.name}")


def create_primogen_npcs(chronicle, st_user):
    """Create Primogen Council NPCs."""
    print("\n--- Creating Primogen Council ---")

    for data in PRIMOGEN:
        clan = VampireClan.objects.filter(name=data["clan"]).first()
        sect = VampireSect.objects.filter(name=data["sect"]).first()

        vampire, created = Vampire.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "clan": clan,
                "sect": sect,
            },
        )
        if created:
            apply_vampire_stats(vampire, data)
            print(f"  Created Primogen: {vampire.name} ({data['clan']})")
        else:
            print(f"  Already exists: {vampire.name}")


def create_anarch_npcs(chronicle, st_user):
    """Create Anarch leadership NPCs."""
    print("\n--- Creating Anarch Leadership ---")

    for data in ANARCH_LEADERS:
        clan = VampireClan.objects.filter(name=data["clan"]).first()
        sect = VampireSect.objects.filter(name=data["sect"]).first()

        vampire, created = Vampire.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "clan": clan,
                "sect": sect,
            },
        )
        if created:
            apply_vampire_stats(vampire, data)
            print(f"  Created Anarch: {vampire.name}")
        else:
            print(f"  Already exists: {vampire.name}")


def create_notable_npcs(chronicle, st_user):
    """Create other notable vampire NPCs."""
    print("\n--- Creating Notable NPCs ---")

    for data in OTHER_NOTABLE:
        clan = VampireClan.objects.filter(name=data["clan"]).first()
        sect = VampireSect.objects.filter(name=data["sect"]).first()

        vampire, created = Vampire.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "clan": clan,
                "sect": sect,
            },
        )
        if created:
            apply_vampire_stats(vampire, data)
            print(f"  Created: {vampire.name}")
        else:
            print(f"  Already exists: {vampire.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Vampire Major NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_leadership_npcs(chronicle, st_user)
    create_primogen_npcs(chronicle, st_user)
    create_anarch_npcs(chronicle, st_user)
    create_notable_npcs(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Vampire major NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
