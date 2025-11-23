"""
Faction-specific character templates for World of Darkness
Templates tailored to specific clans, tribes, and traditions
"""

from core.models import CharacterTemplate

# ========================================
# VAMPIRE: CLAN-SPECIFIC TEMPLATES
# ========================================

# Brujah Brawler
brujah_brawler = CharacterTemplate.objects.get_or_create(
    name="Brujah Brawler",
    gameline="vtm",
    defaults={
        "character_type": "vampire",
        "faction": "Brujah",
        "concept": "Street Fighter",
        "description": "A passionate rebel who fights for their beliefs with fists and fury. Embraces the Brujah clan's revolutionary spirit and their talent for violence.",
        "basic_info": {
            "nature": "FK:Archetype:Rebel",
            "demeanor": "FK:Archetype:Bravo",
        },
        "attributes": {
            "strength": 4,
            "dexterity": 3,
            "stamina": 3,
            "perception": 2,
            "intelligence": 2,
            "wits": 3,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 3,
            "athletics": 2,
            "brawl": 4,
            "empathy": 1,
            "intimidation": 3,
            "streetwise": 3,
            "subterfuge": 1,
            "drive": 2,
            "melee": 2,
            "academics": 1,
            "politics": 2,
        },
        "backgrounds": [
            {"name": "Contacts", "rating": 2},
            {"name": "Herd", "rating": 1},
            {"name": "Allies", "rating": 2},
        ],
        "powers": {
            "celerity": 2,
            "potence": 2,
            "presence": 1,
        },
        "specialties": ["Brawl (Haymakers)", "Intimidation (Threats)"],
        "languages": ["English"],
        "equipment": "Leather jacket, brass knuckles, motorcycle",
        "suggested_freebie_spending": {
            "disciplines": 7,
            "attributes": 2,
            "abilities": 3,
            "willpower": 3,
        },
        "is_official": True,
        "is_public": True,
    },
)[0].add_source("Vampire: The Masquerade Revised", 95)

# Tremere Scholar
tremere_scholar = CharacterTemplate.objects.get_or_create(
    name="Tremere Scholar",
    gameline="vtm",
    defaults={
        "character_type": "vampire",
        "faction": "Tremere",
        "concept": "Occult Researcher",
        "description": "A studious blood mage who seeks forbidden knowledge and masters Thaumaturgy. Embodies the Tremere clan's dedication to magical study and hierarchical structure.",
        "basic_info": {
            "nature": "FK:Archetype:Architect",
            "demeanor": "FK:Archetype:Pedagogue",
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
            "empathy": 2,
            "subterfuge": 2,
            "investigation": 3,
            "academics": 4,
            "medicine": 2,
            "occult": 4,
        },
        "backgrounds": [
            {"name": "Resources", "rating": 2},
            {"name": "Mentor", "rating": 3},
        ],
        "powers": {
            "auspex": 2,
            "dominate": 1,
            "thaumaturgy": 2,
        },
        "specialties": ["Occult (Blood Magic)", "Academics (Ancient Languages)"],
        "languages": ["English", "Latin"],
        "equipment": "Ritual dagger, grimoire, alchemical supplies",
        "suggested_freebie_spending": {
            "disciplines": 7,
            "backgrounds": 3,
            "abilities": 3,
            "willpower": 2,
        },
        "is_official": True,
        "is_public": True,
    },
)[0].add_source("Guide to the Camarilla", 101)

# Toreador Artist
toreador_artist = CharacterTemplate.objects.get_or_create(
    name="Toreador Artist",
    gameline="vtm",
    defaults={
        "character_type": "vampire",
        "faction": "Toreador",
        "concept": "Painter",
        "description": "A passionate artist who finds beauty in the night. Represents the Toreador clan's appreciation for art and sensual experience.",
        "basic_info": {
            "nature": "FK:Archetype:Artist",
            "demeanor": "FK:Archetype:Gallant",
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
            "appearance": 4,
        },
        "abilities": {
            "alertness": 2,
            "empathy": 3,
            "expression": 4,
            "subterfuge": 2,
            "crafts": 3,
            "etiquette": 3,
            "performance": 2,
            "academics": 2,
        },
        "backgrounds": [
            {"name": "Resources", "rating": 3},
            {"name": "Fame", "rating": 2},
        ],
        "powers": {
            "auspex": 2,
            "celerity": 1,
            "presence": 2,
        },
        "specialties": ["Expression (Painting)", "Empathy (Emotions)"],
        "languages": ["English", "French"],
        "equipment": "Art supplies, portfolio, gallery keys",
        "suggested_freebie_spending": {
            "disciplines": 5,
            "backgrounds": 4,
            "abilities": 3,
            "willpower": 3,
        },
        "is_official": True,
        "is_public": True,
    },
)[0].add_source("Vampire: The Masquerade Revised", 92)

# ========================================
# WEREWOLF: TRIBE-SPECIFIC TEMPLATES
# ========================================

# Glass Walker Hacker
glass_walker_hacker = CharacterTemplate.objects.get_or_create(
    name="Glass Walker Hacker",
    gameline="wta",
    defaults={
        "character_type": "werewolf",
        "faction": "Glass Walkers",
        "concept": "Tech-Savvy Urbanite",
        "description": "A modern werewolf who embraces technology and city life. Embodies the Glass Walkers' adaptation to urban environments.",
        "basic_info": {
            "nature": "FK:Archetype:Innovator",
            "demeanor": "FK:Archetype:Architect",
        },
        "attributes": {
            "strength": 3,
            "dexterity": 3,
            "stamina": 3,
            "perception": 3,
            "intelligence": 4,
            "wits": 4,
            "charisma": 2,
            "manipulation": 3,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 3,
            "athletics": 2,
            "brawl": 2,
            "streetwise": 3,
            "computer": 4,
            "drive": 2,
            "firearms": 3,
            "technology": 3,
            "enigmas": 2,
            "science": 3,
        },
        "backgrounds": [
            {"name": "Contacts", "rating": 3},
            {"name": "Resources", "rating": 3},
            {"name": "Fetish", "rating": 1},
        ],
        "powers": {
            "persuasion": 2,
            "control_simple_machine": 1,
        },
        "specialties": ["Computer (Hacking)", "Technology (Robotics)"],
        "languages": ["English"],
        "equipment": "Laptop, smartphone, modified devices",
        "suggested_freebie_spending": {
            "gifts": 5,
            "backgrounds": 4,
            "abilities": 3,
            "willpower": 3,
        },
        "is_official": True,
        "is_public": True,
    },
)[0].add_source("Werewolf: The Apocalypse Revised", 112)

# Red Talon Predator
red_talon_predator = CharacterTemplate.objects.get_or_create(
    name="Red Talon Predator",
    gameline="wta",
    defaults={
        "character_type": "werewolf",
        "faction": "Red Talons",
        "concept": "Wild Hunter",
        "description": "A lupus-born warrior who despises human civilization. Represents the Red Talons' dedication to the wilderness and hatred of humanity.",
        "basic_info": {
            "nature": "FK:Archetype:Predator",
            "demeanor": "FK:Archetype:Survivor",
        },
        "attributes": {
            "strength": 4,
            "dexterity": 4,
            "stamina": 4,
            "perception": 4,
            "intelligence": 2,
            "wits": 4,
            "charisma": 2,
            "manipulation": 1,
            "appearance": 3,
        },
        "abilities": {
            "alertness": 4,
            "athletics": 3,
            "brawl": 4,
            "dodge": 3,
            "primal_urge": 4,
            "survival": 4,
            "animal_ken": 3,
        },
        "backgrounds": [
            {"name": "Pure Breed", "rating": 3},
            {"name": "Totem", "rating": 2},
        ],
        "powers": {
            "razor_claws": 2,
            "leap_of_the_kangaroo": 1,
        },
        "specialties": ["Brawl (Claws)", "Survival (Tracking)"],
        "languages": [],
        "equipment": "None - relies on natural weapons",
        "suggested_freebie_spending": {
            "gifts": 7,
            "attributes": 3,
            "abilities": 3,
            "willpower": 2,
        },
        "is_official": True,
        "is_public": True,
    },
)[0].add_source("Werewolf: The Apocalypse Revised", 119)

# ========================================
# MAGE: TRADITION-SPECIFIC TEMPLATES
# ========================================

# Verbena Herbalist
verbena_herbalist = CharacterTemplate.objects.get_or_create(
    name="Verbena Herbalist",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "faction": "Verbena",
        "concept": "Healer",
        "description": "A practitioner of primal magic who works with herbs, blood, and the cycles of nature. Embodies Verbena traditions of life magic and natural power.",
        "basic_info": {
            "nature": "FK:Archetype:Caregiver",
            "demeanor": "FK:Archetype:Survivor",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 3,
            "stamina": 3,
            "perception": 3,
            "intelligence": 3,
            "wits": 3,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 3,
        },
        "abilities": {
            "awareness": 3,
            "empathy": 3,
            "expression": 2,
            "athletics": 2,
            "meditation": 2,
            "survival": 3,
            "crafts": 2,
            "cosmology": 2,
            "medicine": 3,
            "occult": 3,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 3},
            {"name": "Library", "rating": 2},
        ],
        "powers": {
            "life": 3,
            "prime": 1,
            "spirit": 1,
        },
        "specialties": ["Medicine (Herbalism)", "Occult (Blood Magic)"],
        "languages": ["English"],
        "equipment": "Herb pouch, ritual knife, grimoire",
        "suggested_freebie_spending": {
            "arete": 4,
            "willpower": 3,
            "backgrounds": 3,
            "spheres": 5,
        },
        "is_official": True,
        "is_public": True,
    },
)[0].add_source("Mage: The Ascension Revised", 78)

# Order of Hermes Magus
order_hermes_magus = CharacterTemplate.objects.get_or_create(
    name="Order of Hermes Magus",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "faction": "Order of Hermes",
        "concept": "Ceremonial Magician",
        "description": "A formally trained wizard who practices Hermetic magic with precision and power. Represents the Order's dedication to structured magical study.",
        "basic_info": {
            "nature": "FK:Archetype:Architect",
            "demeanor": "FK:Archetype:Pedagogue",
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
            "awareness": 2,
            "expression": 2,
            "meditation": 3,
            "research": 3,
            "etiquette": 2,
            "academics": 4,
            "cosmology": 3,
            "enigmas": 3,
            "occult": 4,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 3},
            {"name": "Library", "rating": 3},
            {"name": "Mentor", "rating": 2},
        ],
        "powers": {
            "forces": 3,
            "prime": 2,
        },
        "specialties": ["Occult (Hermetic Theory)", "Academics (Latin)"],
        "languages": ["English", "Latin", "Enochian"],
        "equipment": "Wand, ceremonial robes, grimoire",
        "suggested_freebie_spending": {
            "arete": 4,
            "willpower": 2,
            "backgrounds": 4,
            "spheres": 5,
        },
        "is_official": True,
        "is_public": True,
    },
)[0].add_source("Mage: The Ascension Revised", 65)

# Akashic Brotherhood Monk
akashic_monk = CharacterTemplate.objects.get_or_create(
    name="Akashic Brotherhood Monk",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "faction": "Akashic Brotherhood",
        "concept": "Martial Artist",
        "description": "A disciplined warrior who channels magic through physical perfection and mental clarity. Embodies the Brotherhood's path of Do.",
        "basic_info": {
            "nature": "FK:Archetype:Pedagogue",
            "demeanor": "FK:Archetype:Loner",
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
            "appearance": 3,
        },
        "abilities": {
            "alertness": 3,
            "athletics": 3,
            "awareness": 4,
            "brawl": 4,
            "dodge": 3,
            "meditation": 4,
            "cosmology": 2,
            "medicine": 2,
            "occult": 3,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 3},
            {"name": "Mentor", "rating": 2},
        ],
        "powers": {
            "mind": 3,
            "life": 2,
        },
        "specialties": ["Brawl (Martial Arts)", "Meditation (Mindfulness)"],
        "languages": ["English", "Sanskrit"],
        "equipment": "Simple robes, meditation beads",
        "suggested_freebie_spending": {
            "arete": 4,
            "willpower": 4,
            "abilities": 3,
            "spheres": 4,
        },
        "is_official": True,
        "is_public": True,
    },
)[0].add_source("Mage: The Ascension Revised", 60)

print("Faction-specific templates created successfully!")
print(f"- {brujah_brawler.name} (Brujah)")
print(f"- {tremere_scholar.name} (Tremere)")
print(f"- {toreador_artist.name} (Toreador)")
print(f"- {glass_walker_hacker.name} (Glass Walkers)")
print(f"- {red_talon_predator.name} (Red Talons)")
print(f"- {verbena_herbalist.name} (Verbena)")
print(f"- {order_hermes_magus.name} (Order of Hermes)")
print(f"- {akashic_monk.name} (Akashic Brotherhood)")
