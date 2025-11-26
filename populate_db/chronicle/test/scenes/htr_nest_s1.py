"""
Into the Nest - Scene 1: The Missing Students

Hunters investigate disappearances connected to a Seattle nightclub.

Characters: Sarah Mitchell, David Okonkwo
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 1 of Into the Nest."""
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
        name="The Missing Students",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 3, 10),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Missing Students")
        return scene

    print("  Created Scene: The Missing Students")

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
        message="""A cramped apartment near the University of Washington campus. Corkboards
covered with photos, newspaper clippings, and red string connecting patterns
only the initiated can see.

Sarah Mitchell's "war room." Five months ago, she was a graduate student
in forensic psychology. Then her best friend disappeared after a night
at Club Nocturne, a popular downtown venue. The police found nothing.

Sarah found the truth. Or started to.

Six missing students, all last seen at the same club. All written off as
runaways, dropouts, or drug casualties. No bodies. No leads.

Just a pattern that no one else can see."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah pins another photo to the board - victim number seven, reported
missing three days ago*

"University junior. Dean's list. Had a scholarship and a boyfriend who
loved her. Not exactly the profile of someone who just walks away."

*She steps back, studying the pattern*

/roll 5 6
(Intelligence + Investigation - connecting the evidence)

"They're all the same type. Young, healthy, no substance abuse issues.
The kind of people who disappear without a trace..."

*Her voice hardens*

"Because someone TAKES them without a trace."

*She looks at the club's logo on her board*

"Tonight, we go in.""""
        )

    if david:
        scene.add_post(
            character=david,
            display="David Okonkwo",
            message="""*David enters, carrying gear bags filled with surveillance equipment*

"I ran the club through every database I could access. Owner is a shell
company in Delaware. Staff turnover is almost zero - same employees for
fifteen years."

*He sets down the bags*

/roll 5 6
(Intelligence + Computer - presenting research)

"And here's the weird part: health inspection records show the club has
a basement. City permits don't."

*He pulls out blueprints*

"Someone built something down there and paid a lot of money to keep it
off the books."

*He meets Sarah's eyes*

"Whatever's happening to those kids, the answer is underground.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The evidence builds an ugly picture. Club Nocturne isn't just a venue
for bad decisions - it's a hunting ground. Someone's been preying on
young people for over a decade, possibly longer.

The Imbued know what that means. They've seen the signs before.

Vampires.

Not the Hollywood kind. The real kind. The monsters that wear human faces
and treat mortals as livestock.

The police can't help. They're not equipped for this fight. The system
doesn't even acknowledge these things exist.

That's why there are hunters."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah opens one of David's bags, revealing an arsenal of improvised
weapons - stakes, UV flashlights, holy water*

"We've trained for this. We've researched, prepared, planned. But..."

*She hesitates*

/roll 4 6
(Willpower - confronting reality)

"This is real. We're actually going to walk into a vampire nest and try
to save whoever's still alive down there."

*She picks up a stake, testing its weight*

"My Sight's been getting stronger. I see their corruption now - the way
they drain light from the world around them. If there's vampires in that
club, I'll know."

*Her jaw sets*

"And they'll learn there are consequences for taking people I care about.""""
        )

    if david:
        scene.add_post(
            character=david,
            display="David Okonkwo",
            message="""*David nods, his own determination matching hers*

"We go in as clubbers. Observe. Identify the targets. Find the entrance
to that basement."

*He straps on concealed gear*

/roll 5 6
(Wits + Subterfuge - planning infiltration)

"If we find living victims, we extract them first. Take on the vampires
only if we have to."

*He pauses*

"And Sarah - if this goes bad, we retreat. These things are faster and
stronger than us. We win through preparation and surprise, not toe-to-toe
fights."

*He checks his UV flashlight*

"But if we can shut this nest down, save even one person... it's worth
the risk."

[Scene End - Hunters prepare to infiltrate Club Nocturne]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
