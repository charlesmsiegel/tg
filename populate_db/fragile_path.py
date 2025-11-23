"""
Populate database with game objects from "Testaments of the First Cabal" / "The Fragile Path"
This sourcebook details the First Cabal of the Nine Mystick Traditions and the Great Betrayal of 1470.
"""

from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sphere import Sphere
from core.models import Book
from items.models.mage.artifact import Artifact
from items.models.mage.talisman import Talisman
from items.models.mage.wonder import Wonder
from locations.models.core.location import LocationModel
from locations.models.mage.chantry import Chantry
from locations.models.mage.realm import Realm

# =============================================================================
# BOOK
# =============================================================================

fragile_path_book, _ = Book.objects.get_or_create(
    name="The Fragile Path: Testaments of the First Cabal",
    defaults={
        "edition": "Rev",
        "gameline": "mta",
        "url": "https://www.storytellersvault.com/product/706/Mage-The-Ascension-The-Fragile-Path-Testaments-of-the-First-Cabal",
    }
)

# =============================================================================
# ORGANIZATIONS / FACTIONS
# =============================================================================

# Get the base Traditions faction (should already exist)
traditions, _ = MageFaction.objects.get_or_create(
    name="Traditions",
    defaults={"parent": None}
)

# Solificati (defunct Tradition)
solificati, _ = MageFaction.objects.get_or_create(
    name="Solificati",
    defaults={
        "parent": traditions,
        "founded": 1466,
        "description": "Alchemical Tradition focused on perfection and transmutation. Dissolved after the Great Betrayal of Heylel Teomim Thoabath in 1470."
    }
)

# Get other Traditions (should already exist, but create if needed)
verbena, _ = MageFaction.objects.get_or_create(
    name="Verbena",
    defaults={"parent": traditions}
)

celestial_chorus, _ = MageFaction.objects.get_or_create(
    name="Celestial Chorus",
    defaults={"parent": traditions}
)

order_of_hermes, _ = MageFaction.objects.get_or_create(
    name="Order of Hermes",
    defaults={"parent": traditions}
)

euthanatos, _ = MageFaction.objects.get_or_create(
    name="Euthanatos",
    defaults={"parent": traditions}
)

cult_of_ecstasy, _ = MageFaction.objects.get_or_create(
    name="Cult of Ecstasy",
    defaults={"parent": traditions}
)

akashic_brotherhood, _ = MageFaction.objects.get_or_create(
    name="Akashic Brotherhood",
    defaults={"parent": traditions}
)

dreamspeakers, _ = MageFaction.objects.get_or_create(
    name="Dreamspeakers",
    defaults={"parent": traditions}
)

ahl_i_batin, _ = MageFaction.objects.get_or_create(
    name="Ahl-i-Batin",
    defaults={"parent": traditions}
)

# Hermetic Houses
house_flambeau, _ = MageFaction.objects.get_or_create(
    name="House Flambeau",
    defaults={"parent": order_of_hermes}
)

house_quaesitor, _ = MageFaction.objects.get_or_create(
    name="House Quaesitor",
    defaults={"parent": order_of_hermes}
)

house_tytalus, _ = MageFaction.objects.get_or_create(
    name="House Tytalus",
    defaults={"parent": order_of_hermes}
)

# Order of Reason factions
order_of_reason, _ = MageFaction.objects.get_or_create(
    name="Order of Reason",
    defaults={
        "parent": None,
        "description": "Precursor to the Technocratic Union, founded around 1325."
    }
)

cabal_of_pure_thought, _ = MageFaction.objects.get_or_create(
    name="Cabal of Pure Thought",
    defaults={
        "parent": order_of_reason,
        "description": "Witch-hunting forerunner to the New World Order. Led the capture and torture of the First Cabal in 1470."
    }
)

# =============================================================================
# LOCATIONS
# =============================================================================

# Horizon Chantry/Realm
horizon, _ = Realm.objects.get_or_create(
    name="Horizon",
    defaults={
        "description": "The great meeting place and Chantry of the Council of Nine, carved from Primal Force and fed by nine sacred Nodes. Created for the Grand Convocation of 1457-1466. Contains a Grand Hall with nine cloisters and a central Common Hall. Outside the Hall are vast fields providing food and sanctuary for mythic beasts.",
        "created": 1457,
        "gauntlet": 2,
        "rank": 5,
    }
)

# Chantry Doissetep
doissetep, _ = Chantry.objects.get_or_create(
    name="Chantry Doissetep",
    defaults={
        "description": "Ancient Hermetic covenant moved to the Shard Realm of Forces during the crumbling Mythic Age. Home of Porthos Fitz-Empress and center of Hermetic power. Known for political intrigue and rigorous training.",
        "faction": order_of_hermes,
        "chantry_type": "ancestral",
        "rank": 5,
        "node": 5,
        "library": 5,
    }
)

# Other notable locations mentioned
kirkenes, _ = LocationModel.objects.get_or_create(
    name="Kirkenes, Norway",
    defaults={
        "type": "location",
        "description": "Remote Norwegian village in the frozen north where the First Cabal encountered Tormod, an old Craft mage hermit.",
    }
)

narbonne, _ = LocationModel.objects.get_or_create(
    name="Narbonne, France",
    defaults={
        "type": "location",
        "description": "Site of the Great Betrayal in 1470, where Heylel Teomim led the Cabal of Pure Thought against the First Cabal.",
    }
)

garoche, _ = LocationModel.objects.get_or_create(
    name="Garoche, France",
    defaults={
        "type": "location",
        "description": "French town burned to its foundations by the First Cabal while liberating accused witches.",
    }
)

# =============================================================================
# THE FIRST CABAL - THE NINE
# =============================================================================

# 1. Heylel Teomim Thoabath - The Great Betrayer (Solificati)
heylel, _ = Mage.objects.get_or_create(
    name="Heylel Teomim Thoabath",
    defaults={
        "concept": "Hermaphroditic Alchemical Adept",
        "essence": "Pattern",
        "nature": "Visionary",
        "demeanor": "Gallant",
        "affiliation": traditions,
        "faction": solificati,
        "arete": 4,
        "willpower": 9,
        "age": 35,  # Approximate at time of Betrayal
        "description": """Leader of the First Cabal, hermaphroditic creation of alchemical union between Julius de Medici and Mia de Napoli. Creator of the Philosopher's Stone. Beautiful, eloquent, and commanding, but ultimately consumed by hubris. Executed by Gilgul and scattering in 1470 for betraying the Cabal to the Order of Reason. Name translates to 'The Twin Lights of the Morning Star'. Father/mother of twins with Eloine.""",
        "status": "Dec",  # Deceased
        "public": False,
    }
)
# Set spheres for Heylel - as a Solificati master alchemist
heylel.matter = 4
heylel.prime = 4
heylel.life = 3
heylel.forces = 2
heylel.correspondence = 2
heylel.save()

# 2. Eloine "Chosen and Beloved" (Verbena)
eloine, _ = Mage.objects.get_or_create(
    name="Eloine",
    defaults={
        "concept": "Earth Witch and Healer",
        "essence": "Questing",
        "nature": "Caregiver",
        "demeanor": "Celebrant",
        "affiliation": traditions,
        "faction": verbena,
        "arete": 3,
        "willpower": 7,
        "age": 19,  # Young when she joined
        "description": """Verbena Chosen, daughter of Wyck blood, from Ireland. Sensual, innocent, and passionate. Lover of Heylel and mother of his twins. Her spirit was broken by the Betrayal and loss of her children. Forsook her Art after the trial and became a vagabond, aiding refugees from witch hunts. Captured and burned in later years, her faith renewed near death. Named 'Protector' and 'Beloved'. Had thick red hair, green eyes, and went barefoot in all but harsh weather.""",
        "status": "Dec",
        "public": False,
    }
)
eloine.life = 4
eloine.spirit = 3
eloine.prime = 2
eloine.forces = 2
eloine.save()

# 3. Sister Bernadette de la Champagne (Celestial Chorus)
bernadette, _ = Mage.objects.get_or_create(
    name="Sister Bernadette de la Champagne",
    defaults={
        "concept": "Divine Healer and Singer",
        "essence": "Primordial",
        "nature": "Martyr",
        "demeanor": "Penitent",
        "affiliation": traditions,
        "faction": celestial_chorus,
        "arete": 3,
        "willpower": 8,
        "age": 45,  # At time of Cabal formation
        "description": """Born 1421 in Domremy, neighbor to Joan of Arc. Former Dominican Inquisitor who Awakened during plague fever with angelic visions. Communicated solely through song after joining the Chorus. Could manifest multiple projections of herself, each with its own voice. Secretly in love with Heylel. Pure, innocent, yet carried guilt from her Inquisition past. Lived for over 300 years, dying in 1723. Small, waifish figure with raven-black hair and bright blue eyes.""",
        "status": "Dec",
        "public": False,
    }
)
bernadette.life = 3
bernadette.mind = 2
bernadette.prime = 3
bernadette.spirit = 2
bernadette.save()

# 4. Master Louis DuMonte (Order of Hermes, House Quaesitor)
louis_dumont, _ = Mage.objects.get_or_create(
    name="Master Louis DuMonte",
    defaults={
        "concept": "Hermetic Judge and Force Master",
        "essence": "Dynamic",
        "nature": "Judge",
        "demeanor": "Pedagogue",
        "affiliation": traditions,
        "faction": order_of_hermes,
        "subfaction": house_quaesitor,
        "arete": 4,
        "willpower": 9,
        "age": 44,  # Mid-forties
        "description": """Hermetic Magus of House Quaesitor (House of Judges). Aloof, scholarly, and practical. Lost parents to Order of Reason attack in youth. Served as arbiter of disputes within the Cabal. Mastered Forces to devastating effect. Died consumed by Paradox backlash while calling upon tremendous magick to defend the Cabal at Narbonne. Wore plain brown robes, stocky build (5'3"), graying beard. Carried silver amulet, ring with balanced scales, and abacus.""",
        "status": "Dec",
        "public": False,
    }
)
louis_dumont.forces = 5
louis_dumont.matter = 3
louis_dumont.prime = 3
louis_dumont.mind = 2
louis_dumont.save()

# 5. Cygnus Moro (Euthanatos)
cygnus_moro, _ = Mage.objects.get_or_create(
    name="Cygnus Moro",
    defaults={
        "concept": "Balance Bringer and Kali Devotee",
        "essence": "Dynamic",
        "nature": "Judge",
        "demeanor": "Martyr",
        "affiliation": traditions,
        "faction": euthanatos,
        "arete": 4,
        "willpower": 8,
        "age": 71,  # Lived 1399-1470
        "description": """Half-Greek, half-Libyan born 1399. Raised Muslim but fell in with forbidden Kali-serving sect. Awakened through vision of copulating with the Black Mother. Delivered 'Good Death' to deserving targets after careful research. Generous and kind despite his role. Skilled warrior (scimitar, tachi, bow, spears). Claimed to have killed 100+ Crusaders. Tortured to death in Cabal of Pure Thought dungeons, died aged within days. Tall, powerfully built, curly black hair, dark skin, black eyes.""",
        "status": "Dec",
        "public": False,
    }
)
cygnus_moro.entropy = 4
cygnus_moro.life = 3
cygnus_moro.mind = 3
cygnus_moro.spirit = 2
cygnus_moro.save()

# 6. Akrites Salonikas (Cult of Ecstasy / Seers of Chronos)
akrites, _ = Mage.objects.get_or_create(
    name="Akrites Salonikas",
    defaults={
        "concept": "Time-Traveling Prophet and Rebel",
        "essence": "Questing",
        "nature": "Visionary",
        "demeanor": "Rogue",
        "affiliation": traditions,
        "faction": cult_of_ecstasy,
        "arete": 4,
        "willpower": 7,
        "age": 29,  # Young
        "description": """Persian Seer with precognitive abilities. Saw the future Technocratic apocalypse during Awakening. Knew of Heylel's betrayal before it happened but allowed it to occur to prevent worse futures. Escaped the Battle of Narbonne, later rescued survivors. Self-exiled to Arctic afterward, haunted by guilt. Illegitimate son of soldier and slave. Rebellious, passionate storyteller. Used hashish (manifested as Paradox flaw). Nearly golden skin, classic features, short beard, long ponytail. Wore elaborate robes, jeweled earrings, tattooed fingers.""",
        "status": "Ret",  # Retired to Arctic
        "public": False,
    }
)
akrites.time = 5
akrites.mind = 3
akrites.spirit = 3
akrites.correspondence = 2
akrites.save()

# 7. Fall Breeze (Jiu Ling) (Akashic Brotherhood)
fall_breeze, _ = Mage.objects.get_or_create(
    name="Fall Breeze",
    defaults={
        "concept": "Akashic Warrior Linguist",
        "essence": "Dynamic",
        "nature": "Competitor",
        "demeanor": "Bravo",
        "affiliation": traditions,
        "faction": akashic_brotherhood,
        "arete": 3,
        "willpower": 8,
        "age": 17,  # Very young at Convocation
        "description": """Born Jiu Ling near Pacific coast. Fluent in 12+ languages including English, French, Mandarin, Japanese, Arabic, Greek, Latin, Gaelic, African and Iroquois dialects, Cantonese. Mastered Do maneuvers and empathy/telepathy. Quick-tempered, talkative, prone to addiction (hallucinogens, stimulants). Short (5'2"), lithe, sharp features, restless dark eyes. Shaved head when ashamed, grew hair long when proud. Wore loose robes. Died at 30 fighting valiantly at Narbonne, killed dozens before falling.""",
        "status": "Dec",
        "public": False,
    }
)
fall_breeze.life = 3
fall_breeze.mind = 4
fall_breeze.forces = 2
fall_breeze.entropy = 2
fall_breeze.save()

# 8. Walking Hawk (Djiionondo-wanenake / Seneca Turtle Clan)
walking_hawk, _ = Mage.objects.get_or_create(
    name="Walking Hawk",
    defaults={
        "concept": "Dreamspeaker Medicine Man",
        "essence": "Primordial",
        "nature": "Visionary",
        "demeanor": "Judge",
        "affiliation": traditions,
        "faction": dreamspeakers,
        "arete": 4,
        "willpower": 9,
        "age": 55,  # Older warrior turned healer
        "description": """Seneca medicine man of Turtle clan ('People of the Hill'). Former war chief who laid down tomahawk after wolf spirit vision following mortal wounding. Became healer and visionary. Sailed to Europe in double-hulled canoe following vision. Man of few words, plain speech. Distrusted Heylel. Returned to warn his people after Betrayal; his Oration may have inspired Iroquois Confederacy. Wore topknot (often red), plucked hair, loincloth or buckskin, decorated with shells, quills, copper armbands, bear-claw necklace. Carried medicine pouches.""",
        "status": "Dec",
        "public": False,
    }
)
walking_hawk.spirit = 5
walking_hawk.life = 4
walking_hawk.prime = 2
walking_hawk.mind = 2
walking_hawk.save()

# 9. Daud-Allah Abu-Hisham, Ibn-Muqla al-Baghdadi (Ahl-i-Batin)
daud_allah, _ = Mage.objects.get_or_create(
    name="Daud-Allah Abu-Hisham",
    defaults={
        "concept": "Ancient Batini Warrior-Scholar",
        "essence": "Questing",
        "nature": "Pedagogue",
        "demeanor": "Gallant",
        "affiliation": traditions,
        "faction": ahl_i_batin,
        "arete": 5,
        "willpower": 10,
        "age": 450,  # Ancient
        "description": """Name means 'Beloved of Allah'. Over 400 years old when joined Cabal. Fought alongside Saladin in Second Crusade, killed 100+ Crusaders. Master of weaponry (scimitar from Khan, tachi, bow, javelins, spears). Mastered Correspondence, Forces, Spirit. Scholar of many languages, alchemy, Kabbalah, Greek philosophy, Christian Scripture. Gentle, generous nature despite warrior past. Deep respect for Christ's teachings. Cut to shreds at Narbonne. Tall, powerful, wide dark eyes, black hair/goatee, smooth brown skin, wore traditional Persian turban and garb.""",
        "status": "Dec",
        "public": False,
    }
)
daud_allah.correspondence = 5
daud_allah.forces = 4
daud_allah.spirit = 4
daud_allah.mind = 3
daud_allah.prime = 3
daud_allah.save()

# =============================================================================
# OTHER IMPORTANT CHARACTERS
# =============================================================================

# Porthos Fitz-Empress (the compiler/narrator)
porthos, _ = Mage.objects.get_or_create(
    name="Porthos Fitz-Empress",
    defaults={
        "concept": "Ancient Hermetic Archivist",
        "essence": "Pattern",
        "nature": "Pedagogue",
        "demeanor": "Judge",
        "affiliation": traditions,
        "faction": order_of_hermes,
        "subfaction": house_flambeau,
        "arete": 7,
        "willpower": 10,
        "age": 550,  # Over 500 years old
        "description": """Hermes bani Flambeau, Drua'shi Master and Deacon Primus of Chantry Doissetep. Compiler of the Testaments. Born 28 years old when Awakened on his own, helped move Doissetep to Forces Realm. Attended Grand Convocation 1457-1466. Knew and loved Eloine from her youth. Survived over 500 years of wars, intrigue, persecution. Admits to 'more defeats than all nations combined.' Wise but tired, weary of internal Tradition politics. Desires Eloine still after centuries.""",
        "status": "App",
        "public": False,
    }
)
porthos.forces = 5
porthos.prime = 5
porthos.spirit = 4
porthos.matter = 4
porthos.correspondence = 4
porthos.time = 3
porthos.save()

# The Primi (Founders of the Traditions)
nightshade, _ = Mage.objects.get_or_create(
    name="Lady Nightshade",
    defaults={
        "concept": "Verbena Founder",
        "affiliation": traditions,
        "faction": verbena,
        "arete": 6,
        "description": "Founder of the Verbena Tradition. Met with Baldric and Valorian at Mistridge ruins (1439-1440). Named Eloine 'Protector' and 'Chosen One' at her birth.",
        "status": "App",
        "public": False,
    }
)

valorian, _ = Mage.objects.get_or_create(
    name="Master Valorian",
    defaults={
        "concept": "Celestial Chorus Founder",
        "affiliation": traditions,
        "faction": celestial_chorus,
        "arete": 6,
        "description": "Founder of the Celestial Chorus. Nursed Bernadette back to health at Horizon. Met with Nightshade and Baldric at Mistridge (1439-1440). Journeyed East with Sh'zar.",
        "status": "App",
        "public": False,
    }
)

baldric_lasalle, _ = Mage.objects.get_or_create(
    name="Master Baldric LaSalle",
    defaults={
        "concept": "Hermetic Founder",
        "affiliation": traditions,
        "faction": order_of_hermes,
        "subfaction": house_tytalus,
        "arete": 6,
        "description": "Hermes bani House Tytalus. Began quest for great Magi in 1439. Met with Nightshade and Valorian at Mistridge ruins. Brought news of impending Tribunal to Doissetep.",
        "status": "App",
        "public": False,
    }
)

star_of_eagles, _ = Mage.objects.get_or_create(
    name="Star-of-Eagles",
    defaults={
        "concept": "Dreamspeaker Co-Founder",
        "affiliation": traditions,
        "faction": dreamspeakers,
        "arete": 6,
        "description": "Co-founder and chief of Dreamspeakers with Naioba. Met Nightshade in North America. Married Naioba (1456), had three children. Gave Walking Hawk a knife of shiny stone as gift.",
        "status": "App",
        "public": False,
    }
)

naioba, _ = MtAHuman.objects.get_or_create(
    name="Naioba",
    defaults={
        "concept": "Dreamspeaker Co-Founder",
        "nature": "Caregiver",
        "description": "Co-founder of Dreamspeakers with Star-of-Eagles. Wise woman of Mo-Mo Keu dreamlands (Africa). Married Star-of-Eagles (1456), bore three children. Assassinated 1464 by Dreamspeaker barabbi, causing major rift in Tradition.",
        "status": "Dec",
        "public": False,
    }
)

# Minor NPCs
tormod_of_kirkenes, _ = MtAHuman.objects.get_or_create(
    name="Tormod of Kirkenes",
    defaults={
        "concept": "Norwegian Craft Hermit",
        "age": 200,  # Ancient, looked young despite age
        "description": "Old Norwegian Craft mage living as hermit in Kirkenes fjeld for decades. Demonstrated great powers before publicly swearing off 'devil's powers.' Wore only light sackcloth in freezing cold. Cherubic face, thin gray beard, frail frame. Accidentally killed by Time storm while caring for entranced Akrites.",
        "status": "Dec",
        "public": False,
    }
)

# Technocrat antagonists
general_wyndgarde, _ = MtAHuman.objects.get_or_create(
    name="Inquisitor General Wyndgarde",
    defaults={
        "concept": "English Inquisitor",
        "description": "English Inquisitor General defeated by Nightshade in Ireland - she froze his army in a sudden blizzard.",
        "status": "Dec",
        "public": False,
    }
)

# =============================================================================
# ARTIFACTS & WONDERS
# =============================================================================

# The Philosopher's Stone
philosophers_stone, _ = Artifact.objects.get_or_create(
    name="The Philosopher's Stone",
    defaults={
        "rank": 5,
        "quintessence": 20,
        "quintessence_max": 20,
        "description": """Legendary Wonder created by Heylel Teomim Thoabath. Said to alter matter and grant immortality. Exact creation circumstances unclear - possibly related to the alchemical fusion that created Heylel itself. Current location unknown after Heylel's execution.""",
        "background_cost": 7,
    }
)
# Create effect for Philosopher's Stone
stone_effect, _ = Effect.objects.get_or_create(
    name="Philosopher's Stone - Transmutation",
    defaults={
        "prime": 5,
        "matter": 5,
        "life": 3,
        "description": "Transmute matter, extend life, grant perfection",
    }
)
philosophers_stone.power = stone_effect
philosophers_stone.save()

# The Golden Pear of Bottger
golden_pear, _ = Artifact.objects.get_or_create(
    name="The Golden Pear of Bottger",
    defaults={
        "rank": 4,
        "description": "Rumored vessel containing secrets of the Philosopher's Stone. Exact nature and location unknown.",
        "background_cost": 6,
    }
)

# Daud-Allah's Scimitar
scimitar, _ = Wonder.objects.get_or_create(
    name="Daud-Allah's Scimitar",
    defaults={
        "rank": 3,
        "description": "Scimitar captured from a captain in Genghis Khan's army. Wielded by Daud-Allah throughout his centuries of battles.",
        "background_cost": 3,
    }
)

# Akrites' Tattooed Fingers
prophets_mark, _ = Talisman.objects.get_or_create(
    name="Mark of the Prophets",
    defaults={
        "rank": 2,
        "description": "Black circles tattooed across right hand fingers, channeling prophetic Time visions.",
        "background_cost": 2,
    }
)

faithful_mark, _ = Talisman.objects.get_or_create(
    name="Mark of the Faithful",
    defaults={
        "rank": 2,
        "description": "Flaming vessels tattooed on left hand, symbols of devotion.",
        "background_cost": 2,
    }
)

# Walking Hawk's Medicine Mask
dream_mask, _ = Talisman.objects.get_or_create(
    name="Dream-Reading Mask",
    defaults={
        "rank": 3,
        "description": "Seneca mask that transforms the wearer to embody visions seen in dreams, allowing prophetic interpretation.",
        "background_cost": 3,
    }
)

# Louis DuMonte's Tools
silver_amulet, _ = Talisman.objects.get_or_create(
    name="Hermetic Runed Amulet",
    defaults={
        "rank": 2,
        "description": "Silver amulet engraved with endless array of runes, focus for Hermetic ritual.",
        "background_cost": 2,
    }
)

scales_ring, _ = Talisman.objects.get_or_create(
    name="Ring of Balanced Scales",
    defaults={
        "rank": 2,
        "description": "Gold ring with perfectly balanced scales embossed on face, symbol of House Quaesitor justice.",
        "background_cost": 2,
    }
)

# =============================================================================
# EFFECTS / ROTES
# =============================================================================

# Bernadette's Healing
healing_song, _ = Effect.objects.get_or_create(
    name="Song of Celestial Healing",
    defaults={
        "life": 3,
        "mind": 2,
        "prime": 2,
        "description": "Bernadette's signature healing - sings to perceive the Perfect White form and molds dark sickness away like clay.",
    }
)

# Bernadette's Manifestation
choir_manifestation, _ = Effect.objects.get_or_create(
    name="Manifest the Celestial Choir",
    defaults={
        "mind": 3,
        "life": 2,
        "prime": 2,
        "description": "Create multiple physical projections of self, each with own voice, to sing complex polyphonic songs/debates.",
    }
)

# Louis' Catastrophic Forces
master_forces, _ = Effect.objects.get_or_create(
    name="Master's Wrath of Elements",
    defaults={
        "forces": 5,
        "prime": 3,
        "description": "Call down thunder, lightning, rain, howling winds. Shake the ground, fell forests. Devastating but Paradox-prone.",
    }
)

# Akrites' Time Vision
time_travel_vision, _ = Effect.objects.get_or_create(
    name="Journey Through Chronos",
    defaults={
        "time": 5,
        "mind": 2,
        "spirit": 2,
        "description": "Travel consciousness through time, witnessing past and future. Risk of crossing Technocratic Time Gauntlet and creating Time storms.",
    }
)

# Walking Hawk's Spirit Communion
spirit_language, _ = Effect.objects.get_or_create(
    name="Speak the Language of Spirits",
    defaults={
        "spirit": 4,
        "mind": 2,
        "description": "Understand and communicate with spirits of nature - birds, animals, trees, plants, rocks, water, wind.",
    }
)

# Cygnus' Good Death
good_death, _ = Effect.objects.get_or_create(
    name="Deliver the Good Death",
    defaults={
        "entropy": 4,
        "life": 2,
        "spirit": 1,
        "description": "Accelerate entropy to grant swift, painless death and ease passage to next incarnation.",
    }
)

# Heylel's Alchemical Transmutation
alchemical_perfection, _ = Effect.objects.get_or_create(
    name="Alchemical Perfection",
    defaults={
        "matter": 4,
        "prime": 4,
        "life": 3,
        "description": "Transmute and perfect matter and life, the signature Art of the Solificati. Used in Heylel's self-creation.",
    }
)

# Eloine's Earth Magick
earth_communion, _ = Effect.objects.get_or_create(
    name="Dance of Earth and Spirit",
    defaults={
        "life": 4,
        "spirit": 3,
        "prime": 2,
        "description": "Through dance and song-ecstasy, tap into pulse of Earth and draw upon Spirit World. Heal, curse, or commune with nature.",
    }
)

# Fall Breeze's Do Combat
do_mastery, _ = Effect.objects.get_or_create(
    name="Do Combat Mastery",
    defaults={
        "life": 3,
        "forces": 2,
        "mind": 2,
        "description": "Akashic martial arts enhanced by Life (body perfection), Forces (strikes), and Mind (anticipation). Devastating unarmed combat.",
    }
)

print("✓ Created Fragile Path book")
print(f"✓ Created {MageFaction.objects.filter(name__in=['Solificati', 'Cabal of Pure Thought']).count()} new factions")
print(f"✓ Created 9 First Cabal members (The Nine)")
print(f"✓ Created {Mage.objects.filter(name__in=['Porthos Fitz-Empress', 'Lady Nightshade', 'Master Valorian', 'Master Baldric LaSalle', 'Star-of-Eagles']).count()} additional mages")
print(f"✓ Created {MtAHuman.objects.filter(name__in=['Naioba', 'Tormod of Kirkenes', 'Inquisitor General Wyndgarde']).count()} human NPCs")
print(f"✓ Created {LocationModel.objects.filter(name__in=['Horizon', 'Chantry Doissetep', 'Kirkenes, Norway', 'Narbonne, France', 'Garoche, France']).count()} locations")
print(f"✓ Created {Wonder.objects.filter(name__in=['The Philosopher\\'s Stone', 'The Golden Pear of Bottger']).count()} major artifacts")
print(f"✓ Created {Talisman.objects.filter(name__contains='Mark').count()} talismans")
print(f"✓ Created {Effect.objects.filter(name__in=['Song of Celestial Healing', 'Journey Through Chronos']).count()} signature effects")
print("\nFragile Path database population complete!")
