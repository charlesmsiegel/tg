"""
Seattle Test Chronicle - Pack Totem Bindings

Binds werewolf packs to their patron totems using the Pack.totem ForeignKey.

Run with: python manage.py shell < populate_db/chronicle/test/pack_totems.py

Prerequisites:
- Run groups.py first (creates packs)
- Run populate_db/werewolf/totems.py (creates totems)
"""

from characters.models.werewolf.pack import Pack
from characters.models.werewolf.totem import Totem
from game.models import Chronicle


def bind_pack_totems():
    """Bind each pack to their patron totem."""
    print("Binding Packs to Totems...")

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")

    # Pack-Totem bindings
    # Format: {pack_name: totem_name}
    bindings = {
        # Silicon Fangs - Tech-savvy urban Garou
        # Cockroach is perfect: Wisdom totem, tech bonuses, Glass Walker friendly
        "Silicon Fangs": "Cockroach",

        # The Wardens - Traditional warriors protecting sacred places
        # Fenris: War totem, Glory renown, never pass up a worthy fight
        "The Wardens": "Fenris",

        # The Forgotten - Outcasts and misfits (Bone Gnawers, Metis)
        # Rat: War totem, stealth bonuses, friendship of Bone Gnawers
        "The Forgotten": "Rat",
    }

    bound_count = 0
    skipped_count = 0

    for pack_name, totem_name in bindings.items():
        try:
            pack = Pack.objects.get(name=pack_name, chronicle=chronicle)

            # Check if already bound
            if pack.totem is not None:
                print(f"  Skipping: {pack_name} already has totem {pack.totem.name}")
                skipped_count += 1
                continue

            try:
                totem = Totem.objects.get(name=totem_name)
                pack.set_totem(totem)
                print(f"  Bound: {pack_name} -> {totem_name} ({totem.totem_type} totem)")
                bound_count += 1

            except Totem.DoesNotExist:
                print(f"  Warning: Totem '{totem_name}' not found")
                skipped_count += 1

        except Pack.DoesNotExist:
            print(f"  Warning: Pack '{pack_name}' not found")
            skipped_count += 1

    print(f"\nSummary - Bound: {bound_count}, Skipped: {skipped_count}")


def list_pack_totems():
    """List all packs with their totems for verification."""
    print("\nPacks and Their Totems:")
    print("-" * 60)

    chronicle = Chronicle.objects.get(name="Seattle Test Chronicle")
    packs = Pack.objects.filter(chronicle=chronicle)

    for pack in packs:
        if pack.totem:
            print(f"  {pack.name}")
            print(f"    Totem: {pack.totem.name} ({pack.totem.totem_type})")
            print(f"    Cost: {pack.totem.cost} background points")
            if pack.totem.pack_traits:
                print(f"    Pack Traits: {pack.totem.pack_traits[:60]}...")
            if pack.totem.ban:
                print(f"    Ban: {pack.totem.ban}")
        else:
            print(f"  {pack.name}: No totem assigned")
        print()


def populate_pack_totems():
    """Main function to populate pack totem bindings."""
    print("=" * 60)
    print("BINDING PACKS TO TOTEMS")
    print("=" * 60)

    bind_pack_totems()
    list_pack_totems()

    print("=" * 60)
    print("PACK TOTEM BINDING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    populate_pack_totems()

populate_pack_totems()
