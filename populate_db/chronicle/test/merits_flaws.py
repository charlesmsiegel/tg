"""
Seattle Test Chronicle - Merit and Flaw Assignments

Assigns merits and flaws to characters for testing purposes.
Uses the MeritFlawRating through model via character.add_mf().

Run with: python manage.py shell < populate_db/chronicle/test/merits_flaws.py

Prerequisites:
- Run character scripts first (creates characters)
- Merit/flaw data must be loaded (populate_db/merits_and_flaws_INC.py)
"""

from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.character import Character as CharacterModel
from game.models import Chronicle


def assign_merits_and_flaws():
    """Assign merits and flaws to characters based on their gameline."""
    print("Assigning Merits and Flaws...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Merit/Flaw assignments by character name
    # Format: {character_name: [(merit_name, rating), ...]}
    # Positive ratings = Merits, Negative ratings = Flaws
    assignments = {
        # VAMPIRE CHARACTERS
        "Marcus 'Shadow' Webb": [
            ("Acute Senses", 1),           # Merit: Enhanced perception
            ("Curiosity", -2),             # Flaw: Compulsion to investigate
        ],
        "Isabella Santos": [
            ("Concentration", 1),          # Merit: Focus under pressure
            ("Intolerance", -1),           # Flaw: Hatred of incompetence
        ],
        "Roland Cross": [
            ("Common Sense", 1),           # Merit: GM hint system
            ("Nightmares", -1),            # Flaw: Prophetic nightmares
        ],
        "Zoe Kim": [
            ("Eidetic Memory", 2),         # Merit: Perfect recall
            ("Overconfident", -1),         # Flaw: Too sure of abilities
        ],
        "Viktor Krueger": [
            ("Ambidextrous", 1),           # Merit: Both-handed
            ("Short Fuse", -2),            # Flaw: Brujah rage
        ],

        # WEREWOLF CHARACTERS
        "Runs-Through-Fire": [
            ("Physically Impressive", 2),   # Merit: Imposing
            ("Hatred", -3),                 # Flaw: Hates fire spirits
        ],
        "Whispers-to-Stars": [
            ("Spirit Mentor", 3),          # Merit: Helpful spirit
            ("Banned Transformation", -1), # Flaw: Cannot shift during eclipses
        ],
        "Breaks-the-Chain": [
            ("Double-Jointed", 1),         # Merit: Escape artist
            ("Strict Carnivore", -1),      # Flaw: Cannot eat plants
        ],
        "Storm-Singer": [
            ("Perfect Balance (Werewolf)", 1),  # Merit: Never falls
            ("Cursed", -2),                # Flaw: Bad luck in cities
        ],
        "Judges-the-Fallen": [
            ("Natural Channel", 3),        # Merit: Easy spirit contact
            ("Dark Secret", -1),           # Flaw: Hidden past
        ],

        # MAGE CHARACTERS
        "Victor Reyes": [
            ("Computer Aptitude", 1),      # Merit: Tech savvy
            ("Curiosity", -2),             # Flaw: Must investigate
        ],
        "Dr. Eleanor Vance": [
            ("Concentration", 1),          # Merit: Focus
            ("Nightmares", -1),            # Flaw: Haunted dreams
        ],
        "Samantha 'Sam' Torres": [
            ("Medium", 2),                 # Merit: Sees ghosts
            ("Phobia", -2),                # Flaw: Fear of heights
        ],
        "James 'Axiom' Wright": [
            ("Jack of All Trades", 3),     # Merit: Skilled
            ("Overconfident", -1),         # Flaw: Too sure
        ],
        "Sister Maria Vasquez": [
            ("True Faith", 7),             # Merit: Divine power
            ("Driving Goal", -3),          # Flaw: Must serve the divine
        ],

        # WRAITH CHARACTERS
        "Sarah Chen": [
            ("Eidetic Memory", 2),         # Merit: Perfect recall
            ("Curiosity", -2),             # Flaw: Cannot ignore mysteries
        ],
        "Marcus Webb": [
            ("Common Sense", 1),           # Merit: GM hints
            ("Dark Secret", -1),           # Flaw: Hidden shame
        ],
        "Elena Rodriguez": [
            ("Natural Leader", 1),         # Merit: Commands respect
            ("Hatred", -3),                # Flaw: Hates her killer
        ],
        "Thomas 'Tommy' Park": [
            ("Ambidextrous", 1),           # Merit: Both-handed
            ("Short Fuse", -2),            # Flaw: Quick temper
        ],
        "Dr. Rachel Stone": [
            ("Concentration", 1),          # Merit: Focus
            ("Compulsion", -1),            # Flaw: Must help spirits
        ],

        # CHANGELING CHARACTERS
        "Penny Brightwater": [
            ("Acute Senses", 1),           # Merit: Sharp senses
            ("Curiosity", -2),             # Flaw: Childlike wonder
        ],
        "Thornwood": [
            ("Daredevil", 3),              # Merit: Risk-taker
            ("Short Fuse", -2),            # Flaw: Quick to anger
        ],
        "Professor Edwin Merriweather": [
            ("Eidetic Memory", 2),         # Merit: Scholar's mind
            ("Absent-Minded", -3),         # Flaw: Lost in thoughts
        ],
        "Melody Songweaver": [
            ("Perfect Balance (Werewolf)", 1),  # Merit: Graceful
            ("Soft-Hearted", -1),          # Flaw: Cannot harm innocents
        ],
        "Lord Ashcroft": [
            ("Natural Leader", 1),         # Merit: Commands attention
            ("Intolerance", -1),           # Flaw: Dislikes mortals
        ],

        # DEMON CHARACTERS
        "Michael Garrett": [
            ("Common Sense", 1),           # Merit: Practical wisdom
            ("Nightmares", -1),            # Flaw: Memories of the Fall
        ],
        "Dr. Lilith Morgan": [
            ("Concentration", 1),          # Merit: Focus
            ("Curiosity", -2),             # Flaw: Scientific curiosity
        ],
        "Rev. Samuel Black": [
            ("Natural Leader", 1),         # Merit: Inspiring
            ("Dark Secret", -1),           # Flaw: Demonic nature hidden
        ],
        "Catherine 'Cat' Steel": [
            ("Ambidextrous", 1),           # Merit: Combat ready
            ("Short Fuse", -2),            # Flaw: Angelic wrath
        ],
        "Adrian Vex": [
            ("Eidetic Memory", 2),         # Merit: Perfect recall
            ("Compulsion", -1),            # Flaw: Must seek knowledge
        ],

        # HUNTER CHARACTERS
        "Marcus Stone": [
            ("Daredevil", 3),              # Merit: Fearless
            ("Driving Goal", -3),          # Flaw: Must destroy evil
        ],
        "Dr. Sarah Chen": [
            ("Concentration", 1),          # Merit: Focus
            ("Curiosity", -2),             # Flaw: Scientific mind
        ],
        "Father Thomas Rivera": [
            ("Natural Leader", 1),         # Merit: Inspiring faith
            ("Soft-Hearted", -1),          # Flaw: Cannot abandon innocents
        ],
        "Rachel Kim": [
            ("Acute Senses", 1),           # Merit: Heightened awareness
            ("Nightmares", -1),            # Flaw: Traumatic visions
        ],
        "Derek 'Ghost' Williams": [
            ("Ambidextrous", 1),           # Merit: Combat trained
            ("Dark Secret", -1),           # Flaw: Past sins
        ],

        # MUMMY CHARACTERS
        "Khafre": [
            ("Eidetic Memory", 2),         # Merit: Ancient memories
            ("Driving Goal", -3),          # Flaw: Ma'at must be served
        ],
        "Nefertari": [
            ("Natural Leader", 1),         # Merit: Royal bearing
            ("Intolerance", -1),           # Flaw: Dislikes chaos
        ],
        "Set-Nakht": [
            ("Concentration", 1),          # Merit: Scholarly focus
            ("Curiosity", -2),             # Flaw: Must know secrets
        ],
        "Merytre": [
            ("Common Sense", 1),           # Merit: Ancient wisdom
            ("Compulsion", -1),            # Flaw: Must heal the wounded
        ],
        "Senusret": [
            ("Daredevil", 3),              # Merit: Warrior spirit
            ("Hatred", -3),                # Flaw: Hates tomb robbers
        ],
    }

    characters_found = 0
    merits_assigned = 0
    flaws_assigned = 0
    skipped = 0

    for char_name, mf_list in assignments.items():
        try:
            char = CharacterModel.objects.get(name=char_name, chronicle=chronicle)
            characters_found += 1

            for mf_name, rating in mf_list:
                try:
                    mf = MeritFlaw.objects.get(name=mf_name)
                    # For flaws, we often store the absolute value
                    actual_rating = abs(rating)
                    success = char.add_mf(mf, actual_rating)
                    if success:
                        if rating > 0:
                            print(f"  {char_name}: Added merit '{mf_name}' ({rating})")
                            merits_assigned += 1
                        else:
                            print(f"  {char_name}: Added flaw '{mf_name}' ({rating})")
                            flaws_assigned += 1
                    else:
                        print(f"  Warning: Rating {actual_rating} not valid for '{mf_name}'")
                        skipped += 1
                except MeritFlaw.DoesNotExist:
                    print(f"  Warning: Merit/Flaw '{mf_name}' not found, skipping")
                    skipped += 1
        except CharacterModel.DoesNotExist:
            print(f"  Warning: Character '{char_name}' not found, skipping")

    print(f"\nSummary:")
    print(f"  Characters found: {characters_found}")
    print(f"  Merits assigned: {merits_assigned}")
    print(f"  Flaws assigned: {flaws_assigned}")
    print(f"  Skipped: {skipped}")


def populate_merits_flaws():
    """Main function to populate merits and flaws."""
    print("=" * 60)
    print("POPULATING MERITS AND FLAWS")
    print("=" * 60)

    assign_merits_and_flaws()

    print("\n" + "=" * 60)
    print("MERIT/FLAW POPULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_merits_flaws()

populate_merits_flaws()
