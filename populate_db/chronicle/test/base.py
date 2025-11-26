"""
Seattle Test Chronicle - Base Setup

Creates the chronicle, users, and ST relationships for the test chronicle.
Run with: python manage.py shell < populate_db/chronicle/test/base.py
"""

from django.contrib.auth.models import User

from game.models import Chronicle, Gameline, SettingElement, STRelationship

# User definitions: (username, email, is_st)
USER_DATA = [
    ("DarkMaster99", "darkmaster99@test.com", True),  # Head ST
    ("xXShadowWolfXx", "shadowwolf@test.com", False),
    ("CrypticMoon", "crypticmoon@test.com", False),
    ("NightOwl_42", "nightowl42@test.com", False),
    ("pixel_witch", "pixelwitch@test.com", False),
    ("ByteSlayer", "byteslayer@test.com", False),
    ("gh0st_in_shell", "ghostinshell@test.com", False),
    ("Zephyr_Storm", "zephyrstorm@test.com", False),
    ("n00b_hunter", "noobhunter@test.com", False),
    ("ElectricDreamer", "electricdreamer@test.com", False),
    ("void_whisper", "voidwhisper@test.com", False),
]

# Setting elements that differ from standard WoD
SETTING_ELEMENTS = [
    (
        "The Silicon Pact",
        "In 1995, the major supernatural factions of Seattle formed an uneasy truce "
        "to prevent their conflicts from disrupting the tech industry boom. This pact "
        "is fraying as tensions rise.",
    ),
    (
        "The Needle's Shadow",
        "The Space Needle serves as neutral ground where representatives of different "
        "factions can meet. It's protected by ancient wards that predate the structure itself.",
    ),
    (
        "Underground Seattle",
        "The abandoned underground city beneath Pioneer Square has become a haven for "
        "those who don't fit into the surface politics. It's technically unclaimed territory.",
    ),
    (
        "Microsoft's Secret",
        "A cabal of technomancers embedded in major tech companies has been quietly "
        "advancing the Digital Web's influence. Other factions are just now becoming aware of this.",
    ),
    (
        "The Emerald Court's Decline",
        "The local Changeling freehold has been slowly dying as Seattle's dreamers became "
        "obsessed with practical tech pursuits rather than creativity for its own sake.",
    ),
    (
        "The Sound's Depths",
        "Puget Sound holds secrets. Ships occasionally go missing, and strange things "
        "wash ashore. The Garou know something lurks there but won't speak of it.",
    ),
    (
        "Rain City Wraiths",
        "Seattle's perpetual gray weather creates a thin Shroud, making it easier for the "
        "dead to interact with the living. Ghost sightings are common but dismissed as urban legend.",
    ),
    (
        "The Coffee Conspiracy",
        "The explosive growth of Seattle's coffee culture wasn't entirely natural. Certain "
        "parties have been using it to distribute subtle alchemical compounds.",
    ),
]


def create_users():
    """Create test users. Profiles are auto-created via signal."""
    users = {}
    for username, email, is_st in USER_DATA:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        if created:
            user.set_password("testpassword123")
            user.save()
            print(f"Created user: {username}")
        else:
            print(f"User already exists: {username}")
        users[username] = user
    return users


def create_chronicle():
    """Create the Seattle Test Chronicle."""
    chronicle, created = Chronicle.objects.get_or_create(
        name="Seattle Test Chronicle",
        defaults={
            "theme": "Hidden power struggles beneath the tech boom",
            "mood": "Paranoid optimism - innovation masks ancient conflicts",
            "year": 2024,
            "headings": "wod_heading",
        },
    )
    if created:
        print("Created chronicle: Seattle Test Chronicle")
    else:
        print("Chronicle already exists: Seattle Test Chronicle")
    return chronicle


def create_setting_elements(chronicle):
    """Create setting elements and add them to the chronicle."""
    for name, description in SETTING_ELEMENTS:
        element, created = SettingElement.objects.get_or_create(
            name=name,
            defaults={"description": description},
        )
        if element not in chronicle.common_knowledge_elements.all():
            chronicle.common_knowledge_elements.add(element)
        if created:
            print(f"Created setting element: {name}")
        else:
            print(f"Setting element already exists: {name}")


def create_st_relationships(chronicle, st_user):
    """Create ST relationships for all gamelines."""
    # Get all main gamelines
    gameline_names = [
        "World of Darkness",
        "Vampire: the Masquerade",
        "Werewolf: the Apocalypse",
        "Mage: the Ascension",
        "Changeling: the Dreaming",
        "Wraith: the Oblivion",
        "Hunter: the Reckoning",
        "Mummy: the Resurrection",
        "Demon: the Fallen",
    ]

    for gameline_name in gameline_names:
        gameline = Gameline.objects.filter(name=gameline_name).first()
        if gameline:
            relationship, created = STRelationship.objects.get_or_create(
                user=st_user,
                chronicle=chronicle,
                gameline=gameline,
            )
            if created:
                print(f"Created ST relationship: {st_user.username} -> {gameline_name}")
            else:
                print(f"ST relationship already exists: {st_user.username} -> {gameline_name}")
        else:
            print(f"Warning: Gameline not found: {gameline_name}")

    # Set as head ST
    if chronicle.head_st != st_user:
        chronicle.head_st = st_user
        chronicle.save()
        print(f"Set {st_user.username} as head ST")


def main():
    """Run the full setup."""
    print("=" * 60)
    print("Seattle Test Chronicle - Base Setup")
    print("=" * 60)

    # Create users
    print("\n--- Creating Users ---")
    users = create_users()

    # Create chronicle
    print("\n--- Creating Chronicle ---")
    chronicle = create_chronicle()

    # Create setting elements
    print("\n--- Creating Setting Elements ---")
    create_setting_elements(chronicle)

    # Set up ST relationships (DarkMaster99 is the ST)
    print("\n--- Creating ST Relationships ---")
    st_user = users["DarkMaster99"]
    create_st_relationships(chronicle, st_user)

    print("\n" + "=" * 60)
    print("Setup complete!")
    print(f"Chronicle: {chronicle.name}")
    print(f"Head ST: {chronicle.head_st.username if chronicle.head_st else 'None'}")
    print(f"Total users: {len(users)}")
    print(f"Setting elements: {chronicle.common_knowledge_elements.count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
else:
    # When run via `python manage.py shell < script.py`
    main()
