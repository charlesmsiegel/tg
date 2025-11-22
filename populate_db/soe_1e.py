"""
Sons of Ether Tradition Book (1st Edition) - Paradigma Journal
Populates characters, wonders, rotes, locations, and other game objects
"""

from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.faction import MageFaction
from characters.models.core.ability_block import Ability
from characters.models.core.specialty import Specialty
from characters.models.core.meritflaw import MeritFlaw
from items.models.mage.wonder import Wonder
from items.models.mage.artifact import Artifact
from items.models.mage.talisman import Talisman
from locations.models.mage.chantry import Chantry
from locations.models.mage.node import Node
from locations.models.mage.library import Library
from core.models import Book
from game.models import ObjectType


def add_source():
    """Add the sourcebook"""
    soe, _ = Book.objects.get_or_create(
        title="Sons of Ether Tradition Book",
        defaults={
            "type": "mage",
            "edition": 1,
            "year": 1994,
        }
    )
    return soe


def create_factions(soe):
    """Create Sons of Ether subfactions"""

    # Main Tradition
    sons_of_ether, _ = MageFaction.objects.get_or_create(
        name="Sons of Ether",
        defaults={
            "description": "Scientists dedicated to progressive science and grand theories"
        }
    )
    sons_of_ether.add_source("Sons of Ether Tradition Book", parent_name="Traditions")

    # Subfactions
    ethernauts, _ = MageFaction.objects.get_or_create(
        name="Ethernauts",
        parent=sons_of_ether,
        defaults={
            "description": "Scientists obsessed with exploration of Etherspace and the unknown reaches"
        }
    )
    ethernauts.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    utopians, _ = MageFaction.objects.get_or_create(
        name="Utopians",
        parent=sons_of_ether,
        defaults={
            "description": "Dedicated to Science for the betterment of humankind and a better tomorrow"
        }
    )
    utopians.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    cybernauts, _ = MageFaction.objects.get_or_create(
        name="Cybernauts",
        parent=sons_of_ether,
        defaults={
            "description": "Also called Webslingers, obsessed with the Digital Web as the next battleground"
        }
    )
    cybernauts.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    progressivists, _ = MageFaction.objects.get_or_create(
        name="Progressivists",
        parent=sons_of_ether,
        defaults={
            "description": "Reformers seeking to change Victorian standards and equalize power in the Tradition"
        }
    )
    progressivists.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    traditionalists, _ = MageFaction.objects.get_or_create(
        name="Traditionalists",
        parent=sons_of_ether,
        defaults={
            "description": "Conservative Scientists who resist change to the Tradition's structure"
        }
    )
    traditionalists.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    mad_scientists, _ = MageFaction.objects.get_or_create(
        name="Mad Scientists",
        parent=sons_of_ether,
        defaults={
            "description": "Obsessed with their theories to exclusion of ethics and common sense"
        }
    )
    mad_scientists.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    adventurers, _ = MageFaction.objects.get_or_create(
        name="Adventurers",
        parent=sons_of_ether,
        defaults={
            "description": "Also called Pulp Heroes, embrace cliff-hanger serials and ray gun adventures"
        }
    )
    adventurers.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    # Historical organization
    electrodyne, _ = MageFaction.objects.get_or_create(
        name="Electrodyne Engineers",
        defaults={
            "description": "Precursor to Sons of Ether, founded 1865, defected from Technocracy in 1904"
        }
    )
    electrodyne.add_source("Sons of Ether Tradition Book", "The Birth of True Science")

    return sons_of_ether


def create_characters(soe):
    """Create named Sons of Ether characters"""

    # Doctor Eon - "The Man of Many Tomorrows"
    doctor_eon, _ = Mage.objects.get_or_create(
        name="Doctor Eon",
        defaults={
            "description": "Master of many Sciences and Spheres, especially Life and Time. "
                         "Hero of pulp adventures from 1935-1951. Known for physical superiority "
                         "and scientific regimen. Supposedly died in 1951 but may still live in the future.",
            "willpower": 9,
            "arete": 5,
            "essence": "Questing",
            "faction_name": "Sons of Ether",
        }
    )
    doctor_eon.resonance.set_resonance({"dynamic": 3, "static": 2})
    doctor_eon.spheres.set_rank("life", 5)
    doctor_eon.spheres.set_rank("time", 5)
    doctor_eon.spheres.set_rank("forces", 4)
    doctor_eon.spheres.set_rank("matter", 4)
    doctor_eon.spheres.set_rank("correspondence", 3)
    doctor_eon.add_source("Sons of Ether Tradition Book", "The Birth of True Science")

    # Joe "Lucky Skunk" Ross - Terrific Trio member
    joe_ross, _ = MtAHuman.objects.get_or_create(
        name='Joe "Lucky Skunk" Ross',
        defaults={
            "description": "Acolyte and member of Doctor Eon's Terrific Trio. Expert in electricity, "
                         "jack-of-all-trades. Author of pulp accounts of Doc Eon's adventures. "
                         "Large, strong, but clever despite his humble manner.",
        }
    )
    joe_ross.add_source("Sons of Ether Tradition Book", "Into the Hollow Earth")

    # Frank "Bull" Barrett - Terrific Trio member
    bull_barrett, _ = MtAHuman.objects.get_or_create(
        name='Frank "Bull" Barrett',
        defaults={
            "description": "Member of Doctor Eon's Terrific Trio. Expert in physics and mechanical engineering.",
        }
    )
    bull_barrett.add_source("Sons of Ether Tradition Book", "Into the Hollow Earth")

    # Simon "Sesquipedalian" Smith - Terrific Trio member
    simon_smith, _ = MtAHuman.objects.get_or_create(
        name='Simon "Sesquipedalian" Smith',
        defaults={
            "description": "Member of Doctor Eon's Terrific Trio. Expert mathematician and astronomer. "
                         "Known for using long, obscure words.",
        }
    )
    simon_smith.add_source("Sons of Ether Tradition Book", "Into the Hollow Earth")

    # Czar Vargo
    czar_vargo, _ = Mage.objects.get_or_create(
        name="Czar Vargo",
        defaults={
            "description": "Greatest Son of Ether, missing since 1914. Born son of Black Sea fisherman, "
                         "showed genius early. Inventor of the Conversion Engine. Attempted to seize "
                         "world leadership in 1914 to prevent war, forced to retreat. Possibly commands "
                         "fleet in Deep Umbra. Master of Forces.",
            "willpower": 10,
            "arete": 6,
            "essence": "Dynamic",
            "faction_name": "Sons of Ether",
        }
    )
    czar_vargo.resonance.set_resonance({"dynamic": 5})
    czar_vargo.spheres.set_rank("forces", 6)
    czar_vargo.spheres.set_rank("matter", 5)
    czar_vargo.spheres.set_rank("prime", 5)
    czar_vargo.add_source("Sons of Ether Tradition Book", "The Birth of True Science")

    # Count Roland
    count_roland, _ = Mage.objects.get_or_create(
        name="Count Roland",
        defaults={
            "description": "Doctor in Sons of Ether who discovered young Czar Vargo when the boy was 12. "
                         "Mentor to Vargo.",
            "faction_name": "Sons of Ether",
        }
    )
    count_roland.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    # Professor Elias (Frankenstein's Monster)
    elias, _ = Mage.objects.get_or_create(
        name="Professor Elias",
        defaults={
            "description": "Created by Doctor Waldman from dead flesh. The being Mary Shelley used as "
                         "model for Frankenstein's monster. Fled to Hollow Earth, studied with Goro monks, "
                         "Awakened. Returned to find creator dead. Now studies in far north. Virtuous "
                         "despite reputation. Near-ageless.",
            "willpower": 8,
            "arete": 4,
            "essence": "Primordial",
            "faction_name": "Sons of Ether",
        }
    )
    elias.spheres.set_rank("life", 5)
    elias.spheres.set_rank("matter", 4)
    elias.spheres.set_rank("prime", 3)
    elias.add_source("Sons of Ether Tradition Book", "A Much-Maligned Monster")

    # Doctor Waldman
    waldman, _ = Mage.objects.get_or_create(
        name="Doctor Waldman",
        defaults={
            "description": "Austrian Son of Ether who created life from dead matter. Creator of Elias. "
                         "Killed by peasant mob who burned his castle. Had caustic, sexist personality. "
                         "May have aided Byron and Shelley against vampires.",
            "faction_name": "Sons of Ether",
            "status": "Dec",  # Deceased
        }
    )
    waldman.spheres.set_rank("life", 5)
    waldman.spheres.set_rank("matter", 4)
    waldman.add_source("Sons of Ether Tradition Book", "A Much-Maligned Monster")

    # Doctor Alexis Hastings
    alexis, _ = Mage.objects.get_or_create(
        name="Doctor Alexis Hastings",
        defaults={
            "description": "Physical chemist fascinated by alchemy and electricity. Believes electricity "
                         "is key to transformation. Tinkerer who loves to manipulate devices. Enthusiastic "
                         "contributor to Paradigma. Advocates collaboration. Studies Matter and Forces "
                         "almost exclusively. Shy and conservative to strangers, energetic with friends.",
            "willpower": 7,
            "arete": 4,
            "essence": "Dynamic",
            "faction_name": "Sons of Ether",
        }
    )
    alexis.spheres.set_rank("matter", 4)
    alexis.spheres.set_rank("forces", 4)
    alexis.spheres.set_rank("correspondence", 2)
    alexis.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    # Captain Tiberius
    captain_tiberius, _ = Mage.objects.get_or_create(
        name="Captain Tiberius",
        defaults={
            "description": "Commander of the starship Etherjammer. Ethernaut exploring space. "
                         "Leads expeditions to mysterious Planet X. Has built close-knit team of acolytes. "
                         "Uses Velikovsky's theories for navigation.",
            "willpower": 8,
            "arete": 4,
            "faction_name": "Sons of Ether",
        }
    )
    captain_tiberius.spheres.set_rank("correspondence", 4)
    captain_tiberius.spheres.set_rank("forces", 3)
    captain_tiberius.spheres.set_rank("spirit", 3)
    captain_tiberius.add_source("Sons of Ether Tradition Book", "The Birth of True Science")

    # Arerus
    arerus, _ = Mage.objects.get_or_create(
        name="Arerus",
        defaults={
            "description": "Ancient Trojan philosopher, first philosopher before Thales. Author of "
                         "Kitab al Alacir (Book of Ether). Believed to have lived during siege of Troy. "
                         "Father of Sons of Ether philosophy. Posited that everything is One Essence "
                         "(Ether) and becomes Many through action of mind. First to set forth scientific "
                         "principles for magick. Possibly a follower of Heraclitus.",
            "status": "Dec",
            "faction_name": "Sons of Ether",
        }
    )
    arerus.add_source("Sons of Ether Tradition Book", "The Birth of True Science")

    # Sir Lawrence Cabot
    sir_lawrence, _ = Mage.objects.get_or_create(
        name="Sir Lawrence Cabot",
        defaults={
            "description": "Scholar who wrote influential commentaries on Kitab al Alacir. "
                         "Influenced all modern translations of Arerus' work.",
            "faction_name": "Sons of Ether",
        }
    )
    sir_lawrence.add_source("Sons of Ether Tradition Book", "The Birth of True Science")

    # Lorenzo Golo
    lorenzo_golo, _ = Mage.objects.get_or_create(
        name="Lorenzo Golo",
        defaults={
            "description": "Former member of House Verditius in Order of Hermes. Broke away to form "
                         "his own House, founding what would become Sons of Ether lineage.",
            "faction_name": "Sons of Ether",
        }
    )
    lorenzo_golo.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    # General Karl Haushofer
    haushofer, _ = MtAHuman.objects.get_or_create(
        name="General Karl Haushofer",
        defaults={
            "description": "Black magician behind Hitler's rise to power. Led Nazi Thule Society. "
                         "Pursued Doctor Eon into Hollow Earth. Possessed Mental Thrall Helmet and "
                         "Ray Projector. Allied with Mechanocracy. Fell into Smoky God trying to escape, "
                         "believing he was falling toward river but actually falling up due to Hollow "
                         "Earth physics.",
            "status": "Dec",
        }
    )
    haushofer.add_source("Sons of Ether Tradition Book", "Into the Hollow Earth")

    # Master Scientist Wells
    master_wells, _ = Mage.objects.get_or_create(
        name="Master Scientist Wells",
        defaults={
            "description": "Master Scientist who warns against any dealings with Nephandi. "
                         "Has seen great minds fall to corruption, including Doctor Gordon.",
            "willpower": 9,
            "arete": 5,
            "faction_name": "Sons of Ether",
        }
    )
    master_wells.add_source("Sons of Ether Tradition Book", "Opinions")

    # Doctor Gordon (Barabbi)
    doctor_gordon, _ = Mage.objects.get_or_create(
        name="Doctor Gordon",
        defaults={
            "description": "Renowned biologist who was corrupted by Nephandi and became barabbi. "
                         "Dangerous - his understanding of biology turned to evil uses. "
                         "To be reported immediately if encountered.",
            "faction_name": "Nephandi",
            "status": "App",  # Active threat
        }
    )
    doctor_gordon.add_source("Sons of Ether Tradition Book", "Opinions")

    # Arnold Johnson
    arnold, _ = MtAHuman.objects.get_or_create(
        name="Arnold Johnson",
        defaults={
            "description": "90-year-old Sleeper who witnessed Czar Vargo's 1914 takeover attempt. "
                         "One of few who still remembers despite New World Order's efforts. "
                         "Was 12 years old at the time. Became conspiracy theorist.",
        }
    )
    arnold.add_source("Sons of Ether Tradition Book", "The Birth of True Science")

    # Jet Boy
    jetboy, _ = MtAHuman.objects.get_or_create(
        name="Jet Boy",
        defaults={
            "description": "Protege of Doctor Danvers. Equipped with advanced jet backpack. "
                         "Used Rubberon and dart gun with knockout agent. Fought Nazis in WWII. "
                         "Deplores taking life.",
        }
    )
    jetboy.add_source("Sons of Ether Tradition Book", "World War II")

    # Doctor Danvers
    doctor_danvers, _ = Mage.objects.get_or_create(
        name="Doctor Danvers",
        defaults={
            "description": "Inventor and mentor to Jet Boy. Created jet backpack and Rubberon. "
                         "Fought for Allies in WWII.",
            "faction_name": "Sons of Ether",
        }
    )
    doctor_danvers.add_source("Sons of Ether Tradition Book", "World War II")

    # Heylel Teomim (The Betrayer)
    heylel, _ = Mage.objects.get_or_create(
        name="Heylel Teomim",
        defaults={
            "description": "Hermaphrodite Solificati representative to First Cabal in 1466. "
                         "Known for pride and arrogance. Turned barabbi and led Cabal into trap. "
                         "Condemned to gilgul and death. Called 'Heylel Thoabath' (Abomination) after "
                         "betrayal. Tarnished Solificati reputation, leading to their eventual dissolution.",
            "status": "Dec",
        }
    )
    heylel.add_source("Sons of Ether Tradition Book", "The Birth of True Science")

    # Professor Vorgel
    vorgel, _ = Mage.objects.get_or_create(
        name="Professor Vorgel",
        defaults={
            "description": "Called the social phenomenon of acolytes surpassing masters 'The Pinnochio Urge'. "
                         "Brilliant but arrogant, claims no one equals his intellect.",
            "faction_name": "Sons of Ether",
        }
    )
    vorgel.add_source("Sons of Ether Tradition Book", "A Much-Maligned Monster")

    # Dame Aromika
    dame_aromika, _ = Mage.objects.get_or_create(
        name="Dame Aromika",
        defaults={
            "description": "Female Son of Ether, now calling herself an Electrodyne Diva. "
                         "Frustrated with sexism in Tradition. Created Hate Ray but denied recognition "
                         "three times for being a woman.",
            "faction_name": "Sons of Ether",
        }
    )
    dame_aromika.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    # Doctor von Allmen (Nazi)
    von_allmen, _ = Mage.objects.get_or_create(
        name="Doctor von Allmen",
        defaults={
            "description": "Infamous Nazi renegade who created KRAUZE II warbots. His mechanical army "
                         "never left Rhineland Chantry - destroyed by Doctor Eon and Jetboy using Paradox. "
                         "Escaped capture.",
            "faction_name": "Sons of Ether",
            "status": "Ret",  # Renegade
        }
    )
    von_allmen.add_source("Sons of Ether Tradition Book", "Strange Devices")

    # Doctor Brannon Rotham
    rotham, _ = Mage.objects.get_or_create(
        name="Doctor Brannon Rotham",
        defaults={
            "description": "Early 20th century premier Son of Ether. Inventor of R.U.N.T.I.S. suit, "
                         "Bio-Luminescence rote, Battery Man rote, and other formulae. Studied Spirit "
                         "Sphere intensely. Had three servants: Leland (hunchback), Owen, and Lakie.",
            "faction_name": "Sons of Ether",
        }
    )
    rotham.spheres.set_rank("spirit", 4)
    rotham.spheres.set_rank("forces", 4)
    rotham.spheres.set_rank("life", 4)
    rotham.add_source("Sons of Ether Tradition Book", "Strange Devices")

    # David Wayne "The Exterminator" Clarkus
    clarkus, _ = Mage.objects.get_or_create(
        name='David Wayne "The Exterminator" Clarkus',
        defaults={
            "description": "Inventor of Infernal Mole-Blower for fighting mutant moles of Yuk Yuk IV. "
                         "Also used device against Nephandi.",
            "faction_name": "Sons of Ether",
        }
    )
    clarkus.add_source("Sons of Ether Tradition Book", "Strange Devices")

    # Garrett Rhys
    garrett, _ = MtAHuman.objects.get_or_create(
        name="Garrett Rhys",
        defaults={
            "description": "Cult of Ecstasy photographer and stuntman. Friend of Doctor Rotham. "
                         "Uses Hyperphoto Zoom Lens with Spirit Film.",
        }
    )
    garrett.add_source("Sons of Ether Tradition Book", "Strange Devices")

    # X-Cel
    xcel, _ = Mage.objects.get_or_create(
        name="X-Cel",
        defaults={
            "description": "Virtual Adept who collaborated with Doctor Alexis Hastings on laptop design. "
                         "Intuitive grasp of complex models despite lack of formal training.",
            "faction_name": "Virtual Adepts",
        }
    )
    xcel.add_source("Sons of Ether Tradition Book", "Virtual Adepts")

    # Professor Pixel
    pixel, _ = Mage.objects.get_or_create(
        name="Professor Pixel",
        defaults={
            "description": "Cybernaut who believes Digital Web is the next battleground. "
                         "Claims no one will care about astronomical theories in ten years.",
            "faction_name": "Sons of Ether",
        }
    )
    pixel.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    # Lord Craven
    lord_craven, _ = MtAHuman.objects.get_or_create(
        name="Lord Craven",
        defaults={
            "description": "New World Order member who orchestrated destruction of ether theory. "
                         "Wrote note authorizing Michelson-Morley experiment. Suggested recruiting "
                         "Einstein. Suffered nervous heart condition when Electrodyne Engineers defected.",
        }
    )
    lord_craven.add_source("Sons of Ether Tradition Book", "Betrayal and Rebellion")

    # Professor Dubious
    dubious, _ = Mage.objects.get_or_create(
        name="Professor Dubious",
        defaults={
            "description": "Creator of Oxygen Engine on Victoria Station. Personally repairs it when needed. "
                         "Never explained how it works - generates oxygen from various materials, mostly rocks.",
            "faction_name": "Sons of Ether",
        }
    )
    dubious.add_source("Sons of Ether Tradition Book", "Realms of Adventure")

    # Colonel Arno Valiant
    valiant, _ = Mage.objects.get_or_create(
        name="Colonel Arno Valiant",
        defaults={
            "description": "Discovered Etherspace in 1888 by piloting balloon past the sky. "
                         "Stalwart adventurer who theorized ether winds could be navigated.",
            "faction_name": "Sons of Ether",
        }
    )
    valiant.add_source("Sons of Ether Tradition Book", "Realms of Adventure")

    # Captain John Cleve Symmes
    symmes, _ = Mage.objects.get_or_create(
        name="Captain John Cleve Symmes",
        defaults={
            "description": "First Son of Ether to uncover secrets of Hollow Earth in mid-1800s. "
                         "Attempted to gain government funding for expedition, creating Hollow Earth craze.",
            "faction_name": "Sons of Ether",
        }
    )
    symmes.add_source("Sons of Ether Tradition Book", "Realms of Adventure")

    # Olaf Jansen
    olaf, _ = MtAHuman.objects.get_or_create(
        name="Olaf Jansen",
        defaults={
            "description": "Scandinavian sailor who traveled to Hollow Earth with his father. "
                         "Account published by Willis George Emerson in 1908 as 'The Smoky God'. "
                         "Described land of giants worshipping interior sun.",
        }
    )
    olaf.add_source("Sons of Ether Tradition Book", "Realms of Adventure")

    # Lord Dunhampton
    dunhampton, _ = Mage.objects.get_or_create(
        name="Lord Dunhampton",
        defaults={
            "description": "British Earl living in France. Called first Electrodyne Engineers meeting "
                         "to order in 1866. Pompous, gave lengthy speech.",
            "faction_name": "Electrodyne Engineers",
        }
    )
    dunhampton.add_source("Sons of Ether Tradition Book", "Formation of the Modern Tradition")

    # Professor Jacques Etienne
    etienne, _ = Mage.objects.get_or_create(
        name="Professor Jacques Etienne",
        defaults={
            "description": "Well-regarded Professor who gave forthright speech at first Electrodyne "
                         "Engineers meeting explaining purpose: alliance of world's scientists to "
                         "quickly advance sciences together.",
            "faction_name": "Electrodyne Engineers",
        }
    )
    etienne.add_source("Sons of Ether Tradition Book", "Formation of the Modern Tradition")

    # Sir Jarriet
    jarriet, _ = MtAHuman.objects.get_or_create(
        name="Sir Jarriet",
        defaults={
            "description": "Audience member who disrupted first Electrodyne Engineers meeting. "
                         "Accused them of naivete and contempt for national differences. "
                         "Led walkout from the hall.",
        }
    )
    jarriet.add_source("Sons of Ether Tradition Book", "Formation of the Modern Tradition")

    # Earl Glamm
    glamm, _ = Mage.objects.get_or_create(
        name="Earl Glamm",
        defaults={
            "description": "Prestigious and brilliant Doctor. Gracious host of London Sons of Ether "
                         "club in his Manor.",
            "faction_name": "Sons of Ether",
        }
    )
    glamm.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    # Earl Oberon
    oberon, _ = Mage.objects.get_or_create(
        name="Earl Oberon",
        defaults={
            "description": "Chronicler of the Great Hall and Assembly of Science. "
                         "Described governing structure of Tradition.",
            "faction_name": "Sons of Ether",
        }
    )
    oberon.add_source("Sons of Ether Tradition Book", "The Old Boys Club")


def create_wonders(soe):
    """Create Wonders and Devices"""

    # Conversion Engine
    conversion_engine, _ = Artifact.objects.get_or_create(
        name="Conversion Engine",
        defaults={
            "rank": 5,
            "description": "Czar Vargo's advanced device that converts air into energy at unbelievable rate. "
                         "Displayed at Paris Exhibition 1900. Allowed creation of airships. "
                         "Some believe modified engine actually converts ether into energy. "
                         "Uses solar panels, batteries, and Tesla coils.",
            "arete": 5,
            "quintessence_max": 20,
            "background_cost": 5,
        }
    )
    conversion_engine.add_source("Sons of Ether Tradition Book", "Paris Exhibition, 1900")

    # Solar Conversion Engine
    solar_engine, _ = Artifact.objects.get_or_create(
        name="Solar Conversion Engine",
        defaults={
            "rank": 4,
            "description": "Doctor Eon's energy conversion device. Converts sun's rays into electric power "
                         "for his ship. Solar panels collect and store rays, large batteries transfer "
                         "energy into Tesla coils. General Haushofer sought to combine with Ray Projector "
                         "to create fusion gun powered by Smoky God.",
            "arete": 4,
            "quintessence_max": 15,
            "background_cost": 4,
        }
    )
    solar_engine.add_source("Sons of Ether Tradition Book", "Into the Hollow Earth")

    # Mental Thrall Helmet
    thrall_helmet, _ = Talisman.objects.get_or_create(
        name="Mental Thrall Helmet",
        defaults={
            "rank": 4,
            "description": "Large helmet studded with coils and wires. Forces subjects to divulge all "
                         "their secrets through mental control. Used by General Haushofer. "
                         "Can be resisted with Science of Om mental control techniques, and effect "
                         "can be projected outward if user knows how.",
            "arete": 4,
            "quintessence_max": 10,
            "background_cost": 4,
        }
    )
    thrall_helmet.add_source("Sons of Ether Tradition Book", "Into the Hollow Earth")

    # Hyperphoto Zoom Lens with Spirit Film
    zoom_lens, _ = Talisman.objects.get_or_create(
        name="Hyperphoto Zoom Lens with Spirit Film",
        defaults={
            "rank": 3,
            "description": "Enormous telephoto lens fitting any 35mm camera. Uses Correspondence Sensing "
                         "to focus on distant locations and photograph them. Spirit Film reveals true nature "
                         "of subjects - how they appear in Near Umbra, including Avatars and pattern spiders. "
                         "Created by Dr. Rotham for Garrett Rhys. Usually coincidental.",
            "arete": 3,
            "quintessence_max": 15,
            "background_cost": 3,
        }
    )
    zoom_lens.add_source("Sons of Ether Tradition Book", "Strange Devices")

    # Infernal Mole-Blower
    mole_blower, _ = Talisman.objects.get_or_create(
        name="Infernal Mole-Blower",
        defaults={
            "rank": 3,
            "description": "Steel box with small gas engine, gears, and holes for road flares. "
                         "Forces irritating viscous smoke into animal burrows, also works on larger subjects "
                         "like Nephandi. Causes coughing spasms, potential blindness and incapacitation. "
                         "Created by David Wayne Clarkus. Uses Forces 2, Matter 2, Prime 2.",
            "arete": 4,
            "quintessence_max": 20,
            "background_cost": 3,
        }
    )
    mole_blower.add_source("Sons of Ether Tradition Book", "Strange Devices")

    # R.U.N.T.I.S. Suit
    runtis, _ = Artifact.objects.get_or_create(
        name="R.U.N.T.I.S. Suit",
        defaults={
            "rank": 4,
            "description": "Rotham's Umbra Navigation, Transportation and Illumination System. "
                         "Full-metal suit resembling cross between diving suit and Robby the Robot. "
                         "Air-tight with internal food/water (72 hours). Penetrates Gauntlet. "
                         "+4 soak dice, +2 difficulty on Dex rolls. Boosts Strength to 6. "
                         "Ether Jets allow flight in Near Umbra. Removing suit ejects wearer from Umbra. "
                         "Created by Dr. Brannon Rotham.",
            "arete": 4,
            "quintessence_max": 20,
            "background_cost": 4,
        }
    )
    runtis.add_source("Sons of Ether Tradition Book", "Strange Devices")

    # KRAUZE II Warbot
    warbot, _ = Talisman.objects.get_or_create(
        name="KRAUZE II Warbot",
        defaults={
            "rank": 5,
            "description": "Nazi Doctor von Allmen's robots. Can fly, fire beam weaponry, sustain heavy "
                         "damage (5 soak dice, 7 health levels). Stupid (no Mind Science). "
                         "Quickly deplete Primal Force Batteries. Highly vulgar. Army destroyed by "
                         "Doctor Eon and Jetboy using Paradox. Uses Prime 2, Matter 3, Forces 4.",
            "arete": 5,
            "quintessence_max": 20,
            "background_cost": 5,
        }
    )
    warbot.add_source("Sons of Ether Tradition Book", "Strange Devices")

    # Ether Goggles
    goggles, _ = Talisman.objects.get_or_create(
        name="Ether Goggles",
        defaults={
            "rank": 2,
            "description": "Goggles that allow wearer to sense perturbations in the ether. "
                         "Necessary tool to accommodate lack of natural ability to perceive ether. "
                         "Often manufactured in Gernsback Continuum.",
            "arete": 2,
            "quintessence_max": 5,
            "background_cost": 2,
        }
    )
    goggles.add_source("Sons of Ether Tradition Book", "What Is Ether?")

    # Jet Backpack
    jetpack, _ = Talisman.objects.get_or_create(
        name="Jet Backpack",
        defaults={
            "rank": 3,
            "description": "Advanced jet backpack invented by Doctor Danvers for Jet Boy. "
                         "Allows flight. Can be repaired with Rubberon if ruptured.",
            "arete": 3,
            "quintessence_max": 10,
            "background_cost": 3,
        }
    )
    jetpack.add_source("Sons of Ether Tradition Book", "World War II")

    # Rubberon
    rubberon, _ = Wonder.objects.get_or_create(
        name="Rubberon",
        defaults={
            "rank": 2,
            "description": "Vacuum-packed pellet of expandable rubber base. Hardens within minutes "
                         "of air exposure and sticks to whatever it's applied to. "
                         "Invented by Doctor Danvers. Used for quick repairs.",
            "background_cost": 2,
        }
    )
    rubberon.add_source("Sons of Ether Tradition Book", "World War II")

    # C.U.D.D. Beam Lobotomizer
    cudd_beam, _ = Talisman.objects.get_or_create(
        name="C.U.D.D. Beam Lobotomizer",
        defaults={
            "rank": 4,
            "description": "Powerful and feared Mind device. Creators feared by friend and foe alike.",
            "arete": 4,
            "quintessence_max": 15,
            "background_cost": 4,
        }
    )
    cudd_beam.add_source("Sons of Ether Tradition Book", "Theory and Practice")

    # Telepathic Telephone
    tel_phone, _ = Talisman.objects.get_or_create(
        name="Telepathic Telephone",
        defaults={
            "rank": 3,
            "description": "Device allowing mind-to-mind communication. Creators feared by friend and foe.",
            "arete": 3,
            "quintessence_max": 10,
            "background_cost": 3,
        }
    )
    tel_phone.add_source("Sons of Ether Tradition Book", "Theory and Practice")

    # Hypnodisc
    hypnodisc, _ = Talisman.objects.get_or_create(
        name="Hypnodisc",
        defaults={
            "rank": 3,
            "description": "Doctor Headspace's device. Seductive spinning motion defeats even "
                         "Men in Black mental shields and sunglasses. Used to escape New World Order.",
            "arete": 3,
            "quintessence_max": 10,
            "background_cost": 3,
        }
    )
    hypnodisc.add_source("Sons of Ether Tradition Book", "Opinions")

    # Hate Ray
    hate_ray, _ = Talisman.objects.get_or_create(
        name="Hate Ray",
        defaults={
            "rank": 4,
            "description": "Device created by Dame Aromika. She was denied recognition three times "
                         "for being a woman, leading to her frustration with Tradition sexism.",
            "arete": 4,
            "quintessence_max": 15,
            "background_cost": 4,
        }
    )
    hate_ray.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    # Tunneling Tank
    tank, _ = Artifact.objects.get_or_create(
        name="Tunneling Tank",
        defaults={
            "rank": 4,
            "description": "Massive tank used by Doctor Eon and Terrific Trio to reach Hollow Earth. "
                         "Can tunnel through earth. Used to transport equipment including Solar Conversion Engine.",
            "arete": 4,
            "quintessence_max": 20,
            "background_cost": 4,
        }
    )
    tank.add_source("Sons of Ether Tradition Book", "Into the Hollow Earth")

    # Ray Projector
    ray_projector, _ = Talisman.objects.get_or_create(
        name="Ray Projector",
        defaults={
            "rank": 4,
            "description": "Haushofer's own design. Could be combined with Solar Conversion Engine "
                         "to create massively powerful fusion gun fueled by inner sun's energies.",
            "arete": 4,
            "quintessence_max": 15,
            "background_cost": 4,
        }
    )
    ray_projector.add_source("Sons of Ether Tradition Book", "Into the Hollow Earth")

    # Dimensional Attunement Generator
    dag, _ = Artifact.objects.get_or_create(
        name="Dimensional Attunement Generator",
        defaults={
            "rank": 5,
            "description": "Huge Device employing Spirit Effect Outward Journeys. Required to escape "
                         "Earth's orbit and shift into Etherspace. Has 8 dice, needs 15 successes "
                         "(difficulty 8) on extended roll. Requires great time and Quintessence. "
                         "Always vulgar. Can take ~24 Paradox points before shutdown/explosion.",
            "arete": 5,
            "quintessence_max": 30,
            "background_cost": 5,
        }
    )
    dag.add_source("Sons of Ether Tradition Book", "Realms of Adventure")

    # Oxygen Engine
    oxygen_engine, _ = Artifact.objects.get_or_create(
        name="Oxygen Engine",
        defaults={
            "rank": 4,
            "description": "Created by Professor Dubious for Victoria Station. Constantly generates "
                         "oxygen from materials (mostly rocks) fed into it. Professor never explained "
                         "how it works and personally repairs it. Rarely breaks down.",
            "arete": 4,
            "quintessence_max": 20,
            "background_cost": 4,
        }
    )
    oxygen_engine.add_source("Sons of Ether Tradition Book", "Realms of Adventure")


def create_rotes(soe):
    """Create Effects/Rotes"""

    # Using ObjectType for rote type
    rote_type, _ = ObjectType.objects.get_or_create(
        name="Rote",
        type="mta",
    )

    # Find Reality Flaw
    find_flaw, _ = rote_type.objects.get_or_create(
        name="Find Reality Flaw",
        defaults={
            "description": "Detects Paradox damage to reality. With 4+ successes, determines exact "
                         "Paradox amount released and pinpoints any Paradox Flaws' location and size. "
                         "With 6+ successes, offers solution to correct them. Uses Prime 1, Entropy 1.",
        }
    )
    find_flaw.add_source("Sons of Ether Tradition Book", "Additional Formulas")

    # General Anesthesia
    anesthesia, _ = rote_type.objects.get_or_create(
        name="General Anesthesia",
        defaults={
            "description": "For every success, caster ignores penalties of one wound level for duration "
                         "of magickal Effect. Cannot be permanent. Won't negate damage taken after effect. "
                         "Used by Dr. Rotham. Uses Mind 1, Life 1.",
        }
    )
    anesthesia.add_source("Sons of Ether Tradition Book", "Additional Formulas")

    # Knock Out
    knockout, _ = rote_type.objects.get_or_create(
        name="Knock Out",
        defaults={
            "description": "Non-lethal formula for immobilizing subjects. Stuns target's brain for "
                         "double the turns scored. Uses Mind 3 understanding of psyche with Prime 2 "
                         "Rubbing the Bone. More potent than Euthanatos version - focuses on neural "
                         "pattern instead of biological body. Target resists with Willpower (diff 8), "
                         "each success canceling one of Scientist's. Created by Dr. Rotham.",
        }
    )
    knockout.add_source("Sons of Ether Tradition Book", "Additional Formulas")

    # Bio-Luminescence
    biolum, _ = rote_type.objects.get_or_create(
        name="Bio-Luminescence",
        defaults={
            "description": "Converts flesh and blood into glow-in-the-dark substance. Each success = "
                         "more brightness: 1 succ = 1 ft, 2 = 5 ft, 3 = 10 ft, 4 = 15 ft, etc. "
                         "Glow can be concentrated on body parts (teeth, eyes). Originally for safer "
                         "Halloween. Uses Forces 3, Life 3.",
        }
    )
    biolum.add_source("Sons of Ether Tradition Book", "Additional Formulas")

    # Battery Man
    battery_man, _ = rote_type.objects.get_or_create(
        name="Battery Man",
        defaults={
            "description": "Converts body into wet cell storing electrical energy from household socket. "
                         "Each success = 10,000 volts stored. Stored in nervous system. Can discharge to: "
                         "electrocute (successes x3 damage), charge batteries, short-circuit equipment, "
                         "light bulbs, zap things. Must discharge within 1 hour or suffer 1 Health/success. "
                         "Dr. Rotham warns of potential cancer/second head growth. Uses Life 4, Forces 2.",
        }
    )
    battery_man.add_source("Sons of Ether Tradition Book", "Additional Formulas")

    # Science of Om
    science_om, _ = rote_type.objects.get_or_create(
        name="Science of Om",
        defaults={
            "description": "Method of mental control learned from Goro monks. Normally for "
                         "self-meditation, but can be magnified by devices to project mental control "
                         "outward. Doctor Eon used this to overcome Mental Thrall Helmet and turn "
                         "its effects on Haushofer. Mind-based technique.",
        }
    )
    science_om.add_source("Sons of Ether Tradition Book", "Into the Hollow Earth")


def create_locations(soe):
    """Create significant locations"""

    # The Great Hall
    great_hall, _ = Chantry.objects.get_or_create(
        name="The Great Hall",
        defaults={
            "description": "Governing body of Sons of Ether. Resplendent mansion just outside Paris "
                         "with connection to Horizon. True Great Hall exists in Horizon - majestic "
                         "building in classical Parisian style. Assembly of Science meets here to vote "
                         "on important matters. Meritocracy - only proven wise admitted, but disputes "
                         "resolved democratically. Young Scientists can witness Master Scientists debate. "
                         "Portal to Gernsback Continuum located here - strictly controlled access.",
            "gauntlet": 3,
        }
    )
    great_hall.add_source("Sons of Ether Tradition Book", "The Old Boys Club")

    # Victoria Station
    victoria, _ = Chantry.objects.get_or_create(
        name="Victoria Station",
        defaults={
            "description": "Space station orbiting the moon. Pure Victorian-era design with brass and wood. "
                         "Protected by mysterious Faerie allies who mend broken objects and maintain orbit. "
                         "Main departure point for Etherspace. Three Professors, six acolytes on staff. "
                         "Comfortable with port windows viewing distant stars. Oxygen Engine provides air. "
                         "Some want to rename it (Bradbury Outpost, Moon City 1, Arcadia Station). "
                         "Connected to Horizon Realm.",
            "gauntlet": 2,
        }
    )
    victoria.add_source("Sons of Ether Tradition Book", "Realms of Adventure")

    # Gernsback Continuum
    gernsback, _ = Node.objects.get_or_create(
        name="Gernsback Continuum",
        defaults={
            "description": "Recent Horizon Realm connected to Great Hall in Paris. Based on William Gibson "
                         "story and Hugo Gernsback's vision. Art-deco future with ray guns, metal zeppelins, "
                         "sleek saucers. Major playground for new theories and Sciences. Host to Wars of Science "
                         "(duels with zeppelins and ray weaponry). Entertainment includes piloting etherflyers. "
                         "Best place to observe ether behavior. Many ether goggles manufactured here. "
                         "Forces +2, Matter +2, Prime +1 to all effects.",
            "quintessence_max": 10,
            "ratio": 3,
            "gauntlet": 2,
        }
    )
    gernsback.add_source("Sons of Ether Tradition Book", "Realms of Adventure")

    # The Hollow Earth
    hollow_earth, _ = Node.objects.get_or_create(
        name="The Hollow Earth",
        defaults={
            "description": "Very old Realm, shunted from material world to Horizon outpost. "
                         "Portal via North Pole cave - miles of lightless caverns to Summit of Inner Sun. "
                         "Inner tropical world with dinosaurs, ancient mammals, legendary beasts. "
                         "Lost tribes from naked savages to enlightened Goro monks. Inner sun called Smoky God. "
                         "Inhabitants include: Vril (superior beings with energy weapons), deros (degenerated "
                         "robots from Atlantean Space Gods), Morcegos (bat-people). Aurora Borealis is reflection "
                         "from Smoky God through pole gap. Fading fast, may cease to exist. "
                         "Life magick -1 difficulty. Discovered by Captain John Cleve Symmes.",
            "quintessence_max": 15,
            "ratio": 4,
            "gauntlet": 4,
        }
    )
    hollow_earth.add_source("Sons of Ether Tradition Book", "Realms of Adventure")

    # Etherspace
    etherspace, _ = Node.objects.get_or_create(
        name="Etherspace",
        defaults={
            "description": "Not a Horizon Realm but Deep Umbra area. Resembles outer space but filled "
                         "with breathable ether pressure-equalized to Earth. Ether winds blow in eddies "
                         "and currents - regular channels that often shift. Celestial body pull helps "
                         "navigation. Must pass Barriers (Gauntlet and Horizon) requiring powerful "
                         "Dimensional Attunement Generators (15 successes, diff 8). Always vulgar. "
                         "Dangerous: Void Engineer sentries, getting lost, Nephandi, demon hordes. "
                         "Discovered by Colonel Arno Valiant in 1888. Correspondence +1 to all ratings.",
            "quintessence_max": 20,
            "ratio": 5,
            "gauntlet": 9,  # Extremely hard to reach
        }
    )
    etherspace.add_source("Sons of Ether Tradition Book", "Realms of Adventure")

    # Agharta
    agharta, _ = Chantry.objects.get_or_create(
        name="Agharta",
        defaults={
            "description": "Ancient city in Hollow Earth. Home to Goro monks who teach Science of Om. "
                         "Located in caverns beneath Inner Sun summit. Doctor Eon and Terrific Trio "
                         "allied with monks to halt Nazi invasion. Lan Ko was high priest. "
                         "Place of meditation and peace, guards world from destruction.",
            "gauntlet": 3,
        }
    )
    agharta.add_source("Sons of Ether Tradition Book", "Into the Hollow Earth")

    # Symposium Manor
    symposium, _ = Chantry.objects.get_or_create(
        name="Symposium Manor",
        defaults={
            "description": "Prestigious Paris manor where first Electrodyne Engineers meeting was held "
                         "January 1, 1866. Lord Dunhampton presided. Meeting fell short when Sir Jarriet "
                         "led walkout over nationalist concerns.",
            "gauntlet": 4,
        }
    )
    symposium.add_source("Sons of Ether Tradition Book", "Formation of the Modern Tradition")

    # Rhineland Chantry
    rhineland, _ = Chantry.objects.get_or_create(
        name="Rhineland Chantry",
        defaults={
            "description": "Nazi chantry where Doctor von Allmen created KRAUZE II warbots. "
                         "Leveled by Doctor Eon and Jetboy using Paradox. Von Allmen escaped.",
            "status": "Dec",  # Destroyed
            "gauntlet": 4,
        }
    )
    rhineland.add_source("Sons of Ether Tradition Book", "Strange Devices")


def create_books(soe):
    """Create important texts"""

    kitab, _ = Book.objects.get_or_create(
        title="Kitab al Alacir",
        defaults={
            "type": "lore",
            "edition": 1,
            "year": -1200,  # Approximate, ancient Troy
            "description": "The 'Book of Ether' by Arerus of Troy. First philosophical text, "
                         "predating Thales. Divided into two sections: metaphysics (natural philosophy) "
                         "and mysticism (study of thought). Posits everything is variations on single "
                         "Essence (Ether) which becomes Many through mind's action. Everything is One. "
                         "Greatly influenced Aristotle who translated it to Greek and derived Fifth Essence. "
                         "Scientific principles for workings of magick. Everyone has potential to work it. "
                         "Famous English translation by Lord Edmund (1900). Other translations: Fleming (1945), "
                         "Doctor Electrik (1956), Forthright (1981). Standard reading for all Sons of Ether. "
                         "Reading it often triggers Awakening in those with potential.",
        }
    )

    paradigma, _ = Book.objects.get_or_create(
        title="Paradigma",
        defaults={
            "type": "lore",
            "edition": 1,
            "year": 1907,
            "description": "Journal of the Progressive Sciences. Nonprofit scientific and educational journal "
                         "serving Sons of Ether since 1907. Published quarterly. Copies available to all members. "
                         "Back issues available by request. Edited by Doctor William Bridges. "
                         "For 'increase and diffusion of True Science.' Contributors include hundreds of "
                         "Professors, Doctors, and Scientists. Standard place for publication of theories. "
                         "Appearance before local club (editors) often required for publication.",
        }
    )

    paradigma.add_source("Sons of Ether Tradition Book", "Prelude")


def create_merits_flaws(soe):
    """Create any new Merits or Flaws"""

    # The Pinnochio Urge - social phenomenon
    pinnochio, _ = MeritFlaw.objects.get_or_create(
        name="The Pinnochio Urge",
        defaults={
            "ratings": [0],
            "description": "Social phenomenon named by Professor Vorgel. The dream of every young acolyte "
                         "to one day wield the powers of their master. Can lead to resentment if teacher "
                         "is possessive and falsifies progress records.",
        }
    )
    pinnochio.add_source("Sons of Ether Tradition Book", "A Much-Maligned Monster")


def populate_soe():
    """Main population function"""
    print("Adding Sons of Ether sourcebook...")
    soe = add_source()

    print("Creating factions...")
    sons = create_factions(soe)

    print("Creating characters...")
    create_characters(soe)

    print("Creating wonders...")
    create_wonders(soe)

    print("Creating rotes...")
    create_rotes(soe)

    print("Creating locations...")
    create_locations(soe)

    print("Creating books...")
    create_books(soe)

    print("Creating merits/flaws...")
    create_merits_flaws(soe)

    print("Sons of Ether population complete!")


if __name__ == "__main__":
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tg.settings')
    django.setup()

    populate_soe()
