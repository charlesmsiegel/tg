"""
Seattle Test Chronicle - Story Definitions

Creates all Story objects for the test chronicle. Each gameline has two stories.
Scene files are separate and reference these stories.

Run with: python manage.py shell < populate_db/chronicle/test/stories.py
"""

from game.models import Story


def populate_stories():
    """Create all Story objects for the Seattle Test Chronicle."""
    stories = {}

    # =========================================================================
    # VAMPIRE STORIES
    # =========================================================================

    stories["vtm_blood_trade"], created = Story.objects.get_or_create(
        name="Blood in the Water",
    )
    if created:
        print("  Created Story: Blood in the Water (Vampire)")

    stories["vtm_masquerade_breach"], created = Story.objects.get_or_create(
        name="The Masquerade Frays",
    )
    if created:
        print("  Created Story: The Masquerade Frays (Vampire)")

    # =========================================================================
    # WEREWOLF STORIES
    # =========================================================================

    stories["wta_bane_incursion"], created = Story.objects.get_or_create(
        name="Corruption Beneath",
    )
    if created:
        print("  Created Story: Corruption Beneath (Werewolf)")

    stories["wta_lost_kinfolk"], created = Story.objects.get_or_create(
        name="Blood Calls to Blood",
    )
    if created:
        print("  Created Story: Blood Calls to Blood (Werewolf)")

    # =========================================================================
    # MAGE STORIES
    # =========================================================================

    stories["mta_node_conflict"], created = Story.objects.get_or_create(
        name="The Contested Node",
    )
    if created:
        print("  Created Story: The Contested Node (Mage)")

    stories["mta_paradox_storm"], created = Story.objects.get_or_create(
        name="When Reality Rebels",
    )
    if created:
        print("  Created Story: When Reality Rebels (Mage)")

    # =========================================================================
    # WRAITH STORIES
    # =========================================================================

    stories["wto_spectral_threat"], created = Story.objects.get_or_create(
        name="Whispers from the Void",
    )
    if created:
        print("  Created Story: Whispers from the Void (Wraith)")

    stories["wto_fetters_fade"], created = Story.objects.get_or_create(
        name="Chains of the Living",
    )
    if created:
        print("  Created Story: Chains of the Living (Wraith)")

    # =========================================================================
    # CHANGELING STORIES
    # =========================================================================

    stories["ctd_banality_wave"], created = Story.objects.get_or_create(
        name="The Gray Tide",
    )
    if created:
        print("  Created Story: The Gray Tide (Changeling)")

    stories["ctd_chimera_hunt"], created = Story.objects.get_or_create(
        name="Dreams Made Flesh",
    )
    if created:
        print("  Created Story: Dreams Made Flesh (Changeling)")

    # =========================================================================
    # DEMON STORIES
    # =========================================================================

    stories["dtf_earthbound_stirs"], created = Story.objects.get_or_create(
        name="The Foundation Cracks",
    )
    if created:
        print("  Created Story: The Foundation Cracks (Demon)")

    stories["dtf_faith_harvest"], created = Story.objects.get_or_create(
        name="Seeds of Belief",
    )
    if created:
        print("  Created Story: Seeds of Belief (Demon)")

    # =========================================================================
    # HUNTER STORIES
    # =========================================================================

    stories["htr_vampire_nest"], created = Story.objects.get_or_create(
        name="Into the Nest",
    )
    if created:
        print("  Created Story: Into the Nest (Hunter)")

    stories["htr_missing_hunters"], created = Story.objects.get_or_create(
        name="The Silent Cell",
    )
    if created:
        print("  Created Story: The Silent Cell (Hunter)")

    # =========================================================================
    # MUMMY STORIES
    # =========================================================================

    stories["mum_apophis_cult"], created = Story.objects.get_or_create(
        name="Serpents in the City",
    )
    if created:
        print("  Created Story: Serpents in the City (Mummy)")

    stories["mum_relic_theft"], created = Story.objects.get_or_create(
        name="The Stolen Scarab",
    )
    if created:
        print("  Created Story: The Stolen Scarab (Mummy)")

    print(f"Stories populated: {len(stories)} stories created/retrieved.")
    return stories


if __name__ == "__main__":
    populate_stories()
