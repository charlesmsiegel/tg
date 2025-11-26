"""
Seattle Test Chronicle - Hunter PC Auxiliary NPCs

Creates mortal NPCs to support PC Backgrounds like Contacts, Allies, and Resources connections.
These are owned by the ST and represent the NPCs that PCs interact with through their backgrounds.

Run with: python manage.py shell < populate_db/chronicle/test/hunter_pc_aux.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run hunter_characters.py first (creates PCs)
"""

from django.contrib.auth.models import User

from characters.models.hunter.hunter import Hunter
from characters.models.hunter.htrhuman import HtRHuman
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_human_stats(human, data):
    """Apply stats to a HtRHuman NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(human, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "dodge", "empathy",
                    "expression", "intimidation", "intuition", "leadership", "streetwise",
                    "subterfuge", "crafts", "demolitions", "drive", "etiquette",
                    "firearms", "larceny", "melee", "performance", "security", "stealth",
                    "survival", "technology", "academics", "bureaucracy", "computer",
                    "finance", "investigation", "law", "linguistics", "medicine",
                    "occult", "politics", "research", "science"]:
        if ability in data:
            setattr(human, ability, data[ability])

    if "willpower" in data:
        human.willpower = data["willpower"]

    human.save()


# =============================================================================
# CONTACT NPCs - Mortals who provide information to hunter PCs
# =============================================================================

# Jake Mercer's Contacts (3 dots) - Law enforcement and PI network
JAKE_CONTACTS = [
    {
        "name": "Detective Samantha Cross",
        "concept": "Homicide detective who's seen too much",
        "description": "Has worked cases that defy rational explanation. Unofficially shares information "
                       "with Jake when she suspects something supernatural is involved.",
        "strength": 2, "dexterity": 3, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 4, "empathy": 3, "intimidation": 3, "streetwise": 3, "firearms": 3, "investigation": 5, "law": 3,
        "willpower": 6,
    },
    {
        "name": "Tommy 'The Wire' Nguyen",
        "concept": "Surveillance specialist and information broker",
        "description": "Former intelligence contractor who now does private surveillance work. "
                       "Can tap phones, trace IP addresses, and access databases most people don't know exist.",
        "strength": 1, "dexterity": 3, "stamina": 2,
        "charisma": 2, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 3, "subterfuge": 3, "computer": 5, "technology": 5, "security": 4, "investigation": 3,
        "willpower": 5,
    },
    {
        "name": "Maria 'Bail Bonds' Santos",
        "concept": "Bail bondsman with street-level intelligence",
        "description": "Knows everyone in Seattle's criminal justice system. "
                       "Her skip tracers provide information about people who don't want to be found.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 4, "appearance": 2,
        "perception": 3, "intelligence": 3, "wits": 4,
        "alertness": 3, "intimidation": 3, "streetwise": 5, "subterfuge": 3, "investigation": 3, "law": 3,
        "willpower": 5,
    },
]

# Derek Stone's Contacts (3 dots) - Hunter network
DEREK_CONTACTS = [
    {
        "name": "Father Thomas O'Brien",
        "concept": "Catholic priest who knows about the supernatural",
        "description": "Has performed actual exorcisms. Maintains contact with hunters worldwide "
                       "through Church networks. Provides blessed items and spiritual support.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 3,
        "awareness": 4, "empathy": 4, "expression": 3, "leadership": 3, "occult": 5, "academics": 4,
        "willpower": 7,
    },
    {
        "name": "Lena 'Arsenal' Kovacs",
        "concept": "Arms dealer who caters to monster hunters",
        "description": "Supplies specialized ammunition, silver bullets, and other hunter-specific equipment. "
                       "Her workshop produces things you can't find in any store.",
        "strength": 2, "dexterity": 3, "stamina": 2,
        "charisma": 2, "manipulation": 3, "appearance": 2,
        "perception": 3, "intelligence": 4, "wits": 3,
        "alertness": 3, "streetwise": 3, "crafts": 5, "firearms": 4, "melee": 3, "security": 3,
        "willpower": 5,
    },
    {
        "name": "Marcus Webb (The Chronicler)",
        "concept": "Hunter network historian and information hub",
        "description": "Maintains records of hunter activities across the Pacific Northwest. "
                       "When hunters need to know what's been tried before, they call Marcus.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 3,
        "alertness": 3, "empathy": 2, "computer": 4, "research": 5, "occult": 4, "investigation": 4,
        "willpower": 5,
    },
]

# Chris Walker's Contacts (2 dots) - Paranormal investigation community
CHRIS_CONTACTS = [
    {
        "name": "Dr. Elizabeth Moore",
        "concept": "Parapsychologist at the university",
        "description": "Studies supernatural phenomena with scientific methodology. "
                       "Skeptical but open-minded. Her research occasionally turns up genuine evidence.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 3,
        "empathy": 3, "expression": 3, "computer": 3, "technology": 3, "research": 5, "science": 4, "occult": 3,
        "willpower": 5,
    },
    {
        "name": "Kevin 'K-Orb' O'Reilly",
        "concept": "Ghost hunting YouTuber with genuine encounters",
        "description": "Most of his content is entertainment, but occasionally captures real phenomena. "
                       "Has a network of amateur investigators who report unusual activity.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 3, "intelligence": 2, "wits": 3,
        "alertness": 3, "expression": 4, "technology": 4, "computer": 3, "occult": 2, "investigation": 2,
        "willpower": 4,
    },
]

# =============================================================================
# ALLY NPCs - Mortals who actively help hunter PCs
# =============================================================================

# Maria Vasquez's Allies (2 dots) - Healthcare workers
MARIA_ALLIES = [
    {
        "name": "Dr. Robert Chen",
        "concept": "ER doctor who's seen impossible injuries",
        "description": "Has treated wounds that shouldn't exist on humans. "
                       "Helps hunters quietly and provides medical care no questions asked.",
        "strength": 2, "dexterity": 4, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 4,
        "alertness": 3, "empathy": 4, "drive": 2, "medicine": 5, "science": 4,
        "willpower": 6,
    },
    {
        "name": "Nurse Patricia Miller",
        "concept": "Night shift nurse at the county hospital",
        "description": "Works the shift when the strangest cases come in. "
                       "Covers for Maria when she needs to do 'off-the-books' treatment.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 3, "wits": 4,
        "alertness": 3, "empathy": 4, "subterfuge": 2, "medicine": 4, "bureaucracy": 2,
        "willpower": 5,
    },
]

# Yuki Tanaka's Allies (2 dots) - Martial arts community
YUKI_ALLIES = [
    {
        "name": "Sensei Hiroshi Nakamura",
        "concept": "Traditional martial arts master with old knowledge",
        "description": "Teaches traditional Japanese martial arts. His family has hunted oni for generations. "
                       "Doesn't fight anymore but teaches those who do.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 4,
        "alertness": 4, "athletics": 3, "awareness": 3, "empathy": 3, "expression": 3, "brawl": 5, "melee": 4, "occult": 3,
        "willpower": 7,
    },
    {
        "name": "Tommy Chen",
        "concept": "MMA fighter and informal bodyguard",
        "description": "Trains at Yuki's dojo. Doesn't know about the supernatural but is fiercely protective "
                       "of his friends. Will throw down against anyone threatening the community.",
        "strength": 4, "dexterity": 4, "stamina": 4,
        "charisma": 2, "manipulation": 1, "appearance": 3,
        "perception": 3, "intelligence": 2, "wits": 4,
        "alertness": 3, "athletics": 4, "brawl": 5, "dodge": 3, "intimidation": 3, "melee": 2,
        "willpower": 5,
    },
]

# =============================================================================
# FELLOW HUNTER NPCs - Other hunters in the network
# =============================================================================

FELLOW_HUNTERS = [
    {
        "name": "Old Man Peterson",
        "concept": "Retired hunter who runs a safe house",
        "description": "Hunted for forty years before his body gave out. Now runs a safe house "
                       "where injured hunters can recover. Knows more about the supernatural than anyone alive.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 4, "awareness": 4, "empathy": 3, "leadership": 3, "firearms": 3, "survival": 4, "occult": 5, "investigation": 4,
        "willpower": 7,
        "conviction": 3, "vision": 2, "zeal": 1,
    },
    {
        "name": "Sister Catherine",
        "concept": "Ex-nun turned monster hunter",
        "description": "Left the convent after her vision. Now hunts the things that prey on the faithful. "
                       "Her faith is unshakeable and her shotgun is never far away.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 4,
        "alertness": 3, "awareness": 4, "empathy": 3, "expression": 2, "intimidation": 2, "firearms": 3, "melee": 2, "occult": 4, "academics": 3,
        "willpower": 8,
        "conviction": 4, "vision": 1, "zeal": 2,
    },
]


def create_contact_npcs(chronicle, st_user):
    """Create Contact NPCs for hunter PCs."""
    print("\n--- Creating Contact NPCs ---")

    all_contacts = [
        ("Jake Mercer", JAKE_CONTACTS),
        ("Derek Stone", DEREK_CONTACTS),
        ("Chris Walker", CHRIS_CONTACTS),
    ]

    for pc_name, contacts in all_contacts:
        print(f"\nContacts for {pc_name}:")
        for contact_data in contacts:
            human, created = HtRHuman.objects.get_or_create(
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
    """Create Ally NPCs for hunter PCs."""
    print("\n--- Creating Ally NPCs ---")

    all_allies = [
        ("Maria Vasquez", MARIA_ALLIES),
        ("Yuki Tanaka", YUKI_ALLIES),
    ]

    for pc_name, allies in all_allies:
        print(f"\nAllies for {pc_name}:")
        for ally_data in allies:
            human, created = HtRHuman.objects.get_or_create(
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


def create_fellow_hunter_npcs(chronicle, st_user):
    """Create fellow hunter NPCs who support the cell."""
    print("\n--- Creating Fellow Hunter NPCs ---")

    for hunter_data in FELLOW_HUNTERS:
        hunter, created = Hunter.objects.get_or_create(
            name=hunter_data["name"],
            owner=st_user,
            defaults={
                "concept": hunter_data["concept"],
                "description": hunter_data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
            },
        )
        if created:
            # Apply attributes and abilities
            for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                         "appearance", "perception", "intelligence", "wits"]:
                if attr in hunter_data:
                    setattr(hunter, attr, hunter_data[attr])

            for ability in ["alertness", "athletics", "awareness", "brawl", "dodge", "empathy",
                            "expression", "intimidation", "intuition", "leadership", "streetwise",
                            "subterfuge", "crafts", "demolitions", "drive", "etiquette",
                            "firearms", "larceny", "melee", "performance", "security", "stealth",
                            "survival", "technology", "academics", "bureaucracy", "computer",
                            "finance", "investigation", "law", "linguistics", "medicine",
                            "occult", "politics", "research", "science"]:
                if ability in hunter_data:
                    setattr(hunter, ability, hunter_data[ability])

            if "willpower" in hunter_data:
                hunter.willpower = hunter_data["willpower"]
            if "conviction" in hunter_data:
                hunter.conviction = hunter_data["conviction"]
            if "vision" in hunter_data:
                hunter.vision = hunter_data["vision"]
            if "zeal" in hunter_data:
                hunter.zeal = hunter_data["zeal"]

            hunter.save()
            print(f"  Created hunter: {hunter.name}")
        else:
            print(f"  Already exists: {hunter.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Hunter PC Auxiliary NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_contact_npcs(chronicle, st_user)
    create_ally_npcs(chronicle, st_user)
    create_fellow_hunter_npcs(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Hunter auxiliary NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
