"""
When Reality Rebels - Scene 3: Restoration

The cabal escapes the collapsing Realm and seals the rift.

Characters: Elena Vasquez, James Chen
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of When Reality Rebels."""
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
        name="Restoration",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 8, 5),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Restoration")
        return scene

    print("  Created Scene: Restoration")

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
        message="""The Paradox Realm is dying.

Walls of unreality fold in on themselves. The ground - such as it was -
dissolves into static. The sky screams.

And the major Paradox spirit, denied its anchor, lashes out in fury.

Crystalline limbs sweep toward the three mages - Elena, James, and
Michael, newly freed but barely conscious. They have seconds to escape
before the collapsing Realm drags them into oblivion."""
    )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena grabs Michael's arm, pulling him between her and James*

"The rift! It's our only way out - we have to reach it before the
Realm closes!"

*The spirit blocks their path, a mountain of rage*

/roll 6 7
(Wits + Athletics - finding a path)

*She sees it - a gap in the spirit's defense, a moment of hesitation
as it tries to feed on the dissolving Realm*

"NOW! Move!"

*She throws herself forward, dragging Michael with her*

#WP

"James! The spirit! Give us an opening!""""
        )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James turns to face the spirit. It's massive. Ancient. Inevitable.*

*He grins.*

"Hey, ugly."

*His tablet - what's left of it - pulses with light*

/roll 6 6
(Intelligence + Technology - desperate innovation)

"You want pattern? You want ORDER? HERE."

*He uploads everything - every calculation, every formula, every rigid
structure of mathematics and logic his mind can produce*

*The spirit SCREAMS as pure order floods its system, contradicting its
chaotic nature*

"GO! I'm right behind you!"

*He runs, the spirit thrashing in confusion behind him*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""They reach the rift just as it begins to close.

The passage is agony - their bodies and minds stretched across dimensions,
reality trying to decide if they belong in the collapsing Realm or in
the consensus world.

Then they're through.

The Seattle waterfront. 4 AM. The warehouse is gone, replaced by a
shallow crater. But the rift is shrinking, sealing itself as Michael's
consciousness returns to his body.

The Paradox spirit reaches one limb through - and the rift snaps shut,
severing it. The amputated limb dissolves into nothing.

Reality reasserts itself with an almost audible sigh of relief."""
    )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena collapses to her knees, exhaustion hitting all at once*

*Michael lies beside her, breathing but unconscious*

"He's alive. We did it."

*She looks at the crater where the warehouse used to be*

/roll 4 6
(Perception + Awareness - checking for residual Paradox)

"The residue is already fading. Reality remembers what this place was
supposed to be. By morning, the Sleepers will fill in the gaps - gas
leak, structural collapse, something mundane."

*She laughs weakly*

"We should not have survived that.""""
        )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James sits heavily next to Elena. His tablet is slag*

"My poor tablet. We've been through so much together."

*He looks at the unconscious Etherite*

"What happens to him? He caused... a lot of damage. Even if it was
an accident."

*He's not asking to be cruel - just realistic*

/roll 4 6
(Intelligence + Occult - assessing consequences)

"The Traditions are going to want answers. So is whatever faction
that vampire represented. This isn't over."

*He sighs*

"But that's tomorrow's problem. Right now..."

*He lies back on the pavement*

"Right now I'm just going to appreciate being made of consistent
matter.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The first light of dawn touches the Seattle skyline.

Michael stirs, groaning. His eyes open, clear for the first time since
his invention failed. Memory returns in a rush - the Realm, the spirits,
the rescue.

"You came for me," he whispers. "I would have died in there. Or worse."

Elena and James exchange looks. There will be consequences - there
always are. The Technocracy has certainly recorded the event. The
vampire court will want explanations. The Traditions will need to
discuss what almost happened.

But those are problems for later.

For now, three mages watch the sunrise, alive against all odds.

[Scene End - Rift sealed, Michael rescued]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
