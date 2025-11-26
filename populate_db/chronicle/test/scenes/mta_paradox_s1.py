"""
When Reality Rebels - Scene 1: The Backlash

A vulgar spell goes catastrophically wrong, summoning a Paradox spirit.

Characters: Elena Vasquez, James Chen
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of When Reality Rebels."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        elena = CharacterModel.objects.get(name="Elena Vasquez")
    except CharacterModel.DoesNotExist:
        elena = None

    try:
        james = CharacterModel.objects.get(name="James Chen")
    except CharacterModel.DoesNotExist:
        james = None

    scene, created = Scene.objects.get_or_create(
        name="The Backlash",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 8, 5),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Backlash")
        return scene

    print("  Created Scene: The Backlash")

    if elena:
        scene.add_character(elena)
    if james:
        scene.add_character(james)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Seattle waterfront, 3 AM. A warehouse that serves as neutral
meeting ground for various supernatural factions. Tonight, a negotiation
between mages and a vampire representative was supposed to take place.

Instead, everything has gone wrong.

A young Etherite - barely out of apprenticeship - attempted to impress the
gathering with a demonstration of his Invention. A device meant to bend
light and shadow. Instead, he tore a hole in reality.

The Paradox backlash was immediate and catastrophic.

Elena and James arrived just in time to see the warehouse implode into a
sphere of twisted space. The Etherite is gone - either dead or pulled into
the resulting Paradox Realm. The vampire representative fled. And something
is emerging from the wound in the world."""
    )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena throws up a protective ward as reality screams around them*

"Paradox spirit! A big one - the backlash must have been enormous!"

*She can see it now - a thing of angles and impossibilities, a living
contradiction that hurts to look at*

/roll 5 7
(Perception + Occult - analyzing the spirit)

"It's... it's not just one. The tear is still open. More are coming!"

*She grabs James's arm*

"We have to close that rift before the whole waterfront becomes a
Paradox Realm!""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The first Paradox spirit fully manifests. It's called a Wrinkle - a
minor entity, but vicious. Its form constantly shifts, never quite settling
into any recognizable shape.

Behind it, the rift pulses. You can see other things moving in the space
between spaces - larger shapes, hungrier shapes.

The warehouse district is mostly empty at this hour, but there are still
Sleepers nearby. Night workers, homeless people seeking shelter, security
guards. If the Paradox spreads...

Reality itself seems to shimmer around the rift. Cause and effect are
becoming unreliable."""
    )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James is already working, his tablet running calculations at
impossible speed*

"The rift is unstable. That's actually good news - it wants to close. The
Paradox is fighting to restore normalcy."

*He dodges as the Wrinkle lunges toward him*

/roll 6 6
(Dexterity + Athletics - evading the spirit)

"Bad news: something on the other side is holding it open. Something that
wants OUT."

*He shows Elena his readings*

"We need to destabilize whatever's anchoring the rift. If we can break
its hold, reality should snap back like a rubber band."

*He looks at the tear*

"Of course, we'll have to go through the Wrinkles to do it.""""
        )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena begins weaving a pattern - careful, coincidental magic,
nothing that will feed the Paradox further*

"I can banish the Wrinkles, but it'll take time. Can you keep them off
me while I work?"

/roll 5 6
(Intelligence + Occult - preparing banishment)

*The air around her hands shimmers with subtle power*

"And James - whatever's holding that rift open, we're going to need to
deal with it together. I don't care how good your calculations are,
you're not facing a Paradox anchor alone."

*She begins the chant, old words that predate language*

#WP

"Cover me!""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Three more Wrinkles emerge from the rift. They move in ways that
make the eyes water - too fast, too slow, in directions that shouldn't
exist.

Elena's banishment takes hold on the first one. It screams - a sound
like breaking glass - and dissolves back into raw Paradox energy.

But the rift pulses wider.

Through it, you can see the anchor now: a massive shape, like a
crystallized scream made solid. A major Paradox spirit - perhaps even
a Marauder caught between worlds. It's using the rift as a doorway,
trying to pull itself through into consensus reality.

If it succeeds, the resulting Paradox storm could rewrite Seattle."""
    )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James puts himself between Elena and the Wrinkles, technology
and will his only shields*

"I see it! The anchor - it's not just a spirit, it's a PATTERN. Someone -
the Etherite, maybe - their belief is feeding it!"

*He parries a Wrinkle with a force-field barely conjured in time*

/roll 5 6
(Wits + Technology - defensive improvisation)

"If Michael's still alive in there, his fear and confusion are sustaining
the rift. We don't just need to close it - we need to reach him!"

*He shouts over the chaos*

"Elena! Can you project into the Realm? Pull him back?""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Another Wrinkle falls to Elena's banishment. But the major spirit
is almost through now - a crystalline mass of fractured reality, each
facet reflecting a different impossible world.

And within it, barely visible: a human shape. Michael, the young Etherite,
trapped in his own Paradox backlash. Alive, but his consciousness is
what's anchoring the whole catastrophe.

The last Wrinkle charges James. The major spirit reaches one massive
limb through the rift.

The next few moments will determine whether Seattle remains part of
consensus reality.

[Scene End - Major Paradox spirit emerging]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
