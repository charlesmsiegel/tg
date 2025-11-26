"""
Blood Calls to Blood - Scene 3: The Raid

The pack assaults the Genesis Research facility to rescue the kinfolk.

Characters: Runs-Through-Shadows, Storm's Fury
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of Blood Calls to Blood."""
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
        name="The Raid",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 6, 20),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Raid")
        return scene

    print("  Created Scene: The Raid")

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
        message="""2 AM. The abandoned hospital looms against the Seattle skyline, dark
windows like empty eye sockets. Security lights create pools of harsh white
in the parking lot.

The pack has spent three days preparing. They know the guard rotations, the
blind spots in the cameras, the quickest route to the holding areas.

Two other packs from the sept are hitting the facility simultaneously - one
through the loading dock, one through the roof. Shadows and Storm have the
front entrance.

No survivors. No witnesses. No mercy.

This is war."""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows crouches in the darkness outside the security fence. She's
already in Crinos, her black fur blending with the night*

*Through pack-link:*

"Storm. On my mark. Remember - the kinfolk are priority. Everything else is
secondary."

*She watches the guard at the front entrance check his phone*

/roll 7 6
(Perception + Stealth - timing the approach)

*Three... two... one...*

"NOW."

*She vaults the fence in one leap, racing toward the door*"""
        )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm's Crinos form hits the fence like a battering ram. The
chain-link shreds*

*He doesn't bother with stealth. Let them know death is coming*

*His howl shatters the night - the signal for the other packs*

"FOR GAIA! FOR THE KINFOLK!"

*He barrels toward the guard, who's just now reaching for his radio*

/roll 8 6
(Strength + Brawl - overwhelming assault)

*The guard never finishes his call*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Alarms shriek. Red lights flash. The element of surprise is gone, but
it doesn't matter - the Garou are already inside.

The hospital's ground floor is a maze of abandoned rooms and debris-strewn
corridors. But the pack's intelligence was good - a secure door at the end
of the east hallway, recently installed, leads to the basement levels.

Guards in tactical gear pour out of a side room. They're expecting
intruders, but nothing could have prepared them for this. Nine-foot wolf-
monsters with claws like knives and eyes full of holy rage.

The first guard empties his magazine into Storm. The bullets barely slow
him down."""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm feels the bullets tear into him - pain, but distant,
drowned by fury*

/roll 6 6
(Stamina - soaking damage)

*He catches the guard who shot him and hurls him into his companions*

"THESE ARE THE PROTECTORS OF YOUR MASTERS?"

*He tears through them like paper*

/roll 7 6
(Dexterity + Brawl - multiple targets)

"WORTHLESS!"

*Blood splashes the walls*

"Shadows! The door!"""
        )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows is already at the secure door. Her claws gouge into
the reinforced metal*

"Sealed. Electronic locks."

*She looks for a control panel*

/roll 5 7
(Wits + Technology - bypassing security)

*The panel sparks as she tears it open, crossing wires with
practiced precision*

"Got it!"

*The door groans open, revealing stairs leading down into clinical
white light*

"Storm - I can smell them. The kinfolk. They're close.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The basement is a horror show.

Rows of cells line the walls, each containing a cot and a surveillance
camera. Most are occupied - men and women, all kinfolk, identified by
the subtle scent of wolf-blood that clings to them.

Maria Vasquez is in the third cell. She's alive. Sedated, but alive.

But it's the room at the end of the corridor that draws the eye. Through
reinforced glass, medical equipment gleams. Operating tables. Monitoring
stations. And on the tables...

Three women, obviously pregnant. Hooked up to machines that beep and hum
with artificial life.

Dr. Aldrich stands in the center of the room, a syringe in one hand and
a dead man's switch in the other.

"One more step and I flood their systems with adrenaline. The shock will
kill them - and the specimens they carry.""""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows freezes. Her every instinct screams to tear the human
apart, but...*

"Specimens."

*Her voice is deadly calm*

"You call Garou children 'specimens'?"

*She doesn't move, but her mind races*

/roll 6 7
(Intelligence + Medicine - analyzing the equipment)

"Those women. Kinfolk too?"

*Keep him talking. Look for options*

"What's your endgame here, Aldrich? You can't possibly think Pentex would
let you keep this secret forever.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Aldrich's smile is thin. "Secret? This is a pilot program. Once we
prove viable results, Genesis Research goes global. Imagine - controllable
Garou. Bred for loyalty, trained from birth."

His thumb hovers over the trigger.

"The future of warfare. The future of evolution. And you stupid animals are
too primitive to see it."

Behind him, one of the pregnant women stirs. Her eyes open. And for just a
moment, they flash amber - not the glow of fear, but something else.

Something awakening."""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm sees the flash. Understands instantly*

*He meets the woman's eyes and nods, almost imperceptibly*

"You think you can control us, human?"

*He steps forward, drawing Aldrich's attention*

"You think your drugs and your machines can cage the soul of Gaia?"

/roll 6 6
(Manipulation + Intimidation - distraction)

*His voice drops to a growl*

"You have made yourself a monster worse than anything we hunt. And monsters..."

*Behind Aldrich, the woman's restraints strain as her body begins to change*

"...monsters always fall.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The woman's First Change couldn't have come at a better time - or a
worse time, depending on perspective.

She tears free of the restraints, her body twisting into something between
human and wolf. The pain of transformation mixes with the pain of labor,
and her scream becomes a howl.

Aldrich spins, startled. His finger twitches on the trigger-

But Shadows is faster.

The doctor's hand separates from his arm before he can react. The dead man's
switch clatters to the floor, inactive without his grip.

Aldrich's screaming joins the chaos.

The other packs burst in moments later. The cleanup will take hours. But
Maria Vasquez is safe. Twelve other kinfolk are safe. And though two of
the pregnancies end in tragedy, one newborn Garou enters the world in a
hospital that will never see another patient.

The war with Pentex continues.

But tonight, Gaia's children won.

[Scene End - Facility destroyed, kinfolk rescued]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
