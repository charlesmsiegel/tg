"""
The Contested Node - Scene 1: Discovery

A cabal discovers a powerful node that multiple factions want to claim.

Characters: Elena Vasquez, James Chen
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of The Contested Node."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        elena = CharacterModel.objects.get(name="Elena Vasquez")
    except CharacterModel.DoesNotExist:
        elena = None

    try:
        james = CharacterModel.objects.get(name="James Chen")
    except CharacterModel.DoesNotExist:
        james = None

    scene, created = Scene.objects.get_or_create(
        name="Discovery",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 7, 12),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Discovery")
        return scene

    print("  Created Scene: Discovery")

    if elena:
        scene.add_character(elena)
    if james:
        scene.add_character(james)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Underground Seattle. The tunnels beneath Pioneer Square, sealed off
from tourists and forgotten by most of the city. Water drips from ancient
brick, and the air smells of age and secrets.

Elena Vasquez and James Chen have been tracking ley line fluctuations for
a week. Something is happening beneath Seattle - a node is forming, or
perhaps awakening. Either way, the Quintessence readings are off the charts.

The tunnel opens into a chamber that shouldn't exist - a perfect dome of
smooth stone, ancient beyond reckoning. And in its center: a pool of
perfectly still water that glows with soft, pulsing light."""
    )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena steps into the chamber, her breath catching. The resonance
here is... incredible*

"James. Are you seeing this?"

*She kneels at the pool's edge, careful not to touch the water*

/roll 6 7
(Perception + Awareness - reading the Quintessence)

"The Prime flow here is... this isn't a forming node. This is ancient.
Primordial. Something sealed it away centuries ago."

*She looks around the dome*

"Who built this place? And why was it hidden?""""
        )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James runs his hand along the walls, his Virtual Adept senses
parsing the patterns in the stone*

"The architecture doesn't match any style I can identify. Pre-colonial, at
minimum. Maybe pre-human."

*He pulls out a tablet, scanning*

/roll 5 6
(Intelligence + Occult - analyzing the chamber)

"The seal wasn't just physical. Someone wove a pattern into reality itself,
hiding this place from all forms of perception. We only found it because
the seal is failing."

*His expression grows concerned*

"Question is - failing naturally, or being broken from inside?""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The pool's glow intensifies briefly - a pulse of pure Quintessence
that makes both mages' Avatar stir in response. This much raw power, freely
flowing... it's almost intoxicating.

Then the chamber shudders. Dust sifts from the dome's apex. Something is
coming - you can feel it in the resonance, a discordant note cutting through
the pure song of the node.

Footsteps in the tunnel behind you. Multiple sets. And voices - hushed but
urgent, speaking in Latin."""
    )

    if elena:
        scene.add_post(
            character=elena,
            display="Elena Vasquez",
            message="""*Elena's eyes narrow*

"Technocracy wouldn't speak Latin. Which means..."

*She shifts position, putting herself between the entrance and the pool*

/roll 5 6
(Intelligence + Occult - identifying the approaching group)

"Celestial Chorus? No, the resonance is wrong. Too... structured."

*Her hands begin weaving protective patterns in the air*

"James, get ready. Whoever they are, they're not going to be happy to find
us here first.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Three figures enter the chamber. They wear formal robes - an
anachronism in the modern world, but their bearing suggests absolute
confidence in their authority.

The Order of Hermes. House Bonisagus, by their sigils.

The lead figure - an older woman with silver hair and cold eyes - stops
short when she sees the two Tradition mages already present.

"Well. It seems the Chantry's wards were less effective than we believed."

Her gaze moves from Elena to James to the pool.

"This node belongs to House Bonisagus. We have claimed it by right of
discovery and ancient compact. Your presence here is... irregular.""""
        )

    if james:
        scene.add_post(
            character=james,
            display="James Chen",
            message="""*James doesn't lower his tablet, but he does take a careful step
to the side, giving himself room to maneuver*

"With respect, Hermetic, we discovered this node. Your 'wards' kept it
hidden for... what, five hundred years? A thousand? And now that they're
failing, you show up to stake a claim?"

*His voice is polite but firm*

/roll 4 6
(Manipulation + Etiquette - diplomatic deflection)

"Last I checked, the Nine Traditions operate as equals. This node belongs
to whoever can protect it - and right now, that's an open question."

*He glances at Elena*

"Unless there's something in the Protocols I missed about House Bonisagus
owning everything they once lost track of?""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Hermetic's expression flickers - annoyance, perhaps, or grudging
respect for the challenge. Her companions shift, hands moving toward hidden
foci.

"The Protocols are... open to interpretation. But you raise a valid point,
Virtual Adept. Perhaps this matter should be brought before the Council."

She studies the pool again.

"In the meantime, I propose a joint guardianship. None of us leaves, none
of us claims exclusive rights, until the Council decides."

It's a compromise. A reasonable one. But there's something in her eyes that
suggests she's already planning her next move.

[Scene End - Hermetic standoff begins]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
