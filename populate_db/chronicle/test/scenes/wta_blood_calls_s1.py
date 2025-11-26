"""
Blood Calls to Blood - Scene 1: The Missing Kinfolk

A kinfolk family member has disappeared under suspicious circumstances.

Characters: Runs-Through-Shadows, Storm's Fury
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of Blood Calls to Blood."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        shadow = CharacterModel.objects.get(name="Runs-Through-Shadows")
    except CharacterModel.DoesNotExist:
        shadow = None

    try:
        storm = CharacterModel.objects.get(name="Storm's Fury")
    except CharacterModel.DoesNotExist:
        storm = None

    scene, created = Scene.objects.get_or_create(
        name="The Missing Kinfolk",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 6, 15),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Missing Kinfolk")
        return scene

    print("  Created Scene: The Missing Kinfolk")

    if shadow:
        scene.add_character(shadow)
    if storm:
        scene.add_character(storm)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""A small apartment in Capitol Hill. The furniture is sparse but well-
maintained - the home of someone who works hard and doesn't waste money on
appearances.

Photos on the walls show a woman in her thirties with two children. In some
photos, wolves can be seen in the background. This is the home of Maria
Vasquez, kinfolk to the Children of Gaia.

Maria's mother, Elena, sits on the couch. She's been crying. A young Theurge
from the sept stands nearby, having called in the pack.

The children are staying with relatives. Maria has been missing for three
days."""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows enters in Homid, dressed in practical street clothes.
She approaches Elena gently*

"Elena. I'm sorry for what you're going through. We're going to find Maria."

*She glances around the apartment, looking for anything out of place*

"Can you tell us about the last time you saw her? Anything unusual in the
days before she disappeared?"

/roll 5 6
(Perception + Investigation - examining the scene)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Elena wipes her eyes. "She was fine. Normal. She dropped the kids off
on Tuesday morning, said she was going to work." Her voice cracks. "The
restaurant called that afternoon - she never showed up."

The apartment shows no signs of struggle. Maria's phone was found in her car,
parked three blocks away. Her purse and wallet were still inside.

The young Theurge - called Speaks-With-Spirits - adds quietly: "I tried to
contact local spirits. They're... confused. Something happened here, but
their memories have been... clouded. Deliberately obscured.""""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm remains standing, his presence filling the small room.
He keeps his voice gentle - unusual for him*

"Who would want to hurt Maria? She have any enemies? Anyone paying unusual
attention to her?"

*He looks to the Theurge*

"Clouded memories. That takes power. And knowledge of the spirit world."

*His jaw tightens*

"Dancers again? Or something else?"

/roll 4 6
(Intelligence + Occult - identifying possible causes)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Elena shakes her head. "She didn't have enemies. She worked at a
restaurant, she raised her kids, she..." She trails off, then adds: "There
was a man. A few weeks ago. He came into the restaurant, kept asking her
questions. About her family. Where she grew up."

The Theurge adds: "The obscuring wasn't Wyrm-work. Too clean for that. This
was done by someone who knows spiritual protocols. Could be Dancers with
unusual training, but..."

She hesitates.

"It could also be our own kind. Or mages. Or something else entirely.""""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows' expression hardens*

"The man. What did he look like? Did Maria mention anything else about him?"

*She moves to examine Maria's personal effects*

"And this questioning - about her family. Her birth family?"

*She looks at Storm*

"Kinfolk don't just disappear without a trace. Someone wanted her specifically.
And if they knew to obscure the spirits..."

*Her voice drops*

"They knew she was kinfolk. They knew we'd come looking."

/roll 6 7
(Perception + Alertness - looking for clues)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Elena struggles to remember. "Dark hair. Professional-looking. He
had an accent - Eastern European, maybe? Maria said he gave her the creeps.
She told him to leave, and he did. But she mentioned seeing him again, outside
the restaurant. Watching."

Among Maria's things, Shadows finds something: a business card, crumpled like
it was meant to be thrown away but wasn't. It reads:

"GENESIS RESEARCH
'Building Tomorrow's World Today'
Dr. Viktor Aldrich
Acquisitions Specialist"

There's no address. Just a phone number."""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm takes the card, studying it*

"Genesis Research. Acquisitions Specialist."

*His lip curls back from his teeth*

"They talk about kinfolk like they're... inventory."

*He looks at Shadows*

"This isn't random predation. It's hunting. Targeted hunting. Someone is
collecting kinfolk."

*He turns to Elena*

"We're going to find her. And whoever took her is going to learn what
happens when you hunt the families of wolves."

*To Shadows:*

"We need to find out who Genesis Research is. And we need to do it quietly -
before they know we're coming.""""
        )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows nods, pocketing the card*

"I know people who can dig into corporate records. Off the books."

*She turns to the Theurge*

"Speaks-With-Spirits - keep trying to reach the local spirits. Whatever was
used to cloud them might fade with time. Any fragment of memory could help."

*To Elena:*

"Stay with family. Keep the children close. If anyone approaches you, anyone
at all, contact the sept immediately."

*She heads for the door*

"Storm - let's start with that phone number. Sometimes the simplest approach
yields results."

[Scene End - Investigation begins]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
