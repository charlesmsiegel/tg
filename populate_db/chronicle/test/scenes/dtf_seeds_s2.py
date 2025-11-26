"""
Seeds of Belief - Scene 2: Inside the Temple

The Fallen infiltrate the cult and discover its true purpose.

Characters: Zephyrus, Marcus Wells
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of Seeds of Belief."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        zephyrus = CharacterModel.objects.get(name="Zephyrus")
    except CharacterModel.DoesNotExist:
        zephyrus = None

    try:
        marcus = CharacterModel.objects.get(name="Marcus Wells")
    except CharacterModel.DoesNotExist:
        marcus = None

    scene, created = Scene.objects.get_or_create(
        name="Inside the Temple",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 6, 5),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Inside the Temple")
        return scene

    print("  Created Scene: Inside the Temple")

    if zephyrus:
        scene.add_character(zephyrus)
    if marcus:
        scene.add_character(marcus)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Four days undercover. Zephyrus and Marcus have attended services,
participated in study groups, and gradually worked their way into
the Temple's inner circle.

The congregation is genuine - true believers who've found meaning
in Father Emmanuel's teachings. The support groups help addicts recover.
The community dinners feed the homeless. On the surface, everything
seems... good.

But the inner circle tells a different story. Private ceremonies.
Secret initiations. And a hierarchy of devotion that leads to
something called "the Ascension Protocol."""
    )

    if marcus:
        scene.add_post(
            character=marcus,
            display="Marcus Wells",
            message="""*Marcus reports to Zephyrus after another inner circle meeting*

"I've reached the third tier. They trust me now - think I'm a true
believer ready for 'deeper mysteries.'"

*His expression is troubled*

/roll 5 6
(Intelligence + Occult - analyzing the rituals)

"The rituals are genuine Fallen lore. Modified, sanitized, but real.
Emmanuel is teaching them to channel Faith more efficiently."

*He pauses*

"But here's the thing - he's also teaching them to RESIST. Resist
demonic influence. Resist possession."

*He meets Zephyrus's eyes*

"He's not farming them. He's FORTIFYING them. Against us. Against
all Fallen.""""
        )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus processes this information*

"That doesn't make sense. Why would a Fallen teach humans to resist
demons? Unless..."

*A terrible thought forms*

/roll 6 7
(Intelligence + Lore - understanding Emmanuel's plan)

"Unless he's planning something so big that he needs to protect his
investment. Keep other Fallen from poaching his followers."

*He paces*

"The Ascension Protocol. 'The worthy will ascend.' What if he means
it literally?"

*His voice drops*

"What if Emmanuel is trying to create a permanent Faith anchor?
Humans so devoted, so protected, that they become... something else?
Living temples that generate Faith forever?"

*The implications are staggering*

"He's trying to remake humanity.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The truth is even stranger.

That night, Zephyrus and Marcus witness a secret ceremony. The
inner circle gathers in the Temple's basement, around a sigil that
burns with impossible light.

Father Emmanuel stands at the center, his human disguise flickering.
Behind the mask, his true form is beautiful and terrible - one of
the Elohim, the angels who never fell, who chose exile over war.

Not Fallen. Not demon. Something else entirely.

"Brothers and sisters," Emmanuel says, his voice resonating with
celestial authority, "tonight we take the next step. Tonight, we
begin the transformation that will protect humanity from the
darkness forever."

He's not harvesting Faith.

He's building an army."""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus watches in shock*

"Elohim. He's one of the Reconcilers - angels who refused to choose
sides in the war."

*He grabs Marcus*

/roll 4 7
(Willpower - processing the revelation)

"This changes everything. He's not a demon playing god. He's an
ANGEL trying to save humanity from us."

*His voice cracks*

"And I don't know if he's wrong."

*He looks at the ceremony below*

"What do we do, Marcus? Stop him? Help him? He's doing what some
of us wish we had the courage to do."

*The moral ground has shifted beneath their feet*

"Maybe... maybe we should just walk away.""""
        )

    if marcus:
        scene.add_post(
            character=marcus,
            display="Marcus Wells",
            message="""*Marcus's expression hardens*

"No. We can't."

*He gestures at the ceremony*

/roll 5 6
(Intelligence + Politics - analyzing the consequences)

"Think about what happens if Emmanuel succeeds. An army of humans
immune to Fallen influence. Spreading, growing, teaching others
the same resistance."

*His voice is grim*

"The other Fallen - the Raveners, the Luciferans - they won't just
accept extinction. They'll strike first. Hard. The war Emmanuel's
trying to prevent will start because of his preparation."

*He looks at Zephyrus*

"We have to talk to him. Make him understand. There's a way to
protect humanity without starting another war."

*He pauses*

"Or we expose him to the congregation. Let them decide if they want
to be soldiers in an angel's crusade."

[Scene End - Emmanuel's true nature revealed]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
