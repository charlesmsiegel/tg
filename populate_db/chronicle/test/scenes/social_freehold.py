"""
Social Scene: Freehold Gathering

Changelings gather for storytelling and sharing of Glamour.

Characters: Rowan Brightwater, Jack "Patches" McGee
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create the Freehold Gathering social scene."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    characters = {}
    for name in ["Rowan Brightwater", 'Jack "Patches" McGee']:
        try:
            characters[name] = CharacterModel.objects.get(name=name)
        except CharacterModel.DoesNotExist:
            characters[name] = None

    scene, created = Scene.objects.get_or_create(
        name="Freehold Gathering",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 8, 10),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Freehold Gathering")
        return scene

    print("  Created Scene: Freehold Gathering")

    for char in characters.values():
        if char:
            scene.add_character(char)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Gilded Pumpkin, restored after its near-destruction. The
freehold's colors are bright again, its chimeric decorations
dancing with renewed vigor.

Tonight is Story Night - a tradition as old as the fae themselves.
Changelings gather to share tales, weave Glamour, and remember
what it means to dream.

The balefire burns warm in the hearth. The air tastes of honey
and starlight."""
    )

    if characters.get("Rowan Brightwater"):
        scene.add_post(
            character=characters["Rowan Brightwater"],
            display="Rowan Brightwater",
            message="""*Rowan sits near the balefire, her wings casting prismatic
shadows on the walls*

"I'll start tonight. A story from the old country."

*She gestures, and the fire shapes itself into images*

"Once, in the time before the Shattering, there was a Sidhe knight
who loved a mortal woman. Not ravishing - LOVE. True and deep."

*The flames show two figures dancing*

"But the Dreaming and the waking world cannot share, not fully.
And so they made a choice..."

*She tells the tale, and the gathered fae lean in, drinking the
Glamour of a story well-told*"""
        )

    if characters.get('Jack "Patches" McGee'):
        scene.add_post(
            character=characters['Jack "Patches" McGee'],
            display="Patches",
            message="""*Patches listens with unusual attention, his Pooka ears
twitching at the emotional beats*

"That's a sad one, Rowan. Beautiful, but sad."

*He stretches*

"I've got something lighter. True story - well, mostly true.
Pooka truth."

*He grins*

"So there I was, 1987, trying to convince a dragon that I was
actually a very large cat..."

*The gathered changelings groan good-naturedly - they've heard
variations of this tale before*

"No, no, this time it's DIFFERENT. The dragon was from Cleveland.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The stories flow. Sad ones, funny ones, ancient tales and
fresh experiences. Each story adds to the Glamour, strengthening
the freehold's foundations.

A young Eshu shares her first adventure in the Dreaming. An old
Troll recounts battles from before the Shattering. A Sluagh
whispers secrets that may or may not be true.

This is why the fae survive. Not through strength or cunning,
but through story. Through the insistence that wonder is real,
that dreams matter, that the world is stranger and more beautiful
than mundane eyes can see.

The balefire burns bright. The Glamour flows. And for one night,
the Dreaming is very close indeed.

[Scene End]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
