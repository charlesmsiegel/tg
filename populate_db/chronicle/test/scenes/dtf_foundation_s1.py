"""
The Foundation Cracks - Scene 1: The Awakening Earthbound

An ancient Earthbound demon stirs beneath Seattle.

Characters: Zephyrus, Marcus Wells
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of The Foundation Cracks."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        zephyrus = CharacterModel.objects.get(name="Zephyrus")
    except CharacterModel.DoesNotExist:
        zephyrus = None

    try:
        marcus = CharacterModel.objects.get(name="Marcus Wells")
    except CharacterModel.DoesNotExist:
        marcus = None

    scene, created = Scene.objects.get_or_create(
        name="The Awakening Earthbound",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 4, 20),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Awakening Earthbound")
        return scene

    print("  Created Scene: The Awakening Earthbound")

    if zephyrus:
        scene.add_character(zephyrus)
    if marcus:
        scene.add_character(marcus)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""3:33 AM. Every Fallen in Seattle feels it at the same moment.

A PULSE of ancient power, radiating from somewhere beneath the city.
Something vast and terrible, stirring in its millennia-long sleep.
Something that makes even the demons who survived the Abyss feel small.

An Earthbound is awakening.

In the old churches, mortal worshippers wake from nightmares they
can't explain. In hospitals, patients flatline for a moment before
returning to life. The city's foundation - both physical and spiritual -
shivers.

Something hungry is remembering how to want."""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus gasps, clutching his host's chest as the pulse hits him.
Memories flood back - the Abyss, the war, things he'd rather forget*

"No. Not possible. The Earthbound were all accounted for..."

*He reaches out with his supernatural senses, tracing the pulse
back to its source*

/roll 6 6
(Perception + Awareness - locating the Earthbound)

"Under the city. Deep. Something's been sleeping there since before
Seattle was built. Since before humans came to this place."

*His voice drops to a whisper*

"One of the old ones. One of the First Fallen."

*He begins gathering his things*

"I need to find Marcus. This is beyond anything we've faced.""""
        )

    if marcus:
        scene.add_post(
            character=marcus,
            display="Marcus Wells",
            message="""*Marcus arrives at Zephyrus's haven, his mortal face pale but
his Fallen nature burning with alertness*

"I felt it too. Half the thralls in the city are having seizures."

*He paces, agitated*

/roll 5 6
(Intelligence + Occult - analyzing the situation)

"An Earthbound. An UNBOUND one. Do you know what that means?"

*He doesn't wait for an answer*

"The Earthbound are demons who never fell into the Abyss. They've
been on Earth since the beginning, sustained by worship. If one's
waking up..."

*He meets Zephyrus's eyes*

"It's going to need Faith. A lot of it. And it won't care where
it gets it.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Another pulse, stronger this time. Across Seattle, people clutch
their heads. A few of the more sensitive mortals begin praying -
to anything, to anyone, just to make the feeling stop.

That's exactly what the Earthbound wants.

Through their infernal senses, Zephyrus and Marcus can perceive the
entity more clearly now:

*A vast presence, coiled beneath the earth like a serpent. Its true
name is lost to time, but its NATURE is clear - it was once a demon
of hunger and consumption, a thing that fed on mortal fear.*

*And it's STARVING.*

*Five thousand years of sleep, and now it wakes to a world of seven
billion potential meals.*"""
    )

    if zephyrus:
        scene.add_post(
            character=zephyrus,
            display="Zephyrus",
            message="""*Zephyrus focuses, calling on his own nature - once a demon of
the wind and change, now something trying to be better*

"It's weak. The sleep drained it. Right now, it's running on
instinct - sending out those pulses to generate fear, harvesting
the Faith that creates."

*He traces patterns in the air*

/roll 5 7
(Intelligence + Lore - understanding the Earthbound)

"But it's getting stronger. Every pulse, every prayer, every moment
of terror feeds it. We have maybe 48 hours before it's strong enough
to manifest physically."

*He looks at Marcus*

"We need allies. The other Fallen in the city. Maybe even..."

*He hesitates*

"Maybe even the other supernaturals. This isn't a demon problem.
This is everyone's problem.""""
        )

    if marcus:
        scene.add_post(
            character=marcus,
            display="Marcus Wells",
            message="""*Marcus nods grimly*

"I have contacts among the mages. They'll want to know about this -
something this big bleeds into their 'consensus reality' bullshit."

*He pulls out a phone*

/roll 4 6
(Manipulation + Politics - planning outreach)

"And the vampires. They control this city's night. If the Earthbound
manifests physically, it'll disrupt their whole power structure."

*He pauses*

"But Zephyrus - you know what happens if we can't stop it. If we
can't bind it or destroy it."

*His voice hardens*

"We'll have to FEED it. Give it something to consume that isn't
the entire city. Are you prepared for those choices?"

[Scene End - Earthbound threat identified, coalition-building begins]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
