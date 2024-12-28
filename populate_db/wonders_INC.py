from items.models.mage.artifact import Artifact
from items.models.mage.grimoire import Grimoire
from items.models.mage.talisman import Talisman

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
)[0]
Talisman.objects.get_or_create(
    display=False,
    name="Alanson R-25 Hardsuit",
    background_cost=5,
    arete=4,
    quintessence_max=20,
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


Artifact.objects.get_or_create(display=False, name="Dragon Pearls", background_cost=6)[
    0
].add_source("Lore of the Traditions", 35)
Artifact.objects.get_or_create(
    display=False, name="Angel Tear Daggers", quintessence_max=10, background_cost=7
)[0].add_source("Lore of the Traditions", 49)
Talisman.objects.get_or_create(
    display=False, name="Antaratma", arete=4, quintessence_max=10, background_cost=8
)[0].add_source("Lore of the Traditions", 98)

Artifact.objects.get_or_create(display=False, name="Game of Senet", background_cost=2)[
    0
].add_source("Lore of the Traditions", 115)
Artifact.objects.get_or_create(
    display=False, name="Imphepho Wierook", quintessence_max=15, background_cost=3
)[0].add_source("Lore of the Traditions", 115)
Artifact.objects.get_or_create(
    display=False, name="Waidan Ding", quintessence_max=10, background_cost=5
)[0].add_source("Lore of the Traditions", 115)

Talisman.objects.get_or_create(
    display=False, name="Dümerang Blade (2)", arete=2, background_cost=4
)[0].add_source("Lore of the Traditions", 130)
Talisman.objects.get_or_create(
    display=False, name="Dümerang Blade (3)", arete=3, background_cost=8
)[0].add_source("Lore of the Traditions", 130)
Talisman.objects.get_or_create(
    display=False, name="Dümerang Blade (4)", arete=4, background_cost=12
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
)[0].add_source("Lore of the Traditions", 146)
Talisman.objects.get_or_create(
    display=False,
    name="Candle of Communion (2)",
    arete=2,
    background_cost=2,
    quintessence_max=10,
)[0].add_source("Lore of the Traditions", 146)
Talisman.objects.get_or_create(
    display=False,
    name="Candle of Communion (3)",
    arete=3,
    background_cost=2,
    quintessence_max=15,
)[0].add_source("Lore of the Traditions", 146)

Talisman.objects.get_or_create(
    display=False,
    name="Mama Cybele's Tea Collection (2)",
    arete=2,
    background_cost=4,
    quintessence_max=10,
)[0].add_source("Lore of the Traditions", 146)
Talisman.objects.get_or_create(
    display=False,
    name="Mama Cybele's Tea Collection (3)",
    arete=3,
    background_cost=4,
    quintessence_max=15,
)[0].add_source("Lore of the Traditions", 146)
Talisman.objects.get_or_create(
    display=False,
    name="Mama Cybele's Tea Collection (4)",
    arete=4,
    background_cost=4,
    quintessence_max=20,
)[0].add_source("Lore of the Traditions", 146)
Talisman.objects.get_or_create(
    display=False,
    name="Mama Cybele's Tea Collection (5)",
    arete=5,
    background_cost=4,
    quintessence_max=25,
)[0].add_source("Lore of the Traditions", 146)

Talisman.objects.get_or_create(
    display=False,
    name="Grand Book of Shadows (4)",
    arete=4,
    quintessence_max=10,
    background_cost=8,
)[0].add_source("Lore of the Traditions", 131)
Talisman.objects.get_or_create(
    display=False,
    name="Grand Book of Shadows (5)",
    arete=5,
    quintessence_max=15,
    background_cost=8,
)[0].add_source("Lore of the Traditions", 131)
Talisman.objects.get_or_create(
    display=False,
    name="Grand Book of Shadows (6)",
    arete=6,
    quintessence_max=20,
    background_cost=8,
)[0].add_source("Lore of the Traditions", 131)
Talisman.objects.get_or_create(
    display=False,
    name="Grand Book of Shadows (7)",
    arete=7,
    quintessence_max=25,
    background_cost=8,
)[0].add_source("Lore of the Traditions", 131)
Talisman.objects.get_or_create(
    display=False,
    name="Grand Book of Shadows (8)",
    arete=8,
    quintessence_max=25,
    background_cost=8,
)[0].add_source("Lore of the Traditions", 131)

Artifact.objects.get_or_create(
    display=False, name="Rod Logic Computer", quintessence_max=10, background_cost=3
)[0].add_source("Lore of the Traditions", 161)


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
