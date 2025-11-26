"""
Social Scene: Coffee and Commiseration

Hunters meet at a diner to compare notes and decompress.

Characters: Sarah Mitchell, David Okonkwo
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create the Coffee social scene."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    characters = {}
    for name in ["Sarah Mitchell", "David Okonkwo"]:
        try:
            characters[name] = CharacterModel.objects.get(name=name)
        except CharacterModel.DoesNotExist:
            characters[name] = None

    scene, created = Scene.objects.get_or_create(
        name="Coffee and Commiseration",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 9, 20),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Coffee and Commiseration")
        return scene

    print("  Created Scene: Coffee and Commiseration")

    for char in characters.values():
        if char:
            scene.add_character(char)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Beth's Diner. 3 AM. The only customers are a long-haul trucker
nursing his fourth coffee and two people who look like they haven't
slept in days.

The latter are hunters. They've earned their exhaustion.

Outside, Seattle sleeps, unaware of the monsters that walk among
them. Inside, two people who know too much try to remember what
normal feels like."""
    )

    if characters.get("Sarah Mitchell"):
        scene.add_post(
            character=characters["Sarah Mitchell"],
            display="Sarah Mitchell",
            message="""*Sarah wraps her hands around a coffee cup, more for warmth than
the caffeine*

"You know what I miss? Being able to walk past a nightclub without
checking for feeding signs. Just... walking past."

*She stares into her coffee*

"My therapist thinks I have PTSD from 'trauma.' I can't exactly
tell her the trauma is 'I've killed three vampires and watched a
ghost possess my friend.'"

*A tired laugh*

"How do you deal with it, David? The knowing?""""
        )

    if characters.get("David Okonkwo"):
        scene.add_post(
            character=characters["David Okonkwo"],
            display="David Okonkwo",
            message="""*David pours sugar into his coffee - his third packet*

"I compartmentalize. There's 'hunting David' and 'normal David.'
They don't talk to each other."

*He stirs absently*

"Hunting David sees monsters everywhere, trusts no one, sleeps
with a gun under his pillow. Normal David has dinner with his
sister, watches football, pretends everything is fine."

*He looks at Sarah*

"It's not healthy. I know it's not. But it's the only way I've
found to stay functional."

*A pause*

"Does it get easier? Honestly? No. You just get better at carrying it.""""
        )

    if characters.get("Sarah Mitchell"):
        scene.add_post(
            character=characters["Sarah Mitchell"],
            display="Sarah Mitchell",
            message="""*Sarah nods slowly*

"Compartmentalize. I'll try that."

*She flags down the waitress for a refill*

"You know what's funny? Some nights I miss graduate school. Writing
papers about criminal psychology. Worrying about tenure track."

*She shakes her head*

"Now I know what REAL psychology is. The psychology of monsters.
Of people who've seen too much. Of whatever we're becoming."

*She raises her cup*

"To the Vigil. And to coffee strong enough to keep us awake for it.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""They drink in companionable silence. Outside, the sky begins to
lighten. Another night survived.

The waitress refills their cups without being asked. She's seen
their type before - night shift workers, she assumes. People with
jobs that keep them awake when the world sleeps.

She's not entirely wrong.

[Scene End]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
