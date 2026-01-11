from characters.models.vampire.clan import VampireClan
from populate_db.vampire.vampire_clans import (
    brujah,
    gangrel,
    giovanni,
    lasombra,
    toreador,
    tzimisce,
)
from populate_db.vampire.vampire_disciplines import (
    animalism,
    auspex,
    daimoinon,
    dominate,
    flight,
    fortitude,
    melpominee,
    mytherceria,
    necromancy,
    obeah,
    obfuscate,
    obtenebration,
    potence,
    presence,
    protean,
    serpentis,
    temporis,
    thanatosis,
    valeren,
    visceratika,
)

# BAALI
baali = VampireClan.objects.get_or_create(
    name="Baali",
    nickname="Demons, Infernalists",
    weakness="Demonic corruption aura; their dark presence is palpable to those sensitive to such things. "
    "Deeply tied to infernal powers.",
    description="Obscure origins with demonic connections. Can re-embrace vampires into their bloodline "
    "(Daimoinon 6). Practice infernalism and demon worship. Extremely rare and hunted by most vampires. "
    "Seek to bring about apocalypse through demonic means.",
    is_bloodline=True,
    parent_clan=None,  # Obscure/unknown origins
)[0]
baali.disciplines.add(daimoinon, obfuscate, presence)

# DAUGHTERS OF CACOPHONY
daughters = VampireClan.objects.get_or_create(
    name="Daughters of Cacophony",
    nickname="Daughters, Sirens",
    weakness="The Fugue - constant music heard only by the Daughter. Can be distracting and maddening. "
    "They hear an endless song that no one else can perceive.",
    description="Mixed Toreador/Ventrue/Malkavian lineage. Voice-based powers through Melpominee. "
    "All members are female. Obsessed with music and vocal perfection. Often found in music scenes "
    "and performance venues.",
    is_bloodline=True,
    parent_clan=toreador,  # Mixed but primarily Toreador
)[0]
daughters.disciplines.add(fortitude, melpominee, presence)

# GARGOYLES (Standard/Warrior variant)
gargoyle = VampireClan.objects.get_or_create(
    name="Gargoyle",
    nickname="Slaves, Rockheads",
    weakness="Willpower considered 2 points lower when resisting mind control (Warrior variant: "
    "body parts turn to stone during frenzy).",
    description="Created by Tremere from mix of Gangrel, Nosferatu, and Tzimisce vitae. All can fly; "
    "wings required as psychological focus. Warrior variant is most common. Stone-like appearance. "
    "Many have freed themselves from Tremere control.",
    is_bloodline=True,
    parent_clan=gangrel,  # Mixed but listing Gangrel as primary component
)[0]
gargoyle.disciplines.add(flight, fortitude, potence, visceratika)

# GARGOYLE SCOUT
gargoyle_scout = VampireClan.objects.get_or_create(
    name="Gargoyle Scout",
    nickname="Scouts, Spies",
    weakness="Double injury penalties. More fragile than other Gargoyle variants.",
    description="Scout variant of Gargoyles created by Tremere. Specializes in reconnaissance and stealth. "
    "Uses Auspex and Obfuscate for spying. Wings allow flight but frame is lighter and more vulnerable.",
    is_bloodline=True,
    parent_clan=gargoyle,
)[0]
gargoyle_scout.disciplines.add(auspex, obfuscate, flight)

# GARGOYLE SENTINEL
gargoyle_sentinel = VampireClan.objects.get_or_create(
    name="Gargoyle Sentinel",
    nickname="Sentinels, Guardians",
    weakness="Dice pools halved when acting without master or friend present. Psychologically dependent "
    "on having someone to protect.",
    description="Sentinel variant of Gargoyles created by Tremere. Built for guarding and protection. "
    "Extremely loyal when bonded. Suffers from psychological need for someone to protect.",
    is_bloodline=True,
    parent_clan=gargoyle,
)[0]
gargoyle_sentinel.disciplines.add(flight, potence, fortitude)

# HARBINGERS OF SKULLS
harbingers = VampireClan.objects.get_or_create(
    name="Harbingers of Skulls",
    nickname="Harbingers, Lazarenes",
    weakness="Spent centuries in the Shadowlands; many have trauma and Derangements related to death "
    "and the underworld. Corpse-like appearance.",
    description="Cappadocian remnants who survived Giovanni purge. Seek revenge against Giovanni. "
    "Use Necromancy and wear death masks with embedded jewels indicating status and achievements. "
    "Deeply connected to the Underworld.",
    is_bloodline=True,
    parent_clan=giovanni,  # Technically Cappadocian, but listing Giovanni as closest existing
)[0]
harbingers.disciplines.add(auspex, necromancy, fortitude)

# KIASYD
kiasyd = VampireClan.objects.get_or_create(
    name="Kiasyd",
    nickname="Weirds, Philosophers",
    weakness="Alien and unsettling beauty; fae-touched appearance makes social interaction difficult. "
    "Obsessed with knowledge to unhealthy degree.",
    description="Created by Marconius mixing Lasombra vitae with fae essence. Tall, pale, with black eyes. "
    "Obsessed with knowledge and books. Practice Mytherceria, a fae-touched Discipline. Reclusive scholars.",
    is_bloodline=True,
    parent_clan=lasombra,
)[0]
kiasyd.disciplines.add(dominate, mytherceria, obtenebration)

# NAGARAJA
nagaraja = VampireClan.objects.get_or_create(
    name="Nagaraja",
    nickname="Flesh-Eaters",
    weakness="Must consume flesh AND blood to survive. Blood alone provides no sustenance. "
    "This makes feeding extremely difficult and Masquerade-breaking.",
    description="Self-embraced necromancers from ancient Enoch. Overgrown fangs. Connected to True Black Hand. "
    "Practice Vitreous Path Necromancy focusing on soul manipulation. Ancient and mysterious origins. "
    "Indian and Middle Eastern features common.",
    is_bloodline=True,
    parent_clan=None,  # Self-made through necromantic ritual
)[0]
# Note: Vitreous Path is a Necromancy path, so using Necromancy discipline
nagaraja.disciplines.add(auspex, necromancy, serpentis)

# SALUBRI (Healer)
salubri_healer = VampireClan.objects.get_or_create(
    name="Salubri",
    nickname="Cyclops, Unicorns",
    weakness="None mechanically, but hunted by Tremere who claim they are soul-stealers. Third eye on "
    "forehead makes them distinctive and easily identified.",
    description="One of the original 13 Clans, nearly destroyed by Tremere. Healers possess Obeah for "
    "supernatural healing. Third eye on forehead (can be visible or hidden). Only seven Salubri may "
    "exist at once according to tradition.",
    is_bloodline=True,
    parent_clan=None,  # Original clan, not bloodline, but nearly extinct
)[0]
salubri_healer.disciplines.add(auspex, fortitude, obeah)

# SALUBRI WARRIOR
salubri_warrior = VampireClan.objects.get_or_create(
    name="Salubri Antitribu",
    nickname="Furies, Warriors",
    weakness="None mechanically, but hunted by Tremere. Third eye on forehead. More aggressive than Healer "
    "branch but still honorable.",
    description="Warrior branch of Salubri. Possess Valeren for combat instead of Obeah. Protect the weak "
    "and hunt infernalists. Third eye manifests during Valeren use. Found primarily in Sabbat as antitribu.",
    is_bloodline=True,
    parent_clan=salubri_healer,
)[0]
salubri_warrior.disciplines.add(auspex, fortitude, valeren)

# SAMEDI
samedi = VampireClan.objects.get_or_create(
    name="Samedi",
    nickname="Stiffs, Zombies",
    weakness="Putrefying bodies; corpse-like appearance similar to advanced decomposition. "
    "Appearance cannot be raised above 1.",
    description="Presumed Giovanni derivative but origins unclear. Voudoun connections; speak with dead. "
    "Bodies in constant state of decay. Uncertain if descended from Loa or vampire. Practice death magic "
    "and thanatosis. Caribbean and African features common.",
    is_bloodline=True,
    parent_clan=giovanni,  # Presumed connection
)[0]
samedi.disciplines.add(fortitude, obfuscate, thanatosis)

# TRUE BRUJAH
true_brujah = VampireClan.objects.get_or_create(
    name="True Brujah",
    nickname="Eloi",
    weakness="Temporal phasing effects can cause disorientation and disconnection from normal time flow.",
    description="Claim to be true successors to original Brujah before Troile's diablerie. Possess Temporis "
    "for time manipulation instead of Celerity. Calm and intellectual, opposite of modern Brujah passion. "
    "Claim pre-diablerie Brujah legacy and philosophy.",
    is_bloodline=True,
    parent_clan=brujah,
)[0]
true_brujah.disciplines.add(potence, presence, temporis)

# BLOOD BROTHERS
blood_brothers = VampireClan.objects.get_or_create(
    name="Blood Brothers",
    nickname="Brothers, Frankensteins",
    weakness="Must remain in close proximity to their circle (created simultaneously from same group). "
    "Suffer penalties when separated from circle-mates.",
    description="Created by Sabbat Tzimisce through fleshcrafting and mass Embrace. Groups of 3-5 created "
    "simultaneously who share mystical bond. Bred for warfare and loyalty. Nearly identical appearance "
    "within circle. Possess Sanguinus (unique Discipline for sharing blood and powers).",
    is_bloodline=True,
    parent_clan=tzimisce,
)[0]
# Note: Blood Brothers have unique Discipline "Sanguinus" not in base list
blood_brothers.disciplines.add(fortitude, potence)

# OLD CLAN TZIMISCE
old_clan = VampireClan.objects.get_or_create(
    name="Old Clan Tzimisce",
    nickname="Koldun, Old Clan",
    weakness="Must rest surrounded by at least 2 handfuls of soil from place of mortal birth or lose "
    "1 blood point per night. Same earth-dependency as regular Tzimisce.",
    description="Tzimisce who never developed or rejected Vicissitude. Practice Koldunic Sorcery instead. "
    "Possess Dominate rather than Vicissitude. More traditional and spiritual. Tied to land and old ways. "
    "Claim to predate Vicissitude in Tzimisce history.",
    is_bloodline=True,
    parent_clan=tzimisce,
)[0]
old_clan.disciplines.add(animalism, auspex, dominate)

# COUNTRY GANGREL
country_gangrel = VampireClan.objects.get_or_create(
    name="Country Gangrel",
    nickname="Hicks, Rurals",
    weakness="Each frenzy adds animal feature (same as Gangrel). Features tend toward rural/farm animals.",
    description="Gangrel who remained in rural areas when main clan left Camarilla. Some stayed with "
    "Camarilla structure. Same as regular Gangrel but with stronger ties to rural domains and agriculture. "
    "More likely to have farm animal features.",
    is_bloodline=True,
    parent_clan=gangrel,
)[0]
country_gangrel.disciplines.add(animalism, fortitude, protean)

# AHRIMANES
ahrimanes = VampireClan.objects.get_or_create(
    name="Ahrimanes",
    nickname="Cat Ladies",
    weakness="Each frenzy adds feline feature specifically. Connection to spirit world can be distracting.",
    description="All-female Gangrel bloodline with connection to feline spirits. Possess Spiritus "
    "(spirit magic) instead of Fortitude. Found primarily in American Southwest. Changed from Gangrel "
    "through mysterious spiritual transformation. Develop cat-like features.",
    is_bloodline=True,
    parent_clan=gangrel,
)[0]
# Note: Spiritus is unique Discipline, using Animalism as stand-in
ahrimanes.disciplines.add(animalism, protean, auspex)

# LHIANNAN
lhiannan = VampireClan.objects.get_or_create(
    name="Lhiannan",
    nickname="Druids, Wilds",
    weakness="Must consume blood of those who practice specific pagan tradition. Feeding restriction "
    "like Ventrue but more narrow.",
    description="Ancient bloodline connected to Celtic druidic practices. Nearly extinct. Connection to "
    "nature and old ways. Practice nature magic. Scottish and Irish origins. Rumored destroyed but some "
    "may survive. Possess Ogham (nature-based Discipline).",
    is_bloodline=True,
    parent_clan=gangrel,  # Celtic nature connection
)[0]
lhiannan.disciplines.add(animalism, fortitude, presence)
