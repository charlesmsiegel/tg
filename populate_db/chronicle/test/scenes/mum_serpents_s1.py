"""
Serpents in the City - Scene 1: The Cult Discovery

A mummy discovers an Apophis cult operating in Seattle.

Characters: Amenhotep IV, Dr. Constance Grey
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of Serpents in the City."""
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
        name="The Cult Discovery",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 2, 10),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Cult Discovery")
        return scene

    print("  Created Scene: The Cult Discovery")

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
        message="""The Seattle Art Museum. A private viewing of Egyptian antiquities,
invitation only. The city's cultural elite mingle among artifacts
that were old when their ancestors were painting in caves.

Amenhotep IV walks among them in modern guise, ancient eyes cataloging
every piece. Some he remembers. Some he doesn't. Time erases even
the memories of the deathless.

But one artifact draws his attention. A serpent statue, coiled and
waiting, that should not exist. Its provenance is false - he knows,
because he was there when the original was destroyed three thousand
years ago.

Someone has made a copy. Someone who knows far too much."""
    )

    if amenhotep:
        scene.add_post(
            character=amenhotep,
            display="Amenhotep IV",
            message="""*Amenhotep stands before the serpent statue, ancient memories
stirring*

"This is wrong."

*He reaches out but doesn't touch - the hieroglyphics on the base
are deliberately incorrect, hiding a message*

/roll 6 6
(Intelligence + Occult - deciphering the hidden message)

"It's a marker. A cult sign. They're announcing themselves to
anyone who knows what to look for."

*His voice is quiet but carries millennia of anger*

"Apophis. The Serpent that Devours. His followers are here."

*He turns to find Dr. Grey*

"Constance. We have a problem.""""
        )

    if constance:
        scene.add_post(
            character=constance,
            display="Dr. Constance Grey",
            message="""*Constance approaches, champagne glass in hand, playing her role
as museum benefactor*

"I felt the resonance when I walked in. That statue is... wrong.
It makes my teeth ache."

*She examines it with trained eyes*

/roll 5 6
(Perception + Occult - sensing the artifact's nature)

"There's Sekhem in this. Stolen life force, woven into the stone.
Someone poured souls into making this thing."

*Her expression hardens*

"Apophis cultists in Seattle. After all these centuries, they're
still trying to unravel Ma'at."

*She sets down her glass*

"Who owns this piece? Follow the artifact, find the cult.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The statue was donated by a tech billionaire named Harrison Wells.
New money, eccentric, famously interested in "ancient mysteries."
The kind of dilettante who funds archaeological expeditions and
keeps the interesting pieces for himself.

Or so the public story goes.

The Amenti know better. True Apophis cultists don't advertise.
They work in shadows, corrupting from within, preparing the way
for the Serpent's return. Harrison Wells isn't a cultist - he's
being used. A front man for something much older.

The question is: how deep does the infection go?"""
    )

    if amenhotep:
        scene.add_post(
            character=amenhotep,
            display="Amenhotep IV",
            message="""*Amenhotep studies the guest list with ancient patience*

"Wells is a fool. A rich fool, easily manipulated. The real
threat is whoever's pulling his strings."

*He spots someone in the crowd - a woman in black, watching
the room with predator's eyes*

/roll 5 6
(Perception + Awareness - identifying the threat)

"There. The woman by the pharaoh's bust. She moves like a priest -
every gesture deliberate, ritualistic."

*His hand goes to a hidden amulet*

"She's not just a cultist. She's a BELIEVER. The dangerous kind."

*He begins moving to intercept*

"I'll make contact. You watch the exits.""""
        )

    if constance:
        scene.add_post(
            character=constance,
            display="Dr. Constance Grey",
            message="""*Constance positions herself near the main entrance*

"Careful. If she's a true believer, she might recognize what you
are. The old enemies know each other."

*She activates subtle wards woven into her jewelry*

/roll 5 6
(Wits + Occult - preparing defenses)

"I'm setting containment. If this goes badly, I can seal the room
long enough for evacuation."

*She keeps her eyes on the target*

"Amenhotep - if the Apophis cult is operating openly enough to
display artifacts at public events, they're confident. Either
they don't think anyone can stop them..."

*Her voice drops*

"Or they WANT us to know they're here. This could be a trap."

[Scene End - Apophis cult presence confirmed]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
