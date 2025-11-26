"""
The Stolen Scarab - Scene 1: The Theft

A powerful relic is stolen from the mummies' safekeeping.

Characters: Amenhotep IV, Dr. Constance Grey
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of The Stolen Scarab."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        amenhotep = CharacterModel.objects.get(name="Amenhotep IV")
    except CharacterModel.DoesNotExist:
        amenhotep = None

    try:
        constance = CharacterModel.objects.get(name="Dr. Constance Grey")
    except CharacterModel.DoesNotExist:
        constance = None

    scene, created = Scene.objects.get_or_create(
        name="The Theft",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 5, 5),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Theft")
        return scene

    print("  Created Scene: The Theft")

    if amenhotep:
        scene.add_character(amenhotep)
    if constance:
        scene.add_character(constance)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The vault beneath Seattle's Egyptian collection. A place known
only to the Amenti and their most trusted mortal servants.

For three thousand years, the Scarab of Khepri has rested here -
a relic from the time before Osiris, when the gods still walked
openly among mortals. Its power: to preserve life indefinitely,
holding the soul to the body even against death's pull.

This morning, the vault was breached. The wards were bypassed
without triggering. The guards saw nothing.

The Scarab is gone.

Someone knew exactly what they were looking for. And they knew
exactly how to take it."""
    )

    if constance:
        scene.add_post(
            character=constance,
            display="Dr. Constance Grey",
            message="""*Constance examines the empty pedestal, her face pale*

"The wards weren't broken. They were RECOGNIZED. Someone spoke
the proper names, gave the proper offerings. Our own protections
let them pass."

*She traces the residue of power*

/roll 6 6
(Intelligence + Occult - analyzing the breach)

"This wasn't a human thief. The resonance is too old, too precise.
Another mummy did this."

*She meets Amenhotep's eyes*

"One of us betrayed the compact. One of us has decided the Scarab
serves them better than the collective."

*Her voice is bitter*

"After everything we survived, we're still capable of this.""""
        )

    if amenhotep:
        scene.add_post(
            character=amenhotep,
            display="Amenhotep IV",
            message="""*Amenhotep's anger is cold, controlled*

"The Scarab of Khepri. In the wrong hands, it could grant immortality
to anyone - mortal, monster, worse. It could tip the balance of
power in this city permanently."

*He studies the scene*

/roll 5 6
(Perception + Investigation - reading the clues)

"The technique... I've seen this before. Very few of us know these
old ways. The thief is someone who remembers the First Kingdom."

*His jaw tightens*

"That narrows it to perhaps a dozen Amenti worldwide. Most of whom
I know personally."

*He begins pacing*

"This is personal. They're not just stealing an artifact. They're
making a statement.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The investigation expands. Constance checks the Amenti network -
who's been in Seattle recently, who has motive, who has the skill.

The list narrows to one name: Sekhemib, once a general in the
armies of the Second Dynasty. He served Amenhotep in the old
days, before the Fall of the First Kingdom. They were allies.
Friends, even.

But Sekhemib's last resurrection went wrong. His memories
fragmented. He's been unstable for decades, believing himself
still at war with enemies who died three thousand years ago.

If he has the Scarab, he might try to use it on himself -
to lock his current degraded state in place forever."""
    )

    if amenhotep:
        scene.add_post(
            character=amenhotep,
            display="Amenhotep IV",
            message="""*Amenhotep's expression crumbles*

"Sekhemib. My friend. My brother-in-arms."

*He sinks into a chair*

/roll 4 6
(Willpower - processing the revelation)

"I knew his last awakening was difficult. I should have been there
for him. Should have helped him through the confusion."

*He looks at Constance*

"If he uses the Scarab in his current state, he'll be trapped. The
man I knew will never return - just this broken shadow, forever."

*He stands*

"I have to find him. Not to punish - to help, if I can."

*His voice hardens*

"But if he can't be helped... I'll do what's necessary.""""
        )

    if constance:
        scene.add_post(
            character=constance,
            display="Dr. Constance Grey",
            message="""*Constance nods*

"Sekhemib was last seen in the Cascade Mountains. He's been using
an old military bunker as a haven - probably reminds him of
commanding troops."

*She pulls up information*

/roll 5 6
(Intelligence + Investigation - gathering intelligence)

"The bunker is defensible. If he thinks we're enemies, he'll fight
us like he fought the Hyksos."

*She prepares gear*

"We approach carefully. Try to talk first. Remind him who he is,
who WE are."

*She pauses*

"And Amenhotep? If it comes to a fight, remember - he's not the
man you knew. The Spell of Life doesn't always restore what
was there before."

[Scene End - Theft traced to a friend]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
