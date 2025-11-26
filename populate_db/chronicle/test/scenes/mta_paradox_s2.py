"""
When Reality Rebels - Scene 2: Into the Storm

The cabal enters the Paradox Realm to rescue the trapped Etherite.

Characters: Elena Vasquez, James Chen
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of When Reality Rebels."""
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
        name="Into the Storm",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 8, 5),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Into the Storm")
        return scene

    print("  Created Scene: Into the Storm")

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
        message="""There is no time for careful planning.

Elena finishes banishing the last Wrinkle just as the major Paradox spirit
breaches the rift. James throws everything he has into a desperate gambit -
not fighting the spirit, but riding its wake.

The world turns inside out.

They fall through the rift together, tumbling into a place that defies
description. The Paradox Realm. A bubble of unreality where nothing follows
consistent rules. Sky below, ground above, colors that have no names,
geometry that contradicts itself.

And at the center of it all: Michael, encased in crystallized possibility,
his screaming face frozen in the moment of his greatest failure."""
    )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena lands - or falls upward - or simply appears. The transition
is nauseating*

"James? JAMES!"

*She spots him tumbling through impossible space and reaches out with
her will, stabilizing his trajectory*

/roll 6 6
(Wits + Occult - navigating Paradox Realm)

*The realm fights her, but she's touched these spaces before in
her initiation rites*

"Don't try to understand it! Just accept it! The Realm responds to belief!"

*She forces herself to see ground beneath her feet, and suddenly there
IS ground*

"Find your center. Impose YOUR pattern on this place!""""
        )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James's tablet has become a Klein bottle. He stares at it,
forcing himself to accept the impossible*

"Pattern. Right. Pattern."

*He closes his eyes, visualizing order*

/roll 5 7
(Intelligence + Computer - imposing digital order)

*When he opens them, he's surrounded by a bubble of relative normalcy -
straight lines, consistent physics, familiar mathematics*

"That's... actually kind of cool."

*He looks toward the crystallized Etherite*

"Michael's the eye of the storm. His consciousness created this place
when his paradigm shattered. We need to reach him, convince him to
accept what happened."

*He starts walking - or his equivalent of walking in this place*

"Let's go save an idiot.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Realm shifts as they move through it. Sometimes they walk
on solid ground; sometimes they swim through liquid light; sometimes
they simply ARE in a new location without having traveled.

The crystal prison grows closer. Inside, Michael's face is twisted
in terror - stuck in the moment of his invention's catastrophic failure,
reliving it forever.

Paradox entities swirl around the crystal. Not attacking - feeding.
They draw sustenance from Michael's fear and guilt, and in return,
they sustain the Realm itself.

A symbiosis of suffering.

The major spirit that breached the rift is here too, circling like
a shark. It regards the newcomers with what might be hunger."""
    )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena reaches the crystal's edge. Up close, she can see layers
of memory embedded in it - Michael's past, his training, his hopes*

"He's not just trapped. He's BECOMING the Realm. If we don't pull him
out soon, he'll be absorbed completely."

*She places her hands on the crystal*

/roll 6 6
(Manipulation + Empathy - reaching Michael's mind)

"Michael. Michael, can you hear me? My name is Elena. I'm here to help."

*The crystal shudders*

"I know you're afraid. I know you think you've destroyed everything.
But the rift can be closed. The damage can be healed. You just have
to LET GO.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""A voice echoes from within the crystal - Michael's voice, distorted
by impossible acoustics.

"I... I killed them. My invention... I SAW it happen. The vampire, the
others, they were pulled in..."

His guilt is a physical force, pressing down on them.

"I can't let go. If I let go, I have to face what I did. I have to be
RESPONSIBLE."

The Paradox entities stir, agitated by the disturbance. The major
spirit moves closer, its crystalline mass grinding against itself
like breaking ice.

"You should leave. Before you're trapped too. Before I hurt anyone else.""""
        )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James pushes through the crystal's resistance to stand beside Elena*

"Michael, listen to me. I'm a Virtual Adept - I know about failed
experiments. I know about designs that don't work the way they should."

*He pulls up what's left of his tablet - now showing images that shouldn't
exist*

/roll 5 6
(Charisma + Expression - reaching out)

"You made a mistake. A big one. And yeah, people might have died. But
staying here, feeding this Realm - that's not penance. That's just
making it worse."

*He shows Michael images from outside - the rift, the entities
trying to break through*

"Every minute you stay frozen, that rift gets bigger. More entities
escape. More damage to reality. The best thing you can do for
everyone you hurt is COME BACK and help us fix it."

*His voice softens*

"You can hate yourself later. Right now, we need you functional.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The crystal cracks.

Michael's face moves - just slightly, but movement nonetheless.

"I... you're right. Hiding here doesn't help anyone."

The crack spreads. The Paradox entities scream - their food source
is slipping away.

"But I don't know how to get out. I don't know how to face..."

Elena and James feel the Realm beginning to collapse around them.
Without Michael's fear sustaining it, the Paradox energy is
dissipating. Which is good - except they're still inside.

The major spirit ROARS, charging toward them, desperate to consume
whatever energy it can before the Realm fails.

[Scene End - Realm collapsing, spirit attacking]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
