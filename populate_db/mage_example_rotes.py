# Example Rotes from Mage Sourcebooks
# Tradition-specific and common rotes

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.focus import Practice
from characters.models.mage.rote import Rote

from populate_db.attributes import perception, intelligence, wits, manipulation, dexterity, stamina
from populate_db.abilities import awareness, occult, cosmology, brawl, athletics, science, technology, crafts, medicine, expression, subterfuge

from populate_db.practices_INC import highritualmagick, martialarts, faith, shamanism, witchcraft, alchemy, weirdscience, realityhacking, crazywisdom, yoga, medicinework

# ===== AKASHIC BROTHERHOOD ROTES =====

effect = Effect.objects.get_or_create(name="Do Strike (Akashic)")[0]
rote = Rote.objects.get_or_create(
    name="Striking Fist of Dragon",
    effect=effect,
    practice=martialarts,
    attribute=dexterity,
    ability=brawl,
)[0]
rote.description = (
    "The mage channels chi through their strike, dealing aggravated damage. "
    "A classic Akashic combat technique."
)
rote.add_source("Lore of the Traditions", 28)

effect = Effect.objects.get_or_create(name="Chi Healing")[0]
rote = Rote.objects.get_or_create(
    name="Breath of Life Restoration",
    effect=effect,
    practice=medicinework,
    attribute=stamina,
    ability=medicine,
)[0]
rote.description = (
    "The mage uses chi manipulation to heal wounds by redirecting life energy."
)
rote.add_source("Lore of the Traditions", 28)

effect = Effect.objects.get_or_create(name="Increase Speed")[0]
rote = Rote.objects.get_or_create(
    name="Seven League Stride",
    effect=effect,
    practice=martialarts,
    attribute=dexterity,
    ability=athletics,
)[0]
rote.description = (
    "Akashic technique to move at superhuman speeds through time manipulation."
)
rote.add_source("Lore of the Traditions", 29)

# ===== CELESTIAL CHORUS ROTES =====

effect = Effect.objects.get_or_create(name="Holy Fire")[0]
rote = Rote.objects.get_or_create(
    name="Pillar of Divine Flame",
    effect=effect,
    practice=faith,
    attribute=stamina,
    ability=expression,
)[0]
rote.description = (
    "The mage calls down holy fire to smite the unworthy. "
    "A dramatic display of divine wrath."
)
rote.add_source("Lore of the Traditions", 48)

effect = Effect.objects.get_or_create(name="Blessing of the One")[0]
rote = Rote.objects.get_or_create(
    name="Grace of the Divine",
    effect=effect,
    practice=faith,
    attribute=manipulation,
    ability=expression,
)[0]
rote.description = "The mage channels divine grace to bless and strengthen allies."
rote.add_source("Lore of the Traditions", 48)

effect = Effect.objects.get_or_create(name="Heal Living Being (Complex)")
rote = Rote.objects.get_or_create(
    name="Laying On of Hands",
    effect=effect,
    practice=faith,
    attribute=stamina,
    ability=medicine,
)[0]
rote.description = "Classical faith healing through divine intervention and prayer."
rote.add_source("Lore of the Traditions", 49)

# ===== CULT OF ECSTASY ROTES =====

effect = Effect.objects.get_or_create(name="Temporal Fugue")[0]
rote = Rote.objects.get_or_create(
    name="Dance of the Eternal Moment",
    effect=effect,
    practice=crazywisdom,
    attribute=dexterity,
    ability=expression,
)[0]
rote.description = (
    "The mage enters an ecstatic state where time seems to slow or stop, "
    "allowing multiple actions."
)
rote.add_source("Lore of the Traditions", 68)

effect = Effect.objects.get_or_create(name="Ecstatic Vision")[0]
rote = Rote.objects.get_or_create(
    name="Vision Quest",
    effect=effect,
    practice=crazywisdom,
    attribute=perception,
    ability=awareness,
)[0]
rote.description = "Through ecstatic trance, the mage gains visions of past or future."
rote.add_source("Lore of the Traditions", 68)

effect = Effect.objects.get_or_create(name="Influence Mood")[0]
rote = Rote.objects.get_or_create(
    name="Empathic Wave",
    effect=effect,
    practice=crazywisdom,
    attribute=manipulation,
    ability=expression,
)[0]
rote.description = "The mage projects their emotional state to influence others' moods."
rote.add_source("Lore of the Traditions", 69)

# ===== DREAMSPEAKER ROTES =====

effect = Effect.objects.get_or_create(name="Spirit Journey")[0]
rote = Rote.objects.get_or_create(
    name="Walk Between Worlds",
    effect=effect,
    practice=shamanism,
    attribute=stamina,
    ability=cosmology,
)[0]
rote.description = (
    "The shaman steps sideways into the spirit world to commune with spirits."
)
rote.add_source("Lore of the Traditions", 88)

effect = Effect.objects.get_or_create(name="Call Totem Spirit")[0]
rote = Rote.objects.get_or_create(
    name="Summon the Great Spirit",
    effect=effect,
    practice=shamanism,
    attribute=manipulation,
    ability=occult,
)[0]
rote.description = "The Dreamspeaker calls upon a powerful totem spirit for aid."
rote.add_source("Lore of the Traditions", 88)

effect = Effect.objects.get_or_create(name="Medicine Work Healing")[0]
rote = Rote.objects.get_or_create(
    name="Spirit Medicine",
    effect=effect,
    practice=medicinework,
    attribute=stamina,
    ability=medicine,
)[0]
rote.description = "Traditional healing through spirit medicine and ancestral wisdom."
rote.add_source("Lore of the Traditions", 89)

# ===== EUTHANATOS ROTES =====

effect = Effect.objects.get_or_create(name="Good Death")[0]
rote = Rote.objects.get_or_create(
    name="The Merciful End",
    effect=effect,
    practice=yoga,
    attribute=stamina,
    ability=medicine,
)[0]
rote.description = (
    "The Euthanatos grants a peaceful death to those whose time has come, "
    "guiding them through the Wheel."
)
rote.add_source("Lore of the Traditions", 108)

effect = Effect.objects.get_or_create(name="Wheel of Fate")[0]
rote = Rote.objects.get_or_create(
    name="Spin the Wheel",
    effect=effect,
    practice=yoga,
    attribute=perception,
    ability=occult,
)[0]
rote.description = "The mage perceives and manipulates the threads of fate and destiny."
rote.add_source("Lore of the Traditions", 108)

effect = Effect.objects.get_or_create(name="Sense Fate and Fortune", entropy=1)[0]
rote = Rote.objects.get_or_create(
    name="Read the Tapestry",
    effect=effect,
    practice=yoga,
    attribute=perception,
    ability=awareness,
)[0]
rote.description = (
    "The Euthanatos reads the patterns of karma and destiny surrounding a person."
)
rote.add_source("Lore of the Traditions", 109)

# ===== ORDER OF HERMES ROTES =====

effect = Effect.objects.get_or_create(name="Hermetic Circle of Protection")[0]
rote = Rote.objects.get_or_create(
    name="Ward of Solomon",
    effect=effect,
    practice=highritualmagick,
    attribute=intelligence,
    ability=occult,
)[0]
rote.description = (
    "Classic Hermetic protective circle drawn with ritual implements and incantations."
)
rote.add_source("Lore of the Traditions", 128)

effect = Effect.objects.get_or_create(name="Summon Elemental")[0]
rote = Rote.objects.get_or_create(
    name="Conjuration of the Four Quarters",
    effect=effect,
    practice=highritualmagick,
    attribute=manipulation,
    ability=occult,
)[0]
rote.description = "Hermetic ritual to summon and bind elemental spirits."
rote.add_source("Lore of the Traditions", 128)

effect = Effect.objects.get_or_create(name="Alchemical Transmutation")[0]
rote = Rote.objects.get_or_create(
    name="The Philosopher's Work",
    effect=effect,
    practice=alchemy,
    attribute=intelligence,
    ability=science,
)[0]
rote.description = "Classical alchemical transmutation of base metals into gold."
rote.add_source("Lore of the Traditions", 129)

effect = Effect.objects.get_or_create(name="Lightning Bolt")[0]
rote = Rote.objects.get_or_create(
    name="Bolt of Zeus",
    effect=effect,
    practice=highritualmagick,
    attribute=dexterity,
    ability=occult,
)[0]
rote.description = "Hermetic evocation calling down lightning from the heavens."
rote.add_source("Lore of the Traditions", 129)

# ===== SONS OF ETHER ROTES =====

effect = Effect.objects.get_or_create(name="Ether Ray")[0]
rote = Rote.objects.get_or_create(
    name="Etheric Disruptor Beam",
    effect=effect,
    practice=weirdscience,
    attribute=dexterity,
    ability=science,
)[0]
rote.description = (
    "The Etherite fires a beam of etheric energy from a mad science device."
)
rote.add_source("Lore of the Traditions", 148)

effect = Effect.objects.get_or_create(name="Dimensional Portal Device")[0]
rote = Rote.objects.get_or_create(
    name="Portable Tesseract Gate",
    effect=effect,
    practice=weirdscience,
    attribute=intelligence,
    ability=science,
)[0]
rote.description = "A device that opens portals through higher-dimensional space."
rote.add_source("Lore of the Traditions", 148)

effect = Effect.objects.get_or_create(name="Flying (Forces)")
rote = Rote.objects.get_or_create(
    name="Anti-Gravity Harness",
    effect=effect,
    practice=weirdscience,
    attribute=dexterity,
    ability=technology,
)[0]
rote.description = "Weird science device that negates gravity for flight."
rote.add_source("Lore of the Traditions", 149)

# ===== VERBENA ROTES =====

effect = Effect.objects.get_or_create(name="Blood Magic Ritual")[0]
rote = Rote.objects.get_or_create(
    name="The Blood Offering",
    effect=effect,
    practice=witchcraft,
    attribute=stamina,
    ability=occult,
)[0]
rote.description = "Verbena ritual using blood as a focus for powerful life magic."
rote.add_source("Lore of the Traditions", 168)

effect = Effect.objects.get_or_create(name="Primal Transformation")[0]
rote = Rote.objects.get_or_create(
    name="Beast Within",
    effect=effect,
    practice=witchcraft,
    attribute=stamina,
    ability=occult,
)[0]
rote.description = "The witch transforms into an animal form, embracing primal nature."
rote.add_source("Lore of the Traditions", 168)

effect = Effect.objects.get_or_create(name="Call the Wild Hunt")[0]
rote = Rote.objects.get_or_create(
    name="Summon the Horned Lord's Hunt",
    effect=effect,
    practice=witchcraft,
    attribute=manipulation,
    ability=occult,
)[0]
rote.description = (
    "Powerful ritual calling forth the Wild Hunt and its spectral hunters."
)
rote.add_source("Lore of the Traditions", 169)

effect = Effect.objects.get_or_create(name="Heal Living Being (Complex)")
rote = Rote.objects.get_or_create(
    name="Herbal Remedy",
    effect=effect,
    practice=witchcraft,
    attribute=stamina,
    ability=medicine,
)[0]
rote.description = "Natural healing using herbs, poultices, and life magic."
rote.add_source("Lore of the Traditions", 169)

# ===== VIRTUAL ADEPT ROTES =====

effect = Effect.objects.get_or_create(name="Reality Hack")[0]
rote = Rote.objects.get_or_create(
    name="Root Access to Reality",
    effect=effect,
    practice=realityhacking,
    attribute=intelligence,
    ability=technology,
)[0]
rote.description = (
    "The Adept hacks reality's source code to manipulate fundamental parameters."
)
rote.add_source("Lore of the Traditions", 188)

effect = Effect.objects.get_or_create(name="Digital Avatar")[0]
rote = Rote.objects.get_or_create(
    name="Upload Consciousness",
    effect=effect,
    practice=realityhacking,
    attribute=intelligence,
    ability=technology,
)[0]
rote.description = "The mage projects their consciousness into the Digital Web."
rote.add_source("Lore of the Traditions", 188)

effect = Effect.objects.get_or_create(name="Information Overload")[0]
rote = Rote.objects.get_or_create(
    name="Denial of Service Attack",
    effect=effect,
    practice=realityhacking,
    attribute=intelligence,
    ability=technology,
)[0]
rote.description = "Overwhelms target's mind with massive data streams."
rote.add_source("Lore of the Traditions", 189)

# ===== COMMON/UTILITY ROTES =====

effect = Effect.objects.get_or_create(name="Teleport Self (Short Range)")
rote = Rote.objects.get_or_create(
    name="Blink Step",
    effect=effect,
    practice=highritualmagick,
    attribute=dexterity,
    ability=athletics,
)[0]
rote.description = "Instant short-range teleportation for tactical advantage."
rote.add_source("How Do You Do That", 127)

effect = Effect.objects.get_or_create(name="Read Surface Thoughts")[0]
rote = Rote.objects.get_or_create(
    name="Peer Into Mind",
    effect=effect,
    practice=highritualmagick,
    attribute=perception,
    ability=occult,
)[0]
rote.description = "Read the surface thoughts and immediate intentions of a target."
rote.add_source("Mage: the Ascension 20th Anniversary Edition", 519)

effect = Effect.objects.get_or_create(name="Force Shield")[0]
rote = Rote.objects.get_or_create(
    name="Wall of Force",
    effect=effect,
    practice=highritualmagick,
    attribute=stamina,
    ability=occult,
)[0]
rote.description = "Create a barrier of solidified force energy for protection."
rote.add_source("Mage: the Ascension 20th Anniversary Edition", 517)

effect = Effect.objects.get_or_create(name="See Spirits")[0]
rote = Rote.objects.get_or_create(
    name="Spirit Sight",
    effect=effect,
    practice=shamanism,
    attribute=perception,
    ability=awareness,
)[0]
rote.description = "Perceive spirits and the Penumbra while in the material world."
rote.add_source("Mage: the Ascension 20th Anniversary Edition", 521)

effect = Effect.objects.get_or_create(name="Curse of Bad Luck")[0]
rote = Rote.objects.get_or_create(
    name="Jinx",
    effect=effect,
    practice=witchcraft,
    attribute=manipulation,
    ability=occult,
)[0]
rote.description = "Curse a target with persistent bad luck and misfortune."
rote.add_source("Mage: the Ascension 20th Anniversary Edition", 516)

effect = Effect.objects.get_or_create(name="Create Portal (Temporary)")
rote = Rote.objects.get_or_create(
    name="Gateway Between Spaces",
    effect=effect,
    practice=highritualmagick,
    attribute=intelligence,
    ability=cosmology,
)[0]
rote.description = "Open a temporary portal connecting two locations."
rote.add_source("How Do You Do That", 128)

effect = Effect.objects.get_or_create(name="Shapeshift into Animal (Self)")
rote = Rote.objects.get_or_create(
    name="Beast Form",
    effect=effect,
    practice=witchcraft,
    attribute=stamina,
    ability=occult,
)[0]
rote.description = "Transform into an animal shape while retaining human mind."
rote.add_source("How Do You Do That", 34)

effect = Effect.objects.get_or_create(name="Channel Quintessence")[0]
rote = Rote.objects.get_or_create(
    name="Draw Upon the Wellspring",
    effect=effect,
    practice=highritualmagick,
    attribute=stamina,
    ability=occult,
)[0]
rote.description = "Channel Quintessence from a Node or Tass for magical use."
rote.add_source("Mage: the Ascension 20th Anniversary Edition", 520)
