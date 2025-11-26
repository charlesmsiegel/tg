"""
Dreams Made Flesh - Scene 3: The Guardian's Choice

The chimera makes its decision and finds its new purpose.

Characters: Rowan Brightwater, Jack "Patches" McGee
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of Dreams Made Flesh."""
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
        name="The Guardian's Choice",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 12, 6),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Guardian's Choice")
        return scene

    print("  Created Scene: The Guardian's Choice")

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
        message="""The hospital courtyard, in the space between Dreaming and waking.
Three Autumn Court warriors face two Seelie changelings and a wounded
chimera that contains the last hope of its kind.

The air crackles with potential conflict.

Inside the hospital, children sleep. Their dreams flow out into the
Dreaming, fragile threads of imagination that could be snuffed out
by careless violence.

The Hope-Bearer watches, uncertain. It has run for so long. Perhaps
it's time to stop running. Perhaps it's time to fight."""
    )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan places herself between the hunters and the chimera*

"The Hope-Bearer is not a resource. It's a survivor. The last of
its kind, with knowledge we desperately need."

*She meets the leader's cold gaze*

/roll 6 7
(Manipulation + Politics - negotiating)

"You want to harvest its power? Fine. But do you know what's
driving it from the Far Dreaming? The Nightmare Barons are awakening.
If we don't prepare, there won't BE an Autumn Court to serve."

*She lets that sink in*

"The chimera stays here. It guards these children. And in return,
it tells us everything it knows about what's coming. That's a better
deal than whatever power you'd squeeze from its corpse.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Autumn leader - Lady Thornblade - pauses. The Nightmare Barons
are a name even the Unseelie fear.

"You speak of myths."

"The chimera doesn't think they're myths," Rowan responds. "And
neither should you."

Thornblade's eyes flick to the Hope-Bearer, then back to Rowan.
Autumn Court pragmatism wars with Autumn Court survival instinct.

"If what you say is true... we need verification. The chimera comes
with us for questioning."

"The chimera isn't going anywhere it doesn't choose to go." Rowan's
voice hardens. "It's suffered enough.""""
    )

    if patches:
        scene.add_post(
            character=patches,
            display="Jack 'Patches' McGee",
            message="""*Patches steps forward, his usual grin replaced by something
more dangerous*

"Here's the thing about Hope-Bearers, Thornblade. They're creatures
of belief. They do what they're meant to do - inspire hope."

*He gestures at the hospital*

/roll 5 6
(Charisma + Expression - making his point)

"Those kids in there? They believe they'll get better. They believe
tomorrow will be brighter. That's what the Hope-Bearer feeds on -
and what it GIVES."

*His voice drops*

"You want to take that away? Make it serve Autumn's 'necessity'?
All you'll do is kill it. And kill those children's dreams in the
process."

*He meets her eyes*

"Is that really what Autumn wants to be known for?""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Silence stretches. The Hope-Bearer's light pulses - stronger now
than when they found it, fed by the dreams flowing from the hospital.

Lady Thornblade's expression shifts. She's pragmatic, not cruel.
The difference matters.

"A compromise. The chimera remains here, under Seelie protection.
But Autumn receives full reports on the Nightmare Baron threat. And
if the situation changes..."

"Then we renegotiate," Rowan finishes. "Agreed."

Thornblade nods curtly. "Agreed. Don't make me regret this, Brightwater."

She signals her warriors, and they vanish into the Dreaming Roads.

The courtyard falls quiet."""
    )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan sags with relief, then turns to the Hope-Bearer*

"It's over. You're safe."

*The chimera's light blazes brighter - not just recovery, but
transformation. It's choosing its new form, adapting to its new
purpose*

/roll 5 6
(Perception + Kenning - witnessing the transformation)

*What emerges is smaller than before, but somehow MORE. A creature
of gentle light and warm colors, perfectly suited to watching over
dreaming children*

"Welcome home," Rowan whispers. "Guardian of the sick. Bearer of
hope. You have a purpose again."

*The Hope-Bearer brushes against her consciousness with pure gratitude*

*In the hospital, a child wakes from a nightmare, but before fear
can take hold, she sees something beautiful in the corner of her
eye. She smiles, and goes back to sleep.*

[Scene End - Hope-Bearer becomes hospital guardian]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
