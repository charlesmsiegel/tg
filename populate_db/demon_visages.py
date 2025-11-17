from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
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


# Helper function to create traits and link to visage
def create_visage_with_traits(name, house, trait_names):
    visage = Visage.objects.get_or_create(name=name, house=house)[0]

    for trait_name in trait_names:
        trait = ApocalypticFormTrait.objects.get_or_create(
            name=trait_name, house=house
        )[0]
        visage.available_traits.add(trait)

    return visage


# Devil Visages
bel = create_visage_with_traits(
    "Bel",
    devils,
    [
        "Voice of Heaven",
        "Aura of Legend",
        "Wings",
        "Radiant Aura",
        "Flames of the Pit",
        "Command the Faithful",
        "Divine Voice",
        "Celestial Radiance",
    ],
)

nusku = create_visage_with_traits(
    "Nusku",
    devils,
    [
        "Fire Manipulation",
        "Burning Aura",
        "Wings of Flame",
        "Ignite",
        "Heat Shield",
        "Flame Weapon",
        "Fire Immunity",
        "Inferno Form",
    ],
)

qingu = create_visage_with_traits(
    "Qingu",
    devils,
    [
        "Commanding Presence",
        "Fearsome Visage",
        "Enhanced Charisma",
        "Dominate Will",
        "Terror Aura",
        "Serpentine Form",
        "Venomous Strike",
        "Dragon Wings",
    ],
)

# Scourge Visages
dagan = create_visage_with_traits(
    "Dagan",
    scourges,
    [
        "Wind Walk",
        "Breath of Life",
        "Healing Touch",
        "Windborne",
        "Storm Call",
        "Purifying Winds",
        "Air Shield",
        "Cyclone Form",
    ],
)

anshar = create_visage_with_traits(
    "Anshar",
    scourges,
    [
        "Plague Touch",
        "Disease Immunity",
        "Pestilence Aura",
        "Withering Gaze",
        "Swarm Form",
        "Contagion",
        "Decay",
        "Death's Herald",
    ],
)

ellil = create_visage_with_traits(
    "Ellil",
    scourges,
    [
        "Far Sight",
        "Clairvoyance",
        "Omniscient Eye",
        "Wind Messenger",
        "Sky Watcher",
        "Cloud Form",
        "Lightning Strike",
        "Storm Eye",
    ],
)

# Malefactor Visages
kishar = create_visage_with_traits(
    "Kishar",
    malefactors,
    [
        "Stone Skin",
        "Earth Strength",
        "Earthquake",
        "Merge with Stone",
        "Rock Form",
        "Mountain's Endurance",
        "Tremor Sense",
        "Earthen Avatar",
    ],
)

mummu = create_visage_with_traits(
    "Mummu",
    malefactors,
    [
        "Master Craftsman",
        "Animate Object",
        "Perfect Tool",
        "Metal Shaping",
        "Construct Form",
        "Eternal Work",
        "Living Forge",
        "Creation's Touch",
    ],
)

antu = create_visage_with_traits(
    "Antu",
    malefactors,
    [
        "Foundation's Strength",
        "Unbreakable Will",
        "Anchor",
        "Dimensional Lock",
        "Reality Weaving",
        "Matter Control",
        "Atomic Form",
        "Creator's Avatar",
    ],
)

# Fiend Visages
neberu_seer = create_visage_with_traits(
    "Neberu Seer",
    fiends,
    [
        "Time Sight",
        "Prophetic Vision",
        "Fate Reading",
        "Temporal Shift",
        "Illusion Weaving",
        "Mind's Eye",
        "Probability Control",
        "Omniscient Form",
    ],
)

# Defiler Visages
lammasu_ocean = create_visage_with_traits(
    "Lammasu of the Ocean",
    defilers,
    [
        "Water Breathing",
        "Tidal Strength",
        "Storm Summoning",
        "Ocean's Embrace",
        "Aquatic Form",
        "Siren's Call",
        "Beauty's Radiance",
        "Tempest Avatar",
    ],
)

# Devourer Visages
rabisu_hunter = create_visage_with_traits(
    "Rabisu Hunter",
    devourers,
    [
        "Beast Form",
        "Predator's Senses",
        "Claws and Fangs",
        "Feral Strength",
        "Pack Leader",
        "Savage Fury",
        "Wild Empathy",
        "Primordial Beast",
    ],
)

# Slayer Visages
halaku_reaper = create_visage_with_traits(
    "Halaku Reaper",
    slayers,
    [
        "Death's Touch",
        "Spirit Sight",
        "Corpse Animation",
        "Life Drain",
        "Spectral Form",
        "Soul Reaping",
        "Decay Aura",
        "Death's Avatar",
    ],
)
