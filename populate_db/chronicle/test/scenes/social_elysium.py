"""
Social Scene: A Night at Elysium

Vampires gather at the neutral ground for an evening of politics and pleasure.

Characters: Marcus "Shadow" Webb, Victoria Chen, Isabella Santos, Dmitri Volkov
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create the Elysium social scene."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    characters = {}
    for name in ["Marcus 'Shadow' Webb", "Victoria Chen", "Isabella Santos",
                 "Dmitri 'The Bear' Volkov"]:
        try:
            characters[name] = CharacterModel.objects.get(name=name)
        except CharacterModel.DoesNotExist:
            characters[name] = None

    scene, created = Scene.objects.get_or_create(
        name="A Night at Elysium",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 7, 15),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: A Night at Elysium")
        return scene

    print("  Created Scene: A Night at Elysium")

    for char in characters.values():
        if char:
            scene.add_character(char)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Seattle Art Museum, after hours. The Prince has declared Elysium
for the evening - no violence, no powers used in aggression. A rare
chance for the Kindred to mingle without watching their backs.

Classical music plays softly. Blood-wine (actual wine laced with
vitae) circulates among the guests. The great and petty of Seattle's
vampire society exchange pleasantries and veiled insults.

A typical Thursday in undead high society."""
    )

    if characters.get("Victoria Chen"):
        scene.add_post(
            character=characters["Victoria Chen"],
            display="Victoria Chen",
            message="""*Victoria glides through the crowd, stopping to exchange nods
with various Kindred*

"Lovely evening, isn't it? The Prince certainly knows how to
host an event."

*She accepts a glass of blood-wine from a passing server*

"Though I notice the Brujah delegation seems... subdued tonight.
Usually Dmitri has started at least one argument by now."

*She sips, watching the room with calculating eyes*"""
        )

    if characters.get("Dmitri 'The Bear' Volkov"):
        scene.add_post(
            character=characters["Dmitri 'The Bear' Volkov"],
            display="Dmitri Volkov",
            message="""*Dmitri looms near the refreshments, looking uncomfortable in
formal attire*

"I'm not subdued. I'm plotting."

*He doesn't smile, but there's humor in his voice*

"The Toreador primogen has been pushing for expanded hunting
rights in Capitol Hill. I'm deciding whether to argue against
it or let it happen and watch the chaos."

*He drains his blood-wine*

"Politics. I preferred the old days when we just hit things.""""
        )

    if characters.get("Isabella Santos"):
        scene.add_post(
            character=characters["Isabella Santos"],
            display="Isabella Santos",
            message="""*Isabella emerges from examining a painting, her Tremere
robes replaced by an elegant evening dress*

"The old days also had more stake-wielding mobs, Dmitri. I'll
take boardroom maneuvering over burning at the stake."

*She joins the group*

"Besides, politics is just combat with different weapons. You're
better at it than you pretend."

*She glances at Victoria*

"How are things in the Sheriff's domain? I heard there was
excitement at Club Nocturne recently.""""
        )

    if characters.get("Marcus 'Shadow' Webb"):
        scene.add_post(
            character=characters["Marcus 'Shadow' Webb"],
            display="Shadow Webb",
            message="""*Shadow materializes from an actual shadow, making a Toreador
nearby jump*

"Club Nocturne had a pest problem. It's been... addressed."

*He accepts blood-wine, though he doesn't drink it*

"The more interesting question is who's been buying property
in the industrial district. Three warehouses in two months,
all cash, all through shell companies."

*He watches the room*

"Someone's building something. Haven't figured out who yet."

*A slight smile*

"But I'm patient.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The evening progresses. Alliances are tested, gossip is exchanged,
and the endless dance of Kindred politics continues.

No blood is shed. No betrayals occur. For one night, the monsters
pretend to be civilized.

Tomorrow, the masks will slip. But tonight, there is music and
wine and the pleasure of each other's company.

Even the dead need nights like this.

[Scene End]"""
    )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
