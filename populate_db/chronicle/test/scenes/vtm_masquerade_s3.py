"""
The Masquerade Frays - Scene 3: Damage Control

Victoria and Dmitri work to contain the evidence while the Sheriff interrogates Gordon.

Characters: Victoria Chen, Dmitri Volkov
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of The Masquerade Frays."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    try:
        victoria = CharacterModel.objects.get(name="Victoria Chen")
    except CharacterModel.DoesNotExist:
        victoria = None

    try:
        dmitri = CharacterModel.objects.get(name="Dmitri 'The Bear' Volkov")
    except CharacterModel.DoesNotExist:
        dmitri = None

    scene, created = Scene.objects.get_or_create(
        name="Damage Control",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 4, 9),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: Damage Control")
        return scene

    print("  Created Scene: Damage Control")

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
        message="""The Elysium's private study. Victoria has been working for six hours
straight, laptop screens casting blue light across her face. Coffee cups litter
the desk - a human habit she never quite abandoned.

Dmitri enters, dried blood on his knuckles. He drops into a leather chair."""
    )

    if dmitri:
        scene.add_post(
            character=dmitri,
            display="Dmitri Volkov",
            message="""*Dmitri examines his hands with distaste*

"Gordon is with the Sheriff now. The little fool was actually relieved to be
caught - thought we were going to kill him on the spot."

*He looks up at Victoria*

"What is the damage?"""
        )

    if victoria:
        scene.add_post(
            character=victoria,
            display="Victoria Chen",
            message="""*Victoria turns one of the laptops to face Dmitri. Multiple windows
show social media posts, news articles, comment sections*

"Significant but contained. The video was uploaded to TikTok, Instagram, and
Twitter. Total view count before I got it pulled: approximately 47,000."

*She scrolls through data*

"The good news: it was dark, grainy, Gordon's face isn't clearly visible. Most
comments are calling it fake - 'obvious editing,' 'promotional stunt,' the
usual skeptic noise."

/roll 6 6
(Intelligence + Computer - analyzing spread patterns)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""Victoria's analysis is thorough. The video spread in predictable
patterns - first to the original poster's followers, then picked up by a few
paranormal interest accounts. Most mainstream users scrolled past.

But three accounts stood out as anomalies. They saved the video, shared it to
private groups, and their posting history suggests they take supernatural
claims seriously."""
    )

    if victoria:
        scene.add_post(
            character=victoria,
            display="Victoria Chen",
            message="""*Victoria highlights the three accounts*

"These worry me. @SeattleTruthSeeker, @NightWatcher206, and @UrbanLegendHunter.
All three have histories of investigating... unusual occurrences in the city."

*She pulls up more data*

"The first two appear to be standard conspiracy theorists. The third..."

*She frowns*

"@UrbanLegendHunter has posted content that's concerningly accurate. References
to 'night predators,' knowledge of Rack locations, even speculation about Elysium."

/roll 5 7
(Intelligence + Investigation - profiling the accounts)"""
        )

    if dmitri:
        scene.add_post(
            character=dmitri,
            display="Dmitri Volkov",
            message="""*Dmitri leans forward, suddenly interested*

"A hunter? Or just a very observant mortal?"

*His eyes narrow*

"Either way, they know too much. We cannot leave this thread dangling."

*He stands, pacing*

"The Prince will want options. Can you trace these accounts to real identities?"""
        )

    if victoria:
        scene.add_post(
            character=victoria,
            display="Victoria Chen",
            message="""*Victoria's fingers fly across the keyboard*

"Already working on it. The first two use VPNs, but inconsistently. I can
probably trace them within 24 hours."

*She pauses, studying the third account*

"@UrbanLegendHunter is more careful. Dedicated VPN, no personal information in
any posts, account created from a public library computer three years ago."

*She looks at Dmitri*

"This one knows tradecraft. That suggests either law enforcement background,
military intelligence, or..."

/roll 7 7
(Manipulation + Computer - attempting trace)"""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The trace hits a wall. Whoever runs @UrbanLegendHunter has the
technical skills to remain anonymous. Every avenue Victoria tries leads to
dead ends or red herrings.

Then her phone buzzes. A direct message from the account in question:

"I know what you are. I know what you're doing. I'm not your enemy - but I
could be. We should talk. Somewhere public. Tomorrow night."

The message is followed by an address: Pike Place Market, 10 PM."""
    )

    if victoria:
        scene.add_post(
            character=victoria,
            display="Victoria Chen",
            message="""*Victoria stares at the screen, her composure finally cracking*

"That's... not possible. I was using secure protocols. There's no way they
should have been able to trace me back."

*She shows the message to Dmitri*

"They know. And they want to meet."

*Her voice is carefully controlled*

"This could be a trap. But if they wanted to expose us, they've had
opportunities. They're reaching out instead. That suggests negotiation, not
confrontation.

"What do I tell the Prince?"""
        )

    if dmitri:
        scene.add_post(
            character=dmitri,
            display="Dmitri Volkov",
            message="""*Dmitri reads the message twice, his expression unreadable*

"Tell her the truth. We have contained most of the breach, but we have
uncovered a larger problem. Someone in this city knows about us - and they
are sophisticated enough to be dangerous."

*He cracks his knuckles*

"I will attend this meeting with you. If it is a trap, better two of us than
one. If it is genuine..."

*A grim smile*

"Then we will learn what this mortal wants. Everyone wants something."

*He moves toward the door*

"Get some rest, Victoria. You will need your wits about you tomorrow."

[Scene End - Meeting arranged with mysterious hunter]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
