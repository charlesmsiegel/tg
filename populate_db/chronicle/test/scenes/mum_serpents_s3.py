"""
Serpents in the City - Scene 3: The Rescue

The mummies raid the cult's hideout to rescue the captive vessel.

Characters: Amenhotep IV, Dr. Constance Grey
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of Serpents in the City."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        amenhotep = CharacterModel.objects.get(name="Amenhotep IV")
    except CharacterModel.DoesNotExist:
        amenhotep = None

    try:
        constance = CharacterModel.objects.get(name="Dr. Constance Grey")
    except CharacterModel.DoesNotExist:
        constance = None

    scene, created = Scene.objects.get_or_create(
        name="The Rescue",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 2, 15),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Rescue")
        return scene

    print("  Created Scene: The Rescue")

    if amenhotep:
        scene.add_character(amenhotep)
    if constance:
        scene.add_character(constance)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Harrison Wells' estate. A mansion in the hills east of Seattle,
isolated and well-guarded. Five days of surveillance revealed
the cult's operation: sixteen members, rotating guard shifts,
and a basement converted into a ritual chamber.

The captive mummy is there. Still in its death-sleep, suspended
between life and death, waiting for a soul that may never come
if the Serpent's children get their way.

The Amenti don't negotiate with Apophis worshippers.

At 3 AM, Amenhotep and Constance begin their assault."""
    )

    if amenhotep:
        scene.add_post(
            character=amenhotep,
            display="Amenhotep IV",
            message="""*Amenhotep moves through the estate's shadows, ancient and silent*

*The guards never see him. His Sekhem flows through the night,
clouding minds and dimming lights*

/roll 7 6
(Dexterity + Stealth - infiltrating the compound)

*Two guards down, unconscious. Three more wandering, confused by
visions of serpents*

*He reaches the basement entrance and pauses*

"Constance. The wards are strong. Apophis protections - they've been
preparing this place for years."

*His voice is grim through their mental link*

"I'm going to have to break them the hard way. Be ready for the
response.""""
        )

    if constance:
        scene.add_post(
            character=constance,
            display="Dr. Constance Grey",
            message="""*Constance positions herself at the building's heart, where the
power lines converge*

"I'm ready. When you breach, I'll flood the building with Ma'at.
It should disrupt their rituals and weaken any serpent-spirits
they've summoned."

*She begins drawing hieroglyphics in the air with pure Sekhem*

/roll 6 6
(Intelligence + Occult - preparing the counter-ritual)

"Amenhotep - the prince. If they've begun corrupting him..."

*She doesn't finish the thought*

"Just get him out. Whatever condition he's in, we can help him.
But only if he survives tonight."

*She completes the ritual circle*

"On your mark.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The basement is worse than expected.

The ritual chamber is covered in serpent iconography - scales painted
in blood, eyes that seem to follow movement. At the center, a stone
altar holds the captive mummy. His bandages have been partially
removed, replaced with serpent-skin wrappings that pulse with
corrupt energy.

Helena leads the ritual. Eleven cultists form a circle, chanting
in a tongue older than Egypt. The air writhes with invisible
serpents, Apophis's attention drawn to this place.

They're not just holding the prince hostage. They're trying to
CORRUPT him. Turn him into a vessel for the Serpent itself.

The ritual is almost complete."""
    )

    if amenhotep:
        scene.add_post(
            character=amenhotep,
            display="Amenhotep IV",
            message="""*Amenhotep EXPLODES through the basement door, all pretense of
stealth abandoned*

"BY OSIRIS AND RA AND MA'AT HERSELF - CEASE!"

*His voice carries the power of three thousand years*

/roll 8 7
(Charisma + Occult - disrupting the ritual)

#WP

*He channels everything he has into breaking the serpent-working*

*Above, Constance's counter-ritual activates. Light floods the
building - not sunlight, but the light of cosmic order itself*

*The cultists scream as their protections shatter*

"YOU DARE CORRUPT ONE OF MY KIN?!"

*Amenhotep's true form bleeds through his mortal shell - ancient,
terrible, a judge of the dead in righteous fury*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The ritual breaks.

Apophis's attention withdraws, denied its prize. The serpent-wrappings
on the prince's body burst into flame, consumed by the pure power
of Ma'at.

Helena tries to flee. She makes it three steps before Constance
appears in her path.

The other cultists scatter, some fighting, most running. They've
never faced true Amenti before. The legends didn't prepare them
for the reality.

On the altar, the prince stirs. His first breath in centuries.
His eyes open, confused but clear.

Uncorrupted. Saved.

[Scene End - Prince rescued, cult broken]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
