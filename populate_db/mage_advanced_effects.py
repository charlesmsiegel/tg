# Additional Mage Effects from Technical Reference
# Focus on advanced and specialized effects from sourcebooks

from characters.models.mage.effect import Effect

# ===== NECROMANCY & DEATH MAGIC =====
Effect.objects.get_or_create(name="Summon Ghost", spirit=2,)[
    0
].add_source("How Do You Do That", 142)

Effect.objects.get_or_create(name="Summon Powerful Ghost", spirit=3,)[
    0
].add_source("How Do You Do That", 142)

Effect.objects.get_or_create(name="See Into Shadowlands", spirit=1, entropy=1,)[
    0
].add_source("How Do You Do That", 142)

Effect.objects.get_or_create(name="Step Sideways to Shadowlands", spirit=3,)[
    0
].add_source("How Do You Do That", 142)

Effect.objects.get_or_create(name="Speak with Dead", spirit=2, mind=1,)[
    0
].add_source("How Do You Do That", 142)

Effect.objects.get_or_create(name="Bind Ghost", spirit=4,)[
    0
].add_source("How Do You Do That", 143)

Effect.objects.get_or_create(name="Banish Ghost", spirit=3, prime=2,)[
    0
].add_source("How Do You Do That", 143)

Effect.objects.get_or_create(name="Create Zombie (Simple)", life=3, matter=2, prime=2,)[
    0
].add_source("How Do You Do That", 144)

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
Effect.objects.get_or_create(name="Sense Time Flow", time=1,)[
    0
].add_source("How Do You Do That", 154)

Effect.objects.get_or_create(name="See Past (Recent)", time=2,)[
    0
].add_source("How Do You Do That", 154)

Effect.objects.get_or_create(name="See Future (Near)", time=2,)[
    0
].add_source("How Do You Do That", 154)

Effect.objects.get_or_create(name="See Past (Distant)", time=3, correspondence=2,)[
    0
].add_source("How Do You Do That", 154)

Effect.objects.get_or_create(name="See Future (Distant)", time=3,)[
    0
].add_source("How Do You Do That", 154)

Effect.objects.get_or_create(name="Slow Time (Local)", time=3,)[
    0
].add_source("How Do You Do That", 155)

Effect.objects.get_or_create(name="Speed Time (Local)", time=3,)[
    0
].add_source("How Do You Do That", 155)

Effect.objects.get_or_create(name="Freeze Time (Small Area)", time=4,)[
    0
].add_source("How Do You Do That", 155)

Effect.objects.get_or_create(name="Stop Time (Large Area)", time=5,)[
    0
].add_source("How Do You Do That", 155)

Effect.objects.get_or_create(name="Rewind Time (Seconds)", time=5, prime=2,)[
    0
].add_source("How Do You Do That", 156)

Effect.objects.get_or_create(name="Travel Through Time", time=5, spirit=4, prime=3,)[
    0
].add_source("How Do You Do That", 156)

Effect.objects.get_or_create(name="Create Time Loop", time=4, prime=2,)[
    0
].add_source("How Do You Do That", 156)

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

Effect.objects.get_or_create(name="Teleport Others", correspondence=4, life=3,)[
    0
].add_source("How Do You Do That", 127)

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

Effect.objects.get_or_create(name="Fold Space", correspondence=5,)[
    0
].add_source("M20 Core", 515)

Effect.objects.get_or_create(
    name="Ward Against Teleportation",
    correspondence=3,
    prime=2,
)[0].add_source("How Do You Do That", 128)

# ===== ADVANCED LIFE MAGIC =====
Effect.objects.get_or_create(name="Shapeshift into Animal (Self)", life=4,)[
    0
].add_source("How Do You Do That", 34)

Effect.objects.get_or_create(name="Shapeshift into Animal (Others)", life=5,)[
    0
].add_source("How Do You Do That", 34)

Effect.objects.get_or_create(name="Shapeshift into Hybrid Form", life=4, prime=2,)[
    0
].add_source("How Do You Do That", 34)

Effect.objects.get_or_create(name="Create Homunculus", life=5, prime=3, mind=2,)[
    0
].add_source("Book of Secrets", 79)

Effect.objects.get_or_create(name="Clone Body", life=5, prime=2, mind=1,)[
    0
].add_source("Book of Secrets", 79)

Effect.objects.get_or_create(
    name="Enhance Physical Attribute (Permanent)",
    life=4,
    prime=2,
)[0].add_source("M20 Core", 518)

Effect.objects.get_or_create(name="Grant Regeneration", life=4, prime=2,)[
    0
].add_source("M20 Core", 518)

Effect.objects.get_or_create(name="Age/De-Age Target", life=4, time=2,)[
    0
].add_source("M20 Core", 518)

Effect.objects.get_or_create(name="Cure Poison/Disease (Aggravated)", life=4,)[
    0
].add_source("M20 Core", 518)

# ===== ADVANCED MIND MAGIC =====
Effect.objects.get_or_create(name="Read Surface Thoughts", mind=2,)[
    0
].add_source("M20 Core", 519)

Effect.objects.get_or_create(name="Read Deep Thoughts/Memories", mind=3,)[
    0
].add_source("M20 Core", 519)

Effect.objects.get_or_create(name="Implant False Memory", mind=4,)[
    0
].add_source("M20 Core", 519)

Effect.objects.get_or_create(name="Mind Control (Simple Command)", mind=3,)[
    0
].add_source("M20 Core", 519)

Effect.objects.get_or_create(name="Mind Control (Complex)", mind=4,)[
    0
].add_source("M20 Core", 519)

Effect.objects.get_or_create(name="Possession", mind=4, life=3,)[
    0
].add_source("How Do You Do That", 164)

Effect.objects.get_or_create(name="Astral Quest", mind=5, spirit=3,)[
    0
].add_source("M20 Core", 519)

Effect.objects.get_or_create(name="Shatter Mind", mind=5,)[
    0
].add_source("M20 Core", 519)

Effect.objects.get_or_create(name="Create Permanent Mental Illusion", mind=4, prime=2,)[
    0
].add_source("How Do You Do That", 162)

Effect.objects.get_or_create(name="Mass Telepathy", mind=3, correspondence=2,)[
    0
].add_source("M20 Core", 519)

# ===== ADVANCED FORCES =====
Effect.objects.get_or_create(name="Lightning Bolt", forces=3,)[
    0
].add_source("M20 Core", 517)

Effect.objects.get_or_create(name="Fireball", forces=3,)[
    0
].add_source("M20 Core", 517)

Effect.objects.get_or_create(name="Force Shield", forces=3,)[
    0
].add_source("M20 Core", 517)

Effect.objects.get_or_create(name="Flight (Self)", forces=2, life=2,)[
    0
].add_source("How Do You Do That", 126)

Effect.objects.get_or_create(name="Flight (Others)", forces=3, life=2,)[
    0
].add_source("How Do You Do That", 126)

Effect.objects.get_or_create(name="Call Storm", forces=4, prime=2,)[
    0
].add_source("How Do You Do That", 49)

Effect.objects.get_or_create(
    name="Control Weather (Major)",
    forces=5,
    life=2,
    matter=2,
    prime=2,
)[0].add_source("How Do You Do That", 49)

Effect.objects.get_or_create(name="Laser Blast", forces=3, matter=2,)[
    0
].add_source("M20 Core", 517)

Effect.objects.get_or_create(name="EMP Pulse", forces=3, matter=2,)[
    0
].add_source("M20 Core", 517)

Effect.objects.get_or_create(name="Nuclear Blast", forces=5, prime=4,)[
    0
].add_source("M20 Core", 517)

# ===== ADVANCED MATTER =====
Effect.objects.get_or_create(name="Transmute Base Metals to Gold", matter=3,)[
    0
].add_source("M20 Core", 518)

Effect.objects.get_or_create(name="Create Matter from Nothing", matter=4, prime=2,)[
    0
].add_source("M20 Core", 518)

Effect.objects.get_or_create(name="Alter Fundamental Properties", matter=5,)[
    0
].add_source("M20 Core", 518)

Effect.objects.get_or_create(name="Phase Through Matter", matter=3, life=2,)[
    0
].add_source("M20 Core", 518)

Effect.objects.get_or_create(name="Disintegrate Object", matter=4,)[
    0
].add_source("M20 Core", 518)

Effect.objects.get_or_create(name="Turn to Stone", matter=3, life=3,)[
    0
].add_source("M20 Core", 518)

# ===== ADVANCED ENTROPY =====
Effect.objects.get_or_create(name="Curse of Bad Luck", entropy=3,)[
    0
].add_source("M20 Core", 516)

Effect.objects.get_or_create(name="Blessing of Good Fortune", entropy=3,)[
    0
].add_source("M20 Core", 516)

Effect.objects.get_or_create(name="Age Object Rapidly", entropy=3, time=2,)[
    0
].add_source("M20 Core", 516)

Effect.objects.get_or_create(name="Rot Living Being", entropy=4, life=2,)[
    0
].add_source("M20 Core", 516)

Effect.objects.get_or_create(name="Shatter Pattern", entropy=5, prime=2,)[
    0
].add_source("M20 Core", 516)

Effect.objects.get_or_create(name="Control Probability (Major)", entropy=4,)[
    0
].add_source("M20 Core", 516)

Effect.objects.get_or_create(name="Death Curse", entropy=5, life=4, spirit=3,)[
    0
].add_source("M20 Core", 516)

# ===== ADVANCED PRIME =====
Effect.objects.get_or_create(name="Sense Quintessence", prime=1,)[
    0
].add_source("M20 Core", 520)

Effect.objects.get_or_create(name="Channel Quintessence", prime=3,)[
    0
].add_source("M20 Core", 520)

Effect.objects.get_or_create(name="Enchant Talisman", prime=3,)[
    0
].add_source("Book of Secrets", 82)

Effect.objects.get_or_create(name="Create Wonder", prime=5,)[
    0
].add_source("Book of Secrets", 82)

Effect.objects.get_or_create(name="Disenchant Wonder", prime=4,)[
    0
].add_source("M20 Core", 520)

Effect.objects.get_or_create(name="Nullify Magic", prime=3,)[
    0
].add_source("M20 Core", 520)

Effect.objects.get_or_create(name="Permanently Enhance Pattern", prime=5,)[
    0
].add_source("M20 Core", 520)

Effect.objects.get_or_create(name="Fuel Pattern with Quintessence", prime=2,)[
    0
].add_source("M20 Core", 520)

Effect.objects.get_or_create(name="Create Tass", prime=3,)[
    0
].add_source("M20 Core", 520)

Effect.objects.get_or_create(name="Open/Seal Node", prime=4, spirit=2,)[
    0
].add_source("M20 Core", 520)

# ===== ADVANCED SPIRIT =====
Effect.objects.get_or_create(name="See Spirits", spirit=1,)[
    0
].add_source("M20 Core", 521)

Effect.objects.get_or_create(name="Touch Spirit Matter", spirit=2,)[
    0
].add_source("M20 Core", 521)

Effect.objects.get_or_create(name="Step Sideways to Umbra", spirit=3,)[
    0
].add_source("M20 Core", 521)

Effect.objects.get_or_create(name="Reach Into Umbra", spirit=3,)[
    0
].add_source("M20 Core", 521)

Effect.objects.get_or_create(name="Summon Spirit (Minor)", spirit=2,)[
    0
].add_source("How Do You Do That", 148)

Effect.objects.get_or_create(name="Summon Spirit (Powerful)", spirit=3,)[
    0
].add_source("How Do You Do That", 148)

Effect.objects.get_or_create(name="Bind Spirit", spirit=4,)[
    0
].add_source("How Do You Do That", 148)

Effect.objects.get_or_create(name="Create Spirit Gate", spirit=4, prime=2,)[
    0
].add_source("M20 Core", 521)

Effect.objects.get_or_create(name="Create Fetish", spirit=4, prime=2,)[
    0
].add_source("M20 Core", 521)

Effect.objects.get_or_create(name="Strengthen/Weaken Gauntlet", spirit=4,)[
    0
].add_source("M20 Core", 521)

Effect.objects.get_or_create(name="Create Spirit", spirit=5, prime=4,)[
    0
].add_source("M20 Core", 521)

Effect.objects.get_or_create(name="Permanently Destroy Spirit", spirit=5, prime=3,)[
    0
].add_source("M20 Core", 521)

# ===== CROSS-SPLAT EFFECTS =====
Effect.objects.get_or_create(
    name="Break Blood Bond",
    life=4,
    mind=3,
    entropy=3,
    prime=1,
)[0].add_source("Book of Secrets", 86)

Effect.objects.get_or_create(name="Harm Vampire", life=3, matter=2,)[
    0
].add_source("Gods & Monsters", 58)

Effect.objects.get_or_create(name="Heal Vampire", life=3, matter=2,)[
    0
].add_source("Gods & Monsters", 58)

Effect.objects.get_or_create(name="Harm Werewolf", life=3, spirit=3,)[
    0
].add_source("Gods & Monsters", 75)

Effect.objects.get_or_create(name="Heal Werewolf", life=3, spirit=2,)[
    0
].add_source("Gods & Monsters", 75)

Effect.objects.get_or_create(name="Harm Fae", life=3, mind=3,)[
    0
].add_source("Gods & Monsters", 104)

Effect.objects.get_or_create(name="Heal Fae", life=3, mind=3,)[
    0
].add_source("Gods & Monsters", 104)

Effect.objects.get_or_create(name="Counter Fae Glamour", prime=2, mind=2,)[
    0
].add_source("Gods & Monsters", 104)

Effect.objects.get_or_create(name="Harm Ghost", prime=2, entropy=3,)[
    0
].add_source("Gods & Monsters", 120)

Effect.objects.get_or_create(name="Strengthen Ghost", spirit=3, prime=2,)[
    0
].add_source("Gods & Monsters", 120)

# ===== PARADIGM-SPECIFIC EFFECTS =====
# Akashic Brotherhood
Effect.objects.get_or_create(name="Do Strike (Akashic)", life=2, mind=1, prime=1,)[
    0
].add_source("Lore of the Traditions", 28)

Effect.objects.get_or_create(name="Dragon Pearl Meditation", prime=3, mind=2,)[
    0
].add_source("Lore of the Traditions", 28)

Effect.objects.get_or_create(name="Chi Healing", life=3, prime=1,)[
    0
].add_source("Lore of the Traditions", 28)

# Celestial Chorus
Effect.objects.get_or_create(name="Holy Fire", forces=3, prime=2,)[
    0
].add_source("Lore of the Traditions", 48)

Effect.objects.get_or_create(name="Blessing of the One", prime=2, mind=2, life=1,)[
    0
].add_source("Lore of the Traditions", 48)

Effect.objects.get_or_create(name="Call Divine Intervention", prime=4, spirit=3,)[
    0
].add_source("Lore of the Traditions", 48)

# Cult of Ecstasy
Effect.objects.get_or_create(name="Temporal Fugue", time=3, mind=2,)[
    0
].add_source("Lore of the Traditions", 68)

Effect.objects.get_or_create(name="Ecstatic Vision", mind=2, time=1,)[
    0
].add_source("Lore of the Traditions", 68)

# Dreamspeakers
Effect.objects.get_or_create(name="Spirit Journey", spirit=3, mind=1,)[
    0
].add_source("Lore of the Traditions", 88)

Effect.objects.get_or_create(name="Call Totem Spirit", spirit=4,)[
    0
].add_source("Lore of the Traditions", 88)

Effect.objects.get_or_create(name="Medicine Work Healing", life=3, spirit=1,)[
    0
].add_source("Lore of the Traditions", 88)

# Euthanatos
Effect.objects.get_or_create(name="Good Death", entropy=3, life=3, spirit=2,)[
    0
].add_source("Lore of the Traditions", 108)

Effect.objects.get_or_create(name="Wheel of Fate", entropy=4, time=2,)[
    0
].add_source("Lore of the Traditions", 108)

# Order of Hermes
Effect.objects.get_or_create(
    name="Hermetic Circle of Protection",
    prime=2,
    forces=2,
    mind=1,
)[0].add_source("Lore of the Traditions", 128)

Effect.objects.get_or_create(name="Summon Elemental", forces=4, spirit=3, prime=2,)[
    0
].add_source("Lore of the Traditions", 128)

Effect.objects.get_or_create(name="Alchemical Transmutation", matter=3, prime=2,)[
    0
].add_source("Lore of the Traditions", 128)

# Sons of Ether
Effect.objects.get_or_create(name="Ether Ray", forces=3, matter=2, prime=1,)[
    0
].add_source("Lore of the Traditions", 148)

Effect.objects.get_or_create(
    name="Dimensional Portal Device",
    correspondence=4,
    matter=3,
    prime=2,
)[0].add_source("Lore of the Traditions", 148)

# Verbena
Effect.objects.get_or_create(name="Blood Magic Ritual", life=3, prime=2,)[
    0
].add_source("Lore of the Traditions", 168)

Effect.objects.get_or_create(name="Primal Transformation", life=4, spirit=2,)[
    0
].add_source("Lore of the Traditions", 168)

Effect.objects.get_or_create(name="Call the Wild Hunt", spirit=4, life=2, mind=2,)[
    0
].add_source("Lore of the Traditions", 168)

# Virtual Adepts
Effect.objects.get_or_create(name="Reality Hack", correspondence=3, forces=2, prime=1,)[
    0
].add_source("Lore of the Traditions", 188)

Effect.objects.get_or_create(name="Digital Avatar", correspondence=3, mind=3, prime=2,)[
    0
].add_source("Lore of the Traditions", 188)

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

Effect.objects.get_or_create(name="Mind Wipe (Flashy Thing)", mind=3,)[
    0
].add_source("Technocracy Reloaded", 225)

Effect.objects.get_or_create(name="Biometric Scan", life=2, correspondence=1,)[
    0
].add_source("Technocracy Reloaded", 216)

Effect.objects.get_or_create(name="Genetic Modification", life=4, matter=2, prime=2,)[
    0
].add_source("Technocracy Reloaded", 158)

Effect.objects.get_or_create(name="Dimensional Backdoor", correspondence=4, spirit=5,)[
    0
].add_source("Technocracy Reloaded", 227)

Effect.objects.get_or_create(
    name="PAWS Taser (Anti-Shapeshifter)",
    forces=3,
    life=4,
    spirit=3,
    prime=2,
)[0].add_source("Technocracy Reloaded", 224)

Effect.objects.get_or_create(name="Sleepteacher Accelerated Learning", mind=3, time=2,)[
    0
].add_source("Technocracy Reloaded", 230)

# ===== NEPHANDI/MARAUDER EFFECTS =====
Effect.objects.get_or_create(name="Infernal Pact", prime=4, spirit=4, entropy=3,)[
    0
].add_source("Book of the Fallen", 145)

Effect.objects.get_or_create(name="Corrupt Pattern", entropy=4, life=3, prime=2,)[
    0
].add_source("Book of the Fallen", 148)

Effect.objects.get_or_create(name="Summon Demon", spirit=4, prime=3, entropy=2,)[
    0
].add_source("Book of the Fallen", 150)

Effect.objects.get_or_create(name="Reality Cancer", prime=5, entropy=5,)[
    0
].add_source("Book of the Fallen", 155)

# ===== UTILITY & MISCELLANEOUS =====
Effect.objects.get_or_create(name="Permanent Enchantment", prime=5,)[
    0
].add_source("M20 Core", 520)

Effect.objects.get_or_create(name="Counterspell (Basic)", prime=2,)[
    0
].add_source("M20 Core", 542)

Effect.objects.get_or_create(name="Counterspell (Advanced)", prime=3,)[
    0
].add_source("M20 Core", 542)

Effect.objects.get_or_create(name="Dispel Paradox", prime=3, entropy=2,)[
    0
].add_source("M20 Core", 548)

Effect.objects.get_or_create(name="Absorb Quintessence from Living", prime=5, life=3,)[
    0
].add_source("Book of Secrets", 102)

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

Effect.objects.get_or_create(name="Ward Against Spirits", spirit=3, prime=2,)[
    0
].add_source("M20 Core", 521)

Effect.objects.get_or_create(
    name="Mass Teleportation",
    correspondence=5,
    life=3,
    mind=2,
)[0].add_source("M20 Core", 515)

Effect.objects.get_or_create(name="Destroy Pattern Permanently", prime=5, entropy=4,)[
    0
].add_source("M20 Core", 520)
