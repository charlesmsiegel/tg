"""
Populate database with Fiend (Neberu) relics from Houses of the Fallen.
These are house-specific relics for the Fourth House.
"""

from characters.models.demon.house import DemonHouse
from items.models.demon.relic import Relic

# Get the Fiends house
fiends = DemonHouse.objects.get(name="Fiends")

# =============================================================================
# FIEND HOUSE RELICS - HOUSES OF THE FALLEN
# =============================================================================

duality_scrolls = Relic.objects.get_or_create(
    name="Duality Scrolls",
    house=fiends,
    relic_type="house_specific",
    lore_used="Lore of Portals",
    power="Pair of scrolls/books; writing on master appears on slave; information vanishes after moments; slave can be erased with Faith point; modern versions include journals and newspapers",
    material="Matched pair of paper items",
    dice_pool=0,
    difficulty=7,
)[0]
duality_scrolls.add_source("Houses of the Fallen", 104)

bottomless_satchels = Relic.objects.get_or_create(
    name="Bottomless Satchels",
    house=fiends,
    relic_type="house_specific",
    lore_used="Lore of Portals, Lore of the Forge",
    power="Container with unlimited storage space in pocket dimension; must fit through opening; only demons can open (Faith point); structural damage renders useless and destroys contents; container has no weight increase",
    material="Sturdy container (bag, box, etc.)",
    dice_pool=0,
    difficulty=8,
)[0]
bottomless_satchels.add_source("Houses of the Fallen", 105)

armor_of_portals = Relic.objects.get_or_create(
    name="Armor of Portals",
    house=fiends,
    relic_type="ancient",
    lore_used="Lore of Portals",
    power="Plate mail with mirror-like portal plates; blows strike nothing; only hits between plates cause damage; targeting frame adds +4 difficulty; targeting damaged section adds +2 difficulty; portal plates can shatter leaving gaps",
    material="Mirror-like portal plates in armor frame",
    dice_pool=0,
    difficulty=8,
    complexity=9,
    is_permanent=True,
)[0]
armor_of_portals.add_source("Houses of the Fallen", 105)

gaar_asoks_library = Relic.objects.get_or_create(
    name="Gaar-Asok's Library",
    house=fiends,
    relic_type="ancient",
    lore_used="Unknown",
    power="Books recording words spoken into them; written in First Tongue; waterproof and fireproof; contain invaluable knowledge of the past; volumes scattered around the world; creation secrets lost with Guanli",
    material="Ancient books",
    dice_pool=0,
    difficulty=10,
    complexity=10,
    is_permanent=True,
)[0]
gaar_asoks_library.add_source("Houses of the Fallen", 105)

spider_golems = Relic.objects.get_or_create(
    name="Spider Golems",
    house=fiends,
    relic_type="house_specific",
    lore_used="Lore of Portals, Lore of Patterns",
    power="Semi-precious gemstone that sprouts 8 legs when activated; user sees through its eyes; climbs any surface; activation requires code word in First Tongue plus Faith/Willpower point; deactivates beyond 1 mile range; no attack capability",
    material="Semi-precious gemstone",
    dice_pool=0,
    difficulty=7,
)[0]
spider_golems.add_source("Houses of the Fallen", 105)

print("Fiend (Neberu) relics from Houses of the Fallen loaded successfully")
