"""
The Silent Cell - Scene 2: Western State

The hunters enter the abandoned hospital.

Characters: Sarah Mitchell, David Okonkwo
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of The Silent Cell."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        sarah = CharacterModel.objects.get(name="Sarah Mitchell")
    except CharacterModel.DoesNotExist:
        sarah = None

    try:
        david = CharacterModel.objects.get(name="David Okonkwo")
    except CharacterModel.DoesNotExist:
        david = None

    scene, created = Scene.objects.get_or_create(
        name="Western State",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 8, 17),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Western State")
        return scene

    print("  Created Scene: Western State")

    if sarah:
        scene.add_character(sarah)
    if david:
        scene.add_character(david)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Western State Hospital. High noon, sun blazing overhead.

The abandoned buildings sprawl across the grounds like a
wound in the landscape. Victorian architecture gone to rot,
windows dark and empty, walls covered in graffiti from
decades of urban explorers who didn't know what they were
walking into.

Even in daylight, Sarah's Second Sight shows the place crawling
with spiritual residue. Death has soaked into every brick. The
air itself feels wrong - too cold, too still, like the world
is holding its breath.

The main building looms ahead. Whatever took Sigma Cell is in there."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah approaches the main entrance, iron knife in hand*

"My Sight's going haywire. There's... so many of them. Hundreds of
spiritual impressions, all layered on top of each other."

*She pushes through the front doors*

/roll 6 6
(Perception + Awareness - reading the spiritual landscape)

"But there's a pattern. The ghosts are all facing the same direction.
Pointing toward..."

*She looks deeper into the building*

"The old therapy wing. Whatever's commanding them is there."

*She circles salt around the entrance*

"That'll keep our exit clear. Let's move.""""
        )

    if david:
        scene.add_post(
            character=david,
            display="David Okonkwo",
            message="""*David follows, EMF detector crackling*

"Readings are off the scale. This isn't normal haunting - there's
too much energy concentrated in one place."

*He sweeps the detector*

/roll 5 6
(Intelligence + Occult - analyzing the energy patterns)

"I'm getting three distinct heat signatures on thermal. Human-sized.
They're not moving, but they're warm."

*He checks coordinates*

"Second floor, east wing. That's where Sigma Cell is - or what's
left of them."

*He primes his shotgun with salt rounds*

"Let's hope they're still breathing.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The hospital interior is a nightmare of peeling paint and rotting
furniture. Old patient records litter the floors - names, diagnoses,
treatments that would be crimes by modern standards.

And the ghosts.

They're everywhere. Flickering at the edges of vision. Watching from
doorways. Whispering in voices too faint to hear clearly. Not attacking -
not yet. But present. Aware.

A message scratched into a wall, fresh enough to be recent:

"THEY WON'T LET US LEAVE. HE WANTS WHAT WE HAVE."

Sigma Cell's handwriting. They survived long enough to leave a warning."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah photographs the message*

"'He wants what we have.' Their Sight? Their abilities? Someone's
interested in what makes hunters different."

*She hears a sound above - footsteps, deliberate and slow*

/roll 5 7
(Wits + Alertness - detecting approach)

"Contact. Second floor, moving toward the east wing."

*She signals David to cover her*

"It knows we're here. It's herding us, same as Sigma Cell."

*She starts climbing the stairs*

"Only one way to find out what 'he' is. Let's go say hello.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The second floor is worse. The spiritual pressure is almost
physically painful - a weight on the chest, a ringing in the ears.
The ghosts here are more solid, more present.

And they're blocking the path everywhere except the east wing.

The trap is obvious. They're walking into it anyway.

Because in the therapy room at the end of the hall, three figures
slump in chairs. Marcus, Yuki, Father Brennan. Alive - barely.
Catatonic. Their eyes are open but seeing nothing.

And standing behind them, a figure in a white coat that was once
a doctor's garb, now stained with a century of death.

"More visitors," it says, and its voice echoes with a thousand
stolen screams. "More gifts for my collection."

[Scene End - Sigma Cell found, enemy revealed]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
