"""
Demon item population script for Seattle Test Chronicle.

Creates Relics (enhanced, enchanted, and house-specific items) for the Fallen factions.
"""

from accounts.models import Profile
from game.models import Chronicle
from items.models.demon import Relic


def populate_demon_items():
    """Create all Demon items for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # ENHANCED RELICS - Technology improved beyond normal limits
    # =========================================================================

    # Faustian Corporate Tech
    quantum_phone, created = Relic.objects.get_or_create(
        name="The Broker's Terminal",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A smartphone enhanced beyond mortal technology by Victoria
Chen's Faustian agents. The device can access any networked system, encrypt
communications beyond any human ability to crack, and process information at
speeds that would fry conventional hardware.

The terminal is used by Faustian negotiators to verify claims, research targets,
and maintain secure communications during deals. Its capabilities give the
Faustians a significant advantage in corporate warfare.

The device appears entirely mundane to casual inspection, but those with
supernatural senses recognize the impossible sophistication of its internals.""",
            "relic_type": "enhanced",
            "complexity": 6,
            "lore_used": "Lore of Patterns",
            "power": "Universal network access, unbreakable encryption, accelerated processing",
            "material": "High-grade electronics enhanced with Fallen knowledge",
            "is_permanent": True,
            "difficulty": 6,
            "dice_pool": 4,
        },
    )
    if created:
        print(f"  Created Enhanced Relic: {quantum_phone.name}")

    # Luciferan Weapon Cache
    enhanced_firearms, created = Relic.objects.get_or_create(
        name="Arsenal of the Fallen",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A collection of firearms enhanced by Azazel's Luciferans to
perform beyond their specifications. Each weapon has been modified to fire
with greater accuracy, penetration, and reliability than any factory model.

The weapons are distributed among Luciferan operatives for use against the
enemies of the cause. They appear identical to standard firearms but perform
at a level that would confuse any ballistics expert.

The Armory maintains strict accountability for these weapons, tracking each
one and requiring their return after operations.""",
            "relic_type": "enhanced",
            "complexity": 5,
            "lore_used": "Lore of the Forge",
            "power": "Enhanced accuracy, increased damage, perfect reliability",
            "material": "Modified standard firearms",
            "is_permanent": True,
            "difficulty": 6,
            "dice_pool": 3,
        },
    )
    if created:
        print(f"  Created Enhanced Relic: {enhanced_firearms.name}")

    # Cryptic Surveillance Equipment
    truth_seeker, created = Relic.objects.get_or_create(
        name="The Truth Seeker",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A set of surveillance equipment enhanced by Cryptic Fallen
to perceive beyond normal limitations. The cameras see in spectrums invisible
to humans, the microphones pick up whispered conversations from impossible
distances, and the analysis software recognizes patterns no algorithm should
detect.

Sarah Blackwood uses this equipment in her investigations, uncovering truths
that would remain hidden from conventional methods. The Cryptics guard their
surveillance advantage jealously.

The equipment requires regular maintenance from someone who understands its
enhanced nature - mundane technicians find its behavior unpredictable.""",
            "relic_type": "enhanced",
            "complexity": 5,
            "lore_used": "Lore of Light",
            "power": "Enhanced perception across multiple spectrums, pattern recognition",
            "material": "Modified surveillance equipment",
            "is_permanent": True,
            "difficulty": 6,
            "dice_pool": 4,
        },
    )
    if created:
        print(f"  Created Enhanced Relic: {truth_seeker.name}")

    # Reconciler Medical Equipment
    healing_kit, created = Relic.objects.get_or_create(
        name="Mercy's Touch",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Medical equipment enhanced by Nazriel's Reconcilers to heal
injuries that should be beyond saving. The kit includes surgical tools that
cut with impossible precision and medications that work faster and better
than their labels suggest.

Stern Memorial Hospice uses this equipment for cases where conventional
medicine has failed. The Reconcilers view healing as a form of redemption,
proving that their powers can create rather than destroy.

The equipment leaves no evidence of supernatural enhancement - healed patients
simply seem to have been fortunate in their treatment.""",
            "relic_type": "enhanced",
            "complexity": 6,
            "lore_used": "Lore of Flesh",
            "power": "Enhanced healing, precise surgery, accelerated recovery",
            "material": "Modified medical equipment",
            "is_permanent": True,
            "difficulty": 5,
            "dice_pool": 5,
        },
    )
    if created:
        print(f"  Created Enhanced Relic: {healing_kit.name}")

    # =========================================================================
    # ENCHANTED RELICS - Objects imbued with supernatural power
    # =========================================================================

    # Binding Ring
    binding_ring, created = Relic.objects.get_or_create(
        name="Ring of Solomon's Legacy",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A gold ring inscribed with angelic script, one of several
created during the height of Solomon's power. The ring allows its wearer to
bind agreements with supernatural force - oaths sworn on the ring carry
weight that transcends mortal law.

The ring passed through many hands before reaching Seattle, where it serves
as a neutral guarantee for agreements between factions. Pacts sealed with
the ring are enforced by the power woven into its creation.

Breaking an oath sworn on the ring carries severe consequences. The ring
remembers every promise made upon it and enforces them without mercy.""",
            "relic_type": "enchanted",
            "complexity": 0,
            "lore_used": "Lore of Celestials",
            "power": "Bind supernatural oaths, enforce agreements, detect oath-breaking",
            "material": "Gold ring with angelic inscription",
            "is_permanent": True,
            "difficulty": 7,
            "dice_pool": 6,
        },
    )
    if created:
        print(f"  Created Enchanted Relic: {binding_ring.name}")

    # Shadow Key
    shadow_key, created = Relic.objects.get_or_create(
        name="The Shadow Key",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A key forged from shadows made solid, allowing its bearer
to open passages between places where shadows connect. Doors locked by
mundane means yield to this key, and even some supernatural barriers can
be bypassed.

The Cryptics acquired this key from a dying demon who created it centuries
ago. Its origins in the darkness between worlds make it particularly useful
for espionage and escape.

The key has limitations - it cannot open passages warded specifically against
demonic intrusion, and using it leaves traces that can be detected by those
who know what to look for.""",
            "relic_type": "enchanted",
            "complexity": 0,
            "lore_used": "Lore of Paths",
            "power": "Open mundane locks, create shadow passages, bypass basic wards",
            "material": "Solidified shadow",
            "is_permanent": True,
            "difficulty": 7,
            "dice_pool": 5,
        },
    )
    if created:
        print(f"  Created Enchanted Relic: {shadow_key.name}")

    # Truth Mirror
    truth_mirror, created = Relic.objects.get_or_create(
        name="Mirror of Reflected Truth",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A hand mirror that shows the true nature of whatever is
reflected within it. Illusions dissolve, disguises reveal themselves, and
the hidden aspects of a person's nature become visible to the one holding
the mirror.

The mirror was created by an Elohim who sought to understand humanity's
capacity for self-deception. Its truth-revealing nature makes it valuable
for negotiations and interrogations.

Looking into the mirror is disturbing for most viewers, as it shows not
just physical truth but spiritual nature as well. Few enjoy seeing their
true reflection.""",
            "relic_type": "enchanted",
            "complexity": 0,
            "lore_used": "Lore of Light",
            "power": "Reveal true nature, pierce illusions, detect deception",
            "material": "Silver-backed glass with celestial inscriptions",
            "is_permanent": True,
            "difficulty": 6,
            "dice_pool": 5,
        },
    )
    if created:
        print(f"  Created Enchanted Relic: {truth_mirror.name}")

    # Demon's Compass
    demon_compass, created = Relic.objects.get_or_create(
        name="Compass of Lost Souls",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A brass compass that points toward whatever its bearer
seeks, whether a physical location, a person, or an abstract concept. The
compass was created by a Fallen Neberu who specialized in finding things
that wished to remain hidden.

The needle responds to the bearer's desire, spinning until it settles on
the direction of the sought target. The strength of the pull indicates
proximity - a strong pull means the target is near.

The compass cannot distinguish between multiple targets of the same type,
and it provides direction rather than safe paths. Users must navigate
obstacles on their own.""",
            "relic_type": "enchanted",
            "complexity": 0,
            "lore_used": "Lore of Paths",
            "power": "Point toward sought targets, indicate proximity",
            "material": "Brass compass with celestial mechanisms",
            "is_permanent": True,
            "difficulty": 6,
            "dice_pool": 4,
        },
    )
    if created:
        print(f"  Created Enchanted Relic: {demon_compass.name}")

    # =========================================================================
    # HOUSE-SPECIFIC RELICS
    # =========================================================================

    # Devourer Relic
    berserker_torc, created = Relic.objects.get_or_create(
        name="Torc of the Raging Storm",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A bronze torc created by a Devourer for use in battle. When
activated, the torc channels the fury of nature's most destructive forces
through its wearer, granting them terrible strength and resilience at the
cost of reason.

The torc was created during the war in Heaven and has seen countless battles
since. Its power is undeniable, but the fury it invokes is difficult to control
- wearers risk losing themselves to destruction.

The Luciferans keep this relic in reserve for their most desperate conflicts,
knowing its power comes with a price.""",
            "relic_type": "house_specific",
            "complexity": 0,
            "lore_used": "Lore of the Wild",
            "power": "Enhance physical capabilities, invoke battle fury, resist damage",
            "material": "Bronze torc with storm-spirit binding",
            "house": None,  # Would link to Devourers house
            "is_permanent": True,
            "difficulty": 7,
            "dice_pool": 6,
        },
    )
    if created:
        print(f"  Created House Relic: {berserker_torc.name}")

    # Malefactor Relic
    crafters_hammer, created = Relic.objects.get_or_create(
        name="Hammer of First Making",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A hammer used by a Malefactor since before the Fall, when
the Annunaki shaped the physical world according to divine design. The
hammer can reshape matter as if it were clay, allowing its user to craft
or repair almost anything.

The hammer was one of the tools used to build the first cities, and it
retains that creative power. In the hands of a skilled Malefactor, it can
create objects of remarkable quality or repair damage that should be
permanent.

The hammer responds best to creative intent - using it for destruction
rather than creation produces inferior results.""",
            "relic_type": "house_specific",
            "complexity": 0,
            "lore_used": "Lore of the Forge",
            "power": "Shape matter, enhance crafting, repair damage",
            "material": "Primordial metal bound with creative essence",
            "house": None,  # Would link to Malefactors house
            "is_permanent": True,
            "difficulty": 6,
            "dice_pool": 5,
        },
    )
    if created:
        print(f"  Created House Relic: {crafters_hammer.name}")

    # Scourge Relic
    wind_cloak, created = Relic.objects.get_or_create(
        name="Cloak of Hurricane Wings",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A cloak that seems to be woven from wind itself, constantly
rippling even in still air. The cloak was created by an Asharu who specialized
in the wild aspects of their House's powers, binding the essence of storms
into wearable form.

The cloak allows its wearer to ride the winds, moving with supernatural speed
and grace. In combat, the wearer can call upon hurricane forces to batter
enemies or deflect attacks.

The cloak responds to the wearer's emotional state - strong emotions cause
stronger winds, while calm produces gentle breezes.""",
            "relic_type": "house_specific",
            "complexity": 0,
            "lore_used": "Lore of the Winds",
            "power": "Flight, enhanced speed, wind manipulation, deflection",
            "material": "Woven wind essence bound to fabric",
            "house": None,  # Would link to Scourges house
            "is_permanent": True,
            "difficulty": 6,
            "dice_pool": 5,
        },
    )
    if created:
        print(f"  Created House Relic: {wind_cloak.name}")

    # Fiend Relic
    memory_stone, created = Relic.objects.get_or_create(
        name="Stone of Forgotten Futures",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A smooth black stone that shows glimpses of possible futures
to those who gaze into its depths. The stone was created by a Neberu prophet
who sought to preserve their ability to perceive fate across their many
incarnations.

The visions provided by the stone are symbolic rather than literal, requiring
interpretation. Skilled users can gain valuable insights, while the careless
may be led astray by misunderstood prophecies.

The stone has been in the possession of various Fallen seers over the
millennia. Its current location in Seattle makes it available to those
who need guidance.""",
            "relic_type": "house_specific",
            "complexity": 0,
            "lore_used": "Lore of Patterns",
            "power": "See possible futures, perceive fate patterns, prophetic visions",
            "material": "Obsidian imbued with temporal essence",
            "house": None,  # Would link to Fiends house
            "is_permanent": True,
            "difficulty": 7,
            "dice_pool": 6,
        },
    )
    if created:
        print(f"  Created House Relic: {memory_stone.name}")

    # Defiler Relic
    desire_chalice, created = Relic.objects.get_or_create(
        name="Chalice of Heart's Desire",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A silver chalice that, when filled with wine and shared,
allows its user to perceive the deepest desires of those who drink. The
chalice was created by a Lammasu who sought to understand humanity's
emotional nature.

The chalice reveals desires that even the person themselves may not
consciously recognize. This knowledge can be used for manipulation or
for genuine understanding - the chalice judges neither.

The Faustians frequently use this relic during negotiations, learning
what their counterparts truly want beneath their stated demands.""",
            "relic_type": "house_specific",
            "complexity": 0,
            "lore_used": "Lore of Longing",
            "power": "Perceive desires, enhance empathy, emotional insight",
            "material": "Silver chalice with Lammasu inscriptions",
            "house": None,  # Would link to Defilers house
            "is_permanent": True,
            "difficulty": 6,
            "dice_pool": 5,
        },
    )
    if created:
        print(f"  Created House Relic: {desire_chalice.name}")

    # Slayer Relic
    death_blade, created = Relic.objects.get_or_create(
        name="Blade of Final Mercy",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A black-bladed knife created by a Halaku to end suffering
without causing unnecessary pain. The blade's touch brings death cleanly,
without the trauma of normal violence.

The Blade of Final Mercy was intended for compassionate use - ending the
suffering of those beyond help. It has since been used for less merciful
purposes, though it retains its nature of clean, quick death.

The Reconcilers keep this blade secure, using it only when no other option
exists. Its power over death makes it dangerous in the wrong hands.""",
            "relic_type": "house_specific",
            "complexity": 0,
            "lore_used": "Lore of Death",
            "power": "Painless death, sever soul cleanly, resist corruption",
            "material": "Black metal bound with death essence",
            "house": None,  # Would link to Slayers house
            "is_permanent": True,
            "difficulty": 7,
            "dice_pool": 6,
        },
    )
    if created:
        print(f"  Created House Relic: {death_blade.name}")

    # =========================================================================
    # EARTHBOUND ARTIFACTS (Dangerous/Restricted)
    # =========================================================================

    # Earthbound Focus
    earthbound_shard, created = Relic.objects.get_or_create(
        name="Shard of the Foundation",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A fragment of the altar that serves as The Foundation's
binding. The shard was broken off during a conflict and now exists separately
from its source, retaining a connection to the Earthbound demon.

The shard allows communication with The Foundation and can be used to detect
its influence or interference. More dangerously, it can channel a portion of
the Earthbound's power - though such channeling attracts the demon's attention.

The Fallen keep this shard secured and warded, using it only when necessary
to understand or counter The Foundation's activities.""",
            "relic_type": "enchanted",
            "complexity": 0,
            "lore_used": "Lore of the Earth",
            "power": "Communicate with Earthbound, detect influence, limited power channel",
            "material": "Stone fragment from Earthbound altar",
            "is_permanent": True,
            "difficulty": 8,
            "dice_pool": 7,
        },
    )
    if created:
        print(f"  Created Earthbound Relic: {earthbound_shard.name}")

    print("Demon items populated successfully.")

    return {
        "enhanced": [quantum_phone, enhanced_firearms, truth_seeker, healing_kit],
        "enchanted": [binding_ring, shadow_key, truth_mirror, demon_compass],
        "house_specific": [
            berserker_torc,
            crafters_hammer,
            wind_cloak,
            memory_stone,
            desire_chalice,
            death_blade,
        ],
        "earthbound": [earthbound_shard],
    }


if __name__ == "__main__":
    populate_demon_items()
