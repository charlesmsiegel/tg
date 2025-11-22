"""
Populate database with Slayer (Halaku) rituals from Houses of the Fallen.
"""

from characters.models.demon.ritual import Ritual
from populate_db.demon_houses import slayers
from populate_db.demon_lores import lore_of_death
from populate_db.demon_lores import lore_of_portals as lore_portals
from populate_db.demon_lores import lore_of_storms
from populate_db.demon_lores import lore_of_the_earth as lore_earth
from populate_db.demon_lores import lore_of_the_realms as lore_realms
from populate_db.demon_lores import lore_of_the_spirit as lore_spirit
from populate_db.demon_lores import lore_of_the_winds as lore_winds

# =============================================================================
# SLAYER RITUALS - HOUSES OF THE FALLEN
# =============================================================================

reborn_in_new_skin = Ritual.objects.get_or_create(
    name="Reborn in New Skin",
    house=slayers,
)[0]
reborn_in_new_skin.primary_lore = lore_spirit
reborn_in_new_skin.primary_lore_rating = 5
reborn_in_new_skin.secondary_lore_requirements = [
    {"lore_id": lore_death.id, "rating": 4},
    {"lore_id": lore_winds.id, "rating": 2},
]
reborn_in_new_skin.base_cost = 33
reborn_in_new_skin.minimum_casting_time = 121
reborn_in_new_skin.restrictions = "The ritual may be performed only in an underground chamber, such as a cave or cellar. It also requires a living human and a ghostly soul bound into an object. It will not work on dead bodies or on unfettered ghosts."
reborn_in_new_skin.system = """Roll Stamina + Awareness. The number of successes achieved must be greater than the living man's Willpower. For this reason, most donor bodies are beaten and abused for some time before the ritual takes place. If the roll succeeds, the Ankida can command the two souls to switch places. The ritual forges a link between the two souls, which lasts while both endure.

Should the reborn ever be killed, or his soul removed from his body by supernatural means, the original, bound soul snaps immediately back into the body, returning the replacement spirit to its anchoring object. The reborn ghost gains the Physical Attributes and Appearance of its new body and retains the remainder of its own Attributes and Abilities. The transfer is permanent.

This ritual does not work on demon souls, and will not work on any type of supernatural person or creature."""
reborn_in_new_skin.torment_effect = """The high-Torment version of the ritual puts the two spirits involved through excruciating pain as one dies and the other is reborn. This pain will halve the Willpower of both ghosts and give them both a single derangement each."""
reborn_in_new_skin.variations = "An alternative version of this ritual allows the ghost to reclaim its former features as well as a new body. As the soul slips into its new body, the flesh melts and runs like wax before settling into the original face of the newly resurrected spirit. This variation adds Lore of Transfigurations •••."
reborn_in_new_skin.flavor_text = "This ritual was one of the few useful results of the Slayers' constant experiments to overturn the curse of death. In one sense, the ritual is a failure because it doesn't actually prevent death. It merely takes life from one soul and gives it to another."
reborn_in_new_skin.source_page = "Houses of the Fallen, p. 191"
reborn_in_new_skin.save()

havens_peace = Ritual.objects.get_or_create(
    name="Haven's Peace",
    house=slayers,
)[0]
havens_peace.primary_lore = lore_storms
havens_peace.primary_lore_rating = 4
havens_peace.secondary_lore_requirements = [
    {"lore_id": lore_spirit.id, "rating": 3},
    {"lore_id": lore_earth.id, "rating": 4},
]
havens_peace.base_cost = 33
havens_peace.minimum_casting_time = 121
havens_peace.restrictions = "This ritual can only be carried out in the shadow lands, the portion of Haven closest to the living world."
havens_peace.system = """Roll Intelligence + Science. The difficulty of the roll depends on the strength of the spirit storm at the time the ritual is preformed. It should be between 6 and 9, at the Storyteller's discretion. A single success creates an area of peace 100 yards in radius from the point where the ritual sigil is carved into the ground. Each additional success beyond the first adds an additional 50 yards to the radius.

The spirit storm does not appear within the circle, although any soul that steps outside immediately becomes prey to the flaying effect of the Maelstrom (Demon Storytellers Companion, p. 53)."""
havens_peace.torment_effect = """The high-Torment version of the ritual creates the same area of calm, but with terrible consequences to any ghost within the ritual's effect area. Instead of gently forming around the area of peace, the protective ritual drives all spiritual material out into the Tempest beyond the shadow lands and into the severe Maelstrom blowing there. Any soul caught in this ritual is immediately dropped into the Tempest and suffers five dice of lethal damage per turn until destroyed or rescued."""
havens_peace.variations = "This ritual can also be used to create a fortress within the shadow lands, if required. Adding Lore of Portals •• makes the barriers around the ritual site impervious to demons and ghosts as well as the Maelstrom, as per the Evocation's normal effect."
havens_peace.flavor_text = "This is one of the few new rituals developed since the escape from Hell, based on the old Haven-creation rituals. The Charonist group within the Slayers has reworked one of the old creation rituals used while building Haven to create Haven's Peace. It brings peace and calm to an area of Haven, erecting conceptual barriers against the spirit storm."
havens_peace.source_page = "Houses of the Fallen, p. 191"
havens_peace.save()

veil_of_cerberus = Ritual.objects.get_or_create(
    name="The Veil of Cerberus",
    house=slayers,
)[0]
veil_of_cerberus.primary_lore = lore_realms
veil_of_cerberus.primary_lore_rating = 5
veil_of_cerberus.secondary_lore_requirements = [
    {"lore_id": lore_portals.id, "rating": 4},
]
veil_of_cerberus.base_cost = 18
veil_of_cerberus.minimum_casting_time = 81
veil_of_cerberus.restrictions = "This ritual cannot be cast in the presence of any observers except those participating in, and affected by, the ritual. It also requires a small scrap of dried skin and some fresh blood."
veil_of_cerberus.system = """Roll Stamina + Awareness. The difficulty varies based on the strength of the Veil. It will be 6 in a place like a graveyard or deep in the countryside, 7 or 8 in a village or town, and 9 in a major city. Each success adds another two meters to the radius of area transferred into Haven, from a base of a radius of three meters. Should the number of successes fail to extend the radius far enough to bring everyone within the transfer area, then the ritual fails. Not surprisingly, the ritual is normally conducted in a small, huddled group, just to be on the safe side.

If the ritual succeeds, the area within its effect is enclosed with mist for a few moments. When the mist clears, the whole landscape within the ritual's effect, and all things on it, have crossed the Veil. Back in the living world, the landscape has been replaced with its shadow land equivalents, a gray, lifeless facsimile of what was there before. The landscapes will swap back gradually over a period of several hours."""
veil_of_cerberus.torment_effect = """The high-Torment version of this ritual kills any humans who travel with the demons. They pass over the Veil, but leave their bodies behind. From that point onward, they are treated as normal ghosts. The landscape in the living world never really recovers from the effects of a high-Torment use of the Veil of Cerberus. The ground remains forever barren, and animals avoid it."""
veil_of_cerberus.variations = "In a bid to make things even more difficult for pursuing loyalists, a variation of The Veil of Cerberus was devised which incorporates Lore of Flame ••••. It causes the transferred portion of the shadow lands to burst into a terrible conflagration as it emerges in the living world, blocking the progress of the pursuers and erasing all traces of the fleeing demons. There is a rumor that Lore of Patterns ••••• has also been used, to create a time bomb effect, but no fallen have yet been able to recreate that effect."
veil_of_cerberus.flavor_text = "As the Thousand Year War turned into a rout, the rebel Elohim had to adopt more defensive tactics. Cerberus, an accomplished Ankida, conceived this variation on another Haven-building ritual to allow groups of rebels and mortal servants to escape pursuing loyalist forces."
veil_of_cerberus.source_page = "Houses of the Fallen, p. 192"
veil_of_cerberus.save()

print("Slayer (Halaku) rituals from Houses of the Fallen loaded successfully")
