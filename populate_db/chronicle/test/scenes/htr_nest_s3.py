"""
Into the Nest - Scene 3: The Extraction

The hunters fight their way out with the captives.

Characters: Sarah Mitchell, David Okonkwo
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of Into the Nest."""
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
        name="The Extraction",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 3, 11),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Extraction")
        return scene

    print("  Created Scene: The Extraction")

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
        message="""The extraction begins with silence and lockpicks.

Sarah and David move through the cells, freeing captives one by one.
Most are too weak to walk - they've been bled too many times. But
enough are strong enough to help carry the others.

A whispered explanation: "We're getting you out. Stay quiet. Move
when we tell you."

The vampires in the heart chamber are distracted - arguing about
territory, hunting rights, political nonsense. They don't notice
their food supply mobilizing.

Not yet."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah supports a young woman - barely conscious, bite marks on
her neck still fresh*

"David, I've got the last of them. Eleven total - one cell was empty."

*She guides the group toward the stairs*

/roll 5 6
(Dexterity + Stealth - moving the group quietly)

"Everyone stay close. When we hit the door, we run. Don't stop, don't
look back, just run for the street."

*She positions herself at the rear of the group*

"I'll cover the retreat. If anything comes up those stairs-"

*A voice from below, sharp and angry*

"The cattle are loose. FIND THEM.""""
        )

    if david:
        scene.add_post(
            character=david,
            display="David Okonkwo",
            message="""*David spins, UV flashlight up*

"They know. MOVE!"

*He shoves the first captives up the stairs*

/roll 6 6
(Dexterity + Athletics - rapid evacuation)

*The first vampire appears at the bottom of the stairs, impossibly
fast. David hits it with the UV light*

*The vampire SCREAMS, skin smoking, and falls back*

"That won't hold them long! Sarah, I'll handle the rear - get these
people out!"

*More shapes in the darkness below*

"Go! GO! GO!""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The evacuation becomes a desperate sprint.

Captives stumble up the stairs, some carrying others, all terrified.
The staff corridor is chaos - employees who aren't vampires flee
in confusion, not understanding what's happening.

The vampires are behind them, slowed by the UV but not stopped.
Two of them are old enough to push through the pain, pursuing with
murderous intent.

The club proper is only feet away. The noise, the crowd, the witnesses -
safety in numbers. Vampires don't feed in public.

Almost there."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah bursts through the staff door, dragging captives into the
club's main floor*

"FIRE! THERE'S A FIRE IN THE BASEMENT! EVERYONE OUT!"

*The crowd panics. Perfect cover*

/roll 6 6
(Manipulation + Subterfuge - creating chaos)

*She pushes the captives toward the exit, blending them with the
fleeing clubbers*

"Keep moving, don't stop, the van's on Third Street!"

*She turns back, stake in hand, as a vampire tries to follow them
into the crowd*

"Not tonight, monster."

*She drives the stake home*"""
        )

    if david:
        scene.add_post(
            character=david,
            display="David Okonkwo",
            message="""*David emerges last, UV flashlight blazing*

*The second pursuing vampire hesitates at the door, unwilling to
enter a room full of witnesses*

"That's right. Back off."

/roll 5 6
(Willpower - facing down a vampire)

*They lock eyes for a moment. The vampire's gaze is murderous.*

"You've made enemies tonight, hunter. Powerful enemies."

*David backs toward the exit*

"Good. It means we're doing something right."

*He reaches the street, where Sarah and the captives are piling
into their van*

"Drive! Now!"

*Tires screech. They vanish into the Seattle night.*

*Behind them, Club Nocturne burns as someone pulls the fire alarm
for real.*

[Scene End - Captives rescued, nest disrupted]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
