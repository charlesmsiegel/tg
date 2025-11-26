"""
Seattle Test Chronicle - Vampire Characters

Creates Vampire, Ghoul, and Revenant characters for the test chronicle.
Assigns characters to coteries and sets up relationships.

Run with: python manage.py shell < populate_db/chronicle/test/vampire_characters.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run groups.py first (creates coteries)
- Vampire data must be loaded (clans, sects, disciplines)
"""

from django.contrib.auth.models import User

from characters.models.vampire.clan import VampireClan
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.revenant import Revenant, RevenantFamily
from characters.models.vampire.sect import VampireSect
from characters.models.vampire.vampire import Vampire
from characters.models.vampire.coterie import Coterie
from game.models import Chronicle


# =============================================================================
# VAMPIRE CHARACTER DEFINITIONS
# =============================================================================

VAMPIRES = [
    {
        "username": "xXShadowWolfXx",
        "name": "Marcus 'Shadow' Webb",
        "concept": "Information broker who haunts Seattle's underground",
        "clan": "Nosferatu",
        "sect": "Camarilla",
        "coterie": "The Underground",
        "is_leader": True,
        "generation_rating": 10,
        # Attributes (7/5/3) - Mental primary, Social secondary, Physical tertiary
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 3
        "charisma": 2, "manipulation": 3, "appearance": 0,  # Social: 5 (Nosferatu appearance=0)
        "perception": 4, "intelligence": 3, "wits": 3,  # Mental: 7
        # Abilities (13/9/5) - Knowledges primary, Skills secondary, Talents tertiary
        "alertness": 2, "streetwise": 3,  # Talents: 5
        "computer": 3, "stealth": 3, "larceny": 2, "security": 1,  # Skills: 9
        "investigation": 4, "occult": 2, "politics": 3, "technology": 2, "academics": 2,  # Knowledges: 13
        # Disciplines (3 dots in-clan: Animalism, Obfuscate, Potence)
        "obfuscate": 2, "potence": 1,
        # Virtues (7 total)
        "conscience": 3, "self_control": 3, "courage": 3,  # = 9 (base 3 + 6 allocated)
        # Backgrounds (5 points) - NOTE: Contacts 3 needs NPC definitions
        "contacts": 3, "resources": 2,
        "willpower": 4,
        "humanity": 6,
        "description": "A former hacker who was Embraced after discovering too many secrets. "
                       "His network of mortal informants spans the city's tech industry and criminal underworld.",
    },
    {
        "username": "CrypticMoon",
        "name": "Isabella Santos",
        "concept": "Tremere researcher studying Seattle's ley lines",
        "clan": "Tremere",
        "sect": "Camarilla",
        "coterie": "The Inner Circle",
        "generation_rating": 11,
        # Attributes (7/5/3) - Mental primary, Social secondary, Physical tertiary
        "strength": 1, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 2,  # Social: 5
        "perception": 3, "intelligence": 4, "wits": 3,  # Mental: 7
        # Abilities (13/9/5) - Knowledges primary, Talents secondary, Skills tertiary
        "alertness": 2, "empathy": 2, "expression": 2, "subterfuge": 3,  # Talents: 9
        "etiquette": 2, "melee": 1, "stealth": 2,  # Skills: 5
        "academics": 3, "occult": 4, "investigation": 3, "science": 3,  # Knowledges: 13
        # Disciplines (3 dots in-clan: Auspex, Dominate, Thaumaturgy)
        "auspex": 1, "thaumaturgy": 2,
        # Virtues
        "conscience": 3, "self_control": 4, "courage": 2,
        # Backgrounds - NOTE: Mentor 2 needs NPC definition
        "mentor": 2, "resources": 2, "rituals": 1,
        "willpower": 5,
        "humanity": 7,
        "description": "A scholarly Tremere assigned to Seattle to research the unusual convergence of mystical energies. "
                       "Torn between her House duties and her own magical ambitions.",
    },
    {
        "username": "NightOwl_42",
        "name": "Roland Cross",
        "concept": "Prophetic conspiracy theorist",
        "clan": "Malkavian",
        "sect": "Camarilla",
        "coterie": "The Night Gallery",
        "generation_rating": 11,
        # Attributes (7/5/3) - Mental primary, Social secondary, Physical tertiary
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 2,  # Social: 5
        "perception": 4, "intelligence": 3, "wits": 3,  # Mental: 7
        # Abilities (13/9/5) - Knowledges primary, Talents secondary, Skills tertiary
        "alertness": 3, "awareness": 2, "empathy": 2, "subterfuge": 2,  # Talents: 9
        "computer": 2, "stealth": 2, "investigation": 1,  # Skills: 5
        "academics": 2, "occult": 3, "investigation": 4, "politics": 2, "technology": 2,  # Knowledges: 13
        # Disciplines (3 dots in-clan: Auspex, Dementation, Obfuscate)
        "auspex": 2, "dementation": 1,
        # Virtues
        "conscience": 2, "self_control": 3, "courage": 4,
        # Backgrounds - NOTE: Contacts 2 needs NPC definitions
        "contacts": 2, "resources": 1, "fame": 1, "allies": 1,
        "willpower": 4,
        "humanity": 6,
        "description": "His prophecies manifest as elaborate conspiracy theories that most dismiss as madness. "
                       "Those who listen closely, however, find his 'theories' have an uncomfortable habit of coming true.",
    },
    {
        "username": "pixel_witch",
        "name": "Zoe Kim",
        "concept": "Digital artist obsessed with early internet aesthetics",
        "clan": "Toreador",
        "sect": "Camarilla",
        "coterie": "The Night Gallery",
        "generation_rating": 12,
        # Attributes (7/5/3) - Social primary, Mental secondary, Physical tertiary
        "strength": 1, "dexterity": 3, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 4,  # Social: 7
        "perception": 3, "intelligence": 3, "wits": 2,  # Mental: 5
        # Abilities (13/9/5) - Talents primary, Knowledges secondary, Skills tertiary
        "alertness": 2, "empathy": 3, "expression": 4, "subterfuge": 2, "leadership": 2,  # Talents: 13
        "computer": 3, "etiquette": 2,  # Skills: 5
        "academics": 2, "occult": 2, "technology": 3, "investigation": 2,  # Knowledges: 9
        # Disciplines (3 dots in-clan: Auspex, Celerity, Presence)
        "auspex": 1, "presence": 2,
        # Virtues
        "conscience": 4, "self_control": 2, "courage": 3,
        # Backgrounds - NOTE: Retainers 1 = Trevor Nash (her ghoul)
        "fame": 2, "resources": 2, "retainers": 1,
        "willpower": 3,
        "humanity": 7,
        "description": "Her Embrace froze her obsession with early internet aesthetics forever. "
                       "She curates an underground gallery of art that mortals create but never remember making.",
    },
    {
        "username": "ByteSlayer",
        "name": "Viktor Krueger",
        "concept": "Labor organizer channeling Brujah rage",
        "clan": "Brujah",
        "sect": "Camarilla",
        "coterie": "The Underground",
        "generation_rating": 11,
        # Attributes (7/5/3) - Physical primary, Social secondary, Mental tertiary
        "strength": 4, "dexterity": 3, "stamina": 3,  # Physical: 7
        "charisma": 3, "manipulation": 2, "appearance": 2,  # Social: 5
        "perception": 2, "intelligence": 2, "wits": 2,  # Mental: 3
        # Abilities (13/9/5) - Talents primary, Skills secondary, Knowledges tertiary
        "alertness": 2, "athletics": 2, "brawl": 4, "intimidation": 3, "streetwise": 2,  # Talents: 13
        "drive": 2, "firearms": 2, "melee": 3, "stealth": 2,  # Skills: 9
        "law": 2, "politics": 2, "investigation": 1,  # Knowledges: 5
        # Disciplines (3 dots in-clan: Celerity, Potence, Presence)
        "potence": 2, "celerity": 1,
        # Virtues
        "conscience": 3, "self_control": 2, "courage": 4,
        # Backgrounds - NOTE: Allies 3 = union members and activists
        "allies": 3, "contacts": 2,
        "willpower": 5,
        "humanity": 6,
        "description": "A labor organizer in life who now channels his Brujah rage into protecting Seattle's working class "
                       "from both supernatural and corporate exploitation.",
    },
    {
        "username": "gh0st_in_shell",
        "name": "Diana Cross",
        "concept": "Gangrel wilderness scout uncomfortable in cities",
        "clan": "Gangrel",
        "sect": "Independent",
        "coterie": "The Underground",
        "generation_rating": 10,
        # Attributes (7/5/3) - Physical primary, Mental secondary, Social tertiary
        "strength": 3, "dexterity": 4, "stamina": 3,  # Physical: 7
        "charisma": 2, "manipulation": 1, "appearance": 2,  # Social: 3
        "perception": 3, "intelligence": 2, "wits": 3,  # Mental: 5
        # Abilities (13/9/5) - Skills primary, Talents secondary, Knowledges tertiary
        "alertness": 3, "athletics": 2, "brawl": 2, "intimidation": 2,  # Talents: 9
        "animal_ken": 4, "stealth": 4, "survival": 3, "melee": 2,  # Skills: 13
        "occult": 2, "investigation": 2, "medicine": 1,  # Knowledges: 5
        # Disciplines (3 dots in-clan: Animalism, Fortitude, Protean)
        "animalism": 1, "fortitude": 1, "protean": 1,
        # Virtues
        "conscience": 2, "self_control": 3, "courage": 4,
        # Backgrounds - NOTE: Retainers 1 = Murphy the cat (her ghoul cat)
        "retainers": 1, "allies": 2,
        "willpower": 5,
        "humanity": 5,
        "description": "She roams the wilderness around Seattle, uncomfortable with city life but drawn back "
                       "by a childe she refuses to abandon to Camarilla politics.",
    },
    {
        "username": "Zephyr_Storm",
        "name": "Marcus Antonio",
        "concept": "Ventrue investment banker controlling supernatural economy",
        "clan": "Ventrue",
        "sect": "Camarilla",
        "coterie": "The Inner Circle",
        "is_leader": True,
        "generation_rating": 9,
        # Attributes (7/5/3) - Social primary, Mental secondary, Physical tertiary
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 4, "manipulation": 4, "appearance": 3,  # Social: 7 (+1 from base)
        "perception": 2, "intelligence": 3, "wits": 3,  # Mental: 5
        # Abilities (13/9/5) - Knowledges primary, Talents secondary, Skills tertiary
        "alertness": 2, "empathy": 2, "expression": 2, "leadership": 3,  # Talents: 9
        "drive": 1, "etiquette": 3, "firearms": 1,  # Skills: 5
        "academics": 2, "finance": 4, "law": 3, "politics": 4,  # Knowledges: 13
        # Disciplines (3 dots in-clan: Dominate, Fortitude, Presence)
        "dominate": 2, "presence": 1,
        # Virtues
        "conscience": 2, "self_control": 4, "courage": 3,
        # Backgrounds - NOTE: Retainers 2 = Jennifer Walsh (ghoul) and staff
        "resources": 5, "influence": 3, "status_background": 2, "retainers": 2, "herd": 2,
        "willpower": 6,
        "humanity": 5,
        "description": "Controls Seattle's supernatural economy, trading in boons and blood with the precision "
                       "of a hedge fund manager. The de facto leader of the city's Camarilla presence.",
    },
    {
        "username": "n00b_hunter",
        "name": "Ricardo 'Rico' Mendez",
        "concept": "Brujah neonate figuring out unlife",
        "clan": "Brujah",
        "sect": "Camarilla",
        "coterie": None,  # Unaffiliated - too new
        "generation_rating": 13,
        # Attributes (7/5/3) - Physical primary, Social secondary, Mental tertiary
        "strength": 3, "dexterity": 3, "stamina": 3,  # Physical: 6
        "charisma": 2, "manipulation": 2, "appearance": 3,  # Social: 5
        "perception": 2, "intelligence": 2, "wits": 2,  # Mental: 3
        # Abilities (13/9/5) - Talents primary, Skills secondary, Knowledges tertiary
        "alertness": 2, "athletics": 3, "brawl": 3, "empathy": 2, "streetwise": 3,  # Talents: 13
        "drive": 2, "firearms": 2, "melee": 2, "larceny": 2, "stealth": 1,  # Skills: 9
        "investigation": 2, "computer": 2, "law": 1,  # Knowledges: 5
        # Disciplines (3 dots in-clan: Celerity, Potence, Presence)
        "potence": 1, "celerity": 1, "presence": 1,
        # Virtues
        "conscience": 3, "self_control": 3, "courage": 3,
        # Backgrounds - few, as a neonate
        "contacts": 2, "resources": 1,
        "willpower": 4,
        "humanity": 7,
        "description": "Embraced just six months ago, Rico is still figuring out unlife. "
                       "His sire disappeared, leaving him to navigate Kindred society alone.",
    },
    {
        "username": "ElectricDreamer",
        "name": "Cassandra Vex",
        "concept": "Performance artist channeling prophetic visions",
        "clan": "Malkavian",
        "sect": "Camarilla",
        "coterie": "The Night Gallery",
        "generation_rating": 10,
        # Attributes (7/5/3) - Social primary, Mental secondary, Physical tertiary
        "strength": 1, "dexterity": 3, "stamina": 2,  # Physical: 3
        "charisma": 4, "manipulation": 3, "appearance": 3,  # Social: 7
        "perception": 3, "intelligence": 2, "wits": 3,  # Mental: 5
        # Abilities (13/9/5) - Talents primary, Knowledges secondary, Skills tertiary
        "alertness": 2, "awareness": 3, "empathy": 2, "expression": 4, "subterfuge": 2,  # Talents: 13
        "etiquette": 2, "performance": 3,  # Skills: 5
        "academics": 2, "occult": 3, "investigation": 2, "politics": 2,  # Knowledges: 9
        # Disciplines (3 dots in-clan: Auspex, Dementation, Obfuscate)
        "auspex": 2, "dementation": 1,
        # Virtues
        "conscience": 3, "self_control": 2, "courage": 4,
        # Backgrounds - NOTE: Retainers 1 = Simon Grey (her ghoul), Fame 3 in art circles
        "fame": 3, "resources": 3, "retainers": 1,
        "willpower": 4,
        "humanity": 6,
        "description": "Her 'performance art' channels genuine prophetic visions. "
                       "Galleries pay fortunes for pieces that consistently predict disasters.",
    },
    {
        "username": "void_whisper",
        "name": "Silence",
        "concept": "Lasombra antitribu defector to Camarilla",
        "clan": "Lasombra",
        "sect": "Camarilla",
        "coterie": "The Inner Circle",
        "generation_rating": 9,
        # Attributes (7/5/3) - Mental primary, Physical secondary, Social tertiary
        "strength": 2, "dexterity": 3, "stamina": 3,  # Physical: 5
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 3, "intelligence": 4, "wits": 3,  # Mental: 7
        # Abilities (13/9/5) - Skills primary, Knowledges secondary, Talents tertiary
        "alertness": 2, "athletics": 1, "intimidation": 2,  # Talents: 5
        "melee": 3, "stealth": 4, "etiquette": 2, "firearms": 2, "larceny": 2,  # Skills: 13
        "academics": 2, "investigation": 3, "occult": 2, "politics": 2,  # Knowledges: 9
        # Disciplines (3 dots in-clan: Dominate, Obtenebration, Potence)
        "obtenebration": 2, "dominate": 1,
        # Virtues
        "conscience": 2, "self_control": 4, "courage": 3,
        # Backgrounds
        "resources": 2, "contacts": 2, "alternate_identity": 2,
        "willpower": 6,
        "humanity": 5,
        "description": "A Lasombra antitribu who defected to the Camarilla, her mastery of shadow "
                       "is a constant reminder of the Sabbat she betrayed. Trust is hard to earn in her presence.",
    },
]

# =============================================================================
# GHOUL CHARACTER DEFINITIONS
# =============================================================================

GHOULS = [
    {
        "username": "xXShadowWolfXx",
        "name": "Danny Chen",
        "concept": "Bike messenger unknowingly addicted to vampire blood",
        "domitor_name": None,  # Served by a Toreador not in chronicle
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 4, "stamina": 2,  # Physical: 6
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 4
        "perception": 2, "intelligence": 2, "wits": 2,  # Mental: 3
        # Abilities (11/7/4)
        "alertness": 2, "athletics": 3, "streetwise": 3, "subterfuge": 2, "empathy": 1,  # Talents: 11
        "drive": 3, "stealth": 2, "larceny": 2,  # Skills: 7
        "investigation": 2, "computer": 2,  # Knowledges: 4
        # Disciplines
        "potence": 1,  # All ghouls get 1 Potence
        "celerity": 1,  # Learned from domitor
        # Backgrounds - NOTE: Contacts 2 = delivery clients
        "contacts": 2, "resources": 1,
        "willpower": 3,
        "description": "A bike messenger who ferries packages and messages across the city, "
                       "blissfully unaware his 'vitamins' are blood and his boss is undead.",
    },
    {
        "username": "NightOwl_42",
        "name": "Bethany Moore",
        "concept": "Night-shift ER nurse patching up vampires",
        "domitor_name": "Diana Cross",  # Ghouled by Diana
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 3,  # Physical: 4
        "charisma": 3, "manipulation": 2, "appearance": 2,  # Social: 4
        "perception": 3, "intelligence": 3, "wits": 3,  # Mental: 6
        # Abilities (11/7/4)
        "alertness": 2, "empathy": 3, "expression": 1, "subterfuge": 1,  # Talents: 7
        "drive": 2, "etiquette": 1, "stealth": 1,  # Skills: 4
        "academics": 2, "investigation": 2, "medicine": 4, "science": 3,  # Knowledges: 11
        # Disciplines
        "potence": 1,
        "fortitude": 1,  # From Gangrel domitor
        # Backgrounds - NOTE: Allies 2 = hospital staff
        "allies": 2, "resources": 2, "contacts": 1,
        "willpower": 4,
        "description": "A night-shift ER nurse who patches up vampires and their allies, "
                       "asking no questions about the strange wounds she treats.",
    },
    {
        "username": "pixel_witch",
        "name": "Trevor Nash",
        "concept": "Twitch streamer with supernatural gaming instincts",
        "domitor_name": "Zoe Kim",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 3, "manipulation": 3, "appearance": 2,  # Social: 6
        "perception": 2, "intelligence": 2, "wits": 2,  # Mental: 3
        # Abilities (11/7/4)
        "alertness": 2, "awareness": 2, "empathy": 2, "expression": 3, "subterfuge": 2,  # Talents: 11
        "computer": 3, "performance": 2, "technology": 2,  # Skills: 7
        "academics": 2, "investigation": 2,  # Knowledges: 4
        # Disciplines
        "potence": 1,
        "auspex": 1,  # From Toreador domitor - explains his gaming "instincts"
        # Backgrounds - NOTE: Fame 2 = streaming audience
        "fame": 2, "resources": 2, "contacts": 1,
        "willpower": 3,
        "description": "A Twitch streamer whose 'incredible luck' in horror games comes from "
                       "genuinely sensing the supernatural. His viewers think it's just entertainment.",
    },
    {
        "username": "gh0st_in_shell",
        "name": "Murphy",
        "concept": "Impossibly old and intelligent ghouled cat",
        "domitor_name": "Diana Cross",
        # Note: Murphy is a cat, so attributes are unusual
        # Attributes (6/4/3) - adjusted for animal
        "strength": 1, "dexterity": 4, "stamina": 2,  # Physical: 4
        "charisma": 2, "manipulation": 1, "appearance": 3,  # Social: 3
        "perception": 4, "intelligence": 2, "wits": 3,  # Mental: 6
        # Abilities - limited for animal
        "alertness": 4, "athletics": 3, "brawl": 2,  # 9
        "stealth": 4, "survival": 3,  # 7
        "investigation": 2,  # 2
        # Disciplines
        "potence": 1,
        "fortitude": 1,
        # No backgrounds - is a cat
        "willpower": 4,
        "years_as_ghoul": 40,  # Very old for a cat
        "description": "A grizzled cat ghouled by Diana decades ago, impossibly old and intelligent, "
                       "serving as her eyes and ears in places wolves can't go.",
    },
    {
        "username": "Zephyr_Storm",
        "name": "Jennifer Walsh",
        "concept": "Corporate lawyer handling supernatural contracts",
        "domitor_name": "Marcus Antonio",
        # Attributes (6/4/3)
        "strength": 1, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 4, "appearance": 2,  # Social: 6
        "perception": 2, "intelligence": 3, "wits": 3,  # Mental: 4
        # Abilities (11/7/4)
        "alertness": 2, "empathy": 2, "expression": 2, "subterfuge": 3,  # Talents: 9 - correction needed
        "etiquette": 3, "drive": 1,  # Skills: 4
        "academics": 2, "finance": 3, "law": 4, "politics": 2,  # Knowledges: 11
        # Disciplines
        "potence": 1,
        "dominate": 1,  # From Ventrue domitor
        # Backgrounds - NOTE: Allies 1 = legal network
        "resources": 3, "allies": 1, "contacts": 2,
        "willpower": 5,
        "description": "A corporate lawyer handling the legal needs of Kindred who need "
                       "mortal contracts that bind supernaturally as well as legally.",
    },
    {
        "username": "n00b_hunter",
        "name": "Ashley Barnes",
        "concept": "College student accidentally ghouled at a party",
        "domitor_name": None,  # Accidentally ghouled, unknown domitor
        "is_independent": True,
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 2, "appearance": 3,  # Social: 6
        "perception": 2, "intelligence": 3, "wits": 2,  # Mental: 4
        # Abilities (11/7/4)
        "alertness": 2, "empathy": 3, "expression": 2, "subterfuge": 2, "streetwise": 2,  # Talents: 11
        "computer": 2, "drive": 2, "etiquette": 1, "performance": 2,  # Skills: 7
        "academics": 2, "investigation": 2,  # Knowledges: 4
        # Disciplines
        "potence": 1,
        # Backgrounds
        "resources": 1, "contacts": 1,
        "willpower": 3,
        "description": "A college student accidentally ghouled at a party, now addicted to vitae "
                       "without understanding why she can't stop going back to that weird club.",
    },
    {
        "username": "ElectricDreamer",
        "name": "Simon Grey",
        "concept": "Art gallery owner curating vampire propaganda",
        "domitor_name": "Cassandra Vex",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 3,  # Social: 6
        "perception": 3, "intelligence": 3, "wits": 2,  # Mental: 4
        # Abilities (11/7/4)
        "alertness": 2, "empathy": 2, "expression": 3, "subterfuge": 2, "leadership": 2,  # Talents: 11
        "etiquette": 3, "performance": 2, "drive": 1, "computer": 1,  # Skills: 7
        "academics": 2, "finance": 2,  # Knowledges: 4
        # Disciplines
        "potence": 1,
        "auspex": 1,  # From Malkavian domitor
        # Backgrounds - NOTE: Contacts 2 = art world, Fame 1 = gallery reputation
        "resources": 3, "contacts": 2, "fame": 1, "allies": 1,
        "willpower": 4,
        "description": "An art gallery owner convinced he's discovering the next great artistic movement, "
                       "rather than curating vampire propaganda.",
    },
]

# =============================================================================
# REVENANT CHARACTER DEFINITIONS
# =============================================================================

REVENANTS = [
    {
        "username": "CrypticMoon",
        "name": "Dmitri Zantosa",
        "concept": "Last of his line running an exclusive nightclub",
        "family": "Zantosa",  # Will need to create this family
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 4, "manipulation": 3, "appearance": 3,  # Social: 6
        "perception": 2, "intelligence": 2, "wits": 3,  # Mental: 3
        # Abilities (11/7/4)
        "alertness": 2, "empathy": 3, "expression": 2, "subterfuge": 3, "leadership": 1,  # Talents: 11
        "etiquette": 3, "performance": 2, "drive": 1, "stealth": 1,  # Skills: 7
        "finance": 2, "politics": 2,  # Knowledges: 4
        # Disciplines (Zantosa: Auspex, Presence, Vicissitude)
        "presence": 2, "auspex": 1,
        # Backgrounds - NOTE: Resources 4 = nightclub empire, Contacts 2 = Seattle elite
        "resources": 4, "contacts": 2, "influence": 2,
        "willpower": 4,
        "family_flaw": "Hedonistic tendencies and difficulty refusing pleasures",
        "description": "Last of his family line in the Pacific Northwest, this Zantosa revenant "
                       "runs an exclusive nightclub, using hereditary disciplines to manipulate the city's elite.",
    },
    {
        "username": "ByteSlayer",
        "name": "Natasha Grimaldi",
        "concept": "Finance manager with absolute discretion",
        "family": "Grimaldi",  # Will need to create this family
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 2, "manipulation": 4, "appearance": 2,  # Social: 4
        "perception": 3, "intelligence": 4, "wits": 3,  # Mental: 6
        # Abilities (11/7/4)
        "alertness": 2, "empathy": 2, "subterfuge": 3,  # Talents: 7
        "computer": 2, "etiquette": 2,  # Skills: 4
        "academics": 2, "finance": 4, "law": 3, "politics": 2,  # Knowledges: 11
        # Disciplines (Grimaldi: Celerity, Dominate, Fortitude)
        "dominate": 2, "fortitude": 1,
        # Backgrounds - NOTE: Resources 3 = investment portfolio, Contacts 3 = financial network
        "resources": 3, "contacts": 3, "alternate_identity": 1,
        "willpower": 5,
        "family_flaw": "Cold and calculating; difficulty forming genuine emotional bonds",
        "description": "A Grimaldi revenant managing vampire business interests. Her talent for finance "
                       "and absolute discretion make her invaluable—and dangerous to cross.",
    },
    {
        "username": "void_whisper",
        "name": "Alexei Danislav",
        "concept": "Sabbat escapee using talents for Camarilla",
        "family": "Danislav",  # Will need to create this family
        # Attributes (6/4/3)
        "strength": 3, "dexterity": 3, "stamina": 3,  # Physical: 6
        "charisma": 2, "manipulation": 2, "appearance": 1,  # Social: 3
        "perception": 3, "intelligence": 2, "wits": 3,  # Mental: 4
        # Abilities (11/7/4)
        "alertness": 2, "athletics": 2, "brawl": 2, "intimidation": 2,  # Talents: 8 - balance needed
        "crafts": 4, "melee": 2, "stealth": 3, "survival": 2,  # Skills: 11
        "occult": 3, "medicine": 2,  # Knowledges: 5 - balance
        # Disciplines (Danislav: Fortitude, Potence, Vicissitude)
        "fortitude": 2, "vicissitude": 1,
        # Backgrounds - NOTE: Alternate Identity 2 = escaped Sabbat identity
        "resources": 2, "alternate_identity": 2, "contacts": 1,
        "willpower": 5,
        "family_flaw": "Morbid fascination with death and corpses",
        "description": "A Danislav revenant who escaped the Sabbat and fled to Seattle, using his talents "
                       "for corpse preservation to serve Camarilla interests while hiding from his family.",
    },
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_chronicle_and_user(username):
    """Get the Seattle Test Chronicle and a specific user."""
    chronicle = Chronicle.objects.filter(name="Seattle Test Chronicle").first()
    if not chronicle:
        print("ERROR: Seattle Test Chronicle not found. Run base.py first.")
        return None, None

    user = User.objects.filter(username=username).first()
    if not user:
        print(f"ERROR: User {username} not found. Run base.py first.")
        return chronicle, None

    return chronicle, user


def get_clan(clan_name):
    """Get a vampire clan by name."""
    clan = VampireClan.objects.filter(name=clan_name).first()
    if not clan:
        print(f"WARNING: Clan {clan_name} not found.")
    return clan


def get_sect(sect_name):
    """Get a vampire sect by name."""
    sect = VampireSect.objects.filter(name=sect_name).first()
    if not sect:
        print(f"WARNING: Sect {sect_name} not found.")
    return sect


def get_coterie(coterie_name, chronicle):
    """Get a coterie by name."""
    coterie = Coterie.objects.filter(name=coterie_name, chronicle=chronicle).first()
    if not coterie:
        print(f"WARNING: Coterie {coterie_name} not found.")
    return coterie


def get_or_create_revenant_family(family_name):
    """Get or create a revenant family."""
    from characters.models.vampire.discipline import Discipline

    # Family definitions with their disciplines
    FAMILIES = {
        "Zantosa": {
            "description": "Hedonistic servants of the Tzimisce, the Zantosa revel in pleasure and sensation.",
            "weakness": "Hedonistic tendencies; must roll Self-Control to resist opportunities for pleasure.",
            "disciplines": ["Auspex", "Presence", "Vicissitude"],
        },
        "Grimaldi": {
            "description": "Business-minded servants who handle Sabbat mortal affairs and finances.",
            "weakness": "Cold and calculating; difficulty forming genuine emotional connections.",
            "disciplines": ["Celerity", "Dominate", "Fortitude"],
        },
        "Danislav": {
            "description": "Morticians and corpse handlers who prepare bodies for Tzimisce fleshcrafting.",
            "weakness": "Morbid fascination with death; must spend Willpower to avoid inappropriate behavior around corpses.",
            "disciplines": ["Fortitude", "Potence", "Vicissitude"],
        },
    }

    if family_name not in FAMILIES:
        print(f"WARNING: Unknown revenant family: {family_name}")
        return None

    family_data = FAMILIES[family_name]
    family, created = RevenantFamily.objects.get_or_create(
        name=family_name,
        defaults={
            "description": family_data["description"],
            "weakness": family_data["weakness"],
        }
    )

    if created:
        print(f"Created revenant family: {family_name}")
        # Add disciplines
        for disc_name in family_data["disciplines"]:
            disc = Discipline.objects.filter(name=disc_name).first()
            if disc:
                family.disciplines.add(disc)

    return family


def apply_character_stats(character, data):
    """Apply stats from data dict to character."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina",
                 "charisma", "manipulation", "appearance",
                 "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(character, attr, data[attr])

    # Abilities (VtM-specific)
    abilities = [
        "alertness", "athletics", "brawl", "empathy", "expression",
        "intimidation", "streetwise", "subterfuge", "awareness", "leadership",
        "crafts", "drive", "etiquette", "firearms", "melee", "stealth",
        "animal_ken", "larceny", "performance", "survival",
        "academics", "computer", "investigation", "medicine", "science",
        "finance", "law", "occult", "politics", "technology",
    ]
    for ability in abilities:
        if ability in data:
            setattr(character, ability, data[ability])

    # Backgrounds
    backgrounds = [
        "allies", "alternate_identity", "contacts", "domain", "fame",
        "generation", "herd", "influence", "mentor", "resources",
        "retainers", "rituals", "status_background",
    ]
    for bg in backgrounds:
        if bg in data:
            setattr(character, bg, data[bg])

    # Willpower
    if "willpower" in data:
        character.willpower = data["willpower"]
        character.temporary_willpower = data["willpower"]


def apply_vampire_stats(vampire, data):
    """Apply vampire-specific stats."""
    # Disciplines
    disciplines = [
        "animalism", "auspex", "celerity", "chimerstry", "dementation",
        "dominate", "fortitude", "necromancy", "obfuscate", "obtenebration",
        "potence", "presence", "protean", "quietus", "serpentis",
        "thaumaturgy", "vicissitude",
    ]
    for disc in disciplines:
        if disc in data:
            setattr(vampire, disc, data[disc])

    # Virtues
    for virtue in ["conscience", "self_control", "courage", "conviction", "instinct"]:
        if virtue in data:
            setattr(vampire, virtue, data[virtue])

    # Morality
    if "humanity" in data:
        vampire.humanity = data["humanity"]
    if "path_rating" in data:
        vampire.path_rating = data["path_rating"]

    # Generation
    if "generation_rating" in data:
        vampire.generation_rating = data["generation_rating"]


def apply_ghoul_stats(ghoul, data):
    """Apply ghoul-specific stats."""
    # Disciplines ghouls can have
    for disc in ["potence", "celerity", "fortitude", "auspex", "dominate", "obfuscate", "presence"]:
        if disc in data:
            setattr(ghoul, disc, data[disc])

    if "years_as_ghoul" in data:
        ghoul.years_as_ghoul = data["years_as_ghoul"]

    if "is_independent" in data:
        ghoul.is_independent = data["is_independent"]


def apply_revenant_stats(revenant, data):
    """Apply revenant-specific stats."""
    # Disciplines revenants can have
    for disc in ["potence", "celerity", "fortitude", "auspex", "dominate",
                 "obfuscate", "presence", "animalism", "necromancy", "vicissitude"]:
        if disc in data:
            setattr(revenant, disc, data[disc])

    if "family_flaw" in data:
        revenant.family_flaw = data["family_flaw"]


# =============================================================================
# MAIN CREATION FUNCTIONS
# =============================================================================

def create_vampires(chronicle):
    """Create all vampire characters."""
    print("\n--- Creating Vampires ---")
    created_vampires = {}

    for vdata in VAMPIRES:
        user = User.objects.filter(username=vdata["username"]).first()
        if not user:
            print(f"  ERROR: User {vdata['username']} not found")
            continue

        vampire, created = Vampire.objects.get_or_create(
            name=vdata["name"],
            owner=user,
            chronicle=chronicle,
            defaults={
                "concept": vdata["concept"],
                "description": vdata.get("description", ""),
                "npc": False,
            }
        )

        if created:
            # Set clan and sect
            vampire.clan = get_clan(vdata["clan"])
            vampire.sect = get_sect(vdata["sect"])

            # Apply stats
            apply_character_stats(vampire, vdata)
            apply_vampire_stats(vampire, vdata)

            vampire.save()
            print(f"  Created vampire: {vdata['name']} ({vdata['clan']})")
        else:
            print(f"  Vampire already exists: {vdata['name']}")

        created_vampires[vdata["name"]] = vampire

        # Handle coterie membership
        if vdata.get("coterie"):
            coterie = get_coterie(vdata["coterie"], chronicle)
            if coterie:
                coterie.members.add(vampire)
                if vdata.get("is_leader"):
                    coterie.leader = vampire
                    coterie.save()
                    print(f"    -> Set as leader of {vdata['coterie']}")

    return created_vampires


def create_ghouls(chronicle, vampires):
    """Create all ghoul characters."""
    print("\n--- Creating Ghouls ---")

    for gdata in GHOULS:
        user = User.objects.filter(username=gdata["username"]).first()
        if not user:
            print(f"  ERROR: User {gdata['username']} not found")
            continue

        ghoul, created = Ghoul.objects.get_or_create(
            name=gdata["name"],
            owner=user,
            chronicle=chronicle,
            defaults={
                "concept": gdata["concept"],
                "description": gdata.get("description", ""),
                "npc": False,
            }
        )

        if created:
            # Set domitor if specified
            if gdata.get("domitor_name") and gdata["domitor_name"] in vampires:
                ghoul.domitor = vampires[gdata["domitor_name"]]

            # Apply stats
            apply_character_stats(ghoul, gdata)
            apply_ghoul_stats(ghoul, gdata)

            ghoul.save()
            print(f"  Created ghoul: {gdata['name']}")
            if ghoul.domitor:
                print(f"    -> Domitor: {ghoul.domitor.name}")
        else:
            print(f"  Ghoul already exists: {gdata['name']}")


def create_revenants(chronicle):
    """Create all revenant characters."""
    print("\n--- Creating Revenants ---")

    for rdata in REVENANTS:
        user = User.objects.filter(username=rdata["username"]).first()
        if not user:
            print(f"  ERROR: User {rdata['username']} not found")
            continue

        # Get or create family
        family = get_or_create_revenant_family(rdata["family"])

        revenant, created = Revenant.objects.get_or_create(
            name=rdata["name"],
            owner=user,
            chronicle=chronicle,
            defaults={
                "concept": rdata["concept"],
                "description": rdata.get("description", ""),
                "npc": False,
            }
        )

        if created:
            revenant.family = family

            # Apply stats
            apply_character_stats(revenant, rdata)
            apply_revenant_stats(revenant, rdata)

            revenant.save()
            print(f"  Created revenant: {rdata['name']} ({rdata['family']})")
        else:
            print(f"  Revenant already exists: {rdata['name']}")


def main():
    """Run the full vampire character setup."""
    print("=" * 60)
    print("Seattle Test Chronicle - Vampire Character Setup")
    print("=" * 60)

    chronicle = Chronicle.objects.filter(name="Seattle Test Chronicle").first()
    if not chronicle:
        print("ERROR: Seattle Test Chronicle not found. Run base.py first.")
        return

    # Create characters
    vampires = create_vampires(chronicle)
    create_ghouls(chronicle, vampires)
    create_revenants(chronicle)

    # Summary
    print("\n" + "=" * 60)
    print("Vampire character setup complete!")
    print(f"Vampires: {Vampire.objects.filter(chronicle=chronicle).count()}")
    print(f"Ghouls: {Ghoul.objects.filter(chronicle=chronicle).count()}")
    print(f"Revenants: {Revenant.objects.filter(chronicle=chronicle).count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    # When run via `python manage.py shell < script.py`
    main()
