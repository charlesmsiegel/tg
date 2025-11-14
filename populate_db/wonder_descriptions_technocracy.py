# Technocratic Device Descriptions and Effects
# This file adds descriptions and magical effects to Technocratic Devices
# Information extracted from Technocracy: Reloaded and other source books

from items.models.mage.artifact import Artifact
from items.models.mage.talisman import Talisman
from characters.models.mage.effect import Effect

# Alanson Hardsuits - Void Engineer powered armor

# Alanson Light Hardsuit
light_hardsuit_effect = Effect.objects.get_or_create(
    name="Light Combat Armor (Alanson)",
    matter=3,
    forces=2,
    prime=2,
    description="Lightweight powered armor providing protection and enhanced mobility. Includes HUD, environmental seals, and basic combat systems. Armor Rating 3 (+3 soak dice).",
)[0]

light_hardsuit = Talisman.objects.get(name="Alanson Light Hardsuit")
light_hardsuit.description = """The Alanson Light Hardsuit represents the cutting edge of Void Engineer personal protection technology. Designed for operatives who need mobility as much as protection, this powered armor provides substantial defensive capabilities without sacrificing agility.

The suit features:
- **Armor Rating 3**: Provides +3 dice to soak rolls against all physical damage
- **Environmental Sealing**: Complete protection against vacuum, toxins, radiation, and extreme temperatures
- **Heads-Up Display (HUD)**: Tactical information, target tracking, and sensor data overlaid on visor
- **Enhanced Strength**: Servomotors provide +1 Strength for lifting and close combat
- **Limited Flight**: Maneuvering jets allow short bursts of flight or zero-G navigation
- **Communication Suite**: Encrypted quantum-link communicator with global range

The Light Hardsuit is typically deployed for Border Corps Division missions, extraplanetarysecurity operations, and rapid response scenarios. The armor's matte black finish incorporates stealth materials that reduce visual and sensor signatures.

Donning the suit requires 2 minutes with assistance or 5 minutes alone. The suit's Quintessence reserve (25 points) powers all systems, with typical deployment consuming 1-2 points per hour of active use."""
light_hardsuit.save()
light_hardsuit.powers.add(light_hardsuit_effect)

# Alanson R-25 Hardsuit
r25_hardsuit_effect = Effect.objects.get_or_create(
    name="Heavy Combat Armor (Alanson R-25)",
    matter=4,
    forces=3,
    prime=2,
    correspondence=2,
    description="Advanced powered armor with heavy protection, weapons systems, and dimensional stabilizers. Armor Rating 7 when fully powered. Includes integrated weapons and sensor suite.",
)[0]

r25_hardsuit = Talisman.objects.get(name="Alanson R-25 Hardsuit")
r25_hardsuit.description = """The Alanson R-25 Hardsuit is the premier combat armor used by Void Engineer operatives who expect heavy resistance. Substantially more robust than the Light Hardsuit, the R-25 provides maximum protection while maintaining the technological sophistication expected of Enlightened Science.

The suit features:
- **Armor Rating 7**: When fully powered, provides +7 dice to soak rolls (requires 1 Quintessence per scene)
- **Armor Rating 3**: Passive protection even when unpowered
- **Environmental Sealing**: Complete protection against all environmental hazards including hard vacuum and deep ocean pressure
- **Integrated Weapons**: Built-in gauss rifle or plasma caster (wielder's choice at deployment)
- **Dimensional Stabilizers**: Correspondence-based systems that resist teleportation attacks and dimensional shunts
- **Advanced Sensors**: Full-spectrum scanners including infrared, ultraviolet, radiation detection, and Primium resonance scanners
- **Enhanced Strength**: +2 Strength from heavy-duty servomotors
- **Flight Systems**: Sustained flight up to 100 mph for 1 hour per Quintessence point
- **Tactical AI**: Limited artificial intelligence assists with targeting, threat assessment, and tactical analysis

The R-25 is primarily deployed for:
- Deep Umbra exploration and combat
- Paradox Realm incursions
- Reality Deviant elimination operations
- Extradimensional entity containment
- High-threat Construct defense

The suit's distinctive angular design and glowing blue power conduits make it immediately recognizable. It requires 5 minutes to don even with assistance, and its significant bulk (adds 10 lbs to effective weight) makes stealth operations impractical.

The R-25 saw extensive use during the Dimensional Anomaly campaigns of the late 1990s and proved particularly effective against Nephandi incursions. Captain Chen Zhang of the London Border Corps is known to favor this model."""
r25_hardsuit.save()
r25_hardsuit.powers.add(r25_hardsuit_effect)

# Create descriptions for some specific named Technocratic items mentioned in the reference material

# ES-Phone - Enlightened Science Phone (if it exists in the database)
if Talisman.objects.filter(name__icontains="ES-Phone").exists():
    es_phone = Talisman.objects.filter(name__icontains="ES-Phone").first()

    es_phone_effect = Effect.objects.get_or_create(
        name="Secure Communications (ES-Phone)",
        correspondence=3,
        mind=1,
        entropy=2,
        prime=1,
        description="Secure quantum-encrypted smartphone with Digital Web access. Provides global communication, data access, and various Technocratic applications.",
    )[0]

    es_phone.description = """The ES-Phone is standard-issue equipment for all Technocratic operatives, representing the Union's mastery of communication and information technology. Far more than a mere smartphone, this Device provides secure access to the Union's global network and the Digital Web itself.

Key Features:
- **Quantum Encryption**: Entropy-based encryption makes communications impossible to intercept (Data 3/Entropy 2)
- **Digital Web Access**: Direct portal to the Digital Web through specialized VR goggles or neural interface
- **App Suite**:
  - City Eye: Real-time surveillance camera access
  - C-SAM: Chemical/biological sample analysis
  - K-Gram: Encrypted messaging
  - Manar: Augmented reality navigation
  - NOT: Neural Override Transponder (emergency backup consciousness)
  - VDAS Mobile: Vehicular Data Analysis System
- **Global Coverage**: Functions anywhere on Earth and in near-Earth Constructs
- **Biometric Security**: Keyed to specific operative's bioprint
- **Emergency Protocols**: Can summon backup, trigger self-destruct, or upload consciousness to NOT system

The ES-Phone requires 1 Quintessence per day to maintain encryption and Digital Web access. Higher-rank operatives receive phones with additional capabilities including remote drone control, tactical hologram projection, and enhanced AI assistance.

Standard ES-Phones are indistinguishable from high-end commercial smartphones, aiding in maintaining the Technocratic masquerade."""

    es_phone.save()
    if es_phone.powers.exists():
        es_phone.powers.add(es_phone_effect)

# Create some generic Technocratic Device effects that could be applied to various items

# Primium-based effects
primium_counter_effect = Effect.objects.get_or_create(
    name="Primium Countermeasures",
    prime=4,
    description="Primium-enhanced device provides countermagick dice against reality-deviant Effects. The exotic matter disrupts non-Technocratic paradigms.",
)[0]

# Enhanced weapon effects
plasma_weapon_effect = Effect.objects.get_or_create(
    name="Plasma Discharge Weapon",
    forces=4,
    prime=2,
    description="High-energy plasma weapon dealing aggravated damage. Range 100 yards, damage 8 aggravated, capacity 200 shots. Can switch between single shot, burst, and autofire modes.",
)[0]

gauss_weapon_effect = Effect.objects.get_or_create(
    name="Gauss Acceleration Weapon",
    forces=3,
    matter=2,
    description="Magnetically accelerated projectile weapon. Extreme armor penetration. Damage 7 lethal, range 200 yards, capacity 50 rounds. Ignores 2 points of armor.",
)[0]

# Stealth and infiltration effects
optical_camo_effect = Effect.objects.get_or_create(
    name="Optical Camouflage System",
    forces=2,
    correspondence=1,
    description="Advanced light-bending camouflage providing near-invisibility. Adds successes to Stealth rolls for visual detection. Effectiveness reduced when moving.",
)[0]

# Enhanced perception effects
multi_spectrum_effect = Effect.objects.get_or_create(
    name="Multi-Spectrum Scanner",
    forces=1,
    prime=1,
    spirit=1,
    description="Sensors detect across multiple spectrums including infrared, ultraviolet, radiation, and Primium resonance. Can detect invisible entities and magical effects.",
)[0]

# Vehicle/transportation effects
dimensional_drive_effect = Effect.objects.get_or_create(
    name="Dimensional Drive System",
    correspondence=4,
    spirit=3,
    prime=3,
    description="Allows vehicle to traverse dimensional barriers, enter the Umbra, or teleport short distances. Requires significant Quintessence per use.",
)[0]

# Healing/medical effects
nanotech_medical_effect = Effect.objects.get_or_create(
    name="Nanotech Medical System",
    life=4,
    matter=2,
    prime=2,
    description="Advanced medical nanites rapidly heal injuries. Can heal 1 health level per turn for lethal damage, 1 per hour for aggravated. Requires 1 Quintessence per health level.",
)[0]

# Cybernetic enhancement effects
combat_reflex_implant_effect = Effect.objects.get_or_create(
    name="Combat Reflex Implants",
    life=2,
    mind=2,
    time=1,
    description="Neural and adrenal enhancements provide +2 Initiative and +1 to dodge attempts. Grants one free reflexive dodge per turn.",
)[0]

biomod_strength_effect = Effect.objects.get_or_create(
    name="Biomechanical Strength Enhancement",
    life=3,
    matter=2,
    description="Reinforced musculature and skeletal structure. Provides +2 Strength for lifting and striking (maximum 5 before requiring higher-level biomodification).",
)[0]

# Reality Zone manipulation
consensus_anchor_effect = Effect.objects.get_or_create(
    name="Consensus Anchor Field",
    prime=3,
    mind=2,
    entropy=1,
    description="Projects a field that reinforces Technocratic paradigm within area. Increases difficulty of non-scientific magic by +1, reduces Paradox for Technocratic Procedures by -1.",
)[0]

# Data/cyber effects
ai_assistant_effect = Effect.objects.get_or_create(
    name="AI Assistant Protocol",
    mind=3,
    correspondence=2,
    description="Limited artificial intelligence provides tactical analysis, research assistance, and automated tasks. Can operate autonomously for simple instructions.",
)[0]

digital_infiltration_effect = Effect.objects.get_or_create(
    name="Digital Infiltration Suite",
    correspondence=3,
    mind=2,
    entropy=2,
    description="Advanced hacking tools for penetrating computer systems. Reduces difficulty of hacking attempts by -2. Can crack encryption (Entropy 2) and trace data flows (Correspondence 3).",
)[0]

print("Technocratic Device descriptions and effects have been added successfully!")
