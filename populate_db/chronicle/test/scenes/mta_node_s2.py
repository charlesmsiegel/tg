"""
The Contested Node - Scene 2: Complications

More factions arrive to contest the node, and tensions escalate.

Characters: Elena Vasquez, James Chen
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of The Contested Node."""
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
        name="Complications",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 7, 14),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Complications")
        return scene

    print("  Created Scene: Complications")

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
        message="""Two days of uneasy standoff. The Hermetics have erected a ritual
circle at the chamber's north end. Elena and James maintain their own
ward to the south. Neither side sleeps much; neither side trusts the other.

The pool continues to pulse with Quintessence, indifferent to the politics
playing out around it.

Then the Technocracy arrives.

Not through the tunnels - they simply appear, stepping out of nothing as
their dimensional science folds space. Four figures in black tactical gear,
faces hidden behind mirrored visors. New World Order, by their bearing.
And with them: something worse.

A HIT Mark. Chrome and carbon fiber and calculated lethality."""
    )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena's protective wards flare as she spins to face the new threat*

"Technocracy. How did they-"

*She answers her own question*

"The seal failing. They've been monitoring for dimensional anomalies."

*She doesn't drop her guard toward the Hermetics, but her attention is
firmly on the greater threat*

/roll 6 6
(Wits + Alertness - tactical assessment)

"We're outnumbered. Outgunned. And that HIT Mark..."

*Her voice drops*

"James. If this goes bad, grab what you can from the node and run. Someone
has to warn the Chantry.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The lead NWO agent removes his visor. His face is bland, forgettable,
designed that way.

"Designation: Agent Marcus. Iteration X and New World Order joint task force.
This Reality Deviant nexus point has been flagged for containment."

His voice is flat. No emotion. No negotiation.

"You will surrender custody of the anomalous zone. Resistance will be met
with appropriate force."

The HIT Mark's arm reconfigures, revealing a weapon that shouldn't exist in
Sleeper reality.

The Hermetics, for their part, have gone very still. Ancient enemies unite
when faced with extinction."""
    )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James's fingers fly across his tablet, but he's not running
calculations - he's preparing countermeasures*

"Agent Marcus. Let me explain something about this 'anomalous zone.'"

*He steps forward, projecting confidence he doesn't feel*

/roll 5 7
(Manipulation + Subterfuge - stalling)

"That node has been sealed for centuries. Sealed by something that predates
your Technocratic Union, predates the Order of Reason, predates human
civilization. Whatever's down there isn't just Quintessence."

*He gestures at the pool*

"You want to 'contain' something that ancient powers thought was too
dangerous to use? Be my guest. But I'd recommend understanding what you're
dealing with first.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Agent Marcus's expression flickers - just for a moment, but it's there.
Uncertainty.

"Intelligence did not indicate..."

He touches his ear - receiving orders from somewhere.

"Acknowledged. Revision: Subject the anomaly to analysis before containment.
Tradition mages will-"

The pool erupts.

Light explodes from its surface - not the gentle glow of Quintessence, but
something raw and primal. The water rises, takes shape. A figure of living
light, ancient and vast and terrible.

It speaks, and its voice resonates in the Avatars of every mage present:

"CHILDREN OF EARTH. YOU HAVE BROKEN THE SEAL. NOW FACE WHAT LIES WITHIN."

The HIT Mark opens fire. The bullets pass through the light-figure like it
isn't there.

Because for something this old, human weapons are beneath notice."""
    )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena throws herself backward, pulling James with her*

"It's a spirit! Something bound to the node - maybe the reason it was sealed!"

/roll 6 7
(Intelligence + Spirit - understanding the entity)

*The light-figure turns toward the Technocrats. Something like contempt
crosses its luminous features*

"MACHINES. SOULLESS THINGS. YOU DARE TRESPASS IN THE DREAMING WATERS?"

*Elena shouts to the Hermetics*

"We need to work together! Whatever this is, none of us can face it alone!"

#WP

*She begins weaving a containment pattern, hoping the Hermetics will join
their power to hers*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The lead Hermetic - the silver-haired woman - meets Elena's eyes.
A century of inter-Tradition politics weighs against the thing rising from
the pool.

Politics loses.

"Bonisagus pattern, tertiary configuration!" she shouts to her companions.
"Link with the Verbena's weave!"

The three Hermetics begin their own ritual, their power joining Elena's.
Ancient Latin harmonizes with older words of power.

The Technocrats are retreating, dragging their damaged HIT Mark. They'll be
back with reinforcements. But for now, this is a Tradition problem.

The light-figure howls as the containment takes hold. Not defeated - not
even close - but constrained. Buying time.

"YOU CANNOT HOLD ME FOREVER, CHILDREN. THE SEAL IS BROKEN. I WILL BE FREE."

[Scene End - Spirit partially contained, temporary alliance formed]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
