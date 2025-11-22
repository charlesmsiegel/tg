"""
Character Template Population Scripts

Run this to populate all character templates from World of Darkness sourcebooks.
"""

import os
import sys

import django

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")
django.setup()

# Import functions directly when run as module
if __name__ == "__main__":
    from changeling_templates import populate_changeling_templates
    from demon_templates import populate_demon_templates
    from mage_templates import populate_mage_templates
    from vampire_templates import populate_vampire_templates
    from werewolf_templates import populate_werewolf_templates
    from wraith_templates import populate_wraith_templates
else:
    from .changeling_templates import populate_changeling_templates
    from .demon_templates import populate_demon_templates
    from .mage_templates import populate_mage_templates
    from .vampire_templates import populate_vampire_templates
    from .werewolf_templates import populate_werewolf_templates
    from .wraith_templates import populate_wraith_templates


def populate_all_templates():
    """Populate all character templates for all gamelines"""
    print("=" * 60)
    print("POPULATING CHARACTER TEMPLATES")
    print("=" * 60)

    # Mage templates
    print("\n[Mage: The Ascension]")
    populate_mage_templates()

    # Vampire templates
    print("\n[Vampire: The Masquerade]")
    populate_vampire_templates()

    # Werewolf templates
    print("\n[Werewolf: The Apocalypse]")
    populate_werewolf_templates()

    # Changeling templates
    print("\n[Changeling: The Dreaming]")
    populate_changeling_templates()

    # Wraith templates
    print("\n[Wraith: The Oblivion]")
    populate_wraith_templates()

    # Demon templates
    print("\n[Demon: The Fallen]")
    populate_demon_templates()

    print("\n" + "=" * 60)
    print("ALL CHARACTER TEMPLATES POPULATED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    populate_all_templates()
