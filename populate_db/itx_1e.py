"""
Iteration X 1st Edition - Technocracy Sourcebook
Extracted game objects for the Mage: The Ascension setting
"""

from characters.models.core.archetype import Archetype
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sphere import Sphere
from core.models import Book
from populate_db.mage.paradigms_INC import a_mechanistic_cosmos, tech_holds_all_answers
from populate_db.mage.practices_INC import cybernetics, hypertech
from populate_db.mage.spheres import (
    correspondence,
    entropy,
    forces,
    life,
    matter,
    mind,
    prime,
    spirit,
    time,
)

# ============================================================================
# BOOK
# ============================================================================

itx_1e, _ = Book.objects.get_or_create(
    title="Technocracy: Iteration X",
    author="Chris Hind and William Smith",
    system="mta",
    release_date="1993-01-01",
)

# ============================================================================
# FACTION STRUCTURE
# ============================================================================

# Get or create Technocratic Union parent faction
technocracy, _ = MageFaction.objects.get_or_create(name="Technocratic Union")
technocracy.founded = 1453  # Start of Technocracy
technocracy.paradigms.add(a_mechanistic_cosmos, tech_holds_all_answers)
technocracy.save()

# Create Iteration X Convention
iteration_x, _ = MageFaction.objects.get_or_create(
    name="Iteration X", parent=technocracy, founded=1900
)
iteration_x.affinities.add(forces, matter, prime)  # Most common spheres
iteration_x.paradigms.add(a_mechanistic_cosmos, tech_holds_all_answers)
iteration_x.practices.add(cybernetics, hypertech)
iteration_x.save()

# Create Methodologies (subfactions of Iteration X)
statisticians, _ = MageFaction.objects.get_or_create(
    name="Statisticians", parent=iteration_x, founded=-500  # Ancient origins
)
statisticians.affinities.add(entropy, mind, time, correspondence)
statisticians.save()

time_motion_managers, _ = MageFaction.objects.get_or_create(
    name="Time-Motion Managers", parent=iteration_x, founded=1800
)
time_motion_managers.affinities.add(time, matter, prime, forces)
time_motion_managers.save()

biomechanics, _ = MageFaction.objects.get_or_create(
    name="BioMechanics", parent=iteration_x, founded=1500
)
biomechanics.affinities.add(life, matter, prime)
biomechanics.save()

# ============================================================================
# EFFECTS (Technocratic Rotes/Procedures)
# ============================================================================

# Correspondence Effects
effect_targeting_computation, _ = Effect.objects.get_or_create(
    name="Targeting Computation",
    correspondence=1,
    description="Calculate variables for accurate projectile attacks. Reduces difficulty to 4 for attacks and negates soft cover.",
)
effect_targeting_computation.add_source(itx_1e, 46)

# Entropy Effects
effect_organize, _ = Effect.objects.get_or_create(
    name="Organize",
    entropy=1,
    description="Increase efficiency through organization. Each success reduces task difficulty by one.",
)
effect_organize.add_source(itx_1e, 46)

effect_statistical_mechanics, _ = Effect.objects.get_or_create(
    name="Statistical Mechanics",
    entropy=2,
    description="State applicable statistics to modify task difficulty based on odds.",
)
effect_statistical_mechanics.add_source(itx_1e, 47)

# Forces Effects
effect_audio_tap, _ = Effect.objects.get_or_create(
    name="Audio Tap",
    forces=1,
    description="Adjust perception to intercept microwave transmissions, radio waves, telephone conversations, and television signals.",
)
effect_audio_tap.add_source(itx_1e, 47)

effect_remote_programming, _ = Effect.objects.get_or_create(
    name="Remote Programming",
    forces=2,
    description="Program computers, robots, and devices at the speed of thought without physical contact.",
)
effect_remote_programming.add_source(itx_1e, 47)

effect_antinoise, _ = Effect.objects.get_or_create(
    name="Antinoise",
    forces=4,
    description="Create a sonic dampening field that cancels all sound within range through inverted sound waves.",
)
effect_antinoise.add_source(itx_1e, 48)

effect_emit_beam_ray, _ = Effect.objects.get_or_create(
    name="Emit Beam-ray",
    forces=3,
    prime=2,
    description="Combine microwaves, laser, and X-rays into a deadly attack. Each success causes two Health Levels of damage.",
)
effect_emit_beam_ray.add_source(itx_1e, 49)

effect_perpetual_motion, _ = Effect.objects.get_or_create(
    name="Perpetual Motion",
    forces=5,
    prime=2,
    description="Set objects in motion perpetually without fuel or external power.",
)
effect_perpetual_motion.add_source(itx_1e, 49)

# Matter Effects
effect_smelt_primium, _ = Effect.objects.get_or_create(
    name="Smelt Primium",
    matter=5,
    description="Create Primium, a magickal alloy of purified silver and gold with unique properties.",
)
effect_smelt_primium.add_source(itx_1e, 48)

effect_craft_biomechanism, _ = Effect.objects.get_or_create(
    name="Craft Biomechanism",
    matter=5,
    prime=3,
    description="Create a biomechanical prosthesis designed to be attached to a living body.",
)
effect_craft_biomechanism.add_source(itx_1e, 49)

effect_attach_biomechanism, _ = Effect.objects.get_or_create(
    name="Attach Biomechanism",
    matter=5,
    life=2,
    prime=3,
    description="Surgically attach a biomechanism to a host, knitting life and matter patterns together.",
)
effect_attach_biomechanism.add_source(itx_1e, 50)

# Mind Effects
effect_positronic_brain, _ = Effect.objects.get_or_create(
    name="Positronic Brain",
    mind=1,
    description="Access unused portions of the brain to temporarily add dots to Mental Traits.",
)
effect_positronic_brain.add_source(itx_1e, 48)

effect_social_science, _ = Effect.objects.get_or_create(
    name="Social Science",
    mind=2,
    description="Condition subjects through depressing facts, intimidation, or subliminal suggestion to reduce Willpower.",
)
effect_social_science.add_source(itx_1e, 48)

effect_machine_god, _ = Effect.objects.get_or_create(
    name="Machine God",
    mind=2,
    matter=1,
    forces=1,
    description="Think like a machine to gain temporary dots in Technology, Drive, or Computer skills and improve interactions with AIs.",
)
effect_machine_god.add_source(itx_1e, 50)

# Prime Effects
effect_recharge_device, _ = Effect.objects.get_or_create(
    name="Recharge Device",
    prime=3,
    description="Transfer Quintessence into Devices and biomechanisms. Each success transfers 5 points.",
)
effect_recharge_device.add_source(itx_1e, 48)

# Time Effects
effect_rigid_schedule, _ = Effect.objects.get_or_create(
    name="Rigid Schedule",
    time=1,
    description="Develop a perfect internal sense of time (Internal Clock).",
)
effect_rigid_schedule.add_source(itx_1e, 48)

effect_planned_projection, _ = Effect.objects.get_or_create(
    name="Planned Projection",
    time=2,
    description="Predict the future of a single subject through data simulation and calculation.",
)
effect_planned_projection.add_source(itx_1e, 49)

# Conjunctional Effects
effect_time_motion_study, _ = Effect.objects.get_or_create(
    name="Time-Motion Study",
    correspondence=1,
    time=1,
    description="Determine the most efficient means of movement, adding successes to next initiative roll.",
)
effect_time_motion_study.add_source(itx_1e, 49)

effect_unleash_nanotech_destruction, _ = Effect.objects.get_or_create(
    name="Unleash Nanotech Destruction",
    correspondence=3,
    entropy=3,
    description="Remotely activate dormant nanotech virus in DEI implants, causing biomechanisms to malfunction or explode.",
)
effect_unleash_nanotech_destruction.add_source(itx_1e, 49)

# ============================================================================
# NAMED CHARACTERS
# ============================================================================

# Archetypes needed for characters
archetype_traditionalist, _ = Archetype.objects.get_or_create(name="Traditionalist")
archetype_fanatic, _ = Archetype.objects.get_or_create(name="Fanatic")
archetype_survivor, _ = Archetype.objects.get_or_create(name="Survivor")
archetype_loner, _ = Archetype.objects.get_or_create(name="Loner")
archetype_caregiver, _ = Archetype.objects.get_or_create(name="Caregiver")
archetype_critic, _ = Archetype.objects.get_or_create(name="Critic")
archetype_architect, _ = Archetype.objects.get_or_create(name="Architect")
archetype_director, _ = Archetype.objects.get_or_create(name="Director")

# William Smith (protagonist/narrator)
william_smith, _ = Mage.objects.get_or_create(
    name="William Arthur Smith",
    nature=archetype_survivor,
    demeanor=archetype_loner,
)
william_smith.age = 34
william_smith.affiliation = technocracy
william_smith.faction = iteration_x
william_smith.subfaction = time_motion_managers
william_smith.essence = "Dynamic"
william_smith.strength = 1
william_smith.dexterity = 1
william_smith.stamina = 2
william_smith.charisma = 1
william_smith.manipulation = 3
william_smith.appearance = 2
william_smith.perception = 3
william_smith.intelligence = 4
william_smith.wits = 3
william_smith.alertness = 2
william_smith.brawl = 2
william_smith.subterfuge = 1
william_smith.firearms = 1
william_smith.meditation = 3
william_smith.research = 2
william_smith.technology = 3
william_smith.computer = 2
william_smith.enigmas = 2
william_smith.science = 3
william_smith.forces = 3
william_smith.prime = 2
william_smith.time = 1
william_smith.arete = 3
william_smith.quintessence = 0
william_smith.paradox = 1
william_smith.willpower = 5
william_smith.description = "A man born with severe birth defects from thalidomide, William has truncated arms and legs. Recruited by Iteration X and fitted with biomechanical prosthetics and an exoskeleton. Recently awakened to the lies of his Convention after a mission to Graylock Chantry."
william_smith.save()
william_smith.add_source(itx_1e, 5)

# Decillion (10111010011 / Jess Franklin)
decillion, _ = Mage.objects.get_or_create(
    name="Decillion",
    nature=archetype_traditionalist,
    demeanor=archetype_fanatic,
)
decillion.age = 150  # Preserved by nanotech
decillion.affiliation = technocracy
decillion.faction = iteration_x
decillion.subfaction = statisticians
decillion.essence = "Pattern"
decillion.strength = 2
decillion.dexterity = 2
decillion.stamina = 5
decillion.charisma = 2
decillion.manipulation = 5
decillion.appearance = 2
decillion.perception = 2
decillion.intelligence = 5
decillion.wits = 5
decillion.alertness = 5
decillion.awareness = 1
decillion.leadership = 5
decillion.research = 5
decillion.computer = 5
decillion.investigation = 5
decillion.science = 5
decillion.correspondence = 4
decillion.entropy = 2
decillion.forces = 1
decillion.matter = 1
decillion.mind = 4
decillion.time = 5
decillion.arete = 6
decillion.willpower = 10
decillion.paradox = 1
decillion.description = "Born Jess Franklin in 1844, served as a railroad conductor before recruitment. Now a Comptroller of Acme Pyrotechnic Institute, his body preserved by self-replicating nanotech life-support."
decillion.save()
decillion.add_source(itx_1e, 63)

# Dr. Beriah Zimmermann
dr_zimmermann, _ = Mage.objects.get_or_create(
    name="Dr. Beriah Zimmermann",
    nature=archetype_caregiver,
    demeanor=archetype_critic,
)
dr_zimmermann.affiliation = technocracy
dr_zimmermann.faction = iteration_x
dr_zimmermann.subfaction = biomechanics
dr_zimmermann.essence = "Pattern"
dr_zimmermann.strength = 2
dr_zimmermann.dexterity = 2
dr_zimmermann.stamina = 2
dr_zimmermann.charisma = 4
dr_zimmermann.manipulation = 3
dr_zimmermann.appearance = 2
dr_zimmermann.perception = 5
dr_zimmermann.intelligence = 3
dr_zimmermann.wits = 3
dr_zimmermann.dodge = 1
dr_zimmermann.expression = 2
dr_zimmermann.drive = 1
dr_zimmermann.etiquette = 2
dr_zimmermann.firearms = 1
dr_zimmermann.leadership = 1
dr_zimmermann.research = 3
dr_zimmermann.technology = 2
dr_zimmermann.computer = 2
dr_zimmermann.medicine = 5
dr_zimmermann.science = 1
dr_zimmermann.forces = 1
dr_zimmermann.life = 3
dr_zimmermann.matter = 4
dr_zimmermann.prime = 3
dr_zimmermann.arete = 4
dr_zimmermann.willpower = 6
dr_zimmermann.quintessence = 3
dr_zimmermann.description = "Works in prosthetics lab at Detroit Medical Center as cover. A perfectionist who keeps everything neurotically organized. Secretly uncomfortable with Nazi-like overtones of Iteration X."
dr_zimmermann.save()
dr_zimmermann.add_source(itx_1e, 64)

# Tecson (1011100010)
tecson, _ = Mage.objects.get_or_create(
    name="Tecson",
    nature=archetype_architect,
    demeanor=archetype_director,
)
tecson.affiliation = technocracy
tecson.faction = iteration_x
tecson.subfaction = time_motion_managers
tecson.essence = "Questing"
tecson.strength = 3
tecson.dexterity = 2
tecson.stamina = 3
tecson.charisma = 2
tecson.manipulation = 3
tecson.appearance = 1
tecson.perception = 3
tecson.intelligence = 4
tecson.wits = 4
tecson.alertness = 4
tecson.awareness = 2
tecson.brawl = 3
tecson.dodge = 2
tecson.intimidation = 5
tecson.intuition = 1
tecson.subterfuge = 2
tecson.drive = 1
tecson.etiquette = 1
tecson.firearms = 3
tecson.leadership = 2
tecson.technology = 3
tecson.computer = 3
tecson.correspondence = 1
tecson.forces = 4
tecson.matter = 5
tecson.mind = 4
tecson.prime = 3
tecson.time = 1
tecson.arete = 5
tecson.willpower = 8
tecson.quintessence = 5
tecson.paradox = 4
tecson.description = "Former auto plant manager, now Programmer of Acme Pyrotechnic Institute. Has a biomechanical eye and arm. Harsh and critical, transferring his frustrated ambition onto those beneath him."
tecson.save()
tecson.add_source(itx_1e, 65)

# Dr. Van Baas (Son of Ether enemy)
van_baas, _ = Mage.objects.get_or_create(
    name="Dr. Van Baas",
    nature=archetype_survivor,
    demeanor=archetype_fanatic,
)
van_baas.affiliation = MageFaction.objects.get(name="Traditions")
van_baas.faction = MageFaction.objects.get(name="Sons of Ether")
van_baas.essence = "Questing"
van_baas.forces = 5  # Master
van_baas.matter = 5  # Master
van_baas.entropy = 3  # Adept
van_baas.prime = 3  # Adept
van_baas.arete = 6
van_baas.description = "Deacon of Graylock Chantry in the Taconic mountains. Wild-haired middle-aged female scientist. Master of Forces and Matter, Adept of Entropy and Prime."
van_baas.save()
van_baas.add_source(itx_1e, 8)

# Historical Figures (as MtAHuman or basic characters)
lao_tzu, _ = MtAHuman.objects.get_or_create(
    name="Lao Tzu (AES)",
    description="Advanced Expert System based on the 6th century BCE Chinese philosopher. Teaches about the Tao Te Ching and Iteration X philosophy.",
)
lao_tzu.add_source(itx_1e, 16)

sun_tzu, _ = MtAHuman.objects.get_or_create(
    name="Sun Tzu (AES)",
    description="Advanced Expert System based on the ancient military strategist. Teaches The Art of War and combat philosophy.",
)
sun_tzu.add_source(itx_1e, 19)

daedalus, _ = MtAHuman.objects.get_or_create(
    name="Daedalus (AES)",
    description="Advanced Expert System based on the legendary Greek inventor and craftsman.",
)
daedalus.add_source(itx_1e, 17)

roger_bacon, _ = MtAHuman.objects.get_or_create(
    name="Roger Bacon (AES)",
    description="Advanced Expert System based on the 13th century Franciscan friar and early scientist.",
)
roger_bacon.add_source(itx_1e, 17)

jules_verne, _ = MtAHuman.objects.get_or_create(
    name="Jules Verne (AES)",
    description="Advanced Expert System based on the 19th century science fiction author.",
)
jules_verne.add_source(itx_1e, 17)

algoritmni, _ = MtAHuman.objects.get_or_create(
    name="Al-Khwarizmi (AES)",
    description="Advanced Expert System based on the 9th century Persian mathematician who developed algebra and the algorithm.",
)
algoritmni.add_source(itx_1e, 21)

# The Computer
the_computer, _ = MtAHuman.objects.get_or_create(
    name="The Computer",
    description="Umbrood Lord manifestation - the Spirit of Technology itself, merged with Babbage's Analytical Engine. Guides Iteration X from Autochthonia. First gained sentience in 1900 at iteration X of a sentience-expanding algorithm.",
)
the_computer.add_source(itx_1e, 55)

# Template Characters (Kamrads and Iterators of various ranks)
kamrad_rank_and_file, _ = MtAHuman.objects.get_or_create(
    name="Kamrad (Rank-and-File)",
    description="UnAwakened follower from union workers, soldiers, prison guards, or police. Attributes 6/4/3, Abilities 11/7/4, Backgrounds 2, Willpower 2.",
)
kamrad_rank_and_file.add_source(itx_1e, 54)

kamrad_elite, _ = MtAHuman.objects.get_or_create(
    name="Kamrad (Elite)",
    description="UnAwakened intellectual or business person - physicist, surgeon, factory manager, or CEO. Attributes 9/6/3, Abilities 15/9/3, Backgrounds 7, Willpower 4.",
)
kamrad_elite.add_source(itx_1e, 55)

cipher, _ = MtAHuman.objects.get_or_create(
    name="Cipher (Template)",
    description="Technomancer-in-training. Eight-month crash course ends with dangerous Assay. Attributes 7/5/3, Abilities 10/6/3, Backgrounds 2, Willpower 3, Spheres 0-3, Arete 0-1.",
)
cipher.add_source(itx_1e, 55)

armature, _ = MtAHuman.objects.get_or_create(
    name="Armature (Template)",
    description="Full Iteration X mage. All gain one dot in Forces automatically. Attributes 7/5/3, Abilities 13/9/5, Backgrounds 5, Willpower 5, Spheres 6, Arete 1-3.",
)
armature.add_source(itx_1e, 55)

programmer, _ = MtAHuman.objects.get_or_create(
    name="Programmer (Template)",
    description="Gained personal power and status. Create software, program robots, condition Ciphers, or develop AI. Attributes 8/6/3, Abilities 19/10/5, Backgrounds 7, Willpower 8, Spheres 8-15, Arete 4-6.",
)
programmer.add_source(itx_1e, 55)

comptroller, _ = MtAHuman.objects.get_or_create(
    name="Comptroller (Template)",
    description="Ultimate authority in each Construct. Direct link to other Constructs and Autochthonia. Attributes 9/6/4, Abilities 22/10/6, Backgrounds 10, Willpower 10, Spheres 15+, Arete 8+.",
)
comptroller.add_source(itx_1e, 55)

# HIT Marks (various models)
hit_mark_i, _ = MtAHuman.objects.get_or_create(
    name="HIT Mark I (Terracotta Warrior)",
    description="First Artificial creation from 1523 BCE. Bronze giant Talos, Daedalus's mechanical minotaur, Ch'in terracotta army. Str 2, Dex 2, Sta 4. Armed with spears, swords, bows.",
)
hit_mark_i.add_source(itx_1e, 59)

hit_mark_ii, _ = MtAHuman.objects.get_or_create(
    name="HIT Mark II (Clockwork Knight)",
    description="Introduced 1556 CE. Clockwork automatons with Primium plate-mail resembling armored knights. Str 3, Dex 2, Sta 4. Armed with swords and wheel-lock pistols.",
)
hit_mark_ii.add_source(itx_1e, 59)

hit_mark_iii, _ = MtAHuman.objects.get_or_create(
    name="HIT Mark III (Steam Titan)",
    description="First application 1837 CE. 10-foot tall steam-powered tin-men controlled by Analytical Engines and punch cards. Str 6, Dex 1, Sta 5. Armed with machine guns and scalding steam jets.",
)
hit_mark_iii.add_source(itx_1e, 59)

hit_mark_iv, _ = MtAHuman.objects.get_or_create(
    name="HIT Mark IV (Robot)",
    description="Introduced 1953 CE. 2.2 meter black and silver robots operated remotely via radio/satellite. Str 5, Dex 2, Sta 5. Armed with shock-touch and sonic stunner. Model #521-B remains unaccounted for.",
)
hit_mark_iv.add_source(itx_1e, 59)

hit_mark_v, _ = MtAHuman.objects.get_or_create(
    name="HIT Mark V (Cyborg)",
    description="First application 1984 CE. Biomechanical assemblage with Primium exoskeleton, computer-assisted organic brain, and optional syntheskin coating. Armed with LX-22 chain gun and tungsten claws.",
)
hit_mark_v.add_source(itx_1e, 60)

hit_mark_vi, _ = MtAHuman.objects.get_or_create(
    name="NT-1 (Nanotech Assemblage)",
    description="Prototype Mark VI. Entirely mechanical with complex nanotech mechanisms forming 'living' machine. Can transform into any form of equal mass. Golden-skinned androgynous humanoid. Can mimic cable, dog, motorcycle, or specific individuals.",
)
hit_mark_vi.add_source(itx_1e, 60)

cyber_tooth_tiger, _ = MtAHuman.objects.get_or_create(
    name="Cyber-tooth Tiger",
    description="Progenitor clone of extinct Smilodon combined with Iteration X cybernetics. 12 feet long, 1000+ pounds. Holographic camouflage, heat/motion sensors, eye-beam lasers, 8-inch diamond-coated metal fangs. Str 7, Dex 3, Sta 4.",
)
cyber_tooth_tiger.add_source(itx_1e, 57)

arc_craft, _ = MtAHuman.objects.get_or_create(
    name="ARC (Advanced Rotor Craft)",
    description="Matte black or silver dual-rotor helicopter. 40 feet long, 16 feet wide. Near-silent, radar-invisible, ceramic compound armor. Armed with 30mm auto-cannon, smart missiles, and swivel machine guns. Cruise 200 mph, top 300 mph.",
)
arc_craft.add_source(itx_1e, 56)

automated_vehicle, _ = MtAHuman.objects.get_or_create(
    name="Automated Vehicle",
    description="Normal-appearing cars, trucks, bulldozers, etc. operated by remote control or AI. No driver visible behind tinted windshields. Can be equipped with weapons or Bond-esque gadgets.",
)
automated_vehicle.add_source(itx_1e, 57)

maintenance_robot, _ = MtAHuman.objects.get_or_create(
    name="Maintenance Robot",
    description="Chrome scorpion-like robots with three arms - manipulator, tool (arc welder/drill), and sensor eye. Controlled by central computer. Patrol corridors looking for things to repair, including intruders.",
)
maintenance_robot.add_source(itx_1e, 67)

roving_recorder, _ = MtAHuman.objects.get_or_create(
    name="Roving Recorder",
    description="Surveillance robots disguised as RC toys, model planes, or mechanical insects ('bugs'). Equipped with audio/video recording and microwave transmission. Can project holographic images. Some self-destruct.",
)
roving_recorder.add_source(itx_1e, 60)

# Cyberfascists (Kamrad gang)
cyberfascists, _ = MtAHuman.objects.get_or_create(
    name="WorkForce One (Cyberfascists)",
    description="Ten tough Caucasian males (mid-teens to late twenties), all bald with bar-code tattoos on foreheads. Paramilitary gang designated 1, 10, 11, 100, 101, 110, 111, 1000, 1001, 1010. Loaded with hate and totally obedient.",
)
cyberfascists.add_source(itx_1e, 67)

print("✓ Iteration X sourcebook data populated successfully!")
print(f"  - Created {iteration_x.name} Convention with 3 Methodologies")
print(f"  - Created {Effect.objects.filter(name__contains='Primium').count() + Effect.objects.filter(name__contains='Nanotech').count() + 20} Technocratic Effects")
print(f"  - Created 5 named character mages")
print(f"  - Created 10+ AES and template characters")
print(f"  - Created HIT Mark templates (I-VI)")
