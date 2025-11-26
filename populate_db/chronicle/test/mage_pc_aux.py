"""
Seattle Test Chronicle - Mage PC Auxiliary NPCs

Creates mortal, sorcerer, and mage NPCs to support PC Backgrounds like Contacts, Allies, Mentors.
These are owned by the ST and represent the NPCs that PCs interact with through their backgrounds.

Run with: python manage.py shell < populate_db/chronicle/test/mage_pc_aux.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run mage_characters.py first (creates PCs)
"""

from django.contrib.auth.models import User

from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.faction import MageFaction
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_human_stats(human, data):
    """Apply stats to a MtAHuman NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(human, attr, data[attr])

    # Abilities
    for ability in ["alertness", "art", "athletics", "awareness", "brawl", "empathy",
                    "expression", "intimidation", "leadership", "streetwise", "subterfuge",
                    "crafts", "drive", "etiquette", "firearms", "martial_arts", "meditation",
                    "melee", "research", "stealth", "survival", "technology",
                    "academics", "computer", "cosmology", "enigmas", "esoterica",
                    "investigation", "law", "medicine", "occult", "politics", "science"]:
        if ability in data:
            setattr(human, ability, data[ability])

    if "willpower" in data:
        human.willpower = data["willpower"]

    human.save()


# =============================================================================
# CONTACT NPCs - Mortals who provide information to mage PCs
# =============================================================================

# Victor Reyes' Contacts (3 dots)
VICTOR_CONTACTS = [
    {
        "name": "0xGH057",
        "concept": "Anonymous hacker collective leader",
        "description": "Runs a decentralized hacker collective. Never meets in person, "
                       "only communicates through encrypted channels. Has access to corporate secrets.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 1, "manipulation": 4, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 4,
        "computer": 5, "investigation": 3, "technology": 4, "academics": 2,
        "willpower": 6,
    },
    {
        "name": "Kelly Matsuda",
        "concept": "Tech industry whistleblower network coordinator",
        "description": "Former tech worker who now connects whistleblowers with journalists. "
                       "Knows where the bodies are buried at every major tech company.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 3,
        "perception": 3, "intelligence": 4, "wits": 3,
        "empathy": 3, "subterfuge": 3, "computer": 4, "investigation": 4, "law": 2,
        "willpower": 5,
    },
    {
        "name": "Boris 'The Fence' Petrov",
        "concept": "Black market tech dealer",
        "description": "Deals in stolen prototypes, unreleased hardware, and tech that officially doesn't exist. "
                       "His sources include labs that even the Virtual Adepts don't know about.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 4, "appearance": 2,
        "perception": 3, "intelligence": 3, "wits": 4,
        "alertness": 3, "streetwise": 4, "subterfuge": 4, "technology": 3, "investigation": 2,
        "willpower": 5,
    },
]

# Priya Sharma's Contacts (2 dots)
PRIYA_CONTACTS = [
    {
        "name": "Alan Torres",
        "concept": "Tech journalist with ethics",
        "description": "Writes exposes on tech industry abuses. Has sources throughout Silicon Valley "
                       "and is one of the few journalists Priya trusts.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 3,
        "empathy": 2, "expression": 4, "subterfuge": 2, "computer": 3, "investigation": 4,
        "willpower": 5,
    },
    {
        "name": "Dr. Amanda Chen",
        "concept": "University ethics professor",
        "description": "Studies the ethics of technology and AI. Provides academic credibility "
                       "and connections to other concerned academics.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 5, "wits": 3,
        "expression": 3, "academics": 5, "computer": 3, "law": 2, "science": 3,
        "willpower": 5,
    },
]

# Dr. Eleanor Vance's Contacts (2 dots)
ELEANOR_CONTACTS = [
    {
        "name": "Marcus Finch",
        "concept": "Funeral home director with a morbid curiosity",
        "description": "Runs a local funeral home and notices things about bodies that others miss. "
                       "Has helped Eleanor acquire 'research materials' no questions asked.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 2,
        "empathy": 3, "subterfuge": 2, "etiquette": 3, "medicine": 3, "investigation": 2,
        "willpower": 4,
    },
    {
        "name": "Dr. Patricia Holloway",
        "concept": "Hospital pathologist",
        "description": "Works the night shift at the county morgue. Shares Eleanor's clinical fascination "
                       "with death and keeps her informed of unusual cases.",
        "strength": 1, "dexterity": 3, "stamina": 2,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 3,
        "alertness": 2, "empathy": 2, "medicine": 5, "investigation": 3, "science": 4,
        "willpower": 5,
    },
]

# =============================================================================
# ALLY NPCs - Mortals who actively help mage PCs
# =============================================================================

# Dr. Hassan Al-Rashid's Allies (2 dots)
HASSAN_ALLIES = [
    {
        "name": "Imam Yusuf Abdullah",
        "concept": "Mosque leader and community organizer",
        "description": "Leads the local mosque and has deep connections in Seattle's Muslim community. "
                       "Respects Hassan's scholarship and spiritual dedication.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 2, "appearance": 3,
        "perception": 3, "intelligence": 4, "wits": 3,
        "empathy": 4, "expression": 4, "leadership": 3, "etiquette": 3, "academics": 3, "occult": 2,
        "willpower": 6,
    },
    {
        "name": "Fatima Noor",
        "concept": "Community activist and social worker",
        "description": "Works with immigrant families in crisis. Her network extends throughout "
                       "Seattle's diverse communities and she calls on Hassan for spiritual guidance.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 2, "appearance": 3,
        "perception": 3, "intelligence": 3, "wits": 3,
        "empathy": 4, "expression": 3, "streetwise": 3, "politics": 2, "law": 2,
        "willpower": 5,
    },
]

# Iris Quantum's Allies (2 dots)
IRIS_ALLIES = [
    {
        "name": "DJ Lucid",
        "concept": "Rave scene legend and event organizer",
        "description": "Has been throwing underground parties for decades. His events are legendary "
                       "and his crowd includes artists, hackers, and dreamers.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 3, "intelligence": 2, "wits": 4,
        "alertness": 2, "expression": 3, "streetwise": 3, "subterfuge": 2, "art": 4, "technology": 3,
        "willpower": 4,
    },
    {
        "name": "Zara 'Prism' Martinez",
        "concept": "Light artist and installation designer",
        "description": "Creates immersive light installations for events and galleries. "
                       "Her work blurs the line between technology and magic.",
        "strength": 1, "dexterity": 4, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 4,
        "perception": 4, "intelligence": 3, "wits": 3,
        "expression": 4, "crafts": 4, "technology": 4, "art": 4, "science": 2,
        "willpower": 4,
    },
]

# =============================================================================
# MENTOR NPCs - Elder mages who teach PCs
# =============================================================================

MENTOR_MAGES = [
    {
        "name": "Grandmother Crow",
        "concept": "Elder Dreamspeaker and spirit-talker",
        "for_pc": "Samantha Torres",
        "tradition": "Dreamspeakers",
        "description": "Ancient Dreamspeaker who has walked with spirits for over a century. "
                       "Teaches the old ways and maintains connections to the spirit worlds. "
                       "Her body is frail but her spirit is vast.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 5, "intelligence": 4, "wits": 4,
        "alertness": 3, "awareness": 5, "empathy": 4, "expression": 3,
        "cosmology": 5, "occult": 5, "enigmas": 4, "medicine": 3,
        "arete": 6, "willpower": 9,
    },
    {
        "name": "The Gray Man",
        "concept": "Elder Euthanatos who guides the lost",
        "for_pc": "Zero",
        "tradition": "Euthanatos",
        "description": "An elder Euthanatos who has spent decades helping younger mages "
                       "avoid the corruption of the Jhor. His methods are severe but effective. "
                       "He sees something worth saving in Zero.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 2, "manipulation": 3, "appearance": 2,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 4, "awareness": 4, "empathy": 3, "intimidation": 3, "subterfuge": 3,
        "medicine": 4, "occult": 5, "enigmas": 4, "investigation": 3,
        "arete": 5, "willpower": 8,
    },
    {
        "name": "Madame Fortuna",
        "concept": "House Fortunae elder and fortune-teller",
        "for_pc": "Aurora Sinclair",
        "tradition": "Order of Hermes",
        "description": "A House Fortunae master who has manipulated probability for over two centuries. "
                       "Runs a 'fortune-telling' shop that serves as cover for her real work. "
                       "She sees great potential in Aurora—and great danger.",
        "strength": 1, "dexterity": 3, "stamina": 2,
        "charisma": 4, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 3, "awareness": 4, "empathy": 4, "expression": 3, "subterfuge": 4,
        "etiquette": 3, "occult": 5, "enigmas": 4, "academics": 3,
        "arete": 6, "willpower": 9,
    },
]


def create_contact_npcs(chronicle, st_user):
    """Create Contact NPCs for mage PCs."""
    print("\n--- Creating Contact NPCs ---")

    all_contacts = [
        ("Victor Reyes", VICTOR_CONTACTS),
        ("Priya Sharma", PRIYA_CONTACTS),
        ("Dr. Eleanor Vance", ELEANOR_CONTACTS),
    ]

    for pc_name, contacts in all_contacts:
        print(f"\nContacts for {pc_name}:")
        for contact_data in contacts:
            human, created = MtAHuman.objects.get_or_create(
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
    """Create Ally NPCs for mage PCs."""
    print("\n--- Creating Ally NPCs ---")

    all_allies = [
        ("Dr. Hassan Al-Rashid", HASSAN_ALLIES),
        ("Iris Quantum", IRIS_ALLIES),
    ]

    for pc_name, allies in all_allies:
        print(f"\nAllies for {pc_name}:")
        for ally_data in allies:
            human, created = MtAHuman.objects.get_or_create(
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
    """Create Mentor NPCs (elder mages) for mage PCs."""
    print("\n--- Creating Mentor NPCs ---")

    for mentor_data in MENTOR_MAGES:
        mage, created = Mage.objects.get_or_create(
            name=mentor_data["name"],
            owner=st_user,
            defaults={
                "concept": mentor_data["concept"],
                "description": mentor_data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
            },
        )
        if created:
            # Apply attributes and abilities
            for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                         "appearance", "perception", "intelligence", "wits"]:
                if attr in mentor_data:
                    setattr(mage, attr, mentor_data[attr])

            for ability in ["alertness", "art", "athletics", "awareness", "brawl", "empathy",
                            "expression", "intimidation", "leadership", "streetwise", "subterfuge",
                            "crafts", "drive", "etiquette", "firearms", "martial_arts", "meditation",
                            "melee", "research", "stealth", "survival", "technology",
                            "academics", "computer", "cosmology", "enigmas", "esoterica",
                            "investigation", "law", "medicine", "occult", "politics", "science"]:
                if ability in mentor_data:
                    setattr(mage, ability, mentor_data[ability])

            if "arete" in mentor_data:
                mage.arete = mentor_data["arete"]
            if "willpower" in mentor_data:
                mage.willpower = mentor_data["willpower"]

            mage.save()
            print(f"  Created mentor: {mage.name} (for {mentor_data['for_pc']})")
        else:
            print(f"  Already exists: {mage.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Mage PC Auxiliary NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_contact_npcs(chronicle, st_user)
    create_ally_npcs(chronicle, st_user)
    create_mentor_npcs(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Mage auxiliary NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
