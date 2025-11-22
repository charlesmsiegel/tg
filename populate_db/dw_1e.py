"""
Digital Web 1st Edition - Mage: The Ascension Sourcebook
Populate database with characters, items, rotes, and locations from Digital Web
"""

from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.mage import Mage
from characters.models.mage.wonder import Wonder
from characters.models.mage.effect import Effect
from items.models.mage.artifact import Artifact
from items.models.mage.talisman import Talisman
from locations.models.mage.chantry import Chantry
from locations.models.mage.node import Node


def add_source(obj, book="Digital Web 1e", page=None):
    """Helper to add source information"""
    if page:
        obj.add_source(book, page)
    else:
        obj.add_source(book)


def populate_characters():
    """Create NPCs from Digital Web"""

    # Jessica Young - Barkeep at Spy's Demise
    jessica = Mage.objects.get_or_create(
        name="Jessica Young",
        defaults={
            "essence": "Questing",
            "nature": "Architect",
            "demeanor": "Avant-Garde",
            "concept": "Cartographer & Barkeep",
            "tradition": "Virtual Adept",
            "subfaction": "Former Void Engineer",
            "strength": 2,
            "dexterity": 2,
            "stamina": 3,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 3,
            "perception": 4,
            "intelligence": 4,
            "wits": 3,
            "alertness": 3,
            "awareness": 4,
            "computer": 3,
            "cosmology": 5,
            "culture": 2,
            "dodge": 1,
            "enigmas": 1,
            "expression": 5,
            "intuition": 2,
            "linguistics": 1,
            "meditation": 1,
            "melee": 1,
            "research": 4,
            "science": 3,
            "stealth": 2,
            "subterfuge": 1,
            "technology": 4,
            "correspondence": 3,
            "forces": 2,
            "matter": 1,
            "mind": 2,
            "prime": 3,
            "spirit": 1,
            "time": 1,
            "avatar": 4,
            "dream": 1,
            "library": 2,
            "arete": 4,
            "willpower": 8,
            "quintessence": 17,
        }
    )[0]
    add_source(jessica, page=57)

    # "23" - Iteration X Information Broker
    twenty_three = Mage.objects.get_or_create(
        name="23",
        defaults={
            "essence": "Pattern",
            "nature": "Fanatic",
            "demeanor": "Loner",
            "concept": "Information Broker",
            "tradition": "Technocracy",
            "subfaction": "Iteration X",
            "strength": 3,
            "dexterity": 2,
            "stamina": 5,
            "charisma": 2,
            "manipulation": 4,
            "appearance": 3,
            "perception": 4,
            "intelligence": 3,
            "wits": 4,
            "alertness": 3,
            "athletics": 1,
            "awareness": 4,
            "brawl": 1,
            "computer": 4,
            "culture": 3,
            "enigmas": 2,
            "etiquette": 1,
            "firearms": 1,
            "intuition": 2,
            "intimidation": 2,
            "investigation": 2,
            "medicine": 1,
            "research": 3,
            "science": 2,
            "stealth": 2,
            "streetwise": 1,
            "subterfuge": 5,
            "technology": 3,
            "correspondence": 3,
            "forces": 2,
            "life": 1,
            "mind": 2,
            "matter": 1,
            "prime": 2,
            "arcane": 2,
            "avatar": 2,
            "destiny": 3,
            "arete": 5,
            "willpower": 9,
            "quintessence": 12,
            "paradox": 3,
        }
    )[0]
    add_source(twenty_three, page=57)

    # Acid - Hollow One Cybernaut
    acid = Mage.objects.get_or_create(
        name="Acid",
        defaults={
            "essence": "Dynamic",
            "nature": "Martyr",
            "demeanor": "Deviant",
            "tradition": "Hollow Ones",
            "concept": "Wild Cybernaut",
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "charisma": 4,
            "manipulation": 2,
            "appearance": 2,
            "perception": 4,
            "intelligence": 5,
            "wits": 3,
            "alertness": 2,
            "awareness": 4,
            "computer": 4,
            "cosmology": 2,
            "dodge": 1,
            "enigmas": 3,
            "expression": 2,
            "firearms": 1,
            "intuition": 4,
            "medicine": 1,
            "meditation": 1,
            "occult": 3,
            "research": 2,
            "science": 1,
            "stealth": 1,
            "streetwise": 3,
            "subterfuge": 1,
            "technology": 4,
            "correspondence": 2,
            "entropy": 1,
            "forces": 2,
            "mind": 2,
            "prime": 2,
            "spirit": 1,
            "time": 1,
            "allies": 1,
            "avatar": 5,
            "destiny": 5,
            "arete": 3,
            "willpower": 7,
            "quintessence": 13,
            "paradox": 7,
        }
    )[0]
    add_source(acid, page=58)

    # Kalydescope - Experimental Virtual Adept
    kalydescope = Mage.objects.get_or_create(
        name="Kalydescope",
        defaults={
            "essence": "Dynamic",
            "nature": "Avant-garde",
            "demeanor": "Bon Vivant",
            "tradition": "Virtual Adept",
            "concept": "Experimental Shapeshifter",
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "charisma": 3,
            "manipulation": 4,
            "appearance": 3,
            "perception": 3,
            "intelligence": 4,
            "wits": 3,
            "alertness": 2,
            "athletics": 1,
            "awareness": 3,
            "computer": 4,
            "cosmology": 4,
            "culture": 2,
            "drive": 1,
            "dodge": 1,
            "enigmas": 4,
            "etiquette": 1,
            "expression": 1,
            "firearms": 1,
            "intuition": 2,
            "investigation": 2,
            "leadership": 1,
            "medicine": 1,
            "meditation": 2,
            "melee": 1,
            "occult": 2,
            "research": 2,
            "science": 3,
            "stealth": 3,
            "subterfuge": 2,
            "survival": 1,
            "technology": 4,
            "correspondence": 3,
            "entropy": 1,
            "forces": 1,
            "life": 3,
            "matter": 2,
            "mind": 3,
            "prime": 3,
            "spirit": 2,
            "avatar": 5,
            "arcane": 3,
            "dream": 2,
            "mentor": 2,
            "arete": 4,
            "willpower": 7,
            "quintessence": 12,
            "paradox": 8,
        }
    )[0]
    add_source(kalydescope, page=59)

    # Secret Agent John Courage
    courage = Mage.objects.get_or_create(
        name="John Courage",
        defaults={
            "essence": "Dynamic",
            "nature": "Loner",
            "demeanor": "Thrill-seeker",
            "tradition": "Virtual Adept",
            "subfaction": "Rogue Man in Black",
            "concept": "Double/Triple Agent",
            "strength": 3,
            "dexterity": 4,
            "stamina": 4,
            "charisma": 4,
            "manipulation": 3,
            "appearance": 2,
            "perception": 4,
            "intelligence": 4,
            "wits": 5,
            "alertness": 3,
            "athletics": 3,
            "awareness": 3,
            "brawl": 5,
            "computer": 5,
            "dodge": 3,
            "enigmas": 4,
            "firearms": 5,
            "investigation": 5,
            "linguistics": 1,
            "medicine": 2,
            "science": 2,
            "stealth": 6,
            "subterfuge": 5,
            "technology": 4,
            "correspondence": 4,
            "entropy": 2,
            "forces": 4,
            "life": 3,
            "mind": 3,
            "prime": 2,
            "time": 3,
            "arcane": 5,
            "avatar": 4,
            "arete": 4,
            "willpower": 10,
            "quintessence": 6,
            "paradox": 8,
        }
    )[0]
    add_source(courage, page=60)

    # Astarte - Son of Ether in the Net
    astarte = Mage.objects.get_or_create(
        name="Astarte",
        defaults={
            "essence": "Primordial",
            "nature": "Visionary",
            "demeanor": "Director",
            "tradition": "Sons of Ether",
            "concept": "Star Goddess of VR",
            "strength": 2,
            "dexterity": 3,
            "stamina": 3,
            "charisma": 2,
            "manipulation": 4,
            "appearance": 3,
            "perception": 4,
            "intelligence": 4,
            "wits": 4,
            "alertness": 1,
            "awareness": 2,
            "computer": 4,
            "cosmology": 4,
            "culture": 1,
            "dodge": 1,
            "enigmas": 3,
            "etiquette": 1,
            "firearms": 1,
            "intuition": 2,
            "intimidation": 3,
            "investigation": 1,
            "leadership": 1,
            "medicine": 2,
            "meditation": 1,
            "occult": 2,
            "research": 3,
            "science": 2,
            "stealth": 2,
            "subterfuge": 1,
            "technology": 3,
            "correspondence": 3,
            "forces": 3,
            "life": 1,
            "matter": 1,
            "mind": 3,
            "prime": 3,
            "spirit": 3,
            "time": 2,
            "arcane": 2,
            "avatar": 3,
            "library": 4,
            "talisman": 5,
            "arete": 4,
            "willpower": 8,
            "quintessence": 9,
            "paradox": 4,
        }
    )[0]
    add_source(astarte, page=61)

    # Nightwind - Master Virtual Adept
    nightwind = Mage.objects.get_or_create(
        name="Nightwind",
        defaults={
            "essence": "Questing",
            "nature": "Architect",
            "demeanor": "Loner",
            "tradition": "Virtual Adept",
            "concept": "Master Net Navigator",
            "strength": 2,
            "dexterity": 2,
            "stamina": 5,
            "charisma": 2,
            "manipulation": 4,
            "appearance": 3,
            "perception": 5,
            "intelligence": 4,
            "wits": 5,
            "alertness": 4,
            "awareness": 4,
            "computer": 5,
            "cosmology": 2,
            "dodge": 3,
            "drive": 2,
            "enigmas": 3,
            "firearms": 1,
            "intuition": 4,
            "investigation": 4,
            "law": 2,
            "linguistics": 1,
            "medicine": 1,
            "meditation": 1,
            "melee": 1,
            "research": 3,
            "science": 3,
            "stealth": 5,
            "streetwise": 2,
            "subterfuge": 3,
            "technology": 5,
            "correspondence": 3,
            "entropy": 3,
            "forces": 2,
            "life": 1,
            "mind": 3,
            "prime": 3,
            "spirit": 2,
            "time": 1,
            "arcane": 5,
            "avatar": 5,
            "talisman": 2,
            "arete": 6,
            "willpower": 10,
            "quintessence": 14,
            "paradox": 3,
        }
    )[0]
    add_source(nightwind, page=61)

    # Dr. John von Neumann - Master Son of Ether
    von_neumann = Mage.objects.get_or_create(
        name="Dr. John von Neumann",
        defaults={
            "essence": "Questing",
            "nature": "Architect",
            "demeanor": "Visionary",
            "tradition": "Sons of Ether",
            "concept": "AI Researcher",
            "strength": 1,
            "dexterity": 2,
            "stamina": 3,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 2,
            "perception": 5,
            "intelligence": 5,
            "wits": 4,
            "alertness": 3,
            "awareness": 3,
            "computer": 5,
            "dodge": 1,
            "drive": 1,
            "enigmas": 4,
            "intuition": 2,
            "meditation": 2,
            "research": 4,
            "science": 4,
            "technology": 4,
            "correspondence": 5,
            "entropy": 3,
            "life": 2,
            "matter": 4,
            "mind": 3,
            "prime": 3,
            "avatar": 5,
            "node": 5,
            "talisman": 5,
            "arete": 7,
            "willpower": 9,
            "quintessence": 7,
            "paradox": 2,
        }
    )[0]
    add_source(von_neumann, page=79)

    # Bertrand Gerarde - Virtual Adept Apprentice
    gerarde = Mage.objects.get_or_create(
        name="Bertrand Gerarde",
        defaults={
            "essence": "Dynamic",
            "nature": "Conniver",
            "demeanor": "Conformist",
            "tradition": "Virtual Adept",
            "concept": "Von Neumann's Apprentice",
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "charisma": 2,
            "manipulation": 4,
            "appearance": 2,
            "perception": 3,
            "intelligence": 4,
            "wits": 3,
            "alertness": 3,
            "awareness": 3,
            "computer": 4,
            "cosmology": 2,
            "dodge": 1,
            "drive": 1,
            "intuition": 2,
            "meditation": 1,
            "research": 3,
            "science": 3,
            "technology": 3,
            "correspondence": 4,
            "forces": 3,
            "mind": 3,
            "prime": 2,
            "avatar": 4,
            "mentor": 5,
            "node": 5,
            "arete": 4,
            "willpower": 7,
            "quintessence": 8,
            "paradox": 3,
        }
    )[0]
    add_source(gerarde, page=80)

    # Captain Douglas - Sons of Ether Starship Captain
    douglas = Mage.objects.get_or_create(
        name="Captain Vance Douglas",
        defaults={
            "essence": "Dynamic",
            "nature": "Visionary",
            "demeanor": "Fanatic",
            "tradition": "Sons of Ether",
            "concept": "Starship Captain",
            "strength": 3,
            "dexterity": 3,
            "stamina": 2,
            "charisma": 4,
            "manipulation": 3,
            "appearance": 3,
            "perception": 2,
            "intelligence": 2,
            "wits": 3,
            "alertness": 3,
            "athletics": 1,
            "brawl": 2,
            "computer": 2,
            "cosmology": 4,
            "dodge": 2,
            "intuition": 2,
            "leadership": 4,
            "melee": 2,
            "science": 4,
            "technology": 3,
            "matter": 5,
            "correspondence": 3,
            "forces": 4,
            "mind": 2,
            "prime": 2,
            "avatar": 3,
            "destiny": 3,
            "node": 5,
            "arete": 6,
            "willpower": 8,
            "quintessence": 6,
        }
    )[0]
    add_source(douglas, page=80)

    # Ilyana Tanov - Sons of Ether First Officer
    tanov = Mage.objects.get_or_create(
        name="Ilyana Tanov",
        defaults={
            "essence": "Dynamic",
            "nature": "Judge",
            "demeanor": "Director",
            "tradition": "Sons of Ether",
            "concept": "Starship First Officer",
            "strength": 2,
            "dexterity": 3,
            "stamina": 2,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 4,
            "perception": 3,
            "intelligence": 3,
            "wits": 2,
            "awareness": 2,
            "computer": 2,
            "drive": 1,
            "intimidation": 3,
            "intuition": 4,
            "linguistics": 2,
            "meditation": 2,
            "research": 3,
            "science": 4,
            "correspondence": 3,
            "forces": 3,
            "matter": 4,
            "mind": 2,
            "prime": 2,
            "avatar": 2,
            "mentor": 3,
            "node": 5,
            "talisman": 3,
            "arete": 6,
            "willpower": 7,
            "quintessence": 5,
        }
    )[0]
    add_source(tanov, page=81)

    # Ambrose Channing - Renegade Void Engineer
    channing = Mage.objects.get_or_create(
        name="Ambrose Channing",
        defaults={
            "essence": "Primordial",
            "nature": "Judge",
            "demeanor": "Director",
            "tradition": "Technocracy",
            "subfaction": "Void Engineer (Renegade)",
            "concept": "Rebel Astrophysicist",
            "strength": 2,
            "dexterity": 3,
            "stamina": 3,
            "charisma": 3,
            "manipulation": 4,
            "appearance": 3,
            "perception": 4,
            "intelligence": 4,
            "wits": 3,
            "alertness": 4,
            "athletics": 3,
            "awareness": 4,
            "brawl": 2,
            "computer": 4,
            "cosmology": 5,
            "dodge": 2,
            "drive": 3,
            "enigmas": 4,
            "firearms": 2,
            "intuition": 1,
            "intimidation": 2,
            "investigation": 2,
            "linguistics": 1,
            "occult": 3,
            "research": 2,
            "science": 5,
            "stealth": 1,
            "technology": 5,
            "correspondence": 3,
            "entropy": 1,
            "forces": 1,
            "mind": 2,
            "prime": 4,
            "spirit": 1,
            "time": 3,
            "allies": 2,
            "avatar": 3,
            "talisman": 2,
            "arete": 5,
            "willpower": 9,
            "quintessence": 10,
            "paradox": 2,
        }
    )[0]
    add_source(channing, page=93)


def populate_talismans():
    """Create Talismans and Artifacts from Digital Web"""

    # Digital Online Package
    dop = Talisman.objects.get_or_create(
        name="Digital Online Package",
        defaults={
            "rank": 1,
            "gnosis": 3,
            "quintessence": 10,
            "arete": 3,
            "description": "Starter kit for Virtual Adepts including VR helmet, bodysuit, "
                          "expansion card, guide to Digital Web, and maps of major paths.",
        }
    )[0]
    add_source(dop, page=100)

    # Seekers
    seeker = Talisman.objects.get_or_create(
        name="Seeker",
        defaults={
            "rank": 2,
            "gnosis": 6,
            "quintessence": 15,
            "arete": 6,
            "description": "Electronic familiar that floats beside user in the Net, "
                          "performing searches and navigation with 6 dice Perception rolls.",
        }
    )[0]
    add_source(seeker, page=100)

    # Cosmic Communications Package
    cosmic_comm = Talisman.objects.get_or_create(
        name="Cosmic Communications Package",
        defaults={
            "rank": 3,
            "gnosis": 3,
            "quintessence": 6,
            "arete": 3,
            "description": "Card and software that turns any computer into a transceiver for "
                          "radio transmissions, cellular phone, fax/modem, and more.",
        }
    )[0]
    add_source(cosmic_comm, page=100)

    # Electroephemeral Scanner
    scanner = Talisman.objects.get_or_create(
        name="Electroephemeral Scanner",
        defaults={
            "rank": 3,
            "gnosis": 3,
            "quintessence": 10,
            "arete": 3,
            "description": "Scanner that digitizes physical objects into the Digital Web, "
                          "creating virtual representations online.",
        }
    )[0]
    add_source(scanner, page=100)

    # Jump Box
    jumpbox = Talisman.objects.get_or_create(
        name="Jump Box",
        defaults={
            "rank": 3,
            "gnosis": 5,
            "quintessence": 20,
            "arete": 5,
            "description": "Small black box with red button labeled 'Don't Panic' - "
                          "performs Instant Offline effect to emergency disconnect from Net.",
        }
    )[0]
    add_source(jumpbox, page=100)

    # Thought Programs
    thought_prog = Talisman.objects.get_or_create(
        name="Thought Program",
        defaults={
            "rank": 3,
            "gnosis": 5,
            "quintessence": 5,
            "arete": 5,
            "description": "Links to icon via Mind sphere, providing rating 5 in a single "
                          "Ability while in the Net. One per Intelligence point usable.",
        }
    )[0]
    add_source(thought_prog, page=100)

    # Digital Drill
    drill = Talisman.objects.get_or_create(
        name="Digital Drill",
        defaults={
            "rank": 4,
            "gnosis": 8,
            "quintessence": 20,
            "arete": 8,
            "description": "Appears as halogen flashlight - cuts through Restrictions "
                          "unnoticed by de-rezzing and reforming them.",
        }
    )[0]
    add_source(drill, page=100)

    # Magickal Macro Keyboard
    keyboard = Talisman.objects.get_or_create(
        name="Magickal Macro Keyboard",
        defaults={
            "rank": 4,
            "gnosis": 7,
            "quintessence": 30,
            "arete": 7,
            "description": "Keyboard that stores up to 8 magickal effects (max 4th level) "
                          "assigned to keys, activated on keypress with Time and Prime.",
        }
    )[0]
    add_source(keyboard, page=101)

    # Lazarus Transmitter
    lazarus = Talisman.objects.get_or_create(
        name="Lazarus Transmitter",
        defaults={
            "rank": 5,
            "gnosis": 10,
            "quintessence": 10,
            "arete": 10,
            "description": "Surgically implanted failsafe that projects mage into Digital Web "
                          "when critically injured until body can be repaired.",
        }
    )[0]
    add_source(lazarus, page=101)

    # Fiberopticon
    fiberopticon = Talisman.objects.get_or_create(
        name="Fiberopticon",
        defaults={
            "rank": 5,
            "gnosis": 8,
            "quintessence": 20,
            "arete": 8,
            "description": "Von Neumann's powerful Talisman that finds any information in the "
                          "Web, bypasses security, decodes encryption, downloads to user's mind. "
                          "Read-only currently. Generates 1 Paradox per search.",
        }
    )[0]
    add_source(fiberopticon, page=81)


def populate_effects():
    """Create Rotes/Effects from Digital Web"""

    # Hardware Entry
    hardware_entry = Effect.objects.get_or_create(
        name="Hardware Entry",
        defaults={
            "correspondence": 1,
            "effect": "Allows Sensory and Astral Immersion in Digital Web via VR rig. "
                     "Coincidental for mages, vulgar for Sleepers. Difficulty 6, 3+ successes.",
        }
    )[0]
    add_source(hardware_entry, page=98)

    # Wetware Entry
    wetware_entry = Effect.objects.get_or_create(
        name="Wetware Entry",
        defaults={
            "correspondence": 1,
            "effect": "Sensory/Astral Immersion without VR rig, using high-tech computer. "
                     "Difficulty 8, requires 5 successes extended.",
        }
    )[0]
    add_source(wetware_entry, page=98)

    # Instant Offline
    instant_offline = Effect.objects.get_or_create(
        name="Instant Offline",
        defaults={
            "correspondence": 3,
            "forces": 1,
            "effect": "Rips user offline in nanoseconds. Botch inflicts 1 Health per '1' rolled "
                     "from system shock (non-aggravated).",
        }
    )[0]
    add_source(instant_offline, page=98)

    # TechnoVision
    technovision = Effect.objects.get_or_create(
        name="TechnoVision",
        defaults={
            "correspondence": 1,
            "entropy": 1,
            "forces": 1,
            "mind": 1,
            "prime": 1,
            "effect": "Scans Digital Web showing readouts analyzing everything: distances, "
                     "weaknesses, positive identification of icons. Developed by Iteration X.",
        }
    )[0]
    add_source(technovision, page=98)

    # Doe's Password
    does_password = Effect.objects.get_or_create(
        name="Doe's Password",
        defaults={
            "mind": 3,
            "entropy": 2,
            "effect": "Links to Restriction program via Mind, uses Entropy to randomly "
                     "discover entry method. Works on any Restricted Area.",
        }
    )[0]
    add_source(does_password, page=98)

    # Hacker's Glance
    hackers_glance = Effect.objects.get_or_create(
        name="Hacker's Glance",
        defaults={
            "entropy": 2,
            "correspondence": 1,
            "effect": "Analyzes massive information amounts, increasing probability of finding "
                     "desired data. Each success grants 3 successes on data retrieval roll.",
        }
    )[0]
    add_source(hackers_glance, page=98)

    # Create Virtual Object
    create_virtual = Effect.objects.get_or_create(
        name="Create Virtual Object",
        defaults={
            "forces": 3,
            "prime": 2,
            "effect": "Makes permanent electronic object for Digital Web use. Can create knives, "
                     "bats, motorcycles, guns, grenades. Works like physical world up to Forces 3 limits.",
        }
    )[0]
    add_source(create_virtual, page=98)

    # Joshua's Goodbye
    joshuas_goodbye = Effect.objects.get_or_create(
        name="Joshua's Goodbye",
        defaults={
            "forces": 3,
            "entropy": 3,
            "prime": 2,
            "effect": "Order of Hermes rote causing localized surge removing Forces from icon/body. "
                     "Inflicts Health Levels and dumps mage offline with Prime addition.",
        }
    )[0]
    add_source(joshuas_goodbye, page=98)

    # Energy Transformation
    energy_transform = Effect.objects.get_or_create(
        name="Energy Transformation",
        defaults={
            "life": 4,
            "forces": 2,
            "correspondence": 1,
            "effect": "Converts physical body to energy for Holistic transmission into/out of "
                     "Digital Web. Requires laser scanning. Basis of FORCE NEXT LOOP rote.",
        }
    )[0]
    add_source(energy_transform, page=98)

    # Virtual Talisman Transmogrification
    virtual_talisman = Effect.objects.get_or_create(
        name="Virtual Talisman Transmogrification",
        defaults={
            "matter": 3,
            "prime": 3,
            "forces": 2,
            "effect": "Transfers Talisman online like Energy Transformation shifts beings. "
                     "Created by Dr. Solaris to transport mega-ray guns into Digital Web.",
        }
    )[0]
    add_source(virtual_talisman, page=98)

    # High Memory
    high_memory = Effect.objects.get_or_create(
        name="High Memory",
        defaults={
            "mind": 3,
            "entropy": 2,
            "effect": "Shuffles information (equal to Virtual Weight in successes) randomly "
                     "through mage's mind, rendering data undetectable to mental scans.",
        }
    )[0]
    add_source(high_memory, page=99)

    # Restrict Sector
    restrict_sector = Effect.objects.get_or_create(
        name="Restrict Sector",
        defaults={
            "mind": 4,
            "prime": 3,
            "effect": "Creates permanent Restriction sealing sector from access. Takes physical "
                     "form as barriers or guardians. Requires 7 successes vs diff 7 to destroy.",
        }
    )[0]
    add_source(restrict_sector, page=99)

    # Captain's Treasure
    captains_treasure = Effect.objects.get_or_create(
        name="Captain's Treasure",
        defaults={
            "prime": 4,
            "entropy": 2,
            "effect": "Locates financial data conduit (usually Syndicate), shifts it so all "
                     "transactions stream through user's accounts. Prevents detection but risky.",
        }
    )[0]
    add_source(captains_treasure, page=99)

    # Overwrite
    overwrite = Effect.objects.get_or_create(
        name="Overwrite",
        defaults={
            "prime": 4,
            "entropy": 3,
            "forces": 3,
            "effect": "Alters parameters - always vulgar. 5 successes removes parameter, "
                     "1 subtly shifts meaning. Cannot remove contextual formatting.",
        }
    )[0]
    add_source(overwrite, page=99)

    # Tag
    tag = Effect.objects.get_or_create(
        name="Tag",
        defaults={
            "prime": 2,
            "correspondence": 2,
            "mind": 1,
            "effect": "Traces tiny Quintessence mark on target, allowing tracking anywhere "
                     "through Digital Web. Effects last until target goes offline.",
        }
    )[0]
    add_source(tag, page=99)

    # Create Daemon
    create_daemon = Effect.objects.get_or_create(
        name="Create Daemon",
        defaults={
            "spirit": 4,
            "prime": 3,
            "forces": 2,
            "mind": 2,
            "effect": "Binds spirit to electronic Pattern creating Data Beast/daemon. Power level "
                     "= 2 successes on Int+Computer diff 7. Leadership needed for control.",
        }
    )[0]
    add_source(create_daemon, page=99)

    # Information Superhighway
    info_superhighway = Effect.objects.get_or_create(
        name="Information Superhighway",
        defaults={
            "time": 3,
            "correspondence": 3,
            "effect": "Speeds mage through known conduits/sectors by accelerating Time. "
                     "5 successes allows near-light-speed travel. By Cult of Ecstasy 'Epicurus'.",
        }
    )[0]
    add_source(info_superhighway, page=99)

    # Virtual Lockpick
    virtual_lockpick = Effect.objects.get_or_create(
        name="Virtual Lockpick",
        defaults={
            "time": 3,
            "correspondence": 1,
            "forces": 2,
            "mind": 1,
            "effect": "Compresses time in processor, guesses passwords by educated guessing. "
                     "Requires login ID, 5 minutes runtime, Computer 3. No concentration needed.",
        }
    )[0]
    add_source(virtual_lockpick, page=99)


def populate_locations():
    """Create notable locations from Digital Web"""

    # The Spy's Demise - Primary hub
    spys_demise = Node.objects.get_or_create(
        name="The Spy's Demise",
        defaults={
            "description": "Legendary neutral meeting place in Digital Web. Social center for all "
                          "mages, with constantly shifting rooms, secret passages, and conduits to "
                          "all major Grid sectors. Staff dispenses free Quintessence (Tass) equally. "
                          "Rules: No vulgar magick, all violence goes outside, everyone has right to "
                          "enter and receive Tass. Violations result in de-rezzing.",
            "reality_zone": "Digital Web",
        }
    )[0]
    add_source(spys_demise, page=51)

    # Spaceport 1
    spaceport = Node.objects.get_or_create(
        name="Spaceport 1",
        defaults={
            "parent": "The Spy's Demise",
            "description": "Bubble-sphere chamber in Spy's Demise where virtual spaceships dock. "
                          "Populated by aliens, pilots, trophy artists. Run by Space Fleet cabal of "
                          "Sons of Ether and Void Engineers. Connects to space exploration Grid sectors.",
            "reality_zone": "Digital Web",
        }
    )[0]
    add_source(spaceport, page=55)

    # Paradise
    paradise = Node.objects.get_or_create(
        name="Paradise",
        defaults={
            "parent": "The Spy's Demise",
            "description": "Lush tropical resort in Spy's Demise with crystal waters, white sand, "
                          "nightclubs, restaurants, shops. Place for decadent desires and relaxation. "
                          "Connects to chat rooms for virtual flirting and cyber-intimacy.",
            "reality_zone": "Digital Web",
        }
    )[0]
    add_source(paradise, page=55)

    # Cathedral
    cathedral = Node.objects.get_or_create(
        name="Cathedral",
        defaults={
            "parent": "The Spy's Demise",
            "description": "Ornate church with stained-glass windows depicting Ascension scenes. "
                          "Created by Celestial Chorus for spiritual discussions between Traditions "
                          "and Technocracy. Extra Tass dispensed after enlightened debates.",
            "reality_zone": "Digital Web",
        }
    )[0]
    add_source(cathedral, page=56)

    # The Board Room
    board_room = Node.objects.get_or_create(
        name="The Board Room",
        defaults={
            "parent": "The Spy's Demise",
            "description": "Formal meeting room with mahogany table and leather chairs, expandable "
                          "for any size gathering. Created by Syndicate. Used for large meetings and "
                          "business discussions. Screens show moderator and current speaker.",
            "reality_zone": "Digital Web",
        }
    )[0]
    add_source(board_room, page=56)

    # Serenity Grove
    serenity = Node.objects.get_or_create(
        name="Serenity Grove",
        defaults={
            "parent": "The Spy's Demise",
            "description": "Well-landscaped park with lakes, trails, picnic areas, playgrounds. "
                          "Escape from magick and metaphysics - such discussions strictly forbidden "
                          "and enforced by park rangers. Place for relaxation only.",
            "reality_zone": "Digital Web",
        }
    )[0]
    add_source(serenity, page=56)

    # The Crater
    crater = Node.objects.get_or_create(
        name="The Crater",
        defaults={
            "description": "Popular Stacked File arena for virtual combat and duels. Five pits: "
                          "1-3 for duels, 4-5 for team fights. Pit 3 can become Restricted for "
                          "death matches. Run by legendary Cult of Ecstasy martial artist who may "
                          "be trapped here. Good place to gain Quintessence through combat.",
            "reality_zone": "Digital Web",
        }
    )[0]
    add_source(crater, page=31)

    # Pool of Infinite Reflection
    pool = Node.objects.get_or_create(
        name="Pool of Infinite Reflection",
        defaults={
            "description": "First Akashic Brother's meditation space in Digital Web. Place of "
                          "tranquility that can induce temporary Quiet. Complete sensory deprivation "
                          "- no direction, balance, or sensation except ebb and flow of one's icon.",
            "reality_zone": "Digital Web",
        }
    )[0]
    add_source(pool, page=32)

    # The Matterhorn
    matterhorn = Node.objects.get_or_create(
        name="The Matterhorn",
        defaults={
            "description": "Massive mountain on fringe of Formatted Sector, perpetually lashed by "
                          "blizzards. So huge that neither summit nor base is visible. Called 'coughing "
                          "hill' by some Dreamspeakers. True nature unknown.",
            "reality_zone": "Digital Web",
        }
    )[0]
    add_source(matterhorn, page=32)

    # Construct 1010
    construct = Node.objects.get_or_create(
        name="Construct 1010",
        defaults={
            "description": "Iteration X stronghold - mechanical fortress accessed through garbage "
                          "labyrinth. Metal walls hum constantly. Contains RES AI project, cybernetic "
                          "modification chambers, combat training areas. Heavily defended by HIT Marks "
                          "and Guardian programs.",
            "reality_zone": "Digital Web - Technocracy Territory",
        }
    )[0]
    add_source(construct, page=87)

    # Club Dionysis
    club_d = Chantry.objects.get_or_create(
        name="Club Dionysis",
        defaults={
            "description": "Cult of Ecstasy Chantry exploring new frontiers of cyber-sexuality "
                          "using elaborate iconic bodies with novel senses. Run by Tiva, statuesque "
                          "black woman who welcomes open-minded from all Traditions for best parties.",
            "reality_zone": "Digital Web",
            "faction": "Traditions",
        }
    )[0]
    add_source(club_d, page=106)

    # Entropitorium
    entropitorium = Chantry.objects.get_or_create(
        name="Entropitorium",
        defaults={
            "description": "Secretive Euthanatos Chantry studying soul definition by examining icons "
                          "encapsulating psyches. Requests volunteers but rumored to trap unsuspecting "
                          "Cybernaucts. Run by Iman Asrawi. Virtual Adepts sometimes volunteer for study.",
            "reality_zone": "Digital Web",
            "faction": "Traditions",
        }
    )[0]
    add_source(entropitorium, page=106)


def run():
    """Main population function"""
    print("Populating Digital Web 1st Edition content...")

    populate_characters()
    print("✓ Characters populated")

    populate_talismans()
    print("✓ Talismans/Artifacts populated")

    populate_effects()
    print("✓ Rotes/Effects populated")

    populate_locations()
    print("✓ Locations populated")

    print("\nDigital Web 1st Edition population complete!")
    print("\nNote: This sourcebook also includes:")
    print("- Detailed mechanics for the Digital Web (Chapter 1)")
    print("- Two full adventure scenarios (Chapters 3-4)")
    print("- Extensive Net terminology and slang")
    print("- Computer virus mechanics and daemon creation")
    print("- Data Beasts, Webspiders, and other Net denizens")
    print("- Crossover rules for Werewolf and Vampire")
