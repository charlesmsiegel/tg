"""Add the Garou deed-name column to legacy databases."""

from django.db import migrations

from characters.models.werewolf.garou import Werewolf

SHEET_FIELDS = ((Werewolf, ("deed_name",)),)


def add_sheet_cover_facts(apps, schema_editor):
    # ``characters`` has no migration state on legacy installations, so its
    # models are intentionally absent from this migration's historical app
    # registry. Use the live models solely to describe the columns being added.
    connection = schema_editor.connection
    for model, names in SHEET_FIELDS:
        with connection.cursor() as cursor:
            columns = {
                column.name
                for column in connection.introspection.get_table_description(
                    cursor, model._meta.db_table
                )
            }
        # Test syncdb already creates these columns from the current model.
        # Existing deployments need the DDL exactly once.
        for name in names:
            field = model._meta.get_field(name)
            if field.column not in columns:
                schema_editor.add_field(model, field)


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0005_story_chronicle")]
    operations = [migrations.RunPython(add_sheet_cover_facts, migrations.RunPython.noop)]
