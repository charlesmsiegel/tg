"""
Corruption Beneath - Scene 3: Aftermath

The pack deals with the aftermath of the explosion and reports to their sept.

Characters: Runs-Through-Shadows, Storm's Fury
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of Corruption Beneath."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        shadow = CharacterModel.objects.get(name="Runs-Through-Shadows")
    except CharacterModel.DoesNotExist:
        shadow = None

    try:
        storm = CharacterModel.objects.get(name="Storm's Fury")
    except CharacterModel.DoesNotExist:
        storm = None

    try:
        location = LocationModel.objects.get(name="Cascadian Wilderness Caern")
    except LocationModel.DoesNotExist:
        location = None

    scene, created = Scene.objects.get_or_create(
        name="Aftermath",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 5, 4),
            "location": location,
        },
    )

    if not created:
        print("  Scene already exists: Aftermath")
        return scene

    print("  Created Scene: Aftermath")

    if shadow:
        scene.add_character(shadow)
    if storm:
        scene.add_character(storm)

    # =========================================================================
    # POSTS
    # =========================================================================

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The Caern of the Cascadian Wilderness. A place of ancient power,
where the Gauntlet is thin and Gaia's presence can still be felt.

Runs-Through-Shadows and Storm's Fury limp into the heart of the caern,
their wounds slowly healing but the exhaustion of battle still heavy on
their shoulders. The explosion threw them clear - Garou resilience saved
their lives where human fragility ended Cross's.

The sept elders are waiting. Gray-furred wolves, scarred from decades of
warfare against the Wyrm. Their eyes hold neither pity nor congratulation
- only the hard patience of those who have seen too many young warriors
return from battle."""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows shifts to Homid as she approaches the elders. Blood
still stains her clothes - some hers, some not*

"Elders. We bring news from the eastern preserve."

*She keeps her voice steady, despite her exhaustion*

"The corruption was deliberate. Pentex operation. A human servant was
cultivating a Wyrm nexus using industrial waste and ritual magic."

*She pauses*

"Three Black Spiral Dancers guarded the site. They have been dealt with.
The human destroyed herself and the ritual site rather than be captured."

/roll 5 6
(Charisma + Leadership - formal report to sept)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The eldest of the Garou - a massive gray wolf with one milky eye -
shifts to Homid. He's ancient, his human form showing the weight of centuries.
His name is Howls-at-Dawn, and he has led this sept since before any of them
were born.

"You did well to stop the ritual. But you bring troubling news."

He looks at Storm's wounds with the clinical eye of a veteran.

"Pentex grows bolder. Three Dancers committed to guarding a single site?
That speaks of significant investment. They expected us to find it."

His good eye fixes on Shadows.

"What did you learn of their larger plans?"""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm also shifts to Homid, wincing as the transformation
pulls at his healing wounds*

"The human spoke of 'the beginning.' She implied this was one of many such
operations."

*His jaw tightens*

"We should have taken her alive. I failed to-"

*He stops himself*

"The Dancers fought like those with nothing to lose. They were buying time
for the ritual. If we had arrived even an hour later..."

*He shakes his head*

"Pentex is planning something large. The preserve was a test. Or a distraction.""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Howls-at-Dawn nods slowly. The other elders exchange glances -
a silent conversation in the language of pack-bonds and long familiarity.

"You are not wrong to question yourself, Storm's Fury. But you are also not
wrong in what you did. A captured fomor servant tells us only what her
masters allow her to know."

He turns to the gathered sept.

"This news changes our priorities. I am calling a council - all packs will
attend. We must coordinate our response."

He looks back at the two young Garou.

"You have earned rest. But I suspect rest will be in short supply in the
coming days. The Wyrm moves against us with new purpose. We must discover
why - and soon.""""
    )

    if shadow:
        scene.add_post(
            character=shadow,
            display="Runs-Through-Shadows",
            message="""*Shadows bows her head in acknowledgment*

"What would you have us do, elder? Scout other potential sites? Investigate
Pentex's local operations?"

*Her exhaustion is evident, but so is her determination*

"The corruption we stopped had been building for weeks, maybe months. If
there are other such sites..."

*She lets the implication hang*

"We cannot rest while the land bleeds."

/roll 4 6
(Perception + Primal-Urge - sensing the land's pain)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Howls-at-Dawn's expression softens slightly. It's easy to forget,
looking at him, that he was once young and burning with the same fire.

"Your dedication honors Gaia. But a warrior who runs themselves to
exhaustion is no warrior at all. Rest tonight. Let your wounds close fully.
Tomorrow, I will have tasks for you."

He raises a gnarled hand.

"The council will meet at moonrise tomorrow. Attend, and bring your account.
The other packs must hear what you witnessed."

He pauses, then adds: "You have done well, cubs. Remember that, even as the
weight of what comes next settles on your shoulders. This is what it means
to be Garou.""""
    )

    if storm:
        scene.add_post(
            character=storm,
            display="Storm's Fury",
            message="""*Storm straightens, pushing past his pain*

"We will be ready, elder."

*He looks at Shadows, then back at Howls-at-Dawn*

"The Dancers we fought... they were newly turned. Less than a year fallen,
I would guess. That means recruitment. Active conversion."

*His hands clench*

"Someone is building an army. The corruption sites, the new Dancers... it's
all connected."

*He meets the elder's eye*

"When we find them, I want to be there. I want to look into the eyes of
whoever turned those Garou to the Wyrm."

[Scene End - Pack reports to sept]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
