"""Add ChantryBackgroundRating's linked-object columns to legacy databases."""

from django.db import migrations

from locations.models.mage.chantry import ChantryBackgroundRating

LINKED_FIELDS = ("linked_location", "linked_character")


def add_chantry_rating_linked_object(apps, schema_editor):
    # ``locations`` has no migration state on legacy installations, so its
    # models are intentionally absent from this migration's historical app
    # registry. Use the live model solely to describe the columns being added.
    rating = ChantryBackgroundRating
    table = rating._meta.db_table
    with schema_editor.connection.cursor() as cursor:
        columns = {
            column.name
            for column in schema_editor.connection.introspection.get_table_description(
                cursor, table
            )
        }
    # Test syncdb already creates these columns from the current model. Existing
    # deployments need the DDL exactly once.
    for name in LINKED_FIELDS:
        field = rating._meta.get_field(name)
        if field.column not in columns:
            schema_editor.add_field(rating, field)


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0001_scene_visibility")]
    operations = [migrations.RunPython(add_chantry_rating_linked_object, migrations.RunPython.noop)]
