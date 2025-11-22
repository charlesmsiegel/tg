from characters.models.werewolf.gift import Gift, GiftPermission

# ===============================
# BASTET (Werecat) GIFTS
# ===============================

# Bastet Breeds
bastet_homid = GiftPermission.objects.get_or_create(
    shifter="bastet", condition="homid"
)[0]
bastet_feline = GiftPermission.objects.get_or_create(
    shifter="bastet", condition="feline"
)[0]
bastet_metis = GiftPermission.objects.get_or_create(
    shifter="bastet", condition="metis"
)[0]

# Bastet Pryio (auspice-like)
daylight = GiftPermission.objects.get_or_create(shifter="bastet", condition="daylight")[
    0
]
twilight = GiftPermission.objects.get_or_create(shifter="bastet", condition="twilight")[
    0
]
midnight = GiftPermission.objects.get_or_create(shifter="bastet", condition="midnight")[
    0
]

# Bastet Tribes
bagheera = GiftPermission.objects.get_or_create(shifter="bastet", condition="bagheera")[
    0
]
balam = GiftPermission.objects.get_or_create(shifter="bastet", condition="balam")[0]
bubasti = GiftPermission.objects.get_or_create(shifter="bastet", condition="bubasti")[0]
ceilican = GiftPermission.objects.get_or_create(shifter="bastet", condition="ceilican")[
    0
]
khan = GiftPermission.objects.get_or_create(shifter="bastet", condition="khan")[0]
pumonca = GiftPermission.objects.get_or_create(shifter="bastet", condition="pumonca")[0]
qualmi = GiftPermission.objects.get_or_create(shifter="bastet", condition="qualmi")[0]
simba = GiftPermission.objects.get_or_create(shifter="bastet", condition="simba")[0]
swara = GiftPermission.objects.get_or_create(shifter="bastet", condition="swara")[0]

# Bastet Breed Gifts - Homid
g = Gift.objects.get_or_create(name="Sing the Great Cat's Song", rank=1)[0]
g.allowed.add(bastet_homid)
g.description = "Communicate with all felines, from housecats to lions."
g.save()

g = Gift.objects.get_or_create(name="Kitten's Cry", rank=1)[0]
g.allowed.add(bastet_homid)
g.description = "Appear harmless and innocent to others."
g.save()

# Bastet Breed Gifts - Feline
g = Gift.objects.get_or_create(name="Catfeet", rank=1)[0]
g.allowed.add(bastet_feline)
g.description = "Perfect balance and ability to land on feet from any fall."
g.save()

g = Gift.objects.get_or_create(name="Razor Claws", rank=1)[0]
g.allowed.add(bastet_feline)
g.description = "Sharpen claws to deal lethal damage."
g.save()

# Bastet Breed Gifts - Metis
g = Gift.objects.get_or_create(name="Spirit Sight", rank=1)[0]
g.allowed.add(bastet_metis)
g.description = "See into the Penumbra without crossing over."
g.save()

# Bastet Pryio Gifts
g = Gift.objects.get_or_create(name="Hunter's Sense", rank=1)[0]
g.allowed.add(daylight)
g.description = "Track prey unerringly."
g.save()

g = Gift.objects.get_or_create(name="Blur of the Milky Eye", rank=1)[0]
g.allowed.add(twilight)
g.description = "Become difficult to perceive or remember."
g.save()

g = Gift.objects.get_or_create(name="Spirit Speech", rank=1)[0]
g.allowed.add(midnight)
g.description = "Communicate with any spirit."
g.save()

# Bastet Tribe Gifts
g = Gift.objects.get_or_create(name="Shadows at Dawn", rank=1)[0]
g.allowed.add(bagheera)
g.description = "Manipulate shadows and darkness."
g.save()

g = Gift.objects.get_or_create(name="Treeclimber", rank=1)[0]
g.allowed.add(balam)
g.description = "Climb any surface with ease."
g.save()

g = Gift.objects.get_or_create(name="Pulse of the Unseen", rank=1)[0]
g.allowed.add(bubasti)
g.description = "Sense magic and spirits nearby."
g.save()

g = Gift.objects.get_or_create(name="Faerie Kin", rank=1)[0]
g.allowed.add(ceilican)
g.description = "Communicate with and befriend faeries."
g.save()

g = Gift.objects.get_or_create(name="Dragon's Ire", rank=1)[0]
g.allowed.add(khan)
g.description = "Inspire fear in enemies with a roar."
g.save()

g = Gift.objects.get_or_create(name="Mountain Lion's Speed", rank=1)[0]
g.allowed.add(pumonca)
g.description = "Move with incredible speed in short bursts."
g.save()

g = Gift.objects.get_or_create(name="Dazzle", rank=1)[0]
g.allowed.add(qualmi)
g.description = "Confuse enemies with shifting patterns."
g.save()

g = Gift.objects.get_or_create(name="King of Beasts", rank=1)[0]
g.allowed.add(simba)
g.description = "Command other animals with authority."
g.save()

g = Gift.objects.get_or_create(name="Blur of Speed", rank=1)[0]
g.allowed.add(swara)
g.description = "Run at incredible speeds."
g.save()

# ===============================
# CORAX (Wereraven) GIFTS
# ===============================

corax = GiftPermission.objects.get_or_create(shifter="corax", condition="corax")[0]
corax_homid = GiftPermission.objects.get_or_create(shifter="corax", condition="homid")[
    0
]
corax_corvid = GiftPermission.objects.get_or_create(
    shifter="corax", condition="corvid"
)[0]

# Universal Corax Gifts
g = Gift.objects.get_or_create(name="Eye of the Sun", rank=1)[0]
g.allowed.add(corax)
g.description = "See clearly even in brightest light."
g.save()

g = Gift.objects.get_or_create(name="Voice of the Mimic", rank=1)[0]
g.allowed.add(corax)
g.description = "Perfectly imitate any sound or voice."
g.save()

g = Gift.objects.get_or_create(name="Raven's Gleaning", rank=2)[0]
g.allowed.add(corax)
g.description = "Learn secrets from the dead."
g.save()

g = Gift.objects.get_or_create(name="Thieving Talons of the Magpie", rank=1)[0]
g.allowed.add(corax)
g.description = "Steal small objects with supernatural skill."
g.save()

# Corax Breed Gifts
g = Gift.objects.get_or_create(name="Raven's Wing", rank=1)[0]
g.allowed.add(corax_corvid)
g.description = "Fly faster and more gracefully."
g.save()

# ===============================
# GURAHL (Werebear) GIFTS
# ===============================

gurahl_homid = GiftPermission.objects.get_or_create(
    shifter="gurahl", condition="homid"
)[0]
gurahl_ursine = GiftPermission.objects.get_or_create(
    shifter="gurahl", condition="ursine"
)[0]
gurahl_arthren = GiftPermission.objects.get_or_create(
    shifter="gurahl", condition="arthren"
)[0]

# Gurahl Auspices
arcas = GiftPermission.objects.get_or_create(shifter="gurahl", condition="arcas")[0]
uzmati = GiftPermission.objects.get_or_create(shifter="gurahl", condition="uzmati")[0]
kojubat = GiftPermission.objects.get_or_create(shifter="gurahl", condition="kojubat")[0]
kieh = GiftPermission.objects.get_or_create(shifter="gurahl", condition="kieh")[0]

# Gurahl Breed Gifts
g = Gift.objects.get_or_create(name="Mother's Touch", rank=1)[0]
g.allowed.add(gurahl_homid, kieh)
g.description = "Heal wounds with a touch."
g.save()

g = Gift.objects.get_or_create(name="Bear's Strength", rank=1)[0]
g.allowed.add(gurahl_ursine)
g.description = "Gain immense physical strength."
g.save()

# Gurahl Auspice Gifts
g = Gift.objects.get_or_create(name="Survivor", rank=1)[0]
g.allowed.add(arcas)
g.description = "Endure extreme conditions."
g.save()

g = Gift.objects.get_or_create(name="Truth of Gaia", rank=1)[0]
g.allowed.add(uzmati)
g.description = "Detect lies and falsehoods."
g.save()

g = Gift.objects.get_or_create(name="Umbral Bridge", rank=1)[0]
g.allowed.add(kojubat)
g.description = "Step sideways more easily."
g.save()

g = Gift.objects.get_or_create(name="Healing Touch", rank=1)[0]
g.allowed.add(kieh)
g.description = "Heal diseases and poisons."
g.save()

# ===============================
# RATKIN (Wererat) GIFTS
# ===============================

ratkin_homid = GiftPermission.objects.get_or_create(
    shifter="ratkin", condition="homid"
)[0]
ratkin_rodent = GiftPermission.objects.get_or_create(
    shifter="ratkin", condition="rodent"
)[0]
ratkin_metis = GiftPermission.objects.get_or_create(
    shifter="ratkin", condition="metis"
)[0]

# Ratkin Aspects
tunnel_runner = GiftPermission.objects.get_or_create(
    shifter="ratkin", condition="tunnel_runner"
)[0]
warrior = GiftPermission.objects.get_or_create(shifter="ratkin", condition="warrior")[0]
plague_lord = GiftPermission.objects.get_or_create(
    shifter="ratkin", condition="plague_lord"
)[0]
tinkerer = GiftPermission.objects.get_or_create(shifter="ratkin", condition="tinkerer")[
    0
]
shadow_seer = GiftPermission.objects.get_or_create(
    shifter="ratkin", condition="shadow_seer"
)[0]

# Ratkin Breed Gifts
g = Gift.objects.get_or_create(name="Survivor's Luck", rank=1)[0]
g.allowed.add(ratkin_homid)
g.description = "Survive against impossible odds."
g.save()

g = Gift.objects.get_or_create(name="Rat's Feet", rank=1)[0]
g.allowed.add(ratkin_rodent)
g.description = "Squeeze through impossibly small spaces."
g.save()

g = Gift.objects.get_or_create(name="Tunnel Sense", rank=1)[0]
g.allowed.add(ratkin_metis)
g.description = "Never get lost underground."
g.save()

# Ratkin Aspect Gifts
g = Gift.objects.get_or_create(name="Urban Tracker", rank=1)[0]
g.allowed.add(tunnel_runner)
g.description = "Track anyone through a city."
g.save()

g = Gift.objects.get_or_create(name="Bite of the Swarm", rank=1)[0]
g.allowed.add(warrior)
g.description = "Summon rats to attack enemies."
g.save()

g = Gift.objects.get_or_create(name="Plague Carrier", rank=1)[0]
g.allowed.add(plague_lord)
g.description = "Spread disease to enemies."
g.save()

g = Gift.objects.get_or_create(name="Jury-Rig", rank=1)[0]
g.allowed.add(tinkerer)
g.description = "Fix or sabotage technology."
g.save()

g = Gift.objects.get_or_create(name="Eyes of the Rat", rank=1)[0]
g.allowed.add(shadow_seer)
g.description = "See through the eyes of rats."
g.save()

# ===============================
# MOKOLE (Weresaurian) GIFTS
# ===============================

mokole_homid = GiftPermission.objects.get_or_create(
    shifter="mokole", condition="homid"
)[0]
mokole_suchid = GiftPermission.objects.get_or_create(
    shifter="mokole", condition="suchid"
)[0]
mokole_metis = GiftPermission.objects.get_or_create(
    shifter="mokole", condition="metis"
)[0]

# Mokole Streams
makara = GiftPermission.objects.get_or_create(shifter="mokole", condition="makara")[0]
zhong_lung = GiftPermission.objects.get_or_create(
    shifter="mokole", condition="zhong_lung"
)[0]
gumagan = GiftPermission.objects.get_or_create(shifter="mokole", condition="gumagan")[0]

# Mokole Auspices
rising_sun = GiftPermission.objects.get_or_create(
    shifter="mokole", condition="rising_sun"
)[0]
noonday_sun = GiftPermission.objects.get_or_create(
    shifter="mokole", condition="noonday_sun"
)[0]
setting_sun = GiftPermission.objects.get_or_create(
    shifter="mokole", condition="setting_sun"
)[0]

# Mokole Gifts
g = Gift.objects.get_or_create(name="Crocodile's Jaws", rank=1)[0]
g.allowed.add(mokole_suchid)
g.description = "Incredibly powerful bite attack."
g.save()

g = Gift.objects.get_or_create(name="Dragon's Breath", rank=2)[0]
g.allowed.add(rising_sun)
g.description = "Breathe fire at enemies."
g.save()

g = Gift.objects.get_or_create(name="Mnesis", rank=1)[0]
g.allowed.add(setting_sun)
g.description = "Access racial memories of the past."
g.save()

# ===============================
# NUWISHA (Werecoyote) GIFTS
# ===============================

nuwisha = GiftPermission.objects.get_or_create(shifter="nuwisha", condition="nuwisha")[
    0
]
nuwisha_homid = GiftPermission.objects.get_or_create(
    shifter="nuwisha", condition="homid"
)[0]
nuwisha_latrani = GiftPermission.objects.get_or_create(
    shifter="nuwisha", condition="latrani"
)[0]

# Nuwisha Gifts
g = Gift.objects.get_or_create(name="Coyote's Laugh", rank=1)[0]
g.allowed.add(nuwisha)
g.description = "Cause enemies to laugh uncontrollably."
g.save()

g = Gift.objects.get_or_create(name="Trickster's Wisdom", rank=1)[0]
g.allowed.add(nuwisha)
g.description = "See through deceptions and illusions."
g.save()

g = Gift.objects.get_or_create(name="Foolish Bravery", rank=1)[0]
g.allowed.add(nuwisha)
g.description = "Inspire foolhardy courage in others."
g.save()

g = Gift.objects.get_or_create(name="Coyote's Lesson", rank=2)[0]
g.allowed.add(nuwisha)
g.description = "Teach humility through pranks."
g.save()

g = Gift.objects.get_or_create(name="Shape of Coyote's Prank", rank=1)[0]
g.allowed.add(nuwisha_latrani)
g.description = "Take on the form of anyone."
g.save()
