"""
The Contested Node - Scene 3: Resolution

The cabal finds a way to properly reseal the spirit and claim the node.

Characters: Elena Vasquez, James Chen
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of The Contested Node."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        elena = CharacterModel.objects.get(name="Elena Vasquez")
    except CharacterModel.DoesNotExist:
        elena = None

    try:
        james = CharacterModel.objects.get(name="James Chen")
    except CharacterModel.DoesNotExist:
        james = None

    scene, created = Scene.objects.get_or_create(
        name="Resolution",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 7, 16),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Resolution")
        return scene

    print("  Created Scene: Resolution")

    if elena:
        scene.add_character(elena)
    if james:
        scene.add_character(james)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The containment holds, but barely. The light-spirit strains against
the combined weavings of Verbena and Hermes, testing for weaknesses. It's
only a matter of time before it breaks free.

The Hermetics have sent for reinforcements. So has Elena's chantry. And
somewhere above, the Technocracy is certainly mobilizing.

The chamber has become a powder keg with lit fuses on every side.

James has spent the last twelve hours analyzing every scrap of data he can
gather. If there's a solution, it's hiding in the patterns."""
    )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James's eyes are red from staring at screens. His tablet is
connected to three other devices, running parallel analysis*

"I've got it. I think."

*He pulls up a holographic display - the chamber, the node, the spirit*

/roll 7 7
(Intelligence + Occult - breakthrough analysis)

"The original seal wasn't just containing the spirit. It was FEEDING it.
The spirit is the node's guardian - bound here in the First Age to
protect the Quintessence from exploitation."

*He highlights patterns in the display*

"The seal failed because no one was maintaining it. Centuries of neglect.
The guardian woke up because it thought the node was under attack."

*He looks at Elena*

"We don't need to fight it. We need to CONVINCE it we're worthy.""""
        )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena studies the display, exhaustion temporarily forgotten*

"A guardian spirit. Not an enemy - a protector doing its job."

*She turns to the Hermetic leader*

"Your House's records - do they mention anything about this? About
guardians bound to ancient nodes?"

/roll 5 6
(Manipulation + Occult - diplomatic approach)

"Because if James is right, the worst thing we can do is treat this as
a threat. We need to approach it as supplicants, not conquerors."

*She takes a breath*

"I'm going to try something. Lower your containment on my signal.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Hermetic leader hesitates. Her companions look horrified at the
suggestion.

"You would release the entity? The risk-"

"Is less than the risk of the Technocracy returning with enough firepower
to crack this chamber like an egg," Elena interrupts.

The silver-haired woman considers. Then, slowly, she nods.

"On your head be it, Verbena. If this fails..."

"Then we're no worse off than we were already.""""
    )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena steps toward the contained spirit. Its light pulses with
barely contained fury*

*She kneels before it, head bowed*

"Guardian of the Dreaming Waters. I am Elena Vasquez, Verbena, servant of
the Old Ways. I come not to steal or control - I come to ask."

/roll 6 6
(Charisma + Occult - spirit negotiation)

#WP

"The world above has changed. The enemies of magic grow stronger while
its defenders fragment and fight among themselves. This node - YOUR node -
could help restore balance."

*She looks up, meeting the spirit's luminous gaze*

"Let us tend this place as the ancients did. Let us be your hands in the
world above. We will maintain the wards. We will honor the old compacts."

*Her voice is steady*

"Or destroy us, if you find us unworthy. But at least hear our plea.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The spirit's rage dims. Not gone - ancient beings don't forgive so
easily - but tempered by something else. Curiosity, perhaps. Or recognition.

"VERBENA. THE OLD BLOOD STILL FLOWS."

Its attention shifts to James, to the Hermetics.

"AND THESE OTHERS? WHAT CLAIM HAVE THEY?"

Elena doesn't answer for them. This is their test too."""
    )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James steps forward, tablet still in hand*

"I'm James Chen. Virtual Adept. We're... not usually known for reverence
toward old things."

*He sets the tablet down - a gesture of trust*

/roll 5 6
(Charisma + Expression - sincere appeal)

"But we believe in understanding. In learning. In finding patterns that
others miss. The ancients who bound you here - they understood something
important. Something that's been lost."

*He gestures at the chamber*

"I want to learn what they knew. Not to exploit it. To preserve it. To
make sure knowledge like this survives, whatever the Technocracy does to
the world above."

*He meets the spirit's gaze*

"That's my claim. Take it or leave it.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The spirit considers. An eternity passes in a moment.

"THE DREAM REMEMBERS THE SEEKERS OF PATTERN. THEY TOO WERE WORTHY, ONCE."

It turns to the Hermetics. The silver-haired woman straightens her spine
and speaks:

"House Bonisagus has guarded this place for five centuries, though we lost
its location. We failed in our duty. But we would make amends, if permitted."

Another eternal moment.

"FIVE CENTURIES. A BLINK. BUT THERE IS TRUTH IN YOUR WORDS."

The spirit's light begins to fade - not dying, but settling. The pool
calms. The Quintessence flow stabilizes.

"THE SEAL IS RESTORED. I GRANT STEWARDSHIP TO THESE THREE LINES: OLD BLOOD,
PATTERN SEEKER, KEEPER OF NAMES. FAIL ME NOT."

And then it's gone. The chamber is quiet. The node pulses with renewed
power.

The Technocracy, when they return, will find nothing but empty tunnels.
The seal is stronger than ever - and now it has three Traditions to
maintain it.

[Scene End - Node secured, alliance formed]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
