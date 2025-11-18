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

# Remaining Defiler rituals

create_elemental_defiler = Ritual.objects.get_or_create(
    name="Create Elemental (Water)",
    house=defilers,
)[0]
create_elemental_defiler.primary_lore = lore_storms
create_elemental_defiler.primary_lore_rating = 3
create_elemental_defiler.secondary_lore_requirements = [
    {"lore_id": lore_awakening.id, "rating": 2},
    {"lore_id": lore_celestials.id, "rating": 2},
    {"lore_id": lore_fundament.id, "rating": 2},
]
create_elemental_defiler.base_cost = 36
create_elemental_defiler.minimum_casting_time = 81
create_elemental_defiler.restrictions = "This ritual must be performed under the light of a full moon, on the shores of an ocean or sea. A small amount of mercury must be placed in the center of the sigil."
create_elemental_defiler.system = """Roll Manipulation + Occult. The ritual creates a living entity formed entirely of water, with effectively one dot in the following traits: Strength, Dexterity, Stamina, Intelligence, Perception, Wits and Willpower. Each success rolled becomes a dot that the Ankida can allocate to any of these traits or devote to an Ability that she wants the elemental to possess. The elemental can not possess an Ability that the Ankida or any of the Mudu do not possess themselves. The elemental can alter its shape and appearance at will, and it can travel anywhere air can reach. The entity is bound to the Ankida's will, and it will follow her instructions to the best of its ability. The elemental will exist for the duration of a single scene. If a point of the Ankida's temporary Willpower is spent, the elemental will continue to exist until it is destroyed or released by the Ankida. A water elemental effectively has four health levels for the purposes of withstanding damage, but because of its fluid nature, the difficulty of all attempts to hit it increases by two."""
create_elemental_defiler.torment_effect = """The high-Torment version of this ritual creates an amorphous, flesh-eating monster that exists only to hunt and kill the living. Only the creature's Physical Attributes might be increased by the Ankida's successes, and only combat-related Abilities (e.g., Alertness, Brawl and Dodge) may be purchased. The touch of the monster burns like acid, inflicting lethal damage in combat. Finally, the Ankida only nominally controls the creature. A Willpower roll (difficulty 8) must be made on the Ankida's behalf each time she attempts to direct the monster's actions. If the roll fails, the creature acts under the Storyteller's control."""
create_elemental_defiler.variations = ""
create_elemental_defiler.flavor_text = "This powerful ritual allowed the Defilers to create living servants from the very sea, serving the Angels of the Deep in a variety of minor roles."
create_elemental_defiler.source_page = "DPG 189"
create_elemental_defiler.save()

storms_fury = Ritual.objects.get_or_create(
    name="Storm's Fury",
    house=defilers,
)[0]
storms_fury.primary_lore = lore_storms
storms_fury.primary_lore_rating = 4
storms_fury.secondary_lore_requirements = [
    {"lore_id": lore_firmament.id, "rating": 3},
    {"lore_id": lore_winds.id, "rating": 2},
    {"lore_id": lore_humanity.id, "rating": 2},
]
storms_fury.base_cost = 44
storms_fury.minimum_casting_time = 121
storms_fury.restrictions = "This ritual must be performed at the edge of an ocean or sea under an overcast sky. A silver bowl containing salt water must be placed in the center of the sigil."
storms_fury.system = """Roll Intelligence + Survival. The successes rolled are subtracted from the dice pools of every mortal or demon within the storm's area of effect except the Ankida's friends or allies. The storm extends to a radius of a half-mile times the Ankida's Faith score at the time the ritual is successfully cast. This ritual manifests itself as a raging thunderstorm regardless of the climate and season in which the ritual is performed. The effect of this ritual lasts for the duration of a single scene."""
storms_fury.torment_effect = """The effects of the high-Torment version of this ritual are terrible indeed, creating a raging tempest of hellish lightning and acid rain. The successes rolled when determining the effect of the ritual become a lethal damage pool that is rolled every turn for each mortal or demon caught within the storm — friend and foe alike."""
storms_fury.variations = "Toward the end of the war, the Silver Legion developed a version of this ritual that could be centered on a specific individual, provided the Ankida knew the individual's name. Increase Winds and Humanity to ••• each."
storms_fury.flavor_text = "This ritual allowed the Angels of the Deep to pummel their foes with the full fury of a raging storm, directing it as an extension of their will and leaving their allies unscathed."
storms_fury.source_page = "DPG 189-190"
storms_fury.save()

part_the_waters = Ritual.objects.get_or_create(
    name="Part the Waters",
    house=defilers,
)[0]
part_the_waters.primary_lore = lore_storms
part_the_waters.primary_lore_rating = 4
part_the_waters.secondary_lore_requirements = [
    {"lore_id": lore_fundament.id, "rating": 3},
    {"lore_id": lore_paths.id, "rating": 2},
]
part_the_waters.base_cost = 27
part_the_waters.minimum_casting_time = 81
part_the_waters.restrictions = "If the ritual is not cast at high tide, the difficulty to successfully cast it increases by one."
part_the_waters.system = """Roll Stamina + Survival. Each success increases the length of the path by 100 yards. The width of the passage is 10 yards, and it lasts for up to six hours per Faith point. The Ankida can restore the course of the waters whenever she wishes."""
part_the_waters.torment_effect = """The footing of the path is treacherous, and it might contain areas of quicksand and other hazards (the location of which is determined at the Storyteller's discretion). Also, the Ankida does not have control over the duration of the ritual. She cannot end it prematurely, nor know when it is going to expire. The Storyteller secretly rolls dice equal to the character's Torment score. The duration is equal to the maximum duration (six hours per Faith point) divided by the number of successes rolled. If no successes are rolled, the ritual lasts one day per Faith point."""
part_the_waters.variations = "There is said to be a version that creates a path that is a mere 200 yards long, but always centered on the Ankida, so when she moves forward, the waves part before her and close behind her. The maximum depth is twice that of the normal ritual. Increase Fundament to ••••."
part_the_waters.flavor_text = "This ritual allows the demons to create a path through a lake, river or, with enough Faith, a sea. The water rolls back on either side of the designated route, revealing the lake- or riverbed, which is dried sufficiently to support traffic (although it might be uneven and hard to maneuver upon)."
part_the_waters.source_page = "DPG 189-190"
part_the_waters.save()

river_of_blood = Ritual.objects.get_or_create(
    name="River of Blood",
    house=defilers,
)[0]
river_of_blood.primary_lore = lore_storms
river_of_blood.primary_lore_rating = 4
river_of_blood.secondary_lore_requirements = [
    {"lore_id": lore_flesh.id, "rating": 3},
    {"lore_id": lore_portals.id, "rating": 3},
    {"lore_id": lore_transfiguration.id, "rating": 2},
]
river_of_blood.base_cost = 48
river_of_blood.minimum_casting_time = 144
river_of_blood.restrictions = "The ritual needs to be performed on the bank of a river, and an urn containing five pints of human blood must be placed in the center of the sigil."
river_of_blood.system = """Roll Charisma + Empathy. Each success adds a mile of river that is affected from the source point. Beyond the limits of that distance, the blood then flows downstream, under the normal effects of fluid dynamics. For each point of the Ankida's Faith, the transformation into blood lasts a day. After that time, water starts flowing again, but the mass of blood from the ritual still remains, fouling the water until it rots away naturally over the course of several months. All participants, including Khauiki, can donate temporary Willpower. If 20 Willpower is accumulated in this way, the effect becomes permanent."""
river_of_blood.torment_effect = """Such is the power of this ritual that it transforms the pain of the Abyss into material form, creating a powerful and monstrous blood golem that roams the land, killing anyone it can find. The construct is 15 feet tall and its Physical and Mental Attributes, plus its Brawl and Dodge, are each half the Torment score for the ritual (round down). In addition, the profane and liquid form of its body means its touch inflicts lethal damage, and its soak is twice its Stamina (it can soak aggravated damage). It does not receive wound penalties, and whenever it takes 10 levels of damage its body dissolves and re-forms back in the river, as long as the blood still flows there. It can also do so at will. Its first targets are the participants of the ritual."""
river_of_blood.variations = ""
river_of_blood.flavor_text = "All the anguish, resentment and frustrated love of the Angels of the Deep is manifest in this unholy catastrophe. It replaces the life-giving flow of water with a turgid, sticky mass of flowing blood that scars the land and sends an inescapable message to those living upon the Earth."
river_of_blood.source_page = "DPG 190"
river_of_blood.save()

# Remaining Devil rituals

defeat_scry = Ritual.objects.get_or_create(
    name="Defeat Scry",
    house=devils,
)[0]
defeat_scry.primary_lore = lore_celestials
defeat_scry.primary_lore_rating = 3
defeat_scry.secondary_lore_requirements = [
    {"lore_id": lore_firmament.id, "rating": 1},
]
defeat_scry.base_cost = 8
defeat_scry.minimum_casting_time = 16
defeat_scry.restrictions = "The protected area is defined by the size of the sigil."
defeat_scry.system = """Roll Perception + Alertness. The number of successes rolled is subtracted from any attempt to cast the Scry evocation (Firmament ••) on any object or person within the specified area. If the Scry attempt still succeeds, the target of the evocation glows a pale blue. If an object or a person that is already the focus of a Scry attempt enters the protected area, the subject glows blue as well. The protection lasts 12 hours per point of Faith."""
defeat_scry.torment_effect = """The high-Torment effect of this ritual inflicts one health level of bashing damage each turn against individuals attempting to scry into the affected area (this damage can not be soaked). They can still view what is going on, but it's like getting an eyeful of tear gas when they do."""
defeat_scry.variations = "Rumors abound that a ritual could be cast that interferes with scrying attempts, making it appear that the area was empty or that a specifically programmed action was happening within it. Add Light ••••."
defeat_scry.flavor_text = "This ritual creates an area that is protected from scrying attempts."
defeat_scry.source_page = "DPG 191"
defeat_scry.save()

resist_fire = Ritual.objects.get_or_create(
    name="Resist Fire",
    house=devils,
)[0]
resist_fire.primary_lore = lore_flame
resist_fire.primary_lore_rating = 2
resist_fire.secondary_lore_requirements = [
    {"lore_id": lore_flesh.id, "rating": 2},
]
resist_fire.base_cost = 8
resist_fire.minimum_casting_time = 16
resist_fire.restrictions = "The ritual must be cast in direct sunlight. Each subject to be affected must be within the sigil."
resist_fire.system = """Roll Stamina + Dodge. The number of successes rolled determines how many individuals receive the ritual's protection. Each can use their Stamina to soak fire damage for up to five turns per Faith point."""
resist_fire.torment_effect = """The subject does not take damage from fire, but he feels the pain of being burned nonetheless. Each time a character soaks damage inflicted by fire, a Willpower roll must be made with the difficulty equal to 5 + the number of damage levels soaked. If the roll fails, the character loses her actions for the next turn."""
resist_fire.variations = "A powerful version of this ritual allows flame to actually heal the recipient. Each point of fire damage successfully soaked heals one level of bashing damage. Add Awakening •••."
resist_fire.flavor_text = "This ritual gives the subjects the ability to shrug off fire damage. It was designed to help human support troops in battle against loyalist members of the First House."
resist_fire.source_page = "DPG 191"
resist_fire.save()

faith_of_steel = Ritual.objects.get_or_create(
    name="Faith of Steel",
    house=devils,
)[0]
faith_of_steel.primary_lore = lore_radiance
faith_of_steel.primary_lore_rating = 2
faith_of_steel.secondary_lore_requirements = [
    {"lore_id": lore_awakening.id, "rating": 2},
    {"lore_id": lore_longing.id, "rating": 2},
]
faith_of_steel.base_cost = 18
faith_of_steel.minimum_casting_time = 36
faith_of_steel.restrictions = "The focus of the ritual is a human under the Ankida's command who has been wounded in anger within the last hour."
faith_of_steel.system = """Roll Manipulation + Leadership. The effect lasts for 10 minutes per success. One human per point of the Ankida's Faith is affected, as long as the Ankida can see him, and each can deduct his own Faith potential from any wound penalties he receives. In addition, they can keep attacking for an extra number of turns equal to their Faith potential if they are incapacitated (not dead), at -5 to their relevant dice pools. Assume a default potential of 2 unless circumstances dictate otherwise. Even at that level, they are unaffected by injuries that would normally cripple a mortal, making for a fearsome force. Note that the effects of this ritual can be combined with the effects of the Exalt evocation."""
faith_of_steel.torment_effect = """The high-Torment version of this ritual infuses the recipients with an unquenchable bloodlust, driving them into a murderous frenzy. Unless a successful Willpower roll is made (difficulty 7), they will attack the nearest individual, friend or foe, each turn."""
faith_of_steel.variations = ""
faith_of_steel.flavor_text = "This ritual inspires human troops under the Ankida's command, filling them with hope and determination, and allowing them to fight on despite any injuries they receive."
faith_of_steel.source_page = "DPG 192"
faith_of_steel.save()

create_elemental_devil = Ritual.objects.get_or_create(
    name="Create Elemental (Fire)",
    house=devils,
)[0]
create_elemental_devil.primary_lore = lore_flame
create_elemental_devil.primary_lore_rating = 3
create_elemental_devil.secondary_lore_requirements = [
    {"lore_id": lore_awakening.id, "rating": 2},
    {"lore_id": lore_celestials.id, "rating": 2},
    {"lore_id": lore_fundament.id, "rating": 2},
]
create_elemental_devil.base_cost = 36
create_elemental_devil.minimum_casting_time = 81
create_elemental_devil.restrictions = "This ritual must be performed beneath the noonday sun near a source of intense natural heat such as a geothermal spring or a volcano. A small quantity of obsidian must be placed in the center of the sigil."
create_elemental_devil.system = """Roll Manipulation + Occult. The ritual creates a living entity formed entirely of fire, with effectively one dot in the following traits: Strength, Dexterity, Stamina, Intelligence, Perception, Wits and Willpower. Each success rolled becomes a dot that the Ankida can allocate to any of these traits or devote to an Ability that she wants the elemental to possess. The elemental can not possess an Ability that the Ankida or any of the Mudu do not possess themselves. The elemental assumes a lithe, humanoid shape that can wear armor or bear weapons specially crafted to withstand intense heat. The entity is bound to the Ankida's will and will follow her instructions to the best of its ability. The elemental will exist for the duration of a single scene. If a point of the Ankida's temporary Willpower is spent the elemental will continue to exist until it is destroyed or released by the Ankida. A fire elemental has six health levels for the purposes of withstanding damage. Its touch will ignite inflammable objects after one turn of contact and inflict lethal damage in combat."""
create_elemental_devil.torment_effect = """The high-Torment version creates a serpentine creature charged by the Ankida's hatred and driven to torture and kill the living. Only the creature's Physical Attributes can be increased by the Ankida's successes, and only combat-related Abilities (e.g., Alertness, Brawl and Dodge) can be purchased. The creature's body is sheathed in hard scales that provide five dice of armor protection, and its touch inflicts aggravated damage instead of lethal. Finally, the Ankida only nominally controls the creature; a Willpower roll (difficulty 8) must be made on the Ankida's behalf each time she attempts to direct the monster's actions. If the roll fails, the creature acts under the Storyteller's control."""
create_elemental_devil.variations = ""
create_elemental_devil.flavor_text = "This powerful ritual allowed the Devils to create servants of living fire that performed the role of guardians, bodyguards or assassins during the war."
create_elemental_devil.source_page = "DPG 193"
create_elemental_devil.save()

hopes_true_flame = Ritual.objects.get_or_create(
    name="Hope's True Flame",
    house=devils,
)[0]
hopes_true_flame.primary_lore = lore_celestials
hopes_true_flame.primary_lore_rating = 2
hopes_true_flame.secondary_lore_requirements = [
    {"lore_id": lore_flame.id, "rating": 2},
    {"lore_id": lore_longing.id, "rating": 2},
    {"lore_id": lore_radiance.id, "rating": 2},
]
hopes_true_flame.base_cost = 32
hopes_true_flame.minimum_casting_time = 64
hopes_true_flame.restrictions = "The participants of the ritual must not have performed any acts of violence in the previous week."
hopes_true_flame.system = """Roll Manipulation + Empathy (difficulty 8). The number of successes determines how powerful the effect is on those who witness the flame. All those who can see the flame, and who plan violence on the occupants of the building upon which the ritual was cast lose a number of dice from their dice pools equal to the successes rolled. The effect of this ritual lasts for a number of days equal to the Ankida's Faith score at the time the ritual was cast."""
hopes_true_flame.torment_effect = ""
hopes_true_flame.variations = ""
hopes_true_flame.flavor_text = "This ritual creates a tongue of brilliant white flame that blazes above a house or other structure and protects those within it from harm."
hopes_true_flame.source_page = "DPG 193"
hopes_true_flame.save()

# ============================================================================
# DEVOURER RITUALS
# ============================================================================

fruit_of_perfection = Ritual.objects.get_or_create(
    name="Fruit of Perfection",
    house=devourers,
)[0]
fruit_of_perfection.primary_lore = lore_wild
fruit_of_perfection.primary_lore_rating = 2
fruit_of_perfection.secondary_lore_requirements = [
    {"lore_id": lore_radiance.id, "rating": 2},
]
fruit_of_perfection.base_cost = 8
fruit_of_perfection.minimum_casting_time = 16
fruit_of_perfection.restrictions = "The sigil must be drawn around a mature fruit tree and a smaller version inscribed into its bark."
fruit_of_perfection.system = """Roll Charisma + Empathy. One success means that fruit eaten from the ritual tree makes the recipient immune to fear and supernatural forms of mind-control. Two successes mean that the recipient adds one dot to her Intelligence. Three successes means that the recipient adds one dot to each of her Mental Attributes. Four successes mean that the recipient can add one bonus die to all of her dice pools for the duration of the scene. As many pieces of fruit are grown as the Ankida has Faith, each of which can affect one person. The fruit loses its effectiveness within one hour of being picked. If someone eats two pieces of the fruit, the effects do not stack."""
fruit_of_perfection.torment_effect = """The high-Torment effect of this ritual subtracts dice from the relevant traits or dice pools."""
fruit_of_perfection.variations = "There is said to be a version of Fruit of Perfection that was developed during the war. It has the same effect, but it also makes the recipient of the effect more sensitive to the spirit realms as well as the natural one. Add Realms •."
fruit_of_perfection.flavor_text = "This ritual creates a fruit that can be used to impart courage and insight. It was developed in an attempt to inspire humanity before the rebellion."
fruit_of_perfection.source_page = "DPG 193-194"
fruit_of_perfection.save()

bountiful_harvest = Ritual.objects.get_or_create(
    name="Bountiful Harvest",
    house=devourers,
)[0]
bountiful_harvest.primary_lore = lore_wild
bountiful_harvest.primary_lore_rating = 2
bountiful_harvest.secondary_lore_requirements = [
    {"lore_id": lore_earth.id, "rating": 1},
    {"lore_id": lore_storms.id, "rating": 1},
]
bountiful_harvest.base_cost = 12
bountiful_harvest.minimum_casting_time = 16
bountiful_harvest.restrictions = "A small quantity of loam must be placed in the center of the sigil."
bountiful_harvest.system = """Roll Stamina + Survival. The ritual affects an area with a radius in 100-yard increments equal to the number of successes rolled and centered on the sigil. A lush garden blooms into life within the affected area, with thick grass, small streams and tall, fruit-bearing trees. This garden can sprout in an area where one couldn't normally exist — in deserts, snow fields, parking lots or toxic waste dumps. The water, vegetables and fruit created by the ritual are normal and nutritious in every way. The garden exists for a single scene. At the end of that time the water dries up and the plants wither into dust. If the Ankida wishes, however, the garden can be made permanent by spending a temporary Willpower point. It must be tended like any other garden afterward if it is to survive, though."""
bountiful_harvest.torment_effect = """The high-Torment version of this ritual does not create gardens, but lifeless wastelands. All water and vegetation within the affected area dries up and withers away, not to return again until the next blooming season. By spending a temporary Willpower point the effects of this ritual become permanent, creating a blighted area where nothing will ever grow."""
bountiful_harvest.variations = ""
bountiful_harvest.flavor_text = "This ritual was designed to create lush gardens in place of barren wastelands, providing sustenance for the host's mortal flocks in times of need."
bountiful_harvest.source_page = "DPG 194"
bountiful_harvest.save()

heart_of_stone = Ritual.objects.get_or_create(
    name="Heart of Stone",
    house=devourers,
)[0]
heart_of_stone.primary_lore = lore_flesh
heart_of_stone.primary_lore_rating = 3
heart_of_stone.secondary_lore_requirements = [
    {"lore_id": lore_earth.id, "rating": 2},
]
heart_of_stone.base_cost = 10
heart_of_stone.minimum_casting_time = 25
heart_of_stone.restrictions = "The sigil must be inscribed in powdered granite."
heart_of_stone.system = """Roll Stamina + Leadership. The ritual affects as many humans as the number of successes rolled. Each affected individual adds the Ankida's Faith to his soak rolls up to a maximum of twice his Stamina. The effect lasts for one scene."""
heart_of_stone.torment_effect = """All recipients gain the protective advantages of the ritual but also lose one die from all their combat dice pools as the effect literally hardens muscles and skin."""
heart_of_stone.variations = "A subsequent version of this ritual was said to specifically affect metal weapons used to strike the recipient, making the weapon harder and harder to wield effectively due to strange fluctuations in inertia. Every health level of damage soaked by the ritual's effect increases the difficulty of wielding the weapon that inflicted the damage to a maximum difficulty of 10. Add Fundament •••."
heart_of_stone.flavor_text = "This ritual was used to harden the defenses of humans fighting for the rebel cause. The targets gain increased resistance to damage in combat."
heart_of_stone.source_page = "DPG 194"
heart_of_stone.save()

beast_of_babel = Ritual.objects.get_or_create(
    name="Beast of Babel",
    house=devourers,
)[0]
beast_of_babel.primary_lore = lore_beast
beast_of_babel.primary_lore_rating = 3
beast_of_babel.secondary_lore_requirements = [
    {"lore_id": lore_flesh.id, "rating": 2},
    {"lore_id": lore_firmament.id, "rating": 2},
    {"lore_id": lore_humanity.id, "rating": 2},
]
beast_of_babel.base_cost = 36
beast_of_babel.minimum_casting_time = 81
beast_of_babel.restrictions = "The ritual can be performed only under the light of the full moon. Further, the freshly skinned hide of the animal the Ankida wishes to use for the ritual must be placed in the center of the sigil. Further, the animal chosen must be approximately the same size and mass of a typical human being. Insects and small animals such as rodents are not allowed."
beast_of_babel.system = """Roll Stamina + Survival in a resisted roll against each victim's Willpower. The ritual affects an area with a radius in 10-yard increments equal to the Ankida's Faith score at the time the ritual is successfully cast. Each mortal or demon within the affected area that succumbs to the ritual is transformed into the Ankida's chosen animal, taking on its Physical and Mental Attributes, instincts and behavior for the duration of the scene. By expending a temporary Willpower point per victim, the Ankida can make the effects of this ritual permanent."""
beast_of_babel.torment_effect = """The high-Torment version of this ritual infuses its victims with an appetite for human flesh and an insatiable bloodlust. The transformed animals attack the nearest mortal, friend or foe, in an attempt to kill and eat them. If Willpower points are spent to make this effect permanent, the mortal reverts back to his normal form at the end of the scene but transforms beneath the light of each succeeding full moon and remains in animal form until it kills and eats human flesh."""
beast_of_babel.variations = ""
beast_of_babel.flavor_text = "This powerful ritual was developed originally as a form of cruel sport by Devourers of the Ebon Legion, transforming prisoners into animals that the demons could hunt with their hounds. It wasn't long, however, before the battlefield applications of the ritual became obvious."
beast_of_babel.source_page = "DPG 195-196"
beast_of_babel.save()

# ============================================================================
# MALEFACTOR RITUALS
# ============================================================================

disarm = Ritual.objects.get_or_create(
    name="Disarm",
    house=malefactors,
)[0]
disarm.primary_lore = lore_forge
disarm.primary_lore_rating = 3
disarm.secondary_lore_requirements = [
    {"lore_id": lore_fundament.id, "rating": 2},
]
disarm.base_cost = 10
disarm.minimum_casting_time = 25
disarm.restrictions = "A piece of magnetized iron must be placed in the center of the sigil."
disarm.system = """Roll Strength + Technology. The number of successes determines the complexity of the weapons affected by the ritual. One success renders high-tech weapons that use electronic components inoperable. Two successes render complex mechanical weapons such as automatic rifles and machine guns inoperable. Three successes render basic mechanical weapons such as revolvers or crossbows inoperable. Four or more successes render the most basic weapons such as knives and axes unable to function. If used, they will automatically miss their target. This ritual affects an area in a radius of 100-yard increments equal to the Ankida's Faith score at the time the ritual is successfully cast, and its effects last for the duration of the scene."""
disarm.torment_effect = """The high-Torment effect of this ritual allows weapons to function within the affected area but increases the chance for catastrophic accidents. Each success rolled increases the range of numbers that cause a botch on a weapon's to-hit roll. Therefore, if the effect roll netted four successes, any weapons used within the area of effect would botch on a roll of 1, 2, 3, 4 or 5. If a to-hit roll botches, the weapon hits its wielder or the wielder's nearest friend or ally instead."""
disarm.variations = ""
disarm.flavor_text = "This ritual is of uncertain origin. Some legends say that it was adapted from a chorus performed by heavenly angels to disarm a group of mortals loyal to the fallen. Other sources claim that a Malefactor of the Iron Legion, sick with the slaughter of the Time of Atrocities, developed the ritual as a means of ending conflicts before they could begin."
disarm.source_page = "DPG 199-200"
disarm.save()

age_landscape = Ritual.objects.get_or_create(
    name="Age Landscape",
    house=malefactors,
)[0]
age_landscape.primary_lore = lore_earth
age_landscape.primary_lore_rating = 3
age_landscape.secondary_lore_requirements = [
    {"lore_id": lore_wild.id, "rating": 3},
    {"lore_id": lore_death.id, "rating": 2},
]
age_landscape.base_cost = 24
age_landscape.minimum_casting_time = 64
age_landscape.restrictions = "This ritual can be performed only at sunrise or sunset. A lump of sandstone must be placed in the center of the sigil."
age_landscape.system = """Roll Stamina + Science. The area of effect covers a diameter of 200 yards per success centered around the sigil. The edge of the effect is not sharp, it tapers off for another 100 yards beyond that circle. Each success ages the landscape by approximately 1,000 years. Changes are often not immediately apparent, but any observer can watch the slow shifting of ground and vegetation. The exact effects depend upon the composition of the bedrock. Caves form, cliffs become steeper, or the ground level simply drop away a few feet. Any vegetation adapts itself to the new landscape, so that it looks like it was always there (although the individual plants do not change, which might cause some of them to be in unsuitable locations for long-term survival)."""
age_landscape.torment_effect = """The ground is blighted, by weeds and poisonous plants, by crumbling rock and scree, and, if it's wet enough, fetid swamp and quicksand."""
age_landscape.variations = "Apparently some rebels developed a variation of this ritual which also undermined structures built on the surface, so as to attack enemy fortifications. Add Fundament •••."
age_landscape.flavor_text = "The ritual can potentially affect a huge area, changing the geographical characteristics of it in a short period of time. Tens of thousands of years of erosion can be simulated in mere hours. The ritual was used by the fallen to reshape the lands that God had directed to be built and subsequently damaged in His anger."
age_landscape.source_page = "DPG 201"
age_landscape.save()

create_elemental_malefactor = Ritual.objects.get_or_create(
    name="Create Elemental (Earth)",
    house=malefactors,
)[0]
create_elemental_malefactor.primary_lore = lore_earth
create_elemental_malefactor.primary_lore_rating = 3
create_elemental_malefactor.secondary_lore_requirements = [
    {"lore_id": lore_awakening.id, "rating": 2},
    {"lore_id": lore_celestials.id, "rating": 2},
    {"lore_id": lore_fundament.id, "rating": 2},
]
create_elemental_malefactor.base_cost = 36
create_elemental_malefactor.minimum_casting_time = 81
create_elemental_malefactor.restrictions = "This ritual must be performed in a cavern where sunlight cannot reach. A lump of marble must be placed in the center of the sigil."
create_elemental_malefactor.system = """Roll Manipulation + Occult. The ritual creates a living entity formed entirely of fire, with effectively one dot in the following traits: Strength, Dexterity, Stamina, Intelligence, Perception, Wits and Willpower. Each success rolled becomes a dot that the Ankida can allocate to any of these traits or devote to an Ability that she wants the elemental to possess. The elemental can not possess an Ability that the Ankida or any of the Mudu do not possess themselves. The elemental assumes a huge, rocky humanoid shape that can wear armor or carry weapons specially crafted for its massive size. The entity is bound to the Ankida's will, and it will follow her instructions to the best of its ability. The elemental will exist for the duration of a single scene; if a point of the Ankida's temporary Willpower is spent the elemental will continue to exist until destroyed or released by the Ankida. A fire elemental has 10 health levels for the purposes of withstanding damage, and its huge hands inflict lethal damage in combat."""
create_elemental_malefactor.torment_effect = """The high-Torment version creates a living war machine charged by the Ankida's hatred and driven to torture and kill the living. Only the creature's Physical Attributes can be increased by the Ankida's successes, and only combat-related Abilities (e.g., Alertness, Brawl and Dodge) can be purchased. The creature's body is sheathed in stone-hard skin that provide eight dice of armor protection and its fists inflicts aggravated damage instead of lethal. Finally, the Ankida only nominally controls the creature. A Willpower roll (difficulty 8) must be made on the Ankida's behalf each time she attempts to direct the monster's actions. If the roll fails, the creature acts under the Storyteller's control."""
create_elemental_malefactor.variations = ""
create_elemental_malefactor.flavor_text = "This powerful ritual allowed the Malefactors to create servants of living stone that acted as servants and sentient siege engines during the war."
create_elemental_malefactor.source_page = "DPG 201-202"
create_elemental_malefactor.save()

# ============================================================================
# SCOURGE RITUALS
# ============================================================================

micaraels_sight = Ritual.objects.get_or_create(
    name="Micarael's Sight",
    house=scourges,
)[0]
micaraels_sight.primary_lore = lore_firmament
micaraels_sight.primary_lore_rating = 2
micaraels_sight.secondary_lore_requirements = [
    {"lore_id": lore_realms.id, "rating": 2},
]
micaraels_sight.base_cost = 8
micaraels_sight.minimum_casting_time = 16
micaraels_sight.restrictions = "The ritual must be performed in an area lit well enough to read by."
micaraels_sight.system = """Roll Perception + Crafts. The Ankida can see through solid, non-living matter as though it were clear glass. Each success applies the effect to a cubic foot of matter whose perceived volume can be distributed as needed (for example, a six inch x two foot x one foot pane in a brick wall that is six inches thick), anywhere within the Ankida's sight. The effect lasts for a number of turns equal to the Ankida's Faith score."""
micaraels_sight.torment_effect = """The high-Torment effect of this ritual causes the Ankida to see hallucinations that feed the character's paranoia. The demon might see a group of Earthbound thralls laying an ambush for her, or she might see one of her thralls meeting secretly with her worst rival. The Storyteller should choose a hallucination appropriate to the character's personality and the situation, and present the vision as though the character were really seeing it."""
micaraels_sight.variations = "With the addition of Longing ••, this ritual works as a warning, extending to an area 50 feet beyond the perimeter of the sigil. Whenever anyone who wishes the Ankida harm comes into this area, any solid matter between them becomes transparent to her sight, the window moving as required. As many as one enemy can be viewed per success rolled, and the effect lasts half an hour per Faith point."
micaraels_sight.flavor_text = "This ritual was part of an effort to teach the craft of rituals to humans during the Time of Babel. Although that effort was not successful, the ritual's effect — making solid matter perfectly transparent to the Ankida who performed it — was later studied for its military applications against the Heavenly Host."
micaraels_sight.source_page = "DPG 202"
micaraels_sight.save()

rain_of_frogs = Ritual.objects.get_or_create(
    name="Rain of Frogs",
    house=scourges,
)[0]
rain_of_frogs.primary_lore = lore_winds
rain_of_frogs.primary_lore_rating = 3
rain_of_frogs.secondary_lore_requirements = [
    {"lore_id": lore_beast.id, "rating": 3},
    {"lore_id": lore_awakening.id, "rating": 2},
]
rain_of_frogs.base_cost = 24
rain_of_frogs.minimum_casting_time = 64
rain_of_frogs.restrictions = "At least two frogs of complementary sexes are required to perform the ritual. The humidity of the air within the sigil must be at least 70%, although this can be achieved artificially."
rain_of_frogs.system = """Roll Stamina + Animal Ken. Each success creates a cubic yard of frogs for aerial distribution. The frogs are actually brewed in the air, a combination of living creatures and the pure idea of multiplying frogs. The number of successes also determines the distance they can be transported, each one equaling a mile. The Ankida controls the area of the rain of frogs — for greatest impact a restricted area is advised. The velocity of the falling frogs is automatically such that they can survive the fall, and they cause no damage upon impact. The duration of the rain is only a matter of minutes, but the consequences will be hopping around indefinitely."""
rain_of_frogs.torment_effect = """The frogs secrete a toxin that can harm or even kill people who come into contact with them. The usual symptoms include spreading paralysis and difficult breathing. Victims who handle the frogs suffer one level of bashing damage unless a successful Stamina roll (difficulty 8) is made each hour after exposure. The effects of the toxin last for a number of hours equal to the Ankida's Torment score."""
rain_of_frogs.variations = "The variety of creatures that this ritual can be adapted for is limited only by size. A frog is pretty much the maximum weight. Rains of worms, spiders and even fish have all been rumored at one time or another."
rain_of_frogs.flavor_text = "The origins of this ritual are lost, but its persistence in human legend suggests its purpose was to bewilder and distract those who witness it. It is possibly derived from a creation ritual that populated an area with animal life in the manner of a farmer scattering seed."
rain_of_frogs.source_page = "DPG 203-204"
rain_of_frogs.save()

create_elemental_scourge = Ritual.objects.get_or_create(
    name="Create Elemental (Air)",
    house=scourges,
)[0]
create_elemental_scourge.primary_lore = lore_winds
create_elemental_scourge.primary_lore_rating = 3
create_elemental_scourge.secondary_lore_requirements = [
    {"lore_id": lore_awakening.id, "rating": 2},
    {"lore_id": lore_celestials.id, "rating": 2},
    {"lore_id": lore_fundament.id, "rating": 2},
]
create_elemental_scourge.base_cost = 36
create_elemental_scourge.minimum_casting_time = 81
create_elemental_scourge.restrictions = "This ritual must be performed under the light of a full moon, on a cloudy, windy night. A handful of feathers must be placed in the center of the sigil."
create_elemental_scourge.system = """Roll Manipulation + Occult. The ritual creates a living entity formed entirely of air, with effectively one dot in the following traits: Strength, Dexterity, Stamina, Intelligence, Perception, Wits and Willpower. Each success rolled becomes a dot that the Ankida can allocate to any of these traits, or devote to an Ability that she wants the elemental to possess. The elemental can not possess an Ability that the Ankida or any of the Mudu do not possess themselves. The elemental can alter its shape and appearance at will, able to travel anywhere air can reach. The entity is bound to the Ankida's will, and will follow her instructions to the best of its ability. The elemental will exist for the duration of a single scene; if a point of the Ankida's temporary Willpower is spent the elemental will continue to exist until destroyed or released by the Ankida. An air elemental effectively has four health levels for the purposes of withstanding damage, but because of its fluid nature the difficulty of all attempts to hit it increases by two."""
create_elemental_scourge.torment_effect = """The high-Torment version of this ritual creates a monster that exists only to hunt and kill the living. Only the creature's Physical Attributes can be increased by the Ankida's successes, and only combat-related Abilities (e.g., Alertness, Brawl and Dodge) can be purchased. The touch of the monster cuts like a blade, inflicting lethal damage in combat. Finally, the Ankida only nominally controls the creature. A Willpower roll (difficulty 8) must be made on the Ankida's behalf each time she attempts to direct the monster's actions. If the roll fails, the creature acts under the Storyteller's control."""
create_elemental_scourge.variations = ""
create_elemental_scourge.flavor_text = "This powerful ritual allowed the Scourges to create living servants from the very air itself, serving the Angels of the Firmament in a variety of minor roles."
create_elemental_scourge.source_page = "DPG 204"
create_elemental_scourge.save()

# ============================================================================
# SLAYER RITUALS
# ============================================================================

shadow_dark = Ritual.objects.get_or_create(
    name="Shadow Dark",
    house=slayers,
)[0]
shadow_dark.primary_lore = lore_realms
shadow_dark.primary_lore_rating = 2
shadow_dark.secondary_lore_requirements = [
    {"lore_id": lore_light.id, "rating": 2},
]
shadow_dark.base_cost = 8
shadow_dark.minimum_casting_time = 16
shadow_dark.restrictions = "If the ritual is not cast at dawn or twilight, the difficulty increases by one."
shadow_dark.system = """Roll Perception + Awareness. The ritual affects an area with a radius of three yards times the Ankida's Faith score, centered around a point within the Ankida's line of sight. The effect lasts three minutes per point of the Ankida's Faith score. Anyone within the area suffers a modifier of +3 to the difficulty of all actions that interact with physical objects. A successful Willpower roll (difficulty 8) means the person has resisted the distractions of the environment (assuming they think to do so) for up to three turns, and the penalty decreases to +2. Conversely, a blind person or a person trained in Blind Fighting can further reduce this penalty by one (+1 normally, no penalty if a subsequent Willpower roll succeeds), when trying to perform a familiar task. If participants in the ritual donate three points of temporary Willpower, the effect becomes permanent."""
shadow_dark.torment_effect = ""
shadow_dark.variations = "By adding Transfiguration ••, it is said that the ritual can make people within it lose awareness of their own bodily form, which seems to shift and distort with everything else. This adds another +2 to the difficulty of actions (the same Willpower role halves this modifier)."
shadow_dark.flavor_text = "This ritual creates an area of darkness that is more akin to a shadowy reflection of the spirit realm than a simple lack of light. It is not perfect darkness — light sources remain but lack the strength to illuminate other objects. Strange shapes seem to glide by on the darkness. Distances seem distorted, and there is a faint moaning that somehow seems to overshadow most other sound. Even people who are normally used to working blind are affected."
shadow_dark.source_page = "DPG 205"
shadow_dark.save()

spirit_garden = Ritual.objects.get_or_create(
    name="Spirit Garden",
    house=slayers,
)[0]
spirit_garden.primary_lore = lore_spirit
spirit_garden.primary_lore_rating = 2
spirit_garden.secondary_lore_requirements = [
    {"lore_id": lore_wild.id, "rating": 2},
]
spirit_garden.base_cost = 8
spirit_garden.minimum_casting_time = 16
spirit_garden.restrictions = "A recently dead body, a garden in which the flower can grow, and nightfall."
spirit_garden.system = """Roll Charisma + Survival. If the number of successes is greater than the target's Willpower, her spirit is caught within the garden, blooming as a flower. The effect remains as long as the flower is in bloom, but if it is plucked or it wilts, then the soul is lost. Each Faith point gives the flower an extra day of life, but after that, nature takes its course (so it is more effective cast in spring than winter). Note that the effect cannot be made permanent (like Spirit ••••), but it can defer matters until a better solution is found. The exact type of flower depends upon the individual (at Storyteller's discretion)."""
spirit_garden.torment_effect = """The flower is black and poisonous, leaching all sustenance from the soil around it and slowly wilting plant-life within a radius of one yard per Faith point."""
spirit_garden.variations = "A rather different use of this ritual can be made with the addition of Death •. If the flower is eaten by a demon, then the last hours of the human's life can be viewed (one hour per Faith point), and the spirit is lost. The resistance of the spirit to this process adds one to the difficulty of the Charisma + Survival roll."
spirit_garden.flavor_text = "This ritual was one of the first ones designed to protect human spirits from the pull of oblivion, designed even before the higher evocations of the Lore of the Spirit had been formulated. It was not particularly successful, as loyalist Angels of Death could easily sense the garden thus created, and the soul was bound to a fragile bloom that was easily crushed."
spirit_garden.source_page = "DPG 205"
spirit_garden.save()

incarnate_spirit = Ritual.objects.get_or_create(
    name="Incarnate Spirit",
    house=slayers,
)[0]
incarnate_spirit.primary_lore = lore_spirit
incarnate_spirit.primary_lore_rating = 3
incarnate_spirit.secondary_lore_requirements = [
    {"lore_id": lore_flesh.id, "rating": 2},
    {"lore_id": lore_realms.id, "rating": 2},
]
incarnate_spirit.base_cost = 21
incarnate_spirit.minimum_casting_time = 49
incarnate_spirit.restrictions = "This ritual can be performed only on the night of the new moon."
incarnate_spirit.system = """Roll Intelligence + Occult. The number of successes required depends on the thickness of the barrier between the realms in the ritual area. A relatively weak area, such as a graveyard or a church, might require only one success, while a relatively strong area such as a science lab might require as many as four successes. If the roll succeeds the Ankida can incarnate as many spirits as her Faith score. These spirits can be seen and communicated with, and they can even interact with the physical world as though they were flesh and blood, though they are physically weak and frail. Each incarnate spirit has effectively one dot in each of her Physical Attributes, though her Mental and Social Attributes are the same as they were when she was alive (as determined by the Storyteller). If the incarnate spirit suffers a single health level of damage, be it bashing, lethal or aggravated, the body discorporates. In this quasi-physical form, the spirit cannot use any supernatural powers it possesses."""
incarnate_spirit.torment_effect = """The high-Torment version of this ritual infuses the incarnate spirit with some of the Ankida's hate and malevolence, causing it to behave maliciously toward mortals in its presence. If communicated with, it is intentionally hurtful and deceitful, and will try to find ways to injure or kill living beings in its proximity."""
incarnate_spirit.variations = ""
incarnate_spirit.flavor_text = "This ritual was devised by the Slayers to permit grieving mortals to briefly visit with the spirits of the departed."
incarnate_spirit.source_page = "DPG 206-207"
incarnate_spirit.save()

# ============================================================================
# FIEND RITUALS
# ============================================================================

prophetic_dream = Ritual.objects.get_or_create(
    name="Prophetic Dream",
    house=fiends,
)[0]
prophetic_dream.primary_lore = lore_patterns
prophetic_dream.primary_lore_rating = 4
prophetic_dream.secondary_lore_requirements = [
    {"lore_id": lore_firmament.id, "rating": 2},
    {"lore_id": lore_spirit.id, "rating": 1},
]
prophetic_dream.base_cost = 21
prophetic_dream.minimum_casting_time = 49
prophetic_dream.restrictions = "The subject of the ritual must sit or lie in the center of the sigil."
prophetic_dream.system = """Roll Perception + Intuition. The ritual grants the recipient the effects of the Causal Influence evocation presented in the Demon core rules, but using the ritual effect roll to determine the extent of the information gained. The ritual can be focused on a specific person (difficulty 6), place (difficulty 7) or upcoming event (difficulty 9). Spend one Faith point and roll Perception + Intuition. The number of successes rolled determines how many days into the future the recipient can view regarding her subject. It also determines how many questions the player can ask the Storyteller about what the character sees. The evocation fills the recipient's mind with a torrent of images, showing the most likely fate of a specific person, place or event, barring any outside interference. The Storyteller describes the course of events as though the recipient were an outside observer. She isn't privy to the thoughts of the individuals involved, and she must decide the context and meaning of relationships and actions herself."""
prophetic_dream.torment_effect = """The high-Torment version of this ritual shows the recipient where the subject (be it a person, place or event) is at risk of suffering an accident or other misfortune, and it shows the best way to cause the tragic circumstances to occur."""
prophetic_dream.variations = ""
prophetic_dream.flavor_text = "The Fiends developed this ritual during the war as an aid to the commanders of Lucifer's legions, allowing them a glimpse of their own future as a tool to refining their battle plans. In practice the infernal leaders had to apply a great deal of insight to interpret their visions, often requiring the advice of the Neberu once the vision had passed."
prophetic_dream.source_page = "DPG 196-197"
prophetic_dream.save()

print("Created comprehensive ritual database")
print(f"Total rituals created: {Ritual.objects.count()}")
