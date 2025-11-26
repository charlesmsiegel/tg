"""
Blood in the Water - Scene 1: The Informant's Warning

A Nosferatu information broker brings word of unusual activity in the blood trade.
Shadow Webb meets with coterie members to investigate.

Characters: Marcus 'Shadow' Webb, Isabella Santos, Roland Cross
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of Blood in the Water."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Get characters by name
    shadow = CharacterModel.objects.get(name="Marcus 'Shadow' Webb")
    isabella = CharacterModel.objects.get(name="Isabella Santos")
    roland = CharacterModel.objects.get(name="Roland Cross")

    # Get location
    try:
        location = LocationModel.objects.get(name="The Underground", chronicle=chronicle)
    except LocationModel.DoesNotExist:
        location = None

    # Create the scene
    scene, created = Scene.objects.get_or_create(
        name="The Informant's Warning",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 3, 15),
            "location": location,
        },
    )

    if not created:
        print("  Scene already exists: The Informant's Warning")
        return scene

    print("  Created Scene: The Informant's Warning")

    # Add characters to scene
    scene.add_character(shadow)
    scene.add_character(isabella)
    scene.add_character(roland)

    # =========================================================================
    # POSTS - Simulating gameplay
    # =========================================================================

    # ST sets the scene
    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The tunnels beneath Seattle's Pioneer Square district twist and turn
in ways that defy the city's carefully maintained maps. Here, in the domain of the
Nosferatu, Shadow Webb has called a meeting.

The chamber is a repurposed maintenance hub, cables and pipes running along the ceiling
like the veins of some great beast. Several monitors cast their blue glow across the
space, displaying feeds from cameras scattered throughout the city.

Shadow Webb waits in the center, his grotesque features partially hidden in the shadows
he favors. Two of his contacts have arrived - Isabella Santos of the Tremere and Roland
Cross, the Malkavian prophet."""
    )

    # Shadow's opening
    scene.add_post(
        character=shadow,
        display="Shadow Webb",
        message="""*The Nosferatu's voice is a raspy whisper, barely louder than the
humming of the equipment around him*

"Thank you for coming. I know the tunnels aren't... comfortable for everyone."

*He gestures to a monitor showing a grainy feed of a warehouse district*

"Three nights ago, one of my ghouls spotted something unusual at this location. A
delivery - refrigerated trucks, heavy security, and a buyer who paid in gold coins
dated to the 1850s."

*His lips peel back in what might be a smile*

"Someone's moving blood. A lot of it. And they're being very, very careful about who
knows.""""
    )

    # Isabella responds
    scene.add_post(
        character=isabella,
        display="Isabella Santos",
        message="""*Isabella adjusts her glasses, studying the monitor with scholarly interest*

"Gold coins from the 1850s? That's... peculiar. The Kindred presence in Seattle wasn't
established until later. Someone with deep pockets and a sense of history."

*She pulls out a small notebook*

"What kind of blood are we talking about? Bagged from blood banks, or something more...
specialized?"

/roll 5 6
(Intelligence + Occult to recognize any significance in the payment method)"""
    )

    # ST resolves Isabella's roll
    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Isabella's knowledge of occult history triggers a memory - gold coins
from that era were sometimes used by the Sabbat during their western expansion. But
that doesn't quite fit. The Sabbat aren't known for subtlety.

There's another possibility. Some of the older Kindred, particularly those who remember
the chaos of frontier nights, sometimes hoard such currency as a hedge against the
modern financial system's... instability."""
    )

    # Shadow provides more info
    scene.add_post(
        character=shadow,
        display="Shadow Webb",
        message="""*Shadow taps a few keys, bringing up more footage*

"The blood's from multiple sources. Hospital supplies, blood banks, even some direct
harvesting - my people found evidence of a blood den in Rainier Valley that was...
recently vacated."

*His expression darkens*

"But here's what concerns me. The quantity. We're talking hundreds of pints. That's
more than feeding. That's either an army..."

*He pauses*

"...or a ritual.""""
    )

    # Roland speaks
    scene.add_post(
        character=roland,
        display="Roland Cross",
        message="""*Roland has been staring at a fixed point in the air, but now he turns
his attention to the others, his eyes distant*

"The threads are tangled. I see... a red tide rising. Not water. Not rain."

*He blinks, coming back to himself slightly*

"Something old is stirring. I've been having the dreams again - the ones with the
hungry void. Someone is feeding something that should stay asleep."

*He taps his temple*

"The Cobweb whispers of a name. 'Arterius.' Does that mean anything to either of you?"

/roll 6 8
(Auspex - reading the psychic impressions in the room)"""
    )

    # ST resolves Roland's insight
    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Roland's Malkavian insight pierces the veil of mundane perception. For
a moment, he sees the threads of blood that connect this place to the wider city - and
one thread, thicker and darker than the others, leads toward the waterfront.

The name 'Arterius' echoes in his mind, but its full meaning remains frustratingly
unclear. What he does sense is age - whoever or whatever bears that name has existed
for a very, very long time."""
    )

    # Isabella reacts
    scene.add_post(
        character=isabella,
        display="Isabella Santos",
        message="""*Isabella's pen stops mid-note*

"Arterius. That's... I need to check the chantry's records. There's a reference
somewhere - I've seen it, but I can't quite..."

*She frowns, frustrated*

"If we're dealing with something ancient and hungry, the Tremere need to be informed.
Regent Richter will want to know about any potential blood magic being practiced
outside the Pyramid's purview."

*She looks at Shadow*

"Can you get me copies of those surveillance feeds? And the location of that blood den?""""
    )

    # Shadow agrees
    scene.add_post(
        character=shadow,
        display="Shadow Webb",
        message="""*Shadow nods slowly*

"I'll have the data sent to a secure drop. You'll find it tomorrow night."

*He glances between the two*

"I suggest we keep this between us for now. If word gets back to whoever is running
this operation, they'll go to ground. And if the Prince finds out we're investigating
without his knowledge..."

*He shrugs, a disturbing motion given his physique*

"Well. Let's just say I'd rather present him with answers than questions."

/roll 4 6
(Manipulation + Subterfuge - convincing them to keep quiet)"""
    )

    # Resolution
    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The three Kindred come to an uneasy agreement. Shadow will continue
gathering intelligence from his network, Isabella will research the name 'Arterius' in
the Tremere archives, and Roland will attempt to focus his visions on the source of
the disturbance.

As Isabella and Roland prepare to leave through separate exit routes, Shadow's monitors
flicker briefly. For just a moment, one of the warehouse cameras shows a figure
standing in the shadows - watching.

Then the image returns to normal, and Shadow is left wondering if it was a glitch...
or a warning.

[Scene End - To be continued in Scene 2: The Chantry's Secrets]"""
    )

    # Close the scene
    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
