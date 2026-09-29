"""Add Story's chronicle column to legacy databases."""

from django.db import migrations

from tg_schema.schema import add_missing_columns


def add_story_chronicle(apps, schema_editor):
    # ``game`` has no migration state on legacy installations: the live model
    # describes the column (see tg_schema.schema). 0007 assigns existing stories.
    add_missing_columns(schema_editor, "game.Story", ("chronicle",))


# Reversing this migration leaves the column in place (RunPython.noop).


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0004_scene_rolls_and_read_marker")]
    operations = [migrations.RunPython(add_story_chronicle, migrations.RunPython.noop)]
