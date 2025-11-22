from characters.models.core.statistic import Statistic
from characters.models.mage.sorcerer import LinearMagicPath

alchemy = LinearMagicPath.objects.get_or_create(
    name="Alchemy", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 18)
conjuration = LinearMagicPath.objects.get_or_create(
    name="Conjuration", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 20)
conveyance = LinearMagicPath.objects.get_or_create(
    name="Conveyance", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 22)
divination = LinearMagicPath.objects.get_or_create(
    name="Divination", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 23)
ephemera = LinearMagicPath.objects.get_or_create(
    name="Ephemera", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 25)
enchantment = LinearMagicPath.objects.get_or_create(
    name="Enchantment", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 26)
fascination = LinearMagicPath.objects.get_or_create(
    name="Fascination", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 29)
fortune = LinearMagicPath.objects.get_or_create(
    name="Fortune", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 30)
healing = LinearMagicPath.objects.get_or_create(
    name="Healing", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 32)
hellfire = LinearMagicPath.objects.get_or_create(
    name="Hellfire", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 33)
illusion = LinearMagicPath.objects.get_or_create(
    name="Illusion", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 35)
maelstroms = LinearMagicPath.objects.get_or_create(
    name="Maelstroms", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 37)
necromancy = LinearMagicPath.objects.get_or_create(
    name="Necromancy", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 39)
necronics = LinearMagicPath.objects.get_or_create(
    name="Necronics", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 40)
oneiromancy = LinearMagicPath.objects.get_or_create(
    name="Oneiromancy", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 42)
quintessence_manipulation = LinearMagicPath.objects.get_or_create(
    name="Quintessence Manipulation", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 43)
shadows = LinearMagicPath.objects.get_or_create(
    name="Shadows", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 45)
shapeshifting = LinearMagicPath.objects.get_or_create(
    name="Shapeshifting", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 47)
starlight = LinearMagicPath.objects.get_or_create(
    name="Starlight", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 48)
summoning = LinearMagicPath.objects.get_or_create(
    name="Summoning, Binding, and Warding", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 49)
weather_control = LinearMagicPath.objects.get_or_create(
    name="Weather Control", numina_type="hedge_magic"
)[0].add_source("M20 Sorcerer", 50)

LinearMagicPath.objects.get_or_create(name="Animal Psychics", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 54)
LinearMagicPath.objects.get_or_create(name="Anti-Psychic", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 55)
LinearMagicPath.objects.get_or_create(name="Astral Projection", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 56)
LinearMagicPath.objects.get_or_create(name="Biocontrol", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 57)
LinearMagicPath.objects.get_or_create(name="Channeling", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 58)
LinearMagicPath.objects.get_or_create(name="Clairvoyance", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 59)
LinearMagicPath.objects.get_or_create(name="Cyberkinesis", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 60)
LinearMagicPath.objects.get_or_create(name="Cyberpathy", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 61)
LinearMagicPath.objects.get_or_create(
    name="Ectoplasmic Generation", numina_type="psychic"
)[0].add_source("M20 Sorcerer", 62)
LinearMagicPath.objects.get_or_create(name="Mind Shields", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 65)
LinearMagicPath.objects.get_or_create(name="Precognitition", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 65)
LinearMagicPath.objects.get_or_create(name="Psychic Healing", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 66)
LinearMagicPath.objects.get_or_create(name="Psychic Hypnosis", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 67)
LinearMagicPath.objects.get_or_create(
    name="Psychic Invisibility", numina_type="psychic"
)[0].add_source("M20 Sorcerer", 68)
LinearMagicPath.objects.get_or_create(name="Psychic Vampirism", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 69)
LinearMagicPath.objects.get_or_create(name="Psychokinesis", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 70)
LinearMagicPath.objects.get_or_create(name="Psychometry", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 72)
LinearMagicPath.objects.get_or_create(name="Psychoportation", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 73)
LinearMagicPath.objects.get_or_create(name="Pyrokinesis", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 74)
LinearMagicPath.objects.get_or_create(name="Shadow", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 74)
LinearMagicPath.objects.get_or_create(name="Synergy", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 75)
LinearMagicPath.objects.get_or_create(name="Telepathy", numina_type="psychic")[
    0
].add_source("M20 Sorcerer", 76)


for x in LinearMagicPath.objects.all():
    Statistic.objects.get_or_create(name=x.name, property_name=x.property_name)
