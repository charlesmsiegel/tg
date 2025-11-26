"""
The Silent Cell - Scene 1: Missing Hunters

A cell of hunters has gone dark, and Sarah and David investigate.

Characters: Sarah Mitchell, David Okonkwo
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of The Silent Cell."""
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
        name="Missing Hunters",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 8, 15),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Missing Hunters")
        return scene

    print("  Created Scene: Missing Hunters")

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
        message="""The hunter network is small, scattered, operating in cells that rarely
meet face-to-face. Communication happens through encrypted channels,
dead drops, and the occasional carefully arranged rendezvous.

Sigma Cell was one of the good ones. Three experienced hunters based
out of Tacoma, specializing in ghost hunting and spirit cleansing.
They'd been operating for twelve years. Solid, reliable, professional.

Two weeks ago, they went dark. No check-ins. No responses to messages.
No activity on any of their channels.

Hunters don't just disappear. Either they're dead, compromised, or
something worse.

Time to find out which."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah reviews the case file David assembled*

"Sigma Cell's last known operation was investigating hauntings at an
abandoned psychiatric hospital in Steilacoom. Western State Hospital."

*She pulls up photos*

/roll 5 6
(Intelligence + Investigation - reviewing evidence)

"They checked in when they arrived on site, reported 'significant
spiritual activity,' and then... nothing. That was August 1st."

*Her brow furrows*

"I've heard of Western State. It was notorious - over a century of
mental patients, experimental treatments, deaths. If there's a haunted
building in Washington, that's the one."

*She looks at David*

"Something in there was strong enough to take out three experienced
hunters. We need to know what we're walking into.""""
        )

    if david:
        scene.add_post(
            character=david,
            display="David Okonkwo",
            message="""*David spreads research across the table*

"Western State operated from 1871 to 1973. At its peak, it housed
over 2,700 patients. The death toll..."

*He hesitates*

/roll 5 6
(Intelligence + Occult - analyzing the location)

"Over 3,000 documented deaths on the grounds. Mass graves. Experimental
lobotomies. Electroshock therapy. The kind of suffering that leaves
marks."

*He pulls up Sigma Cell's last transmission*

"Listen to this: 'The main building is saturated. Something's organizing
the spirits. Not random haunting - directed. Like they're being USED.'"

*He meets Sarah's eyes*

"Something's controlling the ghosts. Weaponizing them. Sigma Cell
walked into a trap.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The implications are clear. Whatever haunts Western State Hospital
isn't just a collection of restless dead. It's been organized, shaped
into something more dangerous.

That takes power. Intelligence. Will.

Something living has made that place its domain. Or something that
was once living and decided death was just a career change.

Sigma Cell - Marcus, Yuki, and old Father Brennan - walked in
prepared for ghosts. They got something much worse.

The question: are they dead? Or are they still in there, trapped
in a hospital that never closes?"""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah makes her decision*

"We go. But we go smart."

*She starts planning*

/roll 5 6
(Wits + Survival - tactical planning)

"Daylight insertion. Ghosts are weaker during the day - whatever's
commanding them probably is too. We take iron, salt, everything
that disrupts spiritual manifestation."

*She marks up a map of the hospital*

"Primary objective: find Sigma Cell. Secondary: identify what's
controlling the site. Tertiary..."

*She hesitates*

"Tertiary: if our people are dead, we put them to rest properly.
Hunters don't become the monsters they fight."

*Her voice hardens*

"No one gets left behind.""""
        )

    if david:
        scene.add_post(
            character=david,
            display="David Okonkwo",
            message="""*David nods*

"I'll get the gear together. Salt rounds, iron filings, EMF
detectors. And our backup call system - if we go dark, the network
sends in the cavalry."

*He pauses*

/roll 4 6
(Wits + Investigation - considering possibilities)

"Sarah, one thing. What if Sigma Cell isn't dead? What if they've
been... turned? Possessed? Made part of whatever's there?"

*He doesn't flinch from the hard question*

"Can you put down a friend if we have to? Because I need to know
before we go in."

*The question hangs in the air*

"I'm not asking if you're willing. I'm asking if you're able."

[Scene End - Investigation into missing hunters begins]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
