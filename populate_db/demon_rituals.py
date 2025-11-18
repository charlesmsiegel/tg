"""
Populate database with Demon rituals from Demon Players Guide Chapter 6.
"""

from characters.models.demon.house import DemonHouse
from characters.models.demon.lore import Lore
from characters.models.demon.ritual import Ritual

# Get all houses
defilers = DemonHouse.objects.get(name="Defilers")
devils = DemonHouse.objects.get(name="Devils")
devourers = DemonHouse.objects.get(name="Devourers")
fiends = DemonHouse.objects.get(name="Fiends")
malefactors = DemonHouse.objects.get(name="Malefactors")
scourges = DemonHouse.objects.get(name="Scourges")
slayers = DemonHouse.objects.get(name="Slayers")

# Get all lores for reference
lore_awakening = Lore.objects.get(property_name="awakening")
lore_beast = Lore.objects.get(property_name="beast")
lore_celestials = Lore.objects.get(property_name="celestials")
lore_death = Lore.objects.get(property_name="death")
lore_earth = Lore.objects.get(property_name="earth")
lore_flame = Lore.objects.get(property_name="flame")
lore_firmament = Lore.objects.get(property_name="firmament")
lore_flesh = Lore.objects.get(property_name="flesh")
lore_forge = Lore.objects.get(property_name="forge")
lore_fundament = Lore.objects.get(property_name="fundament")
lore_humanity = Lore.objects.get(property_name="humanity")
lore_light = Lore.objects.get(property_name="light")
lore_longing = Lore.objects.get(property_name="longing")
lore_paths = Lore.objects.get(property_name="paths")
lore_patterns = Lore.objects.get(property_name="patterns")
lore_portals = Lore.objects.get(property_name="portals")
lore_radiance = Lore.objects.get(property_name="radiance")
lore_realms = Lore.objects.get(property_name="realms")
lore_spirit = Lore.objects.get(property_name="spirit")
lore_storms = Lore.objects.get(property_name="storms")
lore_transfiguration = Lore.objects.get(property_name="transfiguration")
lore_wild = Lore.objects.get(property_name="wild")
lore_winds = Lore.objects.get(property_name="winds")

# ============================================================================
# DEFILER RITUALS
# ============================================================================

hadrisel_libation = Ritual.objects.get_or_create(
    name="Hadrisel's Libation",
    house=defilers,
)[0]
hadrisel_libation.primary_lore = lore_storms
hadrisel_libation.primary_lore_rating = 2
hadrisel_libation.secondary_lore_requirements = [
    {"lore_id": lore_awakening.id, "rating": 1},
]
hadrisel_libation.base_cost = 6
hadrisel_libation.minimum_casting_time = 9
hadrisel_libation.restrictions = "This ritual requires up to half a liter of pure water, can be performed only under the light of the full moon and requires a silver vessel to contain the libation."
hadrisel_libation.system = """Roll Intelligence + Medicine. Each drink of the libation heals one health level of bashing damage per success. In addition, the libation cleanses the recipient's body of all toxins (e.g., fatigue toxins, the effects of alcohol, etc.) and cures any minor illnesses (e.g., cold, flu, sore throat, etc.). The libation can be used a number of times equal to the Ankida's Faith score at the point the ritual was successfully cast. The libation's potency lasts only until the following full moon, at which point any unused amount reverts back to water."""
hadrisel_libation.torment_effect = """The high-Torment version of this libation creates a viscous, oily liquid that burns to the touch and spreads disease and infection. The number of successes rolled becomes a damage pool that inflicts bashing damage on any target struck by the water. In addition, if the victim has open wounds on his skin or he swallows any of the substance, he will contract a virulent disease at the Storyteller's discretion."""
hadrisel_libation.variations = ""
hadrisel_libation.flavor_text = "This ritual was one of the first cooperative attempts by Defilers and Scourges to create a portable healing draught that could be applied to warriors of the infernal host during battle."
hadrisel_libation.source_page = "DPG 187-188"
hadrisel_libation.save()

sirens_song = Ritual.objects.get_or_create(
    name="Siren's Song",
    house=defilers,
)[0]
sirens_song.primary_lore = lore_longing
sirens_song.primary_lore_rating = 3
sirens_song.secondary_lore_requirements = [
    {"lore_id": lore_radiance.id, "rating": 2},
    {"lore_id": lore_humanity.id, "rating": 1},
]
sirens_song.base_cost = 18
sirens_song.minimum_casting_time = 36
sirens_song.restrictions = "This ritual must be performed at the edge of a large body of water."
sirens_song.system = """Roll Manipulation + Performance. The number of successes determines the radius of the ritual's effect in 100-yard increments, measured from the center of the sigil. If the Ankida's player rolls five successes, the ritual affects every living being within a 500-yard radius. Any mortals caught within this radius will stop what they are doing and make their way toward the ritual sigil unless a successful Willpower roll (difficulty 8) is made. Affected individuals will walk in the most direct path toward the sigil regardless of potential danger. Victims have been known to walk over cliffs, drown themselves in lakes and stagger onto the blades of their enemies. While affected by the ritual, victims can take no other action, even to defend themselves. Once successfully cast, the ritual continues as long as the ritual members continue to sing. Make Stamina + Performance rolls (difficulty 6) for every ritual participant each turn to see if they can continue to maintain the song."""
sirens_song.torment_effect = """The high-Torment version of this song fills the mind of a listener with visions of madness and anguish. Make a Willpower roll (difficulty 8) for any mortal or demon caught within the area of effect. If the roll fails, the victim is overcome with visions of the Abyss and falls to the ground, writhing in pain and fear. Affected individuals can take no actions of any kind as long as the song continues. If the Willpower roll botches, a mortal victim gains a temporary derangement as well. A demon gains one point of temporary Torment."""
sirens_song.variations = "Legend speaks of a version of this ritual that could be centered on distant locations far removed from the casting sigil. Add Firmament •• to the ritual's secondary lore."
sirens_song.flavor_text = "This ritual was developed as a battlefield tactic by the Crimson Legion as a means of luring enemy mortals away from their place on the battlefield and creating an opening that the fallen might then exploit. The song was so alluring and powerful that it resonates in humanity's collective memory to this day."
sirens_song.source_page = "DPG 188"
sirens_song.save()

fiery_vision = Ritual.objects.get_or_create(
    name="Fiery Vision",
    house=defilers,
)[0]
fiery_vision.primary_lore = lore_longing
fiery_vision.primary_lore_rating = 3
fiery_vision.secondary_lore_requirements = [
    {"lore_id": lore_light.id, "rating": 2},
    {"lore_id": lore_radiance.id, "rating": 2},
    {"lore_id": lore_humanity.id, "rating": 1},
]
fiery_vision.base_cost = 32
fiery_vision.minimum_casting_time = 64
fiery_vision.restrictions = "This ritual can be performed only on a clear, cloudless day or night, and a fire must be kept alight in the center of the sigil."
fiery_vision.system = """Roll Charisma + Performance. Any of the Ankida's allies or followers that can see the vision receive a number of temporary Willpower points equal to the number of successes rolled. These extra points can exceed their maximum Willpower rating. These bonus Willpower points can be expended for automatic successes as normal or add to a character's dice pool for making Willpower rolls. The ritual affects individuals within a radius of 100 yards times the Ankida's Faith score at the time the ritual is successfully cast. The effects of this vision last for the duration of a single scene, at which point the individuals' Willpower scores return to normal."""
fiery_vision.torment_effect = """The high-Torment effect of this ritual blasts the souls of the Ankida's enemies, filling their hearts and minds with visions of despair. Enemies of the Ankida who witness the vision lose a number of temporary Willpower points equal to the Ankida's successes. A victim whose Willpower is reduced to 0 is overcome with fear and falls into a catatonic state for the remainder of the scene. Mortals whose Willpower is temporarily reduced to 0 suffer a temporary derangement as well. A demon gains one point of temporary Torment."""
fiery_vision.variations = "A variation on this ritual is said to exist that causes the vision to manifest itself over a geographical location far from the ritual's sigil. Add Firmament •• to the ritual's secondary lore."
fiery_vision.flavor_text = "This ritual was one of the Defilers' signature battlefield effects, creating a blazing image high above the battlefield that exhorted the warriors of the fallen to greater acts of valor and filled the hearts of their enemies with dread. The ritual creates the image of a fiery figure high above the center of the sigil, speaking in thunderous tones that can be understood by all who witness it regardless of their native language."
fiery_vision.source_page = "DPG 188-189"
fiery_vision.save()

# ============================================================================
# DEVILS RITUALS
# ============================================================================

baptism_of_faith = Ritual.objects.get_or_create(
    name="Baptism of Faith",
    house=devils,
)[0]
baptism_of_faith.primary_lore = lore_celestials
baptism_of_faith.primary_lore_rating = 2
baptism_of_faith.secondary_lore_requirements = [
    {"lore_id": lore_longing.id, "rating": 2},
]
baptism_of_faith.base_cost = 8
baptism_of_faith.minimum_casting_time = 16
baptism_of_faith.restrictions = "The recipient must be a willing participant in the baptism. She can be any human other than the thrall of a different demon. The sigil is carved into a plaque of clay that is hung around the recipient's neck."
baptism_of_faith.system = """Roll Charisma + Empathy. The effects of the ritual last for as long as five years per success. When the recipient calls on the Celestial Name of the Ankida, the connection between the two is automatic. In addition, the demon is made aware of the situation of the recipient if the human is baptized or enthralled by a different demon or angel, or on the recipient's death but not if the ritual simply lapses. A demon can have only as many baptized followers as she has permanent Faith points. She may voluntarily break the bond only if the mortal gives his approval (or she kills him). If the recipient later recants, the only way to break the relationship without permission is with another baptism. There is no requirement for the demon to answer any call for help that is made of her by a baptized follower, although the human is often led to believe otherwise. In addition, any rolls made by the human to resist the demon in any way (other than physical combat) incur a +1 difficulty penalty."""
baptism_of_faith.torment_effect = """The high-Torment version of this ritual infuses the human recipient with the demon's Torment as well, creating a deranged individual with violent tendencies. A Willpower roll (difficulty 7) must be made for the baptized individual whenever he suffers a bout of extreme stress. If the roll fails, the individual will attempt to relieve the stress by killing another person."""
baptism_of_faith.variations = ""
baptism_of_faith.flavor_text = "While the thrall relationship is one of the closest between demon and human, others can be forged. Nobody is sure who developed the rite of baptism first, but it was used by both sides during the war to engender loyalties among the various mortal factions. A human bestowed with this ritual can call upon a particular demon for aid, and likewise, the demon can use his baptized followers to gain more information in some circumstances."
baptism_of_faith.source_page = "DPG 190-191"
baptism_of_faith.save()

firestorm = Ritual.objects.get_or_create(
    name="Firestorm",
    house=devils,
)[0]
firestorm.primary_lore = lore_flame
firestorm.primary_lore_rating = 4
firestorm.secondary_lore_requirements = [
    {"lore_id": lore_winds.id, "rating": 4},
]
firestorm.base_cost = 16
firestorm.minimum_casting_time = 64
firestorm.restrictions = "This ritual cannot be performed in rain or fog."
firestorm.system = """Roll Stamina + Survival. Each success inflicts one level of lethal damage on every mortal or demon within the area of effect, which is a roughly hemispherical volume centered anywhere within 300 yards of the ritual. The radius of the firestorm is three yards for each point of the Ankida's Faith at the time the ritual is cast."""
firestorm.torment_effect = """The center of the firestorm can only be the sigil itself. Those on the perimeter and within it are not affected unless there are nearby walls (within half the radius of the effect) which reflect the firestorm back onto the casters."""
firestorm.variations = "The version known to be performed by Lucifer and his cohorts granted the Ankida sufficient control to exclude targets within the area of effect. As well as determining damage, each success of the Stamina + Survival roll means one demon (or demon-/human-sized object) of the Ankida's choice will not be affected by the blast. Add Patterns ••."
firestorm.flavor_text = "This short-lived but powerful ritual creates a much-feared conflagration from which there is little hope of escape."
firestorm.source_page = "DPG 191-192"
firestorm.save()

print("Created sample Defiler and Devil rituals")
print(f"Total rituals created: {Ritual.objects.count()}")
