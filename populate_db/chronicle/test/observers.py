"""
Seattle Test Chronicle - Observer Access

Creates Observer relationships for testing cross-visibility:
- Players can observe other characters they interact with
- ST granted access to sensitive NPCs

Run with: python manage.py shell < populate_db/chronicle/test/observers.py

Prerequisites:
- Run character scripts first (creates characters)
- Run base.py first (creates users)
"""

from django.contrib.auth.models import User

from characters.models.core.character import Character as CharacterModel
from items.models.core.item import ItemModel
from locations.models.core.location import LocationModel
from game.models import Chronicle


def create_character_observers():
    """Create observer relationships between characters."""
    print("Creating Character Observer Relationships...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="storyteller")

    # Observer relationships - who can view what
    # Format: {observer_username: [list of character names they can observe]}
    character_observers = {
        # Vampire player can see some NPC vampires they interact with
        "xXShadowWolfXx": [
            "Prince Katrina Valdez",      # The Prince they report to
            "Dr. Marcus Thorne",          # NPC contact
        ],
        # Mage player can see other tradition mages
        "CrypticMoon": [
            "Dr. Eleanor Vance",          # Fellow Tradition mage
            "Victor Reyes",               # Cabalmate
        ],
        # Werewolf player can see pack allies
        "NightOwl_42": [
            "Storm-Singer",               # Pack ally
            "Elder Speaks-With-Thunder",  # Important NPC
        ],
        # Cross-gameline: a hunter watching a vampire
        "pixel_witch": [
            "Marcus 'Shadow' Webb",       # Vampire they're hunting
        ],
        # Player 5 watches some NPCs
        "ByteSlayer": [
            "The Ferryman",               # Wraith NPC of interest
            "Lord Ashcroft",              # Changeling noble
        ],
        # Player 6 observes cross-gameline
        "RavenInk": [
            "Michael Garrett",            # Demon character
            "Khafre",                      # Mummy
        ],
        # Player 7 can see key political NPCs
        "MidnightCaller": [
            "Prince Katrina Valdez",      # Vampire Prince
            "Duke Thornwood",             # Changeling Duke
        ],
        # Player 8 observes spiritual characters
        "GhostInShell": [
            "Whispers-to-Stars",          # Theurge they've met
            "Sarah Chen",                  # Wraith
        ],
        # Player 9 can see some locations
        "Wanderlust99": [
            "Senusret",                   # Mummy warrior
            "Rev. Samuel Black",          # Demon preacher
        ],
        # Player 10 can see various NPCs
        "StormChaser_X": [
            "Breaks-the-Chain",           # Werewolf they know
            "Penny Brightwater",          # Changeling
        ],
    }

    created_count = 0
    skipped_count = 0

    for observer_username, char_names in character_observers.items():
        try:
            observer_user = User.objects.get(username=observer_username)

            for char_name in char_names:
                try:
                    char = CharacterModel.objects.get(name=char_name)

                    # Check if observer already exists
                    if char.observers.filter(user=observer_user).exists():
                        print(f"  Skipping existing: {observer_username} -> {char_name}")
                        skipped_count += 1
                        continue

                    # Add observer access
                    char.add_observer(observer_user, granted_by=st_user)
                    print(f"  Created: {observer_username} can observe {char_name}")
                    created_count += 1

                except CharacterModel.DoesNotExist:
                    print(f"  Warning: Character '{char_name}' not found, skipping")
                    skipped_count += 1

        except User.DoesNotExist:
            print(f"  Warning: User '{observer_username}' not found, skipping")
            skipped_count += 1

    print(f"\nCharacter Observers - Created: {created_count}, Skipped: {skipped_count}")


def create_location_observers():
    """Create observer relationships for locations."""
    print("\nCreating Location Observer Relationships...")

    st_user = User.objects.get(username="storyteller")

    # Location observers - who can see secret locations
    # Format: {observer_username: [list of location names they can observe]}
    location_observers = {
        # Vampire player can see havens
        "xXShadowWolfXx": [
            "The Underground Haven",
            "Elysium - Pike Place",
        ],
        # Mage player can see chantries
        "CrypticMoon": [
            "The Invisible College Chantry",
            "Pike Place Node",
        ],
        # Werewolf player can see caerns
        "NightOwl_42": [
            "Cascade Caern",
            "Discovery Park Hive",
        ],
        # Changeling player can see freeholds
        "pixel_witch": [
            "The Dreaming Gate Freehold",
            "Pike Place Trod",
        ],
    }

    created_count = 0
    skipped_count = 0

    for observer_username, loc_names in location_observers.items():
        try:
            observer_user = User.objects.get(username=observer_username)

            for loc_name in loc_names:
                try:
                    loc = LocationModel.objects.get(name=loc_name)

                    # Check if observer already exists
                    if loc.observers.filter(user=observer_user).exists():
                        print(f"  Skipping existing: {observer_username} -> {loc_name}")
                        skipped_count += 1
                        continue

                    # Add observer access
                    loc.add_observer(observer_user, granted_by=st_user)
                    print(f"  Created: {observer_username} can observe {loc_name}")
                    created_count += 1

                except LocationModel.DoesNotExist:
                    print(f"  Warning: Location '{loc_name}' not found, skipping")
                    skipped_count += 1

        except User.DoesNotExist:
            print(f"  Warning: User '{observer_username}' not found, skipping")
            skipped_count += 1

    print(f"\nLocation Observers - Created: {created_count}, Skipped: {skipped_count}")


def create_item_observers():
    """Create observer relationships for items."""
    print("\nCreating Item Observer Relationships...")

    st_user = User.objects.get(username="storyteller")

    # Item observers - who can see secret items
    # Format: {observer_username: [list of item names they can observe]}
    item_observers = {
        # Mage player can see other mages' devices
        "CrypticMoon": [
            "The Panopticon",             # Scrying device
            "Quantum Flux Capacitor",     # Talisman
        ],
        # Werewolf player can see fetishes
        "NightOwl_42": [
            "Fang Dagger",
            "Spirit Drum",
        ],
        # Demon player can see relics
        "ByteSlayer": [
            "The Seal of Solomon",
            "Angel Feather",
        ],
    }

    created_count = 0
    skipped_count = 0

    for observer_username, item_names in item_observers.items():
        try:
            observer_user = User.objects.get(username=observer_username)

            for item_name in item_names:
                try:
                    item = ItemModel.objects.get(name=item_name)

                    # Check if observer already exists
                    if item.observers.filter(user=observer_user).exists():
                        print(f"  Skipping existing: {observer_username} -> {item_name}")
                        skipped_count += 1
                        continue

                    # Add observer access
                    item.add_observer(observer_user, granted_by=st_user)
                    print(f"  Created: {observer_username} can observe {item_name}")
                    created_count += 1

                except ItemModel.DoesNotExist:
                    print(f"  Warning: Item '{item_name}' not found, skipping")
                    skipped_count += 1

        except User.DoesNotExist:
            print(f"  Warning: User '{observer_username}' not found, skipping")
            skipped_count += 1

    print(f"\nItem Observers - Created: {created_count}, Skipped: {skipped_count}")


def populate_observers():
    """Main function to populate observer relationships."""
    print("=" * 60)
    print("POPULATING OBSERVER ACCESS")
    print("=" * 60)

    create_character_observers()
    create_location_observers()
    create_item_observers()

    print("\n" + "=" * 60)
    print("OBSERVER POPULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_observers()

populate_observers()
