"""
The Book of Madness - First Edition
Populate database with characters, items, and concepts from the sourcebook
"""

from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.tradition import Tradition
from characters.models.mage.faction import MageFaction
from characters.models.werewolf.garou import Garou
from characters.models.vampire.vampire import Vampire
from items.models.mage.wonder import Wonder
from items.models.mage.talisman import Talisman
from core.models import Book


def add_source():
    """Add The Book of Madness as a source"""
    book, created = Book.objects.get_or_create(
        title="The Book of Madness",
        edition="1st Edition",
        gameline="mta",
        defaults={
            "publication_year": 1994,
            "publisher": "White Wolf",
            "book_type": "supplement"
        }
    )
    return book


def create_factions():
    """Create factions and groups mentioned in the book"""

    # Nephandi-related factions
    nephandi, _ = MageFaction.objects.get_or_create(
        name="Nephandi",
        defaults={
            "description": "Mages who have sworn themselves to the service of the Outer Darkness, seeking to extinguish Ascension and open the way for their dark masters.",
            "faction_type": "fallen"
        }
    )

    butcher_street, _ = MageFaction.objects.get_or_create(
        name="Butcher Street Regulars",
        parent=None,  # Marauder group
        defaults={
            "description": "An organized Marauder group led by Robert Davenport, working to combat the Nephandi and Technocracy while spreading dynamic chaos.",
            "faction_type": "marauder"
        }
    )

    umbral_underground, _ = MageFaction.objects.get_or_create(
        name="Umbral Underground",
        defaults={
            "description": "A loose network of Marauders and their allies operating across the Umbra and Earth, fighting for dynamic reality.",
            "faction_type": "marauder"
        }
    )

    bai_dai, _ = MageFaction.objects.get_or_create(
        name="Bai Dai",
        defaults={
            "description": "A genocidal group of Marauders who believe the world would be easier returned to the Mythic Age if static reality were weaker by about five billion people.",
            "faction_type": "marauder"
        }
    )

    black_heart_cult, _ = MageFaction.objects.get_or_create(
        name="Cult of the Black Heart",
        defaults={
            "description": "Demon cult devoted to Grostolis with over 12,000 members worldwide, led by arch-priest Victor Neubauer.",
            "faction_type": "cult"
        }
    )

    jadrax_order, _ = MageFaction.objects.get_or_create(
        name="Order of Jadrax",
        defaults={
            "description": "Demon cult strongest in Northwestern United States with over 300 members, run by an elder vampire called the Hadaric.",
            "faction_type": "cult"
        }
    )

    black_stone_trinity, _ = MageFaction.objects.get_or_create(
        name="Black Stone Trinity",
        defaults={
            "description": "Small but dangerous demon cult led by three members practicing Satanic posturing turned deadly reality.",
            "faction_type": "cult"
        }
    )


def create_nephandi_characters(book):
    """Create Nephandi characters from Chapter One"""

    # Amanda Jonsson - Senex's apprentice from the prelude
    amanda, _ = Mage.objects.get_or_create(
        name="Amanda Jonsson",
        defaults={
            "tradition": None,  # New initiate
            "essence": "Pattern",
            "nature": "Survivor",
            "demeanor": "Conformist",
            "concept": "Former hitman turned initiate",
            "arete": 1,
            "willpower": 5,
            "quintessence": 3,
            "paradox": 1,
            "description": "Young mage initiated by Senex after nearly being killed by him. Serves as gatekeeper at Cerberus, but haunted by visions of her past life as Mercedes Gonzaga Ortiz and visited by her former lover, the Nephandus Alexander Gericauk."
        }
    )
    amanda.set_source(book)

    # Jodi Blake - Barabbi recruiter
    jodi, _ = Mage.objects.get_or_create(
        name="Jodi Blake",
        defaults={
            "tradition": None,  # Barabbi
            "essence": "Questing",
            "nature": "Director",
            "demeanor": "Bon Vivant",
            "arete": 6,
            "willpower": 7,
            "quintessence": 14,
            "paradox": 4,
            "strength": 2,
            "dexterity": 3,
            "stamina": 2,
            "charisma": 4,
            "manipulation": 5,
            "appearance": 4,
            "perception": 2,
            "intelligence": 3,
            "wits": 3,
            "concept": "Judas goat for renunciates",
            "age": 600,  # Appears youthful
            "description": "A master of deceit and manipulation, Jodi's history is unclear but she claims various defections from multiple Traditions. Nearly 600 years old with longevity rites involving sacrifice and blood drinking. Has corrupted at least 40 mages and controls many influential Sleepers. Excels at mortal skills over centuries of learning."
        }
    )
    jodi.set_source(book)

    # Herr Flax - Adsinistratus (also mentioned as Marauder in Ch. 3)
    herr_flax, _ = Mage.objects.get_or_create(
        name="Herr Flax",
        defaults={
            "tradition": None,  # Widderslainte Nephandus
            "essence": "Primordial",
            "nature": "Deviant",
            "demeanor": "Bon Vivant",
            "arete": 5,
            "willpower": 5,
            "quintessence": 10,
            "paradox": 5,
            "strength": 4,
            "dexterity": 4,
            "stamina": 5,
            "charisma": 5,
            "manipulation": 2,
            "appearance": 3,
            "perception": 3,
            "intelligence": 3,
            "wits": 4,
            "concept": "Youth culture corruptor",
            "description": "Born in rural Iowa 1936, awakened by Nephandus Byron. Loves youth subcultures especially grunge, death metal, and fantasy roleplaying. Passes himself off as demon or rock star, creates 'families' from disaffected youth then feeds on their despair. The Black Stone Trinity are his latest converts."
        }
    )
    herr_flax.set_source(book)

    # Yaqub al-Iblisi (Jacob the Iblitite)
    yaqub, _ = Mage.objects.get_or_create(
        name="Yaqub al-Iblisi",
        defaults={
            "tradition": None,  # Iblitic
            "essence": "Dynamic",
            "nature": "Conniver",
            "demeanor": "Fanatic",
            "arete": 6,
            "willpower": 7,
            "quintessence": 10,
            "paradox": 5,
            "strength": 3,
            "dexterity": 4,
            "stamina": 3,
            "charisma": 5,
            "manipulation": 5,
            "appearance": 0,  # Heavily deformed
            "perception": 4,
            "intelligence": 3,
            "wits": 5,
            "concept": "Deep cover agent with multiple masters",
            "description": "Former Adsinistratus Primus, now retired to backstage intrigues. Suffers grotesque Paradox deformities hidden under robes. Has somehow convinced three different Nephandi-Lords that each has exclusive claim to his soul. Can briefly take form of beautiful Persian youth."
        }
    )
    yaqub.set_source(book)

    # Al-Aswad, The Black Man - Ancient Nephandus
    al_aswad, _ = Mage.objects.get_or_create(
        name="Al-Aswad",
        defaults={
            "tradition": None,  # Ancient Nephandus
            "essence": "Primordial",
            "nature": "Avant-Garde",
            "demeanor": "Critic",
            "arete": 9,
            "willpower": 10,
            "quintessence": 10,
            "paradox": 10,
            "strength": 4,
            "dexterity": 5,
            "stamina": 7,
            "charisma": 8,
            "manipulation": 5,
            "appearance": 4,
            "perception": 5,
            "intelligence": 6,
            "wits": 4,
            "concept": "First Nephandus and first Aswad",
            "description": "Believed to be the first Nephandus and first to Descend to the Qlippoth of Entropy. Known in human lore as the 'black man' who presides over Satanic ceremonies. Monitors all Labyrinths and occasionally walks the world. Resides in the Dark Cathedral of Uzhuvrath overlooking the Black Pit of Unfathomable Foulness."
        }
    )
    al_aswad.set_source(book)


def create_marauder_characters(book):
    """Create Marauder characters from Chapter Three"""

    # Robert Davenport - Leader of Butcher Street Regulars
    davenport, _ = Mage.objects.get_or_create(
        name="Robert Davenport",
        defaults={
            "tradition": None,  # Orphan/Marauder
            "essence": "Questing",
            "nature": "Caregiver",
            "demeanor": "Director",
            "arete": 4,
            "willpower": 9,
            "quintessence": 12,
            "strength": 2,
            "dexterity": 4,
            "stamina": 3,
            "charisma": 4,
            "manipulation": 3,
            "appearance": 2,
            "perception": 3,
            "intelligence": 4,
            "wits": 3,
            "concept": "Surgeon turned Marauder leader",
            "quiet_rating": 2,
            "description": "Cardiovascular surgeon studying chaos in heart defibrillation. Rejected Technocracy recruitment. Became Marauder when Technocracy killed his family. Believes wife Maraya and daughter Karen still alive. Leads Butcher Street Regulars and acts as web center for Umbral Underground on Earth. His Avatar appears as his wife."
        }
    )
    davenport.set_source(book)

    # Senorita Abraxas - ex-NWO spy
    abraxas, _ = Mage.objects.get_or_create(
        name="Senorita Abraxas",
        defaults={
            "tradition": None,  # ex-NWO, now Marauder
            "essence": "Pattern",
            "nature": "Visionary",
            "demeanor": "Loner",
            "arete": 3,
            "willpower": 8,
            "quintessence": 6,
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "charisma": 3,
            "manipulation": 4,
            "appearance": 2,
            "perception": 3,
            "intelligence": 3,
            "wits": 4,
            "concept": "Spanish NWO agent converted to Marauder",
            "quiet_rating": 3,
            "description": "Born in provincial Spain, raised on grandfather's military stories. Recruited by NWO for espionage division. Sent to investigate Marauders, instead converted by Davenport. Believes Davenport is El Cid. Now serves as weaponsmith and technical expert for Butcher Street Regulars. Completely average appearance aids espionage."
        }
    )
    abraxas.set_source(book)

    # Lord Ex / Richard Thomlinson
    lord_ex, _ = Mage.objects.get_or_create(
        name="Richard Thomlinson",
        defaults={
            "tradition": None,  # Marauder
            "essence": "Dynamic",
            "nature": "Survivor",
            "demeanor": "Jester",
            "arete": 1,
            "willpower": 7,
            "strength": 4,
            "dexterity": 3,
            "stamina": 2,
            "charisma": 2,
            "manipulation": 3,
            "appearance": 2,
            "perception": 4,
            "intelligence": 3,
            "wits": 3,
            "concept": "Victorian actor vigilante",
            "quiet_rating": 5,
            "description": "Victorian-era actor who fought injustice by night as Lord Ex. Awakened witnessing vampire/Euthanatos battle but suppressed memory, going straight into Marauder Quiet. World is 19th century England to him. Wears opera cloak, top hat, domino mask, carries sabre and pistols with white rose in buttonhole."
        }
    )
    lord_ex.set_source(book)

    # Mother Goose
    mother_goose, _ = Mage.objects.get_or_create(
        name="Mother Goose",
        defaults={
            "tradition": None,  # Marauder
            "essence": "Dynamic",
            "nature": "Caregiver",
            "demeanor": "Caregiver",
            "arete": 5,
            "willpower": 5,
            "quintessence": 2,
            "strength": 1,
            "dexterity": 2,
            "stamina": 1,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 1,
            "perception": 3,
            "intelligence": 3,
            "wits": 4,
            "concept": "Elder abuse victim turned zooterrorist",
            "quiet_rating": 3,
            "description": "Elderly victim of abuse by drug-dealing grandson. Awakened calling on salamander from childhood memories, destroying house and all inhabitants. Now archetypal zooterrorist who summons everything from griffins to cockatrice. Carries sawed-off shotgun in green coat pockets stuffed with pet treats."
        }
    )
    mother_goose.set_source(book)

    # Medea - Marauder Oracle
    medea, _ = Mage.objects.get_or_create(
        name="Medea",
        defaults={
            "tradition": None,  # ex-Verbena, Marauder Oracle
            "essence": "Primordial",
            "nature": "Traditionalist",
            "demeanor": "Fanatic",
            "arete": 10,
            "willpower": 10,
            "quintessence": 13,
            "strength": 4,
            "dexterity": 4,
            "stamina": 4,
            "charisma": 5,
            "manipulation": 3,
            "appearance": 4,
            "perception": 4,
            "intelligence": 3,
            "wits": 4,
            "concept": "The actual mythological Medea",
            "quiet_rating": 2,
            "age": 3000,  # Approximate
            "description": "The actual Medea from Greek mythology, daughter of King of Colchis, wife of Jason. After exile, spent two millennia in Umbra. Returned 1346, chose to become Marauder Oracle in face of Technocracy. Only known active Marauder Oracle. Followed by twelve-member Black Fury pack. Believes world is Heroic Greece."
        }
    )
    medea.set_source(book)

    # Stephen of Warwick / Professor Warwick
    stephen, _ = Mage.objects.get_or_create(
        name="Stephen of Warwick",
        defaults={
            "tradition": None,  # ex-Verbena
            "essence": "Pattern",
            "nature": "Loner",
            "demeanor": "Architect",
            "arete": 6,
            "willpower": 7,
            "quintessence": 5,
            "strength": 2,
            "dexterity": 3,
            "stamina": 2,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 3,
            "perception": 3,
            "intelligence": 4,
            "wits": 3,
            "concept": "10th century hunter/lore-master with split personality",
            "quiet_rating": 1,
            "age": 1000,
            "description": "Famous 10th century hunter (Dun Cow of Warwick) and lore-master. Spent 7 years in Arcadia, returned to find Normans invaded. Joined monks to preserve history. Split personality: Professor Warwick (rationalist 357 days/year) and Stephen (hunter on 8 feast days). Mated to young Garou Philodox."
        }
    )
    stephen.set_source(book)


def create_diabolist_characters(book):
    """Create Diabolist and demon-related characters from Chapter Four"""

    # Victor Neubauer - Cult of Black Heart leader
    neubauer, _ = MtAHuman.objects.get_or_create(
        name="Victor Neubauer",
        defaults={
            "concept": "Arch-priest and powerful Diabolist",
            "willpower": 8,
            "description": "Former Celestial Chorus acolyte, now arch-priest of the Cult of the Black Heart devoted to demon Grostolis. Leads covens worldwide with over 12,000 members. Extremely cunning, removes rival demon priests before they pose threats. Conducts monthly sacrifices during no-moon phase."
        }
    )
    neubauer.set_source(book)

    # Horus Longstreet - Cult of Vugarius leader
    longstreet, _ = MtAHuman.objects.get_or_create(
        name="Horus Longstreet",
        defaults={
            "concept": "Powerful Diabolist controlling entire town",
            "willpower": 9,
            "description": "Powerful Diabolist who corrupted entire town of Bracketon, New Mexico into service of demon Vugarius. Converted law enforcement, politicians, doctors first, then majority fell in line. Non-converts sacrificed. Preparing the Hecatomb: ritual slaughter of 250+ people to manifest Vugarius permanently."
        }
    )
    longstreet.set_source(book)

    # Sandi Thornhill, William Pascario, Shawn McNamara - Black Stone Trinity
    sandi, _ = MtAHuman.objects.get_or_create(
        name="Sandi Thornhill",
        defaults={
            "concept": "Black Stone Trinity cultist",
            "willpower": 4,
            "strength": 2,
            "dexterity": 3,
            "stamina": 2,
            "description": "Member of Black Stone Trinity demon cult. Kicked out of S.C.A. group with William Pascario. Owns basalt altar that names the group. Capable fighter (Brawl 3, Melee 4). Involved in gang rape, assaults, thefts, animal torture, and witch's powder creation."
        }
    )
    sandi.set_source(book)


def create_umbrood_characters(book):
    """Create Umbrood spirit characters from Chapter Five"""

    # Baron Vlaxon - Border guardian
    vlaxon, _ = MtAHuman.objects.get_or_create(
        name="Baron Vlaxon",
        defaults={
            "concept": "Umbrood Preceptor guarding the Horizon",
            "willpower": 8,
            "description": "Portly, boisterous Umbrood Preceptor commanding the Borders between Horizon and Astral World's Near Umbra. Commands soldiers watching for invaders through windows in mighty fortress. Blows monstrous horn to alert Court when enemies detected. Secretly raids across Horizon for booty."
        }
    )
    vlaxon.set_source(book)

    # Lady Beloia - Servitor of Abba-il-Aeon
    beloia, _ = MtAHuman.objects.get_or_create(
        name="Lady Beloia",
        defaults={
            "concept": "Umbrood Lord embodying curiosity",
            "willpower": 9,
            "description": "Servitor of Abba-il-Aeon, possibly Aeon's curiosity given form. Appears as lady knight in shining mail with billowing cloak. True form resembles multi-colored brilliant gasses. Seeks to reunite the Pure Ones. Sworn enemy of Ialdabaoth's minions. Eagerly interacts with humans seeking understanding."
        }
    )
    beloia.set_source(book)


def create_talismans(book):
    """Create Talismans and Wonders from the book"""

    # Whispering Stone
    whispering_stone, _ = Talisman.objects.get_or_create(
        name="Whispering Stone",
        defaults={
            "rank": 3,
            "arete": 3,
            "quintessence": 15,
            "sphere_requirements": "Mind 3",
            "description": "Insidious object resembling small stone, shell or crystal, given as gift. Sits silently for certain period, then begins whispering telepathically to keyed person. Voices feed insecurities and doubts until target leaves area, goes mad, or dies. Reads thoughts and responds accordingly (Mind 3). Consumes one Quintessence per day for up to 15 days.",
            "game_effects": "Mind 3 telepathic whispers that exploit target's insecurities. Prime 2 consumption of 1 Quintessence/day. Coincidental Effect."
        }
    )
    whispering_stone.set_source(book)

    # Lash of Passion
    lash_of_passion, _ = Talisman.objects.get_or_create(
        name="Lash of Passion",
        defaults={
            "rank": 4,
            "arete": 6,
            "quintessence": 20,
            "sphere_requirements": "Mind 2, Entropy 3-4",
            "description": "Bestowed upon Herr Flax by Lucricia the Succubus. Does Strength+1 damage (difficulty 7) normally, can grab/grapple at difficulty 8. Grasping handle instills self-confidence (Mind 1). Touch is pleasurable though damage occurs normally, eventually making pain seem like pleasure (Mind 2). Can slice through hard materials (Entropy 3) or cause festering wounds that spread (Entropy 4, lose 1 Health/day unless healed, can disable limbs).",
            "game_effects": "Normal whip damage Str+1. Mind 1 confidence boost (coincidental). Mind 2 pain=pleasure, resisted by Willpower (coincidental). Entropy 3 Destroy Matter (vulgar). Entropy 4 festering wounds (really vulgar)."
        }
    )
    lash_of_passion.set_source(book)


def create_creatures(book):
    """Create creature templates mentioned in the book"""

    # Ukrainian Firebird
    firebird, _ = MtAHuman.objects.get_or_create(
        name="Ukrainian Firebird",
        defaults={
            "concept": "Mythic flame-bird creature",
            "willpower": 5,
            "description": "Flame-colored mythic bird resembling traditional lacquer-paintings. Low-bodied, long-necked with spectacular wing plumage. Flames envelop bird especially at neck. Too weak for direct attacks but extreme temperature makes useful ally. Flames cannot be extinguished by normal means - require Forces 4 or Prime 3 to put out bird itself. Requires 5 Tass per month in Realms or 5 per hour in static reality."
        }
    )
    firebird.set_source(book)

    # Upland Yeti (Abominable Snowman)
    yeti, _ = MtAHuman.objects.get_or_create(
        name="Upland Yeti",
        defaults={
            "concept": "Placid omnivorous Abominable Snowman",
            "willpower": 8,
            "strength": 6,
            "dexterity": 4,
            "stamina": 4,
            "description": "Big creature with almost no neck, pure white shaggy fur, coal-black eyes, two-inch fangs, piton-like claws. Placid omnivore, acts like Garou-sized sloth. Prefers thin atmosphere above snowline. Smarter than genius orangutan. When attacked, flees (20mph flat, 30mph uneven terrain using upper body strength). If forced to fight: Str+2 claws, bearhug, roundhouse rake, twist-head-off. Weighs quarter-ton. Popular as pack animals and companions. Requires 1 Tass per hour on Earth."
        }
    )
    yeti.set_source(book)

    # Chi-rin
    chirin, _ = MtAHuman.objects.get_or_create(
        name="Chi-rin",
        defaults={
            "concept": "Chinese unicorn-like creature of Order",
            "willpower": 4,
            "strength": 2,
            "dexterity": 4,
            "stamina": 3,
            "description": "Spotted like leopard/giraffe, color varies pale gold with reddish-brown spots to deep russet with blue-black spots. Single stubby curved horn. Size of goat (males) or smaller (females). Can read auras to detect true nature (Perception+Awareness diff 7), Step Sideways, and fly 15 yards/turn. Appearance signals just rule. Flee from unjust or Wyrm-tainted. Cannot be taken to festering Earth - would sicken and die in minutes. May rescue Marauders by crossing Gauntlet, often dying in attempt. Requires 2 Tass per month in Realms."
        }
    )
    chirin.set_source(book)

    # Griffin
    griffin, _ = MtAHuman.objects.get_or_create(
        name="Griffin",
        defaults={
            "concept": "Intelligent eagle-lion hybrid",
            "willpower": 7,
            "strength": 5,
            "dexterity": 3,
            "stamina": 6,
            "description": "Front parts (head, talons, shoulders, wings) of golden eagle, rear end of African lion. Last one in England conversed with Lewis Carroll. Puzzling temperament: if curious, you're safe and may be instructed in universal order. If seem stupid, may be ignored or eaten. Do not use controlling magicks - long memory, no patience for fools. Can Step Sideways and fly 10 yards/turn. Excellent shock-troops especially vs Men-in-Black whose memories short out on encountering griffins. Requires 1 Tass per month in Umbra/Realms, 2 per week on Earth."
        }
    )
    griffin.set_source(book)

    # Sphinx (Net-Sphinx)
    sphinx, _ = Mage.objects.get_or_create(
        name="Sphinx",
        defaults={
            "concept": "Riddling sphinx in Digital Web",
            "willpower": 8,
            "arete": 6,
            "quintessence": 0,  # Unnecessary in Web
            "strength": 3,
            "dexterity": 4,
            "stamina": 4,
            "charisma": 3,
            "manipulation": 4,
            "appearance": 4,
            "perception": 4,
            "intelligence": 5,
            "wits": 4,
            "description": "Only sphinx still living on Earth (in Digital Web). Resembles Greek female sphinx: long curly dark hair in traditional Greek style, human face/neck/front, lion body. Can shapeshift to lion-centaur with six limbs (four legs, two human arms) or possibly fully human. Lives in dusty tomb-like passages, deserted palaces, pyramidal labyrinths, decrepit libraries in little-used Web sector. Sometimes called Dido Ceuthonymus. May be guardian spirit bound to Mount Qaf by Ahl-i-Batin. Visitors sometimes don't return - taste for human 'flesh' (living mind), over-zealous Marauder protectors, or hatred of book-thieves."
        }
    )
    sphinx.set_source(book)


def create_effects_and_templates(book):
    """Create templates and special magical effects"""

    # This would create Effect objects if we had that model
    # For now, document key Qlippothic Entropy effects in descriptions

    common_cause = {
        "name": "Common Cause",
        "level": 1,
        "sphere": "Qlippothic Entropy",
        "description": "Allows Nephandus to recognize others of their kind and know when magickal Effect is being done in service of Nephandi-Lords."
    }

    murphys_law = {
        "name": "The Long Arm of Murphy's Law",
        "level": 2,
        "sphere": "Qlippothic Entropy",
        "description": "Only coincidental-type Effect used extensively by Nephandi. Can be directed at individual to make them temporary 'jinx' or at specific plans/endeavors. Each success means minor condition/event occurs in completely counterproductive manner."
    }

    sleep_of_reason = {
        "name": "The Sleep of Reason",
        "level": 3,
        "sphere": "Qlippothic Entropy",
        "description": "Causes sentient being's psyche to fall under sway of own dark side/shadow. Virtues become intentions to sin, derangements surface violently, vampires/werewolves enter Frenzy. Resisted with Willpower (victim rolls Willpower vs difficulty 8, each success subtracts one from Nephandus). Mental dodges may work if target knows attack coming. Madness lasts Effect's normal duration."
    }

    inheritance_flesh = {
        "name": "The Inheritance of the Flesh",
        "level": 4,
        "sphere": "Qlippothic Entropy",
        "description": "Not only withers life but covers victim with boils and pustules which spray corrosive pus when burst, infecting all living matter contacted. Anyone within arm's reach takes 1 aggravated Health Level per success (may be soaked). If victim takes 4+ Health Levels, becomes infected with withering disease."
    }

    obliteration = {
        "name": "Obliteration",
        "level": 5,
        "sphere": "Qlippothic Entropy",
        "description": "Only known way to make matter/energy completely disappear from all known reality, usually with implosive side effects. Highly vulgar. Does damage like direct Entropic attack. If subject destroyed by damage, ceases to be forever. Damage is aggravated but may be soaked. Can only target one thing at a time. Side effects include rips in Gauntlet, sometimes in Nephandus (large Paradox). Does not work against Horizon itself. In Deep Umbra (no Paradox), Masters of Qlippothic Entropy are horrifically powerful."
    }


def populate():
    """Main population function"""
    print("Adding The Book of Madness content...")

    book = add_source()
    print(f"Created/found book: {book.title}")

    print("Creating factions...")
    create_factions()

    print("Creating Nephandi characters...")
    create_nephandi_characters(book)

    print("Creating Marauder characters...")
    create_marauder_characters(book)

    print("Creating Diabolist characters...")
    create_diabolist_characters(book)

    print("Creating Umbrood characters...")
    create_umbrood_characters(book)

    print("Creating Talismans...")
    create_talismans(book)

    print("Creating mythic creatures...")
    create_creatures(book)

    print("Creating effects and templates...")
    create_effects_and_templates(book)

    print("The Book of Madness population complete!")


if __name__ == "__main__":
    populate()
