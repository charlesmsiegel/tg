"""
Character templates for Wraith: The Oblivion
Pre-built character concepts from sourcebooks
"""

from core.models import CharacterTemplate


def populate_wraith_templates():
    """Load Wraith character templates from sourcebooks"""

    # Template 1: Detective Ghost
    detective = CharacterTemplate.objects.get_or_create(
        name="Detective Ghost",
        gameline="wto",
        defaults={
            "character_type": "wraith",
            "description": "A cop who died with an unsolved case, now seeking justice from beyond the grave.",
            "source_book": "Wraith: The Oblivion 20th Anniversary, p. 132",
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
                "alertness": 3,
                "athletics": 1,
                "brawl": 2,
                "empathy": 2,
                "intimidation": 3,
                "streetwise": 2,
                "firearms": 3,
                "investigation": 4,
                "law": 2,
                "occult": 1,
            },
            "backgrounds": [
                {"name": "Contacts", "rating": 2},
                {"name": "Memoriam", "rating": 2},
                {"name": "Status", "rating": 2},
            ],
            "powers": {
                "pathos": 5,
                "corpus": 10,
            },
            "specialties": ["Investigation (Crime Scenes)"],
            "languages": ["English"],
            "equipment": "Ghost of badge, phantom gun",
            "suggested_freebie_spending": {
                "arcanoi": 7,
                "pathos": 2,
                "abilities": 4,
                "backgrounds": 2,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 2: Vengeful Spirit
    vengeful = CharacterTemplate.objects.get_or_create(
        name="Vengeful Spirit",
        gameline="wto",
        defaults={
            "character_type": "wraith",
            "description": "Murdered in life, you seek retribution against those who wronged you.",
            "source_book": "Wraith: The Oblivion 20th Anniversary, p. 133",
            "concept": "Avenger",
            "basic_info": {
                "nature": "FK:Archetype:Bravo",
                "demeanor": "FK:Archetype:Survivor",
                "concept": "Avenger",
            },
            "attributes": {
                "strength": 3,
                "dexterity": 3,
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
                "brawl": 3,
                "dodge": 2,
                "intimidation": 4,
                "streetwise": 3,
                "subterfuge": 2,
                "melee": 2,
                "stealth": 3,
                "investigation": 2,
                "occult": 2,
            },
            "backgrounds": [
                {"name": "Haunt", "rating": 2},
                {"name": "Memoriam", "rating": 2},
                {"name": "Notoriety", "rating": 2},
            ],
            "powers": {
                "pathos": 6,
                "corpus": 10,
            },
            "specialties": ["Intimidation (Threats)"],
            "languages": ["English"],
            "equipment": "Remnants of death scene",
            "suggested_freebie_spending": {
                "arcanoi": 7,
                "pathos": 3,
                "willpower": 3,
                "abilities": 2,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 3: Guardian Spirit
    guardian = CharacterTemplate.objects.get_or_create(
        name="Guardian Spirit",
        gameline="wto",
        defaults={
            "character_type": "wraith",
            "description": "You watch over loved ones from the Shadowlands, protecting them from harm.",
            "source_book": "Wraith: The Oblivion 20th Anniversary, p. 134",
            "concept": "Guardian",
            "basic_info": {
                "nature": "FK:Archetype:Caregiver",
                "demeanor": "FK:Archetype:Protector",
                "concept": "Guardian",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 2,
                "stamina": 3,
                "perception": 4,
                "intelligence": 3,
                "wits": 3,
                "charisma": 3,
                "manipulation": 2,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 3,
                "awareness": 3,
                "empathy": 4,
                "expression": 2,
                "streetwise": 1,
                "subterfuge": 2,
                "meditation": 2,
                "stealth": 2,
                "enigmas": 2,
                "medicine": 2,
                "occult": 3,
            },
            "backgrounds": [
                {"name": "Fetters", "rating": 3},
                {"name": "Memoriam", "rating": 2},
                {"name": "Eidolon", "rating": 1},
            ],
            "powers": {
                "pathos": 5,
                "corpus": 10,
            },
            "specialties": ["Empathy (Family)"],
            "languages": ["English"],
            "equipment": "Family heirlooms (as relics)",
            "suggested_freebie_spending": {
                "arcanoi": 7,
                "backgrounds": 4,
                "willpower": 3,
                "abilities": 1,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 4: Lost Soul
    lost = CharacterTemplate.objects.get_or_create(
        name="Lost Soul",
        gameline="wto",
        defaults={
            "character_type": "wraith",
            "description": "Confused and disoriented, you wander the Shadowlands seeking meaning.",
            "source_book": "Wraith: The Oblivion 20th Anniversary, p. 135",
            "concept": "Lost Soul",
            "basic_info": {
                "nature": "FK:Archetype:Loner",
                "demeanor": "FK:Archetype:Survivor",
                "concept": "Lost Soul",
            },
            "attributes": {
                "strength": 2,
                "dexterity": 3,
                "stamina": 2,
                "perception": 3,
                "intelligence": 2,
                "wits": 4,
                "charisma": 2,
                "manipulation": 2,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 3,
                "athletics": 2,
                "awareness": 2,
                "dodge": 3,
                "streetwise": 2,
                "subterfuge": 3,
                "stealth": 3,
                "survival": 2,
                "enigmas": 3,
                "occult": 2,
            },
            "backgrounds": [
                {"name": "Haunt", "rating": 2},
                {"name": "Fetters", "rating": 2},
                {"name": "Allies", "rating": 2},
            ],
            "powers": {
                "pathos": 4,
                "corpus": 10,
            },
            "specialties": ["Stealth (Shadowlands)"],
            "languages": ["English"],
            "equipment": "Personal effects from life",
            "suggested_freebie_spending": {
                "arcanoi": 7,
                "willpower": 4,
                "abilities": 3,
                "backgrounds": 1,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    # Template 5: Scholar of Death
    scholar = CharacterTemplate.objects.get_or_create(
        name="Scholar of Death",
        gameline="wto",
        defaults={
            "character_type": "wraith",
            "description": "In death as in life, you seek knowledge and understanding of the afterlife.",
            "source_book": "Wraith: The Oblivion 20th Anniversary, p. 136",
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
                "perception": 4,
                "intelligence": 4,
                "wits": 3,
                "charisma": 2,
                "manipulation": 3,
                "appearance": 2,
            },
            "abilities": {
                "alertness": 2,
                "awareness": 3,
                "expression": 2,
                "subterfuge": 2,
                "academics": 4,
                "enigmas": 3,
                "investigation": 3,
                "linguistics": 2,
                "occult": 4,
            },
            "backgrounds": [
                {"name": "Memoriam", "rating": 3},
                {"name": "Mentor", "rating": 2},
                {"name": "Status", "rating": 1},
            ],
            "powers": {
                "pathos": 5,
                "corpus": 10,
            },
            "specialties": ["Occult (Shadowlands Lore)"],
            "languages": ["English", "Latin"],
            "equipment": "Ghostly library, research notes",
            "suggested_freebie_spending": {
                "arcanoi": 7,
                "abilities": 4,
                "backgrounds": 3,
                "willpower": 1,
            },
            "is_official": True,
            "is_public": True,
        },
    )[0]

    print(
        f"✓ Created/updated {CharacterTemplate.objects.filter(gameline='wto').count()} Wraith templates"
    )
    return [detective, vengeful, guardian, lost, scholar]


# Execute when loaded
populate_wraith_templates()
