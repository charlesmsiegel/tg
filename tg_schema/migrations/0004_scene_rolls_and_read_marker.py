"""Add Post.roll and UserSceneReadStatus.last_read_post to legacy databases.

``Post.roll`` holds a dice command's outcome for the scene's roll strip; older
posts keep it null and show their message text. ``last_read_post`` places the
scene's unread divider. When the column is new, existing rows get a marker:
a read scene is read through its latest post, and an unread one through the
user's own latest post in it (they had read the scene when they wrote it).
"""

from django.db import migrations
from django.db.models import OuterRef, Subquery

from tg_schema.schema import add_missing_columns, live_model

NEW_FIELDS = (("game.Post", "roll"), ("game.UserSceneReadStatus", "last_read_post"))


def backfill_read_markers(using):
    Post, UserSceneReadStatus = live_model("game.Post"), live_model("game.UserSceneReadStatus")
    posts = Post.objects.using(using).filter(scene=OuterRef("scene")).order_by("-pk")
    statuses = UserSceneReadStatus.objects.using(using).filter(last_read_post__isnull=True)
    statuses.filter(read=True).update(last_read_post=Subquery(posts.values("pk")[:1]))
    own = posts.filter(character__owner=OuterRef("user"))
    statuses.filter(read=False).update(last_read_post=Subquery(own.values("pk")[:1]))


def add_scene_rolls_and_read_marker(apps, schema_editor):
    # ``game`` has no migration state on legacy installations: the live models
    # describe the columns (see tg_schema.schema).
    added = set()
    for label, name in NEW_FIELDS:
        added |= add_missing_columns(schema_editor, label, (name,))
    # The backfill runs only in the release that adds the column, whose models match.
    if "last_read_post" in added:
        backfill_read_markers(schema_editor.connection.alias)


# Reversing this migration leaves the columns in place (RunPython.noop).


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0003_discipline_property_names")]
    operations = [migrations.RunPython(add_scene_rolls_and_read_marker, migrations.RunPython.noop)]
