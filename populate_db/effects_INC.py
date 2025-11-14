# M20 Jumpstart Common Magickal Effects
from characters.models.mage.effect import Effect

Effect.objects.get_or_create(name="Adapt to Environment (Self)", life=2)
Effect.objects.get_or_create(name="Adapt to Environment (Other)", life=3)
Effect.objects.get_or_create(name="Animate Corpse or Parts", life=2, prime=2)
Effect.objects.get_or_create(name="Cause Disease (Self)", life=2)
Effect.objects.get_or_create(name="Cure Disease (Self)", life=2)
Effect.objects.get_or_create(name="Cause Disease (Other)", life=3)
Effect.objects.get_or_create(name="Cure Disease (Other)", life=3)
Effect.objects.get_or_create(name="Cosmetic Alteration", life=3)
Effect.objects.get_or_create(name="Create Body (Simple)", life=2, prime=2)
Effect.objects.get_or_create(name="Create Body (Complex)", life=5, prime=2)
Effect.objects.get_or_create(name="Duplicate Body", life=5, prime=2)
Effect.objects.get_or_create(name="Grow New Limbs or Other Features (Self)", life=3)
Effect.objects.get_or_create(name="Grow New Limbs or Other Features (Other)", life=4)
Effect.objects.get_or_create(name="Harm Living Being (Simple)", life=2)
Effect.objects.get_or_create(name="Heal Living Being (Simple)", life=2)
Effect.objects.get_or_create(name="Harm Living Being (Complex)", life=3)
Effect.objects.get_or_create(name="Heal Living Being (Complex)", life=3)
Effect.objects.get_or_create(name="Heal Fae", life=3, mind=3)
Effect.objects.get_or_create(name="Harm Fae", life=3, mind=3)
Effect.objects.get_or_create(name="Heal Vampire", life=3, matter=2)
Effect.objects.get_or_create(name="Harm Vampire", life=3, matter=2)
Effect.objects.get_or_create(name="Heal Werecreature", life=3, spirit=2)
Effect.objects.get_or_create(name="Harm Werecreature", life=3, spirit=2)
Effect.objects.get_or_create(name="Increase Physique/Traits (Self)", life=3)
Effect.objects.get_or_create(name="Increase Physique/Traits (Other)", life=4)
Effect.objects.get_or_create(name="Increase Speed", time=3)
Effect.objects.get_or_create(name="Reduce Speed", time=3)
Effect.objects.get_or_create(name="Revive Recently Dead", life=4, spirit=4, prime=3)
Effect.objects.get_or_create(name="Rot Body (Entropy)", entropy=4)
Effect.objects.get_or_create(name="Rot Body (Life)", life=4)
Effect.objects.get_or_create(name="Shapeshift (Self)", life=4)
Effect.objects.get_or_create(name="Shapeshift (Other)", life=5)
Effect.objects.get_or_create(name="Soak Aggravated Damage", life=3)
Effect.objects.get_or_create(
    name="Transform into Element (Earth, Metal, Water)", life=3, matter=3
)[0]
Effect.objects.get_or_create(name="Transform into Element (Wood)", life=3)
Effect.objects.get_or_create(
    name="Transform into Element (Air, Fire)", life=3, forces=3
)
Effect.objects.get_or_create(name="Alter Probability", entropy=2)
Effect.objects.get_or_create(name="Bless", entropy=3, life=3)
Effect.objects.get_or_create(name="Curse", entropy=3, life=3)
Effect.objects.get_or_create(name="Cause Decay", entropy=3)[0]  # entropy 3+ variants
Effect.objects.get_or_create(name="Spot Flaws", entropy=1)
Effect.objects.get_or_create(name="Call Storm", forces=4, prime=2)
Effect.objects.get_or_create(name="Conjure Element (Fire, Wind)", forces=3, prime=2)
Effect.objects.get_or_create(
    name="Conjure Element (Earth, Metal, Water)", matter=3, prime=2
)
Effect.objects.get_or_create(name="Conjure Element (Wood)", life=3, prime=2)
Effect.objects.get_or_create(name="Conjure New Object", matter=3, prime=2)[
    0
]  # matter 3+ variants
Effect.objects.get_or_create(name='Conjure "Physical" Illusion', forces=2, prime=2)[
    0
]  # forces 2+ variants
Effect.objects.get_or_create(name="Direct Existing Elements", forces=2)[
    0
]  # forces 2+ variants
Effect.objects.get_or_create(name="Disintegrate Object (Matter)", matter=3)
Effect.objects.get_or_create(
    name="Disintegrate Object (Entropy/Time)", entropy=3, time=3
)
Effect.objects.get_or_create(name="Invisibility Field", forces=2)
Effect.objects.get_or_create(name="Silence Field", forces=2)
Effect.objects.get_or_create(name="Invisibility on Living Being", forces=2, life=2)
Effect.objects.get_or_create(name="Levitation (Forces)", forces=2)
Effect.objects.get_or_create(
    name="Levitation (Correspondence)", correspondence=3, matter=2
)
Effect.objects.get_or_create(name="Flying (Forces)", forces=2)
Effect.objects.get_or_create(name="Flying (Correspondence)", correspondence=3, life=2)
Effect.objects.get_or_create(name="Speed Velocity", forces=2)[0]  # forces 2+ variants
Effect.objects.get_or_create(name="Slow Velocity", forces=2)[0]  # forces 2+ variants
Effect.objects.get_or_create(name="Transform Objects", matter=2)[
    0
]  # matter 2+ variants and other target thing spheres
Effect.objects.get_or_create(name="Transform Forces", forces=3)[
    0
]  # forces 3+ variants and other target thing spheres
Effect.objects.get_or_create(name="Astral Projection", mind=4)
Effect.objects.get_or_create(name="Clairvoyance", correspondence=2)[
    0
]  # Mind 3/Corr 2 variant, why?
Effect.objects.get_or_create(name="Conceal Aura (Mind)", mind=1)
Effect.objects.get_or_create(name="Conceal Aura (Prime)", mind=2)
Effect.objects.get_or_create(name="Alter Aura (Mind)", mind=1)
Effect.objects.get_or_create(name="Alter Aura (Prime)", mind=2)
Effect.objects.get_or_create(name="Conceal Avatar", spirit=2, mind=1)
Effect.objects.get_or_create(name="Conceal Thoughts", mind=1)
Effect.objects.get_or_create(name="Conjure Mental Illusions", mind=2)[
    0
]  # Mind 2+ variants
Effect.objects.get_or_create(name="Influence Mood", mind=2)
Effect.objects.get_or_create(name="Influence Subconscious", mind=3)[
    0
]  # Mind 3+ variants
Effect.objects.get_or_create(name="Mind Control", mind=4)
Effect.objects.get_or_create(name="Prophecy", time=2)[0]  # why mind 2/time 2?
Effect.objects.get_or_create(name="Hindsight", time=2)[0]  # why mind 2/time 2?
Effect.objects.get_or_create(name="Scramble Thoughts", mind=3)
Effect.objects.get_or_create(name="See Through Another's Eyes", mind=3)
Effect.objects.get_or_create(name="Sense Energies (Correspondence)", correspondence=1)
Effect.objects.get_or_create(name="Sense Energies (Time)", time=1)
Effect.objects.get_or_create(name="Sense Energies (Spirit)", spirit=1)
Effect.objects.get_or_create(name="Sense Energies (Matter)", matter=1)
Effect.objects.get_or_create(name="Sense Energies (Forces)", forces=1)
Effect.objects.get_or_create(name="Sense Energies (Life)", life=1)
Effect.objects.get_or_create(name="Sense Energies (Entropy)", entropy=1)
Effect.objects.get_or_create(name="Sense Energies (Mind)", mind=1)
Effect.objects.get_or_create(name="Sense Energies (Prime)", prime=1)
Effect.objects.get_or_create(name="Share Perception", mind=1)[
    0
]  # separate variants for other spheres?
Effect.objects.get_or_create(name="Shield Mind (Other)", mind=2)
Effect.objects.get_or_create(name="Tear Mind Apart", mind=3)
Effect.objects.get_or_create(name="Tear Mind Apart (Aggravated)", mind=3, life=3)
Effect.objects.get_or_create(name="Telepathy", mind=3)
Effect.objects.get_or_create(name="Telekinesis", forces=2)[0]  # forces 2+ variants
Effect.objects.get_or_create(name="Translate Languages", mind=3)
Effect.objects.get_or_create(name="Translate Languages (Group)", mind=3, forces=2)
Effect.objects.get_or_create(name="Absorb Quintessence", prime=3)
Effect.objects.get_or_create(name="Channel Quintessence", prime=3)
Effect.objects.get_or_create(name="Destroy by Draining Quintessence (Object)", prime=4)
Effect.objects.get_or_create(
    name="Destroy by Draining Quintessence (Creature)", prime=5
)
Effect.objects.get_or_create(name="Drain Node", prime=4)
Effect.objects.get_or_create(name="Drain Quintessence", prime=3)
Effect.objects.get_or_create(name="Fuel New Pattern", prime=2)[
    0
]  # variants add appropriate spheres
Effect.objects.get_or_create(name="Share/Exchange Quintessence", prime=3)
Effect.objects.get_or_create(name="Command Spirit", mind=4, spirit=4)
Effect.objects.get_or_create(name="Conjure Spirit", spirit=3)
Effect.objects.get_or_create(name="Drain Spirit's Essence", prime=4, spirit=4)
Effect.objects.get_or_create(name="Harm Spirit/Wraith", spirit=3)
Effect.objects.get_or_create(name="Open Gateway", spirit=4)
Effect.objects.get_or_create(name="Close Gateway", spirit=4)
Effect.objects.get_or_create(name="See Spirits", spirit=1)
Effect.objects.get_or_create(name="Speak to Spirits", spirit=2)
Effect.objects.get_or_create(name="Step Sideways", spirit=3)
Effect.objects.get_or_create(name="Touch Spirit", spirit=2)
Effect.objects.get_or_create(name="Affect Distant Object/Being", correspondence=2)[
    0
]  # Correspondence 2+ variants
Effect.objects.get_or_create(name="Aging (Living Being)", time=3, life=4)[
    0
]  # Time 3+ variants
Effect.objects.get_or_create(name="Reversing Age (Living Being)", time=3, life=4)[
    0
]  # Time 3+ variants
Effect.objects.get_or_create(name="Aging (Object)", time=3, matter=2)[
    0
]  # Time 3+ variants
Effect.objects.get_or_create(name="Reversing Age (Object)", time=3, matter=2)[
    0
]  # Time 3+ variants
Effect.objects.get_or_create(name="Conjure Earthly Being", correspondence=4, life=2)
Effect.objects.get_or_create(
    name="Create Multiple Images (Correspondence)", correspondence=3, prime=2
)[0]
Effect.objects.get_or_create(name="Create Multiple Images (Forces)", forces=2, prime=2)[
    0
]  # forces 2+ variants
Effect.objects.get_or_create(
    name="Create Multiple Objects", correspondence=5, matter=3, prime=2
)[0]
Effect.objects.get_or_create(name="Open Gateway Between Locations", correspondence=4)
Effect.objects.get_or_create(name="Rewind Time", time=3)
Effect.objects.get_or_create(name="Set Time Trigger", time=4)
Effect.objects.get_or_create(name="Teleport (Self)", correspondence=3)
Effect.objects.get_or_create(name="Teleport (Other)", correspondence=4)
Effect.objects.get_or_create(name="Time Travel", time=5)

# M20 Effects
Effect.objects.get_or_create(name="Bullet-Catch", time=3, forces=2, life=2)
Effect.objects.get_or_create(name="Astral Sojourn", mind=4, spirit=3, prime=2)
Effect.objects.get_or_create(name="Agama Re", entropy=4, life=2, spirit=3)
Effect.objects.get_or_create(name="Agama Te", entropy=4, life=3, spirit=4)
Effect.objects.get_or_create(name="Astral Agama", entropy=5, mind=5, spirit=3)
Effect.objects.get_or_create(name="Suggest Sleep", mind=2)
Effect.objects.get_or_create(name="Compel Sleep", mind=4)
Effect.objects.get_or_create(name="Make Tired", life=3)
Effect.objects.get_or_create(name="Create Wonder", prime=4)
Effect.objects.get_or_create(name="Create Fetish (Willing)", prime=4)
Effect.objects.get_or_create(name="Create Fetish (Unwilling)", spirit=4)
Effect.objects.get_or_create(name="Create Periapt", matter=4)
Effect.objects.get_or_create(name="Create Souflower", life=5, prime=3)
Effect.objects.get_or_create(name="Creat Trinket", prime=2)
Effect.objects.get_or_create(name="Mental Illusions that Inflict Damage", mind=3)
Effect.objects.get_or_create(name="Immersive Illusions", forces=4, mind=4, prime=4)
Effect.objects.get_or_create(name="Awaken Object's Spirit", spirit=3)
Effect.objects.get_or_create(name="Harm Ghost", entropy=3, prime=2)
Effect.objects.get_or_create(name="Perfect Object", matter=3)
Effect.objects.get_or_create(name="Consecrate", prime=2)
Effect.objects.get_or_create(name="Ward/Ban", correspondence=2, prime=2)[
    0
]  # Corr/PRime 2+ variant, plus appropriate spheres at 2+
Effect.objects.get_or_create(name="Astral Body of Light", mind=4, spirit=3, prime=2)
Effect.objects.get_or_create(name="Enter a Dream", mind=3)
Effect.objects.get_or_create(name="See Avatar", mind=3, prime=2, spirit=1)
Effect.objects.get_or_create(name="See Through Mental Illusions", mind=4)
Effect.objects.get_or_create(name="Shield Mind (Self)", mind=1)
Effect.objects.get_or_create(name="Create New Node", prime=5)
Effect.objects.get_or_create(name="Create Quintessence Weapon", prime=3)
Effect.objects.get_or_create(name="Employ Periapt", prime=2)
Effect.objects.get_or_create(name="Enchant Object", prime=2)
Effect.objects.get_or_create(name="Energize Periapt", prime=3)
Effect.objects.get_or_create(name="Nullify Paradox", prime=5)
Effect.objects.get_or_create(name="Refine Tass", prime=4)
Effect.objects.get_or_create(name="Tap Wellspring", prime=4)
Effect.objects.get_or_create(name="Body of Light", prime=2)

# How Do You DO That?
# Book of Secrets
Effect.objects.get_or_create(
    name="The Branding Effect", spirit=3, life=3, mind=2, prime=3
)
Effect.objects.get_or_create(
    name="The Branding Effect (Expirating)", spirit=3, life=3, mind=2, prime=3, time=4
)[0]
Effect.objects.get_or_create(
    name="The Branding Effect (Avatar Brand)", spirit=4, life=3, mind=2, prime=3
)[0]
Effect.objects.get_or_create(
    name="The Branding Effect (Glowing)", spirit=3, life=3, mind=2, prime=3, forces=3
)[0]

Effect.objects.get_or_create(name="Gilgul", spirit=5, entropy=5, mind=5, prime=5)
Effect.objects.get_or_create(
    name="Gilgul (Aggravated Damage)", spirit=5, entropy=5, mind=5, prime=5, life=3
)[0]
Effect.objects.get_or_create(
    name="Gilgul (Body to Dust)", spirit=5, entropy=5, mind=5, prime=5, life=5
)[0]
Effect.objects.get_or_create(
    name="Gilgul (Scattered Body to Dust)",
    spirit=5,
    entropy=5,
    mind=5,
    prime=5,
    life=5,
    forces=3,
    correspondence=5,
)[0]

# Gods and Monsters
# Book of the Fallen
# Technocracy: Reloaded
# Rich Bastard's Guide to Magick
# T:R Quickstart
# Operative's Dossier
# Lore of the Traditions
# M20 Victorian Age
# Le Prix à Payer
# Rouen Brûle t elle

# Enlightend Grimoire
Effect.objects.get_or_create(
    name="Balance the Scales",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Blight/Farmer's Favor",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Luck's Blessing/Curse",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Luck of the Lotus",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Nanburbu",
    correspondence=2,
    time=0,
    spirit=3,
    matter=0,
    life=2,
    forces=0,
    entropy=4,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Threefold Return",
    correspondence=0,
    time=4,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ansu Ishten",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Banishing Blessing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Baptism Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Beginner's Luck",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bless the Heavenly Flower",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=4,
    forces=0,
    entropy=5,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bum a Dollar From the Universe",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Buzzwords",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Caesar's Due",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Epiphany of the Muse",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Games of Luck",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Luck Be a Lady Tonight",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Masquerade to Adulthood",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Midwife's Blessing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Nobody Dies in Vegas",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Reflecting Bane",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shishipat's Favor",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Waiting to Exhale",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Weeping for Tammuz",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wurnan Blessing",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ace of Diamonds",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Actively Actuarial",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Death Curse",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Death Wish",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Learn-It",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Rival's Curse",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sha'ir's Sentence",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=3,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spoiling",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Statistical Mechanics",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Vext",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Brand (the Rawhide Effect)",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=2,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Create Virtual Object/Create Daemon",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Digital Disruption",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Doe's Password",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Encode",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Energy Transformation",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=4,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Feedback",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="FIRP",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=3,
    entropy=4,
    mind=5,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Fractal Encryption",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=3,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Hardware Entry",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Information Superhighway",
    correspondence=2,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Instant Offline",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Online Virus Transmitter Program",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=2,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Overwrite",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=3,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Parallax",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Restrict Sector",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="TechnoVision",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=1,
    mind=1,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Virtual Talisman Transmogrification",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Webcrawlers",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Boot Buzzer",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Burn Out",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="FOR NEXT Loop",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Red Button",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=3,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="System Crash",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="System Havoc",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="That Rascal Puff",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Black Card/Little Black Box",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Captain's Treasure",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Core Dump",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Disk-Doctor",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=3,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="DRM",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Encrypt",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Graphic Transmission",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hacker's Glance",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Intel",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mental Interface",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Remote Access",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Virtual Lockpick",
    correspondence=1,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="AI (Artificial Intelligence)",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=5,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Audience of Inanna",
    correspondence=2,
    time=1,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Personal Assistant Software",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=5,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Psychic Interface",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Remote Programming",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Book of Whispers",
    correspondence=0,
    time=3,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Crowd Surfing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Eavesdropper",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="High-Definition",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Monitor Communications",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Nearest and Dearest",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Phone Tap",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="PIN Drop",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Squaring the Circle",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Surveillance",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Telescreen",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tracking Device",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Adad",
    correspondence=2,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Chaos Butterfly",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Contemplation",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dogon Divination",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Find the Lost",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Istar",
    correspondence=3,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Laying on of Hands",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lighting the Path",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Read the Lightning",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Samas",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Search Engine",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Silent Promise of the Spring Tortoise",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sin",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Wyrd Visions",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Binding Oath",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=5,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Fate Mark",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Geasa",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=5,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Major Geas",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=5,
    mind=5,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Minor Geas",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Secret Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=5,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sparrow's Fall",
    correspondence=0,
    time=4,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="All Tomorrow's Parties",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Anunnaku",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Biometric Holographic Recreation",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Celestial Prediction",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Chronopathy",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Crime and Consequences",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Divinations",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Don't Cross the Streams",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Forecasting",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Geometry of Trade",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hepatoscopy",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Jung's Trick",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Long-Range Eyes",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Manipulate Time Fragment",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Nonlinear Prediction",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Peeping Tom",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Planned Projection",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Play Back",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Postcognition",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Psychometry",
    correspondence=0,
    time=2,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Quo Vadis? (Whither Goest Thou?)",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Reading the Umbral Skein",
    correspondence=0,
    time=2,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Running Scenarios",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Salmon of Wisdom",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Scented Handkerchief",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Songs of Future Days",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Strategic Inefficiency Analysis",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sugar Magnolias",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Turning the Wheel of Ages",
    correspondence=0,
    time=2,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="View the Scattered Lotus Petals",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Area Scan",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Auric Trail",
    correspondence=1,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Check the Corners",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Correspondence Sensing",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Distant Sight",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Divided Sight",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Filter All-Space",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Geometric Jars",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Heat Seeking",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Heat Trace",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Map the True Way",
    correspondence=2,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Open/Close Window",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Scan Non-Local Universe",
    correspondence=2,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Scrying",
    correspondence=2,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Seizing the Forgotten",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Stalking the Void",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Anger in the Land",
    correspondence=0,
    time=0,
    spirit=3,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Banish Elemental",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cycle of the Five Agents",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Time Lock",
    correspondence=0,
    time=4,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="No Surrender",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Rouse the Dragon",
    correspondence=0,
    time=0,
    spirit=4,
    matter=5,
    life=0,
    forces=5,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Yao Su Dragon Thunder",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Cuicuilco's Demise",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=0,
    forces=5,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Embracing the Earth Mother",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pele Wai'ula (Pele's Blood)",
    correspondence=3,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pele's Wrath",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="TWACI",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Arc",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Call Lightning",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Discharge Static",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Electrical Chaos",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lightning Gateway",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Pulse of the Electro-Stream",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Akua Kumu Haka (Guided Fireball)",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Awaken Flame",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Balefire",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Ball of Abysmal Flames",
    correspondence=0,
    time=4,
    spirit=0,
    matter=3,
    life=0,
    forces=5,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Betrayal of the Burning Arrow",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Devouring Gullet of Flame",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Dragonstorm",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Eternal Flame",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Fire Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Friction Curse",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Gabriel's Embrace",
    correspondence=2,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Hermes' Brand",
    correspondence=0,
    time=4,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=1,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Ignis",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Inferno",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=5,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lotus Bloom",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Phlogiston Manipulation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Phlogiston Flux",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pop Goes the Weasel",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=2,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Possess Flame",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Proof Against Immolation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Shih-Huang-Ti's Marvelous Game",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wildfire",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wrath of Heaven",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Fiat Lux",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Filter'd Lantern-Light",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Flash",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Glorious Sword of Heaven",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Laser Enhancement",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Laser Production",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Tsuiho - The Fires of Heaven",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="'Ahiu Nalu (Rogue Wave)",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Calling the Wind Lords",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cloud Cover",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=5,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dousing",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dowsing",
    correspondence=2,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Heenalu (Wave Walking)",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mahu (Steam)",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Sing Down the Rain",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Storm Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tempest in a Teapot",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=5,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Waipuilani (Waterspout)",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Weather Working",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cold Water's Blessing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Contingent Effect",
    correspondence=0,
    time=4,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Counterspell Rune",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Divert Prime Force",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Enchant Life",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Master's Enchantment",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Parma Magica",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Programmed Event",
    correspondence=0,
    time=4,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Watch the Weaving",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Awaken the Sleeping Earth",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Glorious is the Temple",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Leying of the Line",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Locate Quintessence Flow",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Node Raider",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Primal Credit Rating",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Prime Location",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Sense Node",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Tap Node",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Terminal Sanitization",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Wellspring",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Bond of Blood",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="The Burning Lotus",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=4,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Convert Node to Tass",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Cup of Joe",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Drain Tass",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Economic Warfare",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Footbind",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=2,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Fount of Paradise",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="The Hand of the Siphoner",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Hymn of Beatific Harmony",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Primal Infusion",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Primal Net",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Radiate Prime Energy",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Recharge Device",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Recharge Gift",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="The Rush",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Sense Quintessence",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Spinning Thread",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Delay Paradox",
    correspondence=0,
    time=3,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Flames of Purification",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Healthy Skepticism",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Holy Stroke",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Matter-Energy Converter",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Paradox Ward",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Penance for the Sicarii",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Quintessence Blast",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Spirit Pilgrimage",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Balancing the Furies",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Charge the Resonance",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Node Spike",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Occlude the Seal of Power",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Orgone Accumulator",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Psychic Impression",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tag",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="The Ball Game",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Blood for the Gods",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Blood of the Sacred King",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Cup of Itz",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Heart for Huitzilopochtli",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Heart's Blood",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Kaumaha (Sacrifice)",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Lanbs to the Slaughter",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Midnight Oil",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Self-Sacrifice",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Arrest the Flight of Arrows",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Crowdsourced Combat",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Infidel's Laughter",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lucky Blow",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sense the Echo of the Dragon",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spearcatcher Rune",
    correspondence=1,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Strategy",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Targeting Computation",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Time-Motion Study",
    correspondence=1,
    time=1,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wearing the Bear Shirt",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wrath of God",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Battle Rune",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Coordinated Fire",
    correspondence=1,
    time=1,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hail of Bullets",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Legion's Life",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Marching Orders",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mind of the Ant Hill",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="108 Plum Blossoms",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Arashi-Waza",
    correspondence=2,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bullet Catch",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=2,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dragon Fist",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Eight Drunken Hsien",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Final Blow",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=4,
    mind=5,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Flying Dragon Kick",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Focus of the Blow",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hands of Death",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Long Fist",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Piercing Cry",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Purifying Step",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Repeating Blow",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=1,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Righteous Fist",
    correspondence=0,
    time=4,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Rolling Hands",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Screech of the Owl",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spirit Wounder",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Blade Sense",
    correspondence=1,
    time=0,
    spirit=0,
    matter=1,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Hero's Challenge",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Iron Snake",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Jabarut (The Darwishim Battle Trance)",
    correspondence=1,
    time=3,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Splitting a Cuirass",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Swordbreaker Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wind-Water Skein",
    correspondence=3,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Deadaim",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Death Ray",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Emit Beam-Ray",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Golden Gunman",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Grand Salvo",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Holdout Weapon",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Hot-Shotting",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Laserblast",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Magic Bullet",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ricochet",
    correspondence=1,
    time=1,
    spirit=0,
    matter=1,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Rudra's Bow",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Swift Lock",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tamping",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tension",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Trickshot",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=1,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bloodsight",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Conclave Wellness Works",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=2,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Detect Mental Anomalies",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Examine Humors",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Prayer of Healing Revelation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Accidental Overdose",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Adaptive Chemistry",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Cinnabar Tears",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="DMSO",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Drug Enhancement",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Experience Substance",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Good Eatin'/Cleanse the Clown",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Manufacture Enlightened Drugs",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Metabolic Mastery",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Persephone's Nectar",
    correspondence=3,
    time=0,
    spirit=0,
    matter=2,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Poison Maiden",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Polysorbate",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=2,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Purge",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Purging the System",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Purify",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sustenance Pill",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Taking Poison for the Enemy",
    correspondence=2,
    time=0,
    spirit=0,
    matter=2,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tolerance",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Witch's Diplomacy",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Accelerated Aging",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Allergic Reaction",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Ana'ana (The Death Prayer)",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Blight of Aging",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=4,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Bone Twisting Palm",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=4,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Curseof the Mayfly",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Destructive Genegineering",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Fluids of Death",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Fuck Off/Fuck Off and Die",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Heart Murmurs",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Little Good Death",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Rip the Man-Body",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Simulate Inborn Errors of Metabolism",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spy's Stigmata",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Witch's Vengeance",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Aphrodite's Blessing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Chirurgeon",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Distill the Azoth Elixir",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Ease of Passage",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hajjaj",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Heal Self",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Heal Simple Creature",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Healer Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Healing Figurine",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Healing Slumber",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Massage Therapy",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mukashuan",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Rapid Healing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Serene Temple",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Stay the God's Hand",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Surpu",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Trauma",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Trauma Transmission",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Adjust Major Anomalies",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Adjust Minor Anomalies",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Help Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Physiological Rule",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Quietsong",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Branding the Heart",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Buzz",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Counter-Irritant",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Curse of Consequences",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Curse of Macha",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Degree Absolute",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=5,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dukhamarana Moksa",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Endless Parchment",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="General Anesthesia",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Knock Out",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Prolong Pleasure/Pain",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Rubbing of Bones",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Turkey Basting",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Stop-Gap Resurrection",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Waters of the Well of Life",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Gift of Prana",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Hua To's Cure",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Alloy",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Alter State",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Alter Weight",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Guncotton's Blessing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Incredible Shrunken Machine",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Matter Association",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Matter Pattern Disassociation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Melt and Reform",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sculpture",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Semi Auto CAD CAM",
    correspondence=5,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tapping the Signal",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Transephemeration Ray Projector",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Transformers",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Analyze Substance",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Evaluation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Machine God",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=1,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Perfection of the Tools",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Abundance",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Apportation",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Kiss of the Virtuous Maiden",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pickpocket",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ripple Through Space",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spatial Sheath",
    correspondence=2,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Summon Weapon",
    correspondence=2,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dash and a Pinch",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Exotic Matter",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Exotic Matter - Antimatter",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Exotic Matter - Primium",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Industry",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Inscribe Amulet",
    correspondence=0,
    time=4,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Jury Rig",
    correspondence=2,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Na Kua's Gift",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=3,
    entropy=0,
    mind=3,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="O'Doul's Ingeniae",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Psychiatric Compounds",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spear of my Fathers",
    correspondence=0,
    time=0,
    spirit=3,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Spontaneous Material Construction",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Temple Pillars",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Burn-Out",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Chainbreaker Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Erode Matter",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sabotage",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sanitize Evidence",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Slay Machine",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tulugaak's Harpoon",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Beads on a String",
    correspondence=2,
    time=0,
    spirit=2,
    matter=2,
    life=0,
    forces=0,
    entropy=2,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bottle of Smoke",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Craft Biomechanism",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Create Fetish",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Create Talen",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Create Talismans and Artifacts",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Enchant Weapon",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Fits Like a Glove",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Gorningstakkr",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Memento Mori",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pretty-Shinies",
    correspondence=1,
    time=0,
    spirit=1,
    matter=1,
    life=0,
    forces=0,
    entropy=1,
    mind=1,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Talisman Tattoos",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Talisman Transmogrification",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Walking Chair",
    correspondence=0,
    time=0,
    spirit=4,
    matter=4,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Watchdog",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Anitquing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="The Aura Adamantium",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Awaken the Inanimae",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bambolai",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Berate the Demon",
    correspondence=0,
    time=0,
    spirit=3,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Caffeine Plus",
    correspondence=0,
    time=2,
    spirit=1,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Like Clockwork",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Maintain Device",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Obsidian Steel",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Penny Dreadful's Bright New Penny",
    correspondence=0,
    time=2,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Perfection of the True Form",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Perpetual Motion",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Shaman's Craft",
    correspondence=0,
    time=0,
    spirit=3,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Vitality",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Back to the Earth",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="The Golden Lion",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Luster",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Seeds of Gold",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Simple Transmutation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Straw into Gold",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Transmutation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Checklist",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Confusing Apishtiss",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
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
)[0]
Effect.objects.get_or_create(
    name="Destroy Structures",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Disintegrator",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Ebon Dragon's Tale",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=3,
    forces=0,
    entropy=4,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Jolt",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Kinetic Push",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lobotomize",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=5,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mershakushtu Qurdu",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mutate Ephemera",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=5,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Night Battle",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=4,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Shango's Grave",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=5,
    entropy=3,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Sneaking Shadow",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Unleash Nanotech Destruction",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Unseen Arm",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=5,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Consecration",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Joyride",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pathfinding",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pixie Lead",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Remebrance",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Remote Piloting Override",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Teleoperate",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wayfarer's Reckoning",
    correspondence=2,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="We'll Get There",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ala Wai (Short Waters)",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Merlin's Ride",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Seven-League Stride",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shortcut",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Internalize Ephemeral Object",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Leap Beyond",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Untether",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=5,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name='Amon Maat, "Hidden Justice"',
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dingo's Touch",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Infiltration",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pass the Key",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Safecracker",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Thief in the Night",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Chain of Whispers",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cry of Distress",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Death Song",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=1,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Dreamcry",
    correspondence=2,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dreamline",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Flower Gesture",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Override Signal",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pirated Media Blitz",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Point-to-Point Narrow-Band Transmission",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Public Posting",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Sound/Thought Transfer",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Subliminal Impulse",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Subliminal Transmission",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Temper Viasilicos",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Thunder's Gauntlet",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=3,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Adder's Tongue",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Auspicious Dialogues",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Babel",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ravensong",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Semiotic Communication",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Speaking in Tongues",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Time's Tongue",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tower of Babel/Speak in Tongues",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="What Did You Say?",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Breach Alien Gauntlet",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Create Gauntlet",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Create Horizon Realm Construct",
    correspondence=0,
    time=0,
    spirit=5,
    matter=4,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Corrupt Text",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Craft Tome",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cypher Wheel",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Neon-Mail",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Unravelling the Text",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Unseen Nomenclature",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Writing on the Wall",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Agama Re Sojourn/Agama Te Sojourn",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=2,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Death's Passage",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=2,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Gate of Culsu",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Going Under the Cloak",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wings of the Lasa",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Liquor's Calling",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Presentation of the Passage Stick",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sense the Dreamsong",
    correspondence=1,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sing the Dreaming Earth",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Songline Soaring",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Songline Walking",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Alley Vanish",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Daedalus Gateway",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Endless Pool",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Free Conjunction",
    correspondence=5,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Heaven's Tumbling Pebbles",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hermes Portal",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mercury's Bridge",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Riding the Railroad",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shuttle",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Voidcast",
    correspondence=4,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Breach Gauntlet Undetectably",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Breach the Gauntlet",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Break the Dreamshell",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bridge of Blood",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Deep Umbra Travel",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Deep Universe Survival",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Detect the Dream Gateway",
    correspondence=1,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dream Locus",
    correspondence=0,
    time=0,
    spirit=2,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dreamquest",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Gateway Transport",
    correspondence=5,
    time=0,
    spirit=5,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Holopuni'au'nei",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Karmic Inversion",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Leap Sideways",
    correspondence=3,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Long-Distance Universal Travel",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Moving the World Walls",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Reverie",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Schedule of Heaven",
    correspondence=0,
    time=1,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shield of the Soul",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Spirit Cloak",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spirit Journey",
    correspondence=2,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Stepping Sideways",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Storm Watch",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Sucking Gate",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Trailblazing",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Umbral Visions",
    correspondence=2,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Universal Travel",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Walking the Open Path",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Aquatic Survival",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Barrel of Iskander",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Format Space",
    correspondence=5,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Liftoff",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=0,
    forces=5,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Nitrogen Narcosis",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="VAR",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=1,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Body of the Spirit",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Daedalus's Wings",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Levitation Walk",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Navigation",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pilot Skyrigger",
    correspondence=5,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Rooftop Leap",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sure Footing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Thunder Bridge",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Traffic Pulse",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Walking on Water",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wings of Icarus",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Calculate Kinematics",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Eagle Eye",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Find the Sun",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Information Glut",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Information Overload",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Landscape of the Mind",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lay of the Land",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sense Connection",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sousveillance",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Whereami?",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cynical Eye",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Danse Macabre",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Detect Lie",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dim Mak",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Idealism",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Locate Disorder and Weakness",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Oathbreaker's Lash",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Organize",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ring of Truth",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="See the Soul's Burn",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sense Corruption",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Audio Tap",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Current Metering",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Darksight",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ear of Dionysus",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Quantify Energy",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=1,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tune Psychic Radio",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Alarm System",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Gene Scan",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Genetics Scan",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Genome Mapping",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Life Scan",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Life Sense",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pattern Store",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Scan Life Signs",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sequencing",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Assess Affinity",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Fragments of Dream",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hidden Switch",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Holes in the Desert",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Instant Measurement",
    correspondence=1,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Monarch's Friend",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name='Aai-ab "Washing the Heart"',
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cram Session",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Deduction",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Find the Guilty",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Followme",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="I Know Your Cousin",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ishin Den Shin",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lip Reading",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mind Empowerment",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mindfulness of Wrong Thought",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="No-Mind",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pathos",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Read the Soul",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Right-Click",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="True Form",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Detect Reality Deviation",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Dialectic",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Find Reality Flaws",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Hallmark",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Inquisitor",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Lore Rune",
    correspondence=1,
    time=0,
    spirit=1,
    matter=1,
    life=1,
    forces=0,
    entropy=0,
    mind=1,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Patterns of the Long Count",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Spot the Man",
    correspondence=1,
    time=0,
    spirit=0,
    matter=1,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name='Hersh, "To Be Patient"',
    correspondence=1,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mirrorshades",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="See No Evil",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spirit Sight",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name='Utchatti, "The Two Divine Eyes"',
    correspondence=1,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cram",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Download Specialization",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Evaluate Fourth Dimensional Fabric",
    correspondence=0,
    time=1,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Internal Clock",
    correspondence=0,
    time=1,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Perfect Time",
    correspondence=0,
    time=1,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Perfect Timing",
    correspondence=0,
    time=1,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sense the Fleeting Moment",
    correspondence=0,
    time=1,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Time Sense",
    correspondence=0,
    time=1,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Kohl Sight",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mark of the Beast",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Smart Drink",
    correspondence=0,
    time=1,
    spirit=1,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=2,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Blood from a Stone",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Coffin for a Fisher",
    correspondence=0,
    time=0,
    spirit=3,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Fetter Ball",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Voice Across the Void",
    correspondence=2,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Voice of the Jade Ancestors",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ghost-Burning",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shadow Sight",
    correspondence=1,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shelter from the Storm",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Soothe the Dead",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Soul-Forging",
    correspondence=0,
    time=0,
    spirit=4,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Atitsiak",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Kispu",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lichedom",
    correspondence=0,
    time=0,
    spirit=4,
    matter=4,
    life=4,
    forces=0,
    entropy=4,
    mind=1,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Song of Orpheus",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=4,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Walk to Too'ga",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Eternal Discipline of the Family",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=2,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Ghost Rune",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hear and Obey",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Reanimation",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Summon Volva",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Field of Yin",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=5,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Goanna's Hiding",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mindscreen",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Passing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Downvote",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
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
)[0]
Effect.objects.get_or_create(
    name="Move Along",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Secure the Scene",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=1,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shield",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Soul Cloak",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="At Ease",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dontcme",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name='Ghayba (Occultation or "Unbeingness")[0]',
    correspondence=4,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Non-Descript",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pass for Normal",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Selective Edit",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name='Sjonhverfing ("Deceiving of the Sight")[0]',
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Well, It Is Vegas",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Antinoise",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Being Invisible",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cloak of Shadows",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dark Streets",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dreamer's Shroud from Day",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Energy Shield",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name='Huli Shjalmr ("Helmet of Hiding")[0]',
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Return to Darkness",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shadow Project",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shinobijutsu",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Silent Circle",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Smoke Screen",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Smoke-bomb Trick",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Sulfurous Darkness",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Summon Fog",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Veil of Invisibility",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ariadne's Thread",
    correspondence=1,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Chain",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Smoker's Timing",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Perfect Fuse",
    correspondence=0,
    time=1,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Synchronize Watches",
    correspondence=0,
    time=1,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Co-Location",
    correspondence=5,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Conference Call",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=4,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Polyappearance",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Simon's Petition",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Accelerate Time",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="An Hour in Hellfire",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Distort Time",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Establish and Exchange Temporal Event Fields",
    correspondence=0,
    time=5,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Establish Local Temporal Event Field",
    correspondence=0,
    time=4,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Frenzy of the Spinning Wheels",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Moment that Stretches",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Nick of Time",
    correspondence=3,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Quantum Temporal Travel",
    correspondence=3,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Serenity of the Stone",
    correspondence=0,
    time=5,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=4,
    mind=3,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Shed the Years",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=4,
    mind=2,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Sidestep Time",
    correspondence=0,
    time=5,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Slow Time",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="St. Vitus's Kiss",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Symphony of the Soul",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Time Warp",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tune In, Turn On, Drop Out",
    correspondence=0,
    time=4,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Zen and the Art of Panhandling",
    correspondence=0,
    time=5,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Blindside",
    correspondence=4,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bubble of Reality",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Daedalean Labyrinth",
    correspondence=5,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Maze of the Minotaur",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Singularity",
    correspondence=4,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spatial Mutations",
    correspondence=5,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Chiminage Rune",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Dimension Bomb",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hellfire",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sharing the Outsider's Gaze",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Spirit Eating",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Spirit Slaying",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Spirit Wounding",
    correspondence=0,
    time=0,
    spirit=4,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Spirit's Caress",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spiritual Persuasion",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Binding Song",
    correspondence=4,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bottle of Djinn",
    correspondence=0,
    time=0,
    spirit=4,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Circle of Binding",
    correspondence=4,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Coerce Spirit",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Compel the Unseen",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Drahma Protector",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ensure the Endless Sleep",
    correspondence=0,
    time=0,
    spirit=2,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Exorcism",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Exorcism Song",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Gauntlet Prison",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Halt the Nagloper",
    correspondence=0,
    time=2,
    spirit=0,
    matter=2,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Holy Pentacles",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Imbue Flesh",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lesser Binding of Spirits",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Living Bridge",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lull the Waking Dreamborn",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Physical Exorcism",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Weaver's Retribution",
    correspondence=3,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Detect Possession",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Evaluate Gauntlet/Scan Locality",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sense the Demon's Weakness",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sense the Nagloper",
    correspondence=0,
    time=2,
    spirit=0,
    matter=1,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shadows in the Mist",
    correspondence=0,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name='Ap-Sobk "The Last Judgment of Sobk"',
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Call Forth the Forgotten",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Call Spirit",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Call the Dreamborn Sibling",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Conjure the Jade Warrior",
    correspondence=0,
    time=0,
    spirit=5,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Dreamborn Rising",
    correspondence=0,
    time=0,
    spirit=2,
    matter=4,
    life=4,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Drums of Elemental Fire",
    correspondence=0,
    time=0,
    spirit=2,
    matter=2,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Enter the Sauna",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Free the Mad Howlers",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Gremlins",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Here Kitty, Kitty",
    correspondence=3,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Jack in the Green",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Loving Scar",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Nuzzlings",
    correspondence=0,
    time=0,
    spirit=3,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Protection of the Golden Race",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Pygmalion's Paradigm",
    correspondence=0,
    time=0,
    spirit=2,
    matter=4,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Satan's Song",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=2,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Shaking Tent",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spirit Roster",
    correspondence=2,
    time=0,
    spirit=1,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Summon Paradox Spirit",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Summon the Earthly Gods",
    correspondence=4,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Visionary Bloodletting",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Zeitgeist",
    correspondence=0,
    time=2,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Affix Gauntlet",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Circle Ward",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Counterintelligence",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Defense Screen vs. Higher Lifeforms",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Defense Screen vs. Lower Lifeforms",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Etheric Shielding",
    correspondence=0,
    time=0,
    spirit=2,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Fortify Gauntlet",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Magic Circle",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="The Master's Hand",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Protection Song",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Psychic Sterilization",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Quahuitl",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Quantum Interference Shielding",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Reconstruct Gauntlet",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Repel the Hungry Dead",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Repel the Kuei",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Safe Little World",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Salt on the Earth",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Secret Labyrinth",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="The Seven Golden Swords of the Tiger",
    correspondence=4,
    time=0,
    spirit=3,
    matter=3,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Spirit Wall",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Spirit Warding",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Telltale",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Time Wards",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Twisted Yarrow Stalks",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wall of Mirrors",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="War of the Inner Sanctum",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ward",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ward Rune",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Warding Heads",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Zisurru",
    correspondence=2,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Back Door Parole",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=1,
)[0]
Effect.objects.get_or_create(
    name="Deceive the Eyes",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Jivitamarana (Death in Life)[0] Yoga",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Love Me, Love Me",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Persona",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Rouge",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Uther's Butchered Visage",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Agrivelopment",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Alter Simple Creature",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Alter Small Sequence",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Attach Biomechanism",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Augment Simple Lifeform",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Brittle Bones",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=4,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Genetic Pattern Matching",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Graft Alien Bio-Matter Between Aliens",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Graft Alien Bio-Matter to Humans",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Green Thumb",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Higher Lifeform Grafting and Recombination",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Limited Grafting and Recombination",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lower Lifeform Manipulation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Major Environmental Alteration",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Minor Environmental Alteration",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mokupuni Palahalaha Wiki",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Mold Tree",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Personal Compression",
    correspondence=5,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Phosphoric Marker",
    correspondence=1,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Clone",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cloning",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Courtesan's Draught/Blessed Heir",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Fatherless Birth",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=5,
    forces=0,
    entropy=5,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Flesh Toys",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="The Foundling",
    correspondence=2,
    time=0,
    spirit=4,
    matter=2,
    life=5,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Genetic Mastery",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Oak of Sanguine Root",
    correspondence=2,
    time=0,
    spirit=0,
    matter=3,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Spontaneous Generation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Supporting the Brain",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=4,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Thorn Wall",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Animal Form",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Animal Shift",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Avatar Form",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Circe's Enchantment",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Deity Form",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=4,
    forces=3,
    entropy=0,
    mind=0,
    prime=4,
)[0]
Effect.objects.get_or_create(
    name="Dionysus's Gift",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Eagle Form",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Holy Union",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Iron Avatar",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=3,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Jaguar Cloak",
    correspondence=0,
    time=0,
    spirit=2,
    matter=3,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="LERMUization",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lesser Shapechanging",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mutate Form",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Notorious Vampiric Lawnchair",
    correspondence=0,
    time=0,
    spirit=0,
    matter=5,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="One with Beasts",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Perfect Metamorphosis",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Qayaq's Fish",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Rokea'ole",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shapechange Curse",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shapeshifter Prison",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shapeshifting",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Storm of Crows",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=1,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Vulcan's Hammer",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=4,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wasp-Spasm",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=3,
    entropy=0,
    mind=0,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="The Weeping Willow",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=5,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Wolf Form",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Adaptation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Adrenal Rush",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Advanced Therapies",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Battery Man",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Better Body",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Biochemical Regulation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bio-Luminescence",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Brain Boost",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Chakra Influence",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Crocodile Blood",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Go Ti Ta",
    correspondence=0,
    time=0,
    spirit=4,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mele Lapa'au",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Multi-Tasking",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Nanotech Integration",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=5,
)[0]
Effect.objects.get_or_create(
    name="Our Enemies are Delicious",
    correspondence=0,
    time=0,
    spirit=3,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Positronic Brain",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Simple Biochemical Manipulation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Strength of the Earth",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Survivor's Charm",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Talons",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Thick Skin",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Titan's Power",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Tumo",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Apathy",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Olive Branch",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Pass Calmly",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=1,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Peace of Buddha",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Peace Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Rat's Rage/Lost Cousin",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Stoicism",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name='Abh-t-ab, "Biting the Heart"',
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Argument of Princes",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Capiche?",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hoodoo Man's Heartbeat",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Primal Dread",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Show of Force",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bewitchment",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Charm Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Exalted Desire",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Kuoha (The Passion Prayer)",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Lecherous Kiss",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Romance",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Taliesin's Song",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Be Cool",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Branding",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Comp Me",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Cool Glamour",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Empathic Projection",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Gatha",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="The Golden Apple",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Grand Style",
    correspondence=0,
    time=0,
    spirit=0,
    matter=1,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="High Rhetoric",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Hope's Birth",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Incitation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Initiation",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="The Look/The Word",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Loving Cup",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mood Swing/Communion",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Motivational Speaking",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Petals of Love",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Physiological Emotion Control",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=4,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Scent of Control",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Shameful Outburst",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Social Science",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Strains of Laughter, Sleep and Sorrow",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Subtle Persuasion",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Witchwind",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=5,
    entropy=0,
    mind=3,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Animal Possession",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Animal Riding",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Bug Off",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=0,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Horsemaster's Bidding",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mono Kahea 'Ai (Shark Call)",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Ratstorm",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sedna's Blessing",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sing to the Whales",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Divine Aura",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Fifteen Minutes",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Going Viral",
    correspondence=4,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="An Uncompromising Commitment to Excellence",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=0,
    entropy=0,
    mind=4,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Coordination",
    correspondence=3,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Karoshi",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=1,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Workflow",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Delion's Haze",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Destroy Thought",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=5,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Downward Spiral",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Magdeline's Dynamic Mind",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Trip",
    correspondence=2,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=1,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dream Drama",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Dream Play",
    correspondence=0,
    time=2,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Nightmare Dance",
    correspondence=0,
    time=0,
    spirit=2,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Delirium",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Frame Up",
    correspondence=0,
    time=0,
    spirit=0,
    matter=3,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
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
)[0]
Effect.objects.get_or_create(
    name="IFF",
    correspondence=2,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=2,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Imaginary Friend",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Painting the War Dance",
    correspondence=0,
    time=0,
    spirit=0,
    matter=2,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Behavior Modification Device",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="False Witness",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="High Memory",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Manipulate Memories",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Manipulate Memory",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Move to Clone",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=5,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Nostalgia",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Plausible Denial",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Probe Thoughts",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Scan Memories",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Transfer Memories",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Worm",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Alter Paradigm",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=5,
    mind=5,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="The Blissful Discipline",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=3,
    entropy=0,
    mind=4,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Consuming Thought",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Create Drone",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=5,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Create Mind",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=5,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Deprocessing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Destructive Paranoia",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=4,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Hypernarrative Influence",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Impulse Purchase",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Internal Obligation",
    correspondence=0,
    time=4,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Maikai (The Seaward Pull)",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Manchurian Condidate",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=5,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Mind Rune",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Morpheus's Kiss",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=2,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Nervous Control",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=3,
    forces=3,
    entropy=0,
    mind=0,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Possession",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Processing",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=5,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Programming",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Psychic Intrusion",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Purge Thought Crime",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Random Impulse",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Recant",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=2,
    mind=2,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Re-education Mode",
    correspondence=0,
    time=3,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="See the Light",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=3,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Self-Possession",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Sinner's Redemption",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=5,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Social Conditioning",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Soul Shaping",
    correspondence=0,
    time=0,
    spirit=5,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=3,
)[0]
Effect.objects.get_or_create(
    name="Temple Gongs",
    correspondence=0,
    time=0,
    spirit=0,
    matter=4,
    life=3,
    forces=4,
    entropy=0,
    mind=4,
    prime=2,
)[0]
Effect.objects.get_or_create(
    name="Ultimate Argument",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=3,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Welcoming the Jester",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]
Effect.objects.get_or_create(
    name="Willful Binding",
    correspondence=0,
    time=0,
    spirit=0,
    matter=0,
    life=0,
    forces=0,
    entropy=0,
    mind=4,
    prime=0,
)[0]

Effect.objects.get_or_create(name="Palimpsest", matter=3, time=2, prime=2)[
    0
].add_source("Lore of the Traditions", 45)
Effect.objects.get_or_create(
    name="Dismiss the Discordant", mind=2, correspondence=2, entropy=2, prime=2
)[0].add_source("Lore of the Traditions", 45)

Effect.objects.get_or_create(
    name="Bullet-Rider's Blessing", entropy=1, matter=3, spirit=3
)[0].add_source("Lore of the Traditions", 82)
Effect.objects.get_or_create(name="Dwennimmen", mind=4, spirit=4)[0].add_source(
    "Lore of the Traditions", 82
)
Effect.objects.get_or_create(name="Blood for the Ghosts", entropy=2, prime=2, spirit=2)[
    0
].add_source("Lore of the Traditions", 97)
Effect.objects.get_or_create(name="The Last Sacrifice", entropy=4, spirit=2)[
    0
].add_source("Lore of the Traditions", 97)
Effect.objects.get_or_create(
    name="NFTs (Non-Fungible Tass/Talismans)", mind=3, prime=2
)[0].add_source("Lore of the Traditions", 162)
Effect.objects.get_or_create(
    name="NFTs (Non-Fungible Tass/Talismans) (Time Tamper Protection)",
    mind=3,
    prime=2,
    time=4,
)[0].add_source("Lore of the Traditions", 162)
Effect.objects.get_or_create(
    name="NFTs (Non-Fungible Tass/Talismans) (Entropy Tamper Protection)",
    mind=3,
    prime=2,
    entropy=3,
)[0].add_source("Lore of the Traditions", 162)
Effect.objects.get_or_create(
    name="NFTs (Non-Fungible Tass/Talismans) (Tracking)",
    correspondence=2,
    mind=3,
    prime=2,
)[0].add_source("Lore of the Traditions", 162)
Effect.objects.get_or_create(
    name="NFTs (Non-Fungible Tass/Talismans) (Time Tamper Protection, Tracking)",
    correspondence=2,
    mind=3,
    prime=2,
    time=4,
)[0].add_source("Lore of the Traditions", 162)
Effect.objects.get_or_create(
    name="NFTs (Non-Fungible Tass/Talismans) (Entropy Tamper Protection, Tracking)",
    correspondence=2,
    mind=3,
    prime=2,
    entropy=3,
)[0].add_source("Lore of the Traditions", 162)
Effect.objects.get_or_create(name="Save State", mind=3, time=2, prime=2)[0].add_source(
    "Lore of the Traditions", 162
)
Effect.objects.get_or_create(
    name="Locate Geospatial Nodal Point",
    forces=4,
    entropy=3,
    correspondence=3,
    matter=3,
)[0].add_source("Lore of the Traditions", 162)
from characters.models.mage.effect import Effect

# ===== NECROMANCY & DEATH MAGIC =====
Effect.objects.get_or_create(
    name="Summon Ghost",
    spirit=2,
)[0].add_source("How Do You Do That", 142)

Effect.objects.get_or_create(
    name="Summon Powerful Ghost",
    spirit=3,
)[0].add_source("How Do You Do That", 142)

Effect.objects.get_or_create(
    name="See Into Shadowlands",
    spirit=1,
    entropy=1,
)[0].add_source("How Do You Do That", 142)

Effect.objects.get_or_create(
    name="Step Sideways to Shadowlands",
    spirit=3,
)[0].add_source("How Do You Do That", 142)

Effect.objects.get_or_create(
    name="Speak with Dead",
    spirit=2,
    mind=1,
)[0].add_source("How Do You Do That", 142)

Effect.objects.get_or_create(
    name="Bind Ghost",
    spirit=4,
)[0].add_source("How Do You Do That", 143)

Effect.objects.get_or_create(
    name="Banish Ghost",
    spirit=3,
    prime=2,
)[0].add_source("How Do You Do That", 143)

Effect.objects.get_or_create(
    name="Create Zombie (Simple)",
    life=3,
    matter=2,
    prime=2,
)[0].add_source("How Do You Do That", 144)

Effect.objects.get_or_create(
    name="Create Zombie (Complex)",
    life=4,
    matter=2,
    prime=2,
    mind=1,
)[0].add_source("How Do You Do That", 144)

Effect.objects.get_or_create(
    name="Restore Recently Dead to Life",
    life=5,
    prime=2,
    spirit=4,
)[0].add_source("How Do You Do That", 145)

Effect.objects.get_or_create(
    name="Restore Long Dead to Life",
    life=5,
    prime=3,
    spirit=5,
    time=3,
)[0].add_source("How Do You Do That", 145)

Effect.objects.get_or_create(
    name="Create Lich (Self)",
    life=5,
    spirit=4,
    prime=3,
    entropy=3,
)[0].add_source("How Do You Do That", 146)

# ===== TIME MANIPULATION =====
Effect.objects.get_or_create(
    name="Sense Time Flow",
    time=1,
)[0].add_source("How Do You Do That", 154)

Effect.objects.get_or_create(
    name="See Past (Recent)",
    time=2,
)[0].add_source("How Do You Do That", 154)

Effect.objects.get_or_create(
    name="See Future (Near)",
    time=2,
)[0].add_source("How Do You Do That", 154)

Effect.objects.get_or_create(
    name="See Past (Distant)",
    time=3,
    correspondence=2,
)[0].add_source("How Do You Do That", 154)

Effect.objects.get_or_create(
    name="See Future (Distant)",
    time=3,
)[0].add_source("How Do You Do That", 154)

Effect.objects.get_or_create(
    name="Slow Time (Local)",
    time=3,
)[0].add_source("How Do You Do That", 155)

Effect.objects.get_or_create(
    name="Speed Time (Local)",
    time=3,
)[0].add_source("How Do You Do That", 155)

Effect.objects.get_or_create(
    name="Freeze Time (Small Area)",
    time=4,
)[0].add_source("How Do You Do That", 155)

Effect.objects.get_or_create(
    name="Stop Time (Large Area)",
    time=5,
)[0].add_source("How Do You Do That", 155)

Effect.objects.get_or_create(
    name="Rewind Time (Seconds)",
    time=5,
    prime=2,
)[0].add_source("How Do You Do That", 156)

Effect.objects.get_or_create(
    name="Travel Through Time",
    time=5,
    spirit=4,
    prime=3,
)[0].add_source("How Do You Do That", 156)

Effect.objects.get_or_create(
    name="Create Time Loop",
    time=4,
    prime=2,
)[0].add_source("How Do You Do That", 156)

# ===== ADVANCED CORRESPONDENCE =====
Effect.objects.get_or_create(
    name="Teleport Self (Short Range)",
    correspondence=3,
    life=2,
)[0].add_source("How Do You Do That", 127)

Effect.objects.get_or_create(
    name="Teleport Self (Long Range)",
    correspondence=4,
    life=2,
)[0].add_source("How Do You Do That", 127)

Effect.objects.get_or_create(
    name="Teleport Others",
    correspondence=4,
    life=3,
)[0].add_source("How Do You Do That", 127)

Effect.objects.get_or_create(
    name="Create Portal (Temporary)",
    correspondence=4,
    spirit=2,
)[0].add_source("How Do You Do That", 128)

Effect.objects.get_or_create(
    name="Create Portal (Permanent)",
    correspondence=4,
    spirit=2,
    prime=2,
)[0].add_source("How Do You Do That", 128)

Effect.objects.get_or_create(
    name="Co-Location (Be In Two Places)",
    correspondence=5,
    life=3,
    mind=3,
)[0].add_source("M20 Core", 515)

Effect.objects.get_or_create(
    name="Fold Space",
    correspondence=5,
)[0].add_source("M20 Core", 515)

Effect.objects.get_or_create(
    name="Ward Against Teleportation",
    correspondence=3,
    prime=2,
)[0].add_source("How Do You Do That", 128)

# ===== ADVANCED LIFE MAGIC =====
Effect.objects.get_or_create(
    name="Shapeshift into Animal (Self)",
    life=4,
)[0].add_source("How Do You Do That", 34)

Effect.objects.get_or_create(
    name="Shapeshift into Animal (Others)",
    life=5,
)[0].add_source("How Do You Do That", 34)

Effect.objects.get_or_create(
    name="Shapeshift into Hybrid Form",
    life=4,
    prime=2,
)[0].add_source("How Do You Do That", 34)

Effect.objects.get_or_create(
    name="Create Homunculus",
    life=5,
    prime=3,
    mind=2,
)[0].add_source("Book of Secrets", 79)

Effect.objects.get_or_create(
    name="Clone Body",
    life=5,
    prime=2,
    mind=1,
)[0].add_source("Book of Secrets", 79)

Effect.objects.get_or_create(
    name="Enhance Physical Attribute (Permanent)",
    life=4,
    prime=2,
)[0].add_source("M20 Core", 518)

Effect.objects.get_or_create(
    name="Grant Regeneration",
    life=4,
    prime=2,
)[0].add_source("M20 Core", 518)

Effect.objects.get_or_create(
    name="Age/De-Age Target",
    life=4,
    time=2,
)[0].add_source("M20 Core", 518)

Effect.objects.get_or_create(
    name="Cure Poison/Disease (Aggravated)",
    life=4,
)[0].add_source("M20 Core", 518)

# ===== ADVANCED MIND MAGIC =====
Effect.objects.get_or_create(
    name="Read Surface Thoughts",
    mind=2,
)[0].add_source("M20 Core", 519)

Effect.objects.get_or_create(
    name="Read Deep Thoughts/Memories",
    mind=3,
)[0].add_source("M20 Core", 519)

Effect.objects.get_or_create(
    name="Implant False Memory",
    mind=4,
)[0].add_source("M20 Core", 519)

Effect.objects.get_or_create(
    name="Mind Control (Simple Command)",
    mind=3,
)[0].add_source("M20 Core", 519)

Effect.objects.get_or_create(
    name="Mind Control (Complex)",
    mind=4,
)[0].add_source("M20 Core", 519)

Effect.objects.get_or_create(
    name="Possession",
    mind=4,
    life=3,
)[0].add_source("How Do You Do That", 164)

Effect.objects.get_or_create(
    name="Astral Quest",
    mind=5,
    spirit=3,
)[0].add_source("M20 Core", 519)

Effect.objects.get_or_create(
    name="Shatter Mind",
    mind=5,
)[0].add_source("M20 Core", 519)

Effect.objects.get_or_create(
    name="Create Permanent Mental Illusion",
    mind=4,
    prime=2,
)[0].add_source("How Do You Do That", 162)

Effect.objects.get_or_create(
    name="Mass Telepathy",
    mind=3,
    correspondence=2,
)[0].add_source("M20 Core", 519)

# ===== ADVANCED FORCES =====
Effect.objects.get_or_create(
    name="Lightning Bolt",
    forces=3,
)[0].add_source("M20 Core", 517)

Effect.objects.get_or_create(
    name="Fireball",
    forces=3,
)[0].add_source("M20 Core", 517)

Effect.objects.get_or_create(
    name="Force Shield",
    forces=3,
)[0].add_source("M20 Core", 517)

Effect.objects.get_or_create(
    name="Flight (Self)",
    forces=2,
    life=2,
)[0].add_source("How Do You Do That", 126)

Effect.objects.get_or_create(
    name="Flight (Others)",
    forces=3,
    life=2,
)[0].add_source("How Do You Do That", 126)

# Duplicate of line 49 - removed

Effect.objects.get_or_create(
    name="Control Weather (Major)",
    forces=5,
    life=2,
    matter=2,
    prime=2,
)[0].add_source("How Do You Do That", 49)

Effect.objects.get_or_create(
    name="Laser Blast",
    forces=3,
    matter=2,
)[0].add_source("M20 Core", 517)

Effect.objects.get_or_create(
    name="EMP Pulse",
    forces=3,
    matter=2,
)[0].add_source("M20 Core", 517)

Effect.objects.get_or_create(
    name="Nuclear Blast",
    forces=5,
    prime=4,
)[0].add_source("M20 Core", 517)

# ===== ADVANCED MATTER =====
Effect.objects.get_or_create(
    name="Transmute Base Metals to Gold",
    matter=3,
)[0].add_source("M20 Core", 518)

Effect.objects.get_or_create(
    name="Create Matter from Nothing",
    matter=4,
    prime=2,
)[0].add_source("M20 Core", 518)

Effect.objects.get_or_create(
    name="Alter Fundamental Properties",
    matter=5,
)[0].add_source("M20 Core", 518)

Effect.objects.get_or_create(
    name="Phase Through Matter",
    matter=3,
    life=2,
)[0].add_source("M20 Core", 518)

Effect.objects.get_or_create(
    name="Disintegrate Object",
    matter=4,
)[0].add_source("M20 Core", 518)

Effect.objects.get_or_create(
    name="Turn to Stone",
    matter=3,
    life=3,
)[0].add_source("M20 Core", 518)

# ===== ADVANCED ENTROPY =====
Effect.objects.get_or_create(
    name="Curse of Bad Luck",
    entropy=3,
)[0].add_source("M20 Core", 516)

Effect.objects.get_or_create(
    name="Blessing of Good Fortune",
    entropy=3,
)[0].add_source("M20 Core", 516)

Effect.objects.get_or_create(
    name="Age Object Rapidly",
    entropy=3,
    time=2,
)[0].add_source("M20 Core", 516)

Effect.objects.get_or_create(
    name="Rot Living Being",
    entropy=4,
    life=2,
)[0].add_source("M20 Core", 516)

Effect.objects.get_or_create(
    name="Shatter Pattern",
    entropy=5,
    prime=2,
)[0].add_source("M20 Core", 516)

Effect.objects.get_or_create(
    name="Control Probability (Major)",
    entropy=4,
)[0].add_source("M20 Core", 516)

Effect.objects.get_or_create(
    name="Death Curse",
    entropy=5,
    life=4,
    spirit=3,
)[0].add_source("M20 Core", 516)

# ===== ADVANCED PRIME =====
# "Sense Quintessence" - duplicate of line 3301, removed

# "Channel Quintessence" - duplicate of line 127, removed

Effect.objects.get_or_create(
    name="Enchant Talisman",
    prime=3,
)[0].add_source("Book of Secrets", 82)

Effect.objects.get_or_create(
    name="Create Wonder",
    prime=5,
)[0].add_source("Book of Secrets", 82)

Effect.objects.get_or_create(
    name="Disenchant Wonder",
    prime=4,
)[0].add_source("M20 Core", 520)

Effect.objects.get_or_create(
    name="Nullify Magic",
    prime=3,
)[0].add_source("M20 Core", 520)

Effect.objects.get_or_create(
    name="Permanently Enhance Pattern",
    prime=5,
)[0].add_source("M20 Core", 520)

Effect.objects.get_or_create(
    name="Fuel Pattern with Quintessence",
    prime=2,
)[0].add_source("M20 Core", 520)

Effect.objects.get_or_create(
    name="Create Tass",
    prime=3,
)[0].add_source("M20 Core", 520)

Effect.objects.get_or_create(
    name="Open/Seal Node",
    prime=4,
    spirit=2,
)[0].add_source("M20 Core", 520)

# ===== ADVANCED SPIRIT =====
# "See Spirits" - duplicate of line 144, removed

Effect.objects.get_or_create(
    name="Touch Spirit Matter",
    spirit=2,
)[0].add_source("M20 Core", 521)

Effect.objects.get_or_create(
    name="Step Sideways to Umbra",
    spirit=3,
)[0].add_source("M20 Core", 521)

Effect.objects.get_or_create(
    name="Reach Into Umbra",
    spirit=3,
)[0].add_source("M20 Core", 521)

Effect.objects.get_or_create(
    name="Summon Spirit (Minor)",
    spirit=2,
)[0].add_source("How Do You Do That", 148)

Effect.objects.get_or_create(
    name="Summon Spirit (Powerful)",
    spirit=3,
)[0].add_source("How Do You Do That", 148)

Effect.objects.get_or_create(
    name="Bind Spirit",
    spirit=4,
)[0].add_source("How Do You Do That", 148)

Effect.objects.get_or_create(
    name="Create Spirit Gate",
    spirit=4,
    prime=2,
)[0].add_source("M20 Core", 521)

Effect.objects.get_or_create(
    name="Create Fetish",
    spirit=4,
    prime=2,
)[0].add_source("M20 Core", 521)

Effect.objects.get_or_create(
    name="Strengthen/Weaken Gauntlet",
    spirit=4,
)[0].add_source("M20 Core", 521)

Effect.objects.get_or_create(
    name="Create Spirit",
    spirit=5,
    prime=4,
)[0].add_source("M20 Core", 521)

Effect.objects.get_or_create(
    name="Permanently Destroy Spirit",
    spirit=5,
    prime=3,
)[0].add_source("M20 Core", 521)

# ===== CROSS-SPLAT EFFECTS =====
Effect.objects.get_or_create(
    name="Break Blood Bond",
    life=4,
    mind=3,
    entropy=3,
    prime=1,
)[0].add_source("Book of Secrets", 86)

Effect.objects.get_or_create(
    name="Harm Vampire",
    life=3,
    matter=2,
)[0].add_source("Gods & Monsters", 58)

Effect.objects.get_or_create(
    name="Heal Vampire",
    life=3,
    matter=2,
)[0].add_source("Gods & Monsters", 58)

Effect.objects.get_or_create(
    name="Harm Werewolf",
    life=3,
    spirit=3,
)[0].add_source("Gods & Monsters", 75)

Effect.objects.get_or_create(
    name="Heal Werewolf",
    life=3,
    spirit=2,
)[0].add_source("Gods & Monsters", 75)

Effect.objects.get_or_create(
    name="Harm Fae",
    life=3,
    mind=3,
)[0].add_source("Gods & Monsters", 104)

Effect.objects.get_or_create(
    name="Heal Fae",
    life=3,
    mind=3,
)[0].add_source("Gods & Monsters", 104)

Effect.objects.get_or_create(
    name="Counter Fae Glamour",
    prime=2,
    mind=2,
)[0].add_source("Gods & Monsters", 104)

Effect.objects.get_or_create(
    name="Harm Ghost",
    prime=2,
    entropy=3,
)[0].add_source("Gods & Monsters", 120)

Effect.objects.get_or_create(
    name="Strengthen Ghost",
    spirit=3,
    prime=2,
)[0].add_source("Gods & Monsters", 120)

# ===== PARADIGM-SPECIFIC EFFECTS =====
# Akashic Brotherhood
Effect.objects.get_or_create(
    name="Do Strike (Akashic)",
    life=2,
    mind=1,
    prime=1,
)[0].add_source("Lore of the Traditions", 28)

Effect.objects.get_or_create(
    name="Dragon Pearl Meditation",
    prime=3,
    mind=2,
)[0].add_source("Lore of the Traditions", 28)

Effect.objects.get_or_create(
    name="Chi Healing",
    life=3,
    prime=1,
)[0].add_source("Lore of the Traditions", 28)

# Celestial Chorus
Effect.objects.get_or_create(
    name="Holy Fire",
    forces=3,
    prime=2,
)[0].add_source("Lore of the Traditions", 48)

Effect.objects.get_or_create(
    name="Blessing of the One",
    prime=2,
    mind=2,
    life=1,
)[0].add_source("Lore of the Traditions", 48)

Effect.objects.get_or_create(
    name="Call Divine Intervention",
    prime=4,
    spirit=3,
)[0].add_source("Lore of the Traditions", 48)

# Cult of Ecstasy
Effect.objects.get_or_create(
    name="Temporal Fugue",
    time=3,
    mind=2,
)[0].add_source("Lore of the Traditions", 68)

Effect.objects.get_or_create(
    name="Ecstatic Vision",
    mind=2,
    time=1,
)[0].add_source("Lore of the Traditions", 68)

# Dreamspeakers
Effect.objects.get_or_create(
    name="Spirit Journey",
    spirit=3,
    mind=1,
)[0].add_source("Lore of the Traditions", 88)

Effect.objects.get_or_create(
    name="Call Totem Spirit",
    spirit=4,
)[0].add_source("Lore of the Traditions", 88)

Effect.objects.get_or_create(
    name="Medicine Work Healing",
    life=3,
    spirit=1,
)[0].add_source("Lore of the Traditions", 88)

# Euthanatos
Effect.objects.get_or_create(
    name="Good Death",
    entropy=3,
    life=3,
    spirit=2,
)[0].add_source("Lore of the Traditions", 108)

Effect.objects.get_or_create(
    name="Wheel of Fate",
    entropy=4,
    time=2,
)[0].add_source("Lore of the Traditions", 108)

# Order of Hermes
Effect.objects.get_or_create(
    name="Hermetic Circle of Protection",
    prime=2,
    forces=2,
    mind=1,
)[0].add_source("Lore of the Traditions", 128)

Effect.objects.get_or_create(
    name="Summon Elemental",
    forces=4,
    spirit=3,
    prime=2,
)[0].add_source("Lore of the Traditions", 128)

Effect.objects.get_or_create(
    name="Alchemical Transmutation",
    matter=3,
    prime=2,
)[0].add_source("Lore of the Traditions", 128)

# Sons of Ether
Effect.objects.get_or_create(
    name="Ether Ray",
    forces=3,
    matter=2,
    prime=1,
)[0].add_source("Lore of the Traditions", 148)

Effect.objects.get_or_create(
    name="Dimensional Portal Device",
    correspondence=4,
    matter=3,
    prime=2,
)[0].add_source("Lore of the Traditions", 148)

# Verbena
Effect.objects.get_or_create(
    name="Blood Magic Ritual",
    life=3,
    prime=2,
)[0].add_source("Lore of the Traditions", 168)

Effect.objects.get_or_create(
    name="Primal Transformation",
    life=4,
    spirit=2,
)[0].add_source("Lore of the Traditions", 168)

Effect.objects.get_or_create(
    name="Call the Wild Hunt",
    spirit=4,
    life=2,
    mind=2,
)[0].add_source("Lore of the Traditions", 168)

# Virtual Adepts
Effect.objects.get_or_create(
    name="Reality Hack",
    correspondence=3,
    forces=2,
    prime=1,
)[0].add_source("Lore of the Traditions", 188)

Effect.objects.get_or_create(
    name="Digital Avatar",
    correspondence=3,
    mind=3,
    prime=2,
)[0].add_source("Lore of the Traditions", 188)

Effect.objects.get_or_create(
    name="Information Overload",
    forces=3,
    mind=3,
    correspondence=2,
)[0].add_source("Lore of the Traditions", 188)

# ===== TECHNOCRATIC PROCEDURES =====
Effect.objects.get_or_create(
    name="HIT Mark Activation (Primium Construct)",
    matter=4,
    life=2,
    prime=3,
)[0].add_source("Technocracy Reloaded", 201)

Effect.objects.get_or_create(
    name="Mind Wipe (Flashy Thing)",
    mind=3,
)[0].add_source("Technocracy Reloaded", 225)

Effect.objects.get_or_create(
    name="Biometric Scan",
    life=2,
    correspondence=1,
)[0].add_source("Technocracy Reloaded", 216)

Effect.objects.get_or_create(
    name="Genetic Modification",
    life=4,
    matter=2,
    prime=2,
)[0].add_source("Technocracy Reloaded", 158)

Effect.objects.get_or_create(
    name="Dimensional Backdoor",
    correspondence=4,
    spirit=5,
)[0].add_source("Technocracy Reloaded", 227)

Effect.objects.get_or_create(
    name="PAWS Taser (Anti-Shapeshifter)",
    forces=3,
    life=4,
    spirit=3,
    prime=2,
)[0].add_source("Technocracy Reloaded", 224)

Effect.objects.get_or_create(
    name="Sleepteacher Accelerated Learning",
    mind=3,
    time=2,
)[0].add_source("Technocracy Reloaded", 230)

# ===== NEPHANDI/MARAUDER EFFECTS =====
Effect.objects.get_or_create(
    name="Infernal Pact",
    prime=4,
    spirit=4,
    entropy=3,
)[0].add_source("Book of the Fallen", 145)

Effect.objects.get_or_create(
    name="Corrupt Pattern",
    entropy=4,
    life=3,
    prime=2,
)[0].add_source("Book of the Fallen", 148)

Effect.objects.get_or_create(
    name="Summon Demon",
    spirit=4,
    prime=3,
    entropy=2,
)[0].add_source("Book of the Fallen", 150)

Effect.objects.get_or_create(
    name="Reality Cancer",
    prime=5,
    entropy=5,
)[0].add_source("Book of the Fallen", 155)

# ===== UTILITY & MISCELLANEOUS =====
Effect.objects.get_or_create(
    name="Permanent Enchantment",
    prime=5,
)[0].add_source("M20 Core", 520)

Effect.objects.get_or_create(
    name="Counterspell (Basic)",
    prime=2,
)[0].add_source("M20 Core", 542)

Effect.objects.get_or_create(
    name="Counterspell (Advanced)",
    prime=3,
)[0].add_source("M20 Core", 542)

Effect.objects.get_or_create(
    name="Dispel Paradox",
    prime=3,
    entropy=2,
)[0].add_source("M20 Core", 548)

Effect.objects.get_or_create(
    name="Absorb Quintessence from Living",
    prime=5,
    life=3,
)[0].add_source("Book of Secrets", 102)

Effect.objects.get_or_create(
    name="Create Horizon Realm",
    correspondence=5,
    spirit=5,
    prime=5,
)[0].add_source("M20 Core", 612)

Effect.objects.get_or_create(
    name="Ward Against Scrying",
    correspondence=3,
    mind=2,
    prime=1,
)[0].add_source("M20 Core", 515)

Effect.objects.get_or_create(
    name="Ward Against Spirits",
    spirit=3,
    prime=2,
)[0].add_source("M20 Core", 521)

Effect.objects.get_or_create(
    name="Mass Teleportation",
    correspondence=5,
    life=3,
    mind=2,
)[0].add_source("M20 Core", 515)

Effect.objects.get_or_create(
    name="Destroy Pattern Permanently",
    prime=5,
    entropy=4,
)[0].add_source("M20 Core", 520)
