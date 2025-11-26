"""
The Masquerade Frays - Scene 2: The Hunt

Dmitri tracks Gordon through the night clubs while Victoria works her
social media contacts.

Characters: Dmitri Volkov
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of The Masquerade Frays."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        dmitri = CharacterModel.objects.get(name="Dmitri 'The Bear' Volkov")
    except CharacterModel.DoesNotExist:
        dmitri = None

    scene, created = Scene.objects.get_or_create(
        name="The Hunt",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 4, 8),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Hunt")
        return scene

    print("  Created Scene: The Hunt")

    if dmitri:
        scene.add_character(dmitri)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The International District at 2 AM still pulses with life. The
legitimate restaurants have closed, but the underground clubs are just getting
started. Neon signs advertise karaoke and late-night noodles; darker
establishments hide behind unmarked doors.

Dmitri moves through the crowd like a shark through water. His imposing frame
draws glances, but his predator's gaze ensures no one holds eye contact for long.

Gordon Price was last seen heading this direction three hours ago."""
    )

    if dmitri:
        scene.add_post(
            character=dmitri,
            display="Dmitri Volkov",
            message="""*Dmitri pauses outside a door marked only with a red dragon
symbol. He can hear the bass thrumming from inside*

*He reaches out with his senses, testing the crowd beyond the door*

"Stupid child. Hiding in a place like this... you make it too easy."

/roll 5 5
(Perception + Alertness - sensing Kindred presence inside)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Through the door, Dmitri's senses brush against something familiar
- the cold emptiness that marks another predator among the living. Someone Kindred
is definitely inside. Whether it's Gordon or another vampire remains to be seen.

The bouncer - a large man with visible gang tattoos - blocks the entrance. "Private
party tonight, friend. Move along."

Behind the bouncer, the door opens briefly, letting out a blast of music and the
scent of blood. Fresh blood. Someone is feeding carelessly in there."""
    )

    if dmitri:
        scene.add_post(
            character=dmitri,
            display="Dmitri Volkov",
            message="""*Dmitri's eyes narrow. Another Masquerade breach in progress.
Tonight is a disaster*

*He locks eyes with the bouncer*

"You will step aside. You will forget you saw me."

/roll 6 7
(Manipulation + Intimidation - enhanced by Presence)

*His voice carries the weight of his Brujah blood, the edge of predatory command
that mortal minds struggle to resist*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The bouncer's confident posture wavers. His hand, which had been
moving toward a concealed weapon, drops to his side. His eyes glaze slightly as
Dmitri's supernatural presence overwhelms his will.

"I... yeah. Go ahead." He steps aside, a confused frown on his face.

Dmitri pushes through the door into a wall of sound and heat. The club is packed -
maybe a hundred mortals dancing, drinking, lost in their own world. And in the VIP
section, visible through the crowd: Gordon Price, his face buried in the neck of an
unconscious woman."""
    )

    if dmitri:
        scene.add_post(
            character=dmitri,
            display="Dmitri Volkov",
            message="""*Dmitri's vision narrows to a red point. The young fool is
doing it again. Right here. Right now*

*He begins moving through the crowd, using his bulk to create a path. His Beast
roars approval at the coming violence*

"Gordon!"

*His voice cuts through the music like a blade*

"Step. Away. From her."

/roll 4 6
(Self-Control check to resist frenzy at the sight of blatant blood)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Gordon's head snaps up, blood staining his lips. His eyes are
wild - the look of a fledgling who's lost control and knows it. For a moment,
he seems ready to fight.

Then he sees who's coming for him.

"Dmitri? I- I didn't mean to- She was willing, I swear-"

He drops the woman (who slumps to the floor, pale but still breathing) and bolts
for the back exit. Several mortals in the VIP section are filming with their
phones."""
    )

    if dmitri:
        scene.add_post(
            character=dmitri,
            display="Dmitri Volkov",
            message="""*Dmitri surges forward, his speed inhuman. The mortals with
phones need to be dealt with, but Gordon is the priority*

*He vaults over the VIP rope and gives chase*

/roll 5 6
(Dexterity + Athletics - pursuing Gordon)

*As he runs, he pulls out his phone and sends a text: "VIP section. Dragon Club.
Phones. Deal with it." Victoria will know what to do*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The chase leads through the back of the club - past startled
kitchen staff, through a storage area, and out into an alley. Gordon is fast,
propelled by terror, but Dmitri is older and more experienced.

He catches the fledgling three blocks later, slamming him against a brick wall
hard enough to crack the mortar.

"The Sheriff is expecting you, little one. And the Prince after him."

Gordon whimpers. "They're going to kill me."

Dmitri's smile is not kind. "If you are very lucky, that is all they will do."

[Scene End - Gordon captured]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
