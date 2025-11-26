"""
Serpents in the City - Scene 2: The Confrontation

The mummies confront the Apophis cultist.

Characters: Amenhotep IV, Dr. Constance Grey
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of Serpents in the City."""
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
        name="The Confrontation",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 2, 10),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Confrontation")
        return scene

    print("  Created Scene: The Confrontation")

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
        message="""Amenhotep approaches the woman in black. Up close, she's older
than she appeared - forty, perhaps fifty, with the bearing of
someone used to command.

Her name tag reads "Dr. Helena Vasquez - Cairo Museum."

A lie, of course. No one from Cairo would display the artifact
the way it's been displayed. The Egyptian government takes a
dim view of Apophis worship.

She turns as Amenhotep approaches, and her eyes widen with
recognition - not of his face, but of what lies beneath.

"Reborn one," she whispers. "I didn't expect you to come yourself.""""
    )

    if amenhotep:
        scene.add_post(
            character=amenhotep,
            display="Amenhotep IV",
            message="""*Amenhotep's smile doesn't reach his eyes*

"Dr. Vasquez. Or should I use your real name?"

*He leans closer, voice low*

/roll 5 6
(Manipulation + Intimidation - asserting dominance)

"I know your order. I've destroyed it three times in three millennia.
Yet here you are again, like weeds in a garden."

*His presence presses against her*

"You wanted my attention. You have it. Now tell me why you've come
to MY city before I decide you're not worth questioning."

*Ancient power ripples beneath his modern facade*

"Speak quickly.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Helena - her true name is meaningless, she's abandoned it for the
Serpent's service - doesn't flinch. A true believer's faith is
its own armor.

"Your city? You've been asleep for decades, Sem-priest. While you
dreamed, we built. The Serpent's children are everywhere now."

She gestures at the crowd.

"Senators, CEOs, generals. People who shape the world. When Apophis
returns, they'll be ready to serve. And all your precious Ma'at
won't save a single one of them."

Her smile is serene.

"But I'm not here to monologue. I'm here to deliver a message:
withdraw from Seattle, or we release what we've captured.""""
    )

    if constance:
        scene.add_post(
            character=constance,
            display="Dr. Constance Grey",
            message="""*Constance appears at Amenhotep's shoulder, having heard
enough through their link*

"What have you captured? Be specific."

*Her voice carries the weight of centuries*

/roll 5 6
(Perception + Occult - reading between the lines)

"You wouldn't threaten us with something small. You wouldn't have
revealed yourselves just for leverage."

*Her eyes narrow*

"A vessel. You've captured a vessel - one of the Khat-bodies waiting
for rebirth."

*She looks at Amenhotep*

"They have a mummy. Still in death-sleep. If they destroy it before
the soul returns..."

*The implications are horrifying*"""
        )

    if amenhotep:
        scene.add_post(
            character=amenhotep,
            display="Amenhotep IV",
            message="""*Amenhotep's calm cracks, ancient rage showing through*

"WHOSE vessel?"

*His hand locks around Helena's wrist with inhuman strength*

/roll 6 6
(Strength + Brawl - physical intimidation)

"Tell me whose body you've stolen, cultist. Tell me before I
forget I was once capable of mercy."

*His grip tightens*

"The Spell of Life is sacred. A mummy in death-sleep is DEFENSELESS.
If you've violated that..."

*His eyes begin to glow faintly*

"There is no corner of this world where you will escape my vengeance.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Helena's serene smile doesn't waver, even as her wrist creaks
under Amenhotep's grip.

"Lord Osiris's own bloodline. A prince who served in the courts
of Ramses. We found him in a private collection, still sleeping,
waiting for his Ka to return."

She leans closer.

"Withdraw from Seattle. Let the Serpent's children work unopposed.
And we return the prince, unharmed. Refuse..."

Her free hand makes a serpent's striking motion.

"And his next death will be permanent."

Around them, the museum guests continue their pleasant evening,
unaware of the ancient war being waged in whispers.

[Scene End - Hostage situation revealed]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
