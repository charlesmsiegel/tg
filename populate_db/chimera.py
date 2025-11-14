from characters.models.changeling import Chimera

# FACSIMILES (5 points)
Chimera.objects.get_or_create(
    name="Golden Coin",
    chimera_type="facsimile",
    chimera_points=5,
    sentience_level="non_sentient",
    appearance="Shimmering gold coin that appears completely real",
    durability=1,
    origin="created_art",
    is_permanent=False,
    creator="Legerdemain Practitioners",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 214)

Chimera.objects.get_or_create(
    name="Illusory Rose",
    chimera_type="facsimile",
    chimera_points=5,
    sentience_level="non_sentient",
    appearance="Perfect red rose that doesn't wilt",
    durability=1,
    origin="created_art",
    is_permanent=False,
    creator="Chicanery Practitioners",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 214)

Chimera.objects.get_or_create(
    name="Shadow Dagger",
    chimera_type="facsimile",
    chimera_points=5,
    sentience_level="non_sentient",
    appearance="Dagger made of solidified shadow",
    durability=1,
    origin="created_art",
    is_permanent=False,
    creator="Autumn Practitioners",
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 215)

# SIMPLE CRAFTED (10 points)
Chimera.objects.get_or_create(
    name="Faerie Hound",
    chimera_type="simple_crafted",
    chimera_points=10,
    sentience_level="semi_sentient",
    appearance="Small glowing dog made of starlight and mist; loyal and affectionate",
    durability=2,
    behavior="Follows master faithfully; warns of danger; cannot harm but can distract enemies",
    origin="created_art",
    is_permanent=False,
    creator="Pooka or Primal Practitioner",
    loyalty=5,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 215)

Chimera.objects.get_or_create(
    name="Singing Bird",
    chimera_type="simple_crafted",
    chimera_points=10,
    sentience_level="semi_sentient",
    appearance="Crystal bird that sings beautiful songs",
    durability=2,
    behavior="Sings to ease emotions; warns of danger through song changes",
    origin="manifested_dream",
    is_permanent=False,
    creator="Summer Practitioner",
    loyalty=4,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 215)

Chimera.objects.get_or_create(
    name="Guardian Spirit",
    chimera_type="simple_crafted",
    chimera_points=10,
    sentience_level="semi_sentient",
    appearance="Ethereal humanoid form of pure Glamour",
    durability=2,
    behavior="Protects specific location or person; can communicate through visions",
    origin="created_art",
    is_permanent=True,
    creator="Sovereign Practitioner",
    loyalty=5,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 216)

# ADVANCED CRAFTED (20 points)
Chimera.objects.get_or_create(
    name="Pixie Companion",
    chimera_type="advanced_crafted",
    chimera_points=20,
    sentience_level="sentient",
    appearance="Tiny humanoid figure with insect-like wings",
    durability=3,
    behavior="Mischievous but loyal; can perform small tasks; speaks in high-pitched voice; enjoys tricks and games",
    special_abilities=["Perform Small Tasks", "Scouting", "Mischief-Making"],
    origin="manifested_dream",
    is_permanent=False,
    creator="Pooka or Trickster Changeling",
    loyalty=3,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 216)

Chimera.objects.get_or_create(
    name="Dream Warden",
    chimera_type="advanced_crafted",
    chimera_points=20,
    sentience_level="sentient",
    appearance="Tall, ethereal guardian with starlit eyes and flowing robes",
    durability=3,
    behavior="Guards dreams and prevents nightmares; can communicate with dreamer",
    special_abilities=["Dream Protection", "Nightmare Banishment", "Emotional Support"],
    origin="manifested_dream",
    is_permanent=False,
    creator="Oneiromancy Master",
    loyalty=5,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 217)

Chimera.objects.get_or_create(
    name="Fae Familiar",
    chimera_type="advanced_crafted",
    chimera_points=20,
    sentience_level="sentient",
    appearance="Intelligent animal (cat, raven, fox, etc.) made of Glamour",
    durability=3,
    behavior="Acts as partner and advisor; can understand and follow complex instructions",
    special_abilities=["Scouting", "Combat Support", "Magical Affinity"],
    origin="created_art",
    is_permanent=True,
    creator="Any experienced Changeling",
    loyalty=4,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 217)

# COMPLEX CRAFTED (30-35 points)
Chimera.objects.get_or_create(
    name="Valiant Servant",
    chimera_type="complex_crafted",
    chimera_points=30,
    sentience_level="fully_sentient",
    appearance="Humanoid figure in archaic armor, eyes glowing with purpose",
    durability=4,
    behavior="Serves with unwavering loyalty and honor; can engage in conversation; fights alongside master",
    special_abilities=["Combat", "Guard Duty", "Conversation", "Complex Task Performance"],
    origin="created_art",
    is_permanent=True,
    creator="Sovereign Practitioner or Ancient Sidhe",
    loyalty=5,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 218)

Chimera.objects.get_or_create(
    name="Winged Drake",
    chimera_type="complex_crafted",
    chimera_points=32,
    sentience_level="fully_sentient",
    appearance="Small dragon with shimmering scales and intelligent eyes",
    durability=4,
    behavior="Proud and fierce; can carry rider; breathes Glamour-fire",
    special_abilities=["Flight", "Combat", "Carrying Capacity", "Glamour Breath"],
    origin="manifested_dream",
    is_permanent=False,
    creator="Dragon's Ire Practitioner",
    loyalty=3,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 218)

Chimera.objects.get_or_create(
    name="Sage Counselor",
    chimera_type="complex_crafted",
    chimera_points=33,
    sentience_level="fully_sentient",
    appearance="Wise elder figure made of living starlight",
    durability=4,
    behavior="Provides counsel and wisdom; remembers all things it has witnessed; teaches cantrips",
    special_abilities=["Wisdom Sharing", "Knowledge", "Cantrip Instruction", "Foresight"],
    origin="manifested_dream",
    is_permanent=False,
    creator="Soothsay Master",
    loyalty=4,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 219)

# MASTER CRAFTED (40-50 points)
Chimera.objects.get_or_create(
    name="Chimera Steed",
    chimera_type="master_crafted",
    chimera_points=45,
    sentience_level="fully_sentient",
    appearance="Majestic horse with ethereal mane and coat of living light",
    durability=5,
    behavior="Intelligent partner; can gallop between worlds; understands speech and feelings",
    special_abilities=["Flight/Dimensional Travel", "Combat Support", "Emotional Bond", "World-Stride Movement"],
    origin="manifested_dream",
    is_permanent=False,
    creator="Master of Wayfare and Metamorphosis",
    loyalty=5,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 219)

Chimera.objects.get_or_create(
    name="Fae Knight",
    chimera_type="master_crafted",
    chimera_points=48,
    sentience_level="fully_sentient",
    appearance="Noble warrior in ornate armor, face hidden by helm, radiating power",
    durability=5,
    behavior="Fully autonomous; tactical fighter; can lead forces; speaks eloquently; seeks honor",
    special_abilities=["Combat Mastery", "Leadership", "Tactical Planning", "Magical Resistance"],
    origin="created_art",
    is_permanent=True,
    creator="Ancient Sidhe House or Master Craftsperson",
    loyalty=5,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 220)

Chimera.objects.get_or_create(
    name="Dreaming Incarnate",
    chimera_type="master_crafted",
    chimera_points=50,
    sentience_level="fully_sentient",
    appearance="Chaotic, ever-changing form reflecting the essence of dreams themselves",
    durability=5,
    behavior="Possesses dream logic; aids in accessing the Dreaming; can manifest others' dreams",
    special_abilities=["Dream Mastery", "Reality Manipulation", "Portal Creation", "Glamour Generation"],
    origin="manifested_dream",
    is_permanent=False,
    creator="Master of Oneiromancy",
    loyalty=2,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 220)

Chimera.objects.get_or_create(
    name="Dryad Guardian",
    chimera_type="master_crafted",
    chimera_points=42,
    sentience_level="fully_sentient",
    appearance="Beautiful humanoid figure made of living wood and flowering vines",
    durability=5,
    behavior="Protects natural spaces; heals those pure of heart; speaks in riddles",
    special_abilities=["Healing", "Nature Control", "Trespass Prevention", "Wisdom Sharing"],
    origin="created_art",
    is_permanent=True,
    creator="Primal/Spring Master",
    loyalty=4,
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 220)
