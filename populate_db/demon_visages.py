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


# Helper function to create traits with costs and link to visage
def create_visage_with_traits(name, house, trait_data):
    """
    Create a visage with traits.
    trait_data is a list of tuples: (name, cost, power_level)
    """
    visage = Visage.objects.get_or_create(name=name, house=house)[0]

    for trait_name, cost, power_level in trait_data:
        trait = ApocalypticFormTrait.objects.get_or_create(
            name=trait_name, house=house, defaults={"cost": cost, "power_level": power_level}
        )[0]
        # Update cost and power_level if already exists
        if trait.cost != cost or trait.power_level != power_level:
            trait.cost = cost
            trait.power_level = power_level
            trait.save()
        visage.available_traits.add(trait)

    return visage


# Devil Visages
# Cost distribution: Mix of moderate and major powers focused on leadership/fire/command
bel = create_visage_with_traits(
    "Bel",
    devils,
    [
        ("Voice of Heaven", 2, "moderate"),
        ("Aura of Legend", 2, "moderate"),
        ("Wings", 1, "minor"),
        ("Radiant Aura", 2, "moderate"),
        ("Flames of the Pit", 2, "moderate"),
        ("Command the Faithful", 3, "major"),
        ("Divine Voice", 3, "major"),
        ("Celestial Radiance", 3, "major"),
    ],
)

nusku = create_visage_with_traits(
    "Nusku",
    devils,
    [
        ("Fire Manipulation", 2, "moderate"),
        ("Burning Aura", 1, "minor"),
        ("Wings of Flame", 2, "moderate"),
        ("Ignite", 2, "moderate"),
        ("Heat Shield", 1, "minor"),
        ("Flame Weapon", 1, "minor"),
        ("Fire Immunity", 2, "moderate"),
        ("Inferno Form", 3, "major"),
    ],
)

qingu = create_visage_with_traits(
    "Qingu",
    devils,
    [
        ("Commanding Presence", 2, "moderate"),
        ("Fearsome Visage", 1, "minor"),
        ("Enhanced Charisma", 1, "minor"),
        ("Dominate Will", 3, "major"),
        ("Terror Aura", 2, "moderate"),
        ("Serpentine Form", 2, "moderate"),
        ("Venomous Strike", 2, "moderate"),
        ("Dragon Wings", 2, "moderate"),
    ],
)

# Scourge Visages
# Cost distribution: Healing, wind, and plague powers
dagan = create_visage_with_traits(
    "Dagan",
    scourges,
    [
        ("Wind Walk", 2, "moderate"),
        ("Breath of Life", 3, "major"),
        ("Healing Touch", 2, "moderate"),
        ("Windborne", 1, "minor"),
        ("Storm Call", 2, "moderate"),
        ("Purifying Winds", 2, "moderate"),
        ("Air Shield", 1, "minor"),
        ("Cyclone Form", 3, "major"),
    ],
)

anshar = create_visage_with_traits(
    "Anshar",
    scourges,
    [
        ("Plague Touch", 2, "moderate"),
        ("Disease Immunity", 1, "minor"),
        ("Pestilence Aura", 2, "moderate"),
        ("Withering Gaze", 2, "moderate"),
        ("Swarm Form", 2, "moderate"),
        ("Contagion", 3, "major"),
        ("Decay", 2, "moderate"),
        ("Death's Herald", 3, "major"),
    ],
)

ellil = create_visage_with_traits(
    "Ellil",
    scourges,
    [
        ("Far Sight", 2, "moderate"),
        ("Clairvoyance", 2, "moderate"),
        ("Omniscient Eye", 3, "major"),
        ("Wind Messenger", 1, "minor"),
        ("Sky Watcher", 2, "moderate"),
        ("Cloud Form", 2, "moderate"),
        ("Lightning Strike", 2, "moderate"),
        ("Storm Eye", 2, "moderate"),
    ],
)

# Malefactor Visages
# Cost distribution: Earth, crafting, and matter manipulation
kishar = create_visage_with_traits(
    "Kishar",
    malefactors,
    [
        ("Stone Skin", 2, "moderate"),
        ("Earth Strength", 2, "moderate"),
        ("Earthquake", 3, "major"),
        ("Merge with Stone", 2, "moderate"),
        ("Rock Form", 2, "moderate"),
        ("Mountain's Endurance", 2, "moderate"),
        ("Tremor Sense", 1, "minor"),
        ("Earthen Avatar", 3, "major"),
    ],
)

mummu = create_visage_with_traits(
    "Mummu",
    malefactors,
    [
        ("Master Craftsman", 1, "minor"),
        ("Animate Object", 2, "moderate"),
        ("Perfect Tool", 1, "minor"),
        ("Metal Shaping", 2, "moderate"),
        ("Construct Form", 2, "moderate"),
        ("Eternal Work", 2, "moderate"),
        ("Living Forge", 3, "major"),
        ("Creation's Touch", 3, "major"),
    ],
)

antu = create_visage_with_traits(
    "Antu",
    malefactors,
    [
        ("Foundation's Strength", 2, "moderate"),
        ("Unbreakable Will", 2, "moderate"),
        ("Anchor", 2, "moderate"),
        ("Dimensional Lock", 3, "major"),
        ("Reality Weaving", 4, "legendary"),
        ("Matter Control", 3, "major"),
        ("Atomic Form", 2, "moderate"),
        ("Creator's Avatar", 4, "legendary"),
    ],
)

# Fiend Visages
# Cost distribution: Time, fate, and illusion powers
neberu_seer = create_visage_with_traits(
    "Neberu Seer",
    fiends,
    [
        ("Time Sight", 2, "moderate"),
        ("Prophetic Vision", 3, "major"),
        ("Fate Reading", 2, "moderate"),
        ("Temporal Shift", 3, "major"),
        ("Illusion Weaving", 2, "moderate"),
        ("Mind's Eye", 2, "moderate"),
        ("Probability Control", 4, "legendary"),
        ("Omniscient Form", 4, "legendary"),
    ],
)

# Defiler Visages
# Cost distribution: Water, beauty, passion powers
lammasu_ocean = create_visage_with_traits(
    "Lammasu of the Ocean",
    defilers,
    [
        ("Water Breathing", 1, "minor"),
        ("Tidal Strength", 2, "moderate"),
        ("Storm Summoning", 3, "major"),
        ("Ocean's Embrace", 2, "moderate"),
        ("Aquatic Form", 2, "moderate"),
        ("Siren's Call", 2, "moderate"),
        ("Beauty's Radiance", 2, "moderate"),
        ("Tempest Avatar", 3, "major"),
    ],
)

# Devourer Visages
# Cost distribution: Beast, primal, wild powers
rabisu_hunter = create_visage_with_traits(
    "Rabisu Hunter",
    devourers,
    [
        ("Beast Form", 2, "moderate"),
        ("Predator's Senses", 1, "minor"),
        ("Claws and Fangs", 1, "minor"),
        ("Feral Strength", 2, "moderate"),
        ("Pack Leader", 2, "moderate"),
        ("Savage Fury", 2, "moderate"),
        ("Wild Empathy", 1, "minor"),
        ("Primordial Beast", 3, "major"),
    ],
)

# Slayer Visages
# Cost distribution: Death, spirit, soul powers
halaku_reaper = create_visage_with_traits(
    "Halaku Reaper",
    slayers,
    [
        ("Death's Touch", 2, "moderate"),
        ("Spirit Sight", 1, "minor"),
        ("Corpse Animation", 2, "moderate"),
        ("Life Drain", 2, "moderate"),
        ("Spectral Form", 2, "moderate"),
        ("Soul Reaping", 3, "major"),
        ("Decay Aura", 2, "moderate"),
        ("Death's Avatar", 3, "major"),
    ],
)
