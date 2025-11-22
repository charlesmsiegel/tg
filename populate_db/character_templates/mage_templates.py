"""
Character templates for Mage: The Ascension
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


def populate_mage_templates():
    """Load Mage character templates from sourcebooks"""

    # Template 1: Virtual Adept Hacker
    hacker = CharacterTemplate.objects.get_or_create(
        name="Virtual Adept Hacker",
        gameline="mta",
        defaults={
            "character_type": "mage",
            "description": "A digital age mage who bends reality through code and virtual reality. You see the Matrix behind the matrix.",
            "source_book": "Mage: The Ascension Revised, p. 93",
            "concept": "Hacker",
            "basic_info": {
                "nature": "FK:Archetype:Visionary",
                "demeanor": "FK:Archetype:Rebel",
                "concept": "Hacker",
                "essence": "FK:Essence:Questing",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 3,
                "stamina": 2,
                "perception": 4,
                "intelligence": 4,
                "wits": 3,
                "charisma": 2,
                "manipulation": 3,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 2,
                "awareness": 2,
                "expression": 1,
                "streetwise": 2,
                "subterfuge": 1,
                "computer": 4,
                "crafts": 2,
                "drive": 1,
                "technology": 3,
                "cosmology": 2,
                "enigmas": 2,
                "investigation": 1,
                "science": 3,
            },
            "backgrounds": [
                {"name": "Avatar", "rating": 3},
                {"name": "Resources", "rating": 2},
                {"name": "Contacts", "rating": 2},
            ],
            "powers": {
                "correspondence": 1,
                "forces": 2,
                "arete": 1,
            },
            "specialties": ["Computer (Hacking)", "Science (Information Theory)"],
            "languages": ["English", "Binary (coding languages)"],
            "equipment": "High-end laptop, smartphone, VR headset, encrypted USB drives",
            "suggested_freebie_spending": {
                "arete": 4,
                "sphere": 2,
                "willpower": 3,
                "abilities": 3,
                "backgrounds": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 2: Hermetic Researcher
    hermetic = CharacterTemplate.objects.get_or_create(
        name="Order of Hermes Scholar",
        gameline="mta",
        defaults={
            "character_type": "mage",
            "description": "A traditional mage steeped in centuries of occult lore, wielding ancient formulae and hermetic principles.",
            "source_book": "Mage: The Ascension Revised, p. 91",
            "concept": "Hermetic Scholar",
            "basic_info": {
                "nature": "FK:Archetype:Traditionalist",
                "demeanor": "FK:Archetype:Pedagogue",
                "concept": "Hermetic Scholar",
                "essence": "FK:Essence:Pattern",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 2,
                "stamina": 2,
                "perception": 3,
                "intelligence": 4,
                "wits": 3,
                "charisma": 3,
                "manipulation": 2,
                "appearance": 2,
            },
            "abilities": {
                "awareness": 3,
                "expression": 2,
                "intimidation": 1,
                "etiquette": 2,
                "meditation": 2,
                "crafts": 1,
                "academics": 4,
                "cosmology": 3,
                "enigmas": 3,
                "investigation": 2,
                "occult": 4,
            },
            "backgrounds": [
                {"name": "Avatar", "rating": 3},
                {"name": "Library", "rating": 2},
                {"name": "Mentor", "rating": 2},
            ],
            "powers": {
                "forces": 2,
                "prime": 1,
                "arete": 1,
            },
            "specialties": [
                "Occult (Hermetic Magic)",
                "Academics (Classical Literature)",
            ],
            "languages": ["English", "Latin", "Ancient Greek"],
            "equipment": "Wand, grimoire, ritual athame, rare occult texts",
            "suggested_freebie_spending": {
                "arete": 4,
                "sphere": 2,
                "willpower": 4,
                "abilities": 2,
                "backgrounds": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 3: Verbena Healer
    healer = CharacterTemplate.objects.get_or_create(
        name="Verbena Healer",
        gameline="mta",
        defaults={
            "character_type": "mage",
            "description": "A nature mage who channels the primal forces of life, death, and rebirth through ancient pagan traditions.",
            "source_book": "Mage: The Ascension Revised, p. 96",
            "concept": "Healer/Midwife",
            "basic_info": {
                "nature": "FK:Archetype:Caregiver",
                "demeanor": "FK:Archetype:Traditionalist",
                "concept": "Healer",
                "essence": "FK:Essence:Primordial",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 3,
                "stamina": 3,
                "perception": 4,
                "intelligence": 3,
                "wits": 3,
                "charisma": 3,
                "manipulation": 2,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 2,
                "athletics": 1,
                "awareness": 3,
                "empathy": 3,
                "expression": 2,
                "meditation": 2,
                "crafts": 2,
                "survival": 3,
                "academics": 1,
                "cosmology": 2,
                "medicine": 4,
                "occult": 3,
            },
            "backgrounds": [
                {"name": "Avatar", "rating": 3},
                {"name": "Allies", "rating": 2},
                {"name": "Contacts", "rating": 2},
            ],
            "powers": {
                "life": 2,
                "prime": 1,
                "arete": 1,
            },
            "specialties": ["Medicine (Herbal Remedies)", "Occult (Pagan Rituals)"],
            "languages": ["English", "Celtic/Gaelic"],
            "equipment": "Herb pouch, athame, ritual bowl, medicinal plants",
            "suggested_freebie_spending": {
                "arete": 4,
                "sphere": 2,
                "willpower": 3,
                "abilities": 3,
                "backgrounds": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 4: Akashic Brother Martial Artist
    akashic = CharacterTemplate.objects.get_or_create(
        name="Akashic Brother",
        gameline="mta",
        defaults={
            "character_type": "mage",
            "description": "A warrior-philosopher who seeks enlightenment through martial discipline and meditation, mastering both body and mind.",
            "source_book": "Mage: The Ascension Revised, p. 89",
            "concept": "Martial Artist",
            "basic_info": {
                "nature": "FK:Archetype:Perfectionist",
                "demeanor": "FK:Archetype:Stoic",
                "concept": "Martial Artist",
                "essence": "FK:Essence:Questing",
            },
            "attributes": {
                "strength": 3,
                "dexterity": 4,
                "stamina": 3,
                "perception": 3,
                "intelligence": 3,
                "wits": 4,
                "charisma": 2,
                "manipulation": 2,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 3,
                "athletics": 4,
                "awareness": 3,
                "brawl": 4,
                "dodge": 3,
                "meditation": 3,
                "stealth": 2,
                "academics": 1,
                "cosmology": 2,
                "medicine": 2,
                "occult": 2,
            },
            "backgrounds": [
                {"name": "Avatar", "rating": 3},
                {"name": "Mentor", "rating": 1},
                {"name": "Dream", "rating": 2},
            ],
            "powers": {
                "life": 1,
                "mind": 2,
                "arete": 1,
            },
            "merits_flaws": [
                {"name": "Do", "rating": 5},
            ],
            "specialties": ["Athletics (Parkour)", "Brawl (Martial Arts)"],
            "languages": ["English", "Mandarin"],
            "equipment": "Simple robes, meditation beads, bo staff",
            "suggested_freebie_spending": {
                "arete": 4,
                "sphere": 2,
                "merit": 5,
                "abilities": 2,
                "backgrounds": 2,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 5: Cult of Ecstasy DJ
    cultist = CharacterTemplate.objects.get_or_create(
        name="Cult of Ecstasy DJ",
        gameline="mta",
        defaults={
            "character_type": "mage",
            "description": "A rave culture mage who finds enlightenment through music, rhythm, and altered states of consciousness.",
            "source_book": "Mage: The Ascension Revised, p. 90",
            "concept": "DJ/Musician",
            "basic_info": {
                "nature": "FK:Archetype:Bon Vivant",
                "demeanor": "FK:Archetype:Visionary",
                "concept": "DJ",
                "essence": "FK:Essence:Dynamic",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 3,
                "stamina": 3,
                "perception": 4,
                "intelligence": 2,
                "wits": 4,
                "charisma": 4,
                "manipulation": 3,
                "appearance": 3,
            },
            "abilities": {
                "alertness": 3,
                "awareness": 2,
                "empathy": 3,
                "expression": 4,
                "streetwise": 3,
                "subterfuge": 2,
                "crafts": 2,
                "performance": 4,
                "cosmology": 1,
                "medicine": 2,
                "occult": 2,
            },
            "backgrounds": [
                {"name": "Avatar", "rating": 3},
                {"name": "Contacts", "rating": 3},
                {"name": "Resources", "rating": 1},
            ],
            "powers": {
                "time": 2,
                "mind": 1,
                "arete": 1,
            },
            "specialties": [
                "Performance (Electronic Music)",
                "Expression (Lyrical Composition)",
            ],
            "languages": ["English", "Spanish"],
            "equipment": "DJ equipment, synthesizers, laptop, portable speakers",
            "suggested_freebie_spending": {
                "arete": 4,
                "sphere": 2,
                "willpower": 2,
                "abilities": 4,
                "backgrounds": 3,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    print(
        f"✓ Created/updated {CharacterTemplate.objects.filter(gameline='mta').count()} Mage templates"
    )
    return [hacker, hermetic, healer, akashic, cultist]


if __name__ == "__main__":
    populate_mage_templates()
    print("\nMage character templates populated successfully!")
