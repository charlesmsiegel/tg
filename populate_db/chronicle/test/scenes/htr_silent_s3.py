"""
The Silent Cell - Scene 3: The Exorcism

The hunters battle the entity controlling Western State.

Characters: Sarah Mitchell, David Okonkwo
"""

from datetime import date

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


def populate_scene():
    """Create Scene 3 of The Silent Cell."""
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
        name="The Exorcism",
        chronicle=chronicle,
        defaults={
            "date_of_scene": date(2022, 8, 17),
            "location": None,
        },
    )

    if not created:
        print("  Scene already exists: The Exorcism")
        return scene

    print("  Created Scene: The Exorcism")

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
        message="""The therapy room. Once a place of supposed healing, now a throne
room for something that was never healed at all.

Dr. Werner Holtz. He died in 1952, officially from a heart attack.
Unofficially, one of his "patients" strangled him with a therapy
strap. His body was buried, but his spirit never left.

Decades of feeding on the hospital's misery transformed him. He's
no longer a ghost - he's a revenant, a thing of pure will and
malice, sustained by the suffering he causes.

And he's discovered that hunters are special. Their Sight, their
abilities, their connection to something greater - he wants it.
He's been draining Sigma Cell for two weeks, trying to steal what
makes them different."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah faces the revenant, her Sight burning*

"You're not a doctor anymore, Holtz. You're just another monster
wearing a human memory."

*She raises her iron knife*

/roll 6 7
(Willpower - resisting the revenant's influence)

#WP

*The revenant's presence pushes against her mind, trying to find
weaknesses*

"I see what you are. A bully who died and kept on bullying. Well,
class is over."

*She hurls a vial of holy water*

"Get away from those people!""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The holy water hits Holtz and he SCREAMS. His form wavers -
beneath the doctor's facade, something twisted and hungry writhes.

But he doesn't run. Instead, he gestures, and the hospital's
ghosts flood into the room. Hundreds of them, all the patients
he's enslaved over decades, now turned into weapons.

"You think you're special?" Holtz snarls. "You're just meat with
delusions. I'll add you to my collection, and nobody will ever
know what happened here."

The ghosts attack. Not one or two, but dozens at once, tearing
at the hunters with spectral hands."""
    )

    if david:
        scene.add_post(
            character=david,
            display="David Okonkwo",
            message="""*David fires salt rounds into the swarm of ghosts, dispersing
them temporarily*

"There's too many! We can't fight them all!"

*He spots something - Father Brennan's hand, twitching*

/roll 5 6
(Perception + Alertness - noticing the opening)

"Sarah! Sigma Cell - they're still fighting! Brennan's got his
rosary, he's trying to wake up!"

*He throws a bag of iron filings at David, creating a circle of
protection around the catatonic hunters*

"If we can break Holtz's hold on them, they can help us!"

*He starts dragging the hunters together*

"Keep him busy!""""
        )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah charges directly at Holtz, iron knife flashing*

"You want special? I'll show you special!"

*She channels everything she has into her Second Sight, seeing
not just the revenant but the chains binding the enslaved ghosts*

/roll 7 6
(Perception + Occult - finding the binding)

"I see it! The bonds - you're not just controlling them, you're
FEEDING on them! They're prisoners too!"

*She turns to the ghosts*

"You don't have to serve him! HE'S the one who hurt you, who USED
you! Fight back!"

*Her words carry the force of Imbued conviction*

"BE FREE!""""
        )

    scene.add_post(
        character=None,
        display="Storyteller",
        message="""The effect is immediate.

The enslaved ghosts hesitate. For a century, they've been Holtz's
slaves - but they remember. They remember the treatments, the
experiments, the pain. And now someone's offering them a choice.

They turn on their master.

Holtz screams as his own victims tear at him. His carefully
constructed dominion crumbles in seconds. The ghosts flood into
him, pulling him apart from within.

Behind David, Father Brennan snaps awake, rosary blazing with
faith. "In nomine Patris et Filii et Spiritus Sancti..."

The exorcism prayer joins Sarah's conviction. Holtz's form begins
to dissolve, pulled toward whatever waits for a soul that's
committed his crimes."""
    )

    if sarah:
        scene.add_post(
            character=sarah,
            display="Sarah Mitchell",
            message="""*Sarah drives her iron knife into Holtz's dissolving form*

"This is for everyone you hurt. Every patient. Every ghost. Every
hunter."

/roll 6 6
(Strength + Melee - delivering the final blow)

*The revenant's scream echoes through the hospital - and cuts off*

*The spiritual pressure lifts. The temperature rises. The ghosts
begin to fade, finally at peace*

*Sarah slumps against a wall*

"It's over."

*She looks at Sigma Cell, now stirring to consciousness*

"Let's get our people out of here. This place can rot."

*Through the window, the first stars are appearing*

*Behind them, Western State Hospital is finally, truly empty.*

[Scene End - Revenant destroyed, hunters rescued]"""
        )

    scene.finished = True
    scene.save()

    print(f"    Added {scene.total_posts()} posts to scene")
    return scene


if __name__ == "__main__":
    populate_scene()
