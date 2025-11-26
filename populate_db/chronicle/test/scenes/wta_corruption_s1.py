"""
Corruption Beneath - Scene 1: The Poisoned Glen

The pack investigates reports of Wyrm-taint spreading through the forest preserve.

Characters: Runs-Through-Shadows, Storm's Fury
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of Corruption Beneath."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        shadow = CharacterModel.objects.get(name="Runs-Through-Shadows")
    except CharacterModel.DoesNotExist:
        shadow = None

    try:
        storm = CharacterModel.objects.get(name="Storm's Fury")
    except CharacterModel.DoesNotExist:
        storm = None

    try:
        location = LocationModel.objects.get(name="Cascadian Wilderness Caern")
    except LocationModel.DoesNotExist:
        location = None

    scene, created = Scene.objects.get_or_create(
        name="The Poisoned Glen",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 5, 3),
            "location": location,
        },
    )

    if not created:
        print("  Scene already exists: The Poisoned Glen")
        return scene

    print("  Created Scene: The Poisoned Glen")

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
        message="""The forest preserve northeast of Seattle was once a place of peace.
Ancient cedars stretched toward the sky, their roots drinking from streams
pure enough to sustain salmon runs. The Garou knew it as a place where Gaia's
presence could still be felt.

Now something is wrong.

Runs-Through-Shadows and Storm's Fury approach the preserve's edge in Lupus
form, having run for two hours through the Umbra to reach this place. Even
from here, the wrongness is palpable - a greasy feeling in the air, a bitter
taste on the tongue."""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*The black wolf's hackles rise as she approaches the treeline. Her
nose wrinkles at the scent - rot and chemicals and something worse*

*She shifts to Glabro, her form expanding to a hunched, muscular humanoid*

"The spirits warned us true. Can you feel it, Storm? The land itself is sick."

*She reaches out with her senses, trying to locate the source of the taint*

/roll 5 6
(Perception + Primal-Urge - sensing Wyrm corruption)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The corruption is like a wound in the world. Shadows detects its
source - about a mile into the forest, where the land dips into a natural
glen. The taint radiates outward from there like infection spreading from
a festering cut.

The spirits here are silent. No birdsong, no rustle of small animals. Even
the wind seems reluctant to pass through these trees."""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm remains in Lupus form, his silver-grey fur bristling. A low
growl rumbles in his chest*

*He shifts to Crinos - the war form. Nine feet of muscle and rage, claws
gleaming in the dim light*

"Then we cut out the infection. This is what we were born for."

*He tests the air, trying to determine what kind of Wyrm creature they face*

/roll 6 6
(Perception + Occult - identifying the type of corruption)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Storm's experience tells him this is no simple Bane infestation. The
pattern of corruption suggests something more insidious - a Wyrm spirit that
has taken root in the physical world, using something as an anchor.

Industrial corruption. Probably chemical. The Wyrm has many servants among
humanity's worst impulses, and illegal dumping is a time-honored method of
spreading its influence.

But there's something else. A pulse of spiritual energy, rhythmic and wrong.
Something is feeding the corruption, nurturing it. This isn't passive pollution
- it's deliberate cultivation."""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows shifts fully into Crinos, her black fur seeming to drink
in the light*

"Not just dumping. Someone is growing this. Feeding it."

*She bares her fangs*

"Pentex? Black Spiral Dancers?"

*She begins moving toward the glen, keeping to the deeper shadows out of
ingrained habit*

/roll 7 6
(Dexterity + Stealth - approaching unseen)

*Her voice drops to a growl*

"We scout first. See what we face. Then we decide if we need the rest of the
pack - or if we can handle this ourselves.""""
        )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm follows, though stealth has never been his strength. His
massive Crinos form crashes through undergrowth that Shadows slips past
like smoke*

"Caution is wise. But if there are Dancers here..."

*His claws flex*

"We do not let them leave. Whatever it takes."

/roll 4 7
(Dexterity + Stealth - moving quietly)

#WP
*He focuses, forcing himself to move with more care than his rage demands*"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The two Garou slip through the dying forest. Every hundred yards,
the corruption grows stronger. Trees show signs of disease - bark peeling,
leaves blackened and curled. Small corpses litter the ground: birds, squirrels,
a deer that simply lay down and never rose again.

Then they reach the glen.

It's worse than they imagined.

A pit has been dug in the earth, perhaps thirty feet across. It's filled with
barrels - dozens of them, many rusted and leaking. The chemical stench is
overwhelming even in the physical world.

But the true horror stands at the pit's edge: a figure in a hazmat suit,
feeding something into the toxic brew. And surrounding the pit, drawn in what
looks like industrial waste, is a ritual circle.

The figure turns, and through the suit's faceplate, you can see it smile.

"Ah. The Garou. Right on schedule.""""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows freezes, every instinct screaming trap. Her eyes scan the
treeline, looking for other threats*

"You expected us."

*It's not a question*

*She shifts her weight, ready to spring in any direction*

/roll 6 6
(Perception + Alertness - detecting ambush)

"Who are you? Why defile this land?""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The hazmat-suited figure laughs. It's a wet, wrong sound.

"Who? I'm Dr. Helena Cross. Formerly of the EPA, currently a servant of
progress." She gestures at the pit. "As for why - this land sits on a nexus
point. Pump enough poison into the earth here, and the rot will spread for
miles. Years of work compressed into months."

She steps back from the pit's edge.

"But you're right to look for the trap. I'm just the gardener. The wolves..."

From the treeline behind them comes a howl - but it's wrong, corrupted,
a sound of madness and hate.

"...the wolves are here for you."

Three shapes emerge from the shadows. Black Spiral Dancers, already in Crinos,
their fur patchy and their eyes glowing with green Balefire.

[To be continued...]"""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm's rage ignites. The Dancers. Garou who fell to the Wyrm,
who danced the Black Spiral and emerged as monsters*

*He throws back his head and howls - not in fear, but in challenge*

"DANCERS! Face us if you dare, traitors!"

*He charges the nearest one, claws extended*

/roll 7 6
(Dexterity + Brawl - opening attack)

"Shadows - the human! Don't let her complete the ritual!"

[Scene End - Battle joined]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
