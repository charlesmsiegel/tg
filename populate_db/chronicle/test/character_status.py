"""
Character Status Script

Sets character statuses to various states (Approved, Submitted, etc.)
to simulate a live chronicle with approved PCs and pending submissions.
"""

from characters.models.core import CharacterModel


def populate_character_status():
    """Set character statuses for the Seattle Test Chronicle."""
    chronicle_chars = CharacterModel.objects.filter(
        chronicle__name="Seattle Test Chronicle"
    )

    # Get all characters and set most to Approved
    approved_count = 0
    submitted_count = 0
    retired_count = 0

    for char in chronicle_chars:
        # NPCs should be approved
        if char.npc:
            char.status = "App"
            char.freebies_approved = True
            char.save()
            approved_count += 1
            continue

        # Most PCs should be approved
        # But let's leave a few in different statuses for testing
        name = char.name.lower()

        # A couple characters in Submitted status (pending approval)
        if "chen" in name or "grey" in name:
            char.status = "Sub"
            char.freebies_approved = False
            char.save()
            submitted_count += 1
            continue

        # One retired character per gameline for testing
        if "ashworth" in name:  # Thomas Ashworth - Wraith
            char.status = "Ret"
            char.freebies_approved = True
            char.save()
            retired_count += 1
            continue

        # Everyone else is approved
        char.status = "App"
        char.freebies_approved = True
        char.save()
        approved_count += 1

    print(f"Character Status Update Complete:")
    print(f"  Approved: {approved_count}")
    print(f"  Submitted: {submitted_count}")
    print(f"  Retired: {retired_count}")


if __name__ == "__main__":
    populate_character_status()
