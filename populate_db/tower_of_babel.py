"""
Tower of Babel - A meta-fictional Mage: The Ascension novel
Extracts characters, items, locations, and concepts from the story
where a writer creates a pocket realm and discovers magick
"""

from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from core.models import Book, CharacterTemplate

# Create the book source
book = Book.objects.get_or_create(
    name="Tower of Babel",
    edition="Novel",
    gameline="mta",
)[0]

# ============================================================================
# CHARACTER TEMPLATES
# ============================================================================

# Ron Church - Awakening Reality Deviant/Writer
ron_church = CharacterTemplate.objects.get_or_create(
    name="Ron Church - Awakening Writer",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "A best-selling author who unconsciously creates a pocket realm through his writing, eventually Awakening to his true nature as a reality deviant. Represents the archetype of the creative mage whose art literally shapes reality.",
        "concept": "Author/Reality Deviant",
        "basic_info": {
            "nature": "FK:Archetype:Visionary",
            "demeanor": "FK:Archetype:Loner",
            "concept": "Writer",
            "essence": "FK:Essence:Primordial",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "perception": 4,
            "intelligence": 4,
            "wits": 3,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 2,
            "awareness": 1,  # Awakens during story
            "expression": 4,
            "intimidation": 1,
            "streetwise": 2,
            "computer": 3,
            "drive": 1,
            "academics": 3,
            "cosmology": 1,  # Learns during Awakening
            "enigmas": 2,
            "investigation": 2,
            "linguistics": 1,
        },
        "backgrounds": [
            {
                "name": "Avatar",
                "rating": 5,
            },  # Extremely powerful - creates whole worlds
            {"name": "Resources", "rating": 3},  # Bestselling author
            {"name": "Contacts", "rating": 2},
        ],
        "powers": {
            "mind": 3,  # Creates entire world through thought
            "spirit": 3,  # Creates pocket realm
            "prime": 2,  # Raw creative power
            "time": 1,
            "arete": 2,  # Post-Awakening
        },
        "specialties": [
            "Expression (Fiction Writing)",
            "Academics (Literature)",
            "Computer (Word Processing)",
        ],
        "languages": ["English"],
        "equipment": "Laptop computer, Tower of Babel manuscript disk, gym bag",
        "merits_and_flaws": [
            {"name": "Natural Linguist", "rating": 2, "type": "merit"},
            {"name": "Nightmares", "rating": 1, "type": "flaw"},
        ],
        "notes": "Unconsciously created the pocket realm of Anglia/Anglopolis while writing 'Death on the Tower'. Unified with his character Zorn during Awakening. Hunted by the Technocracy for creating uncontrolled dynamic reality.",
        "suggested_freebie_spending": {
            "arete": 4,
            "sphere": 6,
            "willpower": 2,
            "abilities": 2,
            "backgrounds": 1,
        },
        "is_official": False,
        "is_public": True,
    },
)[0]
ron_church.add_source("Tower of Babel", "Novel")

# Tun Tzu - Akashic Brotherhood Sage
tun_tzu = CharacterTemplate.objects.get_or_create(
    name="Tun Tzu - Akashic Sage",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "An ancient Akashic Brotherhood sage from the pocket realm of Anglia. Master of the tzu-jan (creative essence/Quintessence). Burned out of his home reality and became trapped in Ron Church's mind, serving as a catalyst for Ron's Awakening.",
        "concept": "Wandering Sage",
        "basic_info": {
            "nature": "FK:Archetype:Visionary",
            "demeanor": "FK:Archetype:Traditionalist",
            "concept": "Sage",
            "essence": "FK:Essence:Questing",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 3,
            "stamina": 3,
            "perception": 4,
            "intelligence": 4,
            "wits": 4,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 3,
            "athletics": 2,
            "awareness": 5,
            "brawl": 3,
            "dodge": 3,
            "meditation": 5,
            "stealth": 2,
            "subterfuge": 1,
            "survival": 3,
            "crafts": 2,
            "melee": 2,
            "academics": 3,
            "cosmology": 5,
            "enigmas": 4,
            "investigation": 2,
            "medicine": 3,
            "occult": 4,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 4},
            {"name": "Dream", "rating": 3},
            {"name": "Destiny", "rating": 4},
        ],
        "powers": {
            "mind": 4,
            "spirit": 4,
            "life": 3,
            "prime": 3,
            "time": 2,
            "arete": 5,
        },
        "specialties": [
            "Awareness (Tzu-Jan/Quintessence)",
            "Cosmology (Pocket Realms)",
            "Meditation (Wu Wei)",
            "Enigmas (Paradoxes of Creation)",
        ],
        "languages": ["Ancient dialect", "English (learned)"],
        "equipment": "White and blue robes, bare feet, luira tree seeds",
        "merits_and_flaws": [
            {
                "name": "Burning Avatar",
                "rating": 5,
                "type": "flaw",
            },  # Burned out of home reality
            {"name": "Sphere Natural (Spirit)", "rating": 5, "type": "merit"},
        ],
        "notes": "One of six sages from a bamboo grove in the pocket realm. Attempted to free 'the Zorn' from his paradigm restrictions. Burned out all his Quintessence and was pulled into Ron's world, then into Ron's mind. Served as psychic conductor for Ron's Awakening. Eventually given new story by meta-author John.",
        "suggested_freebie_spending": {
            "arete": 8,
            "sphere": 4,
            "willpower": 2,
            "abilities": 1,
        },
        "is_official": False,
        "is_public": True,
    },
)[0]
tun_tzu.add_source("Tower of Babel", "Novel")

# Max Zorn - The Character Who Becomes Real
max_zorn = CharacterTemplate.objects.get_or_create(
    name="Max Zorn - Fictional Inquisitor",
    gameline="mta",
    defaults={
        "character_type": "mage",  # Actually becomes a mage through unification with Ron
        "description": "Originally a fictional character - an Inquisitor for the Theocracy in the pocket realm of Anglia. Through his creator Ron Church's unconscious magick and his own spiritual questing, Zorn became real and eventually unified with Ron during Ron's Awakening. Represents the mirror/shadow self.",
        "concept": "Inquisitor/Seeker",
        "basic_info": {
            "nature": "FK:Archetype:Judge",
            "demeanor": "FK:Archetype:Fanatic",  # Later shifts to Penitent
            "concept": "Inquisitor",
            "essence": "FK:Essence:Pattern",
        },
        "attributes": {
            "strength": 4,
            "dexterity": 3,
            "stamina": 4,
            "perception": 3,
            "intelligence": 3,
            "wits": 4,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 3,
        },
        "abilities": {
            "alertness": 4,
            "athletics": 3,
            "awareness": 2,  # Develops spiritual awareness
            "brawl": 4,
            "dodge": 3,
            "intimidation": 3,
            "streetwise": 3,
            "subterfuge": 2,
            "drive": 2,
            "firearms": 4,
            "melee": 2,
            "stealth": 3,
            "survival": 2,
            "academics": 2,
            "investigation": 4,
            "law": 3,
            "politics": 2,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 3},  # Latent, awakens through crisis
            {"name": "Destiny", "rating": 5},  # Destined to unify with creator
            {"name": "Resources", "rating": 2},
        ],
        "powers": {
            # Latent abilities that manifest during unification with Ron
            "forces": 2,
            "mind": 2,
            "prime": 1,
            "arete": 1,  # Awakening during story
        },
        "specialties": [
            "Firearms (Benton Automatic)",
            "Investigation (ALF Operations)",
            "Intimidation (Interrogation)",
        ],
        "languages": ["Anglian (English equivalent)"],
        "equipment": "Navy blue Inquisitor uniform, Benton automatic pistol, Department of Orthodoxy badge",
        "merits_and_flaws": [
            {
                "name": "Charmed Existence",
                "rating": 5,
                "type": "merit",
            },  # Survives impossible situations
            {"name": "Nightmares", "rating": 1, "type": "flaw"},
            {
                "name": "Dark Secret",
                "rating": 3,
                "type": "flaw",
            },  # Prays directly to Creator
        ],
        "notes": "Hero of 'Death on the Tower' novel. Defeated terrorist Kroaker atop Anglopolis Tower. Began spiritual quest after trauma, contacted his Creator (Ron) directly, violating Theocratic Orthodoxy. Hunted by Department of Orthodoxy, briefly allied with ALF under Brady Trimmerhorn. Unified with Ron during Ron's Awakening, becoming one being across two realities.",
        "suggested_freebie_spending": {
            "attributes": 5,
            "abilities": 5,
            "willpower": 3,
            "backgrounds": 2,
        },
        "is_official": False,
        "is_public": True,
    },
)[0]
max_zorn.add_source("Tower of Babel", "Novel")

# Irene - Technocracy Agent Template
irene_agent = CharacterTemplate.objects.get_or_create(
    name="Irene - NWO Operative (Deep Cover)",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "A New World Order operative embedded as a construction loan servicer. Expert in surveillance, manipulation, and conspiracy theories (used as cover). Assigned to monitor and ultimately eliminate reality deviant Ron Church. Represents the tragedy of the Technocracy's human cost.",
        "concept": "Deep Cover Agent",
        "basic_info": {
            "nature": "FK:Archetype:Survivor",
            "demeanor": "FK:Archetype:Caregiver",  # Cover identity
            "concept": "Banker/Spy",
            "essence": "FK:Essence:Pattern",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 3,
            "stamina": 3,
            "perception": 4,
            "intelligence": 4,
            "wits": 3,
            "charisma": 3,
            "manipulation": 4,
            "appearance": 3,
        },
        "abilities": {
            "alertness": 3,
            "awareness": 2,
            "expression": 2,
            "intimidation": 2,
            "streetwise": 2,
            "subterfuge": 4,
            "computer": 4,
            "drive": 2,
            "firearms": 3,
            "technology": 3,
            "academics": 3,
            "enigmas": 3,  # Ironic - uses conspiracy theories as cover
            "finance": 4,
            "investigation": 3,
            "law": 2,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 2},
            {"name": "Backup", "rating": 3},  # Technocracy support
            {"name": "Resources", "rating": 3},
            {"name": "Spies", "rating": 2},
        ],
        "powers": {
            "correspondence": 2,
            "mind": 3,
            "forces": 1,
            "arete": 2,
        },
        "specialties": [
            "Computer (Hacking/Surveillance)",
            "Subterfuge (Long-term Cover)",
            "Finance (Money Laundering)",
            "Enigmas (Conspiracy Theories - Cover)",
        ],
        "languages": ["English", "Technical Jargon"],
        "equipment": "Dream scanner, snub-nosed .38 revolver, encrypted smartphone, banking access codes, mild tranquilizers",
        "merits_and_flaws": [
            {"name": "Natural Linguist", "rating": 2, "type": "merit"},
            {
                "name": "Deep Sleeper",
                "rating": 1,
                "type": "flaw",
            },  # Technocracy conditioning
        ],
        "notes": "Posed as Ron Church's girlfriend while monitoring his unconscious creation of a pocket realm. Used elaborate cover including spouting conspiracy theories. Ultimately tried to kill Ron mercifully rather than let Technocracy vivisect him. Killed by Ron's Awakening backlash.",
        "suggested_freebie_spending": {
            "abilities": 5,
            "backgrounds": 4,
            "willpower": 3,
            "sphere": 3,
        },
        "is_official": False,
        "is_public": True,
    },
)[0]
irene_agent.add_source("Tower of Babel", "Novel")

# Brady Trimmerhorn - Legendary ALF Founder
trimmerhorn = CharacterTemplate.objects.get_or_create(
    name="Brady Trimmerhorn - ALF Founder",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",  # In the pocket realm, not a mage in our sense
        "description": "Legendary Inquisitor who created the Anglian Liberation Front as manufactured opposition to the Theocracy, then actually turned it into real resistance. Disappeared 20 years ago, presumed dead. Actually living as ALF leader. Represents the revolutionary who becomes what he opposed.",
        "concept": "Revolutionary Leader",
        "basic_info": {
            "nature": "FK:Archetype:Rebel",
            "demeanor": "FK:Archetype:Director",
            "concept": "Revolutionary",
        },
        "attributes": {
            "strength": 3,
            "dexterity": 3,
            "stamina": 3,
            "perception": 4,
            "intelligence": 4,
            "wits": 4,
            "charisma": 4,
            "manipulation": 4,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 4,
            "athletics": 2,
            "brawl": 3,
            "dodge": 3,
            "empathy": 3,
            "expression": 3,
            "intimidation": 4,
            "leadership": 5,
            "streetwise": 4,
            "subterfuge": 4,
            "firearms": 4,
            "security": 3,
            "stealth": 3,
            "academics": 3,
            "investigation": 4,
            "law": 3,
            "politics": 4,
        },
        "backgrounds": [
            {"name": "Allies", "rating": 4},
            {"name": "Contacts", "rating": 5},
            {"name": "Resources", "rating": 3},
        ],
        "specialties": [
            "Leadership (Insurgency)",
            "Subterfuge (Manufacturing Evidence)",
            "Politics (Revolutionary Tactics)",
        ],
        "languages": ["Anglian"],
        "equipment": "Various weapons, fake identities, ALF command structure",
        "notes": "Created the ALF as fake opposition while an Inquisitor, then turned it real. Disappeared after 'kidnapping'. Long angular face, sharp nose, gray-brown eyes. Commands absolute loyalty. Killed in Theocracy raid on ALF hideout triggered by Alverston's betrayal.",
        "suggested_freebie_spending": {
            "abilities": 5,
            "attributes": 5,
            "backgrounds": 5,
        },
        "is_official": False,
        "is_public": True,
    },
)[0]
trimmerhorn.add_source("Tower of Babel", "Novel")

# Shantei - Akashic Brotherhood Contact
shantei = CharacterTemplate.objects.get_or_create(
    name="Shantei - Akashic Brother (San Francisco)",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "Young Akashic Brotherhood mage in San Francisco. Well-groomed, neatly dressed. Part of the group that contacted Ron Church after his Awakening to help him understand his abilities and protect him from the Technocracy.",
        "concept": "Akashic Recruiter",
        "basic_info": {
            "nature": "FK:Archetype:Caregiver",
            "demeanor": "FK:Archetype:Pedagogue",
            "concept": "Teacher",
            "essence": "FK:Essence:Questing",
        },
        "attributes": {
            "strength": 3,
            "dexterity": 4,
            "stamina": 3,
            "perception": 3,
            "intelligence": 3,
            "wits": 4,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 3,
        },
        "abilities": {
            "alertness": 3,
            "athletics": 3,
            "awareness": 4,
            "brawl": 3,
            "dodge": 3,
            "empathy": 2,
            "expression": 2,
            "meditation": 3,
            "stealth": 2,
            "academics": 2,
            "cosmology": 3,
            "enigmas": 2,
            "medicine": 2,
            "occult": 3,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 3},
            {"name": "Allies", "rating": 2},
            {"name": "Contacts", "rating": 2},
        ],
        "powers": {
            "life": 2,
            "mind": 2,
            "spirit": 1,
            "arete": 2,
        },
        "specialties": [
            "Awareness (Dynamic Reality)",
            "Cosmology (Pocket Realms)",
        ],
        "languages": ["English", "Cantonese"],
        "equipment": "Business casual attire, smartphone",
        "notes": "Part of San Francisco Akashic Brotherhood. Helped Ron Church after his Awakening. Set up Apocalyptic Press to publish Tower of Babel.",
        "suggested_freebie_spending": {
            "arete": 4,
            "sphere": 3,
            "willpower": 4,
            "abilities": 4,
        },
        "is_official": False,
        "is_public": True,
    },
)[0]
shantei.add_source("Tower of Babel", "Novel")

# Jim Woo - Second Akashic Contact
jim_woo = CharacterTemplate.objects.get_or_create(
    name="Jim Woo - Akashic Brother (San Francisco)",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "Young Akashic Brotherhood mage in San Francisco. Well-groomed, neatly dressed. Partner to Shantei in contacting and training newly Awakened mages, particularly reality deviants.",
        "concept": "Akashic Recruiter",
        "basic_info": {
            "nature": "FK:Archetype:Visionary",
            "demeanor": "FK:Archetype:Confidant",
            "concept": "Recruiter",
            "essence": "FK:Essence:Questing",
        },
        "attributes": {
            "strength": 3,
            "dexterity": 3,
            "stamina": 3,
            "perception": 4,
            "intelligence": 3,
            "wits": 3,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 3,
        },
        "abilities": {
            "alertness": 3,
            "athletics": 2,
            "awareness": 3,
            "brawl": 2,
            "dodge": 2,
            "empathy": 3,
            "expression": 2,
            "meditation": 3,
            "streetwise": 2,
            "academics": 3,
            "computer": 2,
            "cosmology": 3,
            "investigation": 2,
            "occult": 3,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 3},
            {"name": "Allies", "rating": 3},
            {"name": "Resources", "rating": 2},
        ],
        "powers": {
            "mind": 2,
            "spirit": 2,
            "prime": 1,
            "arete": 2,
        },
        "specialties": [
            "Cosmology (Umbral Realms)",
            "Empathy (Awakening Mages)",
        ],
        "languages": ["English", "Mandarin"],
        "equipment": "Business attire, smartphone",
        "notes": "Worked with Shantei to help Ron Church understand his abilities. Part of the corporate-model mage group in San Francisco fighting the Technocracy.",
        "suggested_freebie_spending": {
            "arete": 4,
            "sphere": 3,
            "willpower": 3,
            "backgrounds": 3,
            "abilities": 2,
        },
        "is_official": False,
        "is_public": True,
    },
)[0]
jim_woo.add_source("Tower of Babel", "Novel")

# ============================================================================
# SUPPORTING CHARACTERS (Brief templates)
# ============================================================================

# Jarvis - Zorn's Assistant (Victim)
jarvis = CharacterTemplate.objects.get_or_create(
    name="Jarvis - Young Inquisitor Assistant",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",
        "description": "Eager young assistant to Inquisitor Zorn. Recently graduated top of indoctrination class. Killed by ALF bomb meant for Zorn.",
        "concept": "Loyal Assistant",
        "basic_info": {
            "nature": "FK:Archetype:Gallant",
            "demeanor": "FK:Archetype:Conformist",
            "concept": "Assistant",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "perception": 3,
            "intelligence": 3,
            "wits": 2,
            "charisma": 2,
            "manipulation": 2,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 2,
            "academics": 3,
            "computer": 3,
            "investigation": 2,
            "law": 2,
        },
        "backgrounds": [],
        "notes": "Almost 20 years old. Wire-rim glasses. Eager to please. Killed in bombing at DO office. His death catalyzed Zorn's spiritual crisis.",
        "is_official": False,
        "is_public": True,
    },
)[0]
jarvis.add_source("Tower of Babel", "Novel")

# Marlin Jaquobs/Toano - Double Agent
jaquobs = CharacterTemplate.objects.get_or_create(
    name="Marlin Jaquobs (Toano) - ALF Mole",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",
        "description": "Thin, rat-like Inquisitor who is secretly ALF operative 'Toano'. Blinks rapidly. Married with children. Tried to help Zorn but killed in Theocracy raid on ALF hideout.",
        "concept": "Double Agent",
        "basic_info": {
            "nature": "FK:Archetype:Survivor",
            "demeanor": "FK:Archetype:Conformist",
            "concept": "Mole",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 3,
            "stamina": 2,
            "perception": 3,
            "intelligence": 3,
            "wits": 4,
            "charisma": 2,
            "manipulation": 4,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 3,
            "subterfuge": 4,
            "firearms": 3,
            "investigation": 3,
            "law": 2,
        },
        "backgrounds": [
            {"name": "Allies", "rating": 3},
            {"name": "Contacts", "rating": 3},
        ],
        "notes": "Created fake informants (Alfonse, Desmond, Maria) to set up Zorn. Actually trying to recruit Zorn for ALF. Wife Brenda/Beverly, children. Killed in raid.",
        "is_official": False,
        "is_public": True,
    },
)[0]
jaquobs.add_source("Tower of Babel", "Novel")

# Lorraine Darnell/Alfonse - ALF Informant
lorraine = CharacterTemplate.objects.get_or_create(
    name="Lorraine Darnell (Alfonse) - ALF Informant",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",
        "description": "Waitress at Evander's pub, about 40 years old. Sharp features, shoulder-length brunette hair. ALF informant codenamed 'Alfonse'. Mother of Alverston (14). Killed in Theocracy raid.",
        "concept": "Working Class Informant",
        "basic_info": {
            "nature": "FK:Archetype:Survivor",
            "demeanor": "FK:Archetype:Caregiver",
            "concept": "Waitress/Spy",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 3,
            "stamina": 3,
            "perception": 3,
            "intelligence": 2,
            "wits": 3,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 3,
            "empathy": 2,
            "streetwise": 3,
            "subterfuge": 3,
        },
        "backgrounds": [
            {"name": "Contacts", "rating": 2},
        ],
        "notes": "Single mother, works at Evander's. Son Alverston (14) didn't know about her ALF connections. Tried to help Zorn. Killed when Alverston betrayed location to Theocracy.",
        "is_official": False,
        "is_public": True,
    },
)[0]
lorraine.add_source("Tower of Babel", "Novel")

# The Theocrat - Mysterious Ruler
theocrat = CharacterTemplate.objects.get_or_create(
    name="The Theocrat - Ruler of Anglia",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",  # Or possibly something more
        "description": "Supreme ruler of the Theocracy. Female, thin as iron rod, severely short auburn hair, fierce blue eyes, small nose and mouth. Wears purple velvet cape, tunic, black boots to knees. Terrifyingly powerful presence. Killed by Zorn's Awakening backlash.",
        "concept": "Absolute Ruler",
        "basic_info": {
            "nature": "FK:Archetype:Autocrat",
            "demeanor": "FK:Archetype:Judge",
            "concept": "Theocrat",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 3,
            "stamina": 3,
            "perception": 4,
            "intelligence": 4,
            "wits": 4,
            "charisma": 5,
            "manipulation": 5,
            "appearance": 3,
        },
        "abilities": {
            "intimidation": 5,
            "leadership": 5,
            "expression": 4,
            "subterfuge": 4,
            "politics": 5,
            "law": 5,
        },
        "backgrounds": [
            {"name": "Resources", "rating": 5},
            {"name": "Retainers", "rating": 5},
        ],
        "notes": "Supreme authority in Anglia. Completely emotionless, mechanical. Eyes described as 'predatory, hypnotic'. Familiarity to Ron Church suggests possible connection to Irene. Executed Zorn personally.",
        "is_official": False,
        "is_public": True,
    },
)[0]
theocrat.add_source("Tower of Babel", "Novel")

# ============================================================================
# MINOR CHARACTERS
# ============================================================================

# Ed Rollins - Traitor Inquisitor
rollins = CharacterTemplate.objects.get_or_create(
    name="Ed Rollins - Corrupt Inquisitor",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",
        "description": "Shorter than Zorn, more muscular. Brown hair, friendly smile. Warned Zorn about department politics, then betrayed him. Part of conspiracy at highest levels.",
        "concept": "Friendly Traitor",
        "basic_info": {
            "nature": "FK:Archetype:Conniver",
            "demeanor": "FK:Archetype:Gallant",
        },
        "notes": "Attempted to recruit Zorn, then set trap at Evander's. Present at Zorn's torture and execution.",
        "is_official": False,
        "is_public": True,
    },
)[0]
rollins.add_source("Tower of Babel", "Novel")

# Andre - Sadistic Inquisitor
andre = CharacterTemplate.objects.get_or_create(
    name="Andre - Sadistic Inquisitor",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",
        "description": "Young red-haired Inquisitor. Takes pleasure in torture and interrogation. Enthusiastically exceeded standard procedures on Zorn.",
        "concept": "Sadist",
        "basic_info": {
            "nature": "FK:Archetype:Monster",
            "demeanor": "FK:Archetype:Bravo",
        },
        "notes": "Killed by Zorn's Awakening power - crushed by animated straps.",
        "is_official": False,
        "is_public": True,
    },
)[0]
andre.add_source("Tower of Babel", "Novel")

# Kroaker - ALF Terrorist
kroaker = CharacterTemplate.objects.get_or_create(
    name="Kroaker - ALF Fanatic",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",
        "description": "Extremely tall ALF terrorist. Oversized hands and feet. Wildly frazzled hair. Bloodshot eyes glazed from drugs. Took 43 hostages atop Anglopolis Tower. Killed by Zorn.",
        "concept": "Terrorist",
        "basic_info": {
            "nature": "FK:Archetype:Fanatic",
            "demeanor": "FK:Archetype:Monster",
        },
        "notes": "Defeated by Zorn in 'Death on the Tower'. Strapped with explosives. Zorn's first major victory that made him famous.",
        "is_official": False,
        "is_public": True,
    },
)[0]
kroaker.add_source("Tower of Babel", "Novel")

# Dana Norris - Innocent Victim
dana_norris = CharacterTemplate.objects.get_or_create(
    name="Dana Norris - False Accusation Victim",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",
        "description": "Indoctrination instructor. Model citizen, never even a parking ticket. Member of Young Anglians for Freedom (YAF). Falsely accused of ALF connections by manufactured evidence. Imprisoned and tortured.",
        "concept": "Innocent",
        "basic_info": {
            "nature": "FK:Archetype:Caregiver",
            "demeanor": "FK:Archetype:Pedagogue",
        },
        "notes": "Her false arrest catalyzed Zorn's crisis of faith in the Theocracy. Represents the innocents crushed by the system.",
        "is_official": False,
        "is_public": True,
    },
)[0]
dana_norris.add_source("Tower of Babel", "Novel")

# Men in Black - NWO Operatives
mib = CharacterTemplate.objects.get_or_create(
    name="Men in Black - NWO Enforcers",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "Wide, towering Technocracy enforcers. Completely dressed in black - jackets, shirts, ties, pants, shoes, sunglasses. Carry black briefcases. Preternatural speed. Expression of frozen snarl. Super-powered thugs of the New World Order.",
        "concept": "Enforcer",
        "basic_info": {
            "nature": "FK:Archetype:Bravo",
            "demeanor": "FK:Archetype:Monster",
        },
        "attributes": {
            "strength": 5,
            "dexterity": 4,
            "stamina": 5,
        },
        "powers": {
            "forces": 3,
            "matter": 2,
            "life": 2,
            "arete": 3,
        },
        "notes": "Sent to capture/kill Ron Church. One exploded by Ron's power, one smashed through shower wall. Represent Technocracy's brutal efficiency.",
        "is_official": False,
        "is_public": True,
    },
)[0]
mib.add_source("Tower of Babel", "Novel")

# Nathaniel Early - Ron's Agent
nate = CharacterTemplate.objects.get_or_create(
    name="Nathaniel 'Nate' Early - Literary Agent",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",
        "description": "Ron Church's literary agent. Handsome black man. Professional, competent. Murdered by Technocracy as part of frame job against Ron.",
        "concept": "Agent",
        "basic_info": {
            "nature": "FK:Archetype:Competitor",
            "demeanor": "FK:Archetype:Gallant",
        },
        "notes": "Couldn't sell Tower of Babel to any publisher (Technocracy interference). Shot several times in his Marin County home. Ron was accused.",
        "is_official": False,
        "is_public": True,
    },
)[0]
nate.add_source("Tower of Babel", "Novel")

# Benjamin Hardy - Ron's Accountant
hardy = CharacterTemplate.objects.get_or_create(
    name="Benjamin Hardy - Accountant",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",
        "description": "Ron Church's accountant. Disappeared with $250,000 of Ron's money. Part of Technocracy operation to destroy Ron's life and credibility.",
        "concept": "Embezzler (Technocracy Pawn)",
        "basic_info": {
            "nature": "FK:Archetype:Survivor",
            "demeanor": "FK:Archetype:Conformist",
        },
        "notes": "Vanished, closed all accounts. May have been Technocracy agent or coerced/controlled.",
        "is_official": False,
        "is_public": True,
    },
)[0]
hardy.add_source("Tower of Babel", "Novel")

# Detective Ward - Technocracy Police
ward = CharacterTemplate.objects.get_or_create(
    name="Detective Ward - Technocracy Operative",
    gameline="mta",
    defaults={
        "character_type": "mtahuman",
        "description": "Average-looking detective investigating Ron Church. So average in appearance he could blend into a crowd as only person in room. Part of Technocracy operation. Partner to Detective Stowe.",
        "concept": "Detective",
        "basic_info": {
            "nature": "FK:Archetype:Survivor",
            "demeanor": "FK:Archetype:Conformist",
        },
        "notes": "Worked with Technocracy to frame Ron for Nate's murder. Deliberately unremarkable appearance.",
        "is_official": False,
        "is_public": True,
    },
)[0]
ward.add_source("Tower of Babel", "Novel")

# Meta-Character John - The Author of the Author
john_meta = CharacterTemplate.objects.get_or_create(
    name="John - The Meta-Author",
    gameline="mta",
    defaults={
        "character_type": "mage",  # Or something beyond
        "description": "The author writing about Ron Church writing about Zorn. Light brown hair in ponytail, kind angular face. Wears jeans and sweaters. Lives in bamboo tower in Ron's mind. Represents the infinite regress of creation. May himself be a character in yet another story.",
        "concept": "Creator of Creators",
        "basic_info": {
            "nature": "FK:Archetype:Architect",
            "demeanor": "FK:Archetype:Visionary",
        },
        "notes": "Pulled Tun Tzu into his narrative. Can't fully control Ron, just as Ron can't control Zorn. Aware of the frames within frames. Uses a Mac, not an IBM. Has a cold at end of book. Friend Jens tells German beer jokes.",
        "is_official": False,
        "is_public": True,
    },
)[0]
john_meta.add_source("Tower of Babel", "Novel")

print("Tower of Babel character templates created successfully!")

# ============================================================================
# ORGANIZATIONS & FACTIONS
# ============================================================================

print("\nNote: Organizations would typically be created in a separate system.")
print("Key organizations from Tower of Babel:")
print("- Akashic Brotherhood (San Francisco chapter)")
print("- Technocracy")
print("  - New World Order (Irene, Men in Black, Det. Ward)")
print("  - Syndicate (financial manipulation)")
print("- Department of Orthodoxy (fictional Anglia)")
print("- Anglian Liberation Front / ALF (pocket realm)")
print("- Theocracy of Anglia (pocket realm government)")
print("- Apocalyptic Press (Akashic Brotherhood front company)")

# ============================================================================
# ITEMS, ARTIFACTS, AND WONDERS
# ============================================================================

print("\nKey Items from Tower of Babel:")
print("- Luira Tree (magical plant from pocket realm)")
print("  * Berries reveal truth about reality")
print("  * Grown by Tun Tzu in San Francisco grove")
print("  * Seeds can be carried between worlds")
print("  * Fruit causes visions of creator's world")
print("- Book of Orthodoxy (Theocracy religious text)")
print("- Death on the Tower (Ron's first novel)")
print("- Tower of Babel manuscript disk")
print("- Dream Scanner (Technocracy device)")
print("  * Green blinking light")
print("  * Monitors dreams/mental states")
print("- Benton Automatic Pistol (DO standard issue)")
print("- Men in Black briefcases (unknown contents)")

# ============================================================================
# ROTES AND EFFECTS
# ============================================================================

print("\nKey Magickal Effects from Tower of Babel:")
print("\n1. Pocket Realm Creation (Ron Church)")
print("   Spheres: Spirit 4, Mind 4, Prime 3, Time 2")
print("   Effect: Unconsciously created entire world of Anglia/Anglopolis")
print("   while writing fiction. World became self-sustaining.")
print("\n2. Dream Communication (Ron/Zorn/Tun Tzu)")
print("   Spheres: Mind 3, Spirit 2")
print("   Effect: Communication across realities through dreams.")
print("\n3. Astral Projection (Tun Tzu)")
print("   Spheres: Spirit 3, Mind 2")
print("   Effect: Project consciousness to find and contact the Zorn.")
print("\n4. Mind-Link/Telepathy (Tun Tzu)")
print("   Spheres: Mind 3")
print("   Effect: Direct thought communication, planting knowledge.")
print("\n5. Awakening Backlash (Ron's Awakening)")
print("   Spheres: Prime 4, Forces 3, Mind 3, Life 2")
print("   Effect: Uncontrolled release destroying enemies:")
print("   - Exploded Man in Black")
print("   - Killed Irene (bleeding from eyes/ears, skin cracked)")
print("   - Killed the Theocrat (in pocket realm)")
print("   - Animated straps to kill Andre and others")
print("\n6. Reality Manipulation (Ron post-Awakening)")
print("   Spheres: Forces 2, Matter 2, Prime 2")
print("   Effect: Threw Man in Black through bathroom wall")
print("   without touching him, exploded another.")
print("\n7. Quintessence Sense (Tun Tzu)")
print("   Spheres: Prime 2, Spirit 1")
print("   Effect: Sense the tzu-jan (creative essence/Quintessence)")
print("   flowing through beings and objects.")
print("\n8. Unification of Creator/Created (Ron/Zorn)")
print("   Spheres: Mind 5, Spirit 5, Prime 4, Time 3")
print("   Effect: Merged Ron and Zorn into unified being across")
print("   two realities. Ron embraced his shadow-self.")

# ============================================================================
# LOCATIONS
# ============================================================================

print("\nKey Locations from Tower of Babel:")
print("\nPocket Realm (Anglia):")
print("- Anglopolis - Massive city, sparkling steel and glass")
print("- Anglopolis Tower - Skyscraper, site of Kroaker battle")
print("- Department of Orthodoxy Complex - Government building")
print("  * 50+ floors")
print("  * Zorn's office on 18th floor")
print("  * Senior Inquisitor Martin's office on 27th floor")
print("  * Holding cells in deep sub-levels")
print("  * Theocrat's chamber at very top")
print("- True Way Books - Bookstore, suspected ALF front")
print("- Evander's Pub - Where trap was set for Zorn")
print("- ALF Hideout - Warehouse complex with underground levels")
print("  * Near docks, between 32nd and 44th Streets")
print("  * Underground conference rooms")
print("  * Multiple escape routes")
print("- Bamboo Grove (Tun Tzu's original home)")
print("  * Luira trees")
print("  * Frog pond")
print("  * Six sages lived here")
print("\nReal World (San Francisco):")
print("- Ron's Apartment - Sutter Street, Nob Hill")
print("- Eddy's Corner Pub - Where Tun Tzu first contacted Ron")
print("- Golden Gate Park - Japanese Tea Garden")
print("  * Hidden grove where Ron ate luira berries")
print("  * Frog pond surrounded by stones")
print("- Bayside First Mutual Bank - Where Irene worked")
print("- The Underground News Merchant Bookstore")
print("- The Waterfront Restaurant - Pier Seven")
print("- Starlight Lounge and Motor Lodge - Purple trim, where Ron Awakened")
print("- Nate Early's house - Marin County (murder scene)")
print("\nMental/Astral Realms:")
print("- Ron's Mind - Bamboo grove, tower, storm")
print("- The Tower (Zorn's mental construct)")
print("  * Stone tower built to reach Creator")
print("  * Destroyed by storm during crisis")
print("- Tun Tzu's Grove (in Ron's mind)")
print("  * Bamboo tower where he met John")
print("  * Created by John for Tun Tzu's comfort")

# ============================================================================
# CONCEPTS AND THEMES
# ============================================================================

print("\nKey Themes and Concepts:")
print("- Meta-fiction and multiple layers of reality")
print("- Creator/Created relationship and responsibility")
print("- Awakening through crisis and unity")
print("- Pocket realms/Horizon realms")
print("- Consensus reality vs. dynamic reality")
print("- Technocracy's enforcement of stasis")
print("- Characters gaining independence from creators")
print("- The tzu-jan (creative essence of the Tao/Quintessence)")
print("- Wu wei (actionless action)")
print("- Paradigm restrictions and breaking free")
print("- Mirror selves and shadow integration")
print("- The cost of revolution and resistance")
print("- Betrayal and loyalty in oppressive systems")

# ============================================================================
# MERITS AND FLAWS (Unique)
# ============================================================================

print("\nUnique Merits/Flaws introduced:")
print("- Burning Avatar (5pt Flaw) - Burned out of home reality,")
print("  pulled into another world. Tun Tzu suffered this.")
print("- Fictional Character (Variable) - Literally a character")
print("  from fiction made real. Zorn experienced this.")
print("- Creator's Favorite (5pt Merit) - As protagonist, survive")
print("  impossible situations. Zorn had this until Ron lost control.")

print("\n" + "=" * 70)
print("Tower of Babel extraction complete!")
print("=" * 70)
print("\nThis meta-fictional novel explores Mage: The Ascension themes of:")
print("- Consensus vs. dynamic reality")
print("- The Technocracy's control through stasis")
print("- Awakening and paradigm-breaking")
print("- Creation of pocket realms")
print("- The relationship between creator and created")
print("\nThe book itself would make an excellent sourcebook for chronicles")
print("involving reality deviants, pocket realms, and the philosophical")
print("implications of magick and creation.")
