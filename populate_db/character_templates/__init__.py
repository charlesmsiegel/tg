"""
Character Template Population Scripts

Run this to populate all character templates from World of Darkness sourcebooks.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")
django.setup()

from .mage_templates import populate_mage_templates


def populate_all_templates():
    """Populate all character templates for all gamelines"""
    print("=" * 60)
    print("POPULATING CHARACTER TEMPLATES")
    print("=" * 60)

    # Mage templates
    print("\n[Mage: The Ascension]")
    populate_mage_templates()

    # TODO: Add other gamelines as templates are created
    # populate_vampire_templates()
    # populate_werewolf_templates()
    # populate_demon_templates()
    # populate_changeling_templates()
    # populate_wraith_templates()

    print("\n" + "=" * 60)
    print("ALL CHARACTER TEMPLATES POPULATED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    populate_all_templates()
