from characters.models.werewolf.charm import SpiritCharm
from characters.models.werewolf.spirit_character import SpiritCharacter

x = SpiritCharacter.objects.get_or_create(
    name="Deer", willpower=4, rage=4, gnosis=6, essence=14, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 368)
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Falcon", willpower=8, rage=6, gnosis=5, essence=19, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 368)
x.charms.set(SpiritCharm.objects.filter(name__in=["Swift Flight"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Snake", willpower=5, rage=6, gnosis=8, essence=19, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 368)
x.charms.set(SpiritCharm.objects.filter(name__in=["Paralyzing Stare"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Wolf", willpower=6, rage=7, gnosis=5, essence=18, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 368)
x.charms.set(SpiritCharm.objects.filter(name__in=["Tracking"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Glade Child (Sapling)",
    willpower=7,
    rage=3,
    gnosis=8,
    essence=20,
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 368)
x.charms.set(SpiritCharm.objects.filter(name__in=["Cleanse the Blight", "Realm Sense"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Glade Child (Mature)",
    willpower=7,
    rage=3,
    gnosis=8,
    essence=35,
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 368)
x.charms.set(SpiritCharm.objects.filter(name__in=["Cleanse the Blight", "Realm Sense"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Glade Child (Ancient)",
    willpower=7,
    rage=3,
    gnosis=8,
    essence=50,
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 368)
x.charms.set(SpiritCharm.objects.filter(name__in=["Cleanse the Blight", "Realm Sense"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Lune", willpower=8, rage=4, gnosis=7, essence=19, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 369)
x.charms.set(SpiritCharm.objects.filter(name__in=["Open Moon Bridge"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Stormcrows", willpower=9, rage=7, gnosis=6, essence=22, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 369)
x.charms.set(SpiritCharm.objects.filter(name__in=["Create Wind", "Tracking"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="The Wendigo", willpower=7, rage=10, gnosis=5, essence=32, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 369)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Blast", "Create Wind", "Freeze", "Materialize", "Tracking"]
    )
)
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="The Wild Hunt (Huntsman)",
    willpower=10,
    rage=10,
    gnosis=5,
    essence=40,
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 369)
x.charms.set(SpiritCharm.objects.filter(name__in=["Armor", "Materialize", "Tracking"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="The Wild Hunt (The Hounds)",
    willpower=6,
    rage=7,
    gnosis=2,
    essence=18,
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 369)
x.charms.set(SpiritCharm.objects.filter(name__in=["Materialize", "Tracking"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Ancestor Spirit", willpower=6, rage=8, gnosis=7, essence=21, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 370)
x.charms.set(SpiritCharm.objects.filter(name__in=[]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Earth Elemental", willpower=9, rage=4, gnosis=5, essence=20, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 370)
x.charms.set(
    SpiritCharm.objects.filter(name__in=["Armor", "Materialize", "Umbraquake"])
)
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Air Elemental", willpower=3, rage=8, gnosis=7, essence=18, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 370)
x.charms.set(SpiritCharm.objects.filter(name__in=["Create Wind", "Updraft"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Fire Elemental", willpower=5, rage=10, gnosis=5, essence=20, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 370)
x.charms.set(SpiritCharm.objects.filter(name__in=["Blast", "Create Fires"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Water Elemental", willpower=6, rage=4, gnosis=10, essence=20, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 370)
x.charms.set(
    SpiritCharm.objects.filter(name__in=["Cleanse the Blight", "Flood", "Healing"])
)
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Glass Elemental", willpower=4, rage=7, gnosis=7, essence=18, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 370)
x.charms.set(
    SpiritCharm.objects.filter(name__in=["Blast", "Materialize", "Shatter Glass"])
)
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Electricity Elemental",
    willpower=6,
    rage=7,
    gnosis=5,
    essence=18,
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 370)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Blast", "Control Electrical Systems", "Short Out"]
    )
)
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Chimerling", willpower=3, rage=5, gnosis=10, essence=18, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 371)
x.charms.set(SpiritCharm.objects.filter(name__in=["Shapeshift"]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Engling", willpower=5, rage=1, gnosis=10, essence=16, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 371)
x.charms.set(SpiritCharm.objects.filter(name__in=[]))
x.display = False
x.save()
x = SpiritCharacter.objects.get_or_create(
    name="Curiosi", willpower=5, rage=3, gnosis=9, essence=17, display=False
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 371)
x.charms.set(SpiritCharm.objects.filter(name__in=["Illuminate"]))
x.display = False
x.save()

# ===== MAGE-SPECIFIC SPIRITS =====
# Paradox Spirits, Elementals, Conceptual Spirits, and other entities from Mage sourcebooks

# Paradox Spirits
x = SpiritCharacter.objects.get_or_create(
    name="Paradox Spirit (Minor)",
    willpower=5,
    rage=6,
    gnosis=4,
    essence=15,
    display=True,
)[0]
x.add_source("M20 Core", 549)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Blast", "Tracking", "Realm Sense"]
    )
)
x.description = (
    "Minor Paradox Spirit that hunts mages who use vulgar magic. Appears as a "
    "twisted reflection of the mage's paradigm gone wrong."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Paradox Spirit (Moderate)",
    willpower=7,
    rage=8,
    gnosis=6,
    essence=21,
    display=True,
)[0]
x.add_source("M20 Core", 549)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Blast", "Tracking", "Armor", "Realm Sense", "Corruption"]
    )
)
x.description = (
    "Moderate Paradox Spirit that actively hunts reality deviants. Can drag mages "
    "into Paradox Realms."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Paradox Spirit (Powerful)",
    willpower=9,
    rage=10,
    gnosis=8,
    essence=27,
    display=True,
)[0]
x.add_source("M20 Core", 549)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=[
            "Materialize",
            "Blast",
            "Tracking",
            "Armor",
            "Realm Sense",
            "Corruption",
            "Possession",
            "Shapeshift",
        ]
    )
)
x.description = (
    "Powerful Paradox Spirit that embodies reality's wrath against mages. Can "
    "create Paradox Realms and inflict permanent Paradox flaws."
)
x.save()

# Elemental Spirits (Mage versions)
x = SpiritCharacter.objects.get_or_create(
    name="Fire Elemental (Minor)",
    willpower=4,
    rage=7,
    gnosis=5,
    essence=16,
    display=True,
)[0]
x.add_source("M20 Core", 368)
x.charms.set(SpiritCharm.objects.filter(name__in=["Materialize", "Blast", "Create Fire"]))
x.description = "Minor spirit of fire and heat, embodies flame and combustion."
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Fire Elemental (Powerful)",
    willpower=7,
    rage=9,
    gnosis=7,
    essence=23,
    display=True,
)[0]
x.add_source("M20 Core", 368)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Blast", "Create Fire", "Armor", "Shapeshift"]
    )
)
x.description = "Powerful spirit of fire, can manifest as living flame or fire creatures."
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Water Elemental (Minor)",
    willpower=5,
    rage=3,
    gnosis=6,
    essence=14,
    display=True,
)[0]
x.add_source("M20 Core", 368)
x.charms.set(
    SpiritCharm.objects.filter(name__in=["Materialize", "Healing", "Cleanse the Blight"])
)
x.description = "Minor spirit of water, embodies flow and adaptation."
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Water Elemental (Powerful)",
    willpower=7,
    rage=5,
    gnosis=8,
    essence=20,
    display=True,
)[0]
x.add_source("M20 Core", 368)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Healing", "Cleanse the Blight", "Shapeshift", "Flood"]
    )
)
x.description = "Powerful spirit of water, can create floods and cleanse corruption."
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Earth Elemental (Minor)",
    willpower=6,
    rage=4,
    gnosis=5,
    essence=15,
    display=True,
)[0]
x.add_source("M20 Core", 368)
x.charms.set(
    SpiritCharm.objects.filter(name__in=["Materialize", "Armor", "Umbraquake"])
)
x.description = "Minor spirit of earth and stone, embodies stability and endurance."
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Earth Elemental (Powerful)",
    willpower=8,
    rage=6,
    gnosis=7,
    essence=21,
    display=True,
)[0]
x.add_source("M20 Core", 368)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Armor", "Umbraquake", "Shapeshift", "Solidify Reality"]
    )
)
x.description = (
    "Powerful spirit of earth, can cause earthquakes and create stone barriers."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Air Elemental (Minor)",
    willpower=4,
    rage=5,
    gnosis=7,
    essence=16,
    display=True,
)[0]
x.add_source("M20 Core", 368)
x.charms.set(
    SpiritCharm.objects.filter(name__in=["Materialize", "Create Wind", "Updraft"])
)
x.description = "Minor spirit of air and wind, embodies movement and freedom."
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Air Elemental (Powerful)",
    willpower=6,
    rage=7,
    gnosis=9,
    essence=22,
    display=True,
)[0]
x.add_source("M20 Core", 368)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Create Wind", "Updraft", "Blast", "Shapeshift"]
    )
)
x.description = "Powerful spirit of air, can create storms and hurricane-force winds."
x.save()

# Conceptual Spirits (Umbrood)
x = SpiritCharacter.objects.get_or_create(
    name="Spirit of Knowledge",
    willpower=8,
    rage=2,
    gnosis=9,
    essence=19,
    display=True,
)[0]
x.add_source("M20 Core", 558)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Airt Sense", "Mind Speech", "Realm Sense"]
    )
)
x.description = (
    "Conceptual spirit embodying knowledge and learning. Often found in libraries "
    "and schools."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Spirit of War",
    willpower=7,
    rage=9,
    gnosis=6,
    essence=22,
    display=True,
)[0]
x.add_source("M20 Core", 558)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Armor", "Blast", "Tracking", "Influence"]
    )
)
x.description = (
    "Conceptual spirit embodying conflict and violence. Feeds on rage and battle."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Spirit of Love",
    willpower=6,
    rage=1,
    gnosis=8,
    essence=15,
    display=True,
)[0]
x.add_source("M20 Core", 558)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Healing", "Influence", "Mind Speech"]
    )
)
x.description = (
    "Conceptual spirit embodying love and compassion. Brings people together."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Spirit of Technology",
    willpower=7,
    rage=3,
    gnosis=7,
    essence=17,
    display=True,
)[0]
x.add_source("M20 Core", 558)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Possession", "Airt Sense", "Short Out"]
    )
)
x.description = (
    "Urban spirit embodying technology and machines. Can inhabit computers and devices."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Spirit of the Wild",
    willpower=6,
    rage=6,
    gnosis=8,
    essence=20,
    display=True,
)[0]
x.add_source("M20 Core", 558)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Shapeshift", "Tracking", "Cleanse the Blight"]
    )
)
x.description = (
    "Nature spirit embodying wilderness and primal forces. Opposed to civilization."
)
x.save()

# Node Guardians
x = SpiritCharacter.objects.get_or_create(
    name="Node Guardian (Minor)",
    willpower=6,
    rage=5,
    gnosis=7,
    essence=18,
    display=True,
)[0]
x.add_source("M20 Core", 608)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Armor", "Tracking", "Realm Sense"]
    )
)
x.description = "Spirit bound to guard a node or sacred place. Defends against intruders."
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Node Guardian (Powerful)",
    willpower=8,
    rage=7,
    gnosis=9,
    essence=24,
    display=True,
)[0]
x.add_source("M20 Core", 608)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=[
            "Materialize",
            "Armor",
            "Blast",
            "Tracking",
            "Realm Sense",
            "Solidify Reality",
        ]
    )
)
x.description = (
    "Powerful guardian spirit protecting a major node. Can strengthen the Gauntlet."
)
x.save()

# Avatar Spirits
x = SpiritCharacter.objects.get_or_create(
    name="Avatar Guide (Dynamic)",
    willpower=7,
    rage=6,
    gnosis=8,
    essence=21,
    display=True,
)[0]
x.add_source("M20 Core", 330)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Mind Speech", "Influence", "Materialize", "Airt Sense"]
    )
)
x.description = (
    "Avatar spirit with Dynamic essence. Bold, assertive, pushes mage to action."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Avatar Guide (Pattern)",
    willpower=8,
    rage=3,
    gnosis=7,
    essence=18,
    display=True,
)[0]
x.add_source("M20 Core", 330)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Mind Speech", "Realm Sense", "Materialize", "Solidify Reality"]
    )
)
x.description = (
    "Avatar spirit with Pattern essence. Orderly, methodical, seeks structure."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Avatar Guide (Primordial)",
    willpower=6,
    rage=7,
    gnosis=9,
    essence=22,
    display=True,
)[0]
x.add_source("M20 Core", 330)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Mind Speech", "Shapeshift", "Materialize", "Tracking"]
    )
)
x.description = (
    "Avatar spirit with Primordial essence. Primal, instinctive, connected to nature."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Avatar Guide (Questing)",
    willpower=7,
    rage=4,
    gnosis=8,
    essence=19,
    display=True,
)[0]
x.add_source("M20 Core", 330)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Mind Speech", "Airt Sense", "Materialize", "Tracking"]
    )
)
x.description = (
    "Avatar spirit with Questing essence. Curious, seeking knowledge and growth."
)
x.save()

# Technocratic Constructs
x = SpiritCharacter.objects.get_or_create(
    name="Data Spider",
    willpower=5,
    rage=2,
    gnosis=6,
    essence=13,
    display=True,
)[0]
x.add_source("Technocracy Reloaded", 242)
x.charms.set(
    SpiritCharm.objects.filter(name__in=["Possession", "Tracking", "Airt Sense"])
)
x.description = (
    "Technocratic spirit construct that inhabits computer systems and tracks data."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Security Watcher",
    willpower=6,
    rage=5,
    gnosis=5,
    essence=16,
    display=True,
)[0]
x.add_source("Technocracy Reloaded", 242)
x.charms.set(
    SpiritCharm.objects.filter(name__in=["Materialize", "Tracking", "Armor", "Blast"])
)
x.description = (
    "Technocratic guardian spirit that patrols secure facilities and Constructs."
)
x.save()

# Nephandi Spirits
x = SpiritCharacter.objects.get_or_create(
    name="Blight Spirit",
    willpower=5,
    rage=8,
    gnosis=6,
    essence=19,
    display=True,
)[0]
x.add_source("Book of the Fallen", 143)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Corruption", "Blast", "Possession"]
    )
)
x.description = "Corrupted spirit that spreads decay and corruption. Serves the Nephandi."
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Malfean Servitor",
    willpower=7,
    rage=10,
    gnosis=7,
    essence=24,
    display=True,
)[0]
x.add_source("Book of the Fallen", 74)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Corruption", "Blast", "Armor", "Possession", "Freeze"]
    )
)
x.description = (
    "Powerful corrupted spirit serving Malfean Nephandi. Embodies entropy and decay."
)
x.save()

# Unique/Named Spirits
x = SpiritCharacter.objects.get_or_create(
    name="The Weaver's Child",
    willpower=9,
    rage=4,
    gnosis=9,
    essence=22,
    display=True,
)[0]
x.add_source("M20 Core", 559)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=[
            "Materialize",
            "Solidify Reality",
            "Armor",
            "Possession",
            "Shapeshift",
        ]
    )
)
x.description = (
    "Powerful spirit of order and pattern. Seeks to impose structure on chaos."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="The Wyld's Voice",
    willpower=7,
    rage=8,
    gnosis=10,
    essence=25,
    display=True,
)[0]
x.add_source("M20 Core", 559)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=[
            "Materialize",
            "Break Reality",
            "Shapeshift",
            "Blast",
            "Corruption",
        ]
    )
)
x.description = (
    "Powerful spirit of chaos and change. Seeks to break down rigid structures."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="The Wyrm's Fang",
    willpower=8,
    rage=10,
    gnosis=8,
    essence=26,
    display=True,
)[0]
x.add_source("M20 Core", 559)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=[
            "Materialize",
            "Corruption",
            "Blast",
            "Armor",
            "Possession",
            "Freeze",
        ]
    )
)
x.description = (
    "Powerful corrupted spirit of entropy and destruction. Serves the Wyrm's agenda."
)
x.save()

# Tradition Lore Spirits
x = SpiritCharacter.objects.get_or_create(
    name="Lune (Crescent Moon)",
    willpower=7,
    rage=3,
    gnosis=8,
    essence=18,
    display=True,
)[0]
x.add_source("Lore of the Traditions", 88)
x.charms.set(
    SpiritCharm.objects.filter(name__in=["Materialize", "Open Moon Bridge", "Airt Sense"])
)
x.description = (
    "Moon spirit associated with the Dreamspeakers and werewolves. Helps spirit travel."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Totem of the Golden Chalice",
    willpower=9,
    rage=2,
    gnosis=9,
    essence=20,
    display=True,
)[0]
x.add_source("Lore of the Traditions", 48)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Materialize", "Healing", "Influence", "Mind Speech"]
    )
)
x.description = (
    "Celestial Chorus totem spirit embodying unity and divine grace. Provides guidance."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="The Dragon of the East",
    willpower=10,
    rage=7,
    gnosis=10,
    essence=27,
    display=True,
)[0]
x.add_source("Lore of the Traditions", 28)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=[
            "Materialize",
            "Armor",
            "Blast",
            "Shapeshift",
            "Healing",
            "Tracking",
        ]
    )
)
x.description = (
    "Powerful Akashic totem spirit. Embodies wisdom, strength, and balance of Do."
)
x.save()

x = SpiritCharacter.objects.get_or_create(
    name="Spirit of the Data Stream",
    willpower=6,
    rage=4,
    gnosis=8,
    essence=18,
    display=True,
)[0]
x.add_source("Lore of the Traditions", 188)
x.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Possession", "Airt Sense", "Tracking", "Mind Speech"]
    )
)
x.description = (
    "Virtual Adept spirit ally inhabiting the Digital Web. Guides hackers and reality coders."
)
x.save()

for spirit in SpiritCharacter.objects.all():
    for x in SpiritCharm.objects.filter(
        name__in=[
            "Airt Sense",
            "Materialize",
            "Realm Sense",
            "Re-Form",
        ]
    ):
        spirit.charms.add(x)
