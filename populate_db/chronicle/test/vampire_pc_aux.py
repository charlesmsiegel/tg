"""
Seattle Test Chronicle - Vampire PC Auxiliary NPCs

Creates mortal and vampire NPCs to support PC Backgrounds like Contacts, Allies, Mentors, Herd.
These are owned by the ST and represent the NPCs that PCs interact with through their backgrounds.

Run with: python manage.py shell < populate_db/chronicle/test/vampire_pc_aux.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run vampire_characters.py first (creates PCs)
"""

from django.contrib.auth.models import User

from characters.models.vampire.vampire import Vampire
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.sect import VampireSect
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_human_stats(human, data):
    """Apply stats to a VtMHuman NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(human, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "empathy", "expression",
                    "intimidation", "leadership", "streetwise", "subterfuge",
                    "crafts", "drive", "etiquette", "firearms", "melee", "performance",
                    "larceny", "stealth", "survival", "technology",
                    "academics", "computer", "finance", "investigation", "law",
                    "linguistics", "medicine", "occult", "politics", "science"]:
        if ability in data:
            setattr(human, ability, data[ability])

    if "willpower" in data:
        human.willpower = data["willpower"]

    human.save()


# =============================================================================
# CONTACT NPCs - Mortals who provide information to PCs
# =============================================================================

# Marcus "Shadow" Webb's Contacts (3 dots worth)
MARCUS_CONTACTS = [
    {
        "name": "Derek 'Zero-Day' Chen",
        "concept": "Underground hacker and exploit dealer",
        "description": "Former security researcher who went rogue. Trades zero-day exploits and hacked data. "
                       "Operates out of basement server farms across Seattle. Paranoid but useful.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 1, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 3,
        "computer": 5, "investigation": 3, "technology": 4, "larceny": 2,
        "willpower": 5,
    },
    {
        "name": "Tanya Volkova",
        "concept": "Tech industry insider and corporate spy",
        "description": "Works in HR at a major tech company but really sells hiring data, "
                       "salary information, and corporate secrets to the highest bidder.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 4, "appearance": 3,
        "perception": 3, "intelligence": 3, "wits": 3,
        "empathy": 3, "subterfuge": 4, "computer": 3, "etiquette": 2, "finance": 3,
        "willpower": 4,
    },
    {
        "name": "Marcus 'Slim' Williams",
        "concept": "Street-level fixer and information broker",
        "description": "Runs a pawn shop in Capitol Hill that's really a clearinghouse for stolen goods "
                       "and criminal connections. Knows everyone who operates on the wrong side of the law.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 3, "intelligence": 2, "wits": 4,
        "alertness": 3, "streetwise": 4, "subterfuge": 3, "larceny": 2, "finance": 2,
        "willpower": 4,
    },
]

# Roland Cross's Contacts (2 dots worth)
ROLAND_CONTACTS = [
    {
        "name": "Darren Webb",
        "concept": "Conspiracy podcast host",
        "description": "Hosts 'The Seattle Shadow Hour' podcast. Dismisses most theories as nonsense "
                       "but has accidentally stumbled onto real supernatural events several times.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 3, "wits": 3,
        "expression": 3, "investigation": 3, "computer": 2, "technology": 2,
        "willpower": 4,
    },
    {
        "name": "Linda Chen",
        "concept": "Retired journalist with sources everywhere",
        "description": "Covered local news for 30 years. Now 'retired' but still cultivates sources "
                       "in city hall, the police, and every major institution. Roland's most reliable contact.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 2,
        "perception": 4, "intelligence": 3, "wits": 3,
        "empathy": 3, "expression": 3, "investigation": 4, "politics": 3, "law": 2,
        "willpower": 5,
    },
]

# Viktor Krueger's Contacts (2 dots worth)
VIKTOR_CONTACTS = [
    {
        "name": "Tony Mazzetti",
        "concept": "Union steward and labor organizer",
        "description": "Represents dock workers and knows everything happening at the ports. "
                       "Suspicious of corporate power and sympathetic to Viktor's cause.",
        "strength": 3, "dexterity": 2, "stamina": 3,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 2, "intelligence": 2, "wits": 3,
        "brawl": 2, "intimidation": 2, "leadership": 3, "streetwise": 2, "politics": 2,
        "willpower": 5,
    },
    {
        "name": "Carmen Ortiz",
        "concept": "Immigrant rights advocate",
        "description": "Works at a nonprofit supporting immigrant workers. Has connections throughout "
                       "Seattle's working-class immigrant communities. Trusts Viktor.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 4, "manipulation": 2, "appearance": 3,
        "perception": 3, "intelligence": 3, "wits": 3,
        "empathy": 4, "expression": 3, "streetwise": 2, "law": 2, "politics": 2,
        "willpower": 5,
    },
]

# =============================================================================
# ALLY NPCs - Mortals who actively help PCs
# =============================================================================

# Roland Cross's Ally (1 dot)
ROLAND_ALLIES = [
    {
        "name": "Pete Kowalski",
        "concept": "True believer in Roland's visions",
        "description": "Former accountant who lost his job after claiming to see 'impossible things'. "
                       "One of the few mortals who takes Roland's prophecies seriously. Devoted helper.",
        "strength": 2, "dexterity": 2, "stamina": 2,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 3, "wits": 2,
        "alertness": 2, "investigation": 2, "computer": 3, "finance": 4, "academics": 2,
        "willpower": 4,
    },
]

# Viktor Krueger's Allies (3 dots worth)
VIKTOR_ALLIES = [
    {
        "name": "Maria Santos",
        "concept": "Union activist and organizer",
        "description": "Fearless union organizer who's been arrested at protests. "
                       "Doesn't know Viktor's nature but would die for the cause.",
        "strength": 2, "dexterity": 2, "stamina": 3,
        "charisma": 4, "manipulation": 2, "appearance": 2,
        "perception": 2, "intelligence": 3, "wits": 3,
        "empathy": 2, "expression": 4, "leadership": 3, "streetwise": 2, "politics": 3,
        "willpower": 6,
    },
    {
        "name": "James 'Big Jim' O'Brien",
        "concept": "Retired longshoreman and mentor",
        "description": "Worked the docks for 40 years. Now advises younger workers and Viktor. "
                       "His word carries weight throughout Seattle's labor community.",
        "strength": 3, "dexterity": 1, "stamina": 3,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 3, "intelligence": 2, "wits": 3,
        "brawl": 3, "intimidation": 2, "leadership": 2, "streetwise": 3, "crafts": 3,
        "willpower": 6,
    },
    {
        "name": "Sarah Mitchell",
        "concept": "Labor lawyer and advocate",
        "description": "Pro bono lawyer who represents workers in disputes. "
                       "Provides legal cover for Viktor's more aggressive organizing tactics.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 3, "appearance": 3,
        "perception": 3, "intelligence": 4, "wits": 3,
        "empathy": 2, "expression": 3, "subterfuge": 2, "law": 5, "politics": 3,
        "willpower": 5,
    },
]

# Diana Cross's Allies (2 dots worth)
DIANA_ALLIES = [
    {
        "name": "Jake Morrison",
        "concept": "Wilderness guide and survivalist",
        "description": "Runs backcountry tours in the Cascades. Knows every trail and hidden spot. "
                       "Helped Diana when she first arrived in Seattle.",
        "strength": 3, "dexterity": 3, "stamina": 3,
        "charisma": 2, "manipulation": 1, "appearance": 2,
        "perception": 4, "intelligence": 2, "wits": 3,
        "alertness": 3, "athletics": 3, "survival": 4, "drive": 2, "firearms": 2,
        "willpower": 5,
    },
    {
        "name": "Nancy Clearwater",
        "concept": "Wildlife biologist and nature advocate",
        "description": "Studies predator populations in the Pacific Northwest. "
                       "Unknowingly provides Diana with cover for her hunting activities.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 2,
        "perception": 4, "intelligence": 4, "wits": 2,
        "alertness": 2, "empathy": 2, "survival": 3, "science": 4, "academics": 3,
        "willpower": 4,
    },
]

# =============================================================================
# MENTOR NPCs - Vampires who teach/guide PCs
# =============================================================================

MENTORS = [
    {
        "name": "Maximilian Strauss",
        "concept": "Elder Tremere regent and Isabella's mentor",
        "for_pc": "Isabella Santos",
        "clan": "Tremere",
        "sect": "Camarilla",
        "generation_rating": 7,
        "description": "Ancient Tremere who survived the Inquisition. Now serves as regent of the Pacific Northwest. "
                       "Sees Isabella as a promising student but tests her constantly.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 4, "appearance": 2,
        "perception": 4, "intelligence": 5, "wits": 4,
        "alertness": 3, "awareness": 4, "empathy": 2, "subterfuge": 4,
        "occult": 5, "academics": 4, "investigation": 3, "politics": 4,
        "auspex": 4, "dominate": 3, "thaumaturgy": 5,
        "willpower": 9,
        "humanity": 5,
    },
]

# =============================================================================
# HERD NPCs - Regular feeding sources
# =============================================================================

# Marcus Antonio's Herd (2 dots worth)
MARCUS_HERD = [
    {
        "name": "Crystal Martinez",
        "concept": "Personal assistant who thinks she's part of an exclusive club",
        "description": "Works as Marcus's day assistant. Has been conditioned to think the 'blood donations' "
                       "are part of an elite wellness program. Completely loyal and discreet.",
        "strength": 1, "dexterity": 2, "stamina": 2,
        "charisma": 3, "manipulation": 2, "appearance": 3,
        "perception": 2, "intelligence": 3, "wits": 2,
        "empathy": 2, "etiquette": 3, "computer": 3, "finance": 2,
        "willpower": 3,
    },
    {
        "name": "David Chen",
        "concept": "Bodyguard under the Ventrue's thrall",
        "description": "Former military. Hired as security but has been blood bound to serve as "
                       "both protector and food source. Believes his employer is just eccentric.",
        "strength": 4, "dexterity": 3, "stamina": 3,
        "charisma": 2, "manipulation": 1, "appearance": 2,
        "perception": 3, "intelligence": 2, "wits": 3,
        "alertness": 3, "athletics": 3, "brawl": 4, "firearms": 3, "security": 3,
        "willpower": 4,
    },
]


def create_contact_npcs(chronicle, st_user):
    """Create Contact NPCs for vampire PCs."""
    print("\n--- Creating Contact NPCs ---")

    all_contacts = [
        ("Marcus 'Shadow' Webb", MARCUS_CONTACTS),
        ("Roland Cross", ROLAND_CONTACTS),
        ("Viktor Krueger", VIKTOR_CONTACTS),
    ]

    for pc_name, contacts in all_contacts:
        print(f"\nContacts for {pc_name}:")
        for contact_data in contacts:
            human, created = VtMHuman.objects.get_or_create(
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
    """Create Ally NPCs for vampire PCs."""
    print("\n--- Creating Ally NPCs ---")

    all_allies = [
        ("Roland Cross", ROLAND_ALLIES),
        ("Viktor Krueger", VIKTOR_ALLIES),
        ("Diana Cross", DIANA_ALLIES),
    ]

    for pc_name, allies in all_allies:
        print(f"\nAllies for {pc_name}:")
        for ally_data in allies:
            human, created = VtMHuman.objects.get_or_create(
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
    """Create Mentor NPCs (elder vampires) for vampire PCs."""
    print("\n--- Creating Mentor NPCs ---")

    for mentor_data in MENTORS:
        clan = VampireClan.objects.filter(name=mentor_data["clan"]).first()
        sect = VampireSect.objects.filter(name=mentor_data["sect"]).first()

        vampire, created = Vampire.objects.get_or_create(
            name=mentor_data["name"],
            owner=st_user,
            defaults={
                "concept": mentor_data["concept"],
                "description": mentor_data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
                "clan": clan,
                "sect": sect,
            },
        )
        if created:
            # Apply attributes and abilities
            for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                         "appearance", "perception", "intelligence", "wits"]:
                if attr in mentor_data:
                    setattr(vampire, attr, mentor_data[attr])

            for ability in ["alertness", "athletics", "awareness", "brawl", "empathy",
                            "expression", "intimidation", "leadership", "streetwise", "subterfuge",
                            "crafts", "drive", "etiquette", "firearms", "melee", "performance",
                            "larceny", "stealth", "survival", "technology",
                            "academics", "computer", "finance", "investigation", "law",
                            "linguistics", "medicine", "occult", "politics", "science"]:
                if ability in mentor_data:
                    setattr(vampire, ability, mentor_data[ability])

            # Apply disciplines
            for discipline in ["animalism", "auspex", "celerity", "chimerstry", "daimoinon",
                               "dementation", "dominate", "fortitude", "melpominee", "mytherceria",
                               "necromancy", "obfuscate", "obtenebration", "obeah", "potence",
                               "presence", "protean", "quietus", "serpentis", "spiritus",
                               "thaumaturgy", "thanatosis", "valeren", "vicissitude"]:
                if discipline in mentor_data:
                    setattr(vampire, discipline, mentor_data[discipline])

            if "willpower" in mentor_data:
                vampire.willpower = mentor_data["willpower"]
            if "humanity" in mentor_data:
                vampire.humanity = mentor_data["humanity"]
            if "generation_rating" in mentor_data:
                vampire.generation_rating = mentor_data["generation_rating"]

            vampire.save()
            print(f"  Created mentor: {vampire.name} (for {mentor_data['for_pc']})")
        else:
            print(f"  Already exists: {vampire.name}")


def create_herd_npcs(chronicle, st_user):
    """Create Herd NPCs for vampire PCs."""
    print("\n--- Creating Herd NPCs ---")

    print("\nHerd for Marcus Antonio:")
    for herd_data in MARCUS_HERD:
        human, created = VtMHuman.objects.get_or_create(
            name=herd_data["name"],
            owner=st_user,
            defaults={
                "concept": herd_data["concept"],
                "description": herd_data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
            },
        )
        if created:
            apply_human_stats(human, herd_data)
            print(f"  Created: {human.name}")
        else:
            print(f"  Already exists: {human.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Vampire PC Auxiliary NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_contact_npcs(chronicle, st_user)
    create_ally_npcs(chronicle, st_user)
    create_mentor_npcs(chronicle, st_user)
    create_herd_npcs(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Vampire auxiliary NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
