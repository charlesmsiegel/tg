"""
The Stolen Scarab - Scene 3: Redemption

Sekhemib makes his choice.

Characters: Amenhotep IV, Dr. Constance Grey
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of The Stolen Scarab."""
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
        name="Redemption",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 5, 8),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Redemption")
        return scene

    print("  Created Scene: Redemption")

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
        message="""The command center falls silent. Sekhemib stands frozen, the Scarab
in one hand, his other hand pressed to his head as if trying to
hold his mind together.

The hypnotized mortals stand motionless, awaiting orders that
don't come.

Three thousand years of existence, and it comes down to this
moment. A soldier who's forgotten why he fights. A relic that
could preserve his madness forever. And two friends trying to
reach him through the fog."""
    )

    if amenhotep:
        scene.add_post(
            character=amenhotep,
            display="Amenhotep IV",
            message="""*Amenhotep crosses the remaining distance, ignoring the guards*

"Sekhemib. Listen to me."

*He places his hands on the old general's shoulders*

/roll 6 6
(Charisma + Empathy - final appeal)

#WP

"You are lost because you're trying to hold onto something that
no longer exists. The war. The kingdom. The person you were."

*His voice is gentle but firm*

"But that's the nature of existence, old friend. We change. We
forget. We become new things. It's not a curse - it's a gift."

*He looks at the Scarab*

"If you use that, you'll never change again. Never heal. Never
find peace. You'll be frozen in this moment of pain forever."

*He meets Sekhemib's eyes*

"Let it go. Let me help you find something new to be.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Sekhemib's hand trembles. The Scarab pulses with ancient power,
offering an easy answer: eternal stasis, an end to the confusion.

But somewhere in his fragmented mind, a memory surfaces. Not of
war. Not of battle.

A memory of Amenhotep, sharing wine after a victory. Laughing
about the absurdity of their existence. Making plans for the
next thousand years.

*"Promise me,"* his memory-self says, *"that if I ever lose
myself, you'll bring me back. Or let me go. Don't let me
become a monster."*

*"I promise,"* memory-Amenhotep replies.

Sekhemib's eyes clear, just for a moment."""
    )

    if constance:
        scene.add_post(
            character=constance,
            display="Dr. Constance Grey",
            message="""*Constance sees the change and moves*

"Sekhemib - you don't have to use the Scarab, but you don't have
to be alone either."

*She approaches carefully*

/roll 5 6
(Manipulation + Expression - offering hope)

"There are healers among us. Ways to mend what's broken. It takes
time, and it's painful, but it's POSSIBLE."

*She gestures at the bunker, the guards, the whole sad fortress*

"This isn't who you have to be. This is just... where you got lost.
We can find the way back together."

*She extends a hand*

"Trust us. One more time.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""A long moment passes.

Then Sekhemib places the Scarab in Amenhotep's hand.

"I remember now. The promise. You always kept your promises."

He sags, exhaustion replacing the manic energy.

"I'm tired, old friend. So tired of fighting. Fighting enemies,
fighting myself, fighting the forgetting."

He looks around the bunker as if seeing it clearly for the first
time.

"What have I been doing?"

The hypnotized guards blink awake, confused and frightened.
Sekhemib releases them with a whispered word.

"Take me home, Amenhotep. Wherever that is now. I think... I think
I need to rest."

The Scarab returns to its proper place. A broken soldier begins
the long road to healing. And two friends walk out of the darkness
together.

[Scene End - Scarab recovered, Sekhemib begins recovery]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
