"""
Chains of the Living - Scene 1: The Fading Fetter

A wraith's connection to the living world begins to weaken.

Characters: Margaret "Peggy" Sullivan, Thomas Ashworth
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of Chains of the Living."""
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
        name="The Fading Fetter",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 10, 10),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Fading Fetter")
        return scene

    print("  Created Scene: The Fading Fetter")

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
        message="""The Shadowlands version of a Capitol Hill apartment. Peggy Sullivan
watches her granddaughter through the Shroud - Sarah, now 42, making
dinner for her own children.

For decades, Sarah was Peggy's primary Fetter - the connection to the
living world that kept her from drifting into Oblivion. But something
is wrong.

The connection is weakening. Not because Sarah has forgotten Peggy -
but because Sarah has made peace with her grandmother's death. After
years of grief, she's finally letting go.

For the living, this is healthy. For the dead, it's devastating."""
    )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy presses her hand against the Shroud, watching Sarah laugh
at something her son said*

"She's happy. She's finally happy."

*Her voice is hollow*

"I wanted this for her. Forty years of watching her carry the grief
of my death... I wanted her to heal."

*She feels the Fetter loosening, like a rope being slowly cut*

/roll 4 8
(Willpower - accepting the situation)

"But I didn't realize..."

*Her hand passes further through the Shroud than it should. She's
fading*

"I didn't realize it would feel like dying again.""""
        )

    if thomas:
        scene.add_post(
            character=thomas,
            display="Thomas Ashworth",
            message="""*Thomas materializes beside her, concern evident*

"I felt the disturbance in your Fetters. Margaret, this is serious."

*He examines her corpus, seeing the signs of decay*

/roll 5 6
(Perception + Occult - assessing Fetter damage)

"Your primary Fetter is dissolving. If you don't find a new anchor,
or strengthen an existing one..."

*He doesn't finish the sentence. They both know what happens to
wraiths who lose all their Fetters*

"What other connections do you have? The hospital? Other family?"

*His voice softens*

"Margaret, you've held on this long. We can find a way.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Through the Shroud, Sarah suddenly looks up from her cooking.
For just a moment, her eyes seem to focus on exactly where Peggy
is standing.

"Grandma?"

Her children look at her strangely. Sarah shakes her head, laughing.
"Nothing. Just... remembering something."

The Fetter pulses - not strengthening, but not dissolving either.
A single moment of connection, thin as spider silk.

In the Shadowlands, Peggy's Shadow stirs.

*"Let it go. Let HER go. She doesn't need you anymore. She never
needed you. You were just holding on because you were afraid to
face the Void."*"""
    )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy forces her Shadow down, but its words linger*

"The hospital. I still have connections there - patients I've watched
over, families I've comforted through the Shroud."

*She turns away from Sarah's apartment*

/roll 5 6
(Intelligence + Occult - identifying remaining Fetters)

"And there's... something else. Something I've been avoiding."

*Her voice drops*

"My grave. I've never visited it. Never wanted to see what the
living left behind. But a grave is a Fetter too. A place where
the living remember the dead."

*She looks at Thomas*

"I need to go there. Before it's too late.""""
        )

    if thomas:
        scene.add_post(
            character=thomas,
            display="Thomas Ashworth",
            message="""*Thomas nods slowly*

"Visiting your own grave. It's not easy. The memories, the emotions -
they can be overwhelming. And your Shadow will use every weapon it can."

*He places a hand on her shoulder*

"But you're right. If there's enough Pathos stored in that connection,
it could stabilize you. Possibly even strengthen your other Fetters."

/roll 4 6
(Manipulation + Empathy - offering support)

"I'll come with you. Whatever you face there, you won't face it alone."

*He allows himself a slight smile*

"After all, you've saved my corpus more than once. It's time I
returned the favor."

[Scene End - Journey to Peggy's grave begins]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
