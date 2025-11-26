"""
Seeds of Belief - Scene 1: The New Cult

A dangerous new religious movement threatens the Fallen's carefully balanced world.

Characters: Zephyrus, Marcus Wells
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of Seeds of Belief."""
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
        name="The New Cult",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 6, 1),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The New Cult")
        return scene

    print("  Created Scene: The New Cult")

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
        message="""Seattle's spiritual landscape has shifted.

A new church has appeared - the Temple of the Divine Light. Its
message: angels walk among us, here to guide humanity to ascension.
Its services draw thousands, and its founder claims direct communion
with celestial beings.

For the Fallen, this presents a problem. Faith is their currency,
their sustenance. A charismatic cult leader claiming angelic contact
is either a fraud, a tool of Heaven, or worst of all: telling the
truth about the wrong angels.

Zephyrus and Marcus watch the Temple's evening service from across
the street, sensing something deeply wrong."""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus observes the worshippers filing into the Temple - their
auras bright with genuine faith*

"That's a lot of belief. Directed, focused belief. Whoever's behind
this knows exactly what they're doing."

*He reaches out with his supernatural senses*

/roll 6 6
(Perception + Awareness - sensing the Temple's nature)

"There's... something in there. Something real. Not just smoke and
mirrors."

*His expression darkens*

"I recognize the signature. It's one of us. A Fallen. But it feels
wrong - like they've twisted their nature into something else."

*He looks at Marcus*

"Someone's set themselves up as a god. And they're harvesting all
this Faith.""""
        )

    if marcus:
        scene.add_post(
            character=marcus,
            display="Marcus Wells",
            message="""*Marcus's jaw tightens*

"A Ravener. Or something like one. Using cultists as a Faith battery."

*He watches the crowds*

/roll 5 6
(Intelligence + Investigation - analyzing the situation)

"The followers look healthy. No signs of abuse or manipulation. If
there's a Fallen running this, they're not draining people to death."

*He pauses*

"Which almost makes it worse. A sustainable harvest. Generations
of controlled Faith, all flowing to one source."

*His voice drops*

"Zephyrus, if this spreads beyond Seattle... if this becomes a
model other Fallen can copy..."

*He doesn't finish. They both know what happens when demons start
competing for worshippers.*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The service begins inside. Through the Temple's windows, light
blazes - not electric, but something far older. The congregation's
singing rises in fervent harmony.

Then the founder appears: a man called Father Emmanuel, handsome and
charismatic, radiating an inhuman peace. When he speaks, his voice
carries a resonance that makes mortal hearts ache with devotion.

"Brothers and sisters. The angels speak to me, and through me, to you.
They bring news of coming transformation. Soon, the worthy will
ascend. Soon, the faithful will know paradise."

He gestures, and light coalesces into shapes. Wings. Haloes.

Illusions - but perfect ones. The congregation gasps in rapturous
wonder.

And behind Emmanuel, invisible to mortal eyes, a shadow writhes. His
true form. His true nature. Fallen, and proud of it."""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus watches Father Emmanuel work, recognizing techniques he
himself learned in the early days after the Fall*

"He's good. Really good. Generations of practice, probably. Building
the perfect faith machine."

*He studies the shadow behind the man*

/roll 5 7
(Intelligence + Lore - identifying the Fallen)

"I don't recognize his House. But the way he shapes that light...
Neberu, maybe? One of the angelic scholars?"

*He turns to Marcus*

"We need to get inside. See what he's really doing with all that
Faith. And figure out how to stop him without crashing all that
belief into despair."

*A bitter laugh*

"The faithful don't deserve to suffer just because their god is
a demon.""""
        )

    if marcus:
        scene.add_post(
            character=marcus,
            display="Marcus Wells",
            message="""*Marcus nods*

"Agreed. We go in as potential converts. See how deep this goes,
what his endgame is."

*He looks at the Temple's glowing windows*

/roll 4 6
(Manipulation + Subterfuge - planning infiltration)

"But Zephyrus - we need to consider the possibility that Emmanuel
isn't doing anything wrong. By our standards, anyway."

*He meets his companion's eyes*

"He's harvesting Faith, sure. But he's not hurting anyone. He's
giving them hope, community, purpose. More than most churches do."

*His voice is carefully neutral*

"If we take him down, we need to be sure we're doing it for the right
reasons. Not just because he found a better hustle than us."

[Scene End - Infiltration of the Temple planned]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
