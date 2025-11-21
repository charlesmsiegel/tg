from characters.models.demon.apocalyptic_form import ApocalypticFormTrait
from characters.models.demon.house import DemonHouse
from characters.models.demon.visage import Visage

# Get the houses
from populate_db.demon_houses import defilers, devourers, devils, fiends, malefactors, scourges, slayers

ApocalypticFormTrait.objects.get_or_create(name="Armor", cost=4, house=None)[
    0
].add_source("Demon Players Guide", 98)
ApocalypticFormTrait.objects.get_or_create(
    name="Casts No Reflection", cost=2, house=None
)[0].add_source("Demon Players Guide", 98)
ApocalypticFormTrait.objects.get_or_create(
    name="Claws/Teeth", cost=1, house=None, high_torment_only=True
)[0].add_source("Demon Players Guide", 98)
ApocalypticFormTrait.objects.get_or_create(
    name="Damage Resistance", cost=3, house=None
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(name="Enhanced Ability", cost=3, house=None)[
    0
].add_source("Demon Players Guide", 98)
ApocalypticFormTrait.objects.get_or_create(name="Enhanced Senses", cost=3, house=None)[
    0
].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Mental Acuity", cost=4, house=None
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Social Traits", cost=4, house=None
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(name="Extra Actions", cost=3, house=None)[
    0
].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(
    name="Extra Health Levels", cost=3, house=None
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(
    name="Extra Limbs", cost=3, house=None, high_torment_only=True
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(
    name="Gaping Maw", cost=2, house=None, high_torment_only=True
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(
    name="Horns", cost=1, house=None, high_torment_only=True
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(
    name="Improved Attribute", cost=3, house=None
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(
    name="Improved Initiative", cost=1, house=None
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(name="Increased Size", cost=3, house=None)[
    0
].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(
    name="Lashing Tail", cost=1, house=None, high_torment_only=True
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(
    name="Pass Without Trace", cost=2, house=None
)[0].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(name="Regeneration", cost=4, house=None)[
    0
].add_source("Demon Players Guide", 99)
ApocalypticFormTrait.objects.get_or_create(name="Wings", cost=3, house=None)[
    0
].add_source("Demon Players Guide", 99)

# Defiler abilities
ApocalypticFormTrait.objects.get_or_create(name="Alter Size", cost=3, house=defilers)[
    0
].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(name="Distortion", cost=3, house=defilers)[
    0
].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Empathy", cost=1, house=defilers
)[0].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Intuition", cost=1, house=defilers
)[0].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(
    name="Ichor", cost=2, house=defilers, high_torment_only=True
)[0].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Electricity", cost=2, house=defilers
)[0].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(
    name="Improved Dexterity", cost=2, house=defilers
)[0].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(name="Ink Cloud", cost=2, house=defilers)[
    0
].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(
    name="Lyrical Voice", cost=1, house=defilers
)[0].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(name="Sea's Beauty", cost=3, house=defilers)[
    0
].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(
    name="Shark Hide", cost=3, house=defilers, high_torment_only=True
)[0].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(
    name="Shocking Touch", cost=2, house=defilers
)[0].add_source("Demon Players Guide", 100)
ApocalypticFormTrait.objects.get_or_create(name="Spines", cost=2, house=defilers)[
    0
].add_source("Demon Players Guide", 101)
ApocalypticFormTrait.objects.get_or_create(
    name="Venom", cost=3, house=defilers, high_torment_only=True
)[0].add_source("Demon Players Guide", 101)
ApocalypticFormTrait.objects.get_or_create(
    name="Weather Sense", cost=1, house=defilers
)[0].add_source("Demon Players Guide", 101)

# Devil abilities
ApocalypticFormTrait.objects.get_or_create(name="Affirm", cost=3, house=devils)[
    0
].add_source("Demon Players Guide", 101)
ApocalypticFormTrait.objects.get_or_create(name="Beckon", cost=2, house=devils)[
    0
].add_source("Demon Players Guide", 101)
ApocalypticFormTrait.objects.get_or_create(
    name="Corrosive Spit", cost=2, house=devils, high_torment_only=True
)[0].add_source("Demon Players Guide", 101)
ApocalypticFormTrait.objects.get_or_create(name="Dread Gaze", cost=4, house=devils)[
    0
].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Fiery Blood", cost=4, house=devils, high_torment_only=True
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(name="Immune to Fire", cost=3, house=devils)[
    0
].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Increased Awareness", cost=2, house=devils
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(name="Inhuman Allure", cost=2, house=devils)[
    0
].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(name="Lordly Mien", cost=2, house=devils)[
    0
].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(name="Radiant Aura", cost=1, house=devils)[
    0
].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Scales", cost=3, house=devils, high_torment_only=True
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Sense the Hidden", cost=1, house=devils
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(name="Spark of Faith", cost=3, house=devils)[
    0
].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="The Host", cost=2, house=devils, high_torment_only=True
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Voice of the Damned", cost=1, house=devils
)[0].add_source("Demon Players Guide", 102)

# Devourer abilities
ApocalypticFormTrait.objects.get_or_create(
    name="Aura of Vitality", cost=4, house=devourers
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Chameleon Skin", cost=1, house=devourers
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Disperse", cost=3, house=devourers, high_torment_only=True
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Social Traits", cost=3, house=devourers
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Survival", cost=1, house=devourers
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Frenzy", cost=2, house=devourers, high_torment_only=True
)[0].add_source("Demon Players Guide", 102)
ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Poisons", cost=3, house=devourers
)[0].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(
    name="Natural Weaponry", cost=3, house=devourers
)[0].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(
    name="Nimble Hunter", cost=3, house=devourers
)[0].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(
    name="Primal Mind", cost=3, house=devourers, high_torment_only=True
)[0].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(name="Relentless", cost=1, house=devourers)[
    0
].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(
    name="Sun's Bounty", cost=2, house=devourers
)[0].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(name="Thick Hide", cost=2, house=devourers)[
    0
].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(name="Thorns", cost=1, house=devourers)[
    0
].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(
    name="Toxins", cost=3, house=devourers, high_torment_only=True
)[0].add_source("Demon Players Guide", 103)

# Fiend abilities
ApocalypticFormTrait.objects.get_or_create(
    name="Aura of Misfortune", cost=3, house=fiends, high_torment_only=True
)[0].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(
    name="Cloak of Shadows", cost=2, house=fiends
)[0].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(
    name="Chimerical Attack", cost=3, house=fiends, high_torment_only=True
)[0].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(name="Dread Mien", cost=1, house=fiends)[
    0
].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(name="Enhanced Dodge", cost=1, house=fiends)[
    0
].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Intuition", cost=1, house=fiends
)[0].add_source("Demon Players Guide", 103)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Mental Acuity", cost=3, house=fiends
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(name="Eyes of Fate", cost=4, house=fiends)[
    0
].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Hypnotic Visions", cost=3, house=fiends
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Increased Awareness", cost=1, house=fiends
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(name="Night Sight", cost=2, house=fiends)[
    0
].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Rend the Soul", cost=3, house=fiends, high_torment_only=True
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Sense the Hidden", cost=1, house=fiends
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Sibilant Whispers", cost=1, house=fiends
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Unearthly Glamour", cost=1, house=fiends
)[0].add_source("Demon Players Guide", 104)

# Malefactor abilities
ApocalypticFormTrait.objects.get_or_create(
    name="Alter Size", cost=3, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Conjuration", cost=2, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Dead Reckoning", cost=1, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Ichor", cost=2, house=malefactors, high_torment_only=True
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Bashing Damage", cost=4, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Fire", cost=3, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(name="Iron Skin", cost=3, house=malefactors)[
    0
].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Irresistible Force", cost=2, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Magnetic Field", cost=2, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Master Artisan", cost=1, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Night Sight", cost=2, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Relentless", cost=1, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Spikes", cost=1, house=malefactors, high_torment_only=True
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Thunderous Voice", cost=3, house=malefactors
)[0].add_source("Demon Players Guide", 104)
ApocalypticFormTrait.objects.get_or_create(
    name="Tremor Sense", cost=3, house=malefactors
)[0].add_source("Demon Players Guide", 104)

# Scourge abilities
ApocalypticFormTrait.objects.get_or_create(
    name="Aura of Vitality", cost=4, house=scourges
)[0].add_source("Demon Players Guide", 105)
ApocalypticFormTrait.objects.get_or_create(
    name="Caustic Bile", cost=2, house=scourges, high_torment_only=True
)[0].add_source("Demon Players Guide", 105)
ApocalypticFormTrait.objects.get_or_create(
    name="Cloak of Shadows", cost=2, house=scourges
)[0].add_source("Demon Players Guide", 105)
ApocalypticFormTrait.objects.get_or_create(
    name="Dead Reckoning", cost=1, house=scourges
)[0].add_source("Demon Players Guide", 105)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Dodge", cost=1, house=scourges
)[0].add_source("Demon Players Guide", 105)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Intuition", cost=1, house=scourges
)[0].add_source("Demon Players Guide", 105)
ApocalypticFormTrait.objects.get_or_create(
    name="Immune to Falling Damage", cost=2, house=scourges
)[0].add_source("Demon Players Guide", 105)
ApocalypticFormTrait.objects.get_or_create(
    name="Improved Physical Capabilities", cost=3, house=scourges
)[0].add_source("Demon Players Guide", 105)
ApocalypticFormTrait.objects.get_or_create(
    name="Miasma", cost=3, house=scourges, high_torment_only=True
)[0].add_source("Demon Players Guide", 105)
ApocalypticFormTrait.objects.get_or_create(name="Mist", cost=4, house=scourges)[
    0
].add_source("Demon Players Guide", 105)
ApocalypticFormTrait.objects.get_or_create(
    name="Multiple Eyes", cost=2, house=scourges, high_torment_only=True
)[0].add_source("Demon Players Guide", 106)
ApocalypticFormTrait.objects.get_or_create(
    name="Perfect Balance", cost=1, house=scourges
)[0].add_source("Demon Players Guide", 106)
ApocalypticFormTrait.objects.get_or_create(
    name="Quills", cost=1, house=scourges, high_torment_only=True
)[0].add_source("Demon Players Guide", 106)
ApocalypticFormTrait.objects.get_or_create(
    name="Supernatural Vision", cost=1, house=scourges
)[0].add_source("Demon Players Guide", 106)
ApocalypticFormTrait.objects.get_or_create(
    name="Viscous Flesh", cost=2, house=scourges, high_torment_only=True
)[0].add_source("Demon Players Guide", 106)

# Slayer abilities
ApocalypticFormTrait.objects.get_or_create(
    name="Aura of Dread", cost=2, house=slayers, high_torment_only=True
)[0].add_source("Demon Players Guide", 106)
ApocalypticFormTrait.objects.get_or_create(
    name="Aura of Entropy", cost=2, house=slayers, high_torment_only=True
)[0].add_source("Demon Players Guide", 106)
ApocalypticFormTrait.objects.get_or_create(
    name="Cloak of Shadows", cost=2, house=slayers
)[0].add_source("Demon Players Guide", 106)
ApocalypticFormTrait.objects.get_or_create(name="Conjuration", cost=2, house=slayers)[
    0
].add_source("Demon Players Guide", 106)
ApocalypticFormTrait.objects.get_or_create(
    name="Dead Reckoning", cost=1, house=slayers
)[0].add_source("Demon Players Guide", 106)
ApocalypticFormTrait.objects.get_or_create(name="Death-Grip", cost=4, house=slayers)[
    0
].add_source("Demon Players Guide", 106)
ApocalypticFormTrait.objects.get_or_create(name="Dread Gaze", cost=4, house=slayers)[
    0
].add_source("Demon Players Guide", 107)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Awareness", cost=2, house=slayers
)[0].add_source("Demon Players Guide", 107)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Social Traits", cost=3, house=slayers
)[0].add_source("Demon Players Guide", 107)
ApocalypticFormTrait.objects.get_or_create(name="Ghost Sight", cost=2, house=slayers)[
    0
].add_source("Demon Players Guide", 107)
ApocalypticFormTrait.objects.get_or_create(
    name="Howl of the Damned", cost=1, house=slayers
)[0].add_source("Demon Players Guide", 107)
ApocalypticFormTrait.objects.get_or_create(name="Night Sight", cost=1, house=slayers)[
    0
].add_source("Demon Players Guide", 107)
ApocalypticFormTrait.objects.get_or_create(
    name="Reaper's Breath", cost=3, house=slayers, high_torment_only=True
)[0].add_source("Demon Players Guide", 107)
ApocalypticFormTrait.objects.get_or_create(name="Relentless", cost=1, house=slayers)[
    0
].add_source("Demon Players Guide", 107)
ApocalypticFormTrait.objects.get_or_create(
    name="Touch of Death", cost=3, house=slayers
)[0].add_source("Demon Players Guide", 107)

# Additional traits needed for visages (from Demon: The Fallen core book)
ApocalypticFormTrait.objects.get_or_create(
    name="Shroud of Flames", cost=1, house=devils
)[0].add_source("Demon: The Fallen", 178)
ApocalypticFormTrait.objects.get_or_create(
    name="Immunity to Fire", cost=3, house=devils
)[0].add_source("Demon: The Fallen", 178)
ApocalypticFormTrait.objects.get_or_create(
    name="Chimerical Aura", cost=1, house=fiends
)[0].add_source("Demon: The Fallen", 198)
ApocalypticFormTrait.objects.get_or_create(
    name="Voice of the Grave", cost=1, house=slayers
)[0].add_source("Demon: The Fallen", 215)
ApocalypticFormTrait.objects.get_or_create(
    name="Conjure from Nothing", cost=2, house=slayers
)[0].add_source("Demon: The Fallen", 215)
ApocalypticFormTrait.objects.get_or_create(name="Mirage", cost=2, house=malefactors)[
    0
].add_source("Demon: The Fallen", 190)
ApocalypticFormTrait.objects.get_or_create(
    name="Flashing Fingers", cost=2, house=malefactors
)[0].add_source("Demon: The Fallen", 190)
ApocalypticFormTrait.objects.get_or_create(
    name="Enhanced Perception", cost=3, house=malefactors
)[0].add_source("Demon: The Fallen", 189)
ApocalypticFormTrait.objects.get_or_create(
    name="Night Vision", cost=2, house=malefactors
)[0].add_source("Demon: The Fallen", 188)
ApocalypticFormTrait.objects.get_or_create(
    name="Blades", cost=1, house=malefactors, high_torment_only=True
)[0].add_source("Demon: The Fallen", 192)

# DEVIL VISAGES
# Bel, the Visage of the Celestials
bel = Visage.objects.get_or_create(
    name="Bel",
    house=devils,
    defaults={
        "description": "The apocalyptic form of the Lore of the Celestials reveals the fallen as a luminous, lordly angel, radiating divine grandeur and authority. Her skin literally glows, wreathing her in an aura of golden light that shifts in intensity depending on her mood. Her eyes blaze with the cold light of the stars. Despite her actual physical appearance, the fallen seems to tower over everyone around her."
    },
)[0]
bel.add_source("Demon: The Fallen", 176)
bel.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Wings", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Lordly Mien", house=devils)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Senses", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Increased Awareness", house=devils)[0],
    ]
)
bel.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Claws/Teeth", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Scales", house=devils)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Increased Size", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Dread Gaze", house=devils)[0],
    ]
)

# Nusku, the Visage of the Flames
nusku = Visage.objects.get_or_create(
    name="Nusku",
    house=devils,
    defaults={
        "description": "These demons reveal themselves in a blaze of yellow-orange light. Their skin glows with the seething brilliance of the sun, and their image shimmers like a mirage. Their eyes take on the color of burnished gold, and when angered, the Nusku radiate palpable waves of heat. An angel's hair becomes a deep red or reddish-gold and thickens into a leonine mane. Open flames flare brightly in his presence, seeming to bow toward their master as the tongues of flame are drawn to the divinity in their midst."
    },
)[0]
nusku.add_source("Demon: The Fallen", 178)
nusku.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Shroud of Flames", house=devils)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Immunity to Fire", house=devils)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Actions", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Improved Initiative", house=None)[0],
    ]
)
nusku.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Claws/Teeth", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Lashing Tail", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Increased Size", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Fiery Blood", house=devils)[0],
    ]
)

# Qingu, the Visage of Radiance
qingu = Visage.objects.get_or_create(
    name="Qingu",
    house=devils,
    defaults={
        "description": "The apocalyptic form of the masters of Radiance is an incandescent figure wreathed in a corona of jewel-like color. Their physical features have more in common with the smooth perfection of marble than with human skin. Their voices are pure as crystal, and they cut through the petty din of the mortal world like a razor."
    },
)[0]
qingu.add_source("Demon: The Fallen", 180)
qingu.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Wings", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Inhuman Allure", house=devils)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Radiant Aura", house=devils)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Sense the Hidden", house=devils)[0],
    ]
)
qingu.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Voice of the Damned", house=devils)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Casts No Reflection", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Corrosive Spit", house=devils)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Horns", house=None)[0],
    ]
)

# SCOURGE VISAGES
# Dagan, the Visage of Awakenings
dagan = Visage.objects.get_or_create(
    name="Dagan",
    house=scourges,
    defaults={
        "description": "The apocalyptic form of the masters of animation infuses the angel's mortal body with the blush of youth and vibrant health - even the oldest mortal vessel appears to be in the prime of life and moves with inhuman grace, speed and strength. This aura of life and vitality radiates as a palpable sense of warmth, like a beam of sunlight, and every living being touched is temporarily suffused with its power. Wilted flowers return to full bloom, the injured gain strength and the old forget their afflictions."
    },
)[0]
dagan.add_source("Demon: The Fallen", 182)
dagan.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Aura of Vitality", house=scourges)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Pass Without Trace", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(
            name="Improved Physical Capabilities", house=scourges
        ),
        ApocalypticFormTrait.objects.get_or_create(name="Wings", house=None)[0],
    ]
)
dagan.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Miasma", house=scourges)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Health Levels", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Viscous Flesh", house=scourges)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Limbs", house=None)[0],
    ]
)

# Anshar, the Visage of the Firmament
anshar = Visage.objects.get_or_create(
    name="Anshar",
    house=scourges,
    defaults={
        "description": "These Angels of the Firmament reveal themselves as lithe, ethereal figures with pale skin and large gray eyes. When they speak, their voice echoes faintly, as if from a great distance, and they alternate between bouts of quiet distraction and periods of intense, disquieting scrutiny."
    },
)[0]
anshar.add_source("Demon: The Fallen", 184)
anshar.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Senses", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Wings", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Intuition", house=scourges)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Dodge", house=scourges)[0],
    ]
)
anshar.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Cloak of Shadows", house=scourges)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Multiple Eyes", house=scourges)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Improved Initiative", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Claws/Teeth", house=None)[0],
    ]
)

# Ellil, the Visage of the Winds
ellil = Visage.objects.get_or_create(
    name="Ellil",
    house=scourges,
    defaults={
        "description": "The monarchs of the air reveal themselves as tall and lithe, with large eyes and swift, graceful movements. When in revelatory form, the Ellil are constantly surrounded by shifting winds that ebb and flow with the intensity of their emotions. Any smoke or steam in the area is often sucked by these winds into a swirling vortex that circles their heads and shoulders like an ominous halo."
    },
)[0]
ellil.add_source("Demon: The Fallen", 185)
ellil.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Supernatural Vision", house=scourges)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Wings", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Perfect Balance", house=scourges)[0],
        ApocalypticFormTrait.objects.get_or_create(
            name="Immune to Falling Damage", house=scourges
        ),
    ]
)
ellil.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Claws/Teeth", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Actions", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Quills", house=scourges)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Caustic Bile", house=scourges)[0],
    ]
)

# MALEFACTOR VISAGES
# Kishar, the Visage of the Earth
kishar = Visage.objects.get_or_create(
    name="Kishar",
    house=malefactors,
    defaults={
        "description": "These angels manifest as towering figures with dark skin that ranges from a creamy brown to utter black, and their bodies appear as though hewn from stone, with muscle and bone etched in sharp relief on a frame devoid of soft flesh or fat. The Kishar are hairless, and the irises of their eyes have the clarity and color of gemstones: ruby, sapphire, emerald, garnet, topaz and diamond. The air about them smells of freshly turned earth, rich with the promise of life."
    },
)[0]
kishar.add_source("Demon: The Fallen", 188)
kishar.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Increased Size", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(
            name="Immune to Bashing Damage", house=malefactors
        ),
        ApocalypticFormTrait.objects.get_or_create(name="Irresistible Force", house=malefactors)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Night Vision", house=malefactors)[0],
    ]
)
kishar.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Extra Limbs", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Gaping Maw", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Spikes", house=malefactors)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Ichor", house=malefactors)[0],
    ]
)

# Antu, the Visage of the Paths
antu = Visage.objects.get_or_create(
    name="Antu",
    house=malefactors,
    defaults={
        "description": "The angels of the pathways closely resemble mortals at first glance. Their skin is deeply tanned, as though they'd spent a lifetime in the sun, and the skin around their dark eyes are deeply lined, casting their orbits in permanent shadow. It is only on closer inspection that the worry lines are revealed as intricate patterns that radiate from the angel's eyes and continue to run across the planes of her face, disappearing into her scalp and circling her throat in intricate tattoos. At night these lines reflect the moonlight in ghostly traceries that seem to shift and realign themselves as the angel speaks."
    },
)[0]
antu.add_source("Demon: The Fallen", 189)
antu.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Dead Reckoning", house=malefactors)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Perception", house=malefactors)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Improved Initiative", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Flashing Fingers", house=malefactors)[0],
    ]
)
antu.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Pass Without Trace", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Alter Size", house=malefactors)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Mirage", house=malefactors)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Relentless", house=malefactors)[0],
    ]
)

# Mummu, the Visage of the Forge
mummu = Visage.objects.get_or_create(
    name="Mummu",
    house=malefactors,
    defaults={
        "description": "The angels of the forge appear as giants hammered from the black iron of the earth, their powerfully muscled forms lit with veins of hot magma, and their eyes shining like disks of burnished brass. Their voices are deep and thunderous, like the roar of a furnace. When in their apocalyptic form, these fallen are immune to extremes of temperature and pressure. They can handle hot coals as mortals do ice cubes."
    },
)[0]
mummu.add_source("Demon: The Fallen", 191)
mummu.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Master Artisan", house=malefactors)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Increased Size", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Thunderous Voice", house=malefactors)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Immune to Fire", house=malefactors)[0],
    ]
)
mummu.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Blades", house=malefactors)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Limbs", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Magnetic Field", house=malefactors)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Iron Skin", house=malefactors)[0],
    ]
)

# FIEND VISAGES
# Ninsun, the Visage of Patterns
ninsun = Visage.objects.get_or_create(
    name="Ninsun",
    house=fiends,
    defaults={
        "description": "The angels of the great pattern have skins of indigo. Their hairless bodies are covered with intricate lines and patterns etched in silvery blue light that shifts and realigns depending on the angle of light and the intensity of the angel's mood. Their eyes are like bright sapphires, casting the cold light of the stars."
    },
)[0]
ninsun.add_source("Demon: The Fallen", 194)
ninsun.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Wings", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Improved Initiative", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Intuition", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Mental Acuity", house=fiends)[0],
    ]
)
ninsun.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Aura of Misfortune", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Actions", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Limbs", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Sibilant Whispers", house=fiends)[0],
    ]
)

# Nedu, the Visage of Portals
nedu = Visage.objects.get_or_create(
    name="Nedu",
    house=fiends,
    defaults={
        "description": "The angels of the threshold are tall, ethereal figures, their long limbs and lean bodies wreathed in a veil of shifting shadow. Their movements are as fluid as they are soundless, and their feet leave no impression to mark their passing. When they pass into deep shadow, their eyes shine with a cold, blue light."
    },
)[0]
nedu.add_source("Demon: The Fallen", 196)
nedu.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Pass Without Trace", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Senses", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Increased Awareness", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Wings", house=None)[0],
    ]
)
nedu.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Cloak of Shadows", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Improved Initiative", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Dodge", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Casts No Reflection", house=None)[0],
    ]
)

# Shamash, the Visage of Light
shamash = Visage.objects.get_or_create(
    name="Shamash",
    house=fiends,
    defaults={
        "description": "The apocalyptic form of the masters of this lore paints a demon in shifting patterns of shadow and pale, silvery starlight. These hypnotic images draw the eye and beguile the senses, at times hinting at subtle flashes that reflect the demon's inner thoughts. The Shamash are alluring, chimerical, deceptive, terrifying or achingly beautiful, often from moment to moment."
    },
)[0]
shamash.add_source("Demon: The Fallen", 198)
shamash.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Mental Acuity", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Night Sight", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Chimerical Aura", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Unearthly Glamour", house=fiends)[0],
    ]
)
shamash.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Hypnotic Visions", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Dread Mien", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Chimerical Attack", house=fiends)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Casts No Reflection", house=None)[0],
    ]
)

# DEFILER VISAGES
# Ishhara, the Visage of Longing
ishhara = Visage.objects.get_or_create(
    name="Ishhara",
    house=defilers,
    defaults={
        "description": "The angels of inspiration are visions of beauty, compared to whom even the radiant angels of the Namaru pale. Their golden hair and perfectly sculpted features are the romantic ideal spoken of in mortal poetry and prose, and their honeyed voices melt even the hardest hearts."
    },
)[0]
ishhara.add_source("Demon: The Fallen", 199)
ishhara.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(
            name="Enhanced Social Traits", house=devourers
        ),
        ApocalypticFormTrait.objects.get_or_create(name="Lyrical Voice", house=defilers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Senses", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Intuition", house=defilers)[0],
    ]
)
ishhara.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Claws/Teeth", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Venom", house=defilers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Limbs", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Casts No Reflection", house=None)[0],
    ]
)

# Adad, the Visage of Storms
adad = Visage.objects.get_or_create(
    name="Adad",
    house=defilers,
    defaults={
        "description": "The angels of the storm are tall, statuesque figures, their skins glistening like opal and their dark hair tinged with the deep green of the ocean depths. Blue flickers of ball lightning writhe and dance across their bodies, forming an angry nimbus surrounding their head and shoulders when their fury is aroused."
    },
)[0]
adad.add_source("Demon: The Fallen", 201)
adad.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Weather Sense", house=defilers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Immune to Electricity", house=defilers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Improved Initiative", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Shocking Touch", house=defilers)[0],
    ]
)
adad.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Claws/Teeth", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Spines", house=defilers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Shark Hide", house=defilers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Ink Cloud", house=defilers)[0],
    ]
)

# Mammetum, the Visage of Transfiguration
mammetum = Visage.objects.get_or_create(
    name="Mammetum",
    house=defilers,
    defaults={
        "description": "The angels of transfiguration reveal themselves as luminescent figures devoid of identifying feature or expression, haunting in their silence and deliberate grace. Their entire body is a mirror reflecting the moods and thoughts of those around them, shifting like quicksilver amid a riot of conflicting feelings and expressions."
    },
)[0]
mammetum.add_source("Demon: The Fallen", 203)
mammetum.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Empathy", house=defilers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Casts No Reflection", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Pass Without Trace", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Improved Dexterity", house=defilers)[0],
    ]
)
mammetum.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Claws/Teeth", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Improved Initiative", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Venom", house=defilers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Actions", house=None)[0],
    ]
)

# DEVOURER VISAGES
# Zaltu, the Visage of the Beast
zaltu = Visage.objects.get_or_create(
    name="Zaltu",
    house=devourers,
    defaults={
        "description": "The angels of the hunt are fearsome in their strength and majesty, stalking invisibly through the darkness with panther-like strength and supple grace. The physical appearances of these fallen are many and varied, but most are powerfully muscled and covered in a pelt of fur, with large, golden eyes that glow like coals in the moonlight. They speak in a low, liquid rumble, and their howls chill the blood for miles when they hunt."
    },
)[0]
zaltu.add_source("Demon: The Fallen", 205)
zaltu.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Increased Size", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Senses", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Claws/Teeth", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Actions", house=None)[0],
    ]
)
zaltu.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Thick Hide", house=devourers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Gaping Maw", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Limbs", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Chameleon Skin", house=devourers)[0],
    ]
)

# Ninurtu, the Visage of the Wild
ninurtu = Visage.objects.get_or_create(
    name="Ninurtu",
    house=devourers,
    defaults={
        "description": "The angels of the wilderness manifest as an amalgam of the flora they command and the fauna that thrive beneath their aegis. Their skin is commonly covered by a fine pelt similar to a deer's, and they often possess hooves instead of feet. Their bodies are powerfully muscled, and their eyes change colors like the seasons, ranging from pale gray to deep summer green."
    },
)[0]
ninurtu.add_source("Demon: The Fallen", 207)
ninurtu.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Senses", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Chameleon Skin", house=devourers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Pass Without Trace", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Health Levels", house=None)[0],
    ]
)
ninurtu.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Thorns", house=devourers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Increased Size", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Extra Limbs", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Toxins", house=devourers)[0],
    ]
)

# Aruru, the Visage of Flesh
aruru = Visage.objects.get_or_create(
    name="Aruru",
    house=devourers,
    defaults={
        "description": "The angels of the flesh, who can alter their forms more completely than even the Defilers, manifest themselves as idealized versions of their own mortal forms. Their power exalts the mortal shells that they inhabit, removing any blemishes or deformities and refining their original features to perfection. In a way, this makes their appearance just as alien and wondrous as the shimmering apparitions of their Celestial kin."
    },
)[0]
aruru.add_source("Demon: The Fallen", 209)
aruru.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(
            name="Enhanced Social Traits", house=devourers
        ),
        ApocalypticFormTrait.objects.get_or_create(name="Immune to Poisons", house=devourers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Improved Initiative", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Casts No Reflection", house=None)[0],
    ]
)
aruru.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Extra Health Levels", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Armor", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Gaping Maw", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Regeneration", house=None)[0],
    ]
)

# SLAYER VISAGES
# Namtar, the Visage of Death
namtar = Visage.objects.get_or_create(
    name="Namtar",
    house=slayers,
    defaults={
        "description": "These angels manifest as shadowy figures wreathed in tendrils of ghostly mist that shift and writhe from moment to moment, occasionally reflecting the angels' thoughts in strange, symbolic forms. A pall of silence surrounds these figures, and their feet never seem to touch the ground. Their skin is as pale as alabaster, and their faces are constantly hidden in deep shadow."
    },
)[0]
namtar.add_source("Demon: The Fallen", 211)
namtar.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Wings", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Improved Initiative", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Pass Without Trace", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Casts No Reflection", house=None)[0],
    ]
)
namtar.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Cloak of Shadows", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Death-Grip", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Aura of Entropy", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Damage Resistance", house=None)[0],
    ]
)

# Nergal, the Visage of the Spirit
nergal = Visage.objects.get_or_create(
    name="Nergal",
    house=slayers,
    defaults={
        "description": "The angels of the spirit world appear as pale, serene figures reminiscent of the images of human saints, beautiful, silent and remote. Like others of their House, the Nergal move without noise or effort, seeming to glide along the ground as they move. Only their eyes, colored in shifting patterns of gray and black, hint at the bleak world beyond the mortal realm."
    },
)[0]
nergal.add_source("Demon: The Fallen", 213)
nergal.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Ghost Sight", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Social Traits", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Pass Without Trace", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Wings", house=None)[0],
    ]
)
nergal.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Cloak of Shadows", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Howl of the Damned", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Aura of Dread", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Damage Resistance", house=None)[0],
    ]
)

# Ereshkigal, the Visage of the Realms
ereshkigal = Visage.objects.get_or_create(
    name="Ereshkigal",
    house=slayers,
    defaults={
        "description": "Angels of the Second World manifest as shadowy figures whose features are hidden in perpetual darkness. The air itself seems to wrap about them like a robe of night, conjuring the image of the cowled ferryman of human myth. Their hands are white and bony, like a skeleton's, and they move without effort or sound."
    },
)[0]
ereshkigal.add_source("Demon: The Fallen", 215)
ereshkigal.low_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Dead Reckoning", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Pass Without Trace", house=None)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Enhanced Awareness", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Conjure from Nothing", house=slayers)[0],
    ]
)
ereshkigal.high_torment_traits.set(
    [
        ApocalypticFormTrait.objects.get_or_create(name="Cloak of Shadows", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Relentless", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Voice of the Grave", house=slayers)[0],
        ApocalypticFormTrait.objects.get_or_create(name="Dread Gaze", house=slayers)[0],
    ]
)
