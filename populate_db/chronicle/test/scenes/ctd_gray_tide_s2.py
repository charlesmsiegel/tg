"""
The Gray Tide - Scene 2: Court Politics

The changelings bring their problem to the local court.

Characters: Rowan Brightwater, Jack "Patches" McGee
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of The Gray Tide."""
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
        name="Court Politics",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 11, 3),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Court Politics")
        return scene

    print("  Created Scene: Court Politics")

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
        message="""The Court of the Silver Rain, Seattle's primary Seelie court. In
the Dreaming, it manifests as a great hall of living silver, rain
forever falling outside the windows yet never quite reaching the ground.

Duke Silvermist presides from a throne of crystallized moonlight. Around
him, nobles of both Seelie and Unseelie courts have gathered. The
attack on the freeholds has gotten everyone's attention.

But attention doesn't mean agreement. Court politics rarely does."""
    )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan stands before the assembly, still wearing the exhaustion
of the Gilded Pumpkin's decline*

"Your Grace, honored nobles. I come with dire news."

*She projects images of the fading freeholds into the air - a
Primal-fueled display*

/roll 6 6
(Charisma + Politics - addressing the court)

"Four freeholds, attacked simultaneously. Coordinated Dauntain
assault, using vessels to channel focused Banality. This isn't
random - it's warfare."

*She lets the images fade*

"If we don't act, Seattle will lose all its freeholds within a month.
And without freeholds, where will ANY of us gather Glamour?""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The court murmurs. Some look concerned; others skeptical.

Baron Thornwick, an Unseelie Sidhe known for his pragmatism, speaks
first: "Disturbing claims, Lady Brightwater. But you speak of
'coordinated attack' and 'warfare.' Who is the enemy? Random Dauntain
don't organize."

Countess Moonwhisper, Seelie but famously cautious, adds: "And what
proof do we have beyond fading freeholds? Glamour ebbs and flows.
Perhaps this is a natural cycle."

Duke Silvermist says nothing, watching. Judging."""
    )

    if patches:
        scene.add_post(
            character=patches,
            display="Jack 'Patches' McGee",
            message="""*Patches steps forward, less comfortable with court formality but
unwilling to stay silent*

"Natural cycle? I've SEEN the woman they sent. The Dauntain."

*He reaches into his coat and produces something - a shard of gray
nothing, captured in chimerical glass*

/roll 5 6
(Manipulation + Expression - making his point)

"This is what she left behind when she touched the freehold's
threshold. Pure, concentrated Banality. I've been a Pooka for
fifty years - I've never seen anything like it."

*He holds it up for the court to see*

"Someone MADE this. Someone is manufacturing weapons against us.
If you want proof, there it is.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The shard passes among the nobles. Each one who touches it shudders,
feeling the cold emptiness within.

Baron Thornwick's expression hardens. "Manufactured Banality. This
changes things."

Countess Moonwhisper examines the shard with growing horror. "The
resonance... this wasn't made by Dauntain alone. There's mortal
technology involved. Mortal science."

Duke Silvermist finally speaks, his voice like silver bells:
"Someone has found a way to industrialize the destruction of dreams.
This is no longer a matter for debate."

He rises from his throne.

"I am calling a Quest. Find the source of this manufactured Banality.
Find who commands these Dauntain. And end them, by whatever means
necessary.""""
    )

    if rowan:
        scene.add_post(
            character=rowan,
            display="Rowan Brightwater",
            message="""*Rowan bows, relief and determination mixing on her face*

"Thank you, Your Grace. We accept the Quest."

*She turns to Patches*

/roll 5 6
(Intelligence + Investigation - planning the quest)

"The Dauntain vessel - she was examining vintage toys at the store.
That's our starting point. Who hired her? Where did she come from?"

*To the court:*

"We'll need access to the Dreaming Roads, and permission to operate
in both Seelie and Unseelie territories. This enemy doesn't care
about our courts - we can't afford to either."

*The Duke nods*

"Granted. May the Dreaming guide your path."

[Scene End - Quest granted by the Duke]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
