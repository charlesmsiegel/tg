"""
Whispers from the Void - Scene 3: The Assault

The Spectres attack and the wraiths must hold the line.

Characters: Margaret "Peggy" Sullivan, Thomas Ashworth
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of Whispers from the Void."""
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
        name="The Assault",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 9, 3),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Assault")
        return scene

    print("  Created Scene: The Assault")

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
        message="""The Tempest SCREAMS.

The assault begins at midnight - the hour when the Shroud is weakest,
when the living world sleeps and dreams make the barrier thin.

Spectres pour out of the storm-winds, hundreds of them, a tide of
Oblivion given form. They crash against the hospital's defenses like
waves against a failing seawall.

Peggy is in the burn ward, her reinforcements barely complete. Thomas
guards the morgue. Maria, the young mother, weeps in the pediatric ICU
as she channels her grief into protection.

It's not enough. Nothing could be enough against this.

But they fight anyway."""
    )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*The first Spectre breaks through the ward's protections. Then
a second. A third*

"NO!"

*Peggy draws on her Pathos - the emotional energy that sustains wraiths -
and channels it into Castigate, the art of attacking the Shadow*

/roll 7 6
(Castigate - fighting the Spectres)

*The lead Spectre shrieks as its Shadow is torn apart*

"This is MY death! MY memory! You do not get to corrupt it!"

*More are coming. So many more*

#WP

*She screams back at them, her voice echoing with the pain of every
patient who died in this ward*

"I COULDN'T SAVE THEM THEN! BUT I CAN SAVE THE ONES THEY LEFT BEHIND!""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Spectres recoil from Peggy's fury. For a moment, the line
holds.

Then something larger emerges from the Tempest.

A Nephwrack. A greater Spectre, one who was once a powerful wraith
before falling completely to Oblivion. It has no face - just a
void where features should be, and a voice like grinding bone.

"LITTLE HEALER. YOUR DEFIANCE IS... ADMIRABLE. BUT FUTILE."

It gestures, and a dozen Spectres surge forward as one."""
    )

    if thomas:
        scene.add_post(
            character=thomas,
            display="Thomas Ashworth",
            message="""*Thomas fights his way up from the morgue, leaving a trail of
dissipated Spectres behind him*

*He bursts into the burn ward just as the Nephwrack advances on Peggy*

"Margaret! Get down!"

*He throws a Moliate attack - reshaping the Shadowlands matter around
the greater Spectre*

/roll 6 7
(Moliate - restraining the Nephwrack)

*Spectral chains wrap around the creature's limbs*

"How long can we hold?"

*He already knows the answer. Not long enough*

"The Hierarchy reinforcements - where ARE they?""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Nephwrack tears through Thomas's chains like paper. But the
delay bought precious seconds.

Below, the morgue falls. The Spectres pour through, spreading into
the hospital's lower levels.

Above, Maria's voice rises in a mother's protective scream as the
pediatric ICU comes under assault.

The hospital's living patients stir in their sleep, disturbed by
nightmares they can't explain. Some of them won't wake up.

And still no reinforcements.

The Hierarchy has abandoned them."""
    )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy feels the morgue fall. Feels the breach widen*

"Thomas. We need to fall back. Concentrate our strength."

*She hates the words even as she says them*

/roll 5 6
(Wits + Leadership - tactical retreat)

"The ICU. Maria can't hold alone. If we lose the children's ward..."

*The Nephwrack laughs, a sound like crumbling graves*

"FALL BACK, LITTLE HEALER. IT CHANGES NOTHING. THE OPENING HAS BEGUN."

*Peggy grabs Thomas and RUNS*

"Move! The living come first!""""
        )

    if thomas:
        scene.add_post(
            character=thomas,
            display="Thomas Ashworth",
            message="""*Thomas runs with her, throwing Moliate attacks behind them to
slow the pursuit*

"The children - if the Spectres reach them physically, they won't
just kill them. They'll TURN them. Enfants, trapped in Oblivion
forever."

*His aristocratic composure finally cracks*

/roll 4 7
(Willpower - fighting despair)

"We can't let that happen. Whatever it costs."

*They reach the ICU stairs*

"Margaret. If this is the end... it's been an honor."

*He draws his relic blade - a weapon from his mortal life, still
sharp after decades in the Shadowlands*

"Let's make Oblivion regret coming here.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The pediatric ICU.

Maria stands in the center of the ward, her form blazing with Pathos.
Spectrally, she's linked to every sick child in the room - a mother
protecting her adopted family.

The Spectres circle but cannot breach. Her love is a force they
can't match.

Peggy and Thomas arrive just as the Nephwrack does.

For a long moment, the four beings face each other across the ward.
Living children sleep in their beds, unaware of the war being
fought for their souls.

"YOU CANNOT WIN," the Nephwrack hisses. "THE STORM IS ETERNAL. YOU
ARE MERELY DELAYING THE INEVITABLE."

Then a new voice speaks:

"Delays have a way of becoming permanent."

The Hierarchy reinforcements have arrived. A Deathlord's personal
guard, fifty strong, pouring up from the Tempest.

The battle turns.

[Scene End - Reinforcements arrive]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
