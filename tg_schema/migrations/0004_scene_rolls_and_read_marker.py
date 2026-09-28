"""Add Post.roll and UserSceneReadStatus.last_read_post to legacy databases.

``Post.roll`` holds a dice command's outcome for the scene's roll strip; older
posts keep it null and show their message text. ``last_read_post`` places the
scene's unread divider. When the column is new, existing rows get a marker:
a read scene is read through its latest post, and an unread one through the
user's own latest post in it (they had read the scene when they wrote it).
"""

from django.db import migrations
from django.db.models import OuterRef, Subquery

from game.models import Post, UserSceneReadStatus

NEW_FIELDS = ((Post, "roll"), (UserSceneReadStatus, "last_read_post"))


def table_columns(schema_editor, model):
    with schema_editor.connection.cursor() as cursor:
        return {
            column.name
            for column in schema_editor.connection.introspection.get_table_description(
                cursor, model._meta.db_table
            )
        }


def backfill_read_markers(using):
    posts = Post.objects.using(using).filter(scene=OuterRef("scene")).order_by("-pk")
    statuses = UserSceneReadStatus.objects.using(using).filter(last_read_post__isnull=True)
    statuses.filter(read=True).update(last_read_post=Subquery(posts.values("pk")[:1]))
    own = posts.filter(character__owner=OuterRef("user"))
    statuses.filter(read=False).update(last_read_post=Subquery(own.values("pk")[:1]))


def add_scene_rolls_and_read_marker(apps, schema_editor):
    # ``game`` has no migration state on legacy installations, so its models
    # are intentionally absent from this migration's historical app registry.
    # Use the live models solely to describe the columns being added.
    added = set()
    for model, name in NEW_FIELDS:
        field = model._meta.get_field(name)
        # Test syncdb already creates these columns from the current models.
        # Existing deployments need the DDL exactly once.
        if field.column not in table_columns(schema_editor, model):
            schema_editor.add_field(model, field)
            added.add(name)
    if "last_read_post" in added:
        backfill_read_markers(schema_editor.connection.alias)


# The live model describes each column (legacy databases have no migration state for
# its app), so these fields must keep the definition they shipped with: a later
# change to one of them needs its own migration here, not an edit to this one.
# Reversing this migration leaves the columns in place (RunPython.noop).


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0003_discipline_property_names")]
    operations = [migrations.RunPython(add_scene_rolls_and_read_marker, migrations.RunPython.noop)]
