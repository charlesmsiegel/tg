"""
The Gray Tide - Scene 3: The Factory

The changelings discover the source of the manufactured Banality.

Characters: Rowan Brightwater, Jack "Patches" McGee
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of The Gray Tide."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        rowan = CharacterModel.objects.get(name="Rowan Brightwater")
    except CharacterModel.DoesNotExist:
        rowan = None

    try:
        patches = CharacterModel.objects.get(name='Jack "Patches" McGee')
    except CharacterModel.DoesNotExist:
        patches = None

    scene, created = Scene.objects.get_or_create(
        name="The Factory",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 11, 8),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Factory")
        return scene

    print("  Created Scene: The Factory")

    if rowan:
        scene.add_character(rowan)
    if patches:
        scene.add_character(patches)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The industrial district. A warehouse that, according to records,
has been abandoned for a decade. But the trail led here - the Dauntain
vessel, the manufactured Banality, all of it traced back to this
nondescript building.

In the Dreaming, it's far more ominous. The warehouse is a VOID - a
hole in the fabric of imagination, radiating waves of soul-crushing
emptiness.

Rowan and Patches approach carefully. Whatever's inside is powerful
enough to drain Glamour from miles away. Getting too close could be
fatal for any changeling."""
    )

    if patches:
        scene.add_post(
            character=patches,
            display="Jack 'Patches' McGee",
            message="""*Patches crouches behind a dumpster, his usually colorful coat
seeming to dim in the Banality field*

"I've seen some bad things. Autumn Nightmares, Thallain, that time
I accidentally wandered into an IRS office. But this..."

*He shudders*

/roll 5 7
(Perception + Stealth - scouting the area)

"Guards. Mortal, but... wrong. See how they move? Too precise. Too
regular. Like they've had all the creativity beaten out of them."

*He looks at Rowan*

"Whatever's happening in there, it's not just producing Banality.
It's producing Dauntain. Factory-made enemies of the Dreaming.""""
        )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan's wings have almost completely faded this close to the
source. She can feel her own Glamour being pulled toward the building*

"We can't stay here long. Every minute costs us."

*She studies the building's layout*

/roll 6 6
(Intelligence + Investigation - finding a way in)

"There - a ventilation shaft on the roof. The Banality is strongest
at ground level, pooling like fog. If we come in from above..."

*She summons what Glamour she can*

#WP

"Patches. Whatever we find in there, we document everything. The
court needs to know who's doing this and how."

*She starts climbing*

"And if we get the chance, we burn it to the ground.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Inside, the warehouse is a nightmare of industrial precision.

Assembly lines stretch the length of the building, but they're not
making products. They're making EMPTINESS. Glamour - harvested from
who knows where - flows into machines that strip away everything
that makes it magical, leaving only concentrated Banality.

Workers move through the facility like automatons. Once-colorful
souls, now gray and hollow. Not quite Dauntain yet, but getting
there. The process is... gradual.

And at the center of it all, overseeing the operation: a figure
in a crisp business suit, reviewing efficiency reports on a tablet.

A Sidhe. Or what used to be one.

His eyes are chrome, reflecting no light. His voice, when he speaks
to an underling, carries no emotion whatsoever.

"Production is at 87% capacity. Increase the Glamour intake by 15%.
We have quotas to meet.""""
    )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan recognizes the figure and nearly gasps aloud*

"Lord Ashenveil. He was Seelie Court, fifty years ago. Everyone
thought he died in the Accordance War."

*Her horror deepens*

/roll 5 6
(Intelligence + Occult - understanding the operation)

"He didn't die. He... gave himself to Banality completely. And now
he's trying to make others like him."

*She looks at the assembly lines, the drained workers, the machinery
of despair*

"This isn't just an attack on Seattle's freeholds. It's the beginning
of a purge. If he can manufacture Banality at this scale..."

*Her voice hardens*

"We have to stop him. Tonight.""""
        )

    if patches:
        scene.add_post(
            character=patches,
            display="Jack 'Patches' McGee",
            message="""*Patches is already moving, planting chimerical seeds of chaos
throughout the facility*

"Way ahead of you. I've been seeding disruption since we got here."

/roll 6 6
(Dexterity + Stealth - sabotage)

*He triggers the first seed. A machine sparks and begins producing
rainbow-colored bubbles instead of Banality*

"Pooka trick. Inject enough imagination into a system, and it
starts to malfunction."

*More seeds activate. Chaos spreads*

"We've got maybe five minutes before Chrome-eyes over there realizes
what's happening. Make them count!"

*He draws his chimeric blade*

"Time to remind this bastard what it felt like to dream!""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Alarms sound. Lord Ashenveil looks up from his tablet, chrome eyes
scanning the facility. When he spots Rowan and Patches, there's no
surprise - just cold calculation.

"Changelings. Predicted probability: 73%. Response protocol: engage."

He raises a hand. The drained workers turn as one, moving toward the
intruders with mechanical precision.

But Patches' chaos is spreading faster than Ashenveil anticipated.
Machines explode into color. Workers blink, confused, as fragments
of imagination pierce their gray existence.

The factory is failing. And Ashenveil knows it.

"Facility compromised. Initiating purge protocol."

His other hand moves toward a control panel. Whatever "purge protocol"
means, it can't be good.

[Scene End - Factory sabotaged, confrontation with Ashenveil imminent]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
