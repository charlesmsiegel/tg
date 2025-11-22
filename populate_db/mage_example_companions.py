# Example Companions and Familiars from Mage Sourcebooks
# These serve as templates for player familiars and magical companions

from characters.models.mage.companion import Companion
from characters.models.werewolf.charm import SpiritCharm
from populate_db.advantages import alacrity, armor
from populate_db.advantages import claws_fangs_or_horns as claws
from populate_db.advantages import (
    empathic_bond,
    flexibility,
    human_speech,
    nightsight,
    tracking,
    wings,
)
from populate_db.archetypes import caregiver, explorer, loner, sage, trickster

# Configure advantages
nightsight.add_ratings([1])
tracking.add_ratings([1, 2, 3])
wings.add_ratings([2, 4, 6])
human_speech.add_ratings([2])

# ===== CLASSIC ANIMAL FAMILIARS =====

# Black Cat Familiar (Classic Witchcraft)
black_cat = Companion.objects.get_or_create(
    name="Midnight (Black Cat Familiar)",
    companion_type="familiar",
)[0]
black_cat.description = (
    "A sleek black cat with piercing green eyes. Classic witch's familiar, "
    "grants insight into Entropy magic and can sense bad luck."
)
black_cat.nature = caregiver
black_cat.demeanor = loner
black_cat.strength = 1
black_cat.dexterity = 4
black_cat.stamina = 2
black_cat.charisma = 3
black_cat.manipulation = 3
black_cat.appearance = 4
black_cat.perception = 4
black_cat.intelligence = 2
black_cat.wits = 4
black_cat.willpower = 5
black_cat.alertness = 3
black_cat.athletics = 2
black_cat.brawl = 2
black_cat.stealth = 4
black_cat.survival = 2
black_cat.arcane = 2
black_cat.essence = 6
black_cat.add_source("M20 Core", 335)
black_cat.save()
black_cat.add_advantage(nightsight, 1)
black_cat.add_advantage(claws, 3)
black_cat.add_advantage(alacrity, 2)
black_cat.add_advantage(empathic_bond, 2)

# Raven Familiar (Death Magic)
raven = Companion.objects.get_or_create(
    name="Muninn (Raven Familiar)",
    companion_type="familiar",
)[0]
raven.description = (
    "A large raven with an uncanny intelligence. Associated with death magic, "
    "memory, and prophecy. Can speak a few words."
)
raven.nature = sage
raven.demeanor = trickster
raven.strength = 1
raven.dexterity = 3
raven.stamina = 2
raven.charisma = 2
raven.manipulation = 3
raven.appearance = 2
raven.perception = 5
raven.intelligence = 3
raven.wits = 4
raven.willpower = 6
raven.alertness = 4
raven.athletics = 2
raven.brawl = 1
raven.stealth = 3
raven.survival = 3
raven.arcane = 1
raven.essence = 7
raven.add_source("Lore of the Traditions", 109)
raven.save()
raven.add_advantage(wings, 4)
raven.add_advantage(empathic_bond, 2)
raven.add_advantage(human_speech, 2)
raven.charms.set(SpiritCharm.objects.filter(name__in=["Mind Speech", "Tracking"]))

# Owl Familiar (Wisdom and Mind Magic)
owl = Companion.objects.get_or_create(
    name="Athena's Eye (Owl Familiar)",
    companion_type="familiar",
)[0]
owl.description = (
    "A wise barn owl with enormous eyes. Grants insight into Mind magic "
    "and can see through illusions."
)
owl.nature = sage
owl.demeanor = sage
owl.strength = 1
owl.dexterity = 3
owl.stamina = 2
owl.charisma = 2
owl.manipulation = 2
owl.appearance = 3
owl.perception = 5
owl.intelligence = 3
owl.wits = 4
owl.willpower = 5
owl.alertness = 5
owl.athletics = 2
owl.awareness = 3
owl.brawl = 1
owl.stealth = 4
owl.survival = 2
owl.arcane = 2
owl.essence = 6
owl.add_source("M20 Core", 335)
owl.save()
owl.add_advantage(wings, 4)
owl.add_advantage(nightsight, 1)
owl.add_advantage(empathic_bond, 2)
owl.charms.set(SpiritCharm.objects.filter(name__in=["Airt Sense"]))

# Snake Familiar (Life Magic)
snake = Companion.objects.get_or_create(
    name="Ouroboros (Serpent Familiar)",
    companion_type="familiar",
)[0]
snake.description = (
    "A large python with hypnotic patterns. Grants understanding of Life magic "
    "and the cycles of transformation."
)
snake.nature = loner
snake.demeanor = loner
snake.strength = 2
snake.dexterity = 3
snake.stamina = 3
snake.charisma = 2
snake.manipulation = 3
snake.appearance = 3
snake.perception = 4
snake.intelligence = 2
snake.wits = 3
snake.willpower = 5
snake.alertness = 3
snake.athletics = 2
snake.brawl = 3
snake.stealth = 4
snake.survival = 3
snake.arcane = 1
snake.essence = 5
snake.add_source("M20 Core", 335)
snake.save()
snake.add_advantage(claws, 5)  # Venomous fangs
snake.add_advantage(flexibility, 2)
snake.add_advantage(empathic_bond, 2)

# ===== HOMUNCULUS FAMILIARS =====

# Alchemical Homunculus
homunculus = Companion.objects.get_or_create(
    name="Paracelsus (Homunculus)",
    companion_type="familiar",
)[0]
homunculus.description = (
    "A tiny humanoid creature created through alchemy, standing 8 inches tall. "
    "Assists with laboratory work and can perform simple tasks."
)
homunculus.nature = caregiver
homunculus.demeanor = caregiver
homunculus.strength = 1
homunculus.dexterity = 3
homunculus.stamina = 2
homunculus.charisma = 2
homunculus.manipulation = 2
homunculus.appearance = 2
homunculus.perception = 3
homunculus.intelligence = 3
homunculus.wits = 3
homunculus.willpower = 4
homunculus.alertness = 2
homunculus.crafts = 3
homunculus.science = 2
homunculus.occult = 2
homunculus.arcane = 3
homunculus.essence = 4
homunculus.add_source("Book of Secrets", 79)
homunculus.save()
homunculus.add_advantage(human_speech, 2)
homunculus.add_advantage(empathic_bond, 2)

# ===== SPIRIT FAMILIARS =====

# Fire Elemental Familiar
fire_spirit = Companion.objects.get_or_create(
    name="Ignis (Fire Spirit Familiar)",
    companion_type="familiar",
)[0]
fire_spirit.description = (
    "A minor fire elemental bound as a familiar. Appears as a dancing flame "
    "or a small salamander made of fire. Grants power over Forces magic."
)
fire_spirit.nature = explorer
fire_spirit.demeanor = trickster
fire_spirit.strength = 2
fire_spirit.dexterity = 4
fire_spirit.stamina = 3
fire_spirit.charisma = 3
fire_spirit.manipulation = 2
fire_spirit.appearance = 3
fire_spirit.perception = 3
fire_spirit.intelligence = 2
fire_spirit.wits = 4
fire_spirit.willpower = 5
fire_spirit.rage = 6
fire_spirit.essence = 8
fire_spirit.gnosis = 5
fire_spirit.arcane = 2
fire_spirit.add_source("M20 Core", 336)
fire_spirit.save()
fire_spirit.add_advantage(empathic_bond, 2)
fire_spirit.charms.set(SpiritCharm.objects.filter(name__in=["Blast", "Materialize"]))

# Air Elemental Familiar
air_spirit = Companion.objects.get_or_create(
    name="Zephyr (Air Spirit Familiar)",
    companion_type="familiar",
)[0]
air_spirit.description = (
    "A minor air elemental that appears as a swirling breeze or a translucent "
    "winged figure. Swift and elusive, grants mastery over wind and flight."
)
air_spirit.nature = explorer
air_spirit.demeanor = explorer
air_spirit.strength = 1
air_spirit.dexterity = 5
air_spirit.stamina = 2
air_spirit.charisma = 3
air_spirit.manipulation = 3
air_spirit.appearance = 3
air_spirit.perception = 4
air_spirit.intelligence = 3
air_spirit.wits = 5
air_spirit.willpower = 4
air_spirit.rage = 3
air_spirit.essence = 7
air_spirit.gnosis = 6
air_spirit.arcane = 3
air_spirit.add_source("M20 Core", 336)
air_spirit.save()
air_spirit.add_advantage(alacrity, 4)
air_spirit.add_advantage(empathic_bond, 2)
air_spirit.charms.set(
    SpiritCharm.objects.filter(name__in=["Create Wind", "Updraft", "Materialize"])
)

# ===== UNIQUE/SPECIALIZED COMPANIONS =====

# Cybernetic Familiar (Virtual Adept)
cyber_cat = Companion.objects.get_or_create(
    name="Bit (Cybernetic Cat)",
    companion_type="familiar",
)[0]
cyber_cat.description = (
    "A cat enhanced with cybernetic implants and nanocircuitry. Can interface "
    "with computer systems and navigate the Digital Web."
)
cyber_cat.nature = trickster
cyber_cat.demeanor = loner
cyber_cat.strength = 1
cyber_cat.dexterity = 4
cyber_cat.stamina = 3
cyber_cat.charisma = 3
cyber_cat.manipulation = 3
cyber_cat.appearance = 3
cyber_cat.perception = 4
cyber_cat.intelligence = 3
cyber_cat.wits = 4
cyber_cat.willpower = 5
cyber_cat.alertness = 3
cyber_cat.athletics = 2
cyber_cat.brawl = 2
cyber_cat.computer = 3
cyber_cat.stealth = 4
cyber_cat.technology = 2
cyber_cat.arcane = 2
cyber_cat.essence = 6
cyber_cat.add_source("Lore of the Traditions", 189)
cyber_cat.save()
cyber_cat.add_advantage(nightsight, 1)
cyber_cat.add_advantage(claws, 3)
cyber_cat.add_advantage(empathic_bond, 2)

# Ancestor Spirit Guide (Euthanatos)
ancestor = Companion.objects.get_or_create(
    name="Elder Wisdom (Ancestor Spirit)",
    companion_type="familiar",
)[0]
ancestor.description = (
    "The spirit of an ancient Euthanatos master, appearing as a translucent "
    "figure in robes. Provides guidance on death, fate, and the Wheel."
)
ancestor.nature = sage
ancestor.demeanor = sage
ancestor.strength = 0
ancestor.dexterity = 2
ancestor.stamina = 0
ancestor.charisma = 4
ancestor.manipulation = 3
ancestor.appearance = 3
ancestor.perception = 5
ancestor.intelligence = 5
ancestor.wits = 4
ancestor.willpower = 8
ancestor.rage = 1
ancestor.essence = 12
ancestor.gnosis = 8
ancestor.awareness = 4
ancestor.cosmology = 4
ancestor.esoterica = 5
ancestor.occult = 5
ancestor.arcane = 4
ancestor.add_source("Lore of the Traditions", 109)
ancestor.save()
ancestor.add_advantage(empathic_bond, 2)
ancestor.charms.set(
    SpiritCharm.objects.filter(
        name__in=["Mind Speech", "Materialize", "Airt Sense", "Realm Sense"]
    )
)

# Plant Familiar (Verbena)
plant = Companion.objects.get_or_create(
    name="Thornrose (Animated Plant)",
    companion_type="familiar",
)[0]
plant.description = (
    "A sentient rosebush animated through Verbena life magic. Can move slowly "
    "and has thorny vines for defense."
)
plant.nature = caregiver
plant.demeanor = loner
plant.strength = 3
plant.dexterity = 1
plant.stamina = 4
plant.charisma = 1
plant.manipulation = 1
plant.appearance = 3
plant.perception = 2
plant.intelligence = 1
plant.wits = 2
plant.willpower = 4
plant.alertness = 2
plant.brawl = 2
plant.survival = 3
plant.essence = 5
plant.gnosis = 4
plant.arcane = 2
plant.add_source("Lore of the Traditions", 169)
plant.save()
plant.add_advantage(armor, 2)
plant.add_advantage(claws, 3)  # Thorns
plant.add_advantage(empathic_bond, 2)
plant.charms.set(SpiritCharm.objects.filter(name__in=["Cleanse the Blight"]))

# ===== NON-FAMILIAR COMPANIONS =====

# Acolyte Student
acolyte = Companion.objects.get_or_create(
    name="Aspiring Apprentice",
    companion_type="companion",
)[0]
acolyte.description = (
    "A young student of magic who has not yet Awakened but shows great potential. "
    "Assists with research and can perform minor tasks."
)
acolyte.nature = explorer
acolyte.demeanor = caregiver
acolyte.strength = 2
acolyte.dexterity = 2
acolyte.stamina = 2
acolyte.charisma = 3
acolyte.manipulation = 2
acolyte.appearance = 3
acolyte.perception = 3
acolyte.intelligence = 4
acolyte.wits = 3
acolyte.willpower = 5
acolyte.alertness = 2
acolyte.awareness = 2
acolyte.academics = 3
acolyte.computer = 2
acolyte.esoterica = 2
acolyte.occult = 3
acolyte.research = 3
acolyte.science = 2
acolyte.arcane = 1
acolyte.avatar = 1
acolyte.add_source("M20 Core", 337)
acolyte.save()

# Consors (Awakened Companion)
consors = Companion.objects.get_or_create(
    name="Loyal Consors",
    companion_type="companion",
)[0]
consors.description = (
    "An Awakened individual who has not received formal training but assists "
    "the mage. Has basic magical awareness and can help with rituals."
)
consors.nature = caregiver
consors.demeanor = caregiver
consors.strength = 2
consors.dexterity = 3
consors.stamina = 3
consors.charisma = 3
consors.manipulation = 2
consors.appearance = 3
consors.perception = 3
consors.intelligence = 3
consors.wits = 3
consors.willpower = 6
consors.alertness = 2
consors.awareness = 3
consors.brawl = 2
consors.drive = 2
consors.esoterica = 2
consors.occult = 2
consors.stealth = 2
consors.streetwise = 2
consors.arcane = 2
consors.avatar = 2
consors.add_source("M20 Core", 337)
consors.save()

# Technocratic Assistant
tech_assistant = Companion.objects.get_or_create(
    name="Field Technician",
    companion_type="companion",
)[0]
tech_assistant.description = (
    "A trained Technocratic field agent who assists with operations. "
    "Skilled in technology and maintains equipment."
)
tech_assistant.nature = loner
tech_assistant.demeanor = caregiver
tech_assistant.strength = 3
tech_assistant.dexterity = 3
tech_assistant.stamina = 3
tech_assistant.charisma = 2
tech_assistant.manipulation = 3
tech_assistant.appearance = 2
tech_assistant.perception = 3
tech_assistant.intelligence = 3
tech_assistant.wits = 3
tech_assistant.willpower = 5
tech_assistant.alertness = 3
tech_assistant.athletics = 2
tech_assistant.brawl = 2
tech_assistant.computer = 3
tech_assistant.drive = 2
tech_assistant.firearms = 3
tech_assistant.science = 3
tech_assistant.technology = 4
tech_assistant.requisitions = 2
tech_assistant.add_source("Technocracy Reloaded", 138)
tech_assistant.save()
