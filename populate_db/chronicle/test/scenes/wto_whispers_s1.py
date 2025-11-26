"""
Whispers from the Void - Scene 1: The Warning

A ghostly informant brings news of Spectres massing in the Tempest.

Characters: Margaret "Peggy" Sullivan, Thomas Ashworth
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of Whispers from the Void."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        peggy = CharacterModel.objects.get(name='Margaret "Peggy" Sullivan')
    except CharacterModel.DoesNotExist:
        peggy = None

    try:
        thomas = CharacterModel.objects.get(name="Thomas Ashworth")
    except CharacterModel.DoesNotExist:
        thomas = None

    scene, created = Scene.objects.get_or_create(
        name="The Warning",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 9, 1),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Warning")
        return scene

    print("  Created Scene: The Warning")

    if peggy:
        scene.add_character(peggy)
    if thomas:
        scene.add_character(thomas)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Shadowlands version of Pike Place Market. In death, the famous
market is quieter - the echoes of commerce faded, replaced by the
whispers of ghosts who remember shopping here in life.

Margaret Sullivan tends to her Haunt, a small corner of the market that
remembers being a flower stall. Phantom blooms drift in phantom breeze.

Thomas Ashworth finds her there, his aristocratic features tight with
concern. He's been in the deeper Shadowlands - the places where the
Tempest bleeds through - and he's brought news.

Bad news."""
    )

    if thomas:
        scene.add_post(
            character=thomas,
            display="Thomas Ashworth",
            message="""*Thomas approaches without his usual pretense of calm. That alone
is alarming*

"Margaret. We have a problem."

*He looks around, checking for eavesdroppers among the dead*

"I was in the Tempest. Following rumors of a Nihil forming near the
Cascade Range. What I found..."

*He pauses, collecting himself*

/roll 5 6
(Composure - maintaining calm)

"Spectres. Hundreds of them. Organized. That's not normal - they don't
organize. They feed and destroy and scatter."

*His voice drops*

"Something is uniting them. Something big.""""
        )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy sets down the phantom flower she was arranging. Her face
shows decades of learning not to panic*

"Organized Spectres. That's Malfean work."

*She moves to a clearer space, where she can sense the Tempest's
currents*

/roll 6 6
(Perception + Awareness - sensing the Underworld)

"I feel it too. The pressure. Something's building."

*She looks at Thomas*

"Did you see what's leading them? A Nephwrack? Something worse?"

*Her voice is steady, but her hands have begun moving in old
protective patterns*

"And why Seattle? What's here that the Void wants?""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Tempest's distant roar seems louder today. Other wraiths in
the market have noticed too - they cluster in groups, whispering.
Everyone can feel the change.

Thomas's memories of what he saw surface reluctantly, shaped by his
emotions:

*A canyon of darkness. Spectral shapes crawling over each other
like maggots. And at the bottom, something vast and still,
radiating HUNGER.*

*A voice, if void could speak: "The anchors weaken. The living
forget. Soon the storm will wash them all away."*

The Tempest never forgets a grudge. And Seattle has a lot of dead."""
    )

    if thomas:
        scene.add_post(
            character=thomas,
            display="Thomas Ashworth",
            message="""*Thomas shares the memory, letting Peggy see what he saw*

"I didn't get close enough to identify the leader. But the Spectres
spoke of 'the Opening.' A mass Harrowing aimed at the living world."

*His jaw tightens*

"Seattle's Shroud is thin in places. The homeless population, the
suicide rate from the tech burnouts, the city's history of violence -
all of it creates weak points."

/roll 4 6
(Intelligence + Occult - analyzing the threat)

"If they breach the Shroud in force, they won't just haunt. They'll
CONSUME. Every mortal touched by death will be vulnerable."

*He meets her eyes*

"We need to warn the Hierarchy. And we need to find those weak points
before the Spectres do.""""
        )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy is already moving, gathering what she needs*

"The Hierarchy is slow. By the time they organize, the breach could
already be happening."

*She pulls on her Memoriam - a shawl woven from the love of her
living descendants*

"We do both. I'll contact what's left of my Circle - the other
Pardoners who haven't given in to Oblivion. You reach out to
your Masquer contacts."

/roll 5 6
(Manipulation + Leadership - organizing response)

*She pauses at the edge of her Haunt*

"Thomas. This 'Opening' - did your source say when?"

*Her voice carries dread*

"Because if the Spectres are organizing NOW, they're not planning
for months from now. They're planning for soon.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Thomas's expression answers before his words do.

"Days. Maybe less. The Tempest is... excited. It knows something is
coming. And whatever's leading those Spectres, it's been planning
this for a very long time."

The phantom flowers in Peggy's Haunt shiver, though there's no wind.

"There's one more thing," Thomas adds. "The weak points they're
targeting - I only caught fragments, but one name came up repeatedly."

He hesitates.

"Your hospital, Margaret. The place where you died. Where all
those people died in the fire."

Harborview Medical Center. One of the deadliest locations in Seattle's
history. And if the Spectres breach there...

The ripple effect would be catastrophic.

[Scene End - Threat identified, race against time begins]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
