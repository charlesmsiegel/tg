from characters.models.core.attribute_block import Attribute
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.sorcerer import LinearMagicPath
from populate_db.attributes import (
    appearance,
    charisma,
    dexterity,
    intelligence,
    manipulation,
    perception,
    stamina,
    strength,
    wits,
)
from populate_db.vampire.linear_magic_path import (
    alchemy,
    conjuration,
    conveyance,
    divination,
    enchantment,
    ephemera,
    fascination,
    fortune,
    healing,
    hellfire,
    oneiromancy,
    quintessence_manipulation,
    shadows,
    shapeshifting,
    summoning,
    weather_control,
)

sf = SorcererFellowship.objects.get_or_create(name="Lone Practicitioner")[0].add_source(
    "M20 Sorcerer", 79
)
sf.favored_attributes.add(*Attribute.objects.all())
sf.favored_paths.add(*LinearMagicPath.objects.filter(numina_type="hedge_magic"))
sf = SorcererFellowship.objects.get_or_create(name="Ancient Order of the Aeon Rites")[
    0
].add_source("M20 Sorcerer", 80)
sf.favored_attributes.add(intelligence, wits)
sf.favored_paths.add(conjuration, divination, enchantment, summoning)
sf = SorcererFellowship.objects.get_or_create(name="Arcanum")[0].add_source(
    "M20 Sorcerer", 80
)
sf.favored_attributes.add(intelligence, wits)
sf.favored_paths.add(alchemy, conveyance, enchantment, summoning)
sf = SorcererFellowship.objects.get_or_create(name="Balamo'ob")[0].add_source(
    "M20 Sorcerer", 81
)
sf.favored_attributes.add(stamina, wits)
sf.favored_paths.add(alchemy, healing, shapeshifting, summoning)
sf = SorcererFellowship.objects.get_or_create(name="Children of Osiris")[0].add_source(
    "M20 Sorcerer", 82
)
sf.favored_attributes.add(intelligence, wits)
sf.favored_paths.add(ephemera, healing, alchemy, oneiromancy)
sf = SorcererFellowship.objects.get_or_create(name="Cult of Isis")[0].add_source(
    "M20 Sorcerer", 83
)
sf.favored_attributes.add(charisma, manipulation)
sf.favored_paths.add(divination, fascination, fortune, healing)
sf = SorcererFellowship.objects.get_or_create(name="Cult of Mercury")[0].add_source(
    "M20 Sorcerer", 83
)
sf.favored_attributes.add(charisma, stamina)
sf.favored_paths.add(conjuration, conveyance, divination, fortune)
sf = SorcererFellowship.objects.get_or_create(
    name="Dozen Priests of the Pythian Order"
)[0].add_source("M20 Sorcerer", 84)
sf.favored_attributes.add(charisma, intelligence)
sf.favored_paths.add(divination, healing, shapeshifting, weather_control)
sf = SorcererFellowship.objects.get_or_create(name="Fenian")[0].add_source(
    "M20 Sorcerer", 85
)
sf.favored_attributes.add(manipulation, appearance)
sf.favored_paths.add(fascination, shapeshifting, weather_control)
sf = SorcererFellowship.objects.get_or_create(name="Forn Jafnaðr")[0].add_source(
    "M20 Sorcerer", 85
)
sf.favored_attributes.add(dexterity, wits)
sf.favored_paths.add(divination, enchantment, hellfire, summoning)
sf = SorcererFellowship.objects.get_or_create(name="Maison Liban")[0].add_source(
    "M20 Sorcerer", 87
)
sf.favored_attributes.add(intelligence, manipulation)
sf.favored_paths.add(fortune, shadows, summoning, quintessence_manipulation)
sf = SorcererFellowship.objects.get_or_create(name="Mogen HaLev")[0].add_source(
    "M20 Sorcerer", 87
)
sf.favored_attributes.add(intelligence, perception)
sf.favored_paths.add(divination, ephemera, summoning, fortune, healing, weather_control)
sf = SorcererFellowship.objects.get_or_create(
    name="Nebuu-Afef, the Order of the Golden Fly"
)[0].add_source("M20 Sorcerer", 88)
sf.favored_attributes.add(strength, stamina)
sf.favored_paths.add(conjuration, hellfire, shadows, shapeshifting)
sf = SorcererFellowship.objects.get_or_create(name="Nephite Priesthood")[0].add_source(
    "M20 Sorcerer", 89
)
sf.favored_attributes.add(stamina, wits)
sf.favored_paths.add(divination, enchantment, hellfire, summoning, weather_control)
sf = SorcererFellowship.objects.get_or_create(name="Seven Thunders")[0].add_source(
    "M20 Sorcerer", 90
)
sf.favored_attributes.add(charisma, manipulation)
sf.favored_paths.add(divination, fortune, healing, hellfire)
sf = SorcererFellowship.objects.get_or_create(name="Silver Portal")[0].add_source(
    "M20 Sorcerer", 90
)
sf.favored_attributes.add(charisma, perception)
sf.favored_paths.add(ephemera, fascination, oneiromancy, shadows)
sf = SorcererFellowship.objects.get_or_create(
    name="Society of Enlightened Altruistic Ideologies"
)[0].add_source("M20 Sorcerer", 91)
sf.favored_attributes.add(intelligence, manipulation)
sf.favored_paths.add(alchemy, conjuration, conveyance, enchantment)
sf = SorcererFellowship.objects.get_or_create(name="Star Council")[0].add_source(
    "M20 Sorcerer", 92
)
sf.favored_attributes.add(perception, intelligence)
sf.favored_paths.add(enchantment, healing, shadows, quintessence_manipulation)
sf = SorcererFellowship.objects.get_or_create(name="Thal'hun")[0].add_source(
    "M20 Sorcerer", 92
)
sf.favored_attributes.add(intelligence, wits)
sf.favored_paths.add(conjuration, fortune, hellfire, quintessence_manipulation)
sf = SorcererFellowship.objects.get_or_create(
    name="U.S. Government (Project Twilight)"
)[0].add_source("M20 Sorcerer", 93)
sf.favored_attributes.add(dexterity, wits)
sf.favored_paths.add(divination, fortune, hellfire)
sf = SorcererFellowship.objects.get_or_create(name="Uzoma")[0].add_source(
    "M20 Sorcerer", 95
)
sf.favored_attributes.add(charisma, wits)
sf.favored_paths.add(alchemy, healing, summoning, quintessence_manipulation)


sf = (
    SorcererFellowship.objects.get_or_create(name="Ahl-i-Batin")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 36)
)
sf.favored_attributes.add(wits, dexterity)
sf.favored_paths.add(conjuration, conveyance, divination, fascination)
sf = (
    SorcererFellowship.objects.get_or_create(name="Bata'a")[0]
    .add_source("M20 Sorcerer", 98)
    .add_source("Sorcerer: Paths of Power", 37)
)
sf.favored_attributes.add(stamina, perception)
sf.favored_paths.add(
    enchantment,
    healing,
    alchemy,
    summoning,
    conjuration,
    conveyance,
    divination,
    fortune,
    weather_control,
)
sf = (
    SorcererFellowship.objects.get_or_create(name="Ngoma")[0]
    .add_source("M20 Sorcerer", 98)
    .add_source("Sorcerer: Paths of Power", 39)
)
sf.favored_attributes.add(intelligence, charisma)
sf.favored_paths.add(
    alchemy,
    ephemera,
    healing,
    quintessence_manipulation,
    divination,
    fascination,
    fortune,
    summoning,
)
sf = (
    SorcererFellowship.objects.get_or_create(name="Children of Knowledge")[0]
    .add_source("M20 Sorcerer", 98)
    .add_source("Sorcerer: Paths of Power", 37)
)
sf.favored_attributes.add(intelligence, stamina)
sf.favored_paths.add(alchemy, healing, enchantment)
sf = (
    SorcererFellowship.objects.get_or_create(name="Kopa Loei")[0]
    .add_source("M20 Sorcerer", 99)
    .add_source("Sorcerer: Paths of Power", 38)
)
sf.favored_attributes.add(perception, stamina)
sf.favored_paths.add(conveyance, divination, weather_control)
sf = (
    SorcererFellowship.objects.get_or_create(name="Hollow Ones")[0]
    .add_source("M20 Sorcerer", 98)
    .add_source("Sorcerer: Paths of Power", 38)
)
sf.favored_attributes.add(*Attribute.objects.all())
sf.favored_paths.add(*LinearMagicPath.objects.filter(numina_type="hedge_magic"))
sf = (
    SorcererFellowship.objects.get_or_create(name="Taftani")[0]
    .add_source("M20 Sorcerer", 99)
    .add_source("Sorcerer: Paths of Power", 41)
)
sf.favored_attributes.add(charisma, wits)
sf.favored_paths.add(alchemy, conveyance, enchantment, summoning)
sf = (
    SorcererFellowship.objects.get_or_create(name="Templar Knights")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 41)
)
sf.favored_attributes.add(strength, perception)
sf.favored_paths.add(divination, hellfire, healing, enchantment)
sf = (
    SorcererFellowship.objects.get_or_create(name="Sisters of Hippolyta")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 40)
)
sf.favored_attributes.add(charisma, stamina)
sf.favored_paths.add(healing, divination, enchantment, oneiromancy, fascination)
sf = (
    SorcererFellowship.objects.get_or_create(name="Wu Lung")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 42)
)
sf.favored_attributes.add(intelligence, perception)
sf.favored_paths.add(
    alchemy,
    conjuration,
    enchantment,
    fascination,
    healing,
    quintessence_manipulation,
    summoning,
)
sf = (
    SorcererFellowship.objects.get_or_create(name="Akashayana")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 26)
)
sf.favored_attributes.add(stamina, wits)
sf.favored_paths.add(alchemy, hellfire, healing)
sf = (
    SorcererFellowship.objects.get_or_create(name="Celestial Chorus")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 26)
)
sf.favored_attributes.add(charisma, perception)
sf.favored_paths.add(healing, hellfire, summoning)
sf = (
    SorcererFellowship.objects.get_or_create(name="Cult of Ecstasy")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 27)
)
sf.favored_attributes.add(charisma, stamina)
sf.favored_paths.add(divination, oneiromancy)
sf = (
    SorcererFellowship.objects.get_or_create(name="Dreamspeakers")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 28)
)
sf.favored_attributes.add(charisma, intelligence)
sf.favored_paths.add(fortune, alchemy, oneiromancy, summoning, ephemera)
sf = (
    SorcererFellowship.objects.get_or_create(name="Euthanatos")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 28)
)
sf.favored_attributes.add(dexterity, perception)
sf.favored_paths.add(divination, fortune, healing)
sf = (
    SorcererFellowship.objects.get_or_create(name="Order of Hermes")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 29)
)
sf.favored_attributes.add(intelligence)
sf.favored_paths.add(
    alchemy, hellfire, conjuration, summoning, quintessence_manipulation
)
sf = (
    SorcererFellowship.objects.get_or_create(name="Society of Ether")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 29)
)
sf.favored_attributes.add(intelligence, wits)
sf.favored_paths.add(alchemy, conveyance, hellfire, weather_control, enchantment)
sf = (
    SorcererFellowship.objects.get_or_create(name="Verbena")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 31)
)
sf.favored_attributes.add(wits, stamina)
sf.favored_paths.add(divination, fortune, alchemy, shapeshifting, enchantment)
sf = (
    SorcererFellowship.objects.get_or_create(name="Virtual Adepts")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 31)
)
sf.favored_attributes.add(intelligence, perception)
sf.favored_paths.add(conveyance, conjuration)
sf = (
    SorcererFellowship.objects.get_or_create(name="Iteration X")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 32)
)
sf.favored_attributes.add(intelligence, strength)
sf.favored_paths.add(
    enchantment, alchemy, hellfire, conjuration, conveyance, divination, weather_control
)
sf = (
    SorcererFellowship.objects.get_or_create(name="New World Order")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 33)
)
sf.favored_attributes.add(manipulation, wits)
sf.favored_paths.add(divination, fascination)
sf = (
    SorcererFellowship.objects.get_or_create(name="Syndicate")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 34)
)
sf.favored_attributes.add(manipulation, charisma)
sf.favored_paths.add(divination, fortune, quintessence_manipulation, enchantment)
sf = (
    SorcererFellowship.objects.get_or_create(name="Progenitors")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 34)
)
sf.favored_attributes.add(stamina, intelligence)
sf.favored_paths.add(alchemy, healing)
sf = (
    SorcererFellowship.objects.get_or_create(name="Void Engineers")[0]
    .add_source("M20 Sorcerer", 97)
    .add_source("Sorcerer: Paths of Power", 35)
)
sf.favored_attributes.add(strength, intelligence)
sf.favored_paths.add(conjuration, conveyance, hellfire)
