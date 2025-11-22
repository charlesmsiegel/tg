"""
Populate database with Slayer (Halaku) relics from Houses of the Fallen.
These are house-specific relics for the Seventh House.
"""

from items.models.demon.relic import Relic
from populate_db.demon.demon_houses import slayers

# =============================================================================
# SLAYER HOUSE RELICS - HOUSES OF THE FALLEN
# =============================================================================

havens_gate = Relic.objects.get_or_create(
    name="Haven's Gate",
    house=slayers,
    relic_type="ancient",
    lore_used="Lore of the Realms, Lore of the Spirit",
    power="15-foot tall gates of dark metal; allows instantaneous transit through Veil into shadow lands; demons in apocalyptic form can spot with Perception+Awareness (diff 9); requires Faith/Willpower point to cross; subject to Maelstrom dangers",
    material="Dark metallic substance that absorbs light",
    dice_pool=0,
    difficulty=9,
    complexity=10,
    is_permanent=True,
)[0]
havens_gate.add_source("Houses of the Fallen", 188)

deaths_promise = Relic.objects.get_or_create(
    name="Death's Promise",
    house=slayers,
    relic_type="house_specific",
    lore_used="Lore of Death, Lore of the Spirit",
    power="Amber and silver amulet; changes color when wearer in mortal danger; binds soul to amulet on death; teleports to secure location (original: City of the Dead); modern recreations possible",
    material="Amber in silver circlet on platinum chain",
    dice_pool=0,
    difficulty=7,
)[0]
deaths_promise.add_source("Houses of the Fallen", 188)

soul_anchor = Relic.objects.get_or_create(
    name="Soul Anchor",
    house=slayers,
    relic_type="house_specific",
    lore_used="Lore of Death, Lore of the Spirit",
    power="Large stone block carved as recumbent human; draws spirits of newly dead within miles; holds 15 souls; activated by Faith points (1-3); range = Faith points in miles; used in war and modern times for capturing souls",
    material="Carved stone block",
    dice_pool=0,
    difficulty=7,
)[0]
soul_anchor.add_source("Houses of the Fallen", 188)

madisels_scythe = Relic.objects.get_or_create(
    name="Madisel's Scythe",
    house=slayers,
    relic_type="ancient",
    lore_used="Lore of Death (reshaped by Lucifer)",
    power="Scythe reshaped by Lucifer's touch; inflicts Strength+3 lethal normally; when activated inflicts Strength+3 aggravated with Extinguish Life effect; ignores all armor except halved relic armor; victims burn to death; inspires mortals to violence",
    material="Metal reshaped by Lucifer",
    dice_pool=0,
    difficulty=7,
    complexity=10,
    is_permanent=True,
)[0]
madisels_scythe.add_source("Houses of the Fallen", 189)

havens_light = Relic.objects.get_or_create(
    name="Haven's Light",
    house=slayers,
    relic_type="house_specific",
    lore_used="Lore of the Spirit, Lore of Paths",
    power="Black iron lantern with spirit candle; reveals calm path through Sea of Death/Tempest; path visible only with open shutter; allows navigation to Haven's islands; works for groups of 10 or less",
    material="Black iron-like substance lantern",
    dice_pool=0,
    difficulty=8,
)[0]
havens_light.add_source("Houses of the Fallen", 189)

siklos = Relic.objects.get_or_create(
    name="Siklos (Charon's Scythe)",
    house=slayers,
    relic_type="ancient",
    lore_used="Lore of Death, Lore of the Spirit (forged from souls)",
    power="Scythe forged from 3 willing human warrior souls; charges with Faith from ghosts (up to 10); activated inflicts Strength+3 aggravated (Strength+5 with Faith spent); -2 to hit/wound; ignores all armor; unsokeable; only works in Haven",
    material="Souls of three human warriors",
    dice_pool=0,
    difficulty=7,
    complexity=10,
    is_permanent=True,
)[0]
siklos.add_source("Houses of the Fallen", 190)

