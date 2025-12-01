# Example Rotes from Mage Sourcebooks
# Tradition-specific and common rotes

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.focus import Practice
from characters.models.mage.rote import Rote
from populate_db.abilities import (
    athletics,
    awareness,
    brawl,
    cosmology,
    crafts,
    expression,
    medicine,
    occult,
    science,
    subterfuge,
    technology,
)
from populate_db.attributes import (
    dexterity,
    intelligence,
    manipulation,
    perception,
    stamina,
    wits,
)
from populate_db.mage.effects_INC import (
    effect_alchemical_transmutation,
    effect_blessing_of_the_one,
    effect_blood_magic_ritual,
    effect_call_the_wild_hunt,
    effect_call_totem_spirit,
    effect_channel_quintessence,
    effect_chi_healing,
    effect_create_portal_temporary,
    effect_curse_of_bad_luck,
    effect_digital_avatar,
    effect_dimensional_portal_device,
    effect_do_strike_akashic,
    effect_ecstatic_vision,
    effect_ether_ray,
    effect_flying_forces,
    effect_force_shield,
    effect_good_death,
    effect_heal_living_being_complex,
    effect_hermetic_circle_of_protection,
    effect_holy_fire,
    effect_increase_speed,
    effect_influence_mood,
    effect_information_overload,
    effect_lightning_bolt,
    effect_medicine_work_healing,
    effect_primal_transformation,
    effect_read_surface_thoughts,
    effect_reality_hack,
    effect_see_spirits,
    effect_shapeshift_into_animal_self,
    effect_spirit_journey,
    effect_summon_elemental,
    effect_teleport_self_short_range,
    effect_temporal_fugue,
    effect_wheel_of_fate,
)
from populate_db.mage.practices_INC import (
    alchemy,
    crazywisdom,
    faith,
    highritualmagick,
    martialarts,
    medicinework,
    realityhacking,
    shamanism,
    weirdscience,
    witchcraft,
    yoga,
)

# ===== AKASHIC BROTHERHOOD ROTES =====

rote = Rote.objects.get_or_create(
    name="Striking Fist of Dragon",
    effect=effect_do_strike_akashic,
    practice=martialarts,
    attribute=dexterity,
    ability=brawl,
)[0]
rote.description = (
    "The mage channels chi through their strike, dealing aggravated damage. "
    "A classic Akashic combat technique."
)
rote.add_source("Lore of the Traditions", 28)

rote = Rote.objects.get_or_create(
    name="Breath of Life Restoration",
    effect=effect_chi_healing,
    practice=medicinework,
    attribute=stamina,
    ability=medicine,
)[0]
rote.description = "The mage uses chi manipulation to heal wounds by redirecting life energy."
rote.add_source("Lore of the Traditions", 28)

rote = Rote.objects.get_or_create(
    name="Seven League Stride",
    effect=effect_increase_speed,
    practice=martialarts,
    attribute=dexterity,
    ability=athletics,
)[0]
rote.description = "Akashic technique to move at superhuman speeds through time manipulation."
rote.add_source("Lore of the Traditions", 29)

# ===== CELESTIAL CHORUS ROTES =====

rote = Rote.objects.get_or_create(
    name="Pillar of Divine Flame",
    effect=effect_holy_fire,
    practice=faith,
    attribute=stamina,
    ability=expression,
)[0]
rote.description = (
    "The mage calls down holy fire to smite the unworthy. " "A dramatic display of divine wrath."
)
rote.add_source("Lore of the Traditions", 48)

rote = Rote.objects.get_or_create(
    name="Grace of the Divine",
    effect=effect_blessing_of_the_one,
    practice=faith,
    attribute=manipulation,
    ability=expression,
)[0]
rote.description = "The mage channels divine grace to bless and strengthen allies."
rote.add_source("Lore of the Traditions", 48)

rote = Rote.objects.get_or_create(
    name="Laying On of Hands",
    effect=effect_heal_living_being_complex,
    practice=faith,
    attribute=stamina,
    ability=medicine,
)[0]
rote.description = "Classical faith healing through divine intervention and prayer."
rote.add_source("Lore of the Traditions", 49)

# ===== CULT OF ECSTASY ROTES =====

rote = Rote.objects.get_or_create(
    name="Dance of the Eternal Moment",
    effect=effect_temporal_fugue,
    practice=crazywisdom,
    attribute=dexterity,
    ability=expression,
)[0]
rote.description = (
    "The mage enters an ecstatic state where time seems to slow or stop, "
    "allowing multiple actions."
)
rote.add_source("Lore of the Traditions", 68)

rote = Rote.objects.get_or_create(
    name="Vision Quest",
    effect=effect_ecstatic_vision,
    practice=crazywisdom,
    attribute=perception,
    ability=awareness,
)[0]
rote.description = "Through ecstatic trance, the mage gains visions of past or future."
rote.add_source("Lore of the Traditions", 68)

rote = Rote.objects.get_or_create(
    name="Empathic Wave",
    effect=effect_influence_mood,
    practice=crazywisdom,
    attribute=manipulation,
    ability=expression,
)[0]
rote.description = "The mage projects their emotional state to influence others' moods."
rote.add_source("Lore of the Traditions", 69)

# ===== DREAMSPEAKER ROTES =====

rote = Rote.objects.get_or_create(
    name="Walk Between Worlds",
    effect=effect_spirit_journey,
    practice=shamanism,
    attribute=stamina,
    ability=cosmology,
)[0]
rote.description = "The shaman steps sideways into the spirit world to commune with spirits."
rote.add_source("Lore of the Traditions", 88)

rote = Rote.objects.get_or_create(
    name="Summon the Great Spirit",
    effect=effect_call_totem_spirit,
    practice=shamanism,
    attribute=manipulation,
    ability=occult,
)[0]
rote.description = "The Dreamspeaker calls upon a powerful totem spirit for aid."
rote.add_source("Lore of the Traditions", 88)

rote = Rote.objects.get_or_create(
    name="Spirit Medicine",
    effect=effect_medicine_work_healing,
    practice=medicinework,
    attribute=stamina,
    ability=medicine,
)[0]
rote.description = "Traditional healing through spirit medicine and ancestral wisdom."
rote.add_source("Lore of the Traditions", 89)

# ===== EUTHANATOS ROTES =====

rote = Rote.objects.get_or_create(
    name="The Merciful End",
    effect=effect_good_death,
    practice=yoga,
    attribute=stamina,
    ability=medicine,
)[0]
rote.description = (
    "The Euthanatos grants a peaceful death to those whose time has come, "
    "guiding them through the Wheel."
)
rote.add_source("Lore of the Traditions", 108)

rote = Rote.objects.get_or_create(
    name="Spin the Wheel",
    effect=effect_wheel_of_fate,
    practice=yoga,
    attribute=perception,
    ability=occult,
)[0]
rote.description = "The mage perceives and manipulates the threads of fate and destiny."
rote.add_source("Lore of the Traditions", 108)

rote = Rote.objects.get_or_create(
    name="Read the Tapestry",
    effect=effect_wheel_of_fate,
    practice=yoga,
    attribute=perception,
    ability=awareness,
)[0]
rote.description = "The Euthanatos reads the patterns of karma and destiny surrounding a person."
rote.add_source("Lore of the Traditions", 109)

# ===== ORDER OF HERMES ROTES =====

rote = Rote.objects.get_or_create(
    name="Ward of Solomon",
    effect=effect_hermetic_circle_of_protection,
    practice=highritualmagick,
    attribute=intelligence,
    ability=occult,
)[0]
rote.description = (
    "Classic Hermetic protective circle drawn with ritual implements and incantations."
)
rote.add_source("Lore of the Traditions", 128)

rote = Rote.objects.get_or_create(
    name="Conjuration of the Four Quarters",
    effect=effect_summon_elemental,
    practice=highritualmagick,
    attribute=manipulation,
    ability=occult,
)[0]
rote.description = "Hermetic ritual to summon and bind elemental spirits."
rote.add_source("Lore of the Traditions", 128)

rote = Rote.objects.get_or_create(
    name="The Philosopher's Work",
    effect=effect_alchemical_transmutation,
    practice=alchemy,
    attribute=intelligence,
    ability=science,
)[0]
rote.description = "Classical alchemical transmutation of base metals into gold."
rote.add_source("Lore of the Traditions", 129)

rote = Rote.objects.get_or_create(
    name="Bolt of Zeus",
    effect=effect_lightning_bolt,
    practice=highritualmagick,
    attribute=dexterity,
    ability=occult,
)[0]
rote.description = "Hermetic evocation calling down lightning from the heavens."
rote.add_source("Lore of the Traditions", 129)

# ===== SONS OF ETHER ROTES =====

rote = Rote.objects.get_or_create(
    name="Etheric Disruptor Beam",
    effect=effect_ether_ray,
    practice=weirdscience,
    attribute=dexterity,
    ability=science,
)[0]
rote.description = "The Etherite fires a beam of etheric energy from a mad science device."
rote.add_source("Lore of the Traditions", 148)

rote = Rote.objects.get_or_create(
    name="Portable Tesseract Gate",
    effect=effect_dimensional_portal_device,
    practice=weirdscience,
    attribute=intelligence,
    ability=science,
)[0]
rote.description = "A device that opens portals through higher-dimensional space."
rote.add_source("Lore of the Traditions", 148)

rote = Rote.objects.get_or_create(
    name="Anti-Gravity Harness",
    effect=effect_flying_forces,
    practice=weirdscience,
    attribute=dexterity,
    ability=technology,
)[0]
rote.description = "Weird science device that negates gravity for flight."
rote.add_source("Lore of the Traditions", 149)

# ===== VERBENA ROTES =====

rote = Rote.objects.get_or_create(
    name="The Blood Offering",
    effect=effect_blood_magic_ritual,
    practice=witchcraft,
    attribute=stamina,
    ability=occult,
)[0]
rote.description = "Verbena ritual using blood as a focus for powerful life magic."
rote.add_source("Lore of the Traditions", 168)

rote = Rote.objects.get_or_create(
    name="Beast Within",
    effect=effect_primal_transformation,
    practice=witchcraft,
    attribute=stamina,
    ability=occult,
)[0]
rote.description = "The witch transforms into an animal form, embracing primal nature."
rote.add_source("Lore of the Traditions", 168)

rote = Rote.objects.get_or_create(
    name="Summon the Horned Lord's Hunt",
    effect=effect_call_the_wild_hunt,
    practice=witchcraft,
    attribute=manipulation,
    ability=occult,
)[0]
rote.description = "Powerful ritual calling forth the Wild Hunt and its spectral hunters."
rote.add_source("Lore of the Traditions", 169)

rote = Rote.objects.get_or_create(
    name="Herbal Remedy",
    effect=effect_heal_living_being_complex,
    practice=witchcraft,
    attribute=stamina,
    ability=medicine,
)[0]
rote.description = "Natural healing using herbs, poultices, and life magic."
rote.add_source("Lore of the Traditions", 169)

# ===== VIRTUAL ADEPT ROTES =====

rote = Rote.objects.get_or_create(
    name="Root Access to Reality",
    effect=effect_reality_hack,
    practice=realityhacking,
    attribute=intelligence,
    ability=technology,
)[0]
rote.description = "The Adept hacks reality's source code to manipulate fundamental parameters."
rote.add_source("Lore of the Traditions", 188)

rote = Rote.objects.get_or_create(
    name="Upload Consciousness",
    effect=effect_digital_avatar,
    practice=realityhacking,
    attribute=intelligence,
    ability=technology,
)[0]
rote.description = "The mage projects their consciousness into the Digital Web."
rote.add_source("Lore of the Traditions", 188)

rote = Rote.objects.get_or_create(
    name="Denial of Service Attack",
    effect=effect_information_overload,
    practice=realityhacking,
    attribute=intelligence,
    ability=technology,
)[0]
rote.description = "Overwhelms target's mind with massive data streams."
rote.add_source("Lore of the Traditions", 189)

# ===== COMMON/UTILITY ROTES =====

rote = Rote.objects.get_or_create(
    name="Blink Step",
    effect=effect_teleport_self_short_range,
    practice=highritualmagick,
    attribute=dexterity,
    ability=athletics,
)[0]
rote.description = "Instant short-range teleportation for tactical advantage."
rote.add_source("How Do You Do That", 127)

rote = Rote.objects.get_or_create(
    name="Peer Into Mind",
    effect=effect_read_surface_thoughts,
    practice=highritualmagick,
    attribute=perception,
    ability=occult,
)[0]
rote.description = "Read the surface thoughts and immediate intentions of a target."
rote.add_source("Mage: the Ascension 20th Anniversary Edition", 519)

rote = Rote.objects.get_or_create(
    name="Wall of Force",
    effect=effect_force_shield,
    practice=highritualmagick,
    attribute=stamina,
    ability=occult,
)[0]
rote.description = "Create a barrier of solidified force energy for protection."
rote.add_source("Mage: the Ascension 20th Anniversary Edition", 517)

rote = Rote.objects.get_or_create(
    name="Spirit Sight",
    effect=effect_see_spirits,
    practice=shamanism,
    attribute=perception,
    ability=awareness,
)[0]
rote.description = "Perceive spirits and the Penumbra while in the material world."
rote.add_source("Mage: the Ascension 20th Anniversary Edition", 521)

rote = Rote.objects.get_or_create(
    name="Jinx",
    effect=effect_curse_of_bad_luck,
    practice=witchcraft,
    attribute=manipulation,
    ability=occult,
)[0]
rote.description = "Curse a target with persistent bad luck and misfortune."
rote.add_source("Mage: the Ascension 20th Anniversary Edition", 516)

rote = Rote.objects.get_or_create(
    name="Gateway Between Spaces",
    effect=effect_create_portal_temporary,
    practice=highritualmagick,
    attribute=intelligence,
    ability=cosmology,
)[0]
rote.description = "Open a temporary portal connecting two locations."
rote.add_source("How Do You Do That", 128)

rote = Rote.objects.get_or_create(
    name="Beast Form",
    effect=effect_shapeshift_into_animal_self,
    practice=witchcraft,
    attribute=stamina,
    ability=occult,
)[0]
rote.description = "Transform into an animal shape while retaining human mind."
rote.add_source("How Do You Do That", 34)

rote = Rote.objects.get_or_create(
    name="Draw Upon the Wellspring",
    effect=effect_channel_quintessence,
    practice=highritualmagick,
    attribute=stamina,
    ability=occult,
)[0]
rote.description = "Channel Quintessence from a Node or Tass for magical use."
rote.add_source("Mage: the Ascension 20th Anniversary Edition", 520)
