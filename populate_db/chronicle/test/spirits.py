"""
Seattle Test Chronicle - Spirit Characters

Creates SpiritCharacter NPCs for the test chronicle, including:
- Pack Totems (Werewolf)
- Caern Spirits
- Umbral entities
- Gafflings and Jagglings encountered by characters

Run with: python manage.py shell < populate_db/chronicle/test/spirits.py

Prerequisites:
- Run base.py first (creates chronicle)
- Run populate_db/werewolf/spirit_charms.py (creates charms)
"""

from accounts.models import Profile
from characters.models.werewolf.spirit_character import SpiritCharacter
from characters.models.werewolf.charm import SpiritCharm
from game.models import Chronicle


def create_spirit_characters():
    """Create spirit NPC characters for the chronicle."""
    print("Creating Spirit Characters...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = Profile.objects.get(user__username="DarkMaster99").user

    # Spirit definitions
    spirits = [
        # === PACK TOTEMS ===
        {
            "name": "Iron Wolf",
            "concept": "Totem of the Silicon Fangs pack",
            "description": """A massive spirit wolf with fur of iron gray and eyes that glow
with the light of computer screens. Iron Wolf represents the adaptation of the Garou to
the modern age, embodying both the wild heart of the wolf and the precision of technology.

The totem prowls the Digital Web as easily as the physical Umbra, hunting Pattern Spiders
and defending its pack from Weaver spirits that would trap them in stasis.""",
            "willpower": 7,
            "rage": 6,
            "gnosis": 8,
            "essence": 30,
            "charms": ["Tracking", "Control Electrical Systems", "Materialize", "Armor"],
        },
        {
            "name": "Whisper-in-the-Dark",
            "concept": "Totem of the Wardens pack",
            "description": """An Uktena spirit-guide, Whisper-in-the-Dark appears as a great
serpent made of shadows and starlight. It speaks only in riddles and dream-visions,
guiding its pack to secrets that should remain buried and enemies that must be bound.

The spirit knows many forbidden paths through the Umbra and has ties to spirits that
other totems fear to approach.""",
            "willpower": 9,
            "rage": 3,
            "gnosis": 10,
            "essence": 35,
            "charms": ["Airt Sense", "Realm Sense", "Mind Speech", "Spirit Gossip"],
        },
        {
            "name": "Trash-Heap King",
            "concept": "Totem of the Forgotten pack",
            "description": """A Bone Gnawer totem that appears as a massive rat wearing a
crown made of bottle caps and pull-tabs. Trash-Heap King embodies the resilience of
the forgotten and downtrodden, finding treasure in what others discard.

Despite its humble appearance, the totem commands respect in the urban Umbra, where
the spirits of the dispossessed recognize its authority.""",
            "willpower": 6,
            "rage": 4,
            "gnosis": 7,
            "essence": 25,
            "charms": ["Tracking", "Meld", "Influence", "Flee"],
        },

        # === CAERN SPIRITS ===
        {
            "name": "Heart-of-the-Mountain",
            "concept": "Caern Spirit of Cascade Caern",
            "description": """The mighty spirit of Mount Rainier itself, Heart-of-the-Mountain
appears as a towering figure of stone and volcanic fire. It has watched over the Cascade
Caern for millennia, since before the first Garou came to these lands.

The spirit speaks slowly, its words rumbling like distant earthquakes, and its patience
is legendary. But when roused to anger, its wrath shakes the very foundations of the
mountain.""",
            "willpower": 10,
            "rage": 8,
            "gnosis": 9,
            "essence": 100,
            "charms": ["Materialize", "Armor", "Umbraquake", "Cleanse the Blight"],
        },
        {
            "name": "Old Cedar",
            "concept": "Guardian Spirit of Discovery Park Sept",
            "description": """A nature spirit that has watched over the Discovery Park area
since before Seattle was founded. Old Cedar appears as an ancient tree spirit, its
bark-like skin covered in moss and lichen, with eyes like knotholes that see everything.

The spirit mourns the loss of the old-growth forests but has learned to work with the
Garou who now protect what remains. It is particularly protective of the kinfolk who
maintain the park's natural areas.""",
            "willpower": 8,
            "rage": 4,
            "gnosis": 8,
            "essence": 45,
            "charms": ["Healing", "Cleanse the Blight", "Plant Command", "Meld"],
        },

        # === UMBRAL ENTITIES ===
        {
            "name": "Neon Dragon",
            "concept": "Pattern Spider Major",
            "description": """A powerful Weaver-spirit that manifests as a serpentine dragon
made of flickering neon light and fiber-optic cables. The Neon Dragon patrols Seattle's
technological infrastructure, spinning webs of data and code.

While not inherently hostile, the spirit views anything that disrupts the patterns of
technology as a threat to be neutralized. It has clashed repeatedly with the Virtual
Adepts and Glass Walker theurges who operate in its territory.""",
            "willpower": 7,
            "rage": 5,
            "gnosis": 6,
            "essence": 40,
            "charms": ["Control Electrical Systems", "System Havoc", "Materialize", "Spirit Static"],
        },
        {
            "name": "The Crying Woman",
            "concept": "Wyld Spirit of Pike Place Market",
            "description": """A manifestation of the Wyld chaos that infuses Pike Place Market,
the Crying Woman appears as a weeping figure whose tears become fish that flop away
into nothingness. She embodies the market's chaotic energy - the shouting vendors,
the flying fish, the crush of tourists and locals.

The spirit is unpredictable and dangerous, but those who bring her offerings of
spontaneity and creativity may receive her blessing.""",
            "willpower": 5,
            "rage": 7,
            "gnosis": 9,
            "essence": 35,
            "charms": ["Shapeshift", "Create Water", "Disorient (5 pt)", "Mirage"],
        },

        # === ENEMY SPIRITS ===
        {
            "name": "Smog-Choked",
            "concept": "Bane of Urban Pollution",
            "description": """A Wyrm-spirit born from Seattle's industrial pollution and
vehicle emissions, Smog-Choked appears as a humanoid figure made of gray-brown haze
with burning red eyes. It haunts areas of heavy traffic and industrial activity,
spreading corruption and disease.

The spirit is particularly active during summer inversions when smog blankets the
city, growing stronger as more people cough and wheeze.""",
            "willpower": 6,
            "rage": 7,
            "gnosis": 4,
            "essence": 30,
            "charms": ["Corruption", "Blighted Touch", "Materialize", "Incite Frenzy"],
        },
        {
            "name": "The Clickbait",
            "concept": "Bane of Digital Addiction",
            "description": """A modern Bane born from social media addiction and outrage
culture, the Clickbait appears as a swirling mass of notifications, like-buttons, and
scrolling feeds. It feeds on attention and conflict, driving mortals to endless
doomscrolling and online arguments.

Tech-savvy Garou have identified it as a serious threat to the sept's kinfolk,
especially the younger ones.""",
            "willpower": 5,
            "rage": 6,
            "gnosis": 5,
            "essence": 25,
            "charms": ["Influence", "Possession", "Digital Disruption", "Terror"],
        },

        # === ALLIED SPIRITS ===
        {
            "name": "Grandmother Salmon",
            "concept": "Spirit of Seattle's Waters",
            "description": """An ancient salmon spirit who remembers when the rivers ran
clean and the fish were countless. Grandmother Salmon appears as an enormous silver
salmon whose scales shimmer with memories of spawning runs past.

She aids those who work to restore the waterways and opposes the corruption that
threatens the remaining wild salmon runs. The Uktena have a long alliance with her.""",
            "willpower": 7,
            "rage": 3,
            "gnosis": 9,
            "essence": 40,
            "charms": ["Create Water", "Healing", "Cleanse the Blight", "Dream Journey"],
        },
    ]

    created_count = 0
    skipped_count = 0

    for spirit_data in spirits:
        spirit, created = SpiritCharacter.objects.get_or_create(
            name=spirit_data["name"],
            chronicle=chronicle,
            defaults={
                "owner": st_user,
                "npc": True,
                "description": spirit_data["description"],
                "willpower": spirit_data["willpower"],
                "rage": spirit_data["rage"],
                "gnosis": spirit_data["gnosis"],
                "essence": spirit_data["essence"],
            }
        )

        if created:
            # Assign charms
            for charm_name in spirit_data.get("charms", []):
                try:
                    charm = SpiritCharm.objects.get(name=charm_name)
                    spirit.charms.add(charm)
                except SpiritCharm.DoesNotExist:
                    # Try partial match
                    charms = SpiritCharm.objects.filter(name__icontains=charm_name.split()[0])
                    if charms.exists():
                        spirit.charms.add(charms.first())

            print(f"  Created Spirit: {spirit.name}")
            created_count += 1
        else:
            print(f"  Skipping existing: {spirit.name}")
            skipped_count += 1

    print(f"\nSummary - Created: {created_count}, Skipped: {skipped_count}")


def list_spirits():
    """List all spirits in the chronicle for verification."""
    print("\nSpirits in Seattle Test Chronicle:")
    print("-" * 50)

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    spirits = SpiritCharacter.objects.filter(chronicle=chronicle)

    if not spirits.exists():
        print("  No spirits found.")
        return

    for spirit in spirits:
        charms = ", ".join([c.name for c in spirit.charms.all()[:3]])
        if spirit.charms.count() > 3:
            charms += f"... (+{spirit.charms.count() - 3} more)"
        print(f"  {spirit.name}")
        print(f"    Will {spirit.willpower} | Rage {spirit.rage} | Gnosis {spirit.gnosis} | Essence {spirit.essence}")
        if charms:
            print(f"    Charms: {charms}")


def populate_spirits():
    """Main function to populate spirit characters."""
    print("=" * 60)
    print("POPULATING SPIRIT CHARACTERS")
    print("=" * 60)

    create_spirit_characters()
    list_spirits()

    print("\n" + "=" * 60)
    print("SPIRIT POPULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_spirits()

populate_spirits()
