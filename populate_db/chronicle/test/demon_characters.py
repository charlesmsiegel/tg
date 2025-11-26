"""
Seattle Test Chronicle - Demon Characters

Creates Demon, Thrall, and Earthbound characters for the test chronicle.
Assigns characters to appropriate conclaves based on DESIGN.md groupings.

Run with: python manage.py shell < populate_db/chronicle/test/demon_characters.py
"""

from django.contrib.auth.models import User

from characters.models.demon import (
    Conclave,
    Demon,
    DemonFaction,
    DemonHouse,
    Earthbound,
    Thrall,
)
from game.models import Chronicle


# Character definitions
# Houses: Devils (Namaru), Scourges (Asharu), Malefactors (Annunaki),
#         Fiends (Neberu), Defilers (Lammasu), Devourers (Rabisu), Slayers (Halaku)
# Factions: Luciferans, Faustians, Reconcilers, Cryptics, Raveners

# Virtues must total 6 (conviction + courage + conscience)
# Lores must total 3 at creation

DEMONS = [
    {
        "username": "xXShadowWolfXx",
        "name": "Magistrix",
        "celestial_name": "Anashaleth",
        "host_name": "Elena Kovacs",
        "house": "Malefactors",
        "faction": "Faustians",
        "conclave": "The Architects",
        "is_leader": True,
        "concept": "City planner fallen for pride in architectural works",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 4,
        "appearance": 2,
        "perception": 4,
        "intelligence": 5,
        "wits": 3,
        # Abilities: 13/9/5
        "alertness": 2,
        "crafts": 4,
        "technology": 3,
        "academics": 3,
        "science": 2,
        "subterfuge": 3,
        "leadership": 2,
        "streetwise": 2,
        "politics": 2,
        # Backgrounds (5 points)
        "resources": 2,
        "influence": 2,
        "contacts": 1,
        # Lores (3 dots at creation) - Malefactors favor Forge/Fundament/Earth
        "lore_of_the_forge": 2,
        "lore_of_the_fundament": 1,
        # Virtues (must total 6)
        "conviction": 3,
        "courage": 2,
        "conscience": 1,
        # Faith and Torment
        "faith": 3,
        "torment": 3,
    },
    {
        "username": "CrypticMoon",
        "name": "Verath the Whisper",
        "celestial_name": "Verathiel",
        "host_name": "Mira Chen",
        "house": "Defilers",
        "faction": "Reconcilers",
        "conclave": "The Muses",
        "is_leader": True,
        "concept": "Defiler who fell for love of humanity's potential",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 5,
        "manipulation": 4,
        "appearance": 4,
        "perception": 3,
        "intelligence": 3,
        "wits": 2,
        # Abilities: 13/9/5
        "expression": 4,
        "empathy": 3,
        "subterfuge": 3,
        "performance": 3,
        "alertness": 2,
        "etiquette": 2,
        "academics": 2,
        "occult": 1,
        # Backgrounds (5 points)
        "contacts": 2,
        "resources": 2,
        "followers": 1,
        # Lores (3 dots) - Defilers favor Longing/Storms/Transfiguration
        "lore_of_longing": 2,
        "lore_of_transfiguration": 1,
        # Virtues (must total 6)
        "conviction": 1,
        "courage": 2,
        "conscience": 3,
        # Faith and Torment
        "faith": 4,
        "torment": 3,
    },
    {
        "username": "NightOwl_42",
        "name": "Arakiel",
        "celestial_name": "Arakiel",
        "host_name": "Dr. Nathan Cross",
        "house": "Fiends",
        "faction": "Cryptics",
        "conclave": "The Architects",
        "is_leader": False,
        "concept": "Fiend who fell for curiosity about creation's mechanisms",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 3,
        "appearance": 2,
        "perception": 5,
        "intelligence": 5,
        "wits": 4,
        # Abilities: 13/9/5
        "academics": 4,
        "science": 4,
        "computer": 2,
        "investigation": 2,
        "alertness": 2,
        "occult": 2,
        "enigmas": 2,
        "subterfuge": 1,
        # Backgrounds (5 points)
        "resources": 2,
        "mentor": 2,
        "contacts": 1,
        # Lores (3 dots) - Fiends favor Patterns/Light/Portals
        "lore_of_patterns": 2,
        "lore_of_light": 1,
        # Virtues (must total 6)
        "conviction": 3,
        "courage": 1,
        "conscience": 2,
        # Faith and Torment
        "faith": 3,
        "torment": 3,
    },
    {
        "username": "pixel_witch",
        "name": "Rahab",
        "celestial_name": "Rahabiel",
        "host_name": "Amanda Chen",
        "house": "Defilers",
        "faction": "Reconcilers",
        "conclave": "The Muses",
        "is_leader": False,
        "concept": "Defiler who fell for love of human creativity",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 3,
        "appearance": 3,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "computer": 4,
        "technology": 3,
        "crafts": 3,
        "expression": 2,
        "alertness": 2,
        "academics": 2,
        "occult": 1,
        "subterfuge": 2,
        # Backgrounds (5 points)
        "resources": 2,
        "contacts": 2,
        "followers": 1,
        # Lores (3 dots)
        "lore_of_longing": 2,
        "lore_of_humanity": 1,
        # Virtues (must total 6)
        "conviction": 2,
        "courage": 2,
        "conscience": 2,
        # Faith and Torment
        "faith": 3,
        "torment": 3,
    },
    {
        "username": "ByteSlayer",
        "name": "Ashmedai",
        "celestial_name": "Ashmedai",
        "host_name": "Marcus Chen",
        "house": "Malefactors",
        "faction": "Faustians",
        "conclave": "The Architects",
        "is_leader": False,
        "concept": "Malefactor who fell for pride in craft",
        # Attributes: 7/5/3
        "strength": 3,
        "dexterity": 3,
        "stamina": 3,
        "charisma": 2,
        "manipulation": 3,
        "appearance": 2,
        "perception": 3,
        "intelligence": 5,
        "wits": 3,
        # Abilities: 13/9/5
        "computer": 5,
        "technology": 4,
        "science": 3,
        "crafts": 3,
        "alertness": 2,
        "investigation": 1,
        "subterfuge": 2,
        # Backgrounds (5 points)
        "resources": 3,
        "contacts": 2,
        # Lores (3 dots)
        "lore_of_the_forge": 2,
        "lore_of_patterns": 1,
        # Virtues (must total 6)
        "conviction": 2,
        "courage": 2,
        "conscience": 2,
        # Faith and Torment
        "faith": 3,
        "torment": 3,
    },
    {
        "username": "gh0st_in_shell",
        "name": "Murmur",
        "celestial_name": "Murmuriel",
        "host_name": "David Lynch",
        "house": "Fiends",
        "faction": "Cryptics",
        "conclave": "The Reckoning",
        "is_leader": False,
        "concept": "Fiend who fell for love of secrets",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 4,
        "appearance": 2,
        "perception": 5,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "investigation": 4,
        "subterfuge": 3,
        "stealth": 3,
        "alertness": 3,
        "streetwise": 2,
        "occult": 2,
        "academics": 1,
        "computer": 2,
        # Backgrounds (5 points)
        "contacts": 3,
        "resources": 1,
        "allies": 1,
        # Lores (3 dots)
        "lore_of_patterns": 2,
        "lore_of_light": 1,
        # Virtues (must total 6)
        "conviction": 3,
        "courage": 2,
        "conscience": 1,
        # Faith and Torment
        "faith": 3,
        "torment": 4,
    },
    {
        "username": "Zephyr_Storm",
        "name": "Penemue",
        "celestial_name": "Penemuel",
        "host_name": "Jack Harrison",
        "house": "Fiends",
        "faction": "Cryptics",
        "conclave": "The Architects",
        "is_leader": False,
        "concept": "Fiend who fell for revealing forbidden knowledge",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 4,
        "appearance": 3,
        "perception": 4,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "expression": 4,
        "investigation": 3,
        "academics": 3,
        "subterfuge": 3,
        "alertness": 2,
        "streetwise": 2,
        "computer": 2,
        "politics": 1,
        # Backgrounds (5 points)
        "contacts": 3,
        "resources": 1,
        "allies": 1,
        # Lores (3 dots)
        "lore_of_patterns": 2,
        "lore_of_humanity": 1,
        # Virtues (must total 6)
        "conviction": 2,
        "courage": 2,
        "conscience": 2,
        # Faith and Torment
        "faith": 3,
        "torment": 3,
    },
    {
        "username": "n00b_hunter",
        "name": "Allocer",
        "celestial_name": "Alloceriel",
        "host_name": "Brittany Summers",
        "house": "Defilers",
        "faction": "Reconcilers",
        "conclave": "The Muses",
        "is_leader": False,
        "concept": "Recently fallen Defiler seeking validation",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 3,
        "appearance": 4,
        "perception": 2,
        "intelligence": 3,
        "wits": 3,
        # Abilities: 13/9/5
        "expression": 3,
        "subterfuge": 3,
        "empathy": 2,
        "performance": 3,
        "computer": 2,
        "alertness": 2,
        "streetwise": 2,
        "etiquette": 1,
        # Backgrounds (5 points)
        "fame": 2,
        "resources": 2,
        "contacts": 1,
        # Lores (3 dots)
        "lore_of_longing": 2,
        "lore_of_humanity": 1,
        # Virtues (must total 6)
        "conviction": 1,
        "courage": 2,
        "conscience": 3,
        # Faith and Torment
        "faith": 3,
        "torment": 3,
    },
    {
        "username": "ElectricDreamer",
        "name": "Sariel",
        "celestial_name": "Sarielah",
        "host_name": "Dr. Elena Markova",
        "house": "Fiends",
        "faction": "Reconcilers",
        "conclave": "The Muses",
        "is_leader": False,
        "concept": "Fiend who fell for love of dreams",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 3,
        "perception": 5,
        "intelligence": 4,
        "wits": 4,
        # Abilities: 13/9/5
        "empathy": 3,
        "medicine": 3,
        "occult": 3,
        "investigation": 2,
        "academics": 2,
        "alertness": 3,
        "expression": 2,
        "enigmas": 2,
        # Backgrounds (5 points)
        "resources": 2,
        "contacts": 2,
        "mentor": 1,
        # Lores (3 dots)
        "lore_of_patterns": 2,
        "lore_of_humanity": 1,
        # Virtues (must total 6)
        "conviction": 2,
        "courage": 1,
        "conscience": 3,
        # Faith and Torment
        "faith": 4,
        "torment": 3,
    },
    {
        "username": "void_whisper",
        "name": "Abaddon",
        "celestial_name": "Abaddoniel",
        "host_name": "Frank Morgan",
        "house": "Slayers",
        "faction": "Luciferans",
        "conclave": "The Reckoning",
        "is_leader": True,
        "concept": "Slayer who fell for righteous anger at injustice",
        # Attributes: 7/5/3
        "strength": 4,
        "dexterity": 3,
        "stamina": 3,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 3,
        "wits": 4,
        # Abilities: 13/9/5
        "brawl": 4,
        "melee": 3,
        "intimidation": 3,
        "alertness": 3,
        "investigation": 2,
        "streetwise": 2,
        "occult": 2,
        "stealth": 2,
        # Backgrounds (5 points)
        "contacts": 2,
        "resources": 2,
        "allies": 1,
        # Lores (3 dots) - Slayers favor Death/Spirit/Realms
        "lore_of_death": 2,
        "lore_of_the_spirit": 1,
        # Virtues (must total 6)
        "conviction": 3,
        "courage": 2,
        "conscience": 1,
        # Faith and Torment
        "faith": 3,
        "torment": 4,  # Slayers start at 4
    },
]


# Thrall characters (mortal servants bound to demons)
# Virtues must total 6
THRALLS = [
    {
        "username": "xXShadowWolfXx",
        "name": "Kevin Rhodes",
        "master": "Magistrix",
        "faith_potential": 2,
        "concept": "Construction foreman with supernatural ability to get permits",
        # Attributes: 7/5/3
        "strength": 3,
        "dexterity": 2,
        "stamina": 3,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 2,
        "perception": 2,
        "intelligence": 3,
        "wits": 3,
        # Abilities: 13/9/5
        "leadership": 3,
        "crafts": 3,
        "drive": 2,
        "streetwise": 2,
        "alertness": 2,
        "brawl": 2,
        "subterfuge": 2,
        "technology": 1,
        # Virtues (must total 6)
        "conviction": 2,
        "courage": 2,
        "conscience": 2,
        # Enhancements
        "enhancements": ["Enhanced Persuasion", "Luck"],
    },
    {
        "username": "NightOwl_42",
        "name": "Dr. Patricia Huang",
        "master": "Arakiel",
        "faith_potential": 3,
        "concept": "Graduate student with breakthrough insights",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 5,
        "wits": 4,
        # Abilities: 13/9/5
        "academics": 4,
        "science": 4,
        "computer": 3,
        "investigation": 2,
        "alertness": 2,
        "expression": 1,
        "occult": 1,
        # Virtues (must total 6)
        "conviction": 3,
        "courage": 1,
        "conscience": 2,
        # Enhancements
        "enhancements": ["Enhanced Intellect", "Inspiration"],
    },
    {
        "username": "pixel_witch",
        "name": "Marcus Webb",
        "master": "Rahab",
        "faith_potential": 2,
        "concept": "QA tester with supernatural bug-finding instincts",
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
        "computer": 4,
        "technology": 3,
        "investigation": 3,
        "alertness": 3,
        "academics": 2,
        "crafts": 1,
        "science": 1,
        # Virtues (must total 6)
        "conviction": 2,
        "courage": 2,
        "conscience": 2,
        # Enhancements
        "enhancements": ["Enhanced Perception", "Pattern Recognition"],
    },
    {
        "username": "gh0st_in_shell",
        "name": "Janet Price",
        "master": "Murmur",
        "faith_potential": 3,
        "concept": "True-crime podcaster with supernatural source access",
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
        "expression": 4,
        "investigation": 3,
        "subterfuge": 3,
        "streetwise": 2,
        "computer": 2,
        "alertness": 2,
        "empathy": 2,
        # Virtues (must total 6)
        "conviction": 3,
        "courage": 2,
        "conscience": 1,
        # Enhancements
        "enhancements": ["Enhanced Intuition", "Compelling Voice"],
    },
    {
        "username": "Zephyr_Storm",
        "name": "Sarah Mitchell",
        "master": "Penemue",
        "faith_potential": 2,
        "concept": "Young reporter with impossible scoops",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 3,
        "appearance": 3,
        "perception": 3,
        "intelligence": 3,
        "wits": 3,
        # Abilities: 13/9/5
        "expression": 4,
        "investigation": 3,
        "empathy": 2,
        "alertness": 2,
        "subterfuge": 2,
        "computer": 2,
        "streetwise": 2,
        "academics": 1,
        # Virtues (must total 6)
        "conviction": 2,
        "courage": 2,
        "conscience": 2,
        # Enhancements
        "enhancements": ["Enhanced Intuition", "Luck"],
    },
    {
        "username": "n00b_hunter",
        "name": "Jason Park",
        "master": "Allocer",
        "faith_potential": 1,
        "concept": "Recently bound thrall still processing reality",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 3,
        "perception": 3,
        "intelligence": 3,
        "wits": 3,
        # Abilities: 13/9/5
        "computer": 3,
        "alertness": 2,
        "athletics": 2,
        "subterfuge": 2,
        "empathy": 2,
        "expression": 2,
        "streetwise": 1,
        "drive": 1,
        # Virtues (must total 6)
        "conviction": 2,
        "courage": 2,
        "conscience": 2,
        # Enhancements
        "enhancements": ["Minor Luck"],
    },
    {
        "username": "void_whisper",
        "name": "Detective Morris",
        "master": "Abaddon",
        "faith_potential": 3,
        "concept": "Homicide detective with infernal insight",
        # Attributes: 7/5/3
        "strength": 3,
        "dexterity": 3,
        "stamina": 3,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "investigation": 4,
        "firearms": 3,
        "streetwise": 3,
        "alertness": 3,
        "brawl": 2,
        "intimidation": 2,
        "law": 2,
        # Virtues (must total 6)
        "conviction": 2,
        "courage": 3,
        "conscience": 1,
        # Enhancements
        "enhancements": ["Enhanced Perception", "Death Sense"],
    },
]


# Earthbound characters (ancient demons trapped in reliquaries)
EARTHBOUND = [
    {
        "username": "CrypticMoon",
        "name": "The Resonance",
        "celestial_name": "Kashalel",
        "house": "Fiends",
        "reliquary_type": "location",
        "reliquary_description": "A sacred site now buried under a tech campus parking garage",
        "concept": "Ancient demon seeping influence through concrete into dreams",
        # Urges (replace attributes when manifesting)
        "urge_flesh": 2,
        "urge_thought": 4,
        "urge_emotion": 3,
        # Lores (Earthbound can have more)
        "lore_of_patterns": 3,
        "lore_of_humanity": 2,
        "lore_of_longing": 2,
        # Faith and Torment
        "faith": 5,
        "torment": 7,
        "max_faith": 20,
        # Virtues
        "conviction": 3,
        "courage": 2,
        "conscience": 1,
        # Cult
        "cult_size": "A handful of tech workers who experience 'revelatory dreams'",
    },
    {
        "username": "ByteSlayer",
        "name": "The Foundation",
        "celestial_name": "Barakiel",
        "house": "Malefactors",
        "reliquary_type": "location",
        "reliquary_description": "The bedrock beneath Seattle's oldest church",
        "concept": "Demon corrupting congregation through dreams of righteous fury",
        # Urges
        "urge_flesh": 3,
        "urge_thought": 3,
        "urge_emotion": 3,
        # Lores
        "lore_of_the_forge": 3,
        "lore_of_the_fundament": 2,
        "lore_of_humanity": 2,
        # Faith and Torment
        "faith": 6,
        "torment": 8,
        "max_faith": 25,
        # Virtues
        "conviction": 3,
        "courage": 2,
        "conscience": 1,
        # Cult
        "cult_size": "A devout congregation unknowingly worshipping through prayer",
    },
    {
        "username": "ElectricDreamer",
        "name": "The Frequency",
        "celestial_name": "Nergaliel",
        "house": "Defilers",
        "reliquary_type": "improvised",
        "reliquary_description": "A radio tower broadcasting subliminal messages",
        "concept": "Demon influencing dreams of everyone within broadcast range",
        # Urges
        "urge_flesh": 2,
        "urge_thought": 3,
        "urge_emotion": 4,
        # Lores
        "lore_of_longing": 3,
        "lore_of_radiance": 2,
        "lore_of_storms": 2,
        # Faith and Torment
        "faith": 4,
        "torment": 6,
        "max_faith": 15,
        # Virtues
        "conviction": 2,
        "courage": 2,
        "conscience": 2,
        # Cult
        "cult_size": "Radio station employees and late-night listeners",
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


def create_demons(chronicle, st_user):
    """Create Demon characters and assign to conclaves."""
    print("\n--- Creating Demon Characters ---")

    # Cache houses, factions, and conclaves
    houses = {h.name: h for h in DemonHouse.objects.all()}
    factions = {f.name: f for f in DemonFaction.objects.all()}
    conclaves = {c.name: c for c in Conclave.objects.filter(chronicle=chronicle)}

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
        "leadership",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "performance",
        "stealth",
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
    ]
    backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "alternate_identity",
        "cult",
        "eminence",
        "fame",
        "followers",
        "influence",
        "legacy",
        "pacts",
        "paragon",
        "resources",
        "retainers",
    ]
    lores = [
        "lore_of_awakening",
        "lore_of_the_beast",
        "lore_of_the_celestials",
        "lore_of_death",
        "lore_of_the_earth",
        "lore_of_flame",
        "lore_of_the_firmament",
        "lore_of_the_flesh",
        "lore_of_the_forge",
        "lore_of_the_fundament",
        "lore_of_humanity",
        "lore_of_light",
        "lore_of_longing",
        "lore_of_paths",
        "lore_of_patterns",
        "lore_of_portals",
        "lore_of_radiance",
        "lore_of_the_realms",
        "lore_of_the_spirit",
        "lore_of_storms",
        "lore_of_transfiguration",
        "lore_of_the_wild",
        "lore_of_the_winds",
    ]

    for data in DEMONS:
        # Get or create user
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            print(f"  WARNING: User {data['username']} not found, skipping {data['name']}")
            continue

        # Get house and faction
        house = houses.get(data["house"])
        faction = factions.get(data["faction"])

        if not house:
            print(f"  WARNING: House {data['house']} not found, skipping {data['name']}")
            continue

        # Create or get demon
        demon, created = Demon.objects.get_or_create(
            name=data["name"],
            owner=user,
            defaults={
                "chronicle": chronicle,
                "house": house,
                "faction": faction,
                "celestial_name": data.get("celestial_name", ""),
                "host_name": data.get("host_name", ""),
                "concept": data.get("concept", ""),
                "npc": False,
            },
        )

        if created:
            # Apply stats
            apply_stats(demon, data, attributes)
            apply_stats(demon, data, abilities)
            apply_stats(demon, data, backgrounds)
            apply_stats(demon, data, lores)

            # Set virtues
            demon.conviction = data.get("conviction", 1)
            demon.courage = data.get("courage", 1)
            demon.conscience = data.get("conscience", 1)

            # Set faith and torment
            demon.faith = data.get("faith", 3)
            demon.temporary_faith = demon.faith
            demon.torment = data.get("torment", house.starting_torment)

            # Willpower = Courage for demons
            demon.willpower = demon.courage

            demon.save()
            print(f"  Created demon: {data['name']} ({data['house']}, {data['faction']})")
        else:
            print(f"  Demon already exists: {data['name']}")

        # Assign to conclave
        conclave_name = data.get("conclave")
        if conclave_name and conclave_name in conclaves:
            conclave = conclaves[conclave_name]
            if demon not in conclave.members.all():
                conclave.members.add(demon)
                print(f"    Added to conclave: {conclave_name}")

            if data.get("is_leader"):
                conclave.leader = demon
                conclave.save()
                print(f"    Set as conclave leader")


def create_thralls(chronicle, st_user):
    """Create Thrall characters and link to demon masters."""
    print("\n--- Creating Thrall Characters ---")

    # Cache demons by name for master lookup
    demons = {d.name: d for d in Demon.objects.filter(chronicle=chronicle)}

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
        "leadership",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "performance",
        "stealth",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "occult",
        "science",
        "technology",
        "law",
    ]

    for data in THRALLS:
        # Get or create user
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            print(f"  WARNING: User {data['username']} not found, skipping {data['name']}")
            continue

        # Get master demon
        master = demons.get(data["master"])

        # Create or get thrall
        thrall, created = Thrall.objects.get_or_create(
            name=data["name"],
            owner=user,
            defaults={
                "chronicle": chronicle,
                "master": master,
                "faith_potential": data.get("faith_potential", 1),
                "concept": data.get("concept", ""),
                "enhancements": data.get("enhancements", []),
                "npc": False,
            },
        )

        if created:
            # Apply stats
            apply_stats(thrall, data, attributes)
            apply_stats(thrall, data, abilities)

            # Set virtues
            thrall.conviction = data.get("conviction", 2)
            thrall.courage = data.get("courage", 2)
            thrall.conscience = data.get("conscience", 2)

            # Calculate daily faith
            thrall.daily_faith_offered = (thrall.faith_potential + 1) // 2

            thrall.willpower = 3
            thrall.save()
            master_name = master.name if master else "None"
            print(f"  Created thrall: {data['name']} (master: {master_name})")
        else:
            print(f"  Thrall already exists: {data['name']}")


def create_earthbound(chronicle, st_user):
    """Create Earthbound characters."""
    print("\n--- Creating Earthbound Characters ---")

    # Cache houses
    houses = {h.name: h for h in DemonHouse.objects.all()}

    lores = [
        "lore_of_awakening",
        "lore_of_the_beast",
        "lore_of_the_celestials",
        "lore_of_death",
        "lore_of_the_earth",
        "lore_of_flame",
        "lore_of_the_firmament",
        "lore_of_the_flesh",
        "lore_of_the_forge",
        "lore_of_the_fundament",
        "lore_of_humanity",
        "lore_of_light",
        "lore_of_longing",
        "lore_of_paths",
        "lore_of_patterns",
        "lore_of_portals",
        "lore_of_radiance",
        "lore_of_the_realms",
        "lore_of_the_spirit",
        "lore_of_storms",
        "lore_of_transfiguration",
        "lore_of_the_wild",
        "lore_of_the_winds",
    ]

    for data in EARTHBOUND:
        # Get or create user
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            print(f"  WARNING: User {data['username']} not found, skipping {data['name']}")
            continue

        # Get house
        house = houses.get(data["house"])

        # Create or get earthbound
        earthbound, created = Earthbound.objects.get_or_create(
            name=data["name"],
            owner=user,
            defaults={
                "chronicle": chronicle,
                "house": house,
                "celestial_name": data.get("celestial_name", ""),
                "reliquary_type": data.get("reliquary_type", "location"),
                "reliquary_description": data.get("reliquary_description", ""),
                "concept": data.get("concept", ""),
                "cult_size": data.get("cult_size", ""),
                "npc": True,  # Earthbound are typically NPCs
            },
        )

        if created:
            # Apply urges
            earthbound.urge_flesh = data.get("urge_flesh", 1)
            earthbound.urge_thought = data.get("urge_thought", 1)
            earthbound.urge_emotion = data.get("urge_emotion", 1)

            # Apply lores
            apply_stats(earthbound, data, lores)

            # Set virtues
            earthbound.conviction = data.get("conviction", 2)
            earthbound.courage = data.get("courage", 2)
            earthbound.conscience = data.get("conscience", 2)

            # Set faith and torment
            earthbound.faith = data.get("faith", 5)
            earthbound.temporary_faith = earthbound.faith
            earthbound.max_faith = data.get("max_faith", 15)
            earthbound.torment = data.get("torment", 6)

            # Earthbound willpower based on courage
            earthbound.willpower = earthbound.courage

            earthbound.save()
            print(f"  Created earthbound: {data['name']} ({data['reliquary_type']})")
        else:
            print(f"  Earthbound already exists: {data['name']}")


def main():
    """Run the full Demon character setup."""
    print("=" * 60)
    print("Seattle Test Chronicle - Demon Character Setup")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()
    if not chronicle or not st_user:
        return

    create_demons(chronicle, st_user)
    create_thralls(chronicle, st_user)
    create_earthbound(chronicle, st_user)

    # Summary
    print("\n" + "=" * 60)
    print("Demon character setup complete!")
    print(f"Demons: {Demon.objects.filter(chronicle=chronicle).count()}")
    print(f"Thralls: {Thrall.objects.filter(chronicle=chronicle).count()}")
    print(f"Earthbound: {Earthbound.objects.filter(chronicle=chronicle).count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    # When run via `python manage.py shell < script.py`
    main()
