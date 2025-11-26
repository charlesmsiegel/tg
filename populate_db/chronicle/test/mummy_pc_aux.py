"""
Seattle Test Chronicle - Mummy PC Auxiliary NPCs

Creates mortal NPCs to support PC Backgrounds like Contacts, Allies, and cult members.
These are owned by the ST and represent the NPCs that PCs interact with through their backgrounds.

Run with: python manage.py shell < populate_db/chronicle/test/mummy_pc_aux.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run mummy_characters.py first (creates PCs)
"""

from django.contrib.auth.models import User

from characters.models.mummy.mummy import Mummy
from characters.models.mummy.mtr_human import MtRHuman
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_human_stats(human, data):
    """Apply stats to a MtRHuman NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(human, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "empathy", "expression",
                    "intimidation", "leadership", "streetwise", "subterfuge",
                    "crafts", "drive", "etiquette", "firearms", "larceny", "melee",
                    "performance", "security", "stealth", "survival", "technology",
                    "academics", "computer", "enigmas", "finance", "investigation", "law",
                    "linguistics", "medicine", "occult", "politics", "science"]:
        if ability in data:
            setattr(human, ability, data[ability])

    if "willpower" in data:
        human.willpower = data["willpower"]

    human.save()


# =============================================================================
# CONTACT NPCs - Mortals who provide information to mummy PCs
# =============================================================================

# Ankh-ef-en-Khonsu's Contacts (2 dots) - Museum curator network
ANKH_CONTACTS = [
    {
        "name": "Dr. Sarah Mitchell",
        "concept": "Egyptologist with access to private collections",
        "description": "Curator at the Seattle Art Museum. Has connections to private collectors "
                       "and knows when important artifacts change hands. Unknowingly assists the Amenti.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 3,
        "alertness": 2, "empathy": 3, "expression": 3, "etiquette": 3, "academics": 5, "investigation": 3, "occult": 2,
        "willpower": 5,
    },
    {
        "name": "Thomas Blackwood III",
        "concept": "Antiquities dealer with questionable ethics",
        "description": "Deals in artifacts of uncertain provenance. His network extends from Seattle "
                       "to Cairo. Knows which items have 'unusual' histories.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 4, "appearance": 3,
        "perception": 3, "intelligence": 3, "wits": 4,
        "alertness": 3, "empathy": 2, "subterfuge": 4, "etiquette": 3, "finance": 4, "investigation": 3, "law": 2,
        "willpower": 4,
    },
]

# Kherpheres' Contacts (2 dots) - Academic librarian network
KHERPHERES_CONTACTS = [
    {
        "name": "Patricia Chen",
        "concept": "Research librarian with access to rare collections",
        "description": "Works in special collections at the university library. "
                       "Can access manuscripts and texts that most scholars never see.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 3,
        "alertness": 3, "empathy": 2, "expression": 2, "computer": 4, "academics": 5, "investigation": 4, "linguistics": 3,
        "willpower": 5,
    },
    {
        "name": "Dr. Marcus Weber",
        "concept": "Digital humanities professor preserving ancient texts",
        "description": "Leads projects to digitize and preserve ancient manuscripts. "
                       "His work occasionally uncovers texts that connect to Amenti history.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 5, "wits": 3,
        "expression": 3, "computer": 5, "technology": 4, "academics": 5, "investigation": 3,
        "willpower": 5,
    },
]

# Nefertari's Contacts (2 dots) - Financial investigation
NEFERTARI_CONTACTS = [
    {
        "name": "Agent Michael Torres",
        "concept": "FBI financial crimes investigator",
        "description": "Investigates money laundering and financial fraud. Nefertari has provided "
                       "'anonymous tips' that led to major cases. He owes her favors.",
        "strength": 2, "dexterity": 3, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 3, "intimidation": 3, "subterfuge": 3, "firearms": 3, "investigation": 5, "law": 4, "finance": 4,
        "willpower": 6,
    },
    {
        "name": "Adriana Costa",
        "concept": "Forensic accountant who finds what others miss",
        "description": "Runs a small firm specializing in fraud investigation. "
                       "Her analytical skills border on supernatural—she sees patterns others can't.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 2, "manipulation": 3, "appearance": 2,
        "perception": 5, "intelligence": 5, "wits": 4,
        "alertness": 3, "empathy": 2, "computer": 4, "investigation": 5, "finance": 5, "law": 3,
        "willpower": 5,
    },
]

# =============================================================================
# ALLY NPCs - Mortals who actively help mummy PCs
# =============================================================================

# Ramesses-ankh's Allies (1 dot) - MMA community
RAMESSES_ALLIES = [
    {
        "name": "Coach Miguel Rodriguez",
        "concept": "MMA gym owner and mentor figure",
        "description": "Runs a gym where Ramesses trains. Doesn't ask questions about his student's "
                       "'medical condition' but provides a community and purpose.",
        "strength": 3, "dexterity": 3, "stamina": 4,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 2, "wits": 4,
        "alertness": 3, "athletics": 4, "brawl": 5, "empathy": 3, "leadership": 3, "drive": 2, "melee": 2, "medicine": 2,
        "willpower": 6,
    },
]

# Sekhmet-hotep's Allies (2 dots) - Hospice care
SEKHMET_ALLIES = [
    {
        "name": "Dr. Amanda Brooks",
        "concept": "Hospice doctor who understands death's value",
        "description": "Has worked in end-of-life care for twenty years. "
                       "Sees Sekhmet's 'gift' and doesn't question it—only appreciates the peace she brings.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 3,
        "alertness": 3, "awareness": 3, "empathy": 5, "expression": 3, "medicine": 5, "science": 3,
        "willpower": 6,
    },
    {
        "name": "Elena Vasquez",
        "concept": "Hospice social worker and grief counselor",
        "description": "Helps families through the dying process. "
                       "Has noticed that Sekhmet's visits always seem to bring comfort and resolution.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 3, "appearance": 3,
        "perception": 3, "intelligence": 3, "wits": 3,
        "alertness": 2, "awareness": 2, "empathy": 5, "expression": 4, "etiquette": 2, "academics": 2, "medicine": 2,
        "willpower": 5,
    },
]

# =============================================================================
# CULT MEMBER NPCs - Members of the mummy cults
# =============================================================================

# House of Scrolls cult members
HOUSE_OF_SCROLLS_CULT = [
    {
        "name": "Professor David Lin",
        "concept": "Comparative religion scholar initiated into mysteries",
        "description": "Studies ancient religions academically, but has been shown deeper truths. "
                       "Helps preserve and translate texts for the House of Scrolls.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 3,
        "expression": 4, "academics": 5, "investigation": 3, "linguistics": 4, "occult": 4,
        "willpower": 5,
    },
    {
        "name": "Sophia Papadopoulos",
        "concept": "Graduate student who discovered too much",
        "description": "Her research led her to the cult, and they decided to initiate rather than silence. "
                       "Now assists with research and runs errands for the Amenti.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 3,
        "perception": 4, "intelligence": 4, "wits": 3,
        "alertness": 2, "empathy": 2, "expression": 3, "computer": 3, "academics": 4, "investigation": 4, "occult": 3,
        "willpower": 4,
    },
]

# Keepers of Ma'at cult members
KEEPERS_OF_MAAT_CULT = [
    {
        "name": "Judge Helen Martinez",
        "concept": "Retired judge who serves justice beyond the court",
        "description": "Served on the bench for thirty years. Now works with the Keepers "
                       "to ensure true justice when the legal system fails.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 3, "empathy": 3, "expression": 4, "intimidation": 3, "leadership": 3, "law": 5, "investigation": 4, "politics": 3,
        "willpower": 7,
    },
    {
        "name": "Detective James Washington",
        "concept": "Police detective who brings cases to the Keepers",
        "description": "When the system can't deliver justice, he knows who can. "
                       "Brings information about cases that need... alternative resolution.",
        "strength": 3, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 4,
        "alertness": 4, "intimidation": 3, "streetwise": 4, "firearms": 3, "investigation": 5, "law": 3,
        "willpower": 6,
    },
]

# Lions of Sekhmet cult members
LIONS_OF_SEKHMET_CULT = [
    {
        "name": "Victor Romanov",
        "concept": "Former soldier who found purpose in service",
        "description": "Served in multiple conflicts before the Lions found him. "
                       "Now serves as the cult's protector and trainer.",
        "strength": 4, "dexterity": 4, "stamina": 4,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 2, "wits": 4,
        "alertness": 4, "athletics": 4, "brawl": 4, "intimidation": 3, "firearms": 5, "melee": 4, "stealth": 3, "survival": 4,
        "willpower": 6,
    },
    {
        "name": "Dr. Rachel Green",
        "concept": "Combat medic who serves both aspects of Sekhmet",
        "description": "Served as an army doctor. Understands that sometimes healing requires destruction first. "
                       "Provides medical support for the Lions' operations.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 3, "athletics": 2, "empathy": 3, "firearms": 2, "melee": 2, "medicine": 5, "science": 3,
        "willpower": 6,
    },
]


def create_contact_npcs(chronicle, st_user):
    """Create Contact NPCs for mummy PCs."""
    print("\n--- Creating Contact NPCs ---")

    all_contacts = [
        ("Ankh-ef-en-Khonsu", ANKH_CONTACTS),
        ("Kherpheres", KHERPHERES_CONTACTS),
        ("Nefertari", NEFERTARI_CONTACTS),
    ]

    for pc_name, contacts in all_contacts:
        print(f"\nContacts for {pc_name}:")
        for contact_data in contacts:
            human, created = MtRHuman.objects.get_or_create(
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
    """Create Ally NPCs for mummy PCs."""
    print("\n--- Creating Ally NPCs ---")

    all_allies = [
        ("Ramesses-ankh", RAMESSES_ALLIES),
        ("Sekhmet-hotep", SEKHMET_ALLIES),
    ]

    for pc_name, allies in all_allies:
        print(f"\nAllies for {pc_name}:")
        for ally_data in allies:
            human, created = MtRHuman.objects.get_or_create(
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


def create_cult_npcs(chronicle, st_user):
    """Create cult member NPCs for the mummy cults."""
    print("\n--- Creating Cult Member NPCs ---")

    all_cults = [
        ("House of Scrolls", HOUSE_OF_SCROLLS_CULT),
        ("Keepers of Ma'at", KEEPERS_OF_MAAT_CULT),
        ("Lions of Sekhmet", LIONS_OF_SEKHMET_CULT),
    ]

    for cult_name, members in all_cults:
        print(f"\n{cult_name} members:")
        for member_data in members:
            human, created = MtRHuman.objects.get_or_create(
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


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Mummy PC Auxiliary NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_contact_npcs(chronicle, st_user)
    create_ally_npcs(chronicle, st_user)
    create_cult_npcs(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Mummy auxiliary NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
