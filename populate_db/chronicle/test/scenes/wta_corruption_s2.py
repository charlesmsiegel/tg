"""
Corruption Beneath - Scene 2: The Battle of the Glen

The pack fights the Black Spiral Dancers while trying to stop the ritual.

Characters: Runs-Through-Shadows, Storm's Fury
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of Corruption Beneath."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        shadow = CharacterModel.objects.get(name="Runs-Through-Shadows")
    except CharacterModel.DoesNotExist:
        shadow = None

    try:
        storm = CharacterModel.objects.get(name="Storm's Fury")
    except CharacterModel.DoesNotExist:
        storm = None

    scene, created = Scene.objects.get_or_create(
        name="The Battle of the Glen",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 5, 3),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Battle of the Glen")
        return scene

    print("  Created Scene: The Battle of the Glen")

    if shadow:
        scene.add_character(shadow)
    if storm:
        scene.add_character(storm)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Chaos erupts in the poisoned glen.

Storm's Fury crashes into the lead Dancer - a massive brute whose fur has
fallen out in patches, replaced by scaly growths. They go down in a tangle
of claws and fangs.

The other two Dancers circle, one moving toward Shadows, the other trying to
flank Storm.

Dr. Cross retreats toward the ritual circle, pulling something from her
hazmat suit - a syringe filled with luminescent green fluid."""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows doesn't hesitate. She leaps over the approaching Dancer,
using her momentum to clear the gap between her and the human*

/roll 6 7
(Dexterity + Athletics - acrobatic leap)

*In midair, she shifts to Lupus - smaller, faster, harder to hit*

*She lands between Cross and the ritual circle*

"The ritual ends now, defiler!""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Cross's eyes widen behind her faceplate. She didn't expect the
Garou to ignore the immediate threat.

"Stay back, wolf. You don't understand what you're interfering with."

She raises the syringe. "This is refined Balefire. One injection and I become
something... more. Are you prepared to face that?"

Behind Shadows, the Dancer she leaped over is turning, preparing to attack
her exposed back."""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm's jaws find the throat of his opponent. He bites down HARD*

/roll 8 6
(Strength + Brawl - devastating bite)

*The Dancer beneath him thrashes, claws raking Storm's sides*

/roll 5 6
(Stamina + Athletics - soak damage)

*Through the pain, he sees the other Dancer moving toward Shadows' back*

*He hurls himself off his fallen opponent and intercepts*

"SHADOWS! Behind you! I have it!""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Storm's intervention saves Shadows from an ambush. He crashes into
the second Dancer, and they tumble across the poisoned earth.

The first Dancer - the one Storm savaged - is rising again. Wyrm-tainted
regeneration knits its wounds, though slower than a true Garou's healing.
Its eyes burn with hate and madness.

Three against two, and the humans still has the Balefire syringe."""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows shifts back to Crinos in one fluid motion. She needs
the reach, the power*

"Inject yourself then, human. Make yourself a monster."

*Her voice drops to a growl*

"I've killed worse than you."

*She lunges, claws aimed at the hand holding the syringe*

/roll 6 6
(Dexterity + Brawl - disarming strike)

#WP
*Every ounce of her focus goes into precision*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Shadows' claws slice through the hazmat suit and the flesh beneath.
Cross screams as the syringe goes flying, shattering against a rock.

The luminescent fluid splashes across the ground - and where it lands, the
earth begins to bubble and smoke.

"No! NO! Years of work!" Cross clutches her bleeding hand, staggering back.

But then she laughs, a sound edged with hysteria.

"It doesn't matter. Look."

She points at the ritual circle. The symbols are glowing now, pulsing with
sickly green light. The barrels in the pit are vibrating.

"It's already begun. The poison is seeping into the spirit world. In an hour,
this entire forest will be a Wyrm domain. And there's nothing you can do to
stop it.""""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm finally puts down the Dancer he's fighting - a brutal
combination of claws and fangs that leaves the creature twitching*

*He turns to face the third Dancer and the risen first*

"Shadows! Finish the human! Break the circle!"

*He charges the two remaining Dancers, knowing he can't win against both*

*But he doesn't need to win. He just needs to buy time*

/roll 6 7
(Dexterity + Brawl - fighting two opponents)

*His howl echoes through the dying forest*

"FOR GAIA!""""
        )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows doesn't waste time with the human. She leaps into the
ritual circle and begins tearing at the symbols*

/roll 5 6
(Intelligence + Occult - disrupting the ritual)

*Her claws gouge deep furrows in the earth, breaking the careful patterns*

"Your ritual is broken, defiler. Your servants fall. And you..."

*She turns back to Cross, advancing*

"You will tell us everything. Who sent you. What Pentex plans. All of it."

*Her eyes glow with reflected moonlight*

"Or I will make what the Dancers would have done to you seem merciful.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The ritual circle sputters and dies as Shadows tears through it.
The glow fades, the vibration stops. Whatever was building here has been
interrupted - though the existing corruption remains.

Behind her, Storm faces two Dancers alone. He's taken wounds - deep claw
marks across his chest, a bite on his shoulder. But he's still standing,
still fighting, still roaring his defiance.

Dr. Cross looks at the advancing Garou, at her ruined work, at her bleeding
hand. Something breaks in her eyes.

"Pentex will send others. This is just the beginning."

She reaches for something at her belt - a small device.

"But you won't learn anything from me."

It's a dead man's switch. Connected to the barrels.

"For the Wyrm."

The explosion rocks the glen.

[Scene End - Explosion triggered]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
