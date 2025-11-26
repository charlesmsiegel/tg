"""
Seattle Test Chronicle - Mage Characters

Creates Mage, Sorcerer, and Companion characters for the test chronicle.
Assigns characters to cabals and sets up relationships.

Run with: python manage.py shell < populate_db/chronicle/test/mage_characters.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run groups.py first (creates cabals)
- Mage data must be loaded (factions, spheres, etc.)
"""

from django.contrib.auth.models import User

from characters.models.mage.cabal import Cabal
from characters.models.mage.companion import Companion
from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage
from characters.models.mage.sorcerer import Sorcerer
from game.models import Chronicle


# =============================================================================
# MAGE CHARACTER DEFINITIONS
# =============================================================================

MAGES = [
    {
        "username": "xXShadowWolfXx",
        "name": "Victor Reyes",
        "concept": "Reality hacker who believes the world is a simulation",
        "affiliation": "Traditions",
        "faction": "Virtual Adepts",
        "cabal": "The Digital Underground",
        "essence": "Dynamic",
        "arete": 3,
        # Attributes (7/5/3) - Mental primary, Physical secondary, Social tertiary
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 3, "intelligence": 4, "wits": 3,  # Mental: 7
        # Abilities (13/9/5) - Knowledges primary, Skills secondary, Talents tertiary
        "alertness": 2, "awareness": 1, "subterfuge": 2,  # Talents: 5
        "computer": 4, "technology": 3, "stealth": 2,  # Skills: 9
        "academics": 2, "investigation": 3, "science": 4, "occult": 2, "enigmas": 2,  # Knowledges: 13
        # Spheres (6 dots total, affinity=correspondence)
        "correspondence": 3, "forces": 2, "mind": 1,
        # Backgrounds - NOTE: Library 2 = Digital archives, Node 1 = server farm
        "resources": 2, "library": 2, "node": 1,
        "willpower": 5,
        "quintessence": 3,
        "description": "A Virtual Adept who believes reality is a simulation and he's found the cheat codes. "
                       "Works as a white-hat hacker by day, reality hacker by night.",
    },
    {
        "username": "CrypticMoon",
        "name": "Dr. Eleanor Vance",
        "concept": "Forensic pathologist who guides souls at death",
        "affiliation": "Traditions",
        "faction": "Euthanatos",
        "cabal": "The Invisible College",
        "is_leader": True,
        "essence": "Primordial",
        "arete": 4,
        # Attributes (7/5/3) - Mental primary, Social secondary, Physical tertiary
        "strength": 1, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 2,  # Social: 5
        "perception": 4, "intelligence": 4, "wits": 3,  # Mental: 8 (rank 4 mage bonus)
        # Abilities (13/9/5) - Knowledges primary, Talents secondary, Skills tertiary
        "alertness": 2, "awareness": 3, "empathy": 3, "subterfuge": 1,  # Talents: 9
        "investigation": 2, "medicine": 2, "stealth": 1,  # Skills: 5
        "academics": 2, "investigation": 3, "medicine": 4, "occult": 3, "science": 3,  # Knowledges: 15 - bonus
        # Spheres (9 dots for Arete 4)
        "entropy": 4, "life": 3, "spirit": 2,
        # Backgrounds - NOTE: Mentor 2 = Euthanatos elder, Allies 2 = hospital staff
        "allies": 2, "mentor": 2, "resources": 3,
        "willpower": 6,
        "quintessence": 5,
        "description": "A Euthanatos forensic pathologist who sees death as transformation. "
                       "She guides souls at Seattle's hospitals while investigating unnatural deaths.",
    },
    {
        "username": "NightOwl_42",
        "name": "Samantha 'Sam' Torres",
        "concept": "Sleep researcher walking the Umbra through dreams",
        "affiliation": "Traditions",
        "faction": "Dreamspeakers",
        "cabal": "The Invisible College",
        "essence": "Primordial",
        "arete": 3,
        # Attributes (7/5/3) - Mental primary, Social secondary, Physical tertiary
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 2,  # Social: 5
        "perception": 4, "intelligence": 3, "wits": 3,  # Mental: 7
        # Abilities (13/9/5) - Knowledges primary, Talents secondary, Skills tertiary
        "alertness": 2, "awareness": 3, "empathy": 3, "expression": 1,  # Talents: 9
        "crafts": 1, "etiquette": 2, "meditation": 2,  # Skills: 5
        "academics": 3, "enigmas": 3, "medicine": 2, "occult": 3, "science": 2,  # Knowledges: 13
        # Spheres (6 dots)
        "spirit": 3, "mind": 2, "life": 1,
        # Backgrounds - NOTE: Mentor 1 = tribal elder, Allies 1 = research team
        "mentor": 1, "allies": 1, "resources": 2, "contacts": 1,
        "willpower": 5,
        "quintessence": 4,
        "description": "A Dreamspeaker who works as a sleep researcher at UW, walking the Umbra through dreams "
                       "and treating night terrors that are more real than patients know.",
    },
    {
        "username": "pixel_witch",
        "name": "Priya Sharma",
        "concept": "Information freedom fighter against Technocracy",
        "affiliation": "Traditions",
        "faction": "Virtual Adepts",
        "cabal": "The Digital Underground",
        "essence": "Dynamic",
        "arete": 3,
        # Attributes (7/5/3) - Mental primary, Social secondary, Physical tertiary
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 4, "appearance": 2,  # Social: 6
        "perception": 3, "intelligence": 4, "wits": 2,  # Mental: 6
        # Abilities (13/9/5) - Knowledges primary, Talents secondary, Skills tertiary
        "alertness": 2, "awareness": 1, "expression": 3, "subterfuge": 3,  # Talents: 9
        "computer": 3, "technology": 2,  # Skills: 5
        "academics": 2, "investigation": 4, "occult": 2, "politics": 2, "science": 3,  # Knowledges: 13
        # Spheres (6 dots)
        "correspondence": 2, "entropy": 2, "mind": 2,
        # Backgrounds - NOTE: Contacts 3 = hacker network, Allies 2 = fellow activists
        "contacts": 3, "allies": 2, "resources": 2,
        "willpower": 5,
        "quintessence": 2,
        "description": "A Virtual Adept whose Avatar manifests as a helpful AI assistant. "
                       "She fights the Technocracy's control of information by ensuring truth spreads faster than they can suppress it.",
    },
    {
        "username": "ByteSlayer",
        "name": "Dr. Hassan Al-Rashid",
        "concept": "Imam who sees no conflict between faith and magic",
        "affiliation": "Traditions",
        "faction": "Celestial Chorus",
        "cabal": "The Invisible College",
        "essence": "Pattern",
        "arete": 3,
        # Attributes (7/5/3) - Social primary, Mental secondary, Physical tertiary
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 4, "manipulation": 2, "appearance": 3,  # Social: 6
        "perception": 3, "intelligence": 3, "wits": 3,  # Mental: 6
        # Abilities (13/9/5) - Talents primary, Knowledges secondary, Skills tertiary
        "alertness": 2, "awareness": 2, "empathy": 4, "expression": 3, "leadership": 2,  # Talents: 13
        "etiquette": 2, "meditation": 2, "performance": 1,  # Skills: 5
        "academics": 3, "law": 2, "occult": 3, "theology": 1,  # Knowledges: 9
        # Spheres (6 dots)
        "prime": 3, "spirit": 2, "mind": 1,
        # Backgrounds - NOTE: Allies 3 = congregation, Sanctum 2 = mosque
        "allies": 3, "sanctum": 2, "resources": 1, "influence": 1,
        "willpower": 6,
        "quintessence": 5,
        "description": "A Celestial Chorister and imam who sees no conflict between faith and magic. "
                       "His mosque is a sanctuary for those fleeing supernatural persecution.",
    },
    {
        "username": "gh0st_in_shell",
        "name": "Ghost",
        "concept": "Virtual Adept who exists between worlds",
        "affiliation": "Traditions",
        "faction": "Virtual Adepts",
        "cabal": "The Digital Underground",
        "essence": "Questing",
        "arete": 3,
        # Attributes (7/5/3) - Mental primary, Physical secondary, Social tertiary
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 2, "manipulation": 2, "appearance": 1,  # Social: 3 (exists partially elsewhere)
        "perception": 4, "intelligence": 4, "wits": 3,  # Mental: 8
        # Abilities (13/9/5) - Knowledges primary, Skills secondary, Talents tertiary
        "alertness": 2, "awareness": 2, "subterfuge": 1,  # Talents: 5
        "computer": 4, "stealth": 3, "technology": 2,  # Skills: 9
        "academics": 2, "enigmas": 3, "investigation": 3, "occult": 3, "science": 2,  # Knowledges: 13
        # Spheres (6 dots)
        "correspondence": 3, "spirit": 2, "mind": 1,
        # Backgrounds - NOTE: Avatar 3 = strong but unusual avatar, Arcane 2 = hard to perceive
        "avatar": 3, "arcane": 2, "resources": 1,
        "willpower": 5,
        "quintessence": 6,
        "description": "A Virtual Adept who died during a deep dive into the Digital Web and somehow came back... different. "
                       "She exists partially in both worlds, uncertain which is more real.",
    },
    {
        "username": "Zephyr_Storm",
        "name": "Aurora Sinclair",
        "concept": "Fate reader profiting from Seattle's markets",
        "affiliation": "Traditions",
        "faction": "Order of Hermes",
        "subfaction": "House Fortunae",
        "cabal": "The Fortunate Few",
        "essence": "Questing",
        "arete": 4,
        # Attributes (7/5/3) - Mental primary, Social secondary, Physical tertiary
        "strength": 1, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 4, "appearance": 2,  # Social: 6
        "perception": 4, "intelligence": 4, "wits": 3,  # Mental: 8
        # Abilities (13/9/5) - Knowledges primary, Talents secondary, Skills tertiary
        "alertness": 2, "awareness": 3, "empathy": 2, "subterfuge": 2,  # Talents: 9
        "etiquette": 3, "drive": 1, "computer": 1,  # Skills: 5
        "academics": 3, "enigmas": 3, "finance": 4, "law": 2, "occult": 3,  # Knowledges: 15
        # Spheres (9 dots for Arete 4)
        "entropy": 4, "mind": 3, "correspondence": 2,
        # Backgrounds - NOTE: Resources 5 = vast wealth from predictions
        "resources": 5, "chantry": 2, "contacts": 2, "influence": 2,
        "willpower": 6,
        "quintessence": 6,
        "description": "A hermetic Mage of House Fortunae reading fate in Seattle's stock markets. "
                       "Her investments always pay off, making her invaluable and suspicious to the Technocracy.",
    },
    {
        "username": "n00b_hunter",
        "name": "Tyler Wright",
        "concept": "Newly Awakened Orphan still figuring things out",
        "affiliation": "Traditions",  # Seeking, not committed
        "faction": None,  # Orphan - no tradition yet
        "cabal": None,  # Unaffiliated - too new
        "essence": "Dynamic",
        "arete": 1,
        # Attributes (7/5/3) - Physical primary, Mental secondary, Social tertiary
        "strength": 3, "dexterity": 3, "stamina": 2,  # Physical: 5
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 3, "intelligence": 3, "wits": 3,  # Mental: 6
        # Abilities (13/9/5) - Skills primary, Talents secondary, Knowledges tertiary
        "alertness": 2, "athletics": 2, "brawl": 2, "awareness": 1, "expression": 1, "streetwise": 1,  # Talents: 9
        "computer": 2, "drive": 2, "stealth": 2, "crafts": 2, "firearms": 1, "survival": 2, "technology": 2,  # Skills: 13
        "academics": 2, "investigation": 2, "science": 1,  # Knowledges: 5
        # Spheres (2 dots for Arete 1)
        "forces": 1, "matter": 1,
        # Backgrounds - minimal
        "contacts": 1, "resources": 1,
        "willpower": 4,
        "quintessence": 1,
        "description": "A newly Awakened Orphan trying to figure out what just happened to him. "
                       "Reality broke around him last week, and no one's explained the rules yet.",
    },
    {
        "username": "ElectricDreamer",
        "name": "Iris Quantum",
        "concept": "DJ whose music induces genuine altered states",
        "affiliation": "Traditions",
        "faction": "Cult of Ecstasy",
        "cabal": "The Invisible College",
        "essence": "Dynamic",
        "arete": 3,
        # Attributes (7/5/3) - Social primary, Mental secondary, Physical tertiary
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 4, "manipulation": 3, "appearance": 3,  # Social: 7
        "perception": 3, "intelligence": 2, "wits": 3,  # Mental: 5
        # Abilities (13/9/5) - Talents primary, Skills secondary, Knowledges tertiary
        "alertness": 2, "awareness": 3, "empathy": 3, "expression": 4, "subterfuge": 1,  # Talents: 13
        "computer": 2, "performance": 4, "technology": 3,  # Skills: 9
        "academics": 1, "enigmas": 2, "occult": 2,  # Knowledges: 5
        # Spheres (6 dots)
        "time": 2, "mind": 2, "forces": 2,
        # Backgrounds - NOTE: Fame 2 = DJ reputation, Contacts 2 = music scene
        "fame": 2, "contacts": 2, "resources": 2, "allies": 1,
        "willpower": 4,
        "quintessence": 3,
        "description": "A Cult of Ecstasy DJ whose music induces genuine altered states. "
                       "Her raves are religious experiences that occasionally attract Paradox.",
    },
    {
        "username": "void_whisper",
        "name": "Zero",
        "concept": "Euthanatos who walked too close to the edge",
        "affiliation": "Traditions",
        "faction": "Euthanatos",
        "cabal": "The Threshold",
        "essence": "Primordial",
        "arete": 4,
        # Attributes (7/5/3) - Mental primary, Physical secondary, Social tertiary
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 4, "intelligence": 4, "wits": 3,  # Mental: 8
        # Abilities (13/9/5) - Knowledges primary, Skills secondary, Talents tertiary
        "alertness": 2, "awareness": 2, "intimidation": 1,  # Talents: 5
        "melee": 2, "stealth": 4, "meditation": 3,  # Skills: 9
        "academics": 2, "enigmas": 4, "investigation": 3, "occult": 4,  # Knowledges: 13
        # Spheres (9 dots for Arete 4)
        "entropy": 4, "spirit": 3, "life": 2,
        # Backgrounds - NOTE: Arcane 3 = deliberately obscured existence
        "arcane": 3, "mentor": 1, "destiny": 2,
        "willpower": 7,
        "quintessence": 4,
        "description": "A Euthanatos who went too far down the path of entropy and nearly became a Nephandi. "
                       "Now she walks the edge, helping others avoid her mistakes while atoning for her own.",
    },
]

# =============================================================================
# SORCERER CHARACTER DEFINITIONS
# =============================================================================

SORCERERS = [
    {
        "username": "xXShadowWolfXx",
        "name": "Min-Ji Park",
        "concept": "Korean folk magic practitioner running herbal shop",
        # Attributes (6/4/3)
        "strength": 1, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 2,  # Social: 5
        "perception": 3, "intelligence": 3, "wits": 3,  # Mental: 6
        # Abilities (11/7/4)
        "alertness": 2, "awareness": 2, "empathy": 3, "expression": 2,  # Talents: 9 - adjust
        "crafts": 3, "etiquette": 2, "meditation": 2,  # Skills: 7
        "academics": 1, "medicine": 2, "occult": 3,  # Knowledges: 6 - adjust
        # Note: Linear magic paths would need to be set separately
        # Backgrounds - NOTE: Contacts 2 = International District community
        "contacts": 2, "resources": 2, "allies": 1,
        "willpower": 4,
        "description": "A hedge mage practicing Korean folk magic, running an herbal shop in the International District. "
                       "Her minor enchantments help the community while keeping her under the Technocracy's radar.",
    },
    {
        "username": "NightOwl_42",
        "name": "Howard Chen",
        "concept": "Feng shui master aligning mystical energies",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 2, "manipulation": 3, "appearance": 2,  # Social: 4
        "perception": 4, "intelligence": 3, "wits": 3,  # Mental: 7
        # Abilities (11/7/4)
        "alertness": 2, "awareness": 3, "empathy": 2,  # Talents: 7
        "crafts": 3, "etiquette": 2, "drive": 1, "stealth": 1,  # Skills: 7
        "academics": 2, "enigmas": 3, "occult": 3,  # Knowledges: 8
        # Backgrounds - NOTE: Contacts 3 = wealthy clients, Resources 3 = successful business
        "contacts": 3, "resources": 3, "allies": 1,
        "willpower": 5,
        "description": "A feng shui master whose 'interior decorating' business actually involves aligning mystical energies, "
                       "helping clients avoid supernatural attention for a modest fee.",
    },
    {
        "username": "ByteSlayer",
        "name": "Grandmother Liu",
        "concept": "Ancient practitioner of Chinese alchemy",
        # Attributes (6/4/3)
        "strength": 1, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 2, "appearance": 2,  # Social: 4
        "perception": 4, "intelligence": 4, "wits": 2,  # Mental: 7
        # Abilities (11/7/4)
        "alertness": 2, "awareness": 2, "empathy": 3, "expression": 1,  # Talents: 8
        "crafts": 4, "medicine": 3,  # Skills: 7
        "academics": 2, "enigmas": 2, "occult": 4, "science": 2,  # Knowledges: 10
        # Backgrounds - NOTE: Allies 2 = loyal customers and students
        "allies": 2, "resources": 2, "contacts": 1,
        "willpower": 6,
        "description": "An ancient practitioner of Chinese alchemy running an herbal medicine shop. "
                       "Her tonics and elixirs work minor miracles for those who know to ask.",
    },
    {
        "username": "gh0st_in_shell",
        "name": "Nathan Graves",
        "concept": "Medium hiding real supernatural encounters",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 3,  # Social: 6
        "perception": 3, "intelligence": 3, "wits": 2,  # Mental: 5
        # Abilities (11/7/4)
        "alertness": 2, "awareness": 3, "empathy": 2, "expression": 3, "subterfuge": 2,  # Talents: 12 - adjust
        "computer": 2, "performance": 3, "technology": 2,  # Skills: 7
        "investigation": 2, "occult": 3,  # Knowledges: 5
        # Backgrounds - NOTE: Fame 2 = YouTube channel, Contacts 2 = paranormal community
        "fame": 2, "contacts": 2, "resources": 2,
        "willpower": 4,
        "description": "A medium and spirit-talker running a 'paranormal investigation' YouTube channel. "
                       "His debunking videos carefully hide the truly supernatural while exposing frauds.",
    },
    {
        "username": "n00b_hunter",
        "name": "Emma Chen",
        "concept": "College student who found a real grimoire",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 2, "appearance": 3,  # Social: 5
        "perception": 3, "intelligence": 3, "wits": 2,  # Mental: 5
        # Abilities (11/7/4)
        "alertness": 2, "awareness": 2, "empathy": 2, "expression": 2, "subterfuge": 1,  # Talents: 9
        "computer": 2, "drive": 1, "stealth": 2,  # Skills: 5
        "academics": 3, "investigation": 2, "occult": 2,  # Knowledges: 7
        # Backgrounds
        "resources": 1, "contacts": 1,
        "willpower": 3,
        "description": "A college student who stumbled onto real magic through a grimoire found in a used bookstore. "
                       "Her hedge magic is unstable, powerful, and attracting attention.",
    },
    {
        "username": "void_whisper",
        "name": "Helena Marsh",
        "concept": "Necromancer speaking with the dead for a price",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 2, "manipulation": 3, "appearance": 2,  # Social: 4
        "perception": 4, "intelligence": 3, "wits": 3,  # Mental: 7
        # Abilities (11/7/4)
        "alertness": 2, "awareness": 3, "empathy": 2, "intimidation": 2,  # Talents: 9
        "meditation": 3, "stealth": 2,  # Skills: 5
        "academics": 2, "enigmas": 2, "investigation": 2, "occult": 4,  # Knowledges: 10
        # Backgrounds - NOTE: Contacts 2 = grieving families, allies 1 = other occultists
        "contacts": 2, "resources": 2, "allies": 1,
        "willpower": 5,
        "description": "A practitioner of necromancy who speaks with the dead for a price. "
                       "Her services are sought by grieving families and vengeful ghosts alike.",
    },
]

# =============================================================================
# COMPANION CHARACTER DEFINITIONS
# =============================================================================

COMPANIONS = [
    {
        "username": "CrypticMoon",
        "name": "Father Miguel Torres",
        "concept": "Priest providing sanctuary without practicing magic",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 4, "manipulation": 2, "appearance": 2,  # Social: 5
        "perception": 3, "intelligence": 3, "wits": 2,  # Mental: 5
        # Abilities (11/7/4)
        "alertness": 2, "awareness": 2, "empathy": 4, "expression": 3, "leadership": 2,  # Talents: 13 - adjust
        "etiquette": 2, "drive": 1, "meditation": 2,  # Skills: 5
        "academics": 3, "law": 1, "occult": 2, "theology": 2,  # Knowledges: 8
        # Backgrounds - NOTE: Allies 3 = congregation, Influence 2 = church connections
        "allies": 3, "influence": 2, "resources": 1,
        "willpower": 6,
        "description": "A priest who knows magic exists and aids the local Chantry, "
                       "providing sanctuary and counsel without practicing the Arts himself.",
    },
    {
        "username": "pixel_witch",
        "name": "James Liu",
        "concept": "Tech billionaire funding mage operations",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 4, "appearance": 2,  # Social: 6
        "perception": 3, "intelligence": 3, "wits": 2,  # Mental: 5
        # Abilities (11/7/4)
        "alertness": 2, "empathy": 2, "expression": 2, "leadership": 3, "subterfuge": 2,  # Talents: 11
        "computer": 2, "etiquette": 3, "drive": 1,  # Skills: 6
        "academics": 2, "finance": 4, "law": 2, "technology": 2,  # Knowledges: 10
        # Backgrounds - NOTE: Resources 5 = billionaire, Contacts 3 = tech industry
        "resources": 5, "contacts": 3, "influence": 3, "allies": 1,
        "willpower": 5,
        "description": "A disillusioned tech billionaire who funds mage operations after his daughter was 'cured' by Progenitors. "
                       "He provides resources without understanding the war he's financing.",
    },
    {
        "username": "Zephyr_Storm",
        "name": "Theodore Barnes",
        "concept": "Retired occult professor supporting the Chantry",
        # Attributes (6/4/3)
        "strength": 1, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 2, "appearance": 2,  # Social: 4
        "perception": 3, "intelligence": 4, "wits": 2,  # Mental: 6
        # Abilities (11/7/4)
        "alertness": 2, "awareness": 2, "empathy": 2, "expression": 3,  # Talents: 9
        "computer": 1, "etiquette": 2, "drive": 1,  # Skills: 4
        "academics": 4, "enigmas": 2, "investigation": 2, "occult": 4, "science": 1,  # Knowledges: 13
        # Backgrounds - NOTE: Contacts 2 = academic network, Library 3 = personal occult collection
        "contacts": 2, "library": 3, "resources": 2, "allies": 1,
        "willpower": 5,
        "description": "A retired professor of occult studies who provides research support to the local Chantry, "
                       "knowing just enough to be useful but not enough to be a threat.",
    },
    {
        "username": "ElectricDreamer",
        "name": "Dr. Marcus Webb",
        "concept": "Psychiatrist helping mages integrate mystical experiences",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 2,  # Social: 5
        "perception": 4, "intelligence": 3, "wits": 2,  # Mental: 6
        # Abilities (11/7/4)
        "alertness": 2, "awareness": 2, "empathy": 4, "expression": 2, "subterfuge": 1,  # Talents: 11
        "etiquette": 2, "drive": 1, "meditation": 2,  # Skills: 5
        "academics": 3, "investigation": 2, "medicine": 3, "science": 2,  # Knowledges: 10
        # Backgrounds - NOTE: Contacts 2 = medical community, Allies 2 = patients he's helped
        "contacts": 2, "allies": 2, "resources": 3,
        "willpower": 5,
        "description": "A psychiatrist who helps Mages integrate mystical experiences without losing touch with consensus reality. "
                       "He's seen too much to disbelieve.",
    },
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_faction(affiliation_name, faction_name=None, subfaction_name=None):
    """Get mage faction hierarchy."""
    affiliation = MageFaction.objects.filter(name=affiliation_name, parent=None).first()
    if not affiliation:
        print(f"WARNING: Affiliation {affiliation_name} not found.")
        return None, None, None

    faction = None
    if faction_name:
        faction = MageFaction.objects.filter(name=faction_name, parent=affiliation).first()
        if not faction:
            print(f"WARNING: Faction {faction_name} not found under {affiliation_name}.")

    subfaction = None
    if subfaction_name and faction:
        subfaction = MageFaction.objects.filter(name=subfaction_name, parent=faction).first()
        if not subfaction:
            print(f"WARNING: Subfaction {subfaction_name} not found under {faction_name}.")

    return affiliation, faction, subfaction


def get_cabal(cabal_name, chronicle):
    """Get a cabal by name."""
    cabal = Cabal.objects.filter(name=cabal_name, chronicle=chronicle).first()
    if not cabal:
        print(f"WARNING: Cabal {cabal_name} not found.")
    return cabal


def apply_mage_stats(character, data):
    """Apply stats from data dict to character."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina",
                 "charisma", "manipulation", "appearance",
                 "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(character, attr, data[attr])

    # Abilities (MtA-specific)
    abilities = [
        "alertness", "athletics", "brawl", "empathy", "expression",
        "intimidation", "streetwise", "subterfuge", "awareness", "leadership",
        "crafts", "drive", "etiquette", "firearms", "melee", "stealth",
        "animal_ken", "meditation", "performance", "survival", "technology",
        "academics", "computer", "investigation", "medicine", "science",
        "cosmology", "enigmas", "law", "occult",
    ]
    for ability in abilities:
        if ability in data:
            setattr(character, ability, data[ability])

    # Willpower
    if "willpower" in data:
        character.willpower = data["willpower"]
        character.temporary_willpower = data["willpower"]


def apply_awakened_stats(mage, data):
    """Apply awakened mage-specific stats."""
    # Arete
    if "arete" in data:
        mage.arete = data["arete"]

    # Essence
    if "essence" in data:
        mage.essence = data["essence"]

    # Spheres
    spheres = ["correspondence", "time", "spirit", "mind", "entropy", "prime", "forces", "matter", "life"]
    for sphere in spheres:
        if sphere in data:
            setattr(mage, sphere, data[sphere])

    # Quintessence
    if "quintessence" in data:
        mage.quintessence = data["quintessence"]


# =============================================================================
# MAIN CREATION FUNCTIONS
# =============================================================================

def create_mages(chronicle):
    """Create all mage characters."""
    print("\n--- Creating Mages ---")
    created_mages = {}

    for mdata in MAGES:
        user = User.objects.filter(username=mdata["username"]).first()
        if not user:
            print(f"  ERROR: User {mdata['username']} not found")
            continue

        mage, created = Mage.objects.get_or_create(
            name=mdata["name"],
            owner=user,
            chronicle=chronicle,
            defaults={
                "concept": mdata["concept"],
                "description": mdata.get("description", ""),
                "npc": False,
            }
        )

        if created:
            # Set faction hierarchy
            affiliation, faction, subfaction = get_faction(
                mdata.get("affiliation"),
                mdata.get("faction"),
                mdata.get("subfaction")
            )
            mage.affiliation = affiliation
            mage.faction = faction
            mage.subfaction = subfaction

            # Apply stats
            apply_mage_stats(mage, mdata)
            apply_awakened_stats(mage, mdata)

            mage.save()
            faction_str = mdata.get("faction", "Orphan") or "Orphan"
            print(f"  Created mage: {mdata['name']} ({faction_str})")
        else:
            print(f"  Mage already exists: {mdata['name']}")

        created_mages[mdata["name"]] = mage

        # Handle cabal membership
        if mdata.get("cabal"):
            cabal = get_cabal(mdata["cabal"], chronicle)
            if cabal:
                cabal.members.add(mage)
                if mdata.get("is_leader"):
                    cabal.leader = mage
                    cabal.save()
                    print(f"    -> Set as leader of {mdata['cabal']}")

    return created_mages


def create_sorcerers(chronicle):
    """Create all sorcerer characters."""
    print("\n--- Creating Sorcerers ---")

    for sdata in SORCERERS:
        user = User.objects.filter(username=sdata["username"]).first()
        if not user:
            print(f"  ERROR: User {sdata['username']} not found")
            continue

        sorcerer, created = Sorcerer.objects.get_or_create(
            name=sdata["name"],
            owner=user,
            chronicle=chronicle,
            defaults={
                "concept": sdata["concept"],
                "description": sdata.get("description", ""),
                "npc": False,
            }
        )

        if created:
            # Apply stats
            apply_mage_stats(sorcerer, sdata)

            sorcerer.save()
            print(f"  Created sorcerer: {sdata['name']}")
        else:
            print(f"  Sorcerer already exists: {sdata['name']}")


def create_companions(chronicle):
    """Create all companion characters."""
    print("\n--- Creating Companions ---")

    for cdata in COMPANIONS:
        user = User.objects.filter(username=cdata["username"]).first()
        if not user:
            print(f"  ERROR: User {cdata['username']} not found")
            continue

        companion, created = Companion.objects.get_or_create(
            name=cdata["name"],
            owner=user,
            chronicle=chronicle,
            defaults={
                "concept": cdata["concept"],
                "description": cdata.get("description", ""),
                "npc": False,
            }
        )

        if created:
            # Apply stats
            apply_mage_stats(companion, cdata)

            companion.save()
            print(f"  Created companion: {cdata['name']}")
        else:
            print(f"  Companion already exists: {cdata['name']}")


def main():
    """Run the full mage character setup."""
    print("=" * 60)
    print("Seattle Test Chronicle - Mage Character Setup")
    print("=" * 60)

    chronicle = Chronicle.objects.filter(name="Seattle Test Chronicle").first()
    if not chronicle:
        print("ERROR: Seattle Test Chronicle not found. Run base.py first.")
        return

    # Create characters
    mages = create_mages(chronicle)
    create_sorcerers(chronicle)
    create_companions(chronicle)

    # Summary
    print("\n" + "=" * 60)
    print("Mage character setup complete!")
    print(f"Mages: {Mage.objects.filter(chronicle=chronicle).count()}")
    print(f"Sorcerers: {Sorcerer.objects.filter(chronicle=chronicle).count()}")
    print(f"Companions: {Companion.objects.filter(chronicle=chronicle).count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    # When run via `python manage.py shell < script.py`
    main()
