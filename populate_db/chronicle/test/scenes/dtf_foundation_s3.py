"""
The Foundation Cracks - Scene 3: Into the Underground

The alliance descends to confront the Earthbound.

Characters: Zephyrus, Marcus Wells
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of The Foundation Cracks."""
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
        name="Into the Underground",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 4, 22),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Into the Underground")
        return scene

    print("  Created Scene: Into the Underground")

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
        message="""Midnight. The old Seattle Underground.

The buried streets of the original city, entombed after the Great
Fire of 1889. Now a tourist attraction in parts, forgotten in others.
And beneath the deepest forgotten sections: the Earthbound's lair.

The assault teams move in simultaneously. Radio contact confirms
the vampires have breached Pioneer Square. The werewolves howl from
the waterfront tunnel. Above, the mages' ritual circle begins to glow.

Zephyrus and Marcus lead their team down the main shaft, into
darkness that feels alive.

The Earthbound KNOWS they're coming."""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus descends into the darkness, his infernal nature letting
him see things mortals can't*

"It's aware of us. It's been waiting."

*The walls seem to pulse with a heartbeat far older than the city*

/roll 6 6
(Perception + Alertness - navigating the lair)

"Stay close. The Earthbound can manipulate perception. Make you see
things that aren't there. Make you miss things that are."

*He summons a fraction of his true power - light that burns without
heat, illuminating the buried streets*

"Collins, Marcus - weapons ready. It's going to test us before we
reach the heart.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The first test comes from the walls themselves.

Faces emerge from the brick and stone - the victims of the 1889 fire,
their death agonies preserved in the Earthbound's memory. They reach
out with spectral hands, trying to drag the intruders into the walls.

Collins opens fire with blessed rounds. The ghosts shriek and dissolve.

*"MORE,"* a voice rumbles from below. *"BRING ME MORE. I HAVE BEEN
SO HUNGRY."*

The passage narrows, forcing them single-file. Ahead, a vast chamber
opens up - the Earthbound's nest, where it has slept for millennia."""
    )

    if marcus:
        scene.add_post(
            character=marcus,
            display="Marcus Wells",
            message="""*Marcus pushes forward, his own infernal power manifesting as
shadows that shield the team*

"Radio check - other teams, report!"

*Static. Then voices*

"Vampires engaging hostiles - some kind of corpse-things-"
"Garou here - we've got Banes, corrupted spirits-"

*Marcus curses*

/roll 5 7
(Intelligence + Occult - understanding the defenses)

"It's throwing everything it has at the other teams. Trying to
buy time."

*He looks at Zephyrus*

"Which means WE'RE the real threat. We have to hit it NOW, before
our allies are overwhelmed.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""They enter the heart chamber.

The Earthbound is VAST. A mass of darkness and hunger, coiled around
the remains of whatever it once was. Eyes - too many eyes - open
as they approach. A mouth forms, speaking words that bypass ears
and strike directly at the soul.

*"LITTLE BROTHERS. YOU KNOW WHAT I AM. YOU KNOW YOU CANNOT DEFEAT ME."*

It shifts, revealing glimpses of its true form - something that
was beautiful once, before the endless hunger consumed everything
else.

*"JOIN ME. FEED WITH ME. THERE IS ROOM FOR ALL IN OBLIVION."*

The offer is genuine, and terrifying in its sincerity."""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus faces the ancient evil, his own light burning brighter*

"I remember you. Or what you were. Zaluriel. The Herald of Dawn."

*The name hits the Earthbound like a physical blow*

/roll 7 7
(Manipulation + Expression - invoking true name)

#WP

"You were beautiful once. You brought light to the early world.
And then you let the hunger consume you."

*He steps forward*

"I fell too. I sinned too. But I found something else. Something
beyond hunger and oblivion."

*His voice rises*

"I found CHOICE. And I choose to be more than my worst nature!"

*He attacks - not with violence, but with TRUTH. With the light that
the Earthbound used to carry*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Earthbound SCREAMS.

Not from pain - from recognition. From memory. The light Zephyrus
carries is the same light it abandoned millennia ago. Seeing it
now, wielded against it, is agony worse than any weapon.

*"NO! THAT LIGHT IS GONE! I DESTROYED IT! I-"*

Collins and Marcus press the attack, pouring everything they have
into the momentarily stunned creature. Above, the mages' ritual
reaches its peak, sealing escape routes.

The other teams report victory - the defenders are falling.

And in the heart of the old Seattle, the oldest battle is being
fought: the battle between what something was and what it has become.

The Earthbound has a choice to make.

[Scene End - Final confrontation underway]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
