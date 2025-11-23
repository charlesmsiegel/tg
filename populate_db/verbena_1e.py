"""
Verbena Tradition Book (1st Edition)
Guardians of the Mythic Threads
"""

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.focus import Practice
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.rote import Rote
from core.models import Book, CharacterTemplate

# ==============================================================================
# BOOK
# ==============================================================================

verbena_book = Book.objects.get_or_create(
    name="Tradition Book: Verbena",
    edition="1st",
    gameline="mta",
    defaults={
        "url": "https://www.storytellersvault.com/product/432/Tradition-Book-Verbena",
    },
)[0]

# ==============================================================================
# EFFECTS (Rotes from Appendix One)
# ==============================================================================

# Sense the Fleeting Moment (• Time)
effect_sense_fleeting_moment = Effect.objects.get_or_create(
    name="Sense the Fleeting Moment",
    time=1,
    defaults={
        "description": "This rote allows a Verbena to sense the proper moment in which to act. "
        "By using the Mythic Thread of astrology, a Verbena may choose the perfect time and place "
        "to do a specific thing, and may even be successful at discerning whether or not the thing "
        "should be done at all. Each success on the magick roll lowers the difficulty for one "
        "specific non-magickal task by 1. This is usually coincidental."
    },
)[0]
effect_sense_fleeting_moment.add_source("Tradition Book: Verbena", 63)

# Bloodsight (• Life)
effect_bloodsight = Effect.objects.get_or_create(
    name="Bloodsight",
    life=1,
    defaults={
        "description": "This rote allows a Verbena to sense how healthy a person is, what diseases "
        "(if any) she has, whether she is insane or pregnant or how old she really is, and alerts "
        "him to the presence of any foreign substances including bullets, drugs, and alcohol. "
        "The Verbena also uses this rote to determine someone's lineage. Each success provides one "
        "fact about the target's physical state."
    },
)[0]
effect_bloodsight.add_source("Tradition Book: Verbena", 63)

# Dowsing (• Life, • Correspondence)
effect_dowsing = Effect.objects.get_or_create(
    name="Dowsing",
    life=1,
    correspondence=1,
    defaults={
        "description": "Using a forked stick (hazel is best) and this rote, a Verbena can search "
        "an area for the presence of water (or oil), by sensing both the presence of minute life "
        "forms attracted to the moisture, and the volume of liquid present. This is useful both "
        "for discovering underground resources and for finding water in arid environments. "
        "Each success provides one more piece of information about the liquid."
    },
)[0]
effect_dowsing.add_source("Tradition Book: Verbena", 63 - 64)

# Banishing Blessing (•• Entropy, •• Mind)
effect_banishing_blessing = Effect.objects.get_or_create(
    name="Banishing Blessing",
    entropy=2,
    mind=2,
    defaults={
        "description": "Verbena often use this to rid themselves of people who are annoying but "
        "not actually threatening. By controlling the randomness of everyday events and offering "
        "mental suggestions, a Verbena can cause things to happen which will send the target away. "
        "These things are usually positive: the target wins the lottery and moves away, or finds a "
        "free airline ticket voucher and flies to Paris for a week, or wrangles a car ride even when "
        "the last possibility has dried up. Each success sends the target away for more and more time. "
        "The Effect is always beneficial rather than harmful; this is seen as a more subtle means to be rid of others."
    },
)[0]
effect_banishing_blessing.add_source("Tradition Book: Verbena", 64)

# Calling the Wind Lord (•• Forces, •• Spirit)
effect_calling_wind_lord = Effect.objects.get_or_create(
    name="Calling the Wind Lord",
    forces=2,
    spirit=2,
    defaults={
        "description": "This rote summons spirits of the wind, who will then influence the local "
        "weather. The Verbena use this to alter the weather slightly: a sunny day becomes cloudy, "
        "clouds become rain, rain becomes a thunderstorm. Since the weather is still not completely "
        "predictable even by the science of meteorology, this Effect is usually coincidental. "
        "Each success on the roll enables the Verbena to alter the local weather; the more successes "
        "she rolls, the greater the change. These changes must be gradual and slow; speeding the Effect "
        "can result in vulgar magick. The weather-alteration affects the sky within immediate sight of "
        "the Verbena, lasts a 'normal' length of time, and cannot create phenomena out of nothing."
    },
)[0]
effect_calling_wind_lord.add_source("Tradition Book: Verbena", 64)

# Circle Ward (•• Spirit, • Mind, •• Prime)
effect_circle_ward = Effect.objects.get_or_create(
    name="Circle Ward",
    spirit=2,
    mind=1,
    prime=2,
    defaults={
        "description": "This rote creates a circle of power, within which a Verbena can safely work. "
        "The ward itself is created by summoning four separate and distinctly powerful spirits "
        "(usually allied with one of the four directions, seasons, or classical elements) and weaving "
        "a circular pattern out of their spiritual essences. The result is a very strong ward that can "
        "hold up against many kinds of direct magickal attack. Each success on the roll gives the Verbena "
        "+1 to her countermagick roll for the scene, as long as she stays within the circle. "
        "This rote cannot be maintained for more than one scene per point of stamina."
    },
)[0]
effect_circle_ward.add_source("Tradition Book: Verbena", 64)

# Taliesin's Song (••• Life, •• Mind)
effect_taliesins_song = Effect.objects.get_or_create(
    name="Taliesin's Song",
    life=3,
    mind=2,
    defaults={
        "description": "A Verbena may completely sway another's mind, simply by altering his vocal "
        "chords and singing. This control is coincidental, and allows the Verbena to influence others. "
        "Usually those who use this rote do so only when absolutely necessary. The target must be able "
        "to hear the music sung or words spoken for this rote to be successful. Each success on the roll "
        "adds an automatic success to the Verbena's social roll against the target or targets within range, "
        "for the magick's usual duration. This Effect can be resisted by Willpower if the target is aware "
        "that some coercion is being used. Taliesin's Song is not terribly effective against other mages "
        "(who may be aware that they are being bewitched), but is quite useful when dealing with Sleepers."
    },
)[0]
effect_taliesins_song.add_source("Tradition Book: Verbena", 64)

# Translocation (•••• Correspondence)
effect_translocation = Effect.objects.get_or_create(
    name="Translocation",
    correspondence=4,
    defaults={
        "description": "It is said this rote was first used to transport Arthur and his army to Badon Hill "
        "when Arthur needed magickal aid to defeat those who would not join him. To achieve this Effect, "
        "the Verbena begins to walk, run, or ride (a horse is preferable, although some Verbena have learned "
        "to do this while driving a car). Slowly, the scenery begins to blur around her as she travels toward "
        "her destination. The traveler does not appear 'differently' to outside observers, as the Effect speeds "
        "and slows the traveler gradually. Each success on the Effect roll reduces travel time by 20%. "
        "Five successes on the roll cause the user to arrive almost instantaneously. Note that this Effect can "
        "be coincidental at night or with few witnesses, and the area around the traveler is in deep wilderness "
        "or on a lonely road."
    },
)[0]
effect_translocation.add_source("Tradition Book: Verbena", 64)

# ==============================================================================
# NAMED CHARACTERS (from Prelude and throughout the book)
# ==============================================================================

# Mother Celene - Elder Verbena witch
mother_celene = MtAHuman.objects.get_or_create(
    name="Mother Celene",
    defaults={
        "description": "A severe, elderly woman with penetrating insight and powerful magickal abilities. "
        "She can sense others' hormonal and chemical balances, and teaches through both instruction and pain. "
        "Leader of the Avengers, a strict Circle focused on the old ways and harsh justice.",
        "concept": "Elder Witch Teacher",
        "nature": "Judge",
        "demeanor": "Traditionalist",
        "essence": "Pattern",
    },
)[0]
mother_celene.add_source("Tradition Book: Verbena", 4 - 5)

# Rhianna Flamedancer - Priestess and Teacher
rhianna_flamedancer = Mage.objects.get_or_create(
    name="Rhianna Flamedancer",
    defaults={
        "description": "A Verbena priestess who conducts initiations and teaches new apprentices. "
        "She is wise, compassionate but firm, and guides initiates through their Awakening.",
        "concept": "Verbena Priestess",
        "nature": "Caregiver",
        "demeanor": "Pedagogue",
        "essence": "Pattern",
        "arete": 3,
        "life": 3,
        "prime": 2,
        "spirit": 2,
    },
)[0]
rhianna_flamedancer.add_source("Tradition Book: Verbena", 14 - 15)

# Talien - Technopagan Bard and Loremaster
talien = Mage.objects.get_or_create(
    name="Talien",
    defaults={
        "description": "A young bard and loremaster who uses computers to organize his Book of Shadows "
        "and keep historical facts straight. Considered a 'black sheep' by traditional Verbena, he's a "
        "technopagan who participates in pagan BBS on the net. Despite this, he's trusted to teach history "
        "due to his exceptional organization and knowledge.",
        "concept": "Technopagan Bard",
        "nature": "Judge",
        "demeanor": "Visionary",
        "essence": "Questing",
        "arete": 2,
        "correspondence": 1,
        "forces": 1,
        "life": 2,
        "mind": 1,
        "prime": 1,
        "time": 1,
    },
)[0]
talien.add_source("Tradition Book: Verbena", 16 - 27)

# Lindara - Shapeshifter Teacher
lindara = Mage.objects.get_or_create(
    name="Lindara",
    defaults={
        "description": "A Lifeweaver with exotic features and graceful body, dressed in top-flight "
        "gothic punk gear. She is a shapeshifter capable of changing her form, gender, and appearance "
        "at will. She tests apprentices through trials and teaches about Verbena society and politics.",
        "concept": "Shapeshifter Teacher",
        "nature": "Trickster",
        "demeanor": "Visionary",
        "essence": "Dynamic",
        "arete": 3,
        "life": 4,
        "mind": 2,
        "matter": 1,
    },
)[0]
lindara.add_source("Tradition Book: Verbena", 29 - 37)

# Bear - Gruff Teacher
bear_verbena = MtAHuman.objects.get_or_create(
    name="Bear (Verbena Teacher)",
    defaults={
        "description": "A short, white-haired man with a scraggly beard often full of food particles. "
        "Gruff, dour, and intolerant, but knowledgeable about Verbena structure, Circles, and philosophy. "
        "He speaks in a rapid-fire manner and has strong opinions about all the Verbena factions.",
        "concept": "Gruff Teacher",
        "nature": "Curmudgeon",
        "demeanor": "Bravo",
    },
)[0]
bear_verbena.add_source("Tradition Book: Verbena", 33 - 37)

# Neasha Morningshade - Council Spokesperson
neasha_morningshade = Mage.objects.get_or_create(
    name="Neasha Morningshade",
    defaults={
        "description": "An Adept in her mid-thirties, the quintessential Celtic earth mother type. "
        "She has clear blue eyes and flaming red hair falling to her waist. Though not ravishingly "
        "beautiful, her dignity and grace command attention and respect. She is a spokesperson for "
        "the Verbena to other Traditions and a sought-after teacher. Student of Nightshade, the "
        "Verbena member of the Council of Nine. She leads campaigns to locate and integrate Orphans "
        "into the Verbena, recognizing their power.",
        "concept": "Council Spokesperson",
        "nature": "Visionary",
        "demeanor": "Diplomat",
        "essence": "Pattern",
        "arete": 4,
        "correspondence": 2,
        "life": 4,
        "prime": 3,
        "mind": 2,
        "spirit": 3,
    },
)[0]
neasha_morningshade.add_source("Tradition Book: Verbena", 67)

# Sam Haine - Troubleshooter
sam_haine = Mage.objects.get_or_create(
    name="Sam Haine",
    defaults={
        "description": "A gruff, dour troubleshooter for the Verbena who travels the world looking for "
        "pieces of Mythic Threads. Also known as 'Changing Man' for his ability to magickally change his "
        "appearance. He debunks false occult items the Syndicate sells. Rude, intolerant, and difficult "
        "to understand, but has never been known to tell a lie or repeat sensitive information. "
        "Has been captured by the Technocracy multiple times but always escapes, leading some to suspect "
        "he has allies within the Technocracy.",
        "concept": "Troubleshooter",
        "nature": "Loner",
        "demeanor": "Bravo",
        "essence": "Questing",
        "arete": 3,
        "life": 3,
        "mind": 2,
        "matter": 2,
        "correspondence": 2,
    },
)[0]
sam_haine.add_source("Tradition Book: Verbena", 68)

# Nightshade - Council of Nine Member
nightshade = Mage.objects.get_or_create(
    name="Nightshade",
    defaults={
        "description": "The Verbena representative on the Council of Nine. Master-level mage and teacher "
        "of Neasha Morningshade. Little else is known, maintaining the mystery befitting a Council member.",
        "concept": "Council of Nine Member",
        "nature": "Visionary",
        "essence": "Pattern",
        "arete": 6,
        "life": 5,
        "prime": 4,
        "spirit": 4,
    },
)[0]
nightshade.add_source("Tradition Book: Verbena", 67)

# Lilith - Legendary First Verbena
lilith = MtAHuman.objects.get_or_create(
    name="Lilith the Damned Queen",
    defaults={
        "description": "Known as the Damned Queen or the Lady of Night, Lilith is counted as the first "
        "Verbena - indeed, the first feminist and first mage. The greatest of the Wyck, she was said to "
        "be Adam's first wife who refused a subservient position and was driven from the Garden. She created "
        "a palace for herself in the Umbra - essentially the first Horizon Realm. She gave birth to children, "
        "one of whom became the ancestress of the Garou. She sheltered and Awakened Cain, whose curse changed "
        "him into the first vampire. She taught him her magick, which became vampiric Disciplines. "
        "A beautiful dark woman whose eyes pierce through darkness and disguise to read the soul. "
        "She can read the twines of Fate and shares knowledge for a price. Verbena acknowledge her as the "
        "mother of all Verbena and originator of all Spheres. She may have rescued the four secret Horizon "
        "Realms from the shattered Mythic World. She may still have dealings with the Tradition today.",
        "concept": "Legendary First Verbena",
        "nature": "Visionary",
        "essence": "Primordial",
    },
)[0]
lilith.add_source("Tradition Book: Verbena", 65 - 66)

# Calantha - Black Fury Garou Ally
calantha = MtAHuman.objects.get_or_create(
    name="Calantha",
    defaults={
        "description": "A svelte dark-haired woman in black and red with feral grace. A Garou of the "
        "Black Furies tribe, loosely allied with the Verbena on ecological issues. The Black Furies "
        "suffered the same persecutions as the Verbena during the Burning Times.",
        "concept": "Garou Ally",
        "nature": "Survivor",
    },
)[0]
calantha.add_source("Tradition Book: Verbena", 41 - 42)

# ==============================================================================
# CHARACTER TEMPLATES (Chapter 4)
# ==============================================================================

# Template: Avenging Witch
avenging_witch = CharacterTemplate.objects.get_or_create(
    name="Avenging Witch",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "Born angry. Always an outsider. Misunderstood by everyone. You've built a hard shell "
        "around you, and prefer making other people uncomfortable to feeling the pain of their rejection. "
        "You are the reincarnation of a witch killed during the Burning Times. Your old soul cries out for "
        "revenge and magick provides you with the means to take it. You hunt and punish or remove the enemies "
        "of the Verbena. Death is a part of Life.",
        "concept": "Avenging Witch",
        "basic_info": {
            "nature": "FK:Archetype:Deviant",
            "demeanor": "FK:Archetype:Bravo",
            "essence": "FK:Essence:Primordial",
        },
        "attributes": {
            "strength": 3,
            "dexterity": 4,
            "stamina": 3,
            "perception": 2,
            "intelligence": 3,
            "wits": 3,
            "charisma": 1,
            "manipulation": 2,
            "appearance": 3,
        },
        "abilities": {
            "alertness": 2,
            "athletics": 1,
            "awareness": 2,
            "brawl": 2,
            "dodge": 2,
            "intimidation": 3,
            "streetwise": 1,
            "drive": 2,
            "melee": 2,
            "stealth": 2,
            "survival": 2,
            "culture": 1,
            "occult": 3,
        },
        "backgrounds": [
            {"name": "Arcane", "rating": 1},
            {"name": "Avatar", "rating": 2},
            {"name": "Mentor", "rating": 4},
        ],
        "powers": {
            "life": 3,
            "entropy": 1,
            "prime": 2,
            "arete": 3,
        },
        "specialties": ["Occult (Poisons)"],
        "willpower": 5,
        "equipment": "Knife (ritual athame), herbs, cauldron, black witchy clothing",
        "quote": "You believe this knife is purely ceremonial? Come closer. I will show you its true nature.",
        "roleplaying_hints": "Be aggressive. You are not intimidated by any situation and fear no one (except your Mentor). "
        "Act elusive if anyone gets too inquisitive about your business and always try to keep the upper hand. "
        "If someone offends you too much or harms another Verbena, make him pay.",
        "is_official": True,
        "is_public": True,
    },
)[0]
avenging_witch.add_source("Tradition Book: Verbena", 48 - 49)

# Template: Bard
bard = CharacterTemplate.objects.get_or_create(
    name="Bard (Verbena)",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "Born at the wrong time, you should have been a troubadour or an ancient Celtic bard. "
        "Modern life never suited you very well. While other kids were learning to play guitar, you chose Celtic "
        "lap harp. Unicorns and dragons and great heroes who fought terrible battles filled your imagination. "
        "Truth is important, and you always sensed that grownups were lying when they said magic had never existed "
        "in the world. You are a lorekeeper, judge, facilitator and peacekeeper. Your existence keeps one of the "
        "Mythic Threads alive.",
        "concept": "Bard",
        "basic_info": {
            "nature": "FK:Archetype:Judge",
            "demeanor": "FK:Archetype:Visionary",
            "essence": "FK:Essence:Questing",
        },
        "attributes": {
            "strength": 1,
            "dexterity": 3,
            "stamina": 2,
            "perception": 3,
            "intelligence": 4,
            "wits": 3,
            "charisma": 4,
            "manipulation": 2,
            "appearance": 2,
        },
        "abilities": {
            "etiquette": 3,
            "expression": 3,
            "intuition": 2,
            "leadership": 3,
            "meditation": 1,
            "stealth": 1,
            "survival": 1,
            "culture": 3,
            "enigmas": 2,
            "research": 3,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 2},
            {"name": "Dream", "rating": 2},
            {"name": "Library", "rating": 1},
        ],
        "powers": {
            "correspondence": 1,
            "forces": 1,
            "life": 2,
            "mind": 1,
            "prime": 1,
            "time": 1,
            "arete": 2,
        },
        "willpower": 5,
        "equipment": "Lap harp, music books, notebook and pencil (for song and lyric ideas), library of fantasy books",
        "quote": "Hey, have you heard this one? It's a madrigal. What do you mean 'what's a madrigal?'",
        "roleplaying_hints": "You are judge, facilitator and peacekeeper. Always consider both sides of a question "
        "before making a decision. Quote ancient poems and songs. Lead through inspiration and sound judgement. "
        "Your existence keeps one of the Mythic Threads alive. Act like it.",
        "is_official": True,
        "is_public": True,
    },
)[0]
bard.add_source("Tradition Book: Verbena", 50 - 51)

# Template: Eco-Terrorist Druid
druid = CharacterTemplate.objects.get_or_create(
    name="Eco-Terrorist Druid",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "You grew up in the city among towering buildings and garbage-filled alleyways. "
        "At age thirteen, you went to summer camp and experienced the countryside for the first time. "
        "The forest became your personal kingdom. When you settled near the largest forest in the east, "
        "you learned it was being decimated by logging. You joined eco-terrorists trying to stop deforestation "
        "and then met the true guardians of the forest - the Verbena. You are also a Druid. The Druids were "
        "leaders and teachers in the old days.",
        "concept": "Eco-Terrorist Druid",
        "basic_info": {
            "nature": "FK:Archetype:Visionary",
            "demeanor": "FK:Archetype:Fanatic",
            "essence": "FK:Essence:Pattern",
        },
        "attributes": {
            "strength": 1,
            "dexterity": 3,
            "stamina": 4,
            "perception": 4,
            "intelligence": 3,
            "wits": 3,
            "charisma": 2,
            "manipulation": 1,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 2,
            "athletics": 1,
            "brawl": 2,
            "leadership": 2,
            "streetwise": 2,
            "drive": 2,
            "firearms": 1,
            "stealth": 2,
            "survival": 2,
            "technology": 1,
            "medicine": 1,
            "occult": 1,
        },
        "backgrounds": [
            {"name": "Allies", "rating": 2},
            {"name": "Arcane", "rating": 1},
            {"name": "Avatar", "rating": 2},
            {"name": "Influence", "rating": 1},
            {"name": "Node", "rating": 1},
        ],
        "powers": {
            "forces": 1,
            "life": 2,
            "matter": 2,
            "prime": 2,
            "arete": 2,
        },
        "willpower": 6,
        "equipment": "Robes, sickle, packet of seeds, ecology pamphlets",
        "quote": "Humankind is arrogant. We ask 'if a tree falls in the forest and there is no one to hear it fall, "
        "does it make a noise?' as if the tree's only importance were in our relationship to it. The earth, "
        "the other trees, all life within the woods, hears it fall and echoes with the scream of its descent.",
        "roleplaying_hints": "Read up on ecological issues, especially those having to do with the rainforest and "
        "old-growth woodlands. Quote statistics that support the contention that man will denude the planet of trees "
        "within the next fifty years. Remember you are also a Druid. The Druids were leaders and teachers in the old "
        "days. Assume these positions when you can.",
        "is_official": True,
        "is_public": True,
    },
)[0]
druid.add_source("Tradition Book: Verbena", 52 - 53)

# Template: Shapeshifter
shapeshifter = CharacterTemplate.objects.get_or_create(
    name="Shapeshifter (Verbena)",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "Born into a tribal culture, you were almost allowed to die because of your deformity. "
        "Instead those who were more 'civilized' adopted and raised you. Somewhere within you prowled an ancestral "
        "memory - of a sleek cat or a brilliantly plumed bird. You are a 'primitive' tribesperson decked out in "
        "'civilized' costume; always out of place among those who are out of touch with their bodies and emotions. "
        "The deformity which ruled your life has made you more aware of your own carnal nature. You crave perfection "
        "in yourself and are convinced your shapeshifting holds the key to ultimate Ascension.",
        "concept": "Shapeshifter",
        "basic_info": {
            "nature": "FK:Archetype:Survivor",
            "demeanor": "FK:Archetype:Loner",
            "essence": "FK:Essence:Dynamic",
        },
        "attributes": {
            "strength": 3,
            "dexterity": 2,
            "stamina": 4,
            "perception": 3,
            "intelligence": 3,
            "wits": 2,
            "charisma": 2,
            "manipulation": 1,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 2,
            "awareness": 2,
            "brawl": 2,
            "etiquette": 2,
            "intuition": 2,
            "firearms": 1,
            "stealth": 3,
            "survival": 3,
            "culture": 2,
            "occult": 2,
        },
        "backgrounds": [
            {"name": "Arcane", "rating": 2},
            {"name": "Avatar", "rating": 3},
            {"name": "Mentor", "rating": 2},
        ],
        "powers": {
            "life": 2,
            "mind": 1,
            "time": 2,
            "arete": 3,
        },
        "willpower": 10,
        "equipment": "Stretch clothing, camouflage stick, pistol (let the hunter beware)",
        "quote": "Grrowwll...",
        "roleplaying_hints": "The line from C.S. Lewis' Narnia chronicles, 'It's not as if he were a tame lion,' "
        "suits you perfectly. Show the strength, ferocity and gentleness of the panther within you. Move to the "
        "rhythms of traditional chants and drums rather than the pulse of modern life. Walk in grace and beauty. "
        "Always look for ways to perfect yourself. Talk about shifting with anyone who will listen.",
        "is_official": True,
        "is_public": True,
    },
)[0]
shapeshifter.add_source("Tradition Book: Verbena", 54 - 55)

# Template: Healer/Medicine Man
healer = CharacterTemplate.objects.get_or_create(
    name="Healer/Medicine Man",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "You were born on the reservation and lived with your grandfather, a great medicine man. "
        "You feared you lacked the power or wisdom to become a healer like him because you couldn't have visions. "
        "You tried to become a doctor but couldn't get a scholarship. When your grandfather died, you were left "
        "alone with no money, no power and no future. The Verbena came and promised to teach you how to heal. "
        "After nearly a year with no visions while others had them, you returned to the reservation and renewed "
        "yourself with ancient rituals. A vision came at last and you knew you must return to the Verbena to finish "
        "your training. Though not a traditional medicine man who deals with spirits, you are a healer who respects "
        "and understands the old ways.",
        "concept": "Healer/Medicine Man",
        "basic_info": {
            "nature": "FK:Archetype:Visionary",
            "demeanor": "FK:Archetype:Caregiver",
            "essence": "FK:Essence:Pattern",
        },
        "attributes": {
            "strength": 2,
            "dexterity": 3,
            "stamina": 3,
            "perception": 3,
            "intelligence": 5,
            "wits": 2,
            "charisma": 2,
            "manipulation": 2,
            "appearance": 2,
        },
        "abilities": {
            "alertness": 2,
            "brawl": 2,
            "intuition": 1,
            "meditation": 2,
            "streetwise": 1,
            "survival": 1,
            "culture": 2,
            "enigmas": 1,
            "medicine": 4,
            "occult": 2,
        },
        "backgrounds": [
            {"name": "Avatar", "rating": 3},
            {"name": "Destiny", "rating": 3},
            {"name": "Talisman", "rating": 1},
        ],
        "powers": {
            "entropy": 1,
            "life": 3,
            "prime": 2,
            "arete": 3,
        },
        "willpower": 5,
        "equipment": "Herbs, first aid kit, medicine bag (Talisman), knife",
        "quote": "Let me tell you of my vision.",
        "roleplaying_hints": "Although you have embraced modern medicine and the Verbena way of magick, you are more "
        "than half shaman. Quote heavily from great medicine men of the past. Walk softly on the Earth. She is your "
        "Mother. You hold the powers of life and death in your hands. Use that power wisely. Hold to the others in "
        "your cabal as though they were your tribe. They are.",
        "is_official": True,
        "is_public": True,
    },
)[0]
healer.add_source("Tradition Book: Verbena", 56 - 57)

# Template: Neo-Pagan
neo_pagan = CharacterTemplate.objects.get_or_create(
    name="Neo-Pagan",
    gameline="mta",
    defaults={
        "character_type": "mage",
        "description": "Raised in a home without joy or love, only duty - to parents, religion, and school - "
        "you couldn't believe in the all-powerful, cruel God they said ruled your every thought. Praise was rare; "
        "punishment swift. What was wrong with dancing or listening to loud music or hanging out with other kids? "
        "Secretly, you tried all the things your parents forbade. And God didn't strike you down. Dancing and singing "
        "made you happy. Being kind rather than competitive brought you joy. When your sister was murdered, your parents' "
        "rage pushed you too far. A group of pagans welcomed you and encouraged you to join. You left home and never "
        "looked back, learning about love, sharing - and self-defense. You fervently believe in the Goddess and all "
        "Her blessings.",
        "concept": "Neo-Pagan",
        "basic_info": {
            "nature": "FK:Archetype:Architect",
            "demeanor": "FK:Archetype:Conformist",
            "essence": "FK:Essence:Questing",
        },
        "attributes": {
            "strength": 1,
            "dexterity": 3,
            "stamina": 2,
            "perception": 3,
            "intelligence": 2,
            "wits": 3,
            "charisma": 4,
            "manipulation": 2,
            "appearance": 4,
        },
        "abilities": {
            "etiquette": 2,
            "expression": 2,
            "leadership": 1,
            "meditation": 1,
            "stealth": 1,
            "survival": 2,
            "culture": 1,
            "enigmas": 1,
            "occult": 1,
        },
        "backgrounds": [
            {"name": "Allies", "rating": 2},
            {"name": "Avatar", "rating": 3},
            {"name": "Dream", "rating": 2},
        ],
        "powers": {
            "forces": 1,
            "life": 3,
            "mind": 1,
            "prime": 1,
            "arete": 3,
        },
        "specialties": ["Expression (Dancing)", "Occult (High Ritual)"],
        "willpower": 5,
        "equipment": "Athame, wand, robes, candles, bell, crystal, herbs, cauldron, astrology book",
        "quote": "Come to our festival. There's something there for everyone. The Goddess holds all her children in equal regard.",
        "roleplaying_hints": "You fervently believe in the Goddess and all Her blessings. Tell everyone about them. "
        "Schedule your life around the pagan festivals and make sure everyone knows you do so. Call strangers 'sister' "
        "and 'brother.' Be friendly and supportive unless you feel like you're being taken advantage of, then warn the "
        "sleazeball of the Goddess' wrath when crossed.",
        "is_official": True,
        "is_public": True,
    },
)[0]
neo_pagan.add_source("Tradition Book: Verbena", 58 - 59)

# ==============================================================================
# PRACTICES (Verbena-specific magical styles)
# ==============================================================================

# Verbena-specific practices mentioned in the rotes
Practice.objects.get_or_create(name="Blood Magic")
Practice.objects.get_or_create(name="Herbalism")
Practice.objects.get_or_create(name="Shapeshifting")
Practice.objects.get_or_create(name="Weather Working")
Practice.objects.get_or_create(name="Bardic Voice")
Practice.objects.get_or_create(name="Circle Casting")

print("Verbena Tradition Book data loaded successfully!")
print(f"  - Book: {verbena_book.name}")
print(f"  - Effects: 8 rotes")
print(f"  - Characters: 9 named NPCs")
print(f"  - Templates: 6 character templates")
