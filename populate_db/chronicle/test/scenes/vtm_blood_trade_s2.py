"""
Blood in the Water - Scene 2: The Chantry's Secrets

Isabella Santos researches the name 'Arterius' in the Tremere archives while
dealing with chantry politics.

Characters: Isabella Santos
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 2 of Blood in the Water."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Get characters
    isabella = CharacterModel.objects.get(name="Isabella Santos")

    # Get location
    try:
        location = LocationModel.objects.get(name="Tremere Chantry", chronicle=chronicle)
    except LocationModel.DoesNotExist:
        location = None

    # Create the scene
    scene, created = Scene.objects.get_or_create(
        name="The Chantry's Secrets",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 3, 17),
            "location": location,
        },
    )

    if not created:
        print("  Scene already exists: The Chantry's Secrets")
        return scene

    print("  Created Scene: The Chantry's Secrets")

    scene.add_character(isabella)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Tremere Chantry occupies a renovated Victorian mansion in
Capitol Hill, its mundane appearance concealing layers of mystical protection. The
library occupies the third floor - a climate-controlled sanctuary of ancient tomes
and carefully preserved manuscripts.

Isabella Santos has spent the last two hours searching through the indexes,
following cross-references and consulting the increasingly unhelpful Companion who
serves as librarian.

The name 'Arterius' appears only once in the entire collection - and the volume
it references is kept in the restricted section."""
    )

    scene.add_post(
        character=isabella,
        display="Isabella Santos",
        message="""*Isabella approaches the iron gate separating the restricted
section from the main library*

"Theodore, I need access to volume seven of the 'Annals of the Western Courts.'
It references a name that may be relevant to my current research."

*She keeps her voice carefully neutral, knowing that requests for restricted texts
are reported to the Regent*

/roll 4 7
(Manipulation + Etiquette - navigating chantry bureaucracy)"""
    )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Theodore, the grey-haired Companion who has served as librarian for
decades, peers at Isabella over his spectacles. His expression is politely
noncommittal.

"The Annals are classified at Apprentice Third level, Miss Santos. Your current
standing is Apprentice Second." He pauses, a hint of sympathy in his eyes. "However,
I could note your interest and submit a formal request to Regent Richter. Such
requests typically process within... three to four weeks."

Three weeks. Far too long if something is actively happening in the city."""
    )

    scene.add_post(
        character=isabella,
        display="Isabella Santos",
        message="""*Isabella takes a deep breath, considering her options. She
could try to circumvent the system, but that carries its own risks. Or...*

"Theodore, this research may be time-sensitive. Is there any provision for
expedited access in cases involving potential threats to the Chantry?"

*She leans in slightly*

"I have reason to believe someone outside the Pyramid is conducting blood rituals
in Seattle. If I'm right, Regent Richter will want to know immediately - but I
need context before I bring him speculation."

/roll 5 6
(Charisma + Subterfuge - implying urgency without revealing too much)"""
    )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Theodore's expression shifts subtly. Blood rituals outside the
Pyramid's control - that's a matter the Tremere take very seriously.

"I... see." He removes his spectacles and cleans them slowly. "There is a provision
for emergency consultation. The text cannot leave the restricted section, and your
time would be limited to one hour. Additionally, I would be required to note the
specific passages you consulted."

He meets her eyes. "Do you wish me to invoke this provision?"

The implication is clear: this will be reported. But it might be worth it."""
    )

    scene.add_post(
        character=isabella,
        display="Isabella Santos",
        message="""*Isabella weighs the consequences for a long moment, then nods*

"Yes. Please invoke the provision."

*She follows Theodore through the gate as he unlocks the restricted section. The
air here is heavier, saturated with the residue of protective enchantments. She
can feel the wards pressing against her Auspex like a gentle warning*

*Theodore retrieves a leather-bound volume and places it before her*

"One hour, Miss Santos. The clock begins now."

/roll 6 5
(Intelligence + Occult - researching the Annals)"""
    )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Annals of the Western Courts, Volume Seven, covers the period
from 1870 to 1920 - the turbulent years of westward expansion and the establishment
of Camarilla domains in the Pacific Northwest.

Isabella finds the reference quickly. A marginal note, written in archaic Latin:

'Arterius Maxim - Arrived Seattle 1892 with the Ventrue delegation. Elder of the
Fourth Generation, claiming lineage from the Lasombra Antediluvian through obscure
descent. Disputed. Disappeared during the Great Fire crisis of 1889. Presumed in
torpor or Final Death. No confirmation.'

Fourth Generation. If this Arterius is real... that would make them one of the
oldest Kindred ever to set foot in the Pacific Northwest."""
    )

    scene.add_post(
        character=isabella,
        display="Isabella Santos",
        message="""*Isabella's blood runs cold as she reads the entry. Fourth
Generation. The numbers alone are staggering - such an elder would predate the
founding of most Camarilla institutions*

*She carefully transcribes the relevant passage into her notebook, her hand
trembling slightly*

"Lasombra lineage... but here before the Sabbat's western push. A rogue elder?
Or something else entirely?"

*She flips through more pages, looking for additional references*

/roll 5 7
(Intelligence + Investigation - finding related entries)"""
    )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The search yields one more relevant passage - a report from 1891
describing unusual disappearances among the mortal population near the waterfront.
The investigating Kindred (a Nosferatu named 'Kraven') concluded that a "creature
of considerable age" was feeding without regard for the emerging Masquerade.

The report ends abruptly. Kraven's subsequent entries in the Annals cease.

Isabella's hour is running out. She has enough to know that something ancient was
in Seattle once - and if the blood trade is connected, it might still be here."""
    )

    scene.add_post(
        character=isabella,
        display="Isabella Santos",
        message="""*Isabella closes the volume carefully, her mind racing*

"An elder who may predate the Camarilla itself. Blood being gathered in enormous
quantities. And Roland's visions of something hungry waking up."

*She rises, nodding to Theodore*

"Thank you. I have what I need for now."

*As she leaves the restricted section, she's already planning her next move.
Shadow needs to know about this - but more importantly, she needs to find out
what happened at that waterfront over a century ago. And whether history is
about to repeat itself*

[Scene End - To be continued in Scene 3: The Waterfront]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
