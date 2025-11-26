"""
Seattle Test Chronicle - Mummy Major NPCs

Creates major Mummy NPCs who hold positions of power:
Elder Amenti, cult leaders, and immortal threats.

Run with: python manage.py shell < populate_db/chronicle/test/mummy_npc.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Mummy data must be loaded (dynasties, hekau)
"""

from django.contrib.auth.models import User

from characters.models.mummy.mummy import Mummy
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_mummy_stats(mummy, data):
    """Apply stats to a Mummy NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(mummy, attr, data[attr])

    # Abilities
    for ability in ["alertness", "athletics", "awareness", "brawl", "empathy", "expression",
                    "intimidation", "leadership", "streetwise", "subterfuge",
                    "crafts", "drive", "etiquette", "firearms", "larceny", "melee",
                    "performance", "security", "stealth", "survival", "technology",
                    "academics", "computer", "enigmas", "finance", "investigation", "law",
                    "linguistics", "medicine", "occult", "politics", "science"]:
        if ability in data:
            setattr(mummy, ability, data[ability])

    if "willpower" in data:
        mummy.willpower = data["willpower"]
    if "sekhem" in data:
        mummy.sekhem = data["sekhem"]
    if "ba" in data:
        mummy.ba = data["ba"]
    if "balance" in data:
        mummy.balance = data["balance"]

    mummy.save()


# =============================================================================
# ELDER AMENTI - THOSE WHO HAVE LIVED MANY LIVES
# =============================================================================

ELDER_AMENTI = [
    {
        "name": "Ahmose the Eternal",
        "concept": "Ancient Amenti who has guided Seattle's undying for centuries",
        "dynasty": "Kher-minu",
        "description": "Ahmose has lived more lives than he can easily count. He was a priest in the first "
                       "dynasties, a scholar in Alexandria, a crusader in the Holy Land, and a hundred other "
                       "things before coming to the Pacific Northwest. He guides the Amenti of Seattle, "
                       "teaching the newly risen about their powers and responsibilities. His wisdom is vast, "
                       "his patience legendary, and his power restrained but undeniable.",
        "strength": 3, "dexterity": 3, "stamina": 4,
        "charisma": 4, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 5, "empathy": 4, "expression": 4, "leadership": 5, "subterfuge": 4,
        "etiquette": 4, "melee": 4,
        "academics": 5, "enigmas": 5, "linguistics": 5, "medicine": 4, "occult": 5, "politics": 4,
        "willpower": 10, "sekhem": 8, "ba": 8, "balance": 8,
    },
    {
        "name": "Nefertari the Just",
        "concept": "Judge of the Dead who weighs Seattle's Amenti",
        "dynasty": "Mesektet",
        "description": "Nefertari served as a judge in the courts of the pharaohs, and she continues that "
                       "role in the afterlife. She weighs the actions of Seattle's Amenti against Ma'at, "
                       "determining who serves the balance and who has strayed. Her judgments are final "
                       "among the local mummies, and even the elders defer to her wisdom in matters of law.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 4, "manipulation": 4, "appearance": 4,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 4, "empathy": 5, "expression": 4, "intimidation": 3, "leadership": 4,
        "etiquette": 5,
        "academics": 5, "enigmas": 4, "investigation": 5, "law": 5, "occult": 4, "politics": 4,
        "willpower": 9, "sekhem": 7, "ba": 9, "balance": 9,
    },
]

# =============================================================================
# CULT LEADERS - THOSE WHO GUIDE THE MORTAL FAITHFUL
# =============================================================================

CULT_LEADERS = [
    {
        "name": "Sethnakht the Keeper",
        "concept": "Leader of the House of Scrolls cult",
        "dynasty": "Sefekhi",
        "description": "Sethnakht has spent five thousand years preserving knowledge—first in temples, "
                       "then in libraries, now in digital archives. He leads the House of Scrolls, the "
                       "local cult dedicated to Thoth's wisdom. His mortal followers include academics, "
                       "librarians, and archivists who unknowingly serve the god of knowledge.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 4, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 4,
        "alertness": 3, "awareness": 4, "empathy": 3, "expression": 5, "leadership": 4, "subterfuge": 3,
        "etiquette": 3, "technology": 3,
        "academics": 5, "computer": 4, "enigmas": 5, "investigation": 4, "linguistics": 5, "occult": 5,
        "willpower": 8, "sekhem": 7, "ba": 7, "balance": 7,
    },
    {
        "name": "Khonsu-mes the Vigilant",
        "concept": "Leader of the Keepers of Ma'at cult",
        "dynasty": "Udja-sen",
        "description": "Khonsu-mes was a temple guardian in life and remains one in death. He leads the "
                       "Keepers of Ma'at, a cult dedicated to maintaining cosmic balance in Seattle. "
                       "His followers include police, judges, and social workers who work to uphold justice. "
                       "He sees threats to the balance that others miss and acts to correct them.",
        "strength": 4, "dexterity": 4, "stamina": 4,
        "charisma": 3, "manipulation": 3, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 5, "athletics": 4, "awareness": 4, "brawl": 4, "empathy": 3, "intimidation": 4,
        "leadership": 4,
        "firearms": 3, "melee": 5, "survival": 3,
        "investigation": 5, "law": 4, "occult": 4, "politics": 3,
        "willpower": 9, "sekhem": 7, "ba": 6, "balance": 8,
    },
    {
        "name": "Sekhmet-Hathor the Fierce",
        "concept": "Leader of the Lions of Sekhmet cult",
        "dynasty": "Khri-habi",
        "description": "Sekhmet-Hathor embodies both the destroyer and healer aspects of her goddess. "
                       "She leads the Lions of Sekhmet, a cult of warriors and healers who protect the "
                       "innocent and destroy the corrupt. Her mortal followers include soldiers, doctors, "
                       "and first responders. She teaches that sometimes healing requires destruction first.",
        "strength": 5, "dexterity": 4, "stamina": 5,
        "charisma": 3, "manipulation": 3, "appearance": 4,
        "perception": 4, "intelligence": 4, "wits": 5,
        "alertness": 4, "athletics": 4, "awareness": 3, "brawl": 5, "empathy": 3, "intimidation": 5,
        "leadership": 4,
        "firearms": 4, "melee": 5, "survival": 4,
        "medicine": 5, "occult": 4,
        "willpower": 9, "sekhem": 8, "ba": 5, "balance": 7,
    },
]

# =============================================================================
# THREATS - THOSE WHO HAVE FALLEN FROM MA'AT
# =============================================================================

FALLEN_AMENTI = [
    {
        "name": "Apophis-Ka the Deceiver",
        "concept": "Fallen Amenti who serves the Serpent",
        "dynasty": "Sakhmu",
        "description": "Apophis-Ka was once a faithful servant of the gods, but centuries of existence "
                       "corrupted him. He now serves Apophis, the serpent of chaos, working to upset the "
                       "balance that the other Amenti maintain. His cult in Seattle works in shadows, "
                       "undermining institutions and spreading discord. He believes that only in chaos "
                       "can true freedom be found.",
        "strength": 4, "dexterity": 4, "stamina": 4,
        "charisma": 4, "manipulation": 5, "appearance": 4,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 4, "empathy": 2, "expression": 4, "intimidation": 4, "subterfuge": 5,
        "leadership": 4, "streetwise": 4,
        "larceny": 4, "melee": 4, "stealth": 4,
        "academics": 4, "enigmas": 5, "occult": 5, "politics": 4,
        "willpower": 9, "sekhem": 7, "ba": 3, "balance": 2,
    },
]


def create_elder_amenti(chronicle, st_user):
    """Create elder Amenti NPCs."""
    print("\n--- Creating Elder Amenti ---")

    for data in ELDER_AMENTI:
        mummy, created = Mummy.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
            },
        )
        if created:
            apply_mummy_stats(mummy, data)
            print(f"  Created: {mummy.name}")
        else:
            print(f"  Already exists: {mummy.name}")


def create_cult_leaders(chronicle, st_user):
    """Create cult leader NPCs."""
    print("\n--- Creating Cult Leaders ---")

    for data in CULT_LEADERS:
        mummy, created = Mummy.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
            },
        )
        if created:
            apply_mummy_stats(mummy, data)
            print(f"  Created: {mummy.name}")
        else:
            print(f"  Already exists: {mummy.name}")


def create_fallen_amenti(chronicle, st_user):
    """Create fallen Amenti threat NPCs."""
    print("\n--- Creating Fallen Amenti ---")

    for data in FALLEN_AMENTI:
        mummy, created = Mummy.objects.get_or_create(
            name=data["name"],
            owner=st_user,
            defaults={
                "concept": data["concept"],
                "description": data.get("description", ""),
                "chronicle": chronicle,
                "npc": True,
                "status": "App",
            },
        )
        if created:
            apply_mummy_stats(mummy, data)
            print(f"  Created: {mummy.name}")
        else:
            print(f"  Already exists: {mummy.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Mummy Major NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_elder_amenti(chronicle, st_user)
    create_cult_leaders(chronicle, st_user)
    create_fallen_amenti(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Mummy major NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
