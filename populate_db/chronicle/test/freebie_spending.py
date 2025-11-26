"""
Seattle Test Chronicle - Freebie Spending Records

Creates FreebieSpendingRecord entries to track how characters spent
their freebie points during character creation.

Run with: python manage.py shell < populate_db/chronicle/test/freebie_spending.py

Prerequisites:
- Run character scripts first (creates characters)
"""

from characters.models.core.character import Character as CharacterModel
from game.models import Chronicle, FreebieSpendingRecord


def create_freebie_records():
    """Create freebie spending records for all PCs."""
    print("Creating Freebie Spending Records...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Freebie spending by character - based on typical 15 freebie points
    # Format: {character_name: [(trait_name, trait_type, value, cost), ...]}
    spending = {
        # === VAMPIRE CHARACTERS ===
        # Vampires get 15 freebies, Disciplines cost 7, Abilities 2, Backgrounds 1, Willpower 1
        "Marcus 'Shadow' Webb": [
            ("Obfuscate", "discipline", 2, 7),
            ("Computer", "ability", 3, 2),
            ("Investigation", "ability", 4, 2),
            ("Willpower", "willpower", 4, 4),
        ],
        "Isabella Santos": [
            ("Thaumaturgy", "discipline", 2, 7),
            ("Occult", "ability", 4, 2),
            ("Willpower", "willpower", 5, 4),
            ("Resources", "background", 2, 2),
        ],
        "Roland Cross": [
            ("Auspex", "discipline", 2, 7),
            ("Investigation", "ability", 4, 2),
            ("Awareness", "ability", 2, 2),
            ("Willpower", "willpower", 4, 4),
        ],
        "Zoe Kim": [
            ("Presence", "discipline", 2, 7),
            ("Expression", "ability", 4, 2),
            ("Fame", "background", 2, 2),
            ("Willpower", "willpower", 3, 4),
        ],
        "Viktor Krueger": [
            ("Potence", "discipline", 2, 7),
            ("Brawl", "ability", 3, 2),
            ("Intimidation", "ability", 3, 2),
            ("Willpower", "willpower", 4, 4),
        ],

        # === WEREWOLF CHARACTERS ===
        # Garou get 15 freebies, Gifts cost 7 (level 1), Abilities 2, Rage/Gnosis/Willpower 1
        "Runs-Through-Fire": [
            ("Strength", "attribute", 4, 5),
            ("Athletics", "ability", 3, 2),
            ("Rage", "rage", 5, 1),
            ("Willpower", "willpower", 4, 4),
            ("Kinfolk", "background", 2, 3),
        ],
        "Whispers-to-Stars": [
            ("Gnosis", "gnosis", 5, 2),
            ("Occult", "ability", 4, 2),
            ("Rituals", "ability", 3, 2),
            ("Ancestors", "background", 2, 2),
            ("Willpower", "willpower", 4, 4),
            ("Pure Breed", "background", 2, 3),
        ],
        "Breaks-the-Chain": [
            ("Stealth", "ability", 3, 2),
            ("Larceny", "ability", 2, 2),
            ("Gnosis", "gnosis", 3, 2),
            ("Willpower", "willpower", 4, 4),
            ("Contacts", "background", 2, 2),
            ("Streetwise", "ability", 2, 3),
        ],
        "Storm-Singer": [
            ("Expression", "ability", 3, 2),
            ("Performance", "ability", 3, 2),
            ("Gnosis", "gnosis", 4, 2),
            ("Ancestors", "background", 2, 2),
            ("Willpower", "willpower", 4, 4),
            ("Pure Breed", "background", 1, 3),
        ],
        "Judges-the-Fallen": [
            ("Investigation", "ability", 3, 2),
            ("Law", "ability", 2, 2),
            ("Gnosis", "gnosis", 3, 2),
            ("Willpower", "willpower", 5, 4),
            ("Contacts", "background", 2, 2),
            ("Resources", "background", 2, 3),
        ],

        # === MAGE CHARACTERS ===
        # Mages get 15 freebies, Arete costs 4, Spheres 7, Willpower 1
        "Victor Reyes": [
            ("Correspondence", "sphere", 3, 7),
            ("Computer", "ability", 4, 2),
            ("Willpower", "willpower", 5, 4),
            ("Resources", "background", 2, 2),
        ],
        "Dr. Eleanor Vance": [
            ("Entropy", "sphere", 4, 7),
            ("Medicine", "ability", 4, 2),
            ("Allies", "background", 2, 2),
            ("Willpower", "willpower", 6, 4),
        ],
        "Samantha 'Sam' Torres": [
            ("Spirit", "sphere", 3, 7),
            ("Awareness", "ability", 3, 2),
            ("Enigmas", "ability", 3, 2),
            ("Willpower", "willpower", 4, 4),
        ],
        "James 'Axiom' Wright": [
            ("Forces", "sphere", 3, 7),
            ("Science", "ability", 4, 2),
            ("Technology", "ability", 3, 2),
            ("Willpower", "willpower", 4, 4),
        ],
        "Sister Maria Vasquez": [
            ("Prime", "sphere", 3, 7),
            ("Expression", "ability", 3, 2),
            ("Willpower", "willpower", 6, 4),
            ("Mentor", "background", 2, 2),
        ],

        # === WRAITH CHARACTERS ===
        # Wraiths get 15 freebies, Arcanoi cost 5, Pathos 1, Willpower 2
        "Sarah Chen": [
            ("Argos", "arcanos", 2, 5),
            ("Investigation", "ability", 4, 2),
            ("Pathos", "pathos", 7, 2),
            ("Willpower", "willpower", 5, 4),
            ("Memoriam", "background", 2, 2),
        ],
        "Marcus Webb": [
            ("Inhabit", "arcanos", 2, 5),
            ("Streetwise", "ability", 3, 2),
            ("Pathos", "pathos", 6, 2),
            ("Willpower", "willpower", 4, 4),
            ("Contacts", "background", 2, 2),
        ],
        "Elena Rodriguez": [
            ("Outrage", "arcanos", 2, 5),
            ("Leadership", "ability", 3, 2),
            ("Intimidation", "ability", 2, 2),
            ("Willpower", "willpower", 5, 4),
            ("Status", "background", 2, 2),
        ],
        "Thomas 'Tommy' Park": [
            ("Moliate", "arcanos", 2, 5),
            ("Brawl", "ability", 3, 2),
            ("Athletics", "ability", 2, 2),
            ("Willpower", "willpower", 4, 4),
            ("Allies", "background", 2, 2),
        ],
        "Dr. Rachel Stone": [
            ("Castigate", "arcanos", 2, 5),
            ("Empathy", "ability", 3, 2),
            ("Medicine", "ability", 3, 2),
            ("Willpower", "willpower", 5, 4),
            ("Mentor", "background", 1, 1),
        ],

        # === CHANGELING CHARACTERS ===
        # Changelings get 15 freebies, Arts cost 5, Realms 3, Glamour 3
        "Penny Brightwater": [
            ("Chicanery", "art", 2, 5),
            ("Subterfuge", "ability", 3, 2),
            ("Actor", "realm", 2, 3),
            ("Glamour", "glamour", 5, 3),
            ("Willpower", "willpower", 3, 2),
        ],
        "Thornwood": [
            ("Primal", "art", 2, 5),
            ("Brawl", "ability", 3, 2),
            ("Nature", "realm", 2, 3),
            ("Glamour", "glamour", 5, 3),
            ("Willpower", "willpower", 4, 2),
        ],
        "Professor Edwin Merriweather": [
            ("Soothsay", "art", 3, 5),
            ("Academics", "ability", 4, 2),
            ("Prop", "realm", 2, 3),
            ("Glamour", "glamour", 4, 3),
            ("Willpower", "willpower", 4, 2),
        ],
        "Melody Songweaver": [
            ("Legerdemain", "art", 2, 5),
            ("Performance", "ability", 4, 2),
            ("Fae", "realm", 2, 3),
            ("Glamour", "glamour", 5, 3),
            ("Willpower", "willpower", 3, 2),
        ],
        "Lord Ashcroft": [
            ("Sovereign", "art", 2, 5),
            ("Leadership", "ability", 3, 2),
            ("Actor", "realm", 2, 3),
            ("Glamour", "glamour", 4, 3),
            ("Willpower", "willpower", 5, 2),
        ],

        # === DEMON CHARACTERS ===
        # Demons get 15 freebies, Lores cost 7, Faith 6
        "Michael Garrett": [
            ("Lore of Humanity", "lore", 2, 7),
            ("Empathy", "ability", 3, 2),
            ("Willpower", "willpower", 5, 4),
            ("Contacts", "background", 2, 2),
        ],
        "Dr. Lilith Morgan": [
            ("Lore of the Fundament", "lore", 3, 7),
            ("Science", "ability", 4, 2),
            ("Willpower", "willpower", 5, 4),
            ("Resources", "background", 2, 2),
        ],
        "Rev. Samuel Black": [
            ("Lore of the Celestials", "lore", 2, 7),
            ("Leadership", "ability", 3, 2),
            ("Willpower", "willpower", 6, 4),
            ("Followers", "background", 2, 2),
        ],
        "Catherine 'Cat' Steel": [
            ("Lore of Awakening", "lore", 2, 7),
            ("Melee", "ability", 3, 2),
            ("Brawl", "ability", 2, 2),
            ("Willpower", "willpower", 4, 4),
        ],
        "Adrian Vex": [
            ("Lore of Patterns", "lore", 2, 7),
            ("Occult", "ability", 4, 2),
            ("Investigation", "ability", 2, 2),
            ("Willpower", "willpower", 4, 4),
        ],

        # === HUNTER CHARACTERS ===
        # Hunters get 15 freebies, Edges are special
        "Marcus Stone": [
            ("Conviction", "virtue", 3, 6),
            ("Melee", "ability", 3, 2),
            ("Firearms", "ability", 3, 2),
            ("Willpower", "willpower", 5, 5),
        ],
        "Dr. Sarah Chen": [
            ("Vision", "virtue", 2, 4),
            ("Investigation", "ability", 3, 2),
            ("Science", "ability", 3, 2),
            ("Willpower", "willpower", 5, 5),
            ("Resources", "background", 2, 2),
        ],
        "Father Thomas Rivera": [
            ("Zeal", "virtue", 2, 4),
            ("Empathy", "ability", 3, 2),
            ("Academics", "ability", 3, 2),
            ("Willpower", "willpower", 6, 5),
            ("Contacts", "background", 2, 2),
        ],
        "Rachel Kim": [
            ("Vision", "virtue", 3, 6),
            ("Alertness", "ability", 3, 2),
            ("Investigation", "ability", 2, 2),
            ("Willpower", "willpower", 4, 5),
        ],
        "Derek 'Ghost' Williams": [
            ("Conviction", "virtue", 2, 4),
            ("Stealth", "ability", 3, 2),
            ("Firearms", "ability", 3, 2),
            ("Willpower", "willpower", 5, 5),
            ("Arsenal", "background", 2, 2),
        ],

        # === MUMMY CHARACTERS ===
        # Mummies get 15 freebies
        "Khafre": [
            ("Sekhem", "sekhem", 3, 7),
            ("Occult", "ability", 4, 2),
            ("Willpower", "willpower", 6, 4),
            ("Tomb", "background", 2, 2),
        ],
        "Nefertari": [
            ("Manipulation", "attribute", 4, 5),
            ("Leadership", "ability", 3, 2),
            ("Willpower", "willpower", 5, 4),
            ("Status", "background", 2, 2),
            ("Retainers", "background", 2, 2),
        ],
        "Set-Nakht": [
            ("Sekhem", "sekhem", 3, 7),
            ("Enigmas", "ability", 3, 2),
            ("Occult", "ability", 3, 2),
            ("Willpower", "willpower", 5, 4),
        ],
        "Merytre": [
            ("Life", "hekau", 3, 7),
            ("Medicine", "ability", 4, 2),
            ("Empathy", "ability", 2, 2),
            ("Willpower", "willpower", 5, 4),
        ],
        "Senusret": [
            ("Strength", "attribute", 4, 5),
            ("Melee", "ability", 4, 2),
            ("Athletics", "ability", 3, 2),
            ("Willpower", "willpower", 5, 4),
            ("Ka", "background", 2, 2),
        ],
    }

    created_count = 0
    skipped_count = 0

    for char_name, records in spending.items():
        try:
            char = CharacterModel.objects.get(name=char_name, chronicle=chronicle)

            for trait_name, trait_type, value, cost in records:
                # Check if record already exists
                existing = FreebieSpendingRecord.objects.filter(
                    character=char,
                    trait_name=trait_name,
                    trait_value=value
                ).exists()

                if existing:
                    skipped_count += 1
                    continue

                FreebieSpendingRecord.objects.create(
                    character=char,
                    trait_name=trait_name,
                    trait_type=trait_type,
                    trait_value=value,
                    cost=cost
                )
                created_count += 1

            print(f"  {char_name}: Created {len(records)} freebie records")

        except CharacterModel.DoesNotExist:
            print(f"  Warning: Character '{char_name}' not found")
            skipped_count += len(records)

    print(f"\nSummary - Created: {created_count}, Skipped: {skipped_count}")


def summarize_freebie_spending():
    """Summarize freebie spending by character type."""
    print("\nFreebie Spending Summary:")
    print("-" * 50)

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    chars_with_records = CharacterModel.objects.filter(
        chronicle=chronicle,
        freebie_spendings__isnull=False
    ).distinct()

    total_spent = 0
    for char in chars_with_records:
        spent = sum(r.cost for r in char.freebie_spendings.all())
        total_spent += spent
        print(f"  {char.name}: {spent} freebies spent across {char.freebie_spendings.count()} purchases")

    print(f"\nTotal freebies spent across all characters: {total_spent}")


def populate_freebie_spending():
    """Main function to populate freebie spending records."""
    print("=" * 60)
    print("POPULATING FREEBIE SPENDING RECORDS")
    print("=" * 60)

    create_freebie_records()
    summarize_freebie_spending()

    print("\n" + "=" * 60)
    print("FREEBIE SPENDING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_freebie_spending()

populate_freebie_spending()
