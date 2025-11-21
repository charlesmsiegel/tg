"""
Populate database with Devil (Namaru) relics from Houses of the Fallen.
These are house-specific relics for the First House.
"""

from items.models.demon.relic import Relic

from populate_db.demon_houses import devils

# =============================================================================
# DEVIL HOUSE RELICS - HOUSES OF THE FALLEN
# =============================================================================

subtle_knives = Relic.objects.get_or_create(
    name="Subtle Knives",
    house=devils,
    relic_type="house_specific",
    lore_used="Lore of the Spirit, Lore of Radiance, Lore of the Forge",
    power="Weapon disguised as mundane object; strikes the soul while leaving body unharmed; damage soaked with Wits not Stamina",
    material="Mundane object infused with weapon's spiritual properties",
    dice_pool=0,  # Weapon dependent
    difficulty=6,
)[0]
subtle_knives.add_source("Houses of the Fallen", 24)

marchocias_chime = Relic.objects.get_or_create(
    name="Marchocias' Chime of Repentance",
    house=devils,
    relic_type="ancient",
    lore_used="Unknown",
    power="15-foot silver and crystal chime weighing 2 tons; prevents violence and anger within hearing range; duration 10 x permanent Faith minutes; -1 difficulty to Manipulation rolls against affected",
    material="Silver and precious stones",
    dice_pool=0,  # Based on Performance roll
    difficulty=7,
    complexity=10,
    is_permanent=True,
)[0]
marchocias_chime.add_source("Houses of the Fallen", 25)

dawnrunner = Relic.objects.get_or_create(
    name="The Dawnrunner (Lucifer's Warhorse)",
    house=devils,
    relic_type="ancient",
    lore_used="Lore of Radiance (created by Lucifer)",
    power="Stallion of living light and flame; travels 1000 miles per success on Faith roll; linked to White Horse of Uffington chalk figure; grants temporary Torment each use",
    material="Radiance and sunlight given form; ancient bit and bridle",
    dice_pool=0,  # Based on Faith roll
    difficulty=6,
    complexity=10,
    is_permanent=True,
)[0]
dawnrunner.add_source("Houses of the Fallen", 26)

armor_of_mercy = Relic.objects.get_or_create(
    name="Armor of Mercy",
    house=devils,
    relic_type="house_specific",
    lore_used="Lore of Humanity, Lore of the Celestials, Lore of Longing",
    power="Normal clothing enchanted to make attackers viscerally understand pain they will inflict; mortals must make Willpower roll (diff 9) to attack; demons gain temporary Torment if they strike; attackers lose 1 die from all pools for scene",
    material="Normal clothing (no armor bonus)",
    dice_pool=0,
    difficulty=9,
)[0]
armor_of_mercy.add_source("Houses of the Fallen", 26)

print("Devil (Namaru) relics from Houses of the Fallen loaded successfully")
