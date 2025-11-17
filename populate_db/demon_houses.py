from characters.models.demon.house import DemonHouse

# The Seven Houses of the Fallen

# 1. Devils (Namaru) - The Heralds of the Dawn
devils = DemonHouse.objects.get_or_create(
    name="Devils",
    celestial_name="Namaru",
    starting_torment=4,
    domain="Command, leadership, charisma, will",
)[0]

# 2. Scourges (Asharu) - The Healers and Plague-Bringers
scourges = DemonHouse.objects.get_or_create(
    name="Scourges",
    celestial_name="Asharu",
    starting_torment=3,
    domain="Healing, disease, wind, air, life-death cycles",
)[0]

# 3. Malefactors (Annunaki) - The Artisans and Tool-Makers
malefactors = DemonHouse.objects.get_or_create(
    name="Malefactors",
    celestial_name="Annunaki",
    starting_torment=3,
    domain="Crafting, tools, matter, creation, forging",
)[0]

# 4. Fiends (Neberu) - The Seers and Temporal Manipulators
fiends = DemonHouse.objects.get_or_create(
    name="Fiends",
    celestial_name="Neberu",
    starting_torment=3,
    domain="Fates, time, future, prophecy, illusion, psychology",
)[0]

# 5. Defilers (Lammasu) - The Ocean Angels and Beautifiers
defilers = DemonHouse.objects.get_or_create(
    name="Defilers",
    celestial_name="Lammasu",
    starting_torment=3,
    domain="Water, beauty, passion, desire, the senses, inspiration",
)[0]

# 6. Devourers (Rabisu) - The Wild Beasts
devourers = DemonHouse.objects.get_or_create(
    name="Devourers",
    celestial_name="Rabisu",
    starting_torment=4,
    domain="Wild animals, nature, instinct, primal power, dominion over beasts",
)[0]

# 7. Slayers (Halaku) - The Takers of Souls
slayers = DemonHouse.objects.get_or_create(
    name="Slayers",
    celestial_name="Halaku",
    starting_torment=4,
    domain="Death, spirits, the dead, souls, endings, decay",
)[0]
