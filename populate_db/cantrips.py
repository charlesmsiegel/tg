from characters.models.changeling import Cantrip

# AUTUMN ART
Cantrip.objects.get_or_create(
    name="Creeping Shadows",
    art="autumn",
    level=1,
    primary_realm="fae",
    glamour_cost="Chimerical/Wyrd",
    difficulty=8,
    duration="Scene",
    range="Nearby",
    type_of_effect="chimerical",
    effect="Command shadows to bend to caster's whim. Subtle uses lower Intimidation difficulty by 1 per success. Overt uses grant -1 to Stealth rolls by 1 per success (max 9). Can swallow subjects in shadows for concealment.",
    bunk_examples=["Use cloaks", "Dance with shadows", "Stand in darkness"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 340)

Cantrip.objects.get_or_create(
    name="Autumn Eyes",
    art="autumn",
    level=2,
    primary_realm="fae",
    glamour_cost="1 (Chimerical)",
    difficulty=8,
    duration="Scene",
    range="Sight",
    type_of_effect="chimerical",
    effect="Eyes glow with Samhain light revealing decay, illness, weakness, doom. Spot weak points in objects (+1 damage per success). Diagnose health conditions. Recognize curses with 3+ successes. Identify impending doom.",
    bunk_examples=["Paint eyes with special cosmetics", "Stare intensely", "Close one eye repeatedly"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 340)

Cantrip.objects.get_or_create(
    name="The Poisoned Apple",
    art="autumn",
    level=3,
    primary_realm="prop",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Until effect triggers",
    range="Arm's reach",
    type_of_effect="wyrd",
    effect="Poison target with deadly infusion. On objects, becomes poisonous to next user. Damage equals successes rolled. Mortals resist as Category 5 poison, supernatural beings as Category 3.",
    bunk_examples=["Bake poisoned food", "Speak hexes", "Wear death shrouds"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 341)

Cantrip.objects.get_or_create(
    name="The Withering",
    art="autumn",
    level=4,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Based on successes allocated",
    range="Sight",
    type_of_effect="wyrd",
    effect="Steal vitality, age target by one decade per success dedicated. 2 successes = -1 to physical pools. Duration based on remaining successes. Multiple castings require more successes than existing curse.",
    bunk_examples=["Break objects with age", "Perform aging rituals", "Consume aged items"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 341)

Cantrip.objects.get_or_create(
    name="Shivers",
    art="autumn",
    level=5,
    primary_realm="actor",
    glamour_cost="1 (Chimerical)",
    difficulty=8,
    duration="Days equal to successes x permanent Glamour",
    range="Touch/Near",
    type_of_effect="chimerical",
    effect="Draw out dreams of death/darkness, curse target. Mark target as beacon for ghosts. -1 penalties to concentration or object-use. Prevent Willpower recovery from sleep.",
    bunk_examples=["Collect death symbols", "Visit graves", "Burn belongings"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 341)

# CHICANERY ART
Cantrip.objects.get_or_create(
    name="Trick of the Light",
    art="chicanery",
    level=1,
    primary_realm="actor",
    glamour_cost="Chimerical (0 if within difficulty)",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="chimerical",
    effect="Subtle perception manipulation. Misinterpret targets. Hold up to scrutiny by Perception + Occult (difficulty 8). Creates minor disguises, not elaborate illusions.",
    bunk_examples=["Wear disguises", "Blend into crowds", "Confuse observers"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 343)

Cantrip.objects.get_or_create(
    name="Veiled Eyes",
    art="chicanery",
    level=2,
    primary_realm="fae",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="chimerical",
    effect="Target becomes unnoticed but not invisible. Observers overlook target or item. Counteracts by Perception + Kenning (difficulty 8). Can cloak self or group.",
    bunk_examples=["Wear neutral colors", "Avoid attention", "Move slowly"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 343)

Cantrip.objects.get_or_create(
    name="Dream Logic",
    art="chicanery",
    level=3,
    primary_realm="actor",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="chimerical",
    effect="Confuse targets' minds with Glamour. +3 difficulty to Mental/Social tasks. Make targets suggestible. Targets resist by Willpower (difficulty 8) or spend Willpower to resist suggestions.",
    bunk_examples=["Whisper confusing statements", "Create nonsensical scenarios", "Sing strange songs"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 344)

Cantrip.objects.get_or_create(
    name="Veiled Mind",
    art="chicanery",
    level=4,
    primary_realm="actor",
    glamour_cost="Chimerical (0) or Wyrd (1)",
    difficulty=8,
    duration="1-4 successes vary in duration",
    range="Sight",
    type_of_effect="both",
    effect="Wipe subject from everyone's memory. Can create exceptions with additional Realms. Changeling can unravel effects anytime. Others resist if motivated.",
    bunk_examples=["Make subject leave area", "Describe amnesia rituals", "Destroy memory items"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 344)

Cantrip.objects.get_or_create(
    name="Lost in the Mists",
    art="chicanery",
    level=5,
    primary_realm="actor",
    glamour_cost="Chimerical (0) or Wyrd (1)",
    difficulty=9,
    duration="1-5 successes vary in duration",
    range="Sight",
    type_of_effect="both",
    effect="Strip identity and implant delusions. Target resists via Perception + Kenning (difficulty 9). Can then resist each turn with Willpower (difficulty 8) or spend Willpower for scene.",
    bunk_examples=["Describe desired delusion clearly", "Create symbolic items", "Perform identity-altering rituals"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 344)

# DRAGON'S IRE ART
Cantrip.objects.get_or_create(
    name="Burning Thew",
    art="dragons_ire",
    level=1,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Successes in rounds",
    range="Sight",
    type_of_effect="chimerical",
    effect="Infuse target with burning might. Living creatures: add Strength per success. Objects: add damage dice per success. Gold aura surrounds target. Split successes between efficacy and duration.",
    bunk_examples=["Flex dramatically", "Ignite small flame", "Douse self with accelerant", "Roar battle cry"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 359)

Cantrip.objects.get_or_create(
    name="Confounding Coils",
    art="dragons_ire",
    level=2,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="1 round per success",
    range="Sight",
    type_of_effect="chimerical",
    effect="Grant target grace of coiling serpent. Difficult to hit: +2 difficulty to attacks against subject (max 9). Object becomes slippery/shifting, deflecting strikes. Ineffective against cold iron.",
    bunk_examples=["Dance serpentine movements", "Wrap in ropes", "Create circular patterns"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 360)

Cantrip.objects.get_or_create(
    name="Dragonscales",
    art="dragons_ire",
    level=3,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="1 round per success",
    range="Sight",
    type_of_effect="chimerical",
    effect="Infuse subject with mystical dragon hide toughness. All damage against subject: +2 difficulty (max 9). Shimmer with heat haze. Ineffective against cold iron attacks.",
    bunk_examples=["Brush with scales", "Harden skin", "Coat with metallic dust", "Invoke dragon protection"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 360)

Cantrip.objects.get_or_create(
    name="Holly-Strike",
    art="dragons_ire",
    level=4,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Immediate",
    range="(Willpower x 10) yards/meters",
    type_of_effect="wyrd",
    effect="Blast of eldritch power destroying target. Activation roll = attack roll. Inflicts lethal damage = Willpower + Glamour + extra successes.",
    bunk_examples=["Channel specific element", "Invoke legendary warrior", "Dramatic attack stance"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 360)

Cantrip.objects.get_or_create(
    name="Tripping the Ire",
    art="dragons_ire",
    level=5,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Scene (refreshes each round, loses 1 die)",
    range="Sight",
    type_of_effect="chimerical",
    effect="Grant subject martial wisdom of legendary warriors. Pool of extra dice = successes. Each round divide pool among combat pools.",
    bunk_examples=["Invoke legendary knights", "Glow with ancient power", "Call ancestral warriors"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 361)

# LEGERDEMAIN ART
Cantrip.objects.get_or_create(
    name="Ensnare",
    art="legerdemain",
    level=1,
    primary_realm="prop",
    glamour_cost="Chimerical (0) or Wyrd (1)",
    difficulty=8,
    duration="Successes in turns",
    range="Sight",
    type_of_effect="both",
    effect="Slow/immobilize target. Furniture jumps into way, ground raises, Glamour tendrils trip/weigh target. +3 difficulty to physical actions. Half normal movement speed.",
    bunk_examples=["Create obstacles", "Tangle ropes", "Cause ground displacement"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 365)

Cantrip.objects.get_or_create(
    name="Mooch",
    art="legerdemain",
    level=2,
    primary_realm="prop",
    glamour_cost="Chimerical (0) or Wyrd (1)",
    difficulty=8,
    duration="Instant",
    range="Sight",
    type_of_effect="both",
    effect="Instantly transfer one inanimate object from target to caster. Item appears anywhere on caster's person. Target rolls Perception + Alertness (difficulty 8) to notice.",
    bunk_examples=["Sleight of hand gestures", "Distract target", "Casual theft gestures"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 365)

Cantrip.objects.get_or_create(
    name="Effigy",
    art="legerdemain",
    level=3,
    primary_realm="prop",
    glamour_cost="Chimerical (0) or Wyrd (1)",
    difficulty=8,
    duration="Based on successes",
    range="Line of sight",
    type_of_effect="both",
    effect="Create replica good enough to fool observer briefly. Sentient effigies perform single repetitive action. Objects appear exactly. Exist in physical world. Effigy food tastes bad, no nutrition.",
    bunk_examples=["Sculpt Glamour replica", "Describe copied item", "Perform imitation actions"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 366)

Cantrip.objects.get_or_create(
    name="Gimmix",
    art="legerdemain",
    level=4,
    primary_realm="prop",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="1 turn or successes in turns",
    range="Sight",
    type_of_effect="wyrd",
    effect="Move/control objects with precision/force without touching. Art + Realm = Strength (sudden force) or Dexterity (precision). Attack roll if used offensively.",
    bunk_examples=["Elaborate gestures", "Maintain focus", "Dramatic object manipulation"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 366)

Cantrip.objects.get_or_create(
    name="Smoke and Mirrors",
    art="legerdemain",
    level=5,
    primary_realm="prop",
    glamour_cost="1 (Wyrd) per roll + extended action cost",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="both",
    effect="Create long-lasting, convincing illusions. No mass in mundane world. Requires all relevant Realms. Look/sound/smell real. Extended action accumulates successes.",
    bunk_examples=["Create elaborate mise-en-scene", "Gather props", "Invoke audience perception"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 366)

# METAMORPHOSIS ART
Cantrip.objects.get_or_create(
    name="Sparrows and Nightingales",
    art="metamorphosis",
    level=1,
    primary_realm="fae",
    glamour_cost="Chimerical (0) or Wyrd (1)",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="both",
    effect="Change one fundamental feature to plausible alternative (gender, hair color, height, species equivalent). Can attach condition to duration end. Only one discrete feature. Must be reasonably possible.",
    bunk_examples=["Describe transformation visually", "Invoke animal essence", "Perform ritual alteration"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 368)

Cantrip.objects.get_or_create(
    name="Worms and Giants",
    art="metamorphosis",
    level=2,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="1 scene",
    range="Sight",
    type_of_effect="wyrd",
    effect="Shrink or enlarge subject. Successes determine extent: 1 = 3/4 or 1.5x; 2 = 1/2 or 2x; 3 = 1/4 or 2.5x; 4 = 1/8 or 3x; 5 = 1/16 or 3.5x. Repeated castings stack.",
    bunk_examples=["Perform size-changing gestures", "Describe growth/shrinkage", "Invoke age/youth"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 369)

Cantrip.objects.get_or_create(
    name="Thousandskins",
    art="metamorphosis",
    level=3,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Varies, split with severity",
    range="Sight",
    type_of_effect="wyrd",
    effect="Transform person/object into animal. Retain mind/instincts but gain physical traits. Objects gain typical animal mind. Transformed retain speech (chimerical only). Severity determines animal restrictions.",
    bunk_examples=["Invoke animal spirit", "Perform animal movements", "Describe transformation"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 369)

Cantrip.objects.get_or_create(
    name="Beastskin",
    art="metamorphosis",
    level=4,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Successes divide between features/duration",
    range="Sight",
    type_of_effect="wyrd",
    effect="Partial transformations. Grant animal features (claws, fur, wings, poison fangs). Each success = 1 feature or duration extension. Can set condition to end early.",
    bunk_examples=["Describe specific animal features", "Invoke enhancement magic", "Ritualize partial transformation"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 370)

Cantrip.objects.get_or_create(
    name="Chimeric Exultation",
    art="metamorphosis",
    level=5,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Glamour in minutes (can reset by spending 1 Glamour)",
    range="Sight",
    type_of_effect="wyrd",
    effect="Transform into creature of legend combining traits. Each success = 1 fantastic ability (flight, strength, toughness, fire breath, etc.). Duration always Glamour minutes but can reset with Glamour spending.",
    bunk_examples=["Invoke legendary beasts", "Describe multiple powers", "Dramatic transformation stance"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 370)

# PRIMAL ART
Cantrip.objects.get_or_create(
    name="Oakenshield",
    art="primal",
    level=3,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Until destroyed or scene end",
    range="Sight",
    type_of_effect="wyrd",
    effect="Fortify with protective elemental sheath. Each success = +1 temporary Bruised health level. Damage marked first. Damaged levels vanish. Can't stack with new castings (overwrites).",
    bunk_examples=["Harden skin", "Cover with natural material", "Invoke protection"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 373)

Cantrip.objects.get_or_create(
    name="Elder-Form",
    art="primal",
    level=4,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Based on successes and Glamour",
    range="Sight",
    type_of_effect="wyrd",
    effect="Imbue subject with elemental essence. AIR: invisible, float. EARTH: stone-form. WATER: +1 Dex, breathe underwater. WOOD: rooted in place. FIRE: flame-form, +1 aggravated damage.",
    bunk_examples=["Invoke element spirit", "Describe elemental form", "Channel natural force"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 373)

Cantrip.objects.get_or_create(
    name="Dance of the Five Kings",
    art="primal",
    level=5,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Scene",
    range="Sight",
    type_of_effect="wyrd",
    effect="Master five elements. Command existing elemental manifestations. Realm determines actions: Actor/Fae = elements attack or restrain. Prop/Nature = reshape elements into forms.",
    bunk_examples=["Command elements dramatically", "Invoke elemental lords", "Conduct with gestures"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 374)

# PYRETICS ART
Cantrip.objects.get_or_create(
    name="Kindle",
    art="pyretics",
    level=1,
    primary_realm="prop",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Successes in turns",
    range="Sight",
    type_of_effect="wyrd",
    effect="Heat target causing discomfort not injury. Cook food, start fire, make person sweat/appear feverish, heat gun to burn touch. Inanimate/non-sentient: Storyteller arbitrates.",
    bunk_examples=["Light flame", "Invoke heat", "Heat target dramatically"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 375)

Cantrip.objects.get_or_create(
    name="Illuminate",
    art="pyretics",
    level=2,
    primary_realm="prop",
    glamour_cost="1 (Wyrd) or Chimerical (0)",
    difficulty=8,
    duration="Scene (can end early)",
    range="Based on Realm use",
    type_of_effect="both",
    effect="Create dispelling light. Reveals hidden/obscured things, supernatural illusions, physical disguises, lies. Illusions with lower power than successes revealed.",
    bunk_examples=["Create illumination", "Invoke revelation magic", "Burn away shadows"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 376)

Cantrip.objects.get_or_create(
    name="Purify",
    art="pyretics",
    level=3,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Immediate",
    range="Touch/sight",
    type_of_effect="wyrd",
    effect="Burn away contaminants with chimerical fire (doesn't damage target). Purify water/food, destroy infection/poison, temporarily cure disease. With Fae Realm, burn away curses/cantrip effects.",
    bunk_examples=["Apply cleansing flame", "Invoke purification ritual", "Destroy contamination"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 376)

Cantrip.objects.get_or_create(
    name="Engulf",
    art="pyretics",
    level=4,
    primary_realm="prop",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Successes in turns",
    range="Sight",
    type_of_effect="wyrd",
    effect="Make target combust. Choose: target burns or remains protected with wreath of flame. Once catches other nearby, burns as normal fire. Protected targets: others touching flame suffer 1 aggravated/turn.",
    bunk_examples=["Ignite dramatically", "Invoke conflagration", "Protect with flame"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 376)

Cantrip.objects.get_or_create(
    name="Phoenix Song",
    art="pyretics",
    level=5,
    primary_realm="actor",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Based on successes before resurrection",
    range="Sight",
    type_of_effect="wyrd",
    effect="Grant blessing of rebirth through destruction. If recipient killed/destroyed during scene, bursts to flame and rises renewed. Restores all Health/Willpower/Glamour and resources.",
    bunk_examples=["Invoke phoenix rebirth", "Burn dramatically", "Promise renewal"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 377)

# SKYCRAFT ART
Cantrip.objects.get_or_create(
    name="Howling Gale",
    art="skycraft",
    level=1,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Glamour in minutes or 5 min per success",
    range="Sight",
    type_of_effect="wyrd",
    effect="Call powerful wind aiding/hindering movement. Target person: double movement per 2 successes, or half movement. Wind lasts Glamour minutes. Object target: push at Glamour mph for 5 min per success.",
    bunk_examples=["Dramatic windmaking", "Invoke gale spirit", "Create air current"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 379)

Cantrip.objects.get_or_create(
    name="Electric Gremlins",
    art="skycraft",
    level=2,
    primary_realm="prop",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="chimerical",
    effect="Summon host of gremlins harassing electronics. Fae/Actor: gremlins disrupt complex electronics target uses. Nature/Prop: curse objects making electronics nearby malfunction.",
    bunk_examples=["Invoke gremlins", "Cause electrical chaos", "Invite mischief spirits"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 379)

Cantrip.objects.get_or_create(
    name="Hurricane Speed",
    art="skycraft",
    level=3,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Glamour in rounds",
    range="Sight",
    type_of_effect="wyrd",
    effect="Infuse essence of wind granting speed/reflexes. Object: halve weight, double throw distance per success. Person: +1 Initiative per success, +1 Dexterity per 2 successes.",
    bunk_examples=["Invoke speed magic", "Invoke wind grace", "Dramatic acceleration"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 380)

Cantrip.objects.get_or_create(
    name="Storm Shroud",
    art="skycraft",
    level=4,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="1 round per success",
    range="Sight",
    type_of_effect="wyrd",
    effect="Call lightning essence into target surrounding with electrical aura. Contact = 3 dice bashing damage. Caster immune to own cantrip. Can enchant own weapons/clothing safely.",
    bunk_examples=["Invoke lightning", "Crackle electricity", "Dramatic aura manifestation"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 380)

Cantrip.objects.get_or_create(
    name="Lord of Levin",
    art="skycraft",
    level=5,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Immediate",
    range="Open sky (or from fingertips with Storm Shroud)",
    type_of_effect="wyrd",
    effect="Strike target with lightning. Normally requires open sky. With Storm Shroud active, throw lightning from fingertips. Activation roll = attack roll. 5 dice aggravated damage + 1 per extra success.",
    bunk_examples=["Invoke sky spirits", "Dramatic lightning pose", "Call down celestial power"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 381)

# SOVEREIGN ART
Cantrip.objects.get_or_create(
    name="Dictum",
    art="sovereign",
    level=1,
    primary_realm="actor",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Scene",
    range="Hearing range",
    type_of_effect="wyrd",
    effect="Issue command in caster's voice. Must be single-word or two-word command understandable by listener. Resist via Willpower (difficulty = caster's Glamour). Subject compelled to obey unless violates fundamental nature.",
    bunk_examples=["Formal command statement", "Use authoritative voice", "Dramatic gesturing"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 389)

Cantrip.objects.get_or_create(
    name="Retinue",
    art="sovereign",
    level=2,
    primary_realm="actor",
    glamour_cost="1 (Wyrd) + 1 per Scene use",
    difficulty=8,
    duration="Scene",
    range="Sight",
    type_of_effect="wyrd",
    effect="Enchant group within Scene to respond to caster's leadership. Group acts on caster's direction (within Realm's scope). Scene use requires +1 Glamour and +1 difficulty.",
    bunk_examples=["Gather group", "Issue orders", "Demonstrate authority over followers"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 390)

Cantrip.objects.get_or_create(
    name="Mastery",
    art="sovereign",
    level=3,
    primary_realm="actor",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Successes in scenes",
    range="Sight",
    type_of_effect="wyrd",
    effect="Grant temporary mastery of skill. Subject gains pool of dice = successes for skill use. Lasts successes in scenes. Subjects of Mastery contribute doubled successes to group actions under caster's direction.",
    bunk_examples=["Invoke skill transferrence", "Touch/bless target", "Grant empowerment"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 390)

Cantrip.objects.get_or_create(
    name="Investiture",
    art="sovereign",
    level=4,
    primary_realm="actor",
    glamour_cost="1 (Wyrd) + 1 Willpower",
    difficulty=9,
    duration="Investiture",
    range="Presence",
    type_of_effect="wyrd",
    effect="Grant target temporary authority/privilege. Effect depends on Realm and nature. Investiture requires formal ceremony/coronation. Grants situational authority.",
    bunk_examples=["Formal investiture ceremony", "Crown/anoint", "Declare authority"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 390)

Cantrip.objects.get_or_create(
    name="Unbent Will",
    art="sovereign",
    level=5,
    primary_realm="actor",
    glamour_cost="1 (Wyrd) + 1 Willpower",
    difficulty=9,
    duration="Scene",
    range="Self",
    type_of_effect="wyrd",
    effect="Become living embodiment of authority. All resistance to commands (Dictum/Retinue/Mastery) difficulty raises by Glamour. Caster cannot be intimidated, compelled, or influenced by those of lower Willpower rating.",
    bunk_examples=["Crown self", "Sit throne", "Declare dominion", "Stand imperiously"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 391)

# SUMMER ART
Cantrip.objects.get_or_create(
    name="Flicker-Flies",
    art="summer",
    level=1,
    primary_realm="fae",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Scene",
    range="Sight",
    type_of_effect="chimerical",
    effect="Summon bright dancing light motes evoking emotion. Provide torch-light (Dreaming-visible). Touched by light feel chosen emotion (anger, melancholy, lust, happiness, etc.). -1 difficulty for emotional resonance rolls.",
    bunk_examples=["Create colored lights", "Invoke emotional magic", "Dance with lights"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 385)

Cantrip.objects.get_or_create(
    name="Enkindle",
    art="summer",
    level=2,
    primary_realm="actor",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="chimerical",
    effect="Fan emotion flames to roaring height. Target emotion intensifies. Objects inspire inflamed emotions. Irritation becomes resentment, anger becomes full rage, sadness becomes crippling, happiness becomes leaping.",
    bunk_examples=["Invoke passion magic", "Stoke emotional flames", "Dramatic emotional intensification"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 385)

Cantrip.objects.get_or_create(
    name="Aphrodisia",
    art="summer",
    level=3,
    primary_realm="actor",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Scene",
    range="Sight",
    type_of_effect="chimerical",
    effect="Create all-encompassing awe, fascination, desire. Subject gains magnetic attraction. Person: every word/action entrancing. Object: everyone who beholds covets it. Affects individuals with lower Willpower than successes.",
    bunk_examples=["Invoke attractiveness magic", "Dance seductively", "Embody desirability"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 386)

Cantrip.objects.get_or_create(
    name="Vesta's Blessing",
    art="summer",
    level=4,
    primary_realm="prop",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Until next sunrise or until focus leaves",
    range="Established shelter/fire",
    type_of_effect="wyrd",
    effect="Create home comfort anywhere. Requires shelter/camp/enclosure. Caster becomes aware of non-invited approaches. Welcomed ones restore Willpower/Glamour overnight based on successes.",
    bunk_examples=["Establish sacred fire", "Welcome guests", "Create sanctuary"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 386)

Cantrip.objects.get_or_create(
    name="The Beltane Blade",
    art="summer",
    level=5,
    primary_realm="actor",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Immediate",
    range="Sight",
    type_of_effect="wyrd",
    effect="Erupt target's Banality into red-gold destructive flames. Roll lethal damage (difficulty = target's Banality). With 5+ successes: aggravated damage, every 2 successes burn away 1 Banality.",
    bunk_examples=["Invoke Banality-burning magic", "Dramatic flame manifestation", "Purifying fire"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 387)

# WAYFARE ART
Cantrip.objects.get_or_create(
    name="Hopscotch",
    art="wayfare",
    level=1,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Immediate",
    range="Sight",
    type_of_effect="wyrd",
    effect="Prodigious leaps. Landing always safe regardless of distance. Successes determine jump: 1 = 1 story/30ft; 2 = 2 stories/60ft; 3 = 5 stories/150ft; 4 = 10 stories/300ft; 5 = far as eye sees.",
    bunk_examples=["Leap dramatically", "Invoke jumping magic", "Clear obstacles"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 381)

Cantrip.objects.get_or_create(
    name="Quicksilver",
    art="wayfare",
    level=2,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Next turn",
    range="Sight",
    type_of_effect="wyrd",
    effect="Move as literal blur (speed lines/crackling lightning). Each success = extra action OR doubles movement speed. Hurled objects gain successes as damage dice. Vehicles just speed up.",
    bunk_examples=["Invoke speed magic", "Dramatic acceleration stance", "Trail Glamour"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 382)

Cantrip.objects.get_or_create(
    name="Portal Passage",
    art="wayfare",
    level=3,
    primary_realm="prop",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="1 minute per success",
    range="Up to 10 feet thick barrier",
    type_of_effect="wyrd",
    effect="Create door piercing any barrier (brick/hedge/van). Doors unique to caster (recognizable). Actor/Fae doors: only targeted individuals use. Prop/Nature doors: anyone perceiving Dreaming uses.",
    bunk_examples=["Draw portal", "Invoke gateway magic", "Describe passage destination"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 382)

Cantrip.objects.get_or_create(
    name="Wind Runner",
    art="wayfare",
    level=4,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Based on successes and Glamour",
    range="Sight",
    type_of_effect="wyrd",
    effect="Grant flight power. Objects (rugs, cars): anyone aboard comes along. Weight irrelevant to Glamour. Successes determine flight duration. No safe landing guarantee if magic expires mid-air.",
    bunk_examples=["Invoke flight magic", "Dramatic takeoff", "Invoke wind spirits"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 383)

Cantrip.objects.get_or_create(
    name="Flicker Flash",
    art="wayfare",
    level=5,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Immediate",
    range="Must know/see/possess location",
    type_of_effect="wyrd",
    effect="Teleport anywhere desired. Must know/see/possess destination; can't cross realm boundaries. On others: subject chooses destination. Successes determine speed: (5 - successes) = turns to teleport; 5+ = instant.",
    bunk_examples=["Invoke teleportation magic", "Touch destination", "Dramatic vanishing"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 383)

# WINTER ART
Cantrip.objects.get_or_create(
    name="Chill",
    art="winter",
    level=1,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Successes in turns",
    range="Sight",
    type_of_effect="wyrd",
    effect="Lower target temperature significantly. Living: +1 difficulty to rolls (distraction). Inanimate/non-sentient: Storyteller arbitrates. Changeling has control to cool drinks pleasantly or make creatures shiver.",
    bunk_examples=["Create cold", "Invoke freezing magic", "Winter touch"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 391)

Cantrip.objects.get_or_create(
    name="Hardened Heart",
    art="winter",
    level=2,
    primary_realm="actor",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="chimerical",
    effect="Mute emotion, insulate from manipulation/control. Target cannot spend Willpower during duration. Resist mundane/supernatural mind/emotion control. Objects can resist commands (Dictum).",
    bunk_examples=["Invoke emotional numbness", "Freeze out feeling", "Create cold isolation"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 392)

Cantrip.objects.get_or_create(
    name="Terror of the Long Night",
    art="winter",
    level=3,
    primary_realm="actor",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Scene",
    range="Sight",
    type_of_effect="chimerical",
    effect="Overwhelming existential fear in unending frigid darkness. Target must spend Willpower for any action besides run/hide/cower. Changelings/supernatural resist via Willpower (difficulty 8). Mortals flee automatically.",
    bunk_examples=["Invoke deep fear", "Create primal terror", "Embody winter darkness"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 392)

Cantrip.objects.get_or_create(
    name="Sculpt",
    art="winter",
    level=4,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Based on successes",
    range="Line of sight",
    type_of_effect="wyrd",
    effect="Conjure and sculpt ice. Cannot be mistaken for anything else. Feels bitterly cold to touch. Doesn't melt unless magical heat/flame. Forms approximately 1 cubic foot per turn. Create functional items or combat application.",
    bunk_examples=["Sculpt ice carefully", "Invoke ice formation magic", "Create winter art"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 393)

Cantrip.objects.get_or_create(
    name="Stasis",
    art="winter",
    level=5,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=9,
    duration="Based on successes",
    range="Sight/touch",
    type_of_effect="wyrd",
    effect="Trap target in magical frost. Target immobile, doesn't age/decay/break/change. Conscious beings can resist via Willpower + Stamina (difficulty 9). Supernatural magic thaws frost.",
    bunk_examples=["Invoke magical stasis", "Touch with freezing intent", "Create eternal sleep"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 393)

# SPRING ART
Cantrip.objects.get_or_create(
    name="Awaken",
    art="spring",
    level=1,
    primary_realm="nature",
    glamour_cost="Chimerical (0) or Wyrd (1)",
    difficulty=8,
    duration="Scene (effect dependent)",
    range="Sight/touch",
    type_of_effect="both",
    effect="Call end to hibernation, encourage growth. Plant Glamour seed awakening dormant focus. Anything inert/frozen returns; barren becomes alive. Power by successes (1 = start old car, 5 = counter Stasis).",
    bunk_examples=["Plant seeds", "Invoke growth", "Sing awakening songs"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 383)

Cantrip.objects.get_or_create(
    name="Verdant Reclamation",
    art="spring",
    level=2,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Scene",
    range="Sight",
    type_of_effect="wyrd",
    effect="Speed nature's reclamation. Plant coverage center on target. Roots/flowers/vines sprout covering surface. Lasts 1 scene then withers. Machines become unusable. Living creatures trapped must accumulate successes.",
    bunk_examples=["Invoke rapid growth", "Dance with plants", "Invite nature's embrace"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 384)

Cantrip.objects.get_or_create(
    name="Well of Life",
    art="spring",
    level=3,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Based on successes",
    range="Sight/touch",
    type_of_effect="wyrd",
    effect="Infuse target with healing Glamour. Proximity: restore 1 bashing/lethal per scene. Touch: restore 1 bashing/lethal per turn. Consume focus: restore all bashing/lethal + 1 aggravated.",
    bunk_examples=["Prepare healing focus", "Invoke life force", "Bless food/water"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 384)

Cantrip.objects.get_or_create(
    name="Faerie Ring",
    art="spring",
    level=4,
    primary_realm="nature",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Until next sunrise",
    range="Must create physical circle",
    type_of_effect="wyrd",
    effect="Create protective circle with natural substance. Anyone allowed inside becomes invisible/protected from hostile magic. Each success +1 difficulty for detection/harm. Violators suffer curse.",
    bunk_examples=["Create physical circle", "Invoke protection ritual", "Stand within"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 384)

Cantrip.objects.get_or_create(
    name="Renewal",
    art="spring",
    level=5,
    primary_realm="nature",
    glamour_cost="1 (Wyrd) + 1 Willpower",
    difficulty=8,
    duration="Based on successes",
    range="Sight/recognition",
    type_of_effect="wyrd",
    effect="Grant life to inert/dead target recognized by caster (skeleton/building husk OK). Target returns to life fully as prime. No protections granted. Dies again if killed. Fades at next sunrise.",
    bunk_examples=["Invoke resurrection magic", "Touch target with love", "Perform rebirth ritual"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 385)

# CHRONOS ART
Cantrip.objects.get_or_create(
    name="Backward Glance",
    art="chronos",
    level=1,
    primary_realm="time",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Instant (view of past)",
    range="Sight or known location",
    type_of_effect="chimerical",
    effect="Look backward in time. Range varies by successes: 1 = 1 hour; 2 = 1 day; 3 = 1 week; 4 = 1 month; 5 = 1 year. Specify time or event to focus on.",
    bunk_examples=["Visit location and meditate", "Focus on memory", "Create temporal anchor"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 346)

Cantrip.objects.get_or_create(
    name="Effect and Cause",
    art="chronos",
    level=2,
    primary_realm="time",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="wyrd",
    effect="Scatter temporal progression of target. Sound precedes action, effects precede causes. -3 die penalty to those perceiving target. Knowledgeable casters resist via Wits + Gremayre (difficulty 8).",
    bunk_examples=["Rearrange objects oddly", "Speak in reverse order", "Describe reversed causality"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 347)

Cantrip.objects.get_or_create(
    name="Set in Stone",
    art="chronos",
    level=3,
    primary_realm="time",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Based on successes",
    range="Touch/sight",
    type_of_effect="wyrd",
    effect="Prevent aging, exposure effects on target. Target cannot grow, age, deteriorate, or progress. Doesn't prevent intentional harm. Can prolong other cantrips with sufficient Fae rating.",
    bunk_examples=["Preserve objects carefully", "Ritualize time-stopping", "Hold objects still"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 347)

Cantrip.objects.get_or_create(
    name="Déjà Vu",
    art="chronos",
    level=4,
    primary_realm="time",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Effect lasts turns equal to successes",
    range="Self or willing target",
    type_of_effect="wyrd",
    effect="Relive recent moment to re-experience present with future knowledge. Turn used for orientation (cannot act). Then -3 difficulty to all rolls for successes in turns. Each use increases next use difficulty by 1.",
    bunk_examples=["Describe bunk during casting", "Create time-loop symbolism", "Prepare specifically for moment"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 348)

Cantrip.objects.get_or_create(
    name="Time Dilation",
    art="chronos",
    level=5,
    primary_realm="time",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Subject experiences duration while seconds pass",
    range="Sight",
    type_of_effect="wyrd",
    effect="Push target forward through time out of sync with world. Target ages/suffers time effects while world barely changes. Subject experiences successes duration while seconds pass for others.",
    bunk_examples=["Accelerate growth symbolically", "Describe passage of time", "Ritualize aging"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 348)

# CONTRACT ART
Cantrip.objects.get_or_create(
    name="Done Deal",
    art="contract",
    level=1,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Until contract broken or fulfilled",
    range="Presence required (Realms modify)",
    type_of_effect="chimerical",
    effect="Enter binding oaths with others or sanctify witnessed oaths. Oathbreakers punished by Dreaming. Realms must be Actor/Fae or Prop/Nature. Severity of oath determines curse severity.",
    bunk_examples=["Elaborate oath-taking ceremony", "Blood/ink signing", "Dramatic pronouncements"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 350)

Cantrip.objects.get_or_create(
    name="Liar's Bell",
    art="contract",
    level=2,
    primary_realm="fae",
    glamour_cost="0 (automatic)",
    difficulty=8,
    duration="Permanent once activated",
    range="Bound oath location",
    type_of_effect="chimerical",
    effect="Become aware when someone breaks oath sanctified by caster. Know who and when. Not location/why. Automatically attached to Done Deal. Reduce cantrip difficulty by 1 for locating oathbreaker.",
    bunk_examples=["Listen for bells", "Feel connection to oathbreaker", "Sense betrayal"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 351)

Cantrip.objects.get_or_create(
    name="Castigate",
    art="contract",
    level=3,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Immediate effect",
    range="Anywhere (through oath connection)",
    type_of_effect="chimerical",
    effect="Reach out to inflict punishment on oathbreaker. Reflexively target oathbreaker with known cantrip through whatever Realm bound the oath. No Fae/Actor required.",
    bunk_examples=["Direct curse specifically", "Speak punishment aloud", "Invoke Dreaming's justice"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 351)

Cantrip.objects.get_or_create(
    name="Casual Contract",
    art="contract",
    level=4,
    primary_realm="fae",
    glamour_cost="0 (modifies Done Deal)",
    difficulty=8,
    duration="Until broken",
    range="Within Done Deal's range",
    type_of_effect="chimerical",
    effect="Sanctify careless agreements, idle boasts, sarcastic rejoinders as binding contracts. Permanently modifies Done Deal's scope.",
    bunk_examples=["Casual oath-taking", "Nonverbal binding", "Ironic contract formalization"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 352)

Cantrip.objects.get_or_create(
    name="Sanctified Words",
    art="contract",
    level=5,
    primary_realm="fae",
    glamour_cost="1 (Wyrd) + successes for enchantments",
    difficulty=8,
    duration="Based on enchantment",
    range="Oath location",
    type_of_effect="chimerical",
    effect="Weave Glamour into contracts to grant blessings assisting oath fulfillment. Successes buy enchantments: Favor of Mists (1/die pool), Fortified Will (1/Willpower), Questing Token (1), Bond of Glamour (2/Glamour).",
    bunk_examples=["Inscribe oath terms", "Create magical seals", "Invoke legendary blessings"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 352)

# NAMING ART
Cantrip.objects.get_or_create(
    name="Between the Lines",
    art="naming",
    level=1,
    primary_realm="fae",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Scene (bonus dice persist)",
    range="Sight/hearing",
    type_of_effect="chimerical",
    effect="Understand any language or intended meaning. Realm dictates message source. Any successes allow understanding. Each success = +1 die to contested rolls seeking truth/seeing through lies for scene.",
    bunk_examples=["Study written works", "Listen carefully", "Invoke comprehension magic"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 354)

Cantrip.objects.get_or_create(
    name="Nickname",
    art="naming",
    level=2,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="wyrd",
    effect="Apply cursory label warping identity. Everyone sees target through nickname lens. Sentient creatures cannot regain Willpower unless acting per nickname spirit. Objects conform to nickname spirit.",
    bunk_examples=["Announce nickname publicly", "Describe effect clearly", "Invoke identity change"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 355)

Cantrip.objects.get_or_create(
    name="Saining",
    art="naming",
    level=3,
    primary_realm="fae",
    glamour_cost="1 (Wyrd) per roll",
    difficulty=8,
    duration="Permanent (once learned)",
    range="Must have target presence, intimate knowledge, or possession",
    type_of_effect="wyrd",
    effect="Uncover True Name via extended action. Accumulate successes = target's (Willpower x 3). Gives -5 difficulty to all cantrips/contested magic with target after learning name.",
    bunk_examples=["Perform extended ritual", "Meditate on target", "Accumulate clues"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 355)

Cantrip.objects.get_or_create(
    name="Runic Imprint",
    art="naming",
    level=4,
    primary_realm="prop",
    glamour_cost="1 (Wyrd) + 1 per roll",
    difficulty=8,
    duration="Based on successes",
    range="Touch (apply rune physically or in air/dirt)",
    type_of_effect="wyrd",
    effect="Extended action writing/drawing rune. Spend Glamour per roll. Reduce/enhance Attributes on target. On objects without Attributes, modify function/capability.",
    bunk_examples=["Draw actual runes", "Inscribe carefully", "Speak incantations", "Create magical symbols"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 356)

Cantrip.objects.get_or_create(
    name="Reweaving",
    art="naming",
    level=5,
    primary_realm="fae",
    glamour_cost="1 (Wyrd) + (1 Glamour + 1 Willpower per roll)",
    difficulty=8,
    duration="Based on successes",
    range="Sight",
    type_of_effect="wyrd",
    effect="Extended action rewriting target's name. Minor change (tastes/habits, addiction): 1 success. Moderate (interests/mood, form change): 2. Major (inner nature, Court switch): 3. Total (change Legacies): 4. Fundamental (rearrange Attributes, form change): 5.",
    bunk_examples=["Perform elaborate ritual", "Invoke fundamental change", "Meditate on transformation"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 356)

# ONEIROMANCY ART
Cantrip.objects.get_or_create(
    name="Dream Walk",
    art="oneiromancy",
    level=1,
    primary_realm="fae",
    glamour_cost="1 (Wyrd)",
    difficulty=8,
    duration="Until dream ends or caster leaves",
    range="Must target sleeping being (know well or see)",
    type_of_effect="wyrd",
    effect="Forge bridge between Dreaming and target's mind. Fully enter target's dream. Don't rest yourself. May take chimerical damage. Don't risk physical harm. Spend Willpower to forge connection.",
    bunk_examples=["Sleep next to target", "Meditate on their dreams", "Create sleep-state gesture"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 357)

Cantrip.objects.get_or_create(
    name="Dream Craft",
    art="oneiromancy",
    level=2,
    primary_realm="fae",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Effects last 1 day per success",
    range="Inside target's dream via Dream Walk",
    type_of_effect="chimerical",
    effect="Exert control within dreamscape. Shape dreams, create peaceful/terrifying scenarios. Positive dreams grant +1 Willpower recovery, +2 dice when encountering trigger. Nightmares drain -1 Willpower.",
    bunk_examples=["Narrate dream visions", "Invoke emotional intensity", "Create symbolic imagery"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 357)

Cantrip.objects.get_or_create(
    name="Dream Portal",
    art="oneiromancy",
    level=3,
    primary_realm="fae",
    glamour_cost="1 (Wyrd) per roll (extended action)",
    difficulty=8,
    duration="Portal open while in dream",
    range="Through target's dream to caster's location",
    type_of_effect="wyrd",
    effect="Extended action overlapping dreaming mind with Dreaming itself. Create portal through target's dream. Realm dictates what transports. Successes = mass/volume (1 = adult human).",
    bunk_examples=["Describe portal destination", "Invoke travel magic", "Create gateway symbol"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 358)

Cantrip.objects.get_or_create(
    name="Manifest",
    art="oneiromancy",
    level=4,
    primary_realm="fae",
    glamour_cost="Chimerical (0) or Wyrd (1)",
    difficulty=8,
    duration="Requires daily Glamour infusion or fades when dreamer next sleeps",
    range="Dream to waking world",
    type_of_effect="both",
    effect="Pull dream elements into waking as chimera. Target disappears from dream. Chimera retains dream nature. Automatically gain insight. Maintain with daily Glamour or becomes permanent.",
    bunk_examples=["Describe dream form", "Invoke manifestation magic", "Create symbolic transition"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 358)

Cantrip.objects.get_or_create(
    name="Dream Puppet",
    art="oneiromancy",
    level=5,
    primary_realm="actor",
    glamour_cost="1 (Wyrd) + 1 Willpower if human-level+ intelligence",
    difficulty=9,
    duration="Based on successes",
    range="Via Dream Walk connection",
    type_of_effect="wyrd",
    effect="Invade target's mind and control body while they sleep. Use physical Attributes but retain social/mental Attributes and skills. Can use Arts but not target's abilities. Can't use Dream Walk on others while Puppet-ing.",
    bunk_examples=["Invoke possession magic", "Describe puppet control", "Meditate on target identity"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 359)

# SOOTHSAY ART
Cantrip.objects.get_or_create(
    name="Omen",
    art="soothsay",
    level=1,
    primary_realm="fae",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Instant knowledge",
    range="Sight",
    type_of_effect="chimerical",
    effect="Glimpse subject's destiny thread. Vague, non-immediate. Realm determines target. Multiple castings on same target cumulatively cost +1 Glamour each. Successes reveal destiny clues.",
    bunk_examples=["Traditional divination", "Read signs", "Interpret symbols"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 373)

Cantrip.objects.get_or_create(
    name="Seer's Wisp",
    art="soothsay",
    level=2,
    primary_realm="fae",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Glamour hours",
    range="Conjured within sight",
    type_of_effect="chimerical",
    effect="Conjure bright Dreaming fragment leading to sought target. Whisper name/description. Leads unerringly along Dán paths. Lasts Glamour hours. Only use once per story per subject.",
    bunk_examples=["Create guiding light", "Invoke Dán", "Summon destiny guide"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 373)

Cantrip.objects.get_or_create(
    name="Tattletale",
    art="soothsay",
    level=3,
    primary_realm="actor",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="1 day per success",
    range="Sight (establish focus)",
    type_of_effect="chimerical",
    effect="Scry distant scenes through ensorcelled object/person. Traditionally reflective surface, some use screens/monitors. Requires obvious ritual dedication. Use perception cantrips through focus once connected.",
    bunk_examples=["Prepare scrying focus", "Invoke vision magic", "Meditate on connection"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 374)

Cantrip.objects.get_or_create(
    name="Augury",
    art="soothsay",
    level=4,
    primary_realm="fae",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Instant knowledge",
    range="Realm-dependent",
    type_of_effect="chimerical",
    effect="Extended action reaching into Dán weave. Reveal fragmented path toward desired fortune. Unreliable/expensive road but leads to fated outcome. One clue per success. Only 1 attempt per story per fortune.",
    bunk_examples=["Ritual Dán touching", "Meditation", "Elaborate divination ceremony"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 375)

Cantrip.objects.get_or_create(
    name="Fate Fire",
    art="soothsay",
    level=5,
    primary_realm="fae",
    glamour_cost="Chimerical (0)",
    difficulty=8,
    duration="Hanging (until fortuitous moment) or contested",
    range="Sight",
    type_of_effect="chimerical",
    effect="Lay hands on Dán threads, bending to will. Bless subject: +1 automatic success per success at auspicious moment. Curse subject: -1 automatic success per success at dire moment. One Fate Fire per target at time.",
    bunk_examples=["Invoke destiny threads", "Bless/curse dramatically", "Touch Dán weave"],
)[0].add_source("Changeling: the Dreaming 20th Anniversary Edition", 375)
