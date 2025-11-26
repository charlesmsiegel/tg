"""
The Masquerade Frays - Scene 1: Viral Video

A social media post threatens to expose the Kindred. The Scourge calls for
immediate action.

Characters: Victoria Cross (Toreador), Dmitri Volkov (Brujah)
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of The Masquerade Frays."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Get characters - using names from vampire_characters.py
    try:
        victoria = CharacterModel.objects.get(name="Victoria 'Tori' Chen")
    except CharacterModel.DoesNotExist:
        victoria = None

    try:
        dmitri = CharacterModel.objects.get(name="Dmitri 'The Bear' Volkov")
    except CharacterModel.DoesNotExist:
        dmitri = None

    # Get location
    try:
        location = LocationModel.objects.get(name="The Velvet Room", chronicle=chronicle)
    except LocationModel.DoesNotExist:
        location = None

    scene, created = Scene.objects.get_or_create(
        name="Viral Video",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 4, 8),
            "location": location,
        },
    )

    if not created:
        print("  Scene already exists: Viral Video")
        return scene

    print("  Created Scene: Viral Video")

    if victoria:
        scene.add_character(victoria)
    if dmitri:
        scene.add_character(dmitri)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Velvet Room is a private club in Capitol Hill, known to mortals
as an exclusive art gallery. Tonight, the usual aesthetic appreciation has been
replaced by urgent whispers. The Scourge has called an emergency meeting.

Viktor Kraus stands before a projector screen, his scarred face grim. On the
screen: a paused video from a social media platform. The timestamp reads "Posted
2 hours ago."

"This was uploaded tonight. Thirty thousand views and climbing. Watch."

He hits play. The footage is shaky, clearly from a phone. It shows an alley behind
a nightclub. Two figures - one clearly feeding on the other, face visible in the
streetlight's glow. The victim's expression is one of terror."""
    )

    scene.add_post(
        character=None,
        display="Viktor Kraus (NPC - Sheriff)",
        message="""*The Sheriff pauses the video on the clearest frame of the
feeding Kindred*

"This idiot is Gordon Price. Embraced six months ago. His sire has already been
contacted and is in considerable distress."

*His voice drops to a dangerous growl*

"The Prince wants this contained. The video taken down. The witnesses silenced.
And Gordon brought before him to answer for this violation."

*He looks at the assembled Kindred*

"I need volunteers. People who can work quickly and quietly. There's a mortal who
filmed this. Another who helped it go viral. And a tech platform that's hosting it.
Who's in?""""
    )

    if victoria:
        scene.add_post(
            character=victoria,
            display="Victoria Chen",
            message="""*Victoria studies the frozen frame, her artistic eye picking
out details*

"The location is the Retro Revival on Pike Street. I know the owner - he owes me
several favors."

*She pulls out her phone*

"I can get the club's security footage wiped. That will at least cut off any
additional angles. As for the video itself..."

*She considers*

"I have contacts in the influencer community. Social media manipulation isn't
magic, but the right pressure in the right places can make content... disappear."

/roll 5 6
(Manipulation + Streetwise - assessing the social media angle)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Victoria's assessment is accurate. The video is gaining traction,
but it hasn't hit mainstream media yet. There's a window - perhaps twelve hours -
before it becomes truly uncontrollable.

The original poster is a 22-year-old named Marcus Kim. His profile suggests he's
a regular at the club where the incident occurred. He has no idea what he actually
captured."""
    )

    if dmitri:
        scene.add_post(
            character=dmitri,
            display="Dmitri Volkov",
            message="""*Dmitri cracks his knuckles, the sound echoing in the quiet
room*

"I will find Gordon. He cannot have gone far - he is young and stupid."

*His Russian accent thickens with barely contained anger*

"When I find him, I will bring him to the Prince. In pieces if necessary."

*He looks at the screen*

"The mortal who filmed this. He needs to forget what he saw. I can... persuade
him. If we can find him before dawn."

/roll 4 6
(Wits + Streetwise - tracking Gordon's likely hideouts)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Dmitri knows the habits of young, reckless Kindred. Gordon has
been seen at several underground clubs in the ID district. If he's panicking about
what he's done, he'll be looking for blood to steady his nerves - and he won't be
thinking clearly.

Viktor nods approvingly. "Good. Victoria, handle the digital aspect. Dmitri, bring
me Gordon. I'll deal with the mortal witness personally."

The Sheriff's expression is cold. "We have until dawn. If this video is still
circulating by tomorrow night, the Prince will hold everyone in this room
responsible. Move."

[Scene End - The hunt for Gordon begins]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
