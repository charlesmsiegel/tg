"""
Dreams Made Flesh - Scene 1: The Escaped Chimera

A powerful chimera has crossed into the mortal world.

Characters: Rowan Brightwater, Jack "Patches" McGee
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of Dreams Made Flesh."""
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
        name="The Escaped Chimera",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 12, 5),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Escaped Chimera")
        return scene

    print("  Created Scene: The Escaped Chimera")

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
        message="""The Dreaming Roads are in an uproar.

Three nights ago, something escaped from the Far Dreaming - a chimera
of unusual power, old enough to remember when humans still believed
in magic without question. It broke through the barriers that separate
dream from reality and crossed into the waking world.

A chimera that powerful, loose in Seattle, is a crisis. Mortals will
see impossible things. The Banality of the modern world will try to
destroy it. And if it dies here, the psychic backlash could shatter
what remains of Seattle's already-weakened freeholds.

Someone has to find it. Someone has to bring it home."""
    )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan examines the breach point - a thin spot in the Dreaming
where the chimera forced its way through*

"Look at the damage. Whatever came through, it was big. Really big.
And desperate."

*She traces the residue of dream-stuff left behind*

/roll 6 6
(Perception + Kenning - identifying the chimera)

"The signature... this is old magic. Really old. I think this chimera
might predate the Shattering."

*She looks at Patches with concern*

"If something that ancient is running scared, what was it running FROM?""""
        )

    if patches:
        scene.add_post(
            character=patches,
            display="Jack 'Patches' McGee",
            message="""*Patches sniffs the air, his Pooka senses parsing the dreamstuff*

"I know this scent. Had a dream about it once - everybody does, when
they're little."

*His eyes widen*

/roll 5 6
(Intelligence + Greymayre - identifying the chimera)

"Rowan. This isn't just any chimera. This is a HOPE-BEARER. One of
the great chimera that embody children's belief in possibility."

*He looks almost reverential*

"They're supposed to be extinct. Killed in the Shattering when
belief died."

*His voice drops*

"If one survived... if it's here... we HAVE to save it. Something
like this is irreplaceable.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The trail leads from the breach point into mortal Seattle.
Witnesses (most of them children, with imaginations still open enough
to see) report strange sightings:

A great winged lion glimpsed in the fog.
A creature of pure light dancing through traffic.
A beast made of rainbow and laughter.

The chimera is frightened, disoriented, its form shifting as it
tries to find stable belief to anchor itself. In the Far Dreaming,
belief was abundant. Here, it's starving.

And the Banality of Seattle is beginning to notice the intrusion.

Cold patches spreading through neighborhoods. Dreams turning grey.
The city itself rejecting the presence of something too magical to
exist in the modern world."""
    )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan follows the trail, moving between Dreaming and reality*

"It's heading toward the waterfront. Probably drawn by the remnants
of maritime folklore - sailors always had wild imaginations."

*She pauses, sensing something wrong*

/roll 5 6
(Perception + Awareness - detecting threat)

"We're not the only ones tracking it. Something else is following
the trail. Something that feels like..."

*Her expression darkens*

"Autumn Court hunters. They must want the chimera too - probably to
bind it, use its power."

*She looks at Patches*

"We need to find it first. Can you get ahead of them?""""
        )

    if patches:
        scene.add_post(
            character=patches,
            display="Jack 'Patches' McGee",
            message="""*Patches grins - his first real grin since they started the hunt*

"Ahead of them? I can CONFUSE them. Pooka speciality."

*He starts laying false trails - dream-scent that leads nowhere,
confusing loops of chimeric residue*

/roll 6 6
(Manipulation + Subterfuge - creating diversions)

"Give me ten minutes. The Autumn hunters will be chasing their
own tails."

*He pauses before vanishing into the Dreaming*

"Rowan. When we find this thing... how do we convince it to come
back? It ran from the Far Dreaming for a reason. What if it doesn't
WANT to go home?"

[Scene End - Hunt for the chimera begins]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
