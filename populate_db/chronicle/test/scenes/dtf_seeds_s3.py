"""
Seeds of Belief - Scene 3: The Confrontation

Zephyrus and Marcus confront Father Emmanuel.

Characters: Zephyrus, Marcus Wells
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of Seeds of Belief."""
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
        name="The Confrontation",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 6, 10),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Confrontation")
        return scene

    print("  Created Scene: The Confrontation")

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
        message="""Father Emmanuel's private office. After the ceremony, after the
congregation has gone home, after the Temple falls quiet.

Zephyrus and Marcus wait in the shadows. They've decided to talk
first, fight only if necessary. Emmanuel isn't their enemy - or
at least, he doesn't have to be.

The angel enters alone. He pauses at the threshold, sensing their
presence immediately. To his credit, he doesn't run.

"I wondered how long you would watch," Emmanuel says, his human mask
slipping away. In his true form, he's radiant - light and grace and
an ancient sorrow. "The Fallen always find me eventually.""""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus steps from the shadows, his own true form partially visible*

"We're not here to fight, Emmanuel. Or whatever your true name is."

*He faces the angel - two beings who were once brothers, now separated
by an eternity of different choices*

/roll 6 6
(Charisma + Expression - establishing dialogue)

"I understand what you're doing. I even understand WHY. But you're
going to get these people killed."

*His voice carries genuine concern*

"When the other Fallen learn what you've built here, they won't
negotiate. They'll burn this Temple to the ground and everyone
in it."

*He steps closer*

"Let us help you find another way.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Emmanuel's expression shifts - surprise, skepticism, then something
like cautious hope.

"You would help me? Protect humanity from your own kind?"

He circles them slowly, light rippling with each movement.

"I've watched the Fallen for millennia. I've seen what you do to
mortals - the deals, the manipulation, the slow corruption of souls.
Why should I trust demons who claim to want something different?"

His gaze fixes on Zephyrus.

"Unless... you truly have changed. I've heard rumors of Reconcilers
among the Fallen. Those who seek redemption rather than revenge."

His voice softens.

"Is that what you are, brother? Do you remember what it was like
to serve the Light?""""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus feels the question cut deep*

"I remember everything. The Light. The Fall. The Abyss. The return."

*He lets his own light manifest - dimmer than Emmanuel's, but real*

/roll 5 6
(Charisma + Empathy - sharing truth)

#WP

"I fell because I loved humanity. I thought they deserved more than
God was giving them. I was wrong about a lot of things."

*He meets Emmanuel's ancient eyes*

"But I wasn't wrong about caring. About wanting them to thrive.
That's why I'm here."

*His voice strengthens*

"Your way will lead to war. My way... our way... might lead to
something better. Fallen and angels working together, protecting
mortals instead of fighting over them."

*He extends a hand*

"Help us prove that's possible. Please.""""
        )

    if marcus:
        scene.add_post(
            character=marcus,
            display="Marcus Wells",
            message="""*Marcus adds his voice*

"The Temple doesn't have to end. The community you've built doesn't
have to die."

*He gestures at the office, at the evidence of years of good work*

/roll 5 6
(Manipulation + Politics - proposing compromise)

"Keep teaching. Keep helping. Just... ease off the Ascension Protocol.
Fortifying humans against ALL supernatural influence cuts off more
than Fallen corruption. It cuts off hope, inspiration, genuine
miracles."

*He looks at Emmanuel earnestly*

"Let them be human. Vulnerable and beautiful and capable of amazing
things without becoming soldiers."

*A pause*

"And let us work with you. A Fallen and an angel, protecting Seattle
together. Imagine the message THAT sends.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Silence stretches through the office. Emmanuel considers the
proposal, ancient mind weighing possibilities.

Finally, slowly, he nods.

"A trial. I make no promises beyond that. If you're sincere, if
you truly seek redemption over dominion, I will work with you."

He lets his light dim to mortal levels.

"But understand: if you betray this congregation, if you use them
as your predecessors have used humanity for millennia, I will end
you. Brother or not."

He extends his own hand to meet Zephyrus's.

"Let us try a new path, demon. For their sake, if not our own."

The light that passes between them - Fallen and unfallen, exile and
rebel - carries the weight of hope.

Perhaps, after all these ages, things can be different.

[Scene End - Alliance between Fallen and Elohim]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
