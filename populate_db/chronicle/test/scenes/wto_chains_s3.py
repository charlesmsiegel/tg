"""
Chains of the Living - Scene 3: A New Purpose

Peggy finds meaning in helping other wraiths face their Shadows.

Characters: Margaret "Peggy" Sullivan, Thomas Ashworth
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of Chains of the Living."""
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
        name="A New Purpose",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 10, 15),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: A New Purpose")
        return scene

    print("  Created Scene: A New Purpose")

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
        message="""One week later. The Shadowlands beneath Pike Place Market, in a
quiet corner where wraiths gather to share news and trade Artifacts.

Peggy Sullivan looks different. Not physically - wraiths rarely change
their forms - but there's a steadiness in her that wasn't there before.
Facing her grave, fighting her Shadow, strengthening her Fetters...
the experience has changed her.

Thomas has noticed. So have others. Word spreads quickly among the
dead when someone does what Peggy did.

A young wraith approaches, barely a year dead. His Shadow rides him
hard - you can see it in the way he twitches, the way his eyes dart
to non-existent threats. He's losing the battle, bit by bit."""
    )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy sees the young wraith and immediately understands*

"You're the one who drowned in the lake last summer. I heard about
you - the kayaking accident."

*She moves to intercept him, her manner calm and professional*

"I'm Margaret. People call me Peggy. I used to be a nurse."

*She can see his Shadow writhing beneath the surface, whispering
terrible things*

/roll 5 6
(Perception + Empathy - reading his state)

"I know what your Shadow is saying right now. It's telling you that
you deserved to drown. That you were careless, or stupid, or weak."

*She meets his eyes*

"It's lying. They always lie.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The young wraith - his name was Daniel, in life - stares at her
with desperate hope.

"It won't stop. Day and night, just... telling me I should have
died sooner. That everyone forgot me already. That I should just..."

He can't finish. But they both know what he means. Give in. Let
the Shadow win. Fall into Oblivion.

Around them, other wraiths pause their conversations. Some look
away, uncomfortable. Some watch with interest. Shadow-riding is
common; beating it is rare.

Daniel's Shadow surfaces momentarily - his face distorts, voice
changing.

"She can't help you. No one can help you. You're already dead,
Danny-boy. Embrace the darkness."

Then Daniel reasserts control, gasping."""
    )

    if thomas:
        scene.add_post(
            character=thomas,
            display="Thomas Ashworth",
            message="""*Thomas positions himself to support Peggy, blocking other wraiths
from interfering*

"Margaret knows what she's doing. She's a Pardoner - she heals
Shadows."

*He addresses the gathering crowd*

"Give them space. This is sacred work."

*To Daniel, more gently:*

/roll 4 6
(Manipulation + Leadership - managing the situation)

"What she did at her grave - facing her own Shadow, her own death -
that takes courage most of us don't have. If anyone can help you
find your center, it's her."

*He steps back, ceding the space to Peggy*

"Show them what's possible.""""
        )

    if peggy:
        scene.add_post(
            character=peggy,
            display="Peggy Sullivan",
            message="""*Peggy takes Daniel's hands in hers*

"I'm going to tell you something your Shadow doesn't want you to
know. Are you listening?"

*She waits for his nod*

"You didn't deserve to die. No one deserves to die. Death just...
happens. It's not punishment. It's not failure. It just IS."

/roll 6 6
(Castigate - soothing his Shadow)

#WP

*She channels her Pathos into him, her own hard-won peace flowing
through the connection*

"But living - or existing, for us - that IS a choice. Every moment
you fight that voice, you're choosing to be more than it wants you
to be. Every moment you don't give in, you WIN."

*Her voice rises*

"You are not your Shadow, Daniel. You are NOT your worst thoughts.
You are what you choose to be.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Something shifts in Daniel's posture. The constant twitching
slows. His eyes focus. The Shadow's whispers, while not gone,
fade to a manageable murmur.

"I... I haven't felt this quiet since I died."

He looks at Peggy with wonder.

"How? How did you learn to do that?"

Around them, other wraiths are watching with new interest. Some
of them carry Shadows that ride them just as hard. Some of them
have been dead for decades and never found peace.

Peggy sees them all. And she understands.

This is her new purpose. Not replacing her Fetters to the living -
they're still there, still strong. But adding to them. Building
new connections among the dead.

She was a nurse in life. In death, she'll be a healer of another
kind.

[Scene End - Peggy becomes a Shadow-healer]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
