from characters.models.werewolf.gift import Gift, GiftPermission

# Breed
homid = GiftPermission.objects.get_or_create(shifter="werewolf", condition="homid")[0]
lupus = GiftPermission.objects.get_or_create(shifter="werewolf", condition="lupus")[0]
metis = GiftPermission.objects.get_or_create(shifter="werewolf", condition="metis")[0]

# Auspice
ragabash = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="ragabash"
)[0]
theurge = GiftPermission.objects.get_or_create(shifter="werewolf", condition="theurge")[
    0
]
philodox = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="philodox"
)[0]
galliard = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="galliard"
)[0]
ahroun = GiftPermission.objects.get_or_create(shifter="werewolf", condition="ahroun")[0]

# Tribe
get_of_fenris = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Get of Fenris"
)[0]
croatan = GiftPermission.objects.get_or_create(shifter="werewolf", condition="Croatan")[
    0
]

black_furies = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Black Furies"
)[0]
bone_gnawers = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Bone Gnawers"
)[0]
children_of_gaia = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Children of Gaia"
)[0]
fianna = GiftPermission.objects.get_or_create(shifter="werewolf", condition="Fianna")[0]
glass_walker = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Glass Walkers"
)[0]
red_talons = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Red Talons"
)[0]
shadow_lords = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Shadow Lords"
)[0]
silent_striders = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Silent Striders"
)[0]
silver_fangs = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Silver Fangs"
)[0]
stargazers = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Stargazers"
)[0]
uktena = GiftPermission.objects.get_or_create(shifter="werewolf", condition="Uktena")[0]
wendigo = GiftPermission.objects.get_or_create(shifter="werewolf", condition="Wendigo")[
    0
]

black_spiral_dancers = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Black Spiral Dancers"
)[0]

bunyip = GiftPermission.objects.get_or_create(shifter="werewolf", condition="Bunyip")[0]
white_howlers = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="White Howlers"
)[0]


kucha_ekundu = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Kucha Ekundu"
)[0]
boli_zousizhe = GiftPermission.objects.get_or_create(
    shifter="werewolf", condition="Boli Zousizhe"
)[0]
kinfolk = GiftPermission.objects.get_or_create(shifter="werewolf", condition="Kinfolk")[
    0
]
hakken = GiftPermission.objects.get_or_create(shifter="werewolf", condition="Hakken")[0]


g = Gift.objects.get_or_create(name="Apecraft's Blessings", rank=1)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(name="City Running", rank=1)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(name="Master of Fire", rank=1)[0]
g.allowed.add(homid, get_of_fenris, croatan)

g = Gift.objects.get_or_create(name="Persuasion", rank=1)[0]
g.allowed.add(homid, philodox, fianna, glass_walker)

g = Gift.objects.get_or_create(name="Smell of Man", rank=1)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(name="Jam Technology", rank=2)[0]
g.allowed.add(homid, glass_walker)

g = Gift.objects.get_or_create(name="Mark of the Wolf", rank=2)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(name="Speech of the World", rank=2)[0]
g.allowed.add(homid, silent_striders)

g = Gift.objects.get_or_create(name="Staredown", rank=2)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(
    name="Calm the Savage Beast",
    rank=3,
)[0]
g.allowed.add(homid, children_of_gaia)

g = Gift.objects.get_or_create(name="Cowing the Bullet", rank=3)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(name="Disquiet", rank=3)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(
    name="Reshape Object",
    rank=3,
)[0]
g.allowed.add(homid, bone_gnawers, fianna)

g = Gift.objects.get_or_create(name="Body Shift", rank=4)[0]
g.allowed.add(homid, ahroun, get_of_fenris)

g = Gift.objects.get_or_create(name="Bury the Wolf", rank=4)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(name="Cocoon", rank=4)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(name="Spirit Ward", rank=4)[0]
g.allowed.add(homid, theurge)

g = Gift.objects.get_or_create(name="Assimilation", rank=5)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(name="Beyond Human", rank=5)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(name="Part the Veil", rank=5)[0]
g.allowed.add(homid)

g = Gift.objects.get_or_create(name="Create Element", rank=1)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Primal Anger", rank=1)[0]
g.allowed.add(metis, white_howlers)

g = Gift.objects.get_or_create(name="Rat Head", rank=1)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(
    name="Sense Wyrm",
    rank=1,
)[0]
g.allowed.add(
    metis,
    theurge,
    black_furies,
    silent_striders,
    silver_fangs,
    stargazers,
    uktena,
    black_spiral_dancers,
    white_howlers,
)

g = Gift.objects.get_or_create(name="Shed", rank=1)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Burrow", rank=2)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Curse of Hatred", rank=2)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(
    name="Form Mastery",
    rank=2,
)[0]
g.allowed.add(metis, black_furies, fianna)

g = Gift.objects.get_or_create(
    name="Sense Silver",
    rank=2,
)[0]
g.allowed.add(metis, ahroun, silver_fangs)

g = Gift.objects.get_or_create(name="Chameleon", rank=2)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Eyes of the Cat", rank=3)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Mental Speech", rank=3)[0]
g.allowed.add(metis, philodox)

g = Gift.objects.get_or_create(name="Shell", rank=3)[0]
g.allowed.add(metis, croatan)

g = Gift.objects.get_or_create(name="Gift of the Porcupine", rank=4)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Lash of Rage", rank=4)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Rattler's Bite", rank=4)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Wither Limb", rank=4)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Madness", rank=5)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Protean Form", rank=5)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Totem Gift", rank=5)[0]
g.allowed.add(metis)

g = Gift.objects.get_or_create(name="Hare's Leap", rank=1)[0]
g.allowed.add(lupus, fianna)

g = Gift.objects.get_or_create(
    name="Heightened Senses",
    rank=1,
)[0]
g.allowed.add(lupus, galliard, black_furies)

g = Gift.objects.get_or_create(name="Sense Prey", rank=1)[0]
g.allowed.add(lupus, bunyip)

g = Gift.objects.get_or_create(name="Predator's Arsenal", rank=1)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(name="Prey Mind", rank=1)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(name="Axis Mundi", rank=2)[0]
g.allowed.add(lupus, silent_striders)

g = Gift.objects.get_or_create(name="Eye of the Eagle", rank=2)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(name="Name the Spirit", rank=2)[0]
g.allowed.add(lupus, theurge)

g = Gift.objects.get_or_create(name="Scent of Sight", rank=2)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(name="Catfeet", rank=3)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(name="Monkey Tail", rank=3)[0]
g.allowed.add(lupus, ragabash)

g = Gift.objects.get_or_create(
    name="Sense the Unnatural",
    rank=3,
)[0]
g.allowed.add(lupus, silent_striders)

g = Gift.objects.get_or_create(name="Silence the Weaver", rank=3)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(name="Strength of Gaia", rank=3)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(
    name="Beast Life",
    rank=4,
)[0]
g.allowed.add(lupus, black_furies, children_of_gaia)

g = Gift.objects.get_or_create(name="Gnaw", rank=4)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(name="Scream of Gaia", rank=4)[0]
g.allowed.add(lupus, get_of_fenris)

g = Gift.objects.get_or_create(name="Terror of the Dire Wolf", rank=4)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(name="Elemental Gift", rank=5)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(name="Song of the Great Beast", rank=5)[0]
g.allowed.add(lupus)

g = Gift.objects.get_or_create(name="Blur of the Milky Eye", rank=1)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Infectious Laughter", rank=1)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Liar's Face", rank=1)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Open Seal", rank=1)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(
    name="Scent of Running Water",
    rank=1,
)[0]
g.allowed.add(ragabash, red_talons)

g = Gift.objects.get_or_create(
    name="Blissful Ignorance",
    rank=2,
)[0]
g.allowed.add(ragabash, bone_gnawers, silent_striders)

g = Gift.objects.get_or_create(
    name="Pulse of the Prey",
    rank=2,
)[0]
g.allowed.add(ragabash, black_furies, red_talons)

g = Gift.objects.get_or_create(name="Spider's Song", rank=2)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Taking the Forgotten", rank=2)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Gremlins", rank=3)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Liar's Craft", rank=3)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Open Moon Bridge", rank=3)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Pathfinder", rank=3)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Luna's Blessing", rank=4)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Umbral Dodge", rank=4)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Whelp Body", rank=4)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Thieving Talons of the Magpie", rank=5)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(name="Thousand Forms", rank=5)[0]
g.allowed.add(ragabash, black_furies)

g = Gift.objects.get_or_create(name="Firebringer", rank=6)[0]
g.allowed.add(ragabash)

g = Gift.objects.get_or_create(
    name="Mother's Touch",
    rank=1,
)[0]
g.allowed.add(theurge, children_of_gaia, bunyip)

g = Gift.objects.get_or_create(name="Spirit Snare", rank=1)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Spirit Speech", rank=1)[0]
g.allowed.add(theurge, uktena)

g = Gift.objects.get_or_create(name="Umbral Tether", rank=1)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Battle Mandala", rank=2)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Command Spirit", rank=2)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Sight From Beyond", rank=2)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Exorcism", rank=3)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Pulse of the Invisible", rank=3)[0]
g.allowed.add(theurge, bunyip)

g = Gift.objects.get_or_create(name="Umbral Camouflage", rank=3)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Web Walker", rank=3)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Blurring the Mirror", rank=4)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Grasp of Beyond", rank=4)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Spirit Drain", rank=4)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Feral Lobotomy", rank=5)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Malleable Spirit", rank=5)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Ultimate Argument of Logic", rank=5)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="As in the Beginning", rank=6)[0]
g.allowed.add(theurge)

g = Gift.objects.get_or_create(name="Fangs of Judgment", rank=1)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(
    name="Resist Pain",
    rank=1,
)[0]
g.allowed.add(philodox, children_of_gaia, get_of_fenris, wendigo, black_spiral_dancers)

g = Gift.objects.get_or_create(name="Scent of the True Form", rank=1)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(name="Truth of Gaia", rank=1)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(name="Call to Duty", rank=2)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(name="Command the Gathering", rank=2)[0]
g.allowed.add(philodox, galliard)

g = Gift.objects.get_or_create(name="King of the Beasts", rank=2)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(name="Strength of Purpose", rank=2)[0]
g.allowed.add(philodox, croatan)

g = Gift.objects.get_or_create(name="Scent of the Oathbreaker", rank=3)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(name="Sense Balance", rank=3)[0]
g.allowed.add(philodox, stargazers)

g = Gift.objects.get_or_create(name="Weak Arm", rank=3)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(
    name="Wisdom of the Ancient Ways",
    rank=3,
)[0]
g.allowed.add(philodox, wendigo)

g = Gift.objects.get_or_create(name="Roll Over", rank=4)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(name="Scent of Beyond", rank=4)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(name="Take the True Form", rank=4)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(name="Geas", rank=5)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(name="Wall of Granite", rank=5)[0]
g.allowed.add(philodox)

g = Gift.objects.get_or_create(name="Break the Bonds", rank=6)[0]
g.allowed.add(philodox, galliard)

g = Gift.objects.get_or_create(name="Beast Speech", rank=1)[0]
g.allowed.add(galliard, red_talons)

g = Gift.objects.get_or_create(name="Call of the Wyld", rank=1)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Mindspeak", rank=1)[0]
g.allowed.add(galliard, croatan)

g = Gift.objects.get_or_create(name="Perfect Recall", rank=1)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Call of the Wyrm", rank=2)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Distractions", rank=2)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Dreamspeak", rank=2)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(
    name="Howls in the Night",
    rank=2,
)[0]
g.allowed.add(galliard, red_talons, shadow_lords, white_howlers)

g = Gift.objects.get_or_create(name="Eye of the Cobra", rank=3)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Song of Heroes", rank=3)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Song of Rage", rank=3)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Song of the Siren", rank=3)[0]
g.allowed.add(galliard, fianna)

g = Gift.objects.get_or_create(name="Bridge Walker", rank=4)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Gift of Dreams", rank=4)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Shadows by the Firelight", rank=4)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Fabric of the Mind", rank=4)[0]
g.allowed.add(galliard, uktena)

g = Gift.objects.get_or_create(name="Head Games", rank=5)[0]
g.allowed.add(galliard)

g = Gift.objects.get_or_create(name="Falling Touch", rank=1)[0]
g.allowed.add(ahroun, stargazers)

g = Gift.objects.get_or_create(name="Inspiration", rank=1)[0]
g.allowed.add(ahroun, silver_fangs)

g = Gift.objects.get_or_create(name="Pack Tactics", rank=1)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Razor Claws", rank=1)[0]
g.allowed.add(ahroun, get_of_fenris)

g = Gift.objects.get_or_create(name="Spur Claws", rank=1)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Shield of Rage", rank=2)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Spirit of the Fray", rank=2)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="True Fear", rank=2)[0]
g.allowed.add(ahroun, wendigo)

g = Gift.objects.get_or_create(name="Combat Healing", rank=3)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Heart of Fury", rank=3)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Silver Claws", rank=3)[0]
g.allowed.add(ahroun, silver_fangs)

g = Gift.objects.get_or_create(name="Wind Claws", rank=3)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Clenched Jaw", rank=4)[0]
g.allowed.add(ahroun, kucha_ekundu)

g = Gift.objects.get_or_create(name="Full Moon's Light", rank=4)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Stoking Fury's Furnace", rank=4)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Kiss of Helios", rank=5)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Strength of Will", rank=5)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Unstoppable Warrior", rank=6)[0]
g.allowed.add(ahroun)

g = Gift.objects.get_or_create(name="Breath of the Wyld", rank=1)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Man's Skin", rank=1)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Wyld Resurgence", rank=1)[0]
g.allowed.add(black_furies, croatan)

g = Gift.objects.get_or_create(name="Curse of Aeolus", rank=2)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Kali's Tongue", rank=2)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Kneel", rank=2)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Coup de Grace", rank=3)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Heart Claw", rank=3)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Visceral Agony", rank=3)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Wings of PEgasus", rank=3)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Body Wrack", rank=4)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Wasp Talons", rank=4)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Gorgon's Gaze", rank=5)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Wyld Warp", rank=5)[0]
g.allowed.add(black_furies)

g = Gift.objects.get_or_create(name="Cooking", rank=1)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(
    name="Desperate Strength",
    rank=1,
)[0]
g.allowed.add(bone_gnawers, white_howlers)

g = Gift.objects.get_or_create(
    name="Resist Toxin",
    rank=1,
)[0]
g.allowed.add(bone_gnawers, fianna, black_spiral_dancers, bunyip)

g = Gift.objects.get_or_create(name="Scent of Sweet Honey", rank=1)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Trash is Treasure", rank=1)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Between the Cracks", rank=2)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Cornered Rat's Ferocity", rank=2)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Guide of the Hound", rank=2)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Odious Aroma", rank=2)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Call the Rust", rank=3)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Gift of the Skunk", rank=3)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Gift of the Termite", rank=3)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Laugh of the Hyena", rank=3)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(
    name="Attunement",
    rank=4,
)[0]
g.allowed.add(bone_gnawers, glass_walker, silent_striders)

g = Gift.objects.get_or_create(name="Blink", rank=4)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Infest", rank=4)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Riot", rank=5)[0]
g.allowed.add(bone_gnawers)

g = Gift.objects.get_or_create(name="Survivor", rank=5)[0]
g.allowed.add(bone_gnawers, croatan)

g = Gift.objects.get_or_create(name="Brother's Scent", rank=1)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Jam Weapon", rank=1)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Mercy", rank=1)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Calm", rank=2)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Grandmother's Touch", rank=2)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(
    name="Luna's Armor",
    rank=2,
)[0]
g.allowed.add(children_of_gaia, shadow_lords, silver_fangs)

g = Gift.objects.get_or_create(name="Para Bellum", rank=2)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Unicorn's Arsenal", rank=2)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Dazzle", rank=3)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Lover's Touch", rank=3)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Spirit Friend", rank=3)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Serenity", rank=4)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(
    name="Strike the Air",
    rank=4,
)[0]
g.allowed.add(children_of_gaia, stargazers)

g = Gift.objects.get_or_create(
    name="Uncought Since the Primal Morn",
    rank=4,
)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Halo of the Sun", rank=5)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="The Living Wood", rank=5)[0]
g.allowed.add(children_of_gaia)

g = Gift.objects.get_or_create(name="Faerie Light", rank=1)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Two Tongues", rank=1)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Glib Tongue", rank=2)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Flame Dance", rank=2)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Howl of the Banshee", rank=2)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Howl of the Unseen", rank=2)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Faerie Kin", rank=3)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Fair Fortune", rank=3)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Ley Lines", rank=3)[0]
g.allowed.add(fianna, white_howlers)

g = Gift.objects.get_or_create(name="Balor's Gaze", rank=4)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Phantasm", rank=4)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Call the Hunt", rank=5)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Fog on the Moor", rank=5)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Gift of the Spriggan", rank=5)[0]
g.allowed.add(fianna)

g = Gift.objects.get_or_create(name="Lightning Reflexes", rank=1)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Visage of Fenris", rank=1)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Fangs of the North", rank=2)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Halt the Coward's Flight", rank=2)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Snarl of the Predator", rank=2)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Troll Skin", rank=2)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Might of Thor", rank=3)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Redirect Pain", rank=3)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Venom Blood", rank=3)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Heart of the Mountain", rank=4)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(
    name="Hero's Stand",
    rank=4,
)[0]
g.allowed.add(get_of_fenris, white_howlers)

g = Gift.objects.get_or_create(name="Endurance of Heimdall", rank=5)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Horde of Valhalla", rank=5)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Fenris' Bite", rank=5)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Call Great Fenris", rank=6)[0]
g.allowed.add(get_of_fenris)

g = Gift.objects.get_or_create(name="Control Simple Machine", rank=1)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Diagnostics", rank=1)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Plug and Play", rank=1)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Trick Shot", rank=1)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Cybersenses", rank=2)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Hands Full of Thunder", rank=2)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Power Surge", rank=2)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Steel Fur", rank=2)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Control Complex Machine", rank=3)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Intrusion", rank=3)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Electroshock", rank=3)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(
    name="Elemental Favor",
    rank=3,
)[0]
g.allowed.add(glass_walker, red_talons)

g = Gift.objects.get_or_create(name="Doppelganger", rank=4)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Signal Rider", rank=4)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Tech Speak", rank=4)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Chaos Mechanics", rank=5)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Summon Net-Spider", rank=5)[0]
g.allowed.add(glass_walker)

g = Gift.objects.get_or_create(name="Eye of the Hunter", rank=1)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Hidden Killer", rank=1)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Wolf at the Door", rank=1)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Beastmind", rank=2)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Shadows of the Impergium", rank=2)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Render Down", rank=3)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Territory", rank=3)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Trackless Waste", rank=3)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Gorge", rank=4)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Howl of Death", rank=4)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Quicksand", rank=4)[0]
g.allowed.add(red_talons, bunyip)

g = Gift.objects.get_or_create(name="Curse of Lycaon", rank=5)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(
    name="Gaia's Vengeance",
    rank=5,
)[0]
g.allowed.add(red_talons, white_howlers)

g = Gift.objects.get_or_create(name="Scabwalker Curse", rank=5)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Shield of Gaia", rank=6)[0]
g.allowed.add(red_talons)

g = Gift.objects.get_or_create(name="Aura of Confidence", rank=1)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Fatal Flaw", rank=1)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Seizing the Edge", rank=1)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Shadow Weaving", rank=1)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Whisper Catching", rank=1)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Clap of Thunder", rank=2)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Cold Voice of Reason", rank=2)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Song of the Earth Mother", rank=2)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Direct the Storm", rank=3)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Icy Chill of Despair", rank=3)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Paralyzing Stare", rank=3)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Shadow Cutting", rank=3)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Under the Gun", rank=3)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(
    name="Open Wounds",
    rank=4,
)[0]
g.allowed.add(shadow_lords, black_spiral_dancers)

g = Gift.objects.get_or_create(name="Durance", rank=4)[0]
g.allowed.add(shadow_lords, uktena)

g = Gift.objects.get_or_create(name="Strength of the Dominator", rank=4)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Obedience", rank=5)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Shadow Pack", rank=5)[0]
g.allowed.add(shadow_lords)

g = Gift.objects.get_or_create(name="Heaven's Guidance", rank=1)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Silence", rank=1)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(
    name="Speed of Thought",
    rank=1,
)[0]
g.allowed.add(silent_striders, kucha_ekundu)

g = Gift.objects.get_or_create(name="Visions of Duat", rank=1)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Messenger's Fortitude", rank=2)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Tread Sebek's Back", rank=2)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Adaptation", rank=3)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Great Leap", rank=3)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Mark of the Death-Wolf", rank=3)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Black Mark", rank=4)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Dam the Heartflood", rank=4)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Speed Beyond Thought", rank=4)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Gate of the Moon", rank=5)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Reach the Umbra", rank=5)[0]
g.allowed.add(silent_striders)

g = Gift.objects.get_or_create(name="Eye of the Falcon", rank=1)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Falcon's Grasp", rank=1)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Lambent Flame", rank=1)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Empathy", rank=2)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Hand Blade", rank=2)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Unity of the Pack", rank=2)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Burning Blade", rank=3)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Talons of the Falcon", rank=3)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Wrath of Gaia", rank=3)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Mastery", rank=4)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Mindblock", rank=4)[0]
g.allowed.add(silver_fangs, stargazers)

g = Gift.objects.get_or_create(name="Sidestep Death", rank=4)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Luna's Avenger", rank=5)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Paws of the Newborn Cub", rank=5)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Renew the Cycle", rank=6)[0]
g.allowed.add(silver_fangs)

g = Gift.objects.get_or_create(name="Balance", rank=1)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Channeling", rank=1)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Iron Resolve", rank=1)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Inner Light", rank=2)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Inner Strength", rank=2)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Resist Temptation", rank=2)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Surface Attunement", rank=2)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Wuxing", rank=2)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Clarity", rank=3)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Mericful Blow", rank=3)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Wind's Returning Favor", rank=3)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Preternatural Awareness", rank=4)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Circular Attack", rank=5)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(
    name="Harmorious Unity of the Emeral Mother",
    rank=5,
)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Wisdom of the Seer", rank=5)[0]
g.allowed.add(stargazers)

g = Gift.objects.get_or_create(name="Sense Magic", rank=1)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Shroud", rank=1)[0]
g.allowed.add(uktena, black_spiral_dancers)

g = Gift.objects.get_or_create(name="Spirit of the Lizard", rank=1)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Coils of the Serpent", rank=2)[0]
g.allowed.add(uktena, bunyip)

g = Gift.objects.get_or_create(name="Fetish Fetch", rank=2)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Shadows at Dawn", rank=2)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Spirit of the Bird", rank=2)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Spirit of the Fish", rank=2)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Banish Totem", rank=3)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Chains of Mist", rank=3)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Invisibility", rank=3)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Rending the Craft", rank=3)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Scrying", rank=3)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(
    name="Call Elemental",
    rank=4,
)[0]
g.allowed.add(uktena, black_spiral_dancers)

g = Gift.objects.get_or_create(name="Hand of the Earth Lords", rank=4)[0]
g.allowed.add(uktena, croatan)

g = Gift.objects.get_or_create(name="Fetish Doll", rank=5)[0]
g.allowed.add(uktena)

g = Gift.objects.get_or_create(name="Beat of the Heart-Drum", rank=1)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Call the Breeze", rank=1)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Camouflage", rank=1)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Ice Echo", rank=1)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Cutting Wind", rank=2)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Claws of Frozen Death", rank=2)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Salmon Swim", rank=2)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Speak with Wind Spirits", rank=2)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Blood of the North", rank=3)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Bloody Feast", rank=3)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Sky Running", rank=3)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Call of the Cannibal Spirit", rank=4)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Chill of Early Frost", rank=4)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Invoke the Spirits of the Storm", rank=5)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="Heart of Ice", rank=5)[0]
g.allowed.add(wendigo)

g = Gift.objects.get_or_create(name="See Past the Skin", rank=1)[0]
g.allowed.add(black_spiral_dancers)

g = Gift.objects.get_or_create(name="Mask Taint", rank=5)[0]
g.allowed.add(black_spiral_dancers)

g = Gift.objects.get_or_create(name="Bane Protector", rank=1)[0]
g.allowed.add(black_spiral_dancers)

g = Gift.objects.get_or_create(
    name="Smell Fear",
    rank=2,
)[0]
g.allowed.add(black_spiral_dancers, philodox)

g = Gift.objects.get_or_create(name="Ears of the Bat", rank=2)[0]
g.allowed.add(black_spiral_dancers)

g = Gift.objects.get_or_create(name="Wyrm Hide", rank=2)[0]
g.allowed.add(black_spiral_dancers)

g = Gift.objects.get_or_create(
    name="A Thousand Voices",
    rank=2,
)[0]
g.allowed.add(black_spiral_dancers, theurge)

g = Gift.objects.get_or_create(
    name="Allies Below",
    rank=2,
)[0]
g.allowed.add(black_spiral_dancers, galliard)

g = Gift.objects.get_or_create(
    name="Horns of the Impaler",
    rank=2,
)[0]
g.allowed.add(black_spiral_dancers, ahroun)

g = Gift.objects.get_or_create(name="Patagia", rank=3)[0]
g.allowed.add(black_spiral_dancers)

g = Gift.objects.get_or_create(name="Foaming Fury", rank=3)[0]
g.allowed.add(black_spiral_dancers)

g = Gift.objects.get_or_create(name="Beautiful Lie", rank=3)[0]
g.allowed.add(black_spiral_dancers)

g = Gift.objects.get_or_create(
    name="Touch of the Eer",
    rank=3,
)[0]
g.allowed.add(black_spiral_dancers, ragabash)

g = Gift.objects.get_or_create(name="Crawling Poison", rank=4)[0]
g.allowed.add(black_spiral_dancers)

g = Gift.objects.get_or_create(name="Balefire", rank=5)[0]
g.allowed.add(black_spiral_dancers)

g = Gift.objects.get_or_create(name="Dream of a Thousand Cranes", rank=1)[0]
g.allowed.add(hakken)

g = Gift.objects.get_or_create(name="Fair Path", rank=1)[0]
g.allowed.add(hakken)

g = Gift.objects.get_or_create(name="Storm Winds Slash", rank=2)[0]
g.allowed.add(hakken)

g = Gift.objects.get_or_create(name="Dark of Night", rank=3)[0]
g.allowed.add(hakken)

g = Gift.objects.get_or_create(name="Living Treasure", rank=4)[0]
g.allowed.add(hakken)

g = Gift.objects.get_or_create(name="Divine Wind", rank=5)[0]
g.allowed.add(hakken)

g = Gift.objects.get_or_create(name="Sheng-Nong's Eyes", rank=1)[0]
g.allowed.add(boli_zousizhe)

g = Gift.objects.get_or_create(name="Fu Xi's Honor", rank=2)[0]
g.allowed.add(boli_zousizhe)

g = Gift.objects.get_or_create(name="Yao's Commands", rank=3)[0]
g.allowed.add(boli_zousizhe)

g = Gift.objects.get_or_create(name="Yu's Endurance", rank=4)[0]
g.allowed.add(boli_zousizhe)

g = Gift.objects.get_or_create(name="Huang Di's Sacrifice", rank=5)[0]
g.allowed.add(boli_zousizhe)

g = Gift.objects.get_or_create(name="Feed the Pack", rank=2)[0]
g.allowed.add(kucha_ekundu)

g = Gift.objects.get_or_create(name="Predator's Many Eyes", rank=3)[0]
g.allowed.add(kucha_ekundu)

g = Gift.objects.get_or_create(name="Crocodile Pact", rank=5)[0]
g.allowed.add(kucha_ekundu)

g = Gift.objects.get_or_create(name="Bunyip's Spell", rank=1)[0]
g.allowed.add(bunyip)

g = Gift.objects.get_or_create(name="Crocodile's Cunning", rank=2)[0]
g.allowed.add(bunyip)

g = Gift.objects.get_or_create(name="Lonesome Voice of the Bunyip", rank=3)[0]
g.allowed.add(bunyip)

g = Gift.objects.get_or_create(name="Dance of the Lightning Snakes", rank=4)[0]
g.allowed.add(bunyip)

g = Gift.objects.get_or_create(name="Billabong Bridge", rank=5)[0]
g.allowed.add(bunyip)

g = Gift.objects.get_or_create(name="Turtle Body", rank=1)[0]
g.allowed.add(croatan)

g = Gift.objects.get_or_create(name="Turtle Shell", rank=2)[0]
g.allowed.add(croatan)

g = Gift.objects.get_or_create(name="Call Earth Spirit", rank=3)[0]
g.allowed.add(croatan)

g = Gift.objects.get_or_create(name="Stronger on Stone", rank=4)[0]
g.allowed.add(croatan)

g = Gift.objects.get_or_create(name="Katanka-Sonnak's Spear", rank=5)[0]
g.allowed.add(croatan)

g = Gift.objects.get_or_create(name="Haunting Howl", rank=1)[0]
g.allowed.add(white_howlers)

g = Gift.objects.get_or_create(name="Pain-Strength", rank=2)[0]
g.allowed.add(white_howlers)

g = Gift.objects.get_or_create(name="Sense of the Deep", rank=3)[0]
g.allowed.add(white_howlers)

g = Gift.objects.get_or_create(name="Maddening Howl", rank=4)[0]
g.allowed.add(white_howlers)

g = Gift.objects.get_or_create(name="Mad Strength", rank=5)[0]
g.allowed.add(white_howlers)

g = Gift.objects.get_or_create(name="Eve's Touch", rank=1)[0]
g.allowed.add(kinfolk)

g = Gift.objects.get_or_create(name="Dona Nobis Pacem", rank=1)[0]
g.allowed.add(kinfolk)

g = Gift.objects.get_or_create(name="Echoes", rank=1)[0]
g.allowed.add(kinfolk)
