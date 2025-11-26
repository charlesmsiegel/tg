"""
Seattle Test Chronicle - Werewolf Characters

Creates Werewolf, Kinfolk, and Fera characters for the test chronicle.
Assigns characters to packs and sets up relationships.

Run with: python manage.py shell < populate_db/chronicle/test/werewolf_characters.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run groups.py first (creates packs)
- Werewolf data must be loaded (tribes, gifts, rites)
"""

from django.contrib.auth.models import User

from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.tribe import Tribe
from characters.models.werewolf.pack import Pack
from game.models import Chronicle


# =============================================================================
# WEREWOLF CHARACTER DEFINITIONS
# =============================================================================

WEREWOLVES = [
    {
        "username": "xXShadowWolfXx",
        "name": "Runs-Through-Fire",
        "concept": "Former firefighter turned urban protector",
        "tribe": "Glass Walkers",
        "auspice": "ahroun",
        "breed": "homid",
        "pack": "Silicon Fangs",
        "is_alpha": True,
        "rank": 2,
        # Attributes (7/5/3) - Physical primary, Mental secondary, Social tertiary
        "strength": 4, "dexterity": 3, "stamina": 3,  # Physical: 7
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 3, "intelligence": 2, "wits": 3,  # Mental: 5
        # Abilities (13/9/5) - Talents primary, Skills secondary, Knowledges tertiary
        "alertness": 3, "athletics": 3, "brawl": 3, "intimidation": 2, "primal_urge": 2,  # Talents: 13
        "drive": 2, "firearms": 2, "melee": 2, "stealth": 2, "survival": 1,  # Skills: 9
        "computer": 2, "investigation": 2, "technology": 1,  # Knowledges: 5
        # Rage/Gnosis based on auspice (Ahroun=5) and breed (Homid=1)
        "rage": 5, "gnosis": 1,
        # Renown (Ahroun rank 2: glory 4, honor 1, wisdom 1)
        "glory": 4, "honor": 1, "wisdom": 1,
        # Backgrounds - NOTE: Kinfolk 2 needs NPC definitions, Contacts 2 = fire department
        "kinfolk_rating": 2, "contacts": 2, "resources": 2,
        "willpower": 4,
        "first_change": "Trapped in a burning building, the fire seemed to call to him. "
                       "He burst through the flames, transformed, and saved three children before collapsing.",
        "age_of_first_change": 26,
        "description": "A homid Ahroun of the Glass Walkers who underwent his First Change while trapped "
                       "in a burning building. Now protects the city's Kinfolk from supernatural threats.",
    },
    {
        "username": "CrypticMoon",
        "name": "Whispers-to-Stars",
        "concept": "Spiritual guide communing with feared spirits",
        "tribe": "Uktena",
        "auspice": "theurge",
        "breed": "lupus",
        "pack": "The Wardens",
        "rank": 2,
        # Attributes (7/5/3) - Mental primary, Physical secondary, Social tertiary
        "strength": 2, "dexterity": 3, "stamina": 3,  # Physical: 5
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 4, "intelligence": 3, "wits": 3,  # Mental: 7
        # Abilities (13/9/5) - Knowledges primary, Talents secondary, Skills tertiary
        "alertness": 2, "athletics": 2, "brawl": 1, "empathy": 2, "primal_urge": 3,  # Talents: 10 - adjust
        "animal_ken": 2, "stealth": 3, "survival": 3,  # Skills: 8 - adjust
        "enigmas": 3, "occult": 4, "rituals": 3,  # Knowledges: 10 - adjust
        # Rage/Gnosis based on auspice (Theurge=2) and breed (Lupus=5)
        "rage": 2, "gnosis": 5,
        # Renown (Theurge rank 2: glory 1, honor 0, wisdom 5)
        "glory": 1, "honor": 0, "wisdom": 5,
        # Backgrounds - NOTE: Ancestors 2 = spirit memories, Mentor 1 = elder theurge
        "ancestors": 2, "mentor": 1, "pure_breed": 2,
        "willpower": 4,
        "first_change": "Born in the Cascades, she always heard the whispers of spirits. "
                       "Her First Change came during a vision quest, when the spirits demanded she join them.",
        "age_of_first_change": 2,  # Lupus, changed young
        "description": "A lupus Theurge of the Uktena, born in the Cascades. She serves as the pack's "
                       "spiritual guide, communing with spirits others fear to approach.",
    },
    {
        "username": "NightOwl_42",
        "name": "Breaks-the-Chain",
        "concept": "Metis trickster surviving on cunning",
        "tribe": "Bone Gnawers",
        "auspice": "ragabash",
        "breed": "metis",
        "pack": "The Forgotten",
        "rank": 1,
        # Attributes (7/5/3) - Mental primary, Social secondary, Physical tertiary
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 3, "manipulation": 3, "appearance": 1,  # Social: 4 (metis often low appearance)
        "perception": 3, "intelligence": 3, "wits": 4,  # Mental: 7
        # Abilities (13/9/5) - Talents primary, Skills secondary, Knowledges tertiary
        "alertness": 2, "athletics": 2, "empathy": 2, "expression": 2, "streetwise": 4, "subterfuge": 3,  # Talents: 15 - adjust
        "larceny": 3, "stealth": 3, "survival": 2,  # Skills: 8
        "investigation": 2, "law": 1,  # Knowledges: 3
        # Rage/Gnosis based on auspice (Ragabash=1) and breed (Metis=3)
        "rage": 1, "gnosis": 3,
        # Renown (Ragabash rank 1: total 3, distributed)
        "glory": 1, "honor": 1, "wisdom": 1,
        # Backgrounds
        "contacts": 3, "allies": 1,
        "willpower": 4,
        "first_change": "Born in Seattle's homeless camps, he never knew a time before the Rage. "
                       "His metis deformity—a twisted spine—marks him as an outcast among outcasts.",
        "age_of_first_change": 0,  # Metis, born changed
        "description": "A metis Ragabash of the Bone Gnawers, born in Seattle's homeless camps. "
                       "Uses humor and cunning to survive where strength fails.",
    },
    {
        "username": "pixel_witch",
        "name": "Silicon Dreams",
        "concept": "Digital chronicler of Garou history",
        "tribe": "Glass Walkers",
        "auspice": "galliard",
        "breed": "homid",
        "pack": "Silicon Fangs",
        "rank": 2,
        # Attributes (7/5/3) - Social primary, Mental secondary, Physical tertiary
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 4, "manipulation": 3, "appearance": 3,  # Social: 7
        "perception": 3, "intelligence": 3, "wits": 2,  # Mental: 5
        # Abilities (13/9/5) - Talents primary, Knowledges secondary, Skills tertiary
        "alertness": 2, "empathy": 2, "expression": 4, "leadership": 2, "subterfuge": 3,  # Talents: 13
        "computer": 3, "academics": 2, "investigation": 2, "occult": 2,  # Knowledges: 9
        "performance": 2, "stealth": 2, "technology": 1,  # Skills: 5
        # Rage/Gnosis based on auspice (Galliard=4) and breed (Homid=1)
        "rage": 4, "gnosis": 1,
        # Renown (Galliard rank 2: glory 4, honor 0, wisdom 2)
        "glory": 4, "honor": 0, "wisdom": 2,
        # Backgrounds - NOTE: Fame 1 = urban legend blog
        "contacts": 2, "resources": 2, "fame": 1,
        "willpower": 4,
        "first_change": "Her First Change happened while streaming, fortunately with a 30-second delay. "
                       "She deleted the footage and learned the importance of the Veil that night.",
        "age_of_first_change": 22,
        "description": "A homid Galliard of the Glass Walkers documenting Garou history through encrypted files "
                       "and hidden websites. Her 'urban legend' blog has a very specific audience.",
    },
    {
        "username": "ByteSlayer",
        "name": "Cuts-Through-Steel",
        "concept": "Former Army Ranger fighting the real war",
        "tribe": "Get of Fenris",
        "auspice": "ahroun",
        "breed": "homid",
        "pack": "The Wardens",
        "is_alpha": True,
        "rank": 3,
        # Attributes (7/5/3) - Physical primary, Mental secondary, Social tertiary
        "strength": 4, "dexterity": 4, "stamina": 3,  # Physical: 8 (rank 3)
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 3, "intelligence": 2, "wits": 3,  # Mental: 5
        # Abilities (13/9/5) - Skills primary, Talents secondary, Knowledges tertiary
        "alertness": 3, "athletics": 3, "brawl": 3, "intimidation": 2,  # Talents: 11
        "firearms": 4, "melee": 4, "stealth": 3, "survival": 3,  # Skills: 14
        "investigation": 2, "medicine": 2, "technology": 1,  # Knowledges: 5
        # Rage/Gnosis based on auspice (Ahroun=5) and breed (Homid=1)
        "rage": 6, "gnosis": 2,  # Increased through play
        # Renown (Ahroun rank 3: glory 6, honor 3, wisdom 1)
        "glory": 6, "honor": 3, "wisdom": 1,
        # Backgrounds - NOTE: Fetish 2 = klaive, Kinfolk 2 = Mike Donovan
        "fetish": 2, "kinfolk_rating": 2, "resources": 1,
        "willpower": 5,
        "first_change": "During a firefight in Afghanistan, he saw his squad die. The Rage took him, "
                       "and when he came to, the enemy was dead. All of them. He found a war worth fighting.",
        "age_of_first_change": 24,
        "description": "A former Army Ranger who found a war worth fighting. His pack strikes at "
                       "Pentex operations throughout the region.",
    },
    {
        "username": "gh0st_in_shell",
        "name": "Stalks-the-Pattern",
        "concept": "Investigator of spiritual wounds",
        "tribe": "Silent Striders",
        "auspice": "ragabash",
        "breed": "lupus",
        "pack": "Silicon Fangs",
        "rank": 2,
        # Attributes (7/5/3) - Physical primary, Mental secondary, Social tertiary
        "strength": 2, "dexterity": 4, "stamina": 3,  # Physical: 6
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 4, "intelligence": 3, "wits": 3,  # Mental: 7
        # Abilities (13/9/5) - Skills primary, Talents secondary, Knowledges tertiary
        "alertness": 3, "athletics": 3, "primal_urge": 2, "subterfuge": 2,  # Talents: 10
        "animal_ken": 2, "stealth": 4, "survival": 4, "investigation": 2,  # Skills: 12
        "enigmas": 2, "occult": 3,  # Knowledges: 5
        # Rage/Gnosis based on auspice (Ragabash=1) and breed (Lupus=5)
        "rage": 2, "gnosis": 5,
        # Renown (Ragabash rank 2: total 7)
        "glory": 2, "honor": 2, "wisdom": 3,
        # Backgrounds
        "ancestors": 1, "pure_breed": 1, "resources": 1,
        "willpower": 4,
        "first_change": "The spirits called her from Egypt, whispering of dark patterns in the Pacific Northwest. "
                       "She followed the call and found Seattle waiting.",
        "age_of_first_change": 3,
        "description": "A lupus Ragabash of the Silent Striders investigating the spiritual wounds "
                       "left by Seattle's dark history while evading the ancestors' curse.",
    },
    {
        "username": "Zephyr_Storm",
        "name": "Chases-the-Wind",
        "concept": "Culture keeper bridging traditional and modern ways",
        "tribe": "Wendigo",
        "auspice": "galliard",
        "breed": "homid",
        "pack": "The Wardens",
        "rank": 2,
        # Attributes (7/5/3) - Social primary, Mental secondary, Physical tertiary
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 4, "manipulation": 3, "appearance": 2,  # Social: 6
        "perception": 3, "intelligence": 3, "wits": 3,  # Mental: 6
        # Abilities (13/9/5) - Talents primary, Knowledges secondary, Skills tertiary
        "alertness": 2, "athletics": 2, "empathy": 3, "expression": 4, "leadership": 2,  # Talents: 13
        "occult": 3, "rituals": 3, "law": 2, "academics": 1,  # Knowledges: 9
        "performance": 3, "survival": 2,  # Skills: 5
        # Rage/Gnosis based on auspice (Galliard=4) and breed (Homid=1)
        "rage": 4, "gnosis": 2,
        # Renown (Galliard rank 2: glory 4, honor 0, wisdom 2)
        "glory": 4, "honor": 0, "wisdom": 2,
        # Backgrounds - NOTE: Ancestors 3 = strong connection to tribal history
        "ancestors": 3, "pure_breed": 2, "kinfolk_rating": 1,
        "willpower": 5,
        "first_change": "During a protest to protect sacred lands, the ancestors called to him. "
                       "His First Change scattered the police and saved the demonstration.",
        "age_of_first_change": 19,
        "description": "A homid Galliard of the Wendigo fighting to preserve First Nations culture "
                       "while bridging the gap between traditional ways and modern activism.",
    },
    {
        "username": "n00b_hunter",
        "name": "First-Kill",
        "concept": "Red Talon cub struggling with civilization",
        "tribe": "Red Talons",
        "auspice": "ahroun",
        "breed": "homid",  # Unusual for Red Talon - source of tension
        "pack": "The Forgotten",
        "rank": 1,
        # Attributes (7/5/3) - Physical primary, Social secondary, Mental tertiary
        "strength": 3, "dexterity": 3, "stamina": 3,  # Physical: 6
        "charisma": 2, "manipulation": 1, "appearance": 3,  # Social: 4
        "perception": 2, "intelligence": 2, "wits": 2,  # Mental: 3
        # Abilities (13/9/5) - Talents primary, Skills secondary, Knowledges tertiary
        "alertness": 3, "athletics": 3, "brawl": 4, "intimidation": 2, "primal_urge": 2,  # Talents: 14
        "animal_ken": 2, "stealth": 3, "survival": 3,  # Skills: 8
        "occult": 1,  # Knowledges: 1
        # Rage/Gnosis based on auspice (Ahroun=5) and breed (Homid=1)
        "rage": 5, "gnosis": 1,
        # Renown (Ahroun rank 1: glory 2, honor 1, wisdom 0)
        "glory": 2, "honor": 1, "wisdom": 0,
        # Backgrounds - minimal
        "pure_breed": 1,
        "willpower": 4,
        "first_change": "The rage came during a camping trip. He doesn't remember what happened to his friends. "
                       "The pack found him three days later, blood-soaked and feral.",
        "age_of_first_change": 17,
        "description": "A homid cub of the Red Talons, recently Changed and struggling with the rage inside. "
                       "The pack debates whether civilization has ruined him already.",
    },
    {
        "username": "ElectricDreamer",
        "name": "Dreamwalker",
        "concept": "Metis theurge seeking enlightenment through meditation",
        "tribe": "Stargazers",
        "auspice": "theurge",
        "breed": "metis",
        "pack": "Silicon Fangs",
        "rank": 2,
        # Attributes (7/5/3) - Mental primary, Social secondary, Physical tertiary
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 2,  # Social: 5
        "perception": 4, "intelligence": 4, "wits": 3,  # Mental: 8
        # Abilities (13/9/5) - Knowledges primary, Talents secondary, Skills tertiary
        "alertness": 2, "empathy": 3, "expression": 2, "primal_urge": 3,  # Talents: 10
        "enigmas": 4, "occult": 4, "rituals": 3, "academics": 2,  # Knowledges: 13
        "meditation": 3, "stealth": 2,  # Skills: 5
        # Rage/Gnosis based on auspice (Theurge=2) and breed (Metis=3)
        "rage": 2, "gnosis": 4,
        # Renown (Theurge rank 2: glory 1, honor 0, wisdom 5)
        "glory": 1, "honor": 0, "wisdom": 5,
        # Backgrounds - NOTE: Mentor 2 = elder Stargazer teacher
        "mentor": 2, "ancestors": 1, "spirit_heritage": 1,
        "willpower": 6,
        "first_change": "Born during a celestial alignment, her metis deformity is a third eye that sees the Umbra. "
                       "She views it as a gift rather than a curse.",
        "age_of_first_change": 0,
        "description": "A metis Theurge of the Stargazers seeking enlightenment through meditation "
                       "while her Rage wars with inner peace.",
    },
    {
        "username": "void_whisper",
        "name": "Watches-the-Void",
        "concept": "Shadow Lord theurge sensing Umbral wrongness",
        "tribe": "Shadow Lords",
        "auspice": "theurge",
        "breed": "lupus",
        "pack": "The Wardens",
        "rank": 2,
        # Attributes (7/5/3) - Mental primary, Physical secondary, Social tertiary
        "strength": 2, "dexterity": 3, "stamina": 3,  # Physical: 5
        "charisma": 2, "manipulation": 3, "appearance": 1,  # Social: 3
        "perception": 4, "intelligence": 3, "wits": 4,  # Mental: 8
        # Abilities (13/9/5) - Knowledges primary, Skills secondary, Talents tertiary
        "alertness": 2, "empathy": 1, "intimidation": 2, "primal_urge": 2,  # Talents: 7
        "animal_ken": 2, "stealth": 4, "survival": 3,  # Skills: 9
        "enigmas": 4, "occult": 4, "rituals": 3, "investigation": 2,  # Knowledges: 13
        # Rage/Gnosis based on auspice (Theurge=2) and breed (Lupus=5)
        "rage": 3, "gnosis": 5,
        # Renown (Theurge rank 2: glory 1, honor 0, wisdom 5)
        "glory": 1, "honor": 0, "wisdom": 5,
        # Backgrounds
        "ancestors": 2, "rites": 2, "pure_breed": 1,
        "willpower": 5,
        "first_change": "The spirits of darkness whispered to her from birth. When she Changed, "
                       "she simply acknowledged what she'd always known.",
        "age_of_first_change": 2,
        "description": "A lupus Theurge of the Shadow Lords communing with spirits others fear. "
                       "She knows something is wrong with the Umbra around Seattle but can't identify it.",
    },
]

# =============================================================================
# KINFOLK CHARACTER DEFINITIONS
# =============================================================================

KINFOLK = [
    {
        "username": "xXShadowWolfXx",
        "name": "Sarah Morningkill",
        "concept": "IT security specialist and pack eyes in corporate Seattle",
        "tribe": "Glass Walkers",
        "breed": "homid",
        "relation": "Cousin of a Glass Walker elder",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 3, "appearance": 2,  # Social: 5
        "perception": 3, "intelligence": 4, "wits": 3,  # Mental: 7
        # Abilities (11/7/4)
        "alertness": 2, "empathy": 2, "subterfuge": 3,  # Talents: 7
        "computer": 4, "etiquette": 2, "stealth": 2, "technology": 3,  # Skills: 11
        "academics": 2, "investigation": 2,  # Knowledges: 4
        # Backgrounds - NOTE: Contacts 3 = tech industry, Allies 2 = coworkers
        "contacts": 3, "resources": 3, "allies": 2,
        "willpower": 4,
        "description": "Glass Walker Kinfolk and IT security specialist at a major tech firm. "
                       "She's the pack's eyes inside corporate Seattle.",
    },
    {
        "username": "NightOwl_42",
        "name": "Old Pete",
        "concept": "Food truck operator serving Garou and homeless alike",
        "tribe": "Bone Gnawers",
        "breed": "homid",
        "relation": "Third-generation Bone Gnawer kinfolk",
        # Attributes (6/4/3)
        "strength": 2, "dexterity": 2, "stamina": 3,  # Physical: 4
        "charisma": 3, "manipulation": 2, "appearance": 2,  # Social: 4
        "perception": 3, "intelligence": 2, "wits": 3,  # Mental: 5
        # Abilities (11/7/4)
        "alertness": 3, "empathy": 3, "streetwise": 4, "expression": 1,  # Talents: 11
        "crafts": 3, "drive": 2, "survival": 2,  # Skills: 7
        "investigation": 2, "law": 1, "medicine": 1,  # Knowledges: 4
        # Backgrounds - NOTE: Contacts 4 = street contacts citywide, Allies 2 = homeless community
        "contacts": 4, "allies": 2, "resources": 1,
        "willpower": 4,
        "description": "An elderly Bone Gnawer Kinfolk who runs a food truck, feeding both homeless humans "
                       "and Garou alike. His truck is neutral ground in pack politics.",
    },
    {
        "username": "ByteSlayer",
        "name": "Mike Donovan",
        "concept": "Metalworker crafting fetishes and klaives",
        "tribe": "Get of Fenris",
        "breed": "homid",
        "relation": "Brother of Cuts-Through-Steel",
        # Attributes (6/4/3)
        "strength": 4, "dexterity": 3, "stamina": 3,  # Physical: 7
        "charisma": 2, "manipulation": 1, "appearance": 2,  # Social: 3
        "perception": 3, "intelligence": 2, "wits": 2,  # Mental: 4
        # Abilities (11/7/4)
        "alertness": 2, "athletics": 2, "brawl": 2, "intimidation": 2,  # Talents: 8
        "crafts": 5, "melee": 3, "drive": 1, "firearms": 2,  # Skills: 11
        "occult": 2, "science": 1,  # Knowledges: 3
        # Backgrounds - NOTE: Allies 2 = workshop employees
        "resources": 3, "allies": 2,
        "willpower": 5,
        "gnosis": 1,  # Has Gnosis merit
        "description": "Get of Fenris Kinfolk and owner of a metalworking shop. He crafts fetishes and klaives "
                       "for the local Garou, one of few humans trusted with the sacred work.",
    },
    {
        "username": "Zephyr_Storm",
        "name": "Rosa Martinez",
        "concept": "Environmental lawyer fighting in court",
        "tribe": "Children of Gaia",
        "breed": "homid",
        "relation": "Aunt to several Children of Gaia cubs",
        # Attributes (6/4/3)
        "strength": 1, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 4, "manipulation": 3, "appearance": 2,  # Social: 6
        "perception": 3, "intelligence": 3, "wits": 2,  # Mental: 5
        # Abilities (11/7/4)
        "alertness": 2, "empathy": 3, "expression": 3, "leadership": 2, "subterfuge": 1,  # Talents: 11
        "etiquette": 3, "drive": 2, "computer": 2,  # Skills: 7
        "academics": 2, "law": 4, "investigation": 1,  # Knowledges: 7 - adjust
        # Backgrounds - NOTE: Contacts 2 = legal/environmental, Allies 3 = activist network
        "contacts": 2, "allies": 3, "resources": 2,
        "willpower": 5,
        "description": "A Children of Gaia Kinfolk and environmental lawyer, fighting corporate polluters "
                       "in court while her pack fights them in the Umbra.",
    },
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_tribe(tribe_name):
    """Get a werewolf tribe by name."""
    tribe = Tribe.objects.filter(name=tribe_name).first()
    if not tribe:
        print(f"WARNING: Tribe {tribe_name} not found.")
    return tribe


def get_pack(pack_name, chronicle):
    """Get a pack by name."""
    pack = Pack.objects.filter(name=pack_name, chronicle=chronicle).first()
    if not pack:
        print(f"WARNING: Pack {pack_name} not found.")
    return pack


def apply_werewolf_stats(character, data):
    """Apply stats from data dict to character."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina",
                 "charisma", "manipulation", "appearance",
                 "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(character, attr, data[attr])

    # Abilities (WtA-specific)
    abilities = [
        "alertness", "athletics", "brawl", "empathy", "expression",
        "intimidation", "streetwise", "subterfuge", "leadership", "primal_urge",
        "crafts", "drive", "etiquette", "firearms", "melee", "stealth",
        "animal_ken", "larceny", "performance", "survival",
        "academics", "computer", "investigation", "medicine", "science",
        "enigmas", "law", "occult", "rituals", "technology",
    ]
    for ability in abilities:
        if ability in data:
            setattr(character, ability, data[ability])

    # Willpower
    if "willpower" in data:
        character.willpower = data["willpower"]
        character.temporary_willpower = data["willpower"]


def apply_garou_stats(werewolf, data):
    """Apply werewolf-specific stats."""
    # Auspice and breed
    if "auspice" in data:
        werewolf.auspice = data["auspice"]
    if "breed" in data:
        werewolf.breed = data["breed"]
    if "rank" in data:
        werewolf.rank = data["rank"]

    # Rage and Gnosis
    if "rage" in data:
        werewolf.rage = data["rage"]
    if "gnosis" in data:
        werewolf.gnosis = data["gnosis"]

    # Renown
    if "glory" in data:
        werewolf.glory = data["glory"]
    if "honor" in data:
        werewolf.honor = data["honor"]
    if "wisdom" in data:
        werewolf.wisdom = data["wisdom"]

    # First Change details
    if "first_change" in data:
        werewolf.first_change = data["first_change"]
    if "age_of_first_change" in data:
        werewolf.age_of_first_change = data["age_of_first_change"]


def apply_kinfolk_stats(kinfolk, data):
    """Apply kinfolk-specific stats."""
    if "breed" in data:
        kinfolk.breed = data["breed"]
    if "relation" in data:
        kinfolk.relation = data["relation"]
    if "gnosis" in data:
        kinfolk.gnosis = data["gnosis"]


# =============================================================================
# MAIN CREATION FUNCTIONS
# =============================================================================

def create_werewolves(chronicle):
    """Create all werewolf characters."""
    print("\n--- Creating Werewolves ---")
    created_werewolves = {}

    for wdata in WEREWOLVES:
        user = User.objects.filter(username=wdata["username"]).first()
        if not user:
            print(f"  ERROR: User {wdata['username']} not found")
            continue

        werewolf, created = Werewolf.objects.get_or_create(
            name=wdata["name"],
            owner=user,
            chronicle=chronicle,
            defaults={
                "concept": wdata["concept"],
                "description": wdata.get("description", ""),
                "npc": False,
            }
        )

        if created:
            # Set tribe
            werewolf.tribe = get_tribe(wdata["tribe"])

            # Apply stats
            apply_werewolf_stats(werewolf, wdata)
            apply_garou_stats(werewolf, wdata)

            werewolf.save()
            print(f"  Created werewolf: {wdata['name']} ({wdata['tribe']} {wdata['auspice'].title()})")
        else:
            print(f"  Werewolf already exists: {wdata['name']}")

        created_werewolves[wdata["name"]] = werewolf

        # Handle pack membership
        if wdata.get("pack"):
            pack = get_pack(wdata["pack"], chronicle)
            if pack:
                pack.members.add(werewolf)
                if wdata.get("is_alpha"):
                    pack.leader = werewolf
                    pack.save()
                    print(f"    -> Set as Alpha of {wdata['pack']}")

    return created_werewolves


def create_kinfolk(chronicle):
    """Create all kinfolk characters."""
    print("\n--- Creating Kinfolk ---")

    for kdata in KINFOLK:
        user = User.objects.filter(username=kdata["username"]).first()
        if not user:
            print(f"  ERROR: User {kdata['username']} not found")
            continue

        kinfolk, created = Kinfolk.objects.get_or_create(
            name=kdata["name"],
            owner=user,
            chronicle=chronicle,
            defaults={
                "concept": kdata["concept"],
                "description": kdata.get("description", ""),
                "npc": False,
            }
        )

        if created:
            # Set tribe
            kinfolk.tribe = get_tribe(kdata["tribe"])

            # Apply stats
            apply_werewolf_stats(kinfolk, kdata)
            apply_kinfolk_stats(kinfolk, kdata)

            kinfolk.save()
            print(f"  Created kinfolk: {kdata['name']} ({kdata['tribe']})")
        else:
            print(f"  Kinfolk already exists: {kdata['name']}")


def main():
    """Run the full werewolf character setup."""
    print("=" * 60)
    print("Seattle Test Chronicle - Werewolf Character Setup")
    print("=" * 60)

    chronicle = Chronicle.objects.filter(name="Seattle Test Chronicle").first()
    if not chronicle:
        print("ERROR: Seattle Test Chronicle not found. Run base.py first.")
        return

    # Create characters
    werewolves = create_werewolves(chronicle)
    create_kinfolk(chronicle)

    # Note: Fera are complex and have different models per type
    # They would require separate implementation for each Fera type
    print("\n--- Note: Fera characters require separate implementation ---")
    print("  Fera types (Ananasi, Bastet, Corax, Mokole, Nagah, Ratkin) each have")
    print("  their own models and creation rules. They are listed in DESIGN.md")
    print("  but not created by this script.")

    # Summary
    print("\n" + "=" * 60)
    print("Werewolf character setup complete!")
    print(f"Werewolves: {Werewolf.objects.filter(chronicle=chronicle).count()}")
    print(f"Kinfolk: {Kinfolk.objects.filter(chronicle=chronicle).count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    # When run via `python manage.py shell < script.py`
    main()
