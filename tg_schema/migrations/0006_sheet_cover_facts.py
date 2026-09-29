"""Add the Garou deed-name column to legacy databases."""

from django.db import migrations

from tg_schema.schema import add_missing_columns

SHEET_FIELDS = (("characters.Werewolf", ("deed_name",)),)


def add_sheet_cover_facts(apps, schema_editor):
    # ``characters`` has no migration state on legacy installations: the live
    # models describe the columns (see tg_schema.schema).
    for label, names in SHEET_FIELDS:
        add_missing_columns(schema_editor, label, names)


# Reversing this migration leaves the columns in place (RunPython.noop).


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0005_story_chronicle")]
    operations = [migrations.RunPython(add_sheet_cover_facts, migrations.RunPython.noop)]
