from characters.models.demon.house import DemonHouse
from items.models.demon.relic import Relic
from populate_db.demon_houses import (
    defilers,
    devils,
    devourers,
    malefactors,
    scourges,
    slayers,
)

# Devil House Relics
pyrestone = Relic.objects.get_or_create(
    name="Pyrestone (Frozen Flames)",
    house=devils,
    relic_type="house_specific",
    lore_used="Lore of Flame",
    power="Clear crystal containing trapped fire; activated remotely; explodes with Ignite evocation intensity",
    material="Clear crystal",
    dice_pool=8,
    difficulty=7,
)[0]

first_tongue_scripture = Relic.objects.get_or_create(
    name="First Tongue Scripture",
    house=devils,
    relic_type="house_specific",
    lore_used="Lore of Radiance",
    power="Mortals who learn become immune to illusions and demonic Revelation; can compel others through subconscious commands",
    material="Ancient texts",
    difficulty=8,
)[0]

# Scourge House Relics

armor_of_air = Relic.objects.get_or_create(
    name="Armor of Air",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of the Winds",
    power="Brooch/buckle generating protective air shell; 6 dice pool for ranged attack soak",
    material="Silver brooch or buckle",
    dice_pool=6,
    difficulty=6,
)[0]

cordial_of_dagan = Relic.objects.get_or_create(
    name="Cordial of Dagan",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of Awakening",
    power="Flask that converts liquids to heal sickness; 8 dice pool for healing",
    material="Crystal flask",
    dice_pool=8,
    difficulty=7,
)[0]

crystal_ball = Relic.objects.get_or_create(
    name="Crystal Ball",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of the Firmament",
    power="Round crystal sphere for scrying; difficulty varies by target name knowledge",
    material="Crystal sphere",
    difficulty=7,
)[0]

eagle_eyes = Relic.objects.get_or_create(
    name="Eagle Eyes",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of the Firmament",
    power="Crystal lenses improving sight 10-fold; -3 difficulty to Perception rolls",
    material="Crystal lenses",
    difficulty=4,
)[0]

jar_of_winds = Relic.objects.get_or_create(
    name="Jar of Winds",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of the Winds",
    power="Container with trapped winds; 8 dice pool for force effects",
    material="Clay or glass jar",
    dice_pool=8,
    difficulty=7,
)[0]

needs_beacon = Relic.objects.get_or_create(
    name="Need's Beacon",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of the Winds",
    power="Glass tube/crystal bauble; sends distress cry to creator when broken",
    material="Glass tube or crystal",
    difficulty=6,
)[0]

plague_knife = Relic.objects.get_or_create(
    name="Plague-Knife",
    house=scourges,
    relic_type="house_specific",
    lore_used="Lore of Awakening",
    power="Black dagger dealing disease; 10 dice pool; inflicts bashing disease damage daily",
    material="Black iron dagger",
    dice_pool=10,
    difficulty=7,
)[0]

# Malefactor House Relics

thala_mkudan = Relic.objects.get_or_create(
    name="Thala-m'kudan (The Hidden Mountain)",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of Paths",
    power="Largest mountain ever existed, now in platinum shoebox; sacred meeting place for Annunaki",
    material="Mountain in platinum box",
    complexity=10,
    is_permanent=True,
    difficulty=10,
)[0]

philosophers_stone = Relic.objects.get_or_create(
    name="Philosopher's Stone (Crucible)",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of the Forge",
    power="Convert metals/stones to other materials; 6 dice pool; affects cubic yards equal to successes",
    material="Transmutation stone",
    dice_pool=6,
    difficulty=8,
)[0]

syir = Relic.objects.get_or_create(
    name="Syir (Black Ur-Metal)",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of the Forge",
    power="Spiritually pure metal with awakened essence; counts as Superb material; using it botches on 1-2",
    material="Black ur-metal",
    is_permanent=True,
    difficulty=9,
)[0]

warriors_of_broken_ground = Relic.objects.get_or_create(
    name="Warriors of the Broken Ground",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of the Earth",
    power="Stone automatons rising from earth; activated metal cube creates warriors based on Faith spent",
    material="Metal cube",
    dice_pool=8,
    difficulty=7,
)[0]

tesseract_generator = Relic.objects.get_or_create(
    name="Tesseract Generator",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of Paths",
    power="Warps space causing movement difficulty; 6 dice pool; affects radius = Faith yards",
    material="Complex mechanism",
    dice_pool=6,
    difficulty=8,
    complexity=9,
)[0]

stone_scripture = Relic.objects.get_or_create(
    name="Stone Scripture (Stonespeech)",
    house=malefactors,
    relic_type="house_specific",
    lore_used="Lore of the Forge",
    power="Annunaki secret language encoded in crystals; only Malefactors can create or read",
    material="Encoded crystals",
    is_permanent=True,
    difficulty=7,
)[0]

# Generic Enhanced Relics (examples)

simple_tool = Relic.objects.get_or_create(
    name="Enhanced Simple Tool",
    relic_type="enhanced",
    complexity=1,
    power="Simple tool enhanced with demonic power",
    difficulty=4,
)[0]

complex_device = Relic.objects.get_or_create(
    name="Enhanced Complex Device",
    relic_type="enhanced",
    complexity=5,
    power="Complex device with multiple moving parts enhanced with demonic power",
    difficulty=7,
)[0]

# Generic Enchanted Relics (examples)

enchanted_weapon = Relic.objects.get_or_create(
    name="Enchanted Weapon",
    relic_type="enchanted",
    lore_used="Lore of the Forge",
    power="Weapon containing specific lore effect",
    material="Steel",
    is_permanent=True,
    difficulty=7,
)[0]

enchanted_armor = Relic.objects.get_or_create(
    name="Enchanted Armor",
    relic_type="enchanted",
    lore_used="Lore of the Earth",
    power="Armor with protective lore effect",
    material="Iron",
    is_permanent=True,
    difficulty=8,
)[0]

# Enhanced Items (Demon Players Guide, p. 167-168)

puissant_blade = Relic.objects.get_or_create(
    name="Puissant Blade",
    relic_type="enhanced",
    power="19th-century dueling sword enhanced by demonic power. Difficulty to attack is just 4, inflicts Strength +4 lethal damage. Successes increase base damage or reduce difficulty of attack/parry rolls.",
    material="Steel sword",
    difficulty=5,
)[0]
puissant_blade.add_source("Demon Players Guide", 167)

consecrated_armor = Relic.objects.get_or_create(
    name="Consecrated Armor",
    relic_type="enhanced",
    power="Fine chain shirt, impossibly light and thin enough to wear under clothing. Provides Armor rating of 6 with no penalty to Dexterity-related rolls. Successes increase soak bonus or decrease mobility penalty.",
    material="Chainmail",
    difficulty=5,
)[0]
consecrated_armor.add_source("Demon Players Guide", 167)

lenses_of_clear_sight = Relic.objects.get_or_create(
    name="Lenses of Clear Sight",
    relic_type="enhanced",
    power="Black steel binoculars more powerful than the finest Swiss optics. Reduces difficulty of Alertness rolls by two, magnifies distant sights 15 times closer, peers through shadows and smoke. Successes reduce Alertness difficulty or increase magnification/amplification.",
    material="Black steel binoculars",
    difficulty=7,
)[0]
lenses_of_clear_sight.add_source("Demon Players Guide", 167)

uniform_of_authority = Relic.objects.get_or_create(
    name="Uniform of Authority",
    relic_type="enhanced",
    power="Decorated US Navy captain's uniform with medals. Sailors snap to attention and obey almost any command; even civilians become more likely to follow orders. Difficulty of all Leadership rolls decreases by three. Successes reduce Leadership difficulty.",
    material="Naval uniform with medals",
    difficulty=5,
)[0]
uniform_of_authority.add_source("Demon Players Guide", 167)

precision_tools = Relic.objects.get_or_create(
    name="Precision Tools",
    relic_type="enhanced",
    power="Set of spanners, wrenches, pliers and tools in reinforced steel toolbox with combination lock. Even an amateur can repair engines or reverse plumbing in moments. All appropriate Technology actions have difficulty reduced by three. Successes reduce Crafts or Technology difficulty.",
    material="Tool set in steel toolbox",
    difficulty=5,
)[0]
precision_tools.add_source("Demon Players Guide", 168)

hellfire_explosives = Relic.objects.get_or_create(
    name="Hellfire Explosives",
    relic_type="enhanced",
    power="Metal briefcase containing bomb that explodes into fire and shrapnel. Wires seem to change color and connections. Inflicts nine dice of lethal damage within 10-yard radius; all rolls to defuse suffer +2 difficulty penalty. Successes increase damage pool, blast radius, or difficulty to defuse.",
    material="Metal briefcase with bomb",
    difficulty=7,
)[0]
hellfire_explosives.add_source("Demon Players Guide", 168)

music_of_the_spheres = Relic.objects.get_or_create(
    name="Music of the Spheres",
    relic_type="enhanced",
    power="Classic Fender electric guitar painted with flames, skulls, barbed wire and demons. Produces music so beautiful it could make angels weep. All Performance rolls enjoy -3 difficulty bonus. Successes reduce Performance difficulty. Difficulty 5 for simple instruments, 7 for mechanical, 9 for electronic.",
    material="Electric guitar",
    difficulty=7,
)[0]
music_of_the_spheres.add_source("Demon Players Guide", 168)

ironclad_security = Relic.objects.get_or_create(
    name="Ironclad Security",
    relic_type="enhanced",
    power="Security system with cameras, motion-sensors, heat detectors enhanced by demonic skill. Cameras seem to know where to look, alarms ring despite every trick. Difficulty of all Stealth and Security rolls to bypass increases by two. Difficulty 9 for single system, 10 for complete network.",
    material="Security system network",
    difficulty=10,
)[0]
ironclad_security.add_source("Demon Players Guide", 168)

stealth_suit = Relic.objects.get_or_create(
    name="Stealth Suit",
    relic_type="enhanced",
    power="Traditional ninja obi of slightly padded black cloth with hood. Wearer melts into shadows to become nearly invisible, passing by sentries like a ghost. Reduces difficulty of Stealth rolls by three and provides Armor rating of 2. Successes decrease Stealth difficulty or increase Armor rating.",
    material="Black padded cloth suit",
    difficulty=5,
)[0]
stealth_suit.add_source("Demon Players Guide", 168)

# Enchanted Items (Demon Players Guide, p. 168-173)

warlocks_abacus = Relic.objects.get_or_create(
    name="The Warlock's Abacus",
    relic_type="enchanted",
    lore_used="Lore of Patterns",
    power="Simple abacus attuned to vibrations of Hell. Can calculate whether a summoning ritual will occur in user's city in the next few days. Skilled user can determine where and when the ritual will occur.",
    material="Hand-carved abacus",
    difficulty=7,
)[0]
warlocks_abacus.add_source("Demon Players Guide", 168)

compass_rose = Relic.objects.get_or_create(
    name="Compass Rose",
    relic_type="enchanted",
    lore_used="Lore of Awakening",
    power="Hand-carved compass in fine glass and wood casing. Whisper a name into the glass to fog it; compass points to that person if within a few miles. Lock lasts until end of scene or target is reached.",
    material="Glass and wood casing with compass",
    difficulty=7,
)[0]
compass_rose.add_source("Demon Players Guide", 168)

vermin_flute = Relic.objects.get_or_create(
    name="Vermin Flute",
    relic_type="enchanted",
    lore_used="Lore of the Beast",
    power="Plain wooden pipes that play tune enticing to rats and rodents. Any rat within several miles is compelled to scurry toward the source. Rats swarm within one yard of player and follow if he moves while playing. Player cannot roll more dice than Charisma + Performance pool.",
    material="Wooden pipes",
    difficulty=7,
)[0]
vermin_flute.add_source("Demon Players Guide", 169)

empathy_glasses = Relic.objects.get_or_create(
    name="Empathy Glasses",
    relic_type="enchanted",
    lore_used="Lore of Longing",
    power="Normal-looking glasses that allow wearer to read emotions of anyone she looks at. People appear with aura of various colors based on emotions: red = anger, purple = sexual desire, blue = contentment. User can adjust behavior accordingly.",
    material="Glasses",
    difficulty=7,
)[0]
empathy_glasses.add_source("Demon Players Guide", 169)

book_of_the_dead = Relic.objects.get_or_create(
    name="Book of the Dead",
    relic_type="enchanted",
    lore_used="Lore of Death",
    power="Heavy leather-bound antique book with blank pages. Write name of deceased mortal or demon on left-hand page; writing appears on next page detailing events leading to death. Writing vanishes when closed. Higher difficulty if not using True or Celestial Name.",
    material="Leather-bound book",
    difficulty=7,
)[0]
book_of_the_dead.add_source("Demon Players Guide", 169)

flare_gun = Relic.objects.get_or_create(
    name="Flare Gun",
    relic_type="enchanted",
    lore_used="Lore of Light",
    power="Real firearm (usually large pistol) that can fire bullets of light. Converts one real bullet into packet of dense energy that blinds any target hit. Each activation requires expenditure of one mundane bullet.",
    material="Large pistol",
    difficulty=7,
)[0]
flare_gun.add_source("Demon Players Guide", 169)

eyepatch_of_angra_mainyu = Relic.objects.get_or_create(
    name="Eyepatch of Angra Mainyu",
    relic_type="enchanted",
    lore_used="Lore of Paths",
    power="Leather eye-patch trimmed with steel. Allows user to escape any prison or bypass any obstacle by finding and following a pathway visible only through the patch. User appears to walk through walls or barriers. Path lasts only a turn and cannot be made permanent.",
    material="Leather eye-patch with steel trim",
    difficulty=7,
)[0]
eyepatch_of_angra_mainyu.add_source("Demon Players Guide", 169)

titans_net = Relic.objects.get_or_create(
    name="The Titan's Net",
    relic_type="enchanted",
    lore_used="Lore of the Earth",
    power="Roughly woven net of thin metal wires with small stone in each knot. If user entangles enemy (melee or thrown), ground becomes like water and victim is dragged into earth. Net melds with soil; victim must dig herself out. User must hit target with net (Dexterity + Athletics) before effect takes place.",
    material="Metal wire net with stones",
    difficulty=7,
)[0]
titans_net.add_source("Demon Players Guide", 169)

eye_of_the_seer = Relic.objects.get_or_create(
    name="Eye of the Seer",
    relic_type="enchanted",
    lore_used="Lore of the Firmament",
    power="Beautiful crystal orb the size of a child's head, cut and polished to fine brilliance. Demon who stares into depths sees world around chosen subject. User must possess personal item belonging to target or breathe subject's name onto crystal. Vision is always silent regardless of successes.",
    material="Perfect crystal orb",
    difficulty=7,
)[0]
eye_of_the_seer.add_source("Demon Players Guide", 169)

banner_of_inspiration = Relic.objects.get_or_create(
    name="Banner of Inspiration",
    relic_type="enchanted",
    lore_used="Lore of Radiance",
    power="Flag or banner bearing symbol that inspires followers. When raised or waved, allies who see it are filled with courage and hope, surging forward to battle foes. In modern world, used to inspire rooms of brokers or programmers.",
    material="Flag or banner",
    difficulty=7,
)[0]
banner_of_inspiration.add_source("Demon Players Guide", 169)

porcelain_mask = Relic.objects.get_or_create(
    name="Porcelain Mask",
    relic_type="enchanted",
    lore_used="Lore of Transfiguration",
    power="Blank white porcelain mask that fits neatly over any face. Allows user to alter facial features (neck up only). User must sketch desired features onto mask with pen/paintbrush, then press to face. Mask merges and alters features. Markings must be erased and redone for reuse.",
    material="Porcelain mask",
    difficulty=7,
)[0]
porcelain_mask.add_source("Demon Players Guide", 170)

mirror_of_souls = Relic.objects.get_or_create(
    name="Mirror of Souls",
    relic_type="enchanted",
    lore_used="Lore of the Realms",
    power="Antique mirror that appears normal until user forces will upon it. Reflection changes to image of bleak, lifeless spirit realm. User can step into reflection to enter land of death. Must work will on shadow mirror in realm to return. Mirror reverts to normal behind user.",
    material="Antique mirror",
    difficulty=7,
)[0]
mirror_of_souls.add_source("Demon Players Guide", 170)

dagger_of_venom = Relic.objects.get_or_create(
    name="Dagger of Venom",
    relic_type="enchanted",
    lore_used="Lore of Awakening",
    power="Steel hunting knife with essence of venom instilled into blade. Poisons and contaminates anything it cuts with incredibly virulent poison unknown to medical science. No evidence of poison left in wound; poison is in the metal, not on it. Doctor must be lucky to recognize poisoning.",
    material="Steel dagger",
    difficulty=7,
)[0]
dagger_of_venom.add_source("Demon Players Guide", 170)

cats_eye_collars = Relic.objects.get_or_create(
    name="Cat's Eye Collars",
    relic_type="enchanted",
    lore_used="Lore of the Beast",
    power="Two leather collars studded with clear crystals. User binds one around own neck, other around animal. While both wear collars, demon can project senses into animal (body insensate). Can return to body anytime. If animal is injured, user is yanked back and disoriented (Willpower roll difficulty 7 or +1 difficulty to all rolls for scene).",
    material="Leather collars with crystals",
    difficulty=7,
)[0]
cats_eye_collars.add_source("Demon Players Guide", 170)

flaming_sword = Relic.objects.get_or_create(
    name="Flaming Sword",
    relic_type="enchanted",
    lore_used="Lore of Flame",
    power="Sword encased in flame, poor shadow of weapon Michael raised against Lucifer. Flames surround blade at wielder's command, won't harm user but rake target with horrific burns. Apply effect pool as separate source of damage to anyone hit by sword.",
    material="Sword",
    difficulty=7,
)[0]
flaming_sword.add_source("Demon Players Guide", 170)

bracer_of_black_defense = Relic.objects.get_or_create(
    name="Bracer of Black Defense",
    relic_type="enchanted",
    lore_used="Lore of the Fundament",
    power="Antique bracer of blackened steel and cold iron with engravings of warfare and archery. Animates wearer's arm to block ranged attacks including bullets and arrows. Cannot block evocation attacks. Deflects .50 caliber bullets without damage. Bullets can be deflected at +1 difficulty.",
    material="Blackened steel and cold iron bracer",
    difficulty=7,
)[0]
bracer_of_black_defense.add_source("Demon Players Guide", 170)

spirit_cutting_sword = Relic.objects.get_or_create(
    name="Spirit-Cutting Sword",
    relic_type="enchanted",
    lore_used="Lore of the Spirit",
    power="Enchanted silver-and-steel sword. Lets user sense nearby spirits as hazy outline or smear of darkness. Can physically attack and wound incorporeal spirits and ghosts. Does normal lethal damage for sword type.",
    material="Silver and steel sword",
    difficulty=7,
)[0]
spirit_cutting_sword.add_source("Demon Players Guide", 170)

mourning_coat = Relic.objects.get_or_create(
    name="Mourning Coat",
    relic_type="enchanted",
    lore_used="Lore of the Realms",
    power="Elegant black coat suited for funerals. When activated, allows wearer to stand in worlds of both living and dead simultaneously. Becomes vague shadowy figure that can move through walls and solid objects. Can become more solid in one plane or other with moment of concentration.",
    material="Black coat",
    difficulty=7,
)[0]
mourning_coat.add_source("Demon Players Guide", 171)

wand_of_holy_fire = Relic.objects.get_or_create(
    name="Wand of Holy Fire",
    relic_type="enchanted",
    lore_used="Lore of the Celestials",
    power="Two-foot-long intricately carved wand of black stone and burnished copper with silver and crystal highlights. When leveled at adversary and word of power spoken, blazing white fire leaps from tip to consume target, reducing mortal and demon to ash. Potent weapon from Age of Wrath.",
    material="Black stone and burnished copper wand",
    difficulty=7,
)[0]
wand_of_holy_fire.add_source("Demon Players Guide", 171)

sprinters_shoes = Relic.objects.get_or_create(
    name="Sprinter's Shoes",
    relic_type="enchanted",
    lore_used="Lore of the Fundament",
    power="Expensive sports shoes with soles shot through with copper, steel and platinum wires. User can run at amazing speeds, even up walls for short periods. Requires great exertion; user must make Stamina roll (difficulty 7) after use or suffer level of lethal damage from muscle damage.",
    material="Sports shoes with metal wires",
    difficulty=7,
)[0]
sprinters_shoes.add_source("Demon Players Guide", 171)

brazier_of_distant_sendings = Relic.objects.get_or_create(
    name="Brazier of Distant Sendings",
    relic_type="enchanted",
    lore_used="Lore of the Firmament",
    power="Ornate copper brazier on tripod of blackened steel, fueled with hot coals and fragrant incense. Throw personal effect (hair, fingernail) onto coals; as item is consumed, user can perform evocation onto smoke. Wherever target is in world, wisps of smoke surround them conveying full evocation power.",
    material="Copper brazier on steel tripod",
    difficulty=7,
)[0]
brazier_of_distant_sendings.add_source("Demon Players Guide", 171)

slayers_scythe = Relic.objects.get_or_create(
    name="Slayer's Scythe",
    relic_type="enchanted",
    lore_used="Lore of Death",
    power="Scythe with thin, almost translucent black metal blade on length of blackened wood worn by aeons of use. With touch of blade, can sever mortal's soul from body. Lucky victim may resist, being suffused with paralyzing cold pain with no wound shown.",
    material="Black metal blade on blackened wood",
    difficulty=7,
)[0]
slayers_scythe.add_source("Demon Players Guide", 172)

token_of_appreciation = Relic.objects.get_or_create(
    name="Token of Appreciation",
    relic_type="enchanted",
    lore_used="Lore of Radiance",
    power="Made from gold and precious metals (ornate medal to elegant tie-pin). User inscribes back with bearer's name and own name. While bearer wears token, all mortals treat him with great respect and admiration, welcoming him into homes and lives without hesitation.",
    material="Gold and precious metals",
    difficulty=7,
)[0]
token_of_appreciation.add_source("Demon Players Guide", 172)

drums_of_cataclysm = Relic.objects.get_or_create(
    name="Drums of Cataclysm",
    relic_type="enchanted",
    lore_used="Lore of the Earth",
    power="Large kettle drum of blessed copper and volcanic stone. Pound out cacophony to provoke earthquake. Earth tremors continue as long as user plays, reverberating for few seconds before dying. Terrible strain to play; user must suffer level of bashing damage (cannot be soaked) before activating.",
    material="Blessed copper and volcanic stone drum",
    difficulty=7,
)[0]
drums_of_cataclysm.add_source("Demon Players Guide", 172)

soul_trap = Relic.objects.get_or_create(
    name="Soul Trap",
    relic_type="enchanted",
    lore_used="Lore of the Forge",
    power="Crystal and gold amulet (spirit cage). When activated in presence of spirit (ghost or incorporeal demon), trap sucks spirit in. Once inside, demonic spirits find it nearly impossible to evoke their lore, preventing them from acting against captor. Also uses Pillar of Faith (high-Torment).",
    material="Crystal and gold amulet",
    difficulty=7,
)[0]
soul_trap.add_source("Demon Players Guide", 172)

black_shroud = Relic.objects.get_or_create(
    name="The Black Shroud",
    relic_type="enchanted",
    lore_used="Lore of Death",
    power="Simple ragged shroud woven from finest materials, impossibly old. When placed over freshly deceased body (less than one day), reanimates corpse as mindless zombie loyal to user. Stories exist of White Shroud that truly returns dead to life regardless of time deceased.",
    material="Ancient woven shroud",
    difficulty=7,
)[0]
black_shroud.add_source("Demon Players Guide", 172)

arrow_of_chronos = Relic.objects.get_or_create(
    name="Arrow of Chronos",
    relic_type="enchanted",
    lore_used="Lore of Patterns",
    power="Rare relic from Age of Wrath, made of finest woods and metals. Target struck is propelled forward in time (usually few moments, enough to negate as threat). When enemy pops back, opponent may be gone or backed by reinforcements. Target must be hit by arrow but need not take damage.",
    material="Fine woods and metals arrow",
    difficulty=7,
)[0]
arrow_of_chronos.add_source("Demon Players Guide", 172)

pickpockets_ring = Relic.objects.get_or_create(
    name="Pickpocket's Ring",
    relic_type="enchanted",
    lore_used="Lore of Portals",
    power="White gold and black obsidian ring. Perfect tool for thieves fearing capture. If user holds item in hand bearing ring (small enough for one hand), can make it vanish completely into pocket of twisted space. Item reappears only when willed, popping back into hand.",
    material="White gold and black obsidian ring",
    difficulty=7,
)[0]
pickpockets_ring.add_source("Demon Players Guide", 172)

staff_of_the_skys_fury = Relic.objects.get_or_create(
    name="Staff of the Sky's Fury",
    relic_type="enchanted",
    lore_used="Lore of Storms",
    power="Six-foot-long staff carved from lightning-struck tree, finished with copper, platinum and crystals. Striking and obvious. When power invoked, glaring stream of lightning bolts courses from relic and strikes anyone targeted. Powerful enough to set wood alight, melt stone or metal, reduce humans to greasy smoke.",
    material="Lightning-struck wood with copper, platinum, crystals",
    difficulty=7,
)[0]
staff_of_the_skys_fury.add_source("Demon Players Guide", 172)

# Forgotten Wonders - Ancient Relics (Demon Players Guide, p. 173-175)

soultaker = Relic.objects.get_or_create(
    name="Soultaker",
    relic_type="ancient",
    lore_used="Multiple Lores",
    power="Massive broadsword of siyr (first metal forged after Fall). Blade is chipped and cracked, pommel rusted. Contains willing soul of demon (name forgotten) who uses power on anyone touched by blade to drain energy and imprison souls. If sword kills victim, soul is pulled into blade to be tortured and devoured. Contains multiple demon souls merged into single insane entity called Legion. When cooperative, difficulty to hit/parry is 4, damage is Strength +6 lethal (difficulty 4). When hostile, difficulty is 9. Legion starts with no Faith but gains temporary Faith equal to half victim's Faith potential when killing mortals. Can spend 10 temporary Faith for 1 permanent Faith (max 10). When wounding demons, roll Legion's permanent Faith vs demon's Faith; successes steal temporary Faith (half to Legion, half to wielder). If demon is slain and Legion wins Faith roll, demon's soul is absorbed forever.",
    material="Siyr (black ur-metal)",
    is_permanent=True,
    difficulty=10,
)[0]
soultaker.add_source("Demon Players Guide", 173)

black_throne_of_genhinnom = Relic.objects.get_or_create(
    name="The Black Throne of Genhinnom",
    relic_type="ancient",
    lore_used="Lore of the Firmament",
    power="Created by Lucifer, 20-foot-tall chair of black obsidian and siyr that sat at center of Black Cathedral in rebel city Genhinnom. Incredibly uncomfortable but powerful. Requires 50 points of temporary Faith to activate (all at once or over time). Once activated, resonates with demon's spirit. If mortal looks upon demon sitting on throne, Willpower roll (difficulty 9) or becomes willing, almost fanatical follower who will obey any order, even suicidal ones - but only while demon sits on throne. No limit to number of mortals enthralled. Occupant can perform all Lore of Firmament evocations on followers using own dice pools with no Torment risk (cannot invoke high-Torment versions). Can also use Exalt (Lore of Radiance) on followers at will. Mortals serving throne cannot become thralls or agree to pacts; existing pacts instantly break. User suffers +1 difficulty to all actions when not seated after 10 Faith drained. Throne is massive and weighs many tons.",
    material="Black obsidian and siyr",
    is_permanent=True,
    difficulty=10,
)[0]
black_throne_of_genhinnom.add_source("Demon Players Guide", 174)

soulforge = Relic.objects.get_or_create(
    name="The Soulforge",
    relic_type="ancient",
    lore_used="Lore of Death",
    power="Crafted by Schatenkoji the Ghostsmith. Large, ornately angular cage of copper and metals engraved with untranslatable runes and sigils. Hooks and spikes line inner cage, four wide coiled flanges radiate from top. Demon in mortal host must enter cage, be locked in, then killed (impaled on spikes or shot). As host's blood seeps away, apocalyptic form emerges and is seized by relic. Cage rips demon's energy apart (soul-devouring attempt with 15 dice). If relic wins, it converts energy to Faith and activates second power: wave of invisible black energy washes forth covering radius of one mile per Faith point absorbed. Every mortal in radius is affected by Extinguish Life (Lore of Death) using sacrificed demon's Strength + Awareness pool. Only mortals affected; demons untouched. Any mortal killed outright has soul appear in Soulforge impaled on spike (can hold hundreds or thousands). User can remove soul with long hook to bind into demonic relic. Each day souls are imprisoned costs 1 Faith from sacrificed demon's energy. If Faith runs out, all souls are released. Each activation inflicts 1 temporary Torment on user.",
    material="Copper and metal cage with runes",
    is_permanent=True,
    difficulty=10,
)[0]
soulforge.add_source("Demon Players Guide", 175)
