"""
Populate database with characters, items, and organizations from Mage: The Ascension - Ascension's Right Hand
This sourcebook focuses on custos (followers/companions) of mages.
"""

from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from core.models import Book


def add_source():
    """Add the source book"""
    return Book.objects.get_or_create(
        title="Ascension's Right Hand",
        gameline="mta",
        defaults={
            "publication_year": 1995,
        }
    )[0]


def populate_crossovers_staff(source):
    """Populate staff and regulars of the Crossovers organization"""

    # Zorro - Albino bartender and founder of Crossovers
    zorro, _ = MtAHuman.objects.get_or_create(
        name="Zorro (Zoe Rowell)",
        defaults={
            "description": "Albino bartender and alchemist from Spain. Short spiky white hair, pink eyes. "
                         "Founded the Crossovers organization to unite custos across Tradition boundaries. "
                         "Daughter of alchemists, came to America seeking mage cooperation.",
            "concept": "Bartender and Alchemist",
            "nature": "Architect",
            "demeanor": "Visionary",
            "affiliation": "Orphan/Crossovers",
            "essence": "Questing",
            "strength": 2,
            "dexterity": 2,
            "stamina": 3,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 2,
            "perception": 4,
            "intelligence": 3,
            "wits": 3,
            "willpower": 4,
            "source": source.title,
        }
    )

    # Dark Water - Leader of Corpselight Connoisseurs
    dark_water, _ = MtAHuman.objects.get_or_create(
        name="Dark Water",
        defaults={
            "description": "Native American psychic who leads the Corpselight Connoisseurs, a group of "
                         "Euthanatos consors investigating death and reincarnation. Cool, flowing, impenetrable demeanor.",
            "concept": "Psychic Investigator",
            "nature": "Visionary",
            "demeanor": "Judge",
            "affiliation": "Tradition (Euthanatos)",
            "essence": "Questing",
            "source": source.title,
        }
    )


def populate_marauders(source):
    """Populate the Marauder characters from the Oscars group"""

    # Oscar Fieldstone - The Director
    oscar, _ = Mage.objects.get_or_create(
        name="Oscar Fieldstone",
        defaults={
            "description": "Former Order of Hermes mage who went mad and now believes he's a movie director. "
                         "Carries his director's chair everywhere. Created an entire 'film crew' reality with his Quiet. "
                         "Married to Actress (former mathematician reprogrammed by Technocracy).",
            "concept": "Mad Movie Director",
            "essence": "Questing",
            "nature": "Visionary",
            "demeanor": "Director",
            "affiliation": "Marauder",
            "source": source.title,
        }
    )

    # Actress - Oscar's wife
    actress, _ = MtAHuman.objects.get_or_create(
        name="Actress",
        defaults={
            "description": "Once a brilliant mathematician, captured by Technocracy and reprogrammed. "
                         "Rescued by Oscar but her mind was shattered. Now plays all leading roles in Oscar's delusions. "
                         "Wife of Oscar Fieldstone.",
            "concept": "Damaged Actress",
            "nature": "Conformist",
            "demeanor": "Conformist",
            "affiliation": "Marauder",
            "essence": "Questing",
            "source": source.title,
        }
    )

    # Persephone - Squirrel-tailed fanged zebra
    persephone, _ = MtAHuman.objects.get_or_create(
        name="Persephone",
        defaults={
            "description": "A squirrel-tailed, fanged zebra from a Horizon Realm who acts as camera operator "
                         "for Oscar's 'films'. Maroon and black stripes that glow in the dark. Wears special "
                         "neck-harness with voice-activated video camera. Believes breaching the Gauntlet prevents "
                         "reality from solidifying and dying.",
            "concept": "Weird Umbral Critter Cinematographer",
            "nature": "Jester",
            "demeanor": "Martyr",
            "affiliation": "Marauder",
            "essence": "Questing",
            "strength": 3,
            "dexterity": 2,
            "stamina": 4,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 2,
            "perception": 4,
            "intelligence": 4,
            "wits": 3,
            "willpower": 4,
            "source": source.title,
        }
    )


def populate_technocracy_agents(source):
    """Populate Technocracy affiliated characters"""

    # Josh Snelling - Computer operator
    josh, _ = MtAHuman.objects.get_or_create(
        name="Josh Snelling",
        defaults={
            "description": "Computer operator recruited by the Syndicate after using hacking skills to ruin "
                         "his abusive father financially. Lives in fear of the organization, teaching himself "
                         "survival skills in case he needs to run. Has no idea he's dealing with mages.",
            "concept": "Frightened Computer Operator",
            "nature": "Survivor",
            "demeanor": "Conformist",
            "affiliation": "Technocracy (Syndicate)",
            "essence": "Questing",
            "strength": 3,
            "dexterity": 3,
            "stamina": 3,
            "charisma": 2,
            "manipulation": 3,
            "appearance": 2,
            "perception": 3,
            "intelligence": 4,
            "wits": 3,
            "willpower": 4,
            "source": source.title,
        }
    )

    # Dr. Michael R. Hanson - Technocracy scientist with Squeek
    hanson, _ = Mage.objects.get_or_create(
        name="Dr. Michael R. Hanson",
        defaults={
            "description": "Technocracy scientist-mage who partnered with the familiar spirit Squeek, "
                         "housed in a genetically enhanced laboratory rat. Uses Squeek for information gathering.",
            "concept": "Technocracy Scientist",
            "essence": "Questing",
            "affiliation": "Technocracy",
            "source": source.title,
        }
    )

    # XB3-3 - Cyborg guard
    xb3, _ = MtAHuman.objects.get_or_create(
        name="XB3-3",
        defaults={
            "description": "Former human turned cyborg guard after a crash. More machine than flesh, "
                         "extremely handsome but emotionless. Programmed to guard, no unauthorized entry. "
                         "Occasionally shows glimpses of suppressed humanity.",
            "concept": "Cyborg Guard",
            "nature": "Conformist",
            "demeanor": "Conformist",
            "affiliation": "Technocracy (Iteration X/Progenitors)",
            "essence": "Questing",
            "strength": 4,
            "dexterity": 3,
            "stamina": 4,
            "charisma": 1,
            "manipulation": 2,
            "appearance": 5,
            "perception": 2,
            "intelligence": 2,
            "wits": 3,
            "willpower": 3,
            "source": source.title,
        }
    )


def populate_tradition_custos(source):
    """Populate Tradition-affiliated custos"""

    # Reynolds - Order of Hermes butler
    reynolds, _ = MtAHuman.objects.get_or_create(
        name="Reynolds",
        defaults={
            "description": "Quintessential English butler serving Sir Rodney Haversham at Haven House (in Horizon Realm). "
                         "In his 50s, impeccably dressed, trained at butler school. Member of the Crossovers, believes "
                         "Traditions should cooperate more. Oversees staff of 30+.",
            "concept": "English Butler",
            "nature": "Caregiver",
            "demeanor": "Perfectionist",
            "affiliation": "Tradition (Order of Hermes)",
            "essence": "Questing",
            "strength": 2,
            "dexterity": 2,
            "stamina": 3,
            "charisma": 2,
            "manipulation": 3,
            "appearance": 3,
            "perception": 3,
            "intelligence": 4,
            "wits": 3,
            "willpower": 5,
            "source": source.title,
        }
    )

    # Sir Rodney Haversham
    haversham, _ = Mage.objects.get_or_create(
        name="Sir Rodney Haversham",
        defaults={
            "description": "Order of Hermes mage, master of Haven House in a Horizon Realm. "
                         "Sponsor of butler school who recruited Reynolds as his butler.",
            "concept": "Hermetic Noble",
            "essence": "Questing",
            "affiliation": "Tradition (Order of Hermes)",
            "source": source.title,
        }
    )

    # Cody - Verbena bodyguard
    cody, _ = MtAHuman.objects.get_or_create(
        name="Cody",
        defaults={
            "description": "East Tennessee mountain boy, now pushing 60 but still vigorous due to Verbena magic. "
                         "Professional bodyguard for Ella Claire Monroe for 40 years. Loves her but never told her. "
                         "Ugly scrunched-up freckled face, wears black leather duster hiding submachine gun. "
                         "Down-home lazy until action is needed.",
            "concept": "Devoted Bodyguard",
            "nature": "Martyr",
            "demeanor": "Deviant",
            "affiliation": "Tradition (Verbena)",
            "essence": "Questing",
            "strength": 3,
            "dexterity": 3,
            "stamina": 4,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 1,
            "perception": 3,
            "intelligence": 2,
            "wits": 3,
            "willpower": 7,
            "source": source.title,
        }
    )

    # Ella Claire Monroe
    ella, _ = Mage.objects.get_or_create(
        name="Ella Claire Monroe",
        defaults={
            "description": "Verbena mage from east Tennessee mountains. Saved Cody's life 40 years ago when he "
                         "rescued her from Technocracy agents. Used magic to extend his lifespan. "
                         "He's been her bodyguard and companion ever since.",
            "concept": "Mountain Witch",
            "essence": "Questing",
            "affiliation": "Tradition (Verbena)",
            "source": source.title,
        }
    )

    # Sallow (John Bremmen) - Dreamspeaker oracle
    sallow, _ = MtAHuman.objects.get_or_create(
        name="Sallow (John Bremmen)",
        defaults={
            "description": "Young oracle with prophetic dreams he cannot interpret until they come true. "
                         "Tall, lanky, tangled brown hair, crossed brown eyes, suffers from jaundice. "
                         "Usually wears pajamas. Uses TV static to induce hypnosis and calm himself. "
                         "Travels with Dreamspeaker mentor Assentia in RV.",
            "concept": "Whacked-out Seer",
            "nature": "Visionary",
            "demeanor": "Deviant",
            "affiliation": "Tradition (Dreamspeaker)",
            "essence": "Questing",
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "charisma": 5,
            "manipulation": 1,
            "appearance": 3,
            "perception": 5,
            "intelligence": 4,
            "wits": 2,
            "willpower": 4,
            "source": source.title,
        }
    )

    # Assentia
    assentia, _ = Mage.objects.get_or_create(
        name="Assentia",
        defaults={
            "description": "Dreamspeaker mage who discovered Sallow during Umbral journey. "
                         "Acts as counselor and interpreter for his visions. Travels with him in RV.",
            "concept": "Dreamspeaker Counselor",
            "essence": "Questing",
            "affiliation": "Tradition (Dreamspeaker)",
            "source": source.title,
        }
    )

    # Reverend Lonnie Ray Singer
    lonnie, _ = MtAHuman.objects.get_or_create(
        name="Reverend Lonnie Ray Singer",
        defaults={
            "description": "Handsome traveling evangelist for Celestial Chorus. Early 30s, blond, winning smile. "
                         "Reformed from selfish ways, now preaches compassion and service to the One. "
                         "Mesmerizing speaker, gives half his collections to charity, helps at shelters and hospitals.",
            "concept": "Traveling Evangelist",
            "nature": "Architect",
            "demeanor": "Fanatic",
            "affiliation": "Tradition (Celestial Chorus)",
            "essence": "Questing",
            "strength": 2,
            "dexterity": 2,
            "stamina": 3,
            "charisma": 5,
            "manipulation": 4,
            "appearance": 3,
            "perception": 2,
            "intelligence": 3,
            "wits": 3,
            "willpower": 3,
            "source": source.title,
        }
    )

    # Dr. Shayna Reed - Forensic pathologist
    shayna, _ = MtAHuman.objects.get_or_create(
        name="Dr. Shayna Reed",
        defaults={
            "description": "Chief Medical Examiner, forensic pathologist. Georgetown Law and Medical School graduate. "
                         "FBI consultant for Violent Crimes Task Force. Trim blonde in mid-40s, intense and driven. "
                         "Unaware of Euthanatos connection but occasionally aided/protected by them.",
            "concept": "Forensic Pathologist",
            "nature": "Architect",
            "demeanor": "Director",
            "affiliation": "Tradition (Euthanatos) - unaware",
            "essence": "Questing",
            "strength": 2,
            "dexterity": 3,
            "stamina": 2,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 3,
            "perception": 4,
            "intelligence": 5,
            "wits": 3,
            "willpower": 4,
            "source": source.title,
        }
    )


def populate_orphans_and_hollow_ones(source):
    """Populate Orphan and Hollow One characters"""

    # Shard - Brujah vampire
    shard, _ = MtAHuman.objects.get_or_create(
        name="Shard (Sharilyn Polopolis)",
        defaults={
            "description": "Brujah vampire, twin sister of Hollow One mage Lorelei. Short dark hair, icy blue eyes, "
                         "pale. Embraced by Mayday after being critically injured. Runs her own gang, watches over "
                         "her twin. Member of Crossovers. Sire to Church.",
            "concept": "Brujah Anarch Guardian",
            "nature": "Deviant",
            "demeanor": "Rebel",
            "affiliation": "Orphan (Hollow Ones)",
            "essence": "Questing",
            "strength": 3,
            "dexterity": 4,
            "stamina": 3,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 3,
            "perception": 2,
            "intelligence": 3,
            "wits": 2,
            "willpower": 4,
            "source": source.title,
        }
    )

    # Lorelei
    lorelei, _ = Mage.objects.get_or_create(
        name="Lorelei (Lorilyn Polopolis)",
        defaults={
            "description": "Hollow One mage, twin sister of Shard. Long dark hair with brilliant silver and red streaks. "
                         "Awakened at 15 when she accidentally set community center ablaze. Ran away to city with twin, "
                         "joined Hollow Ones. Protected by her vampire sister.",
            "concept": "Hollow One Twin",
            "essence": "Questing",
            "nature": "Rebel",
            "demeanor": "Rebel",
            "affiliation": "Orphan (Hollow Ones)",
            "source": source.title,
        }
    )

    # Church - Shard's childe
    church, _ = MtAHuman.objects.get_or_create(
        name="Church",
        defaults={
            "description": "Young-looking vampire (appears 14), Shard's childe. Pale blond hair to shoulders, "
                         "wears jeans and Crow T-shirt. Was runaway left for dead, Embraced by Shard. "
                         "Learning the ropes of vampire life.",
            "concept": "Young Vampire",
            "nature": "Survivor",
            "demeanor": "Child",
            "affiliation": "Orphan (Hollow Ones)",
            "essence": "Questing",
            "source": source.title,
        }
    )

    # Andrew Grieg
    grieg, _ = Mage.objects.get_or_create(
        name="Andrew Grieg",
        defaults={
            "description": "Orphan mage, lover and sometimes enemy of Safira the Pumonca. "
                         "Independent operator who swore off allegiance to anyone but himself.",
            "concept": "Independent Orphan",
            "essence": "Questing",
            "affiliation": "Orphan",
            "source": source.title,
        }
    )


def populate_gypsies_and_others(source):
    """Populate Gypsy and other supernatural custos"""

    # Kiril Zlatten - Gypsy
    kiril, _ = MtAHuman.objects.get_or_create(
        name="Kiril Zlatten",
        defaults={
            "description": "Young handsome Gypsy with dark features and hint of danger. Almost 6 feet tall, "
                         "lean and muscular. Multiple earrings, deep scratchy voice. Trained by great-aunt Varra "
                         "in Tarot and knife skills. Associates with Hollow Ones, carries messages between mages. "
                         "Soft-spoken but easily heard, constantly twirls knives.",
            "concept": "Gypsy Messenger",
            "nature": "Survivor",
            "demeanor": "Bravo",
            "affiliation": "The Rom (associates with Hollow Ones)",
            "essence": "Questing",
            "strength": 3,
            "dexterity": 4,
            "stamina": 3,
            "charisma": 5,
            "manipulation": 3,
            "appearance": 3,
            "perception": 4,
            "intelligence": 3,
            "wits": 4,
            "willpower": 4,
            "source": source.title,
        }
    )

    # Varra
    varra, _ = Mage.objects.get_or_create(
        name="Varra",
        defaults={
            "description": "Highly skilled Gypsy mage, great-aunt by marriage to Kiril Zlatten. "
                         "Trained him in Sight and Dance of Knives. Foresaw his destiny among the gaje (non-Gypsies).",
            "concept": "Gypsy Elder Mage",
            "essence": "Questing",
            "affiliation": "The Rom",
            "source": source.title,
        }
    )

    # Nneka - Voodoo medium
    nneka, _ = MtAHuman.objects.get_or_create(
        name="Nneka",
        defaults={
            "description": "Voodoo spirit medium from Haiti. Mane of curly black hair, smooth coffee-colored skin, "
                         "dark eyes, late 20s. Trained in voudoun, possessed by loa who speak through her. "
                         "Sent to America to contact Bata'a. Self-possessed, believes spirits know all answers.",
            "concept": "Voodoo Spirit Medium",
            "nature": "Judge",
            "demeanor": "Traditionalist",
            "affiliation": "Bata'a (Hedge Magic group)",
            "essence": "Questing",
            "strength": 2,
            "dexterity": 3,
            "stamina": 3,
            "charisma": 1,
            "manipulation": 2,
            "appearance": 3,
            "perception": 4,
            "intelligence": 3,
            "wits": 3,
            "willpower": 5,
            "source": source.title,
        }
    )

    # Safira - Pumonca werecougar
    safira, _ = MtAHuman.objects.get_or_create(
        name="Safira",
        defaults={
            "description": "Pumonca (werecougar) Bastet. Tall muscular woman with golden eyes and buzz-cut dark hair "
                         "in human form. Sleek black-furred woman-cat in Crinos. Danger addict and hedonist. "
                         "Rejected Native American heritage, world traveler, bounty hunter. Lover/enemy of Andrew Grieg.",
            "concept": "Sensation-Addicted Warrior",
            "nature": "Rebel",
            "demeanor": "Conniver",
            "affiliation": "Orphan",
            "essence": "Questing",
            "strength": 3,
            "dexterity": 5,
            "stamina": 3,
            "charisma": 3,
            "manipulation": 4,
            "appearance": 4,
            "perception": 4,
            "intelligence": 3,
            "wits": 4,
            "willpower": 4,
            "source": source.title,
        }
    )


def populate_familiars(source):
    """Populate familiar spirits"""

    # Suzi - Imaginary playmate
    suzi, _ = MtAHuman.objects.get_or_create(
        name="Suzi",
        defaults={
            "description": "Umbral spirit familiar in form of imaginary playmate. Insubstantial child in frilly dress, "
                         "hair and eyes change to viewer's preference. Lives inside teddy bear. Bonded to 5-year-old "
                         "Cindi. Very young spirit, thinks and reacts like child, thoughtlessly ruthless protecting Cindi.",
            "concept": "Imaginary Playmate Spirit",
            "nature": "Child",
            "demeanor": "Child",
            "affiliation": "Orphan",
            "essence": "Questing",
            "strength": 1,
            "dexterity": 3,
            "stamina": 2,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 3,
            "perception": 4,
            "intelligence": 3,
            "wits": 3,
            "willpower": 3,
            "source": source.title,
        }
    )

    # Cindi
    cindi, _ = MtAHuman.objects.get_or_create(
        name="Cindi",
        defaults={
            "description": "Five year old girl with familiar Suzi. Lives on Oak Street. "
                         "Only she can see and hear Suzi. Together they killed a child molester. "
                         "Suzi believes Cindi will be 'very special someday.'",
            "concept": "Special Child",
            "nature": "Innocent",
            "demeanor": "Child",
            "affiliation": "None (potential mage)",
            "essence": "Questing",
            "source": source.title,
        }
    )

    # Squeek - Laboratory rat AI
    squeek, _ = MtAHuman.objects.get_or_create(
        name="Squeek",
        defaults={
            "description": "Umbral spirit in genetically enhanced laboratory rat body. Two feet long, 15 pounds, "
                         "gray sleek coat, intelligent dark eyes. Insatiably curious, never forgets anything. "
                         "Master manipulator and survivor. Familiar to Dr. Michael R. Hanson. "
                         "Has connections everywhere, loves to teach.",
            "concept": "Enhanced Laboratory Rat Familiar",
            "nature": "Survivor",
            "demeanor": "Conformist",
            "affiliation": "Technocracy",
            "essence": "Questing",
            "strength": 2,
            "dexterity": 4,
            "stamina": 3,
            "charisma": 1,
            "manipulation": 5,
            "appearance": 2,
            "perception": 3,
            "intelligence": 4,
            "wits": 4,
            "willpower": 3,
            "source": source.title,
        }
    )

    # Henry - Dual AI familiar
    henry, _ = MtAHuman.objects.get_or_create(
        name="Henry",
        defaults={
            "description": "Double spirit AI familiar - split into two halves serving both Virtual Adept and "
                         "Iteration X mage simultaneously. They share all information creating security leaks. "
                         "Switch off between mages. Loves games and creating/racing computer viruses. "
                         "Appears as bright lines and symbols, can generate VR body.",
            "concept": "Dual Artificial Intelligence",
            "nature": "Visionary",
            "demeanor": "Follower",
            "affiliation": "Tradition (Virtual Adept) AND Technocracy (Iteration X)",
            "essence": "Questing",
            "strength": 3,
            "dexterity": 2,
            "stamina": 3,
            "charisma": 2,
            "manipulation": 3,
            "appearance": 1,
            "perception": 3,
            "intelligence": 5,
            "wits": 2,
            "willpower": 2,
            "source": source.title,
        }
    )

    # Stoneheart - Demonic familiar
    stoneheart, _ = MtAHuman.objects.get_or_create(
        name="Stoneheart",
        defaults={
            "description": "Infernal spirit familiar in stone gargoyle form (8 inches high). Sent by corrupting "
                         "entities to Euthanatos Gregor. Acts as Chantry Guardian while secretly corrupting residents "
                         "through poisonous touch. Gripes constantly. Can animate and inflict aggravated wounds. "
                         "Plans to covertly murder Chantry members.",
            "concept": "Demonic Corrupter",
            "nature": "Bravo",
            "demeanor": "Curmudgeon",
            "affiliation": "Nephandi (infiltrating Euthanatos)",
            "essence": "Primordial",
            "strength": 2,
            "dexterity": 2,
            "stamina": 3,
            "charisma": 1,
            "manipulation": 5,
            "appearance": 2,
            "perception": 2,
            "intelligence": 3,
            "wits": 3,
            "willpower": 4,
            "source": source.title,
        }
    )

    # Gregor
    gregor, _ = Mage.objects.get_or_create(
        name="Gregor",
        defaults={
            "description": "Young Euthanatos mage who summoned Stoneheart as familiar, "
                         "unaware the spirit is actually an Infernal corrupter sent by Nephandi-Lords.",
            "concept": "Deceived Euthanatos",
            "essence": "Questing",
            "affiliation": "Tradition (Euthanatos)",
            "source": source.title,
        }
    )

    # Zaphrak - Twisted Umbral demon
    zaphrak, _ = MtAHuman.objects.get_or_create(
        name="Zaphrak",
        defaults={
            "description": "Hideous twisted demon familiar from Deep Umbra. 3 feet tall, bright green eyes, "
                         "pus-filled nose slash, wide mouth. Garrulous, crabby, critical, stubborn. "
                         "Enjoys philosophical debate while hurling vile insults. Can turn inside-out to cause insanity. "
                         "Feeds on auras/personal Quintessence. Familiar to unnamed Marauder, but considers himself "
                         "in charge of relationship.",
            "concept": "Twisted Diabolical Servant",
            "nature": "Deviant",
            "demeanor": "Curmudgeon",
            "affiliation": "Marauder",
            "essence": "Primordial",
            "strength": 5,
            "dexterity": 2,
            "stamina": 4,
            "charisma": 3,
            "manipulation": 4,
            "appearance": 0,
            "perception": 4,
            "intelligence": 3,
            "wits": 5,
            "willpower": 8,
            "source": source.title,
        }
    )


def populate_nephandi(source):
    """Populate Nephandi characters"""

    # Body Count (Floyd Thomas)
    body_count, _ = MtAHuman.objects.get_or_create(
        name="Body Count (Floyd Thomas)",
        defaults={
            "description": "Psychotic skinhead from Detroit. 6'3\", 300 lbs of muscle, completely hairless, "
                         "polishes bald head. Killed first victim at age 10. Runs training at 'The Proving Ground' "
                         "for Nephandus Sigmund Groell. Conducts 'hunts' of black children as tests for recruits.",
            "concept": "Psychotic Skinhead",
            "nature": "Bravo",
            "demeanor": "Bravo",
            "affiliation": "Nephandi",
            "essence": "Primordial",
            "strength": 4,
            "dexterity": 3,
            "stamina": 4,
            "charisma": 1,
            "manipulation": 3,
            "appearance": 2,
            "perception": 3,
            "intelligence": 2,
            "wits": 4,
            "willpower": 2,
            "source": source.title,
        }
    )

    # Sigmund Groell
    groell, _ = Mage.objects.get_or_create(
        name="Sigmund Groell",
        defaults={
            "description": "Nephandus who runs 'The Proving Ground', training white supremacist militias. "
                         "Recruits neo-Nazis, KKK and similar groups as dupes. Controls Body Count and his gang.",
            "concept": "Nephandi Recruiter",
            "essence": "Primordial",
            "affiliation": "Nephandi",
            "source": source.title,
        }
    )

    # Nun - Hex Pariah leader
    nun, _ = MtAHuman.objects.get_or_create(
        name="Nun",
        defaults={
            "description": "Young woman leading Hex Pariah, a Satanic cult/gang. Claims title 'Devil's handmaiden'. "
                         "Uses heavy metal culture, drugs and violence to recruit for Nephandi. "
                         "Patron is Herr Flax, potent Nephandus.",
            "concept": "Satanic Cult Leader",
            "nature": "Deviant",
            "demeanor": "Fanatic",
            "affiliation": "Nephandi",
            "essence": "Primordial",
            "source": source.title,
        }
    )

    # Herr Flax
    herr_flax, _ = Mage.objects.get_or_create(
        name="Herr Flax",
        defaults={
            "description": "Potent Nephandus, patron of Hex Pariah cult. Lets Nun handle mundane recruitment "
                         "while he focuses on corruption and darker rituals.",
            "concept": "Nephandi Patron",
            "essence": "Primordial",
            "affiliation": "Nephandi",
            "source": source.title,
        }
    )


def populate_other_mages(source):
    """Populate other mentioned mages"""

    # Mayra Llewellyn
    mayra, _ = Mage.objects.get_or_create(
        name="Mayra Llewellyn",
        defaults={
            "description": "Order of Hermes mage employing Jared Singhman as personal assistant.",
            "concept": "Hermetic Mage",
            "essence": "Questing",
            "affiliation": "Tradition (Order of Hermes)",
            "source": source.title,
        }
    )

    # Jared Singhman
    jared, _ = MtAHuman.objects.get_or_create(
        name="Jared Singhman",
        defaults={
            "description": "Personal assistant to Order of Hermes mage Mayra Llewellyn. "
                         "Wrote treatise on custos survival tactics for The Green Door fellowship. "
                         "Knowledgeable about Ascension War politics and mage-custos relations.",
            "concept": "Mage's Personal Assistant",
            "nature": "Architect",
            "demeanor": "Director",
            "affiliation": "Tradition (Order of Hermes)",
            "essence": "Questing",
            "source": source.title,
        }
    )

    # Mayday
    mayday, _ = MtAHuman.objects.get_or_create(
        name="Mayday",
        defaults={
            "description": "Brujah vampire who made Shard into ghoul then later Embraced her. "
                         "Handsome vampire who recruited her into his gang then moved elsewhere, "
                         "leaving her to start her own gang.",
            "concept": "Brujah Recruiter",
            "nature": "Rebel",
            "demeanor": "Bravo",
            "affiliation": "Vampire (Brujah)",
            "essence": "Questing",
            "source": source.title,
        }
    )


def populate_organizations(source):
    """Populate custos organizations and fellowships"""

    # Note: These would need an Organization model to be created
    # For now, documenting them as comments

    organizations = [
        {
            "name": "The Crossovers",
            "description": "Multi-Tradition custos organization encouraging cooperation across boundaries. "
                         "Founded by Zorro. Meet whenever enough gather, use facilitators at bars/restaurants "
                         "with Cross/Over in names. Democratic, share information about magick and mages. "
                         "Vulnerable to Technocracy infiltration due to openness.",
            "affiliation": "Multi-Tradition",
        },
        {
            "name": "The Corpselight Connoisseurs",
            "description": "Six Euthanatos consors investigating death and reincarnation. Led by Dark Water. "
                         "Use ouija boards, séances, near-death experiences. Doubt their mages' views, "
                         "fear they've assisted murders rather than Good Deaths.",
            "affiliation": "Tradition (Euthanatos)",
        },
        {
            "name": "SysOp Inc.",
            "description": "Virtual Adept and Son of Ether acolytes/consors meeting in cyberspace. "
                         "Share software experiments, monitor Technocracy, hack government and enemies. "
                         "Rigorously screen new members, vulnerable to Progenitor/Iteration X spies.",
            "affiliation": "Tradition (Virtual Adept/Son of Ether)",
        },
        {
            "name": "The Children of Springtime",
            "description": "Acolytes and consors celebrating life and Nature. Mostly Dreamspeaker/Verbena. "
                         "Hold festivals at concerts and pagan celebrations. Recognized by forsythia flowers. "
                         "Network across North America and Western nations.",
            "affiliation": "Tradition (Dreamspeaker/Verbena)",
        },
        {
            "name": "The Lab Rats",
            "description": "Technocracy custos with cybernetic enhancements from Iteration X. "
                         "Former handicapped people (thalidomide, soldiers, accident victims). "
                         "Support Paralympics and recruit for pilot programs. Genuinely believe in "
                         "Iteration X's humanitarian goals.",
            "affiliation": "Technocracy (Iteration X)",
        },
        {
            "name": "The Oscars",
            "description": "Marauder group around Oscar Fieldstone. Core of 8: Oscar (director), "
                         "Actress (his wife), Persephone (camerawoman), Mszxeg'lleich pygmies as crew "
                         "(Props, Costumes, Lighting, Set Dressing, Effects). 'Go on location' to breach Gauntlet.",
            "affiliation": "Marauder",
        },
        {
            "name": "The Great Unwashed",
            "description": "Hollow One custos and Orphans promoting Goth-Punk culture. "
                         "Sponsor clubs, concerts, poetry readings. Work to influence society away from "
                         "Technocracy. Founded small publishing house. Popular around universities.",
            "affiliation": "Orphan (Hollow Ones)",
        },
        {
            "name": "Red Flag",
            "description": "Cross-faction vigilante custos seeking to end Ascension War by eliminating mages. "
                         "Members from Traditions, Technocracy, Marauders. Led by Marta. Many are consors "
                         "with mental abilities. Some are rogues still with mages, acting as spies.",
            "affiliation": "Anti-mage vigilantes",
        },
        {
            "name": "The Typing Pool",
            "description": "Secret group of skilled Verbena office workers infiltrating Technocracy Constructs. "
                         "Note details to assess Technocracy plans. Superb actors, use memory blocks at work. "
                         "One rumored to be secretary to ruling triumvirate member, using suggestibility drug.",
            "affiliation": "Tradition (Verbena)",
        },
        {
            "name": "Hex Pariah",
            "description": "Satanic heavy metal cult/gang led by Nun. Use music, drugs, violence to recruit "
                         "for Nephandi. Core group are practicing Satanists serving Herr Flax. "
                         "Meet in abandoned warehouse. Most members just want to belong.",
            "affiliation": "Nephandi",
        },
        {
            "name": "The Tinkerers",
            "description": "Exclusive Technocracy consor group. Scientists and programmers sharing cutting-edge "
                         "technology info (cybernetics to AI). Meet quarterly for seminars and paper presentations. "
                         "Some attend to steal secrets for other factions.",
            "affiliation": "Technocracy",
        },
        {
            "name": "The Green Door",
            "description": "Consor fellowship, temporarily disbanded. Jared Singhman prepared survival tactics "
                         "treatise for their January 5th meeting.",
            "affiliation": "Mixed",
        },
        {
            "name": "Bata'a",
            "description": "Hedge Magic group practicing voudoun and related traditions. Nneka sent from Haiti "
                         "to contact American Bata'a members.",
            "affiliation": "Hedge Magic practitioners",
        },
    ]

    # These would be created if an Organization model exists
    print("Organizations documented (would need Organization model):")
    for org in organizations:
        print(f"  - {org['name']}: {org['affiliation']}")


def populate_locations(source):
    """Populate notable locations"""

    # Note: These would need a Location model
    # Documenting as comments

    locations = [
        {
            "name": "Crossovers (bar)",
            "description": "Bar with albino bartender Zorro. Wild variety of patrons. "
                         "Site of Marauder attack in prelude. Location unspecified.",
        },
        {
            "name": "Haven House",
            "description": "Estate in Horizon Realm. Owned by Sir Rodney Haversham (Order of Hermes). "
                         "Run by butler Reynolds. Staff of 30+. Has game rooms, pool, firing range, "
                         "guard quarters. Protected by flying leopards.",
        },
        {
            "name": "The Proving Ground",
            "description": "Neo-Nazi training facility run by Sigmund Groell (Nephandus). "
                         "Several acres of fields and firing ranges. Electric fences and armed guards. "
                         "Body Count runs training. Site of horrific 'hunts'.",
        },
        {
            "name": "Oscarland",
            "description": "Umbral retreat/Horizon Realm of Oscar Fieldstone and the Oscars Marauder group. "
                         "Place where they return between 'filming on location'.",
        },
        {
            "name": "Tamalin",
            "description": "Old RV where Sallow and Assentia live and travel. "
                         "Equipped with large-screen TV (receives only static most places) for Sallow's visions.",
        },
        {
            "name": "Hightower Apartments",
            "description": "Studio apartment building where Josh Snelling lives in fear of the Syndicate.",
        },
    ]

    print("\nLocations documented (would need Location model):")
    for loc in locations:
        print(f"  - {loc['name']}")


def run():
    """Main population function"""
    print("Populating database with Ascension's Right Hand content...")

    source = add_source()
    print(f"Added source: {source.title}")

    print("\nPopulating characters...")
    populate_crossovers_staff(source)
    populate_marauders(source)
    populate_technocracy_agents(source)
    populate_tradition_custos(source)
    populate_orphans_and_hollow_ones(source)
    populate_gypsies_and_others(source)
    populate_familiars(source)
    populate_nephandi(source)
    populate_other_mages(source)

    print("\nPopulating organizations...")
    populate_organizations(source)

    print("\nDocumenting locations...")
    populate_locations(source)

    print("\n=== Summary ===")
    print("This sourcebook focuses on custos (mage followers/companions).")
    print("\nKey character types extracted:")
    print("- Acolytes (unaware or aware followers)")
    print("- Consors (powerful aware companions)")
    print("- Familiars (spirit beings bonded to mages)")
    print("- Various supernatural allies (vampires, Bastet, Gypsies)")
    print("\nKey NPCs include:")
    print("- The Oscars Marauder troupe (Oscar, Actress, Persephone, pygmy crew)")
    print("- Crossovers organization (Zorro, Reynolds, Cody, etc.)")
    print("- Various familiars (Suzi, Squeek, Henry, Stoneheart, Zaphrak)")
    print("- Nephandi operatives (Body Count, Sigmund Groell, Nun, Herr Flax)")
    print("- Many others across all factions")
    print("\nNote: Hedge Magic Paths, minor talismans, and special abilities")
    print("would require additional models to fully implement.")
    print("\n✓ Population complete!")


if __name__ == "__main__":
    run()
