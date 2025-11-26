"""
Changeling item population script for Seattle Test Chronicle.

Creates Treasures (magical items) and Dross (glamour currency) for the Emerald Court.
"""

from accounts.models import Profile
from game.models import Chronicle
from items.models.changeling import Dross, Treasure


def populate_changeling_items():
    """Create all Changeling items for the test chronicle."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # =========================================================================
    # TREASURES - DUCAL REGALIA
    # =========================================================================

    # Crown of the Pacific
    ducal_crown, created = Treasure.objects.get_or_create(
        name="Crown of the Pacific Duke",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """The ceremonial crown of Seattle's Fae nobility, worn by
Duke Sebastian Ashford and his predecessors since the Duchy's founding. The
crown appears as an elegant circlet of silver and emerald to mortal eyes, but
Kithain see a magnificent diadem of living seaweed and precious stones gathered
from the depths of Puget Sound.

The Crown grants its wearer authority over the Duchy's Glamour resources and
allows communication with any Kithain holding fealty. More importantly, it
establishes the Duke as the lawful ruler in the eyes of both Seelie and
Unseelie courts.

The Crown has never been stolen or lost - attempts to take it by force have
met with spectacular failure, as the Crown itself seems to resist illegitimate
claimants.""",
            "rating": 5,
            "treasure_type": "talisman",
            "creator": "Unknown - predates current Duchy",
            "creation_method": "Ancient Glamour-forging during the Dreaming's peak",
            "permanence": True,
            "effects": [
                "Command: Authority over sworn vassals",
                "Perception: Sense disturbances in Duchy holdings",
                "Communication: Mental contact with oath-bound Kithain",
                "Legitimacy: Recognized by all Fae courts",
            ],
            "special_abilities": "The Crown cannot be worn by one who has broken faith with the Dreaming",
            "glamour_storage": 15,
            "glamour_affinity": "Sovereignty",
        },
    )
    if created:
        print(f"  Created Treasure: {ducal_crown.name}")

    # Scepter of Tides
    ducal_scepter, created = Treasure.objects.get_or_create(
        name="Scepter of the Tides",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A companion piece to the Crown, this scepter represents
the Duke's power over the natural forces of the Pacific Northwest. It appears
as a narwhal horn wrapped in silver filigree, but its true form is a spiraling
wave frozen at the moment of breaking.

The Scepter allows its wielder to influence weather and water within the
Duchy's boundaries. Storms can be called or calmed, tides manipulated, and
the creatures of the sea commanded. These powers must be used wisely - the
Dreaming notices excessive interference.

Duke Ashford uses the Scepter sparingly, preferring subtle adjustments to
dramatic displays. He once calmed a storm that would have devastated Seattle's
waterfront, an act remembered gratefully by those who witnessed it.""",
            "rating": 4,
            "treasure_type": "talisman",
            "creator": "A Selkie artificer in service to the first Duke",
            "creation_method": "Bound essence of a sea-spirit during a eclipse",
            "permanence": True,
            "effects": [
                "Weather Control: Influence storms and precipitation",
                "Water Manipulation: Command water in all forms",
                "Sea Creature Affinity: Communication with marine life",
            ],
            "special_abilities": "Enhanced power during full moons and high tides",
            "glamour_storage": 10,
            "glamour_affinity": "Nature",
        },
    )
    if created:
        print(f"  Created Treasure: {ducal_scepter.name}")

    # =========================================================================
    # TREASURES - COURT ITEMS
    # =========================================================================

    # Baron's Blade
    barons_blade, created = Treasure.objects.get_or_create(
        name="Thornguard",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Baron Marcus Stone's personal weapon, a sword that appears
as a polished rapier to mortal eyes but reveals itself as a blade of living
thorns and cold iron to the Kithain. The weapon was forged as a gift from
the Duke upon Marcus's elevation to Baron.

Thornguard is particularly effective against those who break oaths or violate
hospitality. The blade seems to know the intentions of those it faces, burning
with green fire when pointed at traitors or oathbreakers.

The sword carries a mild curse - its wielder becomes increasingly protective
of their charges, sometimes to the point of paranoia. Marcus has learned to
channel this impulse productively.""",
            "rating": 4,
            "treasure_type": "weapon",
            "creator": "Court artificers under Duke Ashford's direction",
            "creation_method": "Glamour-forged from a hawthorn struck by lightning",
            "permanence": True,
            "effects": [
                "Enhanced damage against oathbreakers",
                "Detect treachery when drawn",
                "Create thorny barriers with Glamour expenditure",
            ],
            "special_abilities": "Burns with green fire in presence of betrayal",
            "glamour_storage": 5,
            "glamour_affinity": "Protection",
        },
    )
    if created:
        print(f"  Created Treasure: {barons_blade.name}")

    # Seer's Glass
    seers_glass, created = Treasure.objects.get_or_create(
        name="The Oracle's Lens",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A monocle of crystallized dream-stuff used by the court's
seers to perceive possible futures and hidden truths. The lens shows the
world as it truly is - stripping away Mists, illusions, and deceptions.

Those who look through the Oracle's Lens too often begin to see possibilities
everywhere, their minds fragmenting across potential futures. The court limits
its use to matters of genuine importance.

The lens was discovered in the Far Dreaming by an expedition that lost half
its members to bring it back. The survivors never spoke of what they saw.""",
            "rating": 4,
            "treasure_type": "wonder",
            "creator": "Unknown - found in the Far Dreaming",
            "creation_method": "Unknown - possibly spontaneous dream creation",
            "permanence": True,
            "effects": [
                "Pierce illusions and concealment",
                "Glimpse possible futures",
                "Perceive Chimera invisible to others",
            ],
            "special_abilities": "Extended use risks madness",
            "glamour_storage": 8,
            "glamour_affinity": "Prophecy",
        },
    )
    if created:
        print(f"  Created Treasure: {seers_glass.name}")

    # Herald's Horn
    heralds_horn, created = Treasure.objects.get_or_create(
        name="Voice of the Court",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A silver horn used to make formal proclamations and summon
the Duchy's nobles to court. When blown, the horn's call can be heard by any
Kithain in the Pacific Northwest who owes fealty to the Duke.

The horn can also be used to announce formal challenges, declarations of war,
or calls for sanctuary. Its sound carries legal weight - proclamations made
through the horn are binding under Fae law.

Court heralds have carried variations of this horn for centuries. The current
version incorporates elements of the original and has been enchanted to work
across greater distances.""",
            "rating": 3,
            "treasure_type": "wonder",
            "creator": "Court artificers across generations",
            "creation_method": "Accumulated enchantments over centuries",
            "permanence": True,
            "effects": [
                "Broadcast messages to sworn vassals",
                "Formalize declarations under Fae law",
                "Summon nobles to court within one week",
            ],
            "special_abilities": "Sound carries across the Mists",
            "glamour_storage": 5,
            "glamour_affinity": "Communication",
        },
    )
    if created:
        print(f"  Created Treasure: {heralds_horn.name}")

    # =========================================================================
    # TREASURES - PERSONAL ITEMS
    # =========================================================================

    # Esmeralda's Mask
    esmeraldas_mask, created = Treasure.objects.get_or_create(
        name="Mask of Many Faces",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A theatrical mask crafted by Esmeralda Bright for her own
use. The mask can assume any face the wearer imagines, providing a perfect
disguise that fools both mortal senses and supernatural perception.

Esmeralda created the mask during her career as an actress, using it to play
roles that would otherwise be impossible. The mask has since served for less
innocent purposes, though Esmeralda maintains it has never been used for true
evil.

The mask responds to the wearer's emotions, sometimes shifting to reflect
their true feelings regardless of what face they've chosen. Skilled users
learn to control these tells.""",
            "rating": 3,
            "treasure_type": "talisman",
            "creator": "Esmeralda Bright",
            "creation_method": "Years of theatrical Glamour infusion",
            "permanence": True,
            "effects": [
                "Perfect physical disguise",
                "Voice alteration",
                "Mild empathic projection of chosen persona",
            ],
            "special_abilities": "May reveal true emotions at inopportune moments",
            "glamour_storage": 4,
            "glamour_affinity": "Illusion",
        },
    )
    if created:
        print(f"  Created Treasure: {esmeraldas_mask.name}")

    # Rowan's Pocket Watch
    rowans_watch, created = Treasure.objects.get_or_create(
        name="The Moment Between",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A pocket watch that Rowan Blackwood found in an antique
shop, only to discover it was far more than it appeared. The watch doesn't
keep normal time - instead, it measures moments of significance, chiming when
important events are about to occur.

The watch also allows its bearer to stretch a single moment, creating a brief
pocket of frozen time where they can act while others remain still. This
power is exhausting and can only be used sparingly.

Rowan believes the watch chose her, appearing in her path at a moment when
she desperately needed its guidance. She guards it carefully, knowing such
treasures attract dangerous attention.""",
            "rating": 4,
            "treasure_type": "wonder",
            "creator": "Unknown Nocker artificer",
            "creation_method": "Captured essence of a significant moment",
            "permanence": True,
            "effects": [
                "Sense approaching significant events",
                "Brief time dilation (seconds stretched to moments)",
                "Perfect recall of witnessed events",
            ],
            "special_abilities": "Cannot be lost - always returns to its bearer",
            "glamour_storage": 6,
            "glamour_affinity": "Time",
        },
    )
    if created:
        print(f"  Created Treasure: {rowans_watch.name}")

    # Thorn's Compass
    thorns_compass, created = Treasure.objects.get_or_create(
        name="Compass of Lost Things",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A compass that points not to magnetic north but to whatever
its bearer seeks. Thorn acquired this treasure during his wandering years
and has used it to find lost children, hidden enemies, and secret paths
through the Dreaming.

The compass can only find things that are genuinely lost - items being
deliberately hidden register as static or confusion. This limitation makes
it most useful for rescue missions and exploration rather than espionage.

Thorn keeps the compass on a chain around his neck, consulting it when his
other senses fail him.""",
            "rating": 3,
            "treasure_type": "wonder",
            "creator": "A Sluagh wayfinder",
            "creation_method": "Bound with the longing of separated lovers",
            "permanence": True,
            "effects": [
                "Point toward lost objects or people",
                "Sense proximity to sought target",
                "Navigate unfamiliar terrain",
            ],
            "special_abilities": "Cannot find things deliberately hidden",
            "glamour_storage": 3,
            "glamour_affinity": "Seeking",
        },
    )
    if created:
        print(f"  Created Treasure: {thorns_compass.name}")

    # =========================================================================
    # TREASURES - MINOR ITEMS
    # =========================================================================

    # Dreaming Tea Set
    dream_tea, created = Treasure.objects.get_or_create(
        name="The Dreamer's Tea Service",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """An elegant tea set that brews tea with remarkable properties.
Each cup provides a different effect based on the brew: clarity of thought,
restful sleep, honest conversation, or vivid dreaming.

The set is maintained at the Freehold for communal use. Tea ceremonies using
this service are traditional for important negotiations, as the tea encourages
honesty and discourages hostility.

The set was a gift from a Chinese Hsien who visited Seattle decades ago,
establishing lasting goodwill between the communities.""",
            "rating": 2,
            "treasure_type": "wonder",
            "creator": "Hsien tea master",
            "creation_method": "Traditional dream-weaving techniques",
            "permanence": True,
            "effects": [
                "Various effects based on tea blend",
                "Encourages honest conversation",
                "Mild calming influence",
            ],
            "special_abilities": "Effects vary by preparation",
            "glamour_storage": 3,
            "glamour_affinity": "Hospitality",
        },
    )
    if created:
        print(f"  Created Treasure: {dream_tea.name}")

    # Storyteller's Quill
    storyteller_quill, created = Treasure.objects.get_or_create(
        name="Quill of Living Words",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """A feather quill that writes stories that come alive as
they're read. The words shimmer and shift, occasionally illustrating themselves
with moving images that act out the narrative.

The quill is used by court recorders to document important events and by
entertainers to create enchanting stories. Works written with this quill
are highly valued as gifts.

Extensive use of the quill can cause writer's cramp that lasts for days, as
the stories demand energy from their creator.""",
            "rating": 2,
            "treasure_type": "wonder",
            "creator": "Eshu storyteller collective",
            "creation_method": "Infused with countless spoken tales",
            "permanence": True,
            "effects": [
                "Words animate when read",
                "Stories are more engaging",
                "Written works resist degradation",
            ],
            "special_abilities": "May cause fatigue with extended use",
            "glamour_storage": 2,
            "glamour_affinity": "Stories",
        },
    )
    if created:
        print(f"  Created Treasure: {storyteller_quill.name}")

    # =========================================================================
    # DROSS - GLAMOUR CURRENCY
    # =========================================================================

    # Freehold Dross Supply
    freehold_dross, created = Dross.objects.get_or_create(
        name="Emerald Court Balefire Harvest",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Dross harvested from the Emerald Court's balefire over time.
The dross appears as small emerald crystals that pulse with inner light, each
containing a portion of the dreams that sustain the Freehold.

This supply is maintained for court operations, distributed to nobles for
their duties, and used to reward loyal service. The Duke personally oversees
its allocation during court sessions.

The quality is consistently high, reflecting the strong balefire and active
dreaming community of Seattle.""",
            "quality": "fine",
            "glamour_value": 6,
            "physical_form": "crystal",
            "color": "Emerald green with golden flecks",
            "source": "balefire",
            "is_stable": True,
            "decay_rate": "None - stable balefire dross",
            "resonance": "Sovereignty, community, dreams of the city",
            "special_effects": "Slightly enhances noble Arts",
            "restricted_to": "Court members in good standing",
            "is_consumable": True,
            "recharge_method": "Cannot be recharged - consumed on use",
            "container_description": "Velvet-lined wooden box with ducal seal",
            "estimated_value": "High - official court currency",
        },
    )
    if created:
        print(f"  Created Dross: {freehold_dross.name}")

    # Dream Harvest Dross
    dream_dross, created = Dross.objects.get_or_create(
        name="Seattle Skyline Dreams",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Dross harvested from the dreams of Seattle residents,
particularly the vivid dreams inspired by the city's coffee culture and
creative industries. This dross carries the flavor of ambition and creativity.

The dross takes the form of misty droplets that shimmer with images of the
Seattle skyline. Each drop contains a fragment of someone's dream of success,
artistic inspiration, or innovative breakthrough.

This type of dross is common in Seattle, reflecting the city's dreaming
population. It's suitable for general use but excels at fueling creative
endeavors.""",
            "quality": "common",
            "glamour_value": 3,
            "physical_form": "liquid",
            "color": "Silvery-gray with occasional color bursts",
            "source": "dream",
            "is_stable": True,
            "decay_rate": "Slowly fades if not used within a month",
            "resonance": "Creativity, ambition, coffee-fueled determination",
            "special_effects": "Enhances artistic and creative Arts",
            "restricted_to": "None",
            "is_consumable": True,
            "recharge_method": "Cannot be recharged - consumed on use",
            "container_description": "Small glass vials",
            "estimated_value": "Moderate - common but useful",
        },
    )
    if created:
        print(f"  Created Dross: {dream_dross.name}")

    # Art-Infused Dross
    art_dross, created = Dross.objects.get_or_create(
        name="First Friday Essence",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Dross gathered from Seattle's First Thursday art walks,
when galleries open their doors and creativity flows freely through the
streets. This dross is particularly potent, infused with the energy of
artistic revelation and appreciation.

The dross manifests as paint-like swirls of color that never quite dry,
shifting through the spectrum based on nearby emotions. Each batch reflects
the specific exhibitions that generated it.

Court Eshu maintain regular harvesting schedules during art events, ensuring
a steady supply of this valuable resource.""",
            "quality": "exquisite",
            "glamour_value": 7,
            "physical_form": "liquid",
            "color": "Constantly shifting spectrum",
            "source": "art",
            "is_stable": True,
            "decay_rate": "Stable indefinitely if properly stored",
            "resonance": "Artistic passion, creative revelation, beauty",
            "special_effects": "Significantly enhances Chicanery and artistic endeavors",
            "restricted_to": "None - but expensive",
            "is_consumable": True,
            "recharge_method": "Cannot be recharged - consumed on use",
            "container_description": "Sealed crystal containers",
            "estimated_value": "High - prized by artists",
        },
    )
    if created:
        print(f"  Created Dross: {art_dross.name}")

    # Natural Dross
    natural_dross, created = Dross.objects.get_or_create(
        name="Olympic Rainforest Essence",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Dross gathered from the ancient rainforests of the Olympic
Peninsula, where nature dreams its own dreams of growth, decay, and renewal.
This dross carries the weight of centuries in every drop.

The dross appears as dewdrops that glow with soft green light, occasionally
containing tiny images of ferns, moss, or ancient trees. The scent is of
deep forest and rich earth.

Gathering this dross requires expeditions into the deep forest, where mundane
hazards and supernatural guardians both pose challenges.""",
            "quality": "fine",
            "glamour_value": 5,
            "physical_form": "liquid",
            "color": "Deep forest green",
            "source": "natural",
            "is_stable": True,
            "decay_rate": "Fades if removed from natural settings too long",
            "resonance": "Growth, nature, ancient patience",
            "special_effects": "Enhances Primal Arts and healing",
            "restricted_to": "None",
            "is_consumable": True,
            "recharge_method": "Cannot be recharged - consumed on use",
            "container_description": "Leaf-wrapped bundles",
            "estimated_value": "Moderate-high - requires expedition to gather",
        },
    )
    if created:
        print(f"  Created Dross: {natural_dross.name}")

    # Festival Dross
    festival_dross, created = Dross.objects.get_or_create(
        name="Bumbershoot Revelry",
        chronicle=chronicle,
        defaults={
            "owner": st_user,
            "description": """Dross gathered during Seattle's annual Bumbershoot festival,
when music, art, and celebration fill the city with creative energy. This
dross is wild and potent, but can be unpredictable.

The dross manifests as tiny fireworks that never quite go out, crackling with
contained energy and flashing with colors. The dross occasionally produces
phantom sounds of music and laughter.

This dross is gathered in large quantities during the festival and stored
for year-round use. Its festive nature makes it popular for celebrations.""",
            "quality": "fine",
            "glamour_value": 5,
            "physical_form": "other",
            "color": "Multicolored sparkles",
            "source": "refined",
            "is_stable": False,
            "decay_rate": "Slowly loses potency over months",
            "resonance": "Joy, music, celebration, community",
            "special_effects": "Enhances performance Arts, may cause unexpected effects",
            "restricted_to": "None",
            "is_consumable": True,
            "recharge_method": "Cannot be recharged - consumed on use",
            "container_description": "Sealed festival containers",
            "estimated_value": "Moderate - seasonal availability",
        },
    )
    if created:
        print(f"  Created Dross: {festival_dross.name}")

    print("Changeling items populated successfully.")

    return {
        "regalia": [ducal_crown, ducal_scepter],
        "court_treasures": [barons_blade, seers_glass, heralds_horn],
        "personal_treasures": [esmeraldas_mask, rowans_watch, thorns_compass],
        "minor_treasures": [dream_tea, storyteller_quill],
        "dross": [freehold_dross, dream_dross, art_dross, natural_dross, festival_dross],
    }


if __name__ == "__main__":
    populate_changeling_items()
