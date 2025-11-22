"""
Character templates for Demon: The Fallen
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


def populate_demon_templates():
    """Load Demon character templates from sourcebooks"""

    # Template 1: Fallen Detective
    detective = CharacterTemplate.objects.get_or_create(
        name="Fallen Detective",
        gameline="dtf",
        defaults={
            "character_type": "demon",
            "description": "A Devil who inhabits a detective's body, using mortal connections to navigate the modern world.",
            "source_book": "Demon: The Fallen Core, p. 178",
            "concept": "Detective",
            "basic_info": {
                "nature": "FK:Archetype:Judge",
                "demeanor": "FK:Archetype:Professional",
                "concept": "Detective",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 2,
                "stamina": 3,
                "perception": 4,
                "intelligence": 3,
                "wits": 3,
                "charisma": 2,
                "manipulation": 3,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 2,
                "athletics": 1,
                "brawl": 2,
                "empathy": 2,
                "intimidation": 3,
                "streetwise": 2,
                "firearms": 3,
                "investigation": 4,
                "law": 2,
                "occult": 2,
            },
            "backgrounds": [
                {"name": "Contacts", "rating": 3},
                {"name": "Resources", "rating": 2},
                {"name": "Eminence", "rating": 1},
            ],
            "powers": {
                "faith": 3,
                "torment": 3,
            },
            "specialties": ["Investigation (Crime Scenes)"],
            "languages": ["English", "Enochian"],
            "equipment": "Detective's badge, service weapon, case files",
            "suggested_freebie_spending": {
                "lore": 6,
                "faith": 2,
                "abilities": 4,
                "backgrounds": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 2: Corrupted Artist
    artist = CharacterTemplate.objects.get_or_create(
        name="Corrupted Artist",
        gameline="dtf",
        defaults={
            "character_type": "demon",
            "description": "A Fiend who channels demonic power through creative expression.",
            "source_book": "Demon: The Fallen Core, p. 179",
            "concept": "Artist",
            "basic_info": {
                "nature": "FK:Archetype:Visionary",
                "demeanor": "FK:Archetype:Deviant",
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
                "manipulation": 3,
                "appearance": 3,
            },
            "abilities": {
                "alertness": 2,
                "empathy": 3,
                "expression": 4,
                "subterfuge": 2,
                "crafts": 3,
                "performance": 4,
                "academics": 2,
                "enigmas": 2,
                "occult": 3,
            },
            "backgrounds": [
                {"name": "Contacts", "rating": 2},
                {"name": "Resources", "rating": 2},
                {"name": "Followers", "rating": 2},
            ],
            "powers": {
                "faith": 3,
                "torment": 4,
            },
            "specialties": ["Performance (Dark Art)"],
            "languages": ["English", "Enochian"],
            "equipment": "Art supplies, portfolio, occult symbols",
            "suggested_freebie_spending": {
                "lore": 6,
                "abilities": 4,
                "faith": 2,
                "willpower": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 3: Angelic Warrior
    warrior = CharacterTemplate.objects.get_or_create(
        name="Angelic Warrior",
        gameline="dtf",
        defaults={
            "character_type": "demon",
            "description": "A Scourge who fights the infernal war with righteous fury.",
            "source_book": "Demon: The Fallen Core, p. 180",
            "concept": "Warrior",
            "basic_info": {
                "nature": "FK:Archetype:Defender",
                "demeanor": "FK:Archetype:Bravo",
                "concept": "Warrior",
            },
            "attributes": {
                "strength": 4,
                "dexterity": 3,
                "stamina": 3,
                "perception": 3,
                "intelligence": 2,
                "wits": 3,
                "charisma": 2,
                "manipulation": 2,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 3,
                "athletics": 3,
                "brawl": 4,
                "dodge": 3,
                "intimidation": 3,
                "firearms": 2,
                "melee": 3,
                "stealth": 1,
                "investigation": 1,
                "occult": 2,
            },
            "backgrounds": [
                {"name": "Allies", "rating": 2},
                {"name": "Resources", "rating": 1},
                {"name": "Eminence", "rating": 3},
            ],
            "powers": {
                "faith": 4,
                "torment": 2,
            },
            "specialties": ["Brawl (Apocalyptic Form)"],
            "languages": ["English", "Enochian"],
            "equipment": "Combat gear, weapons, tactical equipment",
            "suggested_freebie_spending": {
                "lore": 6,
                "faith": 2,
                "willpower": 4,
                "attributes": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 4: Tempter
    tempter = CharacterTemplate.objects.get_or_create(
        name="Tempter",
        gameline="dtf",
        defaults={
            "character_type": "demon",
            "description": "A Defiler who corrupts mortals through seduction and manipulation.",
            "source_book": "Demon: The Fallen Core, p. 181",
            "concept": "Tempter",
            "basic_info": {
                "nature": "FK:Archetype:Deviant",
                "demeanor": "FK:Archetype:Bon Vivant",
                "concept": "Tempter",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 3,
                "stamina": 2,
                "perception": 3,
                "intelligence": 3,
                "wits": 4,
                "charisma": 4,
                "manipulation": 4,
                "appearance": 4,
            },
            "abilities": {
                "alertness": 2,
                "empathy": 3,
                "expression": 3,
                "intimidation": 2,
                "streetwise": 2,
                "subterfuge": 4,
                "etiquette": 3,
                "performance": 2,
                "academics": 2,
                "occult": 3,
            },
            "backgrounds": [
                {"name": "Contacts", "rating": 3},
                {"name": "Influence", "rating": 2},
                {"name": "Resources", "rating": 2},
            ],
            "powers": {
                "faith": 3,
                "torment": 4,
            },
            "specialties": ["Subterfuge (Seduction)"],
            "languages": ["English", "Enochian"],
            "equipment": "Designer clothes, expensive accessories",
            "suggested_freebie_spending": {
                "lore": 6,
                "abilities": 5,
                "backgrounds": 3,
                "willpower": 1,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 5: Healer
    healer = CharacterTemplate.objects.get_or_create(
        name="Angelic Healer",
        gameline="dtf",
        defaults={
            "character_type": "demon",
            "description": "A Malefactor who still remembers the purpose of creation and seeks to heal.",
            "source_book": "Demon: The Fallen Core, p. 182",
            "concept": "Healer",
            "basic_info": {
                "nature": "FK:Archetype:Caregiver",
                "demeanor": "FK:Archetype:Martyr",
                "concept": "Healer",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 2,
                "stamina": 3,
                "perception": 4,
                "intelligence": 4,
                "wits": 3,
                "charisma": 3,
                "manipulation": 2,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 2,
                "awareness": 3,
                "empathy": 4,
                "expression": 2,
                "crafts": 2,
                "medicine": 4,
                "academics": 3,
                "investigation": 2,
                "occult": 3,
                "science": 2,
            },
            "backgrounds": [
                {"name": "Allies", "rating": 2},
                {"name": "Resources", "rating": 2},
                {"name": "Eminence", "rating": 2},
            ],
            "powers": {
                "faith": 4,
                "torment": 2,
            },
            "specialties": ["Medicine (Emergency Care)"],
            "languages": ["English", "Enochian"],
            "equipment": "Medical supplies, healing tools",
            "suggested_freebie_spending": {
                "lore": 6,
                "faith": 2,
                "abilities": 4,
                "willpower": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    print(
        f"✓ Created/updated {CharacterTemplate.objects.filter(gameline='dtf').count()} Demon templates"
    )
    return [detective, artist, warrior, tempter, healer]


if __name__ == "__main__":
    populate_demon_templates()
    print("\nDemon character templates populated successfully!")
