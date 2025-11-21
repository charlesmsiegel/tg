"""
Populate database with Scourge (Asharu) rituals from Houses of the Fallen.
"""

from characters.models.demon.lore import Lore
from characters.models.demon.ritual import Ritual

from populate_db.demon_houses import scourges
from populate_db.demon_lores import (
    lore_of_awakening as lore_awakening,
    lore_of_the_fundament as lore_fundament,
    lore_of_humanity,
    lore_of_patterns,
    lore_of_storms,
    lore_of_the_winds as lore_winds,
)

# Lore of Survival not found in demon_lores.py
lore_survival = Lore.objects.get_or_create(property_name="survival")[0]

# =============================================================================
# SCOURGE RITUALS - HOUSES OF THE FALLEN
# =============================================================================

cloud_chariot = Ritual.objects.get_or_create(
    name="Cloud Chariot",
    house=scourges,
)[0]
cloud_chariot.primary_lore = lore_winds
cloud_chariot.primary_lore_rating = 4
cloud_chariot.secondary_lore_requirements = [
    {"lore_id": lore_fundament.id, "rating": 1},
]
cloud_chariot.base_cost = 10
cloud_chariot.minimum_casting_time = 25
cloud_chariot.restrictions = "The ritual must be cast under open sky, in an area of at least 60 percent humidity."
cloud_chariot.system = """The ritual conjures up a clear, glassy vessel like a chariot, carriage or sleigh. Roll Stamina + Survival. Each success gives the Cloud Chariot one hour of existence. The chariot can hold the ritual's Ankida, plus one extra person for every dot of the Ankida's permanent Faith score.

The vessel moves at the Ankida's will. Although she doesn't need to concentrate on it rigidly, she does need to be conscious and coherent. If for some reason she passes out, is incapable of rational mental thought (such as being drugged) or leaves the vessel, the chariot dematerializes and gravity reasserts its hold over the former passengers.

The chariot is fast and maneuverable. Its top speed (in miles per hour) is equal to the Ankida's Faith score multiplied by 50. It's capable of full three-dimensional movement, though it cannot be submerged in water without dissipating, and it can reach an altitude of half the Ankida's Faith score in miles."""
cloud_chariot.torment_effect = """The high-Torment effect of this ritual creates a vessel shaped of the very essence of corruption. The chariot is formed of clouds of bitter acid and bilious air, and it emits a noxious stench of decay. It functions as usual, but passengers suffer a level of bashing damage every hour from the vile air that surrounds it. It destroys small creatures and plants in its wake. Greenery wilts and birds drop out of the sky at its passing."""
cloud_chariot.variations = """With the addition of the Lore of Storms ••, the conjured chariot can safely be submerged without fear of dissipation. The vessel can travel below water with no problems, although its progress is far slower. Its speed is reduced to a quarter of normal, and it can only go to a depth of 10 times the Ankida's Faith score in yards. If the ritual is modified to increase the Lore of the Winds to •••••, the vessel takes its own air supply with it, providing breathable air for the passengers as long as the Chariot remains below water.

Including the Lore of Awakening •••• allows the vessel to move without the direction of the Ankida. She must still be aboard, but she can merely give the craft orders and then sleep, pass out or become as incoherent as she likes. The vessel will continue with its predefined orders as long as the ritual lasts, or until the Ankida gives new commands."""
cloud_chariot.flavor_text = "Demons with mastery over the Lore of the Fundament or the Lore of Winds found that their powers added easy strength and speed to their wings, making fast travel trivial. Many other fallen had no such advantage — and neither did any of their beloved mortals — so the Cloud Chariot was developed."
cloud_chariot.source_page = "Houses of the Fallen, p. 54"
cloud_chariot.save()

fog_of_war = Ritual.objects.get_or_create(
    name="Fog of War",
    house=scourges,
)[0]
fog_of_war.primary_lore = lore_winds
fog_of_war.primary_lore_rating = 3
fog_of_war.secondary_lore_requirements = [
    {"lore_id": lore_humanity.id, "rating": 3},
]
fog_of_war.base_cost = 12
fog_of_war.minimum_casting_time = 36
fog_of_war.restrictions = "The area of the sigil must be overlaid with maidens' veils soaked in tears."
fog_of_war.system = """The ritual conceals the Ankida and his allies from the sight of mortals. The players of each mortal who should see the hidden group may make a Willpower test against difficulty 8. If he achieves more successes than the ritual casting did, he can perceive the group normally (though such perception does not magically reveal the group to any viewer other than that mortal). Otherwise, the group is hidden from mortal sight. The fog automatically conceals the Ankida and a number of additional people — demons or mortals — equal to the Ankida's Faith score.

The ritual does affect the perceptions of other fallen, but to a much smaller degree. A demon can see the concealed group if she succeeds on a Perception + Alertness roll with a difficulty equal to the Ankida's Faith.

Roll Dexterity + Manipulation. Each success gives the fog an hour of duration, after which it dissipates immediately. Demons and others with supernatural awareness register the cloud as a supernatural presence or source of supernatural energy (see Demon, p. 172)."""
fog_of_war.torment_effect = """When Torment affects this ritual, the fog it creates is ominous and menacing. The figures within are obscured by the billows, but the cloud itself is anything but discreet. Shot through with angry gray and red streaks, it looks like a thundercloud in miniature. Enemies who come into contact with the fog are scalded by its venom. It inflicts the Ankida's Faith score in levels of lethal damage on any non-concealed person touched by the cloud."""
fog_of_war.variations = """With the addition of the Lore of the Beast ••, the characters within the cloud become invisible to animals as well.

Adding the Lore of Light • increases the difficulty for viewers to see through the cloud by one.

Including Humanity •• suggests to mortals affected by the concealment that they didn't just see nothing at all, they saw something else entirely — something particularly innocuous and appropriate, like a grazing herd of deer, a flock of gulls, a group of toddling children or anything else that would lull the mortals into inattention. A mortal can resist this effect with a successful Willpower roll (difficulty 8), but if the roll achieves more successes than the Ankida's Willpower, then the entire effect of the cloud, concealment and all, is negated for that mortal only."""
fog_of_war.flavor_text = "The Fog of War was developed to hide groups of demons and their mortal allies from enemy troops. The ritual summons evanescent swirls of fine cloud and mist that subtly billow around the Ankida and his companions."
fog_of_war.source_page = "Houses of the Fallen, p. 54"
fog_of_war.save()

inoculate = Ritual.objects.get_or_create(
    name="Inoculate",
    house=scourges,
)[0]
inoculate.primary_lore = lore_awakening
inoculate.primary_lore_rating = 2
inoculate.secondary_lore_requirements = [
    {"lore_id": lore_patterns.id, "rating": 3},
]
inoculate.base_cost = 10
inoculate.minimum_casting_time = 25
inoculate.restrictions = "The sigil must be drawn in quicksilver."
inoculate.system = """The Inoculate ritual protects all the beneficiaries from future infection, disease and ill health for a given period of time. The protection of the ritual lasts for a number of weeks equal to the Ankida's Faith score. During the casting of the ritual, roll Stamina + Medicine (difficulty 6). The number of successes indicates the number of people the ritual can protect.

Although it is equally efficacious on mortals, demons, animals and indeed all living things, the Inoculate ritual is usually used to protect groups of mortals to whom the Asharu do not have easy or frequent access.

While a subject is protected from harm by this ritual, he cannot be afflicted with any disease, suffer any infections or be poisoned. The protection is unspecific and unalterable, so the subject cannot choose to voluntarily lift his resistance to a contaminating factor. For example, during the course of the protection, he cannot become drunk, as the ritual's lingering effects counteract the alcohol byproducts before they render him intoxicated.

Players of demons and other creatures attempting to inflict supernatural diseases on the character may make a Willpower roll (or the equivalent for that creature) with a difficulty of the Ankida's Willpower. Success indicates that the power takes effect, though the Inoculate effects may mitigate the foreign power in some way at the Storyteller's discretion.

Note that this ritual does not prevent a recipient from simple harm sustained through combat or careless mishap."""
inoculate.torment_effect = """The version of this ritual affected by Torment makes the recipients immune to disease and similar harm themselves but turns them into "plague rats" who infect everyone with whom they come in contact. Roll the Ankida's Willpower (difficulty 7), resisted by the highest of the victims' Willpower ratings. If the ritual takes effect, each net success on the Ankida's roll inflicts a level of bashing damage on everyone who comes into physical contact with the infected character. The high-Torment version of this ritual lasts for one week."""
inoculate.variations = "Increasing the Awakening level to ••• allows the protection to heal minor wounds the beneficiaries sustain. Each subject can shrug off a number of bashing or lethal health levels of damage equal to the Ankida's Faith score over the duration of the ritual's effects."
inoculate.flavor_text = "The Inoculate ritual was developed by desperate Asharu who wearied of seeing the human tribes ravaged again and again by the diseases of war — both natural diseases unavoidable in the poor living conditions of a war-torn land and supernatural maladies that spread as fast as breath."
inoculate.source_page = "Houses of the Fallen, p. 55"
inoculate.save()

print("Scourge (Asharu) rituals from Houses of the Fallen loaded successfully")
