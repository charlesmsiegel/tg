from characters.models.demon.house import House
from characters.models.demon.visage import Visage

# Get the houses
devils = House.objects.get(name="Devils")
scourges = House.objects.get(name="Scourges")
malefactors = House.objects.get(name="Malefactors")
fiends = House.objects.get(name="Fiends")
defilers = House.objects.get(name="Defilers")
devourers = House.objects.get(name="Devourers")
slayers = House.objects.get(name="Slayers")

# Devil Visages
bel = Visage.objects.get_or_create(
    name="Bel",
    house=devils,
    abilities=[
        "Voice of Heaven",
        "Aura of Legend",
        "Wings",
        "Radiant Aura",
        "Flames of the Pit",
        "Command the Faithful",
        "Divine Voice",
        "Celestial Radiance",
    ],
)[0]

nusku = Visage.objects.get_or_create(
    name="Nusku",
    house=devils,
    abilities=[
        "Fire Manipulation",
        "Burning Aura",
        "Wings of Flame",
        "Ignite",
        "Heat Shield",
        "Flame Weapon",
        "Fire Immunity",
        "Inferno Form",
    ],
)[0]

qingu = Visage.objects.get_or_create(
    name="Qingu",
    house=devils,
    abilities=[
        "Commanding Presence",
        "Fearsome Visage",
        "Enhanced Charisma",
        "Dominate Will",
        "Terror Aura",
        "Serpentine Form",
        "Venomous Strike",
        "Dragon Wings",
    ],
)[0]

# Scourge Visages
dagan = Visage.objects.get_or_create(
    name="Dagan",
    house=scourges,
    abilities=[
        "Wind Walk",
        "Breath of Life",
        "Healing Touch",
        "Windborne",
        "Storm Call",
        "Purifying Winds",
        "Air Shield",
        "Cyclone Form",
    ],
)[0]

anshar = Visage.objects.get_or_create(
    name="Anshar",
    house=scourges,
    abilities=[
        "Plague Touch",
        "Disease Immunity",
        "Pestilence Aura",
        "Withering Gaze",
        "Swarm Form",
        "Contagion",
        "Decay",
        "Death's Herald",
    ],
)[0]

ellil = Visage.objects.get_or_create(
    name="Ellil",
    house=scourges,
    abilities=[
        "Far Sight",
        "Clairvoyance",
        "Omniscient Eye",
        "Wind Messenger",
        "Sky Watcher",
        "Cloud Form",
        "Lightning Strike",
        "Storm Eye",
    ],
)[0]

# Malefactor Visages
kishar = Visage.objects.get_or_create(
    name="Kishar",
    house=malefactors,
    abilities=[
        "Stone Skin",
        "Earth Strength",
        "Earthquake",
        "Merge with Stone",
        "Rock Form",
        "Mountain's Endurance",
        "Tremor Sense",
        "Earthen Avatar",
    ],
)[0]

mummu = Visage.objects.get_or_create(
    name="Mummu",
    house=malefactors,
    abilities=[
        "Master Craftsman",
        "Animate Object",
        "Perfect Tool",
        "Metal Shaping",
        "Construct Form",
        "Eternal Work",
        "Living Forge",
        "Creation's Touch",
    ],
)[0]

antu = Visage.objects.get_or_create(
    name="Antu",
    house=malefactors,
    abilities=[
        "Foundation's Strength",
        "Unbreakable Will",
        "Anchor",
        "Dimensional Lock",
        "Reality Weaving",
        "Matter Control",
        "Atomic Form",
        "Creator's Avatar",
    ],
)[0]

# Fiend Visages (generic examples)
neberu_seer = Visage.objects.get_or_create(
    name="Neberu Seer",
    house=fiends,
    abilities=[
        "Time Sight",
        "Prophetic Vision",
        "Fate Reading",
        "Temporal Shift",
        "Illusion Weaving",
        "Mind's Eye",
        "Probability Control",
        "Omniscient Form",
    ],
)[0]

# Defiler Visages (generic examples)
lammasu_ocean = Visage.objects.get_or_create(
    name="Lammasu of the Ocean",
    house=defilers,
    abilities=[
        "Water Breathing",
        "Tidal Strength",
        "Storm Summoning",
        "Ocean's Embrace",
        "Aquatic Form",
        "Siren's Call",
        "Beauty's Radiance",
        "Tempest Avatar",
    ],
)[0]

# Devourer Visages (generic examples)
rabisu_hunter = Visage.objects.get_or_create(
    name="Rabisu Hunter",
    house=devourers,
    abilities=[
        "Beast Form",
        "Predator's Senses",
        "Claws and Fangs",
        "Feral Strength",
        "Pack Leader",
        "Savage Fury",
        "Wild Empathy",
        "Primordial Beast",
    ],
)[0]

# Slayer Visages (generic examples)
halaku_reaper = Visage.objects.get_or_create(
    name="Halaku Reaper",
    house=slayers,
    abilities=[
        "Death's Touch",
        "Spirit Sight",
        "Corpse Animation",
        "Life Drain",
        "Spectral Form",
        "Soul Reaping",
        "Decay Aura",
        "Death's Avatar",
    ],
)[0]
