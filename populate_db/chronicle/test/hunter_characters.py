"""
Seattle Test Chronicle - Hunter Characters

Creates Hunter characters and Creeds for the test chronicle.
Assigns characters to appropriate organizations (cells/networks) based on DESIGN.md.

Run with: python manage.py shell < populate_db/chronicle/test/hunter_characters.py
"""

from django.contrib.auth.models import User

from characters.models.hunter import Creed, Hunter, HunterOrganization
from game.models import Chronicle


# Creed definitions
# Primary Virtues: Conviction (Judge, Visionary), Vision (Defender, Innocent), Zeal (Avenger, Martyr, Redeemer, Wayward)
CREEDS = [
    {
        "name": "Avenger",
        "primary_virtue": "zeal",
        "nickname": "Avengers",
        "philosophy": "Hunt and destroy the monsters that prey on humanity",
        "description": "Avengers are driven by righteous fury against supernatural evil. They believe "
        "the only good monster is a dead monster, and they're willing to take extreme measures "
        "to protect humanity from things that lurk in the dark.",
        "favored_edges": ["demand", "confront"],
    },
    {
        "name": "Defender",
        "primary_virtue": "vision",
        "nickname": "Defenders",
        "philosophy": "Protect the innocent from supernatural threats",
        "description": "Defenders focus on shielding the vulnerable rather than seeking out monsters. "
        "They use their powers to ward away evil, heal the wounded, and create safe spaces "
        "in a dangerous world.",
        "favored_edges": ["ward", "hide", "illuminate"],
    },
    {
        "name": "Innocent",
        "primary_virtue": "vision",
        "nickname": "Innocents",
        "philosophy": "Believe in redemption, even for monsters",
        "description": "Innocents maintain hope that even the darkest creature might be redeemed. "
        "They approach the supernatural with compassion rather than violence, seeking to "
        "understand and heal rather than destroy.",
        "favored_edges": ["illuminate", "radiate"],
    },
    {
        "name": "Judge",
        "primary_virtue": "conviction",
        "nickname": "Judges",
        "philosophy": "Determine the guilty and innocent among the supernatural",
        "description": "Judges believe their role is to weigh the actions of supernatural beings "
        "and determine appropriate consequences. Not all monsters deserve death—some deserve "
        "punishment, some surveillance, some redemption.",
        "favored_edges": ["discern", "balance", "expose"],
    },
    {
        "name": "Martyr",
        "primary_virtue": "zeal",
        "nickname": "Martyrs",
        "philosophy": "Sacrifice yourself to save others",
        "description": "Martyrs are willing to give everything—including their lives—to protect "
        "humanity. They absorb harm meant for others and face dangers that would destroy "
        "lesser hunters, driven by selfless devotion.",
        "favored_edges": ["donate", "becalm", "respire"],
    },
    {
        "name": "Redeemer",
        "primary_virtue": "zeal",
        "nickname": "Redeemers",
        "philosophy": "Save the monsters from themselves",
        "description": "Redeemers believe even monsters can change. They seek to cure vampirism, "
        "free the possessed, and rehabilitate the supernatural. Their methods are controversial "
        "among other hunters.",
        "favored_edges": ["rejuvenate", "redeem"],
    },
    {
        "name": "Visionary",
        "primary_virtue": "conviction",
        "nickname": "Visionaries",
        "philosophy": "Understand the bigger picture of the supernatural world",
        "description": "Visionaries seek to comprehend the grand design behind supernatural events. "
        "They investigate, research, and connect dots that others miss, trying to understand "
        "why the Messengers chose humanity to fight this war.",
        "favored_edges": ["investigate", "witness"],
    },
    {
        "name": "Wayward",
        "primary_virtue": "zeal",
        "nickname": "Wayward",
        "philosophy": "Walk the edge between hunter and hunted",
        "description": "Wayward are the wild cards—hunters whose methods are unpredictable and whose "
        "sanity is often questioned. They hear the Messengers differently than others and "
        "may be touched by something beyond conventional understanding.",
        "favored_edges": ["vengeance", "prosecute"],
    },
]


# Hunter character definitions
# Virtues: conviction, vision, zeal (starting total varies by creed)
# Edges: grouped by virtue (conviction, vision, zeal)
HUNTERS = [
    {
        "username": "xXShadowWolfXx",
        "name": "Jake Mercer",
        "creed": "Judge",
        "organization": "The Vigil",
        "is_leader": True,
        "primary_virtue": "conviction",
        "concept": "Former cop who saw too much, now hunting monsters",
        # Attributes: 7/5/3
        "strength": 3,
        "dexterity": 3,
        "stamina": 3,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 3,
        "wits": 3,
        # Abilities: 13/9/5
        "investigation": 4,
        "firearms": 3,
        "streetwise": 3,
        "alertness": 3,
        "brawl": 2,
        "drive": 2,
        "intimidation": 2,
        "law": 2,
        "subterfuge": 1,
        # Backgrounds (5 points)
        "contacts": 3,
        "resources": 2,
        # Virtues
        "conviction": 3,
        "vision": 2,
        "zeal": 2,
        # Edges (3 starting dots in primary virtue edges)
        "discern": 2,
        "balance": 1,
    },
    {
        "username": "CrypticMoon",
        "name": "Maria Vasquez",
        "creed": "Defender",
        "organization": "The Vigil",
        "is_leader": False,
        "primary_virtue": "vision",
        "concept": "Hospice nurse who protects the dying from predators",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 3,
        "appearance": 3,
        "perception": 4,
        "intelligence": 3,
        "wits": 3,
        # Abilities: 13/9/5
        "medicine": 4,
        "empathy": 3,
        "alertness": 3,
        "expression": 2,
        "academics": 2,
        "occult": 2,
        "subterfuge": 2,
        "stealth": 1,
        # Backgrounds (5 points)
        "allies": 2,
        "contacts": 2,
        "resources": 1,
        # Virtues
        "conviction": 2,
        "vision": 3,
        "zeal": 2,
        # Edges
        "ward": 2,
        "illuminate": 1,
    },
    {
        "username": "NightOwl_42",
        "name": "Derek Stone",
        "creed": "Visionary",
        "organization": "The Network",
        "is_leader": True,
        "primary_virtue": "conviction",
        "concept": "Teacher building a network of monster hunters",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 4,
        "manipulation": 4,
        "appearance": 2,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "leadership": 4,
        "academics": 3,
        "expression": 3,
        "empathy": 2,
        "alertness": 2,
        "investigation": 2,
        "computer": 2,
        "subterfuge": 2,
        # Backgrounds (5 points)
        "contacts": 3,
        "resources": 1,
        "allies": 1,
        # Virtues
        "conviction": 3,
        "vision": 2,
        "zeal": 2,
        # Edges
        "investigate": 2,
        "witness": 1,
    },
    {
        "username": "pixel_witch",
        "name": "Alex Chen",
        "creed": "Visionary",
        "organization": "The Network",
        "is_leader": False,
        "primary_virtue": "conviction",
        "concept": "Content moderator tracking supernatural activity online",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 4,
        "wits": 4,
        # Abilities: 13/9/5
        "computer": 4,
        "investigation": 3,
        "alertness": 3,
        "technology": 3,
        "academics": 2,
        "occult": 1,
        "stealth": 1,
        "subterfuge": 1,
        # Backgrounds (5 points)
        "contacts": 2,
        "resources": 2,
        "allies": 1,
        # Virtues
        "conviction": 3,
        "vision": 2,
        "zeal": 2,
        # Edges
        "investigate": 2,
        "discern": 1,
    },
    {
        "username": "ByteSlayer",
        "name": "Yuki Tanaka",
        "creed": "Avenger",
        "organization": "The Vigil",
        "is_leader": False,
        "primary_virtue": "zeal",
        "concept": "Martial artist teaching supernatural self-defense",
        # Attributes: 7/5/3
        "strength": 3,
        "dexterity": 4,
        "stamina": 3,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 3,
        "perception": 3,
        "intelligence": 2,
        "wits": 4,
        # Abilities: 13/9/5
        "brawl": 4,
        "melee": 3,
        "athletics": 3,
        "alertness": 3,
        "dodge": 2,
        "stealth": 2,
        "intimidation": 1,
        "leadership": 2,
        # Backgrounds (5 points)
        "allies": 2,
        "resources": 2,
        "contacts": 1,
        # Virtues
        "conviction": 2,
        "vision": 2,
        "zeal": 3,
        # Edges
        "demand": 2,
        "confront": 1,
    },
    {
        "username": "gh0st_in_shell",
        "name": "Chris Walker",
        "creed": "Judge",
        "organization": "The Network",
        "is_leader": False,
        "primary_virtue": "conviction",
        "concept": "Paranormal investigator who found the real thing",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 3,
        "appearance": 3,
        "perception": 4,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "investigation": 4,
        "occult": 3,
        "computer": 3,
        "alertness": 3,
        "expression": 2,
        "academics": 2,
        "technology": 2,
        # Backgrounds (5 points)
        "resources": 3,
        "contacts": 2,
        # Virtues
        "conviction": 3,
        "vision": 2,
        "zeal": 2,
        # Edges
        "discern": 2,
        "expose": 1,
    },
    {
        "username": "Zephyr_Storm",
        "name": "Marcus Johnson",
        "creed": "Visionary",
        "organization": "The Network",
        "is_leader": False,
        "primary_virtue": "conviction",
        "concept": "Meteorologist tracking supernatural phenomena in weather",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 5,
        "wits": 3,
        # Abilities: 13/9/5
        "science": 4,
        "computer": 3,
        "investigation": 3,
        "academics": 3,
        "alertness": 2,
        "technology": 2,
        "expression": 1,
        # Backgrounds (5 points)
        "resources": 3,
        "contacts": 2,
        # Virtues
        "conviction": 3,
        "vision": 2,
        "zeal": 2,
        # Edges
        "investigate": 2,
        "witness": 1,
    },
    {
        "username": "n00b_hunter",
        "name": "Kyle Morrison",
        "creed": "Innocent",
        "organization": "The Support Group",
        "is_leader": False,
        "primary_virtue": "vision",
        "concept": "Rookie hunter surviving through sheer luck",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 2,
        "charisma": 3,
        "manipulation": 2,
        "appearance": 3,
        "perception": 3,
        "intelligence": 3,
        "wits": 4,
        # Abilities: 13/9/5
        "alertness": 3,
        "athletics": 2,
        "dodge": 2,
        "streetwise": 2,
        "stealth": 2,
        "drive": 2,
        "computer": 2,
        "brawl": 1,
        "investigation": 1,
        # Backgrounds (5 points)
        "contacts": 2,
        "allies": 2,
        "resources": 1,
        # Virtues (lower - he's new)
        "conviction": 2,
        "vision": 3,
        "zeal": 2,
        # Edges (fewer - just imbued)
        "illuminate": 1,
        "hide": 1,
    },
    {
        "username": "ElectricDreamer",
        "name": "Jasmine Torres",
        "creed": "Martyr",
        "organization": "The Support Group",
        "is_leader": True,
        "primary_virtue": "zeal",
        "concept": "Therapist counseling hunters through psychological trauma",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 2,
        "stamina": 2,
        "charisma": 5,
        "manipulation": 3,
        "appearance": 3,
        "perception": 3,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "empathy": 4,
        "expression": 3,
        "academics": 3,
        "medicine": 2,
        "alertness": 2,
        "subterfuge": 2,
        "occult": 2,
        "leadership": 1,
        # Backgrounds (5 points)
        "allies": 2,
        "contacts": 2,
        "resources": 1,
        # Virtues
        "conviction": 2,
        "vision": 2,
        "zeal": 3,
        # Edges
        "donate": 2,
        "becalm": 1,
    },
    {
        "username": "void_whisper",
        "name": "Rachel Kim",
        "creed": "Avenger",
        "organization": "The Vigil",
        "is_leader": False,
        "primary_virtue": "zeal",
        "concept": "Mortician who ensures monsters stay dead",
        # Attributes: 7/5/3
        "strength": 2,
        "dexterity": 3,
        "stamina": 3,
        "charisma": 2,
        "manipulation": 2,
        "appearance": 2,
        "perception": 4,
        "intelligence": 4,
        "wits": 3,
        # Abilities: 13/9/5
        "medicine": 4,
        "occult": 3,
        "investigation": 3,
        "alertness": 3,
        "academics": 2,
        "stealth": 2,
        "science": 2,
        # Backgrounds (5 points)
        "resources": 2,
        "contacts": 2,
        "allies": 1,
        # Virtues
        "conviction": 2,
        "vision": 2,
        "zeal": 3,
        # Edges
        "demand": 2,
        "confront": 1,
    },
]


def get_chronicle_and_st():
    """Get the Seattle Test Chronicle and its ST user."""
    chronicle = Chronicle.objects.filter(name="Seattle Test Chronicle").first()
    if not chronicle:
        print("ERROR: Seattle Test Chronicle not found. Run base.py first.")
        return None, None

    st_user = User.objects.filter(username="DarkMaster99").first()
    if not st_user:
        print("ERROR: ST user DarkMaster99 not found. Run base.py first.")
        return None, None

    return chronicle, st_user


def apply_stats(character, data, stat_list):
    """Apply stats from data dict to character."""
    for stat in stat_list:
        if stat in data:
            setattr(character, stat, data[stat])


def create_creeds():
    """Create Hunter creeds."""
    print("\n--- Creating Hunter Creeds ---")

    for data in CREEDS:
        creed, created = Creed.objects.get_or_create(
            name=data["name"],
            defaults={
                "primary_virtue": data["primary_virtue"],
                "nickname": data.get("nickname", ""),
                "philosophy": data.get("philosophy", ""),
                "description": data.get("description", ""),
                "favored_edges": data.get("favored_edges", []),
            },
        )
        if created:
            print(f"  Created creed: {data['name']} ({data['primary_virtue']})")
        else:
            print(f"  Creed already exists: {data['name']}")


def create_hunters(chronicle, st_user):
    """Create Hunter characters and assign to organizations."""
    print("\n--- Creating Hunter Characters ---")

    # Cache creeds and organizations
    creeds = {c.name: c for c in Creed.objects.all()}
    organizations = {o.name: o for o in HunterOrganization.objects.all()}

    attributes = [
        "strength",
        "dexterity",
        "stamina",
        "charisma",
        "manipulation",
        "appearance",
        "perception",
        "intelligence",
        "wits",
    ]
    abilities = [
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "awareness",
        "leadership",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "animal_ken",
        "larceny",
        "performance",
        "repair",
        "survival",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "finance",
        "law",
        "occult",
        "politics",
        "technology",
        "dodge",
    ]
    backgrounds = [
        "allies",
        "contacts",
        "influence",
        "mentor",
        "resources",
        "status_background",
    ]
    conviction_edges = [
        "discern",
        "burden",
        "balance",
        "expose",
        "investigate",
        "witness",
        "prosecute",
    ]
    vision_edges = [
        "illuminate",
        "ward",
        "cleave",
        "hide",
        "blaze",
        "radiate",
        "vengeance",
    ]
    zeal_edges = [
        "demand",
        "confront",
        "donate",
        "becalm",
        "respire",
        "rejuvenate",
        "redeem",
    ]
    all_edges = conviction_edges + vision_edges + zeal_edges

    for data in HUNTERS:
        # Get or create user
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            print(f"  WARNING: User {data['username']} not found, skipping {data['name']}")
            continue

        # Get creed
        creed = creeds.get(data["creed"])

        # Create or get hunter
        hunter, created = Hunter.objects.get_or_create(
            name=data["name"],
            owner=user,
            defaults={
                "chronicle": chronicle,
                "creed": creed,
                "primary_virtue": data.get("primary_virtue", "conviction"),
                "concept": data.get("concept", ""),
                "npc": False,
            },
        )

        if created:
            # Apply stats
            apply_stats(hunter, data, attributes)
            apply_stats(hunter, data, abilities)
            apply_stats(hunter, data, backgrounds)
            apply_stats(hunter, data, all_edges)

            # Set virtues
            hunter.conviction = data.get("conviction", 1)
            hunter.vision = data.get("vision", 1)
            hunter.zeal = data.get("zeal", 1)

            # Set temporary virtues equal to permanent
            hunter.temporary_conviction = hunter.conviction
            hunter.temporary_vision = hunter.vision
            hunter.temporary_zeal = hunter.zeal

            # Willpower for hunters
            hunter.willpower = 3

            hunter.save()
            print(f"  Created hunter: {data['name']} ({data['creed']})")
        else:
            print(f"  Hunter already exists: {data['name']}")

        # Assign to organization
        org_name = data.get("organization")
        if org_name and org_name in organizations:
            org = organizations[org_name]
            if hunter not in org.members.all():
                org.members.add(hunter)
                print(f"    Added to organization: {org_name}")

            if data.get("is_leader"):
                org.leader = hunter
                org.save()
                print(f"    Set as organization leader")


def main():
    """Run the full Hunter character setup."""
    print("=" * 60)
    print("Seattle Test Chronicle - Hunter Character Setup")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()
    if not chronicle or not st_user:
        return

    # Create creeds first (they don't require chronicle)
    create_creeds()

    # Create hunters
    create_hunters(chronicle, st_user)

    # Summary
    print("\n" + "=" * 60)
    print("Hunter character setup complete!")
    print(f"Creeds: {Creed.objects.count()}")
    print(f"Hunters: {Hunter.objects.filter(chronicle=chronicle).count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    # When run via `python manage.py shell < script.py`
    main()
