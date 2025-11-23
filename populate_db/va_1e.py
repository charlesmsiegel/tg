"""
Virtual Adepts 1st Edition (1994)
Game objects extracted from the Virtual Adepts sourcebook
"""

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Practice
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.rote import Rote
from core.models import Book, CharacterTemplate
from items.models.mage.talisman import Talisman
from items.models.mage.wonder import Wonder

# ===== BOOK =====
book, _ = Book.objects.get_or_create(
    name="Virtual Adepts (1st Edition)",
    edition="1e",
    gameline="mta",
)

# ===== FACTIONS/LEGIONS =====

cyberpunks, _ = MageFaction.objects.get_or_create(
    name="Cyberpunks",
    parent=MageFaction.objects.get(name="Virtual Adepts"),
)
cyberpunks.description = (
    "Typically free-for-all mercenaries, burning out on drugs and choline enhancers while coding rotes all night. "
    "Flashy and vulgar in their magick, preferring raw power over subtlety. They use Force, Matter and Correspondence "
    "magick extensively and don't fear Paradox - many even seek it out to transform themselves."
)
cyberpunks.save()

cypherpunks, _ = MageFaction.objects.get_or_create(
    name="Cypherpunks",
    parent=MageFaction.objects.get(name="Virtual Adepts"),
)
cypherpunks.description = (
    "An offshoot of the Cyberpunks focused on protection and information-gathering rather than mayhem. "
    "They develop encryption codes and security systems beyond anything the NSA has seen. More subtle than Cyberpunks, "
    "preferring Mind and Matter magick. They encrypt their thoughts and data obsessively."
)
cypherpunks.save()

chaoticians, _ = MageFaction.objects.get_or_create(
    name="Chaoticians",
    parent=MageFaction.objects.get(name="Virtual Adepts"),
)
chaoticians.description = (
    "Cold and calculating scientists who believe information is too complex to manipulate directly and must be "
    "controlled through probabilities. Masters of Entropy and chaos theory, they view the coming Ascension as the "
    "embodiment of chaos theory - when any system becomes too complex, it breaks down. They excel at coincidental magick."
)
chaoticians.save()

reality_hackers, _ = MageFaction.objects.get_or_create(
    name="Reality Hackers",
    parent=MageFaction.objects.get(name="Virtual Adepts"),
)
reality_hackers.description = (
    "The newest and most unique faction. Unlike other Adepts, Reality Hackers have little interest in the Digital Web. "
    "Instead, they hack the universe itself, seeing it as the most intricate network ever created. They specialize in "
    "'life hacking' - reprogramming people's brains and bodies using genetic material, and 'dream hacking' - walking "
    "and manipulating others' dreams."
)
reality_hackers.save()

lab_rats, _ = MageFaction.objects.get_or_create(
    name="Lab Rats",
    parent=MageFaction.objects.get(name="Virtual Adepts"),
)
lab_rats.description = (
    "A group of Virtual Adepts who were born and bred by the Progenitors. They escaped Technocracy control and "
    "now help rescue other children earmarked for the Technocracy. Led by Dance (Desmond Collingsworth), they "
    "strike at the Technocracy by stealing their ammunition - children."
)
lab_rats.save()

# ===== EFFECTS =====

effect_encrypt_thoughts, _ = Effect.objects.get_or_create(
    name="Encrypt Thoughts",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=1,
    prime=2,
)
effect_encrypt_thoughts.description = (
    "This effect protects the mage's thoughts from prying minds by encrypting them. The mage sets a mental 'password' "
    "or key that others must think of to read their mind. Only those who know the key can bypass the encryption. "
    "Each success subtracts two successes from outside attempts to read the Adept's mind, beyond normal countermagick."
)
effect_encrypt_thoughts.add_source("Virtual Adepts (1st Edition)", 61)

effect_degrade_order, _ = Effect.objects.get_or_create(
    name="Degrade Order",
    correspondence=2,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)
effect_degrade_order.description = (
    "This effect accelerates the decay of complex systems by adding Entropy and accelerating Time. A flower might "
    "wither and die in thirty seconds, or a complex machine might rust and fall apart. The effect compresses a "
    "system's relative lifespan into seconds. Correspondence keeps the field effect away from the mage. "
    "Difficulty varies based on size, complexity, and distance: a flower is difficulty 5, a person is 9-10."
)
effect_degrade_order.add_source("Virtual Adepts (1st Edition)", 61)

effect_information_glut, _ = Effect.objects.get_or_create(
    name="Information Glut",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)
effect_information_glut.description = (
    "This effect enhances any one sense, allowing the mage to 'turn up the volume' and perceive things normally "
    "imperceptible. It can provide night vision, enhanced hearing, or accelerated comprehension of sensory input. "
    "Virtual Adepts use it to enhance computer comprehension. The Technocracy uses it as an instrument of torture, "
    "as it affects the mind rather than the body. Each success gives +1 Perception for a scene. With Life 4, "
    "the effect can be made permanent ('hardwiring')."
)
effect_information_glut.add_source("Virtual Adepts (1st Edition)", 62)

effect_holographic_projector, _ = Effect.objects.get_or_create(
    name="Holographic Projector",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=3,
    prime=2,
)
effect_holographic_projector.description = (
    "The Adept projects a hologram (or icon) of themselves wherever they desire. The hologram is made of light patterns, "
    "and Mind magick fools viewers into perceiving smell and other sensory data. The hologram cannot touch or affect "
    "reality, nor can it be harmed. A variant using Correspondence 3 and Forces 2 creates an icon using the mage's "
    "Avatar - this icon can affect reality, but the mage's body remains helpless and takes any damage the icon suffers."
)
effect_holographic_projector.add_source("Virtual Adepts (1st Edition)", 62)

effect_social_engineering, _ = Effect.objects.get_or_create(
    name="Social Engineering",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)
effect_social_engineering.description = (
    "A subtle form of manipulation that lets the Adept convince opponents they are someone else or make themselves "
    "vanish into a crowd. In extreme cases, it can fool pursuers into thinking the Adept isn't really there. "
    "Requires Mind 2 and Subterfuge skill. Difficulty is usually 8, but may be decreased if the Adept is especially "
    "clever or if the subject is elsewhere (on telephone or computer lines)."
)
effect_social_engineering.add_source("Virtual Adepts (1st Edition)", 63)

effect_life_hacking, _ = Effect.objects.get_or_create(
    name="Life Hacking",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=4,
    prime=3,
)
effect_life_hacking.description = (
    "A secret and dangerous Reality Hacker rote that allows reprogramming of a person's brain and body using genetic "
    "material. The mage can reprogram a body to produce hallucinogenic compounds or deadly toxins spontaneously. "
    "There is speculation that old genetic material might allow 'time travel' by taking control of a person long dead. "
    "Some minds are impossible to hack - those with strong psychic potential or Awakened beings resist. The consequences "
    "would be horrifying if this rote fell into Technocracy hands."
)
effect_life_hacking.add_source("Virtual Adepts (1st Edition)", 61)

effect_dream_hacking, _ = Effect.objects.get_or_create(
    name="Dream Hacking",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)
effect_dream_hacking.description = (
    "Reality Hackers use this effect to enter and manipulate the dreams of Sleepers. They claim the virtual worlds "
    "in dreams surpass even the Digital Web. Some place messages in dreams for other Hackers to find, while others "
    "use dreams as meeting spaces. The worlds accessed are said to be keys to understanding the Tapestry and doors "
    "to countless undiscovered Realms."
)
effect_dream_hacking.add_source("Virtual Adepts (1st Edition)", 61)

# ===== NAMED CHARACTERS =====

# Alan Turing (Historical Figure)
alan_turing, _ = MtAHuman.objects.get_or_create(
    name="Alan Turing",
    status="Dec",  # Deceased
    chronicle=None,
)
alan_turing.concept = "Virtual Adept Pioneer"
alan_turing.description = (
    "The virtual leader of the early Virtual Adepts, killed by Technocracy assassination in 1954. Turing was "
    "developing 'virtual reality' technology decades before the Time Table scheduled it. His work threatened to "
    "shatter the Technocracy's carefully planned timeline. The Men in Black terminated him with extreme prejudice. "
    "Many Virtual Adepts see him as a martyr and visionary. Celebrated on 'Net Day' (his birthday/death day)."
)
alan_turing.add_source("Virtual Adepts (1st Edition)", 18, 19)

# Roger "TremaTrode" Thackery
roger_thackery, _ = Mage.objects.get_or_create(
    name='Roger "TremaTrode" Thackery',
    status="App",
    chronicle=None,
)
roger_thackery.concept = "Virtual Adept Liaison"
roger_thackery.tradition = MageFaction.objects.get(name="Virtual Adepts")
roger_thackery.description = (
    "Liaison to the Technocracy Conventions in the 1940s-1950s, later became liaison to the Traditions after the "
    "defection. Took over after James 'Wirehead' Peristone was killed in a London bombing. Provided crucial "
    "information to the Council of Nine about the Technocracy Time Table and other secrets. Accepted the Traditions' "
    "offer of amnesty in 1961. Known for bringing information about the HIT Mark IV to the Traditions in 1979."
)
roger_thackery.add_source("Virtual Adepts (1st Edition)", 18, 20, 21)

# Dante/Desmond Collingsworth
dante, _ = Mage.objects.get_or_create(
    name="Desmond Collingsworth",
    status="App",
    chronicle=None,
)
dante.concept = "Progenitor-born Master, Child Rescuer"
dante.tradition = MageFaction.objects.get(name="Virtual Adepts")
dante.essence = "Pattern"
dante.description = (
    "Born with an Awakened Avatar, Dante's pregnant mother was paid by the Progenitors to participate in experiments. "
    "She died in childbirth. Raised by a Progenitor family under constant surveillance, Dante finished high school at 8, "
    "graduated Harvard, and completed medical school in 5 years. The Lab Rats (Virtual Adepts born from Progenitor "
    "experiments) rescued him. Now he strikes at the Technocracy by rescuing children earmarked for them. Perhaps the "
    "most well-known Tradition Master, Dante always has at least two students. Studying under Dante is extremely elite."
)
dante.add_source("Virtual Adepts (1st Edition)", 65)

# Demonseed Elite/Kibo
demonseed_elite, _ = MtAHuman.objects.get_or_create(
    name="Demonseed Elite",
    status="Dec",  # Sort of - transcended physical form
    chronicle=None,
)
demonseed_elite.concept = "Digital Ascended Being"
demonseed_elite.description = (
    "In the late 1970s-early 1980s, a user achieved Maximum K-rad Eliteness and his soul merged with the global "
    "telecom network. Demonseed Elite is no longer a person but an entity residing in cables and satellite links. "
    "He IS AT&T, Internet, and SouthWestern Bell. He knows everything that happens on his networks and takes any "
    "sign of lameness as a personal insult. To speak his real name is to die. Those who have seen his wrath describe "
    "terrible deaths - intestines ripped out, fiber optic cables twisted through brain matter, foreheads branded "
    "'k-lame.' Said to manifest as a giant orange monster truck with 30-foot tires that crushes rodents flat."
)
demonseed_elite.add_source("Virtual Adepts (1st Edition)", 65, 66)

# Catherine Blass / X-Cel
catherine_blass, _ = Mage.objects.get_or_create(
    name="Catherine Blass",
    status="App",
    chronicle=None,
)
catherine_blass.concept = "Performance Artist / Information Broker"
catherine_blass.tradition = MageFaction.objects.get(name="Virtual Adepts")
catherine_blass.description = (
    "A controversial performance artist known as X-Cel in the Net. European/Hispanic female, 31 years old, 5'6\", 134 lbs. "
    "Achieved fame when her show 'Rage on a Meathook' was banned in Washington D.C. for obscenity. Uses technology "
    "and coincidental magick in spectacular performances - body wired for sound and flogged, four-octave singing range "
    "shattering glasses on video monitors. Known as a merciful information broker in the Net who has rescued Void "
    "Engineers and compromised Iteration X operatives, showing unusual lack of hostility toward Technocracy. Her Net "
    "icon appears as a radiant nun in traditional Mexican garb. Technocracy profile indicates multiple personality "
    "disorder or unhealthy imagination. Named after a Mayan moon goddess."
)
catherine_blass.add_source("Virtual Adepts (1st Edition)", 66)

# Electric Death
electric_death, _ = Mage.objects.get_or_create(
    name="Electric Death",
    status="App",
    chronicle=None,
)
electric_death.concept = "Virtual Adept Master"
electric_death.tradition = MageFaction.objects.get(name="Virtual Adepts")
electric_death.description = (
    "A Virtual Adept Master quoted as saying the other Traditions should be wary of the Adepts' power to subvert "
    "an entire generation of Sleepers. Known for understanding how the Tradition's beliefs are alien to those who "
    "cling to conservatism and tradition."
)
electric_death.add_source("Virtual Adepts (1st Edition)", 12)

# ===== CHARACTER TEMPLATES =====

template_couch_potato, _ = CharacterTemplate.objects.get_or_create(
    name="The Couch Potato",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "tradition": "Virtual Adepts",
        "concept": "Couch Potato",
        "description": (
            "A lazy but brilliant mage who projects their consciousness anywhere through their "
            "entertainment system. Knows every TV show by heart and can quote them endlessly. "
            "Projects holographic icons to interact with the world while remaining safely at home."
        ),
        "basic_info": {
            "nature": "FK:Archetype:Loner",
            "demeanor": "FK:Archetype:Conniver",
            "essence": "FK:Essence:Pattern",
        },
        "attributes": {
            "strength": 1,
            "dexterity": 2,
            "stamina": 2,
            "perception": 3,
            "intelligence": 4,
            "wits": 2,
            "charisma": 2,
            "manipulation": 3,
            "appearance": 1,
        },
        "abilities": {
            "awareness": 1,
            "dodge": 3,
            "streetwise": 1,
            "subterfuge": 4,
            "meditation": 2,
            "technology": 4,  # Leisure Tech specialty
            "culture": 4,  # TV specialty
        },
        "backgrounds": [
            {"name": "Arcane", "rating": 1},
            {"name": "Avatar", "rating": 1},
            {"name": "Mentor", "rating": 1},
        ],
        "powers": {
            "correspondence": 3,
            "forces": 2,
            "time": 1,
            "arete": 3,
        },
        "willpower": 5,
        "quintessence": 4,
        "specialties": ["Technology (Leisure Tech)", "Culture (TV)"],
        "equipment": "Remote control, bathrobe, potato chips, entertainment center, really comfy couch",
        "is_official": True,
        "is_public": True,
    },
)
template_couch_potato[0].add_source("Virtual Adepts (1st Edition)", 48)

template_musician, _ = CharacterTemplate.objects.get_or_create(
    name="The Musician (Virtual Adept)",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "tradition": "Virtual Adepts",
        "concept": "Musician",
        "description": (
            "A one-person band using digital keyboards and MIDI interfaces to create music - and magick. "
            "Channels art through musical instruments rather than keyboards, creating personal special effects "
            "through sound manipulation."
        ),
        "basic_info": {
            "nature": "FK:Archetype:Visionary",
            "demeanor": "FK:Archetype:Rebel",
            "essence": "FK:Essence:Pattern",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 3,
            "stamina": 2,
            "perception": 2,
            "intelligence": 2,
            "wits": 2,
            "charisma": 3,
            "manipulation": 3,
            "appearance": 3,
        },
        "abilities": {
            "alertness": 1,
            "expression": 3,
            "streetwise": 1,
            "drive": 1,
            "technology": 4,  # Musical Equipment specialty
            "computer": 3,
            "culture": 3,  # Music specialty
            "science": 2,
        },
        "backgrounds": [
            {"name": "Allies", "rating": 4},
            {"name": "Influence", "rating": 1},
        ],
        "powers": {
            "correspondence": 1,
            "forces": 3,
            "prime": 2,
            "arete": 3,
        },
        "willpower": 4,
        "quintessence": 3,
        "specialties": ["Technology (Musical Equipment)", "Culture (Music)"],
        "equipment": "Commodore Amiga, Yamaha DX-7 keyboard, drum machine, MIDI guitar, sampling machine, recording deck, tapes of old movies",
        "is_official": True,
        "is_public": True,
    },
)
template_musician[0].add_source("Virtual Adepts (1st Edition)", 50)

template_revisionist, _ = CharacterTemplate.objects.get_or_create(
    name="Revisionist Writer",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "tradition": "Virtual Adepts",
        "concept": "Revisionist Writer",
        "description": (
            "A former government bureaucrat who Awakened to the power of shaping reality through the written word. "
            "Can alter memories and emotions through writing, with a Technocratic Avatar that constantly tries to "
            "dominate them."
        ),
        "basic_info": {
            "nature": "FK:Archetype:Deviant",
            "demeanor": "FK:Archetype:Rebel",
            "essence": "FK:Essence:Pattern",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "perception": 2,
            "intelligence": 3,
            "wits": 4,  # Perceptive specialty
            "charisma": 2,
            "manipulation": 3,
            "appearance": 3,
        },
        "abilities": {
            "awareness": 3,
            "expression": 3,
            "intimidation": 3,
            "subterfuge": 2,
            "computer": 3,
            "culture": 3,
            "enigmas": 2,
            "investigation": 1,
            "law": 1,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 2},
            {"name": "Influence", "rating": 3},
            {"name": "Library", "rating": 2},
        ],
        "powers": {
            "correspondence": 1,
            "mind": 2,
            "prime": 2,
            "arete": 3,
        },
        "willpower": 6,
        "quintessence": 2,
        "specialties": ["Wits (Perceptive)"],
        "equipment": "Portable word-processor with micro-printer, flashy clothes, white-out, pad and pencil",
        "is_official": True,
        "is_public": True,
    },
)
template_revisionist[0].add_source("Virtual Adepts (1st Edition)", 52)

template_cyberpunk, _ = CharacterTemplate.objects.get_or_create(
    name="The Cyberpunk (Virtual Adept)",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "tradition": "Virtual Adepts",
        "concept": "Cyberpunk",
        "description": (
            "A nasty, foul-mouthed brat who runs with a high-tech street gang. Flashy and vulgar with magick, "
            "depending more on natural abilities than deep knowledge. Believes information wants to be free "
            "and has the power to make it so."
        ),
        "basic_info": {
            "nature": "FK:Archetype:Bravo",
            "demeanor": "FK:Archetype:Rebel",
            "essence": "FK:Essence:Dynamic",
        },
        "attributes": {
            "strength": 3,
            "dexterity": 3,
            "stamina": 3,
            "perception": 3,
            "intelligence": 2,
            "wits": 2,
            "charisma": 1,
            "manipulation": 2,
            "appearance": 1,
        },
        "abilities": {
            "alertness": 1,
            "athletics": 1,
            "brawl": 2,
            "dodge": 2,
            "intimidation": 3,
            "streetwise": 3,
            "computer": 3,  # Hacking specialty
            "technology": 2,
            "culture": 1,
        },
        "backgrounds": [
            {"name": "Allies", "rating": 2},
            {"name": "Dream", "rating": 2},
        ],
        "powers": {
            "correspondence": 1,
            "forces": 2,
            "matter": 2,
            "prime": 1,
            "arete": 2,
        },
        "willpower": 3,
        "quintessence": 2,
        "specialties": ["Computer (Hacking)"],
        "equipment": "Portable computer, acoustic coupler, Marshmallow HEX, textphiles, black leather jacket, Jolt Cola",
        "is_official": True,
        "is_public": True,
    },
)
template_cyberpunk[0].add_source("Virtual Adepts (1st Edition)", 54)

template_chaotician, _ = CharacterTemplate.objects.get_or_create(
    name="The Chaotician",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "tradition": "Virtual Adepts",
        "concept": "Chaotician",
        "description": (
            "A physicist and mathematician with intuitive grasp of sciences who manipulates systems from a distance. "
            "Sees patterns in everything and uses chaos theory to affect reality. Dedicated to bringing Ascension "
            "by understanding and manipulating the universal equation."
        ),
        "basic_info": {
            "nature": "FK:Archetype:Architect",
            "demeanor": "FK:Archetype:Fanatic",
            "essence": "FK:Essence:Dynamic",
        },
        "attributes": {
            "strength": 1,
            "dexterity": 3,
            "stamina": 2,
            "perception": 3,
            "intelligence": 5,  # Patterns specialty
            "wits": 2,
            "charisma": 2,
            "manipulation": 2,
            "appearance": 2,  # Impressive specialty
        },
        "abilities": {
            "alertness": 1,
            "dodge": 2,
            "intuition": 2,
            "meditation": 3,
            "stealth": 2,
            "computer": 3,
            "technology": 1,
            "enigmas": 4,
            "investigation": 2,
            "science": 5,  # Intuitive Mathematics specialty
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 3},
            {"name": "Mentor", "rating": 2},
        ],
        "powers": {
            "correspondence": 1,
            "entropy": 3,
            "matter": 2,
            "prime": 1,
            "arete": 3,
        },
        "willpower": 5,
        "quintessence": 3,
        "specialties": [
            "Intelligence (Patterns)",
            "Appearance (Impressive)",
            "Science (Intuitive Mathematics)",
        ],
        "equipment": "Laptop computer, pistol, leather jacket, hand-held radio scanner",
        "is_official": True,
        "is_public": True,
    },
)
template_chaotician[0].add_source("Virtual Adepts (1st Edition)", 56)

template_simulator, _ = CharacterTemplate.objects.get_or_create(
    name="The Mad Simulator",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "tradition": "Virtual Adepts",
        "concept": "Mad Simulator",
        "description": (
            "A former VR pioneer who Awakened when shifting into the Digital Web. Wants to duplicate everything "
            "online - buildings, landscapes, even people - to create a better world. Uncomfortable with physical "
            "intimacy but uninhibited online."
        ),
        "basic_info": {
            "nature": "FK:Archetype:Visionary",
            "demeanor": "FK:Archetype:Loner",
            "essence": "FK:Essence:Dynamic",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "perception": 4,  # Patterns specialty
            "intelligence": 3,
            "wits": 2,
            "charisma": 2,
            "manipulation": 3,
            "appearance": 2,
        },
        "abilities": {
            "athletics": 1,
            "expression": 1,
            "subterfuge": 1,
            "computer": 4,
            "technology": 4,  # V.R. specialty
            "cosmology": 2,
            "culture": 2,
            "enigmas": 1,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 3},
            {"name": "Destiny", "rating": 1},
            {"name": "Library", "rating": 3},
        ],
        "powers": {
            "correspondence": 2,
            "mind": 2,
            "prime": 2,
            "arete": 2,
        },
        "willpower": 4,
        "quintessence": 4,
        "specialties": ["Perception (Patterns)", "Technology (V.R.)"],
        "equipment": "Camera, computer, virtual reality suit, massive software collection, dozen passwords to online services",
        "is_official": True,
        "is_public": True,
    },
)
template_simulator[0].add_source("Virtual Adepts (1st Edition)", 58)

# ===== ROTES =====

# Get references to practices and abilities
try:
    realityhacking = Practice.objects.get(name="Reality Hacking")
except Practice.DoesNotExist:
    realityhacking, _ = Practice.objects.get_or_create(
        name="Reality Hacking",
        defaults={
            "description": "Digital manipulation of reality through code and technology"
        },
    )

try:
    computer = Ability.objects.get(name="Computer")
    intelligence = Attribute.objects.get(name="Intelligence")
    perception = Attribute.objects.get(name="Perception")
    manipulation = Attribute.objects.get(name="Manipulation")
    wits = Attribute.objects.get(name="Wits")
    subterfuge = Ability.objects.get(name="Subterfuge")
except:
    pass  # Abilities and attributes should already exist

rote_encrypt_thoughts, _ = Rote.objects.get_or_create(
    name="Encrypt Thoughts",
    effect=effect_encrypt_thoughts,
    practice=realityhacking,
    attribute=intelligence,
    ability=computer,
)
rote_encrypt_thoughts.description = (
    "Created by the Cypherpunks to protect their brains from prying mages. The mage prepares a program and sets "
    "a public 'key' for encryption. From that point on, no one may read their mind without thinking of the password. "
    "Cypherpunks value information sanctity above all else."
)
rote_encrypt_thoughts.add_source("Virtual Adepts (1st Edition)", 61)

rote_degrade_order, _ = Rote.objects.get_or_create(
    name="Degrade Order",
    effect=effect_degrade_order,
    practice=realityhacking,
    attribute=intelligence,
    ability=computer,
)
rote_degrade_order.description = (
    "Developed by Chaoticians to research chaos effects on complex systems. Applies pressure from two directions - "
    "adding Entropy and accelerating Time. A flower withers in thirty seconds, compressing its relative lifespan."
)
rote_degrade_order.add_source("Virtual Adepts (1st Edition)", 61)

rote_information_glut, _ = Rote.objects.get_or_create(
    name="Information Glut",
    effect=effect_information_glut,
    practice=realityhacking,
    attribute=perception,
    ability=computer,
)
rote_information_glut.description = (
    "Enhances any one sense by 'turning up the volume.' Virtual Adepts use it to accelerate computer comprehension. "
    "The Technocracy uses it as torture, as seen in the Prelude. Can provide night vision, enhanced hearing, or "
    "increase ability to comprehend sensory input."
)
rote_information_glut.add_source("Virtual Adepts (1st Edition)", 62)

rote_holographic_projector, _ = Rote.objects.get_or_create(
    name="Holographic Projector",
    effect=effect_holographic_projector,
    practice=realityhacking,
    attribute=manipulation,
    ability=computer,
)
rote_holographic_projector.description = (
    "Projects a hologram or icon of the Adept wherever desired. The hologram is just light patterns, but Mind magick "
    "fools viewers into perceiving smell and sensory data. Rarely fools mages or detection devices without 4+ successes."
)
rote_holographic_projector.add_source("Virtual Adepts (1st Edition)", 62)

rote_social_engineering, _ = Rote.objects.get_or_create(
    name="Social Engineering",
    effect=effect_social_engineering,
    practice=realityhacking,
    attribute=manipulation,
    ability=subterfuge,
)
rote_social_engineering.description = (
    "The 'Look, there goes Elvis' trick. A favorite combat tactic - distract the enemy with sociological sleight-of-hand "
    "while weaving an escape rote, causing a physical disturbance, or simply fleeing. Virtual Adept fights are quick or not at all."
)
rote_social_engineering.add_source("Virtual Adepts (1st Edition)", 63)

# ===== ITEMS/TALISMANS =====

# Trinary Computer
trinary_computer, _ = Wonder.objects.get_or_create(
    name="Trinary Computer",
    rank=2,
    max_quintessence=0,
    quintessence=0,
    background_cost=0,
)
trinary_computer.description = (
    "A computer magickally enhanced to use three states (on, off, and negative on) to represent information, "
    "giving considerably more processing power and near-intelligence. Standard computers can only handle 'yes' or 'no' "
    "as concepts, but trinary computers can accept 'maybe' through fuzzy logic - the same kind of logic humans use "
    "for concepts like 'warm,' 'fast,' 'cheap,' or 'smart.' Most Virtual Adepts upgrade their systems to trinary "
    "status through rigorous burn-in testing and magical attunement."
)
trinary_computer.add_source("Virtual Adepts (1st Edition)", 62, 63)

# PowerGlove
powerglove, _ = Wonder.objects.get_or_create(
    name="PowerGlove",
    rank=1,
    max_quintessence=0,
    quintessence=0,
    background_cost=0,
)
powerglove.description = (
    "A special glove fitted with sensors that relay hand motion back to the computer. An obvious replacement for "
    "traditional keyboards. Mages using Correspondence 2 can work their computers from a distance with these devices."
)
powerglove.add_source("Virtual Adepts (1st Edition)", 63)

# Heads-Up Display
hud, _ = Wonder.objects.get_or_create(
    name="Heads-Up Display",
    rank=1,
    max_quintessence=0,
    quintessence=0,
    background_cost=0,
)
hud.description = (
    "A video monitor built into the side of mirrorshade glasses. Allows the mage to watch video output in addition "
    "to whatever is in front of them - no need to take eyes off an enemy to see if a rote is running. Combined with "
    "a PowerGlove, this is the choice of many combat mages."
)
hud.add_source("Virtual Adepts (1st Edition)", 63)

# MIDI Musical Instruments
midi_instrument, _ = Wonder.objects.get_or_create(
    name="MIDI Musical Instrument",
    rank=1,
    max_quintessence=0,
    quintessence=0,
    background_cost=0,
)
midi_instrument.description = (
    "Musical instruments that patch into computers through MIDI ports. Expensive but powerful alternative input forms. "
    "Through the instrument, the character can 'intone' rotes that have magickal properties and might even form some "
    "kind of song. Used by Virtual Adept musicians."
)
midi_instrument.add_source("Virtual Adepts (1st Edition)", 63)

# Virtual Reality Suit
vr_suit, _ = Wonder.objects.get_or_create(
    name="Virtual Reality Suit",
    rank=3,
    max_quintessence=5,
    quintessence=0,
    background_cost=2,
)
vr_suit.description = (
    "A full-body suit that allows complete immersion in virtual reality. Provides sensory feedback for all sensations - "
    "touch, hearing, sight, smell. Some have optional settings for taste. Most Virtual Adepts set their icons to taste "
    "like cooked chicken. Essential equipment for serious Net exploration and the Mad Simulator's tool of choice."
)
vr_suit.add_source("Virtual Adepts (1st Edition)", 58, 63)

# ===== ADDITIONAL NAMED CHARACTERS =====

# James "Wirehead" Peristone
james_peristone, _ = MtAHuman.objects.get_or_create(
    name='James "Wirehead" Peristone',
    status="Dec",  # Deceased - killed in London bombing
    chronicle=None,
)
james_peristone.concept = "Virtual Adept Liaison"
james_peristone.description = (
    "Former liaison to the Technocracy Conventions. Killed in a London flat that was bombed in summer 1941. "
    "His death led to Roger 'TremaTrode' Thackery taking over as liaison."
)
james_peristone.add_source("Virtual Adepts (1st Edition)", 18)

# Andrea Collingsworth
andrea_collingsworth, _ = MtAHuman.objects.get_or_create(
    name="Andrea Collingsworth",
    status="Dec",
    chronicle=None,
)
andrea_collingsworth.concept = "Victim of Progenitor Experimentation"
andrea_collingsworth.description = (
    "Mother of Desmond Collingsworth (Dante). Lived in Cabrini Green, Chicago. Was paid $50,000 by Progenitor "
    "Dr. Bens to participate in a secret experiment to treat disabilities in unborn children. Dante was born with "
    "an already-Awakened Avatar, which fascinated the Progenitors. Andrea did not survive Dante's birth. "
    "She had prayed to God to watch over her child - someone was listening, but it wasn't God."
)
andrea_collingsworth.add_source("Virtual Adepts (1st Edition)", 65)

# Dr. Bens
dr_bens, _ = MtAHuman.objects.get_or_create(
    name="Dr. Bens",
    status="App",
    chronicle=None,
)
dr_bens.concept = "Progenitor Researcher"
dr_bens.description = (
    "A Progenitor who discovered an unborn child (Desmond Collingsworth) whose Avatar had already Awakened. "
    "Conducted experiments on Andrea Collingsworth for eight months before Dante's birth. Supervised Dante's "
    "upbringing under constant Progenitor surveillance. Never seen an unborn Awakened Avatar before Dante."
)
dr_bens.add_source("Virtual Adepts (1st Edition)", 65)

# Sharri Powell (Verbena observer)
sharri_powell, _ = Mage.objects.get_or_create(
    name="Sharri Powell",
    status="App",
    chronicle=None,
)
sharri_powell.concept = "Verbena Infiltrator"
sharri_powell.tradition = MageFaction.objects.get(name="Verbena")
sharri_powell.description = (
    "Member of the Amhurst C-Oven who spent six months infiltrating the Virtual Adepts on a 'field trip.' "
    "Compiled detailed intelligence on Adept society, structure, tactics, and relationships with other Traditions. "
    "Wrote report to Brian Hastings warning not to put anything on computer files that shouldn't be seen. "
    "Advised cautious cooperation with the Adepts while maintaining vigilance."
)
sharri_powell.add_source("Virtual Adepts (1st Edition)", 23, 33)

print("Virtual Adepts 1st Edition data loaded successfully!")
print(
    f"  - {MageFaction.objects.filter(parent__name='Virtual Adepts').count()} factions/legions"
)
print(
    f"  - {Effect.objects.filter(sources__name__contains='Virtual Adepts (1st Edition)').count()} effects"
)
print(f"  - 11 named characters")
print(f"  - 6 character templates")
print(f"  - 5 rotes")
print(f"  - 5 wonders/items")
