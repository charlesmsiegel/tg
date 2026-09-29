"""Add ChantryBackgroundRating's linked-object columns to legacy databases."""

from django.db import migrations

from tg_schema.schema import add_missing_columns

LINKED_FIELDS = ("linked_location", "linked_character")


def add_chantry_rating_linked_object(apps, schema_editor):
    # ``locations`` has no migration state on legacy installations: the live model
    # describes the columns (see tg_schema.schema).
    add_missing_columns(schema_editor, "locations.ChantryBackgroundRating", LINKED_FIELDS)


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0001_scene_visibility")]
    operations = [migrations.RunPython(add_chantry_rating_linked_object, migrations.RunPython.noop)]
