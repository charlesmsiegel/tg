"""
Blood in the Water - Scene 3: The Waterfront

The coterie investigates the warehouse district where the blood shipments
were delivered. They discover more than they bargained for.

Characters: Marcus 'Shadow' Webb, Isabella Santos, Roland Cross
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of Blood in the Water."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Get characters
    shadow = CharacterModel.objects.get(name="Marcus 'Shadow' Webb")
    isabella = CharacterModel.objects.get(name="Isabella Santos")
    roland = CharacterModel.objects.get(name="Roland Cross")

    # Get location
    try:
        location = LocationModel.objects.get(
            name="Waterfront District", chronicle=chronicle
        )
    except LocationModel.DoesNotExist:
        location = None

    # Create the scene
    scene, created = Scene.objects.get_or_create(
        name="The Waterfront",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 3, 20),
            "location": location,
        },
    )

    if not created:
        print("  Scene already exists: The Waterfront")
        return scene

    print("  Created Scene: The Waterfront")

    scene.add_character(shadow)
    scene.add_character(isabella)
    scene.add_character(roland)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Seattle waterfront at 3 AM is a study in industrial decay.
Abandoned warehouses line the piers, their rusted cranes silhouetted against the
overcast sky. The smell of salt and diesel hangs in the air.

Shadow's surveillance identified this warehouse as the delivery point. It looks
abandoned - no security, no lights, no signs of recent activity. But the tire tracks
in the mud suggest otherwise.

The three Kindred approach from different directions, converging on the building
through the maze of shipping containers."""
    )

    scene.add_post(
        character=shadow,
        display="Shadow Webb",
        message="""*Shadow emerges from the shadows near a loading dock, his form
barely visible even to Kindred senses*

"No guards. No cameras I can see. Either they've cleared out..."

*He sniffs the air, his enhanced senses probing for the telltale scent of blood*

"...or this is a trap."

/roll 6 6
(Perception + Alertness - scanning for ambush)"""
    )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Shadow's keen senses pick up several concerning details. The faint
hum of a generator somewhere inside the building. The chemical tang of refrigerant.
And underneath it all, the unmistakable copper scent of blood - old blood, stale
but still potent.

More worrying: he can't shake the feeling that something is watching them. Not
from any direction he can identify, but watching nonetheless."""
    )

    scene.add_post(
        character=isabella,
        display="Isabella Santos",
        message="""*Isabella joins the others, keeping her voice low*

"Shadow, I found information about Arterius. If this is connected to them... we
may be dealing with a Fourth Generation elder. Someone who was old when the
Camarilla was young."

*She touches the amulet at her throat - a protective charm prepared for exactly
such encounters*

"I can attempt to sense any Thaumaturgical wards before we enter."

/roll 4 7
(Auspex - scanning for magical defenses)"""
    )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Isabella's mystical senses brush against the warehouse... and
recoil. There is power here - old power, woven into the very foundations of the
building. It's not Thaumaturgy as she knows it. The patterns are wrong, inverted
somehow. Almost like Thaumaturgy's dark mirror.

Whatever created these wards isn't Tremere. And it doesn't want to be found."""
    )

    scene.add_post(
        character=roland,
        display="Roland Cross",
        message="""*Roland has stopped moving, his eyes fixed on something the
others can't see*

"The walls are bleeding. Not now. Before. Many times."

*He turns in a slow circle, tracing invisible patterns in the air*

"This place remembers death. So much death. The hunger here is patient. It's
been waiting..."

*He freezes*

"Someone's coming. From below."

/roll 5 6
(Auspex - piercing the darkness)"""
    )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The moment Roland speaks, the warehouse door creaks open. Not
pushed - opened, as if in invitation.

From somewhere deep inside, a voice drifts out. It's cultured, ancient, carrying
an accent that hasn't been spoken in centuries.

"Please. Do come in. I've been expecting visitors for some time now."

The three Kindred exchange glances. Whoever is inside knows they're here. The
question is whether to accept the invitation - or flee."""
    )

    scene.add_post(
        character=shadow,
        display="Shadow Webb",
        message="""*Shadow's face contorts in what might be frustration*

"So much for the element of surprise."

*He considers their options. Running means losing the only lead they have. Going
in means walking into a situation they don't control*

"We go in. But carefully. Isabella, stay behind me - your blood magic might be
our only edge. Roland, tell us if you sense anything wrong."

*He pauses at the threshold*

"And if I signal, we run. No hesitation."

/roll 3 6
(Courage check to enter)"""
    )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The interior of the warehouse is unexpectedly elegant. What
appeared abandoned from outside has been transformed into something resembling
a Victorian parlor - antique furniture, oil paintings, Persian rugs. The contrast
with the industrial exterior is jarring.

At the center of the room, seated in a high-backed chair, is a figure. It appears
to be a middle-aged man in formal evening wear, but the stillness with which he
sits betrays his nature. No breath. No movement. Perfect, predatory stillness.

"Ah. The Nosferatu, the Tremere, and the Oracle. How... appropriate." His smile
reveals fangs. "I am Julian Arterius. And I believe we have much to discuss.""""
    )

    scene.add_post(
        character=isabella,
        display="Isabella Santos",
        message="""*Isabella forces herself not to take a step backward. Fourth
Generation. The weight of centuries presses against her like a physical force*

"Lord Arterius. We... had heard you were in torpor. Or destroyed."

*She keeps her voice steady, drawing on every ounce of her self-control*

"Why now? Why the blood shipments? The Prince of Seattle will want to know why
an elder moves so openly in his domain."

#WP
(Spending Willpower to resist the elder's presence)"""
    )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Arterius's smile widens, though it never reaches his ancient eyes.

"The blood? A simple matter of sustenance. After a century of slumber, one
develops quite an appetite." He gestures dismissively. "As for the Prince... his
concerns are noted and irrelevant."

He rises from his chair with fluid grace, centuries of predatory instinct
evident in every motion.

"I have returned because something far older than myself is stirring. Something
that threatens this city - and by extension, my investments here. I am not your
enemy, young ones. Not unless you choose to make me one."

His gaze falls on each of them in turn, ancient and measuring.

"The question is: will you help me stop what is coming? Or will you force me to
deal with it... alone?"

[Scene End - The coterie must decide whether to trust an ancient predator]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
