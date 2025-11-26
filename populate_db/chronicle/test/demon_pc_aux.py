"""
Seattle Test Chronicle - Demon PC Auxiliary NPCs

Creates mortal NPCs to support PC Backgrounds like Contacts, Allies, Mentors, Cult, and Followers.
These are owned by the ST and represent the NPCs that PCs interact with through their backgrounds.

Run with: python manage.py shell < populate_db/chronicle/test/demon_pc_aux.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run demon_characters.py first (creates PCs)
"""

from django.contrib.auth.models import User

from characters.models.demon.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.house import DemonHouse
from characters.models.demon.faction import DemonFaction
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_human_stats(human, data):
    """Apply stats to a DtFHuman NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(human, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "empathy", "expression",
                    "intimidation", "intuition", "leadership", "streetwise", "subterfuge",
                    "crafts", "drive", "etiquette", "firearms", "larceny", "melee",
                    "performance", "security", "stealth", "survival", "technology",
                    "academics", "computer", "finance", "investigation", "law",
                    "linguistics", "medicine", "occult", "politics", "religion", "science"]:
        if ability in data:
            setattr(human, ability, data[ability])

    if "willpower" in data:
        human.willpower = data["willpower"]

    human.save()


# =============================================================================
# CONTACT NPCs - Mortals who provide information to demon PCs
# =============================================================================

# Murmur's Contacts (3 dots) - Conspiracy theorist network
MURMUR_CONTACTS = [
    {
        "name": "Stanley 'The Truth' Webber",
        "concept": "Conspiracy podcast host with actual sources",
        "description": "Runs a conspiracy theory podcast that occasionally stumbles onto real supernatural events. "
                       "His network of paranoid listeners has eyes everywhere.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 4, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 3,
        "alertness": 3, "expression": 4, "subterfuge": 2, "computer": 3, "investigation": 4,
        "willpower": 4,
    },
    {
        "name": "Detective Nancy Reyes",
        "concept": "True crime researcher with access to cold case files",
        "description": "Retired detective who now helps amateur investigators. "
                       "Has unofficial access to police databases and a network of active officers.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 3,
        "alertness": 3, "empathy": 3, "streetwise": 3, "investigation": 5, "law": 4,
        "willpower": 5,
    },
    {
        "name": "Marcus 'Deep Web' Chen",
        "concept": "Dark web investigator and information broker",
        "description": "Navigates the dark web's most dangerous corners. "
                       "Trades in secrets that never see the light of day.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 2, "manipulation": 4, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 4,
        "alertness": 3, "subterfuge": 4, "computer": 5, "technology": 4, "investigation": 3,
        "willpower": 5,
    },
]

# Penemue's Contacts (3 dots) - Journalist network
PENEMUE_CONTACTS = [
    {
        "name": "Rachel Torres",
        "concept": "Investigative journalist at major newspaper",
        "description": "Has won awards for exposing corporate corruption. "
                       "Her sources extend into every major Seattle institution.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 4, "intelligence": 4, "wits": 3,
        "alertness": 3, "empathy": 3, "expression": 5, "subterfuge": 3, "investigation": 5, "law": 2,
        "willpower": 5,
    },
    {
        "name": "Jake Morrison",
        "concept": "Documentary filmmaker with a cause",
        "description": "Makes documentaries about social injustice. "
                       "Has access to communities that don't trust mainstream media.",
        "strength": 2, "dexterity": 3, "stamina": 2,
        "charisma": 4, "manipulation": 2, "appearance": 3,
        "perception": 4, "intelligence": 3, "wits": 3,
        "alertness": 3, "empathy": 4, "expression": 4, "drive": 2, "technology": 3, "academics": 2,
        "willpower": 4,
    },
    {
        "name": "Sarah Blackwell",
        "concept": "Whistleblower protection advocate",
        "description": "Helps whistleblowers go public safely. "
                       "Has connections to lawyers, journalists, and safe houses.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 4, "appearance": 3,
        "perception": 3, "intelligence": 4, "wits": 4,
        "empathy": 4, "subterfuge": 4, "law": 4, "politics": 3, "investigation": 2,
        "willpower": 6,
    },
]

# =============================================================================
# ALLY NPCs - Mortals who actively help demon PCs
# =============================================================================

# Abaddon's Ally (1 dot) - Underground vigilante
ABADDON_ALLIES = [
    {
        "name": "Marcus 'Ghost' Williams",
        "concept": "Vigilante who patrols dangerous neighborhoods",
        "description": "Former soldier who protects his community with fists and fear. "
                       "Doesn't ask questions about Abaddon's nature—only cares about results.",
        "strength": 4, "dexterity": 3, "stamina": 3,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 2, "wits": 4,
        "alertness": 4, "athletics": 3, "brawl": 4, "intimidation": 4, "streetwise": 3, "firearms": 3,
        "willpower": 5,
    },
]

# =============================================================================
# MENTOR NPCs - Elder demons who guide PCs
# =============================================================================

MENTOR_DEMONS = [
    {
        "name": "Professor Elijah Crane",
        "host_name": "Professor Elijah Crane",
        "celestial_name": "Samyaza",
        "concept": "Elder Neberu scholar and patient teacher",
        "for_pc": "Arakiel",
        "house": "Neberu",
        "faction": "Reconcilers",
        "description": "A Watcher who has spent centuries observing humanity's progress. "
                       "Now teaches at the university, guiding both mortal students and young demons. "
                       "His patience is legendary—but so is his disappointment when it's tested.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 4,
        "alertness": 3, "awareness": 4, "empathy": 4, "expression": 4,
        "academics": 5, "occult": 5, "science": 4, "investigation": 4,
        "faith": 7, "torment": 3, "willpower": 8,
    },
]

# =============================================================================
# CULT NPCs - Earthbound worshippers
# =============================================================================

# The Resonance - Tech workers experiencing revelatory dreams (for Earthbound)
THE_RESONANCE_CULT = [
    {
        "name": "David Park",
        "concept": "Tech lead who receives 'divine' inspiration in dreams",
        "description": "Senior engineer whose innovations come from dreams he doesn't remember. "
                       "Unknowingly serves the Earthbound's agenda through his creations.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 5, "wits": 3,
        "empathy": 2, "leadership": 2, "computer": 5, "technology": 4, "science": 4,
        "willpower": 4,
    },
    {
        "name": "Jennifer Liu",
        "concept": "AI researcher pushing ethical boundaries",
        "description": "Brilliant researcher whose work edges toward true artificial consciousness. "
                       "The whispers in her sleep guide her toward discoveries she shouldn't make.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 2, "manipulation": 3, "appearance": 3,
        "perception": 4, "intelligence": 5, "wits": 4,
        "alertness": 2, "expression": 2, "computer": 5, "science": 5, "academics": 4,
        "willpower": 5,
    },
]

# The Foundation - Church congregation (unknowing worship)
THE_FOUNDATION_CULT = [
    {
        "name": "Pastor Michael Grant",
        "concept": "Charismatic preacher channeling Earthbound power",
        "description": "Thinks he's doing God's work. The congregation's faith empowers an Earthbound, "
                       "and the Pastor's sermons grow more extreme as the whispers guide him.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 5, "manipulation": 4, "appearance": 3,
        "perception": 3, "intelligence": 3, "wits": 3,
        "empathy": 3, "expression": 5, "leadership": 4, "subterfuge": 2, "religion": 4, "occult": 1,
        "willpower": 5,
    },
    {
        "name": "Sister Mary Catherine",
        "concept": "Devoted nun who experiences visions",
        "description": "Her visions are genuine—but their source is not what she believes. "
                       "Interprets Earthbound communications as messages from God.",
        "strength": 1, "dexterity": 2, "stamina": 3,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 3,
        "awareness": 4, "empathy": 4, "expression": 3, "medicine": 2, "religion": 5, "occult": 2,
        "willpower": 6,
    },
]

# =============================================================================
# FOLLOWER NPCs - Mortals inspired by demons
# =============================================================================

# Verath the Whisper's Followers (1 dot) - Inspired artists
VERATH_FOLLOWERS = [
    {
        "name": "Cassandra Moon",
        "concept": "Performance artist channeling forbidden inspiration",
        "description": "Her art has become darker, more intense since she met Verath. "
                       "Audiences leave her shows changed in ways they can't explain.",
        "strength": 1, "dexterity": 4, "stamina": 2,
        "charisma": 4, "manipulation": 3, "appearance": 4,
        "perception": 4, "intelligence": 3, "wits": 3,
        "empathy": 3, "expression": 5, "subterfuge": 2, "performance": 5, "crafts": 3, "occult": 1,
        "willpower": 4,
    },
]

# Rahab's Followers (1 dot) - Game developers
RAHAB_FOLLOWERS = [
    {
        "name": "Tyler 'Glitch' Martinez",
        "concept": "Game developer creating reality-bending experiences",
        "description": "His games contain hidden patterns that affect players' minds. "
                       "Doesn't fully understand why his designs work—just follows his muse.",
        "strength": 1, "dexterity": 3, "stamina": 2,
        "charisma": 2, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 2, "expression": 3, "computer": 5, "technology": 4, "crafts": 3, "science": 2,
        "willpower": 4,
    },
]


def create_contact_npcs(chronicle, st_user):
    """Create Contact NPCs for demon PCs."""
    print("\n--- Creating Contact NPCs ---")

    all_contacts = [
        ("Murmur", MURMUR_CONTACTS),
        ("Penemue", PENEMUE_CONTACTS),
    ]

    for pc_name, contacts in all_contacts:
        print(f"\nContacts for {pc_name}:")
        for contact_data in contacts:
            human, created = DtFHuman.objects.get_or_create(
                name=contact_data["name"],
                owner=st_user,
                defaults={
                    "concept": contact_data["concept"],
                    "description": contact_data.get("description", ""),
                    "chronicle": chronicle,
                    "npc": True,
                    "status": "App",
                },
            )
            if created:
                apply_human_stats(human, contact_data)
                print(f"  Created: {human.name}")
            else:
                print(f"  Already exists: {human.name}")


def create_ally_npcs(chronicle, st_user):
    """Create Ally NPCs for demon PCs."""
    print("\n--- Creating Ally NPCs ---")

    all_allies = [
        ("Abaddon", ABADDON_ALLIES),
    ]

    for pc_name, allies in all_allies:
        print(f"\nAllies for {pc_name}:")
        for ally_data in allies:
            human, created = DtFHuman.objects.get_or_create(
                name=ally_data["name"],
                owner=st_user,
                defaults={
                    "concept": ally_data["concept"],
                    "description": ally_data.get("description", ""),
                    "chronicle": chronicle,
                    "npc": True,
                    "status": "App",
                },
            )
            if created:
                apply_human_stats(human, ally_data)
                print(f"  Created: {human.name}")
            else:
                print(f"  Already exists: {human.name}")


def create_mentor_npcs(chronicle, st_user):
    """Create Mentor NPCs (elder demons) for demon PCs."""
    print("\n--- Creating Mentor NPCs ---")

    for mentor_data in MENTOR_DEMONS:
        house = DemonHouse.objects.filter(name=mentor_data["house"]).first()
        faction = DemonFaction.objects.filter(name=mentor_data["faction"]).first()

        demon, created = Demon.objects.get_or_create(
            name=mentor_data["host_name"],
            owner=st_user,
            defaults={
                "concept": mentor_data["concept"],
                "description": mentor_data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "house": house,
                "faction": faction,
                "host_name": mentor_data.get("host_name", ""),
            },
        )
        if created:
            # Apply attributes and abilities
            for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                         "appearance", "perception", "intelligence", "wits"]:
                if attr in mentor_data:
                    setattr(demon, attr, mentor_data[attr])

            for ability in ["alertness", "athletics", "awareness", "brawl", "empathy",
                            "expression", "intimidation", "intuition", "leadership",
                            "streetwise", "subterfuge", "crafts", "drive", "etiquette",
                            "firearms", "larceny", "melee", "performance", "security",
                            "stealth", "survival", "technology", "academics", "computer",
                            "finance", "investigation", "law", "linguistics", "medicine",
                            "occult", "politics", "religion", "science"]:
                if ability in mentor_data:
                    setattr(demon, ability, mentor_data[ability])

            if "faith" in mentor_data:
                demon.faith = mentor_data["faith"]
            if "torment" in mentor_data:
                demon.torment = mentor_data["torment"]
            if "willpower" in mentor_data:
                demon.willpower = mentor_data["willpower"]

            demon.save()
            print(f"  Created mentor: {demon.name} (for {mentor_data['for_pc']})")
        else:
            print(f"  Already exists: {demon.name}")


def create_cult_npcs(chronicle, st_user):
    """Create Cult NPCs for Earthbound demons."""
    print("\n--- Creating Cult NPCs ---")

    all_cults = [
        ("The Resonance", THE_RESONANCE_CULT),
        ("The Foundation", THE_FOUNDATION_CULT),
    ]

    for cult_name, members in all_cults:
        print(f"\n{cult_name} cult members:")
        for member_data in members:
            human, created = DtFHuman.objects.get_or_create(
                name=member_data["name"],
                owner=st_user,
                defaults={
                    "concept": member_data["concept"],
                    "description": member_data.get("description", ""),
                    "chronicle": chronicle,
                    "npc": True,
                    "status": "App",
                },
            )
            if created:
                apply_human_stats(human, member_data)
                print(f"  Created: {human.name}")
            else:
                print(f"  Already exists: {human.name}")


def create_follower_npcs(chronicle, st_user):
    """Create Follower NPCs for demon PCs."""
    print("\n--- Creating Follower NPCs ---")

    all_followers = [
        ("Verath the Whisper", VERATH_FOLLOWERS),
        ("Rahab", RAHAB_FOLLOWERS),
    ]

    for pc_name, followers in all_followers:
        print(f"\nFollowers for {pc_name}:")
        for follower_data in followers:
            human, created = DtFHuman.objects.get_or_create(
                name=follower_data["name"],
                owner=st_user,
                defaults={
                    "concept": follower_data["concept"],
                    "description": follower_data.get("description", ""),
                    "chronicle": chronicle,
                    "npc": True,
                    "status": "App",
                },
            )
            if created:
                apply_human_stats(human, follower_data)
                print(f"  Created: {human.name}")
            else:
                print(f"  Already exists: {human.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Demon PC Auxiliary NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_contact_npcs(chronicle, st_user)
    create_ally_npcs(chronicle, st_user)
    create_mentor_npcs(chronicle, st_user)
    create_cult_npcs(chronicle, st_user)
    create_follower_npcs(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Demon auxiliary NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
