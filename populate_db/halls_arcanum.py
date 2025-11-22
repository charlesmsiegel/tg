"""
Populate script for Halls of the Arcanum sourcebook

This script extracts all game-relevant objects from the Halls of the Arcanum
sourcebook (1996) for Mage: The Ascension, including:
- Named characters (both Awakened and mortal)
- Artifacts and Wonders
- Character templates
- Organizations
"""

from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.faction import MageFaction
from items.models.mage.wonder import Wonder
from core.models import Book

# =============================================================================
# BOOK
# =============================================================================

book, _ = Book.objects.get_or_create(
    name="Halls of the Arcanum",
    gameline="mta",
    defaults={
        "edition": "Rev",
        "url": "https://www.storytellersvault.com/product/108/Halls-of-the-Arcanum",
    }
)

# =============================================================================
# ORGANIZATIONS / FACTIONS
# =============================================================================

# The Arcanum itself (as a faction)
arcanum, _ = MageFaction.objects.get_or_create(
    name="The Arcanum",
    defaults={
        "description": "A mortal society dedicated to the pursuit and acquisition of arcane knowledge. "
        "Founded in 1885, its members seek enlightenment through the investigation of supernatural mysteries."
    }
)

# Hermetic Order of the Rising Day (HORD)
hord, _ = MageFaction.objects.get_or_create(
    name="Hermetic Order of the Rising Day",
    defaults={
        "description": "A Victorian-era occult fraternity that preceded the Arcanum. "
        "Known for its high standards of magical research but eventually became little more than theatrical ritual."
    }
)

# Les Frères de la Rose Croix
freres, _ = MageFaction.objects.get_or_create(
    name="Les Frères de la Rose Croix",
    defaults={
        "description": "The Brothers of the Rose Cross, founded in Morocco in 1893 by Etienne Dulac. "
        "A highly secretive group of visionary mystics who care less for scholarship than mystical experience."
    }
)

# Society of Leopold
leopold, _ = MageFaction.objects.get_or_create(
    name="Society of Leopold",
    defaults={
        "description": "The oldest organization dedicated to studying and eliminating the supernatural. "
        "Modern heir to the Inquisition, seeking the extermination of all supernaturals as creatures of the devil."
    }
)

# Order of St. Hermes (distinct from Order of Hermes)
st_hermes, _ = MageFaction.objects.get_or_create(
    name="Order of St. Hermes",
    defaults={
        "description": "Heterodox Christians who elevated Hermes Trismegistus to sainthood. "
        "Began within the Church in the Middle Ages, dedicated to keeping alchemical knowledge alive. "
        "Broke from the Church during the Reformation."
    }
)

# Crucible Genetics Amalgamated (CGA)
cga, _ = MageFaction.objects.get_or_create(
    name="Crucible Genetics Amalgamated",
    defaults={
        "description": "Biochemistry company descended from a religious zealot who turned to science. "
        "Hunts supernaturals for scientific experimentation including torture and vivisection. "
        "Founded by Reverend Jebediah Brown."
    }
)

# =============================================================================
# MAJOR CHARACTERS - FOUNDERS & HISTORICAL FIGURES
# =============================================================================

# Benjamen Holmscroft - Enigmatic founder
holmscroft, _ = MtAHuman.objects.get_or_create(
    name="Benjamen Holmscroft",
    defaults={
        "description": "Enigmatic founder and first Grand Chancellor of the Arcanum (1885-1914). "
        "Little is known about his origins before joining HORD in 1879. Allegedly died in 1914, but many suspect he lives on. "
        "Owned Vannever Hall which became the Foundation House. May be one of the Undying.",
        "nature": "Architect",
        "essence": "Questing",
        "strength": 2,
        "dexterity": 2,
        "stamina": 4,
        "charisma": 3,
        "manipulation": 4,
        "appearance": 3,
        "perception": 4,
        "intelligence": 5,
        "wits": 4,
        "alertness": 2,
        "awareness": 4,
        "expression": 4,
        "intuition": 2,
        "etiquette": 5,
        "firearms": 3,
        "leadership": 3,
        "meditation": 2,
        "melee": 2,
        "research": 4,
        "stealth": 2,
        "occult": 4,
        "enigmas": 2,
        "willpower": 8,
    }
)

# Winthrop Murray - Secretary and Egyptologist, became Undying
murray, _ = MtAHuman.objects.get_or_create(
    name="Winthrop Murray",
    defaults={
        "description": "Prominent Victorian Egyptologist and first Secretary of the Arcanum. "
        "Served as Holmscroft's personal secretary. After meeting an Undying Egyptian sorcerer, "
        "he recreated the ritual of immortality. Staged his death and may work with the Red Monks.",
        "nature": "Traditionalist",
        "strength": 2,
        "dexterity": 2,
        "stamina": 4,
        "charisma": 3,
        "manipulation": 4,
        "appearance": 3,
        "perception": 4,
        "intelligence": 5,
        "wits": 4,
        "alertness": 2,
        "awareness": 4,
        "expression": 4,
        "intuition": 2,
        "etiquette": 5,
        "firearms": 3,
        "leadership": 3,
        "meditation": 2,
        "melee": 2,
        "research": 4,
        "stealth": 2,
        "academics": 4,
        "occult": 4,
        "enigmas": 2,
        "willpower": 8,
    }
)

# Jebediah Brown - Reverend and vampire hunter, later alchemist
brown, _ = MtAHuman.objects.get_or_create(
    name="Reverend Jebediah Brown",
    defaults={
        "description": "Anglican clergyman and founding member of the Arcanum who withdrew to pursue his own mission. "
        "Expert on vampire lore. Later learned alchemy and founded Crucible Genetics Amalgamated. "
        "'Died' in 1902 but continues to hunt and experiment on supernaturals. Uses alchemical longevity.",
        "nature": "Critic",
        "strength": 3,
        "dexterity": 2,
        "stamina": 3,
        "charisma": 5,
        "manipulation": 4,
        "appearance": 2,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        "alertness": 3,
        "awareness": 1,
        "brawl": 2,
        "expression": 4,
        "intuition": 3,
        "intimidation": 4,
        "subterfuge": 3,
        "etiquette": 3,
        "firearms": 4,
        "leadership": 3,
        "meditation": 2,
        "melee": 4,
        "research": 2,
        "technology": 3,
        "occult": 2,
        "theology": 3,
        "willpower": 8,
    }
)

# Etienne Dulac - French occultist who refused to join
dulac, _ = MtAHuman.objects.get_or_create(
    name="Etienne Dulac",
    defaults={
        "description": "French occultist who was invited to the founding of the Arcanum but withdrew "
        "after disagreeing with proposed tenets. Founded Les Frères de la Rose Croix in Morocco in 1893.",
        "nature": "Fanatic",
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 3,
        "appearance": 3,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        "occult": 4,
        "leadership": 3,
        "subterfuge": 3,
        "willpower": 7,
    }
)

# Liam McPhee - Irish poet and faerie expert
mcphee, _ = MtAHuman.objects.get_or_create(
    name="Liam McPhee",
    defaults={
        "description": "Irish poet and founding member of the Arcanum. First Chancellor of the Dublin Chapter House. "
        "Expert in faerie lore. Said to have fae blood - looks to be in his early 20s but is in his late 40s. "
        "Disappeared mysteriously, continuing the pattern of his enigmatic life.",
        "nature": "Visionary",
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 2,
        "appearance": 4,
        "perception": 3,
        "intelligence": 4,
        "wits": 4,
        "expression": 4,
        "intuition": 3,
        "occult": 3,
        "willpower": 6,
    }
)

# Jonathan Kelvin - American thanatologist
kelvin, _ = MtAHuman.objects.get_or_create(
    name="Jonathan Kelvin",
    defaults={
        "description": "American founding member from Boston, expert in thanatology and afterlife beliefs. "
        "First Chancellor of the Boston Chapter. Never recovered from the 1910 Boston Chapter House fire. "
        "Later moved to Washington D.C. to oversee American Chapters.",
        "nature": "Visionary",
        "strength": 2,
        "dexterity": 2,
        "stamina": 3,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 2,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        "awareness": 2,
        "research": 4,
        "occult": 3,
        "academics": 4,
        "willpower": 7,
    }
)

# Massimo Linarelli - Italian member
linarelli, _ = MtAHuman.objects.get_or_create(
    name="Massimo Linarelli",
    defaults={
        "description": "Italian founding member of the Arcanum from Rome. "
        "Maintained correspondence with various European scholars and clergy.",
        "nature": "Traditionalist",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 3,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        "academics": 3,
        "occult": 3,
        "willpower": 6,
    }
)

# Roger Corwin - Psychiatrist and lycanthropy expert
corwin, _ = MtAHuman.objects.get_or_create(
    name="Roger Corwin",
    defaults={
        "description": "Founding member from Salisbury, originally a psychiatrist (alienist) who studied lycanthropy. "
        "Initially believed it was purely psychiatric but later changed his views. "
        "Appointed Chancellor of the Vienna Chapter House.",
        "nature": "Judge",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 2,
        "perception": 4,
        "intelligence": 4,
        "wits": 3,
        "psychology": 4,
        "medicine": 3,
        "academics": 3,
        "occult": 2,
        "willpower": 6,
    }
)

# =============================================================================
# MODERN DAY CHARACTERS
# =============================================================================

# Madelaine Beaucourt - Current Grand Chancellor
beaucourt, _ = MtAHuman.objects.get_or_create(
    name="Madelaine Beaucourt",
    defaults={
        "description": "Current Grand Chancellor of the Arcanum, a noted Indologist educated in finest French universities. "
        "Forceful and professional, groomed by the White Monks. Serves their bidding loyally. French, late 40s.",
        "nature": "Visionary",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 4,
        "appearance": 2,
        "perception": 4,
        "intelligence": 3,
        "wits": 3,
        "alertness": 1,
        "awareness": 2,
        "expression": 4,
        "intuition": 3,
        "intimidation": 4,
        "subterfuge": 1,
        "etiquette": 2,
        "firearms": 3,
        "leadership": 4,
        "meditation": 1,
        "research": 3,
        "technology": 3,
        "computer": 1,
        "enigmas": 1,
        "occult": 3,
        "willpower": 7,
    }
)

# Jarmya Talbot - Preeminent linguist
talbot, _ = MtAHuman.objects.get_or_create(
    name="Jarmya Talbot",
    defaults={
        "description": "Elderly Indo-European linguist with mastery of dozens of languages. "
        "Joined the Arcanum fresh from his doctorate. Lives at the Foundation House. "
        "Seeks to reconstruct proto-Indo-European, believing it will reveal sacred mysteries.",
        "nature": "Judge",
        "strength": 1,
        "dexterity": 1,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 3,
        "appearance": 2,
        "perception": 4,
        "intelligence": 5,
        "wits": 3,
        "academics": 5,
        "research": 4,
        "occult": 3,
        "willpower": 7,
    }
)

# Lynne Stanhope - Managing editor
stanhope, _ = MtAHuman.objects.get_or_create(
    name="Lynne Stanhope",
    defaults={
        "description": "Managing editor of the Annual Proceedings of the Arcanum. "
        "Former tabloid journalist who came to the Arcanum investigating a possession case. "
        "Works closely with the Editorial Board.",
        "nature": "Perfectionist",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 3,
        "perception": 3,
        "intelligence": 3,
        "wits": 3,
        "expression": 3,
        "research": 3,
        "technology": 2,
        "academics": 2,
        "investigation": 3,
        "willpower": 6,
    }
)

# Helga Sørensen - Oslo Chancellor
sorensen, _ = MtAHuman.objects.get_or_create(
    name="Helga Sørensen",
    defaults={
        "description": "Chancellor of the Oslo Chapter House. Norwegian woman in her 70s who joined at age 61, "
        "one of the oldest Neophytes in Arcanum history. Self-educated expert on Norwegian, Finnish, and Swedish witchcraft. "
        "Warm and motherly, cherishes her background as wife and mother.",
        "nature": "Caregiver",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 2,
        "perception": 3,
        "intelligence": 3,
        "wits": 3,
        "empathy": 3,
        "occult": 4,
        "academics": 3,
        "willpower": 6,
    }
)

# Sandeep D'Souza - New Delhi Chancellor
dsouza, _ = MtAHuman.objects.get_or_create(
    name="Sandeep D'Souza",
    defaults={
        "description": "Chancellor of the New Delhi Chapter House and editor-in-chief of the Encyclopedia of the Arcane. "
        "Intellectual luminary with comprehensive learning in occult history, linguistics, religion. "
        "Born in New Delhi, educated at Harvard, Wisconsin, and Columbia. Highest standards.",
        "nature": "Perfectionist",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 3,
        "perception": 3,
        "intelligence": 5,
        "wits": 3,
        "academics": 5,
        "research": 5,
        "occult": 4,
        "leadership": 3,
        "willpower": 7,
    }
)

# Reverend Montague Winters - Hermetic scholar
winters, _ = MtAHuman.objects.get_or_create(
    name="Reverend Montague Winters",
    defaults={
        "description": "Episcopal priest and preeminent Hermetic tradition scholar. Dean of College of Hermetic Studies. "
        "Practicing Hermeticist and alchemist who believes Christianity and Hermeticism are reconcilable. "
        "Inspired by Giordano Bruno. Works in complete privacy, has never taken a student.",
        "nature": "Visionary",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 3,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        "academics": 4,
        "occult": 5,
        "theology": 4,
        "research": 4,
        "willpower": 7,
    }
)

# Geoffrey Truesdell - Elder Brother/Mentor
truesdell, _ = MtAHuman.objects.get_or_create(
    name="Geoffrey Truesdell",
    defaults={
        "description": "Elder Brother and Journeyman serving as mentor to new Neophytes. "
        "Georgetown Chapter House. Patient teacher and guide to those beginning the Journey.",
        "nature": "Pedagogue",
        "strength": 2,
        "dexterity": 2,
        "stamina": 3,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 3,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        "leadership": 3,
        "research": 4,
        "occult": 4,
        "academics": 4,
        "instruction": 4,
        "willpower": 7,
    }
)

# =============================================================================
# TEMPLATE CHARACTERS (Neophytes)
# =============================================================================

# Jonathan Lewis - Neophyte narrator
lewis, _ = MtAHuman.objects.get_or_create(
    name="Jonathan Lewis",
    defaults={
        "description": "Renaissance historian and new Neophyte of the Arcanum (Georgetown Chapter). "
        "Cambridge educated, initially joined for access to research materials but is beginning "
        "to understand the deeper mission. Keeps a detailed journal of his Journey.",
        "nature": "Traditionalist",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 2,
        "perception": 3,
        "intelligence": 3,
        "wits": 3,
        "academics": 3,
        "research": 3,
        "computer": 1,
        "occult": 2,
        "willpower": 5,
    }
)

# Nahar Khan - Neophyte parapsychologist
khan, _ = MtAHuman.objects.get_or_create(
    name="Nahar Khan",
    defaults={
        "description": "Bengali-American licensed psychologist and parapsychologist. Late 20s. "
        "Founded the Foundation for Paranormal Studies but faced bankruptcy. "
        "Joined the Arcanum for funding in exchange for research. Studies unexplored dimensions of the mind.",
        "nature": "Visionary",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 2,
        "perception": 3,
        "intelligence": 3,
        "wits": 2,
        "awareness": 3,
        "psychology": 3,
        "meditation": 2,
        "research": 2,
        "academics": 2,
        "medicine": 1,
        "occult": 2,
        "willpower": 6,
    }
)

# William Barron - Neophyte linguist
barron, _ = MtAHuman.objects.get_or_create(
    name="William Barron",
    defaults={
        "description": "Linguist in early 20s, fluent in Sanskrit, Coptic, Persian, Syriac, Aramaic, Arabic, "
        "plus classical and modern European languages. Never finished undergraduate English degree, "
        "mostly self-taught. Reserved but friendly. Assists with translations of ancient manuscripts.",
        "nature": "Loner",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 3,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        "academics": 4,
        "research": 3,
        "occult": 2,
        "willpower": 5,
    }
)

# Paul DeLevie - Neophyte engineer
delevie, _ = MtAHuman.objects.get_or_create(
    name="Paul DeLevie",
    defaults={
        "description": "Jack of all trades with engineering training. Tall, rugged, outdoorsy. "
        "Hired by Arcanum as special consultant on various occasions. 'Reservoir of manly knowledge.' "
        "Armed (carries two concealed firearms) and capable in survival situations.",
        "nature": "Survivor",
        "strength": 3,
        "dexterity": 3,
        "stamina": 3,
        "charisma": 2,
        "manipulation": 1,
        "appearance": 3,
        "perception": 3,
        "intelligence": 2,
        "wits": 3,
        "alertness": 3,
        "athletics": 3,
        "brawl": 3,
        "dodge": 2,
        "firearms": 4,
        "melee": 2,
        "survival": 3,
        "stealth": 3,
        "technology": 3,
        "willpower": 6,
    }
)

# =============================================================================
# STAFF CHARACTERS
# =============================================================================

# Mark Wayne - Secretary
wayne, _ = MtAHuman.objects.get_or_create(
    name="Mark Wayne",
    defaults={
        "description": "Young, cute French major working as secretary at a local Arcanum Chapter. "
        "Answers phones, types, generally clueless about the real nature of what's in the building. "
        "His uncle pulled strings to get him the job.",
        "nature": "Conformist",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 1,
        "appearance": 3,
        "perception": 2,
        "intelligence": 2,
        "wits": 2,
        "alertness": 1,
        "athletics": 3,
        "expression": 2,
        "technology": 2,
        "computer": 1,
        "willpower": 4,
    }
)

# Sylvia Dorn - Security consultant
dorn, _ = MtAHuman.objects.get_or_create(
    name="Sylvia Dorn",
    defaults={
        "description": "Former security guard who saw a UFO and ended up in tabloids, ruining her career. "
        "The Arcanum hired her to manage security operations. Trim black woman, about 30, "
        "short and petite but all muscle. Wears dark glasses. Efficient and paranoid (professionally).",
        "nature": "Jobsworth",
        "strength": 3,
        "dexterity": 3,
        "stamina": 3,
        "charisma": 2,
        "manipulation": 1,
        "appearance": 2,
        "perception": 3,
        "intelligence": 2,
        "wits": 3,
        "alertness": 3,
        "athletics": 3,
        "brawl": 3,
        "dodge": 2,
        "intimidation": 1,
        "streetwise": 1,
        "firearms": 4,
        "leadership": 1,
        "melee": 2,
        "stealth": 3,
        "technology": 3,
        "investigation": 3,
        "law": 2,
        "medicine": 1,
        "occult": 1,
        "willpower": 6,
    }
)

# Mr. Parks - Steward
parks, _ = MtAHuman.objects.get_or_create(
    name="Edward Parks",
    defaults={
        "description": "Steward of the Foundation House, part of a long-standing tradition - "
        "the Parks family has managed Vannever Hall for generations. Middle-aged, dignified, "
        "brisk Queen's English accent. Knows secret passageways and undiscovered cellars. "
        "Expects respect and gives it.",
        "nature": "Jobsworth",
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 4,
        "appearance": 3,
        "perception": 3,
        "intelligence": 2,
        "wits": 3,
        "alertness": 3,
        "diplomacy": 3,
        "etiquette": 5,
        "firearms": 2,
        "leadership": 2,
        "melee": 3,
        "stealth": 3,
        "technology": 2,
        "investigation": 3,
        "law": 2,
        "medicine": 1,
        "occult": 4,
        "willpower": 5,
    }
)

# =============================================================================
# ORDER OF HERMES OBSERVER
# =============================================================================

# Andrew Taylor - Order of Hermes mage who studies the Arcanum
taylor, _ = Mage.objects.get_or_create(
    name="Andrew Taylor",
    defaults={
        "description": "Former Arcanum Journeyman (Washington D.C. Chapter) who was chosen by an Order of Hermes Magus "
        "as apprentice. Now Awakened, continues to study the Arcanum's origins and true nature. "
        "Pleasant academic type: brown trench coat, tweed jacket, round spectacles, leather satchel. "
        "Quiet in public except at scholarly gatherings where he's eloquent.",
        "nature": "Judge",
        "essence": "Questing",
        "strength": 2,
        "dexterity": 2,
        "stamina": 3,
        "charisma": 3,
        "manipulation": 4,
        "appearance": 3,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        "alertness": 2,
        "athletics": 2,
        "awareness": 3,
        "dodge": 2,
        "expression": 4,
        "intuition": 3,
        "etiquette": 2,
        "firearms": 3,
        "leadership": 3,
        "meditation": 3,
        "research": 4,
        "stealth": 2,
        "technology": 1,
        "cosmology": 3,
        "enigmas": 3,
        "investigation": 2,
        "occult": 3,
        "willpower": 8,
        "arete": 6,
        "forces": 4,
        "mind": 4,
        "prime": 3,
        "correspondence": 1,
        "life": 2,
        "matter": 2,
        "spirit": 1,
    }
)

# =============================================================================
# TEMPLATE ARCHETYPES
# =============================================================================

# The Aspirant template
aspirant, _ = MtAHuman.objects.get_or_create(
    name="The Aspirant (Template)",
    defaults={
        "description": "Template: Seeker of the sacred and hidden. Has felt longing since childhood, "
        "seeking something other. Traveled the world exploring mythologies. Intellectually restless, "
        "never content. Quotes obscure mystics. The sacred is everywhere but hidden.",
        "nature": "Visionary",
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 2,
        "perception": 3,
        "intelligence": 4,
        "wits": 2,
        "alertness": 2,
        "awareness": 3,
        "brawl": 2,
        "dodge": 2,
        "expression": 2,
        "intuition": 4,
        "etiquette": 2,
        "meditation": 3,
        "melee": 2,
        "research": 2,
        "stealth": 3,
        "survival": 2,
        "enigmas": 2,
        "investigation": 3,
        "occult": 3,
        "willpower": 5,
    }
)

# Bibliothecary template
bibliothecary, _ = MtAHuman.objects.get_or_create(
    name="Bibliothecary (Template)",
    defaults={
        "description": "Template: Expert in books themselves - binding, conservation, analysis. "
        "Books mean more than people. Trained in both academic and technical aspects of book history. "
        "Can verify authenticity of texts. Shows real excitement only over books, not ideas.",
        "nature": "Fanatic",
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 3,
        "appearance": 2,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        "alertness": 2,
        "awareness": 1,
        "expression": 2,
        "intuition": 2,
        "crafts": 3,
        "research": 3,
        "technology": 2,
        "academics": 4,
        "investigation": 3,
        "occult": 2,
        "science": 3,
        "willpower": 6,
    }
)

# Fey Poet template
fey_poet, _ = MtAHuman.objects.get_or_create(
    name="Fey Poet (Template)",
    defaults={
        "description": "Template: Disappeared for seven years as a child, returned with no memory "
        "but strange knowledge and intuition. Writes poetry. Attention span varies wildly. "
        "Entranced by natural beauty. Says enigmatic things. Acts both young and old.",
        "nature": "Deviant",
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 2,
        "appearance": 4,
        "perception": 3,
        "intelligence": 2,
        "wits": 2,
        "alertness": 2,
        "awareness": 3,
        "brawl": 2,
        "dodge": 2,
        "expression": 4,
        "intuition": 3,
        "leadership": 1,
        "meditation": 2,
        "melee": 2,
        "stealth": 3,
        "survival": 2,
        "enigmas": 1,
        "willpower": 5,
    }
)

# Hermetic Scholar template
hermetic_scholar, _ = MtAHuman.objects.get_or_create(
    name="Hermetic Scholar (Template)",
    defaults={
        "description": "Template: Young, knowledgeable but inexperienced. Fascinated with the occult since childhood. "
        "Tutored by mysterious mentor who disappeared, leaving only a note to 'Seek the Arcanum.' "
        "Expert in Hermetic sciences. Arrogant about areas of expertise. Shows wisdom beyond years.",
        "nature": "Traditionalist",
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 3,
        "intelligence": 3,
        "wits": 3,
        "awareness": 2,
        "intuition": 2,
        "etiquette": 2,
        "firearms": 2,
        "leadership": 2,
        "meditation": 2,
        "melee": 3,
        "research": 2,
        "enigmas": 2,
        "investigation": 1,
        "occult": 3,
        "willpower": 7,
    }
)

# Psychic Investigator template
psychic_investigator, _ = MtAHuman.objects.get_or_create(
    name="Psychic Investigator (Template)",
    defaults={
        "description": "Template: Ex-cop who nearly died from head trauma, emerged from coma "
        "able to see spirits. Kicked off the force. Tabloid case led to Arcanum recruitment. "
        "Tough, doesn't buy occult malarkey normally but forced to broaden horizons. Calm under fire.",
        "nature": "Survivor",
        "strength": 3,
        "dexterity": 2,
        "stamina": 3,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 3,
        "intelligence": 2,
        "wits": 4,
        "alertness": 3,
        "athletics": 2,
        "awareness": 2,
        "brawl": 3,
        "dodge": 2,
        "intuition": 2,
        "streetwise": 2,
        "firearms": 3,
        "stealth": 2,
        "investigation": 3,
        "law": 2,
        "willpower": 6,
    }
)

# =============================================================================
# ARTIFACTS & WONDERS
# =============================================================================

# Mentat Stone - Matrix
mentat_matrix, _ = Wonder.objects.get_or_create(
    name="Mentat Stone (Matrix)",
    defaults={
        "description": "A psychic focus stone that helps psychics better focus their abilities. "
        "Carrying a Matrix lowers the difficulty of Psychic Phenomena rolls by 1.",
        "rank": 1,
        "background_cost": 1,
        "quintessence_max": 0,
    }
)

# Mentat Stone - Inhibitor
mentat_inhibitor, _ = Wonder.objects.get_or_create(
    name="Mentat Stone (Inhibitor)",
    defaults={
        "description": "A stone that interferes with psychic activity. Those carrying an Inhibitor "
        "are protected from psychic interference: the use of any psychic affinity which would "
        "directly affect the bearer has the difficulty increased by 1.",
        "rank": 1,
        "background_cost": 1,
        "quintessence_max": 0,
    }
)

# Shadow Cloak
shadow_cloak, _ = Wonder.objects.get_or_create(
    name="Shadow Cloak",
    defaults={
        "description": "A black cloak that makes the wearer almost invisible in darkness or shadow. "
        "Grants three automatic successes (or three additional dice) of Stealth when traveling in dim light.",
        "rank": 2,
        "background_cost": 2,
        "quintessence_max": 0,
    }
)

# Faerie Ring
faerie_ring, _ = Wonder.objects.get_or_create(
    name="Faerie Ring",
    defaults={
        "description": "Intricately wrought silver ring indicating the blessing of the fae. "
        "The wearer is considered a friend of the fae folk and will be welcomed by them. "
        "The ring increases the difficulty of fae magic (Glamour) used against the wearer by 2.",
        "rank": 3,
        "background_cost": 3,
        "quintessence_max": 0,
    }
)

# Silver Chalice
silver_chalice, _ = Wonder.objects.get_or_create(
    name="Silver Chalice",
    defaults={
        "description": "A powerful healing chalice, possibly related to the Holy Grail. "
        "Drinking pure spring water from it while standing on holy ground immediately heals all damage "
        "(aggravated or not). Can only be used once each full moon, and a person can only benefit once ever.",
        "rank": 4,
        "background_cost": 4,
        "quintessence_max": 0,
    }
)

# Crusader's Sword
crusaders_sword, _ = Wonder.objects.get_or_create(
    name="Crusader's Sword",
    defaults={
        "description": "Medieval broadsword from the Crusades with a saint's bone-splinter in the hilt. "
        "When wielded by one with True Faith, the reversed hilt acts as a holy symbol and the blade "
        "ignites with holy power. Adds one die of damage per Faith roll success. "
        "Wounds are aggravated. Requires Strength 3 to wield, causes Strength+5 damage. "
        "The Arcanum owns five variants; Society of Leopold has three more.",
        "rank": 5,
        "background_cost": 5,
        "quintessence_max": 0,
    }
)

# The Holy Grail
holy_grail, _ = Wonder.objects.get_or_create(
    name="The Holy Grail",
    defaults={
        "description": "The chalice used by Christ at the Last Supper, later used by Joseph of Arimathea "
        "to collect the Lord's blood as it dripped from the Cross. The Quest for the Grail is the focus "
        "of much medieval literature. A glimpse of the Grail is a glimpse of Heaven. "
        "Greater Relic - beyond system mechanics, requires great quest.",
        "rank": 10,
        "background_cost": 10,
        "quintessence_max": 100,
    }
)

# Durandal
durandal, _ = Wonder.objects.get_or_create(
    name="Durandal",
    defaults={
        "description": "The sword of Roland, one of Charlemagne's Paladins. Once wielded by Hector of Troy. "
        "So powerful that no metal can resist it. Disappeared after Roland's death, "
        "said to be somewhere in Arabia. Greater Relic - beyond system mechanics, requires great quest.",
        "rank": 10,
        "background_cost": 10,
        "quintessence_max": 100,
    }
)

# The Cauldron of Annwn
cauldron_annwn, _ = Wonder.objects.get_or_create(
    name="The Cauldron of Annwn",
    defaults={
        "description": "Located in the Otherworld, said to have powers of healing. "
        "A corpse placed in it is brought back to life, though lacking the power of speech. "
        "Some tales link it with the Grail. Greater Relic - beyond system mechanics, requires great quest.",
        "rank": 10,
        "background_cost": 10,
        "quintessence_max": 100,
    }
)

# =============================================================================
# MINOR CHARACTERS
# =============================================================================

# Other founding members mentioned
heath, _ = MtAHuman.objects.get_or_create(
    name="Stewart Heath",
    defaults={
        "description": "Founding member of the Arcanum from Manchester. "
        "One of the original nine who gathered at Vannever Hall in 1885.",
        "nature": "Traditionalist",
        "willpower": 6,
    }
)

harker, _ = MtAHuman.objects.get_or_create(
    name="Peter Harker",
    defaults={
        "description": "Founding member of the Arcanum from London. "
        "One of the original nine who gathered at Vannever Hall in 1885.",
        "nature": "Traditionalist",
        "willpower": 6,
    }
)

# Those who declined to join
kenealy, _ = MtAHuman.objects.get_or_create(
    name="George Kenealy",
    defaults={
        "description": "Invited to the founding of the Arcanum but declined. "
        "Was himself a magus of the Order of Hermes. Failed to detect Holmscroft's true nature.",
        "nature": "Traditionalist",
        "willpower": 6,
    }
)

sullivan, _ = MtAHuman.objects.get_or_create(
    name="Thomas Sullivan",
    defaults={
        "description": "Invited to the founding of the Arcanum but declined.",
        "nature": "Traditionalist",
        "willpower": 5,
    }
)

# Minor character from prelude
christine, _ = MtAHuman.objects.get_or_create(
    name="Christine",
    defaults={
        "description": "Arcanist rock-climber searching for a long-lost church in the Ethiopian Highlands. "
        "This sort of field work - dangerous but potentially rewarding - is typical of Arcanum missions.",
        "nature": "Thrill-Seeker",
        "strength": 2,
        "dexterity": 3,
        "stamina": 3,
        "athletics": 3,
        "climbing": 3,
        "survival": 2,
        "willpower": 6,
    }
)

keith, _ = MtAHuman.objects.get_or_create(
    name="Keith",
    defaults={
        "description": "Arcanist rock-climber, partner to Christine, searching for a long-lost church "
        "in the Ethiopian Highlands. Skilled and better prepared for the dangerous climb.",
        "nature": "Survivor",
        "strength": 3,
        "dexterity": 3,
        "stamina": 3,
        "athletics": 3,
        "climbing": 4,
        "survival": 3,
        "willpower": 6,
    }
)

# Historic alchemists mentioned
seneca_hunt, _ = MtAHuman.objects.get_or_create(
    name="Seneca Hunt",
    defaults={
        "description": "Recently deceased historian of the Arcanum and expert in Elizabethan studies. "
        "Had begun researching a thorough history of the Arcanum, gathering notes and primary research, "
        "before suffering a heart attack. His notes form the basis for Neophyte training materials.",
        "nature": "Architect",
        "academics": 5,
        "research": 5,
        "occult": 3,
        "willpower": 7,
    }
)

print("Halls of the Arcanum populate script completed successfully!")
print(f"Created book: {book.name}")
print(f"Created {MageFaction.objects.filter(name__in=['The Arcanum', 'Hermetic Order of the Rising Day', 'Les Frères de la Rose Croix', 'Society of Leopold', 'Order of St. Hermes', 'Crucible Genetics Amalgamated']).count()} organizations")
print(f"Created/updated {MtAHuman.objects.filter(name__icontains='Template').count()} character templates")
print(f"Created/updated {Wonder.objects.filter(name__in=['Mentat Stone (Matrix)', 'Mentat Stone (Inhibitor)', 'Shadow Cloak', 'Faerie Ring', 'Silver Chalice', 'Crusader\\'s Sword', 'The Holy Grail', 'Durandal', 'The Cauldron of Annwn']).count()} wonders/artifacts")
print(f"Total characters created/updated: {MtAHuman.objects.filter(name__in=[h.name for h in [holmscroft, murray, brown, dulac, mcphee, kelvin, linarelli, corwin, beaucourt, talbot, stanhope, sorensen, dsouza, winters, truesdell, lewis, khan, barron, delevie, wayne, dorn, parks, aspirant, bibliothecary, fey_poet, hermetic_scholar, psychic_investigator, heath, harker, kenealy, sullivan, christine, keith, seneca_hunt]]).count()}")
print(f"Total Awakened mages: {Mage.objects.filter(name='Andrew Taylor').count()}")
