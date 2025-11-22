from items.models.werewolf.talen import Talen

# TALENS - One-use spirit-infused items

# Bane Arrows
Talen.objects.get_or_create(
    name="Bane Arrow",
    rank=1,
    gnosis=6,
    description="Single-use arrow that always hits Banes and deals Strength +5 aggravated damage to them.",
    spirit="War Spirit or Predator Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 226)

# Black Anger
Talen.objects.get_or_create(
    name="Black Anger",
    rank=1,
    gnosis=6,
    description="Potion that increases Rage by 3 temporary points when consumed.",
    spirit="Rage Spirit or War Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 226)

# Clear Water
Talen.objects.get_or_create(
    name="Clear Water",
    rank=1,
    gnosis=5,
    description="Water that purifies, removing one level of poison or disease when consumed.",
    spirit="Water Elemental or Cleansing Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 226)

# Gaia's Breath
Talen.objects.get_or_create(
    name="Gaia's Breath",
    rank=1,
    gnosis=4,
    description="Bag that captures and stores air, providing oxygen for 30 minutes when opened.",
    spirit="Air Elemental",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 226)

# Moon Sign
Talen.objects.get_or_create(
    name="Moon Sign",
    rank=1,
    gnosis=7,
    description="Token that identifies bearer's tribe, auspice, and rank to other Garou.",
    spirit="Lune",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 226)

# Spirit Egg
Talen.objects.get_or_create(
    name="Spirit Egg",
    rank=1,
    gnosis=5,
    description="Egg containing a bound spirit that is released when broken.",
    spirit="Various spirits",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 227)

# Stone of Silence
Talen.objects.get_or_create(
    name="Stone of Silence",
    rank=1,
    gnosis=6,
    description="Stone that creates a 20-foot radius zone of silence where no sound enters or leaves for one scene.",
    spirit="Silence Spirit or Shadow Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 227)

# Sun's Blessing
Talen.objects.get_or_create(
    name="Sun's Blessing",
    rank=1,
    gnosis=6,
    description="Creates a 30-foot radius of daylight for one scene.",
    spirit="Servant of Helios",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 227)

# Unbreakable Cord
Talen.objects.get_or_create(
    name="Unbreakable Cord",
    rank=1,
    gnosis=7,
    description="Rope that cannot be cut and holds for one scene.",
    spirit="Earth Elemental or Strength Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 227)

# Wind's Return
Talen.objects.get_or_create(
    name="Wind's Return",
    rank=1,
    gnosis=8,
    description="Token that causes thrown weapon to return to wielder's hand after being thrown.",
    spirit="Air Elemental or Bird Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 227)

# Death Dust
Talen.objects.get_or_create(
    name="Death Dust",
    rank=2,
    gnosis=7,
    description="Powder that causes disease. Victim must roll Stamina (difficulty 7) or contract illness.",
    spirit="Disease Spirit or Decay Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 227)

# Dragon's Blood
Talen.objects.get_or_create(
    name="Dragon's Blood",
    rank=2,
    gnosis=6,
    description="Potion that grants immunity to fire for one scene.",
    spirit="Fire Elemental or Dragon Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 227)

# Feral Claws
Talen.objects.get_or_create(
    name="Feral Claws",
    rank=2,
    gnosis=6,
    description="Applied to claws, causes them to deal aggravated damage for one scene.",
    spirit="Predator Spirit or War Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 227)

# Moon Glow
Talen.objects.get_or_create(
    name="Moon Glow",
    rank=2,
    gnosis=4,
    description="Glowing orb that illuminates a 30-foot radius for one scene.",
    spirit="Lune or Light Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 228)

# Spirit Bottle
Talen.objects.get_or_create(
    name="Spirit Bottle",
    rank=2,
    gnosis=7,
    description="Bottle that can trap a spirit with Gnosis 7 or less.",
    spirit="Binding Spirit or Weaver Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 228)

# Traveler's Knot
Talen.objects.get_or_create(
    name="Traveler's Knot",
    rank=2,
    gnosis=5,
    description="Allows holder to travel at double movement speed for one scene.",
    spirit="Road Spirit or Journey Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 228)

# Warm Blanket
Talen.objects.get_or_create(
    name="Warm Blanket",
    rank=2,
    gnosis=4,
    description="Blanket that keeps wearer warm even in extreme cold, protecting from hypothermia for one scene.",
    spirit="Fire Elemental or Comfort Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 228)

# Wolf's Blood
Talen.objects.get_or_create(
    name="Wolf's Blood",
    rank=2,
    gnosis=6,
    description="Potion that heals two health levels of damage when consumed.",
    spirit="Healing Spirit or Wolf Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 228)

# Bane Seed
Talen.objects.get_or_create(
    name="Bane Seed",
    rank=3,
    gnosis=7,
    description="Seed that grows into a plant that repels Banes from the area.",
    spirit="Nature Spirit or Plant Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 228)

# Moon Bridge Token
Talen.objects.get_or_create(
    name="Moon Bridge Token",
    rank=3,
    gnosis=8,
    description="Opens a moon bridge to a known caern one time.",
    spirit="Lune",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 228)

# Spirit Whistle
Talen.objects.get_or_create(
    name="Spirit Whistle",
    rank=3,
    gnosis=7,
    description="Whistle that summons a specific type of spirit (spirit must answer but may be angry).",
    spirit="Relevant spirit type",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 229)

# Wyrm Scale
Talen.objects.get_or_create(
    name="Wyrm Scale",
    rank=3,
    gnosis=8,
    description="Scale that grants immunity to Wyrm toxins and poisons for one scene.",
    spirit="Purification Spirit or Gaia Spirit",
    display=False,
)[0].add_source("Werewolf: the Apocalypse 20th Anniversary Edition", 229)
