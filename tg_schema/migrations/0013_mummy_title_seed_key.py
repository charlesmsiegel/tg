"""Add nullable permanent identities to Mummy titles without rewriting existing rows.

The population command adopts unkeyed rows explicitly after migration. Reversing
keeps the column and unique index. Removed models, fields and tables are skipped.
"""

from django.db import migrations, models

from tg_schema.schema import live_field, live_model, table_columns, table_names


def add_mummy_title_seed_key(apps, schema_editor):
    model = live_model("characters.MummyTitle")
    field = live_field(model, "seed_key")
    if field is None:
        return
    connection = schema_editor.connection
    table = model._meta.db_table
    if table not in table_names(connection):
        return
    if field.column not in table_columns(connection, table):
        schema_editor.add_field(model, field)
    with connection.cursor() as cursor:
        constraints = connection.introspection.get_constraints(cursor, table)
        if any(
            spec["unique"] and spec["columns"] == [field.column] for spec in constraints.values()
        ):
            return
    # Use the declared constraint's name on fresh and patched databases alike.
    constraint = next(
        spec
        for spec in model._meta.constraints
        if isinstance(spec, models.UniqueConstraint) and spec.fields == ("seed_key",)
    )
    quote = connection.ops.quote_name
    schema_editor.execute(
        f"CREATE UNIQUE INDEX {quote(constraint.name)} ON {quote(table)} ({quote(field.column)})"
    )


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0012_protect_player_reality_zones")]
    operations = [migrations.RunPython(add_mummy_title_seed_key, migrations.RunPython.noop)]
