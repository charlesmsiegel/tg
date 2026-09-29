"""Add scene visibility to legacy databases without a game migration baseline."""

from django.db import migrations

from tg_schema.schema import add_missing_columns


def add_scene_visibility(apps, schema_editor):
    # ``game`` has no migration state on legacy installations, so its models are
    # absent from this migration's historical registry: the live model describes
    # the column (see tg_schema.schema).
    add_missing_columns(schema_editor, "game.Scene", ("visibility",))


class Migration(migrations.Migration):
    initial = True
    operations = [migrations.RunPython(add_scene_visibility, migrations.RunPython.noop)]
