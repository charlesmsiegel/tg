"""
Populate database with Defiler (Lammasu) relics from Houses of the Fallen.
These are house-specific relics for the Fifth House.
"""

from items.models.demon.relic import Relic

from populate_db.demon_houses import defilers

# =============================================================================
# DEFILER HOUSE RELICS - HOUSES OF THE FALLEN
# =============================================================================

lyruphams_robe = Relic.objects.get_or_create(
    name="Lyrupham's Robe",
    house=defilers,
    relic_type="ancient",
    lore_used="Unknown",
    power="Shimmering robe of greens, blues, browns trimmed with liquid marble; reduces difficulty of Empathy, Intuition, Leadership and Performance rolls by 1 when activated",
    material="Diaphanous material with shifting colors",
    dice_pool=0,
    difficulty=7,
    complexity=9,
    is_permanent=True,
)[0]
lyruphams_robe.add_source("Houses of the Fallen", 127)

chant_of_life_long_passing = Relic.objects.get_or_create(
    name="The Chant of Life Long Passing",
    house=defilers,
    relic_type="house_specific",
    lore_used="Lore of Longing",
    power="Complex Enochian composition; mortals hearing it are immune to mind control and gain -1 difficulty to Willpower rolls for scene; mortals cannot perform ancient form; rumored healing variation removes derangements",
    material="Musical composition in Enochian",
    dice_pool=0,
    difficulty=8,
)[0]
chant_of_life_long_passing.add_source("Houses of the Fallen", 128)

iesus_caul = Relic.objects.get_or_create(
    name="Iesu's Caul",
    house=defilers,
    relic_type="ancient",
    lore_used="Unknown",
    power="Half-fossilized birth caul; protects owner and blood-bonded individuals from storms and rough seas; -2 difficulty to Athletics/Survival for swimming; negates storm damage; lasts days equal to owner's Faith; no range limit",
    material="Fossilized birth caul",
    dice_pool=0,
    difficulty=7,
    complexity=8,
    is_permanent=True,
)[0]
iesus_caul.add_source("Houses of the Fallen", 128)

jacincatis_trident = Relic.objects.get_or_create(
    name="Jacincati's Trident (Bane of Angels)",
    house=defilers,
    relic_type="ancient",
    lore_used="Lore of Storms",
    power="Obsidian trident with shark hide grip; inflicts Strength+2 lethal normally; when activated inflicts Strength+2 aggravated damage; penetrates mundane armor; only relic armor can soak; emits magnetic field disrupting electronics in Faith yards radius",
    material="Obsidian with shark hide",
    dice_pool=0,
    difficulty=7,
    complexity=9,
    is_permanent=True,
)[0]
jacincatis_trident.add_source("Houses of the Fallen", 129)

man_beside_tree = Relic.objects.get_or_create(
    name="Man Beside a Tree",
    house=defilers,
    relic_type="ancient",
    lore_used="Unknown",
    power="Life-size sculpture from kiatum (pliable rock at 480°F); retains heat indefinitely; reliquary of Earthbound Basirajkael; contains portions of Belial's True Name; causes aggravated damage from heat; requires extensive cooling system",
    material="Kiatum (heated rock)",
    dice_pool=0,
    difficulty=10,
    complexity=10,
    is_permanent=True,
)[0]
man_beside_tree.add_source("Houses of the Fallen", 129)

manacles_of_ashmael = Relic.objects.get_or_create(
    name="The Manacles of Ashmael",
    house=defilers,
    relic_type="house_specific",
    lore_used="Lore of the Spirit, Lore of the Firmament",
    power="Crystal manacles bonding captive to captor; captor knows captive's location and can read thoughts with Perception+Awareness (diff 7); only demons can activate; captor can release with touch; breaking requires 10 dice soak, 6 health levels, damages wearer with aggravated damage",
    material="Crystal manacles",
    dice_pool=10,
    difficulty=7,
)[0]
manacles_of_ashmael.add_source("Houses of the Fallen", 129)

tears_of_tiamat = Relic.objects.get_or_create(
    name="The Tears of Tiamat",
    house=defilers,
    relic_type="ancient",
    lore_used="Lore of Longing",
    power="Black crystalline spheres 1 inch diameter; worn against skin grants +1 Manipulation; in eye socket grants +1 Charisma and dream manipulation (Manipulation+Intuition vs Willpower; effects last Faith days); mortals cannot become thralls while affected",
    material="Black crystal",
    dice_pool=0,
    difficulty=7,
    complexity=9,
    is_permanent=True,
)[0]
tears_of_tiamat.add_source("Houses of the Fallen", 130)

print("Defiler (Lammasu) relics from Houses of the Fallen loaded successfully")
