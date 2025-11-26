"""
Seattle Test Chronicle - Changeling Characters

Creates Changeling, Inanimae, Nunnehi, and AutumnPerson characters for the test chronicle.
Assigns characters to appropriate motleys based on DESIGN.md groupings.

Run with: python manage.py shell < populate_db/chronicle/test/changeling_characters.py
"""

from django.contrib.auth.models import User

from characters.models.changeling import (
    AutumnPerson,
    Changeling,
    Inanimae,
    Kith,
    Motley,
    Nunnehi,
)
from game.models import Chronicle


# Character definitions
# Kiths: Boggan, Nocker, Pooka, Satyr, Sidhe (Arcadian/Autumn), Sluagh, Troll, etc.
# Seemings: childling, wilder, grump
# Courts: seelie, unseelie

CHANGELINGS = [
    {
        "username": "xXShadowWolfXx",
        "name": "Pixel",
        "kith": "Nocker",
        "seeming": "wilder",
        "court": "unseelie",
        "motley": "The Toybox Rebellion",
        "is_leader": False,
        "concept": "Video game creator obsessed with capturing Glamour in code",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "alertness": 2,
        "crafts": 4,
        "computer": 3,
        "technology": 3,
        "science": 2,
        "expression": 2,
        "subterfuge": 1,
        "stealth": 2,
        "kenning": 2,
        # Backgrounds (5 points)
        "resources": 2,
        "chimera": 2,
        "dreamers": 1,
        # Arts (3 points): Nockers favor crafting-related arts
        "primal": 2,
        "legerdemain": 1,
        # Realms (5 points)
        "prop": 3,
        "scene": 2,
        # Glamour/Banality
        "glamour": 4,
        "banality": 4,
    },
    {
        "username": "CrypticMoon",
        "name": "Lord Ashford",
        "kith": "Autumn Sidhe",
        "seeming": "grump",
        "court": "seelie",
        "motley": "The Court of Whispers",
        "is_leader": True,
        "concept": "Ancient noble who remembers the Shattering",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 4,
        "appearance": 3,
        "perception": 3,
        "intelligence": 3,
        "wits": 3,
        # Abilities: 13/9/5
        "alertness": 2,
        "etiquette": 4,
        "subterfuge": 3,
        "leadership": 2,
        "expression": 2,
        "academics": 3,
        "occult": 2,
        "politics": 3,
        "kenning": 2,
        # Backgrounds (5 points)
        "title": 3,
        "remembrance": 2,
        # Arts (3 points): Sidhe favor sovereign
        "sovereign": 2,
        "soothsay": 1,
        # Realms (5 points)
        "actor": 3,
        "fae": 2,
        # Glamour/Banality
        "glamour": 4,
        "banality": 5,
    },
    {
        "username": "NightOwl_42",
        "name": "Brambleheart",
        "kith": "Sluagh",
        "seeming": "grump",
        "court": "unseelie",
        "motley": "The Court of Whispers",
        "is_leader": False,
        "concept": "Morgue worker who collects secrets from the dead",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 1,
        "manipulation": 3,
        "appearance": 1,
        "perception": 5,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "alertness": 3,
        "stealth": 4,
        "investigation": 3,
        "medicine": 2,
        "kenning": 3,
        "subterfuge": 3,
        "streetwise": 2,
        "occult": 3,
        # Backgrounds (5 points)
        "contacts": 2,
        "chimera": 2,
        "remembrance": 1,
        # Arts (3 points): Sluagh favor soothsay
        "soothsay": 2,
        "naming": 1,
        # Realms (5 points)
        "actor": 2,
        "fae": 2,
        "nature_realm": 1,
        # Glamour/Banality
        "glamour": 4,
        "banality": 5,
    },
    {
        "username": "pixel_witch",
        "name": "Widget",
        "kith": "Boggan",
        "seeming": "wilder",
        "court": "seelie",
        "motley": "The Toybox Rebellion",
        "is_leader": False,
        "concept": "Cozy cafe owner nurturing dreamers",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 3,
        "charisma": 4,
        "manipulation": 2,
        "appearance": 3,
        "perception": 3,
        "intelligence": 2,
        "wits": 2,
        # Abilities: 13/9/5
        "empathy": 3,
        "expression": 2,
        "crafts": 4,
        "etiquette": 2,
        "streetwise": 2,
        "alertness": 2,
        "academics": 1,
        "kenning": 2,
        "subterfuge": 1,
        "leadership": 1,
        # Backgrounds (5 points)
        "holdings": 2,
        "dreamers": 2,
        "resources": 1,
        # Arts (3 points): Boggans favor helpful arts
        "primal": 2,
        "wayfare": 1,
        # Realms (5 points)
        "actor": 3,
        "prop": 2,
        # Glamour/Banality
        "glamour": 5,
        "banality": 3,
    },
    {
        "username": "ByteSlayer",
        "name": "Forge",
        "kith": "Nocker",
        "seeming": "grump",
        "court": "unseelie",
        "motley": "The Toybox Rebellion",
        "is_leader": True,
        "concept": "Master craftsman building impossible devices",
        # Attributes: 7/5/3
        "strength": 3,
        "dexterity": 4,
        "stamina": 3,
        "charisma": 1,
        "manipulation": 2,
        "appearance": 1,
        "perception": 3,
        "intelligence": 5,
        "wits": 3,
        # Abilities: 13/9/5
        "crafts": 5,
        "technology": 4,
        "science": 3,
        "alertness": 2,
        "computer": 2,
        "repair": 3,
        "kenning": 2,
        "stealth": 1,
        # Backgrounds (5 points)
        "chimera": 3,
        "treasure": 2,
        # Arts (3 points)
        "primal": 3,
        # Realms (5 points)
        "prop": 4,
        "fae": 1,
        # Glamour/Banality
        "glamour": 4,
        "banality": 5,
    },
    {
        "username": "gh0st_in_shell",
        "name": "Hollow",
        "kith": "Sluagh",
        "seeming": "wilder",
        "court": "unseelie",
        "motley": "The Court of Whispers",
        "is_leader": False,
        "concept": "Urban explorer who speaks only in whispers",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 4,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 3,
        "wits": 4,
        # Abilities: 13/9/5
        "stealth": 4,
        "alertness": 3,
        "streetwise": 3,
        "investigation": 2,
        "survival": 2,
        "larceny": 2,
        "kenning": 3,
        "subterfuge": 2,
        # Backgrounds (5 points)
        "contacts": 3,
        "chimera": 1,
        "remembrance": 1,
        # Arts (3 points)
        "wayfare": 2,
        "soothsay": 1,
        # Realms (5 points)
        "scene": 3,
        "actor": 2,
        # Glamour/Banality
        "glamour": 5,
        "banality": 3,
    },
    {
        "username": "Zephyr_Storm",
        "name": "Tempest",
        "kith": "Autumn Sidhe",
        "seeming": "wilder",
        "court": "seelie",
        "motley": "The Storm's Eye",
        "is_leader": True,
        "concept": "Passionate idealist of House Liam protecting dreamers",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 5,
        "manipulation": 3,
        "appearance": 4,
        "perception": 2,
        "intelligence": 2,
        "wits": 3,
        # Abilities: 13/9/5
        "leadership": 3,
        "expression": 3,
        "empathy": 3,
        "etiquette": 2,
        "alertness": 2,
        "melee": 2,
        "kenning": 3,
        "politics": 2,
        "athletics": 1,
        # Backgrounds (5 points)
        "title": 2,
        "retinue": 2,
        "dreamers": 1,
        # Arts (3 points)
        "sovereign": 2,
        "wayfare": 1,
        # Realms (5 points)
        "actor": 3,
        "fae": 2,
        # Glamour/Banality
        "glamour": 5,
        "banality": 3,
    },
    {
        "username": "n00b_hunter",
        "name": "Sprocket",
        "kith": "Nocker",
        "seeming": "childling",
        "court": "seelie",
        "motley": "The Toybox Rebellion",
        "is_leader": False,
        "concept": "Young apprentice struggling with homework and the Dreaming",
        # Attributes: 7/5/3
        "strength": 1,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 2,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5 (fewer due to age)
        "crafts": 3,
        "technology": 2,
        "computer": 2,
        "alertness": 2,
        "athletics": 1,
        "academics": 2,
        "kenning": 2,
        "expression": 1,
        # Backgrounds (5 points)
        "mentor": 3,  # Forge
        "chimera": 1,
        "dreamers": 1,
        # Arts (3 points)
        "primal": 2,
        "legerdemain": 1,
        # Realms (5 points)
        "prop": 2,
        "fae": 2,
        "actor": 1,
        # Glamour/Banality - childlings get +1 glamour
        "glamour": 5,
        "banality": 2,
    },
    {
        "username": "ElectricDreamer",
        "name": "Neon",
        "kith": "Pooka",
        "seeming": "wilder",
        "court": "seelie",
        "motley": "The Storm's Eye",
        "is_leader": False,
        "concept": "Electric eel Pooka and club promoter",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 4,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 3,
        "appearance": 3,
        "perception": 3,
        "intelligence": 2,
        "wits": 3,
        # Abilities: 13/9/5
        "subterfuge": 3,
        "expression": 3,
        "streetwise": 3,
        "performance": 3,
        "empathy": 2,
        "alertness": 2,
        "etiquette": 2,
        "kenning": 2,
        # Backgrounds (5 points)
        "contacts": 3,
        "dreamers": 2,
        # Arts (3 points)
        "chicanery": 2,
        "wayfare": 1,
        # Realms (5 points)
        "actor": 3,
        "scene": 2,
        # Glamour/Banality
        "glamour": 5,
        "banality": 3,
    },
    {
        "username": "void_whisper",
        "name": "Umbra",
        "kith": "Sluagh",
        "seeming": "grump",
        "court": "unseelie",
        "motley": "The Court of Whispers",
        "is_leader": False,
        "concept": "Elder keeper of secrets who remembers the Shattering",
        # Attributes: 7/5/3
        "strength": 1,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 1,
        "manipulation": 4,
        "appearance": 1,
        "perception": 5,
        "intelligence": 5,
        "wits": 4,
        # Abilities: 13/9/5
        "stealth": 3,
        "alertness": 3,
        "kenning": 4,
        "occult": 4,
        "investigation": 2,
        "subterfuge": 3,
        "intimidation": 2,
        "enigmas": 2,
        # Backgrounds (5 points)
        "remembrance": 4,
        "contacts": 1,
        # Arts (3 points)
        "soothsay": 3,
        # Realms (5 points)
        "actor": 2,
        "fae": 2,
        "time": 1,
        # Glamour/Banality
        "glamour": 4,
        "banality": 6,
    },
]


# Inanimae characters (elemental fae)
# Kingdoms: kubera (earth), ondine (water), paroseme (wood), sylph (air), salamander (fire), solimond (crystal), mannikin (artificial)
# Seemings: glimmer (young), naturae (mature), ancient (old)
# Seasons: spring, summer, autumn, winter

INANIMAE = [
    {
        "username": "xXShadowWolfXx",
        "name": "Granite",
        "kingdom": "kubera",
        "inanimae_seeming": "glimmer",
        "season": "autumn",
        "concept": "Stone spirit awakened from demolished building",
        "anchor_description": "A chunk of granite in a sculptor's studio",
        # Attributes: 7/5/3
        "strength": 4,
        "dexterity": 2,
        "stamina": 4,
        "charisma": 1,
        "manipulation": 1,
        "appearance": 2,
        "perception": 3,
        "intelligence": 3,
        "wits": 2,
        # Abilities: 13/9/5
        "alertness": 2,
        "crafts": 3,
        "survival": 2,
        "athletics": 1,
        "brawl": 2,
        "academics": 1,
        "science": 1,
        "kenning": 2,
        # Backgrounds (5 points)
        "chimera": 2,
        "holdings": 2,
        "remembrance": 1,
        # Mana (replaces glamour)
        "mana": 4,
    },
    {
        "username": "pixel_witch",
        "name": "Codex",
        "kingdom": "mannikin",
        "inanimae_seeming": "glimmer",
        "season": "winter",
        "concept": "Spirit awakened in a vintage computer",
        "anchor_description": "A vintage Apple IIe computer in a collector's home",
        # Attributes: 7/5/3
        "strength": 1,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 1,
        "perception": 4,
        "intelligence": 5,
        "wits": 4,
        # Abilities: 13/9/5
        "computer": 4,
        "technology": 3,
        "science": 2,
        "alertness": 2,
        "investigation": 2,
        "enigmas": 2,
        "kenning": 2,
        # Backgrounds (5 points)
        "chimera": 3,
        "remembrance": 2,
        # Mana
        "mana": 4,
    },
    {
        "username": "Zephyr_Storm",
        "name": "Zephyr",
        "kingdom": "sylph",
        "inanimae_seeming": "naturae",
        "season": "spring",
        "concept": "Air spirit bound to an old weathervane",
        "anchor_description": "An antique weathervane atop a historic Seattle hotel",
        # Attributes: 7/5/3
        "strength": 1,
        "dexterity": 4,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 3,
        "perception": 4,
        "intelligence": 2,
        "wits": 4,
        # Abilities: 13/9/5
        "alertness": 3,
        "athletics": 3,
        "stealth": 2,
        "survival": 2,
        "expression": 2,
        "kenning": 3,
        "science": 1,  # Weather patterns
        "enigmas": 1,
        # Backgrounds (5 points)
        "holdings": 3,
        "chimera": 2,
        # Mana
        "mana": 5,
    },
    {
        "username": "ElectricDreamer",
        "name": "Circuit",
        "kingdom": "solimond",
        "inanimae_seeming": "glimmer",
        "season": "summer",
        "concept": "Fire/energy spirit bound to a neon sign",
        "anchor_description": "A neon sign outside a jazz club",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 2,
        "appearance": 4,
        "perception": 3,
        "intelligence": 2,
        "wits": 3,
        # Abilities: 13/9/5
        "expression": 3,
        "performance": 2,
        "alertness": 2,
        "empathy": 2,
        "kenning": 3,
        "technology": 2,
        "streetwise": 2,
        "crafts": 1,
        # Backgrounds (5 points)
        "holdings": 2,
        "chimera": 2,
        "dreamers": 1,
        # Mana
        "mana": 5,
    },
]


# Nunnehi characters (Native American fae)
# Tribes: may_may_gway_shi, yunwi_tsundi, canotina, kachina, nanehi, nunnehi_proper, other
# Seemings: katchina (young), kohedan (balanced), kurganegh (elder)
# Paths: warrior, healer, sage, trickster

NUNNEHI = [
    {
        "username": "CrypticMoon",
        "name": "Rain Walker",
        "tribe": "nunnehi_proper",
        "nunnehi_seeming": "kohedan",
        "path": "sage",
        "concept": "Spirit of the Coast Salish awakened by activist dreams",
        "sacred_place": "A hidden grove in the Cascade foothills",
        "spirit_guide": "Salmon",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 3,
        "perception": 4,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "empathy": 3,
        "expression": 2,
        "alertness": 3,
        "occult": 3,
        "survival": 2,
        "kenning": 3,
        "politics": 2,
        "enigmas": 2,
        # Backgrounds (5 points)
        "remembrance": 3,
        "contacts": 2,
        # Medicine (replaces glamour)
        "medicine": 5,
    },
    {
        "username": "ByteSlayer",
        "name": "Thunder Bear",
        "tribe": "nunnehi_proper",
        "nunnehi_seeming": "kohedan",
        "path": "warrior",
        "concept": "Warrior spirit channeling collective fury to protect sacred sites",
        "sacred_place": "An ancient burial ground threatened by development",
        "spirit_guide": "Bear",
        # Attributes: 7/5/3
        "strength": 4,
        "dexterity": 3,
        "stamina": 4,
        "charisma": 2,
        "manipulation": 1,
        "appearance": 2,
        "perception": 3,
        "intelligence": 2,
        "wits": 3,
        # Abilities: 13/9/5
        "brawl": 4,
        "athletics": 3,
        "intimidation": 3,
        "alertness": 2,
        "survival": 3,
        "melee": 2,
        "kenning": 2,
        # Backgrounds (5 points)
        "holdings": 3,
        "allies": 2,
        # Medicine
        "medicine": 4,
    },
    {
        "username": "void_whisper",
        "name": "Raven's Shadow",
        "tribe": "nunnehi_proper",
        "nunnehi_seeming": "kurganegh",
        "path": "trickster",
        "concept": "Trickster spirit using chaos to maintain balance",
        "sacred_place": "A deserted island in Puget Sound",
        "spirit_guide": "Raven",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 4,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 4,
        "appearance": 2,
        "perception": 4,
        "intelligence": 3,
        "wits": 4,
        # Abilities: 13/9/5
        "subterfuge": 4,
        "stealth": 3,
        "alertness": 3,
        "streetwise": 2,
        "occult": 2,
        "kenning": 3,
        "larceny": 2,
        "enigmas": 2,
        # Backgrounds (5 points)
        "remembrance": 3,
        "chimera": 2,
        # Medicine
        "medicine": 5,
    },
]


# Autumn People (anti-fae mortals)
# Archetypes: authority, bureaucrat, cynic, fundamentalist, corporate, scientist, debunker, other
# Awareness: unaware, suspicious, aware, hunter

AUTUMN_PEOPLE = [
    {
        "username": "NightOwl_42",
        "name": "Margaret Wells",
        "archetype": "authority",
        "banality_rating": 8,
        "awareness": "unaware",
        "concept": "Retired schoolteacher unknowingly hosting a fae soul",
        "motivation": "Maintain order and structure in a chaotic world",
        "is_dauntain": False,
        # Attributes: 7/5/3
        "strength": 1,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 2,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "leadership": 3,
        "empathy": 2,
        "expression": 3,
        "academics": 4,
        "alertness": 2,
        "etiquette": 2,
        "subterfuge": 2,
        "politics": 1,
    },
    {
        "username": "gh0st_in_shell",
        "name": "David Kowalski",
        "archetype": "cynic",
        "banality_rating": 7,
        "awareness": "suspicious",
        "concept": "Aging programmer hosting a fading fae soul",
        "motivation": "Recapture the innovative spark of youth",
        "is_dauntain": False,
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 3,
        "intelligence": 5,
        "wits": 4,
        # Abilities: 13/9/5
        "computer": 4,
        "technology": 3,
        "science": 2,
        "academics": 2,
        "alertness": 2,
        "investigation": 2,
        "crafts": 2,
    },
    {
        "username": "n00b_hunter",
        "name": "Jenny Walsh",
        "archetype": "other",
        "banality_rating": 6,
        "awareness": "unaware",
        "concept": "Teenager hosting a Changeling soul struggling to emerge",
        "motivation": "Understand the inexplicable moments of wonder and terror",
        "is_dauntain": False,
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 3,
        "perception": 4,
        "intelligence": 3,
        "wits": 3,
        # Abilities: 13/9/5
        "alertness": 3,
        "expression": 2,
        "empathy": 3,
        "athletics": 2,
        "academics": 2,
        "computer": 2,
        "streetwise": 1,
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


def create_changelings(chronicle, st_user):
    """Create Changeling characters and assign to motleys."""
    print("\n--- Creating Changeling Characters ---")

    # Cache kiths and motleys
    kiths = {k.name: k for k in Kith.objects.all()}
    motleys = {m.name: m for m in Motley.objects.filter(chronicle=chronicle)}

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
        "kenning",
        "leadership",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "enigmas",
        "gremayre",
        "law",
        "politics",
        "technology",
        "occult",
        "repair",
    ]
    backgrounds = [
        "contacts",
        "mentor",
        "chimera",
        "dreamers",
        "holdings",
        "remembrance",
        "resources",
        "retinue",
        "title",
        "treasure",
        "allies",
    ]
    arts = [
        "autumn",
        "spring",
        "summer",
        "winter",
        "chicanery",
        "chronos",
        "contract",
        "dragons_ire",
        "legerdemain",
        "metamorphosis",
        "naming",
        "oneiromancy",
        "primal",
        "pyretics",
        "skycraft",
        "soothsay",
        "sovereign",
        "wayfare",
    ]
    realms = ["actor", "fae", "nature_realm", "prop", "scene", "time"]

    for data in CHANGELINGS:
        # Get or create user
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            print(f"  WARNING: User {data['username']} not found, skipping {data['name']}")
            continue

        # Get kith
        kith = kiths.get(data["kith"])
        if not kith:
            print(f"  WARNING: Kith {data['kith']} not found, skipping {data['name']}")
            continue

        # Create or get changeling
        changeling, created = Changeling.objects.get_or_create(
            name=data["name"],
            owner=user,
            defaults={
                "chronicle": chronicle,
                "kith": kith,
                "seeming": data["seeming"],
                "court": data["court"],
                "concept": data.get("concept", ""),
                "npc": False,
            },
        )

        if created:
            # Apply stats
            apply_stats(changeling, data, attributes)
            apply_stats(changeling, data, abilities)
            apply_stats(changeling, data, backgrounds)
            apply_stats(changeling, data, arts)
            apply_stats(changeling, data, realms)

            # Set glamour/banality
            if "glamour" in data:
                changeling.glamour = data["glamour"]
            if "banality" in data:
                changeling.banality = data["banality"]

            changeling.willpower = 4  # Default for changelings
            if data["seeming"] == "grump":
                changeling.willpower = 5  # Grumps get +1
            if data["seeming"] == "childling":
                changeling.glamour = max(changeling.glamour, 5)  # Childlings get +1

            changeling.save()
            print(f"  Created changeling: {data['name']} ({data['kith']} {data['seeming']})")
        else:
            print(f"  Changeling already exists: {data['name']}")

        # Assign to motley
        motley_name = data.get("motley")
        if motley_name and motley_name in motleys:
            motley = motleys[motley_name]
            if changeling not in motley.members.all():
                motley.members.add(changeling)
                print(f"    Added to motley: {motley_name}")

            if data.get("is_leader"):
                motley.leader = changeling
                motley.save()
                print(f"    Set as motley leader")


def create_inanimae(chronicle, st_user):
    """Create Inanimae characters."""
    print("\n--- Creating Inanimae Characters ---")

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
        "kenning",
        "crafts",
        "drive",
        "stealth",
        "survival",
        "computer",
        "investigation",
        "science",
        "enigmas",
        "technology",
        "performance",
        "repair",
    ]
    backgrounds = ["chimera", "holdings", "remembrance", "dreamers", "contacts", "allies"]

    for data in INANIMAE:
        # Get or create user
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            print(f"  WARNING: User {data['username']} not found, skipping {data['name']}")
            continue

        # Create or get inanimae
        inanimae, created = Inanimae.objects.get_or_create(
            name=data["name"],
            owner=user,
            defaults={
                "chronicle": chronicle,
                "kingdom": data["kingdom"],
                "inanimae_seeming": data["inanimae_seeming"],
                "season": data["season"],
                "concept": data.get("concept", ""),
                "anchor_description": data.get("anchor_description", ""),
                "npc": False,
            },
        )

        if created:
            # Apply stats
            apply_stats(inanimae, data, attributes)
            apply_stats(inanimae, data, abilities)
            apply_stats(inanimae, data, backgrounds)

            # Set mana (replaces glamour for Inanimae)
            if "mana" in data:
                inanimae.mana = data["mana"]

            inanimae.willpower = 4
            inanimae.save()
            print(f"  Created inanimae: {data['name']} ({data['kingdom']})")
        else:
            print(f"  Inanimae already exists: {data['name']}")


def create_nunnehi(chronicle, st_user):
    """Create Nunnehi characters."""
    print("\n--- Creating Nunnehi Characters ---")

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
        "kenning",
        "crafts",
        "melee",
        "stealth",
        "survival",
        "occult",
        "enigmas",
        "politics",
        "larceny",
    ]
    backgrounds = ["remembrance", "contacts", "holdings", "allies", "chimera"]

    for data in NUNNEHI:
        # Get or create user
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            print(f"  WARNING: User {data['username']} not found, skipping {data['name']}")
            continue

        # Create or get nunnehi
        nunnehi, created = Nunnehi.objects.get_or_create(
            name=data["name"],
            owner=user,
            defaults={
                "chronicle": chronicle,
                "tribe": data["tribe"],
                "nunnehi_seeming": data["nunnehi_seeming"],
                "path": data["path"],
                "concept": data.get("concept", ""),
                "sacred_place": data.get("sacred_place", ""),
                "spirit_guide": data.get("spirit_guide", ""),
                "npc": False,
            },
        )

        if created:
            # Apply stats
            apply_stats(nunnehi, data, attributes)
            apply_stats(nunnehi, data, abilities)
            apply_stats(nunnehi, data, backgrounds)

            # Set medicine (replaces glamour for Nunnehi)
            if "medicine" in data:
                nunnehi.medicine = data["medicine"]

            nunnehi.willpower = 4
            nunnehi.save()
            print(f"  Created nunnehi: {data['name']} ({data['path']})")
        else:
            print(f"  Nunnehi already exists: {data['name']}")


def create_autumn_people(chronicle, st_user):
    """Create AutumnPerson characters."""
    print("\n--- Creating Autumn People Characters ---")

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
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "leadership",
        "crafts",
        "etiquette",
        "stealth",
        "academics",
        "computer",
        "investigation",
        "science",
        "technology",
        "politics",
    ]

    for data in AUTUMN_PEOPLE:
        # Get or create user
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            print(f"  WARNING: User {data['username']} not found, skipping {data['name']}")
            continue

        # Create or get autumn person
        autumn_person, created = AutumnPerson.objects.get_or_create(
            name=data["name"],
            owner=user,
            defaults={
                "chronicle": chronicle,
                "archetype": data["archetype"],
                "banality_rating": data["banality_rating"],
                "awareness": data["awareness"],
                "concept": data.get("concept", ""),
                "motivation": data.get("motivation", ""),
                "is_dauntain": data.get("is_dauntain", False),
                "npc": False,
            },
        )

        if created:
            # Apply stats
            apply_stats(autumn_person, data, attributes)
            apply_stats(autumn_person, data, abilities)

            autumn_person.willpower = 3
            autumn_person.save()
            print(f"  Created autumn person: {data['name']} ({data['archetype']})")
        else:
            print(f"  Autumn person already exists: {data['name']}")


def main():
    """Run the full Changeling character setup."""
    print("=" * 60)
    print("Seattle Test Chronicle - Changeling Character Setup")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()
    if not chronicle or not st_user:
        return

    create_changelings(chronicle, st_user)
    create_inanimae(chronicle, st_user)
    create_nunnehi(chronicle, st_user)
    create_autumn_people(chronicle, st_user)

    # Summary
    print("\n" + "=" * 60)
    print("Changeling character setup complete!")
    print(f"Changelings: {Changeling.objects.filter(chronicle=chronicle).count()}")
    print(f"Inanimae: {Inanimae.objects.filter(chronicle=chronicle).count()}")
    print(f"Nunnehi: {Nunnehi.objects.filter(chronicle=chronicle).count()}")
    print(f"Autumn People: {AutumnPerson.objects.filter(chronicle=chronicle).count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    # When run via `python manage.py shell < script.py`
    main()
