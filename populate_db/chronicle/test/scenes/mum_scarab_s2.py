"""
The Stolen Scarab - Scene 2: The Bunker

The mummies confront their broken comrade.

Characters: Amenhotep IV, Dr. Constance Grey
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of The Stolen Scarab."""
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
        name="The Bunker",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 5, 8),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Bunker")
        return scene

    print("  Created Scene: The Bunker")

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
        message="""A Cold War-era bunker, buried deep in the Cascade Mountains. The
entrance is hidden, but Amenhotep knows the signs - Sekhemib always
did leave markers for his troops to follow.

Inside, the concrete corridors have been transformed. Hieroglyphics
cover every surface, military maps blend with ancient battle plans,
and weapons from across three thousand years of warfare line the walls.

Sekhemib's fragmented mind has built itself a fortress.

He waits in the command center, the Scarab of Khepri clutched in
one hand. He's dressed in a bizarre mixture of Egyptian armor and
modern tactical gear.

And he's not alone. A dozen mortals, hypnotized and armed, stand
guard around him."""
    )

    if amenhotep:
        scene.add_post(
            character=amenhotep,
            display="Amenhotep IV",
            message="""*Amenhotep approaches with hands raised, showing he carries no
weapons*

"Sekhemib. My old friend. Do you know me?"

*He speaks gently, as to a wounded animal*

/roll 6 6
(Charisma + Empathy - reaching through the confusion)

"We served together. Remember? The battles against the Hyksos.
The defense of Memphis. You saved my life at Avaris."

*He takes a careful step forward*

"I'm not your enemy. I never was. Whatever you think is happening,
whatever war you think you're fighting - it's over. It ended
millennia ago."

*His voice cracks*

"Please, my friend. Come back to us.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Sekhemib's eyes flicker. For a moment, recognition breaks through
the madness.

"Amenhotep? Is that... no. No, you're dead. You fell at Thebes.
I SAW you fall."

His grip tightens on the Scarab.

"You're a trick. A deception sent by the enemy. They've grown clever
in my absence."

He gestures, and his mortal guards raise their weapons.

"I will not be deceived. I will not FALL again. The Scarab will
preserve me. Keep me strong. Keep me READY for when the enemy
returns."

His voice rises to a shout.

"AND THEY WILL RETURN! THEY ALWAYS RETURN!""""
    )

    if constance:
        scene.add_post(
            character=constance,
            display="Dr. Constance Grey",
            message="""*Constance tries a different approach*

"General Sekhemib. I am Dr. Constance Grey - Mesektet, reborn. I
was not there at the battles you remember, but I know your name."

*She kneels, showing respect*

/roll 5 6
(Manipulation + Empathy - using different tactics)

"Your service to Egypt is legendary. Your courage is sung in the
halls of the dead. But general - the war is WON."

*She meets his eyes*

"The Hyksos are dust. Their empire is forgotten. EGYPT still stands,
in ways you cannot imagine. Your victory endured."

*She gestures at the bunker*

"You don't need to keep fighting. You've already won.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Something shifts in Sekhemib's expression. The words are reaching
him - not completely, but enough.

"Won? We... won?"

He looks at the Scarab in his hand.

"But I remember falling. I remember the darkness. The forgetting.
If we won, why do I feel like I'm still fighting?"

Tears stream down his ancient face.

"I don't understand anymore. I can't tell what's real. Is this
real? Are YOU real?"

The guards' weapons waver as his concentration breaks.

"I took the Scarab because... because I thought if I could stop
changing, stop FORGETTING, I could find my way back. But I can't
find my way back. There's nothing to go back TO."

[Scene End - Sekhemib's confusion breaks through]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
