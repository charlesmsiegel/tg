from characters.models.demon.house import House
from items.models.demon.relic import Relic

# Get the houses
devils = House.objects.get(name="Devils")
scourges = House.objects.get(name="Scourges")
malefactors = House.objects.get(name="Malefactors")

# Devil House Relics

pyrestone = Relic.objects.get_or_create(
    name="Pyrestone (Frozen Flames)",
    house=devils,
    relic_type="house_specific",
    lore_used="Lore of Flame",
    power="Clear crystal containing trapped fire; activated remotely; explodes with Ignite evocation intensity",
    material="Clear crystal",
    dice_pool=8,
    difficulty=7,
)[0]

first_tongue_scripture = Relic.objects.get_or_create(
    name="First Tongue Scripture",
    house=devils,
    relic_type="house_specific",
    lore_used="Lore of Radiance",
    power="Mortals who learn become immune to illusions and demonic Revelation; can compel others through subconscious commands",
    material="Ancient texts",
    difficulty=8,
)[0]

# Scourge House Relics

armor_of_air = Relic.objects.get_or_create(
    name="Armor of Air",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of the Winds",
    power="Brooch/buckle generating protective air shell; 6 dice pool for ranged attack soak",
    material="Silver brooch or buckle",
    dice_pool=6,
    difficulty=6,
)[0]

cordial_of_dagan = Relic.objects.get_or_create(
    name="Cordial of Dagan",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of Awakening",
    power="Flask that converts liquids to heal sickness; 8 dice pool for healing",
    material="Crystal flask",
    dice_pool=8,
    difficulty=7,
)[0]

crystal_ball = Relic.objects.get_or_create(
    name="Crystal Ball",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of the Firmament",
    power="Round crystal sphere for scrying; difficulty varies by target name knowledge",
    material="Crystal sphere",
    difficulty=7,
)[0]

eagle_eyes = Relic.objects.get_or_create(
    name="Eagle Eyes",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of the Firmament",
    power="Crystal lenses improving sight 10-fold; -3 difficulty to Perception rolls",
    material="Crystal lenses",
    difficulty=4,
)[0]

jar_of_winds = Relic.objects.get_or_create(
    name="Jar of Winds",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of the Winds",
    power="Container with trapped winds; 8 dice pool for force effects",
    material="Clay or glass jar",
    dice_pool=8,
    difficulty=7,
)[0]

needs_beacon = Relic.objects.get_or_create(
    name="Need's Beacon",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of the Winds",
    power="Glass tube/crystal bauble; sends distress cry to creator when broken",
    material="Glass tube or crystal",
    difficulty=6,
)[0]

plague_knife = Relic.objects.get_or_create(
    name="Plague-Knife",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of Awakening",
    power="Black dagger dealing disease; 10 dice pool; inflicts bashing disease damage daily",
    material="Black iron dagger",
    dice_pool=10,
    difficulty=7,
)[0]

# Malefactor House Relics

thala_mkudan = Relic.objects.get_or_create(
    name="Thala-m'kudan (The Hidden Mountain)",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of Paths",
    power="Largest mountain ever existed, now in platinum shoebox; sacred meeting place for Annunaki",
    material="Mountain in platinum box",
    complexity=10,
    is_permanent=True,
    difficulty=10,
)[0]

philosophers_stone = Relic.objects.get_or_create(
    name="Philosopher's Stone (Crucible)",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of the Forge",
    power="Convert metals/stones to other materials; 6 dice pool; affects cubic yards equal to successes",
    material="Transmutation stone",
    dice_pool=6,
    difficulty=8,
)[0]

syir = Relic.objects.get_or_create(
    name="Syir (Black Ur-Metal)",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of the Forge",
    power="Spiritually pure metal with awakened essence; counts as Superb material; using it botches on 1-2",
    material="Black ur-metal",
    is_permanent=True,
    difficulty=9,
)[0]

warriors_of_broken_ground = Relic.objects.get_or_create(
    name="Warriors of the Broken Ground",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of the Earth",
    power="Stone automatons rising from earth; activated metal cube creates warriors based on Faith spent",
    material="Metal cube",
    dice_pool=8,
    difficulty=7,
)[0]

tesseract_generator = Relic.objects.get_or_create(
    name="Tesseract Generator",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of Paths",
    power="Warps space causing movement difficulty; 6 dice pool; affects radius = Faith yards",
    material="Complex mechanism",
    dice_pool=6,
    difficulty=8,
    complexity=9,
)[0]

stone_scripture = Relic.objects.get_or_create(
    name="Stone Scripture (Stonespeech)",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of the Forge",
    power="Annunaki secret language encoded in crystals; only Malefactors can create or read",
    material="Encoded crystals",
    is_permanent=True,
    difficulty=7,
)[0]

# Generic Enhanced Relics (examples)

simple_tool = Relic.objects.get_or_create(
    name="Enhanced Simple Tool",
    relic_type="enhanced",
    complexity=1,
    power="Simple tool enhanced with demonic power",
    difficulty=4,
)[0]

complex_device = Relic.objects.get_or_create(
    name="Enhanced Complex Device",
    relic_type="enhanced",
    complexity=5,
    power="Complex device with multiple moving parts enhanced with demonic power",
    difficulty=7,
)[0]

# Generic Enchanted Relics (examples)

enchanted_weapon = Relic.objects.get_or_create(
    name="Enchanted Weapon",
    relic_type="enchanted",
    lore_used="Lore of the Forge",
    power="Weapon containing specific lore effect",
    material="Steel",
    is_permanent=True,
    difficulty=7,
)[0]

enchanted_armor = Relic.objects.get_or_create(
    name="Enchanted Armor",
    relic_type="enchanted",
    lore_used="Lore of the Earth",
    power="Armor with protective lore effect",
    material="Iron",
    is_permanent=True,
    difficulty=8,
)[0]
