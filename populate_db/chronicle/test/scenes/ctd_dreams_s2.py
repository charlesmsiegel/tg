"""
Dreams Made Flesh - Scene 2: Finding the Hope-Bearer

The changelings locate the chimera and learn its story.

Characters: Rowan Brightwater, Jack "Patches" McGee
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of Dreams Made Flesh."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        rowan = CharacterModel.objects.get(name="Rowan Brightwater")
    except CharacterModel.DoesNotExist:
        rowan = None

    try:
        patches = CharacterModel.objects.get(name='Jack "Patches" McGee')
    except CharacterModel.DoesNotExist:
        patches = None

    scene, created = Scene.objects.get_or_create(
        name="Finding the Hope-Bearer",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 12, 6),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Finding the Hope-Bearer")
        return scene

    print("  Created Scene: Finding the Hope-Bearer")

    if rowan:
        scene.add_character(rowan)
    if patches:
        scene.add_character(patches)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""A children's hospital on the outskirts of Seattle. In the mundane
world, it's a place of healing and hope - and sickness and fear.

In the Dreaming, it blazes with possibility. Children's dreams, even
in illness, burn bright. This is where the Hope-Bearer came to rest.

Rowan and Patches find it in the hospital's courtyard garden, visible
only in the Dreaming. It's magnificent and heartbreaking - a creature
of pure hope, but wounded. Fading. The mortal world is killing it,
slowly but surely.

And yet, around it, the dreams of sick children shine a little brighter."""
    )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan approaches the chimera slowly, reverently. Up close, she
can see the damage - great rents in its dreamstuff where Banality
has begun to eat away*

"Oh, you beautiful thing. What happened to you?"

*She reaches out, not quite touching*

/roll 6 6
(Charisma + Empathy - communicating with the chimera)

"We're not here to hurt you. We're not here to bind you. We want
to help."

*The chimera's eyes - shifting pools of colored light - focus on her*

*It speaks, though not in words. Images, feelings, memories flowing
directly into Rowan's mind*

"Show me. Show me why you ran.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Hope-Bearer's memories unfold:

*The Far Dreaming, beautiful beyond description. A realm of pure
imagination where chimera lived freely.*

*Then: darkness. A presence creeping through the dreamscape, consuming
everything it touched. Not Banality - something older, hungrier.*

*The Nightmare Barons. Ancient enemies of Hope, rising again after
millennia of slumber.*

*The Hope-Bearer fleeing, the last of its kind, as the Nightmare
Barons consumed everything it knew.*

*The desperate leap through the Dreaming's barriers, choosing exile
in a world of Banality over death in a realm of nightmares.*

The message is clear: something terrible is awakening in the Far
Dreaming. And it's coming this way."""
    )

    if patches:
        scene.add_post(
            character=patches,
            display="Jack 'Patches' McGee",
            message="""*Patches has gone very still, his usual mischief replaced by
genuine fear*

"Nightmare Barons. Those are supposed to be myths. Stories we tell
each other to scare fledglings."

*He looks at the wounded chimera*

/roll 4 7
(Intelligence + Greymayre - understanding the threat)

"But myths come from somewhere. And if the Hope-Bearer remembers
them..."

*He turns to Rowan*

"We have a bigger problem than one escaped chimera. The Dreaming
itself is under attack. And this is the only survivor who can tell
us what's coming."

*He looks at the hospital around them*

"We have to save it. Not just for itself - for all of us.""""
        )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan's mind races. The chimera can't survive in the mortal
world much longer. But sending it back means sending it to die*

"There might be another way. Not the Far Dreaming - but a place
IN the mortal world where belief is strong enough to sustain it."

*She gestures at the hospital*

/roll 5 6
(Intelligence + Occult - forming a plan)

"This hospital. These children. Their dreams are powerful - powerful
enough to keep a Hope-Bearer alive."

*She looks at the chimera*

"What if you stayed here? Not trapped - ANCHORED. You would feed
on their hope, and in return, you would strengthen their dreams.
A symbiosis."

*The chimera's light flickers - considering*

"You could be their guardian. The hope they don't know they have.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Hope-Bearer's response comes as a wave of cautious hope.

It has been running for so long. Fighting for so long. The idea of
a home - a purpose - is almost too much to process.

But there's a complication.

The Autumn Court hunters arrive, tracking the false trails Patches
left but eventually finding their way here. Three Sidhe warriors,
cold and pragmatic, serving interests that see the Hope-Bearer as
a resource to be harvested.

"Step away from the chimera, Seelie," their leader commands.
"We claim it in the name of Autumn's necessity."

The Hope-Bearer shrinks back, light dimming with fear.

[Scene End - Autumn Court confrontation]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
