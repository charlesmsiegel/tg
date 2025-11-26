"""
XP and Weeks Script

Creates Week records for XP tracking and simulates the XP system.
"""

from datetime import date, timedelta

from characters.models.core import CharacterModel
from game.models import Chronicle, Scene, Week


def populate_xp_weeks():
    """Create Week records and set up XP tracking."""
    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    print("Setting up XP tracking system...")

    # =========================================================================
    # CREATE WEEK RECORDS
    # =========================================================================
    # Create weeks for 2022 (when our scenes take place)
    create_weeks_for_year(2022)

    # =========================================================================
    # MARK SCENES AS FINISHED WITH XP GIVEN
    # =========================================================================
    mark_scenes_finished()

    # =========================================================================
    # AWARD XP TO CHARACTERS
    # =========================================================================
    award_character_xp()

    print("XP tracking setup complete!")


def create_weeks_for_year(year):
    """Create Week records for a given year."""
    print(f"  Creating Week records for {year}...")

    # Start from first Sunday of the year
    jan_1 = date(year, 1, 1)
    days_until_sunday = (6 - jan_1.weekday()) % 7
    if days_until_sunday == 0:
        first_sunday = jan_1
    else:
        first_sunday = jan_1 + timedelta(days=days_until_sunday)

    # Create 52 weeks
    weeks_created = 0
    current_sunday = first_sunday
    while current_sunday.year == year:
        week, created = Week.objects.get_or_create(end_date=current_sunday)
        if created:
            weeks_created += 1
        current_sunday += timedelta(days=7)

    print(f"    Created {weeks_created} new Week records")


def mark_scenes_finished():
    """Mark all test chronicle scenes as finished."""
    print("  Marking scenes as finished...")

    scenes = Scene.objects.filter(chronicle__name="Seattle Test Chronicle")
    updated = scenes.update(finished=True, xp_given=True)
    print(f"    Marked {updated} scenes as finished with XP given")


def award_character_xp():
    """Award XP to characters based on scene participation."""
    print("  Awarding XP to characters...")

    # Get all PC characters in the chronicle
    characters = CharacterModel.objects.filter(
        chronicle__name="Seattle Test Chronicle",
        npc=False,
    )

    for char in characters:
        # Count scenes the character participated in
        scene_count = char.scenes.count()

        # Award 1 XP per scene plus a base amount
        base_xp = 10  # Starting XP
        scene_xp = scene_count * 2  # 2 XP per scene

        # Set character XP
        char.xp = base_xp + scene_xp
        char.save()

        if scene_count > 0:
            print(f"    {char.name}: {char.xp} XP ({scene_count} scenes)")


if __name__ == "__main__":
    populate_xp_weeks()
