"""
Seattle Test Chronicle - Derangement Assignments

Assigns derangements to characters for testing purposes.
Especially relevant for Malkavians, but other characters can have them too.

Run with: python manage.py shell < populate_db/chronicle/test/derangements.py

Prerequisites:
- Run character scripts first (creates characters)
- Run populate_db/derangements.py (creates derangements)
"""

from characters.models.core.derangement import Derangement
from characters.models.core.character import Character as CharacterModel
from game.models import Chronicle


def assign_derangements():
    """Assign derangements to characters."""
    print("Assigning Derangements...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Derangement assignments
    # Format: {character_name: [list of derangement names]}
    assignments = {
        # VAMPIRE - MALKAVIANS (Clan weakness requires derangement)
        "Roland Cross": [
            "Paranoia",  # Sees conspiracies everywhere (fits prophet concept)
        ],

        # VAMPIRE - Others with mental trauma
        "Marcus 'Shadow' Webb": [
            "Obsessive-Compulsive",  # Must organize information
        ],
        "Viktor Krueger": [
            "Paranoia",  # Brujah rage + labor organizer = sees enemies
        ],

        # WEREWOLF - Battle scars and spiritual trauma
        "Runs-Through-Fire": [
            "Fugue",  # PTSD from fire-related trauma
        ],
        "Breaks-the-Chain": [
            "Paranoia",  # Metis constantly watched and judged
        ],

        # MAGE - Paradox and awakening trauma
        "Victor Reyes": [
            "Paranoia",  # Believes "they" are watching through the simulation
        ],
        "Samantha 'Sam' Torres": [
            "Multiple Personalities",  # Dream-walking has fractured her psyche
        ],

        # WRAITH - Death trauma
        "Sarah Chen": [
            "Obsessive-Compulsive",  # Must solve the mystery of her death
        ],
        "Marcus Webb": [
            "Paranoia",  # Can't trust anyone, even in death
        ],
        "Thomas 'Tommy' Park": [
            "Hysteria",  # Emotional volatility from violent death
        ],

        # CHANGELING - Banality exposure and Bedlam
        "Professor Edwin Merriweather": [
            "Schizophrenia",  # Too much time in the Dreaming
        ],
        "Penny Brightwater": [
            "Multiple Personalities",  # Child-like alter vs. fae nature
        ],

        # DEMON - Torment and fallen memories
        "Michael Garrett": [
            "Fugue",  # Host's memories vs. fallen memories
        ],
        "Catherine 'Cat' Steel": [
            "Hysteria",  # Angelic wrath manifests as emotional outbursts
        ],

        # HUNTER - Trauma from the Imbuing
        "Marcus Stone": [
            "Obsessive-Compulsive",  # Must hunt, must protect
        ],
        "Rachel Kim": [
            "Paranoia",  # Sees monsters everywhere
        ],

        # MUMMY - Ancient memories
        "Set-Nakht": [
            "Multiple Personalities",  # Past lives intruding
        ],
        "Senusret": [
            "Paranoia",  # Too many betrayals in 3000 years
        ],
    }

    assigned_count = 0
    skipped_count = 0

    for char_name, derangement_names in assignments.items():
        try:
            char = CharacterModel.objects.get(name=char_name, chronicle=chronicle)

            for derangement_name in derangement_names:
                try:
                    derangement = Derangement.objects.get(name=derangement_name)

                    # Check if already has derangement
                    if char.derangements.filter(pk=derangement.pk).exists():
                        print(f"  Skipping existing: {char_name} has {derangement_name}")
                        skipped_count += 1
                        continue

                    char.derangements.add(derangement)
                    print(f"  Assigned: {char_name} now has {derangement_name}")
                    assigned_count += 1

                except Derangement.DoesNotExist:
                    print(f"  Warning: Derangement '{derangement_name}' not found")
                    skipped_count += 1

        except CharacterModel.DoesNotExist:
            print(f"  Warning: Character '{char_name}' not found")
            skipped_count += 1

    print(f"\nSummary - Assigned: {assigned_count}, Skipped: {skipped_count}")


def list_characters_with_derangements():
    """List all characters with derangements for verification."""
    print("\nCharacters with Derangements:")
    print("-" * 50)

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    chars_with_derangements = CharacterModel.objects.filter(
        chronicle=chronicle,
        derangements__isnull=False
    ).distinct()

    if not chars_with_derangements.exists():
        print("  No characters with derangements found.")
        return

    for char in chars_with_derangements:
        derangements = ", ".join([d.name for d in char.derangements.all()])
        print(f"  {char.name}: {derangements}")


def populate_derangements():
    """Main function to populate derangement assignments."""
    print("=" * 60)
    print("POPULATING DERANGEMENTS")
    print("=" * 60)

    assign_derangements()
    list_characters_with_derangements()

    print("\n" + "=" * 60)
    print("DERANGEMENT POPULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_derangements()

populate_derangements()
