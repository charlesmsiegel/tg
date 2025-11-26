"""
Whispers from the Void - Scene 2: Reinforcing the Shroud

The wraiths work to strengthen the barrier at Harborview.

Characters: Margaret "Peggy" Sullivan, Thomas Ashworth
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of Whispers from the Void."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        peggy = CharacterModel.objects.get(name='Margaret "Peggy" Sullivan')
    except CharacterModel.DoesNotExist:
        peggy = None

    try:
        thomas = CharacterModel.objects.get(name="Thomas Ashworth")
    except CharacterModel.DoesNotExist:
        thomas = None

    scene, created = Scene.objects.get_or_create(
        name="Reinforcing the Shroud",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 9, 2),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Reinforcing the Shroud")
        return scene

    print("  Created Scene: Reinforcing the Shroud")

    if peggy:
        scene.add_character(peggy)
    if thomas:
        scene.add_character(thomas)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Harborview Medical Center. In the living world, it's a beacon of
healing - trauma surgeons saving lives, nurses comforting the dying.

In the Shadowlands, it's a haunted place. The hospital's history is
written in ghost-blood: the fire of 1987 that killed dozens, the
daily deaths that accumulate like sediment, the despair of families
who lost loved ones.

Margaret Sullivan died here. The memory of smoke still lingers in
her corpus.

The Shroud here is paper-thin. And even now, she can feel it weakening
further."""
    )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy stands in the Shadowlands version of the hospital lobby,
feeling the weight of all its deaths*

"I can sense them. The Spectres. They're probing the barrier. Testing
for weaknesses."

*She extends her awareness through the building*

/roll 6 6
(Perception + Awareness - mapping the Shroud's weak points)

"Three critical points. The old burn ward - where I died. The morgue.
And the pediatric ICU."

*Her voice cracks slightly on the last*

"Children. They always target children."

*She steadies herself*

"We need to shore up all three before the assault begins.""""
        )

    if thomas:
        scene.add_post(
            character=thomas,
            display="Thomas Ashworth",
            message="""*Thomas surveys the space with a strategist's eye*

"The morgue I can handle. My Masquers have experience with places
of death. We can weave protections that will hold for at least a
few days."

*He looks toward the upper floors*

"The burn ward and the ICU are more challenging. They're not just
thin spots - they're WOUNDS. Old pain keeping them open."

/roll 5 6
(Intelligence + Occult - analyzing the weak points)

"We don't just need to reinforce the Shroud. We need to address
the underlying trauma. Somehow."

*He glances at Peggy*

"The burn ward is your domain. You're connected to it. Can you
face going back?""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The question hangs in the air. For wraiths, returning to the site
of their death is always painful. The memories surge up, overwhelming
and raw, threatening to pull them toward their own Shadow's darkness.

But Margaret has faced her death before. The fire. The smoke. The
screams of patients she couldn't save.

To strengthen the Shroud there, she'll have to relive all of it.

Elsewhere in the hospital, other wraiths gather. Thomas's Masquer
allies, a few Hierarchy soldiers, some Renegades who've put aside
their differences for the emergency. Not many - most wraiths fled
when they sensed what was coming.

They'll have to be enough."""
    )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy closes her eyes, centering herself*

"I can face it. I have to."

*She looks at Thomas*

"The pediatric ICU - do we have anyone who can work that site? It
needs someone who understands that kind of grief."

/roll 4 7
(Wits + Empathy - identifying the right person)

*A thought strikes her*

"Maria. The young mother who died in labor last year. She hasn't
moved on - she's still tied to the hospital, watching over sick
children."

*Her voice softens*

"It will hurt her. But she might be the only one who can seal
that wound."

*She starts toward the stairs*

"Let's begin. Every minute we wait, the Spectres grow stronger.""""
        )

    if thomas:
        scene.add_post(
            character=thomas,
            display="Thomas Ashworth",
            message="""*Thomas nods, already moving toward the morgue*

"I'll send word to Maria. And I'll make sure the morgue is secured
before I come to back you up."

*He pauses at the threshold between wings*

"Margaret. What you're about to do - walking back into your death -
your Shadow will try to use it against you. Don't let it win."

/roll 5 6
(Manipulation + Empathy - offering support)

*His usual aristocratic detachment softens*

"You're one of the few who remember why we fight. What happens to
the living matters. Don't let Oblivion convince you otherwise."

*He straightens*

"I'll be there as soon as I can. Hold the line."

*He vanishes into the morgue's darkness*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Alone, Peggy climbs the stairs to the fourth floor. The burn ward.

Even after decades, she can smell phantom smoke. The walls here
remember flame. The Shroud is so thin she can see the living world
bleeding through - doctors making rounds, patients sleeping fitfully.

And on the other side of the Shroud, pressing against it, she sees
the first Spectres.

A dozen of them, at least. Twisted things, their features erased by
Oblivion. They haven't broken through yet, but they're close. So close.

Her Shadow stirs.

*"Why fight it? You couldn't save them then. You can't save them now.
Let the fire take them all."*

Peggy pushes the voice down and begins her work.

[Scene End - Shroud reinforcement begins]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
