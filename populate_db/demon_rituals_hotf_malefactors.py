"""
Populate database with Malefactor (Annunaki) rituals from Houses of the Fallen.
"""

from characters.models.demon.ritual import Ritual

from populate_db.demon_houses import malefactors
from populate_db.demon_lores import (
    lore_of_the_celestials as lore_celestials,
    lore_of_the_earth as lore_earth,
    lore_of_the_firmament as lore_firmament,
    lore_of_flame,
    lore_of_the_forge as lore_forge,
    lore_of_paths as lore_paths,
    lore_of_the_realms as lore_realms,
)

# =============================================================================
# MALEFACTOR RITUALS - HOUSES OF THE FALLEN
# =============================================================================

volcano = Ritual.objects.get_or_create(
    name="Volcano",
    house=malefactors,
)[0]
volcano.primary_lore = lore_earth
volcano.primary_lore_rating = 5
volcano.secondary_lore_requirements = [
    {"lore_id": lore_flame.id, "rating": 2},
]
volcano.base_cost = 14
volcano.minimum_casting_time = 49
volcano.restrictions = "The sigil for this ritual must be carved into solid ground, either earth or natural stone (not concrete)."
volcano.system = """Roll Strength + Survival. If the roll succeeds, a volcano grows from the ritual's sigil, a massive cone of earth that spouts molten lava for a number of hours equal to the successes gained. The lava moves slowly in an ever-expanding radius and causes great damage to the surrounding area. The Ankida cannot control the spread of the lava once the volcano begins to erupt.

Each hour, the radius affected increases by a number of yards equal to 100 times the successes of the ritual. (So with three successes, the lava would spread out another 300 yards each hour.) Almost all objects in the area will be destroyed, including buildings and vehicles, once they come into contact with the lava.

Any character in contact with the lava suffers a number of lethal damage levels each turn equal to the successes rolled, which cannot be soaked by armor.

When the ritual's effect ends, the volcano crumbles in on itself and the lava cools unnaturally quickly, leaving behind a lake of coarse, brittle stone about an hour later."""
volcano.torment_effect = """The high-Torment version of this ritual produces lava steaming with corruption and radioactive toxins, jetting from the volcano high into the air. The corrupt lava expands much faster than normal. The radius affected increases by a mile each hour, regardless of the successes rolled. When the ritual ends, the lava stays hot and will take several days to cool. Furthermore, its corrupt nature poisons the earth beneath it, rendering it permanently toxic and polluted."""
volcano.variations = "One version of this ritual also produces a cloud of smoke and ash that jets from the volcano, blotting out all light for a number of miles around equal to the successes rolled. Add Lore of the Winds ••• to the secondary lore requirements."
volcano.flavor_text = "The Malefactors were not created to control fire, but they worked hand in hand with the Heralds before the Fall, crafting the lava underpinnings and molten heart of the earth. With this ritual, the Ankida and her assistants can rekindle the planet's burning blood, bringing it to the earth's face — there to erupt, spewing molten lava and rivers of fire out onto the surface."
volcano.source_page = "Houses of the Fallen, p. 83"
volcano.save()

hunters_byway = Ritual.objects.get_or_create(
    name="Hunter's Byway",
    house=malefactors,
)[0]
hunters_byway.primary_lore = lore_paths
hunters_byway.primary_lore_rating = 2
hunters_byway.secondary_lore_requirements = [
    {"lore_id": lore_firmament.id, "rating": 2},
    {"lore_id": lore_realms.id, "rating": 2},
]
hunters_byway.base_cost = 18
hunters_byway.minimum_casting_time = 36
hunters_byway.restrictions = "The item used as a focus must be placed in the center of the ritual's sigil."
hunters_byway.system = """Roll Wits + Survival. If the ritual succeeds, a pathway visible to all the participants but not to observers appears leading from the sigil, and fading from view a few yards away. If someone follows the path, she passes into the spirit realm. From the outside, she simply fades from view, while from her perspective, she moves down a luminous, misty tunnel surrounded by darkness.

Movement along the path is not instantaneous. It takes a base of 10 minutes, minus one minute for each success on the ritual roll, to reach the other end and exit back into reality. The traveler appears just behind the person being hunted, who will probably be taken by surprise. He must gain more successes on a Perception + Awareness roll than the successes of the ritual to notice his pursuer arrive.

Once the traveler exits the path, it collapses, and she must find her own way back to the ritual site if she wishes to return."""
hunters_byway.torment_effect = """The high-Torment version appears to work as normal, but it is actually far more dangerous. The pathway actually stays open for a number of hours equal to the successes rolled — hours in which any ghost or spirit that happens upon the path through the realms can exit at either end and wreak havoc."""
hunters_byway.variations = "None"
hunters_byway.flavor_text = "This ritual is used to track down missing persons or demons — whether they are simply lost or actively hiding from the Ankida. The ritual is focused on an item that belongs to the person being sought and that has a degree of significance. The ritual creates a path through the spirit realms, bypassing the physical world and exiting back into reality just behind the person being hunted."
hunters_byway.source_page = "Houses of the Fallen, p. 83"
hunters_byway.save()

chalice_of_faith = Ritual.objects.get_or_create(
    name="Chalice of Faith",
    house=malefactors,
)[0]
chalice_of_faith.primary_lore = lore_forge
chalice_of_faith.primary_lore_rating = 5
chalice_of_faith.secondary_lore_requirements = [
    {"lore_id": lore_celestials.id, "rating": 5},
]
chalice_of_faith.base_cost = 20
chalice_of_faith.minimum_casting_time = 100
chalice_of_faith.restrictions = "The item to be affected must be placed in the center of the ritual's sigil. This item must be specially prepared by the Ankida ahead of time."
chalice_of_faith.system = """Roll Charisma + Crafts (difficulty 7). Success means that the item's spiritual nature is permanently altered, making it a storehouse for Faith. The chalice can hold a maximum number of temporary Faith points equal to the successes gained on the evocation.

To place Faith into a chalice, the wielder makes a Faith roll (difficulty 7). Each success transfers a point from her temporary pool to the chalice. Withdrawing Faith works in a similar fashion. The user makes a Faith roll (difficulty 7), and each success draws a point from the chalice into character's pool, up to his normal limit. The chalice can only be used once in each fashion per scene (one deposit, one withdrawal).

Chalices have a very unusual spiritual nature, and they stand out to a demon's supernatural awareness (difficulty 7 to detect), but the observer will only know what the item actually does by gaining five successes on a detection roll."""
chalice_of_faith.torment_effect = """The high-Torment version of this ritual creates a poisoned chalice, a relic that taints whatever Faith it contains. Whenever a demon draws Faith from a tainted chalice, he gains a point of temporary Torment for each Faith point he takes."""
chalice_of_faith.variations = "None"
chalice_of_faith.flavor_text = "Faith is the lifeblood of the fallen, a precious commodity that becomes even more valuable because of its scarcity. Faith can only be generated by mortal worshippers, and it cannot be stored, preserved or channeled to another demon — or so most demons believe. The Malefactors, though, know differently, for they made an incredible discovery in the closing hours of the Shattering — a ritual that could store Faith in an object!"
chalice_of_faith.source_page = "Houses of the Fallen, p. 84"
chalice_of_faith.save()

print("Malefactor (Annunaki) rituals from Houses of the Fallen loaded successfully")
