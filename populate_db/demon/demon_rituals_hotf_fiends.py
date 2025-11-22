"""
Populate database with Fiend (Neberu) rituals from Houses of the Fallen.
"""

from characters.models.demon.ritual import Ritual
from populate_db.demon.demon_houses import fiends
from populate_db.demon.demon_lores import lore_of_patterns as lore_patterns
from populate_db.demon.demon_lores import lore_of_portals as lore_portals

# =============================================================================
# FIEND RITUALS - HOUSES OF THE FALLEN
# =============================================================================

eternal_imprisonment = Ritual.objects.get_or_create(
    name="Ritual of Eternal Imprisonment",
    house=fiends,
)[0]
eternal_imprisonment.primary_lore = lore_portals
eternal_imprisonment.primary_lore_rating = 5
eternal_imprisonment.secondary_lore_requirements = [
    {"lore_id": lore_patterns.id, "rating": 5},
    {"lore_id": lore_portals.id, "rating": 2},
]
eternal_imprisonment.base_cost = 36
eternal_imprisonment.minimum_casting_time = 144
eternal_imprisonment.restrictions = "The subject of this ritual is placed in a metal rectangular container, and this container is placed in the center of the sigil. This ritual requires at least seven fallen who possess Lore of Patterns ••••• because of the difficulty of completely freezing time around the box in the center of the sigil, but there is still only one Ankida."
eternal_imprisonment.system = """Roll Intelligence + Science (difficulty 8). The victim resists by using Willpower. If the Ankida is successful, the victim disappears from view, never to be seen again. The being is frozen in time, and as the Earth speeds away through space in its rotation and revolution, the victim becomes lost in the vast eternity of space - an eternity locked in solitary confinement with no hope of release, escape or death.

If the Ankida's roll fails, the ritual ends immediately and must be started again.

If the ritual botches, however, there is a risk that the temporal bubble meant to contain the prisoner will claim his jailers instead. Make a Willpower roll for every person involved in the ritual against a difficulty of 8. If the roll fails, the person disappears. The good news is that the effects on the hapless participant are not permanent. The individual will return to the time stream at some point, but cannot control when or where her return will occur. The Storyteller is the final arbiter on the time and location of the victim's return, and he can choose arbitrarily when and where the event happens."""
eternal_imprisonment.torment_effect = "None"
eternal_imprisonment.variations = "There are rumors that the ritual could be performed with seven Mudu with Lore of Portals ••••, which would permit the prisoner to be teleported back to reality after a specific length of time had passed or a certain set of conditions had been met."
eternal_imprisonment.flavor_text = "This nightmarish ritual was created in the last days of the war as a means of striking fear into the hearts of enemy angels. It was only used twice, and so horrific were its effects that all but the most hardened fallen cried out against it ever being used again. In fact, some fallen think that it was the use of this ritual that caused the Creator to cast the rebels into the Abyss. The ritual was thought to be lost, until one of the books of Gaar-Asok turned up with the details of the ritual mentioned inside."
eternal_imprisonment.source_page = "Houses of the Fallen, p. 106"
eternal_imprisonment.save()

