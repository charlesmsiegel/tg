from items.models.mage.artifact import Artifact
from items.models.mage.grimoire import Grimoire
from items.models.mage.talisman import Talisman
from characters.models.mage.effect import Effect

Artifact.objects.get_or_create(display=False, name="'O'ole Tatu", background_cost=6)
Talisman.objects.get_or_create(
    display=False,
    name="3-Dim Sonographic Sense Factory",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Abh-t Dagger", background_cost=4, arete=2, quintessence_max=10
)[0]
Artifact.objects.get_or_create(display=False, name="Abundanti's Oil", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Accelerated Force Cannon (AFC)",
    background_cost=9,
    arete=6,
    quintessence_max=30,
)[0]
Artifact.objects.get_or_create(display=False, name="Advanced Bugs", background_cost=1)
Artifact.objects.get_or_create(
    display=False, name="Advanced Power Cell (APC)", background_cost=3
)[0]
Artifact.objects.get_or_create(
    display=False, name="Akaa' Et Nuon Ta", background_cost=4
)[0].add_source("Book of the Fallen", 165)
Talisman.objects.get_or_create(
    display=False,
    name="Alanson Light Hardsuit",
    background_cost=8,
    arete=3,
    quintessence_max=25,
    description="""The Alanson Light Hardsuit represents the cutting edge of Void Engineer personal protection technology. Designed for operatives who need mobility as much as protection, this powered armor provides substantial defensive capabilities without sacrificing agility.

The suit features:
- **Armor Rating 3**: Provides +3 dice to soak rolls against all physical damage
- **Environmental Sealing**: Complete protection against vacuum, toxins, radiation, and extreme temperatures
- **Heads-Up Display (HUD)**: Tactical information, target tracking, and sensor data overlaid on visor
- **Enhanced Strength**: Servomotors provide +1 Strength for lifting and close combat
- **Limited Flight**: Maneuvering jets allow short bursts of flight or zero-G navigation
- **Communication Suite**: Encrypted quantum-link communicator with global range

The Light Hardsuit is typically deployed for Border Corps Division missions, extraplanetary security operations, and rapid response scenarios. The armor's matte black finish incorporates stealth materials that reduce visual and sensor signatures.

Donning the suit requires 2 minutes with assistance or 5 minutes alone. The suit's Quintessence reserve (25 points) powers all systems, with typical deployment consuming 1-2 points per hour of active use.""",
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Alanson R-25 Hardsuit",
    background_cost=5,
    arete=4,
    quintessence_max=20,
    description="""The Alanson R-25 Hardsuit is the premier combat armor used by Void Engineer operatives who expect heavy resistance. Substantially more robust than the Light Hardsuit, the R-25 provides maximum protection while maintaining the technological sophistication expected of Enlightened Science.

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

The R-25 saw extensive use during the Dimensional Anomaly campaigns of the late 1990s and proved particularly effective against Nephandi incursions. Captain Chen Zhang of the London Border Corps is known to favor this model.""",
)[0]
Artifact.objects.get_or_create(display=False, name="Alley Shades", background_cost=2)
Talisman.objects.get_or_create(
    display=False, name="Anti-Gerasone", background_cost=8, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(
    display=False, name="Aole Koheoheo Tatu", background_cost=4
)
Talisman.objects.get_or_create(
    display=False, name="Arachne's Web", background_cost=9, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False, name="ARC-2", background_cost=12, arete=7, quintessence_max=35
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Armor of Achilles",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Artificer's Badger",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Assassin's Blade", background_cost=8
)
Artifact.objects.get_or_create(display=False, name="Astral Tiki", background_cost=2)
Talisman.objects.get_or_create(
    display=False, name="AUAV", background_cost=10, arete=7, quintessence_max=35
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Aurora Transatmospheric Fighter",
    background_cost=13,
    arete=8,
    quintessence_max=40,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Auspicious Sistrum",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Bafflejack", background_cost=2, arete=2, quintessence_max=10
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Bangles of Infinite Acceptance",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Barrel Improvements", background_cost=2
)
Talisman.objects.get_or_create(
    display=False,
    name="Barrier Field Generator (BFG)",
    background_cost=7,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Battle Homunculus",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(display=False, name="Beast Cloak", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Bilateral Pattern-Fusion Suit",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Bio-Cloaking", background_cost=6, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False, name="Bio-Printer", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Biological Dislocator",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="Biomesh Armor", background_cost=2)
Talisman.objects.get_or_create(
    display=False, name="BioSpy", background_cost=6, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(
    display=False, name="Biotemporal Maintenance Field Generator", background_cost=8
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Bird of Reason",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Bird Staff of Osanyin", background_cost=6
)
Talisman.objects.get_or_create(
    display=False,
    name="Black Helicopters",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Blade-Blaster Brand Rocket Blades",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Blast Pistol", background_cost=7, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Block Party Videos",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Blood Kris", background_cost=8, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Body-Forger's Arm",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Bolingbroke's Cathedra",
    background_cost=0,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Bond Fine Tobacco Products",
    background_cost=6,
    arete=4,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Bone Spurs", background_cost=6, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(display=False, name="Bottle of Fire", background_cost=8)
Artifact.objects.get_or_create(
    display=False, name="Branch of the World Tree", background_cost=4
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Brittany's Music Box",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Bulletproof Hoodie", background_cost=6
)
Artifact.objects.get_or_create(display=False, name="Bullroarer", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Cardio-Muscular Assemblage",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Carte Blanche", background_cost=7, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Cascade 23 Laser Pistol",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Cauldron of Spies", background_cost=6
)
Talisman.objects.get_or_create(
    display=False, name="Cephalic VCR", background_cost=9, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Chango's Blade",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Chatter Bomb", background_cost=10, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False, name="CHIRP Card", background_cost=6, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False, name="Chirp Node", background_cost=8, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False, name="Chitin", background_cost=6, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(display=False, name="Claws", background_cost=4)
Artifact.objects.get_or_create(display=False, name="Clay Man Amulet", background_cost=5)
Talisman.objects.get_or_create(
    display=False, name="Clockers", background_cost=7, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Clockwork Sycamore",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Cloning Devices",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(display=False, name="Clout Perfume", background_cost=2)
Artifact.objects.get_or_create(
    display=False, name="Cloë the Growl-Growl Bear", background_cost=3
)[0]
Talisman.objects.get_or_create(
    display=False, name="CMAP", background_cost=5, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False, name="Coco Macaque", background_cost=8, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(display=False, name="Codex Mendoza", background_cost=0)
Artifact.objects.get_or_create(
    display=False, name="Coding Tunes, Vol I", background_cost=2
)
Talisman.objects.get_or_create(
    display=False,
    name="Communications Jammer",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Consensual Hallucination Generator",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Cord of the Three Winds",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Corporate Raider Jet",
    background_cost=12,
    arete=7,
    quintessence_max=35,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Correlli's Badass Jackhammer",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Cosmic Communications Package",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Craftmason Pistol",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Creation Engine",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Daedalean Passages",
    background_cost=9,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False, name="DCMDs", background_cost=1, arete=1, quintessence_max=5
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Deep Space Combat Armor",
    background_cost=12,
    arete=7,
    quintessence_max=35,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Demon Mask", background_cost=6, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(display=False, name="Detox Implant", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Deviant's Heart",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Devil-Chaser Whip",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Dharma Bomb/Apple of Discord", background_cost=2
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Diana's Arrows",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Digital Dollz", background_cost=8, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Digital Drill",
    background_cost=10,
    arete=8,
    quintessence_max=40,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Digital Enhancement Implants", background_cost=8
)[0]
Artifact.objects.get_or_create(
    display=False, name="Digital Interface Armband", background_cost=6
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Digital Online Package",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Dimension Phase Disruption Emitter (DPDE)", background_cost=6
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Dimensional Sensory Unit",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Dirty Bomb", background_cost=10, arete=6, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False, name="Disguise Hat", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Distance Vision",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="Divining Staff", background_cost=4)
Artifact.objects.get_or_create(
    display=False, name="Doc Eon's Action Jackets", background_cost=0
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Doc Eon's Gas Bullets",
    background_cost=3,
    arete=3,
    quintessence_max=0,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Doc Eon's Lemurian Lightning Gun",
    background_cost=0,
    arete=5,
    quintessence_max=0,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Doc Eon's Time Watch",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Dogon Divination Bowl", background_cost=2
)
Artifact.objects.get_or_create(display=False, name="Dormancy Tiki", background_cost=8)
Talisman.objects.get_or_create(
    display=False,
    name="Dr. Day's Hypodermic",
    background_cost=0,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Dr. Reuter's Jewel of Inspiration", background_cost=3
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Dr. Wingbat's Ether jet Rocketpack",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Dr. Worvil's Wand",
    background_cost=0,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="Dream Gate", background_cost=10)
Artifact.objects.get_or_create(
    display=False, name="Dream Spirit Bag", background_cost=6
)
Talisman.objects.get_or_create(
    display=False,
    name="Ear of Dionysus",
    background_cost=3,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Ebon Candles of Manifest Nigrescence", background_cost=4
)[0]
Artifact.objects.get_or_create(
    display=False, name="Ectoplasmic Disruption Rounds", background_cost=3
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Ectoplasmic Disruptor Cannon (EDC)",
    background_cost=9,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(
    display=False, name="EDG Virtuous Executive Smartphone", background_cost=4
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Electroephemeral Scanner",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Electropulse Hand",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="ELMART", background_cost=8, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(display=False, name="EMP Grenade", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Encephalographic Probe",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Endless Ammo Clips",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(display=False, name="Energy Drinks", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Energy Enhancement Module",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Enhanced Pheromones", background_cost=1
)
Talisman.objects.get_or_create(
    display=False,
    name="Enlightened Smartphone",
    background_cost=0,
    arete=1,
    quintessence_max=1,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Environmental Sustainability Adjustment", background_cost=3
)[0]
Artifact.objects.get_or_create(
    display=False, name="Ether Tracking Clockwork Wonder Globe", background_cost=8
)[0]
Artifact.objects.get_or_create(
    display=False, name="Exo-Musculature and Exo-Skeletons", background_cost=6
)[0]
Talisman.objects.get_or_create(
    display=False, name="Exoskeleton", background_cost=9, arete=6, quintessence_max=30
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Extraction Device",
    background_cost=10,
    arete=6,
    quintessence_max=30,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Extrasensory Access", background_cost=2
)
Talisman.objects.get_or_create(
    display=False,
    name="E/E, Personal Cloaking Device",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Facial Reconstruction", background_cost=2
)
Talisman.objects.get_or_create(
    display=False, name="Faerie Cap", background_cost=5, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(
    display=False,
    name="Falconi and Associates Elite Business Attire",
    background_cost=4,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Fan of Kang Wu",
    background_cost=8,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(display=False, name="Fencing Square", background_cost=4)
Artifact.objects.get_or_create(display=False, name="Fertility Tiki", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Fireball Pearl",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Fishbowl of Prosperity", background_cost=4
)
Talisman.objects.get_or_create(
    display=False,
    name="Five-Fire Stone",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Fix-Sea Staff", background_cost=4, arete=2, quintessence_max=10
)[0]
Talisman.objects.get_or_create(
    display=False, name="Flesh Canvas", background_cost=6, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(display=False, name="Floating Oil", background_cost=4)
Artifact.objects.get_or_create(display=False, name="Flying Unguent", background_cost=3)
Talisman.objects.get_or_create(
    display=False,
    name="Folding Gate of Armaghast",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(display=False, name="Foot Pads", background_cost=2)
Artifact.objects.get_or_create(display=False, name="Fortune Tiki", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Fractal Symphonies",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name='G42 "Raptor" Vibroblades',
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="General Prosthetic Tools",
    background_cost=3,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Ghost-Devouring Jack-o'-Lantern", background_cost=2
)[0]
Artifact.objects.get_or_create(display=False, name="Gills", background_cost=4)
Artifact.objects.get_or_create(display=False, name="Ginger Dragons", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Girdle of Hippolyta",
    background_cost=0,
    arete=6,
    quintessence_max=30,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Glasses of Speed Reading",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="GODSPIN Blotter Acid", background_cost=4
)
Talisman.objects.get_or_create(
    display=False, name="Golden Bands", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False, name="Golden Walnut", background_cost=5, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(
    display=False, name="Great Sigil Pendant", background_cost=4
)
Talisman.objects.get_or_create(
    display=False,
    name="Green Dome Manar",
    background_cost=5,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="Guardian Tiki", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Gun for the Job",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Hail of Division",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Half Inch Deck",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Hand of Glory", background_cost=9, arete=5, quintessence_max=25
)[0]
Artifact.objects.get_or_create(
    display=False, name="Hardsuit Modules", background_cost=1
)
Talisman.objects.get_or_create(
    display=False,
    name="Hare's-foot Ward",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Havoc Gun", background_cost=10, arete=7, quintessence_max=35
)[0]
Artifact.objects.get_or_create(
    display=False, name="Hazelnuts of Wisdom", background_cost=1
)
Artifact.objects.get_or_create(display=False, name="He'e Tatu", background_cost=4)
Artifact.objects.get_or_create(
    display=False, name="Healing Figurine", background_cost=4
)
Talisman.objects.get_or_create(
    display=False, name="HEAT Chip", background_cost=6, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(display=False, name="Hei", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Heihou no Sebrio The Samurai Suit",
    background_cost=0,
    arete=6,
    quintessence_max=30,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Heimdall V Leadstopper", background_cost=6
)
Artifact.objects.get_or_create(display=False, name="Helix Ring", background_cost=6)
Talisman.objects.get_or_create(
    display=False,
    name="Helm of Heimdall",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Hephaistos' Tables",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Herbal Plaster of the Ancients",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Hermes's Carriage",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Hidioshi Wearable Translator", background_cost=6
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Hiroshima Bone",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Holdout Compartment",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Holdout Weapons",
    background_cost=6,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Holocomputer", background_cost=2, arete=1, quintessence_max=5
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Holographic Projector",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="Holy Water", background_cost=0)
Talisman.objects.get_or_create(
    display=False,
    name="Horatius's Thunder",
    background_cost=8,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Horizon Gateway",
    background_cost=10,
    arete=6,
    quintessence_max=35,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Hot-Mach I Speedster",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="Hrunting", background_cost=8)
Artifact.objects.get_or_create(display=False, name="Huaca", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Huginn and Muninn Suppression Systems",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Hydrogen Battery", background_cost=5
)
Talisman.objects.get_or_create(
    display=False,
    name="Hypermed Injection System",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Hypersynaptic Reaction System",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="Iago's Mask", background_cost=10)
Talisman.objects.get_or_create(
    display=False, name="ICOE", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Identification",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(display=False, name="Impact Armor", background_cost=4)
Talisman.objects.get_or_create(
    display=False, name="iMPALA", background_cost=4, arete=2, quintessence_max=10
)[0]
Artifact.objects.get_or_create(display=False, name="Imperial Tiger", background_cost=0)
Talisman.objects.get_or_create(
    display=False,
    name="Implant Chain Gun",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="Implant Radio", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Implanted Plasma Cannon",
    background_cost=9,
    arete=6,
    quintessence_max=30,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Infinite Change Purse", background_cost=4
)
Artifact.objects.get_or_create(display=False, name="Info Spider", background_cost=6)
Artifact.objects.get_or_create(display=False, name="Inform-a-Vision", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Infravision Receptors",
    background_cost=3,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(display=False, name="Inhabited Car", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Innovation, Inc.'s Personal Lift Generator 5000",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Invisible Explosive",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="Ionic Cloth", background_cost=0)
Talisman.objects.get_or_create(
    display=False,
    name="Ionic Disruptor",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Iron Kraken", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False, name="Iron Lung", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False,
    name='Iteration MP-0 "Penetrator"',
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="Ixos Acid", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Jagg'd Blade of Rending",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Jangler Pod", background_cost=10, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Jonah's Chariot",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Juk Ak", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False, name="Jump Box", background_cost=8, arete=5, quintessence_max=25
)[0]
Artifact.objects.get_or_create(display=False, name="Justice Blades", background_cost=3)
Artifact.objects.get_or_create(
    display=False, name="Kahu Huruhuru (Feather Cloak)", background_cost=4
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Kaleidoscopic REM Suit",
    background_cost=5,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="Keypads", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Khalil aba-Malek, The Iron Satan",
    background_cost=0,
    arete=8,
    quintessence_max=0,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Kid Kimota's Jovian Thundergloves",
    background_cost=9,
    arete=6,
    quintessence_max=30,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Kinetic Legs", background_cost=5, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Kinetic Transfer Safeguard (KTS)",
    background_cost=7,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(display=False, name="Kismet Bindi", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Komo-ho'ali'i's Gift",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="KROM Module", background_cost=4)
Talisman.objects.get_or_create(
    display=False, name="Lab Assistant", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Lady Wudlowe's Menhirs",
    background_cost=0,
    arete=5,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Lash of Passion",
    background_cost=10,
    arete=6,
    quintessence_max=30,
)[0]
Artifact.objects.get_or_create(display=False, name="Lawai'a Tatu", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Lazarus Transmitter",
    background_cost=10,
    arete=10,
    quintessence_max=50,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Leadstopper Vest", background_cost=6
)
Talisman.objects.get_or_create(
    display=False,
    name="Leng Chao's Chamber of Yin-Yang",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Lethe's Spheres",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Liber Tenebris Distalis", background_cost=6
)[0]
Talisman.objects.get_or_create(
    display=False, name="Light Meter", background_cost=5, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(
    display=False, name="Lighter-Than-Air Masticated Conveyance Gel", background_cost=3
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Limitless Bow",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(display=False, name="Link Collar", background_cost=6)
Talisman.objects.get_or_create(
    display=False,
    name="Lon McAin's Cool Shoes",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(display=False, name="Looking Glass", background_cost=4)
Talisman.objects.get_or_create(
    display=False, name="Lucky Coin", background_cost=5, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(display=False, name="Lustral Water", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Lycanthroscope",
    background_cost=4,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Mad Fiddles of Dr. Mercer",
    background_cost=6,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Mad Mook's Million Eyes on the World",
    background_cost=3,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Madam Xanadu's All-Seeing Fortune Machine", background_cost=4
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Madness Grenade",
    background_cost=10,
    arete=7,
    quintessence_max=0,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Magick Sword Coin",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Magickal Macro Keyboard",
    background_cost=11,
    arete=7,
    quintessence_max=35,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Magnatronic III VASP Computer",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Magnifying Glass",
    background_cost=2,
    arete=1,
    quintessence_max=5,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Manar Scanner", background_cost=3, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(display=False, name="Mapping Implant", background_cost=2)
Artifact.objects.get_or_create(
    display=False, name="Mark IV Hand Computer", background_cost=1
)
Artifact.objects.get_or_create(
    display=False, name="Mark VII Cassini AUC", background_cost=0
)
Talisman.objects.get_or_create(
    display=False,
    name="Martian Purifier",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Martinez Robust Hardsuit",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Mask of Silent Death",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Mask of the Warrior", background_cost=4
)
Artifact.objects.get_or_create(
    display=False, name="Master Joro's Sash", background_cost=6
)
Talisman.objects.get_or_create(
    display=False, name="Master Remote", background_cost=6, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Matter Transmission Portal",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Med Pack", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False, name="Medi-Bot", background_cost=7, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(display=False, name="Medicine Bag", background_cost=2)
Talisman.objects.get_or_create(
    display=False, name="MEGA Pen", background_cost=0, arete=5, quintessence_max=30
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Mental Enhancement Glasses",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Michael Durmstrang's Creepy-Ass China Doll", background_cost=5
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Micro Tool Kit",
    background_cost=3,
    arete=1,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(display=False, name="Micro-RPV", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Micron Light Cycle",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="MIDAS Card", background_cost=0)
Talisman.objects.get_or_create(
    display=False, name="Mirrorshades", background_cost=3, arete=2, quintessence_max=10
)[0]
Artifact.objects.get_or_create(
    display=False, name="Mjollnir Handguns", background_cost=6
)
Talisman.objects.get_or_create(
    display=False, name="Mobile Home", background_cost=8, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(display=False, name="Mokomai", background_cost=6)
Talisman.objects.get_or_create(
    display=False,
    name="Molecular Phone",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Mu-Jen", background_cost=8, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(
    display=False, name="Multi-Purpose Computer Implant", background_cost=3
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Multi-Terrain Explorer",
    background_cost=11,
    arete=6,
    quintessence_max=30,
)[0]
Artifact.objects.get_or_create(display=False, name="Nanopatch", background_cost=2)
Artifact.objects.get_or_create(
    display=False, name="Nanotech Medichines", background_cost=6
)
Talisman.objects.get_or_create(
    display=False, name="Nanovaccine", background_cost=4, arete=2, quintessence_max=10
)[0]
Talisman.objects.get_or_create(
    display=False, name="Net Gear", background_cost=9, arete=5, quintessence_max=25
)[0]
Artifact.objects.get_or_create(display=False, name="Night Eyes", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Nightmare Field Generator",
    background_cost=6,
    arete=3,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Nine Jade Dragons", background_cost=5
)
Talisman.objects.get_or_create(
    display=False,
    name="Nine-Dragon Tattoos",
    background_cost=9,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Node Seekers", background_cost=5, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Non-Puncturing Injector",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Nondescript Van",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Nothing to See Here",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="NSN Plasma Caster",
    background_cost=10,
    arete=6,
    quintessence_max=30,
)[0]
Artifact.objects.get_or_create(display=False, name="Nuclear Bomb", background_cost=20)
Artifact.objects.get_or_create(
    display=False, name="Oho-Kui (Battle Wig)", background_cost=6
)
Talisman.objects.get_or_create(
    display=False,
    name="Omnichronal Watch",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(display=False, name="Online Access", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Orbital Manar Station",
    background_cost=6,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(display=False, name="Organic Knife", background_cost=6)
Talisman.objects.get_or_create(
    display=False,
    name="Oriole of Tranquility",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Orrery of Madame des Bellestours", background_cost=0
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="P22 Gauss Needler",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="Pahu Ino-Nui", background_cost=10)
Talisman.objects.get_or_create(
    display=False, name="Paladin Sedan", background_cost=8, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Panoramic Surveillance Node",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(display=False, name="Paradox Stone", background_cost=5)
Talisman.objects.get_or_create(
    display=False, name="Parking Karma", background_cost=4, arete=2, quintessence_max=10
)[0]
Artifact.objects.get_or_create(display=False, name="Passion Tiki", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Pattern-Ripping Claws",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="PDNA", background_cost=9, arete=5, quintessence_max=25
)[0]
Artifact.objects.get_or_create(display=False, name="Peacemaker", background_cost=8)
Talisman.objects.get_or_create(
    display=False, name="Pele's Lamaku", background_cost=6, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(display=False, name="Penance Bonds", background_cost=0)
Artifact.objects.get_or_create(display=False, name="Perfected Focus", background_cost=1)
Talisman.objects.get_or_create(
    display=False,
    name="Performance Blade",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Perimeter Alarm",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Personal Cerebral Translation Unit",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Personality Software", background_cost=8
)
Artifact.objects.get_or_create(
    display=False, name="Physical Structure Enhancement", background_cost=2
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Physical Transfer Unit or Suit",
    background_cost=10,
    arete=6,
    quintessence_max=30,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Physiognomizer",
    background_cost=0,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Pincer Tool", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="PKD Paranoia Amplifier",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="PlastiSkin", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False, name="Plutonium Pill", background_cost=3, arete=3, quintessence_max=0
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Pluvius' Javelinman",
    background_cost=12,
    arete=7,
    quintessence_max=35,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Pneumatic Arm", background_cost=9, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Pocket Poltergeist",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Portable Manar", background_cost=2, arete=1, quintessence_max=5
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Portable Virtual Reality System",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Power Suit", background_cost=4, arete=2, quintessence_max=10
)[0]
Talisman.objects.get_or_create(
    display=False, name="Prayer Beads", background_cost=6, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Predator's Pheromones",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Prehensile Tail",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False, name="PRETI gun", background_cost=8, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Primium Blade",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Primium Countermeasures", background_cost=4
)[0]
Talisman.objects.get_or_create(
    display=False, name="Primium Cuffs", background_cost=3, arete=2, quintessence_max=10
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Primium Knuckles",
    background_cost=2,
    arete=1,
    quintessence_max=5,
)[0]
Artifact.objects.get_or_create(
    display=False, name="procedure.rand.enlight/40.4292.18.23.c", background_cost=6
)[0]
Artifact.objects.get_or_create(display=False, name="Prodigy", background_cost=1)
Talisman.objects.get_or_create(
    display=False,
    name="Professor Parallax's Displacement Device",
    background_cost=11,
    arete=6,
    quintessence_max=30,
)[0]
Artifact.objects.get_or_create(display=False, name="Prophetic Skull", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Protocol Beeper",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Qi Needler", background_cost=7, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Quad-Leg System",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Quantum Datacaster",
    background_cost=8,
    arete=6,
    quintessence_max=30,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Quantum Field Inverter (QFI)",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Quantum Monitor",
    background_cost=3,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(display=False, name="QUEST Transport", background_cost=0)
Artifact.objects.get_or_create(
    display=False, name="Qui La Machinae X156", background_cost=0
)
Artifact.objects.get_or_create(
    display=False, name="Qui La Machinae X160", background_cost=40
)
Artifact.objects.get_or_create(
    display=False, name="Qui La Machinae X200 “Vader”", background_cost=0
)[0]
Artifact.objects.get_or_create(
    display=False, name="Quintessence Absorbing Device (QAD)", background_cost=8
)[0]
Artifact.objects.get_or_create(
    display=False, name="Radical Pigment Alteration", background_cost=4
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Rapid Text Stream Data Reader",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="Raptor Silencer", background_cost=2)
Artifact.objects.get_or_create(display=False, name="Ravana's Skin", background_cost=7)
Talisman.objects.get_or_create(
    display=False,
    name="Reality Modulation Units (RMU)",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(display=False, name="Rebreather", background_cost=4)
Artifact.objects.get_or_create(
    display=False, name="Remote Piloted Vehicle", background_cost=4
)
Talisman.objects.get_or_create(
    display=False,
    name="Remote Sensors",
    background_cost=7,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Retinal Encoding Organism (RetEncO)",
    background_cost=0,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Rimbaud's Recipe for Sacred Absinthe", background_cost=4
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Robes of Blessing",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Rocket Chariot",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Rod of Holy Cleansing",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="Sacred Bullhide", background_cost=4)
Artifact.objects.get_or_create(display=False, name="Salvation Bell", background_cost=6)
Artifact.objects.get_or_create(display=False, name="Sampo Fragments", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Samson's Gauntlets",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Schrödinger's Closet",
    background_cost=8,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Scout Drone", background_cost=6, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(
    display=False, name="Sea Spirit Shell", background_cost=3
)
Artifact.objects.get_or_create(display=False, name="Seeds of Decay", background_cost=10)
Talisman.objects.get_or_create(
    display=False, name="Seekers", background_cost=8, arete=6, quintessence_max=30
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Selective Mine",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Senex's Blade",
    background_cost=12,
    arete=6,
    quintessence_max=30,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Sense Amplifiers",
    background_cost=2,
    arete=1,
    quintessence_max=5,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Sense Recorders",
    background_cost=2,
    arete=1,
    quintessence_max=5,
)[0]
Artifact.objects.get_or_create(display=False, name="Sensor Glasses", background_cost=2)
Talisman.objects.get_or_create(
    display=False, name="Sensor Organ", background_cost=3, arete=2, quintessence_max=10
)[0]
Artifact.objects.get_or_create(
    display=False, name="Sensory Enhancers", background_cost=3
)
Artifact.objects.get_or_create(
    display=False, name="Sentinel Satellite", background_cost=0
)
Talisman.objects.get_or_create(
    display=False, name="Serpent Blade", background_cost=4, arete=2, quintessence_max=10
)[0]
Artifact.objects.get_or_create(display=False, name="Serpent Pen", background_cost=8)
Talisman.objects.get_or_create(
    display=False,
    name="Seven-Precious Branch",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Shan Tattoo of Undisciplined Strength",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Shapeshifting", background_cost=8, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False, name="Shattered Lens", background_cost=2, arete=1, quintessence_max=5
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Shifter's Skin",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Shocker", background_cost=7, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Shotgun Microphone",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Shuriken Glove",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Silver Fan", background_cost=8, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(display=False, name="Silver Strand", background_cost=6)
Talisman.objects.get_or_create(
    display=False, name="Sin-TV", background_cost=5, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(display=False, name="Siren's Scent", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Siren's Tears and the Breather Collar",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Skeletal Enhancement", background_cost=2
)
Artifact.objects.get_or_create(display=False, name="SkinSuits", background_cost=10)
Talisman.objects.get_or_create(
    display=False, name="Skyrigger", background_cost=10, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False, name="Sleepteacher", background_cost=8, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Sleepwalker's Drum",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Slip-Rex, The King of Lubricants", background_cost=4
)[0]
Artifact.objects.get_or_create(display=False, name="Sorcerous Tiki", background_cost=4)
Artifact.objects.get_or_create(display=False, name="Soul Mates", background_cost=0)
Artifact.objects.get_or_create(display=False, name="Space Jam", background_cost=4)
Artifact.objects.get_or_create(
    display=False, name="Spear of Gobhniu", background_cost=8
)
Artifact.objects.get_or_create(display=False, name="SPECM", background_cost=5)
Talisman.objects.get_or_create(
    display=False,
    name="Spectre Limousine",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Spirit Door", background_cost=8, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Spirit Goggles",
    background_cost=4,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Spiritual Armor", background_cost=10
)
Artifact.objects.get_or_create(
    display=False, name="Spiritus Pastille", background_cost=4
)
Artifact.objects.get_or_create(display=False, name="Spy-Glass", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Stage II Power Glove",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="STAR Units", background_cost=10, arete=5, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False, name="Stealth Suit", background_cost=6, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False, name="Styx Armor", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False, name="Sub-Dermals", background_cost=6, arete=3, quintessence_max=15
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Subdermal Transponder",
    background_cost=2,
    arete=1,
    quintessence_max=0,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Subliminal Broadcaster", background_cost=4
)
Artifact.objects.get_or_create(
    display=False, name="Submersible Car", background_cost=10
)
Artifact.objects.get_or_create(display=False, name="Super-Steroids", background_cost=3)
Artifact.objects.get_or_create(
    display=False, name="Sword of Discharge", background_cost=4
)
Talisman.objects.get_or_create(
    display=False, name="Sword-Breaker", background_cost=4, arete=2, quintessence_max=10
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Swords of Mars",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Syringe Pharmacopeia", background_cost=4
)
Talisman.objects.get_or_create(
    display=False,
    name="Talisman of the Mask",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="Tass Tapes", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Tass-Powered Propulsion Units (TPUs)",
    background_cost=10,
    arete=6,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(
    display=False, name='TDR "Living" Computer and Video Games', background_cost=0
)[0]
Talisman.objects.get_or_create(
    display=False, name="TDSPV", background_cost=10, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Telepathy Specs",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Telescoping Limb",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Tempest Hardening",
    background_cost=6,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Temporal Transit Converter (TTC)",
    background_cost=11,
    arete=6,
    quintessence_max=30,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Adze Unparalleled",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Aether Codex", background_cost=4
)
Talisman.objects.get_or_create(
    display=False,
    name="The Alchemy of Unity",
    background_cost=0,
    arete=6,
    quintessence_max=0,
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Asklepian Tractate", background_cost=6
)
Artifact.objects.get_or_create(display=False, name="The Bioroid Eva", background_cost=0)
Artifact.objects.get_or_create(display=False, name="The Black Bible", background_cost=4)
Artifact.objects.get_or_create(
    display=False, name="The Black Book of Manu", background_cost=4
)
Talisman.objects.get_or_create(
    display=False,
    name="The Black Cauldron",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Black Rat's Rats",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Bond of ibn Daud", background_cost=3
)
Talisman.objects.get_or_create(
    display=False,
    name="The Bond Watch",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Book of Shadows of Maeve McKinnon", background_cost=6
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Chains of Leviathan", background_cost=7
)[0]
Talisman.objects.get_or_create(
    display=False, name="The Chopper", background_cost=10, arete=5, quintessence_max=25
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Cloud Dance of Eternal Vision and Joy", background_cost=6
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Codex Licentia", background_cost=4
)
Talisman.objects.get_or_create(
    display=False, name="The DDGR Card", background_cost=7, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Deadly Warbots of Doctor van Allmen",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Dithyramb of the Maenad Melanippe", background_cost=8
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Divine Staff of Fortuitous Intervention", background_cost=4
)[0]
Artifact.objects.get_or_create(display=False, name="The DoCo", background_cost=0)
Talisman.objects.get_or_create(
    display=False,
    name="The Emperor's Songbird",
    background_cost=10,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Espiritus Mini-Vac",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Fiberopticon",
    background_cost=12,
    arete=8,
    quintessence_max=40,
)[0]
Artifact.objects.get_or_create(display=False, name="The Filth Altar", background_cost=5)
Artifact.objects.get_or_create(
    display=False, name="The Greater Key of Solomon", background_cost=4
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Grimoire of Honorius", background_cost=4
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Grimorium Verum", background_cost=4
)
Artifact.objects.get_or_create(
    display=False, name="The Guitar of the Spirits", background_cost=8
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Hammer of Charun", background_cost=10
)
Talisman.objects.get_or_create(
    display=False,
    name="The Hyperphoto Zoom Lens with Spirit Film",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Infernal Mole-Blower",
    background_cost=6,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="The Lemegeton", background_cost=4)
Artifact.objects.get_or_create(
    display=False, name="The Lens of Zadkiel", background_cost=4
)
Artifact.objects.get_or_create(
    display=False, name="The Liber Labyrinthus", background_cost=4
)
Artifact.objects.get_or_create(
    display=False, name="The Liber Spiritum", background_cost=4
)
Artifact.objects.get_or_create(display=False, name="The Mask Maker", background_cost=2)
Artifact.objects.get_or_create(
    display=False, name="The Masquer's Grand Disguise", background_cost=6
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Mirror of Penthesilea",
    background_cost=0,
    arete=6,
    quintessence_max=30,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Orb of Honorius",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Piacenza Liver", background_cost=2
)
Talisman.objects.get_or_create(
    display=False,
    name="The Purifier's Needles",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The R.U.N.T.I.S. Suit",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Ragnaroc Home Security System",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Rebooter Self-Retrieval Bio-Printer",
    background_cost=0,
    arete=8,
    quintessence_max=40,
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Recorder's Heavenly Scroll", background_cost=4
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Robes of the Golden Mandarin", background_cost=0
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Sebel-el-Mafouh Whash", background_cost=4
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Second Key of Ablamerch", background_cost=4
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Six Seals of Ganzir", background_cost=4
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Sorcerer's Apprentice", background_cost=8
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Spirit Chant of Upopotak", background_cost=2
)[0]
Artifact.objects.get_or_create(
    display=False, name="The Staff of Heralds", background_cost=0
)
Artifact.objects.get_or_create(
    display=False, name="The Temple of the Theoi Cthon", background_cost=8
)[0]
Artifact.objects.get_or_create(display=False, name="The Tenth Seat", background_cost=0)
Talisman.objects.get_or_create(
    display=False,
    name="The Testing Flask",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The Thief's Claw",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="The Twins", background_cost=0)
Artifact.objects.get_or_create(
    display=False, name="The Uranian Pleasure Manual", background_cost=10
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="The War Machine",
    background_cost=0,
    arete=6,
    quintessence_max=30,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Theresita's Thousand Magick-Finger Bed",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Thirsty Blade of Kali",
    background_cost=11,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="THOMAS Combat Systems",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Thought Programs",
    background_cost=2,
    arete=1,
    quintessence_max=5,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Thought Transference Device",
    background_cost=10,
    arete=6,
    quintessence_max=30,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Three Pearls of Thunder and Lightning",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Tide Jewel", background_cost=10, arete=5, quintessence_max=25
)[0]
Artifact.objects.get_or_create(display=False, name="Time-Divider", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="Titan's Armor, or Saint George's Plate",
    background_cost=8,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Tonics and Potions", background_cost=3
)
Artifact.objects.get_or_create(display=False, name="Torc of Donn", background_cost=8)
Talisman.objects.get_or_create(
    display=False, name="Totem Tattoo", background_cost=8, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(
    display=False, name="Tradition Blades", background_cost=10
)
Artifact.objects.get_or_create(display=False, name="Trance Drum", background_cost=4)
Artifact.objects.get_or_create(
    display=False, name="Tranquility Raptor Class Corvette", background_cost=18
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Transport Pass Card",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Traveler's Charm", background_cost=2
)
Artifact.objects.get_or_create(display=False, name="Traveling Coat", background_cost=4)
Talisman.objects.get_or_create(
    display=False, name="Trollhide", background_cost=9, arete=5, quintessence_max=25
)[0]
Artifact.objects.get_or_create(display=False, name="Trushades", background_cost=2)
Talisman.objects.get_or_create(
    display=False, name="Truth Serum", background_cost=4, arete=2, quintessence_max=10
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Truth-Seeing Stone",
    background_cost=2,
    arete=1,
    quintessence_max=5,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Tsu-Ti (Divine Bamboo)",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Tsukahara Shigekatsu's August Mirror",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="Twilight Balm", background_cost=4)
Talisman.objects.get_or_create(
    display=False, name="TWURP", background_cost=9, arete=5, quintessence_max=25
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Ultra-Silencer",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(display=False, name="Unbullets", background_cost=3)
Talisman.objects.get_or_create(
    display=False,
    name="Undead Strength",
    background_cost=7,
    arete=4,
    quintessence_max=20,
)[0]
Artifact.objects.get_or_create(display=False, name="UniCash Card", background_cost=6)
Artifact.objects.get_or_create(display=False, name="Universal ID", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Universal Identification Card Kit",
    background_cost=5,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Universal Nanotech Interface", background_cost=4
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Universal Suit",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="UNIVID", background_cost=6, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Unstoppable Binoculars",
    background_cost=3,
    arete=2,
    quintessence_max=10,
)[0]
Talisman.objects.get_or_create(
    display=False, name="USAC", background_cost=6, arete=4, quintessence_max=20
)[0]
Artifact.objects.get_or_create(display=False, name="Usurer's Purse", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Vap'rous Candles of Lethe",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="VBC-3 Bio-Computer and Mind-Link XF251",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Vehicular Manar",
    background_cost=4,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Vehicular Satellite Uplink", background_cost=4
)[0]
Artifact.objects.get_or_create(
    display=False, name="Vending Machines (Chi Restoration)", background_cost=0
)[0]
Artifact.objects.get_or_create(display=False, name="Vengeance Blade", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Verrecchia's Marvelous Lions",
    background_cost=0,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Viasilicos", background_cost=8, arete=6, quintessence_max=30
)[0]
Talisman.objects.get_or_create(
    display=False, name="Vision Jewel", background_cost=4, arete=2, quintessence_max=10
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Visual Data & Analysis Spectrum (VDAS)",
    background_cost=6,
    arete=3,
    quintessence_max=0,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Voice Disguiser",
    background_cost=4,
    arete=2,
    quintessence_max=10,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Void Engine Shuttlecraft", background_cost=3
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Void Engineer Light Environment Suit",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Vrum Vrum Boom",
    background_cost=0,
    arete=6,
    quintessence_max=30,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Wand of Health", background_cost=6, arete=4, quintessence_max=0
)[0]
Artifact.objects.get_or_create(display=False, name="War Tiki", background_cost=2)
Artifact.objects.get_or_create(display=False, name="Ward Tiki", background_cost=4)
Artifact.objects.get_or_create(display=False, name="Warware", background_cost=2)
Artifact.objects.get_or_create(display=False, name="WatchCom", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Whispering Stone",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Wings of Icarus",
    background_cost=9,
    arete=5,
    quintessence_max=25,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Wired", background_cost=2, arete=1, quintessence_max=2
)[0]
Talisman.objects.get_or_create(
    display=False, name="Witchward", background_cost=4, arete=2, quintessence_max=10
)[0]
Talisman.objects.get_or_create(
    display=False, name="Wolf Link", background_cost=8, arete=4, quintessence_max=20
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Wolf-Paw Amulet",
    background_cost=2,
    arete=5,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Woodblock of Auspicious Formulae",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Wound-Bearing Torc", background_cost=6
)
Artifact.objects.get_or_create(
    display=False, name="Wurnan Stick (Message Stick)", background_cost=4
)[0]
Artifact.objects.get_or_create(display=False, name="X-Ray Glasses", background_cost=2)
Talisman.objects.get_or_create(
    display=False,
    name="X117 Death Ray",
    background_cost=11,
    arete=8,
    quintessence_max=40,
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="X14 A Thunderhead",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Talisman.objects.get_or_create(
    display=False, name="Xenon Bulb", background_cost=6, arete=3, quintessence_max=15
)[0]
Artifact.objects.get_or_create(
    display=False, name="Yidaki (Didjeridu)", background_cost=2
)
Artifact.objects.get_or_create(display=False, name="Youth Drugs", background_cost=4)
Talisman.objects.get_or_create(
    display=False,
    name="Z488-C Video Data Retrieval System",
    background_cost=6,
    arete=3,
    quintessence_max=15,
)[0]
Artifact.objects.get_or_create(
    display=False, name="Zelly's Eternal Theatre", background_cost=0
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Zephraim Pincke's Automata Arcade",
    background_cost=0,
    arete=6,
    quintessence_max=30,
)[0]
Artifact.objects.get_or_create(display=False, name="Zulu Warshield", background_cost=2)


Artifact.objects.get_or_create(
    display=False,
    name="Dragon Pearls",
    background_cost=6,
    description="""These sacred pearls are treasured artifacts of the Akashic Brotherhood, serving as powerful Quintessence channeling conduits. Formed through decades of meditation and prime energy manipulation, each pearl contains crystallized enlightenment. The pearls glow with an inner light when filled with Quintessence, and skilled practitioners can draw upon this stored energy to fuel their magical workings. They are often worn as prayer beads or carried in silk pouches.""",
)[0].add_source("Lore of the Traditions", 35)
Artifact.objects.get_or_create(
    display=False,
    name="Angel Tear Daggers",
    quintessence_max=10,
    background_cost=7,
    description="""These paired daggers are forged from a mysterious crystalline substance said to be the solidified tears of angels. Whether this origin is literal or metaphorical, the daggers possess undeniable holy power. The translucent blades shimmer with an inner radiance, glowing softly in the presence of evil or infernal entities.

The Angel Tear Daggers are particularly prized by mages who hunt demons, Nephandi, and other creatures of darkness. Against such beings, the daggers deal aggravated damage and ignore certain forms of supernatural protection. The blades also provide a warning system - they glow more brightly as evil draws near, with intensity proportional to the threat level.

Each dagger deals Strength + 1 lethal damage normally, or Strength + 2 aggravated damage against infernal entities. The daggers can store up to 10 points of Quintessence and are often carried by Celestial Chorus members and other mages who battle dark forces. Legend holds that they were gifts from a repentant demon who wished to aid humanity's struggle against the Infernal.""",
)[0].add_source("Lore of the Traditions", 49)
Talisman.objects.get_or_create(
    display=False,
    name="Antaratma",
    arete=4,
    quintessence_max=10,
    background_cost=8,
    description="""The Antaratma is a sacred talisman of the Euthanatos Tradition, designed to protect the wielder from the madness of Quiet that can afflict mages who peer too deeply into the Wheel of Ages. Crafted through complex rituals involving Spirit, Mind, and Prime magicks, this talisman appears as an ornate silver medallion inscribed with Sanskrit mantras and symbols of the eternal wheel. When activated, it provides 1 level of Quiet resistance per 2 successes rolled on the user's Arete. Additionally, once per day, the Antaratma can provide a single Willpower point to fuel spellcasting, drawing on the stored spiritual energy within.""",
)[0].add_source("Lore of the Traditions", 98)

Artifact.objects.get_or_create(
    display=False,
    name="Game of Senet",
    background_cost=2,
    description="""The Game of Senet is an ancient Egyptian board game that predates most modern forms of divination. This particular set is more than just a game - it is a tool for reading fate and probability. The board is made of aged sycamore wood with squares of ivory and ebony, and the playing pieces are carved from semiprecious stones.

When two players engage in a proper ritual game of Senet, the movements of the pieces across the board trace the paths of probability and fate. Skilled practitioners can read these patterns to divine future events, understand the consequences of different choices, or identify opportune moments for action. The game requires at least one hour of focused play to produce meaningful divination results.

The Senet board also serves as a focus for Entropy magic, making it easier to manipulate probability or read the threads of fate. Some versions of the game are said to be gateways to the Duat (Egyptian underworld), allowing communication with the deceased or spirits of ancient Egypt.""",
)[0].add_source("Lore of the Traditions", 115)
Artifact.objects.get_or_create(
    display=False,
    name="Imphepho Wierook",
    quintessence_max=15,
    background_cost=3,
    description="""Imphepho (Helichrysum petiolare) is a sacred plant used in southern African traditional practices, particularly among the Xhosa and Zulu peoples. This specially prepared wierook (incense) has been blessed by Dreamspeaker shamans to enhance its natural spiritual properties.

When burned, the aromatic smoke of Imphepho creates a bridge between the physical and spirit worlds. The smoke carries prayers, requests, and offerings to the ancestors and spirits, while simultaneously inviting their presence and guidance into the ritual space. Practitioners often use Imphepho before important decisions, healing work, or when seeking ancestral wisdom.

The incense enhances spiritual perception, making it easier to sense the presence of spirits and receive their messages. It also provides a degree of protection, as malevolent spirits typically avoid the sacred smoke. A complete bundle provides enough Imphepho for approximately 10-15 ritual burnings. The incense can store up to 15 points of Quintessence and is particularly effective when combined with other Spirit-focused rituals.""",
)[0].add_source("Lore of the Traditions", 115)
Artifact.objects.get_or_create(
    display=False,
    name="Waidan Ding",
    quintessence_max=10,
    background_cost=5,
    description="""The Waidan Ding is a three-legged bronze cauldron used in Chinese external alchemy (waidan). This particular ding has been used in countless alchemical operations over centuries, absorbing magical resonance until it became a Wonder in its own right. The vessel is inscribed with Taoist trigrams and dragons, and it shows the patina of great age.

The ding serves as both container and catalyst for alchemical transmutations. When used in the creation of elixirs, talismans, or other alchemical products, it reduces the difficulty of the working and can improve the quality of the final product. The cauldron is particularly suited for:
- Creating medicinal elixirs and potions
- Transmuting base metals toward gold
- Purifying substances to reveal their quintessential nature
- Brewing longevity formulas
- Crafting alchemical Tass

The ding can store up to 10 points of Quintessence, which it draws from when aiding alchemical processes. Practitioners typically consecrate the vessel before each major working, and the greatest respect is shown when cleaning it, as the residue from past operations contributes to its power. This particular ding is associated with the Wu Lung tradition of Chinese sorcerers.""",
)[0].add_source("Lore of the Traditions", 115)

Talisman.objects.get_or_create(
    display=False,
    name="Dümerang Blade (2)",
    arete=2,
    background_cost=4,
    description="""This enchanted weapon appears as an elegant boomerang blade with Hermetic sigils etched along its curved edge. Created by the Order of Hermes, the Dümerang Blade is a masterwork of Forces and Correspondence magick that allows it to return unerringly to its wielder's hand after being thrown. The blade is perfectly balanced for both melee combat and ranged attacks.

The Dümerang Blade has an Arete rating of 2 which automatically regenerates each day, allowing the wielder to channel Quintessence through the weapon. When thrown, the blade traces an arc through the air, striking its target before curving back to the wielder's waiting hand. Masters of the blade can throw it through impossible trajectories, having it strike multiple opponents or navigate around obstacles.

The weapon deals Strength + 2 lethal damage in melee and Strength + 1 lethal damage when thrown (range 20 yards). Some versions of the blade were crafted as automotive ignition keys, with the pommel serving as a hood ornament when not in use.""",
)[0].add_source("Lore of the Traditions", 130)
Talisman.objects.get_or_create(
    display=False,
    name="Dümerang Blade (3)",
    arete=3,
    background_cost=8,
    description="""This enchanted weapon appears as an elegant boomerang blade with Hermetic sigils etched along its curved edge. Created by the Order of Hermes, the Dümerang Blade is a masterwork of Forces and Correspondence magick that allows it to return unerringly to its wielder's hand after being thrown. The blade is perfectly balanced for both melee combat and ranged attacks.

The Dümerang Blade has an Arete rating of 3 which automatically regenerates each day, allowing the wielder to channel Quintessence through the weapon. When thrown, the blade traces an arc through the air, striking its target before curving back to the wielder's waiting hand. Masters of the blade can throw it through impossible trajectories, having it strike multiple opponents or navigate around obstacles.

The weapon deals Strength + 2 lethal damage in melee and Strength + 1 lethal damage when thrown (range 20 yards). Some versions of the blade were crafted as automotive ignition keys, with the pommel serving as a hood ornament when not in use.""",
)[0].add_source("Lore of the Traditions", 130)
Talisman.objects.get_or_create(
    display=False,
    name="Dümerang Blade (4)",
    arete=4,
    background_cost=12,
    description="""This enchanted weapon appears as an elegant boomerang blade with Hermetic sigils etched along its curved edge. Created by the Order of Hermes, the Dümerang Blade is a masterwork of Forces and Correspondence magick that allows it to return unerringly to its wielder's hand after being thrown. The blade is perfectly balanced for both melee combat and ranged attacks.

The Dümerang Blade has an Arete rating of 4 which automatically regenerates each day, allowing the wielder to channel Quintessence through the weapon. When thrown, the blade traces an arc through the air, striking its target before curving back to the wielder's waiting hand. Masters of the blade can throw it through impossible trajectories, having it strike multiple opponents or navigate around obstacles.

The weapon deals Strength + 2 lethal damage in melee and Strength + 1 lethal damage when thrown (range 20 yards). Some versions of the blade were crafted as automotive ignition keys, with the pommel serving as a hood ornament when not in use.""",
)[0].add_source("Lore of the Traditions", 130)

Grimoire.objects.get_or_create(
    display=False, name="Kitab al-Alacir", rank=5, is_primer=True
)[0].add_source("Lore of the Traditions", 131)

Talisman.objects.get_or_create(
    display=False, name="The Last Caer", arete=5, quintessence_max=25
)[0].add_source("Lore of the Traditions", 131)

Talisman.objects.get_or_create(
    display=False,
    name="Candle of Communion (1)",
    arete=1,
    background_cost=2,
    quintessence_max=5,
    description="""A hand-crafted ritual candle, typically made from beeswax infused with sacred herbs and oils. The Candle of Communion is a staple tool among Verbena practitioners, particularly those who work with spirits and ancestors. When lit with proper ritual intent, the candle's flame becomes a beacon in both the physical world and the Umbra, opening channels of communication.

The candle (Arete 1) glows with an otherworldly light when activated, and spirits are drawn to its warmth. The practitioner can speak with entities across the Gauntlet, receive messages from ancestors, or even attract helpful spirits to aid in magical workings. The quality of communion depends on the candle's Arete rating - lower rated candles provide vaguer, more symbolic communication, while higher rated ones allow for clearer dialogue.

Each candle typically provides several hours of burn time, and master crafters can create candles with specific attunements to particular types of spirits or ancestors.""",
)[0].add_source("Lore of the Traditions", 146)
Talisman.objects.get_or_create(
    display=False,
    name="Candle of Communion (2)",
    arete=2,
    background_cost=2,
    quintessence_max=10,
    description="""A hand-crafted ritual candle, typically made from beeswax infused with sacred herbs and oils. The Candle of Communion is a staple tool among Verbena practitioners, particularly those who work with spirits and ancestors. When lit with proper ritual intent, the candle's flame becomes a beacon in both the physical world and the Umbra, opening channels of communication.

The candle (Arete 2) glows with an otherworldly light when activated, and spirits are drawn to its warmth. The practitioner can speak with entities across the Gauntlet, receive messages from ancestors, or even attract helpful spirits to aid in magical workings. The quality of communion depends on the candle's Arete rating - lower rated candles provide vaguer, more symbolic communication, while higher rated ones allow for clearer dialogue.

Each candle typically provides several hours of burn time, and master crafters can create candles with specific attunements to particular types of spirits or ancestors.""",
)[0].add_source("Lore of the Traditions", 146)
Talisman.objects.get_or_create(
    display=False,
    name="Candle of Communion (3)",
    arete=3,
    background_cost=2,
    quintessence_max=15,
    description="""A hand-crafted ritual candle, typically made from beeswax infused with sacred herbs and oils. The Candle of Communion is a staple tool among Verbena practitioners, particularly those who work with spirits and ancestors. When lit with proper ritual intent, the candle's flame becomes a beacon in both the physical world and the Umbra, opening channels of communication.

The candle (Arete 3) glows with an otherworldly light when activated, and spirits are drawn to its warmth. The practitioner can speak with entities across the Gauntlet, receive messages from ancestors, or even attract helpful spirits to aid in magical workings. The quality of communion depends on the candle's Arete rating - lower rated candles provide vaguer, more symbolic communication, while higher rated ones allow for clearer dialogue.

Each candle typically provides several hours of burn time, and master crafters can create candles with specific attunements to particular types of spirits or ancestors.""",
)[0].add_source("Lore of the Traditions", 146)

Talisman.objects.get_or_create(
    display=False,
    name="Mama Cybele's Tea Collection (2)",
    arete=2,
    background_cost=4,
    quintessence_max=10,
    description="""Mama Cybele is a renowned Verbena herbalist whose tea collection has become legendary among the Traditions. Each blend in her collection is carefully crafted from rare herbs, flowers, and other natural ingredients, infused with Life and Prime magick to create powerful healing and enhancement effects.

This tea collection (Arete 2) contains numerous blends, each with different properties:
- **Healing Blend**: Accelerates natural healing, can cure diseases
- **Dreaming Tea**: Grants prophetic visions and insights during sleep
- **Vitality Brew**: Provides sustained energy without the crash of mundane stimulants
- **Protection Tisane**: Strengthens the body's natural defenses
- **Clarity Infusion**: Sharpens the mind and enhances mental acuity

The teas are typically prepared with proper ritual - water blessed under appropriate moon phases, steeped for specific durations while chanting, and consumed with mindful intent. Higher Arete collections contain rarer and more potent blends capable of more dramatic effects.

The collection is usually stored in an antique wooden box with individual compartments for each blend, labeled in Mama Cybele's flowing script.""",
)[0].add_source("Lore of the Traditions", 146)
Talisman.objects.get_or_create(
    display=False,
    name="Mama Cybele's Tea Collection (3)",
    arete=3,
    background_cost=4,
    quintessence_max=15,
    description="""Mama Cybele is a renowned Verbena herbalist whose tea collection has become legendary among the Traditions. Each blend in her collection is carefully crafted from rare herbs, flowers, and other natural ingredients, infused with Life and Prime magick to create powerful healing and enhancement effects.

This tea collection (Arete 3) contains numerous blends, each with different properties:
- **Healing Blend**: Accelerates natural healing, can cure diseases
- **Dreaming Tea**: Grants prophetic visions and insights during sleep
- **Vitality Brew**: Provides sustained energy without the crash of mundane stimulants
- **Protection Tisane**: Strengthens the body's natural defenses
- **Clarity Infusion**: Sharpens the mind and enhances mental acuity

The teas are typically prepared with proper ritual - water blessed under appropriate moon phases, steeped for specific durations while chanting, and consumed with mindful intent. Higher Arete collections contain rarer and more potent blends capable of more dramatic effects.

The collection is usually stored in an antique wooden box with individual compartments for each blend, labeled in Mama Cybele's flowing script.""",
)[0].add_source("Lore of the Traditions", 146)
Talisman.objects.get_or_create(
    display=False,
    name="Mama Cybele's Tea Collection (4)",
    arete=4,
    background_cost=4,
    quintessence_max=20,
    description="""Mama Cybele is a renowned Verbena herbalist whose tea collection has become legendary among the Traditions. Each blend in her collection is carefully crafted from rare herbs, flowers, and other natural ingredients, infused with Life and Prime magick to create powerful healing and enhancement effects.

This tea collection (Arete 4) contains numerous blends, each with different properties:
- **Healing Blend**: Accelerates natural healing, can cure diseases
- **Dreaming Tea**: Grants prophetic visions and insights during sleep
- **Vitality Brew**: Provides sustained energy without the crash of mundane stimulants
- **Protection Tisane**: Strengthens the body's natural defenses
- **Clarity Infusion**: Sharpens the mind and enhances mental acuity

The teas are typically prepared with proper ritual - water blessed under appropriate moon phases, steeped for specific durations while chanting, and consumed with mindful intent. Higher Arete collections contain rarer and more potent blends capable of more dramatic effects.

The collection is usually stored in an antique wooden box with individual compartments for each blend, labeled in Mama Cybele's flowing script.""",
)[0].add_source("Lore of the Traditions", 146)
Talisman.objects.get_or_create(
    display=False,
    name="Mama Cybele's Tea Collection (5)",
    arete=5,
    background_cost=4,
    quintessence_max=25,
    description="""Mama Cybele is a renowned Verbena herbalist whose tea collection has become legendary among the Traditions. Each blend in her collection is carefully crafted from rare herbs, flowers, and other natural ingredients, infused with Life and Prime magick to create powerful healing and enhancement effects.

This tea collection (Arete 5) contains numerous blends, each with different properties:
- **Healing Blend**: Accelerates natural healing, can cure diseases
- **Dreaming Tea**: Grants prophetic visions and insights during sleep
- **Vitality Brew**: Provides sustained energy without the crash of mundane stimulants
- **Protection Tisane**: Strengthens the body's natural defenses
- **Clarity Infusion**: Sharpens the mind and enhances mental acuity

The teas are typically prepared with proper ritual - water blessed under appropriate moon phases, steeped for specific durations while chanting, and consumed with mindful intent. Higher Arete collections contain rarer and more potent blends capable of more dramatic effects.

The collection is usually stored in an antique wooden box with individual compartments for each blend, labeled in Mama Cybele's flowing script.""",
)[0].add_source("Lore of the Traditions", 146)

Talisman.objects.get_or_create(
    display=False,
    name="Grand Book of Shadows (4)",
    arete=4,
    quintessence_max=10,
    background_cost=8,
    description="""The Grand Book of Shadows is a magnificent leather-bound tome that serves as both grimoire and mystical artifact for a Verbena coven. Bound in aged leather and inscribed with symbols of the Goddess and God, this book is more than just a repository of spells - it is a living record of the coven's practices, history, and collective wisdom.

The book (Arete 4) typically resides on a central altar and is treated with great reverence. Each page contains hand-written entries from generations of witches, detailing rituals, herb lore, spell formulae, and mystical insights. The book itself has absorbed so much magical energy over the years that it has developed a quasi-sentient awareness.

Many Grand Books of Shadows can function as Familiars (see Familiar Background), offering guidance, warning of danger, or even refusing to open if a non-initiate attempts to read it. The book can:
- Store and organize magical knowledge
- Teach new spells and rituals to worthy students
- Provide mystical insights and guidance
- Generate protective wards when placed on an altar
- Record magical workings automatically when they occur nearby

The book grows more powerful as it ages, accumulating wisdom and Quintessence. Some of the oldest examples are considered irreplaceable treasures of their Traditions, containing lost knowledge and unique spell variants found nowhere else.""",
)[0].add_source("Lore of the Traditions", 131)
Talisman.objects.get_or_create(
    display=False,
    name="Grand Book of Shadows (5)",
    arete=5,
    quintessence_max=15,
    background_cost=8,
    description="""The Grand Book of Shadows is a magnificent leather-bound tome that serves as both grimoire and mystical artifact for a Verbena coven. Bound in aged leather and inscribed with symbols of the Goddess and God, this book is more than just a repository of spells - it is a living record of the coven's practices, history, and collective wisdom.

The book (Arete 5) typically resides on a central altar and is treated with great reverence. Each page contains hand-written entries from generations of witches, detailing rituals, herb lore, spell formulae, and mystical insights. The book itself has absorbed so much magical energy over the years that it has developed a quasi-sentient awareness.

Many Grand Books of Shadows can function as Familiars (see Familiar Background), offering guidance, warning of danger, or even refusing to open if a non-initiate attempts to read it. The book can:
- Store and organize magical knowledge
- Teach new spells and rituals to worthy students
- Provide mystical insights and guidance
- Generate protective wards when placed on an altar
- Record magical workings automatically when they occur nearby

The book grows more powerful as it ages, accumulating wisdom and Quintessence. Some of the oldest examples are considered irreplaceable treasures of their Traditions, containing lost knowledge and unique spell variants found nowhere else.""",
)[0].add_source("Lore of the Traditions", 131)
Talisman.objects.get_or_create(
    display=False,
    name="Grand Book of Shadows (6)",
    arete=6,
    quintessence_max=20,
    background_cost=8,
    description="""The Grand Book of Shadows is a magnificent leather-bound tome that serves as both grimoire and mystical artifact for a Verbena coven. Bound in aged leather and inscribed with symbols of the Goddess and God, this book is more than just a repository of spells - it is a living record of the coven's practices, history, and collective wisdom.

The book (Arete 6) typically resides on a central altar and is treated with great reverence. Each page contains hand-written entries from generations of witches, detailing rituals, herb lore, spell formulae, and mystical insights. The book itself has absorbed so much magical energy over the years that it has developed a quasi-sentient awareness.

Many Grand Books of Shadows can function as Familiars (see Familiar Background), offering guidance, warning of danger, or even refusing to open if a non-initiate attempts to read it. The book can:
- Store and organize magical knowledge
- Teach new spells and rituals to worthy students
- Provide mystical insights and guidance
- Generate protective wards when placed on an altar
- Record magical workings automatically when they occur nearby

The book grows more powerful as it ages, accumulating wisdom and Quintessence. Some of the oldest examples are considered irreplaceable treasures of their Traditions, containing lost knowledge and unique spell variants found nowhere else.""",
)[0].add_source("Lore of the Traditions", 131)
Talisman.objects.get_or_create(
    display=False,
    name="Grand Book of Shadows (7)",
    arete=7,
    quintessence_max=25,
    background_cost=8,
    description="""The Grand Book of Shadows is a magnificent leather-bound tome that serves as both grimoire and mystical artifact for a Verbena coven. Bound in aged leather and inscribed with symbols of the Goddess and God, this book is more than just a repository of spells - it is a living record of the coven's practices, history, and collective wisdom.

The book (Arete 7) typically resides on a central altar and is treated with great reverence. Each page contains hand-written entries from generations of witches, detailing rituals, herb lore, spell formulae, and mystical insights. The book itself has absorbed so much magical energy over the years that it has developed a quasi-sentient awareness.

Many Grand Books of Shadows can function as Familiars (see Familiar Background), offering guidance, warning of danger, or even refusing to open if a non-initiate attempts to read it. The book can:
- Store and organize magical knowledge
- Teach new spells and rituals to worthy students
- Provide mystical insights and guidance
- Generate protective wards when placed on an altar
- Record magical workings automatically when they occur nearby

The book grows more powerful as it ages, accumulating wisdom and Quintessence. Some of the oldest examples are considered irreplaceable treasures of their Traditions, containing lost knowledge and unique spell variants found nowhere else.""",
)[0].add_source("Lore of the Traditions", 131)
Talisman.objects.get_or_create(
    display=False,
    name="Grand Book of Shadows (8)",
    arete=8,
    quintessence_max=25,
    background_cost=8,
    description="""The Grand Book of Shadows is a magnificent leather-bound tome that serves as both grimoire and mystical artifact for a Verbena coven. Bound in aged leather and inscribed with symbols of the Goddess and God, this book is more than just a repository of spells - it is a living record of the coven's practices, history, and collective wisdom.

The book (Arete 8) typically resides on a central altar and is treated with great reverence. Each page contains hand-written entries from generations of witches, detailing rituals, herb lore, spell formulae, and mystical insights. The book itself has absorbed so much magical energy over the years that it has developed a quasi-sentient awareness.

Many Grand Books of Shadows can function as Familiars (see Familiar Background), offering guidance, warning of danger, or even refusing to open if a non-initiate attempts to read it. The book can:
- Store and organize magical knowledge
- Teach new spells and rituals to worthy students
- Provide mystical insights and guidance
- Generate protective wards when placed on an altar
- Record magical workings automatically when they occur nearby

The book grows more powerful as it ages, accumulating wisdom and Quintessence. Some of the oldest examples are considered irreplaceable treasures of their Traditions, containing lost knowledge and unique spell variants found nowhere else.""",
)[0].add_source("Lore of the Traditions", 131)

Artifact.objects.get_or_create(
    display=False, name="Rod Logic Computer", quintessence_max=10, background_cost=3
)[0].add_source("Lore of the Traditions", 161)

# Create Effects for Wonders and attach them

# Dragon Pearls - Use existing Channel Quintessence effect
dragon_pearls = Artifact.objects.get(name="Dragon Pearls")
dragon_pearls.power = Effect.objects.get(name="Channel Quintessence")
dragon_pearls.save()

# Antaratma - Quiet resistance talisman
antaratma_effect = Effect.objects.get_or_create(
    name="Quiet Resistance (Antaratma)",
    mind=3,
    prime=2,
    spirit=2,
    description="Provides resistance to Quiet and madness. Grants 1 level of Quiet resistance per 2 successes on Arete roll. Can provide a Willpower point for casting once per day.",
)[0]
antaratma = Talisman.objects.get(name="Antaratma")
antaratma.powers.add(antaratma_effect)

# Dümerang Blade - Returning weapon
dumerang_effect = Effect.objects.get_or_create(
    name="Returning Weapon (Dümerang Blade)",
    forces=2,
    correspondence=2,
    prime=2,
    description="Enchanted boomerang that automatically returns to the wielder's hand after being thrown. The blade auto-regenerates its Arete rating daily. Can be used as both melee and ranged weapon.",
)[0]
for arete_level in [2, 3, 4]:
    dumerang = Talisman.objects.get(name=f"Dümerang Blade ({arete_level})")
    dumerang.powers.add(dumerang_effect)

# Candle of Communion - Spirit communication
candle_effect = Effect.objects.get_or_create(
    name="Spirit Communion (Candle)",
    spirit=3,
    mind=2,
    prime=2,
    description="When lit, this candle opens a channel of communication with spirits, ancestors, and entities in the Umbra. The flickering flame creates a beacon visible in both the physical and spirit worlds, attracting helpful spirits and allowing for clearer communion.",
)[0]
for arete_level in [1, 2, 3]:
    candle = Talisman.objects.get(name=f"Candle of Communion ({arete_level})")
    candle.powers.add(candle_effect)

# Mama Cybele's Tea Collection - Healing and enhancement
tea_heal_effect = Effect.objects.get_or_create(
    name="Herbal Healing (Tea)",
    life=3,
    prime=2,
    description="Magically enhanced herbal tea that promotes healing and well-being. Different blends can cure ailments, grant visions, provide energy, or offer protection.",
)[0]
tea_enhance_effect = Effect.objects.get_or_create(
    name="Herbal Enhancement (Tea)",
    life=2,
    mind=1,
    description="Herbal tea that temporarily enhances physical or mental capabilities, or provides prophetic dreams and insights.",
)[0]
for arete_level in [2, 3, 4, 5]:
    tea = Talisman.objects.get(name=f"Mama Cybele's Tea Collection ({arete_level})")
    tea.powers.add(tea_heal_effect)
    tea.powers.add(tea_enhance_effect)

# Grand Book of Shadows - Living grimoire
book_power_effect = Effect.objects.get_or_create(
    name="Mystical Grimoire Power (Book of Shadows)",
    prime=3,
    spirit=2,
    mind=2,
    description="A living grimoire that stores knowledge, spells, and mystical power. Can function as a Familiar, offering advice and magical assistance. Contains centuries of Verbena wisdom and practices.",
)[0]
for arete_level in [4, 5, 6, 7, 8]:
    if Talisman.objects.filter(name=f"Grand Book of Shadows ({arete_level})").exists():
        book = Talisman.objects.get(name=f"Grand Book of Shadows ({arete_level})")
        book.powers.add(book_power_effect)

# Angel Tear Daggers - Holy weapons
angel_dagger_effect = Effect.objects.get_or_create(
    name="Blessed Blade (Angel Tears)",
    prime=2,
    spirit=2,
    forces=1,
    description="Daggers forged from crystallized tears of angels (or so the legend claims). Highly effective against demonic and infernal entities, dealing aggravated damage to such beings. The blades glow with soft silver light when evil is near.",
)[0]
angel_daggers = Artifact.objects.get(name="Angel Tear Daggers")
angel_daggers.power = angel_dagger_effect
angel_daggers.save()

# Game of Senet - Divination board game
senet_effect = Effect.objects.get_or_create(
    name="Fate Game (Senet)",
    entropy=2,
    time=1,
    description="An ancient Egyptian board game that can divine fate and fortune. Playing the game allows glimpses into probability streams and potential futures.",
)[0]
senet = Artifact.objects.get(name="Game of Senet")
senet.power = senet_effect
senet.save()

# Imphepho Wierook - Ancestral incense
imphepho_effect = Effect.objects.get_or_create(
    name="Ancestral Incense (Imphepho)",
    spirit=2,
    mind=1,
    prime=1,
    description="Sacred incense that opens channels to the ancestors and spirits. The smoke carries prayers and messages to the spirit world while inviting ancestral guidance and protection.",
)[0]
imphepho = Artifact.objects.get(name="Imphepho Wierook")
imphepho.power = imphepho_effect
imphepho.save()

# Waidan Ding - Alchemical cauldron
ding_effect = Effect.objects.get_or_create(
    name="Alchemical Vessel (Ding)",
    matter=3,
    prime=2,
    forces=1,
    description="An alchemical cauldron used for transmutation and the creation of elixirs. Enhances all alchemical workings and can transmute base materials into more refined substances.",
)[0]
ding = Artifact.objects.get(name="Waidan Ding")
ding.power = ding_effect
ding.save()

# Alanson Light Hardsuit - Void Engineer armor
light_hardsuit_effect = Effect.objects.get_or_create(
    name="Light Combat Armor (Alanson)",
    matter=3,
    forces=2,
    prime=2,
    description="Lightweight powered armor providing protection and enhanced mobility. Includes HUD, environmental seals, and basic combat systems. Armor Rating 3 (+3 soak dice).",
)[0]
light_hardsuit = Talisman.objects.get(name="Alanson Light Hardsuit")
light_hardsuit.powers.add(light_hardsuit_effect)

# Alanson R-25 Hardsuit - Heavy combat armor
r25_hardsuit_effect = Effect.objects.get_or_create(
    name="Heavy Combat Armor (Alanson R-25)",
    matter=4,
    forces=3,
    prime=2,
    correspondence=2,
    description="Advanced powered armor with heavy protection, weapons systems, and dimensional stabilizers. Armor Rating 7 when fully powered. Includes integrated weapons and sensor suite.",
)[0]
r25_hardsuit = Talisman.objects.get(name="Alanson R-25 Hardsuit")
r25_hardsuit.powers.add(r25_hardsuit_effect)

# ===== EXAMPLE WONDERS, TALISMANS, ARTIFACTS FROM MAGE SOURCEBOOKS =====
# These serve as examples and templates for magical items

from items.models.mage.wonder import Wonder
from items.models.mage.charm import Charm
from characters.models.mage.resonance import Resonance

# Dragon Pearls (Akashic Brotherhood)
pearl = Wonder.objects.get_or_create(
    name="Dragon Pearl (Lesser)",
    rank=3,
    background_cost=6,
    quintessence_max=5,
)[0]
pearl.description = (
    "A crystallized sphere of Quintessence used by Akashic mages to channel chi. "
    "Grants +1 die to Life and Prime effects when held during casting."
)
pearl.add_source("Lore of the Traditions", 28)
pearl.set_rank(3)
pearl.add_resonance(Resonance.objects.get_or_create(name="Harmonious")[0])
pearl.add_resonance(Resonance.objects.get_or_create(name="Balanced")[0])
pearl.save()

pearl_greater = Wonder.objects.get_or_create(
    name="Dragon Pearl (Greater)",
    rank=5,
    background_cost=12,
    quintessence_max=10,
)[0]
pearl_greater.description = (
    "A master-crafted Dragon Pearl containing immense power. "
    "Grants +2 dice to Life and Prime effects and can store Paradox."
)
pearl_greater.add_source("Lore of the Traditions", 28)
pearl_greater.set_rank(5)
pearl_greater.add_resonance(Resonance.objects.get_or_create(name="Harmonious")[0])
pearl_greater.add_resonance(Resonance.objects.get_or_create(name="Powerful")[0])
pearl_greater.save()

# Flying Carpet
carpet = Wonder.objects.get_or_create(
    name="Flying Carpet of Al-Rashid",
    rank=4,
    background_cost=10,
    quintessence_max=15,
)[0]
carpet.description = (
    "An enchanted Persian carpet that flies at the will of its owner. "
    "Can carry up to 4 passengers at speeds up to 100 mph."
)
carpet.add_source("M20 Core", 656)
carpet.set_rank(4)
carpet.add_resonance(Resonance.objects.get_or_create(name="Swift")[0])
carpet.add_resonance(Resonance.objects.get_or_create(name="Mystical")[0])
carpet.save()

# Hermetic Staff of Power
staff = Wonder.objects.get_or_create(
    name="Staff of the Magi",
    rank=5,
    background_cost=15,
    quintessence_max=20,
)[0]
staff.description = (
    "A powerful Hermetic staff carved from ancient oak and bound with silver. "
    "Grants +2 dice to all ritual magic and can channel lightning bolts (Forces 3)."
)
staff.add_source("Lore of the Traditions", 128)
staff.set_rank(5)
staff.add_resonance(Resonance.objects.get_or_create(name="Powerful")[0])
staff.add_resonance(Resonance.objects.get_or_create(name="Ancient")[0])
staff.save()

# Verbena Athame
athame = Wonder.objects.get_or_create(
    name="Athame of the Moon",
    rank=3,
    background_cost=6,
    quintessence_max=10,
)[0]
athame.description = (
    "A ritual dagger used in Verbena witchcraft, especially blood magic. "
    "Reduces difficulty of Life magic by -1 when used to draw blood."
)
athame.add_source("Lore of the Traditions", 168)
athame.set_rank(3)
athame.add_resonance(Resonance.objects.get_or_create(name="Primal")[0])
athame.add_resonance(Resonance.objects.get_or_create(name="Vital")[0])
athame.save()

# Virtual Adept Cyberdeck
cyberdeck = Wonder.objects.get_or_create(
    name="Reality Hacker's Cyberdeck",
    rank=4,
    background_cost=10,
    quintessence_max=12,
)[0]
cyberdeck.description = (
    "An advanced cyberdeck modified with resonant circuits for reality hacking. "
    "Grants +2 dice to Correspondence and Mind effects when hacking reality or the Digital Web."
)
cyberdeck.add_source("Lore of the Traditions", 188)
cyberdeck.set_rank(4)
cyberdeck.add_resonance(Resonance.objects.get_or_create(name="Digital")[0])
cyberdeck.add_resonance(Resonance.objects.get_or_create(name="Innovative")[0])
cyberdeck.save()

# Healing Potion
potion = Talisman.objects.get_or_create(
    name="Elixir of Regeneration",
    rank=2,
    background_cost=4,
    quintessence_max=3,
)[0]
potion.description = (
    "An alchemical potion that heals 2 health levels of lethal damage when consumed. "
    "Single use."
)
potion.add_source("M20 Core", 656)
potion.set_rank(2)
potion.quintessence_max = 3
potion.save()

# Wand of Lightning
wand = Talisman.objects.get_or_create(
    name="Wand of Chain Lightning",
    rank=3,
    background_cost=6,
    quintessence_max=10,
)[0]
wand.description = (
    "A Hermetic wand that can unleash lightning bolts. Contains 10 charges, "
    "each dealing 4 dice of lethal damage (Forces 3)."
)
wand.add_source("Lore of the Traditions", 129)
wand.set_rank(3)
wand.save()

# Scrying Mirror
mirror = Talisman.objects.get_or_create(
    name="Mirror of True Seeing",
    rank=3,
    background_cost=6,
    quintessence_max=8,
)[0]
mirror.description = (
    "A polished obsidian mirror that allows remote viewing anywhere on Earth. "
    "Uses Correspondence 3, Time 2 for past viewing."
)
mirror.add_source("M20 Core", 656)
mirror.set_rank(3)
mirror.save()

# Ring of Protection
ring = Talisman.objects.get_or_create(
    name="Ring of Warding",
    rank=2,
    background_cost=4,
    quintessence_max=5,
)[0]
ring.description = (
    "A silver ring inscribed with protective runes. Grants +2 dice to soak "
    "and can activate a shield once per day (Forces 2)."
)
ring.add_source("M20 Core", 656)
ring.set_rank(2)
ring.save()

# Legendary Artifacts
excalibur = Artifact.objects.get_or_create(
    name="Sword of the Rightful King",
    rank=5,
    background_cost=15,
    quintessence_max=25,
)[0]
excalibur.description = (
    "A legendary sword of power that can only be wielded by the worthy. "
    "Deals aggravated damage, grants +3 to all combat pools, and radiates an "
    "aura of divine authority (Prime 5, Forces 3, Mind 3)."
)
excalibur.add_source("M20 Core", 658)
excalibur.set_rank(5)
excalibur.add_resonance(Resonance.objects.get_or_create(name="Noble")[0])
excalibur.add_resonance(Resonance.objects.get_or_create(name="Powerful")[0])
excalibur.add_resonance(Resonance.objects.get_or_create(name="Holy")[0])
excalibur.save()

# Philosopher's Stone
stone = Artifact.objects.get_or_create(
    name="The Philosopher's Stone",
    rank=5,
    background_cost=15,
    quintessence_max=30,
)[0]
stone.description = (
    "The legendary alchemical artifact capable of transmuting base metals to gold, "
    "granting immortality, and creating Tass. The ultimate goal of alchemists "
    "(Matter 5, Prime 5, Life 5)."
)
stone.add_source("Lore of the Traditions", 129)
stone.set_rank(5)
stone.add_resonance(Resonance.objects.get_or_create(name="Perfect")[0])
stone.add_resonance(Resonance.objects.get_or_create(name="Transformative")[0])
stone.save()

# Holy Grail
grail = Artifact.objects.get_or_create(
    name="The Holy Grail",
    rank=5,
    background_cost=15,
    quintessence_max=50,
)[0]
grail.description = (
    "The cup of Christ, legendary artifact of the Celestial Chorus. "
    "Grants perfect healing, spiritual enlightenment, and connection to the Divine "
    "(Life 5, Prime 5, Spirit 5, Mind 4)."
)
grail.add_source("Lore of the Traditions", 48)
grail.set_rank(5)
grail.add_resonance(Resonance.objects.get_or_create(name="Holy")[0])
grail.add_resonance(Resonance.objects.get_or_create(name="Divine")[0])
grail.add_resonance(Resonance.objects.get_or_create(name="Healing")[0])
grail.save()

# Spirit Whistle
whistle = Charm.objects.get_or_create(
    name="Spirit-Calling Whistle",
    rank=2,
    background_cost=4,
    quintessence_max=5,
    arete=2,
)[0]
whistle.power = Effect.objects.get(name="Summon Spirit (Minor)")
whistle.description = (
    "A carved bone whistle that summons friendly spirits when blown. "
    "Contains a minor air spirit."
)
whistle.add_source("M20 Core", 658)
whistle.set_rank(2)
whistle.save()

# Ghost-Slaying Sword
ghostblade = Charm.objects.get_or_create(
    name="Blade of Ectoplasmic Severance",
    rank=3,
    background_cost=6,
    quintessence_max=8,
    arete=3,
)[0]
ghostblade.power = Effect.objects.get(name="Harm Ghost")
ghostblade.description = (
    "A sword bound with a spirit that allows it to harm incorporeal entities. "
    "Deals aggravated damage to ghosts and spirits."
)
ghostblade.add_source("M20 Core", 658)
ghostblade.set_rank(3)
ghostblade.save()

# Grimoires
grimoire1 = Grimoire.objects.get_or_create(
    name="The Lesser Key of Solomon",
    rank=3,
)[0]
grimoire1.description = (
    "A classic grimoire of Hermetic magic containing rituals for summoning "
    "and binding spirits. Teaches Spirit 3, Prime 2, and High Ritual Magick."
)
grimoire1.add_source("Lore of the Traditions", 128)
grimoire1.set_rank(3)
grimoire1.save()

grimoire2 = Grimoire.objects.get_or_create(
    name="The Sutra of Perfect Understanding",
    rank=4,
)[0]
grimoire2.description = (
    "An ancient Buddhist text revealing the secrets of Do and enlightenment. "
    "Teaches Life 4, Mind 4, and advanced martial arts techniques."
)
grimoire2.add_source("Lore of the Traditions", 28)
grimoire2.set_rank(4)
grimoire2.save()

grimoire3 = Grimoire.objects.get_or_create(
    name="The Grand Book of Shadows",
    rank=4,
)[0]
grimoire3.description = (
    "A massive tome containing generations of Verbena wisdom, blood rituals, "
    "and natural magic. Teaches Life 4, Prime 3, Forces 3, and Witchcraft."
)
grimoire3.add_source("Lore of the Traditions", 168)
grimoire3.set_rank(4)
grimoire3.save()

grimoire4 = Grimoire.objects.get_or_create(
    name="The Digital Necronomicon",
    rank=4,
)[0]
grimoire4.description = (
    "A constantly-updating digital grimoire in the Deep Web containing advanced "
    "reality hacking techniques. Teaches Correspondence 4, Forces 3, Mind 3."
)
grimoire4.add_source("Lore of the Traditions", 188)
grimoire4.set_rank(4)
grimoire4.save()

grimoire5 = Grimoire.objects.get_or_create(
    name="Dr. Tesla's Collected Works",
    rank=5,
)[0]
grimoire5.description = (
    "The complete works of Nikola Tesla, annotated with Etheric theories. "
    "Teaches Forces 5, Matter 4, Prime 3, and Weird Science."
)
grimoire5.add_source("Lore of the Traditions", 148)
grimoire5.set_rank(5)
grimoire5.save()

# Technocratic Devices
flashything = Wonder.objects.get_or_create(
    name="Memory Reorganization Device (Flashy Thing)",
    rank=3,
    background_cost=6,
    quintessence_max=10,
)[0]
flashything.description = (
    "A pen-shaped device that erases memories of reality deviation and replaces "
    "them with consensus-acceptable explanations (Mind 3, Prime 2)."
)
flashything.add_source("Technocracy Reloaded", 225)
flashything.set_rank(3)
flashything.save()

nanites = Talisman.objects.get_or_create(
    name="Advanced Cellular Reconstruction Nanites",
    rank=3,
    background_cost=6,
    quintessence_max=8,
)[0]
nanites.description = (
    "Microscopic medical nanobots that rapidly heal injuries. "
    "Heals 3 health levels of lethal damage or 1 aggravated over 24 hours."
)
nanites.add_source("Technocracy Reloaded", 218)
nanites.set_rank(3)
nanites.save()

portal = Wonder.objects.get_or_create(
    name="Portable Dimensional Gateway",
    rank=4,
    background_cost=10,
    quintessence_max=15,
)[0]
portal.description = (
    "A briefcase-sized device that opens stable portals to predetermined locations "
    "or the Deep Umbra (Correspondence 4, Spirit 3, Prime 2)."
)
portal.add_source("Technocracy Reloaded", 227)
portal.set_rank(4)
portal.save()

exo = Wonder.objects.get_or_create(
    name="AEGIS Mark VII Powered Armor",
    rank=4,
    background_cost=10,
    quintessence_max=12,
)[0]
exo.description = (
    "Advanced powered armor with enhanced strength, armor plating, and integrated "
    "weapon systems. +3 Strength, +5 Armor, built-in weapons "
    "(Matter 4, Forces 3, Life 2)."
)
exo.add_source("Technocracy Reloaded", 205)
exo.set_rank(4)
exo.save()

probdev = Wonder.objects.get_or_create(
    name="Statistical Variance Optimization Device",
    rank=3,
    background_cost=6,
    quintessence_max=10,
)[0]
probdev.description = (
    "A subtle device disguised as a luxury watch that manipulates probability "
    "to ensure favorable outcomes in business and gambling (Entropy 3)."
)
probdev.add_source("Technocracy Reloaded", 182)
probdev.set_rank(3)
probdev.save()

# Unique/Plot Devices
doissetep_stone = Artifact.objects.get_or_create(
    name="Heartstone of Doissetep",
    rank=5,
    background_cost=15,
    quintessence_max=100,
)[0]
doissetep_stone.description = (
    "The central Node stone from the destroyed Chantry of Doissetep. "
    "Contains immense Quintessence and can anchor Horizon Realms. "
    "Radiates powerful Hermetic resonance (Prime 5, Spirit 5, All Spheres 3)."
)
doissetep_stone.add_source("M20 Core", 612)
doissetep_stone.set_rank(5)
doissetep_stone.add_resonance(Resonance.objects.get_or_create(name="Ancient")[0])
doissetep_stone.add_resonance(Resonance.objects.get_or_create(name="Powerful")[0])
doissetep_stone.add_resonance(Resonance.objects.get_or_create(name="Tragic")[0])
doissetep_stone.save()

detector = Wonder.objects.get_or_create(
    name="Avatar Storm Early Warning System",
    rank=3,
    background_cost=6,
    quintessence_max=8,
)[0]
detector.description = (
    "A device that detects approaching Avatar Storms and Paradox buildups. "
    "Essential for safe Umbral travel (Spirit 3, Prime 2, Entropy 1)."
)
detector.add_source("M20 Core", 534)
detector.set_rank(3)
detector.save()


for a in Artifact.objects.all():
    if a.rank == 0:
        a.rank = max([a.background_cost // 2, 1])
        a.save()
for t in Talisman.objects.all():
    if t.rank == 0:
        t.rank = max([t.background_cost // 2, 1])
        t.save()
# for c in Charm.objects.all():
#     pass
