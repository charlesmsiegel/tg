"""
Seattle Test Chronicle - Character Groups

Creates the various character groups (coteries, packs, cabals, etc.) for the test chronicle.
Does NOT create or assign characters - just the group structures.

Run with: python manage.py shell < populate_db/chronicle/test/groups.py

Known Issues:
- Demon groups are called "Conclave" in code, but "Court" in WoD terminology
- Hunter groups use "HunterOrganization" model, not a Group subclass called "Cell"
- Mummy has no group model; using generic Group as workaround
"""

from django.contrib.auth.models import User

from characters.models.changeling import Motley
from characters.models.core import Group
from characters.models.demon import Conclave
from characters.models.hunter import HunterOrganization
from characters.models.mage import Cabal
from characters.models.vampire import Coterie
from characters.models.werewolf import Pack
from characters.models.wraith import Circle
from game.models import Chronicle


# Group definitions by gameline
# Format: (name, description)

COTERIES = [
    (
        "The Inner Circle",
        "The Camarilla elite of Seattle. This coterie controls the city's supernatural "
        "economy and politics from the shadows of corporate boardrooms and exclusive clubs. "
        "Led by the Ventrue financier Marcus Antonio, they maintain order through wealth, "
        "influence, and carefully applied pressure.",
    ),
    (
        "The Night Gallery",
        "Artists and visionaries bound by their obsession with creation and prophecy. "
        "This coterie gathers at underground galleries and exclusive showings, where the "
        "line between art and madness blurs. Their works often predict disasters before "
        "they occur, though few mortals recognize the warnings.",
    ),
    (
        "The Underground",
        "Street-level operators who keep Seattle's supernatural underworld running. "
        "Information brokers, labor advocates, and wilderness scouts who handle the "
        "dirty work the Inner Circle won't touch. They know the city's secrets better "
        "than anyone, from the tunnels below to the forgotten corners above.",
    ),
]

PACKS = [
    (
        "Silicon Fangs",
        "An urban pack of tech-savvy Garou who protect Seattle's spirit landscape from "
        "the corrupting influence of the Weaver's overreach. Glass Walkers, Silent Striders, "
        "and Stargazers working together to maintain balance in a city drowning in technology. "
        "They fight the war for Gaia with code as much as claw.",
    ),
    (
        "The Wardens",
        "Traditional warriors drawn from the proud tribes of the Garou Nation. Get of Fenris, "
        "Shadow Lords, Wendigo, and Uktena united by their dedication to protecting the sacred "
        "places of the Pacific Northwest. They strike hard against Pentex operations and defend "
        "the caerns from all who would defile them.",
    ),
    (
        "The Forgotten",
        "Outcasts and misfits who found each other when no other pack would have them. "
        "A Bone Gnawer trickster and a Red Talon cub struggling with civilization form an "
        "unlikely bond, surviving on the margins of Garou society while proving their worth "
        "through cunning rather than raw strength.",
    ),
]

CABALS = [
    (
        "The Invisible College",
        "A cross-Tradition alliance united by the belief that wisdom transcends factional "
        "boundaries. Euthanatos death-guides, Dreamspeakers, Celestial Choristers, and Cultists "
        "of Ecstasy share knowledge and protect Seattle's Awakened community from threats both "
        "mundane and supernatural. Their diversity is their strength.",
    ),
    (
        "The Digital Underground",
        "Virtual Adepts fighting the Technocracy's control of information one hack at a time. "
        "Reality programmers and data liberators who believe truth should flow freely through "
        "the Digital Web. They've made Seattle's tech infrastructure their battleground, "
        "ensuring the Masses have access to what the Union would hide.",
    ),
    (
        "The Fortunate Few",
        "A small but influential cabal centered around House Fortunae's mastery of fate magic. "
        "Their investments always pay off, their plans rarely fail, and their enemies find "
        "themselves plagued by unfortunate coincidences. The Technocracy watches them closely, "
        "suspicious of their uncanny success.",
    ),
    (
        "The Threshold",
        "Mages who walk the edge between wisdom and oblivion. Founded by a Euthanatos who "
        "nearly fell to the Nephandi, this cabal helps others avoid the same fate. They "
        "specialize in entropy magic and the transformation of the soul, guiding those "
        "who've seen too much darkness back toward the light.",
    ),
]

CIRCLES = [
    (
        "The Unquiet",
        "Wraiths bound by their shared need for resolution. A bootlegger from the 1920s, "
        "an internment camp victim, a cold case murder victim, and a WWI veteran work together "
        "to resolve each other's Fetters while protecting the living descendants who anchor "
        "them to the Skinlands. Their diverse eras bring unique perspectives to the Shadowlands.",
    ),
    (
        "The Watch",
        "Hierarchy loyalists who maintain order in Seattle's Shadowlands. Veterans of different "
        "wars united by duty, they protect weaker wraiths from Spectres and enforce the laws "
        "of the dead. Their efficiency makes them respected—and feared—throughout the local "
        "Necropolis.",
    ),
    (
        "The Lost Generation",
        "Young wraiths still adjusting to death in the modern age. A teenager from the 80s, "
        "a recent overdose victim, and a 90s musician form an unlikely support group, helping "
        "each other navigate the Shadowlands while clinging to the pop culture touchstones "
        "of their abbreviated lives.",
    ),
]

MOTLEYS = [
    (
        "The Toybox Rebellion",
        "Makers and dreamers united by their love of creation. Nockers and a Boggan who've "
        "turned their backs on courtly politics to focus on what matters: building amazing "
        "things and nurturing the dreams of mortals. Their workshop-cafe is a haven for "
        "artists and inventors seeking inspiration.",
    ),
    (
        "The Court of Whispers",
        "Keepers of secrets in Seattle's fae underground. Sluagh and a Sidhe noble who "
        "remember the Shattering trade in information and favors, maintaining an intelligence "
        "network that spans the mortal and chimerical worlds. They know things that could "
        "shake kingdoms—and they never forget.",
    ),
    (
        "The Storm's Eye",
        "Idealists fighting to protect Seattle's dreamers from the crushing weight of Banality. "
        "A passionate Sidhe of House Liam and a Pooka promoter lead this motley, organizing "
        "events and interventions to keep the spark of wonder alive in a city obsessed with "
        "practical innovation.",
    ),
]

CONCLAVES = [
    (
        "The Architects",
        "Demons who fell for pride in creation now work to reshape Seattle according to their "
        "own designs. Malefactors and Fiends united by Faustian ambition and Cryptic curiosity, "
        "they build systems and structures that subtly undermine the divine order while "
        "advancing their own inscrutable agendas.",
    ),
    (
        "The Muses",
        "Reconcilers seeking redemption through inspiring humanity's potential. Defilers and "
        "Neberu who believe the Fallen can find salvation by nurturing mortal creativity and "
        "dreams. They walk among artists and visionaries, kindling sparks of greatness while "
        "searching for their own path back to grace.",
    ),
    (
        "The Reckoning",
        "Demons who've embraced righteous fury and the pursuit of hidden truths. Caught between "
        "Luciferan rebellion and Ravener destruction, they dispense harsh justice and uncover "
        "secrets that Heaven and Hell would prefer stayed buried. Their methods are extreme, "
        "but their convictions are absolute.",
    ),
]

# Hunter Organizations use a different model with additional fields
HUNTER_ORGANIZATIONS = [
    (
        "The Vigil",
        "cell",
        "Direct action against supernatural threats. Hunters who've seen too much to look away.",
        "Protect the innocent by eliminating monsters. No negotiation, no compromise.",
    ),
    (
        "The Network",
        "network",
        "Information gathering and pattern analysis. Knowledge is the first weapon.",
        "Track supernatural activity, build databases, share intelligence between cells.",
    ),
    (
        "The Support Group",
        "cell",
        "Healing the psychological toll of the hunt. Even monster hunters need someone to talk to.",
        "Provide counseling and mentorship to Imbued struggling with their new reality.",
    ),
]

# Mummy Cults - using generic Group model as workaround (no Cult model exists)
MUMMY_CULTS = [
    (
        "The House of Scrolls",
        "Scholars devoted to Thoth, god of wisdom and writing. These mummies seek to recover "
        "and preserve knowledge lost to the ages, from the Library of Alexandria to forgotten "
        "tombs. In Seattle, they work through universities and private collections, piecing "
        "together fragments of eternal truth.",
    ),
    (
        "The Keepers of Ma'at",
        "Guardians of cosmic balance and divine order. Servants of various gods united by their "
        "commitment to maintaining harmony between the mortal world and the divine. They shape "
        "cities, protect artifacts, and ensure sacred geometry flows through modern architecture.",
    ),
    (
        "The Lions of Sekhmet",
        "Warriors blessed by the lioness goddess of war and healing. These mummies have known "
        "violence across countless lives, fighting in every era's conflicts. Some seek worthy "
        "opponents; others try to break the cycle of bloodshed that follows them through eternity.",
    ),
    (
        "The Awakening",
        "Newly risen mummies still piecing together memories of past lives. The resurrection "
        "has barely begun for these Amenti, who struggle to reconcile ancient Egyptian souls "
        "with modern American bodies. They support each other through the confusion of rebirth.",
    ),
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


def create_coteries(chronicle, owner):
    """Create Vampire coteries."""
    print("\n--- Creating Vampire Coteries ---")
    for name, description in COTERIES:
        coterie, created = Coterie.objects.get_or_create(
            name=name,
            chronicle=chronicle,
            defaults={"description": description, "owner": owner},
        )
        if created:
            print(f"Created coterie: {name}")
        else:
            print(f"Coterie already exists: {name}")


def create_packs(chronicle, owner):
    """Create Werewolf packs."""
    print("\n--- Creating Werewolf Packs ---")
    for name, description in PACKS:
        pack, created = Pack.objects.get_or_create(
            name=name,
            chronicle=chronicle,
            defaults={"description": description, "owner": owner},
        )
        if created:
            print(f"Created pack: {name}")
        else:
            print(f"Pack already exists: {name}")


def create_cabals(chronicle, owner):
    """Create Mage cabals."""
    print("\n--- Creating Mage Cabals ---")
    for name, description in CABALS:
        cabal, created = Cabal.objects.get_or_create(
            name=name,
            chronicle=chronicle,
            defaults={"description": description, "owner": owner},
        )
        if created:
            print(f"Created cabal: {name}")
        else:
            print(f"Cabal already exists: {name}")


def create_circles(chronicle, owner):
    """Create Wraith circles."""
    print("\n--- Creating Wraith Circles ---")
    for name, description in CIRCLES:
        circle, created = Circle.objects.get_or_create(
            name=name,
            chronicle=chronicle,
            defaults={"description": description, "owner": owner},
        )
        if created:
            print(f"Created circle: {name}")
        else:
            print(f"Circle already exists: {name}")


def create_motleys(chronicle, owner):
    """Create Changeling motleys."""
    print("\n--- Creating Changeling Motleys ---")
    for name, description in MOTLEYS:
        motley, created = Motley.objects.get_or_create(
            name=name,
            chronicle=chronicle,
            defaults={"description": description, "owner": owner},
        )
        if created:
            print(f"Created motley: {name}")
        else:
            print(f"Motley already exists: {name}")


def create_conclaves(chronicle, owner):
    """Create Demon conclaves."""
    print("\n--- Creating Demon Conclaves ---")
    for name, description in CONCLAVES:
        conclave, created = Conclave.objects.get_or_create(
            name=name,
            chronicle=chronicle,
            defaults={"description": description, "owner": owner},
        )
        if created:
            print(f"Created conclave: {name}")
        else:
            print(f"Conclave already exists: {name}")


def create_hunter_organizations():
    """Create Hunter organizations (cells/networks)."""
    print("\n--- Creating Hunter Organizations ---")
    for name, org_type, philosophy, goals in HUNTER_ORGANIZATIONS:
        org, created = HunterOrganization.objects.get_or_create(
            name=name,
            defaults={
                "organization_type": org_type,
                "philosophy": philosophy,
                "goals": goals,
            },
        )
        if created:
            print(f"Created hunter organization: {name} ({org_type})")
        else:
            print(f"Hunter organization already exists: {name}")


def create_mummy_cults(chronicle, owner):
    """Create Mummy cults using generic Group model (no Cult model exists)."""
    print("\n--- Creating Mummy Cults (as generic Groups) ---")
    for name, description in MUMMY_CULTS:
        # Using base Group model since no Cult model exists
        cult, created = Group.objects.get_or_create(
            name=name,
            chronicle=chronicle,
            defaults={"description": description, "owner": owner},
        )
        if created:
            print(f"Created mummy cult (Group): {name}")
        else:
            print(f"Mummy cult already exists: {name}")


def main():
    """Run the full group setup."""
    print("=" * 60)
    print("Seattle Test Chronicle - Group Setup")
    print("=" * 60)

    chronicle, st_user = get_chronicle_and_st()
    if not chronicle or not st_user:
        return

    # Create groups for each gameline
    create_coteries(chronicle, st_user)
    create_packs(chronicle, st_user)
    create_cabals(chronicle, st_user)
    create_circles(chronicle, st_user)
    create_motleys(chronicle, st_user)
    create_conclaves(chronicle, st_user)
    create_hunter_organizations()
    create_mummy_cults(chronicle, st_user)

    # Summary
    print("\n" + "=" * 60)
    print("Group setup complete!")
    print(f"Coteries: {Coterie.objects.filter(chronicle=chronicle).count()}")
    print(f"Packs: {Pack.objects.filter(chronicle=chronicle).count()}")
    print(f"Cabals: {Cabal.objects.filter(chronicle=chronicle).count()}")
    print(f"Circles: {Circle.objects.filter(chronicle=chronicle).count()}")
    print(f"Motleys: {Motley.objects.filter(chronicle=chronicle).count()}")
    print(f"Conclaves: {Conclave.objects.filter(chronicle=chronicle).count()}")
    print(f"Hunter Organizations: {HunterOrganization.objects.count()}")
    print(f"Mummy Cults (Groups): {Group.objects.filter(chronicle=chronicle, name__in=[c[0] for c in MUMMY_CULTS]).count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    # When run via `python manage.py shell < script.py`
    main()
