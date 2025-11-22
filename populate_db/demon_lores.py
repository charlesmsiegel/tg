from characters.models.demon.house import DemonHouse
from characters.models.demon.lore import Lore
from populate_db.demon_houses import (
    defilers,
    devils,
    devourers,
    fiends,
    malefactors,
    scourges,
    slayers,
)

# Scourge House Lores
lore_of_awakening = Lore.objects.get_or_create(
    name="Lore of Awakening",
    property_name="awakening",
    description="Animate living and unliving matter; enlivening objects, creation of life-like constructs",
)[0]
lore_of_awakening.houses.add(scourges)

lore_of_the_firmament = Lore.objects.get_or_create(
    name="Lore of the Firmament",
    property_name="firmament",
    description="View people and events across vast distances; long-range perception and scrying",
)[0]
lore_of_the_firmament.houses.add(scourges)

lore_of_the_winds = Lore.objects.get_or_create(
    name="Lore of the Winds",
    property_name="winds",
    description="Call and command the winds; wind summoning, air manipulation, flight assistance",
)[0]
lore_of_the_winds.houses.add(scourges)

# Devourer House Lores
lore_of_the_beast = Lore.objects.get_or_create(
    name="Lore of the Beast",
    property_name="beast",
    description="Summon, control, and possess animals; command over animal servants and familiars",
)[0]
lore_of_the_beast.houses.add(devourers)

lore_of_the_flesh = Lore.objects.get_or_create(
    name="Lore of the Flesh",
    property_name="flesh",
    description="Restore, enhance, and shape living flesh; healing, enhancement, transformation",
)[0]
lore_of_the_flesh.houses.add(devourers)

lore_of_the_wild = Lore.objects.get_or_create(
    name="Lore of the Wild",
    property_name="wild",
    description="Command green things of forest and field; plant control, nature command",
)[0]
lore_of_the_wild.houses.add(devourers)

# Devil House Lores
lore_of_the_celestials = Lore.objects.get_or_create(
    name="Lore of the Celestials",
    property_name="celestials",
    description="Enhance evocations of other demons; support and amplification powers",
)[0]
lore_of_the_celestials.houses.add(devils)

lore_of_flame = Lore.objects.get_or_create(
    name="Lore of Flame",
    property_name="flame",
    description="Summon and control fire; fire creation, manipulation, transformation",
)[0]
lore_of_flame.houses.add(devils)

lore_of_radiance = Lore.objects.get_or_create(
    name="Lore of Radiance",
    property_name="radiance",
    description="Inspire, awe, and terrify mortals; revelation, divine manifestation, awe-inspiring presence",
)[0]
lore_of_radiance.houses.add(devils)

# Slayer House Lores
lore_of_death = Lore.objects.get_or_create(
    name="Lore of Death",
    property_name="death",
    description="Secrets of death and decay; manipulation of corpses, decay, endings",
)[0]
lore_of_death.houses.add(slayers)

lore_of_the_realms = Lore.objects.get_or_create(
    name="Lore of the Realms",
    property_name="realms",
    description="Travel between physical and spirit realms; dimensional crossing, astral travel",
)[0]
lore_of_the_realms.houses.add(slayers)

lore_of_the_spirit = Lore.objects.get_or_create(
    name="Lore of the Spirit",
    property_name="spirit",
    description="Summon, command, and bind spirits of dead; necromancy, ghost control",
)[0]
lore_of_the_spirit.houses.add(slayers)

# Malefactor House Lores
lore_of_the_earth = Lore.objects.get_or_create(
    name="Lore of the Earth",
    property_name="earth",
    description="Control forces of earth, stone, mountains; geological manipulation, earthquake powers",
)[0]
lore_of_the_earth.houses.add(malefactors)

lore_of_the_forge = Lore.objects.get_or_create(
    name="Lore of the Forge",
    property_name="forge",
    description="Shape raw matter into objects of wonder; crafting, transmutation, object animation",
)[0]
lore_of_the_forge.houses.add(malefactors)

lore_of_paths = Lore.objects.get_or_create(
    name="Lore of Paths",
    property_name="paths",
    description="Find, create, or seal pathways between points; teleportation, portal creation",
)[0]
lore_of_paths.houses.add(malefactors)

lore_of_the_fundament = Lore.objects.get_or_create(
    name="Lore of the Fundament",
    property_name="fundament",
    description="Secrets of fundamental forces underlying universe; gravity, inertia, basic physics manipulation",
)[0]
lore_of_the_fundament.houses.add(malefactors)

# Fiend House Lores
lore_of_light = Lore.objects.get_or_create(
    name="Lore of Light",
    property_name="light",
    description="Manipulate light to create potent illusions; illusion creation, perception manipulation",
)[0]
lore_of_light.houses.add(fiends)

lore_of_patterns = Lore.objects.get_or_create(
    name="Lore of Patterns",
    property_name="patterns",
    description="Read Grand Design and predict future; prophecy, fate manipulation, calculation",
)[0]
lore_of_patterns.houses.add(fiends)

lore_of_portals = Lore.objects.get_or_create(
    name="Lore of Portals",
    property_name="portals",
    description="Control doorways between spaces and dimensions; dimensional travel, gateway creation",
)[0]
lore_of_portals.houses.add(fiends)

# Defiler House Lores
lore_of_longing = Lore.objects.get_or_create(
    name="Lore of Longing",
    property_name="longing",
    description="Manipulate mortal's deepest desires; desire manifestation and exploitation",
)[0]
lore_of_longing.houses.add(defilers)

lore_of_storms = Lore.objects.get_or_create(
    name="Lore of Storms",
    property_name="storms",
    description="Command power of sea and storm; water manipulation, weather control",
)[0]
lore_of_storms.houses.add(defilers)

lore_of_transfiguration = Lore.objects.get_or_create(
    name="Lore of Transfiguration",
    property_name="transfiguration",
    description="Transform into object of another's desire; shapeshifting, transformation",
)[0]
lore_of_transfiguration.houses.add(defilers)

# Common/Unaligned Lore
lore_of_humanity = Lore.objects.get_or_create(
    name="Lore of Humanity",
    property_name="humanity",
    description="Engage, influence, and manipulate mortals; human psychology and control",
)[0]
lore_of_humanity.houses.add(
    devils, scourges, malefactors, fiends, defilers, devourers, slayers
)
