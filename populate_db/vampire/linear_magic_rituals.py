from characters.models.mage.sorcerer import LinearMagicPath, LinearMagicRitual
from populate_db.vampire.linear_magic_path import (
    alchemy,
    conjuration,
    conveyance,
    divination,
    enchantment,
    ephemera,
    fascination,
    fortune,
    healing,
    hellfire,
    illusion,
    maelstroms,
    necromancy,
    necronics,
    oneiromancy,
    quintessence_manipulation,
    shadows,
    shapeshifting,
    starlight,
    summoning,
)

LinearMagicRitual.objects.get_or_create(
    name="Alcohol Enhancing Powder", level=1, path=alchemy
)[0].add_source("M20 Sorcerer", 19)
LinearMagicRitual.objects.get_or_create(
    name="Cure for Common Cold", level=1, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Drug of Ignore Wound Penalties", level=1, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(name="Sobering Tonic", level=1, path=alchemy)[
    0
].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Unbreakable Mirror", level=1, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(name="Enhanced LSD", level=2, path=alchemy)[
    0
].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Potion that Doubles Running Speed", level=2, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="One Hour Sleep Energy Drink", level=2, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Light, Durable, Strong, Alloy", level=3, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Dust that Reveals Invisible Things", level=3, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Drug that increases Strength and Stamina by 1", level=4, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Drugs that Slow Aging", level=4, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Salve Allowing Shroud-Sight", level=4, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Incendiary Bullet", level=4, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Powder that increases Manipulation and Expression by 1", level=4, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Pungeant Scent that Repels Werewolves", level=5, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Potions that Mimic Vampire Powers", level=5, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Potion that gives three dots of Potence", level=5, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Potion that Accelerates Healing", level=5, path=alchemy
)[0].add_source("M20 Sorcerer", 20)
LinearMagicRitual.objects.get_or_create(
    name="Object Permanence", level=2, path=conjuration
)[0].add_source("M20 Sorcerer", 21)
LinearMagicRitual.objects.get_or_create(name="Always Armed", level=3, path=conjuration)[
    0
].add_source("M20 Sorcerer", 21)
LinearMagicRitual.objects.get_or_create(name="Shitstorm", level=3, path=conjuration)[
    0
].add_source("M20 Sorcerer", 21)
LinearMagicRitual.objects.get_or_create(name="Extraction", level=4, path=conjuration)[
    0
].add_source("M20 Sorcerer", 22)
LinearMagicRitual.objects.get_or_create(name="Spring", level=1, path=conveyance)[
    0
].add_source("M20 Sorcerer", 22)
LinearMagicRitual.objects.get_or_create(name="Teleport Ward", level=2, path=conveyance)[
    0
].add_source("M20 Sorcerer", 22)
LinearMagicRitual.objects.get_or_create(
    name="Get Me the Heck Outta Here!", level=3, path=conveyance
)[0].add_source("M20 Sorcerer", 22)
LinearMagicRitual.objects.get_or_create(
    name="Information Superhighway", level=4, path=conveyance
)[0].add_source("M20 Sorcerer", 23)
LinearMagicRitual.objects.get_or_create(name="Teleportal", level=5, path=conveyance)[
    0
].add_source("M20 Sorcerer", 23)
LinearMagicRitual.objects.get_or_create(
    name="Army Jacket of Arcane", level=1, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Well-Aimed Handgun", level=1, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Restful Stuffed Animal", level=1, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Hawkeye Medallion", level=1, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Dodging Toe-Ring", level=1, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Background Candle", level=1, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Frame of Preservation", level=1, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Bullet Attracting Flask", level=2, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Enhanced Bullets", level=2, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Dancing Anklet", level=2, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(name="Toe Nail", level=2, path=enchantment)[
    0
].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Warning Charm", level=2, path=enchantment
)[0].add_source("M20 Sorcerer", 27)
LinearMagicRitual.objects.get_or_create(
    name="Anti-Fae Ring", level=2, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Running Shoes", level=3, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Amulet Against Sorcery", level=3, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Ghost-Slaying Sword", level=3, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Healing Salve", level=3, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Obsidian Bull Torque of Strength", level=3, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Cleaning Hankerchief", level=3, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(name="Heartseeker", level=4, path=enchantment)[
    0
].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(name="Answer Skull", level=4, path=enchantment)[
    0
].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Torc of Superhuman Strength", level=4, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Damage Reduction Tunic", level=4, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Translation Book", level=4, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Infinite Money Pouch", level=5, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Amulet of Protection", level=5, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Amulet of Hiding", level=5, path=enchantment
)[0].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(name="Silent Cloak", level=5, path=enchantment)[
    0
].add_source("M20 Sorcerer", 28)
LinearMagicRitual.objects.get_or_create(
    name="Mastered Piano", level=5, path=enchantment
)[0].add_source("M20 Sorcerer", 29)
LinearMagicRitual.objects.get_or_create(
    name="Animated Servant", level=5, path=enchantment
)[0].add_source("M20 Sorcerer", 29)
LinearMagicRitual.objects.get_or_create(
    name="Eldritch Mark", level=1, path=enchantment
)[0].add_source("M20 Sorcerer", 29)
LinearMagicRitual.objects.get_or_create(
    name="Enhance Craftmanship", level=2, path=enchantment
)[0].add_source("M20 Sorcerer", 29)
LinearMagicRitual.objects.get_or_create(
    name="Belle/Beau/Bright of the Ball", level=3, path=fascination
)[0].add_source("M20 Sorcerer", 30)
LinearMagicRitual.objects.get_or_create(
    name="Love Potion Number 9", level=4, path=fascination
)[0].add_source("M20 Sorcerer", 30)
LinearMagicRitual.objects.get_or_create(name="Death Curse", level=1, path=fortune)[
    0
].add_source("M20 Sorcerer", 31)
LinearMagicRitual.objects.get_or_create(name="Step on a Crack", level=2, path=fortune)[
    0
].add_source("M20 Sorcerer", 31)
LinearMagicRitual.objects.get_or_create(name="Bashert", level=3, path=fortune)[
    0
].add_source("M20 Sorcerer", 32)
LinearMagicRitual.objects.get_or_create(name="Freudian Slip", level=4, path=fortune)[
    0
].add_source("M20 Sorcerer", 32)
LinearMagicRitual.objects.get_or_create(
    name="Generational Wealth", level=5, path=fortune
)[0].add_source("M20 Sorcerer", 32)
LinearMagicRitual.objects.get_or_create(name="Healing Slumber", level=1, path=healing)[
    0
].add_source("M20 Sorcerer", 33)
LinearMagicRitual.objects.get_or_create(name="Jolt", level=2, path=healing)[
    0
].add_source("M20 Sorcerer", 33)
LinearMagicRitual.objects.get_or_create(name="Mike's Cure-All", level=3, path=healing)[
    0
].add_source("M20 Sorcerer", 33)
LinearMagicRitual.objects.get_or_create(name="Humor Alignment", level=4, path=healing)[
    0
].add_source("M20 Sorcerer", 33)
LinearMagicRitual.objects.get_or_create(name="Fire's Weal", level=2, path=hellfire)[
    0
].add_source("M20 Sorcerer", 34)
LinearMagicRitual.objects.get_or_create(name="Hellblade", level=2, path=hellfire)[
    0
].add_source("M20 Sorcerer", 34)
LinearMagicRitual.objects.get_or_create(
    name="Purification of the Inferno", level=3, path=hellfire
)[0].add_source("M20 Sorcerer", 35)
LinearMagicRitual.objects.get_or_create(name="Smoldering Ruin", level=5, path=hellfire)[
    0
].add_source("M20 Sorcerer", 35)
LinearMagicRitual.objects.get_or_create(name="Cruel Whispers", level=2, path=illusion)[
    0
].add_source("M20 Sorcerer", 36)
LinearMagicRitual.objects.get_or_create(
    name="Hard-Light Constructs", level=3, path=illusion
)[0].add_source("M20 Sorcerer", 37)
LinearMagicRitual.objects.get_or_create(name="Instant Feast", level=4, path=illusion)[
    0
].add_source("M20 Sorcerer", 37)
LinearMagicRitual.objects.get_or_create(name="Oubliette", level=5, path=illusion)[
    0
].add_source("M20 Sorcerer", 37)
LinearMagicRitual.objects.get_or_create(name="Rest in Peace", level=2, path=maelstroms)[
    0
].add_source("M20 Sorcerer", 38)
LinearMagicRitual.objects.get_or_create(
    name="Calm Above, Hell Below", level=3, path=maelstroms
)[0].add_source("M20 Sorcerer", 38)
LinearMagicRitual.objects.get_or_create(
    name="Shelter for the Dead", level=5, path=maelstroms
)[0].add_source("M20 Sorcerer", 38)
LinearMagicRitual.objects.get_or_create(name="Deathsight", level=1, path=necromancy)[
    0
].add_source("M20 Sorcerer", 40)
LinearMagicRitual.objects.get_or_create(
    name="Wrapped in a Shroud", level=3, path=necromancy
)[0].add_source("M20 Sorcerer", 40)
LinearMagicRitual.objects.get_or_create(name="Forced Medium", level=4, path=necromancy)[
    0
].add_source("M20 Sorcerer", 40)
LinearMagicRitual.objects.get_or_create(name="Steal Life", level=5, path=necromancy)[
    0
].add_source("M20 Sorcerer", 40)
LinearMagicRitual.objects.get_or_create(name="Shroud Bubble", level=3, path=necronics)[
    0
].add_source("M20 Sorcerer", 41)
LinearMagicRitual.objects.get_or_create(name="Shut It Down", level=3, path=necronics)[
    0
].add_source("M20 Sorcerer", 41)
LinearMagicRitual.objects.get_or_create(name="Doxxing", level=4, path=necronics)[
    0
].add_source("M20 Sorcerer", 42)
LinearMagicRitual.objects.get_or_create(name="Overwrite", level=5, path=necronics)[
    0
].add_source("M20 Sorcerer", 42)
LinearMagicRitual.objects.get_or_create(
    name="Symbol Interpretation", level=1, path=oneiromancy
)[0].add_source("M20 Sorcerer", 43)
LinearMagicRitual.objects.get_or_create(
    name="Bedtime Story", level=2, path=oneiromancy
)[0].add_source("M20 Sorcerer", 43)
LinearMagicRitual.objects.get_or_create(
    name="Invade Demesne", level=3, path=oneiromancy
)[0].add_source("M20 Sorcerer", 43)
LinearMagicRitual.objects.get_or_create(name="Dream Scream", level=4, path=oneiromancy)[
    0
].add_source("M20 Sorcerer", 43)
LinearMagicRitual.objects.get_or_create(
    name="Quintessence Infusion", level=2, path=quintessence_manipulation
)[0].add_source("M20 Sorcerer", 45)
LinearMagicRitual.objects.get_or_create(
    name="Shape Quintessence", level=3, path=quintessence_manipulation
)[0].add_source("M20 Sorcerer", 45)
LinearMagicRitual.objects.get_or_create(name="Lifting Shadows", level=1, path=shadows)[
    0
].add_source("M20 Sorcerer", 46)
LinearMagicRitual.objects.get_or_create(name="Grip of Shades", level=3, path=shadows)[
    0
].add_source("M20 Sorcerer", 46)
LinearMagicRitual.objects.get_or_create(name="Face Theft", level=1, path=shapeshifting)[
    0
].add_source("M20 Sorcerer", 47)
LinearMagicRitual.objects.get_or_create(
    name="Fix the True Form", level=4, path=shapeshifting
)[0].add_source("M20 Sorcerer", 47)
LinearMagicRitual.objects.get_or_create(
    name="Megafauna Transformation", level=5, path=shapeshifting
)[0].add_source("M20 Sorcerer", 47)

LinearMagicRitual.objects.get_or_create(name="Loud Strain", level=1, path=alchemy)[
    0
].add_source("Tome of Rituals", 4)
LinearMagicRitual.objects.get_or_create(name="Oxen Balm", level=2, path=alchemy)[
    0
].add_source("Tome of Rituals", 4)
LinearMagicRitual.objects.get_or_create(
    name="Tea of Fortification", level=3, path=alchemy
)[0].add_source("Tome of Rituals", 4)
LinearMagicRitual.objects.get_or_create(name="Excelerant", level=4, path=alchemy)[
    0
].add_source("Tome of Rituals", 4)
LinearMagicRitual.objects.get_or_create(
    name="Glaze of the Wolf's Bane", level=5, path=alchemy
)[0].add_source("Tome of Rituals", 5)
LinearMagicRitual.objects.get_or_create(
    name="Slight Manipulation", level=1, path=conjuration
)[0].add_source("Tome of Rituals", 5)
LinearMagicRitual.objects.get_or_create(
    name="Conjurer's Tether", level=2, path=conjuration
)[0].add_source("Tome of Rituals", 5)
LinearMagicRitual.objects.get_or_create(
    name="Herculean Lift", level=3, path=conjuration
)[0].add_source("Tome of Rituals", 5)
LinearMagicRitual.objects.get_or_create(
    name="Call the Swarm", level=4, path=conjuration
)[0].add_source("Tome of Rituals", 5)
LinearMagicRitual.objects.get_or_create(
    name="Aerial Redirect", level=5, path=conjuration
)[0].add_source("Tome of Rituals", 5)
LinearMagicRitual.objects.get_or_create(
    name="Ritual of Binding", level=1, path=conveyance
)[0].add_source("Tome of Rituals", 5)
LinearMagicRitual.objects.get_or_create(name="Juggernaut", level=2, path=conveyance)[
    0
].add_source("Tome of Rituals", 6)
LinearMagicRitual.objects.get_or_create(name="Autopilot", level=3, path=conveyance)[
    0
].add_source("Tome of Rituals", 6)
LinearMagicRitual.objects.get_or_create(name="Scenic Route", level=4, path=conveyance)[
    0
].add_source("Tome of Rituals", 6)
LinearMagicRitual.objects.get_or_create(
    name="Send Messenger", level=5, path=conveyance
)[0].add_source("Tome of Rituals", 6)
LinearMagicRitual.objects.get_or_create(name="Far Sight", level=1, path=divination)[
    0
].add_source("Tome of Rituals", 6)
LinearMagicRitual.objects.get_or_create(
    name="Divine the Heart", level=2, path=divination
)[0].add_source("Tome of Rituals", 6)
LinearMagicRitual.objects.get_or_create(
    name="Overlapping Symbolism", level=3, path=divination
)[0].add_source("Tome of Rituals", 6)
LinearMagicRitual.objects.get_or_create(
    name="Morning's Preparedness", level=4, path=divination
)[0].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(
    name="Behold Entwined Fates", level=5, path=divination
)[0].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(
    name="Reveal the Unseen", level=1, path=ephemera
)[0].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(
    name="Blessed Offerings", level=2, path=ephemera
)[0].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(name="Dismissal", level=3, path=ephemera)[
    0
].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(
    name="Shield the Silver Cord", level=4, path=ephemera
)[0].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(
    name="Weight of the Gods", level=5, path=ephemera
)[0].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(name="Brightshades", level=1, path=enchantment)[
    0
].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(
    name="Superquantum Processor", level=2, path=enchantment
)[0].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(
    name="Psi-Noise Generator", level=3, path=enchantment
)[0].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(
    name="Aura Contacts", level=4, path=enchantment
)[0].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(name="Zombie Dust", level=5, path=enchantment)[
    0
].add_source("Tome of Rituals", 7)
LinearMagicRitual.objects.get_or_create(
    name="Positive Self-Talk", level=1, path=fascination
)[0].add_source("Tome of Rituals", 8)
LinearMagicRitual.objects.get_or_create(name="Mindbinding", level=2, path=fascination)[
    0
].add_source("Tome of Rituals", 8)
LinearMagicRitual.objects.get_or_create(
    name="Glass Slipper", level=3, path=fascination
)[0].add_source("Tome of Rituals", 8)
LinearMagicRitual.objects.get_or_create(
    name="Intensive Conditioning", level=4, path=fascination
)[0].add_source("Tome of Rituals", 8)
LinearMagicRitual.objects.get_or_create(name="Filibuster", level=5, path=fascination)[
    0
].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(name="Persistent Error", level=1, path=fortune)[
    0
].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(name="The Third Time", level=2, path=fortune)[
    0
].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(name="Loudstep", level=3, path=fortune)[
    0
].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(name="Tonal Shift", level=4, path=fortune)[
    0
].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(
    name="The Book of Heroes", level=5, path=fortune
)[0].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(
    name="Suppress Deprivation", level=1, path=healing
)[0].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(name="Comfortably Numb", level=2, path=healing)[
    0
].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(
    name="Post-Facto Grounding", level=3, path=healing
)[0].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(name="Carrier", level=4, path=healing)[
    0
].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(name="New Flesh", level=5, path=healing)[
    0
].add_source("Tome of Rituals", 9)
LinearMagicRitual.objects.get_or_create(
    name="Inviolate Tumblers", level=1, path=hellfire
)[0].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(name="Shocking Blow", level=2, path=hellfire)[
    0
].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(name="Sigil of Toxin", level=3, path=hellfire)[
    0
].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(name="Landmine", level=4, path=hellfire)[
    0
].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(name="Epicenter", level=5, path=hellfire)[
    0
].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(name="White Noise", level=1, path=illusion)[
    0
].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(name="Phantom Pain", level=2, path=illusion)[
    0
].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(name="Clean Up", level=3, path=illusion)[
    0
].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(
    name="Enhance Tolerance", level=4, path=illusion
)[0].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(name="Ride-Along", level=5, path=illusion)[
    0
].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(name="Shadow Ban", level=1, path=maelstroms)[
    0
].add_source("Tome of Rituals", 10)
LinearMagicRitual.objects.get_or_create(name="Thunderstruck", level=2, path=maelstroms)[
    0
].add_source("Tome of Rituals", 11)
LinearMagicRitual.objects.get_or_create(
    name="Cleansing Rain", level=3, path=maelstroms
)[0].add_source("Tome of Rituals", 11)
LinearMagicRitual.objects.get_or_create(name="Shadow Trap", level=4, path=maelstroms)[
    0
].add_source("Tome of Rituals", 11)
LinearMagicRitual.objects.get_or_create(
    name="Whip the Maelstrom", level=5, path=maelstroms
)[0].add_source("Tome of Rituals", 11)
LinearMagicRitual.objects.get_or_create(
    name="Filtered Visions", level=1, path=necromancy
)[0].add_source("Tome of Rituals", 12)
LinearMagicRitual.objects.get_or_create(
    name="Peel Back the Shroud", level=2, path=necromancy
)[0].add_source("Tome of Rituals", 12)
LinearMagicRitual.objects.get_or_create(
    name="Shroud Interference", level=3, path=necromancy
)[0].add_source("Tome of Rituals", 12)
LinearMagicRitual.objects.get_or_create(
    name="Compelled Exit", level=4, path=necromancy
)[0].add_source("Tome of Rituals", 12)
LinearMagicRitual.objects.get_or_create(name="Bind Shadow", level=5, path=necromancy)[
    0
].add_source("Tome of Rituals", 12)
LinearMagicRitual.objects.get_or_create(
    name="Amplified Impedence", level=1, path=necronics
)[0].add_source("Tome of Rituals", 12)
LinearMagicRitual.objects.get_or_create(
    name="Negate Resistance", level=2, path=necronics
)[0].add_source("Tome of Rituals", 12)
LinearMagicRitual.objects.get_or_create(name="Transmit Ghost", level=3, path=necronics)[
    0
].add_source("Tome of Rituals", 12)
LinearMagicRitual.objects.get_or_create(name="Feedback", level=4, path=necronics)[
    0
].add_source("Tome of Rituals", 12)
LinearMagicRitual.objects.get_or_create(
    name="Enhance Ectopresence", level=5, path=necronics
)[0].add_source("Tome of Rituals", 13)
LinearMagicRitual.objects.get_or_create(
    name="Core Revelation", level=1, path=oneiromancy
)[0].add_source("Tome of Rituals", 13)
LinearMagicRitual.objects.get_or_create(
    name="Malleable Gossamer", level=2, path=oneiromancy
)[0].add_source("Tome of Rituals", 13)
LinearMagicRitual.objects.get_or_create(
    name="Craft Nightmare", level=3, path=oneiromancy
)[0].add_source("Tome of Rituals", 13)
LinearMagicRitual.objects.get_or_create(
    name="Recurring Dream", level=4, path=oneiromancy
)[0].add_source("Tome of Rituals", 13)
LinearMagicRitual.objects.get_or_create(
    name="Nightmare Riot", level=5, path=oneiromancy
)[0].add_source("Tome of Rituals", 13)
LinearMagicRitual.objects.get_or_create(
    name="Sorcerer's Sight", level=1, path=quintessence_manipulation
)[0].add_source("Tome of Rituals", 14)
LinearMagicRitual.objects.get_or_create(
    name="Imbue Receptacle", level=2, path=quintessence_manipulation
)[0].add_source("Tome of Rituals", 14)
LinearMagicRitual.objects.get_or_create(
    name="Fuel Pattern", level=3, path=quintessence_manipulation
)[0].add_source("Tome of Rituals", 14)
LinearMagicRitual.objects.get_or_create(
    name="Parma Magica", level=4, path=quintessence_manipulation
)[0].add_source("Tome of Rituals", 14)
LinearMagicRitual.objects.get_or_create(
    name="Momentary Nexus", level=5, path=quintessence_manipulation
)[0].add_source("Tome of Rituals", 14)
LinearMagicRitual.objects.get_or_create(name="Haze", level=1, path=shadows)[
    0
].add_source("Tome of Rituals", 15)
LinearMagicRitual.objects.get_or_create(name="Unsettling Curse", level=2, path=shadows)[
    0
].add_source("Tome of Rituals", 15)
LinearMagicRitual.objects.get_or_create(name="Shadow Armor", level=3, path=shadows)[
    0
].add_source("Tome of Rituals", 15)
LinearMagicRitual.objects.get_or_create(name="Abyssal Horror", level=4, path=shadows)[
    0
].add_source("Tome of Rituals", 15)
LinearMagicRitual.objects.get_or_create(name="Shadow Tentacle", level=5, path=shadows)[
    0
].add_source("Tome of Rituals", 15)
LinearMagicRitual.objects.get_or_create(name="Pelt", level=1, path=shapeshifting)[
    0
].add_source("Tome of Rituals", 15)
LinearMagicRitual.objects.get_or_create(name="Soft Body", level=2, path=shapeshifting)[
    0
].add_source("Tome of Rituals", 15)
LinearMagicRitual.objects.get_or_create(name="Claws", level=3, path=shapeshifting)[
    0
].add_source("Tome of Rituals", 15)
LinearMagicRitual.objects.get_or_create(
    name="Echolocation", level=4, path=shapeshifting
)[0].add_source("Tome of Rituals", 15)
LinearMagicRitual.objects.get_or_create(
    name="Grizzly Death", level=5, path=shapeshifting
)[0].add_source("Tome of Rituals", 15)
LinearMagicRitual.objects.get_or_create(name="Close Portal", level=1, path=starlight)[
    0
].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(
    name="Armor of Starlight", level=2, path=starlight
)[0].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(
    name="Shared Navigation", level=3, path=starlight
)[0].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(name="Bulwark", level=4, path=starlight)[
    0
].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(name="Helldive", level=5, path=starlight)[
    0
].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(name="Infest", level=1, path=summoning)[
    0
].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(
    name="Ward Against Spirits", level=2, path=summoning
)[0].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(
    name="Interrogate Spirit", level=3, path=summoning
)[0].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(
    name="Protection Against Vampires", level=4, path=summoning
)[0].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(
    name="Protection Against Werewolves", level=4, path=summoning
)[0].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(
    name="Protection Against Mages", level=4, path=summoning
)[0].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(
    name="Protection Against Changelings", level=4, path=summoning
)[0].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(
    name="Protection Against Ghosts", level=4, path=summoning
)[0].add_source("Tome of Rituals", 16)
LinearMagicRitual.objects.get_or_create(name="Summon Demon", level=5, path=summoning)[
    0
].add_source("Tome of Rituals", 16)


for path in LinearMagicPath.objects.all():
    LinearMagicRitual.objects.get_or_create(
        name=f"Store Spell ({path.name})", level=5, path=path
    )[0].add_source("M20 Sorcerer", 14)
