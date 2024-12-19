from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.focus import Practice
from characters.models.mage.rote import Rote


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
