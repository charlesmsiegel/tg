"""Keep player-created reality zones private after their last place is removed.

Add sticky provenance and classify all currently linked zones. Independent staff
references stay public. No names or descriptions are rewritten, so staff edits
survive. Later model, field, table or column removal skips the corresponding work;
re-running only marks zones that are still unclassified. Reversing keeps the data.
"""

from django.db import migrations

from tg_schema.schema import add_missing_columns, live_field, live_model, table_columns, table_names


def protect_player_reality_zones(apps, schema_editor):
    zone_model = live_model("locations.RealityZone")
    marker = live_field(zone_model, "is_player_zone")
    if marker is None:
        return
    connection = schema_editor.connection
    tables = table_names(connection)
    if zone_model._meta.db_table not in tables:
        return
    add_missing_columns(schema_editor, "locations.RealityZone", ("is_player_zone",))
    using = connection.alias
    for relation in zone_model._meta.related_objects:
        field = relation.field
        if field.name != "reality_zone":
            continue
        table = field.model._meta.db_table
        if table not in tables or field.column not in table_columns(connection, table):
            continue
        linked = (
            relation.related_model.objects.using(using)
            .exclude(reality_zone_id=None)
            .values("reality_zone_id")
        )
        zone_model.objects.using(using).filter(pk__in=linked, is_player_zone=False).update(
            is_player_zone=True
        )


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0011_retire_custom_visibility")]
    operations = [migrations.RunPython(protect_player_reality_zones, migrations.RunPython.noop)]
