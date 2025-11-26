"""
Seattle Test Chronicle - Mage Rote Assignments

Assigns rotes to Mage characters based on their Tradition/Faction.
Uses the rotes M2M field on Mage model.

Run with: python manage.py shell < populate_db/chronicle/test/rotes.py

Prerequisites:
- Run character scripts first (creates mages)
- Run populate_db/mage/mage_example_rotes.py (creates rotes)
"""

from characters.models.mage.mage import Mage
from characters.models.mage.rote import Rote
from game.models import Chronicle


def assign_rotes():
    """Assign rotes to mages based on their faction/tradition."""
    print("Assigning Mage Rotes...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Rote assignments by character name
    # Format: {character_name: [list of rote names]}
    assignments = {
        # Victor Reyes - Virtual Adept (Correspondence, Forces, Mind)
        "Victor Reyes": [
            "Digital Web Journey",        # Correspondence - travel through Digital Web
            "Information Overload",       # Mind - overwhelm with data
            "System Crash",               # Forces/Correspondence - disrupt tech
        ],

        # Dr. Eleanor Vance - Euthanatos (Entropy, Life, Spirit)
        "Dr. Eleanor Vance": [
            "Kiss of Gentle Death",       # Life/Entropy - painless death
            "Wheel of Fortune",           # Entropy - probability manipulation
            "Speak with the Dead",        # Spirit - commune with ghosts
        ],

        # Samantha 'Sam' Torres - Dreamspeaker (Spirit, Mind, Prime)
        "Samantha 'Sam' Torres": [
            "Spirit Journey",             # Spirit - umbral travel
            "Dream Prophecy",             # Mind - prophetic dreams
            "Channel Quintessence",       # Prime - gather energy
        ],

        # James 'Axiom' Wright - Sons of Ether (Matter, Forces, Time)
        "James 'Axiom' Wright": [
            "Ether Ray",                  # Forces - energy weapon
            "Dimensional Portal Device",  # Time/Correspondence - create portal
            "Alchemical Transmutation",   # Matter - transform substances
        ],

        # Sister Maria Vasquez - Celestial Chorus (Prime, Spirit, Life)
        "Sister Maria Vasquez": [
            "Pillar of Divine Flame",     # Prime/Forces - holy fire
            "Grace of the Divine",        # Life - blessing/healing
            "Laying On of Hands",         # Life - healing touch
        ],
    }

    assigned_count = 0
    skipped_count = 0

    for mage_name, rote_names in assignments.items():
        try:
            mage = Mage.objects.get(name=mage_name, chronicle=chronicle)

            for rote_name in rote_names:
                try:
                    rote = Rote.objects.get(name=rote_name)

                    # Check if already has rote
                    if mage.rotes.filter(pk=rote.pk).exists():
                        print(f"  Skipping existing: {mage_name} knows {rote_name}")
                        skipped_count += 1
                        continue

                    mage.rotes.add(rote)
                    print(f"  Assigned: {mage_name} learned {rote_name}")
                    assigned_count += 1

                except Rote.DoesNotExist:
                    # Try partial match
                    rotes = Rote.objects.filter(name__icontains=rote_name.split()[0])
                    if rotes.exists():
                        rote = rotes.first()
                        if not mage.rotes.filter(pk=rote.pk).exists():
                            mage.rotes.add(rote)
                            print(f"  Assigned (partial match): {mage_name} learned {rote.name}")
                            assigned_count += 1
                        else:
                            skipped_count += 1
                    else:
                        print(f"  Warning: Rote '{rote_name}' not found")
                        skipped_count += 1

        except Mage.DoesNotExist:
            print(f"  Warning: Mage '{mage_name}' not found")
            skipped_count += 1

    print(f"\nSummary - Assigned: {assigned_count}, Skipped: {skipped_count}")


def assign_random_rotes():
    """Assign random appropriate rotes to mages without enough rotes."""
    print("\nAssigning Additional Random Rotes...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    mages = Mage.objects.filter(chronicle=chronicle, npc=False)

    for mage in mages:
        current_rotes = mage.rotes.count()
        if current_rotes < 2:
            # Find rotes that match the mage's spheres
            max_sphere = max(
                mage.correspondence, mage.entropy, mage.forces,
                mage.life, mage.matter, mage.mind,
                mage.prime, mage.spirit, mage.time
            )
            if max_sphere > 0:
                # Get random rotes the mage doesn't already have
                available_rotes = Rote.objects.exclude(
                    pk__in=mage.rotes.values_list('pk', flat=True)
                ).order_by('?')[:3 - current_rotes]

                for rote in available_rotes:
                    mage.rotes.add(rote)
                    print(f"  {mage.name}: Added random rote '{rote.name}'")


def list_mages_with_rotes():
    """List all mages with their rotes for verification."""
    print("\nMages with Rotes:")
    print("-" * 50)

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    mages = Mage.objects.filter(chronicle=chronicle)

    for mage in mages:
        rotes = mage.rotes.all()
        if rotes.exists():
            rote_names = ", ".join([r.name for r in rotes])
            print(f"  {mage.name}: {rote_names}")
        else:
            print(f"  {mage.name}: No rotes")


def populate_rotes():
    """Main function to populate rote assignments."""
    print("=" * 60)
    print("POPULATING MAGE ROTES")
    print("=" * 60)

    assign_rotes()
    assign_random_rotes()
    list_mages_with_rotes()

    print("\n" + "=" * 60)
    print("ROTE POPULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_rotes()

populate_rotes()
