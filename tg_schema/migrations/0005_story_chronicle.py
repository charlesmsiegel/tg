"""Add Story's chronicle column to legacy databases."""

from django.db import migrations

from game.models import Story


def add_story_chronicle(apps, schema_editor):
    # ``game`` has no migration state on legacy installations, so its models
    # are intentionally absent from this migration's historical app registry.
    # Use the live model solely to describe the column being added.
    story = Story
    field = story._meta.get_field("chronicle")
    with schema_editor.connection.cursor() as cursor:
        columns = {
            column.name
            for column in schema_editor.connection.introspection.get_table_description(
                cursor, story._meta.db_table
            )
        }
    # Test syncdb already creates this column from the current model. Existing
    # deployments need the DDL exactly once; their stories keep no chronicle.
    if field.column not in columns:
        schema_editor.add_field(story, field)


# The live model describes each column (legacy databases have no migration state for
# its app), so these fields must keep the definition they shipped with: a later
# change to one of them needs its own migration here, not an edit to this one.
# Reversing this migration leaves the columns in place (RunPython.noop).


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0004_scene_rolls_and_read_marker")]
    operations = [migrations.RunPython(add_story_chronicle, migrations.RunPython.noop)]
