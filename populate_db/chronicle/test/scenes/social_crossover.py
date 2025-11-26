"""
Social Scene: Neutral Ground

Representatives from different supernatural factions meet to discuss Seattle.

Characters: Multiple gamelines
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create the Neutral Ground crossover social scene."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Try to get characters from multiple gamelines
    character_names = [
        "Victoria Chen",  # Vampire
        "Elena Vasquez",  # Mage
        "Zephyrus",  # Demon
        "Sarah Mitchell",  # Hunter
    ]

    characters = {}
    for name in character_names:
        try:
            characters[name] = CharacterModel.objects.get(name=name)
        except CharacterModel.DoesNotExist:
            characters[name] = None

    scene, created = Scene.objects.get_or_create(
        name="Neutral Ground",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 10, 1),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Neutral Ground")
        return scene

    print("  Created Scene: Neutral Ground")

    for char in characters.values():
        if char:
            scene.add_character(char)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Paramount Theatre, closed for "private event." Actually closed
because four different flavors of supernatural entity needed a
place to talk without killing each other.

Neutral ground is hard to find in Seattle. Everywhere belongs to
someone. But the Paramount has history - built in 1928, it's seen
enough strange gatherings that one more doesn't register.

Tonight's agenda: territorial boundaries. Too many supernatural
factions operating in too small a space. Something has to give.

Or someone."""
    )

    if characters.get("Victoria Chen"):
        scene.add_post(
            character=characters["Victoria Chen"],
            display="Victoria Chen",
            message="""*Victoria represents the Camarilla, looking entirely too comfortable
in the ornate surroundings*

"The Kindred were here first. We have established feeding grounds,
established Elysium, established LAW. Whatever arrangements we make
must acknowledge that foundation."

*She crosses her legs, examining the others*

"I'm not here to start a war. But I won't cede territory we've held
for a century just because other... parties... have decided to
become active."

*Her smile is diplomatic but cold*

"What do the Traditions propose?""""
        )

    if characters.get("Elena Vasquez"):
        scene.add_post(
            character=characters["Elena Vasquez"],
            display="Elena Vasquez",
            message="""*Elena sits apart, uncomfortable with the company but pragmatic
about necessity*

"The Traditions have no interest in your 'feeding grounds.' We
don't feed on mortals."

*She makes a face*

"What we require is access to sites of power. Ley line nexuses.
Places where the Tapestry is thin. Most of these don't overlap
with vampire territory."

*She produces a map*

"I propose a simple exchange: you stay out of our nodes, we stay
out of your... whatever you call them. The night clubs and blood
banks and whatever else you use."

*A pause*

"It's not friendship. But it's functional.""""
        )

    if characters.get("Zephyrus"):
        scene.add_post(
            character=characters["Zephyrus"],
            display="Zephyrus",
            message="""*Zephyrus speaks carefully - a demon among creatures who might
hate him on principle*

"The Fallen have no formal territory. We're... scattered. Individual.
Each of us has our own arrangements with our hosts and our communities."

*He spreads his hands*

"What we want is simple: to exist without being hunted. To help who
we can without interference. To find our own redemption."

*He looks at each representative in turn*

"I know what I am. What we were. But we're trying to be something
different now. Some of us, anyway."

*His voice drops*

"All we ask is a chance to prove that.""""
        )

    if characters.get("Sarah Mitchell"):
        scene.add_post(
            character=characters["Sarah Mitchell"],
            display="Sarah Mitchell",
            message="""*Sarah sits stiffly, acutely aware she's the only human in the room*

"I'm here because someone has to speak for the people who don't know
this meeting is happening. The normal people. The ones you all feed
on or recruit or whatever it is you do."

*Her voice is steady despite her fear*

"Hunters don't want territory. We don't want treaties. We want
people to stop DYING."

*She meets each set of inhuman eyes*

"So here's our offer: police yourselves. Don't leave bodies. Don't
leave witnesses. Don't leave traumatized families wondering what
happened to their loved ones."

*A pause*

"Do that, and we stay out of your way. Fail..."

*She lets the implication hang*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The negotiations continue. Compromises are offered, rejected,
modified. Old grievances surface and are grudgingly set aside.

No one leaves happy. But no one leaves dead, either.

By dawn, there's something like an agreement. Not peace - not
among creatures like these - but an understanding. A framework
for coexistence.

Seattle remains a city of monsters. But tonight, the monsters
have agreed to share.

It won't last forever. It never does.

But for now, it's enough.

[Scene End]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
