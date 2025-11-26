"""
Into the Nest - Scene 2: The Descent

The hunters enter Club Nocturne and discover the basement.

Characters: Sarah Mitchell, David Okonkwo
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of Into the Nest."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        sarah = CharacterModel.objects.get(name="Sarah Mitchell")
    except CharacterModel.DoesNotExist:
        sarah = None

    try:
        david = CharacterModel.objects.get(name="David Okonkwo")
    except CharacterModel.DoesNotExist:
        david = None

    scene, created = Scene.objects.get_or_create(
        name="The Descent",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 3, 11),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Descent")
        return scene

    print("  Created Scene: The Descent")

    if sarah:
        scene.add_character(sarah)
    if david:
        scene.add_character(david)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Club Nocturne. 1 AM. The bass thrums through bodies packed onto the
dance floor. Lights pulse in hypnotic patterns. The air is thick with
sweat, alcohol, and something else - something predatory.

Sarah and David blend into the crowd, dressed to kill in more ways than
one. Their weapons are hidden but accessible. Their senses are on high
alert.

The club looks like any other weekend hotspot. Beautiful people dancing,
drinking, flirting. VIP sections cordoned off with velvet rope.

But Sarah's Sight shows something different. Some of those beautiful
people don't have auras. Some of them aren't people at all."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah moves through the crowd, her Sight filtering reality*

"I count four. Two at the bar, one working the VIP section, one on the
dance floor."

*She speaks through a tiny earpiece to David*

/roll 6 6
(Perception + Awareness - using Second Sight)

"The one at VIP is watching everyone. Choosing. God, David, it's like
watching a fox in a henhouse."

*She spots movement near the back*

"There - staff door by the emergency exit. Someone just went through
who definitely doesn't have a pulse. That's our entrance."

*Her hand brushes her concealed stake*

"Give me five minutes, then follow.""""
        )

    if david:
        scene.add_post(
            character=david,
            display="David Okonkwo",
            message="""*David positions himself near the staff door, pretending to
check his phone*

"Copy that. Security camera on the door, but I can loop it remotely."

*His fingers work on his phone*

/roll 5 6
(Dexterity + Technology - bypassing security)

"Camera's on loop. You have a three-minute window before anyone
notices the timestamp jump."

*He scans the crowd, watching the vampires Sarah identified*

"The ones at the bar are feeding. Subtle - looks like making out to
anyone not paying attention. But they're drinking from those people."

*His voice is tight*

"Sarah, be careful. There could be more downstairs. A lot more.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Sarah slips through the staff door. Beyond is a corridor of
industrial grey - far removed from the club's sleek aesthetic.
The music fades as she moves deeper, replaced by a silence that
feels intentional.

The basement entrance is at the end of the hall. A heavy door,
reinforced steel, with an electronic lock. Someone's spent a lot
of money keeping this place secure.

Through the door, muffled sounds. Crying. Moaning. The sounds of
people in despair.

The missing students. They're still alive.

For now."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah approaches the door, her heart pounding*

"David, I've found them. Multiple people alive down there. The door's
got an electronic lock - sending you a picture."

*She photographs the keypad*

/roll 5 7
(Wits + Investigation - analyzing the lock)

#WP

*She forces herself to think clearly*

"Wait. There's a pattern on the keys - wear marks. The code uses only
four numbers: 1, 3, 7, 9. That narrows it to 24 combinations."

*She starts trying combinations*

"Come on, come on..."

*The lock clicks*

"I'm in. Coming down to join you.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The basement is a horror show.

Cells line the walls - actual cells, with bars and locks, like a
private dungeon. Inside, Sarah counts at least a dozen people.
Some are recent additions, still wearing club clothes. Others
have been here longer - pale, thin, marked by repeated feedings.

And at the far end, in a larger chamber: the nest's heart. Three
vampires, lounging among silk cushions, blood-bags and wine glasses
within easy reach. They're feeding casually, treating their victims
like appetizers at a party.

They haven't noticed Sarah yet. The darkness is their friend.

It can be hers too."""
    )

    if david:
        scene.add_post(
            character=david,
            display="David Okonkwo",
            message="""*David arrives, UV flashlight in hand*

"Oh god."

*He takes in the scene, professional detachment cracking*

/roll 4 6
(Composure - maintaining focus)

*He pulls himself together*

"Twelve captives. Three hostiles. We can't fight them all and
extract the prisoners."

*He thinks rapidly*

"The UV flashlights - we can use them to cover our escape. Vampires
react to concentrated UV like a flashbang."

*He looks at Sarah*

"We get the prisoners moving, hit the vampires with UV, and run.
Not glorious, but it keeps people alive."

[Scene End - Nest discovered, extraction planning]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
