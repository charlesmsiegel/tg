"""
Seattle Test Chronicle - Item Ownership and Location

Assigns items to characters (owned_by) and locations (located_at)
using the ManyToMany relationships on ItemModel.

Run with: python manage.py shell < populate_db/chronicle/test/item_ownership.py

Prerequisites:
- Run character scripts first (creates characters)
- Run location scripts first (creates locations)
- Run item scripts first (creates items)
"""

from characters.models.core.character import Character as CharacterModel
from items.models.core.item import ItemModel
from locations.models.core.location import LocationModel
from game.models import Chronicle


def assign_item_ownership():
    """Assign items to character owners via owned_by M2M."""
    print("Assigning Item Ownership...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Item ownership assignments
    # Format: {item_name: [list of character names who own it]}
    ownership = {
        # VAMPIRE ITEMS
        "The Scepter of Seattle": ["Prince Katrina Valdez"],
        "The Keeper's Ledger": ["Adelaide Marsh"],
        "Blood Rose Chalice": ["Isabella Santos"],
        "Shadowstep Cloak": ["Marcus 'Shadow' Webb"],

        # WEREWOLF ITEMS
        "Fang Dagger": ["Runs-Through-Fire"],
        "Spirit Drum": ["Whispers-to-Stars"],
        "Klaive of the North Wind": ["Storm-Singer"],
        "War Hammer of Thunder": ["Judges-the-Fallen"],

        # MAGE ITEMS
        "The Panopticon": ["Victor Reyes"],
        "Staff of the Celestial Order": ["Sister Maria Vasquez"],
        "Quantum Flux Capacitor": ["James 'Axiom' Wright"],

        # WRAITH ITEMS
        "The Soul Mirror": ["Sarah Chen"],
        "Chains of Binding": ["Marcus Webb"],
        "Shroud Weaver's Loom": ["Elena Rodriguez"],

        # CHANGELING ITEMS
        "Dreaming Compass": ["Penny Brightwater"],
        "Thornwood Staff": ["Thornwood"],
        "Professor's Monocle": ["Professor Edwin Merriweather"],

        # DEMON ITEMS
        "The Seal of Solomon": ["Michael Garrett"],
        "Fallen Blade": ["Catherine 'Cat' Steel"],
        "Grimoire of Names": ["Adrian Vex"],

        # HUNTER ITEMS
        "Hunter's Cross": ["Father Thomas Rivera"],
        "Ghost Sight Goggles": ["Dr. Sarah Chen"],
        "Blessed Ammunition": ["Marcus Stone"],

        # MUMMY ITEMS
        "Sekhem Staff": ["Khafre"],
        "Canopic Jar of Set": ["Set-Nakht"],
        "Ankh of Resurrection": ["Merytre"],
    }

    assigned_count = 0
    skipped_count = 0

    for item_name, owner_names in ownership.items():
        try:
            item = ItemModel.objects.get(name=item_name, chronicle=chronicle)

            for owner_name in owner_names:
                try:
                    owner = CharacterModel.objects.get(name=owner_name)

                    # Check if already owned
                    if item.owned_by.filter(pk=owner.pk).exists():
                        print(f"  Skipping existing: {owner_name} owns {item_name}")
                        skipped_count += 1
                        continue

                    item.owned_by.add(owner)
                    print(f"  Assigned: {owner_name} owns {item_name}")
                    assigned_count += 1

                except CharacterModel.DoesNotExist:
                    print(f"  Warning: Character '{owner_name}' not found")
                    skipped_count += 1

        except ItemModel.DoesNotExist:
            print(f"  Warning: Item '{item_name}' not found")
            skipped_count += 1

    print(f"\nOwnership - Assigned: {assigned_count}, Skipped: {skipped_count}")


def assign_item_locations():
    """Assign items to locations via located_at M2M."""
    print("\nAssigning Item Locations...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Item location assignments
    # Format: {item_name: [list of location names where it's located]}
    locations = {
        # VAMPIRE ITEMS - At Court or Havens
        "The Scepter of Seattle": ["Elysium - Pike Place"],
        "The Keeper's Ledger": ["Elysium - Pike Place"],
        "Blood Rose Chalice": ["The Tremere Chantry"],

        # WEREWOLF ITEMS - At Caerns or Septs
        "Spirit Drum": ["Cascade Caern"],
        "Klaive of the North Wind": ["Discovery Park Sept"],

        # MAGE ITEMS - At Chantries
        "Cross House Library": ["The Cross House"],
        "The Panopticon": ["The Digital Sanctum"],
        "Staff of the Celestial Order": ["The Temple of Inner Light"],

        # WRAITH ITEMS - At Haunts
        "The Soul Mirror": ["The Pike Place Haunt"],
        "Chains of Binding": ["Seattle Center Necropolis"],

        # CHANGELING ITEMS - At Freeholds
        "Dreaming Compass": ["The Dreaming Gate Freehold"],
        "Thornwood Staff": ["Green Lake Hollow"],

        # DEMON ITEMS - At Lairs
        "The Seal of Solomon": ["St. Mark's Cathedral"],
        "Grimoire of Names": ["The Athenaeum"],

        # HUNTER ITEMS - At Safehouses
        "Hunter's Cross": ["The Watch House"],
        "Ghost Sight Goggles": ["University Safe House"],

        # MUMMY ITEMS - At Temples
        "Sekhem Staff": ["The Seattle Temple of Ma'at"],
        "Canopic Jar of Set": ["Burke Museum Collection"],
    }

    assigned_count = 0
    skipped_count = 0

    for item_name, location_names in locations.items():
        try:
            item = ItemModel.objects.get(name=item_name, chronicle=chronicle)

            for loc_name in location_names:
                try:
                    location = LocationModel.objects.get(name=loc_name)

                    # Check if already at location
                    if item.located_at.filter(pk=location.pk).exists():
                        print(f"  Skipping existing: {item_name} at {loc_name}")
                        skipped_count += 1
                        continue

                    item.located_at.add(location)
                    print(f"  Assigned: {item_name} located at {loc_name}")
                    assigned_count += 1

                except LocationModel.DoesNotExist:
                    print(f"  Warning: Location '{loc_name}' not found")
                    skipped_count += 1

        except ItemModel.DoesNotExist:
            print(f"  Warning: Item '{item_name}' not found")
            skipped_count += 1

    print(f"\nLocations - Assigned: {assigned_count}, Skipped: {skipped_count}")


def populate_item_ownership():
    """Main function to populate item ownership and locations."""
    print("=" * 60)
    print("POPULATING ITEM OWNERSHIP AND LOCATIONS")
    print("=" * 60)

    assign_item_ownership()
    assign_item_locations()

    print("\n" + "=" * 60)
    print("ITEM OWNERSHIP POPULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_item_ownership()

populate_item_ownership()
