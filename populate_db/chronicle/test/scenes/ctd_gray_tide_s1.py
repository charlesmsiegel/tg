"""
The Gray Tide - Scene 1: The Fading Dream

Banality threatens to consume a beloved freehold.

Characters: Rowan Brightwater, Jack "Patches" McGee
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of The Gray Tide."""
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
        name="The Fading Dream",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 11, 1),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Fading Dream")
        return scene

    print("  Created Scene: The Fading Dream")

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
        message="""The Gilded Pumpkin, a freehold hidden behind a vintage toy store
in Capitol Hill. In the Dreaming, it's a glorious palace of wonder -
towers of spinning tops, gardens of candy-cane flowers, a sky that
changes color with the visitors' moods.

At least, it used to be.

Now the colors are fading. The candy-cane flowers droop. The sky is
a persistent, worrying gray.

Rowan Brightwater has watched the freehold slowly die for three months.
Every week, a little more Glamour drains away. Every day, Banality
creeps a little closer.

Something is wrong. Deeply, fundamentally wrong."""
    )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan stands in what used to be the freehold's Heart - the place
where Glamour pooled deepest. Now it's barely a trickle*

"Three months. I've tried everything. Revelry, inspiration, artistic
events - nothing stops the drain."

*She touches a wilting flower, watching it grey at the edges*

/roll 5 6
(Perception + Kenning - diagnosing the problem)

"This isn't natural Banality encroachment. It's too fast, too focused.
Something is actively pulling Glamour out of this place."

*Her wings - visible in the Dreaming as iridescent dragonfly wings -
droop with exhaustion*

"We're losing the Gilded Pumpkin. And if we lose this freehold..."

*She doesn't finish. Everyone knows what happens to changelings without
Glamour*"""
        )

    if patches:
        scene.add_post(
            character=patches,
            display="Jack 'Patches' McGee",
            message="""*Patches ambles in, his patchwork coat even more mismatched than
usual. His Pooka ears twitch nervously*

"Rowan. Bad news from the Dreaming Roads."

*He pulls out a map covered in hastily scrawled notes*

/roll 4 6
(Intelligence + Investigation - sharing findings)

"I've been checking the other freeholds. The Gilded Pumpkin isn't
the only one fading. Three others in Seattle - the Midnight Carousel,
the Cloud Castle, the Laughing Library - all showing the same symptoms."

*His usual grin is absent*

"Something's hunting us. Hunting our Glamour. And it's winning.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The news hits Rowan like a physical blow. Four freeholds, all fading
at once. This isn't coincidence - it's coordinated attack.

The Gilded Pumpkin's balefire flickers. Once, it burned bright with
the dreams of children who believed in magic. Now it's barely an ember.

A chill runs through the freehold - not physical cold, but the cold
of Banality pressing closer. The gray sky darkens.

Something is coming.

Through the freehold's door, in the mundane toy store, a customer
enters. Her aura is wrong - too gray, too empty, like a black hole
where a person should be. She begins examining the vintage toys with
clinical detachment, and where she touches, color fades."""
    )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan sees the woman's aura through the Dreaming and FREEZES*

"Dauntain."

*The word is barely a whisper*

"Patches. That woman. She's Dauntain - a changeling who's given
herself to Banality."

*Her hand goes to her chimerical blade*

/roll 5 7
(Perception + Kenning - reading the Dauntain)

"No. Not just Dauntain. She's a VESSEL. Someone is channeling
Banality THROUGH her."

*She backs away from the door*

"We need to evacuate the freehold. Now. Before she finds the entrance.""""
        )

    if patches:
        scene.add_post(
            character=patches,
            display="Jack 'Patches' McGee",
            message="""*Patches's Pooka nature rebels at the idea of running, but even
he can feel the wrongness radiating from the mundane side*

"If she's a vessel, there's something bigger behind this. Someone's
using Dauntain as weapons."

*He starts herding the lesser chimera toward the back exit*

/roll 5 6
(Wits + Stealth - organizing quiet evacuation)

"The other freeholds - same thing? Dauntain attacks?"

*He pauses*

"Rowan, if someone's weaponized Banality against all of Seattle's
freeholds at once, we're not dealing with random Dauntain. We're
dealing with a conspiracy."

*His voice drops*

"We need help. Court help."

[Scene End - Dauntain threat identified]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
