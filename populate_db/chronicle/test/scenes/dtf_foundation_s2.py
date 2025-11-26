"""
The Foundation Cracks - Scene 2: The Gathering

The Fallen assemble allies from across Seattle's supernatural community.

Characters: Zephyrus, Marcus Wells
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of The Foundation Cracks."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        zephyrus = CharacterModel.objects.get(name="Zephyrus")
    except CharacterModel.DoesNotExist:
        zephyrus = None

    try:
        marcus = CharacterModel.objects.get(name="Marcus Wells")
    except CharacterModel.DoesNotExist:
        marcus = None

    scene, created = Scene.objects.get_or_create(
        name="The Gathering",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 4, 21),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Gathering")
        return scene

    print("  Created Scene: The Gathering")

    if zephyrus:
        scene.add_character(zephyrus)
    if marcus:
        scene.add_character(marcus)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""A neutral location - the Space Needle's observation deck, closed
for "private event." In truth, a gathering of monsters.

Vampires from the Camarilla and Anarchs. Mages from two different
Traditions. A werewolf pack representative, deeply uncomfortable
but present. Two hunters who've been convinced this threat is real.
And the Fallen - Zephyrus, Marcus, and three others who answered the call.

The Earthbound's pulses have grown stronger. Half of Seattle's population
is sleeping poorly, plagued by nightmares that feel too real. Emergency
rooms report a 300% increase in panic attacks.

Time is running out."""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus stands at the center of the gathering, his presence
both demonic and strangely reassuring*

"Thank you all for coming. I know trust is... complicated, given
our natures. But what's awakening beneath us doesn't care about
our feuds."

*He projects an image - his best visualization of the Earthbound*

/roll 6 6
(Charisma + Leadership - addressing the council)

"This is an Earthbound. A demon that never fell into the Abyss.
It's been sleeping under Seattle for five thousand years. Now it's
waking up, and it's HUNGRY."

*He meets each set of eyes in turn*

"Within 24 hours, it will manifest physically. When it does, it will
begin feeding on the population's fear. Thousands will die. Maybe
more."

*He pauses*

"We can stop it. But only together.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The reactions are mixed.

The vampire representative - a Ventrue elder named Katherine - speaks
first: "Assuming we believe you, demon, what exactly do you propose?
We're hardly equipped to fight something older than civilization."

The werewolf - a scarred Garou called Breaks-the-Chain - growls:
"We fought Wyrm-things before. This smells different. Worse."

The mage, a Hermetic named Dr. Ashworth, frowns: "The resonance
patterns are consistent with a major spirit awakening. If the Fallen
are correct about its nature..."

The hunter, a grizzled man named Collins, just loads his shotgun.
"Tell me where to shoot.""""
        )

    if marcus:
        scene.add_post(
            character=marcus,
            display="Marcus Wells",
            message="""*Marcus steps forward with tactical information*

"We've traced the Earthbound's resting place. It's beneath the old
Seattle Underground - the buried city from the 1889 fire. It anchored
itself to the mass death trauma of that disaster."

*He spreads a map*

/roll 5 6
(Intelligence + Investigation - presenting the plan)

"The entity can't move yet. It's tied to its anchor point. That's
our advantage - we bring the fight to it, before it can break free."

*He indicates several points on the map*

"Three entry points to the Underground. If we hit all three
simultaneously, we can trap it, weaken it with combined assault,
and either bind it or destroy it."

*He looks at the assembled supernaturals*

"I won't lie. Some of us are going to die. But if we don't do this,
EVERYONE dies.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The room digests this information.

Katherine speaks again: "The Camarilla will commit three Kindred.
Our existence depends on stable mortals - this threatens that."

Breaks-the-Chain: "My pack will take one entry point. Wyrm or not,
corruption must be fought."

Dr. Ashworth: "The Traditions can provide ritual support. Binding
magics to contain the entity if direct combat fails."

Collins, the hunter: "Just point me at the bastard."

The alliance is fragile, born of desperation rather than trust. But
it's an alliance nonetheless.

Another pulse radiates from below. Stronger. Hungrier.

The Earthbound is dreaming of its first meal in five millennia."""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus feels the pulse and steadies himself*

"We move at midnight. That gives us twelve hours to prepare."

*He addresses each faction*

/roll 5 7
(Manipulation + Leadership - coordinating factions)

"Vampires - you take the Pioneer Square entrance. Your speed and
resilience will be crucial. Werewolves - the waterfront tunnel. If
anything tries to escape, you're our containment. Mages - establish
your ritual circle topside. We'll need you to seal breaches in
reality when we engage."

*He looks at Collins and the other hunters*

"Hunters - you're with me and Marcus. We'll take the main shaft.
We know how demons think. We know their weaknesses."

*He takes a breath*

"This ends tonight. One way or another."

[Scene End - Alliance formed, assault planned]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
