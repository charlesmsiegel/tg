"""
Populate database with characters, items, and locations from The Chaos Factor.
This sourcebook details Samuel Haight's final confrontation in Mexico City.
"""

from characters.models.mage.mage import Mage
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Instrument, Practice, Paradigm
from characters.models.mage.sphere import Sphere
from characters.models.mage.effect import Effect
from characters.models.mage.rote import Rote
from characters.models.werewolf.wtahuman import WtAHuman
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.tribe import Tribe
from characters.models.werewolf.renown import RenownRating
from characters.models.vampire.vtm import Vampire
from characters.models.vampire.vtm_human import VtMHuman
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute, AttributeRating
from items.models.mage.wonder import Wonder
from items.models.werewolf.fetish import Fetish
from locations.models.mage.node import Node
from locations.models.core.location import Location, City
from core.models import Language
import random


def create_chaos_factor_data():
    """Create all Chaos Factor related content."""
    create_factions()
    create_paradigms_and_practices()
    create_effects_and_rotes()
    create_major_npcs()
    create_minor_npcs()
    create_templates()
    create_items()
    create_locations()


def create_factions():
    """Create or get factions mentioned in the book."""
    # Mage Factions
    MageFaction.objects.get_or_create(
        name="New World Order",
        defaults={
            "description": "Technocratic Convention focused on social control and information management"
        }
    )

    MageFaction.objects.get_or_create(
        name="Iteration X",
        defaults={
            "description": "Technocratic Convention focused on technology and machinery"
        }
    )

    MageFaction.objects.get_or_create(
        name="Syndicate",
        defaults={
            "description": "Technocratic Convention focused on economics and wealth"
        }
    )

    MageFaction.objects.get_or_create(
        name="Progenitors",
        defaults={
            "description": "Technocratic Convention focused on biology and life sciences"
        }
    )

    MageFaction.objects.get_or_create(
        name="Celestial Chorus",
        defaults={
            "description": "Tradition focused on Unity and the One"
        }
    )

    MageFaction.objects.get_or_create(
        name="Nephandi",
        defaults={
            "description": "Fallen mages who serve entropy and corruption"
        }
    )

    # Werewolf Tribes
    Tribe.objects.get_or_create(
        name="Bone Gnawers",
        defaults={
            "willpower": 4,
            "description": "Urban survivors, the tribe of the homeless and downtrodden"
        }
    )

    Tribe.objects.get_or_create(
        name="Black Spiral Dancers",
        defaults={
            "willpower": 3,
            "description": "Fallen Garou corrupted by the Wyrm"
        }
    )

    Tribe.objects.get_or_create(
        name="Skin Dancers",
        defaults={
            "willpower": 5,
            "description": "False Garou created through dark rituals using the skins of true werewolves"
        }
    )


def create_paradigms_and_practices():
    """Create paradigms and practices for mages."""
    Paradigm.objects.get_or_create(
        name="A Mechanistic Cosmos",
        defaults={"description": "The universe operates like a vast machine"}
    )

    Paradigm.objects.get_or_create(
        name="Divine Order and Earthly Chaos",
        defaults={"description": "Reality reflects the will of the One"}
    )

    Practice.objects.get_or_create(
        name="Cybernetics",
        defaults={"description": "Integration of technology and consciousness"}
    )

    Practice.objects.get_or_create(
        name="High Ritual Magick",
        defaults={"description": "Formal ceremonial magic"}
    )


def create_effects_and_rotes():
    """Create Effects and Rotes from The Chaos Factor."""

    # Haight's Countermagick
    countermagick = Effect.objects.create(
        name="Haight's Counterspell",
        description="A powerful countermagick effect that disrupts enemy magic. Haight uses the Staff of the World Tree to fuel this effect.",
        prime=3,
        spirit=2,
    )

    # Spirit Flaying - Haight's signature attack
    spirit_flay = Effect.objects.create(
        name="Spirit Flaying",
        description="Tears a spirit from a living being, causing massive damage. Used by Haight to create Skin Dancers.",
        spirit=5,
        life=3,
        prime=2,
    )

    # Pandemonium Corruption
    corruption = Effect.objects.create(
        name="Pandemonium's Grasp",
        description="The Pandemonium's corrupting influence manifests as black tendrils that drain willpower and plant seeds of darkness.",
        mind=4,
        spirit=3,
        entropy=3,
    )

    # Technocracy Combat Procedure - Force Blast
    force_blast = Effect.objects.create(
        name="Directed Energy Weapon",
        description="Standard Technocracy combat procedure using focused energy beams.",
        forces=3,
        prime=2,
    )

    # Technocracy - Teleportation
    teleport = Effect.objects.create(
        name="Emergency Extraction Protocol",
        description="Technocracy emergency teleportation for agents in danger.",
        correspondence=4,
        prime=2,
    )

    # Celestial Chorus - Protective Ward
    ward = Effect.objects.create(
        name="Shield of Faith",
        description="A protective barrier powered by faith in the One. Used by Bernardino de Sahagun.",
        prime=3,
        forces=2,
        spirit=2,
    )

    # Celestial Chorus - Healing
    healing = Effect.objects.create(
        name="Divine Restoration",
        description="Healing through channeling the power of the One.",
        life=4,
        prime=2,
    )

    # Nephandi - Corruption Seed
    seed = Effect.objects.create(
        name="Seed of Corruption",
        description="Plants a spiritual seed of darkness that slowly corrupts the target's Avatar.",
        entropy=4,
        spirit=3,
        mind=2,
        prime=2,
    )

    # Nephandi - Summon Bane
    summon_bane = Effect.objects.create(
        name="Call the Wyrm",
        description="Summons powerful Bane spirits to serve the caster.",
        spirit=4,
        entropy=2,
        prime=2,
    )

    # Reality Reconstruction - Used to fight the Pandemonium
    reality_fix = Effect.objects.create(
        name="Reality Reconstruction",
        description="Rebuilds consensus reality in areas corrupted by the Pandemonium or Nephandi influence.",
        prime=5,
        matter=3,
        spirit=3,
        mind=2,
    )

    # Create some sample rotes
    # High Ritual Magick practice for these rotes
    ritual_practice = Practice.objects.get(name="High Ritual Magick")
    cybernetics_practice = Practice.objects.get(name="Cybernetics")

    # Get attributes and abilities for rotes
    intelligence = Attribute.objects.get(property_name="intelligence")
    perception = Attribute.objects.get(property_name="perception")
    wits = Attribute.objects.get(property_name="wits")

    occult = Ability.objects.get(property_name="occult")
    computer = Ability.objects.get(property_name="computer")
    awareness = Ability.objects.get(property_name="awareness")

    # Celestial Chorus Healing Rote
    Rote.objects.create(
        name="Divine Restoration Rote",
        description="Traditional Celestial Chorus healing technique.",
        effect=healing,
        practice=ritual_practice,
        attribute=intelligence,
        ability=occult,
    )

    # Technocracy Force Blast Rote
    Rote.objects.create(
        name="Standard DEW Protocol",
        description="Technocracy's standardized Directed Energy Weapon procedure.",
        effect=force_blast,
        practice=cybernetics_practice,
        attribute=perception,
        ability=computer,
    )

    # Nephandi Corruption Rote
    Rote.objects.create(
        name="The Sepulchre's Touch",
        description="Nephandi technique for corrupting Avatars, taught by Amelio Santa Lucien.",
        effect=seed,
        practice=ritual_practice,
        attribute=wits,
        ability=occult,
    )

    print("Created Effects and Rotes from The Chaos Factor")


def create_major_npcs():
    """Create major NPCs from The Chaos Factor."""

    # Samuel Haight - The main antagonist
    haight = Mage.objects.create(
        name="Samuel Haight",
        nature="Deviant",
        demeanor="Architect",
        essence="Dynamic",
        affiliation=None,  # Orphan
        strength=5,
        dexterity=3,
        stamina=5,
        charisma=5,
        manipulation=5,
        appearance=2,
        perception=4,
        intelligence=4,
        wits=4,
        alertness=4,
        athletics=4,
        brawl=3,
        intimidation=5,
        streetwise=3,
        subterfuge=4,
        animal_ken=3,
        firearms=5,
        melee=4,
        stealth=4,
        computer=2,
        investigation=4,
        linguistics=3,
        occult=5,
        arete=5,
        willpower=9,
        age=45,
        apparent_age=45,
        description="The Skinner. A Kinfolk turned false Garou through dark rituals, now wielding stolen magical power."
    )
    haight.spheres.create(sphere=Sphere.objects.get(name="Correspondence"), rating=2)
    haight.spheres.create(sphere=Sphere.objects.get(name="Entropy"), rating=3)
    haight.spheres.create(sphere=Sphere.objects.get(name="Forces"), rating=3)
    haight.spheres.create(sphere=Sphere.objects.get(name="Life"), rating=2)
    haight.spheres.create(sphere=Sphere.objects.get(name="Matter"), rating=3)
    haight.spheres.create(sphere=Sphere.objects.get(name="Prime"), rating=2)
    haight.spheres.create(sphere=Sphere.objects.get(name="Spirit"), rating=4)

    # Huitzilopoctli/Shaitan - Ancient Baali vampire
    shaitan = Vampire.objects.create(
        name="Shaitan",
        nature="Architect",
        demeanor="Visionary",
        clan="Baali",
        generation=4,
        sire="Ashur",
        strength=7,
        dexterity=6,
        stamina=7,
        charisma=8,
        manipulation=9,
        appearance=0,
        perception=6,
        intelligence=6,
        wits=7,
        alertness=4,
        brawl=5,
        intimidation=9,
        leadership=8,
        subterfuge=9,
        melee=5,
        occult=9,
        willpower=10,
        age=6500,
        apparent_age=20,
        description="Ancient Baali Methuselah, once known as Huitzilopoctli, Aztec god of war. Servant of the demon Baal."
    )

    # Cardinal Melinda Galbraith - Sabbat leader
    melinda = Vampire.objects.create(
        name="Melinda Galbraith",
        nature="Director",
        demeanor="Judge",
        clan="Toreador Antitribu",
        generation=5,
        sire="Helena",
        strength=6,
        dexterity=7,
        stamina=6,
        charisma=8,
        manipulation=8,
        appearance=5,
        perception=7,
        intelligence=6,
        wits=6,
        alertness=4,
        brawl=5,
        leadership=5,
        occult=3,
        willpower=9,
        age=850,
        apparent_age=30,
        description="Cardinal of Mexico City, leader of the Sabbat in Mexico. Former thrall of Helena."
    )

    # Monte Diaz / Quetzalcoatl - New World Order leader
    nwo_faction = MageFaction.objects.get(name="New World Order")
    monte = Mage.objects.create(
        name="Monte Diaz",
        nature="Judge",
        demeanor="Director",
        essence="Pattern",
        affiliation=nwo_faction,
        strength=2,
        dexterity=2,
        stamina=3,
        charisma=5,
        manipulation=4,
        appearance=3,
        perception=4,
        intelligence=5,
        wits=5,
        alertness=3,
        leadership=5,
        computer=5,
        occult=5,
        arete=8,
        willpower=7,
        age=500,
        apparent_age=40,
        description="Possesses the body of the Oracle Quetzalcoatl. Leader of Technocracy forces in Mexico City."
    )
    monte.spheres.create(sphere=Sphere.objects.get(name="Correspondence"), rating=4)
    monte.spheres.create(sphere=Sphere.objects.get(name="Forces"), rating=5)
    monte.spheres.create(sphere=Sphere.objects.get(name="Life"), rating=4)
    monte.spheres.create(sphere=Sphere.objects.get(name="Mind"), rating=4)
    monte.spheres.create(sphere=Sphere.objects.get(name="Matter"), rating=4)
    monte.spheres.create(sphere=Sphere.objects.get(name="Prime"), rating=5)
    monte.spheres.create(sphere=Sphere.objects.get(name="Spirit"), rating=4)

    # Maria de Guadalupe - Iteration X leader
    iter_x = MageFaction.objects.get(name="Iteration X")
    maria = Mage.objects.create(
        name="Maria de Guadalupe",
        nature="Architect",
        demeanor="Critic",
        essence="Questing",
        affiliation=iter_x,
        strength=3,
        dexterity=4,
        stamina=2,
        charisma=3,
        manipulation=3,
        appearance=5,
        perception=5,
        intelligence=3,
        wits=3,
        alertness=3,
        firearms=3,
        computer=5,
        arete=6,
        willpower=9,
        description="Leader of Iteration X in Mexico City. Poses as the Virgin of Guadalupe."
    )
    maria.spheres.create(sphere=Sphere.objects.get(name="Correspondence"), rating=5)
    maria.spheres.create(sphere=Sphere.objects.get(name="Forces"), rating=4)
    maria.spheres.create(sphere=Sphere.objects.get(name="Life"), rating=3)
    maria.spheres.create(sphere=Sphere.objects.get(name="Mind"), rating=4)
    maria.spheres.create(sphere=Sphere.objects.get(name="Matter"), rating=3)
    maria.spheres.create(sphere=Sphere.objects.get(name="Prime"), rating=3)

    # Bernardino de Sahagun - Celestial Chorus elder
    chorus = MageFaction.objects.get(name="Celestial Chorus")
    sahagun = Mage.objects.create(
        name="Bernardino de Sahagun",
        nature="Architect",
        demeanor="Caregiver",
        essence="Pattern",
        affiliation=chorus,
        strength=3,
        dexterity=3,
        stamina=3,
        charisma=3,
        manipulation=5,
        appearance=3,
        perception=4,
        intelligence=5,
        wits=5,
        alertness=3,
        leadership=3,
        occult=2,
        arete=8,
        willpower=10,
        age=600,
        description="Ancient Celestial Chorus mage who has protected Mexico City for centuries."
    )
    sahagun.spheres.create(sphere=Sphere.objects.get(name="Correspondence"), rating=3)
    sahagun.spheres.create(sphere=Sphere.objects.get(name="Forces"), rating=5)
    sahagun.spheres.create(sphere=Sphere.objects.get(name="Life"), rating=4)
    sahagun.spheres.create(sphere=Sphere.objects.get(name="Mind"), rating=2)
    sahagun.spheres.create(sphere=Sphere.objects.get(name="Matter"), rating=3)
    sahagun.spheres.create(sphere=Sphere.objects.get(name="Prime"), rating=5)
    sahagun.spheres.create(sphere=Sphere.objects.get(name="Spirit"), rating=4)
    sahagun.spheres.create(sphere=Sphere.objects.get(name="Time"), rating=2)

    # Father Machete - Bone Gnawer Sept Leader
    bone_gnawers = Tribe.objects.get(name="Bone Gnawers")
    machete = Werewolf.objects.create(
        name="Father Machete",
        breed="Metis",
        auspice="Ahroun",
        tribe=bone_gnawers,
        nature="Caregiver",
        demeanor="Curmudgeon",
        strength=4,
        dexterity=3,
        stamina=3,
        charisma=4,
        manipulation=5,
        appearance=2,
        perception=3,
        intelligence=4,
        wits=5,
        alertness=5,
        athletics=5,
        brawl=5,
        melee=5,
        occult=1,
        rank=5,
        glory=0,
        honor=0,
        wisdom=0,
        willpower=8,
        description="Leader of the Sweet Water Sept in Mexico City. A metis warrior."
    )

    # Amelio Santa Lucien - Nephandi leader
    nephandi = MageFaction.objects.get(name="Nephandi")
    amelio = Mage.objects.create(
        name="Amelio Santa Lucien",
        nature="Architect",
        demeanor="Deviant",
        essence="Primordial",
        affiliation=nephandi,
        strength=3,
        dexterity=5,
        stamina=3,
        charisma=5,
        manipulation=5,
        appearance=5,
        perception=3,
        intelligence=5,
        wits=5,
        alertness=3,
        firearms=5,
        leadership=5,
        occult=5,
        arete=7,
        willpower=8,
        age=2000,
        description="Leader of the Nephandi in the Underbelly of the Wyrm. Member of the Sepulchre."
    )
    amelio.spheres.create(sphere=Sphere.objects.get(name="Correspondence"), rating=2)
    amelio.spheres.create(sphere=Sphere.objects.get(name="Entropy"), rating=5)
    amelio.spheres.create(sphere=Sphere.objects.get(name="Forces"), rating=4)
    amelio.spheres.create(sphere=Sphere.objects.get(name="Life"), rating=5)
    amelio.spheres.create(sphere=Sphere.objects.get(name="Mind"), rating=3)
    amelio.spheres.create(sphere=Sphere.objects.get(name="Matter"), rating=5)
    amelio.spheres.create(sphere=Sphere.objects.get(name="Prime"), rating=5)
    amelio.spheres.create(sphere=Sphere.objects.get(name="Spirit"), rating=2)
    amelio.spheres.create(sphere=Sphere.objects.get(name="Time"), rating=4)

    print("Created major NPCs from The Chaos Factor")


def create_minor_npcs():
    """Create minor NPCs and templates."""

    # Robert Lawson - Syndicate
    syndicate = MageFaction.objects.get(name="Syndicate")
    robert = Mage.objects.create(
        name="Robert Lawson",
        nature="Architect",
        demeanor="Director",
        essence="Pattern",
        affiliation=syndicate,
        strength=4,
        dexterity=3,
        stamina=3,
        charisma=4,
        manipulation=5,
        appearance=3,
        perception=5,
        intelligence=4,
        wits=3,
        brawl=5,
        firearms=5,
        leadership=5,
        occult=5,
        arete=6,
        willpower=7,
        description="Syndicate leader in Mexico City. Controls much of the city's criminal economy."
    )
    robert.spheres.create(sphere=Sphere.objects.get(name="Correspondence"), rating=3)
    robert.spheres.create(sphere=Sphere.objects.get(name="Forces"), rating=3)
    robert.spheres.create(sphere=Sphere.objects.get(name="Life"), rating=4)
    robert.spheres.create(sphere=Sphere.objects.get(name="Mind"), rating=3)
    robert.spheres.create(sphere=Sphere.objects.get(name="Matter"), rating=2)
    robert.spheres.create(sphere=Sphere.objects.get(name="Prime"), rating=2)
    robert.spheres.create(sphere=Sphere.objects.get(name="Spirit"), rating=4)

    # Dr. Niles Anderson - Progenitor
    progenitors = MageFaction.objects.get(name="Progenitors")
    niles = Mage.objects.create(
        name="Doctor Niles Anderson",
        nature="Fanatic",
        demeanor="Director",
        essence="Questing",
        affiliation=progenitors,
        strength=3,
        dexterity=2,
        stamina=3,
        charisma=1,
        manipulation=2,
        appearance=2,
        perception=4,
        intelligence=5,
        wits=3,
        alertness=2,
        occult=5,
        arete=7,
        willpower=8,
        description="Mad Progenitor conducting horrific experiments in Mexico City."
    )
    niles.spheres.create(sphere=Sphere.objects.get(name="Entropy"), rating=4)
    niles.spheres.create(sphere=Sphere.objects.get(name="Forces"), rating=3)
    niles.spheres.create(sphere=Sphere.objects.get(name="Life"), rating=5)
    niles.spheres.create(sphere=Sphere.objects.get(name="Matter"), rating=5)
    niles.spheres.create(sphere=Sphere.objects.get(name="Prime"), rating=5)
    niles.spheres.create(sphere=Sphere.objects.get(name="Time"), rating=3)

    # Joe "Boot" Hill - Assamite Antitribu
    joe = Vampire.objects.create(
        name='Joe "Boot" Hill',
        nature="Cavalier",
        demeanor="Gallant",
        clan="Assamite Antitribu",
        generation=7,
        sire="Bernard del Gado",
        strength=6,
        dexterity=5,
        stamina=6,
        charisma=4,
        manipulation=3,
        appearance=2,
        perception=6,
        intelligence=2,
        wits=4,
        alertness=4,
        brawl=5,
        firearms=5,
        melee=5,
        occult=5,
        willpower=8,
        age=143,
        apparent_age=27,
        description="Black Hand Dominion in Mexico City. Old West gunslinger turned vampire hunter."
    )

    # Archbishop Alicia Barrows - Malkavian Antitribu
    alicia = Vampire.objects.create(
        name="Alicia Barrows",
        nature="Fanatic",
        demeanor="Deviant",
        clan="Malkavian Antitribu",
        generation=6,
        sire="Andre Milano",
        strength=3,
        dexterity=5,
        stamina=4,
        charisma=5,
        manipulation=7,
        appearance=4,
        perception=5,
        intelligence=4,
        wits=6,
        alertness=4,
        brawl=3,
        leadership=5,
        occult=2,
        willpower=10,
        age=593,
        apparent_age=18,
        description="Malkavian Archbishop of Mexico City. Obsessed with preventing Gehenna."
    )

    # Harzomatuili - Black Spiral Dancer Leader
    black_spirals = Tribe.objects.get(name="Black Spiral Dancers")
    harzo = Werewolf.objects.create(
        name="Harzomatuili",
        breed="Homid",
        auspice="Ahroun",
        tribe=black_spirals,
        nature="Bravo",
        demeanor="Deviant",
        strength=5,
        dexterity=3,
        stamina=5,
        charisma=4,
        manipulation=5,
        appearance=0,
        perception=5,
        intelligence=4,
        wits=5,
        alertness=4,
        brawl=5,
        melee=5,
        occult=5,
        rank=6,
        glory=0,
        honor=0,
        wisdom=0,
        willpower=8,
        age=500,
        description="Leader of the Black Spiral Dancers in the Underbelly of the Wyrm."
    )

    print("Created minor NPCs from The Chaos Factor")


def create_templates():
    """Create generic character templates from The Chaos Factor."""

    # Skin Dancer Warrior Template
    skin_dancers = Tribe.objects.get(name="Skin Dancers")
    skin_dancer_warrior = Werewolf.objects.create(
        name="Skin Dancer Warrior (Template)",
        breed="Homid",  # False Garou, actually human
        auspice="Ahroun",
        tribe=skin_dancers,
        nature="Bravo",
        demeanor="Monster",
        strength=4,
        dexterity=3,
        stamina=4,
        charisma=2,
        manipulation=2,
        appearance=1,
        perception=3,
        intelligence=2,
        wits=3,
        alertness=3,
        athletics=3,
        brawl=4,
        intimidation=3,
        melee=3,
        stealth=2,
        occult=1,
        rank=2,
        glory=0,
        honor=0,
        wisdom=0,
        willpower=5,
        description="A false Garou created through dark rituals by Samuel Haight. Wears the skin of a true werewolf and can shapeshift, but lacks spiritual connection to Gaia.",
    )

    # Black Spiral Dancer Pack Member Template
    black_spirals = Tribe.objects.get(name="Black Spiral Dancers")
    spiral_pack = Werewolf.objects.create(
        name="Black Spiral Dancer Pack Member (Template)",
        breed="Homid",
        auspice="Ahroun",
        tribe=black_spirals,
        nature="Deviant",
        demeanor="Bravo",
        strength=4,
        dexterity=3,
        stamina=4,
        charisma=2,
        manipulation=3,
        appearance=2,
        perception=3,
        intelligence=2,
        wits=3,
        alertness=3,
        athletics=4,
        brawl=4,
        intimidation=4,
        melee=3,
        occult=2,
        rank=3,
        glory=0,
        honor=0,
        wisdom=0,
        willpower=6,
        description="Corrupted Garou serving the Wyrm. Found in the Underbelly beneath Mexico City.",
    )

    # Sabbat Pack Priest Template
    sabbat_priest = Vampire.objects.create(
        name="Sabbat Pack Priest (Template)",
        nature="Fanatic",
        demeanor="Martyr",
        clan="Lasombra",
        generation=9,
        sire="Unknown",
        strength=3,
        dexterity=3,
        stamina=3,
        charisma=3,
        manipulation=4,
        appearance=2,
        perception=3,
        intelligence=3,
        wits=3,
        alertness=2,
        brawl=3,
        leadership=3,
        occult=4,
        willpower=7,
        age=150,
        apparent_age=25,
        description="Typical Sabbat pack priest in Mexico City. Leads the pack in Vaulderie and maintains their spiritual connection to the sect.",
    )

    # Sabbat Ductus (Pack Leader) Template
    sabbat_ductus = Vampire.objects.create(
        name="Sabbat Ductus (Template)",
        nature="Director",
        demeanor="Bravo",
        clan="Brujah Antitribu",
        generation=8,
        sire="Unknown",
        strength=4,
        dexterity=4,
        stamina=4,
        charisma=3,
        manipulation=3,
        appearance=2,
        perception=3,
        intelligence=2,
        wits=4,
        alertness=3,
        brawl=4,
        firearms=3,
        leadership=4,
        melee=4,
        intimidation=4,
        occult=2,
        willpower=7,
        age=200,
        apparent_age=30,
        description="Sabbat pack leader responsible for tactical decisions and pack coordination.",
    )

    # Technocracy Hit Mark Template
    nwo = MageFaction.objects.get(name="New World Order")
    hit_mark = Mage.objects.create(
        name="Technocracy Hit Mark (Template)",
        nature="Soldier",
        demeanor="Conformist",
        essence="Pattern",
        affiliation=nwo,
        strength=3,
        dexterity=4,
        stamina=3,
        charisma=2,
        manipulation=2,
        appearance=2,
        perception=4,
        intelligence=3,
        wits=4,
        alertness=4,
        athletics=3,
        brawl=3,
        firearms=4,
        melee=3,
        stealth=3,
        computer=2,
        occult=2,
        arete=3,
        willpower=6,
        description="Standard Technocracy field agent. Armed with advanced weapons and reality stabilization equipment.",
    )
    hit_mark.spheres.create(sphere=Sphere.objects.get(name="Correspondence"), rating=2)
    hit_mark.spheres.create(sphere=Sphere.objects.get(name="Forces"), rating=3)
    hit_mark.spheres.create(sphere=Sphere.objects.get(name="Matter"), rating=2)
    hit_mark.spheres.create(sphere=Sphere.objects.get(name="Prime"), rating=2)

    # Iteration X Scientist Template
    iter_x = MageFaction.objects.get(name="Iteration X")
    iter_scientist = Mage.objects.create(
        name="Iteration X Scientist (Template)",
        nature="Architect",
        demeanor="Perfectionist",
        essence="Questing",
        affiliation=iter_x,
        strength=2,
        dexterity=2,
        stamina=2,
        charisma=2,
        manipulation=3,
        appearance=2,
        perception=3,
        intelligence=4,
        wits=3,
        computer=4,
        investigation=3,
        science=4,
        technology=4,
        occult=3,
        arete=4,
        willpower=6,
        description="Iteration X researcher focused on cybernetic enhancement and technological advancement.",
    )
    iter_scientist.spheres.create(sphere=Sphere.objects.get(name="Forces"), rating=3)
    iter_scientist.spheres.create(sphere=Sphere.objects.get(name="Life"), rating=2)
    iter_scientist.spheres.create(sphere=Sphere.objects.get(name="Matter"), rating=3)
    iter_scientist.spheres.create(sphere=Sphere.objects.get(name="Prime"), rating=2)

    # Bone Gnawer Street Warrior Template
    bone_gnawers = Tribe.objects.get(name="Bone Gnawers")
    bone_gnawer = Werewolf.objects.create(
        name="Bone Gnawer Street Warrior (Template)",
        breed="Homid",
        auspice="Ahroun",
        tribe=bone_gnawers,
        nature="Survivor",
        demeanor="Caregiver",
        strength=3,
        dexterity=3,
        stamina=3,
        charisma=2,
        manipulation=3,
        appearance=2,
        perception=3,
        intelligence=2,
        wits=4,
        alertness=4,
        athletics=3,
        brawl=4,
        streetwise=4,
        melee=3,
        stealth=3,
        survival=3,
        occult=1,
        rank=2,
        glory=0,
        honor=0,
        wisdom=0,
        willpower=5,
        description="Member of the Sweet Water Sept in Mexico City. Defender of the homeless and downtrodden.",
    )

    # Nephandi Corruptor Template
    nephandi = MageFaction.objects.get(name="Nephandi")
    nephandi_corruptor = Mage.objects.create(
        name="Nephandi Corruptor (Template)",
        nature="Deviant",
        demeanor="Confidant",
        essence="Primordial",
        affiliation=nephandi,
        strength=2,
        dexterity=3,
        stamina=2,
        charisma=4,
        manipulation=4,
        appearance=3,
        perception=3,
        intelligence=3,
        wits=3,
        subterfuge=4,
        occult=4,
        intimidation=3,
        arete=4,
        willpower=7,
        description="Fallen mage who serves the Wyrm. Works to corrupt others and spread darkness.",
    )
    nephandi_corruptor.spheres.create(sphere=Sphere.objects.get(name="Entropy"), rating=3)
    nephandi_corruptor.spheres.create(sphere=Sphere.objects.get(name="Mind"), rating=3)
    nephandi_corruptor.spheres.create(sphere=Sphere.objects.get(name="Spirit"), rating=2)
    nephandi_corruptor.spheres.create(sphere=Sphere.objects.get(name="Prime"), rating=2)

    # Nosferatu Antitribu Warren Dweller Template
    nos_antitribu = Vampire.objects.create(
        name="Nosferatu Antitribu Warren Dweller (Template)",
        nature="Survivor",
        demeanor="Loner",
        clan="Nosferatu Antitribu",
        generation=10,
        sire="Unknown",
        strength=4,
        dexterity=3,
        stamina=4,
        charisma=1,
        manipulation=3,
        appearance=0,
        perception=4,
        intelligence=3,
        wits=4,
        alertness=3,
        stealth=4,
        survival=3,
        investigation=3,
        occult=2,
        willpower=6,
        age=120,
        apparent_age=30,
        description="Nosferatu living in the Warren beneath Mexico City. Shares space with Nephandi and Black Spiral Dancers in the Underbelly.",
    )

    print("Created character templates from The Chaos Factor")


def create_items():
    """Create magical items from The Chaos Factor."""

    # Staff of the World Tree - Haight's main weapon
    staff = Wonder.objects.create(
        name="Staff of the World Tree",
        rank=5,
        description="A massive staff carved from the World Tree of the Crombey Farm Chantry. "
                   "Glows with stolen Quintessence and grants powerful countermagick abilities. "
                   "The staff is actually a Paradox battery that will eventually explode.",
        background="Stolen by Samuel Haight from the Verbena Chantry. Made from a branch of their sacred World Tree.",
        quintessence_max=200,
        is_unique=True,
    )

    # Sun Lamp - Anti-vampire weapon
    sun_lamp = Wonder.objects.create(
        name="Sun Lamp",
        rank=4,
        description="A device that releases stored and magnified solar radiation in a beam. "
                   "Designed to harm vampires with artificial sunlight.",
        background="Created by Samuel Haight using Forces and Prime magic to store solar energy.",
        quintessence_max=20,
        is_unique=True,
    )

    # The Virgin's Tear - Sacrificial dagger
    tear = Wonder.objects.create(
        name="The Virgin's Tear",
        rank=4,
        description="A sacrificial dagger with a four-foot blade. Enchanted to allow the bearer "
                   "to return to the Caul of the Pandemonium from anywhere when heavily injured.",
        background="Used by Amelio Santa Lucien in dark rituals.",
        quintessence_max=10,
        is_unique=True,
    )

    # Father Machete's Machete
    machete_fetish = Fetish.objects.create(
        name="Machete of Rage",
        rank=4,
        gnosis=6,
        description="A massive silver-edged machete that grants 1 Rage point per turn, "
                   "but only for attacking with the weapon. Allows at least two strikes per round.",
        background="Father Machete's signature weapon.",
        is_unique=True,
    )

    # Stone Bag
    stone_bag = Fetish.objects.create(
        name="Stone Bag",
        rank=4,
        gnosis=5,
        description="A battered leather bag with several pockets that can store Gnosis. "
                   "Weighs normally for the bearer but becomes extremely heavy (thousands of pounds) "
                   "for anyone trying to take it by force. Causes 4 extra dice of damage when used as a weapon.",
        background="Carried by Mother Baggy Pants of the Sweet Water Sept.",
        is_unique=True,
    )

    # Mask of Death
    mask = Fetish.objects.create(
        name="Mask of Death",
        rank=5,
        gnosis=8,
        description="A wooden skull mask that allows the wearer to be completely ignored by everyone, "
                   "even in Crinos form. The wearer can take any form and not be noticed. "
                   "Effect ends if the wearer makes a violent action against a target.",
        background="Special fetish created by the Bone Gnawers of Mexico City for the Days of the Dead.",
        is_unique=False,
    )

    # Thunderwyrm Egg
    egg = Fetish.objects.create(
        name="Thunderwyrm Egg",
        rank=4,
        gnosis=8,
        description="A small thunderwyrm preserved in amber. When activated, calls any thunderwyrms "
                   "within 50 miles to aid the bearer. If none exist, the egg hatches and the "
                   "thunderwyrm doubles in size and becomes a willing slave. Single use if hatched.",
        background="Carried by Harzomatuili, leader of the Black Spiral Dancers.",
        is_unique=True,
    )

    print("Created items from The Chaos Factor")


def create_locations():
    """Create important locations from The Chaos Factor."""

    # Mexico City
    mexico_city = City.objects.create(
        name="Mexico City",
        description="Capital of Mexico and largest city in the Americas. Home to over 20 million people. "
                   "Stronghold of the Sabbat in North America. Heavily polluted and corrupt.",
        population=20000000,
    )

    # The Underbelly of the Wyrm
    underbelly = Location.objects.create(
        name="The Underbelly of the Wyrm",
        parent=mexico_city,
        description="A massive underground complex beneath Mexico City, combining a Black Spiral Dancer Hive, "
                   "Nephandi Labyrinth, and Nosferatu Warren. Home to the Pandemonium, a living cancerous entity "
                   "that serves as a Caul for the Nephandi. Contains several powerful hidden Nodes.",
        gauntlet_rating=2,
    )

    # The Pandemonium
    pandemonium = Node.objects.create(
        name="The Pandemonium",
        parent=underbelly,
        rank=5,
        description="A massive, pulsing black entity growing from the ruins of Huitzilopoctli's pyramid. "
                   "Living cancerous growth that filters mage Avatars through corruption. Contains the Nephandi Caul "
                   "and connection to the Black Spiral. Defended by corrupted Men in Black.",
        quintessence_per_week=50,
        quintessence_form="Angst and suffering",
        gauntlet_rating=2,
    )

    # Shrine of the Virgin of Guadalupe
    shrine = Node.objects.create(
        name="Shrine of the Virgin of Guadalupe",
        parent=mexico_city,
        rank=4,
        description="Powerful Node and holy site. One of the few Nodes not held by the Technocracy. "
                   "Considered Holy Ground. Original temple to Tonantzin destroyed by Conquistadors. "
                   "The Celestial Chorus maintains strong influence here.",
        quintessence_per_week=20,
        quintessence_form="Faith and devotion",
        gauntlet_rating=4,
    )

    # Paraiso Vista
    paraiso = Location.objects.create(
        name="Paraiso Vista",
        description="A small, peaceful town of 432 people about 80 miles north of Mexico City. "
                   "Completely untouched by the Wyrm and modern corruption. Protected by Huitzilopoctli "
                   "for 300 years as his personal preserve. The people want for nothing and live in harmony.",
        population=432,
    )

    # Huitzilopoctli's Haven
    haven = Location.objects.create(
        name="Dragon's Lair",
        parent=paraiso,
        description="Hidden Haven of Shaitan/Huitzilopoctli carved into a mountain north of Paraiso Vista. "
                   "Entrance hidden behind a stream, concealed by a massive stone dragon head. "
                   "Contains the bodies of four failed Childer, an antechamber with four preserved hearts, "
                   "and the main chamber with a stone altar and Shaitan's resting place.",
    )

    # Tower of Al Durab
    tower = Location.objects.create(
        name="Tower of Al Durab",
        description="A legendary Hermetic Chantry in the Jordanian desert. Changes size and appearance constantly. "
                   "Home to isolationist mages dedicated to studying the Kabbalah. Protected by golems and sand storms. "
                   "No new members have joined in over 400 years. All mages here are Masters or Oracles.",
        gauntlet_rating=3,
    )

    # Lake Tezcoco
    lake = Location.objects.create(
        name="Lake Tezcoco",
        parent=mexico_city,
        description="Ancient lake where Tenochtitlan once stood. Now heavily polluted. "
                   "Waters run deep over the Underbelly of the Wyrm. Contains a scale model of ancient Tenochtitlan "
                   "that causes visions and plants seeds of Wyrm corruption. Swarming with Banes.",
        gauntlet_rating=2,
    )

    # Zona Rosa
    zona = Location.objects.create(
        name="Zona Rosa",
        parent=mexico_city,
        description="Wealthy shopping district with elegant restaurants and international shops. "
                   "The only 'safe' area in Mexico City during most times. During Days of the Dead, anything goes.",
        population=50000,
    )

    # Sweet Water Sept Territory (Alameda Park)
    alameda = Location.objects.create(
        name="Alameda Park",
        parent=mexico_city,
        description="260 square mile park in the heart of Mexico City. Home territory of the Sweet Water Sept "
                   "of Bone Gnawers. Contains museums, monuments, and the Olympic Sports Center. "
                   "No formal caern exists here, but the Bone Gnawers defend it fiercely.",
    )

    print("Created locations from The Chaos Factor")


if __name__ == "__main__":
    create_chaos_factor_data()
    print("\nCompleted populating The Chaos Factor data!")
