"""
Character templates for Werewolf: The Apocalypse
Pre-built character concepts from sourcebooks
"""

import os
import sys
import django

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")
django.setup()

from core.models import CharacterTemplate


def populate_werewolf_templates():
    """Load Werewolf character templates from sourcebooks"""

    # Template 1: Ahroun Warrior
    warrior = CharacterTemplate.objects.get_or_create(
        name="Ahroun Warrior",
        gameline="wta",
        defaults={
            "character_type": "werewolf",
            "description": "A full moon warrior, bred for battle and born to lead the charge against the Wyrm.",
            "source_book": "Werewolf: The Apocalypse Revised, p. 95",
            "concept": "Warrior",
            "basic_info": {
                "nature": "FK:Archetype:Bravo",
                "demeanor": "FK:Archetype:Defender",
                "concept": "Warrior",
            },
            "attributes": {
                "strength": 3,
                "dexterity": 3,
                "stamina": 4,
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
                "primal_urge": 2,
                "melee": 3,
                "survival": 3,
                "enigmas": 1,
                "rituals": 2,
            },
            "backgrounds": [
                {"name": "Pure Breed", "rating": 2},
                {"name": "Fetish", "rating": 2},
                {"name": "Totem", "rating": 2},
            ],
            "powers": {
                "rage": 5,
                "gnosis": 3,
            },
            "specialties": ["Brawl (Claws)"],
            "languages": ["English"],
            "equipment": "Grand klaive, tribal markings, war paint",
            "suggested_freebie_spending": {
                "gifts": 7,
                "rage": 3,
                "abilities": 3,
                "backgrounds": 2,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 2: Theurge Mystic
    mystic = CharacterTemplate.objects.get_or_create(
        name="Theurge Mystic",
        gameline="wta",
        defaults={
            "character_type": "werewolf",
            "description": "A crescent moon shaman who walks between worlds and speaks with spirits.",
            "source_book": "Werewolf: The Apocalypse Revised, p. 96",
            "concept": "Mystic",
            "basic_info": {
                "nature": "FK:Archetype:Visionary",
                "demeanor": "FK:Archetype:Pedagogue",
                "concept": "Mystic",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 2,
                "stamina": 3,
                "perception": 4,
                "intelligence": 3,
                "wits": 4,
                "charisma": 3,
                "manipulation": 2,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 2,
                "empathy": 3,
                "expression": 2,
                "primal_urge": 3,
                "survival": 2,
                "animal_ken": 2,
                "meditation": 3,
                "cosmology": 3,
                "enigmas": 4,
                "occult": 3,
                "rituals": 4,
            },
            "backgrounds": [
                {"name": "Rites", "rating": 3},
                {"name": "Totem", "rating": 2},
                {"name": "Ancestors", "rating": 1},
            ],
            "powers": {
                "rage": 3,
                "gnosis": 5,
            },
            "specialties": ["Rituals (Rites of the Spirits)"],
            "languages": ["English"],
            "equipment": "Spirit talismans, ritual drum, medicine bag",
            "suggested_freebie_spending": {
                "gifts": 7,
                "gnosis": 3,
                "backgrounds": 3,
                "abilities": 2,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 3: Ragabash Trickster
    trickster = CharacterTemplate.objects.get_or_create(
        name="Ragabash Trickster",
        gameline="wta",
        defaults={
            "character_type": "werewolf",
            "description": "A new moon scout who uses cunning and stealth to outwit the enemies of Gaia.",
            "source_book": "Werewolf: The Apocalypse Revised, p. 97",
            "concept": "Trickster",
            "basic_info": {
                "nature": "FK:Archetype:Trickster",
                "demeanor": "FK:Archetype:Jester",
                "concept": "Trickster",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 4,
                "stamina": 3,
                "perception": 3,
                "intelligence": 3,
                "wits": 4,
                "charisma": 3,
                "manipulation": 3,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 3,
                "athletics": 2,
                "dodge": 4,
                "empathy": 2,
                "streetwise": 3,
                "subterfuge": 4,
                "larceny": 2,
                "stealth": 4,
                "survival": 2,
                "enigmas": 2,
                "investigation": 2,
            },
            "backgrounds": [
                {"name": "Contacts", "rating": 3},
                {"name": "Totem", "rating": 2},
                {"name": "Kinfolk", "rating": 1},
            ],
            "powers": {
                "rage": 3,
                "gnosis": 4,
            },
            "specialties": ["Stealth (Urban)"],
            "languages": ["English"],
            "equipment": "Urban camouflage, lock picks, smartphone",
            "suggested_freebie_spending": {
                "gifts": 7,
                "abilities": 4,
                "willpower": 2,
                "attributes": 2,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 4: Philodox Judge
    judge = CharacterTemplate.objects.get_or_create(
        name="Philodox Judge",
        gameline="wta",
        defaults={
            "character_type": "werewolf",
            "description": "A half moon mediator who keeps the peace and upholds the Litany.",
            "source_book": "Werewolf: The Apocalypse Revised, p. 98",
            "concept": "Judge",
            "basic_info": {
                "nature": "FK:Archetype:Judge",
                "demeanor": "FK:Archetype:Mediator",
                "concept": "Judge",
            },
            "attributes": {
                "strength": 3,
                "dexterity": 2,
                "stamina": 3,
                "perception": 4,
                "intelligence": 3,
                "wits": 3,
                "charisma": 3,
                "manipulation": 3,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 3,
                "empathy": 4,
                "expression": 2,
                "intimidation": 2,
                "primal_urge": 2,
                "brawl": 2,
                "leadership": 3,
                "enigmas": 2,
                "law": 3,
                "rituals": 3,
            },
            "backgrounds": [
                {"name": "Totem", "rating": 2},
                {"name": "Pure Breed", "rating": 2},
                {"name": "Allies", "rating": 2},
            ],
            "powers": {
                "rage": 4,
                "gnosis": 4,
            },
            "specialties": ["Empathy (Mediating Disputes)"],
            "languages": ["English"],
            "equipment": "Litany scroll, tribal token, peace pipe",
            "suggested_freebie_spending": {
                "gifts": 7,
                "abilities": 3,
                "willpower": 3,
                "backgrounds": 2,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 5: Galliard Bard
    bard = CharacterTemplate.objects.get_or_create(
        name="Galliard Bard",
        gameline="wta",
        defaults={
            "character_type": "werewolf",
            "description": "A gibbous moon storyteller who preserves the tales and traditions of the Garou.",
            "source_book": "Werewolf: The Apocalypse Revised, p. 99",
            "concept": "Bard",
            "basic_info": {
                "nature": "FK:Archetype:Celebrant",
                "demeanor": "FK:Archetype:Gallant",
                "concept": "Bard",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 3,
                "stamina": 3,
                "perception": 3,
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
                "intimidation": 2,
                "primal_urge": 2,
                "leadership": 2,
                "performance": 4,
                "enigmas": 2,
                "occult": 2,
                "rituals": 3,
            },
            "backgrounds": [
                {"name": "Totem", "rating": 2},
                {"name": "Ancestors", "rating": 2},
                {"name": "Kinfolk", "rating": 2},
            ],
            "powers": {
                "rage": 4,
                "gnosis": 4,
            },
            "specialties": ["Performance (Storytelling)"],
            "languages": ["English"],
            "equipment": "Musical instrument, tale scrolls, tribal regalia",
            "suggested_freebie_spending": {
                "gifts": 7,
                "abilities": 4,
                "backgrounds": 2,
                "willpower": 2,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    print(f"✓ Created/updated {CharacterTemplate.objects.filter(gameline='wta').count()} Werewolf templates")
    return [warrior, mystic, trickster, judge, bard]


if __name__ == "__main__":
    populate_werewolf_templates()
    print("\nWerewolf character templates populated successfully!")
