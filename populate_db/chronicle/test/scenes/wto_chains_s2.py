"""
Chains of the Living - Scene 2: The Grave Visit

Peggy faces her grave and confronts her Shadow.

Characters: Margaret "Peggy" Sullivan, Thomas Ashworth
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of Chains of the Living."""
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
        name="The Grave Visit",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 10, 11),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Grave Visit")
        return scene

    print("  Created Scene: The Grave Visit")

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
        message="""Evergreen Washelli Cemetery. A quiet corner of North Seattle where
the dead rest and the living come to remember.

In the Shadowlands, the cemetery is a place of power. So many memories,
so many connections between the quick and the dead. Ghosts drift among
the stones, some visiting their own graves, others simply existing in
the accumulated Pathos.

Margaret Sullivan's grave is modest. A simple headstone with her name,
dates, and the words "Beloved Mother and Nurse." Fresh flowers rest
against the stone - Sarah still visits, every month.

Peggy hasn't seen it in forty years."""
    )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy stands before her grave, unable to move. The flowers -
Sarah's flowers - hurt more than she expected*

"She still comes. After all these years."

*Her voice breaks*

"I never... I never wanted to see this. See myself reduced to a
name and two dates."

*She kneels before the stone*

/roll 4 8
(Composure - facing her death)

*The Pathos here is strong. Decades of grief, love, remembrance -
all focused on this one patch of earth*

"Hello, Margaret. It's been a while."

*She touches the headstone, and the world SHIFTS*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Shadowlands around Peggy warps. Memories flood in - not just
her memories, but the memories of everyone who ever visited this grave.

*Sarah, seventeen, sobbing on the fresh earth*
*Her son, awkwardly leaving a drawing when he was six*
*Colleagues from the hospital, paying respects*
*Strangers who noticed the flowers and wondered*

And beneath it all, her own death. The fire. The smoke. The patients
she couldn't save before the ceiling fell.

Her Shadow SURGES.

*"Remember? REMEMBER? You let them die. You were supposed to save
them and you FAILED. This grave should be marked 'Failure.' 'Coward.'
'The woman who wasn't good enough.'"*"""
    )

    if thomas:
        scene.add_post(
            character=thomas,
            display="Thomas Ashworth",
            message="""*Thomas rushes to Peggy's side as she convulses with memory*

"Margaret! Fight it! It's your Shadow - it's using the grave's
power against you!"

*He tries to stabilize her with his own Pathos*

/roll 5 6
(Pathos - supporting another wraith)

"Listen to me! Those people who visited - they didn't remember a
failure. They remembered a woman who died TRYING TO SAVE OTHERS!"

*He pulls her focus toward the flowers*

"Sarah doesn't come here every month to mourn a coward. She comes
because she's PROUD of you!"

*He can feel the Shadow's presence, pressing against Peggy's
consciousness*

"Fight, Margaret! You're stronger than it!""""
        )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy is drowning in memory. The fire. The screams. Her own
final breath*

*But through it all, she hears Thomas. And she hears something else*

*Sarah's voice, from the last time she visited: "I hope you're at
peace, Grandma. I hope you know how much we all loved you. How
much we still love you."*

"I... I died trying."

*She forces the words out*

/roll 6 6
(Willpower - fighting the Shadow)

#WP

"I DIED TRYING TO SAVE THEM!"

*She screams it at her Shadow*

"I didn't fail! I did everything I could! And I kept doing it -
forty years as a ghost, protecting the living, because that's
WHO I AM!"

*The Shadow recoils*

*The Fetter BLAZES with renewed strength*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The grave pulses with Pathos. All those years of accumulated love
and memory flow into Peggy, strengthening her corpus, renewing her
connection to the living world.

Her Shadow slinks back into the depths of her consciousness, defeated
for now. It will return - Shadows always return - but for this moment,
Margaret Sullivan stands victorious over her own darkness.

The flowers on her grave seem to glow slightly in the Shadowlands'
perpetual twilight. A new Fetter, forged from four decades of being
loved and remembered.

She's not ready to face Oblivion yet.

[Scene End - Fetter strengthened, Shadow defeated]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
