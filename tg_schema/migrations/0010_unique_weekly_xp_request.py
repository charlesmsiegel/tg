"""One weekly XP request per character and week.

A double submit could file two requests for the same character and week, after which
the profile's approval queue failed with MultipleObjectsReturned. For each duplicated
(week, character) pair this keeps one row, preferring an approved request (its XP has
been awarded) and then the oldest, and deletes the others: a pending duplicate claims
XP for a week that has a request already, and an approved duplicate's XP stays on the
character (only the record goes). Rows whose week or character is gone (NULL) are
left alone; the index treats NULLs as distinct. Then a unique index on
(week, character) is added unless the table already has a unique constraint on them
(a fresh database gets it from the model).

Self-contained SQL: the table and columns are named here, not taken from the live
model, so later model changes can't alter what this migration does.
"""

from django.db import migrations

from tg_schema.schema import table_columns, table_names

TABLE = "game_weeklyxprequest"
INDEX = "unique_weekly_xp_request"
COLUMNS = {"id", "week_id", "character_id", "approved"}


def has_unique_week_character(connection, cursor):
    constraints = connection.introspection.get_constraints(cursor, TABLE)
    return any(
        spec["unique"] and sorted(spec["columns"]) == ["character_id", "week_id"]
        for spec in constraints.values()
    )


def make_weekly_xp_request_unique(apps, schema_editor):
    connection = schema_editor.connection
    # A later release that renames the table or these columns owns them (see
    # tg_schema.schema): skip rather than fail every migrate.
    if TABLE not in table_names(connection) or not COLUMNS <= table_columns(connection, TABLE):
        return
    q = connection.ops.quote_name
    table, approved = q(TABLE), q("approved")
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT week_id, character_id FROM {table}"
            " WHERE week_id IS NOT NULL AND character_id IS NOT NULL"
            " GROUP BY week_id, character_id HAVING COUNT(*) > 1"
        )
        for week_id, character_id in cursor.fetchall():
            cursor.execute(
                f"SELECT id FROM {table} WHERE week_id = %s AND character_id = %s"
                f" ORDER BY {approved} DESC, id",
                [week_id, character_id],
            )
            keep = cursor.fetchone()[0]
            cursor.execute(
                f"DELETE FROM {table} WHERE week_id = %s AND character_id = %s AND id <> %s",
                [week_id, character_id, keep],
            )
        if not has_unique_week_character(connection, cursor):
            cursor.execute(f"CREATE UNIQUE INDEX {q(INDEX)} ON {table} (week_id, character_id)")


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0009_human_age_limits")]
    operations = [migrations.RunPython(make_weekly_xp_request_unique, migrations.RunPython.noop)]
