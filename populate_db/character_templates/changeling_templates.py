"""
Character templates for Changeling: The Dreaming
Pre-built character concepts from sourcebooks
"""

import os
import sys

import django

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")
django.setup()

from core.models import CharacterTemplate


def populate_changeling_templates():
    """Load Changeling character templates from sourcebooks"""

    # Template 1: Childling Dreamer
    dreamer = CharacterTemplate.objects.get_or_create(
        name="Childling Dreamer",
        gameline="ctd",
        defaults={
            "character_type": "changeling",
            "description": "A young changeling full of wonder and creativity, still deeply connected to the Dreaming.",
            "source_book": "Changeling: The Dreaming 20th Anniversary, p. 145",
            "concept": "Dreamer",
            "basic_info": {
                "nature": "FK:Archetype:Child",
                "demeanor": "FK:Archetype:Innocent",
                "concept": "Dreamer",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 3,
                "stamina": 2,
                "perception": 3,
                "intelligence": 2,
                "wits": 4,
                "charisma": 3,
                "manipulation": 2,
                "appearance": 3,
            },
            "abilities": {
                "alertness": 2,
                "empathy": 3,
                "expression": 3,
                "kenning": 3,
                "streetwise": 1,
                "subterfuge": 2,
                "crafts": 2,
                "etiquette": 1,
                "performance": 2,
                "academics": 2,
                "enigmas": 3,
                "gremayre": 2,
            },
            "backgrounds": [
                {"name": "Chimera", "rating": 2},
                {"name": "Dreamers", "rating": 2},
                {"name": "Mentor", "rating": 2},
            ],
            "powers": {
                "glamour": 5,
                "willpower": 3,
            },
            "specialties": ["Expression (Storytelling)"],
            "languages": ["English"],
            "equipment": "Favorite toy, dream journal, colorful clothes",
            "suggested_freebie_spending": {
                "arts": 5,
                "realms": 3,
                "glamour": 2,
                "abilities": 5,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 2: Wilder Artist
    artist = CharacterTemplate.objects.get_or_create(
        name="Wilder Artist",
        gameline="ctd",
        defaults={
            "character_type": "changeling",
            "description": "A passionate creator who channels Glamour through art and performance.",
            "source_book": "Changeling: The Dreaming 20th Anniversary, p. 146",
            "concept": "Artist",
            "basic_info": {
                "nature": "FK:Archetype:Visionary",
                "demeanor": "FK:Archetype:Bon Vivant",
                "concept": "Artist",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 3,
                "stamina": 2,
                "perception": 4,
                "intelligence": 3,
                "wits": 3,
                "charisma": 4,
                "manipulation": 2,
                "appearance": 3,
            },
            "abilities": {
                "alertness": 2,
                "empathy": 2,
                "expression": 4,
                "kenning": 2,
                "streetwise": 2,
                "subterfuge": 1,
                "crafts": 3,
                "performance": 4,
                "academics": 2,
                "enigmas": 2,
                "gremayre": 2,
            },
            "backgrounds": [
                {"name": "Contacts", "rating": 2},
                {"name": "Dreamers", "rating": 3},
                {"name": "Treasure", "rating": 1},
            ],
            "powers": {
                "glamour": 4,
                "willpower": 4,
            },
            "specialties": ["Performance (Music)"],
            "languages": ["English"],
            "equipment": "Musical instrument or art supplies, portfolio",
            "suggested_freebie_spending": {
                "arts": 5,
                "realms": 3,
                "abilities": 4,
                "willpower": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 3: Grump Crafter
    crafter = CharacterTemplate.objects.get_or_create(
        name="Grump Crafter",
        gameline="ctd",
        defaults={
            "character_type": "changeling",
            "description": "An experienced artisan who has weathered Banality but still creates wonders.",
            "source_book": "Changeling: The Dreaming 20th Anniversary, p. 147",
            "concept": "Crafter",
            "basic_info": {
                "nature": "FK:Archetype:Architect",
                "demeanor": "FK:Archetype:Curmudgeon",
                "concept": "Crafter",
            },
            "attributes": {
                "strength": 3,
                "dexterity": 3,
                "stamina": 3,
                "perception": 4,
                "intelligence": 4,
                "wits": 2,
                "charisma": 2,
                "manipulation": 2,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 2,
                "empathy": 1,
                "intimidation": 2,
                "kenning": 3,
                "subterfuge": 2,
                "crafts": 4,
                "etiquette": 2,
                "melee": 1,
                "academics": 2,
                "enigmas": 3,
                "gremayre": 4,
                "politics": 2,
            },
            "backgrounds": [
                {"name": "Holdings", "rating": 3},
                {"name": "Resources", "rating": 2},
                {"name": "Title", "rating": 1},
            ],
            "powers": {
                "glamour": 4,
                "willpower": 5,
            },
            "specialties": ["Crafts (Metalwork)"],
            "languages": ["English"],
            "equipment": "Master craftsman tools, workshop",
            "suggested_freebie_spending": {
                "arts": 5,
                "realms": 3,
                "willpower": 3,
                "backgrounds": 4,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 4: Knight Errant
    knight = CharacterTemplate.objects.get_or_create(
        name="Knight Errant",
        gameline="ctd",
        defaults={
            "character_type": "changeling",
            "description": "A noble warrior sworn to protect the Dreaming and uphold chivalric ideals.",
            "source_book": "Changeling: The Dreaming 20th Anniversary, p. 148",
            "concept": "Knight",
            "basic_info": {
                "nature": "FK:Archetype:Defender",
                "demeanor": "FK:Archetype:Gallant",
                "concept": "Knight",
            },
            "attributes": {
                "strength": 3,
                "dexterity": 3,
                "stamina": 3,
                "perception": 3,
                "intelligence": 2,
                "wits": 3,
                "charisma": 3,
                "manipulation": 2,
                "appearance": 3,
            },
            "abilities": {
                "alertness": 3,
                "athletics": 3,
                "brawl": 2,
                "dodge": 2,
                "kenning": 2,
                "leadership": 3,
                "drive": 1,
                "etiquette": 3,
                "melee": 4,
                "academics": 1,
                "gremayre": 2,
                "law": 2,
            },
            "backgrounds": [
                {"name": "Title", "rating": 2},
                {"name": "Treasure", "rating": 2},
                {"name": "Mentor", "rating": 2},
            ],
            "powers": {
                "glamour": 4,
                "willpower": 5,
            },
            "specialties": ["Melee (Sword)"],
            "languages": ["English"],
            "equipment": "Sword, shield, coat of arms",
            "suggested_freebie_spending": {
                "arts": 5,
                "realms": 3,
                "willpower": 3,
                "abilities": 4,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 5: Street Urchin
    urchin = CharacterTemplate.objects.get_or_create(
        name="Street Urchin",
        gameline="ctd",
        defaults={
            "character_type": "changeling",
            "description": "A scrappy survivor who lives on the margins of both mortal and fae society.",
            "source_book": "Changeling: The Dreaming 20th Anniversary, p. 149",
            "concept": "Street Urchin",
            "basic_info": {
                "nature": "FK:Archetype:Survivor",
                "demeanor": "FK:Archetype:Rogue",
                "concept": "Street Urchin",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 4,
                "stamina": 2,
                "perception": 3,
                "intelligence": 2,
                "wits": 4,
                "charisma": 3,
                "manipulation": 3,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 3,
                "athletics": 2,
                "dodge": 3,
                "empathy": 2,
                "kenning": 2,
                "streetwise": 4,
                "subterfuge": 3,
                "larceny": 3,
                "stealth": 3,
                "survival": 2,
                "enigmas": 1,
                "gremayre": 1,
            },
            "backgrounds": [
                {"name": "Contacts", "rating": 3},
                {"name": "Allies", "rating": 2},
                {"name": "Chimera", "rating": 1},
            ],
            "powers": {
                "glamour": 4,
                "willpower": 4,
            },
            "specialties": ["Streetwise (Urban Survival)"],
            "languages": ["English"],
            "equipment": "Backpack, stolen goods, street clothes",
            "suggested_freebie_spending": {
                "arts": 5,
                "realms": 3,
                "abilities": 5,
                "willpower": 2,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    print(
        f"✓ Created/updated {CharacterTemplate.objects.filter(gameline='ctd').count()} Changeling templates"
    )
    return [dreamer, artist, crafter, knight, urchin]


if __name__ == "__main__":
    populate_changeling_templates()
    print("\nChangeling character templates populated successfully!")
