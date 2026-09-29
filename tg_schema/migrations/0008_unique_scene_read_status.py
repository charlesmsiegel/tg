"""One scene read status per user and scene.

Rows whose user or scene is gone are deleted (they now go with them: CASCADE).
Duplicate rows for a user and scene are merged into the oldest: read only if
every copy was, with the newest marker. Then a unique index on (user, scene) is
added unless the table already has a unique constraint on them (a fresh database
gets it from the model).

Self-contained SQL: the table and columns are named here, not taken from the live
model, so later model changes can't alter what this migration does.
"""

from django.db import migrations

from tg_schema.schema import table_names

TABLE = "game_userscenereadstatus"
INDEX = "unique_user_scene_read_status"


def has_unique_user_scene(connection, cursor):
    constraints = connection.introspection.get_constraints(cursor, TABLE)
    return any(
        spec["unique"] and sorted(spec["columns"]) == ["scene_id", "user_id"]
        for spec in constraints.values()
    )


def make_scene_read_status_unique(apps, schema_editor):
    connection = schema_editor.connection
    if TABLE not in table_names(connection):
        return
    q = connection.ops.quote_name
    table, read, marker = q(TABLE), q("read"), q("last_read_post_id")
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {table} WHERE user_id IS NULL OR scene_id IS NULL")
        cursor.execute(
            f"SELECT user_id, scene_id, MIN(id), MIN(CASE WHEN {read} THEN 1 ELSE 0 END),"
            f" MAX({marker}) FROM {table} GROUP BY user_id, scene_id HAVING COUNT(*) > 1"
        )
        for user_id, scene_id, keep, all_read, newest in cursor.fetchall():
            cursor.execute(
                f"UPDATE {table} SET {read} = %s, {marker} = %s WHERE id = %s",
                [bool(all_read), newest, keep],
            )
            cursor.execute(
                f"DELETE FROM {table} WHERE user_id = %s AND scene_id = %s AND id <> %s",
                [user_id, scene_id, keep],
            )
        if not has_unique_user_scene(connection, cursor):
            cursor.execute(f"CREATE UNIQUE INDEX {q(INDEX)} ON {table} (user_id, scene_id)")


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0007_assign_story_chronicles")]
    operations = [migrations.RunPython(make_scene_read_status_unique, migrations.RunPython.noop)]
