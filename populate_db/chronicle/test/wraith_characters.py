"""
Seattle Test Chronicle - Wraith Characters

Creates Wraith characters for the test chronicle.
Assigns characters to circles.

Run with: python manage.py shell < populate_db/chronicle/test/wraith_characters.py

Prerequisites:
- Run base.py first (creates chronicle and users)
- Run groups.py first (creates circles)
- Wraith data must be loaded (guilds, arcanoi, etc.)
"""

from django.contrib.auth.models import User

from characters.models.wraith.wraith import Wraith
from characters.models.wraith.guild import Guild
from characters.models.wraith.circle import Circle
from game.models import Chronicle


# =============================================================================
# WRAITH CHARACTER DEFINITIONS
# =============================================================================

WRAITHS = [
    {
        "username": "xXShadowWolfXx",
        "name": "Thomas Blackwood",
        "concept": "1920s bootlegger haunting his old speakeasy",
        "circle": "The Unquiet",
        "death_era": "1920s",
        # Attributes (7/5/3)
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 3, "manipulation": 4, "appearance": 2,  # Social: 6
        "perception": 3, "intelligence": 3, "wits": 2,  # Mental: 5
        # Abilities (13/9/5)
        "alertness": 2, "athletics": 1, "brawl": 2, "empathy": 2, "streetwise": 4, "subterfuge": 3,  # Talents: 14
        "drive": 2, "firearms": 3, "larceny": 3, "stealth": 2,  # Skills: 10
        "finance": 2, "investigation": 2, "law": 1,  # Knowledges: 5
        # Arcanoi (5 dots)
        "inhabit": 2, "phantasm": 2, "argos": 1,
        # Core stats
        "corpus": 10, "pathos_permanent": 5, "willpower": 5,
        # Backgrounds - NOTE: Haunt 3 = the speakeasy, Memoriam 2 = great-granddaughter
        "haunt": 3, "memoriam": 2, "contacts": 1,
        "description": "A 1920s bootlegger who died in a police raid, still haunting the underground speakeasy "
                       "that became his Haunt. His Fetters are the building and his great-granddaughter who now owns it.",
    },
    {
        "username": "CrypticMoon",
        "name": "Lily Tanaka",
        "concept": "Internment camp victim watching over descendants",
        "circle": "The Unquiet",
        "death_era": "1940s",
        # Attributes (7/5/3)
        "strength": 1, "dexterity": 2, "stamina": 2,  # Physical: 3
        "charisma": 3, "manipulation": 2, "appearance": 3,  # Social: 5
        "perception": 4, "intelligence": 3, "wits": 3,  # Mental: 7
        # Abilities (13/9/5)
        "alertness": 3, "awareness": 2, "empathy": 4, "expression": 2, "subterfuge": 2,  # Talents: 13
        "crafts": 2, "etiquette": 2, "stealth": 3,  # Skills: 7 - adjust
        "academics": 2, "investigation": 2, "occult": 2,  # Knowledges: 6
        # Arcanoi (5 dots)
        "lifeweb": 3, "keening": 2,
        # Core stats
        "corpus": 10, "pathos_permanent": 6, "willpower": 6,
        # Backgrounds - NOTE: Memoriam 3 = family heirlooms scattered as Fetters
        "memoriam": 3, "legacy": 2, "allies": 1,
        "description": "A Japanese-American woman who died in the internment camps, her Fetters tied to family heirlooms "
                       "scattered across Seattle. She watches over her descendants with fierce protectiveness.",
    },
    {
        "username": "NightOwl_42",
        "name": "Corporal James Murphy",
        "concept": "WWI veteran confused by the modern world",
        "circle": "The Unquiet",
        "death_era": "1918",
        # Attributes (7/5/3)
        "strength": 3, "dexterity": 2, "stamina": 3,  # Physical: 5
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 3, "intelligence": 2, "wits": 4,  # Mental: 6
        # Abilities (13/9/5)
        "alertness": 3, "athletics": 2, "brawl": 3, "intimidation": 2,  # Talents: 10
        "firearms": 3, "melee": 2, "stealth": 2, "survival": 2,  # Skills: 9
        "medicine": 2, "occult": 1, "academics": 2,  # Knowledges: 5
        # Arcanoi (5 dots)
        "outrage": 3, "embody": 2,
        # Core stats
        "corpus": 10, "pathos_permanent": 4, "willpower": 5,
        # Backgrounds - NOTE: Legacy 2 = misspelled name on memorial (Fetter)
        "legacy": 2, "artifact": 1, "memoriam": 1,
        "description": "A WWI doughboy who died of Spanish Flu in 1918, confused why the world changed so much. "
                       "His Fetter is a war memorial where his name is misspelled.",
    },
    {
        "username": "pixel_witch",
        "name": "Arcade",
        "concept": "1989 teenager who experiences reality as a game",
        "circle": "The Lost Generation",
        "death_era": "1989",
        # Attributes (7/5/3)
        "strength": 2, "dexterity": 4, "stamina": 2,  # Physical: 5
        "charisma": 3, "manipulation": 2, "appearance": 3,  # Social: 5
        "perception": 3, "intelligence": 2, "wits": 2,  # Mental: 4
        # Abilities (13/9/5)
        "alertness": 2, "athletics": 3, "brawl": 1, "empathy": 2, "expression": 2, "streetwise": 2,  # Talents: 12
        "crafts": 1, "drive": 2, "technology": 3, "stealth": 2,  # Skills: 8
        "computer": 2, "investigation": 2, "science": 1,  # Knowledges: 5
        # Arcanoi (5 dots)
        "inhabit": 3, "phantasm": 2,
        # Core stats
        "corpus": 10, "pathos_permanent": 5, "willpower": 4,
        # Backgrounds - NOTE: Artifact 2 = old arcade cabinet (Fetter that keeps being restored)
        "artifact": 2, "memoriam": 1, "contacts": 1,
        "description": "A teenager who died in a car crash in 1989, her Fetter an old arcade cabinet that keeps "
                       "getting restored and resold. She experiences reality as a game she's determined to beat.",
    },
    {
        "username": "ByteSlayer",
        "name": "Sergeant Major William Price",
        "concept": "Vietnam veteran protecting homeless wraiths",
        "circle": "The Watch",
        "death_era": "2000s",
        # Attributes (7/5/3)
        "strength": 3, "dexterity": 3, "stamina": 3,  # Physical: 6
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 3, "intelligence": 2, "wits": 4,  # Mental: 6
        # Abilities (13/9/5)
        "alertness": 3, "athletics": 2, "brawl": 3, "intimidation": 3, "leadership": 2,  # Talents: 13
        "firearms": 3, "melee": 2, "stealth": 2, "survival": 2,  # Skills: 9
        "medicine": 2, "investigation": 2, "tactics": 1,  # Knowledges: 5
        # Arcanoi (5 dots)
        "outrage": 3, "castigate": 2,
        # Core stats
        "corpus": 10, "pathos_permanent": 5, "willpower": 6,
        # Backgrounds - NOTE: Artifact 2 = dog tags (multiple Fetters in pawn shops)
        "artifact": 2, "status_background": 2, "allies": 1,
        "description": "A Vietnam veteran who died homeless on Seattle streets, his Fetters are dog tags "
                       "held by various pawn shops. He protects homeless Wraiths from Spectres.",
    },
    {
        "username": "gh0st_in_shell",
        "name": "Jane Doe #47",
        "concept": "Cold case murder victim seeking closure for others",
        "circle": "The Unquiet",
        "death_era": "1970s",
        # Attributes (7/5/3)
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 2, "manipulation": 2, "appearance": 2,  # Social: 3
        "perception": 4, "intelligence": 4, "wits": 3,  # Mental: 8
        # Abilities (13/9/5)
        "alertness": 3, "awareness": 3, "empathy": 2, "subterfuge": 2,  # Talents: 10
        "investigation": 3, "stealth": 4, "larceny": 2,  # Skills: 9
        "academics": 2, "investigation": 4, "law": 2,  # Knowledges: 8
        # Arcanoi (5 dots)
        "fatalism": 3, "mnemosynis": 2,
        # Core stats
        "corpus": 10, "pathos_permanent": 5, "willpower": 5,
        # Backgrounds - NOTE: Legacy 2 = case file in cold case archives (Fetter)
        "legacy": 2, "contacts": 2,
        "description": "A murder victim from the 1970s, identity unknown, her Fetter is the case file in Seattle PD's "
                       "cold case archives. She solves murders so others get the closure she never will.",
    },
    {
        "username": "Zephyr_Storm",
        "name": "Captain Henrik Johansson",
        "concept": "19th century ship captain lost at sea",
        "circle": "The Watch",
        "death_era": "1880s",
        # Attributes (7/5/3)
        "strength": 3, "dexterity": 2, "stamina": 3,  # Physical: 5
        "charisma": 3, "manipulation": 3, "appearance": 2,  # Social: 5
        "perception": 3, "intelligence": 2, "wits": 3,  # Mental: 5
        # Abilities (13/9/5)
        "alertness": 2, "athletics": 2, "brawl": 2, "intimidation": 2, "leadership": 4,  # Talents: 12
        "crafts": 2, "melee": 2, "navigation": 3, "survival": 2,  # Skills: 9
        "academics": 2, "occult": 2,  # Knowledges: 4
        # Arcanoi (5 dots)
        "argos": 3, "outrage": 2,
        # Core stats
        "corpus": 10, "pathos_permanent": 5, "willpower": 6,
        # Backgrounds - NOTE: Artifact 3 = ship's bell in maritime museum (Fetter)
        "artifact": 3, "status_background": 2,
        "description": "A 19th century ship captain who went down with his vessel in Puget Sound, "
                       "his Fetter a ship's bell now displayed in a maritime museum.",
    },
    {
        "username": "n00b_hunter",
        "name": "Brandon Cole",
        "concept": "Teenager still figuring out being dead",
        "circle": "The Lost Generation",
        "death_era": "recent",
        # Attributes (7/5/3)
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 3, "manipulation": 2, "appearance": 3,  # Social: 5
        "perception": 3, "intelligence": 2, "wits": 3,  # Mental: 5
        # Abilities (13/9/5)
        "alertness": 2, "athletics": 2, "brawl": 1, "empathy": 3, "expression": 2, "streetwise": 2,  # Talents: 12
        "computer": 2, "drive": 2, "performance": 2, "stealth": 1,  # Skills: 7
        "academics": 2, "investigation": 1, "science": 1,  # Knowledges: 4
        # Arcanoi (5 dots) - minimal, new wraith
        "embody": 2, "phantasm": 2, "keening": 1,
        # Core stats
        "corpus": 10, "pathos_permanent": 4, "willpower": 3,
        # Backgrounds - NOTE: Memoriam 2 = friends who moved on (Fetters)
        "memoriam": 2, "contacts": 1,
        "description": "A teenager who overdosed at a party last year, his Fetters tied to friends who moved on "
                       "faster than he'd like. He's still figuring out being dead.",
    },
    {
        "username": "ElectricDreamer",
        "name": "FREQUENCY",
        "concept": "1990s electronic musician haunting his unreleased demos",
        "circle": "The Lost Generation",
        "death_era": "1990s",
        # Attributes (7/5/3)
        "strength": 2, "dexterity": 3, "stamina": 2,  # Physical: 4
        "charisma": 4, "manipulation": 2, "appearance": 3,  # Social: 6
        "perception": 3, "intelligence": 2, "wits": 3,  # Mental: 5
        # Abilities (13/9/5)
        "alertness": 2, "awareness": 2, "empathy": 2, "expression": 4, "streetwise": 2,  # Talents: 12
        "crafts": 2, "performance": 4, "technology": 3,  # Skills: 9
        "academics": 1, "computer": 2, "occult": 2,  # Knowledges: 5
        # Arcanoi (5 dots)
        "keening": 3, "inhabit": 2,
        # Core stats
        "corpus": 10, "pathos_permanent": 5, "willpower": 4,
        # Backgrounds - NOTE: Artifact 2 = demo tape (Fetter that keeps showing up in thrift stores)
        "artifact": 2, "memoriam": 2,
        "description": "A 1990s electronic musician who died of a drug overdose, his Fetter a demo tape of "
                       "unreleased songs that keeps showing up in thrift stores.",
    },
    {
        "username": "void_whisper",
        "name": "The Silence",
        "concept": "Medieval executioner serving as efficient Reaper",
        "circle": "The Watch",
        "death_era": "unknown/ancient",
        # Attributes (7/5/3)
        "strength": 3, "dexterity": 4, "stamina": 2,  # Physical: 6
        "charisma": 1, "manipulation": 3, "appearance": 1,  # Social: 3
        "perception": 4, "intelligence": 3, "wits": 3,  # Mental: 7
        # Abilities (13/9/5)
        "alertness": 3, "athletics": 2, "brawl": 2, "intimidation": 4,  # Talents: 11
        "melee": 4, "stealth": 4, "survival": 2,  # Skills: 10
        "investigation": 2, "occult": 3,  # Knowledges: 5
        # Arcanoi (5 dots)
        "castigate": 3, "argos": 2,
        # Core stats
        "corpus": 10, "pathos_permanent": 4, "willpower": 7,
        # Backgrounds - NOTE: Status 3 = Hierarchy rank, Artifact 1 = unknown Fetter
        "status_background": 3, "artifact": 1,
        "description": "A medieval executioner who followed the settlers west, Fetter unknown even to her. "
                       "She serves the Hierarchy as an efficient Reaper, collecting souls without question.",
    },
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_circle(circle_name, chronicle):
    """Get a circle by name."""
    circle = Circle.objects.filter(name=circle_name, chronicle=chronicle).first()
    if not circle:
        print(f"WARNING: Circle {circle_name} not found.")
    return circle


def apply_wraith_stats(wraith, data):
    """Apply stats from data dict to wraith."""
    # Attributes
    for attr in ["strength", "dexterity", "stamina",
                 "charisma", "manipulation", "appearance",
                 "perception", "intelligence", "wits"]:
        if attr in data:
            setattr(wraith, attr, data[attr])

    # Abilities (WtO-specific)
    abilities = [
        "alertness", "athletics", "brawl", "empathy", "expression",
        "intimidation", "streetwise", "subterfuge", "awareness", "leadership",
        "crafts", "drive", "etiquette", "firearms", "melee", "stealth",
        "larceny", "performance", "survival", "technology",
        "academics", "computer", "investigation", "medicine", "science",
        "finance", "law", "occult", "politics",
    ]
    for ability in abilities:
        if ability in data:
            setattr(wraith, ability, data[ability])

    # Arcanoi
    arcanoi = [
        "argos", "castigate", "embody", "fatalism", "flux",
        "inhabit", "keening", "lifeweb", "moliate", "mnemosynis",
        "outrage", "pandemonium", "phantasm", "usury", "intimation",
    ]
    for arcanos in arcanoi:
        if arcanos in data:
            setattr(wraith, arcanos, data[arcanos])

    # Core wraith stats
    if "corpus" in data:
        wraith.corpus = data["corpus"]
    if "pathos_permanent" in data:
        wraith.pathos_permanent = data["pathos_permanent"]
        wraith.pathos = data["pathos_permanent"]

    # Willpower
    if "willpower" in data:
        wraith.willpower = data["willpower"]
        wraith.temporary_willpower = data["willpower"]


# =============================================================================
# MAIN CREATION FUNCTIONS
# =============================================================================

def create_wraiths(chronicle):
    """Create all wraith characters."""
    print("\n--- Creating Wraiths ---")
    created_wraiths = {}

    for wdata in WRAITHS:
        user = User.objects.filter(username=wdata["username"]).first()
        if not user:
            print(f"  ERROR: User {wdata['username']} not found")
            continue

        wraith, created = Wraith.objects.get_or_create(
            name=wdata["name"],
            owner=user,
            chronicle=chronicle,
            defaults={
                "concept": wdata["concept"],
                "description": wdata.get("description", ""),
                "npc": False,
            }
        )

        if created:
            # Apply stats
            apply_wraith_stats(wraith, wdata)

            wraith.save()
            print(f"  Created wraith: {wdata['name']} ({wdata.get('death_era', 'unknown')})")
        else:
            print(f"  Wraith already exists: {wdata['name']}")

        created_wraiths[wdata["name"]] = wraith

        # Handle circle membership
        if wdata.get("circle"):
            circle = get_circle(wdata["circle"], chronicle)
            if circle:
                circle.members.add(wraith)

    return created_wraiths


def main():
    """Run the full wraith character setup."""
    print("=" * 60)
    print("Seattle Test Chronicle - Wraith Character Setup")
    print("=" * 60)

    chronicle = Chronicle.objects.filter(name="Seattle Test Chronicle").first()
    if not chronicle:
        print("ERROR: Seattle Test Chronicle not found. Run base.py first.")
        return

    # Create characters
    wraiths = create_wraiths(chronicle)

    # Summary
    print("\n" + "=" * 60)
    print("Wraith character setup complete!")
    print(f"Wraiths: {Wraith.objects.filter(chronicle=chronicle).count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    main()
