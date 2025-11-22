"""
Character templates for Vampire: The Masquerade
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


def populate_vampire_templates():
    """Load Vampire character templates from sourcebooks"""

    # Template 1: Detective (Brujah/Ventrue)
    detective = CharacterTemplate.objects.get_or_create(
        name="Detective",
        gameline="vtm",
        defaults={
            "character_type": "vampire",
            "description": "A world-weary cop who's seen it all—now from the other side of the yellow tape.",
            "source_book": "Vampire: The Masquerade Revised, p. 87",
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
                "empathy": 1,
                "intimidation": 3,
                "streetwise": 2,
                "firearms": 3,
                "drive": 2,
                "investigation": 4,
                "law": 2,
                "occult": 1,
            },
            "backgrounds": [
                {"name": "Contacts", "rating": 3},
                {"name": "Resources", "rating": 2},
                {"name": "Mentor", "rating": 1},
            ],
            "powers": {
                "auspex": 2,
                "fortitude": 1,
            },
            "specialties": ["Investigation (Crime Scenes)"],
            "languages": ["English"],
            "equipment": "Detective's badge, 9mm pistol, handcuffs, notebook",
            "suggested_freebie_spending": {
                "disciplines": 5,
                "backgrounds": 2,
                "willpower": 3,
                "abilities": 5,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 2: Socialite (Toreador/Ventrue)
    socialite = CharacterTemplate.objects.get_or_create(
        name="Socialite",
        gameline="vtm",
        defaults={
            "character_type": "vampire",
            "description": "You've always been the life of the party, and death won't stop you now.",
            "source_book": "Vampire: The Masquerade Revised, p. 88",
            "concept": "Socialite",
            "basic_info": {
                "nature": "FK:Archetype:Gallant",
                "demeanor": "FK:Archetype:Bon Vivant",
                "concept": "Socialite",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 2,
                "stamina": 2,
                "perception": 3,
                "intelligence": 2,
                "wits": 4,
                "charisma": 4,
                "manipulation": 3,
                "appearance": 4,
            },
            "abilities": {
                "empathy": 3,
                "expression": 2,
                "leadership": 1,
                "streetwise": 1,
                "subterfuge": 3,
                "etiquette": 4,
                "performance": 2,
                "academics": 1,
                "finance": 2,
                "politics": 2,
            },
            "backgrounds": [
                {"name": "Influence", "rating": 2},
                {"name": "Resources", "rating": 3},
                {"name": "Status", "rating": 2},
            ],
            "powers": {
                "presence": 2,
                "celerity": 1,
            },
            "specialties": ["Etiquette (High Society)"],
            "languages": ["English", "French"],
            "equipment": "Designer clothes, smartphone, black AmEx card",
            "suggested_freebie_spending": {
                "disciplines": 5,
                "backgrounds": 3,
                "willpower": 2,
                "attributes": 5,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 3: Street Preacher (Brujah/Gangrel)
    preacher = CharacterTemplate.objects.get_or_create(
        name="Street Preacher",
        gameline="vtm",
        defaults={
            "character_type": "vampire",
            "description": "A voice crying out in the urban wilderness, bringing harsh truths to those who will listen.",
            "source_book": "Vampire: The Masquerade Revised, p. 89",
            "concept": "Street Preacher",
            "basic_info": {
                "nature": "FK:Archetype:Fanatic",
                "demeanor": "FK:Archetype:Visionary",
                "concept": "Street Preacher",
            },
            "attributes": {
                "strength": 3,
                "dexterity": 2,
                "stamina": 3,
                "perception": 3,
                "intelligence": 3,
                "wits": 2,
                "charisma": 4,
                "manipulation": 2,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 2,
                "empathy": 2,
                "expression": 4,
                "intimidation": 3,
                "streetwise": 3,
                "brawl": 2,
                "survival": 2,
                "academics": 2,
                "occult": 2,
                "theology": 3,
            },
            "backgrounds": [
                {"name": "Contacts", "rating": 2},
                {"name": "Allies", "rating": 2},
                {"name": "Herd", "rating": 2},
            ],
            "powers": {
                "potence": 2,
                "presence": 1,
            },
            "specialties": ["Expression (Sermons)"],
            "languages": ["English"],
            "equipment": "Worn bible, megaphone, simple robes",
            "suggested_freebie_spending": {
                "disciplines": 5,
                "willpower": 4,
                "abilities": 3,
                "backgrounds": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 4: Criminal (Giovanni/Nosferatu)
    criminal = CharacterTemplate.objects.get_or_create(
        name="Criminal",
        gameline="vtm",
        defaults={
            "character_type": "vampire",
            "description": "You made your living breaking the law, and unlife hasn't changed your profession.",
            "source_book": "Vampire: The Masquerade Revised, p. 90",
            "concept": "Criminal",
            "basic_info": {
                "nature": "FK:Archetype:Survivor",
                "demeanor": "FK:Archetype:Deviant",
                "concept": "Criminal",
            },
            "attributes": {
                "strength": 3,
                "dexterity": 4,
                "stamina": 2,
                "perception": 3,
                "intelligence": 2,
                "wits": 4,
                "charisma": 2,
                "manipulation": 3,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 3,
                "athletics": 2,
                "brawl": 2,
                "dodge": 3,
                "streetwise": 4,
                "subterfuge": 2,
                "firearms": 2,
                "larceny": 4,
                "stealth": 3,
                "computer": 1,
                "investigation": 2,
            },
            "backgrounds": [
                {"name": "Contacts", "rating": 3},
                {"name": "Resources", "rating": 2},
                {"name": "Retainers", "rating": 1},
            ],
            "powers": {
                "obfuscate": 2,
                "celerity": 1,
            },
            "specialties": ["Larceny (Safecracking)"],
            "languages": ["English"],
            "equipment": "Lock picks, burner phone, dark clothing",
            "suggested_freebie_spending": {
                "disciplines": 5,
                "abilities": 5,
                "backgrounds": 3,
                "willpower": 2,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 5: Scholar (Tremere/Ventrue)
    scholar = CharacterTemplate.objects.get_or_create(
        name="Scholar",
        gameline="vtm",
        defaults={
            "character_type": "vampire",
            "description": "Knowledge is power, and you've spent your existence accumulating both.",
            "source_book": "Vampire: The Masquerade Revised, p. 91",
            "concept": "Scholar",
            "basic_info": {
                "nature": "FK:Archetype:Architect",
                "demeanor": "FK:Archetype:Pedagogue",
                "concept": "Scholar",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 2,
                "stamina": 2,
                "perception": 3,
                "intelligence": 4,
                "wits": 3,
                "charisma": 2,
                "manipulation": 3,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 1,
                "awareness": 2,
                "expression": 2,
                "subterfuge": 2,
                "etiquette": 2,
                "academics": 4,
                "investigation": 3,
                "linguistics": 2,
                "occult": 4,
                "science": 2,
            },
            "backgrounds": [
                {"name": "Library", "rating": 3},
                {"name": "Mentor", "rating": 2},
                {"name": "Resources", "rating": 2},
            ],
            "powers": {
                "auspex": 2,
                "thaumaturgy": 1,
            },
            "specialties": ["Occult (Vampiric Lore)"],
            "languages": ["English", "Latin", "Ancient Greek"],
            "equipment": "Rare books, research notes, reading glasses",
            "suggested_freebie_spending": {
                "disciplines": 5,
                "backgrounds": 3,
                "abilities": 4,
                "willpower": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    print(
        f"✓ Created/updated {CharacterTemplate.objects.filter(gameline='vtm').count()} Vampire templates"
    )
    return [detective, socialite, preacher, criminal, scholar]


if __name__ == "__main__":
    populate_vampire_templates()
    print("\nVampire character templates populated successfully!")
