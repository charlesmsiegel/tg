"""Add scene visibility to legacy databases without a game migration baseline."""

from django.db import migrations

from game.models import Scene


def add_scene_visibility(apps, schema_editor):
    # ``game`` has no migration state on legacy installations, so its models
    # are intentionally absent from this migration's historical app registry.
    # Use the live model solely to describe the column being added.
    scene = Scene
    table = scene._meta.db_table
    with schema_editor.connection.cursor() as cursor:
        columns = {
            column.name
            for column in schema_editor.connection.introspection.get_table_description(
                cursor, table
            )
        }
    # Test syncdb already creates this column from the current model. Existing
    # deployments need the DDL exactly once.
    if "visibility" not in columns:
        schema_editor.add_field(scene, scene._meta.get_field("visibility"))


class Migration(migrations.Migration):
    initial = True
    operations = [migrations.RunPython(add_scene_visibility, migrations.RunPython.noop)]
