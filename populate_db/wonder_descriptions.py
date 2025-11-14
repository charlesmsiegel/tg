# Wonder Descriptions and Effects
# This file adds descriptions and magical effects to wonders defined in wonders_INC.py
# Information extracted from Mage: The Ascension source books

from items.models.mage.artifact import Artifact
from items.models.mage.talisman import Talisman
from characters.models.mage.effect import Effect

# Create effects for wonders

# Dragon Pearls - Akashic Brotherhood artifact
# Quintessence channeling conduits
dragon_pearl_effect = Effect.objects.get_or_create(
    name="Quintessence Channeling (Dragon Pearls)",
    prime=3,
    description="Channels and stores Quintessence, allowing the user to draw upon mystical energies for spellcasting. Acts as a conduit for Prime energy.",
)[0]

dragon_pearls = Artifact.objects.get(name="Dragon Pearls")
dragon_pearls.description = """These sacred pearls are treasured artifacts of the Akashic Brotherhood, serving as powerful Quintessence channeling conduits. Formed through decades of meditation and prime energy manipulation, each pearl contains crystallized enlightenment. The pearls glow with an inner light when filled with Quintessence, and skilled practitioners can draw upon this stored energy to fuel their magical workings. They are often worn as prayer beads or carried in silk pouches."""
dragon_pearls.power = dragon_pearl_effect
dragon_pearls.save()

# Antaratma - Euthanatos talisman
# Resists Quiet, provides Willpower for casting
antaratma_effect = Effect.objects.get_or_create(
    name="Quiet Resistance (Antaratma)",
    mind=3,
    prime=2,
    spirit=2,
    description="Provides resistance to Quiet and madness. Grants 1 level of Quiet resistance per 2 successes on Arete roll. Can provide a Willpower point for casting once per day.",
)[0]

antaratma = Talisman.objects.get(name="Antaratma")
antaratma.description = """The Antaratma is a sacred talisman of the Euthanatos Tradition, designed to protect the wielder from the madness of Quiet that can afflict mages who peer too deeply into the Wheel of Ages. Crafted through complex rituals involving Spirit, Mind, and Prime magicks, this talisman appears as an ornate silver medallion inscribed with Sanskrit mantras and symbols of the eternal wheel. When activated, it provides 1 level of Quiet resistance per 2 successes rolled on the user's Arete. Additionally, once per day, the Antaratma can provide a single Willpower point to fuel spellcasting, drawing on the stored spiritual energy within."""
antaratma.save()
antaratma.powers.add(antaratma_effect)

# Dümerang Blade - Order of Hermes boomerang weapon
dumerang_effect = Effect.objects.get_or_create(
    name="Returning Weapon (Dümerang Blade)",
    forces=2,
    correspondence=2,
    prime=2,
    description="Enchanted boomerang that automatically returns to the wielder's hand after being thrown. The blade auto-regenerates its Arete rating daily. Can be used as both melee and ranged weapon.",
)[0]

for arete_level in [2, 3, 4]:
    dumerang = Talisman.objects.get(name=f"Dümerang Blade ({arete_level})")
    dumerang.description = f"""This enchanted weapon appears as an elegant boomerang blade with Hermetic sigils etched along its curved edge. Created by the Order of Hermes, the Dümerang Blade is a masterwork of Forces and Correspondence magick that allows it to return unerringly to its wielder's hand after being thrown. The blade is perfectly balanced for both melee combat and ranged attacks.

The Dümerang Blade has an Arete rating of {arete_level} which automatically regenerates each day, allowing the wielder to channel Quintessence through the weapon. When thrown, the blade traces an arc through the air, striking its target before curving back to the wielder's waiting hand. Masters of the blade can throw it through impossible trajectories, having it strike multiple opponents or navigate around obstacles.

The weapon deals Strength + 2 lethal damage in melee and Strength + 1 lethal damage when thrown (range 20 yards). Some versions of the blade were crafted as automotive ignition keys, with the pommel serving as a hood ornament when not in use."""
    dumerang.save()
    dumerang.powers.add(dumerang_effect)

# Candle of Communion - Verbena talisman
candle_effect = Effect.objects.get_or_create(
    name="Spirit Communion (Candle)",
    spirit=3,
    mind=2,
    prime=2,
    description="When lit, this candle opens a channel of communication with spirits, ancestors, and entities in the Umbra. The flickering flame creates a beacon visible in both the physical and spirit worlds, attracting helpful spirits and allowing for clearer communion.",
)[0]

for arete_level in [1, 2, 3]:
    candle = Talisman.objects.get(name=f"Candle of Communion ({arete_level})")
    candle.description = f"""A hand-crafted ritual candle, typically made from beeswax infused with sacred herbs and oils. The Candle of Communion is a staple tool among Verbena practitioners, particularly those who work with spirits and ancestors. When lit with proper ritual intent, the candle's flame becomes a beacon in both the physical world and the Umbra, opening channels of communication.

The candle (Arete {arete_level}) glows with an otherworldly light when activated, and spirits are drawn to its warmth. The practitioner can speak with entities across the Gauntlet, receive messages from ancestors, or even attract helpful spirits to aid in magical workings. The quality of communion depends on the candle's Arete rating - lower rated candles provide vaguer, more symbolic communication, while higher rated ones allow for clearer dialogue.

Each candle typically provides several hours of burn time, and master crafters can create candles with specific attunements to particular types of spirits or ancestors."""
    candle.save()
    candle.powers.add(candle_effect)

# Mama Cybele's Tea Collection - Verbena talisman
tea_heal_effect = Effect.objects.get_or_create(
    name="Herbal Healing (Tea)",
    life=3,
    prime=2,
    description="Magically enhanced herbal tea that promotes healing and well-being. Different blends can cure ailments, grant visions, provide energy, or offer protection.",
)[0]

tea_enhance_effect = Effect.objects.get_or_create(
    name="Herbal Enhancement (Tea)",
    life=2,
    mind=1,
    description="Herbal tea that temporarily enhances physical or mental capabilities, or provides prophetic dreams and insights.",
)[0]

for arete_level in [2, 3, 4, 5]:
    tea = Talisman.objects.get(name=f"Mama Cybele's Tea Collection ({arete_level})")
    tea.description = f"""Mama Cybele is a renowned Verbena herbalist whose tea collection has become legendary among the Traditions. Each blend in her collection is carefully crafted from rare herbs, flowers, and other natural ingredients, infused with Life and Prime magick to create powerful healing and enhancement effects.

This tea collection (Arete {arete_level}) contains numerous blends, each with different properties:
- **Healing Blend**: Accelerates natural healing, can cure diseases
- **Dreaming Tea**: Grants prophetic visions and insights during sleep
- **Vitality Brew**: Provides sustained energy without the crash of mundane stimulants
- **Protection Tisane**: Strengthens the body's natural defenses
- **Clarity Infusion**: Sharpens the mind and enhances mental acuity

The teas are typically prepared with proper ritual - water blessed under appropriate moon phases, steeped for specific durations while chanting, and consumed with mindful intent. Higher Arete collections contain rarer and more potent blends capable of more dramatic effects.

The collection is usually stored in an antique wooden box with individual compartments for each blend, labeled in Mama Cybele's flowing script."""
    tea.save()
    tea.powers.add(tea_heal_effect)
    tea.powers.add(tea_enhance_effect)

# Grand Book of Shadows - Verbena grimoire/talisman
book_power_effect = Effect.objects.get_or_create(
    name="Mystical Grimoire Power (Book of Shadows)",
    prime=3,
    spirit=2,
    mind=2,
    description="A living grimoire that stores knowledge, spells, and mystical power. Can function as a Familiar, offering advice and magical assistance. Contains centuries of Verbena wisdom and practices.",
)[0]

for arete_level in [4, 5, 6, 7, 8]:
    # Check if this version exists
    book_name = f"Grand Book of Shadows ({arete_level})"
    if Talisman.objects.filter(name=book_name).exists():
        book = Talisman.objects.get(name=book_name)
        book.description = f"""The Grand Book of Shadows is a magnificent leather-bound tome that serves as both grimoire and mystical artifact for a Verbena coven. Bound in aged leather and inscribed with symbols of the Goddess and God, this book is more than just a repository of spells - it is a living record of the coven's practices, history, and collective wisdom.

The book (Arete {arete_level}) typically resides on a central altar and is treated with great reverence. Each page contains hand-written entries from generations of witches, detailing rituals, herb lore, spell formulae, and mystical insights. The book itself has absorbed so much magical energy over the years that it has developed a quasi-sentient awareness.

Many Grand Books of Shadows can function as Familiars (see Familiar Background), offering guidance, warning of danger, or even refusing to open if a non-initiate attempts to read it. The book can:
- Store and organize magical knowledge
- Teach new spells and rituals to worthy students
- Provide mystical insights and guidance
- Generate protective wards when placed on an altar
- Record magical workings automatically when they occur nearby

The book grows more powerful as it ages, accumulating wisdom and Quintessence. Some of the oldest examples are considered irreplaceable treasures of their Traditions, containing lost knowledge and unique spell variants found nowhere else."""
        book.save()
        book.powers.add(book_power_effect)

# Angel Tear Daggers - mentioned in Lore of the Traditions p.49
angel_dagger_effect = Effect.objects.get_or_create(
    name="Blessed Blade (Angel Tears)",
    prime=2,
    spirit=2,
    forces=1,
    description="Daggers forged from crystallized tears of angels (or so the legend claims). Highly effective against demonic and infernal entities, dealing aggravated damage to such beings. The blades glow with soft silver light when evil is near.",
)[0]

angel_daggers = Artifact.objects.get(name="Angel Tear Daggers")
angel_daggers.description = """These paired daggers are forged from a mysterious crystalline substance said to be the solidified tears of angels. Whether this origin is literal or metaphorical, the daggers possess undeniable holy power. The translucent blades shimmer with an inner radiance, glowing softly in the presence of evil or infernal entities.

The Angel Tear Daggers are particularly prized by mages who hunt demons, Nephandi, and other creatures of darkness. Against such beings, the daggers deal aggravated damage and ignore certain forms of supernatural protection. The blades also provide a warning system - they glow more brightly as evil draws near, with intensity proportional to the threat level.

Each dagger deals Strength + 1 lethal damage normally, or Strength + 2 aggravated damage against infernal entities. The daggers can store up to 10 points of Quintessence and are often carried by Celestial Chorus members and other mages who battle dark forces. Legend holds that they were gifts from a repentant demon who wished to aid humanity's struggle against the Infernal."""
angel_daggers.power = angel_dagger_effect
angel_daggers.save()

# Game of Senet - Ancient Egyptian board game artifact
senet_effect = Effect.objects.get_or_create(
    name="Fate Game (Senet)",
    entropy=2,
    time=1,
    description="An ancient Egyptian board game that can divine fate and fortune. Playing the game allows glimpses into probability streams and potential futures.",
)[0]

senet = Artifact.objects.get(name="Game of Senet")
senet.description = """The Game of Senet is an ancient Egyptian board game that predates most modern forms of divination. This particular set is more than just a game - it is a tool for reading fate and probability. The board is made of aged sycamore wood with squares of ivory and ebony, and the playing pieces are carved from semiprecious stones.

When two players engage in a proper ritual game of Senet, the movements of the pieces across the board trace the paths of probability and fate. Skilled practitioners can read these patterns to divine future events, understand the consequences of different choices, or identify opportune moments for action. The game requires at least one hour of focused play to produce meaningful divination results.

The Senet board also serves as a focus for Entropy magic, making it easier to manipulate probability or read the threads of fate. Some versions of the game are said to be gateways to the Duat (Egyptian underworld), allowing communication with the deceased or spirits of ancient Egypt."""
senet.power = senet_effect
senet.save()

# Imphepho Wierook - South African Dreamspeaker incense
imphepho_effect = Effect.objects.get_or_create(
    name="Ancestral Incense (Imphepho)",
    spirit=2,
    mind=1,
    prime=1,
    description="Sacred incense that opens channels to the ancestors and spirits. The smoke carries prayers and messages to the spirit world while inviting ancestral guidance and protection.",
)[0]

imphepho = Artifact.objects.get(name="Imphepho Wierook")
imphepho.description = """Imphepho (Helichrysum petiolare) is a sacred plant used in southern African traditional practices, particularly among the Xhosa and Zulu peoples. This specially prepared wierook (incense) has been blessed by Dreamspeaker shamans to enhance its natural spiritual properties.

When burned, the aromatic smoke of Imphepho creates a bridge between the physical and spirit worlds. The smoke carries prayers, requests, and offerings to the ancestors and spirits, while simultaneously inviting their presence and guidance into the ritual space. Practitioners often use Imphepho before important decisions, healing work, or when seeking ancestral wisdom.

The incense enhances spiritual perception, making it easier to sense the presence of spirits and receive their messages. It also provides a degree of protection, as malevolent spirits typically avoid the sacred smoke. A complete bundle provides enough Imphepho for approximately 10-15 ritual burnings. The incense can store up to 15 points of Quintessence and is particularly effective when combined with other Spirit-focused rituals."""
imphepho.power = imphepho_effect
imphepho.save()

# Waidan Ding - Chinese alchemical cauldron
ding_effect = Effect.objects.get_or_create(
    name="Alchemical Vessel (Ding)",
    matter=3,
    prime=2,
    forces=1,
    description="An alchemical cauldron used for transmutation and the creation of elixirs. Enhances all alchemical workings and can transmute base materials into more refined substances.",
)[0]

ding = Artifact.objects.get(name="Waidan Ding")
ding.description = """The Waidan Ding is a three-legged bronze cauldron used in Chinese external alchemy (waidan). This particular ding has been used in countless alchemical operations over centuries, absorbing magical resonance until it became a Wonder in its own right. The vessel is inscribed with Taoist trigrams and dragons, and it shows the patina of great age.

The ding serves as both container and catalyst for alchemical transmutations. When used in the creation of elixirs, talismans, or other alchemical products, it reduces the difficulty of the working and can improve the quality of the final product. The cauldron is particularly suited for:
- Creating medicinal elixirs and potions
- Transmuting base metals toward gold
- Purifying substances to reveal their quintessential nature
- Brewing longevity formulas
- Crafting alchemical Tass

The ding can store up to 10 points of Quintessence, which it draws from when aiding alchemical processes. Practitioners typically consecrate the vessel before each major working, and the greatest respect is shown when cleaning it, as the residue from past operations contributes to its power. This particular ding is associated with the Wu Lung tradition of Chinese sorcerers."""
ding.power = ding_effect
ding.save()

print("Wonder descriptions and effects have been added successfully!")
