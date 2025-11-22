"""
Populate database with Devourer (Rabisu) relics from Houses of the Fallen.
These are house-specific relics for the Sixth House.
"""

from items.models.demon.relic import Relic
from populate_db.demon_houses import devourers

# =============================================================================
# DEVOURER HOUSE RELICS - HOUSES OF THE FALLEN
# =============================================================================

caul_of_rest = Relic.objects.get_or_create(
    name="Caul of Rest",
    house=devourers,
    relic_type="house_specific",
    lore_used="Lore of the Beast, Lore of Awakening",
    power="Transparent membrane placed over body; renders target deathlike and comatose; 8 dice pool vs target's Willpower (diff 8); subject feels no pain, requires little oxygen/food, ages slowly; Perception+Medicine (diff 8) to detect life; lasts until removed; reusable after 24 hours",
    material="Tough transparent membrane",
    dice_pool=8,
    difficulty=9,
)[0]
caul_of_rest.add_source("Houses of the Fallen", 157)

mask_of_zaltu = Relic.objects.get_or_create(
    name="Mask of Zaltu",
    house=devourers,
    relic_type="house_specific",
    lore_used="Lore of the Beast",
    power="Animal face mask; transforms wearer into specific animal form; 8 dice pool; difficulty varies by size (4-8); transformation lasts scene; usable 5 times per day; cannot be worn by mortals; user can evoke while transformed",
    material="Animal fur, fangs, or natural materials",
    dice_pool=8,
    difficulty=6,
)[0]
mask_of_zaltu.add_source("Houses of the Fallen", 157)

panacea = Relic.objects.get_or_create(
    name="Panacea",
    house=devourers,
    relic_type="house_specific",
    lore_used="Lore of Awakening",
    power="Jewelry or charm that prevents pain from wounds; 6 dice pool (diff 6); each success reduces wound penalties by 1; effects last for scene; cannot be reactivated same scene",
    material="Jewelry or charm",
    dice_pool=6,
    difficulty=6,
)[0]
panacea.add_source("Houses of the Fallen", 158)

wildsong = Relic.objects.get_or_create(
    name="Wildsong",
    house=devourers,
    relic_type="house_specific",
    lore_used="Lore of the Beast",
    power="Panpipes or flute; possesses and controls animals via bound demon spirit; 8 dice pool; controls animals within 5 mile radius; control lasts 5 turns, extendable; contains demon with Possess Animals evocation",
    material="Rustic pipes or flutes",
    dice_pool=8,
    difficulty=7,
)[0]
wildsong.add_source("Houses of the Fallen", 158)

sinews_of_speed = Relic.objects.get_or_create(
    name="Sinews of Speed",
    house=devourers,
    relic_type="house_specific",
    lore_used="Lore of the Beast, Lore of the Forge",
    power="Wrappings made from predator tendons; grants multiple actions in combat; spend Faith points for extra actions up to Faith score; only usable by demons; active for one scene",
    material="Tendons and sinews from agile predator",
    dice_pool=0,
    difficulty=7,
)[0]
sinews_of_speed.add_source("Houses of the Fallen", 159)

thicket_dust = Relic.objects.get_or_create(
    name="Thicket Dust",
    house=devourers,
    relic_type="house_specific",
    lore_used="Lore of the Wild",
    power="Golden-green sand causing explosive plant growth; 12 dice pool (diff 7); plants increase by cubic yards equal to successes; growth in 1 turn; Strength equal to successes for damage; lasts 1 scene or permanent with Willpower; single use",
    material="Fine golden-green sand",
    dice_pool=12,
    difficulty=7,
)[0]
thicket_dust.add_source("Houses of the Fallen", 160)

unerring_map = Relic.objects.get_or_create(
    name="Unerring Map",
    house=devourers,
    relic_type="house_specific",
    lore_used="Lore of the Wild, Lore of the Firmament",
    power="Papyrus or hide roll showing detailed terrain map; 6 dice pool; diff 6 wilderness/8 urban; shows 1+ miles radius; natural features brown, people gold, animals green, demons red (Willpower diff 7 to avoid); lasts 1 scene; usable 3 times per day",
    material="Papyrus or tanned hide",
    dice_pool=6,
    difficulty=6,
)[0]
unerring_map.add_source("Houses of the Fallen", 160)

