#!/usr/bin/env python
"""
Master Runner Script for Seattle Test Chronicle

Executes all population scripts in the correct order to create a fully
fleshed out test chronicle with characters, locations, items, stories,
scenes, and all supporting data.

Usage:
    python manage.py shell < populate_db/chronicle/test/run_all.py

Or run directly from Django shell:
    exec(open('populate_db/chronicle/test/run_all.py').read())
"""

import os
import sys
import importlib.util
from pathlib import Path


def run_script(script_path, description):
    """Run a population script and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_path}")
    print('='*60)

    try:
        spec = importlib.util.spec_from_file_location("module", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Try to find and run the main populate function
        for func_name in ['populate', 'populate_db', 'main', 'run']:
            if hasattr(module, func_name):
                getattr(module, func_name)()
                print(f"✓ {description} complete")
                return True

        # If no standard function, look for populate_* functions
        for name in dir(module):
            if name.startswith('populate_'):
                getattr(module, name)()
                print(f"✓ {description} complete")
                return True

        print(f"⚠ No populate function found in {script_path}")
        return False

    except Exception as e:
        print(f"✗ Error in {description}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all population scripts in order."""
    base_dir = Path(__file__).parent

    print("\n" + "="*60)
    print("SEATTLE TEST CHRONICLE - FULL POPULATION")
    print("="*60)

    # Define execution order
    scripts = [
        # Phase 1: Foundation
        ("base.py", "Chronicle foundation (users, ST relationships)"),
        ("groups.py", "Character groups (coteries, packs, cabals, etc.)"),

        # Phase 2: Core Content - Characters
        ("vampire_characters.py", "Vampire characters"),
        ("vampire_npc.py", "Vampire NPCs"),
        ("vampire_pc_aux.py", "Vampire auxiliary PCs"),
        ("werewolf_characters.py", "Werewolf characters"),
        ("werewolf_npc.py", "Werewolf NPCs"),
        ("werewolf_pc_aux.py", "Werewolf auxiliary PCs"),
        ("mage_characters.py", "Mage characters"),
        ("mage_npc.py", "Mage NPCs"),
        ("mage_pc_aux.py", "Mage auxiliary PCs"),
        ("wraith_characters.py", "Wraith characters"),
        ("wraith_npc.py", "Wraith NPCs"),
        ("wraith_pc_aux.py", "Wraith auxiliary PCs"),
        ("changeling_characters.py", "Changeling characters"),
        ("changeling_npc.py", "Changeling NPCs"),
        ("changeling_pc_aux.py", "Changeling auxiliary PCs"),
        ("demon_characters.py", "Demon characters"),
        ("demon_npc.py", "Demon NPCs"),
        ("demon_pc_aux.py", "Demon auxiliary PCs"),
        ("hunter_characters.py", "Hunter characters"),
        ("hunter_npc.py", "Hunter NPCs"),
        ("hunter_pc_aux.py", "Hunter auxiliary PCs"),
        ("mummy_characters.py", "Mummy characters"),
        ("mummy_npc.py", "Mummy NPCs"),
        ("mummy_pc_aux.py", "Mummy auxiliary PCs"),

        # Phase 3: Core Content - Locations
        ("vampire_location.py", "Vampire locations"),
        ("werewolf_location.py", "Werewolf locations"),
        ("mage_location.py", "Mage locations"),
        ("wraith_location.py", "Wraith locations"),
        ("changeling_location.py", "Changeling locations"),
        ("demon_location.py", "Demon locations"),
        ("hunter_location.py", "Hunter locations"),
        ("mummy_location.py", "Mummy locations"),

        # Phase 4: Core Content - Items
        ("vampire_items.py", "Vampire items"),
        ("werewolf_items.py", "Werewolf items"),
        ("mage_items.py", "Mage items"),
        ("wraith_items.py", "Wraith items"),
        ("changeling_items.py", "Changeling items"),
        ("demon_items.py", "Demon items"),
        ("hunter_items.py", "Hunter items"),
        ("mummy_items.py", "Mummy items"),

        # Phase 5: Stories and Scenes
        ("stories.py", "Story arcs"),
    ]

    # Scene scripts (in scenes/ subdirectory)
    scene_scripts = [
        # Vampire scenes
        ("scenes/vtm_blood_trade_s1.py", "VtM Blood Trade Scene 1"),
        ("scenes/vtm_blood_trade_s2.py", "VtM Blood Trade Scene 2"),
        ("scenes/vtm_blood_trade_s3.py", "VtM Blood Trade Scene 3"),
        ("scenes/vtm_masquerade_s1.py", "VtM Masquerade Scene 1"),
        ("scenes/vtm_masquerade_s2.py", "VtM Masquerade Scene 2"),
        ("scenes/vtm_masquerade_s3.py", "VtM Masquerade Scene 3"),
        # Werewolf scenes
        ("scenes/wta_corruption_s1.py", "WtA Corruption Scene 1"),
        ("scenes/wta_corruption_s2.py", "WtA Corruption Scene 2"),
        ("scenes/wta_corruption_s3.py", "WtA Corruption Scene 3"),
        ("scenes/wta_blood_calls_s1.py", "WtA Blood Calls Scene 1"),
        ("scenes/wta_blood_calls_s2.py", "WtA Blood Calls Scene 2"),
        ("scenes/wta_blood_calls_s3.py", "WtA Blood Calls Scene 3"),
        # Mage scenes
        ("scenes/mta_node_s1.py", "MtA Node Scene 1"),
        ("scenes/mta_node_s2.py", "MtA Node Scene 2"),
        ("scenes/mta_node_s3.py", "MtA Node Scene 3"),
        ("scenes/mta_paradox_s1.py", "MtA Paradox Scene 1"),
        ("scenes/mta_paradox_s2.py", "MtA Paradox Scene 2"),
        ("scenes/mta_paradox_s3.py", "MtA Paradox Scene 3"),
        # Wraith scenes
        ("scenes/wto_whispers_s1.py", "WtO Whispers Scene 1"),
        ("scenes/wto_whispers_s2.py", "WtO Whispers Scene 2"),
        ("scenes/wto_whispers_s3.py", "WtO Whispers Scene 3"),
        ("scenes/wto_chains_s1.py", "WtO Chains Scene 1"),
        ("scenes/wto_chains_s2.py", "WtO Chains Scene 2"),
        ("scenes/wto_chains_s3.py", "WtO Chains Scene 3"),
        # Changeling scenes
        ("scenes/ctd_gray_tide_s1.py", "CtD Gray Tide Scene 1"),
        ("scenes/ctd_gray_tide_s2.py", "CtD Gray Tide Scene 2"),
        ("scenes/ctd_gray_tide_s3.py", "CtD Gray Tide Scene 3"),
        ("scenes/ctd_dreams_s1.py", "CtD Dreams Scene 1"),
        ("scenes/ctd_dreams_s2.py", "CtD Dreams Scene 2"),
        ("scenes/ctd_dreams_s3.py", "CtD Dreams Scene 3"),
        # Demon scenes
        ("scenes/dtf_foundation_s1.py", "DtF Foundation Scene 1"),
        ("scenes/dtf_foundation_s2.py", "DtF Foundation Scene 2"),
        ("scenes/dtf_foundation_s3.py", "DtF Foundation Scene 3"),
        ("scenes/dtf_seeds_s1.py", "DtF Seeds Scene 1"),
        ("scenes/dtf_seeds_s2.py", "DtF Seeds Scene 2"),
        ("scenes/dtf_seeds_s3.py", "DtF Seeds Scene 3"),
        # Hunter scenes
        ("scenes/htr_nest_s1.py", "HtR Nest Scene 1"),
        ("scenes/htr_nest_s2.py", "HtR Nest Scene 2"),
        ("scenes/htr_nest_s3.py", "HtR Nest Scene 3"),
        ("scenes/htr_silent_s1.py", "HtR Silent Scene 1"),
        ("scenes/htr_silent_s2.py", "HtR Silent Scene 2"),
        ("scenes/htr_silent_s3.py", "HtR Silent Scene 3"),
        # Mummy scenes
        ("scenes/mum_serpents_s1.py", "Mummy Serpents Scene 1"),
        ("scenes/mum_serpents_s2.py", "Mummy Serpents Scene 2"),
        ("scenes/mum_serpents_s3.py", "Mummy Serpents Scene 3"),
        ("scenes/mum_scarab_s1.py", "Mummy Scarab Scene 1"),
        ("scenes/mum_scarab_s2.py", "Mummy Scarab Scene 2"),
        ("scenes/mum_scarab_s3.py", "Mummy Scarab Scene 3"),
        # Social scenes
        ("scenes/social_elysium.py", "Social: Elysium"),
        ("scenes/social_coffee.py", "Social: Hunter Coffee"),
        ("scenes/social_freehold.py", "Social: Freehold Gathering"),
        ("scenes/social_crossover.py", "Social: Crossover Meeting"),
    ]

    # Phase 6: Relationships and Systems
    post_scripts = [
        ("group_membership.py", "Group membership assignments"),
        ("character_status.py", "Character approval status"),
        ("background_links.py", "Background links to NPCs/items/locations"),
        ("xp_weeks.py", "XP and Week tracking"),
        ("journal_entries.py", "Character journal entries"),
        ("leadership.py", "Political hierarchy and leadership"),

        # Phase 7: Advanced Features
        ("traits.py", "Gameline-specific traits (gifts, etc.)"),
        ("merits_flaws.py", "Merit and flaw assignments"),
        ("derangements.py", "Derangement assignments"),
        ("rotes.py", "Mage rote assignments"),
        ("spirits.py", "Spirit character NPCs"),
        ("city.py", "City of Seattle"),
        ("location_nesting.py", "Location hierarchy"),
        ("item_ownership.py", "Item ownership and locations"),
        ("observers.py", "Observer access permissions"),
        ("xp_requests.py", "XP spending requests"),
        ("freebie_spending.py", "Character freebie spending records"),
        ("pack_totems.py", "Pack totem bindings"),
    ]

    # Run all scripts
    success_count = 0
    fail_count = 0
    skip_count = 0

    all_scripts = scripts + scene_scripts + post_scripts

    for script_name, description in all_scripts:
        script_path = base_dir / script_name
        if script_path.exists():
            if run_script(str(script_path), description):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f"⚠ Skipping {script_name} (file not found)")
            skip_count += 1

    # Summary
    print("\n" + "="*60)
    print("POPULATION COMPLETE")
    print("="*60)
    print(f"✓ Successful: {success_count}")
    print(f"✗ Failed: {fail_count}")
    print(f"⚠ Skipped: {skip_count}")
    print("="*60)


if __name__ == "__main__":
    main()
