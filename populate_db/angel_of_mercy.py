"""
The Angel of Mercy - Story Objects
By Sam Chupp

Extracts characters, items, locations, factions, and effects from the Angel of Mercy scenario.
"""

from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.resonance import Resonance
from core.models import Book
from items.models.mage.artifact import Artifact
from items.models.mage.talisman import Talisman
from items.models.mage.wonder import Wonder
from locations.models.core.location import LocationModel
from locations.models.mage.chantry import Chantry

# ====================
# BOOK
# ====================

book_angel_of_mercy = Book.objects.get_or_create(
    name="The Angel of Mercy",
    gameline="mta",
)[0]
book_angel_of_mercy.description = (
    "A scenario by Sam Chupp featuring themes of deception and the conflict between "
    "the Nephandi, Technocracy, and Traditions over a demon-imprisoning statue."
)
book_angel_of_mercy.save()


# ====================
# FACTIONS
# ====================

# Get Nephandi parent faction
nephandi, _ = MageFaction.objects.get_or_create(name="Nephandi", parent=None)

# Iron Circle - neo-Nazi Odinist diabolist group
iron_circle, _ = MageFaction.objects.get_or_create(
    name="Iron Circle",
    parent=nephandi,
)
iron_circle.description = (
    "A secret society of neo-Nazi Odinist diabolists who were originally part of "
    "Hitler's experimental ritual magicians. The group was officially disbanded after "
    "D-Day but secretly continued operations, practicing Odinist rituals and dark magic. "
    "Based in Berlin/Germany, they seek powerful artifacts and demons to further their goals."
)
iron_circle.founded = 1933
iron_circle.add_source(book_angel_of_mercy.name, 0)
iron_circle.save()


# ====================
# LOCATIONS
# ====================

# Val du Bosque, Provençal, France
val_du_bosque = LocationModel.objects.get_or_create(
    name="Val du Bosque",
)[0]
val_du_bosque.description = (
    "A region in Provençal, France, once a stronghold of Celestial Chorus activity. "
    "In the 11th century, the Cathar 'heretics' of the region sheltered many wandering "
    "Choirmages. This area was the site where a greater demon was accidentally released "
    "by Order of Hermes mages and subsequently imprisoned by Celestial Chorus mages."
)
val_du_bosque.add_source(book_angel_of_mercy.name, 0)
val_du_bosque.save()

# Church of St. Martin in Mercille
church_st_martin = LocationModel.objects.get_or_create(
    name="Church of St. Martin",
)[0]
church_st_martin.description = (
    "A church in the village of Mercille, France. In A.D. 1171, Celestial Chorus mages "
    "lured a greater demon here and imprisoned it within a white marble statue of a Seraph "
    "given by the Pope. The church became a site of pilgrimage for Choristers who would "
    "watch over the imprisoned demon."
)
church_st_martin.parent = val_du_bosque
church_st_martin.add_source(book_angel_of_mercy.name, 0)
church_st_martin.save()

# Notre Dame Cathedral, Strasbourg
notre_dame_strasbourg = LocationModel.objects.get_or_create(
    name="Notre Dame Cathedral, Strasbourg",
)[0]
notre_dame_strasbourg.description = (
    "Cathedral in Strasbourg, France, where the Angel of Mercille statue was held "
    "after World War II until it was auctioned off to finance cathedral renovations."
)
notre_dame_strasbourg.add_source(book_angel_of_mercy.name, 0)
notre_dame_strasbourg.save()

# Angel Fountain Mall
angel_fountain_mall = LocationModel.objects.get_or_create(
    name="Angel Fountain Mall",
)[0]
angel_fountain_mall.description = (
    "A renovated shopping mall built on the site of a failed downtown shopping area. "
    "Opened by real-estate developer Michael Wellington, the mall's centerpiece is the "
    "Angel of Mercille statue placed in an atrium fountain. The mall became the site of "
    "ritual murders, gang activity, and ultimately a major conflict between the Nephandi "
    "and Technocracy. The area around the fountain has a Paradox rating of 1, increasing "
    "to 3 during major events."
)
angel_fountain_mall.gauntlet = 7
angel_fountain_mall.add_source(book_angel_of_mercy.name, 0)
angel_fountain_mall.save()

# Iron Circle Chantry
iron_circle_chantry = Chantry.objects.get_or_create(
    name="Iron Circle Chantry",
)[0]
iron_circle_chantry.description = (
    "The secret Chantry of the Iron Circle in Berlin, Germany. This is where Kjarl "
    "Nordsen and other members practice their Odinist rituals and conduct dark magic. "
    "The Chantry serves as a base for operations seeking powerful artifacts and demons."
)
iron_circle_chantry.faction = iron_circle
iron_circle_chantry.add_source(book_angel_of_mercy.name, 0)
iron_circle_chantry.save()


# ====================
# EFFECTS
# ====================

# Ward-breaking ritual effect
effect_ward_breaking_ritual = Effect.objects.get_or_create(
    name="Ward-Breaking Ritual (Demon Prison)",
    spirit=4,
    prime=4,
    correspondence=3,
    entropy=3,
    life=3,
    matter=3,
)[0]
effect_ward_breaking_ritual.description = (
    "A complex ritual designed to destroy wards imprisoning a greater demon. "
    "The effect requires Correspondence (cast at distance), Prime (raw Quintessence to break wards), "
    "Spirit (re-form demon's spiritual body), Matter and Life (blood as physical focus), "
    "and Entropy (erode static pattern and fuel demon's negative energies). "
    "Takes approximately 36 hours and uses runes as foci."
)
effect_ward_breaking_ritual.add_source(book_angel_of_mercy.name, 0)
effect_ward_breaking_ritual.save()

# Mind/Correspondence psychic scan
effect_psychic_scan = Effect.objects.get_or_create(
    name="Remote Psychic Scan",
    correspondence=2,
    mind=3,
)[0]
effect_psychic_scan.description = (
    "Allows the mage to scan a target's mind at a distance to discern their nature, "
    "identity, and capabilities. Used by Kjarl Nordsen to assess potential threats."
)
effect_psychic_scan.add_source(book_angel_of_mercy.name, 0)
effect_psychic_scan.save()

# Umbral teleportation
effect_umbral_teleport = Effect.objects.get_or_create(
    name="Umbral Teleportation",
    spirit=3,
    correspondence=3,
)[0]
effect_umbral_teleport.description = (
    "Shifts a target into the Umbra and allows a spirit to carry them to a predetermined "
    "location. Used as an escape mechanism."
)
effect_umbral_teleport.description
effect_umbral_teleport.add_source(book_angel_of_mercy.name, 0)
effect_umbral_teleport.save()

# Rune creation effect (for one-shot Talismans)
effect_create_ward_rune = Effect.objects.get_or_create(
    name="Create Ward-Breaking Rune",
    spirit=4,
    prime=4,
    correspondence=3,
    entropy=3,
    life=3,
    matter=3,
)[0]
effect_create_ward_rune.description = (
    "Creates a physical rune that serves as a focus for ward-breaking energies. "
    "The rune is scribed with a one-shot Talisman (iron spike with diamond tip) and "
    "contains 4 points of Quintessence to fuel the magickal pattern."
)
effect_create_ward_rune.add_source(book_angel_of_mercy.name, 0)
effect_create_ward_rune.save()

# Entropy bolt (demon attack)
effect_entropy_bolt_rank4 = Effect.objects.get_or_create(
    name="Entropy Bolt (Rank 4)",
    entropy=4,
)[0]
effect_entropy_bolt_rank4.description = (
    "A bolt of pure Entropy that inflicts decay and dissolution. Used by the greater "
    "demon imprisoned in the Angel statue."
)
effect_entropy_bolt_rank4.add_source(book_angel_of_mercy.name, 0)
effect_entropy_bolt_rank4.save()

# Mind communication (via device)
effect_mind_comm_tech = Effect.objects.get_or_create(
    name="Mind Communication via Technology",
    mind=2,
    correspondence=2,
)[0]
effect_mind_comm_tech.description = (
    "Allows communication through technological devices (digital watches, computers, "
    "radios, etc.). Used by Technomancers to interrogate mages. Sleepers cannot hear "
    "this Mind-based communication."
)
effect_mind_comm_tech.add_source(book_angel_of_mercy.name, 0)
effect_mind_comm_tech.save()

# Video feed redirect (Jody Kramer's instinctive effect)
effect_video_redirect = Effect.objects.get_or_create(
    name="Instinctive Video Feed Redirect",
    correspondence=3,
)[0]
effect_video_redirect.description = (
    "An instinctive Correspondence effect that pipes video directly into a broadcast "
    "feed, bypassing normal transmission. Used by Jody Kramer when she Awakens."
)
effect_video_redirect.add_source(book_angel_of_mercy.name, 0)
effect_video_redirect.save()

# Blood transmutation (part of ward-breaking)
effect_blood_transmutation = Effect.objects.get_or_create(
    name="Water to Blood Transmutation",
    prime=3,
    life=3,
    correspondence=3,
)[0]
effect_blood_transmutation.description = (
    "Transmutes water into blood through a long-distance ritual. Part of the ward-breaking "
    "ritual that provides a physical focus for the demon's manifestation. Takes 36 hours "
    "and uses channeled Quintessence through runic foci."
)
effect_blood_transmutation.add_source(book_angel_of_mercy.name, 0)
effect_blood_transmutation.save()


# ====================
# ITEMS - ARTIFACTS
# ====================

# Angel of Mercille Statue
angel_statue = Artifact.objects.get_or_create(
    name="Angel of Mercille",
    rank=5,
    background_cost=10,
)[0]
angel_statue.description = (
    "A statue of purest white marble depicting a beautiful Seraph with wings unfurled "
    "and face cast downward, looking vigilant and pensive. Given by the Pope to the "
    "Church of St. Martin in Mercille, France. In A.D. 1171, Celestial Chorus mages "
    "imprisoned a greater demon within this statue through tremendous sacrifice. "
    "The statue also houses an angelic spirit. When examined closely, it emanates "
    "powerful malefic energy. The demon was deemed too powerful to banish and remains "
    "imprisoned unless powerful ward-breaking rituals are performed."
)
angel_statue.quintessence_max = 50
angel_statue.add_source(book_angel_of_mercy.name, 0)

# Add resonances
malefic_res, _ = Resonance.objects.get_or_create(name="Malefic")
entropic_res, _ = Resonance.objects.get_or_create(name="Entropic")
holy_res, _ = Resonance.objects.get_or_create(name="Holy")
ancient_res, _ = Resonance.objects.get_or_create(name="Ancient")

angel_statue.add_resonance(malefic_res)
angel_statue.add_resonance(malefic_res)
angel_statue.add_resonance(malefic_res)  # Very strong malefic presence
angel_statue.add_resonance(entropic_res)
angel_statue.add_resonance(entropic_res)
angel_statue.add_resonance(holy_res)  # From the angel
angel_statue.add_resonance(ancient_res)
angel_statue.save()


# ====================
# ITEMS - TALISMANS
# ====================

# Marko's Iron Chain
markos_chain = Talisman.objects.get_or_create(
    name="Iron Chain of the Blood Lords",
    rank=3,
    background_cost=6,
)[0]
markos_chain.description = (
    "A chain of iron that grants its wearer exceptional protection against magick. "
    "Grants +3 dice to Willpower rolls to resist direct magickal attacks. Grows cold "
    "when magick is used nearby. Can be detached and used as a weapon (manriki-gusari "
    "style), inflicting aggravated damage. Allows the wearer to contact Kjarl Nordsen "
    "via a conjunctional Correspondence/Mind effect (takes one turn of concentration). "
    "A Talisman and symbol of Marko's partial initiation into the Iron Circle."
)
markos_chain.quintessence_max = 10
markos_chain.arete = 3
markos_chain.add_source(book_angel_of_mercy.name, 0)

# Add powers
markos_chain.powers.add(effect_psychic_scan)  # Communication aspect

dark_res, _ = Resonance.objects.get_or_create(name="Dark")
protective_res, _ = Resonance.objects.get_or_create(name="Protective")
markos_chain.add_resonance(dark_res)
markos_chain.add_resonance(dark_res)
markos_chain.add_resonance(entropic_res)
markos_chain.add_resonance(protective_res)
markos_chain.save()

# Iron Spike with Diamond Tip (Ward-Breaking Rune Talisman)
# One-shot Talisman - multiple were created
iron_spike_talisman = Talisman.objects.get_or_create(
    name="Iron Spike with Diamond Tip (Ward Rune)",
    rank=4,
    background_cost=8,
)[0]
iron_spike_talisman.description = (
    "A one-shot Talisman crafted by the Iron Circle for Kjarl Nordsen's ward-breaking "
    "ritual. The spike has a diamond tip and contains 4 points of Quintessence. "
    "When used to scribe a rune on marble (or other surface), it creates a permanent "
    "magickal pattern that serves as a focus for the ward-breaking ritual. Six runes "
    "are needed, forming a hexagonal pattern and six-pointed star. Once used, the "
    "Quintessence is discharged and the Talisman is spent."
)
iron_spike_talisman.quintessence_max = 4
iron_spike_talisman.arete = 4
iron_spike_talisman.add_source(book_angel_of_mercy.name, 0)
iron_spike_talisman.powers.add(effect_create_ward_rune)
iron_spike_talisman.save()


# ====================
# ITEMS - WONDERS
# ====================

# Kjarl's Swastika Necklace (Focus)
swastika_necklace = Wonder.objects.get_or_create(
    name="Swastika Necklace (Odinist Focus)",
    rank=2,
    background_cost=4,
)[0]
swastika_necklace.description = (
    "A swastika necklace used by Kjarl Nordsen as a focus for Forces, Spirit, and Prime "
    "magick. An Odinist symbol of the Iron Circle."
)
swastika_necklace.quintessence_max = 5
swastika_necklace.add_source(book_angel_of_mercy.name, 0)
swastika_necklace.save()

# Kjarl's Nazi Dagger (Focus)
nazi_dagger = Wonder.objects.get_or_create(
    name="Nazi Ritual Dagger",
    rank=2,
    background_cost=4,
)[0]
nazi_dagger.description = (
    "A ritual dagger used by Kjarl Nordsen as a focus for Life and Entropy magick. "
    "Bears Nazi insignia and is used in dark rituals."
)
nazi_dagger.quintessence_max = 5
nazi_dagger.add_source(book_angel_of_mercy.name, 0)
nazi_dagger.add_resonance(dark_res)
nazi_dagger.add_resonance(entropic_res)
nazi_dagger.save()

# Kjarl's Monocle (Focus)
monocle_focus = Wonder.objects.get_or_create(
    name="Monocle of Mental Piercing",
    rank=2,
    background_cost=4,
)[0]
monocle_focus.description = (
    "A monocle used by Kjarl Nordsen as a focus for Mind magick. Aids in mental "
    "perception and psychic scanning."
)
monocle_focus.quintessence_max = 5
monocle_focus.add_source(book_angel_of_mercy.name, 0)
monocle_focus.save()


# ====================
# CHARACTERS - MAGES
# ====================

# Kjarl Nordsen - Diabolic Nephandus, Adept of the Iron Circle
kjarl = Mage.objects.get_or_create(name="Kjarl Nordsen")[0]
kjarl.description = (
    "A powerful Nephandus and Adept of the Iron Circle. Son of Thor Nordsen, one of "
    "the original Iron Circle members who escaped war crimes trials. Kjarl seeks to "
    "capture and bind the greater demon imprisoned in the Angel of Mercille statue. "
    "He has made pacts with demons and employs three servitor demons. Currently conducting "
    "a complex ward-breaking ritual to free the demon. Kjarl is a formidable opponent "
    "with mastery over multiple Spheres and no qualms about sacrificing others for power."
)
kjarl.nature = "Fanatic"
kjarl.demeanor = "Deviant"
kjarl.concept = "Diabolic Nephandus"

# Attributes
kjarl.strength = 3
kjarl.dexterity = 4
kjarl.stamina = 4
kjarl.charisma = 4
kjarl.manipulation = 3
kjarl.appearance = 1
kjarl.perception = 3
kjarl.intelligence = 4
kjarl.wits = 3

# Abilities
kjarl.alertness = 2
kjarl.athletics = 2
kjarl.awareness = 4
kjarl.brawl = 4
kjarl.dodge = 3
kjarl.expression = 3
kjarl.intimidation = 4
kjarl.intuition = 4
kjarl.subterfuge = 4
kjarl.streetwise = 3

kjarl.drive = 2
kjarl.etiquette = 3
kjarl.firearms = 2
kjarl.leadership = 4
kjarl.meditation = 4
kjarl.melee = 4
kjarl.research = 3
kjarl.stealth = 4
kjarl.technology = 3

kjarl.computer = 1
kjarl.cosmology = 4
kjarl.enigmas = 3
kjarl.investigation = 2
kjarl.law = 2
kjarl.medicine = 4
kjarl.occult = 5
kjarl.science = 3

# Backgrounds
kjarl.allies = 4  # Iron Circle
kjarl.arcane = 4
kjarl.avatar = 5
kjarl.dream = 2
kjarl.influence = 2
kjarl.mentor = 3

# Spheres
kjarl.correspondence = 4
kjarl.entropy = 4
kjarl.forces = 2
kjarl.life = 4
kjarl.mind = 4
kjarl.matter = 4
kjarl.prime = 3
kjarl.spirit = 4
kjarl.time = 1

kjarl.arete = 6
kjarl.willpower = 8
kjarl.quintessence = 7
kjarl.paradox = 5

kjarl.affiliation = iron_circle
kjarl.faction = iron_circle

kjarl.add_source(book_angel_of_mercy.name, 0)
kjarl.save()

# Jody Kramer - Newly Awakened Orphan (Potential Virtual Adept)
jody = Mage.objects.get_or_create(name="Jody Kramer")[0]
jody.description = (
    "A television news reporter for 'Eyewitness Newsline'. Jody is tenacious and "
    "dedicated to getting the truth, even if it costs her job. While covering the "
    "Angel Fountain Mall blood fountain story, she Awakened as an Orphan mage during "
    "a moment of intense conflict with the Technocracy. Her Avatar manifested the "
    "ability to use Correspondence magick instinctively, piping her video feed directly "
    "into the six o'clock news broadcast. The Technocracy sees her as a major threat - "
    "a member of the media with the ability to see past Paradox. Without guidance, she "
    "may be 'dealt with' by the Technocracy or recruited by the Traditions."
)
jody.nature = "Visionary"
jody.demeanor = "Critic"
jody.concept = "Investigative Reporter"

# Attributes (slightly above average human)
jody.strength = 2
jody.dexterity = 3
jody.stamina = 2
jody.charisma = 3
jody.manipulation = 3
jody.appearance = 3
jody.perception = 4
jody.intelligence = 3
jody.wits = 4

# Abilities
jody.alertness = 3
jody.athletics = 1
jody.awareness = 2
jody.expression = 3
jody.intuition = 3
jody.streetwise = 2
jody.subterfuge = 2

jody.drive = 2
jody.etiquette = 2
jody.research = 3
jody.technology = 3

jody.academics = 2
jody.computer = 3
jody.investigation = 4
jody.media = 4
jody.politics = 2

# Backgrounds
jody.contacts = 3
jody.resources = 2

# Spheres (just Awakened, very limited)
jody.correspondence = 1  # Instinctive manifestation
jody.forces = 1  # Potential

jody.arete = 1
jody.willpower = 6
jody.quintessence = 4
jody.essence = "Questing"

jody.add_source(book_angel_of_mercy.name, 0)
jody.save()


# ====================
# CHARACTERS - MtAHumans (Acolytes and Sleepers)
# ====================

# Marko - Neo-Nazi Diabolist Gangster Acolyte
marko = MtAHuman.objects.get_or_create(name="Marko")[0]
marko.description = (
    "A neo-Nazi diabolist gangster and Acolyte to Kjarl Nordsen. Marko is an immense, "
    "Aryan-looking man with shocking white hair and a swastika branded into his shoulder. "
    "Originally a street punk, he was befriended by Kjarl and taken to Germany where he "
    "witnessed the secret rituals of the Iron Circle. He returned to America to serve "
    "Kjarl's mission, performing ritual murders to enchant the ground around Angel Fountain "
    "Mall. Marko leads the Blood Lords gang and wields a powerful iron chain Talisman. "
    "He is cold, frigid, and shark-like in demeanor, letting nothing rattle him. "
    "Unknown to Kjarl, the pact demon has begun recruiting Marko's loyalty through dreams, "
    "grooming him to potentially replace Kjarl."
)
marko.nature = "Bravo"
marko.demeanor = "Monster"
marko.concept = "Neo-Nazi Diabolist Gangster"

# Attributes
marko.strength = 5
marko.dexterity = 4
marko.stamina = 3
marko.charisma = 4
marko.manipulation = 2
marko.appearance = 2
marko.perception = 4
marko.intelligence = 2
marko.wits = 4

# Abilities
marko.alertness = 3
marko.athletics = 4
marko.awareness = 2
marko.brawl = 4
marko.intimidation = 4
marko.streetwise = 4
marko.subterfuge = 4

marko.drive = 2
marko.firearms = 3
marko.leadership = 4
marko.melee = 3
marko.stealth = 2
marko.survival = 3

marko.law = 1
marko.medicine = 1
marko.occult = 3

# Backgrounds
marko.contacts = 3
marko.allies = 1
marko.mentor = 3  # Kjarl

marko.willpower = 9

marko.add_source(book_angel_of_mercy.name, 0)
marko.save()

# Blood Lords Gang Member Template
blood_lord_template = MtAHuman.objects.get_or_create(name="Blood Lord Gang Member")[0]
blood_lord_template.description = (
    "Members of the Blood Lords, a neo-Nazi Satanist gang led by Marko. They wear red "
    "jackets with swastikas and inverted pentagrams. The gang has 22 members total. "
    "They have sworn their lives to Marko and think of themselves as 'an elite urban "
    "fighting force for the Führer.' They are armed with chains, tonfas, knives, and "
    "handguns (Colt Anacondas, one member has a Glock 20 as a gift from Marko)."
)
blood_lord_template.nature = "Soldier"
blood_lord_template.demeanor = "Fanatic"
blood_lord_template.concept = "Neo-Nazi Gang Member"

# Attributes
blood_lord_template.strength = 3
blood_lord_template.dexterity = 3
blood_lord_template.stamina = 2
blood_lord_template.charisma = 2
blood_lord_template.manipulation = 2
blood_lord_template.appearance = 2
blood_lord_template.perception = 2
blood_lord_template.intelligence = 2
blood_lord_template.wits = 3

# Abilities
blood_lord_template.alertness = 2
blood_lord_template.athletics = 2
blood_lord_template.brawl = 3
blood_lord_template.dodge = 3
blood_lord_template.streetwise = 3

blood_lord_template.drive = 1
blood_lord_template.firearms = 3
blood_lord_template.melee = 2

blood_lord_template.law = 1
blood_lord_template.medicine = 1

blood_lord_template.willpower = 5

blood_lord_template.add_source(book_angel_of_mercy.name, 0)
blood_lord_template.save()

# Thor Nordsen - Kjarl's father, original Iron Circle member
thor = MtAHuman.objects.get_or_create(name="Thor Nordsen")[0]
thor.description = (
    "An Odinist from the original Iron Circle research group formed during Hitler's regime. "
    "Father of Kjarl Nordsen. Thor was one of the diabolists who escaped war crimes trials "
    "after WWII using coincidental magick. He traced the Angel of Mercille to Strasbourg "
    "after the war, recognizing it as an Infernal object of great power. Thor trained his "
    "son Kjarl in the ways of the Iron Circle."
)
thor.nature = "Fanatic"
thor.demeanor = "Traditionalist"
thor.concept = "Nazi Occultist (Retired)"
thor.add_source(book_angel_of_mercy.name, 0)
thor.save()

# Johann Landouer - original Iron Circle member
johann = MtAHuman.objects.get_or_create(name="Johann Landouer")[0]
johann.description = (
    "An Odinist from the original Iron Circle research group. Along with Thor Nordsen, "
    "Johann escaped war crimes trials after WWII and continued to practice Odinist rituals "
    "in secret. He helped trace the Angel of Mercille statue after the war."
)
johann.nature = "Deviant"
johann.demeanor = "Traditionalist"
johann.concept = "Nazi Occultist (Retired)"
johann.add_source(book_angel_of_mercy.name, 0)
johann.save()

# Michael Wellington - Real Estate Developer (Sleeper)
wellington = MtAHuman.objects.get_or_create(name="Michael Wellington")[0]
wellington.description = (
    "A fairly successful real-estate developer who opened the Angel Fountain Mall on the "
    "site of a failed downtown shopping area. On vacation in France, he became seized with "
    "the idea of making the Angel of Mercille statue the centerpiece of his new development. "
    "He purchased the statue before auction and had it shipped on his private jet. Wellington "
    "refused Kjarl Nordsen's offers to purchase the statue. Under constant surveillance by "
    "the Syndicate due to his business holdings. Unaware of the supernatural significance "
    "of the statue."
)
wellington.nature = "Capitalist"
wellington.demeanor = "Director"
wellington.concept = "Real Estate Developer"
wellington.resources = 4
wellington.add_source(book_angel_of_mercy.name, 0)
wellington.save()

# Jorge Hernandez - Maintenance Worker (Sleeper)
jorge = MtAHuman.objects.get_or_create(name="Jorge Hernandez")[0]
jorge.description = (
    "A maintenance worker at Angel Fountain Mall who was involved in cleaning the bloody "
    "fountain. Despite Wellington's threats of termination, Jorge contacted reporter "
    "Jody Kramer with his blood-soaked overalls as evidence. He had little to lose by "
    "going to the media and potentially much to gain. A police check cleared him of any "
    "wrongdoing."
)
jorge.nature = "Survivor"
jorge.demeanor = "Conformist"
jorge.concept = "Maintenance Worker"
jorge.contacts = 1
jorge.add_source(book_angel_of_mercy.name, 0)
jorge.save()

# Dylanoor - Ancient Druid Spirit (Historical Character)
dylanoor = MtAHuman.objects.get_or_create(name="Dylanoor (Spirit)")[0]
dylanoor.description = (
    "An ancient Druid who originally banished the greater demon that would later be "
    "imprisoned in the Angel of Mercille statue. His spirit may contact Verbena mages "
    "to help them spiritually throughout the story. Dylanoor exists primarily as a "
    "spirit guide from ages past."
)
dylanoor.nature = "Judge"
dylanoor.demeanor = "Sage"
dylanoor.concept = "Ancient Druid Spirit"
dylanoor.add_source(book_angel_of_mercy.name, 0)
dylanoor.save()


# ====================
# RESONANCES
# ====================

# Create any additional resonances referenced in the story
infernal_res, _ = Resonance.objects.get_or_create(name="Infernal")
malicious_res, _ = Resonance.objects.get_or_create(name="Malicious")
corrupt_res, _ = Resonance.objects.get_or_create(name="Corrupt")
guardian_res, _ = Resonance.objects.get_or_create(name="Guardian")
vigilant_res, _ = Resonance.objects.get_or_create(name="Vigilant")

# Add sources
for res in [infernal_res, malicious_res, corrupt_res, guardian_res, vigilant_res]:
    res.add_source(book_angel_of_mercy.name, 0)
    res.save()


print("The Angel of Mercy objects created successfully!")
print(f"- Book: {book_angel_of_mercy.name}")
print(f"- Factions: {iron_circle.name}")
print(f"- Locations: 5 locations created")
print(f"- Effects: 8 effects created")
print(f"- Artifacts: {angel_statue.name}")
print(f"- Talismans: {markos_chain.name}, {iron_spike_talisman.name}")
print(f"- Wonders: 3 focus items created")
print(f"- Mages: {kjarl.name}, {jody.name}")
print(f"- MtAHumans/Acolytes: {marko.name}, {blood_lord_template.name}, and 5 others")
print("All objects from The Angel of Mercy have been extracted!")
