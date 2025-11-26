"""
Seattle Test Chronicle - Location Hierarchy

Sets up parent-child relationships between locations to create
a nested location structure (e.g., rooms within buildings,
neighborhoods within cities).

Run with: python manage.py shell < populate_db/chronicle/test/location_nesting.py

Prerequisites:
- Run location scripts first (creates locations)
"""

from locations.models.core.location import LocationModel
from game.models import Chronicle


def setup_location_hierarchy():
    """Set up parent-child relationships for locations."""
    print("Setting up Location Hierarchy...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Location hierarchy definitions
    # Format: {parent_name: [list of child location names]}
    hierarchy = {
        # SEATTLE ROOT LOCATIONS
        # Vampire locations nested under Elysiums/Domains
        "Seattle Art Museum": [
            "Olympic Sculpture Park Gallery",  # If exists
        ],

        # Mage locations - Chantries containing sub-locations
        "The Cross House": [
            "Cross House Library",
            "Cross House Sanctum",
        ],
        "The Digital Sanctum": [
            "Server Farm Node",
        ],
        "Prometheus Labs": [
            "Lab Alpha",
            "Lab Beta",
        ],

        # Werewolf locations - Caerns containing sacred sites
        "Cascade Caern": [
            "Heart of the Mountain",
            "The Hunting Grounds",
        ],
        "Discovery Park Sept": [
            "Gathering Stone",
            "Spirit Lodge",
        ],

        # Wraith locations - Necropoli containing haunts
        "Seattle Center Necropolis": [
            "The Space Needle Haunt",
            "Experience Music Project Nihil",
        ],
        "Pike Place Market Haunt": [
            "The Underground Passages",
            "Rachel the Pig Shrine",
        ],

        # Changeling locations - Freeholds containing trod entrances
        "The Dreaming Gate Freehold": [
            "Freehold Court Chamber",
            "Dream Garden",
        ],
        "Green Lake Hollow": [
            "The Willow Circle",
        ],

        # Demon locations - Lairs within larger structures
        "St. Mark's Cathedral": [
            "Cathedral Crypts",
            "Bell Tower Sanctum",
        ],

        # Hunter locations - Safehouses with secure rooms
        "The Watch House": [
            "Armory",
            "Communications Center",
        ],

        # Mummy locations - Temples with inner chambers
        "The Seattle Temple of Ma'at": [
            "Inner Sanctum",
            "Hall of Judgment",
        ],
    }

    nested_count = 0
    skipped_count = 0

    for parent_name, children in hierarchy.items():
        try:
            parent = LocationModel.objects.get(name=parent_name, chronicle=chronicle)

            for child_name in children:
                try:
                    child = LocationModel.objects.get(name=child_name, chronicle=chronicle)

                    # Check if already nested
                    if child.parent == parent:
                        print(f"  Skipping existing: {child_name} already under {parent_name}")
                        skipped_count += 1
                        continue

                    # Set parent relationship
                    child.parent = parent
                    child.save()
                    print(f"  Nested: {child_name} under {parent_name}")
                    nested_count += 1

                except LocationModel.DoesNotExist:
                    # Create a simple sub-location if it doesn't exist
                    child = LocationModel.objects.create(
                        name=child_name,
                        chronicle=chronicle,
                        parent=parent,
                        description=f"A sub-location within {parent_name}.",
                        owner=parent.owner
                    )
                    print(f"  Created and nested: {child_name} under {parent_name}")
                    nested_count += 1

        except LocationModel.DoesNotExist:
            print(f"  Warning: Parent location '{parent_name}' not found, skipping children")
            skipped_count += len(children)

    print(f"\nSummary - Nested: {nested_count}, Skipped: {skipped_count}")


def list_location_tree():
    """Print the location hierarchy tree for verification."""
    print("\nLocation Hierarchy Tree:")
    print("-" * 50)

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Get root locations (no parent)
    roots = LocationModel.objects.filter(chronicle=chronicle, parent__isnull=True)

    def print_tree(location, indent=0):
        prefix = "  " * indent + ("└─ " if indent > 0 else "")
        child_count = LocationModel.objects.filter(parent=location).count()
        suffix = f" ({child_count} children)" if child_count > 0 else ""
        print(f"{prefix}{location.name}{suffix}")

        children = LocationModel.objects.filter(parent=location)
        for child in children:
            print_tree(child, indent + 1)

    for root in roots[:10]:  # Limit to first 10 roots to avoid overwhelming output
        print_tree(root)

    remaining = roots.count() - 10
    if remaining > 0:
        print(f"\n  ... and {remaining} more root locations")


def populate_location_nesting():
    """Main function to populate location hierarchy."""
    print("=" * 60)
    print("POPULATING LOCATION HIERARCHY")
    print("=" * 60)

    setup_location_hierarchy()
    list_location_tree()

    print("\n" + "=" * 60)
    print("LOCATION HIERARCHY COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_location_nesting()

populate_location_nesting()
