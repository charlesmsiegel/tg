# Example Wonders, Talismans, Artifacts, and Magical Items from Mage Sourcebooks

from characters.models.mage.resonance import Resonance
from items.models.mage.artifact import Artifact
from items.models.mage.charm import Charm
from items.models.mage.grimoire import Grimoire
from items.models.mage.talisman import Talisman
from items.models.mage.wonder import Wonder

from populate_db.effects_INC import effect_summon_spirit_minor, effect_harm_ghost

# ===== WONDERS (Permanent Magical Items) =====

# Dragon Pearls (Akashic Brotherhood)
pearl = Wonder.objects.get_or_create(
    name="Dragon Pearl (Lesser)",
    rank=3,
    background_cost=6,
    quintessence_max=5,
)[0]
pearl.description = (
    "A crystallized sphere of Quintessence used by Akashic mages to channel chi. "
    "Grants +1 die to Life and Prime effects when held during casting."
)
pearl.add_source("Lore of the Traditions", 28)
pearl.set_rank(3)
pearl.add_resonance(Resonance.objects.get_or_create(name="Harmonious")[0])
pearl.add_resonance(Resonance.objects.get_or_create(name="Balanced")[0])
pearl.save()

pearl_greater = Wonder.objects.get_or_create(
    name="Dragon Pearl (Greater)",
    rank=5,
    background_cost=12,
    quintessence_max=10,
)[0]
pearl_greater.description = (
    "A master-crafted Dragon Pearl containing immense power. "
    "Grants +2 dice to Life and Prime effects and can store Paradox."
)
pearl_greater.add_source("Lore of the Traditions", 28)
pearl_greater.set_rank(5)
pearl_greater.add_resonance(Resonance.objects.get_or_create(name="Harmonious")[0])
pearl_greater.add_resonance(Resonance.objects.get_or_create(name="Powerful")[0])
pearl_greater.save()

# Flying Carpet (Correspondence Wonder)
carpet = Wonder.objects.get_or_create(
    name="Flying Carpet of Al-Rashid",
    rank=4,
    background_cost=10,
    quintessence_max=15,
)[0]
carpet.description = (
    "An enchanted Persian carpet that flies at the will of its owner. "
    "Can carry up to 4 passengers at speeds up to 100 mph."
)
carpet.add_source("M20 Core", 656)
carpet.set_rank(4)
carpet.add_resonance(Resonance.objects.get_or_create(name="Swift")[0])
carpet.add_resonance(Resonance.objects.get_or_create(name="Mystical")[0])
carpet.save()

# Hermetic Staff of Power
staff = Wonder.objects.get_or_create(
    name="Staff of the Magi",
    rank=5,
    background_cost=15,
    quintessence_max=20,
)[0]
staff.description = (
    "A powerful Hermetic staff carved from ancient oak and bound with silver. "
    "Grants +2 dice to all ritual magic and can channel lightning bolts (Forces 3)."
)
staff.add_source("Lore of the Traditions", 128)
staff.set_rank(5)
staff.add_resonance(Resonance.objects.get_or_create(name="Powerful")[0])
staff.add_resonance(Resonance.objects.get_or_create(name="Ancient")[0])
staff.save()

# Verbena Athame
athame = Wonder.objects.get_or_create(
    name="Athame of the Moon",
    rank=3,
    background_cost=6,
    quintessence_max=10,
)[0]
athame.description = (
    "A ritual dagger used in Verbena witchcraft, especially blood magic. "
    "Reduces difficulty of Life magic by -1 when used to draw blood."
)
athame.add_source("Lore of the Traditions", 168)
athame.set_rank(3)
athame.add_resonance(Resonance.objects.get_or_create(name="Primal")[0])
athame.add_resonance(Resonance.objects.get_or_create(name="Vital")[0])
athame.save()

# Virtual Adept Cyberdeck
cyberdeck = Wonder.objects.get_or_create(
    name="Reality Hacker's Cyberdeck",
    rank=4,
    background_cost=10,
    quintessence_max=12,
)[0]
cyberdeck.description = (
    "An advanced cyberdeck modified with resonant circuits for reality hacking. "
    "Grants +2 dice to Correspondence and Mind effects when hacking reality or the Digital Web."
)
cyberdeck.add_source("Lore of the Traditions", 188)
cyberdeck.set_rank(4)
cyberdeck.add_resonance(Resonance.objects.get_or_create(name="Digital")[0])
cyberdeck.add_resonance(Resonance.objects.get_or_create(name="Innovative")[0])
cyberdeck.save()

# ===== TALISMANS (Limited-Use Magical Items) =====

# Healing Potion
potion = Talisman.objects.get_or_create(
    name="Elixir of Regeneration",
    rank=2,
    background_cost=4,
    quintessence_max=3,
)[0]
potion.description = (
    "An alchemical potion that heals 2 health levels of lethal damage when consumed. "
    "Single use."
)
potion.add_source("M20 Core", 656)
potion.set_rank(2)
potion.quintessence_max = 3
potion.save()

# Wand of Lightning
wand = Talisman.objects.get_or_create(
    name="Wand of Chain Lightning",
    rank=3,
    background_cost=6,
    quintessence_max=10,
)[0]
wand.description = (
    "A Hermetic wand that can unleash lightning bolts. Contains 10 charges, "
    "each dealing 4 dice of lethal damage (Forces 3)."
)
wand.add_source("Lore of the Traditions", 129)
wand.set_rank(3)
wand.save()

# Scrying Mirror
mirror = Talisman.objects.get_or_create(
    name="Mirror of True Seeing",
    rank=3,
    background_cost=6,
    quintessence_max=8,
)[0]
mirror.description = (
    "A polished obsidian mirror that allows remote viewing anywhere on Earth. "
    "Uses Correspondence 3, Time 2 for past viewing."
)
mirror.add_source("M20 Core", 656)
mirror.set_rank(3)
mirror.save()

# Ring of Protection
ring = Talisman.objects.get_or_create(
    name="Ring of Warding",
    rank=2,
    background_cost=4,
    quintessence_max=5,
)[0]
ring.description = (
    "A silver ring inscribed with protective runes. Grants +2 dice to soak "
    "and can activate a shield once per day (Forces 2)."
)
ring.add_source("M20 Core", 656)
ring.set_rank(2)
ring.save()

# ===== ARTIFACTS (Unique/Legendary Items) =====

# The Excalibur Archetype
excalibur = Artifact.objects.get_or_create(
    name="Sword of the Rightful King",
    rank=5,
    background_cost=15,
    quintessence_max=25,
)[0]
excalibur.description = (
    "A legendary sword of power that can only be wielded by the worthy. "
    "Deals aggravated damage, grants +3 to all combat pools, and radiates an "
    "aura of divine authority (Prime 5, Forces 3, Mind 3)."
)
excalibur.add_source("M20 Core", 658)
excalibur.set_rank(5)
excalibur.add_resonance(Resonance.objects.get_or_create(name="Noble")[0])
excalibur.add_resonance(Resonance.objects.get_or_create(name="Powerful")[0])
excalibur.add_resonance(Resonance.objects.get_or_create(name="Holy")[0])
excalibur.save()

# Philosopher's Stone
stone = Artifact.objects.get_or_create(
    name="The Philosopher's Stone",
    rank=5,
    background_cost=15,
    quintessence_max=30,
)[0]
stone.description = (
    "The legendary alchemical artifact capable of transmuting base metals to gold, "
    "granting immortality, and creating Tass. The ultimate goal of alchemists "
    "(Matter 5, Prime 5, Life 5)."
)
stone.add_source("Lore of the Traditions", 129)
stone.set_rank(5)
stone.add_resonance(Resonance.objects.get_or_create(name="Perfect")[0])
stone.add_resonance(Resonance.objects.get_or_create(name="Transformative")[0])
stone.save()

# Holy Grail
grail = Artifact.objects.get_or_create(
    name="The Holy Grail",
    rank=5,
    background_cost=15,
    quintessence_max=50,
)[0]
grail.description = (
    "The cup of Christ, legendary artifact of the Celestial Chorus. "
    "Grants perfect healing, spiritual enlightenment, and connection to the Divine "
    "(Life 5, Prime 5, Spirit 5, Mind 4)."
)
grail.add_source("Lore of the Traditions", 48)
grail.set_rank(5)
grail.add_resonance(Resonance.objects.get_or_create(name="Holy")[0])
grail.add_resonance(Resonance.objects.get_or_create(name="Divine")[0])
grail.add_resonance(Resonance.objects.get_or_create(name="Healing")[0])
grail.save()

# ===== CHARMS (Spirit-Bound Items) =====

# Spirit Whistle
whistle = Charm.objects.get_or_create(
    name="Spirit-Calling Whistle",
    rank=2,
    background_cost=4,
    quintessence_max=5,
    arete=2,
)[0]
whistle.power = effect_summon_spirit_minor
whistle.description = (
    "A carved bone whistle that summons friendly spirits when blown. "
    "Contains a minor air spirit."
)
whistle.add_source("M20 Core", 658)
whistle.set_rank(2)
whistle.save()

# Ghost-Slaying Sword
ghostblade = Charm.objects.get_or_create(
    name="Blade of Ectoplasmic Severance",
    rank=3,
    background_cost=6,
    quintessence_max=8,
    arete=3,
)[0]
ghostblade.power = effect_harm_ghost
ghostblade.description = (
    "A sword bound with a spirit that allows it to harm incorporeal entities. "
    "Deals aggravated damage to ghosts and spirits."
)
ghostblade.add_source("M20 Core", 658)
ghostblade.set_rank(3)
ghostblade.save()

# ===== GRIMOIRES (Books of Power) =====

# Basic Hermetic Grimoire
grimoire1 = Grimoire.objects.get_or_create(
    name="The Lesser Key of Solomon",
    rank=3,
)[0]
grimoire1.description = (
    "A classic grimoire of Hermetic magic containing rituals for summoning "
    "and binding spirits. Teaches Spirit 3, Prime 2, and High Ritual Magick."
)
grimoire1.add_source("Lore of the Traditions", 128)
grimoire1.set_rank(3)
grimoire1.save()

# Advanced Akashic Text
grimoire2 = Grimoire.objects.get_or_create(
    name="The Sutra of Perfect Understanding",
    rank=4,
)[0]
grimoire2.description = (
    "An ancient Buddhist text revealing the secrets of Do and enlightenment. "
    "Teaches Life 4, Mind 4, and advanced martial arts techniques."
)
grimoire2.add_source("Lore of the Traditions", 28)
grimoire2.set_rank(4)
grimoire2.save()

# Verbena Book of Shadows
grimoire3 = Grimoire.objects.get_or_create(
    name="The Grand Book of Shadows",
    rank=4,
)[0]
grimoire3.description = (
    "A massive tome containing generations of Verbena wisdom, blood rituals, "
    "and natural magic. Teaches Life 4, Prime 3, Forces 3, and Witchcraft."
)
grimoire3.add_source("Lore of the Traditions", 168)
grimoire3.set_rank(4)
grimoire3.save()

# Virtual Adept Codex
grimoire4 = Grimoire.objects.get_or_create(
    name="The Digital Necronomicon",
    rank=4,
)[0]
grimoire4.description = (
    "A constantly-updating digital grimoire in the Deep Web containing advanced "
    "reality hacking techniques. Teaches Correspondence 4, Forces 3, Mind 3."
)
grimoire4.add_source("Lore of the Traditions", 188)
grimoire4.set_rank(4)
grimoire4.save()

# Sons of Ether Mad Science Manual
grimoire5 = Grimoire.objects.get_or_create(
    name="Dr. Tesla's Collected Works",
    rank=5,
)[0]
grimoire5.description = (
    "The complete works of Nikola Tesla, annotated with Etheric theories. "
    "Teaches Forces 5, Matter 4, Prime 3, and Weird Science."
)
grimoire5.add_source("Lore of the Traditions", 148)
grimoire5.set_rank(5)
grimoire5.save()

# ===== TECHNOCRATIC DEVICES =====

# Neuro-Optical Transmitter
flashything = Wonder.objects.get_or_create(
    name="Memory Reorganization Device (Flashy Thing)",
    rank=3,
    background_cost=6,
    quintessence_max=10,
)[0]
flashything.description = (
    "A pen-shaped device that erases memories of reality deviation and replaces "
    "them with consensus-acceptable explanations (Mind 3, Prime 2)."
)
flashything.add_source("Technocracy Reloaded", 225)
flashything.set_rank(3)
flashything.save()

# Progenitor Healing Nanites
nanites = Talisman.objects.get_or_create(
    name="Advanced Cellular Reconstruction Nanites",
    rank=3,
    background_cost=6,
    quintessence_max=8,
)[0]
nanites.description = (
    "Microscopic medical nanobots that rapidly heal injuries. "
    "Heals 3 health levels of lethal damage or 1 aggravated over 24 hours."
)
nanites.add_source("Technocracy Reloaded", 218)
nanites.set_rank(3)
nanites.save()

# Void Engineer Dimensional Portal
portal = Wonder.objects.get_or_create(
    name="Portable Dimensional Gateway",
    rank=4,
    background_cost=10,
    quintessence_max=15,
)[0]
portal.description = (
    "A briefcase-sized device that opens stable portals to predetermined locations "
    "or the Deep Umbra (Correspondence 4, Spirit 3, Prime 2)."
)
portal.add_source("Technocracy Reloaded", 227)
portal.set_rank(4)
portal.save()

# Iteration X Combat Exoskeleton
exo = Wonder.objects.get_or_create(
    name="AEGIS Mark VII Powered Armor",
    rank=4,
    background_cost=10,
    quintessence_max=12,
)[0]
exo.description = (
    "Advanced powered armor with enhanced strength, armor plating, and integrated "
    "weapon systems. +3 Strength, +5 Armor, built-in weapons "
    "(Matter 4, Forces 3, Life 2)."
)
exo.add_source("Technocracy Reloaded", 205)
exo.set_rank(4)
exo.save()

# Syndicate Probability Manipulator
probdev = Wonder.objects.get_or_create(
    name="Statistical Variance Optimization Device",
    rank=3,
    background_cost=6,
    quintessence_max=10,
)[0]
probdev.description = (
    "A subtle device disguised as a luxury watch that manipulates probability "
    "to ensure favorable outcomes in business and gambling (Entropy 3)."
)
probdev.add_source("Technocracy Reloaded", 182)
probdev.set_rank(3)
probdev.save()

# ===== UNIQUE/PLOT DEVICES =====

# Reality-Defining Item
doissetep_stone = Artifact.objects.get_or_create(
    name="Heartstone of Doissetep",
    rank=5,
    background_cost=15,
    quintessence_max=100,
)[0]
doissetep_stone.description = (
    "The central Node stone from the destroyed Chantry of Doissetep. "
    "Contains immense Quintessence and can anchor Horizon Realms. "
    "Radiates powerful Hermetic resonance (Prime 5, Spirit 5, All Spheres 3)."
)
doissetep_stone.add_source("M20 Core", 612)
doissetep_stone.set_rank(5)
doissetep_stone.add_resonance(Resonance.objects.get_or_create(name="Ancient")[0])
doissetep_stone.add_resonance(Resonance.objects.get_or_create(name="Powerful")[0])
doissetep_stone.add_resonance(Resonance.objects.get_or_create(name="Tragic")[0])
doissetep_stone.save()

# Avatar Storm Detector
detector = Wonder.objects.get_or_create(
    name="Avatar Storm Early Warning System",
    rank=3,
    background_cost=6,
    quintessence_max=8,
)[0]
detector.description = (
    "A device that detects approaching Avatar Storms and Paradox buildups. "
    "Essential for safe Umbral travel (Spirit 3, Prime 2, Entropy 1)."
)
detector.add_source("M20 Core", 534)
detector.set_rank(3)
detector.save()
