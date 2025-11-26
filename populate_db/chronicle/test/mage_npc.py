"""
Seattle Test Chronicle - Mage Major NPCs

Creates major Mage NPCs who hold positions of power:
Chantry leadership, Tradition representatives, and Technocracy threats.

Run with: python manage.py shell < populate_db/chronicle/test/mage_npc.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Mage data must be loaded (traditions, spheres)
"""

from django.contrib.auth.models import User

from characters.models.mage.mage import Mage
from characters.models.mage.faction import MageFaction
from game.models import Chronicle


def get_chronicle_and_st():
    """Get the chronicle and ST user."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="DarkMaster99")
    return chronicle, st_user


def apply_mage_stats(mage, data):
    """Apply stats to a Mage NPC."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina", "charisma", "manipulation",
                 "appearance", "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(mage, attr, data[attr])

    # Abilities
    for ability in ["alertness", "art", "athletics", "awareness", "brawl", "empathy",
                    "expression", "intimidation", "leadership", "streetwise", "subterfuge",
                    "crafts", "drive", "etiquette", "firearms", "martial_arts", "meditation",
                    "melee", "research", "stealth", "survival", "technology",
                    "academics", "computer", "cosmology", "enigmas", "esoterica",
                    "investigation", "law", "medicine", "occult", "politics", "science"]:
        if ability in data:
            setattr(mage, ability, data[ability])

    # Spheres
    for sphere in ["correspondence", "entropy", "forces", "life", "matter",
                   "mind", "prime", "spirit", "time"]:
        if sphere in data:
            setattr(mage, sphere, data[sphere])

    if "arete" in data:
        mage.arete = data["arete"]
    if "willpower" in data:
        mage.willpower = data["willpower"]
    if "quintessence" in data:
        mage.quintessence = data["quintessence"]

    mage.save()


# =============================================================================
# CHANTRY LEADERSHIP - SEATTLE TRADITION ALLIANCE
# =============================================================================

CHANTRY_LEADERSHIP = [
    {
        "name": "Archmagus Solomon Cross",
        "concept": "Order of Hermes Deacon and Chantry leader",
        "tradition": "Order of Hermes",
        "description": "Archmagus Cross has led Seattle's Tradition Chantry for forty years. A master of "
                       "Prime and Forces, his formal hermetic approach clashes with the Virtual Adepts "
                       "but his power keeps them in line. The Chantry occupies a Victorian mansion on "
                       "Capitol Hill, its interior far larger than physics should allow. He maintains "
                       "the Nodes of Seattle and arbitrates disputes between Traditions.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 3, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 4,
        "alertness": 3, "awareness": 4, "expression": 3, "intimidation": 3, "leadership": 5, "subterfuge": 3,
        "etiquette": 4, "meditation": 4,
        "academics": 5, "cosmology": 4, "enigmas": 5, "occult": 5, "science": 3,
        "correspondence": 3, "forces": 5, "prime": 5, "spirit": 3,
        "arete": 6, "willpower": 9, "quintessence": 20,
    },
    {
        "name": "Dr. Yuki Tanaka",
        "concept": "Akashic Brother sensei and martial wisdom keeper",
        "tradition": "Akashic Brotherhood",
        "description": "Master Tanaka teaches at a martial arts studio that doubles as the Akashic presence "
                       "in Seattle. Her Do enables her to see the flows of conflict and harmony in the city. "
                       "She advises the Chantry on matters of physical and spiritual balance, and her students "
                       "are the first line of defense against Marauder incursions.",
        "strength": 3, "dexterity": 5, "stamina": 4,
        "charisma": 3, "manipulation": 2, "appearance": 3,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 5, "athletics": 5, "awareness": 4, "brawl": 5, "empathy": 3, "expression": 2,
        "martial_arts": 5, "meditation": 5, "stealth": 3,
        "cosmology": 3, "enigmas": 4, "medicine": 3, "occult": 3,
        "entropy": 2, "life": 4, "mind": 4, "time": 3,
        "arete": 5, "willpower": 8, "quintessence": 15,
    },
    {
        "name": "Mother Celestine",
        "concept": "Celestial Chorus priestess maintaining spiritual harmony",
        "tradition": "Celestial Chorus",
        "description": "Mother Celestine serves as the Celestial Chorus representative and chaplain to "
                       "the Chantry. Her prayers can heal the wounded and her blessings protect against "
                       "corruption. She works closely with Dr. Hassan Al-Rashid, seeing beyond the surface "
                       "differences of their faiths to the One they both serve.",
        "strength": 2, "dexterity": 2, "stamina": 3,
        "charisma": 5, "manipulation": 2, "appearance": 3,
        "perception": 4, "intelligence": 4, "wits": 4,
        "alertness": 3, "awareness": 5, "empathy": 5, "expression": 4, "leadership": 3,
        "etiquette": 3, "meditation": 4,
        "academics": 3, "cosmology": 4, "occult": 4,
        "life": 4, "mind": 3, "prime": 4, "spirit": 4,
        "arete": 5, "willpower": 9, "quintessence": 18,
    },
    {
        "name": "Maestro",
        "concept": "Cult of Ecstasy elder who has tripped through time",
        "tradition": "Cult of Ecstasy",
        "description": "No one knows Maestro's birth name or exact age. They've taken so many journeys through "
                       "altered consciousness that time moves strangely around them. Their rave temple in an "
                       "abandoned warehouse has become a Node, fed by the ecstatic energy of dancers who "
                       "never quite remember what happened the night before.",
        "strength": 2, "dexterity": 4, "stamina": 3,
        "charisma": 4, "manipulation": 3, "appearance": 4,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 4, "awareness": 5, "empathy": 4, "expression": 4, "streetwise": 3, "subterfuge": 3,
        "performance": 5, "meditation": 4,
        "cosmology": 4, "enigmas": 5, "occult": 4,
        "entropy": 3, "life": 3, "mind": 5, "time": 5,
        "arete": 6, "willpower": 8, "quintessence": 16,
    },
]

# =============================================================================
# VIRTUAL ADEPT PRESENCE
# =============================================================================

VIRTUAL_ADEPTS = [
    {
        "name": "Nexus",
        "concept": "Virtual Adept elder who helped build the Digital Web",
        "tradition": "Virtual Adepts",
        "description": "Nexus was one of the Adepts who broke from the Technocracy in the 1960s. "
                       "She's built server farms that touch the Digital Web and maintains nodes of "
                       "data that preserve secrets the Technocracy would prefer deleted. The younger "
                       "Adepts see her as a legendary figure; she sees them as reckless children.",
        "strength": 2, "dexterity": 3, "stamina": 2,
        "charisma": 2, "manipulation": 4, "appearance": 3,
        "perception": 5, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 3, "expression": 2, "subterfuge": 4,
        "technology": 5,
        "computer": 5, "enigmas": 4, "investigation": 3, "science": 5,
        "correspondence": 5, "entropy": 3, "forces": 4, "mind": 3,
        "arete": 5, "willpower": 7, "quintessence": 14,
    },
]

# =============================================================================
# TECHNOCRACY THREATS
# =============================================================================

TECHNOCRACY = [
    {
        "name": "Director Marcus Hayes",
        "concept": "NWO Director overseeing Seattle operations",
        "affiliation": "New World Order",
        "description": "Director Hayes runs the Seattle Construct from offices in a downtown high-rise. "
                       "His Operatives monitor mage activity throughout the region, and his Adjustment "
                       "teams handle problems that can't be explained away. He believes he's protecting "
                       "humanity from dangerous Reality Deviants—and he's very good at his job.",
        "strength": 2, "dexterity": 3, "stamina": 3,
        "charisma": 4, "manipulation": 5, "appearance": 3,
        "perception": 4, "intelligence": 5, "wits": 5,
        "alertness": 4, "awareness": 3, "empathy": 3, "intimidation": 4, "leadership": 5, "subterfuge": 5,
        "etiquette": 3, "firearms": 2,
        "academics": 4, "computer": 3, "investigation": 5, "law": 3, "politics": 5, "science": 3,
        "correspondence": 3, "entropy": 2, "mind": 5, "time": 2,
        "arete": 4, "willpower": 8, "quintessence": 10,
    },
    {
        "name": "Dr. Elena Vasquez",
        "concept": "Progenitor researcher studying Awakened biology",
        "affiliation": "Progenitors",
        "description": "Dr. Vasquez runs Prometheus Labs, a biotech startup that's actually a Progenitor "
                       "front. Her research into Awakened physiology has produced treatments that can "
                       "suppress magical abilities—temporarily. She views mages as fascinating specimens "
                       "first and threats second, which makes her arguably more dangerous.",
        "strength": 2, "dexterity": 2, "stamina": 3,
        "charisma": 3, "manipulation": 4, "appearance": 3,
        "perception": 4, "intelligence": 5, "wits": 4,
        "alertness": 3, "awareness": 3, "empathy": 2, "expression": 3, "subterfuge": 3,
        "technology": 4,
        "academics": 4, "computer": 4, "investigation": 3, "medicine": 5, "science": 5,
        "entropy": 2, "life": 5, "matter": 3, "mind": 2,
        "arete": 4, "willpower": 7, "quintessence": 12,
    },
    {
        "name": "Agent Sarah Chen",
        "concept": "Iteration X hunter tracking Reality Deviants",
        "affiliation": "Iteration X",
        "description": "Agent Chen is a cybernetically enhanced operative tasked with eliminating "
                       "dangerous Reality Deviants. Her HIT Mark enhancements make her faster and stronger "
                       "than any human, and her targeting systems never miss. She's been assigned to Seattle "
                       "after eliminating three Marauders in California.",
        "strength": 4, "dexterity": 5, "stamina": 4,
        "charisma": 2, "manipulation": 2, "appearance": 2,
        "perception": 5, "intelligence": 4, "wits": 5,
        "alertness": 5, "athletics": 4, "awareness": 3, "brawl": 4, "intimidation": 3,
        "drive": 3, "firearms": 5, "melee": 3, "stealth": 4, "technology": 4,
        "computer": 4, "investigation": 4, "science": 3,
        "forces": 4, "life": 2, "matter": 3, "time": 2,
        "arete": 4, "willpower": 8, "quintessence": 8,
    },
]


def create_chantry_leadership(chronicle, st_user):
    """Create Chantry leadership NPCs."""
    print("\n--- Creating Chantry Leadership ---")

    for data in CHANTRY_LEADERSHIP:
        mage, created = Mage.objects.get_or_create(
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
            apply_mage_stats(mage, data)
            print(f"  Created: {mage.name} ({data['tradition']})")
        else:
            print(f"  Already exists: {mage.name}")


def create_virtual_adepts(chronicle, st_user):
    """Create Virtual Adept NPCs."""
    print("\n--- Creating Virtual Adepts ---")

    for data in VIRTUAL_ADEPTS:
        mage, created = Mage.objects.get_or_create(
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
            apply_mage_stats(mage, data)
            print(f"  Created: {mage.name}")
        else:
            print(f"  Already exists: {mage.name}")


def create_technocracy_threats(chronicle, st_user):
    """Create Technocracy threat NPCs."""
    print("\n--- Creating Technocracy Threats ---")

    for data in TECHNOCRACY:
        mage, created = Mage.objects.get_or_create(
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
            apply_mage_stats(mage, data)
            print(f"  Created: {mage.name} ({data['affiliation']})")
        else:
            print(f"  Already exists: {mage.name}")


def main():
    """Run the full NPC creation."""
    print("=" * 60)
    print("Seattle Test Chronicle - Mage Major NPCs")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()

    create_chantry_leadership(chronicle, st_user)
    create_virtual_adepts(chronicle, st_user)
    create_technocracy_threats(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Mage major NPCs complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
