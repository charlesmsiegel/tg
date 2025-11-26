"""
Blood Calls to Blood - Scene 2: Following the Trail

The pack investigates Genesis Research and discovers a horrifying truth.

Characters: Runs-Through-Shadows, Storm's Fury
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of Blood Calls to Blood."""
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
        name="Following the Trail",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 6, 17),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Following the Trail")
        return scene

    print("  Created Scene: Following the Trail")

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
        message="""A dingy office in the industrial district. Fluorescent lights hum
overhead. A Glass Walker kinfolk named Kyle works at a computer station
surrounded by multiple monitors.

Kyle is good at finding things that don't want to be found. He's been
digging into Genesis Research for two days straight.

The expression on his face says he found something - and he wishes he
hadn't."""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows enters, immediately picking up on Kyle's distress*

"What did you find?"

*She moves to look at the screens*

"Kyle - what is Genesis Research?"

/roll 5 6
(Intelligence + Computer - understanding the data)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Kyle's voice is hollow. "Genesis Research doesn't exist. Not officially.
It's a shell - layers of holding companies, offshore accounts, buried under
enough paperwork to hide a small country."

He pulls up documents. "But I found patterns. Purchases of medical equipment.
Genetic testing supplies. And properties - isolated properties, bought through
different shells but all connected."

He takes a breath. "Then I found this."

He shows a file - personnel records from a defunct biotech firm. One name is
highlighted: Dr. Viktor Aldrich. His previous employer: Magadon Pharmaceuticals.

"Magadon is a Pentex subsidiary.""""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm's growl is barely human*

"Pentex. Again. Always Pentex."

*He leans over Kyle's shoulder*

"These properties - where are they? If they're holding Maria..."

*His claws have partially extended without his realizing it*

"Show me everything. Every location. Every name. Everyone involved in this."

/roll 4 7
(Intelligence + Investigation - analyzing the data)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Kyle pulls up a map. Red dots mark properties connected to Genesis
Research. Most are unremarkable - office buildings, storage facilities.

But one stands out: a former hospital in the industrial district, purchased
two years ago and listed as "under renovation." No permits have been filed.
No construction crews have been seen.

"There's something else," Kyle says. He shows them shipping manifests. "Genesis
has received multiple deliveries of laboratory equipment. Including..."

He swallows hard.

"Including equipment used for artificial insemination. And genetic manipulation."

The implications hang in the air like poison."""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows goes very still*

"They're not just collecting kinfolk. They're..."

*She can't finish the sentence*

*Her eyes find Storm's*

"Breeding. They're trying to breed Garou. Artificially."

*Her voice is barely a whisper*

"That's why they needed Maria. Why they needed to know her lineage. They're
selecting for the strongest bloodlines."

*Her hands are shaking*

"We need to get into that hospital. Tonight."

/roll 5 6
(Willpower - maintaining composure)"""
        )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm's transformation into Crinos is involuntary - pure rage
made manifest. The room shakes as his bulk expands*

*Kyle scrambles backward*

*Storm's voice is a snarl*

"They DARE. They think they can cage us? Breed us like animals?"

*He punches a wall, leaving a crater*

/roll 5 5
(Willpower - fighting frenzy)

#WP

*With tremendous effort, he forces himself back to Homid*

"Tonight. We free Maria and everyone else they've taken. And we burn that
place to the ground.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Kyle, still pressed against the far wall, manages to speak. "There's
one more thing. The hospital has security - serious security. Armed guards,
electronic surveillance, the works. And..."

He pulls up another file. "Heat signatures from a satellite pass. There are
people inside. At least twenty. Maybe more."

He looks at the two Garou.

"If Maria's in there, she's not alone. There are other kinfolk. Maybe other
Garou too. Whatever's happening in there, it's been going on for a while.""""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows regains her composure, though her eyes burn*

"Then we don't go in blind. We scout. We plan. And we bring everyone we can
trust."

*She turns to Storm*

"This is bigger than one rescue mission. If Pentex is breeding Garou - or
trying to - this is a threat to every sept in the nation. We need to know
everything before we act."

*She looks at the hospital schematic*

"Kyle - can you get us building plans? Security rotations? Anything?"

"And we need to contact the sept. This... this changes everything."

[Scene End - Horror discovered]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
