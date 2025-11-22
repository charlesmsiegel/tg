from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.focus import Practice
from characters.models.mage.rote import Rote
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


def rote_helper(name, sphere_dict, practice, attribute, ability, description=""):
    return Rote.objects.get_or_create(
        name=name,
        description=description,
        effect=Effect.objects.get_or_create(
            name=name, **sphere_dict, description=description
        )[0],
        practice=Practice.objects.get_or_create(name=practice)[0],
        attribute=Attribute.objects.get_or_create(name=attribute)[0],
        ability=Ability.objects.get_or_create(name=ability)[0],
    )[0]


rote_helper("Ceration", {"matter": 3}, "Alchemy", "Dexterity", "Crafts").add_source(
    "Prism of Focus", 34
)
rote_helper(
    "Elevate Material",
    {"matter": 2, "prime": 2},
    "Alchemy",
    "Intelligence",
    "Occult",
).add_source("Prism of Focus", 34)
rote_helper(
    "Putrefaction", {"entropy": 3}, "Alchemy", "Intelligence", "Science"
).add_source("Prism of Focus", 34)
rote_helper(
    "Releasing the Beast Within",
    {"life": 3, "mind": 3},
    "Animalism",
    "Perception",
    "Survival",
).add_source("Prism of Focus", 37)
rote_helper(
    "Talk With the Animals", {"mind": 2}, "Animalism", "Charisma", "Animal Kinship"
).add_source("Prism of Focus", 38)
rote_helper(
    "Quiet as a Mouse", {"forces": 2}, "Animalism", "Dexterity", "Stealth"
).add_source("Prism of Focus", 38)
rote_helper(
    "Call of the Heart", {"spirit": 2}, "Animalism", "Charisma", "Awareness"
).add_source("Prism of Focus", 38)
rote_helper(
    "Mine!", {"mind": 3}, "Appropriation", "Charisma", "Intimidation"
).add_source("Prism of Focus", 40)
rote_helper(
    "Biased Contract",
    {"entropy": 3, "mind": 4, "matter": 1},
    "Appropriation",
    "Intelligence",
    "Law",
).add_source("Prism of Focus", 41)
rote_helper(
    "I Got What You Need", {"mind": 4}, "Art of Desire", "Manipulation", "Subterfuge"
).add_source("Prism of Focus", 43)
rote_helper(
    "I Know a Guy",
    {"mind": 2, "correspondence": 3},
    "Art of Desire",
    "Intelligence",
    "Politics",
).add_source("Prism of Focus", 43)
rote_helper(
    "If I Can't Find It, It Doesn't Exist",
    {"matter": 1, "correspondence": 3},
    "Art of Desire",
    "Perception",
    "Awareness",
).add_source("Prism of Focus", 43)
rote_helper(
    "Logistics",
    {"correspondence": 2, "matter": 1},
    "Art of Desire",
    "Charisma",
    "Leadership",
).add_source("Prism of Focus", 43)
rote_helper(
    "Tell Me What You Want", {"mind": 3}, "Art of Desire", "Charisma", "Etiquette"
).add_source("Prism of Focus", 44)
rote_helper(
    "Soothe the Savage Beast (Animal)",
    {"mind": 2},
    "Bardism",
    "Manipulation",
    "Empathy",
).add_source("Prism of Focus", 46)
rote_helper(
    "Soothe the Savage Beast (Human)", {"mind": 4}, "Bardism", "Manipulation", "Empathy"
).add_source("Prism of Focus", 46)
rote_helper(
    "Martial Anthem", {"mind": 2, "correspondence": 3}, "Bardism", "Charisma", "Art"
).add_source("Prism of Focus", 46)
rote_helper(
    "Inhabit the Character", {"spirit": 2, "life": 2}, "Bardism", "Charisma", "Art"
).add_source("Prism of Focus", 47)
rote_helper(
    "Spit in the Face of God", {"prime": 4}, "Chaos Magick", "Manipulation", "Awareness"
).add_source("Prism of Focus", 49)
rote_helper(
    "Unorthodox Reading",
    {"time": 2, "correspondence": 2},
    "Chaos Magick",
    "Intelligence",
    "Esoterica",
).add_source("Prism of Focus", 49)
rote_helper(
    "Inadvisable Summons", {"spirit": 2}, "Chaos Magick", "Intelligence", "Esoterica"
).add_source("Prism of Focus", 50)
rote_helper(
    "Evoke Egregore", {"spirit": 2}, "Chaos Magick", "Charisma", "Intuition"
).add_source("Prism of Focus", 50)
rote_helper(
    "Gift of the Self", {"prime": 3}, "Charity", "Charisma", "Crafts"
).add_source("Prism of Focus", 51)
rote_helper(
    "Laying a Helping Hand", {"life": 3}, "Charity", "Manipulation", "Empathy"
).add_source("Prism of Focus", 52)
rote_helper("Lend a Hand", {"mind": 3}, "Charity", "Charisma", "Expression").add_source(
    "Prism of Focus", 52
)
rote_helper(
    "Magickal Metallurgy: Chronium",
    {"matter": 4, "time": 3},
    "Craftwork",
    "Strength",
    "Crafts",
).add_source("Prism of Focus", 54)
rote_helper(
    "Magickal Metallurgy: Aetherium",
    {"matter": 4, "prime": 3},
    "Craftwork",
    "Strength",
    "Crafts",
).add_source("Prism of Focus", 54)
rote_helper(
    "Magickal Metallurgy: Astralium",
    {"matter": 4, "mind": 4},
    "Craftwork",
    "Strength",
    "Crafts",
).add_source("Prism of Focus", 54)
rote_helper(
    "Magickal Metallurgy: Umbrite",
    {"matter": 4, "spirit": 3},
    "Craftwork",
    "Strength",
    "Crafts",
).add_source("Prism of Focus", 54)
rote_helper(
    "Unweave Fate", {"entropy": 5}, "Craftwork", "Dexterity", "Crafts"
).add_source("Prism of Focus", 54)
rote_helper(
    "Flawless Creation", {"entropy": 3}, "Craftwork", "Dexterity", "Art"
).add_source("Prism of Focus", 55)
rote_helper(
    "Inversion Festival",
    {"spirit": 5, "correspondence": 5},
    "Crazy Wisdom",
    "Charisma",
    "Intuition",
).add_source("Prism of Focus", 57)
rote_helper(
    "Refuse Thy Name",
    {"correspondence": 3},
    "Crazy Wisdom",
    "Intelligence",
    "Intuition",
).add_source("Prism of Focus", 57)
rote_helper(
    "Irrational Numerology",
    {"correspondence": 3},
    "Crazy Wisdom",
    "Intelligence",
    "Enigmas",
).add_source("Prism of Focus", 57)
rote_helper(
    "Inside Out", {"mind": 4}, "Crazy Wisdom", "Perception", "Meditation"
).add_source("Prism of Focus", 57)
rote_helper(
    "Synesthetic OVerload", {"mind": 3, "forces": 2}, "Crazy Wisdom", "Wits", "Art"
).add_source("Prism of Focus", 58)
rote_helper(
    "Memory Dump", {"mind": 3, "forces": 2}, "Cybernetics", "Perception", "Computer"
).add_source("Prism of Focus", 60)
rote_helper(
    "Pulley Redirect", {"forces": 2}, "Cybernetics", "Strength", "Science"
).add_source("Prism of Focus", 60)
rote_helper(
    "Upgrade", {"matter": 3, "life": 3}, "Cybernetics", "Intelligence", "Technology"
).add_source("Prism of Focus", 60)
rote_helper(
    "Nothing To See Here", {"mind": 2}, "Dominion", "Appearance", "Intimidation"
).add_source("Prism of Focus", 63)
rote_helper(
    "Nothing To See Here (Crowd)",
    {"mind": 2, "correspondence": 3},
    "Dominion",
    "Appearance",
    "Intimidation",
).add_source("Prism of Focus", 63)
rote_helper(
    "My Will Be Done", {"mind": 4}, "Dominion", "Charisma", "Belief Systems"
).add_source("Prism of Focus", 63)
rote_helper(
    "Mind over Matter",
    {"forces": 2, "mind": 3},
    "Dominion",
    "Dexterity",
    "Intimidation",
).add_source("Prism of Focus", 64)
rote_helper("Alpha Dog", {"mind": 1}, "Dominion", "Charisma", "Leadership").add_source(
    "Prism of Focus", 64
)
rote_helper(
    "Fiery Speech",
    {"correspondence": 3, "mind": 3},
    "Elementalism",
    "Charisma",
    "Empathy",
).add_source("Prism of Focus", 66)
rote_helper(
    "Roaring Wind", {"forces": 3, "prime": 2}, "Elementalism", "Stamina", "Survival"
).add_source("Prism of Focus", 66)
rote_helper(
    "Hemoplastics", {"matter": 3, "life": 2}, "Elementalism", "Stamina", "Crafts"
).add_source("Prism of Focus", 67)
rote_helper(
    "Deity's Wrath", {"entropy": 4}, "Faith", "Charisma", "Theology"
).add_source("Prism of Focus", 69)
rote_helper(
    "Healing Prayer", {"life": 3}, "Faith", "Stamina", "Belief Systems"
).add_source("Prism of Focus", 69)
rote_helper(
    "Gift of Prophecy", {"time": 2, "mind": 2}, "Faith", "Perception", "Enigmas"
).add_source("Prism of Focus", 70)
rote_helper(
    "Divine Transformation",
    {"forces": 3, "life": 4, "prime": 4, "spirit": 2, "mind": 1},
    "God-Bonding",
    "Stamina",
    "Cosmology",
).add_source("Prism of Focus", 72)
rote_helper(
    "Divine Guidance", {"time": 2}, "God-Bonding", "Perception", "Lucid Dreaming"
).add_source("Prism of Focus", 72)
rote_helper(
    "My Own Olympus", {"correspondence": 3}, "God-Bonding", "Perception", "Cosmology"
).add_source("Prism of Focus", 73)
rote_helper(
    "My Own Olympus (Umbral)",
    {"correspondence": 3, "spirit": 3},
    "God-Bonding",
    "Perception",
    "Cosmology",
).add_source("Prism of Focus", 73)
rote_helper(
    "Know the Back Streets",
    {"correspondence": 2},
    "Gutter Magick",
    "Wits",
    "Area Knowledge",
).add_source("Prism of Focus", 75)
rote_helper(
    "Savenging (Matter)",
    {"correspondence": 1, "matter": 1},
    "Gutter Magick",
    "Perception",
    "Streetwise",
).add_source("Prism of Focus", 75)
rote_helper(
    "Savenging (Forces)",
    {"correspondence": 1, "forces": 1},
    "Gutter Magick",
    "Perception",
    "Streetwise",
).add_source("Prism of Focus", 75)
rote_helper(
    "Savenging (Life)",
    {"correspondence": 1, "life": 1},
    "Gutter Magick",
    "Perception",
    "Streetwise",
).add_source("Prism of Focus", 75)
rote_helper(
    "Gang Sign", {"mind": 2}, "Gutter Magick", "Charisma", "Streetwise"
).add_source("Prism of Focus", 75)
rote_helper(
    "Power Outage", {"forces": 2}, "Gutter Magick", "Dexterity", "Technology"
).add_source("Prism of Focus", 75)
rote_helper(
    "Illusio Creo (Audiovisual)",
    {"forces": 3, "prime": 2},
    "High Ritual Magick",
    "Manipulation",
    "Enigmas",
).add_source("Prism of Focus", 78)
rote_helper(
    "Illusio Creo (Immersive)",
    {"forces": 4, "prime": 2},
    "High Ritual Magick",
    "Manipulation",
    "Enigmas",
).add_source("Prism of Focus", 78)
rote_helper(
    "Dämon Beschwören", {"spirit": 4}, "High Ritual Magick", "Intelligence", "Esoterica"
).add_source("Prism of Focus", 78)
rote_helper(
    "Barred Doors (Living Beings)",
    {"correspondence": 4, "prime": 2, "life": 3},
    "High Ritual Magick",
    "Wits",
    "Occult",
).add_source("Prism of Focus", 78)
rote_helper(
    "Barred Doors (Spirits)",
    {"correspondence": 4, "prime": 2, "spirit": 4},
    "High Ritual Magick",
    "Wits",
    "Occult",
).add_source("Prism of Focus", 78)
rote_helper(
    "Barred Doors (Specific Beings)",
    {"correspondence": 4, "prime": 2, "mind": 4},
    "High Ritual Magick",
    "Wits",
    "Occult",
).add_source("Prism of Focus", 78)
rote_helper(
    "Force Field Generator",
    {"forces": 2, "prime": 2},
    "Hypertech",
    "Wits",
    "Technology",
).add_source("Prism of Focus", 82)
rote_helper(
    "Nanoassembly",
    {"correspondence": 4, "matter": 4, "prime": 2},
    "Hypertech",
    "Intelligence",
    "Crafts",
).add_source("Prism of Focus", 82)
rote_helper(
    "Fortune Favors the Bold", {"entropy": 3}, "Investment", "Charisma", "Leadership"
).add_source("Prism of Focus", 86)
rote_helper(
    "Material Improvement", {"matter": 3}, "Investment", "Intelligence", "Law"
).add_source("Prism of Focus", 86)
rote_helper(
    "Asset Flip",
    {"correspondence": 3, "matter": 1, "prime": 1, "entropy": 1},
    "Investment",
    "Perception",
    "Research",
).add_source("Prism of Focus", 86)
rote_helper(
    "Self-Sustenance", {"life": 2, "prime": 2}, "Invigoration", "Stamina", "Meditation"
).add_source("Prism of Focus", 88)
rote_helper(
    "Energizing Touch", {"prime": 3}, "Invigoration", "Strength", "Athletics"
).add_source("Prism of Focus", 89)
rote_helper(
    "Cool and Collected", {"mind": 1}, "Invigoration", "Wits", "Meditation"
).add_source("Prism of Focus", 89)
rote_helper(
    "Pain Suppression", {"life": 2}, "Invigoration", "Stamina", "Brawl"
).add_source("Prism of Focus", 89)
rote_helper(
    "Harvest Blight",
    {"life": 2, "correspondence": 3},
    "Maleficia",
    "Intelligence",
    "Occult",
).add_source("Prism of Focus", 91)
rote_helper(
    "Mental Eclipse", {"mind": 3}, "Maleficia", "Manipulation", "Enigmas"
).add_source("Prism of Focus", 91)
rote_helper(
    "Mark of the Outcast",
    {"prime": 4, "mind": 2, "life": 2},
    "Maleficia",
    "Stamina",
    "Torture",
).add_source("Prism of Focus", 91)
rote_helper(
    "Bullet Catch",
    {"forces": 2, "life": 2, "time": 3},
    "Martial Arts",
    "Dexterity",
    "Athletics",
).add_source("Prism of Focus", 94)
rote_helper(
    "Double Jump", {"forces": 3}, "Martial Arts", "Strength", "Athletics"
).add_source("Prism of Focus", 94)
rote_helper(
    "Monkey Mischief", {"forces": 2}, "Martial Arts", "Manipulation", "Intimidation"
).add_source("Prism of Focus", 94)
rote_helper(
    "Poison Purge", {"life": 2}, "Martial Arts", "Stamina", "Esoterica"
).add_source("Prism of Focus", 94)
rote_helper(
    "Soundtrack of Reality", {"entropy": 2}, "Media Control", "Charisma", "Expression"
).add_source("Prism of Focus", 96)
rote_helper(
    "Viral Spread", {"correspondence": 3}, "Media Control", "Manipulation", "Art"
).add_source("Prism of Focus", 97)
rote_helper(
    "Anonymous Source",
    {"correspondence": 3, "mind": 4},
    "Media Control",
    "Manipulation",
    "Subterfuge",
).add_source("Prism of Focus", 97)
rote_helper(
    "Deepfake (illusion)", {"forces": 2}, "Media Control", "Manipulation", "Subterfuge"
).add_source("Prism of Focus", 97)
rote_helper(
    "Deepfake (transformation)",
    {"life": 2},
    "Media Control",
    "Manipulation",
    "Subterfuge",
).add_source("Prism of Focus", 97)
rote_helper(
    "Anesthesia", {"life": 2}, "Medicine-Work", "Stamina", "Medicine"
).add_source("Prism of Focus", 99)
rote_helper(
    "Cleanup", {"matter": 3, "entropy": 3}, "Medicine-Work", "Intelligence", "Science"
).add_source("Prism of Focus", 99)
rote_helper(
    "Cleansing Rite", {"prime": 5}, "Medicine-Work", "Charisma", "Meditation"
).add_source("Prism of Focus", 100)
rote_helper(
    "Mind/Body Sync", {"mind": 3, "life": 2}, "Medicine-Work", "Stamina", "Medicine"
).add_source("Prism of Focus", 100)
rote_helper(
    "Knowledge from on High",
    {"mind": 4, "spirit": 2},
    "Mediumship",
    "Charisma",
    "Research",
).add_source("Prism of Focus", 102)
rote_helper(
    "Spirit Guide", {"spirit": 2}, "Mediumship", "Charisma", "Cosmology"
).add_source("Prism of Focus", 102)
rote_helper(
    "Ghost Hunter's Eye",
    {"entropy": 1, "spirit": 1},
    "Mediumship",
    "Perception",
    "Awareness",
).add_source("Prism of Focus", 102)
rote_helper(
    "Long Strange Trip (Middle Umbra)",
    {"spirit": 3},
    "Mediumship",
    "Stamina",
    "Cosmology",
).add_source("Prism of Focus", 102)
rote_helper(
    "Long Strange Trip (High Umbra)",
    {"spirit": 3, "mind": 4, "prime": 2},
    "Mediumship",
    "Stamina",
    "Cosmology",
).add_source("Prism of Focus", 102)
rote_helper(
    "Long Strange Trip (Low Umbra)",
    {"spirit": 3, "entropy": 4, "life": 2},
    "Mediumship",
    "Stamina",
    "Cosmology",
).add_source("Prism of Focus", 102)
rote_helper(
    "Materialize Thought",
    {"mind": 3, "matter": 3, "prime": 2},
    "Psionics",
    "Intelligence",
    "Lucid Dreaming",
).add_source("Prism of Focus", 104)
rote_helper(
    "Mental Push", {"forces": 2}, "Psionics", "Intelligence", "Intimidation"
).add_source("Prism of Focus", 104)
rote_helper(
    "Reading the Leaves", {"time": 2}, "Psionics", "Perception", "Enigmas"
).add_source("Prism of Focus", 104)
rote_helper(
    "Bit Flip",
    {"forces": 2, "entropy": 2},
    "Reality Hacking",
    "Manipulation",
    "Computer",
).add_source("Prism of Focus", 107)
rote_helper(
    "MacGuyver", {"matter": 4}, "Reality Hacking", "Wits", "Jury-Rigging"
).add_source("Prism of Focus", 107)
rote_helper(
    "Percussive Maintenance (Physical)",
    {"matter": 3, "entropy": 3},
    "Reality Hacking",
    "Strength",
    "Technology",
).add_source("Prism of Focus", 107)
rote_helper(
    "Percussive Maintenance (Spiritual)",
    {"matter": 3, "spirit": 2},
    "Reality Hacking",
    "Strength",
    "Technology",
).add_source("Prism of Focus", 107)
rote_helper(
    "I'm In", {"correspondence": 2, "forces": 2}, "Reality Hacking", "Wits", "Computer"
).add_source("Prism of Focus", 107)
rote_helper(
    "Vision Quest",
    {"spirit": 3, "entropy": 2, "mind": 2},
    "Shamanism",
    "Perception",
    "Cosmology",
).add_source("Prism of Focus", 110)
rote_helper(
    "Rite of the Sun and Moon", {"entropy": 4}, "Shamanism", "Wits", "Enigmas"
).add_source("Prism of Focus", 111)
rote_helper(
    "Ancestral Guidance",
    {"spirit": 2, "time": 2},
    "Shamanism",
    "Intelligence",
    "Esoterica",
).add_source("Prism of Focus", 111)
rote_helper(
    "Lave Tet",
    {"prime": 2, "spirit": 2, "entropy": 2},
    "Voudoun",
    "Dexterity",
    "Intimidation",
).add_source("Prism of Focus", 113)
rote_helper(
    "Koulè Yo (mind)", {"mind": 1}, "Voudoun", "Perception", "Awareness"
).add_source("Prism of Focus", 114)
rote_helper(
    "Koulè Yo (spirit)", {"spirit": 1}, "Voudoun", "Perception", "Awareness"
).add_source("Prism of Focus", 114)
rote_helper(
    "Simbi's Flow", {"spirit": 2, "matter": 2}, "Voudoun", "Charisma", "Belief Systems"
).add_source("Prism of Focus", 114)
rote_helper(
    "Surviving Oggun's Forge", {"forces": 2}, "Voudoun", "Stamina", "Crafts"
).add_source("Prism of Focus", 114)
rote_helper(
    "Entanglement Engine",
    {"correspondence": 3},
    "Weird Science",
    "Intelligence",
    "Technology",
).add_source("Prism of Focus", 116)
rote_helper(
    "Share a Cold", {"life": 3}, "Witchcraft", "Charisma", "Medicine"
).add_source("Prism of Focus", 119)
rote_helper(
    "Familiar Soul", {"spirit": 4}, "Witchcraft", "Intelligence", "Occult"
).add_source("Prism of Focus", 119)
rote_helper(
    "Break Curse", {"entropy": 1}, "Witchcraft", "Wits", "Awareness"
).add_source("Prism of Focus", 120)
rote_helper(
    "Dig a Well", {"prime": 5}, "Witchcraft", "Strength", "Awareness"
).add_source("Prism of Focus", 120)
rote_helper(
    "Nadi Shodhana (Decreased Difficulty)", {"life": 2}, "Yoga", "Stamina", "Athletics"
).add_source("Prism of Focus", 122)
rote_helper(
    "Nadi Shodhana (Increased Attributes)", {"life": 3}, "Yoga", "Stamina", "Athletics"
).add_source("Prism of Focus", 122)
rote_helper("Yoga Nidra", {"mind": 4}, "Yoga", "Perception", "Meditation").add_source(
    "Prism of Focus", 122
)
rote_helper(
    "Agni Prana", {"forces": 3, "prime": 2}, "Yoga", "Stamina", "Survival"
).add_source("Prism of Focus", 123)

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

# Get common attributes
from populate_db.attributes import (
    dexterity,
    intelligence,
    manipulation,
    perception,
    stamina,
    wits,
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
rote.description = (
    "The mage uses chi manipulation to heal wounds by redirecting life energy."
)
rote.add_source("Lore of the Traditions", 28)

rote = Rote.objects.get_or_create(
    name="Seven League Stride",
    effect=effect_increase_speed,
    practice=martialarts,
    attribute=dexterity,
    ability=athletics,
)[0]
rote.description = (
    "Akashic technique to move at superhuman speeds through time manipulation."
)
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
    "The mage calls down holy fire to smite the unworthy. "
    "A dramatic display of divine wrath."
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
rote.description = (
    "The shaman steps sideways into the spirit world to commune with spirits."
)
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

effect_sense_fate_and_fortune = Effect.objects.get_or_create(
    name="Sense Fate and Fortune", entropy=1
)[0]
rote = Rote.objects.get_or_create(
    name="Read the Tapestry",
    effect=effect_sense_fate_and_fortune,
    practice=yoga,
    attribute=perception,
    ability=awareness,
)[0]
rote.description = (
    "The Euthanatos reads the patterns of karma and destiny surrounding a person."
)
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
rote.description = (
    "The Etherite fires a beam of etheric energy from a mad science device."
)
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
rote.description = (
    "Powerful ritual calling forth the Wild Hunt and its spectral hunters."
)
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
rote.description = (
    "The Adept hacks reality's source code to manipulate fundamental parameters."
)
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
