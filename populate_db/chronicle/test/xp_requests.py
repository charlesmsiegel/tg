"""
Seattle Test Chronicle - XP Spending Requests

Creates XP spending requests in various states (pending, approved, denied)
to test the approval workflow.

Run with: python manage.py shell < populate_db/chronicle/test/xp_requests.py

Prerequisites:
- Run character scripts first (creates characters)
- Run xp_weeks.py first (gives characters XP)
"""

from django.contrib.auth.models import User
from django.utils import timezone

from characters.models.core.character import Character as CharacterModel
from game.models import Chronicle, XPSpendingRequest


def create_xp_requests():
    """Create XP spending requests for testing approval workflow."""
    print("Creating XP Spending Requests...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    st_user = User.objects.get(username="storyteller")

    # XP Spending Requests to create
    # Format: {character_name: [(trait_name, trait_type, trait_value, cost, status), ...]}
    # status: "pending", "approved", "denied"
    requests = {
        # VAMPIRE CHARACTERS - Mix of pending and approved
        "Marcus 'Shadow' Webb": [
            ("Obfuscate", "discipline", 3, 14, "pending"),  # Raising Obfuscate 2->3
            ("Computer", "ability", 4, 8, "approved"),      # Computer 3->4 (approved)
        ],
        "Isabella Santos": [
            ("Thaumaturgy", "discipline", 3, 21, "pending"),  # Thaumaturgy 2->3
            ("Occult", "ability", 5, 10, "pending"),          # Occult 4->5 (pending)
        ],
        "Roland Cross": [
            ("Auspex", "discipline", 3, 14, "approved"),   # Auspex 2->3 (approved)
            ("Investigation", "ability", 5, 10, "pending"), # Investigation 4->5
        ],
        "Zoe Kim": [
            ("Presence", "discipline", 3, 14, "denied"),   # Denied - needs justification
            ("Expression", "ability", 5, 10, "pending"),   # Expression 4->5
        ],
        "Viktor Krueger": [
            ("Potence", "discipline", 3, 14, "pending"),   # Potence 2->3
            ("Brawl", "ability", 4, 8, "approved"),        # Brawl 3->4 (approved)
        ],

        # WEREWOLF CHARACTERS
        "Runs-Through-Fire": [
            ("Strength", "attribute", 5, 20, "pending"),   # Strength 4->5
            ("Athletics", "ability", 4, 8, "approved"),    # Athletics 3->4
        ],
        "Whispers-to-Stars": [
            ("Gnosis", "gnosis", 6, 12, "pending"),        # Gnosis 5->6
            ("Occult", "ability", 5, 10, "pending"),       # Occult 4->5
        ],
        "Breaks-the-Chain": [
            ("Wits", "attribute", 4, 16, "pending"),       # Wits 3->4
            ("Stealth", "ability", 3, 6, "approved"),      # Stealth 2->3
        ],

        # MAGE CHARACTERS
        "Victor Reyes": [
            ("Correspondence", "sphere", 4, 28, "pending"),  # Correspondence 3->4
            ("Computer", "ability", 5, 10, "approved"),      # Computer 4->5
        ],
        "Dr. Eleanor Vance": [
            ("Entropy", "sphere", 5, 35, "pending"),       # Entropy 4->5
            ("Medicine", "ability", 5, 10, "approved"),    # Medicine 4->5
        ],
        "Samantha 'Sam' Torres": [
            ("Spirit", "sphere", 4, 28, "pending"),        # Spirit 3->4
            ("Awareness", "ability", 4, 8, "denied"),      # Denied - no in-game development
        ],

        # WRAITH CHARACTERS
        "Sarah Chen": [
            ("Argos", "arcanos", 3, 14, "pending"),        # Argos 2->3
            ("Investigation", "ability", 4, 8, "approved"), # Investigation 3->4
        ],
        "Elena Rodriguez": [
            ("Outrage", "arcanos", 3, 14, "pending"),      # Outrage 2->3
            ("Intimidation", "ability", 3, 6, "pending"),  # Intimidation 2->3
        ],

        # CHANGELING CHARACTERS
        "Penny Brightwater": [
            ("Chicanery", "art", 3, 14, "pending"),        # Chicanery 2->3
            ("Subterfuge", "ability", 4, 8, "approved"),   # Subterfuge 3->4
        ],
        "Professor Edwin Merriweather": [
            ("Soothsay", "art", 4, 21, "pending"),         # Soothsay 3->4
            ("Academics", "ability", 5, 10, "pending"),    # Academics 4->5
        ],

        # DEMON CHARACTERS
        "Michael Garrett": [
            ("Lore of Humanity", "lore", 3, 14, "pending"),  # Humanity 2->3
            ("Empathy", "ability", 4, 8, "approved"),        # Empathy 3->4
        ],
        "Dr. Lilith Morgan": [
            ("Lore of the Fundament", "lore", 4, 21, "pending"),  # Fundament 3->4
            ("Science", "ability", 5, 10, "pending"),             # Science 4->5
        ],

        # HUNTER CHARACTERS
        "Marcus Stone": [
            ("Conviction", "virtue", 4, 20, "pending"),    # Conviction 3->4
            ("Melee", "ability", 4, 8, "approved"),        # Melee 3->4
        ],
        "Dr. Sarah Chen": [
            ("Vision", "virtue", 3, 15, "pending"),        # Vision 2->3
            ("Investigation", "ability", 4, 8, "pending"), # Investigation 3->4
        ],

        # MUMMY CHARACTERS
        "Khafre": [
            ("Sekhem", "sekhem", 4, 28, "pending"),        # Sekhem 3->4
            ("Occult", "ability", 5, 10, "approved"),      # Occult 4->5
        ],
        "Nefertari": [
            ("Manipulation", "attribute", 5, 20, "pending"),  # Manipulation 4->5
            ("Leadership", "ability", 4, 8, "pending"),       # Leadership 3->4
        ],
    }

    created_count = 0
    skipped_count = 0

    for char_name, request_list in requests.items():
        try:
            char = CharacterModel.objects.get(name=char_name, chronicle=chronicle)

            for trait_name, trait_type, trait_value, cost, status in request_list:
                # Determine approved status string
                if status == "approved":
                    approved_status = "approved"
                    approved_by = st_user
                    approved_at = timezone.now()
                elif status == "denied":
                    approved_status = "denied"
                    approved_by = st_user
                    approved_at = timezone.now()
                else:
                    approved_status = "pending"
                    approved_by = None
                    approved_at = None

                # Check if request already exists
                existing = XPSpendingRequest.objects.filter(
                    character=char,
                    trait_name=trait_name,
                    trait_value=trait_value
                ).exists()

                if existing:
                    print(f"  Skipping existing request: {char_name} - {trait_name}")
                    skipped_count += 1
                    continue

                # Create the request
                xp_request = XPSpendingRequest.objects.create(
                    character=char,
                    trait_name=trait_name,
                    trait_type=trait_type,
                    trait_value=trait_value,
                    cost=cost,
                    approved=approved_status,
                    approved_by=approved_by,
                    approved_at=approved_at
                )
                print(f"  Created {status} request: {char_name} - {trait_name} to {trait_value} ({cost} XP)")
                created_count += 1

        except CharacterModel.DoesNotExist:
            print(f"  Warning: Character '{char_name}' not found, skipping")
            skipped_count += 1

    print(f"\nSummary:")
    print(f"  Requests created: {created_count}")
    print(f"  Skipped: {skipped_count}")


def summarize_pending_requests():
    """Print summary of pending XP requests for ST approval."""
    print("\nPending XP Requests for Approval:")
    print("-" * 50)

    pending = XPSpendingRequest.objects.filter(approved="pending")

    if not pending.exists():
        print("  No pending requests.")
        return

    for req in pending:
        print(f"  {req.character.name}: {req.trait_name} -> {req.trait_value} ({req.cost} XP)")

    print(f"\nTotal pending: {pending.count()}")


def populate_xp_requests():
    """Main function to populate XP spending requests."""
    print("=" * 60)
    print("POPULATING XP SPENDING REQUESTS")
    print("=" * 60)

    create_xp_requests()
    summarize_pending_requests()

    print("\n" + "=" * 60)
    print("XP REQUEST POPULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_xp_requests()

populate_xp_requests()
